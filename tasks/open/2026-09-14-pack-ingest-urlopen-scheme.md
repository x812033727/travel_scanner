---
id: 2026-09-14-pack-ingest-urlopen-scheme
title: Pack ingest urlopen accepts any scheme Commons hands back
status: review
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-14T11:14:16Z
created_at: 2026-09-14T04:01:21Z
completed_at:
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
---

# Pack ingest urlopen accepts any scheme Commons hands back

## Why

`app/guides/pack_ingest.py::UrllibTransport.handle_request` passes the request URL straight
to `urllib.request.urlopen`:

```python
raw = urllib.request.Request(str(request.url), headers=..., method=request.method)
with urllib.request.urlopen(raw, timeout=60) as answer:
```

`urlopen` is not an HTTP client. It also opens `file:`, `ftp:` and `data:`. `httpx` is
configured with `follow_redirects=True`, and the URL it is asked for is not always a module
constant: `fetch_image` is called with `info.image_url`, which is whatever Wikimedia's
`imageinfo` returned as `thumburl` or `url`.

So the set of things this can open is "whatever Commons says", not "an HTTPS URL on
commons.wikimedia.org". A `file:///…` value coming back from the API — or a redirect to one —
would be read off the developer's disk and packed into an article image.

Two reasons this is P3 and not higher. The module is a CLI (`python -m app.guides.pack_cli`)
run by a person or a writing agent over a workspace in this repository; nothing about it is
reachable from an HTTP request. And it takes a compromised or misbehaving Wikimedia API to
produce the bad URL in the first place.

It is still worth closing, because the fix is three lines and the current code offers no
resistance at all — the transport is a straight pass-through, which is exactly the shape that
gets copied into somewhere it matters.

Found on 2026-09-14 by `S310`, which `2026-09-13-ruff-flake8-bandit` turned on and then
suppressed for this file pending this task.

## Definition of done

- [x] `UrllibTransport` refuses any request whose scheme is not `http` or `https`, with a
      clear error rather than a silent read.
- [x] The Commons fetch path still works end to end — an ordinary redirect is still followed,
      pinned by a test.
- [x] The `S310` entry for `app/guides/pack_ingest.py` stays, and its comment now says why:
      the rule objects to `urlopen` at all, which is the one thing that cannot change — the
      transport exists precisely because httpx's own connections are refused by Wikimedia.

## What was done, and the part that was nearly wrong

Two changes, and the second only exists because the first step of this task said to check the
redirect path "rather than assuming it". Checking it showed the assumption was false.

**The scheme check.** `handle_request` refuses anything but `http`/`https` with a
`PackIngestError`, raised rather than returned as a status because `_get` retries some
statuses and no retry improves this.

**Redirects handed back to httpx.** Left alone, `urlopen` follows redirects *internally*, so
the hop never re-enters `handle_request` and the check above only ever sees the first URL.
Measured, not assumed:

| redirect target | plain `urlopen` |
| --- | --- |
| `file:///etc/hostname` | refused by urllib itself |
| `ftp://example.invalid/x` | **followed** — urllib's redirect rule allows http, https *and* ftp |
| `/ok` | followed |

So the naive fix would have left `ftp:` reachable through a redirect. `_NoRedirect` stops
urllib following them; the 3xx comes back through the existing `HTTPError` branch with its
`Location` intact, and httpx — which `commons_client` already configures with
`follow_redirects=True` — re-enters the transport for the next hop, where the scheme check
applies again.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides_pack_ingest.py -q
```

Both halves were checked against the code without them, which is what makes them more than
an assertion:

- remove the scheme check → 5 tests fail (three direct schemes, both redirects);
- keep the check but let `urlopen` follow redirects again → **exactly one** fails, the `ftp:`
  redirect. That single failure is the whole argument for the second half.

## Notes

- `defusedxml` is unrelated here; the `S314` entry for this file covers `_parse_svg` reading a
  diagram out of the workspace, which is a separate question and stays suppressed.
- The `pyproject.toml` comment refresh for both this entry and the Airalo one is scoped to
  `2026-09-14-airalo-feed-utf16-doctype`, so the file is claimed once rather than by two
  tasks the same agent happens to own.
- Filed while working `2026-09-13-ruff-flake8-bandit`, which is where the `S310` suppression
  lives.
