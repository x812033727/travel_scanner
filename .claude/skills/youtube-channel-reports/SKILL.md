---
name: youtube-channel-reports
description: 讀 Mokaair 頻道的 YouTube 數據來分析與改進影片：站台每天下載 YouTube Reporting API 的報表（觀看、engaged views、觀看時間、平均觀看百分比、縮圖曝光與點閱率、流量來源與搜尋字詞、播放位置、裝置、年齡性別、分享、字幕、片尾畫面、訂閱增減），配對過影片工具權杖的 AI 用 tools/video/youtube-reports 從站台讀原始列，不碰 Google 授權。要看某支或某批影片的成效、比較題材、標題、縮圖或 Shorts 與長片、找觀眾從哪裡來、寫成效報告或下一批的改進建議，或報表讀不到（要重新連結、要啟用 API）時，先讀這個 skill。Read the channel's YouTube Reporting API data from the site with a paired video tool token, analyse it and turn it into concrete improvements.
metadata:
  short-description: 從站台讀 YouTube 頻道報表，分析並提出改進
---

# 頻道報表（youtube-channel-reports）

站台把頻道每天的 YouTube Reporting API 報表下載保存（`docs/videos/YOUTUBE-REPORTS.md`），
你用影片工具權杖從站台讀，**不需要也不要去要 Google 的憑證**。數字是 YouTube 寫的原值。

## 1. 先確認能讀

```bash
node tools/video/cli.mjs login --name "Claude 雲端 session"   # 沒有 MOKAAIR_VIDEO_TOKEN 時配對一次，站主在後台按允許
node tools/video/youtube-reports/cli.mjs overview              # 有哪些報表、涵蓋哪幾天、站台的影片
node tools/video/youtube-reports/cli.mjs sync                  # 抓 YouTube 新產生的報表（12 小時內做過就略過）
```

| `overview`／`sync` 說 | 原因與處理 |
| --- | --- |
| exit 3、「沒有包含 YouTube Analytics」 | 頻道是在加報表之前連結的。請站主到 `/admin/videos` 設定分頁按「重新連結」，同意畫面勾 Analytics。你不能代勞。 |
| 「還沒有啟用 YouTube Reporting API」 | 站主的 Google Cloud 專案要啟用該 API（「API 和服務」→「程式庫」）。 |
| `waiting_for_first_report` 有東西 | job 剛建，YouTube 一兩天內才產出第一份與前 30 天；先不要下結論。 |
| exit 4、401 | 權杖失效，重新 `login`。 |

資料晚 48–72 小時，日期是**太平洋時間**的日。最近兩天的空白不是零。主機每天自動同步兩次，平常不必手動 `sync`。

## 2. 拿資料

```bash
node tools/video/youtube-reports/cli.mjs export --out "$TMPDIR/yt" --days 56     # overview.json + 每個家族一個 CSV
node tools/video/youtube-reports/cli.mjs rows --report channel_reach_basic --from 2026-10-01 --to 2026-10-31 --slug ai-agent-vs-chatbot
node tools/video/youtube-reports/cli.mjs rows --report channel_traffic_source --video VIDEO_ID --names --out traffic.csv
```

先用這兩個現成的彙總，不用自己寫加總程式（數字是工具在你這端算的，輸出已標明「自行計算」）：

```bash
node tools/video/youtube-reports/cli.mjs videos --window 7                    # 每支影片公開後 7 天：觀看、觀看時間、平均觀看時長與百分比、互動、淨訂閱、曝光與點閱率
node tools/video/youtube-reports/cli.mjs videos --window 28 --long --format csv --out long-28d.csv
node tools/video/youtube-reports/cli.mjs videos --shorts --published-since 2026-10-01
node tools/video/youtube-reports/cli.mjs traffic --slug ai-agent-vs-chatbot  # 流量來源占比，加上前十個搜尋字詞、推薦來源影片、外部網站
```

`videos` 的 `window_complete: false` 表示還沒滿那幾天，不要拿來跟滿的比。平均觀看百分比與點閱率的
單位照 YouTube 的欄位（文件沒寫是 0–1 還是 0–100，看實際數值判斷後在報告裡寫明）。

檔案放在 scratchpad 或暫存目錄，**不要 commit 原始 CSV**（那是頻道的數據，不屬於 repo）。
`overview.json` 的 `videos` 把 YouTube id 對到站台的 slug、標題、分類、是否 Shorts、系列與公開時間；
影片的企劃與腳本在 `docs/videos/<slug>/`。

欄位照第一列讀（YouTube 會加欄位）。常用的：

- `channel_basic`：`views`、`engaged_views`、`watch_time_minutes`、`average_view_duration_seconds`、
  `average_view_duration_percentage`、`likes`、`comments`、`shares`、`subscribers_gained`、`subscribers_lost`；
  一支影片一天會有很多列（依 `country_code`、`subscribed_status`、`live_or_on_demand` 拆開）。
- `channel_reach_basic`：`video_thumbnail_impressions`、`video_thumbnail_impressions_ctr`（比例，0–1）。
- `channel_traffic_source`：`traffic_source_type`（數字代碼；`--names` 加上名稱，對照表在
  `tools/video/youtube-reports/codes.mjs`：5 搜尋、7 推薦影片、24 Shorts、3 瀏覽功能、9 外部…）
  與 `traffic_source_detail`（搜尋時是搜尋字詞、推薦時是來源影片 id、外部時是網頁）。

## 3. 怎麼分析才有用

`videos`、`traffic` 不夠用、要自己合併數字時，要用對的方法：把列加總時，`views`、`watch_time_minutes`、曝光次數可以直接加；
**平均值與比率不能直接加或平均**——平均觀看時長要用 `watch_time_minutes ÷ views` 重算，
點閱率要用「曝光 × 點閱率」加總後再除以總曝光。

要回答的問題，依序：

1. **縮圖與標題有沒有讓人點**：每支影片前 7 天的曝光次數與點閱率；點閱率低、曝光高 → 改縮圖標題。
2. **點進來的人有沒有留下來**：平均觀看百分比與時長；長片前段掉人 → 改開場與鉤子（看
   skill `youtube-video` 的腳本規則）。報表沒有逐秒留存曲線，需要時請站主從 Studio 匯出。
3. **觀眾從哪裡來**：搜尋（看 `traffic_source_detail` 的搜尋字詞，能變成下一支的題目與標題）、
   推薦、Shorts 動態、外部。
4. **誰在看**：國家、年齡性別、裝置、字幕語言 → 決定配音與字幕語言、畫面字的大小。
5. **帶來訂閱的是哪幾支**：`subscribers_gained − subscribers_lost`。
6. 比較時對齊時間窗（公開後第 1–7 天、1–28 天），樣本少就說樣本少；Shorts 與長片分開比，
   Shorts 看 `engaged_views`，兩種觀看數定義不同，不要混。

## 4. 寫出結論

- 報告寫在 `docs/videos/<批次或 slug>/metrics.md` 或對應的票，列出影片 id、時間窗、資料取得時間。
- 每個你算出來的數字標明「依 YouTube 報表原始數據自行計算」；**不要把它當成 YouTube 的數字，
  也不要放上公開網頁或影片說明**（YouTube 開發人員政策的衍生指標規定，`docs/videos/YOUTUBE-REPORTS.md`）。
- 建議要具體到能做：哪幾支的縮圖要重做、下一批題目、標題用哪些搜尋字詞、哪個語言要配音。
  能做但這次不做的，用 `npm run tasks -- new` 開票，不要只留在對話裡。
- 沒有資料的地方寫「缺資料」，不要估。
