
DOCUMENT_TYPES = [
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


def classify_document(text: str) -> dict:
    text_lower = text.lower()

    keywords = {
        "claim_forms": [
            "claim form", "insurance claim", "claim number",
            "policy number", "claimant"
        ],
        "cheque_or_bank_details": [
            "bank account", "account number", "ifsc",
            "cancelled cheque", "bank details"
        ],
        "identity_document": [
            "identity document", "aadhaar", "passport",
            "voter id", "identity number"
        ],
        "itemized_bill": [
            "itemized bill", "itemised bill", "total charges",
            "unit price", "quantity", "bill amount"
        ],
        "discharge_summary": [
            "discharge summary", "date of discharge",
            "discharge diagnosis", "date of admission"
        ],
        "prescription": [
            "prescription", "prescribed medicines",
            "dosage", "tablet"
        ],
        "investigation_report": [
            "investigation report", "laboratory report",
            "test results", "haemoglobin", "hemoglobin"
        ],
        "cash_receipt": [
            "cash receipt", "payment received",
            "receipt number", "amount paid"
        ],
    }

    scores = {
        category: sum(
            1 for keyword in words if keyword in text_lower
        )
        for category, words in keywords.items()
    }

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return {
            "document_type": "other",
            "confidence": 0.0
        }

    return {
        "document_type": best_category,
        "confidence": round(
            scores[best_category] / len(keywords[best_category]), 2
        )
    }
