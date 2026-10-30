---
id: 2026-10-30-curio-old-rule-remakes-under-the
title: Curio old-rule remakes under the 10-25 rules, no burn-in: batch 1 H01 H04 H05 H09 U02
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-curio-old-rules-b8fde7
claimed_at: 2026-10-30T19:34:52Z
created_at: 2026-10-30T19:32:03Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-h01-v3
  - docs/videos/curio-h04-v3
  - docs/videos/curio-h05-v3
  - docs/videos/curio-h09-v2
  - docs/videos/curio-u02-v3
---

# Curio old-rule remakes under the 10-25 rules, no burn-in: batch 1 H01 H04 H05 H09 U02

## Why

站主 2026-10-31：已上架的舊片另外改新規則、未上架的改新規則，全部不燒字幕。這張票管「舊規則做的奇聞檔案局」19 支裡的 18 支：
10-13 到 10-15 的 `-v2` 與更早的版本，是 10-25 開場五步、對觀眾說話、13 分鐘之前做的。清單與計畫在
`origin/claude/video-reclassify-rules-44b738` 的 `docs/videos/history-curiosity/old-rule-inventory-20261031.md`、`new-rules-migration-20261031.md`。
舊片、舊 slug、YouTube 上的影片一律不動；新片核准後換片由站主決定。

## Definition of done

- [ ] 第一批五支（H01 瑪麗賽勒斯特號、H04 佳特洛夫、H05 D.B. Cooper、H09 艾爾哈特、U02 51 區）的新 slug 稿子：`lint` 0 錯誤、獨立查核寫在 `verify-1.md`、兩位盲讀讀者沒有任何一題同時答否（記錄在 `panel/`）。
- [ ] 第一批的 `tts`、`keyframes`、`music` dry-run 實際金額連同稿子交給站主，一批一次核准。未核准前不做任何付費生成。
- [ ] 其餘集數的順序與狀態寫在這張票上。

## Steps

- [ ] H01 v3 試跑，定下撰稿、查核、盲評的流程。
- [ ] H04 v3、H05 v3、H09 v2、U02 v3。
- [ ] 跨集檢查：五集的「你」與自己的反應句不是同一句套路、標題公式、縮圖字。
- [ ] 報價、開 PR、交站主。

## How to verify

`node tools/video/cli.mjs lint --slug <slug>`；`node tools/video/cli.mjs narrative --slug <slug> --answers <file>`；`node tools/video/cli.mjs keyframes --slug <slug> --dry-run`；`npm run check:tasks`。

## Notes

### 順序（一批最多 5 支，先做目前公開、題目最有名的）

| 批 | 舊 slug | 新 slug | 狀態 |
| --- | --- | --- | --- |
| 1 | curio-h01-v2 瑪麗賽勒斯特號 | curio-h01-v3 | 進行中 |
| 1 | curio-h04-v2 佳特洛夫 | curio-h04-v3 | 進行中 |
| 1 | curio-h05-v2 D.B. Cooper | curio-h05-v3 | 進行中 |
| 1 | curio-h09 艾爾哈特（只在 `origin/codex/curio-h09-earhart-20261015`，main 沒有） | curio-h09-v2 | 進行中 |
| 1 | curio-u02-v2 51 區 | curio-u02-v3 | 進行中 |
| 2 | curio-h02-v2 羅阿諾克、h03-v2 通古斯、h06-v2 安娜塔西亞、h07-v2 鐵面人、h10 富蘭克林遠征 | 各 `-v3`（h10 為 `-v2`） | 未開始 |
| 3 | curio-h11 伏尼契、h12 弗蘭南燈塔、l08-v2 麥田圈、m09 安提基特拉、u09 小綠人 | 各下一版 | 未開始 |
| 4 | curio-s12 關原、s15 伊達政宗、s21 鬱金香 | 各 `-v2` | 未開始 |
| — | curio-s31 | 不重寫 | `curio-s31-v2` 是 Codex 照 10-25 規則做的（`origin/codex/curio-s31-new-rules-20261026`，票 `2026-10-26-curio-s31-new-rules` 只在該分支，10-29 還在做日語配音），但 `burn_in: true`：只需要重新合成，由重新合成那一線（session `burn-in-reassemble`，10-31 確認）負責，不屬於這張票 |

### 動手前查過的舊票（都不擋）

- `2026-10-13-remake-curio-h04-h05-h06-with`：認領停在 10-14，完成條件全勾，只是沒關；範圍是 `-v2`。
- `2026-10-14-remake-curio-h07-with-the-series`：認領停在 10-14，`curio-h07-v2` 已上架；範圍是 `-v2`。
- `2026-10-20-remake-ten-curio-episodes-in-the`：只管 S 軸十集，跟這份名單沒有重疊。
