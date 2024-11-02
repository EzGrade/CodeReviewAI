"""
Unit tests for the url module.
"""

import pytest
from url import extract_repo_from_url


def test_valid_url_with_https():
    """
    Test extract_repo_from_url function with valid URL containing HTTPS
    :return:
    """
    url = "https://github.com/test_owner/test_repo"
    expected_result = ("test_owner", "test_repo")
    result = extract_repo_from_url(url)
    assert result == expected_result


def test_valid_url_with_ssh():
    """
    Test extract_repo_from_url function with valid URL containing SSH
    :return:
    """
    url = "git@github.com:test_owner/test_repo.git"
    expected_result = ("test_owner", "test_repo")
    result = extract_repo_from_url(url)
    assert result == expected_result


def test_invalid_url():
    """
    Test extract_repo_from_url function with invalid URL
    :return:
    """
    url = "https://invalid_url.com/test_owner/test_repo"
    with pytest.raises(ValueError):
        extract_repo_from_url(url)


def test_url_without_owner_or_repo():
    """
    Test extract_repo_from_url function with URL missing owner or repo
    :return:
    """
    url = "https://github.com/"
    with pytest.raises(ValueError):
        extract_repo_from_url(url)


def test_url_with_branch():
    """
    Test extract_repo_from_url function with URL containing branch
    :return:
    """
    url = "https://github.com/test_owner/test_repo/tree/feat/main"
    expected_result = ("test_owner", "test_repo")
    result = extract_repo_from_url(url)
    assert result == expected_result
