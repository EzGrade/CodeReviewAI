import pytest
from utils.util_url.url import extract_repo_from_url


def test_valid_url_with_https():
    url = "https://github.com/test_owner/test_repo"
    expected_result = ("test_owner", "test_repo")
    result = extract_repo_from_url(url)
    assert result == expected_result


def test_valid_url_with_ssh():
    url = "git@github.com:test_owner/test_repo.git"
    expected_result = ("test_owner", "test_repo")
    result = extract_repo_from_url(url)
    assert result == expected_result


def test_invalid_url():
    url = "https://invalid_url.com/test_owner/test_repo"
    with pytest.raises(ValueError):
        extract_repo_from_url(url)


def test_url_without_owner_or_repo():
    url = "https://github.com/"
    with pytest.raises(ValueError):
        extract_repo_from_url(url)


def test_url_with_branch():
    url = "https://github.com/test_owner/test_repo/tree/feat/main"
    expected_result = ("test_owner", "test_repo")
    result = extract_repo_from_url(url)
    assert result == expected_result
