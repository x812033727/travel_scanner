---
id: 2026-10-22-independently-verify-expanded-c08-line-sources
title: Independently verify expanded C08 line sources and visuals
status: done
priority: P2
area: docs
owner: codex-c08-expanded-source-review
claimed_at: 2026-10-22T12:58:03Z
created_at: 2026-10-22T12:57:46Z
completed_at: 2026-10-22T13:02:22Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-expanded.md
---

# Independently verify expanded C08 line sources and visuals

## Why

C08 從 79 句補到 96 句後，舊版來源收據已不適用。需要另一名未撰稿者逐句核對新增內容與原發布資料、舊 HOLD 的修復、逐鏡是否暗示不存在的史料，以及時長是否仍只是估算。

## Definition of done

- [x] 對 PR #1681 的精確 head、旁白與逐鏡 SHA 留下 96/96 獨立逐句來源判定和直接來源連結。
- [x] 寫清楚唯一 HOLD 的最小改法、改稿後重審範圍與視覺／時長界線。

## Steps

- [x] 直接讀 MoMA、龜甲萬、GK 的原發布頁／PDF，逐句對照 96 句與 96 鏡。
- [x] 核對 96/96 ID、81 shot／15 card、卡片連續數、提示詞禁字與正文文字估時。
- [x] 以新 SHA 寫審查收據，保留 `c080419` HOLD，交作者改稿後重審。

## How to verify

收據：`docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-expanded.md`。送審基準是 commit `6a363c1bde3b338d83b8a5ab4b511efadc2ec768`；用 `Get-FileHash -Algorithm SHA256` 核對兩份現稿仍與收據一致；用 `rg '^\| c080[1-6][0-9]{2} \|' <收據>` 檢查 96 個獨立 ID；`npm run check:tasks` 與 `git diff --check` 檢查任務及文件格式。

## Notes

舊版 `c080405` HOLD 已解。新稿 `c080419` 說「兩份後來的說明只支持少滴」，但 MoMA 在防滴與控流雙要求之後稱內斜嘴尖為解法；僅防滴機制有具體解釋，不能概括該來源只支持防滴。收據給最小修法及需重審 ID。第 2–6 章 2,324 字元僅估算約 510 秒，C08 尚無 TTS 實測；本任務不放行媒體費用。
