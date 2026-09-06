"""Which coordinate sources may be kept without another look."""

from __future__ import annotations

from app.locations.coordinates import has_durable_coordinates, is_durable_coordinate_source


def test_the_catalogue_only_trusts_a_source_a_human_vouched_for() -> None:
    assert is_durable_coordinate_source("wikidata", "https://www.wikidata.org/wiki/Q1")
    assert not is_durable_coordinate_source("google_places", "https://maps.google.com/x")
    assert not is_durable_coordinate_source("user_paste", "https://maps.google.com/x")
    assert not is_durable_coordinate_source("wikidata", "http://www.wikidata.org/wiki/Q1")


def test_a_traveller_s_own_stop_may_keep_the_point_their_link_carried() -> None:
    assert is_durable_coordinate_source(
        "google_places", "https://maps.google.com/x", scope="trip"
    )
    assert is_durable_coordinate_source(
        "user_paste", "https://maps.google.com/x", scope="trip"
    )
    # The scope widens the sources, it does not drop the https rule.
    assert not is_durable_coordinate_source("user_paste", "http://maps.google.com/x", scope="trip")
    assert not is_durable_coordinate_source("guessed", "https://example.com", scope="trip")


def test_coordinates_still_have_to_be_real_numbers() -> None:
    assert has_durable_coordinates(35.7, 139.7, "curated", "https://example.org/a")
    assert not has_durable_coordinates(None, 139.7, "curated", "https://example.org/a")
    assert not has_durable_coordinates(999, 139.7, "curated", "https://example.org/a")
