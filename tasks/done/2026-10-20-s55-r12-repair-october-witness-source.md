---
id: 2026-10-20-s55-r12-repair-october-witness-source
title: S55 R12 repair October witness source wording
status: done
priority: P2
area: docs
owner: codex-s55-r12-author
claimed_at: 2026-10-20T22:44:22Z
created_at: 2026-10-20T22:44:20Z
completed_at: 2026-10-20T22:45:19Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/video.json
  - docs/videos/curio-s55/claims.md
  - docs/videos/curio-s55/script.md
  - docs/videos/curio-s55/review/r12-author-source-fix.md
---

# S55 R12 repair October witness source wording

## Why

R11 的獨立史料覆核只 HOLD `s55065`：原句說富蘭克林本人沒有親眼看到十月繫留試驗，但固定來源只證明這回細節見於後出的書，不能推斷他是否在場。

## Definition of done

- [x] 旁白和同 ID 主張列改為只歸屬後出文獻，保留十月仍繫留的界線。
- [x] R12 五檔 SHA 凍結、劇本重產、逐字對齊及 lint 通過，交給獨立覆核。

## Steps

- [x] 依 R11 獨立覆核建議改 `s55065` 並精確回溯差異。
- [x] 重產劇本，跑機械檢查，寫 R12 作者交接。

## How to verify

`node tools/video/cli.mjs script --slug curio-s55`、`node tools/video/cli.mjs lint --slug curio-s55 --json`、`npm run tasks -- check`；逐 ID 核對 `video.json` 與 `claims.md`；SHA 和反向替換結果見 `docs/videos/curio-s55/review/r12-author-source-fix.md`。

## Notes

R12 只改 `s55065` 的口說句與同列來源界線；沒有改來源連結、其他旁白或畫面提示詞。這是作者候選稿，仍須獨立史料、雙盲敘事、政策、音檢；未呼叫付費媒體。
