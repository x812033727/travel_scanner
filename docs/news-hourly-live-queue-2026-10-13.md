# AI 每小時新聞：10/13 新進候選與流動佇列

## 盤點界線

- 2026-10-13 18:18（Asia/Taipei）正式站 `/zh-TW/admin/news` 重新載入後顯示：**待審查 9、需重寫／失敗 11、已發布 605、已退件 984**。清單逐筆比對 [13:46 固定 70 筆名冊](news-hourly-backlog-2026-10-13.md)：其中 8 筆待審、9 筆需重寫／失敗屬舊名冊；本頁只列 3 筆新進候選。全站計數會流動，不能將差額當候選終態。
- 本頁的三筆在當次檢查均**未發布、未退件**。只做唯讀候選／來源／執行紀錄核對；沒有按付費「重新執行」或「不是重複，繼續寫」。後台重寫頁明示重跑會再花 AI 費用。
- 任何後續 AI 寫稿、五語審查、Jev 決定、Guide 公開頁都須分開驗收。正式站 SSH 呼叫曾遭自動審核阻擋，本頁沒有以其他通道繞過。
- 18:23 唯讀打開「新聞設定／AI 設定」：新聞撰稿及查核是 Claude Sonnet 5.5、最終修改及代審是 Claude Opus 5.5，四者目前皆走 **Claude 訂閱帳號**；新聞自動模式及 AI 代審開著。訂閱帳號頁顯示部分帳號額度充足；API 頁顯示 Claude 連線選「訂閱帳號」、Anthropic API key **未設定**，最後連線測試是 9/28，不能證明 10/13 可用。兩筆新候選回「組織停用 Claude 訂閱存取」；不能把餘額畫面當成執行成功或自行切換共用帳號／計費路徑。未更改任何設定。
- 19:00 再讀正式站：**待審查 10、需重寫／失敗 11、已發布 605、已退件 986**。新進的 Character.AI 使本頁流動候選增為 4 筆；其他站內計數變動不得直接歸因於本次操作。13:46 固定 70 筆仍以其 ID 名冊計：9 已發布、44 已退件、17 未終態（8 待審、9 需重寫／失敗）。

## 18:40 帳號切換後的路由核對

- 站主選擇恢復 Claude 訂閱路線並自行換預設帳號。18:40 正式站 AI 設定讀回 Claude Code **帳號 B** 為預設；Apple 私密轉寄信箱的 **帳號 D** 仍列為已登入、不是預設。新聞四階段仍顯示 Claude 訂閱連線。預設只決定輪替起點：主機代理從多個可用登入槽輪替，不能因 B 顯示預設就斷定 10/13 前的兩筆失敗用 B，或保證下一筆只用 B。
- 正式站目前尚未把「Your organization has disabled Claude subscription access for Claude Code」辨識成 `subscription_auth_failed`：該錯誤現走一般 `subscription_run_failed`／502，**同一請求不會輪替到下一帳號**。同一 draft PR 已補精確分類及 fake CLI 跨帳號回歸，66 項代理測試通過，詳見[工作單](../tasks/open/2026-10-13-classify-failed-oauth-token-refresh-as.md)。仍須合併及部署後才能改變正式站行為；本機通過不代表訂閱存取恢復。
- 後台的訂閱「測試連線」只核登入／額度概要，不會用新聞模型實際回答，不能證明組織權限已恢復；帳號頁的額度刷新可能另送一則 Haiku 探測，也不作零費用證據。新聞執行紀錄沒有保存被選中的帳號槽，失敗紀錄 `0 / 0` tokens 仍非供應商帳單。若同一帳號仍回此錯誤，[Anthropic 錯誤說明](https://code.claude.com/docs/en/errors#your-organization-has-disabled-claude-subscription-access)將其列為伺服器端存取限制；僅改本地預設或同帳號重新登入不能當解除限制的證明。Apple 登入方式本身也不是權限證據。
- 19:00 新 Character.AI 候選的執行紀錄顯示草稿、兩輪查證、最終編修、語系審查、AI 最終判斷均成功，Claude Sonnet 5.5／Opus 5.5 各有非零 tokens。這證明**該次**訂閱模型路線有實際回答；UI 沒有帳號槽或供應商帳單，不能斷定由預設 B 回答、舊兩筆故障可重跑或其既有費用為零。

| 候選 ID／目前狀態 | 已核實的差異與障礙 | 可執行的後續 |
| --- | --- | --- |
| `189b04da-bfce-437d-be2b-09e18ecbeded` Ledger／CryptoBilis，`manual_review`、Jev「可能重複」信心 0.830 | 本站 [10/12 舊文](https://mokaair.com/zh-TW/life/crypto-news-ledger-cryptobilis-exploit-20261012)原說裝置如何被竄改「尚未說明」；另一篇同日 72 小時更新亦未涵蓋 10/13 鑑識機制。候選來源為 [Ledger 官方 X 聲明](https://x.com/Ledger/status/2109896739985453358)；直接讀取 X 遇 403，[引用該聲明的報導](https://crypto.news/ledger-reveals-how-hidden-chips-stole-recovery-phrases/)稱新增微控制器擷取螢幕復原詞並以 eSIM／LTE 外傳。候選尚無五語草稿、事實清單、硬檢查；因此不是可以立即發布的已完成稿。 | 這是與 10/12 已刊「發現植入物」不同的**機制說明**，不宜只因同事件就當純重複退件。10/12 舊文的時點句已完成五語更正，見下。先補可原生讀取且可稽核的 Ledger 一手資料，再決定讓此候選寫新進展或編入既刊文；選「不是重複，繼續寫」會觸發付費 AI。新稿的五語與損失估算須獨立查核。 |
| `68acc96e-25c4-4121-b193-2fc98553d3e2` Manus／OPPO，`failed`／`AppError` | 保存了 10/13 [Manus 第一方公告](https://manus.im/blog/manus-partners-oppo)與 13 條事實，證據 SHA-256 `e0f482cf6ec9eba21664984c0bdc9c01c135a56280212e964ca917ffca454dea`；三次 Jev 重複檢查通過、信心 0.060。沒有五語草稿。失敗訊息為 `subscription_run_failed`：組織停用 Claude Code 訂閱存取，並建議使用 Anthropic API key 或由管理員開通；這是 provider／帳號障礙，不是新聞內容被判不合格。 | 保留故障狀態，先由帳號持有人確認 Claude 存取與先前呼叫／計費收據，再決定單筆重跑。後台僅提供整篇付費重跑或退件；不能因故障直接退掉有一手來源的獨立事件。 |
| `e7499e2e-fa42-49a2-8568-d264565d212c` 英國法院／約 61,000 BTC，`failed`／`AppError` | CoinDesk 10/13 來源保存 hash `5f80de1308a2ab6562f1096d070125404da9bf742fce28f4667a8daada3f506b`；Jev 重複檢查三次通過、信心 0.100。三次草稿 run 均回同一 `subscription_run_failed`／Claude 訂閱停用錯誤，UI 各顯示 `0 / 0` tokens；這不是零費用收據。沒有五語草稿／事實／硬檢。英國高等法院 [10/12 判決 [2026] EWHC 2509 (KB)](https://caselaw.nationalarchives.gov.uk/ewhc/kb/2026/2509)只決定受害者所有權主張將適用何地法律，並明言實體權利與證據仍待後續審理；判決記錄查扣超過 61,000 BTC。 | 保留為真實新事件與 provider 故障。先核帳號／付費收據，再決定單筆重跑；未來稿不可寫成英國政府已獲最終所有權或受害人無權取回。英文標題的「提高保留機會」是媒體推論，不是法院命令。 |
| `75fc82b8-95cf-4b5a-9847-2b69b89be3bc` Character.AI Chapter 11，`manual_review`／AI judge `needs human` | 19:00 新候選，Guide `7ef4ef32-0997-4b6c-9746-d13df042bc79`，來源只有 [The Verge](https://www.theverge.com/ai-artificial-intelligence/1009802/character-ai-files-for-bankruptcy-disney)，證據 SHA-256 `1a8284b9dae43e465f3a8af7c3830da389a4a1346ce02e1c19763514b306fa89`。AI judge 指出四語把 Google 招攬人才的「much」誇大為「大部分／大半／대부분」；zh-TW、zh-CN、ja、ko 均已保存為**草稿 v2**，改成「許多人才／许多人才／多くの人材／많은 인재」，en 保持草稿 v1。獨立查 [Character.AI 公告](https://www.businesswire.com/news/home/20261012656385/en/Character.ai-Initiates-Voluntary-Chapter-11-Proceeding-to-Facilitate-Value-Maximizing-Sale-Process)與[官方說明](https://blog.character.ai/an-update-on-character-ai/)又發現五語稿將 Disney Worldwide Services 擬議的 **2,000 萬美元加過渡服務、部分智慧財產權與公司請求權的非專屬永久授權起始競標**泛寫成「收購部分未公開資產」，混淆所有權與授權；交易仍待更高／更優出價及法院程序。 | 保持待審；先把官方來源加入可稽核的候選證據，按原生查核關卡修五語交易用語、服務條件、表格與 FAQ，復核後才考慮發布。現有「新增來源」只註冊掃描 feed，既存候選的 refresh／verify 不會加入新 URL；Guide 手工來源會在新聞重查核時被候選來源覆寫，不能用它繞過候選證據。未按「重新查核」或「五語發布」；沒有把 v2 草稿算作通過或公開。既存[來源擴充工作單](../tasks/open/2026-10-10-add-audited-source-extension-for-held.md)可涵蓋通用功能，但其受控套用名冊只有另三筆，需另明列本候選；目前 scope 與活躍工作單衝突，未強制認領。 |

## 已完成的既刊文時點更正

- 10/12 Ledger／CryptoBilis 已刊 Guide `85861504-be13-453a-a343-eefd1abb996d` 的五語原版均為已發布 v2。原正文與 FAQ 的「尚未說明植入方法」現在式，若在 10/13 讀取會與新的鑑識報導相衝；因此只把該句明確限定在 **2026-10-12 CoinDesk 報導當時**，連 FAQ 問題也加日期。沒有把仍缺原生可讀一手來源的 10/13 鑑識細節塞入 10/12 文章，也沒有改動損失估算。
- 18:25–18:31（Asia/Taipei）分別保存、填具體發布理由並發布 [zh-TW](https://mokaair.com/zh-TW/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[zh-CN](https://mokaair.com/zh-CN/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[en](https://mokaair.com/en/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[ja](https://mokaair.com/ja/life/crypto-news-ledger-cryptobilis-exploit-20261012)、[ko](https://mokaair.com/ko/life/crypto-news-ledger-cryptobilis-exploit-20261012)。五語編輯器均讀回 **已發布 v4**；五個公開頁的更正正文、FAQ 問題與展開後答案均已直接讀回。這是已刊 Guide 更正，**不改**三筆新候選的終態或 9／11 佇列。
- 以 Guide ID 篩正式站稽核，五筆 `guide_article_published` 在 18:26–18:31 均顯示成功；其中 [zh-TW 事件 `06593642-afb6-45f0-bb23-d5c1804919d2`](https://mokaair.com/zh-TW/admin/audit?target=85861504-be13-453a-a343-eefd1abb996d&page=1&event=06593642-afb6-45f0-bb23-d5c1804919d2)、[zh-CN 事件 `52c552a8-1f9b-4135-9b28-7117e4132af2`](https://mokaair.com/zh-TW/admin/audit?target=85861504-be13-453a-a343-eefd1abb996d&page=1&event=52c552a8-1f9b-4135-9b28-7117e4132af2)與 [en 事件 `9552d3ca-4185-4a9e-ad1b-8199e3adaf04`](https://mokaair.com/zh-TW/admin/audit?target=85861504-be13-453a-a343-eefd1abb996d&page=1&event=9552d3ca-4185-4a9e-ad1b-8199e3adaf04)的 ID 已讀到。ja／ko 成功列可見，展開詳情時遇 429 即停，未取得這兩筆事件 ID；不把未讀 ID 寫成已取得。18:31 再盤點仍為待審 9／需重寫 11。

## 下次接手的順序

1. Character.AI 先解決官方來源與候選證據不一致，修五語「收購資產」／「授權」混淆，再依原生 AI／人工關卡查核；四語 v2 僅修人才量詞，不等於全文可發布。
2. 19:00 已有一筆真實訂閱模型執行成功，但仍須核 Manus 與法院案先前 run 的帳號槽／計費收據；預設 B、額度畫面或 `0 / 0` tokens 都不是舊 run 零費用證明。精確 org-disabled 錯誤分類已本地驗證，待 PR 合併、正式站部署後才能改其失敗輪替。Anthropic API key 尚未設定，不自行改共用計費路徑或直接按整篇重跑。
3. Ledger 補可查的一手公告；10/12 舊文時點已更正，剩下是明確決定新稿或再更新既刊文，再走相應的五語查核和 Jev 關卡。
4. 每筆有後續動作時讀回候選、run、人工／AI 判斷、Guide 五語版本與公開頁；更新本名冊及同一 draft PR #1480。固定 70 筆終態仍按另一名冊單獨計算。
