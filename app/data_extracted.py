
import re
from typing import Optional


def extract_field(pattern: str, text: str) -> Optional[str]:
    """Extract the first matching field using a regular expression."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_claim_data(text: str) -> dict:
    """Extract basic structured fields from a claim document."""

    return {
        "claim_reference": extract_field(
            r"Claim Reference:\s*([A-Z0-9-]+)", text
        ),
        "patient_name": extract_field(
            r"Patient Name:\s*([A-Za-z ]+?)(?=\s*(?:Date of Birth:|DOB:|Age:|$))",
            text,
        ),
        "date_of_birth": extract_field(
            r"(?:Date of Birth|DOB):\s*([A-Za-z0-9, /-]+?)(?=\s*(?:Policy Number:|Age:|Gender:|$))",
            text,
        ),
        "policy_number": extract_field(
            r"Policy Number:\s*([A-Z0-9-]+)", text
        ),
        "provider_name": extract_field(
            r"Provider Name:\s*(.*?)(?=\s*(?:Hospital/Clinic:|Date of Service:|$))",
            text,
        ),
        "date_of_service": extract_field(
            r"Date of Service:\s*([A-Za-z0-9, /-]+?)(?=\s*(?:Provider Name:|Hospital/Clinic:|Diagnosis:|$))",
            text,
        ),
        "diagnosis": extract_field(
            r"Diagnosis:\s*(.*?)(?=\s*(?:Treatment Provided:|Total Amount Claimed:|$))",
            text,
        ),
        "total_amount_claimed": extract_field(
            r"Total Amount Claimed:\s*\$?\s*([\d,]+(?:\.\d{1,2})?)",
            text,
        ),
    }
