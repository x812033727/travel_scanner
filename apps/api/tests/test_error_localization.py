"""Every error a reader can hit says what went wrong, in their language.

``app_error_handler`` answers a non-zh-TW reader from ``ERROR_DETAILS[locale][code]`` and
falls back to ``GENERIC_DETAILS`` when the code is not in the table. The fallback is not a
failure the tests could otherwise see: the request still returns the right status and the
right code, and only the sentence a person reads turns into "The request could not be
completed." So the coverage is asserted here instead.

Admin and deployment endpoints are exempt on purpose. They are Traditional Chinese first —
the panel itself is — and their operator reads the code as often as the sentence.
"""

from __future__ import annotations

import re
from pathlib import Path

from app.i18n import ERROR_DETAILS, LOCALES

APP = Path(__file__).resolve().parent.parent / "app"
RAISED = re.compile(r'AppError\(\s*\d+\s*,\s*"([a-z0-9_]+)"')
# A path is an operator surface when it sits in an admin router or the deployment centre.
OPERATOR_ONLY = ("admin", "deployments")
TRANSLATED = tuple(locale for locale in LOCALES if locale != "zh-TW")


def _codes_by_surface() -> tuple[set[str], set[str]]:
    public: set[str] = set()
    operator: set[str] = set()
    for path in sorted(APP.rglob("*.py")):
        relative = path.relative_to(APP).as_posix()
        target = operator if any(part in relative for part in OPERATOR_ONLY) else public
        target.update(RAISED.findall(path.read_text(encoding="utf-8")))
    return public, operator - public


def test_every_public_error_code_has_a_sentence_in_every_locale() -> None:
    public, _ = _codes_by_surface()
    assert public, "the scan found no error codes at all, so it is not doing its job"
    for locale in TRANSLATED:
        missing = sorted(code for code in public if code not in ERROR_DETAILS[locale])
        assert not missing, (
            f"{len(missing)} public error codes have no {locale} sentence, so a reader "
            f"gets the generic one: {', '.join(missing[:12])}"
        )


def test_the_locales_answer_the_same_set_of_codes() -> None:
    """A code translated into three of four languages is the worst of both worlds."""
    reference = set(ERROR_DETAILS["en"])
    for locale in TRANSLATED:
        assert set(ERROR_DETAILS[locale]) == reference, (
            f"{locale} and en disagree about which codes have a sentence: "
            f"{sorted(reference ^ set(ERROR_DETAILS[locale]))[:12]}"
        )


def test_no_sentence_is_empty_or_a_leftover_format_string() -> None:
    """The table cannot interpolate, so a `{...}` in it would reach the reader verbatim."""
    for locale in TRANSLATED:
        for code, sentence in ERROR_DETAILS[locale].items():
            assert sentence.strip(), f"{locale}/{code} is empty"
            assert "{" not in sentence, f"{locale}/{code} still carries a placeholder"
