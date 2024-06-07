import pytest
from fastapi.testclient import TestClient
from PDFSummarizerFinancialEndpoint import app

client = TestClient(app)

def test_summarize_pdf_endpoint():
    pdf_path = "../PDF/Plaid_Asset_Report.pdf"  # Replace with the path to your test PDF file
    with open(pdf_path, "rb") as pdf_file:
        response = client.post(
            "/summarize/",
            files={"file": ("sample.pdf", pdf_file, "application/pdf")}
        )

    assert response.status_code == 200
    json_response = response.json()
    assert "summary" in json_response
    assert isinstance(json_response["summary"], str)

def test_invalid_file_type():
    text_path = "../requirements.txt"  # Replace with the path to your test non-pdf file
    with open(text_path, "rb") as text_file:
        response = client.post(
            "/summarize/",
            files={"file": ("text_file.txt", text_file, "text/plain")}
        )

    assert response.status_code == 400
    json_response = response.json()
    assert json_response["detail"] == "File must be a PDF."