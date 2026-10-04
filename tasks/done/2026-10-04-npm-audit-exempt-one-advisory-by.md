---
id: 2026-10-04-npm-audit-exempt-one-advisory-by
title: npm audit: exempt one advisory by id with a reason and a review date, so a red run means something new
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-04T11:49:53Z
created_at: 2026-10-04T11:49:33Z
completed_at: 2026-10-04T11:50:01Z
branch:
depends_on: []
scope:
  - tools/npm-audit-gate.mjs
  - tools/npm-audit-gate.test.mjs
  - tools/npm-audit-allow.json
  - .github/workflows/npm-audit.yml
---

# npm audit: exempt one advisory by id with a reason and a review date, so a red run means something new

## Why

每天排程的 `npm audit --audit-level=high` 從 2026-10-01 起常紅（issue #1173）：`braces` 3.0.3 的
GHSA-vfj7-8cjw-p6xm 沒有修正版（受影響範圍 <= 3.0.3，就是最新版），只經
eslint-config-next → @next/eslint-plugin-next → fast-glob → micromatch 進來，`npm audit --omit=dev` 是 0 筆。
上游出修正版之前每天紅一次，紅燈就不再代表「有新問題」。站主 2026-10-04 決定：只對這一筆豁免。

## Definition of done

- [x] 正式環境的相依（`--omit=dev`）照舊零豁免。
- [x] 整棵樹 high 以上的公告，只有 `tools/npm-audit-allow.json` 逐筆列出（公告編號＋套件＋原因＋複查日）的才放行；複查日過了就再紅。
- [x] 別的公告、同一公告出現在別的套件、registry 沒回報告，都照樣紅。
- [x] 上游修好後清單裡多餘的項目會印警告。

## How to verify

`node --test tools/npm-audit-gate.test.mjs tools/supply-chain.test.mjs`；
`npm audit --json | node tools/npm-audit-gate.mjs` 印 `npm audit gate: ok`。合併後手動觸發一次 npm audit workflow。

## Notes

- 複查日 2026-11-04。到期時先看公告有沒有修正版：有就升級並刪掉清單項目，沒有才延期。
- 追上游的票是 `2026-10-04-investigate-braces-advisory-in-the-next`，這張只做關卡。
