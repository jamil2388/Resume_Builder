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

# Note: We are not testing a successful /tailor-resume call here 
# because it would require a real Gemini API Key and pdflatex installation.
# In a real TDD environment, we would 'mock' the resume_tailoring function.
