from fastapi import FastAPI
from api.review.views import router
app = FastAPI()
app.include_router(router)
