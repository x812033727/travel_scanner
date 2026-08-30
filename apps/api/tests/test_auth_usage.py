from uuid import uuid4

from app.auth.service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.usage.service import search_operation_cost


def test_password_and_jwt_roundtrip() -> None:
    hashed = hash_password("a-strong-demo-password")
    assert verify_password("a-strong-demo-password", hashed)
    user_id = uuid4()
    assert decode_access_token(create_access_token(user_id)) == user_id


def test_credit_cost_precedence() -> None:
    assert search_operation_cost({"trip_type": "multi_city", "modules": ["flight"]}) == (
        "multi_city_optimization",
        15,
    )
    assert search_operation_cost(
        {
            "trip_type": "round_trip",
            "modules": ["flight", "hotel", "activities", "transport"],
            "preferences": {"optimization_mode": "balanced"},
        }
    ) == ("full_trip_optimization", 10)
    assert search_operation_cost({"modules": ["flight", "hotel"]}) == ("flight_hotel_search", 5)
