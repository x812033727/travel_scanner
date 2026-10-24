---
id: 2026-10-20-s54-r16-two-line-oral-wording
title: S54 R16 two-line oral wording repair
status: done
priority: P2
area: docs
owner: codex-s54-r16-author
claimed_at: 2026-10-20T23:02:52Z
created_at: 2026-10-20T23:02:48Z
completed_at: 2026-10-20T23:05:22Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/brief.md
  - docs/videos/curio-s54/claims.md
  - docs/videos/curio-s54/video.json
  - docs/videos/curio-s54/script.md
  - docs/videos/curio-s54/review/r16-author-oral-repair.md
---

# S54 R16 two-line oral wording repair

## Why

R15 全片音檢在兩輪限縮重錄後，`s54002` 仍被辨成「一邊是郵資」，`s54013` 的什魯斯伯里地名仍被誤寫。兩句需要保住已查的史實，改成較自然、較不易產生同音歧義的口播，並重新凍結五檔交給獨立覆核。

## Definition of done

- [x] 只修 R15 音檢留下的兩句，對應主張表與劇本逐字一致；其他場景、來源、畫面及 loop 不變。
- [x] 開場 30–60 秒、正文書面下界至少 8 分鐘，影片 lint 無錯誤和警告。
- [x] 留下精確五檔 SHA-256 與作者交接，供獨立史料／敘事／政策覆核。

## Steps

- [x] 改 `video.json` 和 `claims.md` 的 `s54002`、`s54013`；重產 `script.md`，依實際字數更新 `brief.md`。
- [x] 驗證逐句對齊、時間下界與 R15 反向雜湊；撰寫 [R16 作者交接](../../docs/videos/curio-s54/review/r16-author-oral-repair.md)。

## How to verify

`node tools/video/cli.mjs script --slug curio-s54`；`node tools/video/cli.mjs lint --slug curio-s54 --json`。後者回報 0 errors、0 warnings、7 章、148 句、14.115 分鐘書面估長。Python 逐字檢查 145／145 主張列、148／148 旁白行，開場 165 漢字、正文 2,681 漢字（8.25 分鐘／325 字每分鐘）。反向代回兩句後 `video.json`、`claims.md` 均精確回到 R15 SHA；`brief.md` 只改兩個字數估值。凍結詳見交接。

## Notes

`s54002` 以「新費率今天正式開始」保留 P07 時點，避開「一便士／一邊是」；`s54013` 以「外地親戚」概括 P01 什魯斯伯里親戚，地名留在研究表。R15 兩句音檔和政策憑證皆不適用新版。未重配語音或動用付費媒體；獨立覆核尚未執行。
