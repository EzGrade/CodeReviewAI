import re
import logger

logger = logger.get_logger(__name__)


def extract_repo_from_url(repo_url: str) -> tuple:
    """
    Extract owner and repo from GitHub repository URL
    :param repo_url:
    :return:
    """
    logger.debug(f"Extracting owner and repo from URL: {repo_url}")
    pattern = r'github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+)'
    match = re.search(pattern, repo_url)
    if match:
        owner = match.group('owner')
        repo = match.group('repo')
        logger.debug(f"Extracted owner: {owner}, repo: {repo}")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub repository URL")
