"""Offline research-tool checks; pyproj is deliberately not an API dependency.

From apps/api:
uv run --with pyproj==3.7.2 pytest ../../docs/hotel-platforms/test_seoul_source.py -q
"""

from unittest.mock import patch

import pytest
from inspect_seoul_source import projected_pair, selected_facts, transform_pair, verify_saved


def permit(**changes):
    return {
        "관리번호": "3130000-201-2018-00005",
        "사업장명": "라이즈호텔",
        "영업상태코드": "01",
        "도로명주소": "서울특별시 마포구 양화로 130 (서교동)",
        "좌표정보(X)": "192971.947727746",
        "좌표정보(Y)": "450243.232547428",
        "discarded_field": "not retained",
        **changes,
    }


@pytest.mark.parametrize(
    "x,y,expected",
    [
        ("192971.947727746", "450243.232547428", (37.5544322, 126.9212509)),
        ("198619.38819773", "451135.740279961", (37.5624998, 126.9851617)),
        ("205601.904041677", "445151.509504571", (37.5085668, 127.0641469)),
    ],
)
def test_epsg_5174_transform_is_reproducible(x, y, expected):
    assert transform_pair(x, y) == expected


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", "", None, "not a number"])
def test_bad_projected_coordinate_is_rejected(value):
    with pytest.raises((TypeError, ValueError)):
        projected_pair(value, "450243")


def test_wrong_axis_order_rejected_instead_of_saving_wrong_location():
    with pytest.raises(ValueError, match="outside Seoul"):
        transform_pair("450243.232547428", "192971.947727746")


def test_extracts_only_selected_permit_fields_not_entire_dataset():
    row = permit()
    selected = selected_facts([permit(관리번호="unrelated"), row], {row["관리번호"]})
    assert len(selected) == 1
    assert set(selected[0]) == {"permit_id", "name", "address", "x", "y", "latitude", "longitude"}
    assert selected[0]["latitude"] == 37.5544322


def test_closed_missing_and_duplicate_permits_require_review():
    row = permit()
    ids = {row["관리번호"]}
    with pytest.raises(ValueError, match="Missing selected"):
        selected_facts([], ids)
    with pytest.raises(ValueError, match="status review"):
        selected_facts([permit(영업상태코드="03")], ids)
    with pytest.raises(ValueError, match="Duplicate permit"):
        selected_facts([row, row], ids)


def test_verify_saved_all_ten_does_not_call_network():
    with patch("httpx.post", side_effect=AssertionError("Offline verification must not fetch")):
        assert verify_saved() == 10
