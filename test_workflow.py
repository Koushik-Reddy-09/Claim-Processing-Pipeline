
from unittest.mock import patch
from app.workflow import claim_workflow

sample_pages = [
    {
        "page_number": 1,
        "text": "IDENTITY DOCUMENT\nName: Rahul Kumar\nID Number: ID123456"
    },
    {
        "page_number": 2,
        "text": (
            "DISCHARGE SUMMARY\n"
            "Date of Admission: 10 October 2026\n"
            "Date of Discharge: 15 October 2026\n"
            "Discharge Diagnosis: Viral Fever"
        )
    },
    {
        "page_number": 3,
        "text": (
            "ITEMIZED BILL\n"
            "Description of Service: Consultation\n"
            "Quantity: 1\nUnit Price: 500\nTotal Charges: 500"
        )
    },
]

def mock_classifier(text):
    if "IDENTITY DOCUMENT" in text:
        return {
            "document_type": "identity_document",
            "confidence": 0.95,
        }
    elif "DISCHARGE SUMMARY" in text:
        return {
            "document_type": "discharge_summary",
            "confidence": 0.95,
        }
    elif "ITEMIZED BILL" in text:
        return {
            "document_type": "itemized_bill",
            "confidence": 0.95,
        }
    return {"document_type": "other", "confidence": 0.0}

def mock_gemini(prompt):
    if "Classify this PDF page" in prompt:
         if "IDENTITY DOCUMENT" in prompt:
            return '{"document_type": "identity_document", "confidence": 0.95}'
         
         elif "DISCHARGE SUMMARY" in prompt:
            return '{"document_type": "discharge_summary", "confidence": 0.95}'
         elif "ITEMIZED BILL" in prompt:
            return '{"document_type": "itemized_bill", "confidence": 0.95}'
         return '{"document_type": "other", "confidence": 0.5}'
    if "hospital discharge summary" in prompt:
        return '{"patient_name": "Rahul Kumar", "admission_date": "10 October 2026", "discharge_date": "15 October 2026", "diagnosis": "Viral Fever"}'
    elif "identity" in prompt.lower():
        return '{"name": "Rahul Kumar", "document_type": "Identity Document", "document_number": "ID123456"}'
    else:
        return '{"description": "Consultation", "quantity": 1, "unit_price": 500, "total_charges": 500}'

with patch(
    "app.workflow.classify_document",
    side_effect=mock_classifier,
), patch(
    "app.workflow.ask_gemini",
    side_effect=mock_gemini,
):
    result = claim_workflow.invoke({
        "pages": sample_pages,
        "segregated_pages": [],
        "id_data": [],
        "discharge_data": [],
        "bill_data": [],
        "final_result": {},
    })

print("Workflow executed successfully!")
print(result["final_result"])
