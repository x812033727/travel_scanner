---
id: 2026-11-14-gate-new-producible-pool-themes-on
title: Gate new producible pool themes on an improved audience score of 6.5
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-pool-audience
claimed_at: 2026-11-14T17:23:34Z
created_at: 2026-11-14T17:23:33Z
completed_at:
branch: claude/determined-lamport-1dky28
depends_on: []
scope:
  - tools/video/curio/pool
  - tools/video/so-thats-why/pool
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
---

# Gate new producible pool themes on an improved audience score of 6.5

## Why

站主 2026-11-14：擴充時成題的要「經過評分，然後改進再入題」，門檻 6.5；並要求現有入題的長題案（不論分數高低）也先跑一次這個流程。

## Definition of done

- [x] 基準評分（`reviews/audience-20261114.json`）以外的評分紀錄，可成題長題要有 `audience.rounds`（初評與依短評做的改動），且複評 ≥ 6.5，否則 `build`／`check` 失敗。
- [ ] 現有可成題長題案（奇聞 138、原來如此 107）各跑一輪：依短評改片名、追問與章節講法 → 新評審複評；複評較低就保留原版。
- [ ] 兩池 README 寫明流程；THEMES.md 顯示改進前後分數。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/curio/pool/pool.test.mjs tools/video/so-thats-why/pool/pool.test.mjs
```

## Notes

- 改進只動包裝：片名、核心追問、章節標題與講法、章節順序（開場與收尾不動）。秒數、章節數、用到的素材不變，新文字不得出現原文沒有的數字。
