# 系列診斷：數據、門檻與決策表

`.agents/skills/producer/SKILL.md` §2 的細節。

## 拿數據

```bash
node tools/video/youtube-reports/cli.mjs overview                     # channel 那行要是 Mokaair；報表進來了沒
node tools/video/youtube-reports/cli.mjs videos --window 7 --long      # 每支長片公開後 7 天
node tools/video/youtube-reports/cli.mjs videos --window 7 --shorts
node tools/video/youtube-reports/cli.mjs traffic --slug <slug> --top 10
node tools/video/youtube-reports/cli.mjs export --out <SCRATCH>/yt --days 56
```

`overview --json` 的 `videos` 把 YouTube id 對到站台的 slug 與系列。原始 CSV 留在 scratchpad，不進 repo。
報表晚 48–72 小時，最近兩天的空白不是零；`window_complete: false` 的不要跟滿的比。

站台沒有報表時（剛重新連結、Reporting API 剛啟用，第一份要一兩天），退回 Studio：
單支影片的「觸及」分頁有縮圖曝光、點閱率、流量來源與「曝光次數和對觀看時間的影響」（只算自然曝光）。

宣傳的花費只在 Studio「內容 → 宣傳活動」：每筆的費用、曝光、觀看、訂閱、後續觀看；詳情頁有地區與最佳化目標。
Google Ads 帳戶裡看不到這些宣傳活動，只有帳單總額。

## 系列表

| 欄 | 怎麼算 | 用途 |
| --- | --- | --- |
| 支數 | 該系列公開的支數 | 少於 3 支不下結論 |
| 自然觀看中位數 | 觀看扣掉流量來源 `ADVERTISING` | 真正的拉力 |
| 自然點閱率 | 縮圖曝光點閱率（報表 `channel_reach_basic` 的 ctr） | 包裝好不好 |
| 平均觀看百分比 | `average_view_duration_percentage` | 內容撐不撐得住 |
| 前 30 秒留存 | Studio 留存曲線的 30 秒處 | 開場有沒有兌現標題 |
| 付費占比 | 廣告觀看 ÷ 總觀看 | 超過一半就先看自然那一半 |
| 留言 | `comments` | 有沒有人在乎 |
| 每 NT$100 後續觀看 | 宣傳表的後續觀看 ÷ 費用 × 100 | 宣傳有沒有帶來會回來的人 |

2026-11-03 的基準：11 筆宣傳共 NT$4,486，換到 1,113 位訂閱、637 次後續觀看；表現最好的 GPT-6 那筆每 NT$100 約 50 次後續觀看，
Gmail 那筆約 0.4 次。之後的宣傳拿這兩個數字比。

## 門檻與出處

- 點閱率：YouTube 說一半的頻道與影片落在 2%–10%，要跟自己的歷史比、分流量來源看；曝光變多時點閱率本來就會掉。
  https://support.google.com/youtube/answer/7628154 、 https://support.google.com/youtube/answer/16767369
- 高點閱率配低觀看時間是標題黨的訊號，推薦會變少；推薦系統看的是滿意度，不只是觀看時間。
  https://support.google.com/youtube/answer/16089387
- 縮圖／標題 A/B 測試看觀看時間佔比，不看點閱率；最多三組，只能在桌機版 Studio，Shorts 不能用。
  https://support.google.com/youtube/answer/16391400
- Studio 宣傳：要漲訂閱選「觀眾成長」；帶來的訂閱與觀看時間**不算 YPP 營利資格**；官方建議每筆至少 100 美元，前一兩天是學習期。
  https://services.google.com/fh/files/misc/youtube_promote_creator_playbook_us.pdf
- 前 30 秒留存 70% 以上算好、60% 以下算弱：只有創作者個人樣本，**未查證**，當參考不當門檻。

## 決策表

| 看到的 | 判斷 | 下一步 |
| --- | --- | --- |
| 自然點閱率低於 2%，平均觀看百分比還可以 | **改包裝** | 縮圖照 `scorecards.md` 重畫、標題把認得的名字放前面；用「測試與比較」，7 天後看 |
| 點閱率正常，前 30 秒留存或平均觀看百分比明顯低於頻道其他系列 | **改內容** | 開場 5 秒先兌現標題；看留存曲線第一個大掉點對到稿子哪一句 |
| 點閱率與留存都還可以，但曝光很少 | **加碼** | 長片配 Shorts 導流；宣傳只投中文地區、最佳化選「後續觀看次數」、預算照官方建議 |
| 付費占比超過九成、留言是零 | **先別再買** | 停宣傳，先修包裝與內容，等自然數字出來 |
| 三支以上都低於門檻，改過包裝也沒起色 | **停或換形式** | 寫一段為什麼停；題材還有價值就換形式（長片改 Shorts、旁白改短劇） |

## 2026-11-03 的第一次判讀（供比較）

- 28 天 3.1 萬觀看、955 小時、訂閱 +939，幾乎全是宣傳買的；沒投宣傳的片每支 4–30 次觀看。
- 30 支片留言數全是 0；留言設定是開的，也沒有待審核。
- 宣傳地區原本是美、馬、日、韓、泰、台六國，中文片投到日韓泰；推薦來源出現動畫、獵奇與成人類影片。
- 奇聞檔案局縮圖大字沒有人名、臉被字蓋住；改成「名字＋反轉」後五項評分每支高 1–10 分（`scorecards.md`）。
