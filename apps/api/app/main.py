from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy import text

from app.config import get_settings
from app.db import engine
from app.infra import get_redis
from app.middleware import RequestContextMiddleware
from app.problems import AppError, app_error_handler

settings = get_settings()
app = FastAPI(title="Travel Scanner API", version="0.1.0", default_response_class=ORJSONResponse)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
async def ready() -> dict[str, str]:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        await get_redis().ping()
    except Exception as exc:
        raise AppError(503, "dependencies_unavailable", "Database or Redis is unavailable") from exc
    return {"status": "ready", "database": "ok", "redis": "ok"}

