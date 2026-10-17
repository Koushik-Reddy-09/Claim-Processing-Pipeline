Medical Claim Processing Pipeline

Overview:

A Python-based medical insurance claim processing system that accepts PDF claim documents, extracts page text, classifies document types, and extracts information using a LangGraph workflow.

Features:

1.PDF upload through a FastAPI endpoint.

2.Text extraction from PDF pages using PyMuPDF.

3.Classification into nine document categories.

4.LangGraph workflow with three extraction agents:
     .Identity Document Agent
     .Discharge Summary Agent
     .Itemized Bill Agent

5.Aggregation of extracted data into JSON output.

6.Local keyword-based classification and pattern-based extraction.

Technology Stack:

Python
FastAPI and Uvicorn
LangGraph
PyMuPDF
Pydantic
Python-dotenv

Project Structure:

Claim-Processing-pipeline/
├── app/
│   ├── main.py
│   ├── workflow.py
│   ├── segregator.py
│   ├── pdf_utils.py
│   ├── data_extracted.py
│   ├── validator.py
│   └── gemini_client.py
├── test_workflow.py
├── requirements.txt
├── .env.example
└── README.md

Setup
1.Install Python 3.11 or later.

2.Create and activate a virtual environment.

3.Install dependencies:

           pip install -r requirements.txt

Run the Application:

Start the FastAPI server:

             uvicorn app.main:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs

Use POST /api/process to upload a PDF and provide a claim ID.

Run the Workflow Test: 

        python test_workflow.py

Current Limitations:
Document classification uses keyword matching, and extraction uses regular expressions. Results may vary depending on document formatting and wording. Identity, discharge summary, and itemized bill extraction support common field labels rather than every possible document format.