
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.gemini_client import ask_gemini


class ClaimState(TypedDict):
    pages: list
    segregated_pages: list
    id_data: list
    discharge_data: list
    bill_data: list
    final_result: dict



from app.segregator import classify_document



def segregator_node(state: ClaimState):
    document_types = [
        "claim_forms",
        "cheque_or_bank_details",
        "identity_document",
        "itemized_bill",
        "discharge_summary",
        "prescription",
        "investigation_report",
        "cash_receipt",
        "other",
    ]

    segregated_pages = []

    for page in state["pages"]:
        prompt = f"""
Classify this PDF page into exactly ONE document type from this list:
{document_types}

Return only valid JSON in this format:
{{"document_type": "one_type_from_the_list", "confidence": 0.0}}

Do not invent information.
Page number: {page.get("page_number")}
Page text:
{page["text"][:4000]}

"""
        result = classify_document(page["text"])
        segregated_pages.append({
            **page,
            "classification": result,
        })

    return {"segregated_pages": segregated_pages}





def id_agent_node(state: ClaimState):
    id_pages = [
        page for page in state["segregated_pages"]
        if page["classification"]["document_type"] == "identity_document"
    ]

    id_data = []

    for page in id_pages:
        prompt = f"""
        Extract identity information from this document.
        Return only valid JSON with available fields such as:
        name, document_type, document_number, date_of_birth.

        Do not invent missing values.
        Document text:
        {page["text"][:5000]}
        """

        try:
            import re

            text = page["text"]
            data = {}

            name_match = re.search(
                r"Name\s*:\s*([^\n]+)", text, re.IGNORECASE
            )
            id_match = re.search(
                r"(?:ID Number|Aadhaar Number|Document Number)\s*:\s*([^\n]+)",
                text, re.IGNORECASE
            )

            data["name"] = name_match.group(1).strip() if name_match else None
            data["document_number"] = id_match.group(1).strip() if id_match else None
            data["document_type"] = "Identity Document"

            id_data.append({
                "page_number": page.get("page_number"),
                "data": data
            })

        except Exception as error:
            print("ID Agent error:", error)
            id_data.append({
                "page_number": page.get("page_number"),
                "data": {}
            })

    return {"id_data": id_data}


def discharge_agent_node(state: ClaimState):
    discharge_pages = [
        page for page in state["segregated_pages"]
        if page["classification"]["document_type"] == "discharge_summary"
    ]

    discharge_data = []

    for page in discharge_pages:
        prompt = f"""
        Extract information from this hospital discharge summary.
        Return only valid JSON with available fields such as:
        patient_name, admission_date, discharge_date,
        diagnosis, treatment, hospital_name.

        Do not invent missing values.

        Document text:
        {page["text"][:5000]}
        """

        try:
            import re

            text = page["text"]
            data = {}
            patterns = {
                "patient_name": r"Patient Name\s*:\s*([^\n]+)",
                "admission_date": r"Date of Admission\s*:\s*([^\n]+)",
                "discharge_date": r"Date of Discharge\s*:\s*([^\n]+)",
                "diagnosis": r"(?:Discharge Diagnosis|Diagnosis)\s*:\s*([^\n]+)",
            }

            for field, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                data[field] = match.group(1).strip() if match else None

            discharge_data.append({
                "page_number": page.get("page_number"),
                "data": data,
            })
        except Exception as error:
            print("Discharge Agent error:", error)
            discharge_data.append({
            "page_number": page.get("page_number"),
                "data": {},
            })

    return {"discharge_data": discharge_data}




def bill_agent_node(state: ClaimState):
    bill_pages = [
        page for page in state["segregated_pages"]
        if page["classification"]["document_type"] == "itemized_bill"
    ]

    bill_data = []

    for page in bill_pages:
        import re

        text = page["text"]
        data = {}
        patterns = {
            "description": r"Description of Service\s*:\s*([^\n]+)",
            "quantity": r"Quantity\s*:\s*(\d+)",
            "unit_price": r"Unit Price\s*:\s*([\d,.]+)",
            "total_charges": r"Total Charges\s*:\s*([\d,.]+)",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            value = match.group(1).strip() if match else None

            if field in ("quantity", "unit_price", "total_charges") and value:
                value = value.replace(",", "")
                value = int(value) if field == "quantity" else float(value)

            data[field] = value

        bill_data.append({
            "page_number": page.get("page_number"),
            "data": data,
        })

    return {"bill_data": bill_data}


def aggregator_node(state: ClaimState):
    return {
        "final_result": {
            "identity_documents": state["id_data"],
            "discharge_summaries": state["discharge_data"],
            "itemized_bills": state["bill_data"],
        }
    }



builder = StateGraph(ClaimState)

builder.add_node("AI Segregator Agent", segregator_node)
builder.add_node("ID Agent", id_agent_node)
builder.add_node("Discharge Summary Agent", discharge_agent_node)
builder.add_node("Itemized Bill Agent", bill_agent_node)
builder.add_node("Aggregator", aggregator_node)

builder.add_edge(START, "AI Segregator Agent")
builder.add_edge("AI Segregator Agent", "ID Agent")
builder.add_edge("AI Segregator Agent", "Discharge Summary Agent")
builder.add_edge("AI Segregator Agent", "Itemized Bill Agent")

builder.add_edge("ID Agent", "Aggregator")
builder.add_edge("Discharge Summary Agent", "Aggregator")
builder.add_edge("Itemized Bill Agent", "Aggregator")

builder.add_edge("Aggregator", END)

claim_workflow = builder.compile()
