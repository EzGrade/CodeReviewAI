"""
Views for the review endpoint
"""

import logging
from fastapi import APIRouter

from openai import BadRequestError
from starlette.responses import JSONResponse

from api.review.models import Review
from services.service_github.service import Github
from services.service_openai.service import OpenAi
from services.service_prompt.service import Prompt
from utils.util_ai.ai_response import parse_review_text
from utils.util_url.url import extract_repo_from_url

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(path="/review")
async def review(request: Review):
    """
    Review POST endpoint
    :param request:
    :return:
    """
    logger.debug(
        "Review request: %s",
        request
    )
    assignment_description = request.assignment_description
    repo_owner, repo_name = extract_repo_from_url(request.github_repo_url)
    candidate_level = request.candidate_level
    force_reload_files = request.repository_force_reload_files

    try:
        github_service = Github(
            owner=repo_owner,
            repo=repo_name,
            force_reload=force_reload_files
        )
    except ValueError as e:
        logger.error(
            "Invalid GitHub repository URL: %s",
            e
        )
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid GitHub repository URL"}
        )
    files = github_service.get_repository_files()
    prompt_service = Prompt(
        assignment=assignment_description,
        files_content=files,
        candidate_level=candidate_level
    )
    openai_service = OpenAi(
        context=prompt_service.get_prompt()
    )
    try:
        openai_response = openai_service.get_response()
    except BadRequestError as e:
        logger.error(
            "OpenAI request error: %s",
            e
        )
        return JSONResponse(
            status_code=400,
            content={
                "detail": e.message
            }
        )

    response = {
        "found_files": len(files),
    }
    response.update(parse_review_text(openai_response))
    return JSONResponse(
        status_code=200,
        content={
            "response": response
        }
    )
