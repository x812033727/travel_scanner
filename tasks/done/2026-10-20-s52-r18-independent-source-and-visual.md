---
id: 2026-10-20-s52-r18-independent-source-and-visual
title: S52 R18 independent source and visual review
status: done
priority: P2
area: docs
owner: codex-s52-r18-source
claimed_at: 2026-10-20T21:22:29Z
created_at: 2026-10-20T21:22:26Z
completed_at: 2026-10-20T21:24:53Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52/review/r18-source-independent.md
---

# S52 R18 independent source and visual review

## Why

R18 刪去三句重述並改兩句口播；R17 的來源與畫面 PASS 綁舊雜湊，須獨立核新稿。

## Definition of done

- [x] 留下 R18 五檔雜湊、固定原文、精確差分、116 句對齊、畫面與長度的 PASS／HOLD 界限。

## Steps

- [x] 重讀 Cook／Kippis／1771 原報固定全文；核改句及刪句是否仍符合原文。
- [x] 逆建 R17 `video.json` 驗雜湊；核 116／116 主張、劇本重生、畫面提示詞與 lint。

## How to verify

`sha256sum docs/videos/curio-s52/{brief.md,research.md,claims.md,video.json,script.md}`；`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s52 --json`；見審核紀錄中的逆建雜湊與 325 CPM 估時。

## Notes

`review/r18-source-independent.md` 的文字來源與書面畫面 PASS。新隔離盲讀、TTS、音訊與實際插圖仍是獨立關卡；舊媒體不可當新稿驗收。
