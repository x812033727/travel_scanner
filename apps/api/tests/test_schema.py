from app.schema import expected_schema_revision, schema_is_current


def test_expected_schema_revision_is_current_head() -> None:
    assert expected_schema_revision() == "0005_admin_provider_settings"
    assert schema_is_current("0005_admin_provider_settings") is True
    assert schema_is_current("0002_itinerary_sharing") is False
    assert schema_is_current(None) is False
