from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.auth.service import require_capability
from app.models import User
from app.video_plans.catalog import list_plans
from app.video_plans.schemas import PlanCatalog, PlanPage, PlanStage

ContentReader = Annotated[User, Depends(require_capability("content.read"))]
router = APIRouter(prefix="/admin/video-plans", tags=["admin-video-plans"])


@router.get("", response_model=PlanPage)
def get_video_plans(
    _user: ContentReader,
    q: Annotated[str | None, Query(max_length=200)] = None,
    catalog: Annotated[PlanCatalog | None, Query()] = None,
    stage: Annotated[PlanStage | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
) -> PlanPage:
    return list_plans(q=q, catalog=catalog, stage=stage, page=page, page_size=page_size)
