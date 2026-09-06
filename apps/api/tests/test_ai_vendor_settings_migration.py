"""Unit-level checks of migration 0047 that need no database.

The pure merge/strip step and the Fernet derivation are what could silently lose a
key; both are exercised here against the app's own helpers. The database round trip
lives in ``test_migration_0047_ai_vendors.py`` behind ``RUN_INTEGRATION_TESTS=1``.
"""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

from app.admin.service import decrypt_secrets, encrypt_secrets
from app.config import Settings

MIGRATION = (
    Path(__file__).resolve().parents[1] / "migrations" / "versions" / "0047_ai_vendor_settings.py"
)


def load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("migration_0045", MIGRATION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_split_moves_keys_and_base_urls_and_keeps_everything_else() -> None:
    migration = load()
    sources = {
        "ai_planner": migration.VendorRow(
            {"ai_planner_mode": "auto", "openai_api_base_url": "https://api.openai.com/v1"},
            {"openai_api_key": "sk-planner", "anthropic_api_key": "sk-claude"},
        ),
        "gemini_guides": migration.VendorRow(
            {
                "hotspot_guide_gemini_model": "gemini-3.8-flash",
                "hotspot_guide_gemini_base_url": "https://generativelanguage.googleapis.com",
            },
            {"hotspot_guide_gemini_api_key": "g-key"},
        ),
    }
    assert migration.has_moved_fields(sources)

    merged, stripped = migration.split_vendor_fields(sources, None)

    assert merged.config == {
        "openai_api_base_url": "https://api.openai.com/v1",
        "hotspot_guide_gemini_base_url": "https://generativelanguage.googleapis.com",
    }
    assert merged.secrets == {
        "openai_api_key": "sk-planner",
        "anthropic_api_key": "sk-claude",
        "hotspot_guide_gemini_api_key": "g-key",
    }
    assert stripped["ai_planner"].config == {"ai_planner_mode": "auto"}
    assert stripped["ai_planner"].secrets == {}
    assert stripped["gemini_guides"].config == {"hotspot_guide_gemini_model": "gemini-3.8-flash"}
    assert stripped["gemini_guides"].secrets == {}
    assert not migration.has_moved_fields(stripped)
    # The inputs are not mutated, so a failed transaction can be retried.
    assert sources["ai_planner"].secrets == {
        "openai_api_key": "sk-planner",
        "anthropic_api_key": "sk-claude",
    }


def test_values_already_on_the_vendor_row_win_and_a_gemini_only_install_moves() -> None:
    migration = load()
    target = migration.VendorRow(
        {"openai_api_base_url": "https://api.openai.com/kept"}, {"openai_api_key": "sk-kept"}
    )
    sources = {
        "ai_planner": migration.VendorRow(
            {"openai_api_base_url": "https://api.openai.com/v1"}, {"openai_api_key": "sk-old"}
        )
    }
    merged, stripped = migration.split_vendor_fields(sources, target)
    assert merged.config["openai_api_base_url"] == "https://api.openai.com/kept"
    assert merged.secrets["openai_api_key"] == "sk-kept"
    assert stripped["ai_planner"].config == {} and stripped["ai_planner"].secrets == {}

    gemini_only = {"gemini_guides": migration.VendorRow({}, {"hotspot_guide_gemini_api_key": "g"})}
    assert migration.has_moved_fields(gemini_only)
    merged, _ = migration.split_vendor_fields(gemini_only, None)
    assert merged.secrets == {"hotspot_guide_gemini_api_key": "g"}

    untouched = {"ai_planner": migration.VendorRow({"ai_planner_mode": "auto"}, {})}
    assert not migration.has_moved_fields(untouched)


def test_fernet_derivation_matches_the_app() -> None:
    migration = load()
    settings = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        settings_encryption_key="dedicated-settings-key",
    )
    fernet = migration._fernet(settings)
    from_app = encrypt_secrets({"openai_api_key": "sk-round-trip"}, settings)
    assert migration._decrypt("ai_planner", from_app, fernet) == {"openai_api_key": "sk-round-trip"}
    from_migration = migration._encrypt({"minimax_api_key": "mm-round-trip"}, fernet)
    assert decrypt_secrets(from_migration, settings) == {"minimax_api_key": "mm-round-trip"}
    assert migration._encrypt({}, fernet) is None
    assert migration._decrypt("ai_planner", None, fernet) == {}
    with pytest.raises(RuntimeError):
        migration._decrypt("ai_planner", "not-a-fernet-token", fernet)
