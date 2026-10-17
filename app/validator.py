
REQUIRED_DOCUMENTS = [
    "claim_form",
    "bank_statement",
    "government_id",
    "prescription",
    "lab_report",
    "medical_bill",
]


def validate_claim(pages: list, extracted_data: dict) -> dict:
    issues = []

    # Check for missing document types
    found_types = {
        page.get("classification", {}).get("document_type")
        for page in pages
    }

    for document in REQUIRED_DOCUMENTS:
        if document not in found_types:
            issues.append({
                "type": "missing_document",
                "document": document,
                "message": f"Required document missing: {document}",
            })

    # Check required claim fields
    required_fields = [
        "claim_reference",
        "patient_name",
        "policy_number",
        "date_of_service",
        "diagnosis",
        "total_amount_claimed",
    ]

    for field in required_fields:
        if not extracted_data.get(field):
            issues.append({
                "type": "missing_field",
                "field": field,
                "message": f"Claim field missing: {field}",
            })

    return {
        "validation_status": (
            "review_required" if issues else "passed"
        ),
        "issue_count": len(issues),
        "issues": issues,
    }
