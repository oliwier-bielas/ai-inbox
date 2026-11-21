from fastapi import FastAPI
from app.email.router import router as email_router
from app.analysis.router import router as analysis_router
from app.core.exception_handlers import register_exception_handlers

app = FastAPI()

# routers
app.include_router(email_router)
app.include_router(analysis_router)

register_exception_handlers(app)
