from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.auth.service import require_capability
from app.models import User
from app.video_pools import catalog
from app.video_pools.schemas import (
    ExpansionPage,
    PoolOverview,
    SeriesKey,
    ThemeDetail,
    ThemePage,
    ThemeSort,
    ThemeStatus,
)

ContentReader = Annotated[User, Depends(require_capability("content.read"))]
router = APIRouter(prefix="/admin/video-pools", tags=["admin-video-pools"])


@router.get("", response_model=PoolOverview)
def get_pools(_user: ContentReader) -> PoolOverview:
    return catalog.overview()


@router.get("/{series}/themes", response_model=ThemePage)
def get_themes(
    _user: ContentReader,
    series: SeriesKey,
    status: Annotated[ThemeStatus, Query()] = "producible",
    category: Annotated[str | None, Query(max_length=100)] = None,
    min_score: Annotated[float | None, Query(ge=1, le=10)] = None,
    q: Annotated[str | None, Query(max_length=200)] = None,
    sort: Annotated[ThemeSort, Query()] = "rank",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
) -> ThemePage:
    return catalog.list_themes(
        series,
        status=status,
        category=category,
        min_score=min_score,
        q=q,
        sort=sort,
        page=page,
        page_size=page_size,
    )


@router.get("/{series}/themes/{theme_id}", response_model=ThemeDetail)
def get_theme(
    _user: ContentReader,
    series: SeriesKey,
    theme_id: Annotated[str, Path(max_length=40, pattern=r"^[A-Za-z0-9_-]+$")],
) -> ThemeDetail:
    return catalog.theme_detail(series, theme_id)


@router.get("/{series}/expansions", response_model=ExpansionPage)
def get_expansions(_user: ContentReader, series: SeriesKey) -> ExpansionPage:
    return catalog.expansions(series)
