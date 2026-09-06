from app.ai import catalog
from app.config import Settings


def test_every_catalog_id_is_a_valid_model_id_and_unique_per_vendor() -> None:
    for vendor, entries in catalog.MODEL_CATALOG.items():
        ids = [entry.id for entry in entries]
        assert len(ids) == len(set(ids)), vendor
        for entry in entries:
            assert catalog.valid_model_id(entry.id), entry.id
            assert entry.label
            assert entry.capabilities


def test_shipped_defaults_are_in_the_catalog() -> None:
    settings = Settings()
    for field, value in (
        ("openai_model", settings.openai_model),
        ("anthropic_model", settings.anthropic_model),
        ("minimax_model", settings.minimax_model),
        ("hotspot_guide_gemini_model", settings.hotspot_guide_gemini_model),
        ("gemini_model", settings.gemini_model),
    ):
        assert value in [entry.id for entry in catalog.model_options(field)], field


def test_field_options_only_offer_models_the_code_path_can_drive() -> None:
    for field in ("openai_model", "minimax_model", "hotspot_guide_ai_openai_model"):
        assert all(
            "responses_json_schema_strict" in entry.capabilities
            for entry in catalog.model_options(field)
        )
    for field in ("anthropic_model", "hotspot_guide_ai_anthropic_model"):
        assert all(
            "anthropic_structured_output" in entry.capabilities
            for entry in catalog.model_options(field)
        )
    assert all(
        "gemini_grounded" in entry.capabilities
        for entry in catalog.model_options("hotspot_guide_gemini_model")
    )
    for field in ("gemini_model", "hotspot_guide_ai_gemini_model"):
        assert all(
            "gemini_structured" in entry.capabilities for entry in catalog.model_options(field)
        )
    assert "hotspot_guide_ai_gemini_model" in catalog.OPTIONAL_MODEL_FIELDS
    assert catalog.field_options(("ai_planner_mode", "openai_model")).keys() == {"openai_model"}
    assert catalog.field_options(("route_cache_ttl_seconds",)) == {}


def test_model_id_pattern_matches_the_security_audit_rule() -> None:
    assert catalog.valid_model_id("gpt-5.6-terra")
    assert catalog.valid_model_id("ft:gpt-5.6-terra:org:abc")
    assert catalog.valid_model_id("models_v2")
    assert not catalog.valid_model_id("")
    assert not catalog.valid_model_id("gpt/../admin")
    assert not catalog.valid_model_id("model name")
    assert not catalog.valid_model_id("a" * 129)


def test_model_label_falls_back_to_the_raw_id() -> None:
    assert catalog.model_label("gemini", "gemini-3.8-flash") == "Gemini 3.8 Flash"
    assert catalog.model_label("gemini", "gemini-9-custom") == "gemini-9-custom"
