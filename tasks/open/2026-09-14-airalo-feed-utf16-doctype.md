---
id: 2026-09-14-airalo-feed-utf16-doctype
title: Airalo feed XXE guard misses a UTF-16 encoded DOCTYPE
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-14T01:09:19Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/travel_services/jobs.py
  - apps/api/tests/test_travel_services.py
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

- [ ] A UTF-16LE and a UTF-16BE feed carrying `<!DOCTYPE` or `<!ENTITY` are refused, the same
      as the UTF-8 form.
- [ ] A normal UTF-8 feed still parses and still produces the same products.
- [ ] `app/travel_services/jobs.py` no longer needs the `S314` per-file ignore in
      `pyproject.toml`, or the ignore's comment says why it still does.

## Steps

- [ ] Cheapest fix that closes it without a dependency: strip NUL bytes before the marker
      test (`body.replace(b"\x00", b"")`), which folds UTF-16 down to ASCII for the purpose
      of the scan while leaving `body` itself untouched for the parser.
- [ ] Consider `defusedxml` instead. It is the correct answer to this whole class rather than
      to this one encoding, but it is a new dependency for one feed — weigh that, and write
      the decision down here either way.
- [ ] Whatever is chosen, keep the size limit: it is the other half of the DoS defence and
      does not depend on encoding.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_travel_services.py -q
```

Add a case per encoding: `"<!DOCTYPE x>...".encode("utf-16-le")` and `utf-16-be`, both
refused, plus the existing UTF-8 feed still parsing.

## Notes

- Do not "fix" this by decoding the body to text and scanning that: guessing an encoding to
  decide whether to trust a document is the same mistake one layer up.
- Filed while working `2026-09-13-ruff-flake8-bandit`, which is where the `S314` suppression
  and its comment live.
