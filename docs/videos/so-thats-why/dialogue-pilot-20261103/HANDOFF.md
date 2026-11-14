# 原來如此事務所（對話版）交接（2026-11-07）

> **2026-11-10 起停用。** 站主：備份不再推分支，製作的所有檔案由做片的 session 用 [`todrive.sh`](../../ai-drama-drive/todrive.sh) 直接傳到雲端硬碟 `AI劇/<名稱>/<集數>/製作檔/`，規則在 [`AI-DRAMA-DRIVE.md`](../../AI-DRAMA-DRIVE.md)。`tobranch.sh` 會拒絕執行。下面提到的「備份分支」一律改成傳雲端硬碟 `AI劇/原來如此事務所/<代碼>/製作檔/`；要備份什麼不變。

給下一個接手的對話。先讀這份，再讀同資料夾的 [`README.md`](README.md) 第 9 節（每一集的關卡表，照順序走）與第 10 節（P07／P14／P08 的教訓），以及 [`SCORECARD.md`](SCORECARD.md)。範本集數用 [`../../sothatswhy-p08-popcorn-pressure/`](../../sothatswhy-p08-popcorn-pressure/)。

## 站主定下的規則

- **誰核准哪一關**：稿子、聲音、畫風、分鏡由 Claude 請獨立代理查核、盲評、評分後自己核准（`approve --gate … --note`，附評分與「owner delegated」）；成片、上架、語言三關由站主在 /admin/videos 決定。站主 2026-11-07：「都依據你建議的決定就好 不用問我」。
- **生圖、雙系列人物分家與人景配比定案（2026-11-14 起）**：**停用 MiniMax 生圖**；全系列改用代理內建 `generate_image`（`16:9` 滿版，有角色鏡 `ImagePaths` **必傳 Repo 內正式 2.5 頭身 Q 版設定圖** `docs/videos/so-thats-why/series-sheets/characters/chief/chief-canon-v2.png` 或 `kid/kid-canon-v2.png`，禁用舊版 MiniMax 失敗檔，並與《奇聞檔案局》3.5 頭身修長比例 `Ada` 嚴格分家）生成**「劇場級動畫光影 × 厚塗水粉質感」**（完整英文基底句見 [`../look.md`](../look.md)），再以 `keyframes import --provider external --usd 0` 匯入。**全集不必每鏡都有人**：約 **45%–65%** 鏡頭設 `"nobody": true` 直接畫純機制剖面與物件對照，角色鏡頭約 **35%–55%** 只放提問、反應、轉折與首尾。遇到生圖配額冷卻時先跑八語翻譯與配音或分批等待，絕不退回 MiniMax。
- **語音與配樂定案（2026-11-14 起）**：中文（`zh-TW`）固定用 Gemini（所長 `Sulafat`、小問 `Leda`，語速 ≥ 4.4 字／秒）；八語配音（`en,ja,ko,es,pt,id,vi,th`）固定用 MiniMax（`dub --provider minimax`）；系列配樂床沿用 `sothatswhy-bed-r2.m4a`（sha256 `9bb4ba6f…`，見 [`../../explainer-series/README.md`](../../explainer-series/README.md)），不另外生成。
- 畫面不放字、正文不用卡片；片尾三張圖（小問比讚，不拿印章）；小孩沒有筆記本；每張圖匯入後切 2 倍放大檢視圖由獨立子代理逐張審過（眼睛、手指、零文字亂碼、道具數量與幾何結構 100% 正確）；盲評含「沒頭沒尾」（`no_orphans`）。
- 角色設定圖沿用系列的（`video.json` 的 `series`，見 [`../series-sheets/README.md`](../series-sheets/README.md)）。
- 翻譯合併後一定跑 `render --thumbnails-only`，看過八張語言縮圖才打包。
- 第一次 `qa` 之前先 `review-push --report-only`，否則「有示範」會被當教學片。
- **成片觀眾視角評分與備份順序**（2026-11-10 起改傳雲端硬碟；2026-11-14 加入成片觀眾審片關卡）：`assemble`＋`qa`（11/11）後**必先派未參與製作的獨立子代理完成成片觀眾視角評分（`review/audience-review.md`，六項各 ≥ 7.5、總均 ≥ 8.0）**，凡挑出縮圖裁切、色溫疲勞、低對比、無字圖解難懂或角色破綻，**一律先修完並重過 `qa`（11/11）**；全部修完確認無誤後，才把整個工作目錄（重製要用的所有檔案：`audio/`、`dubs/`、`keyframes/`、`characters/`、`frames/`、`clips/`、`build/`、時間軸、清單、核准紀錄與 `upload/`）完整傳到雲端硬碟 `AI/備份/AI劇/原來如此事務所/<主題分類>/<P集數>/製作檔/<slug>/` 並逐檔核對數量與雜湊（[`../../AI-DRAMA-DRIVE.md`](../../AI-DRAMA-DRIVE.md)），最後才執行 `review-push --gate final`。
- 回報用繁體中文；單集製作不開 PR，除非站主說。

## 各集狀態

| 集數 | 狀態 | 備份分支 |
| --- | --- | --- |
| P02 雲變大雨（`rmQ9yD0I6tI`） | 已上架、八語完成 | `claude/backup-sothatswhy-p02-p05`（工作目錄去掉 mp4／wav／dubs，另有 `site-files/` 從站上抓回的全部核准檔） |
| P05 羽絨衣（`BirHcIAlfz4`） | 已上架、八語完成 | 同上（只有工作目錄部分；站上檔案未補完，站主說從 P08 起好好備份即可） |
| P07 冰箱門 | 已上架；站主自己上傳了八語配音與縮圖 | `claude/backup-sothatswhy-p07-p14`（工作目錄去掉 wav／dubs，加上完整 `upload/` 含切塊成片、八語 m4a、縮圖） |
| P14 天空的顏色 | 同 P07 | 同上 |
| P08 爆米花 | 成片、上架已核准；八語配音、字幕、縮圖做完，語言包已送審（站上確認 8 配音、8 縮圖、8 字幕都在），等站主核准語言、上傳 YouTube 後貼網址。分鏡第二次評分 54／70 | `claude/backup-sothatswhy-p08-popcorn-pressure`（每關完整備份，最後一次 5,020 檔、0 不符） |

P07、P14 後台各有一個沒有音檔的語言包待核准，站主不要核准（舊的核准仍有效）。

## 怎麼做一集（摘要，細節在 README 第 9 節與第 10.7–10.8 節）

1. 從題庫或 [`../refresh-20261101/EPISODES.md`](../refresh-20261101/EPISODES.md) 挑題，`npm run tasks -- new … --area docs`、`claim`。
2. 撰稿照對話版規格寫 `brief.md`（`## 站主觀點` 寫「只借來做什麼」，不寫「不講」）、`claims.md`、`build_scenes.py`（語速 ≥ 4.4 字／秒，10 分鐘正文約 2,700–2,900 字；頂層設 `"pauses": {"line_ms": 0, "scene_ms": 150}`、`"still_motion": "beat"`）。
3. 獨立子代理逐條查核寫 `verify-1.md`；`narrative` 盲評 14 題由全新子代理只讀轉寫稿作答，全過才核准稿子。
4. `tts`（Gemini `Sulafat`＋`Leda`）→ `check-audio` → 核准聲音 → `look`（沿用系列設定圖）。
5. 關鍵影格用代理內建 `generate_image`（`16:9` 滿版，套用 [`../look.md`](../look.md) 的「劇場級動畫光影 × 厚塗水粉質感」基底句與角色設定圖參考）逐批生圖，再用 `keyframes import --provider external --usd 0` 匯入（嚴禁用 MiniMax 生圖）。
6. 切 2 倍放大檢視圖由獨立子代理逐張審過（SCORECARD 分鏡評分 ≥ 49／70，各項 ≥ 6，零文字亂碼、眼睛手指正常、道具數量與幾何結構 100% 正確）→ 核准分鏡。
7. 八語翻譯（`en,ja,ko,es,pt,id,vi,th`，帶定版系列譯名後綴）→ `i18n-merge` → 獨立審稿 → `dub --provider minimax` 八語配音（`fit.json` 超時就縮句重跑）→ `check-audio` → `render`（逐張檢視繁中含 A/B 變體與八語全部縮圖）→ `clips` → `assemble` → `captions` → `package` → `qa`（11/11 全過）→ **獨立子代理成片觀眾視角評分（`review/audience-review.md`）→ 瑕疵全數修完並重過 `qa`（11/11）** → 完整備份至 Google Drive（獨立代理核對 0 漏檔）→ `review-push --gate final`。

## 還沒做完的票

- `tasks/open/2026-11-07-sothatswhy-p08-dialogue-mountain-boiling-and.md`：P08，只剩站主核准語言、上傳 YouTube；記下影片網址後 `npm run tasks -- done`。
- `tasks/open/2026-11-06-keyframe-judge-refuses-some-child-character.md`：評審拒答（PROHIBITED_CONTENT）的處理已寫進 `keyframes.mjs`，還缺測試。
- `tasks/open/2026-11-06-curio-and-brand-story-skills-the.md`：奇聞與品牌故事 skill 補眼睛檢查。

## 已知的坑

- 八語縮圖：英、日、葡、印尼的字常太長，撞到右上的「原來如此事務所」標記就不會畫，`render --thumbnails-only` 會印 note；把 headline 與 sub 縮短到兩行內再 `i18n-merge` 重畫。
- 送語言包後用 `review-files --dry-run --gate languages` 確認站上有 8 個 dub、8 個 thumbnail、8 個 captions。

- 評審比對設定圖時會把所長的灰髮加回去；所長鏡頭用 `CHIEFFIX_DESC`（不寫灰髮），挑圖時要看灰髮面積。
- 小問會漂成馬尾、包包頭、帽兜、男孩頭、照片風；`KIDFIX_TAIL` 加 `EXTRA` 補「hood down, short black bob hanging free」與 flat 2D。
- MiniMax 提示詞上限約 840 字，加了 `EXTRA` 要注意長度。
- 背景工作會因容器重開或閒置被收掉；回來先 `pgrep` 確認，用 `nohup` 跑。
- 磁碟是固定額度；清空間前先照上面的備份規則備份。
