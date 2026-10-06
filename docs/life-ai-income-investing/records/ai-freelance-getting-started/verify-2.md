# ai-freelance-getting-started — 第二輪查核（2026-10-05）

審稿人既不是撰稿人也不是第一輪查核人。範圍：第一輪改過或無法確認的每一項，加上 verify-1.md 主張清單第 2、5、8…行（每三行取一行），再做法遵與讀者優先審查。

## 讀法

- 出任務（taskergo、pricing、about-us、toolbox/contract、case.518.com.tw 轉址）、PRO360（pro/faq、how-pro360-work）、智慧財產局 電子郵件1140522c、全國法規資料庫（著作權法第 12 條、各類所得扣繳率標準）：`curl -sSL`，UA 用 Mokaair-editorial/1.0，全部 HTTP 200，讀之前先去掉 `<!-- -->` 註解與 script。
- Upwork 4 篇、Fiverr 2 篇：說明頁直接讀今天仍回 403。改讀同站 Zendesk 公開 API `/api/v2/help_center/en-us/articles/<id>.json`，HTTP 200，回應裡的 `html_url` 與 sources 網址相同。updated_at：211062538 2026-10-04、211062898 2026-10-05、211063718 2026-10-04、211063698 2026-10-04、34069565843985 2026-10-05、34998793899665 2026-10-04。
- 輔助腳本：_tools/ai-freelance-getting-started/zd.py、page.py（第一輪的檔案，原樣重跑），輸出存在 _tools/ai-freelance-getting-started/v2out/。

## A. 重查第一輪改過的項目

| 主張 | 結果 | 來源上的根據 |
|---|---|---|
| 出任務免費帳號每月只能解鎖 1 次聊聊，不限次數要付費訂閱 | 確認 | pricing：「解鎖聊聊 可與案主洽談更多細節 1次/月｜無限次」；注意事項「諮詢回覆次數（免費版 1 次/月）」 |
| 回覆案主訊息是否扣點寫「以官方公告為準」 | 確認，維持不變 | taskergo FAQ 說 T Points「用於兌換 TaskerGo……以及回覆案主的訊息」，收費總覽又說「基本提案免費」；兩處仍然並存 |
| 案主刊登一般案件免費，接案者基本提案免費 | 確認 | taskergo 收費總覽：發案端「刊登一般案件完全免費」；接案端「基本提案免費」 |
| 摘要「搶先提案、訂閱或報價等費用」 | 確認 | pricing 有月、季、年訂閱方案；PRO360 FAQ 寫報價費用 |
| Upwork 服務費在提案或邀約送出後就鎖定 | 確認，改了措辭 | 「Once a proposal, offer, or contract is sent, the Freelancer Service Fee is locked in」。原句「送出提案或邀約後」讀起來像是接案者送出邀約，但邀約是客戶送的；改成「提案或邀約一送出就鎖定」 |
| Connects 每個案件要用的數量不同 | 確認 | 「The number of Connects you'll need varies per job」 |
| 時薪計費週期以 UTC 計 | 確認 | 「begins on Monday at 00:00 midnight UTC and ends on the following Sunday at 23:59 UTC. Your funds become available 10 days later」 |
| Fiverr 帳號可能被永久停權 | 確認 | 「the freelancer's account may be permanently suspended」 |
| 「以 Upwork 為例」、站內連結文字、「30 天效期的方案」 | 確認 | ai-hallucination-fact-check 在內容目錄的標題，與 inline 文字一字不差；pricing「30 天效期・$600 起」 |

第一輪無法確認的項目：
- Upwork／Fiverr 403：重跑一次，結果相同；Zendesk API 讀法可以接受，sources 仍寫原本的說明頁網址。
- Tasker FAQ 與收費總覽互相矛盾：今天仍然矛盾，維持寫「以官方公告為準」。
- Fiverr 服務條款沒有讀：80% 與 14 天結清期出自 How Fiverr works for freelancers（「freelancers receive 80% of the client's cleared payment. Funds are subject to a 14-day clearing period」），這是第一手說明頁，足以作為來源。
- 字數：見 C 節。
- 撰稿人違反規則（git status、heredoc）：發生在先前的 session，現在無法補救。這一輪沒有執行 git，也沒有用含中文的 heredoc；改稿腳本用 Write 寫成檔案再執行。

## A. 隨機抽查（verify-1 主張清單第 2、5、8…行）

| 主張 | 結果 |
|---|---|
| case.518.com.tw 轉址到 tasker.com.tw | 確認（curl -L 的 effective URL 是 https://www.tasker.com.tw/） |
| 成交不抽成、沒有第三方金流服務費 | 確認（「目前不抽成，無第三方金流服務費」） |
| TaskerGo 30 天效期的方案 600 點起 | 確認（BASIC 30 Days Pass 提案額度 600；pricing「30 天效期・$600 起」；T Points 與新台幣 1:1） |
| 2025 年 7 月起停止代收付 | 確認（「2025/7 關閉第三方金流：停止代收付與第三方金流服務費，回歸雙方自行協議付款」） |
| PRO360 每次手動報價扣儲值金，金額依服務類別而定，報價時會提示 | 確認（FAQ 兩題） |
| Upwork 服務費 0% 到 15% | 確認（「ranges from 0% to 15% per contract」） |
| 實拿 20 美元、費率 10%，開 22.22 美元 | 確認（說明頁的範例；20÷0.9＝22.22） |
| 固定價合約由客戶先存入里程碑款項 | 確認（「clients must fund each milestone or project upfront」） |
| 時薪計費週期週一到週日 | 確認（同上，UTC） |
| Fiverr 14 天結清期，部分資格可縮短 | 確認（Top Rated、Fiverr Pro） |
| Fiverr AI 爭議看有沒有明顯錯誤、AI 幻覺，以及是否客製 | 確認（「free from clear mistakes or AI-generated hallucinations, and tailored to the client's specific needs」） |
| 圖解「AI 只做發想，成品要有你的實際創作」 | 確認（電子郵件1140522c 二(一)：有人類實際創意投入仍可受保護；二(二)：完全由 AI 演算獨立完成者無法享有著作權；發布日期 114-05-22） |
| 報價＝想實拿÷（1－抽成比例） | 確認（與 Upwork 範例一致） |
| 摘要「Upwork 0% 到 15%、Fiverr 80%」 | 確認 |
| 表格 caption「查證於 2026 年 10 月」 | 確認（也讓圖頁尾的 2026 在正文中有出處） |
| 3 個站內連結都在允許清單裡，而且存在 | 確認（content/ai-tools-choose-by-task.json、website-income-models.json、ai-hallucination-fact-check.json） |
| sources 15 筆 | 確認（9 筆直接回 200，6 筆透過 Zendesk API 回 200） |

另外順手核對：著作權法第 12 條第 2、3 項（未約定歸屬時著作財產權歸受聘人，出資人得利用）；各類所得扣繳率標準第 2 條第八款（執行業務報酬 10%）、第 13 條（每次扣繳稅額 2,000 元以下免扣繳）。正文沒有寫這些數字，維持原狀。

事實錯誤：零。第一輪的修正全部成立；唯一改動的事實相關句子是 Upwork 的鎖定時點，措辭改得更精確，意思沒有改變。

## B. 法遵審查

- 收入承諾：沒有「月入」「被動收入」「躺著賺」「輕鬆賺」，沒有收入截圖，也沒有見證。「工時制……收入也跟著變少」是說明計費方式的風險，不是收入承諾。
- 金額舉例：新台幣 800 元那一段原本就標了「以下數字都是假設」，但計算沒有完整寫出來。→ 改成「800×4＝3,200 元」，加上原有的 3,400÷0.8＝4,250，算式全部寫出。Upwork 的 20 美元例子原本沒有標「假設」，也沒有寫算式。→ 改成「假設想每小時實拿 20 美元……就要開 20÷0.9＝22.22 美元」。
- 平台費率要有日期：只有表格 caption 寫了日期，摘要與內文的費率旁邊都沒有。→ 摘要第 2 句開頭加「截至 2026 年 10 月」；平台一節的導言改成「以下是 2026 年 10 月的規則：……」。
- 不以兩個平台推論整體：原句「台灣平台多半不抽成」「國際平台則……」是從各兩個平台推論到所有平台。→ 改成「這裡的兩個台灣平台」「兩個國際平台」，Fiverr 部分寫「審核或結清期」。
- 不推薦平台：四個平台都只寫規則，沒有排名，沒有「推薦」，也沒有優劣比較。符合要求。
- 法律陳述：著作權寫明智慧財產局（主管機關）的解釋與著作權法第 12 條。稅的那一句原本沒有寫出依據。→ 改成「可能依各類所得扣繳率標準先扣繳稅款」，該法規已在 sources 裡，並且沒有寫稅率數字。個資那一條是實務建議（先確認工具的資料政策並取得客戶同意），沒有對個資法做法律陳述。正文沒有提到消保法、公平交易法。
- 責任歸屬：「AI 寫錯的地方由交付的人負責」原本是一句沒有出處的斷言。→ 接一句平台規則「以 Fiverr 為例，接案者要對交付成果完全負責」（「Freelancers are fully accountable for the final work they deliver」）。
- callout 的「客戶一眼就看得出來」是沒有來源的概括。→ 刪除。

## C. 讀者優先與文字

- 導言第一段原本是「關鍵不在會不會用工具，而在挑對案子……」，沒有直接回答問題。→ 改成一句話給出結論：「用 AI 接案，適合的是需求明確、成品能逐項檢查的案子，報價要把查證時間與平台費用算進去，交付前一定要自己檢查一次。」
- 「本文」「這篇」：0 次。
- 外文第一次出現都有中文：MTPE（譯後編修）、logo（標誌）、Freelancer Service Fee（服務費）、Connects 點數、T Points 點數、TaskerGo 搶先提案服務、UTC（世界協調時間）、聊聊（站內洽談訊息）。
- 正文沒有描述查證過程（沒有「查證時」「官網寫」「我們查不到」「本批」「撰稿」）。「Fiverr 的規定是」「智慧財產局的解釋是」是在說明規則本身與主管機關，不是在描述查證過程。callout 原本的「回說明頁再確認」改成「再回平台確認」。
- 用語符合台灣用法，沒有驚嘆號，也沒有「總結來說」。
- 出任務那一段原本寫「訂金、分期與驗收條件都要寫進合約」，與後面合約清單的「訂金、分期與驗收後的付款時間」重複。→ 改成「付款與驗收條件要自己寫進合約」。
- 字數：第一輪 2,714 字，第二輪 2,784 字（intake 區間 1,800–3,000，通過）。增加的字數全部來自法遵要求：算式、日期、法規名稱、平台責任規則。超過 §10.6 建議的 2,600 字。我找過沒有灌水的段落可以刪：表格與內文重複是規格要求，每節的段落也都承載不同的規則，所以沒有為了壓字數而刪掉事實。協調者如果要壓到 2,600，最可刪的是 callout 第二句（與合約清單第 3 項重複），以及最後一段「檢查完留一份簡單紀錄」。

## 圖

hero.png、diagram-1.png 重新渲染並打開檢查：標籤沒有壓線，沒有溢出，構圖置中；hero 只有一行字「AI 接案入門」，沒有長條、曲線、金幣、logo 或人臉；alt 與畫面一致。圖上唯一的數字 2026，正文裡有出現。

## 機械關卡

- `pack_cli ingest --dry-run`：exit 0，「dry run: nothing written」。
- `intake_check.py`：RESULT PASS（0 failures），body_length=2784。
- 改稿腳本：_tools/ai-freelance-getting-started/verify2_edit_pack.py（12 處逐字替換，每處都斷言只比對到一次）。
