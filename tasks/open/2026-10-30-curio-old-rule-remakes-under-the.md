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
  - docs/videos/history-curiosity/old-rule-remake-playbook-20261031.md
---

# Curio old-rule remakes under the 10-25 rules, no burn-in: batch 1 H01 H04 H05 H09 U02

## Why

站主 2026-10-31：已上架的舊片另外改新規則、未上架的改新規則，全部不燒字幕。這張票管「舊規則做的奇聞檔案局」19 支裡的 18 支：
10-13 到 10-15 的 `-v2` 與更早的版本，是 10-25 開場五步、對觀眾說話、13 分鐘之前做的。清單與計畫在
`origin/claude/video-reclassify-rules-44b738` 的 `docs/videos/history-curiosity/old-rule-inventory-20261031.md`、`new-rules-migration-20261031.md`。
舊片、舊 slug、YouTube 上的影片一律不動；新片核准後換片由站主決定。

## Definition of done

- [x] 第一批五支（H01 瑪麗賽勒斯特號、H04 佳特洛夫、H05 D.B. Cooper、H09 艾爾哈特、U02 51 區）的新 slug 稿子：`lint` 0 錯誤、獨立查核寫在 `verify-1.md`、兩位盲讀讀者沒有任何一題同時答否（記錄在 `panel/`）。
- [x] 第一批的 `tts`、`keyframes` dry-run 實際數字連同稿子交給站主（`music` 要等旁白才報得出，用 skill 的每首約 US$0.15）。未核准前不做任何付費生成。
- [x] 其餘集數的順序與狀態寫在這張票上，並另開票 `2026-10-30-curio-old-rule-remakes-batches-2` 讓下一位認領。
- [ ] 站主核准報價後，走旁白、插圖、配樂、成片。換片由站主決定。

## Steps

- [x] H01 v3 試跑，定下撰稿、查核、盲評的流程。
- [x] H04 v3、H05 v3、H09 v2、U02 v3。
- [x] 跨集檢查：五集的「你」與自己的反應句不是同一句套路、標題公式、縮圖字。
- [x] 報價、開 PR、交站主。

## How to verify

`node tools/video/cli.mjs lint --slug <slug>`；`node tools/video/cli.mjs narrative --slug <slug> --answers <file>`；`node tools/video/cli.mjs keyframes --slug <slug> --dry-run`；`npm run check:tasks`。

## Notes

### 順序（一批最多 5 支，先做目前公開、題目最有名的）

| 批 | 舊 slug | 新 slug | 狀態 |
| --- | --- | --- | --- |
| 1 | curio-h01-v2 瑪麗賽勒斯特號 | curio-h01-v3 | 稿子、查核、盲評（第 9 輪）、lint 都過，等站主 |
| 1 | curio-h04-v2 佳特洛夫 | curio-h04-v3 | 稿子、查核、盲評（第 4 輪）、lint 都過，等站主 |
| 1 | curio-h05-v2 D.B. Cooper | curio-h05-v3 | 稿子、查核、盲評（第 11 輪）、lint 都過，等站主 |
| 1 | curio-h09 艾爾哈特（只在 `origin/codex/curio-h09-earhart-20261015`，main 沒有） | curio-h09-v2 | 稿子、查核、盲評（第 6 輪）、lint 0 錯誤 1 邊界警告，等站主 |
| 1 | curio-u02-v2 51 區 | curio-u02-v3 | 稿子、查核、盲評（第 6 輪）、lint 都過，等站主 |
| 2 | curio-h02-v2 羅阿諾克、h03-v2 通古斯、h06-v2 安娜塔西亞、h07-v2 鐵面人、h10 富蘭克林遠征 | 各 `-v3`（h10 為 `-v2`） | 未開始 |
| 3 | curio-h11 伏尼契、h12 弗蘭南燈塔、l08-v2 麥田圈、m09 安提基特拉、u09 小綠人 | 各下一版 | 未開始 |
| 4 | curio-s12 關原、s15 伊達政宗、s21 鬱金香 | 各 `-v2` | 未開始 |
| — | curio-s31 | 不重寫 | `curio-s31-v2` 是 Codex 照 10-25 規則做的（`origin/codex/curio-s31-new-rules-20261026`，票 `2026-10-26-curio-s31-new-rules` 只在該分支，10-29 還在做日語配音），但 `burn_in: true`：只需要重新合成，由重新合成那一線（session `burn-in-reassemble`，10-31 確認）負責，不屬於這張票 |

### 動手前查過的舊票（都不擋）

- `2026-10-13-remake-curio-h04-h05-h06-with`：認領停在 10-14，完成條件全勾，只是沒關；範圍是 `-v2`。
- `2026-10-14-remake-curio-h07-with-the-series`：認領停在 10-14，`curio-h07-v2` 已上架；範圍是 `-v2`。
- `2026-10-20-remake-ten-curio-episodes-in-the`：只管 S 軸十集，跟這份名單沒有重疊。

### 第一批的數字（2026-10-31，dry-run 實數）

| slug | 正文字數 | 句數 | 插圖 | 卡片 | 「你」每千字 | lint 估片長 | 盲評輪數 | 插圖一次／三次上限 | 旁白計費字元 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| curio-h01-v3 | 3,273 | 145 | 122 | 8 | 7.3 | 15.7 分 | 9 | US$1.65／4.94 | 3,796 |
| curio-h04-v3 | 3,198 | 140 | 119 | 9 | 4.7 | 15.2 分 | 4 | US$1.61／4.82 | 3,673 |
| curio-h05-v3 | 3,234 | 148 | 115 | 11 | 5.6 | 15.5 分 | 11 | US$1.55／4.66 | 3,731 |
| curio-h09-v2 | 3,537 | 146 | 124 | 8 | 5.9 | 16.8 分 | 6 | US$1.67／5.02 | 4,131 |
| curio-u02-v3 | 3,732 | 167 | 132 | 11 | 4.8 | 17.7 分 | 6 | US$1.78／5.35 | 4,570 |
| 合計 | | | | | | | | US$8.26／24.79 | 19,901 |

配樂五首約 US$0.75（skill 的每首約 US$0.15；`music --dry-run` 要等旁白才算得出）。一批上限約 **US$25.54**；上一批實際每集 US$1.4–2.7，預計 US$8–14。旁白字元算在網站 Gemini 額度（`tts --dry-run` 當下顯示本月還有 4,119,572 字元），工具沒有換算成美元。

### 這批學到的（下一批照做）

- **同時最多 3 個子代理時的節奏：** 一位撰稿 45–55 分鐘、約 50 萬 token；一位查核 15–25 分鐘、約 30 萬 token；一位盲讀 1–2 分鐘、約 8.6 萬 token。
- **查核每集都退 13–26 處：** 主要是把來源講強、替人補心情、提示詞畫了未滿 70 年的真人。撰稿的自查抓不到這些，不能省。
- **片長與字數互相矛盾：** 規則寫 13 分鐘、約 3,500 字，但 H24 實測約 4 字／秒（2,902 字 12:10）。3,200–3,700 字會落在 14–17 分鐘。這批依字數走，等站主試聽第一支再決定。
- **盲評最常同否的是照年代走（`one_line`）和岔題（`no_detour`）：** 撰稿時就要照年代排章、刪掉與主問題無關的好故事；開場不能講掉結果。盲評過程刪掉的段落：H01 的 2001 年殘骸與帕克騙保，H05 的模仿劫機與安檢規定，H09 的 1937 澳洲週刊與 1943 電影，都不是事實有錯。
- **問句一定要回收：** 為了湊懸念加的問句，下一輪就會被 `payoffs` 擋。改用「問題來了」「更怪的是」或把問句放在下一句就回答的地方。

### 上架前要再查

- `curio-h09-v2`：潟湖的鋼管還在研究中（amelia.prf.org），2026-10-19 的結果可能更新。
- `curio-u02-v3`：1978 年的年月只有 Merlin 一個來源；片尾「三十五年」依賴它，已標成「照我的算法」。
- `curio-h01-v3`：亞瑟活到 1931 年只有兩個非一手來源；德沃證詞、莎拉的信經部落格轉錄，法庭原件沒開到。
- `curio-h05-v3`：「丹庫柏」「迪比庫柏」沒寫 `say`，聽檢要聽。`curio-h04-v3`：高姆、普茲林是音譯，聽檢可能要改字。
