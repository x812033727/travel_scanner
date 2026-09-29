---
id: 2026-09-29-video-illustrated-slides-media
title: Illustrated slides: keyframes and music stages run for slides videos
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-29T09:14:22Z
completed_at:
branch:
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

- [ ] `keyframes --slug` 對插圖投影片能跑，同樣的快取、judge、帳本、單支上限、STOP、聯絡表；look 關卡只在 `hasCast(doc)` 時查。
- [ ] 投影片的 `keyframes/manifest.json` 綁 `look_hash + pictures_hash`；`visual_hash` 變了不重判。
- [ ] `keyframeRubric` 在 `!burnIn(doc)` 時沒有 `subtitle_band`；`style` 準則改成「符合 look 的畫風描述」。
- [ ] `music --slug` 對有 `music` 的任何格式能跑；`music.track` 走 `_music/` 不呼叫伺服器。
- [ ] `stages.mjs` 在 `format === "slides"` 時讀 `status.slides_enabled`／`slides_image`／`slides_max_usd_per_video`，沒有就退回漫劇欄位。
- [ ] dry-run 印最壞成本（× 最多 N 次）。
- [ ] 漫劇 fixture 的既有測試不變。

## Steps

- [ ] `keyframes.mjs` 守門、關卡、manifest 綁定、rubric、dry-run。
- [ ] `music.mjs` 守門。
- [ ] `stages.mjs` 格式感知的 status／價格／上限。
- [ ] 測試：`look-keyframes.test.mjs`、`media.test.mjs`。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs keyframes --file tools/video/core/fixtures/illustrated/video.json --dry-run --workdir <tmp>
```

## Notes

- 每小時 240 次生圖、360 次 judge（`admin_api.py:67-72`）：一支 75 張最多 225 次，工人一小時只跑一支，第二支 exit 4 等下一輪。
- `look.style_frames` 可給 3–4 張定調圖當 style reference，讓 60–75 張畫風一致。
