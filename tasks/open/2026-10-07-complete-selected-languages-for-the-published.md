---
id: 2026-10-07-complete-selected-languages-for-the-published
title: Complete selected languages for the uploaded LLM explainer
status: review
priority: P1
area: docs
owner: codex-llm-selected-languages
claimed_at: 2026-10-07T04:26:29Z
created_at: 2026-10-07T04:25:59Z
completed_at:
branch: codex/llm-selected-language-completion-20261007
depends_on: []
scope:
  - docs/videos/ai-term-large-language-model/i18n
  - docs/videos/recovery/2026-10-07-llm-selected-languages.md
---

# Complete selected languages for the uploaded LLM explainer

## Why

The uploaded `ai-term-large-language-model` video has selected English, Japanese,
Korean and Simplified Chinese metadata/CC, plus English/Japanese/Korean dubbing.
The approved package contains only zh-TW and no language review exists, so the
current consumer refuses it as an expired language choice. Complete the selected
assets against the approved source and send a source-bound language review.

## Acceptance

- [x] Translate all four selected locales and independently review them.
- [x] Produce and check the three selected dubs within existing settings, retaining
  exact request receipts and completed clips on any uncertain provider result.
- [x] Produce CC and metadata, preserving the approved final and zh-TW audio.
- [x] Submit verifiable metadata and language manifest; validate with the real
  production consumer and record its persisted review status.
- [x] Record hashes, selected parts, actual validation and remaining owner actions.

## Boundaries

No source-video rewrite, YouTube upload/publication, budget changes or deployment.
Generated media and operational scripts remain outside Git. The ordinary native
language producer's missing manifest is tracked separately; use a one-time source
manifest for this batch rather than changing another session's active tooling.

## Definition of done

- [x] All selected assets are current, independently reviewed and attached to one
  persisted source-bound language review. Original approved media and YouTube
  delivery identity remain unchanged; any required owner action is stated.

## Steps

- [x] Snapshot the actual remote choices, latest final/publish approvals and source
  hashes; recover only the matching original media without re-rendering it.
- [x] Complete all four native translation worksheets and independent reviews.
- [x] Synthesize English/Japanese/Korean using the existing Gemini settings and
  cache; shorten only the single English line identified by actual fit.
- [x] Finish native audio checks, captions and packaging for the selected parts.
- [x] Validate uploaded bytes with the production consumer in a read-only
  transaction, submit once, then verify persisted pending review and source pins.
- [ ] Save the final evidence and open a draft PR for the translation records.

## How to verify

Use the bundled compatible Node runtime for native video CLI commands:

```text
tools/video/cli.mjs lint --slug ai-term-large-language-model
tools/video/cli.mjs check-audio --slug ai-term-large-language-model --locale <en|ja|ko> --workdir C:\Users\x8120\mokaair-work\videos --second-opinion <existing offline Whisper command>
tools/video/cli.mjs captions --slug ai-term-large-language-model --workdir C:\Users\x8120\mokaair-work\videos
tools/video/cli.mjs package --slug ai-term-large-language-model --workdir C:\Users\x8120\mokaair-work\videos
npm run check:tasks
```

Automatic audio clearance requires all 138 actual clips to have current
input-bound verdicts, zero unchecked lines, zero remaining flags and a successful
native check run. The completed actual checks retain 1 English, 4 Japanese and
4 Korean flags, with zero unchecked lines. Each locale completed two quality
retakes and two appropriate independently reviewed listener rounds. Native audio
checks exit 1; fit, captions and packaging pass. A source-bound pending owner
review preserves all actual transcripts, scores, clips and timing, without
declaring automatic clearance, owner acceptance or a Studio upload.
The private submission scripts preserve one POST intent and receipts; production
validation uses the installed `read_approved_package` with `verify_files=True`,
and changes no approvals or delivery state. Exact receipts and resulting review
identity belong in `docs/videos/recovery/2026-10-07-llm-selected-languages.md`.

The completed review is `dbabfb6d-7a76-40c5-b668-f4cac8045662`, status `pending`,
content SHA-256
`d512388a533425734e52dcf84b81e0ac26d6472e2dc1f4548f62ce560d530efa`.
All 13 exact attachments were validated. The installed real consumer now refuses
the unapproved language review, while a detached approved candidate passes the
full source/byte contract. No persisted approval or Studio delivery changed.

## Notes

The actual remote choice is en/ja/ko metadata+CC+dub and zh-CN metadata+CC, decided
`2026-10-04T15:36:31.277219Z`. All four locales contain 138 stable lines and eight
chapters. The original source, final, narration and approval receipts are frozen.

Windows twice refused promotion of a complete saved speech answer. The operation
retained the exact full WAV and sent/confirmed receipts, validated request and
answer hashes and dead producers, and promoted only the local receipt. Subsequent
native runs reused those answers. A narrow runtime workaround also retained two
later complete English answers. No uncertain request was cleared or resent. The
native defect is filed separately as
`2026-10-07-preserve-full-speech-answers-when-windows`.

Generated media and detailed provider receipts stay outside Git under
`C:\Users\x8120\mokaair-work`. The ordinary producer's missing metadata/manifest
is separately tracked in draft PR #1363; this task changes no shared video tools.
