"""Unit guards for the trip and per-day note contracts.

The endpoints themselves are exercised against a real Postgres in
tests/test_integration_postgres_redis.py; these pin the request shapes and the
route registration, which is where a note feature quietly disappears.
"""

import pytest
from pydantic import ValidationError

from app.main import app
from app.trips.router import TripDayNoteRequest, TripMetadataPatchRequest


def test_note_routes_are_published() -> None:
    paths = app.openapi()["paths"]
    assert "patch" in paths["/api/v1/trips/{trip_id}"]
    assert "put" in paths["/api/v1/trips/{trip_id}/days/{day_date}/notes"]


def test_a_trip_note_is_trimmed_and_an_empty_one_clears_it() -> None:
    assert TripMetadataPatchRequest(version=1, notes="  要先寄放行李  ").notes == "要先寄放行李"
    # Explicitly sending "" is how the box clears; it must not store whitespace.
    cleared = TripMetadataPatchRequest(version=1, notes="   ")
    assert cleared.notes is None
    assert "notes" in cleared.model_fields_set


def test_a_patch_that_changes_nothing_is_rejected() -> None:
    # Without this the endpoint would bump the version for a no-op and 409
    # every other tab the traveller has open.
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest(version=1)


def test_a_note_cannot_be_unbounded() -> None:
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest(version=1, notes="字" * 4001)
    with pytest.raises(ValidationError):
        TripDayNoteRequest(version=1, notes="字" * 4001)


def test_a_day_note_needs_a_version_like_every_other_trip_write() -> None:
    with pytest.raises(ValidationError):
        TripDayNoteRequest(notes="這天要先訂位")  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        TripDayNoteRequest(version=0, notes="這天要先訂位")
    assert TripDayNoteRequest(version=3, notes="這天要先訂位").notes == "這天要先訂位"
    # An omitted body is how a day note is deleted.
    assert TripDayNoteRequest(version=3).notes is None
