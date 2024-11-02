"""
Utility functions for URL manipulation
"""

import re
import logger

logger = logger.get_logger(__name__)


def extract_repo_from_url(repo_url: str) -> tuple:
    """
    Extract owner, repo, and optionally branch from GitHub repository URL
    :param repo_url: GitHub repository URL
    :return: tuple containing owner and repo
    """
    logger.debug(
        "Extracting owner and repo from URL: %s",
        repo_url
    )

    pattern = r'(?:https://github\.com/|git@github\.com:)(?P<owner>[^/]+)/(?P<repo>[^/.]+)'
    match = re.search(pattern, repo_url)

    if match:
        owner = match.group('owner')
        repo = match.group('repo')
        logger.debug("Extracted owner: %s, repo: %s", owner, repo)
        return owner, repo

    raise ValueError("Invalid GitHub repository URL")
