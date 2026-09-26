---
id: 2026-09-26-video-drama-pilot
title: Video drama T10: pilot episode from a public-domain Shanhaijing tale, end to end
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-26T01:53:47Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-automation
  - 2026-09-26-video-drama-skill-docs
  - 2026-09-26-video-drama-media-web-routes
scope:
  - docs/videos/jingwei-fills-the-sea
  - docs/videos/lexicon.json
---

# Video drama T10: pilot episode from a public-domain Shanhaijing tale, end to end

## Why

第一支漫劇：公有領域的山海經故事（精衛填海），2–4 分鐘、16:9、電影感 3D 寫實、燒錄繁中字幕＋五語 CC。目的除了上架，還要校準門檻（`KEYFRAME_MIN_PSNR`、judge 分數、重做率）、量實際花費，並確認正式主機的地區沒有被 Gemini 的影片功能擋住。站主 2026-09-26 決定先不設預算上限，第一支用最好的模型做。

## Definition of done

- [ ] `docs/videos/jingwei-fills-the-sea/` 有 brief、video.json、claims、verify、i18n；lint 零錯誤。
- [ ] 站主在 `/admin/videos` 選過角色設定圖與分鏡；旁白核准；`checks.json` 全過；每鏡 identity ≥7；沒有凍格 >2 秒；−14 LUFS。
- [ ] 站主看完 720p 成片，認為畫面與節奏在參考影片之上；上架包含揭露勾選。
- [ ] 實際花費、每鏡秒數、重做率、地區測試結果記進票的 Notes，並轉交給持有 `docs/videos/DRAMA.md` 的票寫進成本節。

## Steps

- [ ] 企劃（故事前提、角色、看點）→ 站主選大綱 → 撰稿與連貫性查核 → `look` → 選圖 → `tts` → `keyframes` → 分鏡 → `render` → `clips`（第一鏡先單獨跑，測地區）→ `music` → `assemble` → 翻譯與 `captions` → 成片送審 → `package`。

## How to verify

```bash
node tools/video/cli.mjs status --slug jingwei-fills-the-sea
node tools/video/cli.mjs clips --slug jingwei-fills-the-sea --dry-run
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
