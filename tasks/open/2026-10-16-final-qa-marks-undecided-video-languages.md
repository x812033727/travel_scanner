---
id: 2026-10-16-final-qa-marks-undecided-video-languages
title: Final QA marks undecided video languages as missing captions
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-16T13:09:29Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa
---

# Final QA marks undecided video languages as missing captions

## Why

M09 follows the current owner flow: finish and review the zh-TW cut, then ask the owner which additional languages to make. Before that choice, the work directory has no `languages.json`. `qa --slug curio-m09` and `review-push --gate final --manual-review` both reported captions FAIL (`en`, `ja`, `ko`: no caption file), although the 95 zh-TW cues passed and no additional language had yet been selected. This makes the final report 10/11 for an expected workflow state. The current fallback in `tools/video/core/stages.mjs` intentionally requests all locales for older projects without a choice, so changing that global fallback may break legacy videos.

## Definition of done

- [ ] Final QA distinguishes an owner language choice that has not happened yet from a selected locale whose captions are missing or stale.
- [ ] A current zh-TW video with valid zh-TW captions can reach owner final review without a misleading multilingual-caption failure; once the owner selects extra languages, their selected captions remain enforced at the appropriate gate.
- [ ] Legacy projects that intentionally use the no-choice all-locale fallback keep their existing behavior.

## Steps

- [ ] Identify the QA call path and available evidence for `language choice pending` versus a legacy video without a panel.
- [ ] Add focused tests for pending, selected, and legacy cases, then update the QA result wording/check.

## How to verify

Run the focused `tools/video/qa` tests and `npm run test:tools`; reproduce the M09 pre-choice report without changing its approved final cut or language selection.

## Notes

Observed 2026-10-16: M09 final SHA `9D9799CDF2E1B9165BD3F7817860107B085518AD47C18E03CC7C97BE4D6BF2F7`, `review/qa.json` 10/11, `captions` detail names only en/ja/ko; 95 zh-TW cues are current. Manual final review submission accepted and is pending owner. The two TypeSafe Jev QA calls were accounted for separately; this task must not rerun paid QA merely to test behavior.
