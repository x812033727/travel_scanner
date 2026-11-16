---
id: 2026-11-14-sothatswhy-p12-dialogue-qr-code-damage
title: "sothatswhy P12 dialogue: QR Code damage and error correction"
status: done
priority: P2
area: docs
owner: antigravity-sothatswhy-p12
claimed_at: 2026-11-14T04:05:46Z
created_at: 2026-11-14T04:05:32Z
completed_at: 2026-11-16T00:08:36Z
branch: video/sothatswhy-p12-qr-code
depends_on: []
scope:
  - docs/videos/sothatswhy-p12-qr-code
  - docs/videos/lexicon.json
---

# sothatswhy P12 dialogue: QR Code damage and error correction

## Why

Produce episode P12 (〈QR Code 缺一塊，為什麼還讀得出來？〉, slug `sothatswhy-p12-qr-code`) of the 原來如此事務所 (`sothatswhy`) dialogue explainer series, following all 2026-11-14 series and explainer rules, with self-generated theatrical-light rich-gouache V2 keyframes imported via `keyframes import --provider external --usd 0` (no MiniMax image generation), distinct 2.5-head chibi character sheets (`chief-canon-v2.png` + `kid-canon-v2.png`) + `45%–65%` `nobody: true` mechanism/object shots, Gemini `zh-TW` voices (`Sulafat` + `Leda`), MiniMax 8-locale dubs (`en,ja,ko,es,pt,id,vi,th`), post-assembly independent audience review, and full Google Drive backup before `review-push --gate final`.

## Definition of done

- [x] `brief.md` and `claims.md` written from firsthand reading of DENSO WAVE (`qrcode.com`) and Reed-Solomon teaching sources (`checked_on: 2026-11-14`), respecting round-2 material boundaries (no ISO-only mask/format/timing claims).
- [x] `build_scenes.py` -> `video.json` and `script.md` pass `lint` with 0 errors, `pauses: {line_ms: 0, scene_ms: 150}`, `still_motion: "beat"`, multi-line scenes, <20s to core question after intro, independent fact-check (`verify-1.md`), and blind 14-question `narrative` panel (`no_orphans` included).
- [x] `zh-TW` narration synthesized with Gemini (`Sulafat` / `Leda`), measured >= 4.4 chars/s (`5.11 chars/s`), passes `check-audio`.
- [x] Series character sheets reused (`look` approved with 0 MiniMax calls); all 80 shot keyframes generated externally (`generate_image`, 16:9, text-free theatrical-light rich gouache, `43/80 = 53.75%` 2.5-head chibi V2 character shots + `37/80 = 46.25%` `nobody: true` object/mechanism shots) and imported via `keyframes import --provider external --usd 0`, passing 2x quadrant inspection and storyboard scorecard (`68/70` in `review/scorecard-2-storyboard.md`).
- [x] Assembled with `sothatswhy` bookends (`mokaair-sothatswhy-bookends-v3-endscreen`, `82263266d425`) and `sothatswhy-bed-r2.m4a` (`final.mp4 sha256 b9a7b1839d31`, `18,187 frames`, `606.26 s`, `-14 LUFS`), passes independent post-assembly audience review (`9.13/10` average, `64.3/70` technical in `review/audience-review.md` with all thumbnail wrap findings fixed) and `qa` (`11/11`), 8 locales translated with series title suffixes, 11 thumbnails rendered and checked, and 8 dubs synthesized with MiniMax (`dub --provider minimax` + `check-audio --locale`).
- [x] Full workdir + `_repo_docs/` snapshot backed up to Google Drive `AI/備份/AI劇/原來如此事務所/數位科技與通訊工程/P12/製作檔/sothatswhy-p12-qr-code/` (folder ID `1kMdSO7TbqNqoTayAhSlB5c7Xo_Kln7EO`, `0` differences) and `review-push --slug sothatswhy-p12-qr-code --gate final` submitted to `/admin/videos`.

## Steps

- [x] Verify paired video tool token, series character sheets, `_branding`, and `sothatswhy-bed-r2.m4a`.
- [x] Write `brief.md`, `claims.md`, `build_scenes.py`, `video.json`, `script.md`; run `lint`, independent `verify-1.md`, and blind `narrative` 14-question panel.
- [x] Run `tts` (Gemini) + `check-audio`; verify speech rate >= 4.4 chars/s (`5.11 chars/s`).
- [x] Run `look` (reusing series sheets) + generate & import all 80 V2 keyframes (`keyframes import --provider external --usd 0`) + independent 2x quadrant inspection (`68/70`).
- [x] Run `render`, `clips`, `assemble`, 8-locale MiniMax `dub` + `check-audio --locale`, `captions`, post-assembly independent audience review (`9.13/10`), and `qa` (`11/11`).
- [x] Back up full workdir + `upload/` + `_repo_docs/` snapshot to Google Drive (`1kMdSO7TbqNqoTayAhSlB5c7Xo_Kln7EO`), pull owner `final` approval, run `package` (`4/4` passed, `metadata.json sha256 f8c6814d945d`), and submit `review-push --gate publish` (`pending`) and `review-push --gate languages` (`pending`, 34 files verified via `review-files --dry-run --gate languages`) to `/admin/videos`.
- [x] After owner approves `publish` + `languages` on `/admin/videos` and links YouTube URL: run `npm run tasks -- done 2026-11-14-sothatswhy-p12-dialogue-qr-code-damage`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug sothatswhy-p12-qr-code
node tools/video/cli.mjs qa --slug sothatswhy-p12-qr-code
node tools/video/cli.mjs review-files --slug sothatswhy-p12-qr-code --dry-run --gate languages
npm run check:tasks && npm run test:docs-videos
```

## Notes

- **2026-11-15 Completed**: `final` (`2026-11-15T03:44:13Z`), `languages` (`2026-11-15T04:18:08Z`), and `publish` (`2026-11-15T04:18:12Z`) all approved on `/admin/videos`; uploaded and synced to YouTube as `2ouKXqeC05A` (`https://youtu.be/2ouKXqeC05A`, 9-locale metadata + 9-locale CC captions + thumbnail synced `done` at `2026-11-15T11:20:38Z`; 8-locale dubs & localized thumbnails recorded).
- Google Drive full production + `upload/` + final `approvals.json` backup verified (`2,994` files, `0` differences) at `AI/備份/AI劇/原來如此事務所/數位科技與通訊工程/P12/製作檔/sothatswhy-p12-qr-code/` (Drive folder ID `1kMdSO7TbqNqoTayAhSlB5c7Xo_Kln7EO`).
- Pairing token approved by owner (`antigravity-sothatswhy`).
- Shared `docs/videos/lexicon.json` has `"Code": "扣德"`, so `"QR Code": "Q R Code"` (plus `"QR": "Q R"`, `"CD": "C D"`, `"Reed-Solomon": "Reed Solomon"`) is appended so longest-match substitution reads `"QR Code"` naturally instead of `"扣德"`.
