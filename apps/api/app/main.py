from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.ai.router import router as ai_router
from app.alerts.router import router as alerts_router
from app.auth.router import router as auth_router
from app.config import get_settings
from app.db import engine
from app.infra import get_redis
from app.middleware import RequestContextMiddleware
from app.places.router import router as places_router
from app.problems import AppError, app_error_handler
from app.search.router import router as search_router
from app.trips.router import router as trips_router
from app.usage.router import router as usage_router

settings = get_settings()
app = FastAPI(title="Travel Scanner API", version="0.1.0")
app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
app.include_router(auth_router, prefix="/api/v1")
app.include_router(usage_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(trips_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(places_router, prefix="/api/v1")


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
