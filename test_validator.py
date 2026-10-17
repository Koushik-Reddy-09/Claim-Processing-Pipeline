print("Validator test started")
from app.validator import validate_claim

sample_pages = [
    {
        "classification": {
            "document_type": "claim_form"
        }
    },
    {
        "classification": {
            "document_type": "bank_statement"
        }
    },
]

sample_claim = {
    "claim_reference": "CLM-2024-789456",
    "patient_name": "John Michael Smith",
    "policy_number": "POL-987654321",
    "date_of_service": "January 10, 2025",
    "diagnosis": "Acute Bronchitis",
    "total_amount_claimed": "450.00",
}

result = validate_claim(sample_pages, sample_claim)
print(result)
print("Validator test finished")
