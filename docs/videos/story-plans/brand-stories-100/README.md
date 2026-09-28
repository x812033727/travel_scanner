# 品牌故事企劃清單（100 個）

主機每天從這份清單依序做兩支品牌故事影片。為什麼這樣做、一支影片長什麼樣、清單怎麼變成資料庫裡的集數，都寫在 [`docs/videos/STORY.md`](../../STORY.md)。

站主 2026-09-28 核准了題目與順序：日常用品與隱形標準 40、日本／韓國／台灣旅途會遇到的品牌 40（日本 24、韓國 8、台灣 8）、科技與軟體 20。題目避開參考頻道做過的主題。

## 檔案

| 檔案 | 內容 | 誰改 |
| --- | --- | --- |
| `stories/<代號>.json` | 一個故事的企劃：提問、六段要點、必查事實、來源、人物、圖像注意事項 | 人或代理，照 [`AUTHORING.md`](AUTHORING.md) |
| `reviews/<代號>.json` | 第二個人查核的紀錄，綁著故事內容的雜湊；故事改了就要重查。`notes` 與 `reviewer_only` 會跟著故事編進 `stories.json` | 查核的人或代理 |
| `schedule.json` | 50 天、每天 12:00 與 20:00 各一支；順序只寫在這裡 | 人 |
| `series.json` | 作品列的欄位與全部影片共用的畫風 | 人 |
| `approved-seeds.json` | 站主核准時的暫定標題與轉折，留作紀錄 | 不改 |
| `reserve.json` | 備選題目，都還沒查核 | 人 |
| `stories.json` | 匯入伺服器用的檔案：作品列加上照順序排好的 100 個故事。每個故事多帶 `caveats`（查核紀錄的 `notes`），工人讀不到來源的事實多帶 `reviewer_only: true` | 產生的，不要手改 |
| [`SCHEDULE.md`](SCHEDULE.md) | 給人看的 50 天排程表 | 產生的，不要手改 |

## 改完之後

```bash
node tools/video/story-plans/validate.mjs --write     # 重新產生 stories.json 與 SCHEDULE.md，並檢查
node tools/video/story-plans/validate.mjs             # 只檢查；CI 的 npm run test:tools 也會檢查
node tools/video/story-plans/validate.mjs --format    # 把每個故事檔的欄位排成固定順序
node tools/video/story-plans/validate.mjs --fetch     # 另外把每個來源實際讀一次（要連網，手動跑，約 4 分鐘）
node tools/video/story-plans/validate.mjs --only A01,B18 --fetch --report read.json   # 只看這幾個故事，並把讀到的結果存成 JSON
node tools/video/story-plans/read.mjs <網址> <要找的字> ...   # 照工人的方式讀一頁，看這些字在不在工人留下的那一段
```

檢查的規則在 `tools/video/story-plans/plan.mjs`：100 個故事、分類數量、代號與 slug 不重複、六段要點、每個必查事實的來源夠不夠、每個故事有一份對得上內容的查核紀錄、排程每天兩支而且每個故事只排一次。

### `--fetch` 讀到的三種結果

`--fetch` 用的就是主機工人的讀取程式（`tools/video/automation/fetch.mjs`），用工人的名字（`Mokaair-editorial/1.0`），同一個網域一次一頁、間隔 1 秒，不同網域同時讀。逾時或伺服器錯誤會再試一次。

| 結果 | 意思 | 算不算問題 |
| --- | --- | --- |
| `200 text` | 工人讀得到文字 | 不算 |
| `200 no text` | 網頁在，但工人讀不到文字：PDF、超過 3 MB、或內容要靠程式才顯示 | 這一頁本身不算；但一個必查事實引用的頁面**全部**都是這種時算，要再補一頁工人讀得到的。真的沒有這樣的頁面時，由查核的人把那一條列進查核紀錄的 `reviewer_only` |
| 其他（403、404、逾時） | 連結是死的，影片說明欄的參考資料也會是死連結 | 算，要換掉 |

工人一頁只留前 40,000 個字。很長的頁面（年報、長條目）要用 `read.mjs` 確認那句話在前面那一段裡。

## 常見的修改

- **改一個故事的內容**：改 `stories/<代號>.json`。查核紀錄綁著內容，改了一個字就過期：照 [`AUTHORING.md`](AUTHORING.md) §查核重新查過、把新的雜湊寫進 `reviews/<代號>.json`，再跑 `--write`。
- **換順序**：改 `schedule.json`，跑 `--write`。故事檔裡沒有編號，不用跟著改。
- **換掉一個題目**：代號不變，從 `reserve.json` 挑同一分類的題目重寫那個故事檔，並在下面「換掉的題目」記一行。
- **已經匯入之後再改**：重新匯入只會更新還沒開始製作的集數（`STORY.md` §企劃清單與集數列）。

## 匯入

伺服器的匯入指令在票 `2026-09-28-video-story-api-series-kind`。上線之後，站主同意時在主機上跑：

```bash
python -m app.cli video-story-import --series brand-stories < stories.json            # 試跑，不寫入
python -m app.cli video-story-import --series brand-stories --apply --limit 2 --episodes-per-day 1 < stories.json   # 試作：只匯入排程的前兩個
python -m app.cli video-story-import --series brand-stories --apply < stories.json    # 之後匯入其餘的
```

作品不存在時，匯入會照 `series.json` 建立它；已經存在時不會改作品的欄位（每日支數之後在後台改）。

## 查核的結果

100 個故事都由另一個代理在新的對話裡查核過（[`AUTHORING.md`](AUTHORING.md) §查核），查核的人總共打開了一千多個來源。每個故事都被改過，沒有一個原封不動通過：流傳的商業故事常常在年份、數字與「誰先做的」上面出錯。

- 標題跟站主核准時不一樣的，列在 [`SCHEDULE.md`](SCHEDULE.md) 最下面，兩個版本並排。
- 每個故事改了什麼，寫在 `reviews/<代號>.json` 的 `changes`；還有疑慮但沒有證據改的地方寫在 `notes`，撰稿與查核時要看。
- 標題是查核過的暫定標題。製作時撰稿模型可以改寫得更吸引人，但每個數字與說法仍然要對得到 `must_verify`。

## 換掉的題目

說法站不住腳的，先改成查得到的說法；連故事都不成立的才從 `reserve.json` 換題目，並在這裡記一行。到 2026-09-28 為止沒有換掉任何題目。

| 代號 | 原本的題目 | 換成 | 原因 |
| --- | --- | --- | --- |
| （沒有） | | | |
