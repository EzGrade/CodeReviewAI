import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def review_data():
    return {
        "assignment_description": "Test assignment",
        "github_repo_url": "https://github.com/test_owner/test_repo",
        "candidate_level": "junior"
    }


def test_review_endpoint_valid_data(review_data, mocker):
    mocker.patch('services.service_github.service.Github.__init__', return_value=None)
    mocker.patch('services.service_github.service.Github.get_repository_files', return_value=["file1.py", "file2.py"])
    mocker.patch('services.service_prompt.service.Prompt.get_prompt', return_value="Test prompt")
    mocker.patch('services.service_openai.service.OpenAi.get_response', return_value="Test response")

    response = client.post("/review", json=review_data)
    assert response.status_code == 200
    assert response.json() == {"response": {'found_files': 2, 'raw_text': 'Test response'}}


def test_review_endpoint_invalid_url(mocker):
    review_data = {
        "assignment_description": "Test assignment",
        "github_repo_url": "https://github.com/invalid_owner/invalid_repo",
        "candidate_level": "junior"
    }

    response = client.post("/review", json=review_data)
    assert response.status_code == 422


def test_review_endpoint_missing_fields():
    review_data = {
        "assignment_description": "Test assignment",
        "github_repo_url": "https://github.com/test_owner/test_repo"
    }

    response = client.post("/review", json=review_data)
    assert response.status_code == 422
