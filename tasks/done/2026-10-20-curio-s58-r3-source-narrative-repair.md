---
id: 2026-10-20-curio-s58-r3-source-narrative-repair
title: Curio S58 R3 source and narrative repair
status: done
priority: P2
area: docs
owner: codex-s58-preproduction
claimed_at: 2026-10-20T23:43:43Z
created_at: 2026-10-20T23:43:40Z
completed_at: 2026-10-21T00:03:23Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s58
---

# Curio S58 R3 source and narrative repair

## Why

S58 R2 的獨立史料／書面畫面覆核為 HOLD：四句直接引文落在錯的 Dagron 段落，另有跨段錨點、超出史料的收件動作、關鍵口播與提示詞不合及縮圖單位錯誤。兩位無前情讀者的正式 OR 合併為 8／13，五個必答題未過：`no_spoiler`、`one_line`、`payoffs`、`no_recap`、`no_detour`。需用同一主問題重寫，並保留 R2 原票、正式紀錄及五檔 SHA。

## Definition of done

- [x] 五份 R3 作者候選創作檔有固定 SHA，R1/R2 收據與 HOLD 票完整保留。
- [x] 六章正文按 10 月至 1 月順時推進；濃縮開場不先交代後果，正文最快文字估算 ≥8 分鐘。
- [x] 錯引文、口播超界、紙卷綁腿／羽管綁尾畫面和「則」單位已按 R2 回饋修正。
- [x] `video.json`／逐句表／衍生劇本逐字連號，影片 lint 無錯誤或警告，文件測試與任務檢查通過。
- [x] 作者收據明示 R3 仍待非作者史料／書面畫面與兩位新盲讀，未自評 PASS 或使用付費媒體。

## Steps

- [x] 依 R2 史料與正式雙盲票修訂同一鳥郵主線、窄主張及插圖界線。
- [x] 生成 R3 五檔、固定 SHA，先通知主工作者啟動獨立審核。
- [x] 補 R3 作者收據與本任務紀錄；保留 R1/R2 所有證據。

## How to verify

在倉庫根目錄執行：

```sh
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s58
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs script --slug curio-s58
npm run test:docs-videos
npm run check:tasks
sha256sum docs/videos/curio-s58/{research.md,brief.md,claims.md,video.json,script.md}
```

作者另按場景 ID 比對 `video.json`、`claims.md`、`script.md` 146／146 句及連號；新一輪來源與盲讀仍須非作者完成。

## Notes

R3 作者收據在 `docs/videos/curio-s58/review/r3-author-freeze.md`。R2 HOLD 詳見 `review/r2-source-independent.md` 與 `review/r2-merge/summary.md`。影片 lint 0 errors／0 warnings；正文 2632 漢字，按每分鐘 325 字估 8.10 分鐘；文件測試 236／236；任務檢查 exit 0（其他任務既有警告）。不因這些工具測試推定史料與敘事已獨立通過。
