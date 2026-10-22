---
id: 2026-10-22-independently-verify-c08-shortened-75-line
title: Independently verify C08 shortened 75-line script and visuals
status: done
priority: P2
area: docs
owner: codex-gpt6-c08-independent-short-75
claimed_at: 2026-10-22T13:49:12Z
created_at: 2026-10-22T13:49:07Z
completed_at: 2026-10-22T13:50:49Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-short-75.md
---

# Independently verify C08 shortened 75-line script and visuals

## Why

PR #1681 的 C08 被敘事盲讀退回後從 82 句大幅縮為 75 句；舊來源 PASS 只綁舊 SHA。需要另一代理從 K1/K2a/K3/D1/R1/M1 原頁重新逐句核對旁白與同 ID 畫面，防止縮稿把來源界線寫成定論。

## Definition of done

- [x] 對 75／75 句與 75／75 列畫面留下綁定本輪 PR head、script／visual／R1 補充 SHA 的獨立逐 ID PASS/HOLD 收據，交代一處需修字句與其他證據邊界。

## Steps

- [x] 直接重開 K1、K2a、K3、D1、M1 原頁並目視 GK Report No.34 印刷頁 23–24。
- [x] 核對所有 75 句及同 ID 畫面、11 張卡片、1961／2005／2018 年代、補充與倒取兩開口、銷售總數缺席與不做零滴保證。

## How to verify

讀 docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-short-75.md；用 Get-FileHash -Algorithm SHA256 核對三份輸入檔；比較 script.md 與 visual-plan.md 的 75 個 ID；執行 git diff --cached --check 和 npm run check:tasks（本機先前被 policy 擋的兩份 orphan open 票會使後者失敗，提交樹不含它們）。

## Notes

獨立總判 HOLD c080207：「太重」超過 MoMA 的 unwieldy 與 GK 廚房／陶壺回顧，改「笨重」或「不便上桌」後須新 SHA 覆核。其他 74 句與 75 畫面來源界線 PASS；旁白盲讀、美術品質、TTS、站主核准另待。先前兩個 orphan open 票曾因自動審查 blocked by policy 而保留，本輪不碰。
2026-10-22：tasks done 已寫出本輪 done 票，Windows 仍留下未追蹤的 open 原檔；先前同類單檔刪除被自動審查 blocked by policy，本輪未重試或繞過。提交僅納入 done 票及來源收據，三份 orphan open 原檔留在本機。
