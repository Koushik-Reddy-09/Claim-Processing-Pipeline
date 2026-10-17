from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.pdf_utils import extract_pages
from app.segregator import classify_document
from app.data_extracted import extract_claim_data
from app.validator import validate_claim
from app.workflow import claim_workflow
app = FastAPI(
    title="Claim Processing Pipeline",
    description="API for processing PDF insurance claims",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    pdf_bytes = await file.read()

    if not pdf_bytes.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file.",
        )

    try:
        pages = extract_pages(pdf_bytes)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
    result = claim_workflow.invoke({
    "pages": pages,
    "segregated_pages": [],
    "id_data": [],
    "discharge_data": [],
    "bill_data": [],
    "final_result": {},
})

    return JSONResponse(
    content={
        "claim_id": claim_id,
        "page_count": len(pages),
        "pages": result["segregated_pages"],
        "extracted_data": result["final_result"],
    }
)

