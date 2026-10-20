---
id: 2026-10-20-s55-r11-independent-source-and-written
title: S55 R11 independent source and written visual review
status: done
priority: P2
area: docs
owner: codex-s55-r11-source
claimed_at: 2026-10-20T22:40:23Z
created_at: 2026-10-20T22:40:20Z
completed_at: 2026-10-20T22:43:28Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/review/r11-source-independent.md
---

# S55 R11 independent source and written visual review

## Why

S55 R10 的 140 句正式音檢仍有 14 個旗標。R11 作者只改了 14 句口說及逐句表，必須由獨立讀者核對固定版史料、書面畫面與歷史先後，再決定是否可進敘事及媒體關卡。

## Definition of done

- [x] 以五檔固定 SHA 與 F／M／E 固定全文獨立逐句覆核 14 句，寫出可追溯 PASS／HOLD，不沿用 R10 結論。
- [x] 檢查全 138 主張、140 旁白與畫面時序，明示後續是否能進關卡。

## Steps

- [x] 重取固定來源、重算全文 SHA，確認固定 Git 引用頁可達。
- [x] 比對 14 句與周邊提示詞、全片證據層次、R10 反向雜湊。
- [x] 將獨立判定寫入 `docs/videos/curio-s55/review/r11-source-independent.md`。

## How to verify

`sha256sum docs/videos/curio-s55/{brief.md,research.md,claims.md,video.json,script.md}`；`node tools/video/cli.mjs lint --slug curio-s55 --json`；`npm run check:tasks`。逐項來源證據與固定 Git URL 回應記在覆核頁。

## Notes

**結論：史料 HOLD，限定 `s55065`。** M 記載十月十五日試驗，但沒有證明富蘭克林本人不在場。R11 把「非 F 目擊記載」改成「富蘭克林沒有親眼見到這回」，超出可查範圍。建議口說「十月這回的細節，要看後來的書：氣球在空中停了多久？」並同步 `claims.md`、重產劇本、再凍結和獨立覆核。其餘 13 句及書面畫面可過；不改創作檔、不呼叫付費媒體。`s55031` 的「解開繩索」以解除牽制的泛義可通，F 原字為 cut，若再修可用「切斷繩索後」更精確。
