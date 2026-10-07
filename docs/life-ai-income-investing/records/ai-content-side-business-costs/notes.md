# ai-content-side-business-costs — 查證紀錄

查證日一律 2026-10-05。格式：主張｜來源網址｜查證日｜怎麼讀到的。

讀法說明：
- 「curl」= `curl -sSL`，UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，確認 HTTP 200，
  去掉 `<!-- -->` 註解與 script／style 後讀本文。腳本：/home/user/batch-ai-income/_tools/ai-content-side-business-costs/page.py、art.py。
- 「Zendesk API」= Substack 說明中心網頁對本環境回 403；改讀官方公開 JSON
  `https://support.substack.com/api/v2/help_center/en-us/articles/<id>.json`（HTTP 200，回應含 html_url 與 updated_at），
  sources 寫原始說明頁網址。腳本：zd.py。
- 「WebFetch」= 頁面靠 JavaScript 填值時，用 WebFetch 再讀一次渲染後的內容交叉。
- 本環境的出口在美國，WordPress.com、Gemini 國際頁、Claude 定價頁都以美元顯示；台灣定價只用 gemini.google/tw 的台灣頁。

## 部落格

- WordPress.com 免費方案的網站會向訪客顯示 WordPress.com 廣告，升級 Personal 才關掉｜https://wordpress.com/pricing/｜2026-10-05｜curl 200：「Free sites display WordPress.com ads to visitors. Upgrade to Personal to turn them off.」
- Personal 月繳每月 US$9；年繳折算每月 US$4（Save 55%）；兩年 US$3.25、三年 US$2.75（正文只用月繳與年繳）｜https://wordpress.com/pricing/｜2026-10-05｜curl 200 價格列 + WebFetch 交叉（Monthly $9、Yearly $4/month）
- 價格不含稅（excl. taxes）；續約價在靜態 HTML 是未填值的範本「Auto-renews at %(renewalMonthlyPrice)s」，頁面另有 `wpcom_renewal_pricing_increase` 實驗旗標 → 正文寫「續約價以結帳頁為準」｜https://wordpress.com/pricing/｜2026-10-05｜curl 200 原始 HTML
- 「年繳比月繳便宜一半以上」：4÷9＝0.44，頁面標 Save 55%｜同上｜2026-10-05｜計算 + 頁面標示
- 第一年免費自訂網域只限年繳以上：「Free domain for one year with annual plans.」「All annual and multi-year paid plans include a free custom domain for the first year… Monthly plans do not include a free domain.」（查核第一輪更正：原稿寫「付費方案第一年附自訂網域」）｜https://wordpress.com/pricing/｜2026-10-05｜curl 200
- AdSense 資格：年滿 18 歲、有自己的原創且符合政策的內容、要能存取所提交網站的 HTML 原始碼；資格條件裡沒有任何流量或訂閱數字｜https://support.google.com/adsense/answer/9724｜2026-10-05｜curl 200（hl=en）
- 「仍要通過審核」：同頁提到 AdSense site approvals（網站核准）系列影片，表示網站送出後要經核准｜同上｜2026-10-05｜curl 200（見 doubts：措辭是推論）

## 電子報

- Substack 不論訂閱人數都免費發行；開啟付費訂閱後 Substack 收每筆訂閱款的 10%，Stripe 另收金流手續費｜https://support.substack.com/hc/en-us/articles/360037607131-How-much-does-Substack-cost｜2026-10-05｜Zendesk API 200，updated_at 2026-10-05T00:45:19Z
- Substack 自訂網域一次 US$50（初稿用過，最後一版正文已刪）｜同上｜2026-10-05｜Zendesk API
- Substack 的收款服務商是 Stripe，付費訂閱要看 Stripe 支援國家名單｜https://support.substack.com/hc/en-us/articles/360041314672-Are-there-any-countries-or-geographies-where-payments-aren-t-supported-on-Substack｜2026-10-05｜Zendesk API 200
- Stripe 支援國家／地區名單（Global availability）沒有台灣（有香港、日本、新加坡、泰國、馬來西亞等）｜https://stripe.com/global｜2026-10-05｜curl 200，逐項讀名單
- beehiiv 免費方案訂閱者上限「Up to 2,500」｜https://www.beehiiv.com/pricing｜2026-10-05｜curl 200 Plan limits 表 + WebFetch 交叉
- beehiiv 付費訂閱（Paid subscriptions, 0% take rate）列在 Lite 方案；FAQ：beehiiv 不從付費訂閱與數位商品收入抽成，只扣 Stripe 標準手續費 → 正文「付費訂閱從 Lite 方案開始，平台不抽成」「兩家的付費訂閱都經 Stripe 收款」｜同上｜2026-10-05｜curl 200
- beehiiv 付費方案價格隨訂閱人數滑桿變動（預設 1,000 位時 Lite 顯示 $49/mo、Pro $95/mo，標示 Yearly billing），靜態頁與 WebFetch 對「月繳或年繳折算」的讀法不一致 → 正文不寫金額，只寫「依訂閱人數計價」｜同上｜2026-10-05｜curl + WebFetch

## 短影音與 AI 訂閱

- YouTube 自動字幕支援語言包含 Chinese；口音、方言、背景噪音等會造成錯誤，官方要求創作者一律檢查並修正｜https://support.google.com/youtube/answer/6373554｜2026-10-05｜curl 200（hl=en）
- Google AI Plus 台灣每月新台幣 165 元（免費方案 2 倍用量、可用影片生成）｜https://gemini.google/tw/subscriptions/?hl=zh-TW｜2026-10-05｜curl 200，台灣頁「每月 NT$ 165 元」
- Google AI Pro 台灣每月新台幣 650 元（免費方案 4 倍用量、可用影片生成）｜同上｜2026-10-05｜curl 200，「每月 NT$ 650 元」
- 「Google 的方案在台灣直接標新台幣」｜同上｜2026-10-05｜台灣頁價格以 NT$ 標示
- Claude Pro 月繳每月 US$20；年繳折算每月 US$17（一次付 US$200）；價格不含稅｜https://claude.com/pricing｜2026-10-05｜curl 200：「$17 Per month with annual subscription discount ($200 billed up front). $20 if billed monthly.」「Prices shown don't include applicable tax.」（正文表格只用月繳 20 美元）
- ChatGPT 方案價格：chatgpt.com/pricing、openai.com/chatgpt/pricing、help.openai.com 對 curl 與 WebFetch 都回 403，web.archive.org 連線被重設 → 正文不寫 ChatGPT 價格，改連站內比較文｜—｜2026-10-05｜讀不到
- 剪輯軟體價格沒有查證 → 表格寫「以官方公告為準」｜—｜2026-10-05｜—

## 每週時間（全部是假設）

- 部落格 2＋0.5＋2＋1＋0.5＝6 小時；電子報 1.5＋0.5＋1＋0.5＝3.5 小時；短影音 1.5＋2＋3＋1.5＋1＝9 小時；合計 18.5 小時；18.5÷7＝2.64 →「平均每天兩個半小時以上」｜無來源，正文每項標明「假設」｜2026-10-05｜計算

## Google 搜尋

- 生成式模型不是檢索事實，而是依訓練資料預測可能的字詞序列，所以會有幻覺；發布前要人工查核所有 AI 產出，包括 title 元素、meta description、結構化資料與圖片替代文字｜https://developers.google.com/search/docs/fundamentals/using-gen-ai-content｜2026-10-05｜curl 200（hl=en；zh-tw 版缺「hallucinations」與人工查核那句，以英文版為準）
- 用生成式 AI 產生大量對使用者沒有附加價值的頁面，可能違反大量內容濫用（scaled content abuse）政策｜同上｜2026-10-05｜curl 200
- 大量內容濫用的定義與例子：為操控排名而大量產生網頁；例子含用生成式 AI 大量產生頁面、抓取內容後以同義詞替換或翻譯等自動轉換產生頁面｜https://developers.google.com/search/docs/essentials/spam-policies｜2026-10-05｜curl 200（hl=en）；中文譯名「大量內容濫用」取自 using-gen-ai-content 的 zh-tw 版
- 「適當使用 AI 或自動化功能並不會違反我們的規範」「使用 AI 並不會為內容帶來任何特殊排名優勢」｜https://developers.google.com/search/blog/2023/02/google-search-and-ai-content｜2026-10-05｜curl 200（伺服器依 Accept-Language 轉到 zh-tw 版）
- 「誰、怎麼做、為什麼」；大量用自動化產生內容時，揭露並說明 AI 怎麼用、為何有用；目的應是幫助人而非吸引搜尋流量｜https://developers.google.com/search/docs/fundamentals/creating-helpful-content｜2026-10-05｜curl 200（en 與 zh-tw）
- 用 AI 生成的大頭照、虛構姓名或假資歷讓內容看似專家撰寫，屬於欺騙｜同上｜2026-10-05｜curl 200（hl=en，"Fabricating creator profiles…is a form of deception"）

## YouTube

- 必須揭露的生成式 AI 內容：讓真人看似說或做了沒做過的事、變造真實事件或地點的畫面、生成看似真實但沒發生的場景、以 AI 音樂為影片主體｜https://support.google.com/youtube/answer/14328491｜2026-10-05｜curl 200（en 與 zh-Hant）
- 揭露位置：YouTube 工作室上傳流程「屬性」區塊的「AI 使用情形」選「是」（英文版為 Attributes → AI use）｜同上｜2026-10-05｜curl 200 zh-Hant
- 不需揭露的例子包括用生成式 AI 做大綱、腳本、縮圖、標題、資訊圖表，字幕製作，複製自己的聲音做旁白或配音｜同上｜2026-10-05｜curl 200
- 揭露不會限制影片觀眾，也不影響營利資格；經常不揭露可能被手動加標籤、移除內容或暫停 YPP｜同上｜2026-10-05｜curl 200
- 頻道營利政策「空泛或重複性內容」（Generic or Repetitive Content）不能營利的例子：使用一般或非原創範本製作的 AI 生成內容，給人大量產製的感覺，缺乏創作者的原創思維或真實觀點｜https://support.google.com/youtube/answer/1311392｜2026-10-05｜curl 200（en 與 zh-Hant；頁首 2025-07-15 公告寫把 repetitious content 改名 inauthentic content，現行小節標題又是 Generic or Repetitive Content，正文只用現行小節名）
- YPP 廣告分潤門檻：1,000 位訂閱者＋過去 12 個月 4,000 小時有效觀看時數，或 1,000 位訂閱者＋過去 90 天 1,000 萬次有效 Shorts 觀看；Shorts 動態的觀看時數不計入 4,000 小時｜https://support.google.com/youtube/answer/72851｜2026-10-05｜curl 200（en 與 zh-Hant）
- 擴大版 YPP：500 位訂閱者＋過去 90 天 3 部有效公開上傳，再加過去 12 個月 3,000 小時有效觀看時數或過去 90 天 300 萬次有效 Shorts 觀看；提早使用粉絲贊助與購物功能｜https://support.google.com/youtube/answer/13429240｜2026-10-05｜curl 200（hl=en）
- 擴大版 YPP 適用國家／地區名單包含 Taiwan｜同上｜2026-10-05｜curl 200，逐項讀名單
- 2027 年 2 月 1 日起新創作者的 YPP 廣告與 Premium 門檻：1,000 位訂閱者＋過去 365 天 8,000 小時有效觀看時數，或過去 90 天 2,000 萬次有效 Shorts 觀看；已在 YPP 者不受影響｜https://support.google.com/youtube/answer/12843009｜2026-10-05｜curl 200（en 與 zh-Hant）
- 粉絲贊助、YouTube 創作者合作計畫、YouTube Shopping 的資格不變（500 位訂閱者＋3,000 小時或 300 萬次 Shorts 觀看）｜同上｜2026-10-05｜curl 200
- Shorts 創作者收益池：要每月分潤，過去 90 天有效 Shorts 觀看須維持 1,000 萬次（英文版列在 2027 年 2 月 1 日更新底下，zh-Hant 版寫「現在起」）→ 正文寫「同一波更新也規定」，不寫生效日｜同上｜2026-10-05｜curl 200（見 doubts）
- 頁首：須在 2027 年 1 月 31 日前接受新版條款（初稿用過，最後一版正文已刪）｜https://support.google.com/youtube/answer/72851｜2026-10-05｜curl 200

## 站內連結

- ai-free-vs-paid-plans-2026、email-newsletter-planning、ai-for-youtube-creators、website-income-models 四篇都存在於 apps/api/app/guides/content/，kind=life，有 zh-TW；連結文字用各篇 zh-TW 標題｜repo｜2026-10-05｜intake_check 逐一 ok

## 圖

- diagram-1.svg 上唯一的數字是頁尾 2026，正文表格 caption「查證於 2026 年 10 月」有｜—｜2026-10-05｜intake_check「every number on the diagram is in the text」
- diagram 每一格步驟名稱都對應正文：大綱與初稿／標題與摘要／字幕初稿／腳本初稿（AI 能縮短清單）；查證、親身經驗、拍攝錄音剪輯、經營讀者（省不了清單）；校對與揭露（字幕校對 + YouTube 揭露）
- hero.svg：時鐘、兩顆橘色星形火花、三條虛線連到筆電、信封、手機；一行字「用 AI 經營內容副業」56px；沒有長條、曲線、金幣、logo、人臉；alt 已依最後渲染結果改寫

## 查核第一輪（2026-10-05，另一位查核者逐條重開官方頁）

讀法：自己的 curl 快取（/home/user/batch-ai-income/_tools/ai-content-side-business-costs/v1/pg.py、zd.py），不沿用撰稿者快取。
Substack 說明頁對 curl 回 Cloudflare「Just a moment...」403，web.archive.org CDX 連線被重設，改讀同網域官方 Zendesk JSON
（360037607131 updated_at 2026-10-05T00:45:19Z；360041314672 updated_at 2026-10-03T13:52:17Z），sources 保留原始說明頁網址。
其餘 16 個來源網址 curl -sSL 皆 HTTP 200。

- 更正：WordPress.com 免費網域只限年繳以上，月繳不附｜https://wordpress.com/pricing/｜2026-10-05｜curl 200
- 更正：AdSense 資格補上「內容要符合計畫政策」（「your own content that meets our policies」「Does your content comply with the AdSense Program policies?」）｜https://support.google.com/adsense/answer/9724｜2026-10-05｜curl 200 hl=en
- 更正：摘要的 YPP 門檻補上期間（過去 12 個月 4,000 小時、過去 90 天 1,000 萬次 Shorts）｜https://support.google.com/youtube/answer/72851｜2026-10-05｜curl 200 hl=en
- 更正：擴大版 YPP 是「3 valid public uploads in the last 90 days」，不限長影片｜https://support.google.com/youtube/answer/13429240｜2026-10-05｜curl 200 hl=en
- 更正：YouTube Premium 原括號「付費會員」易與頻道會員（粉絲贊助）混淆，改為「YouTube 的付費訂閱服務」｜https://support.google.com/youtube/answer/12843009｜2026-10-05｜curl 200
- 補充：Shorts 創作者收益池未達 1,000 萬次「will not be removed from YPP」｜https://support.google.com/youtube/answer/12843009｜2026-10-05｜curl 200 hl=en 與 zh-Hant
- 措辭：揭露 AI「won't limit a video's audience」→「不會限縮影片的觀眾群」（原「觸及」）｜https://support.google.com/youtube/answer/14328491｜2026-10-05｜curl 200
- 措辭：「predict a likely sequence of words based on their training data」→「依訓練資料預測可能的字詞序列」｜https://developers.google.com/search/docs/fundamentals/using-gen-ai-content｜2026-10-05｜curl 200 hl=en

## 查核第二輪（2026-10-05，第三位查核者）

讀法：自己的 curl 快取（/home/user/batch-ai-income/_tools/ai-content-side-business-costs/v2/fetch.py、cache/），22 個網址 21 個 HTTP 200；
Substack 說明頁仍回 Cloudflare 403、web.archive.org CDX 仍被重設，改讀同網域官方 Zendesk JSON（HTTP 200）。細節見 verify-2.md。

- 更正（措辭）：「大量用自動化產生內容時」→「內容主要靠自動化產生時」（「If automation is used to substantially generate content」）｜https://developers.google.com/search/docs/fundamentals/creating-helpful-content｜2026-10-05｜curl 200 hl=en
- 更正（措辭）：Substack「抽收入的 10%」→「從每筆訂閱款抽 10%」（「10% of each subscription payment」）｜https://support.substack.com/hc/en-us/articles/360037607131-How-much-does-Substack-cost｜2026-10-05｜Zendesk API 200

## 機械與視覺關卡（2026-10-05）

- pack_cli ingest --dry-run：通過；intake_check：0 FAIL，1 WARN（no hero title found to check uniqueness，自繪 hero 沒有 images.json，屬預期）。
- 正文計字 2,647（工具計法含摘要與表格、非空白字元；其中漢字 1,839），在 1,800–3,000 區間內，略高於 2,200–2,600 的目標；事實已過兩輪查核，未為湊區間刪內容。
- hero.png、diagram-1.png 重新渲染並逐張看過：無文字壓線、無溢框、箭頭為 butt 線帽、字級全部 ≥ 15；圖上唯一的數字 2026 出現在表格 caption「查證於 2026 年 10 月」。
- 只改了說明文字：hero alt 的「右上角」改為「時鐘右上方」；diagram-1 的 alt 與 caption 把「橘色格」改為「橘框白底格」、「青綠色」改為「青綠底格」，與實際畫面一致。
- hero 與同批其他 11 張 hero 構圖不同（本篇是時鐘居中、三條虛線連到筆電、信封、手機；同批沒有時鐘或信封）。

## 跨篇核對（2026-10-05）

- 新增姊妹篇連結：ai-money-making-course-red-flags（每週時間一節後）。
