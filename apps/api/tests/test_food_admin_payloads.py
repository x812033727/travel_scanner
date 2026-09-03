from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.foods.admin_router import (
    FoodAreaWritePayload,
    FoodCategoryWritePayload,
    FoodMerchantBatchPayload,
    FoodMerchantSourcePayload,
    FoodMerchantUpdatePayload,
    FoodMerchantWritePayload,
    TaxonomyBatchPayload,
)

NAMES = {"zh-TW": "新宿", "zh-CN": "新宿", "en": "Shinjuku", "ja": "新宿", "ko": "신주쿠"}


def test_food_merchant_batch_accepts_verify_and_activate() -> None:
    merchant_id = uuid4()

    payload = FoodMerchantBatchPayload(ids=[merchant_id], action="verify_activate")

    assert payload.ids == [merchant_id]
    assert payload.action == "verify_activate"


def test_food_merchant_batch_rejects_unknown_action() -> None:
    with pytest.raises(ValidationError):
        FoodMerchantBatchPayload(ids=[uuid4()], action="publish")  # type: ignore[arg-type]


def test_food_area_payload_requires_five_locales_and_paired_coordinates() -> None:
    payload = FoodAreaWritePayload(
        slug="tokyo-shinjuku", destination_id="tokyo", names={**NAMES, "en": " Shinjuku "}
    )
    assert payload.names["en"] == "Shinjuku"
    assert payload.is_active is True
    with pytest.raises(ValidationError):
        FoodAreaWritePayload(slug="tokyo-shinjuku", destination_id="tokyo", names={"zh-TW": "新宿"})
    with pytest.raises(ValidationError):
        FoodAreaWritePayload(slug="Tokyo Shinjuku", destination_id="tokyo", names=NAMES)
    with pytest.raises(ValidationError):
        FoodAreaWritePayload(
            slug="tokyo-shinjuku", destination_id="tokyo", names=NAMES, latitude=35.69
        )


def test_food_category_payload_validates_names() -> None:
    payload = FoodCategoryWritePayload(slug="ramen", names=NAMES, display_order=3)
    assert payload.names == NAMES
    with pytest.raises(ValidationError):
        FoodCategoryWritePayload(slug="ramen", names={**NAMES, "ko": " "})


def test_food_merchant_payloads_accept_taxonomy_fields() -> None:
    source = FoodMerchantSourcePayload(
        source_type="official_tourism",
        source_title="Official guide",
        source_url="https://www.gotokyo.org/en/",
    )
    payload = FoodMerchantWritePayload(
        slug="tokyo-test",
        destination_id="tokyo",
        country_code="JP",
        name="Test",
        local_name="テスト",
        sources=[source],
        area_slug="tokyo-shibuya",
        category_slugs=["ramen", "izakaya-bar"],
    )
    assert payload.food_ids == []
    assert payload.category_slugs == ["ramen", "izakaya-bar"]
    with pytest.raises(ValidationError):
        FoodMerchantWritePayload(
            slug="tokyo-test",
            destination_id="tokyo",
            country_code="JP",
            name="Test",
            local_name="テスト",
            sources=[source],
            category_slugs=["ramen", "ramen"],
        )
    cleared = FoodMerchantUpdatePayload(area_slug=None)
    assert "area_slug" in cleared.model_fields_set
    assert FoodMerchantUpdatePayload().category_slugs is None
    assert FoodMerchantUpdatePayload(food_ids=[]).food_ids == []
    with pytest.raises(ValidationError):
        FoodMerchantUpdatePayload(category_slugs=["Bad Slug"])


def test_taxonomy_batch_payload_actions() -> None:
    assert TaxonomyBatchPayload(ids=[uuid4()], action="deactivate").action == "deactivate"
    with pytest.raises(ValidationError):
        TaxonomyBatchPayload(ids=[uuid4()], action="delete")  # type: ignore[arg-type]
