import pytest
from fastapi.testclient import TestClient
from Models.FinancialSummarizerV2Endpoint import app

client = TestClient(app)

@pytest.mark.parametrize("file_name, content_type, doc_type, expected_status", [
    ("test.csv", "text/csv", "credit", 200),
    ("test.json", "application/json", "bank", 200),
    ("test.txt", "text/plain", "asset", 200),
    ("test.pdf", "application/pdf", "profit_loss", 200),
    ("test.html", "text/html", "default", 200)
])
def test_summarize_endpoint_with_various_formats(file_name, content_type, doc_type, expected_status):
    file_path = f"./Models/PDF/{file_name}"
    with open(file_path, "rb") as file:
        response = client.post(
            "/summarize/",
            files={"file": (file_name, file, content_type)},
            data={"doc_type": doc_type}
        )
        print(response.content.decode())  # Make sure to decode bytes to string for clarity
    assert response.status_code == expected_status

# Test to ensure handling of unsupported file formats
def test_invalid_file_type():
    file_path = "./Models/PDF/unsupported_file_type.xyz"  # Ensure this points to a specific file
    try:
        with open(file_path, "rb") as file:
            response = client.post(
                "/summarize/",
                files={"file": ("unsupported_file_type.xyz", file, "application/octet-stream")}
            )
        assert response.status_code == 400
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except PermissionError:
        print(f"Permission denied for: {file_path}")
