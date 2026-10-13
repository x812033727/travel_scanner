# AI 每小時新聞：10/13 新進候選與流動佇列

## 盤點界線

- 2026-10-13 18:18（Asia/Taipei）正式站 `/zh-TW/admin/news` 重新載入後顯示：**待審查 9、需重寫／失敗 11、已發布 605、已退件 984**。清單逐筆比對 [13:46 固定 70 筆名冊](news-hourly-backlog-2026-10-13.md)：其中 8 筆待審、9 筆需重寫／失敗屬舊名冊；本頁只列 3 筆新進候選。全站計數會流動，不能將差額當候選終態。
- 本頁的三筆在當次檢查均**未發布、未退件**。只做唯讀候選／來源／執行紀錄核對；沒有按付費「重新執行」或「不是重複，繼續寫」。後台重寫頁明示重跑會再花 AI 費用。
- 任何後續 AI 寫稿、五語審查、Jev 決定、Guide 公開頁都須分開驗收。正式站 SSH 呼叫曾遭自動審核阻擋，本頁沒有以其他通道繞過。
- 18:23 唯讀打開「新聞設定／AI 設定」：新聞撰稿及查核是 Claude Sonnet 5.5、最終修改及代審是 Claude Opus 5.5，四者目前皆走 **Claude 訂閱帳號**；新聞自動模式及 AI 代審開著。訂閱帳號頁顯示部分帳號額度充足；API 頁顯示 Claude 連線選「訂閱帳號」、Anthropic API key **未設定**，最後連線測試是 9/28，不能證明 10/13 可用。兩筆新候選回「組織停用 Claude 訂閱存取」；不能把餘額畫面當成執行成功或自行切換共用帳號／計費路徑。未更改任何設定。

| 候選 ID／目前狀態 | 已核實的差異與障礙 | 可執行的後續 |
| --- | --- | --- |
| `189b04da-bfce-437d-be2b-09e18ecbeded` Ledger／CryptoBilis，`manual_review`、Jev「可能重複」信心 0.830 | 本站 [10/12 舊文](https://mokaair.com/zh-TW/life/crypto-news-ledger-cryptobilis-exploit-20261012)原說裝置如何被竄改「尚未說明」；另一篇同日 72 小時更新亦未涵蓋 10/13 鑑識機制。候選來源為 [Ledger 官方 X 聲明](https://x.com/Ledger/status/2109896739985453358)；直接讀取 X 遇 403，[引用該聲明的報導](https://crypto.news/ledger-reveals-how-hidden-chips-stole-recovery-phrases/)稱新增微控制器擷取螢幕復原詞並以 eSIM／LTE 外傳。候選尚無五語草稿、事實清單、硬檢查；因此不是可以立即發布的已完成稿。 | 這是與 10/12 已刊「發現植入物」不同的**機制說明**，不宜只因同事件就當純重複退件。10/12 舊文的時點句已完成五語更正，見下。先補可原生讀取且可稽核的 Ledger 一手資料，再決定讓此候選寫新進展或編入既刊文；選「不是重複，繼續寫」會觸發付費 AI。新稿的五語與損失估算須獨立查核。 |
| `68acc96e-25c4-4121-b193-2fc98553d3e2` Manus／OPPO，`failed`／`AppError` | 保存了 10/13 [Manus 第一方公告](https://manus.im/blog/manus-partners-oppo)與 13 條事實，證據 SHA-256 `e0f482cf6ec9eba21664984c0bdc9c01c135a56280212e964ca917ffca454dea`；三次 Jev 重複檢查通過、信心 0.060。沒有五語草稿。失敗訊息為 `subscription_run_failed`：組織停用 Claude Code 訂閱存取，並建議使用 Anthropic API key 或由管理員開通；這是 provider／帳號障礙，不是新聞內容被判不合格。 | 保留故障狀態，先由帳號持有人確認 Claude 存取與先前呼叫／計費收據，再決定單筆重跑。後台僅提供整篇付費重跑或退件；不能因故障直接退掉有一手來源的獨立事件。 |
| `e7499e2e-fa42-49a2-8568-d264565d212c` 英國法院／約 61,000 BTC，`failed`／`AppError` | CoinDesk 10/13 來源保存 hash `5f80de1308a2ab6562f1096d070125404da9bf742fce28f4667a8daada3f506b`；Jev 重複檢查三次通過、信心 0.100。三次草稿 run 均回同一 `subscription_run_failed`／Claude 訂閱停用錯誤，UI 各顯示 `0 / 0` tokens；這不是零費用收據。沒有五語草稿／事實／硬檢。英國高等法院 [10/12 判決 [2026] EWHC 2509 (KB)](https://caselaw.nationalarchives.gov.uk/ewhc/kb/2026/2509)只決定受害者所有權主張將適用何地法律，並明言實體權利與證據仍待後續審理；判決記錄查扣超過 61,000 BTC。 | 保留為真實新事件與 provider 故障。先核帳號／付費收據，再決定單筆重跑；未來稿不可寫成英國政府已獲最終所有權或受害人無權取回。英文標題的「提高保留機會」是媒體推論，不是法院命令。 |

## 已完成的既刊文時點更正

- 10/12 Ledger／CryptoBilis 已刊 Guide `85861504-be13-453a-a343-eefd1abb996d` 的五語原版均為已發布 v2。原正文與 FAQ 的「尚未說明植入方法」現在式，若在 10/13 讀取會與新的鑑識報導相衝；因此只把該句明確限定在 **2026-10-12 CoinDesk 報導當時**，連 FAQ 問題也加日期。沒有把仍缺原生可讀一手來源的 10/13 鑑識細節塞入 10/12 文章，也沒有改動損失估算。
- 18:25–18:31（Asia/Taipei）分別保存、填具體發布理由並發布 [zh-TW](https://mokaair.com/zh-TW/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[zh-CN](https://mokaair.com/zh-CN/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[en](https://mokaair.com/en/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[ja](https://mokaair.com/ja/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[ko](https://mokaair.com/ko/life/crypto-news-ledger-cryptobilis-exploit-20261012)。五語編輯器均讀回 **已發布 v4**；五個公開頁的更正正文、FAQ 問題與展開後答案均已直接讀回。這是已刊 Guide 更正，**不改**三筆新候選的終態或 9／11 佇列。
- 以 Guide ID 篩正式站稽核，五筆 `guide_article_published` 在 18:26–18:31 均顯示成功；其中 [zh-TW 事件 `06593642-afb6-45f0-bb23-d5c1804919d2`](https://mokaair.com/zh-TW/admin/audit?target=85861504-be13-453a-a343-eefd1abb996d&page=1&event=06593642-afb6-45f0-bb23-d5c1804919d2)、[zh-CN 事件 `52c552a8-1f9b-4135-9b28-7117e4132af2`](https://mokaair.com/zh-TW/admin/audit?target=85861504-be13-453a-a343-eefd1abb996d&page=1&event=52c552a8-1f9b-4135-9b28-7117e4132af2)與 [en 事件 `9552d3ca-4185-4a9e-ad1b-8199e3adaf04`](https://mokaair.com/zh-TW/admin/audit?target=85861504-be13-453a-a343-eefd1abb996d&page=1&event=9552d3ca-4185-4a9e-ad1b-8199e3adaf04)的 ID 已讀到。ja／ko 成功列可見，展開詳情時遇 429 即停，未取得這兩筆事件 ID；不把未讀 ID 寫成已取得。18:31 再盤點仍為待審 9／需重寫 11。

## 下次接手的順序

1. 先由帳號持有人核 Manus 與法院案的 Claude 訂閱組織存取、輪轉帳號實際路由與失敗 run 計費；不要把 UI 的額度或 `0 / 0` tokens 當可用／零費用證明。Anthropic API key 尚未設定，不能假設有無成本的替代路徑，也不要自行改共用帳號／模型連線或直接按整篇重跑。
2. Ledger 補可查的一手公告；10/12 舊文時點已更正，剩下是明確決定新稿或再更新既刊文，再走相應的五語查核和 Jev 關卡。
3. 每筆有後續動作時讀回候選、run、人工／AI 判斷、Guide 五語版本與公開頁；更新本名冊及同一 draft PR #1480。固定 70 筆終態仍按另一名冊單獨計算。
