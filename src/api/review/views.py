from fastapi import APIRouter
from api.review.models import Review

router = APIRouter()


@router.post(path="/review")
async def review(request: Review):
    return request.model_dump()
