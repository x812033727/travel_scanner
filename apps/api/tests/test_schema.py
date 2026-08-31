from app.schema import expected_schema_revision, schema_is_current


def test_expected_schema_revision_is_current_head() -> None:
    assert expected_schema_revision() == "0010_hotspot_intelligence"
    assert schema_is_current("0010_hotspot_intelligence") is True
    assert schema_is_current("0009_usage_account_status") is False
    assert schema_is_current("0008_flight_status_lookups") is False
    assert schema_is_current("0007_alert_integrity") is False
    assert schema_is_current("0002_itinerary_sharing") is False
    assert schema_is_current(None) is False
