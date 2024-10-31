from fastapi import APIRouter
from api.review.models import Review
from services.github_service import Github
from utils.url import extract_repo_from_url

router = APIRouter()


@router.post(path="/review")
async def review(request: Review):
    assignment_description = request.assignment_description
    repo_owner, repo_name = extract_repo_from_url(request.github_repo_url)
    candidate_level = request.candidate_level

    github_service = Github(
        owner=repo_owner,
        repo=repo_name,
    )
