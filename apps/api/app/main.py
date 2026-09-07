from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.admin.dashboard_router import router as admin_dashboard_router
from app.admin.router import router as admin_router
from app.admin.router import runtime_router
from app.admin.user_router import router as admin_user_router
from app.affiliates.router import router as affiliates_router
from app.ai.router import router as ai_router
from app.alerts.router import router as alerts_router
from app.analytics.router import admin_router as admin_analytics_router
from app.analytics.router import router as analytics_router
from app.auth.router import router as auth_router
from app.config import get_settings
from app.crawlers.router import router as crawlers_router
from app.db import engine
from app.deployments.router import router as deployments_router
from app.flights.router import router as flight_status_router
from app.foods.admin_router import router as admin_foods_router
from app.foods.router import router as foods_router
from app.fx.router import router as fx_router
from app.holidays.router import router as holidays_router
from app.hotspots.admin_router import router as admin_hotspots_router
from app.hotspots.router import router as hotspots_router
from app.infra import get_redis
from app.line.router import router as line_router
from app.middleware import RequestBodyLimitMiddleware, RequestContextMiddleware
from app.places.router import public_router as public_places_router
from app.places.router import router as places_router
from app.problems import AppError, app_error_handler, validation_error_handler
from app.providers.flight_router import router as flight_router
from app.providers.router import router as providers_router
from app.restaurants.admin_router import router as admin_restaurants_router
from app.restaurants.admin_sources_router import router as admin_restaurant_sources_router
from app.restaurants.router import router as restaurants_router
from app.restaurants.user_router import router as restaurant_user_router
from app.saved.router import router as saved_items_router
from app.schema import expected_schema_revision, schema_is_current
from app.search.router import router as search_router
from app.trips.export_router import router as trip_export_router
from app.trips.ingest_router import router as trip_places_router
from app.trips.intents import router as trip_intents_router
from app.trips.router import public_router as public_trips_router
from app.trips.router import router as trips_router
from app.trips.share_router import router as trip_share_router
from app.trips.stay_router import router as trip_stay_router
from app.ui_text.router import admin_router as admin_ui_text_router
from app.ui_text.router import runtime_router as ui_text_runtime_router
from app.usage.router import admin_router as admin_usage_router
from app.usage.router import router as usage_router

settings = get_settings()
settings.validate_api_serving_security()
app = FastAPI(
    title="Mokaair API",
    version="0.1.0",
    docs_url=None if settings.production else "/docs",
    redoc_url=None if settings.production else "/redoc",
    openapi_url=None if settings.production else "/openapi.json",
)
app.add_middleware(RequestBodyLimitMiddleware, max_bytes=settings.api_max_request_bytes)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(admin_dashboard_router, prefix="/api/v1")
app.include_router(admin_user_router, prefix="/api/v1")
app.include_router(deployments_router, prefix="/api/v1")
app.include_router(runtime_router, prefix="/api/v1")
app.include_router(ui_text_runtime_router, prefix="/api/v1")
app.include_router(admin_ui_text_router, prefix="/api/v1")
app.include_router(affiliates_router, prefix="/api/v1")
app.include_router(usage_router, prefix="/api/v1")
app.include_router(admin_usage_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(flight_status_router, prefix="/api/v1")
app.include_router(trips_router, prefix="/api/v1")
app.include_router(trip_intents_router, prefix="/api/v1")
app.include_router(trip_stay_router, prefix="/api/v1")
app.include_router(trip_export_router, prefix="/api/v1")
app.include_router(trip_share_router, prefix="/api/v1")
app.include_router(trip_places_router, prefix="/api/v1")
app.include_router(public_trips_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(admin_analytics_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(places_router, prefix="/api/v1")
app.include_router(fx_router, prefix="/api/v1")
app.include_router(holidays_router, prefix="/api/v1")
app.include_router(public_places_router, prefix="/api/v1")
app.include_router(providers_router, prefix="/api/v1")
app.include_router(flight_router, prefix="/api/v1")
app.include_router(crawlers_router, prefix="/api/v1")
app.include_router(hotspots_router, prefix="/api/v1")
app.include_router(admin_hotspots_router, prefix="/api/v1")
app.include_router(restaurants_router, prefix="/api/v1")
app.include_router(restaurant_user_router, prefix="/api/v1")
app.include_router(saved_items_router, prefix="/api/v1")
app.include_router(admin_restaurants_router, prefix="/api/v1")
app.include_router(admin_restaurant_sources_router, prefix="/api/v1")
app.include_router(foods_router, prefix="/api/v1")
app.include_router(admin_foods_router, prefix="/api/v1")
app.include_router(line_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
async def ready() -> dict[str, str]:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
            current_revision = await connection.scalar(
                text("SELECT version_num FROM alembic_version")
            )
            if not schema_is_current(current_revision):
                raise RuntimeError(
                    "Database schema is not current: "
                    f"expected {expected_schema_revision()}, found {current_revision or 'none'}"
                )
        await get_redis().ping()
    except Exception as exc:
        raise AppError(
            503,
            "dependencies_unavailable",
            "資料庫、資料結構或 Redis 目前無法使用",
        ) from exc
    return {
        "status": "ready",
        "database": "ok",
        "redis": "ok",
        "schema": str(current_revision),
    }
