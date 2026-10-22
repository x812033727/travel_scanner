---
id: 2026-10-22-recheck-c13-victorinox-repaired-script-and
title: Recheck C13 Victorinox repaired script and visuals
status: done
priority: P2
area: docs
owner: codex-c13-independent-v2
claimed_at: 2026-10-22T18:47:06Z
created_at: 2026-10-22T18:46:59Z
completed_at: 2026-10-22T18:48:55Z
branch: codex/brand-story-victorinox-c13-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-victorinox-c13/reviews/independent-v2-script-visual-review.md
---

# Recheck C13 Victorinox repaired script and visuals

## Why

站主已採用 C13 企劃。初版逐句審查 HOLD 後，作者改了 T02–T03 的人員借調說法、E03／T03 字卡及全部插圖提示詞；交站主審劇本前，另一名代理需要在精確新版雜湊上重新檢查來源、畫面及故事接力。

## Definition of done

- [x] 只改獨立 review receipt，不碰作者的劇本、來源筆記或分鏡；綁定六個輸入檔的 SHA。
- [x] 對舊 HOLD 差異給出 PASS／HOLD、具體行號與一手來源；另寫稿面機械與敘事限制。
- [x] 保留 TTS、成圖、盲讀、站主核准與付費關卡的邊界。

## Steps

- [x] 認領窄 scope，重開原發行者與同期文件，比對舊審輸入和作者修稿。
- [x] 逐鏡解析 JSON，核對句 ID、卡片、插圖和排程比例。
- [x] 寫 exact-hash HOLD 收據，待作者修訂後再請別人核新 SHA。

## How to verify

以 `Get-FileHash -Algorithm SHA256` 重算 `treatment.md`、`source-matrix.md`、`script.md`、`script-source-notes.md`、`visual-plan.md`、`visual-plan.json`；解析 JSON 重算 75/75、61/14、599/490 秒、最長連卡 2。`git diff --check` 與 `git diff --cached --check` 驗本票與收據。`npm run check:tasks` 若仍因本 worktree 既有未追蹤重複票失敗，按錯誤原樣記錄，不動那些檔案。

## Notes

2026-10-23：本輪 **HOLD**。T02–T03 已與 S6 本人事後回憶一致，61 個插圖 prompt 的 style 冗字移除；E03 卡把未定單位的 sales 寫成件數「銷量」，N11 卡把 2001 年九月後寫成模糊的「2001 後」。H06／O05–O06／T04／N02／N06 口播查核過程，H03／O11／N11 重播 1989 年的反轉。詳見 `docs/videos/story-everyday-victorinox-c13/reviews/independent-v2-script-visual-review.md`。無付費製作或站主稿件核准。
