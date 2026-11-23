from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.auth.service import require_capability
from app.models import User
from app.video_dramas import catalog
from app.video_dramas.schemas import DocumentDetail, DramaIndex, EpisodeDetail, SeriesKey

ContentReader = Annotated[User, Depends(require_capability("content.read"))]
router = APIRouter(prefix="/admin/video-dramas", tags=["admin-video-dramas"])


@router.get("", response_model=DramaIndex)
def get_dramas(_user: ContentReader) -> DramaIndex:
    return catalog.load_index()


@router.get("/{series}/episodes/{slug}", response_model=EpisodeDetail)
def get_episode(
    _user: ContentReader,
    series: SeriesKey,
    slug: Annotated[str, Path(max_length=80, pattern=r"^[a-z0-9-]+-e\d{3}(?:-r\d+)?$")],
) -> EpisodeDetail:
    return catalog.episode(series, slug)


@router.get("/{series}/documents/{doc_id}", response_model=DocumentDetail)
def get_document(
    _user: ContentReader,
    series: SeriesKey,
    doc_id: Annotated[str, Path(max_length=200, pattern=r"^[A-Za-z0-9_-]+$")],
) -> DocumentDetail:
    return catalog.document(series, doc_id)
