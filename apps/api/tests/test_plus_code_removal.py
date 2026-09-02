from app.main import app
from app.models import FoodMerchant, HotspotPlaceProfile, TravelHotspot, TripPlanItem
from app.places.google import LOCATE_FIELD_MASK, PLACE_PROFILE_FIELD_MASK
from app.restaurants.google import DETAIL_FIELD_MASK, NEARBY_FIELD_MASK


def test_plus_code_columns_are_absent_from_current_models() -> None:
    assert "plus_code_global" not in TravelHotspot.__table__.columns
    assert "plus_code_global" not in FoodMerchant.__table__.columns
    assert "plus_code_global" not in TripPlanItem.__table__.columns
    assert "plus_code_global" not in HotspotPlaceProfile.__table__.columns
    assert "plus_code_compound" not in HotspotPlaceProfile.__table__.columns


def test_google_field_masks_do_not_request_plus_codes() -> None:
    for field_mask in (
        LOCATE_FIELD_MASK,
        PLACE_PROFILE_FIELD_MASK,
        NEARBY_FIELD_MASK,
        DETAIL_FIELD_MASK,
    ):
        assert "plusCode" not in field_mask


def test_admin_plus_code_preview_routes_are_removed() -> None:
    paths = set(app.openapi()["paths"])
    assert "/api/v1/admin/hotspots/plus-code-preview" not in paths
    assert "/api/v1/admin/foods/merchants/plus-code-preview" not in paths
