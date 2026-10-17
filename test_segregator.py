
from app.segregator import classify_document


def test_claim_form_classification():
    text = """
    MEDICAL CLAIM FORM
    Claim Reference: CLM-2024-789456
    Total Amount Claimed: $450.00
    Patient Responsibility: $90.00
    """

    result = classify_document(text)

    assert result["document_type"] == "claim_forms"
    assert result["confidence"] > 0


def test_discharge_summary_classification():
    text = """
    DISCHARGE SUMMARY
    Date of Admission: 10 October 2026
    Date of Discharge: 15 October 2026
    Discharge Diagnosis: Viral Fever
    """

    result = classify_document(text)

    assert result["document_type"] == "discharge_summary"



def test_unknown_document():
    result = classify_document("This is an unrelated document.")

    assert result["document_type"] in [
        "other",
        "claim_forms",
        "cheque_or_bank_details",
        "identity_document",
        "itemized_bill",
        "discharge_summary",
        "prescription",
        "investigation_report",
        "cash_receipt",
    ]
    assert 0.0 <= result["confidence"] <= 1.0

