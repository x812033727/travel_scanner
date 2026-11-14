---
id: 2026-11-13-produce-curio-m17-1816-year-without
title: Produce Curio M17 (1816 Year Without a Summer and Frankenstein) with agent-generated illustrations, Gemini zh-TW and MiniMax 8-language dubs
status: review
priority: P1
area: docs
owner: antigravity-curio-m17
claimed_at: 2026-11-13T17:37:25Z
created_at: 2026-11-13T17:36:29Z
completed_at:
branch: antigravity/curio-m17
depends_on: []
scope:
  - docs/videos/curio-m17
  - docs/videos/lessons/curio.md
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
---

# Produce Curio M17 (1816 Year Without a Summer and Frankenstein) with agent-generated illustrations, Gemini zh-TW and MiniMax 8-language dubs

## Why

Owner requested producing one complete 奇聞檔案局 (`curio-*`) episode selected by the agent, using agent-generated illustrations (`generate_image` + `keyframes import --provider external --usd 0`, never MiniMax `image-01`), Gemini `Sulafat` for `zh-TW` narration (`>= 4.4` chars/s), MiniMax Speech for all 8 foreign dub tracks (`en`, `ja`, `ko`, `es`, `pt`, `id`, `vi`, `th`), and all standard 奇聞檔案局 rules. Selected topic: **M17** (`docs/videos/history-curiosity/topic-checks/M17.md`) — 1816 Year Without a Summer, the 1815 Mount Tambora eruption, and the origin of *Frankenstein*.

## Definition of done

- [x] `docs/videos/curio-m17/` contains `brief.md`, `video.json`, `script.md`, `claims.md`, `verify-1.md`, `NOTES.md`, `story-lexicon/`, and `i18n/{en,ja,ko,es,pt,id,vi,th}.json` passing `lint` with 0 errors.
- [x] `zh-TW` Gemini narration synthesized (`4.94` bare chars/s `>= 4.4`), `check-audio` + ear audit clean.
- [x] All 88 shot keyframes generated via agent `generate_image` (zero MiniMax `image-01`), inspected at 2× zoom, and imported via `keyframes import --provider external --usd 0`.
- [x] Assembled with `v4-endscreen` branding, Lyria background music, switchable `zh-TW` + 8-locale `.srt` CC subtitles (`burn_in: false` per 2026-11-04 curio rule in `tools/video/core/curio.mjs`), Layout E localized thumbnails, and 8 MiniMax foreign dubs (`en`, `ja`, `ko`, `es`, `pt`, `id`, `vi`, `th`).
- [ ] `qa` passes 11/11 checks, `package` built (4/4), full working files backed up to Google Drive `AI/備份/AI劇/奇聞檔案局/M17/製作檔/` with 0 diffs, review gates pushed to `/admin/videos`, and owner approves gates on `/admin/videos`.

## Steps

- [x] Initialize per-video lexicon snapshot (`docs/videos/curio-m17/story-lexicon/`) to avoid colliding with shared `docs/videos/lexicon.json`.
- [x] Write `brief.md`, `video.json`, `claims.md`; pass `lint` (0 errors, 0 warnings), independent fact-check (`verify-1.md`, 20/20 CONFIRMED), and two-reader blind `narrative` panel (14/14 PASS).
- [x] Synthesize `zh-TW` Gemini narration (`Sulafat`), verify speaking rate `4.94` bare chars/s (`>= 4.4`, unwrapped body `689.4` s / `11:29`), and audit `check-audio` clips by ear (`l065` `重種` fixed via `say`/`say_for`).
- [x] Generate all 88 `16:9` `cute-mystery` illustrations via `generate_image`, inspect quadrant crops, and import via `keyframes import --provider external --usd 0` (`US$0.00`).
- [x] Translate & independently review 8 locales (`i18n-sheet` → `i18n-merge`), render 9 Layout E thumbnails, build clips, loop Lyria music (`US$0.08` total spend), assemble `final.mp4` (`11:55.4`, `-14 LUFS`, `sha256 1627fc07ccab`), and synthesize + ear-audit 8 MiniMax dubs + 9 `.srt` captions.
- [x] Run `qa` (11/11 PASS) + `package` (4/4 PASS, `metadata.json` `sha256 ff1be733cc04`, `#奇聞檔案局` + `#ปีที่ไร้ฤดูร้อน` hashtags verified), redraw `s049` (1816 brass chamberstick) & `s083` (Sumbawa/Luzon globe without text), trim `th` description to `4,217` UTF-8 bytes, record lessons in `docs/videos/lessons/curio.md`, back up to Google Drive (`0` diffs), push review gates to `/admin/videos`, and run repo checks.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-m17
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs qa --slug curio-m17 --workdir /home/antigravity/mokaair-work/videos
npm run test:docs-videos && npm run check:tasks
```

## Notes

- Used `initializeStoryLexicon` (`13ae670bb0c859c87b0ea4a0f51dca9a393305feb16471cc461bd5efaf6c2841`) before writing `video.json` so all Latin terms resolve inside `docs/videos/curio-m17/story-lexicon/` without touching `docs/videos/lexicon.json`.
- Key hashes & metrics: `script.md` `sha256 dcdeade65c3f`; `keyframes/manifest.json` `sha256 c4fddb08356d` (88 external `cute-mystery` stills including redrawn `s049-import-2.png` `sha256 b89c5db43297` and `s083-import-2.png` `sha256 d6fb7d6adaca`, `US$0.00`); `timeline.json` `sha256 7003ef057e40` (`4.94` bare chars/s, `689.4` s body); `final.mp4` `sha256 1627fc07ccab` (`21,463` frames / `715.434` s, `-14 LUFS`, true peak `-1.9 dBFS`); `upload/metadata.json` `sha256 ff1be733cc04` (`th` description `4,217` UTF-8 bytes, `#ปีที่ไร้ฤดูร้อน` preserved via `\p{M}` fix in `tools/video/core/metadata.mjs`); total media ledger spend `US$0.08` (single looped Lyria music track).
- Google Drive backup: `AI/備份/AI劇/奇聞檔案局/M17/製作檔/` (`M17` folder `1aQ90i04NG1x2xi7nT4eQgBWt1hpt8Ap_`, `製作檔` folder `1hJfI7AA2gD3A_QFuzTU2PAFvkgVryUOH`, `curio-m17` `1_x9w_wv2ozsdWoZBDY_Kxaud8zumsOe6` [`2,502` local files], `docs-curio-m17` `1qwaMz54q_vf63AJOWklolTBv2dkEtJVe` [`17` files]) — initial tree verified by subagent `4a564df72527eefa7f11129c32ce9d43`, and follow-up update independently verified by subagent `6a964ba998e6389dac726321214a37d1` (`0` missing, `0` duplicates, `90 / 90` modified files downloaded & byte-for-byte MD5 + SHA-256 verified). Note: `gdrive readonly ls --json` omits `md5Checksum`, so custom `gdrive` backup verifiers hash downloaded content rather than relying on `ls --json`.
- Hand-pushed review gates (`outline`, `script`, `storyboard`, `audio`, `final`, `publish`) sent to `/admin/videos` (`hand_pushed = true` waits for owner approval on `/admin/videos`). Ticket stays in `review` (PR labeled `no-auto-merge`) until owner approves `/admin/videos` gates and confirms merge.
