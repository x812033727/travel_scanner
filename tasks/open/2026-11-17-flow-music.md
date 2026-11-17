---
id: 2026-11-17-flow-music
title: Flow Music 配樂庫：剪短音樂與音效、試聽、接進產線
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-17T16:01:15Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/explainer-series/music-library
---

# Flow Music 配樂庫：剪短音樂與音效、試聽、接進產線

## Why

站主 2026-11-17 要一套奇聞檔案局與原來如此事務所共用的底樂、短音樂、音效，存在雲端硬碟以後直接用。
202 首（含第三波的轉場與情境音效）已經用 Flow Music（Lyria 3.5）生成並備份（做法與結果見
[`docs/videos/explainer-series/music-library/README.md`](../../docs/videos/explainer-series/music-library/README.md)），
但只有底樂能直接放進 `_music/` 用。短音樂要 3–10 秒卻都生成約 1 分鐘，音效也是約 1 分鐘、多段聲音夾靜音，
還不能當產線的音效組用；也沒有人聽過任何一首。

## Definition of done

- [ ] 每首底樂聽過一次，`manifest.json` 標上「可用／不用」與理由（有人聲、有爆點、搶旁白的主旋律都算不用）。
- [ ] 每段短音樂剪出要用的那幾秒，存成 `*-cut.m4a`，manifest 記剪點。
- [ ] 每個音效切出單一一聲，各系列整理成一組第 2 版音效組（`_sfx/curio-flow/`、`_sfx/sothatswhy-flow/`），跑過 `assemble sfx-measure`。
- [ ] 雲端硬碟兩個 `flow-music-20261117/` 資料夾更新，`todrive.sh --check` 或 sha256 比對 0 差異。
- [ ] 決定用這套配樂的影片上傳時 AI 揭露怎麼勾（`qa/checks.mjs` 的 `disclosureDecision` 看不出 `_music/` 的檔是 AI 做的）。

## Steps

- [ ] 從雲端硬碟 `AI劇/奇聞檔案局/_共用/製作檔/curio-music-library/flow-music-20261117/` 與
      `AI劇/原來如此事務所/_共用/製作檔/sothatswhy-music-library/flow-music-20261117/` 取檔。
- [ ] 試聽並標記（可派代理用 Gemini 聽、寫理由，站主抽聽）。
- [ ] 用 ffmpeg `silencedetect` 找切點，剪短音樂與音效。
- [ ] 寫音效組 manifest（source 寫「Google Flow Music（Lyria 3.5），帳號 twocypress84」）並量測。
- [ ] 回傳雲端硬碟並核對。

## How to verify

`node tools/video/cli.mjs assemble sfx-measure --set curio-flow` 印出 manifest 的 sha256；用一支測試影片
`assemble` 後 `checks.json` 的 `metrics.sfx.min_bed_margin_db` ≥ 6。

## Notes

- `sothatswhy-sfx-splash` 整合響度 −44.5 LUFS，可能幾乎是靜音。
- WAV 原檔還在 Flow Music 上，`manifest.json` 的 `flow_music_id` 可以用 `/__api/download/audio/<id>?format=wav` 在已登入的頁面裡重抓。
