"""
Tests for the review endpoint
"""

import pytest
from fastapi.testclient import TestClient
from github import UnknownObjectException

from main import app
import github

client = TestClient(app)


@pytest.fixture
def review_data():
    """
    Review data fixture
    :return:
    """
    return {
        "assignment_description": "Test assignment",
        "github_repo_url": "https://github.com/test_owner/test_repo",
        "candidate_level": "junior"
    }


def test_review_endpoint_valid_data(review_data, mocker):
    """
    Test review endpoint with valid data
    :param review_data:
    :param mocker:
    :return:
    """
    mocker.patch(
        'services.service_github.service.Github.__init__',
        return_value=None
    )
    mocker.patch(
        'services.service_github.service.Github.get_repository_files',
        return_value=["file1.py", "file2.py"]
    )
    mocker.patch(
        'services.service_prompt.service.Prompt.get_prompt',
        return_value="Test prompt"
    )
    mocker.patch(
        'services.service_openai.service.OpenAi.get_response',
        return_value="Test response"
    )

    response = client.post("/review", json=review_data)
    assert response.status_code == 200
    assert response.json() == {"response": {'found_files': 2, 'raw_text': 'Test response'}}


def test_review_endpoint_missing_fields():
    """
    Test review endpoint with missing fields
    :return:
    """
    review_data = {
        "assignment_description": "Test assignment",
        "github_repo_url": "https://github.com/test_owner/test_repo"
    }

    response = client.post("/review", json=review_data)
    assert response.status_code == 422


@pytest.fixture
def invalid_repo_url_payload():
    return {
        "assignment_description": "Test assignment",
        "github_repo_url": "https://github.com/invalid/repo",
        "candidate_level": "junior",
        "repository_force_reload_files": False
    }


def test_invalid_repo_url(invalid_repo_url_payload, mocker):
    # Mock the GitHub class to raise UnknownObjectException
    mocker.patch(
        "services.service_github.service.Github.get_repository",
        side_effect=UnknownObjectException(404, "Not Found", None)
    )

    response = client.post("/review", json=invalid_repo_url_payload)
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid GitHub repository URL"}
