"""Five-locale plus original-script names for attractions, dishes and merchants.

The site speaks five locales (``app.i18n.LOCALES``). A place also carries an
*original* name in the script of its own country (原文): 浅草寺 for Sensō-ji,
한국의집 for Korea House. Catalog rows and saved trip items store both, so a
traveller who switches the UI language sees every planned stop re-labelled
instead of frozen in whatever language they used when they added it.

A name map is a plain ``dict[str, str]``::

    {
        "zh-TW": "淺草寺", "zh-CN": "浅草寺", "en": "Sensō-ji",
        "ja": "浅草寺", "ko": "센소지",
        "original": "浅草寺", "original_locale": "ja",
    }

``build_localized_names`` fills every site locale from whatever the caller
knows (explicit translations, the original text, a canonical fallback) so
readers never have to chase gaps; ``resolve_localized_name`` picks the label
for one locale and is tolerant of partial maps written by administrators.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from app.i18n import LOCALES, Locale

ORIGINAL_KEY = "original"
ORIGINAL_LOCALE_KEY = "original_locale"
NAME_KEYS: tuple[str, ...] = (*LOCALES, ORIGINAL_KEY, ORIGINAL_LOCALE_KEY)

# The language a place in this country writes its own name in. Thai and
# Vietnamese are not site locales, so their originals are kept only as
# ``original`` and never stand in for a site locale.
ORIGINAL_LOCALE_BY_COUNTRY: dict[str, str] = {
    "JP": "ja",
    "KR": "ko",
    "TW": "zh-TW",
    "HK": "zh-TW",
    "SG": "en",
    "TH": "th",
    "VN": "vi",
}

# When a locale has no translation, which other locales are the least surprising
# stand-in: the sibling Chinese script first for Chinese readers, English for
# everyone else, and a broader sweep after that so the map is always complete.
FALLBACK_LOCALES: Mapping[str, tuple[Locale, ...]] = {
    "zh-TW": ("zh-CN", "en", "ja", "ko"),
    "zh-CN": ("zh-TW", "en", "ja", "ko"),
    "en": ("zh-TW", "zh-CN", "ja", "ko"),
    "ja": ("en", "zh-TW", "zh-CN", "ko"),
    "ko": ("en", "zh-TW", "zh-CN", "ja"),
}

# Thai, Hangul jamo, kana, the unified CJK block and Hangul syllables.
_NON_LATIN_SCRIPT = re.compile(r"[฀-๿ᄀ-ᇿ぀-ヿ㐀-鿿가-힯]")


# Escapes rather than literal characters: written literally, the compatibility-block
# bound resolved to its unified codepoint (U+8C48, not U+F900) and the range silently
# swallowed every Hangul syllable, so Korean names counted as Chinese.
_HAN_SCRIPT = re.compile("[㐀-䶿一-鿿豈-﫿]")


def has_han_script(value: str | None) -> bool:
    """True when the text contains a Chinese character a Chinese reader can read.

    Used to tell a curated Chinese name from one that is only nominally Chinese —
    a seed whose name is Hangul or Thai is not a zh-TW label, and treating it as
    one shows Korean script to Chinese readers.
    """
    return bool(value and _HAN_SCRIPT.search(value))


def original_locale_for(country_code: str | None) -> str | None:
    """Language tag of the original script for a country, or ``None`` when unknown."""

    if not country_code:
        return None
    return ORIGINAL_LOCALE_BY_COUNTRY.get(country_code.upper())


def is_latin_script(value: str | None) -> bool:
    """True when the text has no CJK, Hangul or Thai characters (a romanized label)."""

    return bool(value and value.strip()) and _NON_LATIN_SCRIPT.search(value or "") is None


def _clean(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def build_localized_names(
    *,
    names: Mapping[str, object] | None = None,
    original: str | None = None,
    original_locale: str | None = None,
    country_code: str | None = None,
    fallback: str | None = None,
) -> dict[str, str]:
    """Return a complete five-locale map plus the original text.

    ``names`` holds whatever translations exist. A locale that is missing takes
    the original when that locale *is* the original language, then the first
    present locale from :data:`FALLBACK_LOCALES`, then ``fallback``. The result
    is empty only when nothing at all is known, so callers can store it as-is.
    """

    supplied = {locale: _clean((names or {}).get(locale)) for locale in LOCALES}
    original_text = _clean(original) or _clean((names or {}).get(ORIGINAL_KEY))
    language = (
        _clean(original_locale)
        or _clean((names or {}).get(ORIGINAL_LOCALE_KEY))
        or original_locale_for(country_code)
        or ""
    )
    canonical = _clean(fallback)
    result: dict[str, str] = {}
    for locale in LOCALES:
        value = supplied[locale]
        if not value and original_text and language == locale:
            value = original_text
        if not value:
            stand_ins = (supplied[candidate] for candidate in FALLBACK_LOCALES[locale])
            value = next((candidate for candidate in stand_ins if candidate), "")
        if not value:
            value = canonical or original_text
        if value:
            result[locale] = value
    if original_text:
        result[ORIGINAL_KEY] = original_text
        if language:
            result[ORIGINAL_LOCALE_KEY] = language
    return result


def resolve_localized_name(
    names: Mapping[str, Any] | None,
    locale: str,
    *,
    fallback: str | None = None,
) -> str | None:
    """Label for ``locale``: the translation, a fallback locale, the original, then ``fallback``."""

    if not names:
        return fallback
    value = _clean(names.get(locale))
    if value:
        return value
    for candidate in FALLBACK_LOCALES.get(locale, FALLBACK_LOCALES["en"]):
        value = _clean(names.get(candidate))
        if value:
            return value
    return _clean(names.get(ORIGINAL_KEY)) or fallback


def original_name(names: Mapping[str, Any] | None) -> str | None:
    """The original-script text stored in a name map, if any."""

    if not names:
        return None
    return _clean(names.get(ORIGINAL_KEY)) or None


def has_localized_names(names: Mapping[str, Any] | None) -> bool:
    """True when at least one site locale carries a label."""

    if not names:
        return False
    return any(_clean(names.get(locale)) for locale in LOCALES)


def sanitize_localized_names(names: Mapping[str, object] | None) -> dict[str, str]:
    """Keep only known keys with non-empty text (administrator input, JSON columns)."""

    if not names:
        return {}
    return {key: _clean(names.get(key)) for key in NAME_KEYS if _clean(names.get(key))}


def join_localized_names(
    first: Mapping[str, Any] | None,
    second: Mapping[str, Any] | None,
    *,
    separator: str = " · ",
) -> dict[str, str]:
    """Combine two maps locale by locale (a dish plus its merchant, for example).

    Locales present in only one map keep that side alone; the original texts are
    joined the same way and the original locale is taken from the first map.
    """

    left = sanitize_localized_names(first)
    right = sanitize_localized_names(second)
    result: dict[str, str] = {}
    for key in (*LOCALES, ORIGINAL_KEY):
        parts = [value for value in (left.get(key), right.get(key)) if value]
        if parts:
            result[key] = separator.join(dict.fromkeys(parts))
    language = left.get(ORIGINAL_LOCALE_KEY) or right.get(ORIGINAL_LOCALE_KEY)
    if language and result.get(ORIGINAL_KEY):
        result[ORIGINAL_LOCALE_KEY] = language
    return result


# Trip items keep one map per human-readable field so a composite title such as
# "ラーメン · Ichiran Shibuya" and a location that is really an address stay
# independently localizable.
ITEM_TITLE_KEY = "title"
ITEM_LOCATION_KEY = "location_name"


def item_names(
    *,
    title: Mapping[str, Any] | None,
    location_name: Mapping[str, Any] | None = None,
) -> dict[str, dict[str, str]]:
    """Build the ``names_json`` value stored on a trip item; empty maps are dropped."""

    result: dict[str, dict[str, str]] = {}
    for key, value in ((ITEM_TITLE_KEY, title), (ITEM_LOCATION_KEY, location_name)):
        cleaned = sanitize_localized_names(value)
        if has_localized_names(cleaned):
            result[key] = cleaned
    return result


def resolve_item_field(
    names_json: Mapping[str, Any] | None,
    field: str,
    locale: str,
    *,
    fallback: str | None,
) -> str | None:
    """Localized text for one trip-item field, or the stored text when nothing is known."""

    field_names = (names_json or {}).get(field)
    if not isinstance(field_names, Mapping) or not has_localized_names(field_names):
        return fallback
    return resolve_localized_name(field_names, locale, fallback=fallback)
