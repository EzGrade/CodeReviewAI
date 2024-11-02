"""
This file is used to include all the routers in the application.
"""

from fastapi import FastAPI
from api.review.views import router
app = FastAPI()
app.include_router(router)
