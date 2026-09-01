from app.schema import expected_schema_revision, schema_is_current


def test_expected_schema_revision_is_current_head() -> None:
    assert expected_schema_revision() == "0014_user_preferred_locale"
    assert schema_is_current("0014_user_preferred_locale") is True
    assert schema_is_current("0013_hotspot_discovery") is False
    assert schema_is_current("0012_line_price_alerts") is False
    assert schema_is_current("0011_auth_session_version") is False
    assert schema_is_current("0010_hotspot_intelligence") is False
    assert schema_is_current("0009_usage_account_status") is False
    assert schema_is_current("0008_flight_status_lookups") is False
    assert schema_is_current("0007_alert_integrity") is False
    assert schema_is_current("0002_itinerary_sharing") is False
    assert schema_is_current(None) is False
