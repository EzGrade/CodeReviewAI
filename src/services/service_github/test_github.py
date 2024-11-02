from unittest.mock import patch, MagicMock
import pytest
from services.service_github.service import Github


@pytest.fixture
def github_instance():
    with patch('services.service_github.service.RedisClient') as MockRedisClient, \
            patch('services.service_github.service.Auth') as MockAuth, \
            patch('services.service_github.service.GithubAPI') as MockGithubAPI:
        mock_redis_client = MockRedisClient.return_value
        mock_auth = MockAuth.Token.return_value
        mock_github_api = MockGithubAPI.return_value

        # Mock the repo object and get_repo behavior
        mock_repo = MagicMock()
        mock_repo.default_branch = 'main'
        mock_github_api.get_repo.return_value = mock_repo

        # Inject the mock API client directly to avoid actual network calls
        yield Github(owner='test_owner', repo='test_repo', github_api=mock_github_api)


def test_get_repository_files_from_cache(github_instance):
    """
    Test if the repository files are retrieved from the cache.
    """
    github_instance.redis_client.get.return_value = "{'file1.txt': 'content1', 'file2.txt': 'content2'}"

    files = github_instance.get_repository_files()

    assert files == {'file1.txt': 'content1', 'file2.txt': 'content2'}
    github_instance.redis_client.get.assert_called_once()
    github_instance.repository.get_contents.assert_not_called()


def test_get_repository_files_from_github(github_instance):
    """
    Test if the repository files are retrieved from GitHub when the cache is empty.
    """
    github_instance.redis_client.get.return_value = None
    mock_file = MagicMock()
    mock_file.type = 'file'
    mock_file.path = 'file1.txt'
    mock_file.decoded_content = b'content1'
    github_instance.repository.get_contents.return_value = [mock_file]

    files = github_instance.get_repository_files()

    assert files == {'file1.txt': 'content1'}
    github_instance.redis_client.get.assert_called_once()
    github_instance.repository.get_contents.assert_called_once_with('', ref='main')
    github_instance.redis_client.set.assert_called_once()
