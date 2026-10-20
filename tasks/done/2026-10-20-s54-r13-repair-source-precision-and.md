---
id: 2026-10-20-s54-r13-repair-source-precision-and
title: S54 R13 repair source precision and May chronology
status: done
priority: P2
area: docs
owner: codex-s54-r13-author
claimed_at: 2026-10-20T21:41:02Z
created_at: 2026-10-20T21:41:00Z
completed_at: 2026-10-20T21:46:58Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s54/brief.md
  - docs/videos/curio-s54/research.md
  - docs/videos/curio-s54/claims.md
  - docs/videos/curio-s54/video.json
  - docs/videos/curio-s54/script.md
  - docs/videos/curio-s54/review/r13-author-fix.md
---

# S54 R13 repair source precision and May chronology

## Why

R12 的獨立史料覆核因 `s54031` 具體說「逐封」記帳、`s54143` 把「得知」說成親眼「見到」而 HOLD。無背景盲讀 A 又因五月末段先跳到發售一個月後再倒回 5 月 21／29 日，且轉入銷記防重用支線，對 `one_line` 和 `no_detour` 投 No。需重新收緊史料、按時間走完供應主線，再交不同工作者審查。

## Definition of done

- [x] 修掉兩處來源 HOLD 所指的超出原文說法，結尾不再倒敘或轉入銷記支線。
- [x] 開場維持 30–60 秒工具估長，最快正文超過 8 分鐘；場景、劇本、主張表逐字對齊，影片 lint 0 錯誤／0 警告。
- [x] 五檔 SHA-256 凍結在作者紀錄，由不同工作者再做獨立史料／畫面核查和兩位無背景敘事盲讀。

## Steps

- [x] 以希爾原文 H 9612–9643、13221–25 修正 `s54031`、`s54094`。
- [x] 以 H 13353–13400 重寫 `s54130–46` 為印製、分發、發售約一個月後的倫敦供應爭議，撤下銷記支線。
- [x] 同步企劃、研究、口播、主張、畫面提示、loop 和說明欄；保留 S54 TTS STOP。

## How to verify

- `node tools/video/cli.mjs script --slug curio-s54`：重新產生劇本。
- `node tools/video/cli.mjs lint --slug curio-s54 --json`：0 errors／0 warnings。
- `sha256sum docs/videos/curio-s54/{brief.md,research.md,claims.md,video.json,script.md}`：與 `docs/videos/curio-s54/review/r13-author-fix.md` 五筆相符。
- 場景、主張、劇本 ID 與口播 145／145 對齊；`npm run check:tasks` 與 `git diff --check` 通過。

## Notes

詳見 `docs/videos/curio-s54/review/r13-author-fix.md`。本輪只做作者修稿，未自審史料、畫面或 13 題敘事。舊稿 TTS 只有六句草稿快取，新稿核准前保留 `/workspace/.video-work/curio-s54/STOP`，不得續做媒體。
