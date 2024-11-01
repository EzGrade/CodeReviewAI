from fastapi import APIRouter
import logging

from starlette.responses import JSONResponse

from api.review.models import Review
from services.github_service import Github
from services.openai_service import OpenAi
from services.prompt_service import Prompt
from utils.ai_response import parse_review_text
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
    prompt_service = Prompt(
        assignment=assignment_description,
        files_content=github_service.get_repository_files(),
        candidate_level=candidate_level
    )
    openai_service = OpenAi(
        context=prompt_service.get_prompt()
    )
    response = parse_review_text(openai_service.get_response())
    return JSONResponse(content={"response": response})
