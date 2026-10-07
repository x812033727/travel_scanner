# ai-content-side-business-costs — 查核第二輪（2026-10-05）

第二輪查核者（非撰稿者、非第一輪）。所有來源今天自己重開：`curl -sSL`，UA
`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，確認 HTTP 狀態，去掉 `<!-- -->`、script、style 後讀本文。
腳本與快取：`/home/user/batch-ai-income/_tools/ai-content-side-business-costs/v2/`（fetch.py、cache/、scan.py、edit*.py）。

讀法：22 個網址中 21 個 HTTP 200。Substack 說明頁仍回 Cloudflare 403（「Just a moment...」），web.archive.org CDX
連線被重設（curl 35）；改讀同網域官方 Zendesk JSON（`support.substack.com/api/v2/help_center/en-us/articles/<id>.json`，HTTP 200，
360037607131 updated_at 2026-10-05T00:45:19Z、360041314672 updated_at 2026-10-03T13:52:17Z），sources 保留原始說明頁網址。

格式：主張｜結果（ok / fixed / softened）｜來源｜讀到的原文

## A1. 第一輪改過的項目（全部重查）

- WordPress.com 年繳以上第一年附自訂網域，月繳不附｜ok｜https://wordpress.com/pricing/｜「Free domain for one year with annual plans.」「All annual and multi-year paid plans include a free custom domain for the first year… Monthly plans do not include a free domain.」
- AdSense 資格補「符合計畫政策」｜ok｜https://support.google.com/adsense/answer/9724｜「If you have your own content that meets our policies and you're 18 or over」「Does your content comply with the AdSense Program policies?」
- 摘要 YPP 門檻「一年 4,000 小時」「90 天 1,000 萬次 Shorts」｜ok｜https://support.google.com/youtube/answer/72851｜「1,000 subscribers with 4,000 qualified watch hours in the last 12 months, or … 10 million qualified Shorts views in the last 90 days」
- 擴大版「過去 90 天 3 部有效公開上傳」｜ok｜https://support.google.com/youtube/answer/13429240｜「500 subscribers with 3 valid public uploads in the last 90 days, and 3,000 qualified watch hours in the last 12 months, or … 3 million qualified Shorts views in the last 90 days」
- 「YouTube Premium（YouTube 的付費訂閱服務）」｜ok｜https://support.google.com/youtube/answer/12843009｜「Updating YPP ads & Premium entry thresholds」；括號說明不與頻道會員（粉絲贊助）混淆
- Shorts 創作者收益池 1,000 萬次、未達標不會被移出 YPP｜ok｜https://support.google.com/youtube/answer/12843009｜「you will not be removed from YPP and this will not impact other YPP earnings」；zh-Hant「未達這個門檻不會失去 YouTube 合作夥伴計畫資格」
- 「不會限縮影片的觀眾群」，也不影響營利資格｜ok｜https://support.google.com/youtube/answer/14328491｜「Disclosing AI content won't limit a video's audience or impact its eligibility to earn money.」
- 「依訓練資料預測可能的字詞序列」｜ok｜https://developers.google.com/search/docs/fundamentals/using-gen-ai-content｜「generative models don't retrieve facts, but predict a likely sequence of words based on their training data」
- 篇幅｜ok｜intake_check：第一輪 2,653 字，第二輪改完 2,647 字，在 1,800–3,000 內

## A2. 第一輪無法確認的項目（重查）

- Substack 費用與收款地區：說明頁仍 403、Wayback 仍不通；官方 Zendesk JSON 今天讀到「Publishing on Substack is free, no matter how many subscribers you have. If you turn on paid subscriptions, Substack keeps 10% of subscription revenue, and Stripe charges its own payment processing fees.」「10% of each subscription payment」，以及「If you're planning to add paid subscriptions, you can view a list of countries supported by Stripe, our payments provider.」內容與正文一致。
- WordPress.com 續約價：原始 HTML 仍是未填值範本「Auto-renews at %(renewalMonthlyPrice)s per month」（144 處），正文維持「續約價以結帳頁為準」。價格以 US$ 顯示是本環境出口所見，表格 caption 寫「價格照各官網標示的幣別」，沒有寫成台灣訪客一定看到美元；維持。
- Shorts 收益池生效日：英文版列在「Starting February 1, 2027, we are introducing updates」底下；zh-Hant 版寫「現在起」。兩版仍不一致，正文「同一波更新也規定」不寫日期，維持。
- 字數 2,647，比 2,200–2,600 的目標多 47 字，仍在 1,800–3,000 區間。逐段看過沒有灌水段落；刪掉了與 callout 重複的一句（見 C）。剩下的都是規則與數字，不再為了湊目標硬刪。
- 每週時數：三組數字都標「（假設）」，加總 6＋3.5＋9＝18.5，18.5÷7≈2.64 →「平均每天兩個半小時以上」正確。ChatGPT 與剪輯軟體價格仍不寫數字（「以官方公告為準」與站內比較文），維持。

## A3. 其餘主張隨機三分之一（verify-1.md 的主張行，從第 2 行起每隔三行）

- Personal 月繳每月 US$9｜ok｜https://wordpress.com/pricing/｜價格列「US$ 9 US$ 4 US$ 3.25 US$ 2.75 per month … Save 55%」
- 續約價以結帳頁為準｜ok｜同上（見 A2）
- AdSense 資格條件沒有流量數字｜ok｜https://support.google.com/adsense/answer/9724｜整頁只有 18 歲一個數字條件
- Substack 付費訂閱抽 10%，另加 Stripe 手續費｜ok，措辭 fixed｜Zendesk JSON｜「10% of each subscription payment」；正文「抽收入的 10%」改「從每筆訂閱款抽 10%」，避免讀成抽全部收入
- beehiiv 免費方案最多 2,500 位訂閱者｜ok｜https://www.beehiiv.com/pricing｜「Subscribers, Free, Up to 2,500」「Free includes up to 2,500 subscribers」
- beehiiv 付費方案依訂閱人數計價｜ok｜同上｜「Pricing for 1,000 subscribers」加訂閱人數滑桿；Lite「$49 /mo Yearly billing」只是 1,000 人時的預設值，正文不寫金額
- Google AI Plus 台灣每月 NT$165｜ok｜https://gemini.google/tw/subscriptions/?hl=zh-TW｜「每月 NT$ 165 元」；AI Pro「每月 NT$ 650 元」
- Claude Pro 月繳 US$20，不含稅｜ok｜https://claude.com/pricing｜「$20 if billed monthly.」「Prices shown don't include applicable tax.」
- 部落格 6、電子報 3.5、短影音 9 小時｜ok｜計算（假設，無來源）
- 使用 AI 不會帶來特殊排名優勢｜ok｜https://developers.google.com/search/blog/2023/02/google-search-and-ai-content｜「Using AI doesn't give content any special gains.」「Appropriate use of AI or automation is not against our guidelines.」
- 譯名「大量內容濫用」｜ok｜https://developers.google.com/search/docs/fundamentals/using-gen-ai-content?hl=zh-tw｜「Google 針對大量內容濫用行為的垃圾內容政策」
- 「誰、怎麼做、為什麼」｜fixed（措辭）｜https://developers.google.com/search/docs/fundamentals/creating-helpful-content｜原文是「If automation is used to substantially generate content」，指內容主要由自動化產生，不是「大量」；正文「大量用自動化產生內容時」改為「內容主要靠自動化產生時」。「primarily making content to attract search engine visits, that's not aligned」→「不是吸引搜尋流量」ok
- 揭露位置「屬性」→「AI 使用情形」選「是」｜ok｜https://support.google.com/youtube/answer/14328491?hl=zh-Hant｜「請在「屬性」部分的「AI 使用情形」下方輕觸「是」」
- 經常不揭露可能被移除內容或暫停 YPP｜ok｜同上 en｜「consistently choose not to disclose … removal of content or suspension from the YouTube Partner Program」
- 台灣適用擴大版 YPP｜ok｜https://support.google.com/youtube/answer/13429240｜國家名單「… Switzerland Taiwan Thailand …」
- 廣告分潤門檻（正文）｜ok｜https://support.google.com/youtube/answer/72851｜同 A1
- 已在 YPP 者不受影響；粉絲贊助門檻不變｜ok｜https://support.google.com/youtube/answer/12843009｜「If you are already in YPP, your status is not impacted」「There are no changes to the eligibility requirements for fan funding」
- 未達收益池門檻不會被移出 YPP｜ok｜同 A1
- hero 無數字、無 logo、一行字 ≥ 40px，alt 與渲染一致｜ok｜重新渲染看過：時鐘、兩顆橘色火花、三條虛線連筆電／信封／手機，底部一行「用 AI 經營內容副業」，構圖置中
- checked_on 全部 2026-10-05｜ok｜intake_check

另外順手核對（不在抽樣內但正文有用到）：大量內容濫用定義與兩個例子（spam-policies「many pages are generated for the primary purpose of manipulating search rankings」「Using generative AI tools … to generate many pages without adding value」「Scraping … automated transformations like synonymizing, translating」）ok；Stripe 名單（https://stripe.com/global）仍沒有台灣 ok；YouTube 自動字幕語言含 Chinese、「Always review automatic captions」ok；「空泛或重複性內容」是 zh-Hant 現行小節名，例子「使用一般或非原創範本製作的 AI 生成內容…缺乏創作者的原創思維或真實觀點」ok；YPP 頻道審查「review your channel as a whole」ok。

diagram-1 重新渲染看過：三列五格、箭頭不壓字、圖例在下方、右下 © 2026；正文「查證於 2026 年 10 月」有 2026。

## B. 法遵（AI 賺錢篇）

- 收入承諾：全文沒有「月入」「被動收入」「躺著賺」「輕鬆賺」「保證」，沒有收入截圖或見證；導言明寫「收入因人而異，這裡只談成本、時間與規則」。通過。
- 金額示例：沒有收入示例；唯一的試算是每週時數，三項都標「（假設）」並列出每一步的時數與加總。通過。
- 平台費率：Substack 10%、beehiiv 0% take rate（寫成「平台不抽成」）、Stripe 手續費只說「另加」不寫數字，都照平台自己的頁面；表格 caption 寫「查證於 2026 年 10 月」。通過。
- 法律陳述：正文沒有稅法、著作權、個資法、消保法、公平交易法的陳述；平台規則（Google 搜尋、YouTube）都有官方頁。通過。
- 推薦：WordPress.com、Substack、beehiiv、Google AI、Claude 只陳述規則與價格，沒有「比較好」「首選」；「先選一種」指內容形式，不是平台。「Google 的方案在台灣直接標新台幣」是幣別事實，不是推薦。通過。
- 「人在台灣要先解決收款管道」只指出限制，沒有教人規避 Stripe 的國家限制。通過。

## C. 讀者優先與文風

- 出處不在句子裡敘述：正文以平台為主詞陳述規則（「Google 建議…」「YouTube 要求…」），沒有「官網寫」「查證時」「我們查不到」「本批」「撰稿」。通過。
- 「本文」「這篇」：0 次。通過。
- 外文詞第一次出現附中文：Google AdSense（Google 的網站廣告計畫）、Stripe（金流商）、Shorts（短影音）、scaled content abuse（大量內容濫用）、YPP（YouTube 合作夥伴計畫）、YouTube Premium（YouTube 的付費訂閱服務）、YouTube 工作室；WordPress.com、Substack、beehiiv、Personal、Lite、AI Plus、AI Pro、Claude Pro 是產品與方案名。通過。
- 台灣用語：軟體、影片、使用者、資料；沒有驚嘆號、沒有「總結來說」。通過。
- 導言第一段第一句「用 AI 經營內容副業，開辦費可以壓得很低，吃緊的是時間。」一句話回答問題。通過。
- 重複：「記下自己前四週每一步的實際時數」在時間一節開頭與 callout 各出現一次；時間一節開頭改為「下面的數字都是假設，只示範怎麼拆，實際時數以自己的紀錄為準：」，四週紀錄留給 callout。
- 字數 2,647（目標 2,200–2,600，區間 1,800–3,000），見 A2。

## 改動清單

1. 「大量用自動化產生內容時」→「內容主要靠自動化產生時」（helpful content 原文 substantially generate）——事實精確度。
2. 「開了付費訂閱才抽收入的 10%」→「開了付費訂閱才從每筆訂閱款抽 10%」（Substack「10% of each subscription payment」）——措辭精確度。
3. 時間一節開頭刪去與 callout 重複的「記下前四週」一句——文風。

機械關卡：`pack_cli ingest --dry-run` 通過（dry run: nothing written）；`intake_check.py` RESULT PASS（0 failures），body_length 2,647，自稱 0 次，圖上數字都在正文。
