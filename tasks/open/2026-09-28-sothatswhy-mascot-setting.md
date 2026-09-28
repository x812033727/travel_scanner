---
id: 2026-09-28-sothatswhy-mascot-setting
title: So That's Why: design the original mascot (the director) and the 3-second opener
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T06:50:53Z
created_at: 2026-09-28T06:00:00Z
completed_at:
branch: claude/knowledge-series-planning-v84n79
depends_on: []
scope:
  - docs/videos/so-thats-why/mascot.md
---

# So That's Why: design the original mascot (the director) and the 3-second opener

## Why

「原來如此事務所」每集片頭、章節卡與結尾蓋章都有吉祥物「所長」，關鍵影格要拿它的設定圖當參考才會跨 100 集一致。還沒有造型、提示詞與設定圖。

## Definition of done

- [x] `docs/videos/so-thats-why/mascot.md`：外觀描述、英文提示詞、色盤、禁止事項（不像任何既有角色或頻道吉祥物，不用黑貓）。
- [ ] 站主從候選設定圖選定一張（圖檔留在 repo 外，文件記雜湊與日期）。
- [x] 片頭 3 秒（推門、蓋章「受理」）與結尾蓋章「原來如此」的分鏡。

## Steps

- [x] 寫三個造型方向給站主選。
- [ ] 生成設定圖、站主選定、記錄。

## How to verify

站主在後台核准設定圖；`mascot.md` 記錄的雜湊與存檔一致。

## Notes

- 2026-09-28：`mascot.md` 寫好三個方向（A 水豚、B 郵差鴿、C 燈泡機器人，推薦 A）、系列 `look`（`preset: custom`，`style`／`negative` 已對過 `tools/video/core/drama.mjs` 的 LOOK_KEYS）、片頭與結尾分鏡。等站主選方向；選定後才能跑 `look` 生設定圖，要漫劇設定開啟與圖片金鑰（主機）。
