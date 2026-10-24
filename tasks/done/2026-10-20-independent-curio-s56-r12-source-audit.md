---
id: 2026-10-20-independent-curio-s56-r12-source-audit
title: Independent Curio S56 R12 source audit
status: done
priority: P2
area: docs
owner: codex-s56-r12-source
claimed_at: 2026-10-20T23:11:26Z
created_at: 2026-10-20T23:11:23Z
completed_at: 2026-10-20T23:14:22Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/review/r12-source-independent.md
---

# Independent Curio S56 R12 source audit

## Why

R11 的 154 句語音音檢仍有 `s56096`、`s56174` 兩旗標，作者只改兩句口播形成 R12。新版須由非作者重新核固定 Foster／Loesch 原文、154 列主張與書面畫面，不能沿用 R11 判票或音訊。

## Definition of done

- [x] 在 [R12 獨立報告](../../docs/videos/curio-s56/review/r12-source-independent.md) 留下五檔精確 SHA、兩句原文裁決、全稿差分與 PASS／HOLD 邊界。

## Steps

- [x] 重算五檔、F／L 固定來源提交、blob 與全文 SHA；核對兩句及相鄰畫面。
- [x] 比對 R11 精確 JSON／劇本雜湊、154 列主張及 234 個連結；跑 lint、文件影片測試與任務檢查。

## How to verify

`sha256sum docs/videos/curio-s56/{brief.md,research.md,claims.md,video.json,script.md}`；`sha256sum /tmp/s56-chicago-{foster,loesch}/*.txt`；`node tools/video/cli.mjs lint --slug curio-s56 --json`；`npm run test:docs-videos`；`npm run check:tasks`。兩個新增檔各用 `git diff --no-index --check /dev/null <file>` 驗空白（新增差分的預期退出碼 1，沒有空白錯誤輸出）。精確差分與原文行號見報告。

## Notes

2026-10-20 UTC：R12 史料與書面畫面 **PASS**；154／154 主張／劇本對齊，lint 0 errors／0 warnings，文件影片測試 236／236 通過。R11 音檢 HOLD 不轉作 R12 音訊 PASS；新讀者盲評、政策及 R12 全句重錄音檢仍須另做。未改作者五檔、未用付費媒體。
