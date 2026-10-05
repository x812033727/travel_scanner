# 《偶的江湖》第 1–5 集的製作檔（續寫用）

這裡是寫第 1–5 集劇本時用的工作檔，2026-10-05 從雲端 session 的暫存區備份進 repo，同一天由本機 session 接手寫完。正式成品在 `docs/videos/ou-de-jianghu-e00N/`；這裡是產生它們的來源，之後哪一集要改，先改這裡再合併。

## 進度（2026-10-05 完成）

| 集 | 分場表 | 五幕 | 整集審 | 整集修與驗收 | 成品 |
| --- | --- | --- | --- | --- | --- |
| 1 | 完成 | 完成 | 完成 | 完成 | 正式稿：`ou-de-jianghu-e001/`（跨集審後只補了金印形狀） |
| 2 | 完成 | 完成 | `ep2/review-findings.json`（2 major、9 minor） | 完成，驗收通過（1,393.7 秒） | `ou-de-jianghu-e002/` 五檔齊 |
| 3 | 完成 | 完成 | `ep3/review-findings.json`（8 minor）＋第二輪 `review-findings-2.json`（2） | 完成，驗收通過（1,404.6 秒） | `ou-de-jianghu-e003/` 五檔齊 |
| 4 | 完成 | 完成 | `ep4/review-findings.json`（7 minor） | 完成，驗收通過（1,400.0 秒） | `ou-de-jianghu-e004/` 五檔齊 |
| 5 | 完成 | 完成 | `ep5/review-findings.json`（7 minor）＋第二輪 `review-findings-2.json`（1，主控裁定不改） | 完成，驗收通過（1,404.5 秒） | `ou-de-jianghu-e005/` 五檔齊 |

跨集連戲審（三個鏡頭：時間線與位置、物證與知情、台詞與口吻）提了 7 條，對抗驗證後成立 2 條（第 2 集金印的形狀、第 5 集書齋抽屜的位置），都已修進 acts 並重新合併；第 1 集的一道印也補了形狀。四集的 `brief.md` 與 `review.md` 照第 1 集的形狀寫成；每集 lint 0 錯誤、craft 全達標、shot_reading 0 陷阱，原作名稱掃描 0 筆。主編裁定記在票 `tasks/done/2026-10-04-ou-de-jianghu-e002-e005-scripts.md` 的 Notes。

還沒做的不在這裡：配音核定、查核、聽眾審稿與劇本關卡（要後台先有原生長篇動畫作品與各集集數列），見各集 `brief.md` 的「製作差距」。

## 檔案

- `cast.json`：全系列共用的角色物件，14 人，含 `shot_looks` 與暫定聲音。每集的 `characters` 從這裡逐字照抄，設定圖才能共用。說明在 `cast-notes.md`。
- `epN/beats.md`：分場表，是寫鏡頭唯一的依據，格式見第 1 集的 `ep1/beats.md`。
- `epN/meta.json`：YouTube 標題、說明、tags、出場名單、縮圖（`thumbnail.shot` 是縮圖用的鏡 id）。
- `epN/header.json`：由 `node header.mjs --ep N` 從 `cast.json` 與 `meta.json` 產生，不要手改。
- `epN/acts/a0N.json`：每幕的 scene 陣列，line 不寫 id。
- `epN/ids.json`：已配發的 line id，重新合併時沿用。
- `epN/review-findings*.json`：整集審的意見與修訂紀錄；`-2` 是第二輪驗收剩下的。
- `epN/check-act.mjs`：在 `epN/` 底下跑 `node check-act.mjs a0N [--craft]` 或 `--all --craft`，等於 `node ../check.mjs --ep N …`。
- `check.mjs`：schema、lint、片長估算、craft 與 shot_reading，一次跑完。暫存寫在 `epN/tmp-<label>/`（每個幕一個目錄，五幕可以平行檢查），git 會忽略。
- `merge.mjs`：把五幕合成 `docs/videos/ou-de-jianghu-e00N/video.json` 與 `series.json`；合併後再跑 `node tools/video/cli.mjs script --slug ou-de-jianghu-e00N` 產生 `script.md`。
- `dialogue.py`：輸出整集台詞檢視 `epN/dialogue.txt`，給審稿用（`python dialogue.py --ep N`）。

腳本從自己的位置找 repo 根目錄，Windows 與 Linux 都能跑；Windows 上跑 `dialogue.py` 前先 `export PYTHONUTF8=1`。

## 要改某一集時

1. 改 `epN/acts/a0N.json`（不改 scene id：章名表、縮圖與 `ids.json` 都綁 id）。
2. 在 `epN/` 跑 `node check-act.mjs --all --craft`：SCHEMA 0、LINT ERRORS 0、各幕在分場表第一節的目標 ±10 秒、總長 1,390–1,418 秒、CRAFT 全達標、SHOT READING 0 陷阱。
3. 在 repo 根目錄跑 `node docs/videos/series-plans/ou-de-jianghu/production/merge.mjs --ep N`，再跑 `cli.mjs script` 與 `lint`、`drama_craft_check.mjs`、`shot_reading.mjs`。
4. `review.md` 的數字（秒數、章名起點、高張力時間碼）跟著改。
5. 續跑長時間的工作時，用檔案判斷哪些幕已完成，不要依賴 workflow 的快取：容器常重啟，pipeline 續跑時快取前綴會錯位，已寫好的幕會被重寫。

## 寫下一集（第 6 集起）

照第 2–5 集的做法：分場表 → 每幕一個代理（讀 `beats.md`、`cast-notes.md`、`header.json`、第 1 集同一幕當範本、`ep2/review-findings.json` 當反例）→ 每幕過 `check-act.mjs` → 一位整集審寫 `review-findings.json` → 一位修訂 → 一位對抗驗收（剩的寫 `-2`）→ 合併 → 跨集審 → `brief.md` 與 `review.md`。新角色先加進 `cast.json` 與 `cast-notes.md`，再 `node header.mjs --ep N`。
