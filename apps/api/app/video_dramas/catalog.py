from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from pydantic import ValidationError

from app.problems import AppError
from app.video_dramas.schemas import (
    DocKind,
    DocumentDetail,
    DramaIndex,
    EpisodeDetail,
    EpisodeText,
    SeriesContent,
    SeriesIndex,
    SeriesKey,
)

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent / "data"
MAX_FILE_BYTES = 16 * 1024 * 1024
DOC_ORDER: tuple[DocKind, ...] = ("brief", "script", "storyboard", "review")


def _unavailable(exc: Exception) -> AppError:
    logger.error("Packaged AI drama scripts are unavailable (%s)", type(exc).__name__)
    return AppError(503, "video_dramas_unavailable", "劇本資料包缺漏或驗證失敗，請檢查部署版本")


def _read(name: str) -> bytes:
    with (DATA_DIR / name).open("rb") as source:
        content = source.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise ValueError("drama bundle file exceeds the packaged size limit")
    return content


def load_index() -> DramaIndex:
    """Read the image's immutable script index; repository files are never read at runtime."""
    try:
        return DramaIndex.model_validate_json(_read("index.json"))
    except (OSError, ValueError, ValidationError) as exc:
        raise _unavailable(exc) from exc


def _series(index: DramaIndex, key: SeriesKey) -> SeriesIndex:
    for series in index.series:
        if series.key == key:
            return series
    raise AppError(404, "video_drama_not_found", "找不到這部劇")


def _content(series: SeriesIndex) -> SeriesContent:
    try:
        raw = _read(f"{series.key}.json")
        if hashlib.sha256(raw).hexdigest() != series.content_sha256:
            raise ValueError("drama content does not match its index")
        content = SeriesContent.model_validate_json(raw)
        if content.key != series.key:
            raise ValueError("drama content belongs to another series")
        return content
    except (OSError, ValueError, ValidationError) as exc:
        raise _unavailable(exc) from exc


def episode(key: SeriesKey, slug: str) -> EpisodeDetail:
    series = _series(load_index(), key)
    summary = next((item for item in series.episodes if item.slug == slug), None)
    if summary is None:
        raise AppError(404, "video_drama_not_found", "找不到這一集")
    docs = _content(series).episodes.get(slug, {})
    return EpisodeDetail(
        series=key,
        slug=slug,
        title=summary.title,
        docs=[EpisodeText(kind=kind, markdown=docs[kind]) for kind in DOC_ORDER if kind in docs],
    )


def document(key: SeriesKey, doc_id: str) -> DocumentDetail:
    series = _series(load_index(), key)
    meta = next((item for item in series.documents if item.id == doc_id), None)
    if meta is None:
        raise AppError(404, "video_drama_not_found", "找不到這份企劃文件")
    markdown = _content(series).documents.get(doc_id)
    if markdown is None:
        raise _unavailable(ValueError("document missing from content"))
    return DocumentDetail(
        series=key, id=doc_id, path=meta.path, title=meta.title, markdown=markdown
    )
