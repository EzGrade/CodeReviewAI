import re


def extract_repo_from_url(repo_url: str) -> tuple:
    pattern = r'github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+)'
    match = re.search(pattern, repo_url)
    if match:
        return match.group('owner'), match.group('repo')
    else:
        raise ValueError("Invalid GitHub repository URL")
