"""One spelling for the warnings the API hands to a client.

A warning used to be a finished Traditional Chinese sentence. Every reader got it,
in every locale, because the string left here already written. The fix was to send a
code and let the reader's own catalog say it — `walk_route_beta`, `coordinate_fallback`
— which `apps/web/lib/warnings.ts` translates.

Codes alone do not cover the warnings that name something: a currency, a module, the
day that could not be compared. This adds parameters to the same string, in the one
shape that survives being stored in `warnings_json` and read back years later:

    coordinate_fallback
    stale_exchange_rate?currency=JPY
    provider_fallback?module=flights&provider=Amadeus

The reader's side splits on the first `?` and interpolates the rest into the message.
Nothing about the storage changes: a warning is still one string in a JSON array, and
the sentences already written into old trips still render as themselves, because the
web side passes anything that is not code-shaped straight through.
"""

from urllib.parse import urlencode

# Same shape the web side tests for, so a warning that leaves here is one it will
# recognise. Kept deliberately narrow: no dots, no spaces, nothing that could be
# mistaken for a sentence in any of the five languages.
_CODE = "abcdefghijklmnopqrstuvwxyz0123456789_"


def warning_code(code: str, **params: object) -> str:
    """Spell one warning as `code` or `code?name=value`.

    Values are percent-encoded, so a provider called `Trip.com` or a date with a
    slash cannot break the string apart. Parameters are sorted, so the same warning
    is always the same string — callers deduplicate warnings by value.
    """
    if not code or code[0] not in _CODE[:26] or any(letter not in _CODE for letter in code):
        raise ValueError(f"warning code must be lower snake_case: {code!r}")
    if not params:
        return code
    pairs = sorted((name, str(value)) for name, value in params.items() if value is not None)
    return f"{code}?{urlencode(pairs)}" if pairs else code


def is_warning_code(value: str) -> bool:
    """True when a string left here as a code rather than as something to read.

    Used where a warnings list is folded into a sentence a member reads: a code says
    nothing to them, so only free text a provider actually wrote may go in.
    """
    code, _, params = value.partition("?")
    if not code or code[0] not in _CODE[:26] or any(letter not in _CODE for letter in code):
        return False
    return not params or all("=" in pair for pair in params.split("&"))
