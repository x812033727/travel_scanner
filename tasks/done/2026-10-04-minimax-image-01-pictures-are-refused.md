---
id: 2026-10-04-minimax-image-01-pictures-are-refused
title: MiniMax image-01 pictures are refused: the adapter takes the bytes, not a download URL
status: done
priority: P1
area: api
owner: claude-opus-5-5-minimax
claimed_at: 2026-10-04T06:34:34Z
created_at: 2026-10-04T06:32:27Z
completed_at: 2026-10-04T06:51:58Z
branch: claude/minimax-image-inline
depends_on: []
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/tests/test_video_media_providers.py
  - apps/api/tests/test_video_media_jobs.py
---

# MiniMax image-01 pictures are refused: the adapter takes the bytes, not a download URL

## Why

The owner switched the illustrated slides' image model to MiniMax `image-01` on the settings
tab. On 2026-10-04 every picture request was failing on production with

```
the vendor's download URL is not an https address
```

That message is `check_download` in `apps/api/app/video_media/providers/__init__.py`, which
lets the server fetch only an `https` URL on a named public host. `MiniMaxImages` asked the
vendor for `"response_format": "url"`, took `data.image_urls[0]` and handed it to the download
step; the link MiniMax answers with does not pass the check, so no `image-01` picture has ever
been stored. The server deliberately logs no vendor text, so the link itself was never seen:
its scheme and host are not known, and the check is not to be loosened to fit a guess.

Decision: do not download at all. MiniMax's image API returns the picture in the answer when
asked (`response_format: base64` -> `data.image_base64`, a list of base64 strings), which is
how the Gemini image adapter already works (`Submitted(inline=...)`). Rejected: allowing `http`
or an IP literal in `check_download` (it is the guard that keeps the server from fetching
arbitrary addresses a vendor names).

## Definition of done

- [x] `MiniMaxImages` asks for `response_format: base64` and returns the decoded first entry
      of `data.image_base64` as inline bytes; a job run through the real adapter ends `ready`
      with the type read from the bytes, US$0.0035 on the job and one image on the meter.
- [x] An answer that carries only `image_urls` still goes down the download path and through
      `check_download`: a refused link fails with the same message and code as before.
- [x] An empty list, an entry that is not a string, text that is not base64 and an empty
      picture are each a `MediaUpstreamError(502, ..., "failed")` with a fixed message that
      repeats nothing the vendor sent; the job gives its budget back.
- [ ] After deploy: one live `image-01` picture is stored (see How to verify). Not possible
      from this branch: the MiniMax key lives only on the server.

## Steps

- [x] Read how `Submitted.inline` is consumed (`jobs._settle` -> `_store_bytes` ->
      `MediaStore.put_stream`) and confirm nothing there is Gemini-specific.
- [x] Read MiniMax's API reference for the field name and the picture's format.
- [x] Adapter: `base64` request, `decode_image`, the link fallback.
- [x] Tests: the request body, bytes in the answer (JPEG, PNG, line-wrapped), link-only
      answers, twelve unusable answers, and one job through the state machine.

## How to verify

```bash
cd apps/api
uv run ruff check . && uv run mypy app && uv run mypy tests
uv run pytest tests/test_video_media_providers.py tests/test_video_media_jobs.py tests/test_video_media_catalog.py -q
```

After deploy (the owner's settings already name `image-01`):

```bash
node tools/video/cli.mjs keyframes --slug ai-term-token --shot two-bags
```

One picture is drawn and stored, and the ledger shows about US$0.0035 for it. If it fails,
the job's error says which branch was taken: `MiniMax's image is not valid base64` or
`MiniMax returned no image` (the answer had no usable `image_base64`), or the old `the
vendor's download URL is not an https address` (the vendor ignored `response_format` and sent
a link again).

## Notes

- How inline bytes are consumed, read on 2026-10-04: `jobs._settle` stores `submitted.inline`
  through `_store_bytes` -> `MediaStore.put_stream`, which reads the content type from the
  first bytes (`storage.sniff_type`: PNG, JPEG, WebP, ...), enforces
  `video_media_max_file_bytes` and the store's total, and refuses a zero-byte or unknown file
  with 415 and no refund. `Submitted.content_type` is read by nothing in `jobs.py`; the job's
  type is the store's. The price is `meter.usd_for(model, ...)` from the catalog row and the
  meter is keyed by kind, so neither knows the vendor. Nothing needed changing there.
- Refunds differ by where an answer fails, as for Gemini: an error raised in `submit` (no
  picture, not base64) gives the budget back and zeroes `usd_estimate`; a link refused in
  `fetch`, or bytes the store refuses, keep the charge. So a picture MiniMax billed but sent
  garbled is refunded on our meter (US$0.0035 each); the download path never refunded it.
- MiniMax's reference (`platform.minimax.io/docs/api-reference/image-generation-t2i` and
  `-i2i`, and the mainland `platform.minimaxi.com` copy, read 2026-10-04): `response_format`
  is `url` (default, "expires in 24 hours") or `base64`; `data.image_base64` is "an array of
  base64-encoded images". No page states the picture's format; the guide's sample saves the
  decoded bytes as `output-N.jpeg`. So the adapter reads the type from the bytes instead of
  claiming JPEG.
- The reference also documents `metadata.failed_count` ("images blocked due to content
  safety"). A blocked picture with `status_code` 0 would arrive as an empty list and fail as
  `video_media_upstream_failed`, as an empty `image_urls` did; mapping it to `blocked` would
  be a separate change, once a live refusal shows what the answer looks like.
- `decode_image` drops whitespace before decoding (line-wrapped base64 is legal) and is
  strict otherwise (`validate=True`): a `data:` prefix or any stray character is refused.
- Claimed with `--force`: `2026-10-03-illustrated-slides-round-2-a-family` still sits in
  `review` with `apps/api/app/video_media/providers` and `apps/api/tests` in its scope, but
  its PR #1172 merged on 2026-10-03, its remote branch is gone, no open PR touches these files
  and its two open items (the receipt rebind, the post-deploy look) edit neither.
- None of the three files is bound by `docs/videos/long-form/review.json`.
- The one unticked item (a live picture after deploy) was left unticked on purpose: no call to
  MiniMax was made from this branch. It travels with the deploy of this change; the pull
  request's body carries the same command, and whoever deploys runs it and reads the ledger.
