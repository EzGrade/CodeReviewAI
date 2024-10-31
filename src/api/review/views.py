from fastapi import APIRouter
import logging

from starlette.responses import JSONResponse

from api.review.models import Review
from services.github_service import Github
from utils.url import extract_repo_from_url

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(path="/review")
async def review(request: Review):
    logger.debug(f"Review request: {request}")
    assignment_description = request.assignment_description
    repo_owner, repo_name = extract_repo_from_url(request.github_repo_url)
    candidate_level = request.candidate_level

    github_service = Github(
        owner=repo_owner,
        repo=repo_name,
    )
    return JSONResponse(content={"message": github_service.get_repository_files()})
