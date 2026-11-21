from fastapi import FastAPI
from app.email.router import router as email_router
from app.core.exception_handlers import register_exception_handlers

app = FastAPI()

app.include_router(email_router)

register_exception_handlers(app)
