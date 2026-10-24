---
id: 2026-10-24-prepare-c19-seven-bank-canonical-video
title: Prepare C19 Seven Bank canonical video project
status: done
priority: P1
area: docs
owner: codex-c19-canonical
claimed_at: 2026-10-24T04:22:03Z
created_at: 2026-10-24T04:21:59Z
completed_at: 2026-10-24T04:27:26Z
branch: codex/c19-seven-bank-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19
---

# Prepare C19 Seven Bank canonical video project

## Why

C19 Seven Bank has an owner-approved 79-line Traditional Chinese script and
79-shot visual plan, and the backend already has its pending script review card.
It has no canonical `video.json` or related project files for the video tools.
Build a nonpaid project without changing the approved original bytes or
implying that a script card is a finished film.

## Definition of done

- [x] Canonical project files and a reproducible conversion preserve all 79
      approved narration lines and visual pairs, including 69 illustration
      directions and 10 postproduction cards.
- [x] Independent read-only conversion review confirms exact script/visual
      parity and the source-review boundary.
- [x] Focused lint, facts checks, core tests, task-board check and diff check
      run with recorded outcomes.
- [x] The project records its paper duration shortfall and all remaining paid,
      audio, media, final QA and owner gates.

## Steps

- [x] Lock the five approved source hashes and map six chapters, bookends,
      claims and cards into the canonical schema.
- [x] Split only overlong scenes at punctuation, with concatenated scene text
      equal to the approved sentence and no alteration to the original files.
- [x] Add pronunciation candidates with `say_for` binding; obtain separate
      review before treating any reading as approved.
- [x] Add conversion receipt, run checks and independent parity review.
- [x] Prepare a draft PR with `no-auto-merge`; this task covers the project-file
      preparation only, not paid production or publication.

## How to verify

`node docs/videos/story-everyday-seven-bank-c19/build-canonical.mjs`,
`node tools/video/cli.mjs lint --slug story-everyday-seven-bank-c19`,
focused facts and core tests, `npm run check:tasks`, source SHA-256 readback,
and an independent scene/line/card comparison against `script.md` and
`visual-plan.json`.

## Notes

Owner approval binds `script.md` SHA-256
`B4AF0F8A47D57E57D35A86A6092851F0282D52B5B5CA95DD62DFE036D0588E8F`
and `visual-plan.json` SHA-256
`8496FA62BD8BC9DA93F82B2B72F76826CA30FDFB47481C83F47E60038E9E6D50`.
The source matrix and independent v13 review distinguish fictional customer
scenes, company retrospectives, period documents, and 2010 financial figures.
At 250 spoken units/minute, post-hook narration is only 458.16 seconds on
paper; pauses are not pure narration. No C19 paid-pilot quote or approval exists.
The independent read-only conversion review passed, with the c190310a and
c190610a adjacent-edit constraints recorded in the preflight receipt.
