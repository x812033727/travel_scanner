---
id: 2026-10-22-verify-c08-c080419-source-scope-fix
title: Verify C08 c080419 source-scope fix
status: done
priority: P2
area: docs
owner: codex-c08-c080419-source-review
claimed_at: 2026-10-22T13:08:31Z
created_at: 2026-10-22T13:08:22Z
completed_at: 2026-10-22T13:09:09Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-c080419-delta.md
---

# Verify C08 c080419 source-scope fix

## Why

C08 前一輪 96 句獨立審查只 HOLD `c080419`，作者已修改該句。舊稿雜湊不能直接放行新稿，須由未改稿者對 MoMA、GK 與相鄰段落重新界定來源範圍。

## Definition of done

- [x] 留下綁定新 PR head 與兩份 SHA 的 delta PASS／HOLD 收據，明確說明舊 HOLD 是否解除。
- [x] 證明受審檔案差異及 96/96 ID 對齊，並保留稿件以外的 TTS、盲讀及付費關卡。

## Steps

- [x] 直接對照 MoMA 與 GK 原發布頁，核對 `c080419` 及相鄰句與對應畫面。
- [x] 核對 SHA、前一版差異、96/96 ID、shot/card 結構並寫收據。

## How to verify

收據：`docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-c080419-delta.md`；審查基準 `08057df27a150b2efc3710d671773e2d86984639`。用 `Get-FileHash -Algorithm SHA256`、`git diff 6a363c1bd..08057df27 -- script.md visual-plan.md`、機械 ID 比對、`npm run check:tasks` 與 `git diff --check` 核對。

## Notes

PASS：`c080419` 已不再將 MoMA 限定為「只支持少滴」，而是說兩份後來說明都談滴液但沒有逐次量測；相鄰雙要求與小角機制語境無新增 HOLD。視覺檔未改。C08 TTS 及站主稿件核准仍另關。
