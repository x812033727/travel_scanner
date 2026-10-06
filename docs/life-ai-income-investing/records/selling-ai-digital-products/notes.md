# selling-ai-digital-products — 查證紀錄

查證日一律 2026-10-05。格式：主張｜來源網址｜查證日｜怎麼讀到的。

讀法說明：
- 「curl 200」= `curl -sSL`，UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，HTTP 200，去掉 `<!-- -->` 註解與 script／style 後讀本文。腳本：/home/user/batch-ai-income/_tools/selling-ai-digital-products/page.py；讀回的文字檔存在同一目錄（*.txt）。
- 「Zendesk API」= Etsy 說明中心網頁對本環境回 403，改讀同一篇文章的公開 JSON API `https://help.etsy.com/api/v2/help_center/en-us/articles/<id>.json`（HTTP 200，回應含 html_url 與 updated_at，內容即說明頁本文）。腳本 zd.py、zdsearch.py。sources 寫原始說明頁網址。
- 「Inertia JSON」= Gumroad 說明中心頁面本文放在 `data-page` 屬性的 JSON 裡，curl 200 後解出 JSON 讀本文。腳本 inertia.py。
- 「搜尋摘要」= helpx.adobe.com 與 help.openai.com 對 curl 與 WebFetch 都回 403（Akamai／Cloudflare）；OpenAI 說明中心的 `.json` 讀法也已失效（301 轉回 HTML 再 403）。web.archive.org 在本環境連線被重設（代理紀錄 ws_closed_mid_exchange，重試多次），archive.org/wayback/available 只回得出快照索引（Adobe 規範頁最近快照 20260924204905），讀不到快照內容。所以這兩站的條目改用 WebSearch 限定官方網域（helpx.adobe.com、help.openai.com），讀搜尋結果對該頁的摘要，每條至少兩次不同查詢交叉一致才寫。sources 仍寫原始網址。**這些條目請查核者優先重讀。**

## 圖庫：Adobe Stock

〔查核第一輪：helpx 規範頁仍讀不到；正文只留勾選、虛構、授權書、提示詞不提名人與品牌四點，其餘改為以官方規範為準；見文末〕

- Adobe Stock 接受的內容類型包括 Gen AI（「We accept many types of content such as photos, illustrations, videos, vectors, Gen AI and more」）｜https://contributor.stock.adobe.com/｜2026-10-05｜curl 200，FAQ「How can I start selling my content?」
- 投稿內容用在 Adobe Stock、Firefly、Express 與 Creative Cloud（「Your submissions will fuel Adobe Stock, Firefly, Express, and Creative Cloud」）｜https://contributor.stock.adobe.com/｜2026-10-05｜curl 200
- 投稿是非專屬合作、保有作品權利（「you enter a non-exclusive partnership」）｜https://contributor.stock.adobe.com/｜2026-10-05｜curl 200，FAQ「Do I keep the rights」
- 作者分成：圖片（Photos, vectors, illustrations）33%、影片 35%；每次下載實拿金額依買家方案而定（表列 3 credits 月訂 $3.30 到 350+ credits 的 $0.33–$0.40 等，正文未寫具體金額）｜https://contributor.stock.adobe.com/royalties｜2026-10-05｜curl 200，Earnings Breakdown
- 投稿協議 2024 年 6 月 18 日生效；第 1 條授權 Adobe 用於營運網站、推廣、授權給使用者、開發新功能與服務；第 4 條所有權不移轉｜https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Adobe-Stock-Contributor-Agreement-en_US-20240618.pdf｜2026-10-05｜curl 200（http://www.adobe.com/go/contributorterms 轉址到此 PDF），pdftotext
- 第 3.1 條：投稿者保證擁有作品全部權利，或具有授與授權所需的全部權利（正文寫「保證擁有必要的權利」）｜同上｜2026-10-05｜pdftotext
- 第 5.2 條：投稿者須完成收款所需的 IRS 表格；Foreign Person 要主張租稅協定的扣繳減免或免除時才提交 IRS Form W-8；需扣繳的稅從應付款扣除。〔查核第一輪改寫〕正文「收款前要完成必要的美國國稅局（IRS）表格；不是美國人的投稿者，要主張租稅協定的扣繳減免得交 W-8 表格，需要扣繳的稅會直接從款項扣除」，表格「收款前要完成 IRS 稅務表格」｜同上｜2026-10-05｜pdftotext，查核者重讀 5.2 條
- 上傳時須勾選「Created using generative AI tools」，所有生成式 AI 作品都要勾｜https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html｜2026-10-05｜搜尋摘要（三次查詢一致）
- 人物或財產是虛構的，勾選「People and Property are fictional」｜同上｜2026-10-05｜搜尋摘要（三次一致）
- 以可辨識真人為本（上傳真人照片當提示、在提示詞點名某人）需要 model release｜同上｜2026-10-05｜搜尋摘要（第一次查詢；第三次查詢摘要的「Model releases in Adobe Stock」頁為佐證）
- 提示詞、標題、關鍵字不得含：藝術家名、真人、虛構角色、仍受著作權保護的作品、政府機關名、第三方智慧財產、暗示真實新聞事件的描述｜同上｜2026-10-05｜搜尋摘要（第一、三次一致；第二次摘要列出藝術家、人名、政府機關、第三方 IP）
- 標題與關鍵字不必加「generative AI」，由勾選框分類｜同上｜2026-10-05｜搜尋摘要（第二次查詢）
- 須確認所用生成工具條款允許把產出拿去商業授權｜同上｜2026-10-05｜搜尋摘要（第一、三次一致）
- 同一提示詞或相近提示詞不要投多個版本｜同上｜2026-10-05｜搜尋摘要（第一、三次一致；第三次另有「相似素材最多三個」，單一摘要，正文未寫）
- 照片要像相機拍攝、主體存在於現實；奇幻概念歸插畫；人與動物不得有解剖錯誤｜同上｜2026-10-05｜搜尋摘要（正文初稿寫過，精簡時刪去）

## 圖庫：Shutterstock、iStock

- Shutterstock 不接受投稿者上傳 AI 生成內容；理由：須能證明 IP 所有權，AI 生成內容的所有權無法歸給單一個人；無法驗證模型來源，無法確保補償所有參與的創作者（頁面日期 July 16, 2025）｜https://submit.shutterstock.com/help/en/articles/10594622-content-policy-updates-ai-generated-content｜2026-10-05｜curl 200
- iStock 不允許生成式 AI 視覺作品進入圖庫；允許以手動或 AI 修圖工具對非 AI 原作做有限修飾（例：移除角落垃圾桶），不允許以 AI 加入新元素、主體或物件｜https://www.istockphoto.com/legal/ai-free-imagery-policy｜2026-10-05｜curl 200
- （未用）Getty Images 投稿者社群頁 contributors.gettyimages.com/article/10847 curl 只回 1,368 bytes 的空殼頁，不當來源；正文只寫 iStock。

## 模板與數位下載：Gumroad

- 直接銷售（個人頁或直接連結）每筆 10% + $0.50；Discover 市集每筆 30%｜https://gumroad.com/pricing｜2026-10-05｜curl 200
- 2025 年 1 月 1 日起 Gumroad 為 Merchant of Record，處理全球銷售稅代收代繳｜https://gumroad.com/pricing｜2026-10-05｜curl 200
- 不收月費（no monthly charges／no monthly payments）｜https://gumroad.com/pricing；https://gumroad.com/help/article/66-gumroads-fees｜2026-10-05｜curl 200／Inertia JSON
- 10% + $0.50 不含刷卡手續費（2.9% + $0.30）與 PayPal 手續費；Discover 30% 已含所有金流手續費｜https://gumroad.com/help/article/66-gumroads-fees｜2026-10-05｜Inertia JSON（另有：當月已付款銷售額達 $20,000 後直接銷售降為 5% + $0.50，正文初稿寫過後刪去）
- 台灣在銀行撥款國家表內，幣別 TWD（表內另註 min 800，正文未寫）｜https://gumroad.com/help/article/13-getting-paid｜2026-10-05｜Inertia JSON
- 撥款最低餘額 $100 USD；頁面另註「Countries showing "(min X)" have a higher minimum payout threshold than the standard $100 USD requirement」，台灣列為「TWD (min 800)」，兩者怎麼換算頁面沒寫清楚。〔查核第一輪改寫〕正文「撥款門檻標準是餘額 100 美元，台灣另有新台幣門檻，以撥款說明頁為準」，表格「新台幣撥款，門檻見撥款說明頁」｜同上｜2026-10-05｜Inertia JSON
- 假設示範：售價 10 美元、刷卡、不計稅 → 平台費 10×10%+0.50=1.50；刷卡費 10×2.9%+0.30=0.59；實拿 7.91。Discover：10×(1−30%)=7.00｜自行計算，費率來源同上｜2026-10-05｜計算
- 不得轉售非自己創作的產品：ebooks、courses、prompts、notion planners、templates、video clips、fonts、presets；PLR／MRR 轉售權電子書也不行｜https://gumroad.com/help/article/155-things-you-cant-sell-on-gumroad｜2026-10-05｜Inertia JSON
- 禁止「AI services — selling access to AI tools, chatbots, image or content generation services, or subscriptions to AI services fulfilled outside of Gumroad」｜同上；https://gumroad.com/prohibited｜2026-10-05｜Inertia JSON

## 模板與數位下載：Etsy

- 刊登費每個 $0.20，效期 4 個月；交易費為訂單總額 6.5%；金流手續費依國家而定；換匯時收 2.5%｜https://help.etsy.com/hc/en-us/articles/115014483627-What-are-the-Fees-and-Taxes-for-Selling-on-Etsy｜2026-10-05｜Zendesk API（updated_at 2026-10-05T02:35:50Z）
- （未用）Offsite Ads 15%／12%、上限 $100；開店費依地區而定
- 金流手續費依收款銀行帳戶所在地，例：United States 3% + 0.25 USD；表內沒有台灣｜https://help.etsy.com/hc/en-us/articles/115015628847-What-are-Payment-Processing-Fees-for-Selling-on-Etsy｜2026-10-05｜Zendesk API（佐證，未列入 sources）
- Etsy Payments 可用國家名單沒有台灣（有香港、日本、南韓、新加坡等）｜https://help.etsy.com/hc/en-us/articles/115015710408-Countries-Eligible-for-Etsy-Payments｜2026-10-05｜Zendesk API（updated_at 2026-10-05T03:46:46Z）
- 開店時要註冊 Etsy Payments；所在國家尚未支援者，目前無法在 Etsy 開新店｜https://help.etsy.com/hc/en-us/articles/115014503608-How-to-Get-Paid-on-Etsy｜2026-10-05｜Zendesk API
- 「Designed by a seller」包含 seller-prompted AI creations；這類作品必須揭露使用 AI；數位商品必須由賣家製作或設計｜https://help.etsy.com/hc/en-us/articles/360024112614-What-Can-I-Sell-on-Etsy｜2026-10-05｜Zendesk API
- （未用）數位商品每刊登最多 5 個檔案、每個 20MB｜https://help.etsy.com/hc/en-us/articles/115015628347-How-to-Manage-Your-Digital-Listings｜2026-10-05｜Zendesk API
- etsy.com/legal/fees 與 etsy.com/legal/creativity 直接讀與 WebFetch 都 403，未使用。

## GPT Store（OpenAI）

〔查核第一輪：本節的個人帳號、工作區、分潤、退場與延後日期四條今天讀不到官方頁，正文已改為「以官方公告為準」，sources 已換掉 help.openai.com；見文末〕

- 個人帳號（Free、Go、Plus、Pro）不能建立或發布新的 GPT；既有 GPT 仍可使用，符合原方案與權限時仍可編輯｜https://help.openai.com/en/articles/8798878-sharing-and-publishing-gpts；https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq｜2026-10-05｜搜尋摘要（三次查詢一致）
- Business、Enterprise、Edu 工作區的建立、編輯、上架依工作區設定與權限｜https://help.openai.com/en/articles/8798878-sharing-and-publishing-gpts｜2026-10-05｜搜尋摘要
- 依使用量的 GPT 收益只和一小群美國開發者測試（在 GPT Store 有熱門作品者），目前不接受新的開發者加入｜https://help.openai.com/en/articles/8798878-sharing-and-publishing-gpts｜2026-10-05｜搜尋摘要（兩次查詢一致）。注意：原「Monetizing Your GPT FAQ」https://help.openai.com/en/articles/9119255-monetizing-your-gpt-faq 現在 302 轉到 8798878，搜尋摘要可能來自舊索引（見 doubts）
- 自訂 GPT 預定 2026 年 12 月 11 日退場；有核准延後的 Enterprise 工作區為 2027 年 2 月 11 日｜https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq｜2026-10-05｜搜尋摘要（兩次查詢一致）
- 退場日後自訂 GPT 與其 GPT 頁面無法存取｜同上｜2026-10-05｜搜尋摘要
- 遷移到外掛（plugin）：指令→技能、連接的應用程式→外掛的 apps、知識檔案→參考檔；custom actions 不會轉移｜同上｜2026-10-05｜搜尋摘要（正文只留「自訂動作不會轉移」）
- 遷移不帶走分享設定與使用者；遷移後的個人外掛預設私人；公開需另走外掛送審流程｜同上｜2026-10-05｜搜尋摘要
- 外掛送審：上傳 ZIP、自動檢查、送審，核准後自行發布；要以本人或公司名義發布，需在組織設定完成 individual 或 business verification｜https://developers.openai.com/plugins/deploy/submission｜2026-10-05｜curl 200（.md 版）
- openai.com 各頁（introducing-the-gpt-store、usage-policies 等）curl 403，未使用。

## 標示與授權（台灣）

- 以 AI 為工具且有人類實際創意投入者，成果可受著作權保護；AI 獨立創作、無人類創意投入者，原則上不受保護（電子郵件1111031，發布 111-10-31，更新 114-04-28）｜https://www.tipo.gov.tw/tw/copyright/692-16813.html｜2026-10-05｜curl 200
- 生成式 AI 產製、依具體情況無受保護人類創作內容的圖片，是否須標示製作者及來源、如何標示，著作權法無規範，可自行決定（電子郵件1150828c 第五點，發布 115-08-28，更新 115-09-10）｜https://www.tipo.gov.tw/tw/copyright/692-94326.html｜2026-10-05｜curl 200
- 著作權法第 37 條第 1 項：授權約定不明之部分，推定為未授權｜https://www.tipo.gov.tw/tw/copyright/692-94326.html（頁內「相關法條」全文引用）｜2026-10-05｜curl 200
- 人工智慧基本法公布日期民國 115 年 01 月 14 日（正文寫「2026 年 1 月公布」）；第 4 條主詞為「政府推動人工智慧之研發與應用」，第 5 款：「人工智慧之產出應做適當資訊揭露或標記」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093｜2026-10-05｜curl 200
- 「純 AI 生成的圖，你很難用著作權阻止別人複製」「不要標獨家／版權所有」是依上列解釋推出的寫作建議，不是任何一頁的原文。

## 圖與 hero

- diagram-1.svg 上的數字：33（%）、10（%）、0.50、30（%）、2026、12、11，正文都有（intake 檢查 ok）。
- hero.svg：條紋遮雨棚市集攤位、三件商品（圖片、模板、對話框）、櫃台前緣三枚吊牌、一行字「賣 AI 數位商品」60px。無 logo、無人臉、無長條或曲線。


## 查核第一輪（2026-10-05，獨立查核者）

逐條紀錄見 verify-1.md。讀法與這一輪的改動：

- Adobe Stock 生成式 AI 規範頁（helpx.adobe.com）：curl、WebFetch、helpx 其他語系路徑（sg、ph_en、tw）、AEM `.plain.html`、stock.adobe.com 的 artist hub PDF 全部 403；web.archive.org 連線被重設，WebFetch 也不能讀 archive。只讀到 Adobe 社群論壇（community.adobe.com）2023-08-19 的〈Important generative AI reminders〉（作者 MatHayward，頁面看不出員工身分，所以不列入 sources），內容與今天兩次 WebSearch（限定 helpx.adobe.com）對規範頁的摘要一致：所有生成式 AI 作品勾「Created using generative AI tools」；有人物或財產且為虛構才勾「People and Property are fictional」；用真人或真實財產生成要附 model release 或 property release；不要用模仿其他藝術家風格、提到名人或品牌的提示詞。正文只留這四點，其餘（政府機關名、新聞事件、生成工具條款、相似提示詞）改成「完整的禁用清單與其他條件，以 Adobe Stock 的生成式 AI 投稿規範為準」。sources 仍保留官方規範頁網址（本環境 403，待第二輪或協調者用一般瀏覽器確認）。
- OpenAI：help.openai.com 與 openai.com 仍全部 403（含 9119255 舊網址，現在轉址前就 403）。改讀 OpenAI 自己的文件站 learn.chatgpt.com（developers.openai.com/codex/migrate-custom-gpts 301 到 https://learn.chatgpt.com/docs/migrate-custom-gpts，HTTP 200，另讀 `.md` 版與 llms-full.txt）。這一頁今天寫得到的：We're transitioning custom GPTs to plugins…before custom GPTs are retired；At retirement, custom GPTs stop running and leave the GPT directory；new GPT creation stops（"even after new GPT creation stops"、"while GPT creation is still available"）；Migration turns your GPT's instructions into a skill and brings over its knowledge files and connected apps. Rebuild custom actions separately；Your new plugin starts private；Access to the original GPT does not automatically give someone access to the plugin。頁面沒有任何日期，而且寫明 "timelines for other plans may differ"。
  - 改動：退場日 2026-12-11、Enterprise 延後 2027-02-11、「Free、Go、Plus、Pro 個人帳號不能建立或發布新的 GPT」、「分潤只限一小群美國開發者、不再接受新的開發者」都只來自搜尋摘要，今天讀不到官方頁，一律改為「以官方公告為準」（正文、摘要、description、表格、diagram-1.svg 第三欄與 desc）。
  - sources 拿掉兩個 help.openai.com 網址（讀不到），換成 learn.chatgpt.com/docs/migrate-custom-gpts。
- 外掛送審（developers.openai.com/plugins/deploy/submission，HTTP 200，讀 `.md` 版）：上傳 ZIP、自動檢查、送審、核准後自行發布；「Complete individual or business verification in organization settings to publish under your name or a company name」。正文「想上架到外掛目錄，得以個人或公司身分完成驗證並送審」。
- Etsy：help.etsy.com 網頁今天也是 403，改讀同站 Zendesk JSON API（/api/v2/help_center/en-us/articles/<id>.json，HTTP 200，四篇 updated_at 都是 2026-10-05）。費用、可用國家、開店條件、AI 揭露與撰稿紀錄一致；四篇全文都沒有 Taiwan 一字，「台灣暫時無法開新店」是兩頁合讀的推論，正文寫法維持「它的可用國家沒有台灣，台灣賣家暫時無法開新店」。
- 智慧局電子郵件1150828c 第五點講的是「是否須標示其製作者及來源」，正文改成「要不要標示製作者與來源、怎麼標」。
- 注意事項 callout 的「買家可能要求退款」沒有來源，改寫為「標榜獨家卻無法排除別人使用相同或相似的圖，容易和買家起爭議」。
- Gumroad 2025-01-01 起為 Merchant of Record：pricing 頁 FAQ 寫「We'll collect taxes in regions where we have tax obligations as a merchant of record」，正文改成「以登記賣方（Merchant of Record）身分代收代繳銷售稅」，不寫「各地」。
- iStock 表格改成「只允許對非 AI 原作做有限修圖」（原文 limited edits to their original, non-AI created work）。
- 正文長度 2,604（批次帶 1,800–3,000）。

## 查核第二輪（2026-10-05，獨立查核者）

逐條紀錄見 verify-2.md；今天讀回的全文在 `_tools/selling-ai-digital-products/fc2/`。

- ChatGPT Enterprise 的自訂 GPT 正在退場（「Custom GPTs in ChatGPT Enterprise are being retired.」）｜https://learn.chatgpt.com/docs/build-plugins｜2026-10-05｜curl 200
- 遷移指南的對象是 ChatGPT Enterprise 工作區（「This guide is for ChatGPT Enterprise workspace admins and people migrating GPTs they created」；「public sharing and timelines for other plans may differ」）。正文、摘要、description、表格與 diagram-1 第三欄改成只說企業版退場，其他方案「以官方公告為準」｜https://learn.chatgpt.com/docs/migrate-custom-gpts｜2026-10-05｜curl 200
- Gumroad 撥款頁今天寫「Some countries have higher local currency minimums—see the "(min X)" values」，台灣 TWD (min 800)；正文仍不寫數字｜https://gumroad.com/help/article/13-getting-paid｜2026-10-05｜Inertia JSON
- 假設例改成列出算式：10 × 10% + 0.50 = 1.50；10 × 2.9% + 0.30 = 0.59；10 − 1.50 − 0.59 = 7.91；10 × (1 − 30%) = 7｜費率來源同 Gumroad 各頁｜2026-10-05｜計算
- helpx.adobe.com、help.openai.com、openai.com 今天仍 403；web.archive.org CDX 連線被重設。Adobe 規範四點以 WebSearch（限定 helpx.adobe.com）兩次摘要交叉，維持。
- 正文長度 2,678。

## 跨篇核對（2026-10-05）

- 新增姊妹篇連結：ai-content-side-business-costs（上架檢查清單後）。人工智慧基本法公布日期民國 115 年 1 月 14 日，與「2026 年 1 月公布」相符｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093｜2026-10-05
