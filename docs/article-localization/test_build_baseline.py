"""Baseline target classification tests; no production state is accessed."""

import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "build_baseline", Path(__file__).with_name("build_baseline.py")
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_public_existing_drafts_are_publication_targets_not_translation_targets():
    work = module.locale_work(
        {locale: {} for locale in module.LOCALES}, ["zh-TW"], "published"
    )
    assert work == {
        "missing_locales": [],
        "translation_missing_locales": [],
        "publication_missing_locales": ["en", "ja", "ko", "zh-CN"],
        "publication_locales": ["en", "ja", "ko", "zh-CN"],
        "target_locales": ["en", "ja", "ko", "zh-CN"],
    }


def test_private_pack_only_targets_documents_that_need_translation():
    work = module.locale_work({"zh-TW": {}}, [], "draft")
    assert work["translation_missing_locales"] == ["en", "ja", "ko", "zh-CN"]
    assert work["publication_missing_locales"] == []
    assert work["target_locales"] == ["en", "ja", "ko", "zh-CN"]


def test_provenance_distinguishes_repository_database_draft_and_publication():
    provenance = module.locale_provenance(
        ["zh-TW", "en"],
        {
            "en": {"published_version": None},
            "ja": {"published_version": None},
            "ko": {"published_version": 3},
        },
    )
    assert provenance == {
        "zh-TW": "repository-only",
        "en": "database-draft",
        "ja": "database-draft",
        "ko": "database-published",
    }
