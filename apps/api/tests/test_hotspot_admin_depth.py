from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.hotspots.admin_router import HotspotReviewRequest


def _payload(**changes: object) -> dict[str, object]:
    return {
        "ids": [uuid4()],
        "action": "update",
        "is_deep_travel": True,
        "depth_kind": "urban_local",
        "locality_score": 85,
        "distinctiveness_score": 85,
        "feasibility_score": 85,
        "evidence_score": 90,
        "depth_reason": "具有可驗證的地方生活脈絡",
        "access_minutes": 30,
        "recommended_duration_minutes": 120,
        **changes,
    }


def test_admin_depth_review_accepts_explainable_score() -> None:
    payload = HotspotReviewRequest.model_validate(_payload())
    assert payload.depth_kind == "urban_local"


@pytest.mark.parametrize(
    "changes",
    [
        {"locality_score": 10, "distinctiveness_score": 10, "feasibility_score": 10},
        {"access_minutes": 46},
        {"depth_reason": None},
    ],
)
def test_admin_depth_review_rejects_incomplete_or_invalid_values(
    changes: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        HotspotReviewRequest.model_validate(_payload(**changes))


def test_admin_can_remove_depth_marker_without_score_fields() -> None:
    payload = HotspotReviewRequest.model_validate(
        {"ids": [uuid4()], "action": "update", "is_deep_travel": False}
    )
    assert payload.is_deep_travel is False
