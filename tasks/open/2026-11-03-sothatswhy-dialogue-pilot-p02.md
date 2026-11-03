---
id: 2026-11-03-sothatswhy-dialogue-pilot-p02
title: 原來如此事務所對話版試做：P02 雲變午後大雨（所長＋小問）
status: in-progress
priority: P2
area: docs
owner: claude-opus-stw-dialogue
claimed_at: 2026-11-03T07:17:05Z
created_at: 2026-11-03T07:12:15Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - docs/videos/so-thats-why/dialogue-pilot-20261103
  - docs/videos/sothatswhy-p02-cloud-rain
---

# 原來如此事務所對話版試做：P02 雲變午後大雨（所長＋小問）

## Why

站主 2026-11-03 要開始做原來如此事務所的影片：照奇聞檔案局的規則，但開頭不做濃縮、
直接放已核准的原來如此系列片頭動畫，並加一個發問的小孩跟原本的主持人一問一答（站主說「有點像 Tech Signal」）。
這推翻了系列「沒有固定角色、單一旁白」的舊定案，所以先試做一集再決定量產。
企劃、角色分工、畫面規則、treatment 與開拍順序在
[`docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`](../../docs/videos/so-thats-why/dialogue-pilot-20261103/README.md)。

## Definition of done

- [ ] 站主確認對話版形式（角色、分工、`cute-cartoon` 或 `cute-mystery`、Tech Signal 的理解）。
- [ ] P02 一集成片交給站主看（`review-push --gate final`），附實際花費與試做量到的問題。
- [ ] 試做結論寫回企劃頁：要不要量產、主機路線要改什麼（`explainer-series.mjs` 目前固定 `characters: []`）。

## Steps

- [ ] 站主確認企劃頁 §1–§3。
- [ ] 小問的聲音試聽，站主選一個。
- [ ] 撰稿 `docs/videos/sothatswhy-p02-cloud-rain/video.json`（`format: "drama"`、兩個角色、`speaker`、`loops` ≥ 11、`CURIO_MUSIC`、`subtitles.burn_in: true`）。
- [ ] 另一個代理逐主張查核（企劃頁 §7）→ 盲評 `narrative` → `lint` 0 錯誤 → `script.md` 給站主。
- [ ] 角色設定圖（每角色 3 張）→ 站主選。
- [ ] 旁白兩個聲音 → `check-audio` → 站主聽。
- [ ] 整集插圖一次報價、一次授權 → `keyframes --takes 3` → 分鏡給站主。
- [ ] `branding --pull --series sothatswhy`、片頭 `intro_at: "start"` → 配樂 → 合成 → 品管 → 成片給站主。

## How to verify

`node tools/video/cli.mjs lint --slug sothatswhy-p02-cloud-rain` 0 錯誤；`narrative` 每題通過；
成片開頭是 11.9 秒系列片頭、第一句是小問的問題；站主在 `/admin/videos` 看過成片。

## Notes

- 2026-11-03：只做了企劃，沒有付任何費用。repo 裡找不到「Tech Signal」的資料，企劃照「一個大人講解、一個小孩代替觀眾發問」理解，等站主確認。
- MiniMax `image-01` 讀不懂多人互動，兩個角色一律正反打不同框；小問兼任內容插圖裡那「一個人」。
