# 品牌故事企劃清單（100 個）

主機每天從這份清單依序做兩支品牌故事影片。為什麼這樣做、一支影片長什麼樣、清單怎麼變成資料庫裡的集數，都寫在 [`docs/videos/STORY.md`](../../STORY.md)。

站主 2026-09-28 核准了題目與順序：日常用品與隱形標準 40、日本／韓國／台灣旅途會遇到的品牌 40（日本 24、韓國 8、台灣 8）、科技與軟體 20。題目避開參考頻道做過的主題。

## 檔案

| 檔案 | 內容 | 誰改 |
| --- | --- | --- |
| `stories/<代號>.json` | 一個故事的企劃：提問、六段要點、必查事實、來源、人物、圖像注意事項 | 人或代理，照 [`AUTHORING.md`](AUTHORING.md) |
| `reviews/<代號>.json` | 第二個人查核的紀錄，綁著故事內容的雜湊；故事改了就要重查 | 查核的人或代理 |
| `schedule.json` | 50 天、每天 12:00 與 20:00 各一支；順序只寫在這裡 | 人 |
| `series.json` | 作品列的欄位與全部影片共用的畫風 | 人 |
| `approved-seeds.json` | 站主核准時的暫定標題與轉折，留作紀錄 | 不改 |
| `reserve.json` | 備選題目，都還沒查核 | 人 |
| `stories.json` | 匯入伺服器用的檔案：作品列加上照順序排好的 100 個故事 | 產生的，不要手改 |
| [`SCHEDULE.md`](SCHEDULE.md) | 給人看的 50 天排程表 | 產生的，不要手改 |

## 改完之後

```bash
node tools/video/story-plans/validate.mjs --write     # 重新產生 stories.json 與 SCHEDULE.md，並檢查
node tools/video/story-plans/validate.mjs             # 只檢查；CI 的 npm run test:tools 也會檢查
node tools/video/story-plans/validate.mjs --format    # 把每個故事檔的欄位排成固定順序
node tools/video/story-plans/validate.mjs --fetch     # 另外把每個來源網址實際抓一次（要連網，手動跑）
```

檢查的規則在 `tools/video/story-plans/plan.mjs`：100 個故事、分類數量、代號與 slug 不重複、六段要點、每個必查事實的來源夠不夠、排程每天兩支而且每個故事只排一次。

`--fetch` 用主機工人的名字（`Mokaair-editorial/1.0`）去抓，每個網域間隔 1 秒。工人查核時也是這樣抓，所以這裡抓不到的來源對工人沒有用，要換掉。

## 常見的修改

- **改一個故事的內容**：改 `stories/<代號>.json`，跑 `--write`。
- **換順序**：改 `schedule.json`，跑 `--write`。故事檔裡沒有編號，不用跟著改。
- **換掉一個題目**：代號不變，從 `reserve.json` 挑同一分類的題目重寫那個故事檔，並在下面「換掉的題目」記一行。
- **已經匯入之後再改**：重新匯入只會更新還沒開始製作的集數（`STORY.md` §企劃清單與集數列）。

## 匯入

伺服器的匯入指令在票 `2026-09-28-video-story-api-series-kind`。上線之後，站主同意時在主機上跑：

```bash
python -m app.cli video-story-import --series brand-stories < stories.json            # 試跑
python -m app.cli video-story-import --series brand-stories --apply < stories.json    # 寫入
```

## 換掉的題目

寫企劃時查核過每個題目的核心說法。說法站不住腳的，先改成查得到的說法；連故事都不成立的才換題目。

| 代號 | 原本的題目 | 結果 | 原因 |
| --- | --- | --- | --- |
