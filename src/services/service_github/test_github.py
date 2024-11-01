import pytest
from unittest.mock import MagicMock
from services.service_github.service import Github


@pytest.fixture
def mock_github_integration(mocker):
    mock_github_integration = mocker.patch('services.service_github.service.GithubIntegration')
    mock_github_integration_instance = mock_github_integration.return_value
    mock_github_integration_instance.get_installations.return_value = [
        MagicMock(id=123, get_repos=lambda: [MagicMock(owner=MagicMock(login='test_owner'))])
    ]
    return mock_github_integration_instance


@pytest.fixture
def mock_app_auth(mocker):
    return mocker.patch('services.service_github.service.Auth.AppAuth')


@pytest.fixture
def github(mock_github_integration, mock_app_auth):
    mock_github_for_installation = mock_github_integration.get_github_for_installation.return_value
    mock_repo = mock_github_for_installation.get_repo.return_value

    def mock_get_contents(path, ref):
        if path == "":
            return [
                MagicMock(type='file', path='file1.txt', decoded_content=b'content1'),
                MagicMock(type='dir', path='dir1')
            ]
        elif path == "dir1":
            return [
                MagicMock(type='file', path='dir1/file2.txt', decoded_content=b'content2')
            ]
        else:
            return []

    mock_repo.get_contents.side_effect = mock_get_contents

    return Github(owner='test_owner', repo='test_repo')


def test_get_installation_id(github):
    installation_id = github.get_installation_id('test_owner')
    assert installation_id == 123


def test_get_repository_files(github):
    files = github.get_repository_files()
    expected_files = {
        'file1.txt': 'content1',
        'dir1/file2.txt': 'content2'
    }
    assert files == expected_files
