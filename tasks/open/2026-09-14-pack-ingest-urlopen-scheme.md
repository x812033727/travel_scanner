---
id: 2026-09-14-pack-ingest-urlopen-scheme
title: Pack ingest urlopen accepts any scheme Commons hands back
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-14T04:01:21Z
completed_at:
branch:
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

- [ ] `UrllibTransport` refuses any request whose scheme is not `http` or `https`, with a
      clear error rather than a silent read.
- [ ] The Commons fetch path still works end to end.
- [ ] The `S310` entry for `app/guides/pack_ingest.py` is gone from `pyproject.toml`, or its
      comment says why it still has to be there.

## Steps

- [ ] In `handle_request`, check `request.url.scheme` against `{"http", "https"}` before
      building the `urllib` request, and raise rather than returning a response — a caller
      that gets a 4xx back would retry it, and this is not a retryable condition.
- [ ] Check the redirect path too. `follow_redirects=True` means httpx re-enters
      `handle_request` for each hop, so the same guard should cover a redirect into `file:`;
      confirm that is actually true rather than assuming it.
- [ ] Add a test with a `file://` URL asserting the refusal. The module's I/O is injected and
      the existing tests mock the `httpx.Client`, so this one has to exercise the transport
      directly.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run pytest tests/test_guides_pack_ingest.py -q
```

## Notes

- Do not "fix" this by switching to plain `httpx`. The transport exists because Wikimedia's
  edge answers httpx's own connections with 403 whatever the User-Agent says, which is
  documented in the class docstring. The scheme check is the fix; the transport stays.
- Filed while working `2026-09-13-ruff-flake8-bandit`, which is where the `S310` suppression
  and its comment live.
