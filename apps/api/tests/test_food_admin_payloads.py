from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.foods.admin_router import FoodMerchantBatchPayload


def test_food_merchant_batch_accepts_verify_and_activate() -> None:
    merchant_id = uuid4()

    payload = FoodMerchantBatchPayload(ids=[merchant_id], action="verify_activate")

    assert payload.ids == [merchant_id]
    assert payload.action == "verify_activate"


def test_food_merchant_batch_rejects_unknown_action() -> None:
    with pytest.raises(ValidationError):
        FoodMerchantBatchPayload(ids=[uuid4()], action="publish")  # type: ignore[arg-type]
