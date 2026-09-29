---
id: 2026-09-28-ai-season-one-final-review
title: Finalize AI season one audio and scene review before publication
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T01:52:53Z
completed_at:
branch: codex/shorts-backend-audit
depends_on: []
scope:
  - docs/ai-video-season-01
---

# Finalize AI season one audio and scene review before publication

## Why

The six AI explainer videos are synthesized graphic review cuts, not accepted publication masters. Preserve the outstanding work explicitly.

## Definition of done

- [ ] Human listening review resolves pronunciation and pacing issues across all eighteen videos.
- [ ] Final scene editing matches the intended storyboards and passes complete audiovisual review.
- [ ] Channel destination and upload settings are confirmed, sources refreshed, and release-checklist.csv reflects actual evidence.

## Steps

- [ ] Restore local exports or rebuild using the package README.
- [ ] Complete listening, scene and publication checks; retain evidence.

## How to verify

Use docs/ai-video-season-01/release-checklist.csv and operations.md. Do not infer approval or successful publication from the existing technical validation receipts.

## Notes

No upload, public release or paid service is authorized by the packaging PR. The one-million-view objective remains unverified. This follow-up is open and unclaimed.

### 2026-09-29 live Shorts review

- Read all 12 current `ai-real-world-*-short-*` final reviews in the production Shorts tab and downloaded the exact review media for independent ffprobe/loudness and nine-frame-per-video visual review. No production review status, settings, upload or schedule was changed.
- All 12 remain pending. All 12 sampled caption baselines extend below the existing y=1600 safe boundary (text bottom about 1610; background about 1630); eight opening titles also extend beyond x=902. Rebuild the vertical layout before approval. The footer around y=1860 is also hidden by the Shorts overlay. Backend overlay inspection confirms the problem on `ai-real-world-05-uneven-abilities-short-1`.
- Seven are below the configured loudness floor of -15 LUFS: `05-uneven-abilities-short-1` (-15.18), `03-machine-internet-short-1` (-15.29), `06-digital-yesman-short-1` (-15.03), `01-image-trust-short-2` (-15.16), `02-confident-errors-short-2` (-15.27), `04-tasks-and-jobs-short-2` (-15.21), `06-digital-yesman-short-2` (-15.16). Prefix each with `ai-real-world-`.
- Two are shorter than the current 25-second setting: `ai-real-world-04-tasks-and-jobs-short-2` is 23.00 seconds; `ai-real-world-06-digital-yesman-short-2` is 24.43 seconds. Treat this as the site's editorial setting, not a YouTube minimum.
- `ai-real-world-05-uneven-abilities-short-1` splits the proper name Gemini across consecutive captions (`Gemi` / `ni Deep Think`). `ai-real-world-01-image-trust-short-2` discusses C2PA provenance credentials but its title calls them AI labels; change the title to describe source credentials accurately.
- All 12 submitted reports lack `check.json` and `verify.json`, fail policy, and lack a full-video link. Do not bypass these using manual approval. The six parent videos are now visibly approved at 08:29-08:30 Asia/Taipei on 2026-09-29, so the old 07:08-07:10 source-not-approved failures are stale; rerun QA rather than re-approve the parents. Parents remain in language production, with no public full-video address visible.
- Historical claims sampled against official pages on 2026-09-29: advanced Gemini Deep Think IMO 2025 gold-level performance; ILO 2025 occupational exposure (not job loss); Thales 2026 report's 53% bot traffic using 2025 data; C2PA provenance does not prove depicted events true. The sampled numerical claims are supported; this does not replace a script-hash-bound verifier or listening review.
- Follow-up: rebuild layout/caption segmentation, normalize the seven tracks, resolve the two short runtimes, repair wording, perform real listening and hash-bound verification, refresh parent/link/policy checks, and resubmit. Review media, exact hashes, browser snapshots and the complete audit are saved outside Git in the dated `shorts-audit-20260929` audit package. No listening or mobile/YouTube playback acceptance is claimed.

### 2026-09-29 owner-authorized Shorts corrections

- Rebuilt all 12 Shorts using the dated native Pillow renderer in `tools/rebuild_shorts.py`; historical media stays unchanged outside Git. Fixed title/cards/footer/caption safety, punctuation wrapping, Gemini segmentation, C2PA title wording, and three phrases flagged by automated narration checks. Original unmodified phrases reused the retained Hanhan WAVs.
- All 12 final videos fully decode and pass actual native integration checks: 71/71 narration phrases, script schemas, SRT timelines, 1080x1920/30fps/H.264/AAC 48kHz, final audio loudness and peaks, final/video/frame hashes, and measured glyph/card bounds. Maximum measured content bottom is y=1362 and caption background bottom is y=1559. Final durations are 26.00-29.97 seconds; the two previously short videos are now 26 seconds.
- Current independently verified scripts have 37 supported claims/editorial boundaries. Final QA now accepts all approved source-video evidence and the measured layout; each cut passes 9/12. The remaining policy item needs owner-decided channel stance; metadata/links need real public parent-video URLs. No fake link or manual approval bypass was used.
- Corrected final reviews were sent to existing backend projects and reloaded to compare video/QA/attachment hashes. All remain pending. The external `shorts-fixes-20260929` package contains the exact final manifest and receipts; repository delivery receipt is `docs/videos/ai-shorts/releases/2026-09-29-corrections.json`.
- This completes the authorized technical/content correction of the 12 Shorts, not the original ticket's human acceptance of all 18 videos. No publication, upload or deployment occurred. Browser playback verification could not complete because of CDP focus timeouts; record reloads used the existing video API client. Human listening and phone/player acceptance remain unchecked.
