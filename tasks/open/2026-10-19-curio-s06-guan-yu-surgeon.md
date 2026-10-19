---
id: 2026-10-19-curio-s06-guan-yu-surgeon
title: Curio S06 Guan Yu's unnamed surgeon and the later Hua Tuo scene
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s06
claimed_at: 2026-10-19T20:22:22Z
created_at: 2026-10-19T20:22:22Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s06
---

# Curio S06 關羽的無名醫生與後來的華佗場景

## Why

站主要求持續製作 S 軸歷史影片。《三國志》確有關羽刮骨治傷記載，但並未寫醫生姓名與手術年份；《三國演義》第七十五回把華佗、馬良對弈與樊城戰事寫進同一幕。題庫原稿把「醫生不是華佗」寫成確定句，製作前須拆開史書可證與小說編排。

## Definition of done

- [x] 用固定版本原文建立史書、小說、華佗與曹沖年表的核對底稿。
- [ ] 完成 8–10 分鐘史料可核的企劃、逐句劇本、畫面與獨立來源覆核及盲讀。
- [ ] 媒體製作、音訊與成片品管；待目前 S23、S26 媒體佇列與服務容量安排。

## Steps

- [x] 確認沒有其他 S06 認領與同名影片，認領窄 scope。
- [x] 記錄《三國志》關羽左臂、無名醫生、未記手術年份；《三國演義》樊城右臂、華佗、馬良對弈。
- [x] 核對《三國志》華佗死於曹沖之前，曹沖卒於建安十三年；只用這條年表判定**小說放在樊城之役的華佗場景**年代不合，不推定史書無年份的治療者身分。
- [x] 依站主的持續製作委託採用 A 案，完成 `brief.md`；S26 已有新稿在盲讀佇列，S23 圖像仍等共享額度。
- [ ] 撰寫 S06 逐句劇本、分鏡與來源表，送獨立審讀。

## How to verify

閱讀 `docs/videos/curio-s06/research.md` 的固定版連結與原文定位；後續用 `node tools/video/cli.mjs lint --slug curio-s06`、獨立來源覆核及全新盲讀。

## Notes

本票僅改 `docs/videos/curio-s06`；不改 `topics.json` 或其他集。史書內容為傳世文字，不把晚出小說細節拍成歷史目擊。插圖避免傷口與血畫面。S06 尚未啟用付費媒體。
