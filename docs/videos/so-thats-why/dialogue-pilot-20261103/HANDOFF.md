# 原來如此事務所（對話版）交接（2026-11-07）

給下一個接手的對話。先讀這份，再讀同資料夾的 [`README.md`](README.md) 第 9 節（每一集的關卡表，照順序走）與第 10 節（P07／P14／P08 的教訓），以及 [`SCORECARD.md`](SCORECARD.md)。範本集數用 [`../../sothatswhy-p08-popcorn-pressure/`](../../sothatswhy-p08-popcorn-pressure/)。

## 站主定下的規則

- **誰核准哪一關**：稿子、聲音、畫風、分鏡由 Claude 請獨立代理查核、盲評、評分後自己核准（`approve --gate … --note`，附評分與「owner delegated」）；成片、上架、語言三關由站主在 /admin/videos 決定。站主 2026-11-07：「都依據你建議的決定就好 不用問我」。
- 畫面不放字、正文不用卡片；片尾三張圖（小問比讚，不拿印章）；小孩沒有筆記本；每張臉逐張放大看眼睛；盲評含「沒頭沒尾」（`no_orphans`）。
- 角色設定圖沿用系列的（`video.json` 的 `series`，見 [`../series-sheets/README.md`](../series-sheets/README.md)）；配樂沿用 `sothatswhy-p02-bed.m4a`，不另外生成。
- 翻譯合併後一定跑 `render --thumbnails-only`，看過八張語言縮圖才打包。
- 第一次 `qa` 之前先 `review-push --report-only`，否則「有示範」會被當教學片。
- **備份**（站主 2026-11-07 多次強調）：每過一關就把整個工作目錄（重製要用的所有檔案：`audio/`、`dubs/`、`keyframes/` 每一張候選、`characters/`、`frames/`、`clips/`、`build/`、時間軸、清單、核准紀錄）加上 `upload/` 全部上傳檔，推到 `claude/backup-<slug>`，超過 90 MB 切塊，逐檔核對雜湊；之後才產生或補上的檔案也補進同一個分支；交給站主或送上後台的檔案一律先進分支；沒備份完不准刪任何檔案。工具：[`tools/tobranch.sh`](tools/tobranch.sh)。
- 回報用繁體中文；不開 PR，除非站主說。

## 各集狀態

| 集數 | 狀態 | 備份分支 |
| --- | --- | --- |
| P02 雲變大雨（`rmQ9yD0I6tI`） | 已上架、八語完成 | `claude/backup-sothatswhy-p02-p05`（工作目錄去掉 mp4／wav／dubs，另有 `site-files/` 從站上抓回的全部核准檔） |
| P05 羽絨衣（`BirHcIAlfz4`） | 已上架、八語完成 | 同上（只有工作目錄部分；站上檔案未補完，站主說從 P08 起好好備份即可） |
| P07 冰箱門 | 已上架；站主自己上傳了八語配音與縮圖 | `claude/backup-sothatswhy-p07-p14`（工作目錄去掉 wav／dubs，加上完整 `upload/` 含切塊成片、八語 m4a、縮圖） |
| P14 天空的顏色 | 同 P07 | 同上 |
| P08 爆米花 | 成片已核准、上架包已送審（等站主核准上架）；八語翻譯進行中 → 之後 `i18n-merge`、`dub`、`render --thumbnails-only`、`package`、`review-push --gate languages`（等上架核准後才送語言包） | `claude/backup-sothatswhy-p08-popcorn-pressure`（每關完整備份） |

P07、P14 後台各有一個沒有音檔的語言包待核准，站主不要核准（舊的核准仍有效）。

## 怎麼做一集（摘要，細節在 README 第 9 節）

1. 從 [`../refresh-20261101/EPISODES.md`](../refresh-20261101/EPISODES.md) 挑題（剩 P01 P03 P04 P06 P09–P13 P15–P19；P06 泡泡、P16 潮汐、P17 壁虎較適合小孩發問），`npm run tasks -- new … --area docs`、`claim`。
2. 撰稿代理照 P08 寫 `brief.md`（`## 站主觀點` 寫「只借來做什麼」，不寫「不講」）、`claims.md`、`build_scenes.py`（3.2 字／秒，正文約 2,400–2,600 字）。
3. 另一個代理逐條查核寫 `verify-1.md`；`narrative` 盲評 14 題由全新代理只讀轉寫稿作答，全過才核准稿子。
4. `tts` → `check-audio`（「殼」常被聽錯，換說法）→ 核准聲音 → `look`（沿用設定圖）。
5. `keyframes --takes 3`（背景、`nohup`，跑完一次約 3–5 小時）。三次都不過的不要信評審分數：代理逐張放大挑；挑不到的改提示詞（`EXTRA` 字典），一輪全部修完；用 [`tools/repin.py`](tools/repin.py) 固定，`keyframes --shot` 會把固定的丟掉，最後一定再固定一次。
6. 分鏡評分 ≥ 49／70：卡住的通常是「圖文相符」（講數字、機制的鏡頭要畫成東西本身，用 `scene()`）和「角色一致」。過了就核准分鏡。
7. `render clips assemble captions qa` → 送成片 → 站主核准 → `package` → 送上架 → 八語翻譯（四個代理，對齊 P07 的 `i18n/`）→ `i18n-merge` → `dub`（一次一語系，斷線就 `speech-journal.mjs forget` 重試；`fit.json` 超時就縮句）→ `render --thumbnails-only` → `package` → 上架核准後送語言包。

## 還沒做完的票

- `tasks/open/2026-11-07-sothatswhy-p08-dialogue-mountain-boiling-and.md`：P08，見上。
- `tasks/open/2026-11-06-keyframe-judge-refuses-some-child-character.md`：評審拒答（PROHIBITED_CONTENT）的處理已寫進 `keyframes.mjs`，還缺測試。
- `tasks/open/2026-11-06-curio-and-brand-story-skills-the.md`：奇聞與品牌故事 skill 補眼睛檢查。

## 已知的坑

- 評審比對設定圖時會把所長的灰髮加回去；所長鏡頭用 `CHIEFFIX_DESC`（不寫灰髮），挑圖時要看灰髮面積。
- 小問會漂成馬尾、包包頭、帽兜、男孩頭、照片風；`KIDFIX_TAIL` 加 `EXTRA` 補「hood down, short black bob hanging free」與 flat 2D。
- MiniMax 提示詞上限約 840 字，加了 `EXTRA` 要注意長度。
- 背景工作會因容器重開或閒置被收掉；回來先 `pgrep` 確認，用 `nohup` 跑。
- 磁碟是固定額度；清空間前先照上面的備份規則備份。
