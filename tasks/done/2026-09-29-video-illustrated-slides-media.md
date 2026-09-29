---
id: 2026-09-29-video-illustrated-slides-media
title: Illustrated slides: keyframes and music stages run for slides videos
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:26:18Z
created_at: 2026-09-29T09:14:22Z
completed_at: 2026-09-29T09:29:07Z
branch: claude/sharp-brown-dh2x95
depends_on:
  - 2026-09-29-video-illustrated-slides-schema
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/music.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/media.test.mjs
---

# Illustrated slides: keyframes and music stages run for slides videos

## Why

插圖投影片（票 `2026-09-29-video-illustrated-slides-schema`）的圖與配樂要由既有的媒體階段做，但 `media/keyframes.mjs:103` 與 `media/music.mjs:45` 用 `isDrama` 擋掉非漫劇；`keyframes.mjs:119-129` 的 look 關卡用 `narratorOnly`（也要 `isDrama`），`:165` 的 manifest 綁 `visual_hash`（改任何卡片文字就整批重判，每張 judge US$0.01）；rubric 有 CC-only 影片不需要的 `subtitle_band`。

## Definition of done

- [x] `keyframes --slug` 對插圖投影片能跑，同樣的快取、judge、帳本、單支上限、STOP、聯絡表；look 關卡只在 `hasCast(doc)` 時查。
- [x] 投影片的 `keyframes/manifest.json` 綁 `look_hash + pictures_hash`；`visual_hash` 變了不重判。
- [x] `keyframeRubric` 在 `!burnIn(doc)` 時沒有 `subtitle_band`；`style` 準則改成「符合 look 的畫風描述」。
- [x] `music --slug` 對有 `music` 的任何格式能跑；`music.track` 走 `_music/` 不呼叫伺服器。
- [x] `stages.mjs` 在 `format === "slides"` 時讀 `status.slides_enabled`／`slides_image`／`slides_max_usd_per_video`，沒有就退回漫劇欄位。
- [x] dry-run 印最壞成本（× 最多 N 次）。
- [x] 漫劇 fixture 的既有測試不變。

## Steps

- [x] `keyframes.mjs` 守門、關卡、manifest 綁定、rubric、dry-run。
- [x] `music.mjs` 守門。
- [x] `stages.mjs` 格式感知的 status／價格／上限。
- [x] 測試：`look-keyframes.test.mjs`、`media.test.mjs`。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs keyframes --file tools/video/core/fixtures/illustrated/video.json --dry-run --workdir <tmp>
```

## Notes

- 每小時 240 次生圖、360 次 judge（`admin_api.py:67-72`）：一支 75 張最多 225 次，工人一小時只跑一支，第二支 exit 4 等下一輪。
- `look.style_frames` 可給 3–4 張定調圖當 style reference，讓 60–75 張畫風一致。

- 2026-09-29：做完。`stages.mjs` 加 `SLIDES_FORMAT`、`choiceFor`、`capFor`，`statusProblem`／`imagePrice`／`chosenModel` 多一個 `format` 參數，`Stage` 多 `format`；伺服器有 `slides_enabled`／`slides_image`／`slides_max_usd_per_video` 時投影片用自己的，沒有就照漫劇的（票 `2026-09-29-video-slides-media-api` 補伺服器端）。`keyframes.mjs` 的守門改 `hasPictures`、look 關卡只在 `hasCast`、投影片的 manifest 綁 `pictures_hash`、rubric 在不燒錄時沒有 `subtitle_band`、沒有角色時 style 問題改問 look 的描述；dry-run 印最多 N 次的上限。`music.mjs` 去掉 `isDrama`。
- 觀察：綁定變了（改 camera）會重走每個 shot，但快取直接回沒變的圖、不打伺服器，只有 judge 各再算一次 US$0.01。
