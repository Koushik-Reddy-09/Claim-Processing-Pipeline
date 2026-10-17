
from app.data_extracted import extract_claim_data

sample_text = """
Claim Reference: CLM-2024-789456
Patient Name: John Michael Smith
Date of Birth: March 15, 1985
Policy Number: POL-987654321
Provider Name: Dr. Sarah Johnson, MD
Date of Service: January 10, 2025
Diagnosis: Acute Bronchitis (ICD-10: J20.9)
Total Amount Claimed: $450.00
"""

result = extract_claim_data(sample_text)

for field, value in result.items():
    print(f"{field}: {value}")
