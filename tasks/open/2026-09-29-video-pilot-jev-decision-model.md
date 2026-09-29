---
id: 2026-09-29-video-pilot-jev-decision-model
title: Pilot the first illustrated storytelling video: Jev, the model that only decides
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-29T09:14:25Z
completed_at:
branch:
depends_on:
  - 2026-09-29-video-storytelling-prompts
scope:
  - docs/videos/jev-decision-model-explained
  - docs/videos/ILLUSTRATED.md
---

# Pilot the first illustrated storytelling video: Jev, the model that only decides

## Why

計畫的每個數字（成本、節奏、judge 一次過的比例、站主審片分鐘數）都是估的；第一支插圖說書影片要拿真實數字，並與 Gary Chen 的參考片（`2mtn-Qp59y4`，同題）並排比較。現有 10 支的資料夾都在別的票的 scope 裡，所以新開一支。

## Definition of done

- [ ] `docs/videos/jev-decision-model-explained/`：brief（站主觀點、觀眾看完能做到的事、每個數字在當天官方頁查核：TypeSafe AI 的 Jev、193.6×／444.6×、RLCD、輸出 token 免費、每百萬輸入 token 約 US$0.042、Diogo Almeida）→ video.json（說書式、shot 每 5–8 秒）→ 旁白 → 插圖（Flash、自動核准）→ 合成 → CC → qa → 上架包。
- [ ] 驗收：鉤子 ≤20 秒；≥2 個「你以為…其實…」；每章結尾是問題；無狀態 >8 秒、平均 ≤6 秒、share ≥ 0.5；shot 溶接、章節硬切、單狀態卡片漂移；床 ≤ −24 LUFS、成片 −14 LUFS；音效不搶戲；畫面無燒錄字；媒體花費 ≤ US$15。
- [ ] `ILLUSTRATED.md` 的數字表：插圖張數、重做次數、judge 一次過比例、分鐘數、站主審成片分鐘數、費用。
- [ ] 站主看過並決定 10 支舊片重做（`restyle`＋加圖）或照舊上架。

## Steps

- [ ] 在 `/admin/videos` 發起投影片影片，題目「爆紅的 Jev 不聊天只做決定：快 200 倍、便宜 400 倍是真的嗎？」。
- [ ] 走完全自動路線，每一步記數字。
- [ ] 寫回 `ILLUSTRATED.md`。

## How to verify

`node tools/video/cli.mjs status --slug jev-decision-model-explained` 依序出現 keyframes drawn → storyboard approved → frames rendered → music generated → video assembled → final video approved；`qa` 的 pace 項印最長、平均、share；`media-status` 印帳本。

## Notes

站主第 0 期要先做：後台貼說書式 `voice.style` 與常設指示；工人主機放 `_music/`、`_sfx/` 授權檔與 manifest；打開 `slides_media_enabled`（或過渡期的 `drama_enabled`＋系列 `image_model`）。
