---
id: 2026-11-09-sothatswhy-p17-gecko-feet
title: 原來如此事務所對話版：P17 壁虎黏得住，怎麼又能走得動？
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-focused-hopper
claimed_at: 2026-11-09T00:00:54Z
created_at: 2026-11-09T00:00:49Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - docs/videos/sothatswhy-p17-gecko-feet
  - docs/videos/lexicon.json
---

# 原來如此事務所對話版：P17 壁虎黏得住，怎麼又能走得動？

## Why

原來如此事務所對話版（所長＋小問）的下一集。題目照 `docs/videos/so-thats-why/refresh-20261101/EPISODES.md` 的 P17，
做法照 `docs/videos/so-thats-why/dialogue-pilot-20261103/HANDOFF.md`、README §9–§10，以及 PR #2048 的
`docs/videos/explainer-series/`（兩邊衝突時以共用區為準）。

## Definition of done

- [x] 稿子：獨立查核 `verify-1.md`、盲評 14 題全過、`lint` 0 錯誤，Claude 依站主授權核准。
- [x] 旁白兩個聲音、`check-audio`，核准；角色設定圖沿用系列。
- [ ] 插圖畫完、另一個代理逐張放大檢查、分鏡評分 ≥ 49／70，核准分鏡。
- [ ] 配樂（`sothatswhy-bed-r2.m4a`）→ 合成 → `qa` 11 項 → 成片送站主（`final`）。
- [ ] 上架確認、八語翻譯與配音、八語縮圖、語言包，站主核准。
- [ ] 每過一關備份到 `transfer/sothatswhy-p17-gecko-feet`（`docs/videos/explainer-series/backup/tobranch.sh`）。

## How to verify

`node tools/video/cli.mjs status --slug sothatswhy-p17-gecko-feet`；`lint` 0 錯誤；站主在 /admin/videos 看過成片。

## Notes

- 2026-11-09：稿子四輪盲評才全過（5 → 3 → 2 → 0 題不過）；亞里斯多德那段整段刪掉（查核發現原文是爬樹、跟主線無關）。
  `Tokay`、`gecko` 依站主要求加進 `lexicon.json`，用英文念。
- `check-audio` 一直把「十億」聽成「十一」、「撕貼紙」聽成「是貼紙」、「腳趾」聽成「餃子」：改說法比重錄有效。
- 旁白 12:56；插圖報價 US$1.71（三 take 上限 US$5.14），2026-11-09 開始 `keyframes --takes 3`。
- 容器磁碟只剩約 6 GB，`.git` 裡有舊備份留下的約 4.8 GB loose objects（舊 tobranch 寫法），清理指令被自動模式擋下，等站主決定。
- 2026-11-09：站主要求刪 P07／P14 工作目錄騰空間。獨立代理第一次核對發現 P07 的 en/ja/ko 逐句配音等 741 檔（288 MB）、P14 三個 JSON 不在 GitHub；
  兩個工作目錄整個用新版 `tobranch.sh` 推到 `claude/backup-sothatswhy-p07-p14` 的 `local-20261109/<slug>/`（head 5683fbcf，verify 0），
  同一代理只看 GitHub 重跑 `coverage.sh`：兩集 missing 0、mismatches 0、`.SPLIT` 0 不符，才刪；磁碟 6.1 → 7.7 GB。
  兩邊都沒有的（早在 11-07 就沒了）：兩集繁中逐句旁白、P07 其餘五語與 P14 八語的逐句配音（成品配音在分支與 YouTube）。
