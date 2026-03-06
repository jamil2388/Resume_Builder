import pytest
from fastapi.testclient import TestClient
from api import app
import os

client = TestClient(app)

def test_read_main():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_tailor_resume_missing_params():
    """Test missing parameters returns 400."""
    # Test JSON missing body
    response = client.post("/tailor-resume", json={})
    assert response.status_code == 400
    
    # Test Form missing fields
    response = client.post("/tailor-resume", data={})
    assert response.status_code == 400

def test_unsupported_media_type():
    """Test that sending plain text returns 415."""
    response = client.post("/tailor-resume", content="Just some text")
    assert response.status_code == 415

def test_tailor_resume_multipart_form():
    """Test that multipart form data is accepted."""
    response = client.post(
        "/tailor-resume",
        data={"job_position": "ML", "job_description": "Test description"}
    )
    # It might still return 500 if the underlying tailoring fails, 
    # but we want to ensure it doesn't return 415 or 422.
    assert response.status_code != 415
    assert response.status_code != 422

def test_tailor_resume_file_upload():
    """Test that file upload is accepted."""
    from io import BytesIO
    file_content = b"Mock job description"
    file = {"description_file": ("job.txt", BytesIO(file_content), "text/plain")}
    response = client.post(
        "/tailor-resume",
        data={"job_position": "ML"},
        files=file
    )
    assert response.status_code != 415
    assert response.status_code != 422
