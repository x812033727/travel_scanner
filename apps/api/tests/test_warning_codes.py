import pytest

from app.warnings import warning_code


def test_a_warning_without_parameters_is_just_the_code() -> None:
    assert warning_code("coordinate_fallback") == "coordinate_fallback"


def test_parameters_are_appended_in_a_stable_order() -> None:
    # Callers deduplicate warnings by value, so the same warning has to spell the
    # same string every time regardless of keyword order.
    assert warning_code("provider_fallback", provider="Amadeus", module="flights") == (
        "provider_fallback?module=flights&provider=Amadeus"
    )
    assert warning_code("provider_fallback", module="flights", provider="Amadeus") == (
        "provider_fallback?module=flights&provider=Amadeus"
    )


def test_values_that_would_break_the_string_apart_are_encoded() -> None:
    assert warning_code("uncomparable_day", day="2026-11-10") == "uncomparable_day?day=2026-11-10"
    assert warning_code("provider_fallback", provider="Trip.com & co") == (
        "provider_fallback?provider=Trip.com+%26+co"
    )
    # The separator itself cannot appear unencoded in a value, so the reader's side
    # can always split on the first '?'.
    assert warning_code("x_warning", note="a?b=c").count("?") == 1


def test_none_parameters_are_dropped_rather_than_written_as_the_word_none() -> None:
    assert warning_code("stale_exchange_rate", currency=None) == "stale_exchange_rate"


def test_a_code_that_is_not_lower_snake_case_is_refused() -> None:
    # A sentence must never reach a client as if it were a code: the reader's side
    # would translate code-shaped strings and drop the ones it does not know.
    for bad in ["", "Walk_Route", "walk route", "路線服務尚未啟用", "walk.route", "1walk"]:
        with pytest.raises(ValueError):
            warning_code(bad)


def test_no_new_warning_is_written_as_a_finished_sentence() -> None:
    """A warning that leaves the API must be a code, not one language's sentence.

    The web side prints anything that is not code-shaped exactly as it arrives, so a
    Traditional Chinese sentence written here reaches a Japanese reader as Traditional
    Chinese. This walks the source rather than the endpoints because the endpoints that
    emit these are spread across a dozen routers, several of them behind a provider
    call; a source rule is the one that stays true when a new one is added.

    The exceptions below are deliberate and each has a reason. Adding to this list is a
    decision, not a formality: everything on it is copy some reader cannot read.
    """
    import re
    from pathlib import Path

    han = re.compile(r"[㐀-䶿一-鿿]")
    emits = re.compile(r"warnings\.append\(|\"warnings\":|warnings=\[|\bwarning=|_WARNING(?:S)? = ")
    # An AppError detail is a different contract: it is translated per locale by
    # app_error_handler through ERROR_DETAILS, so its zh-TW sentence is correct here.
    detail = re.compile(r"AppError\(")
    allowed = {
        # The airline fare lab is one of the four features the owner keeps closed, and
        # its three screens are written in Traditional Chinese throughout — they render
        # `warnings` verbatim, with no catalog to look a code up in. Sending codes there
        # would put identifiers on screen. Paired with localising those screens in
        # 2026-09-11-fare-lab-warnings-and-copy.
        ("app/crawlers/back_to_back.py", "stale rate"),
        ("app/crawlers/back_to_back.py", "no rate"),
        ("app/providers/live_back_to_back.py", "no live fare"),
    }
    found = set()
    for path in sorted(Path("app").rglob("*.py")):
        lines = path.read_text(encoding="utf-8").split("\n")
        for number, line in enumerate(lines, 1):
            if not han.search(line):
                continue
            window = "\n".join(lines[max(0, number - 4) : number])
            if detail.search(line):
                continue
            if emits.search(line) or emits.search(window):
                found.add((str(path), number, line.strip()))

    unexpected = [row for row in sorted(found) if row[0] not in {path for path, _ in allowed}]
    listed = "\n".join(f"  {path}:{number}: {text}" for path, number, text in unexpected)
    assert not unexpected, (
        f"warnings must be codes; write them with app.warnings.warning_code:\n{listed}"
    )
    # And the exceptions are still only the three that were argued for.
    assert {path for path, _, _ in found} == {path for path, _ in allowed}
