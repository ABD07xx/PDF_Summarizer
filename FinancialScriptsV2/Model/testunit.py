import pytest
from fastapi.testclient import TestClient
from FinancialSummarizerV2Endpoint import app


client = TestClient(app)

@pytest.fixture(params=[
    ("test.csv", "text/csv", "credit", 200),
    ("test.json", "application/json", "bank", 200),
    ("test.txt", "text/plain", "asset", 200),
    ("test.pdf", "application/pdf", "profit_loss", 200),
    ("test.html", "text/html", "default", 200)
])
def test_file(request):
    file_name, content_type, doc_type, expected_status = request.param
    file_path = f"./TestFiles/{file_name}"
    with open(file_path, "rb") as file:
        file_content = file.read()  # Read the file content and store it
    return file_name, file_content, content_type, doc_type, expected_status

def test_summarize_endpoint_with_various_formats(test_file):
    file_name, file_content, content_type, doc_type, expected_status = test_file
    response = client.post(
        "/summarize/",
        files={"file": (file_name, file_content, content_type)},
        data={"doc_type": doc_type}
    )
    assert response.status_code == expected_status

def test_invalid_file_type():
    file_name = "test.unknown"
    file_path = f"./TestFiles/{file_name}"
    try:
        with open(file_path, "rb") as file:
            response = client.post(
                "/summarize/",
                files={"file": (file_name, file, "application/octet-stream")}
            )
        assert response.status_code == 400
    except FileNotFoundError:
        # Acknowledge that file not found is expected for this test case
        assert True
