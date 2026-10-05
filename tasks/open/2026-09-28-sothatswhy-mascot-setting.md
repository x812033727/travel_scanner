---
id: 2026-09-28-sothatswhy-mascot-setting
title: "So That's Why: series look and the 3-second opener (no mascot)"
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T06:00:00Z
completed_at:
branch: claude/knowledge-series-planning-v84n79
depends_on: []
scope:
  - docs/videos/so-thats-why/look.md
---

# So That's Why: series look and the 3-second opener (no mascot)

## Why

「原來如此事務所」100 集要一眼認得出是同一個系列。站主 2026-09-28 決定不用吉祥物，所以辨識度只能靠固定畫風、色盤與片頭、結尾的蓋章動作；這些要先定好，每集的 `look` 與片頭才能重用。

## Definition of done

- [x] `docs/videos/so-thats-why/look.md`：系列 `look`（扁平插畫、色盤、negative 擋文字與吉祥物）、人物與 logo 的畫法規則、片頭 3 秒、結尾蓋章、章節卡。
- [ ] 片頭三張關鍵影格生成，站主確認；檔名與 SHA-256 記在 `look.md` 的「選定紀錄」（圖檔留在 repo 外）。

## Steps

- [x] 寫 `look.md`。
- [ ] 主機開啟漫劇設定與圖片金鑰後，用 `look.md` 的 `look` 與片頭分鏡生成三張關鍵影格。
- [ ] 站主確認，記雜湊。

## How to verify

站主看過三張片頭關鍵影格；`look.md` 記錄的雜湊與存檔一致。

## Notes

- 2026-09-28：第一版寫了吉祥物「所長」的三個造型方向（水豚、郵差鴿、燈泡機器人）。站主回覆「不用所長」，所以刪掉 `mascot.md`、改寫成 `look.md`，片頭改成無人的門、信與印章。id 保留不改，因為 `2026-09-28-sothatswhy-pilot-3` 依賴它。
- `look` 的 `style`／`negative`／`candidates` 已對過 `tools/video/core/drama.mjs` 的 LOOK_KEYS；`push-in`、`drift` 是 `tools/video/assemble/drama.mjs` 的運鏡關鍵字。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus (since 2026-09-28T06:50:53Z) was stale and is released so it stops locking its scope. Landed: #904 #950 #962. Still open: Generate three opener keyframes after the host enables drama settings and image key; Owner confirms keyframes; record filenames and SHA-256 in look.md.
