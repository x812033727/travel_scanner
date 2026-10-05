# 《偶的江湖》第 1–5 集的製作檔（續寫用）

這裡是寫第 1–5 集劇本時用的工作檔，2026-10-05 因為額度快用完，先從 session 的暫存區備份進 repo，讓下一個 session 接著做。正式成品在 `docs/videos/ou-de-jianghu-e00N/`；這裡是產生它們的來源。

## 進度（2026-10-05）

| 集 | 分場表 | 五幕 | 整集審 | 整集修 | 成品 |
| --- | --- | --- | --- | --- | --- |
| 1 | 完成 | 完成 | 完成 | 完成 | 正式稿：`ou-de-jianghu-e001/` |
| 2 | 完成 | 完成，各幕過檢查 | 完成：`ep2/review-findings.json`，2 major、9 minor | **未做** | 草稿：`ou-de-jianghu-e002/` |
| 3 | 完成 | 完成，各幕過檢查 | **未做** | **未做** | 草稿：`ou-de-jianghu-e003/` |
| 4 | 完成 | a01–a03 完成；**a04、a05 未寫** | — | — | 無 |
| 5 | 完成 | **五幕未寫** | — | — | 無 |

第 2、3 集的 `brief.md` 只是最短的三節草稿，`review.md` 還沒寫。分場表四份都經過連戲審、戲劇審、修訂與跨集審；主編裁定記在票 `tasks/open/2026-10-04-ou-de-jianghu-e002-e005-scripts.md` 的 Notes。

## 檔案

- `cast.json`：全系列共用的角色物件，14 人，含 `shot_looks` 與暫定聲音。每集的 `characters` 從這裡逐字照抄，設定圖才能共用。說明在 `cast-notes.md`。
- `epN/beats.md`：分場表，是寫鏡頭唯一的依據，格式見第 1 集的 `ep1/beats.md`。
- `epN/meta.json`：YouTube 標題、說明、tags、出場名單、縮圖。
- `epN/header.json`：由 `node header.mjs --ep N` 從 `cast.json` 與 `meta.json` 產生，不要手改。
- `epN/acts/a0N.json`：每幕的 scene 陣列，line 不寫 id。
- `epN/ids.json`：已配發的 line id，重新合併時沿用。
- `epN/check-act.mjs`：在 `epN/` 底下跑 `node check-act.mjs a0N [--craft]` 或 `--all`，等於 `node ../check.mjs --ep N …`。
- `check.mjs`：schema、lint、片長估算、craft 與 shot_reading，一次跑完。暫存寫在 `epN/tmp/`，git 會忽略。
- `merge.mjs`：把五幕合成 `docs/videos/ou-de-jianghu-e00N/video.json` 與 `series.json`。
- `dialogue.py`：輸出整集台詞檢視 `epN/dialogue.txt`，給審稿用。

腳本裡的 repo 路徑寫死成 `/home/user/travel_scanner`，換位置要先改。

## 接著做

1. 寫第 4 集 a04、a05，以及第 5 集五幕。每幕一個代理，提示詞照第 1 集：
   - 先讀 `epN/beats.md`、`epN/header.json`、`cast-notes.md`，以及第 1 集同一幕的成品當範本。
   - 只寫自己那一幕的 `epN/acts/a0N.json`。
   - 跑 `node check-act.mjs a0N` 與 `--craft`，修到 schema 與 lint 錯誤 0、shot_reading 0 陷阱、該幕 272–292 秒、單幕 craft 全達標。
2. 每集一位整集審：跑 `--all --craft`，用 `python3 dialogue.py --ep N` 產生台詞檢視，對照分場表找接縫、時段、說破、重複句的問題。再一位整集修，修到全集 1,390–1,418 秒且檢查全過。第 2 集的審稿意見已經在 `ep2/review-findings.json`，可以直接進修訂。
3. 合併成品：
   - 跑 `node merge.mjs --ep N`，再跑 `node tools/video/cli.mjs script --slug ou-de-jianghu-e00N` 與 `lint`。
   - 用私人對照表掃原作人名。
   - 照第 1 集的形狀寫 `brief.md` 與 `review.md`。
4. 續跑長時間的工作時，用檔案判斷哪些幕已完成，不要依賴 workflow 的快取。容器常重啟，pipeline 續跑時快取前綴會錯位，已寫好的幕會被重寫。
