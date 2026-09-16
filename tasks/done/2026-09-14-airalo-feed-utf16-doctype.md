---
id: 2026-09-14-airalo-feed-utf16-doctype
title: Airalo feed XXE guard misses a UTF-16 encoded DOCTYPE
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-14T11:14:43Z
created_at: 2026-09-14T01:09:19Z
completed_at: 2026-09-16T06:12:11Z
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - apps/api/app/travel_services/jobs.py
  - apps/api/tests/test_travel_services_jobs.py
  - apps/api/pyproject.toml
---

# Airalo feed XXE guard misses a UTF-16 encoded DOCTYPE

## Why

`app/travel_services/jobs.py::parse_airalo` parses a partner feed with the standard library
and guards it by hand:

```python
if len(body) > FEED_LIMIT or b"<!DOCTYPE" in body.upper() or b"<!ENTITY" in body.upper():
    raise ValueError("Unsafe feed")
root = ElementTree.fromstring(body)
```

The intent is right and the guard does work for a UTF-8 feed. It does not work for a UTF-16
one. `bytes.upper()` only folds ASCII, and in UTF-16 every ASCII character is interleaved
with a NUL byte, so `<!DOCTYPE` on the wire is `<\x00!\x00D\x00O\x00...` and neither `in`
test matches. `ElementTree` honours the encoding in the XML declaration, so it would then
parse a document the guard believed it had rejected.

What that buys an attacker is entity-expansion denial of service — the "billion laughs"
shape — inside the worker. Python's `ElementTree` does not resolve external entities, so this
is not file disclosure.

It is also not reachable today by anyone but Airalo: `AIRALO_FEED` is a hardcoded
`https://www.airalo.com/products.xml` with no configurable URL, so exploiting it means
serving the payload from that host. That is why this is P3 and not higher. It is still worth
closing, because the guard is *meant* to be the defence and currently has a hole in exactly
the encoding a non-English vendor is most likely to emit.

Found on 2026-09-14 while triaging `S314` for `2026-09-13-ruff-flake8-bandit`, which turned
the rule on and then suppressed it for this file pending this task.

## Definition of done

- [x] A UTF-16LE and a UTF-16BE feed carrying `<!DOCTYPE` or `<!ENTITY` are refused, the same
      as the UTF-8 form.
- [x] A normal UTF-8 feed still parses and still produces the same products.
- [x] `app/travel_services/jobs.py` no longer needs the `S314` per-file ignore — **it does
      still need it**, and the comment in `pyproject.toml` now says why: the rule objects to
      `ElementTree` at all, not to this guard, and replacing it means taking on `defusedxml`.
      See the decision below.

## What was done

`_declares_dtd(body)` replaces the inline scan, and drops NUL bytes before matching:

```python
flattened = body.replace(b"\x00", b"").upper()
return b"<!DOCTYPE" in flattened or b"<!ENTITY" in flattened
```

That folds UTF-16 and UTF-32 down to the ASCII the scan can read, and cannot hide anything a
real feed contains, because NUL is not a valid XML character in any encoding — so a UTF-8
body has none to drop.

Confirmed first that the hole was real rather than theoretical: `ElementTree.fromstring`
does parse a UTF-16 document, so the declaration the old guard missed would have been parsed.

## `defusedxml` was weighed and declined

It is the right answer to the whole class rather than to one encoding, and it is already in
the environment — but only as a transitive **dev** dependency, under `pip-audit`. Using it in
`app/` means promoting it to a runtime dependency, in the image and the lock file, for one
feed on one hardcoded URL whose other defences (the 15 MB cap, no external entity resolution
in `ElementTree`) are unchanged. That is disproportionate. If a second XML source ever
arrives, revisit it then — and that is the moment the `S314` suppression should be revisited
too.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_travel_services_jobs.py -q
```

The tests were checked against the old guard, not just the new one: restoring
`flattened = body.upper()` fails the two UTF-16 cases and the padded-body case, and passes
everything else. A test that cannot fail on the bug it names is not evidence.

## Notes

- The tests live in a new `tests/test_travel_services_jobs.py` — see the scope note below.
- Writing them turned up an unrelated trap worth knowing: expat rejects `UTF-16-LE` and
  `UTF-16-BE` as *declared* encoding labels. A UTF-16 document declares `UTF-16` and relies on
  a byte order mark, so the test helper pairs each codec with the label and BOM that actually
  parse. Naming the codec twice does not work.
- Filed by the 2026-09-13 security review, found while triaging `S314` for
  `2026-09-13-ruff-flake8-bandit`.
- **Scope narrowed 2026-09-14.** This originally listed `tests/test_travel_services.py`, which
  `2026-09-12-trip-partner-offer-availability` (`claude-fable-5-1`) is mid-edit on, and
  `claim` refused it. Rather than take over a task whose claim is merely stale, the feed tests
  go in a new `tests/test_travel_services_jobs.py`. `parse_airalo` lives in
  `app/travel_services/jobs.py` and had no test module of its own, so that is where these
  belong anyway — the collision just made it obvious.
