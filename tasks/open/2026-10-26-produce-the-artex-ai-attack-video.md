---
id: 2026-10-26-produce-the-artex-ai-attack-video
title: Produce the ARTEX AI attack video: the keys left lying around (artex-ai-attack-leftover-keys)
status: in-progress
priority: P2
area: docs
owner: claude-artex-video
claimed_at: 2026-10-26T23:27:20Z
created_at: 2026-10-26T23:27:16Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - docs/videos/artex-ai-attack-leftover-keys
  - docs/videos/reference-study-20261026-ai-news
---

# Produce the ARTEX AI attack video: the keys left lying around (artex-ai-attack-leftover-keys)

## Why

On 2026-10-26 the owner asked for a new video topic and chose the ARTEX group from the week's
YouTube search (`docs/videos/reference-study-20261026-ai-news/README.md`). Microsoft (10-21),
GMO (10-19), 91APP (10-22) and the Ministry of Digital Affairs' security office (10-21) all
describe AI-driven attacks that did not open a new hole: they used keys left lying around (apps
already granted access, a database key in GitLab, long-lived plaintext credentials). The news
channels covered who attacked whom; nobody gave viewers a check they can run. This video does.

## Definition of done

- [ ] The owner has chosen an outline from `brief.md`.
- [ ] `video.json`, `claims.md` and `loops` pass `lint`; two verifier passes recorded.
- [ ] Narration, final cut and publish package approved on the site; the owner uploads.

## Steps

- [x] Search this week's YouTube groups and write the research record.
- [x] Open the official sources and record them under the workdir's `_tools/sources/`.
- [x] Run the git-history demo (2026-10-26, git 2.43.0) and keep its transcript.
- [x] Write `brief.md` with three outlines.
- [ ] Owner picks the outline (`review-push --gate outline`).
- [ ] Script, verify, narrate, render, publish package.

## How to verify

`node tools/video/cli.mjs status --slug artex-ai-attack-leftover-keys` names the next step.

## Notes

- Workdir (outside the repo): the session scratchpad's `artex/workdir/artex-ai-attack-leftover-keys/`,
  with `_tools/sources/` (page HTML and text) and `_tools/run/` (`run.sh`, `transcript.txt`).
- Zeabur's October report does not mention ARTEX or AI tooling: it may appear only as a parallel
  example of long-lived keys, never as linked to ARTEX. Taiwan's July AI attack (security office)
  names no tool either.
- Still to open before writing: the security office's own press release on moda.gov.tw (only the
  iThome report was read), and CrowdStrike's Korean-bank write-up if outline B is chosen.
- GMO's own numbers are about 20 companies on one host plus 6 more hosts; "about 80" is a media figure.

- 2026-10-28: all 8 dubs made (two retake rounds, then rewording in 7 locales; about 17 lines stay flagged as transcription spelling only: pt tá/está, id udah/client, th ค่ะ, ja アプリの資格情報 kept as the Google page name). 8 locale thumbnails fitted. Package 4/4; languages gate pushed — waiting on the owner (upload the dub tracks in Studio, then tick the dubs-uploaded box). Publish card still needs the Studio URL.
