# selling-ai-digital-products — 查核第二輪（2026-10-05）

第二輪查核者：既不是撰稿者，也不是第一輪查核者。範圍：(A) 重查第一輪改過與未決的每一條，加上 verify-1.md 條列的隨機三分之一（第 2、5、8…71 條，每三條取一條）；(B) 法遵；(C) 讀者優先與文風。

讀法：`curl -sSL`，UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，看 HTTP 狀態、去掉 `<!-- -->` 註解與 script／style 再讀。腳本沿用 `_tools/selling-ai-digital-products/page.py`、`inertia.py`（Gumroad）、`zd.py`（Etsy Zendesk JSON API）；今天讀回的全文存在 `_tools/selling-ai-digital-products/fc2/*.txt`，改稿腳本是 `fc2/edit2.py` 與 `fc2/trim3.py`（都是寫成檔案再執行，沒有用 shell heredoc），改前的備份是 `fc2/pack.before2.json` 與 `fc2/diagram-1.before2.svg`。

## A. 重查結果

### 今天 HTTP 200、逐字對過的來源

| 主張（正文現況） | 判定 | 來源（今天讀到的原文） |
|---|---|---|
| Adobe Stock 接受 Gen AI 投稿；投稿內容用在 Firefly 等產品；非專屬授權、作品仍屬於你 | ok | contributor.stock.adobe.com：「We accept many types of content such as photos, illustrations, videos, vectors, Gen AI」「Your submissions will fuel Adobe Stock, Firefly, Express, and Creative Cloud」「non-exclusive partnership」 |
| 作者分成圖片（照片、向量、插圖）33%、影片 35%，每次下載實拿依買家方案而定 | ok | contributor.stock.adobe.com/royalties（Earnings Breakdown） |
| 收款前要完成必要 IRS 表格；非美國人主張租稅協定扣繳減免才交 W-8；扣繳稅從款項扣除（第一輪改寫） | ok | 投稿協議 PDF 第 5.2 條（adobe.com/go/contributorterms 今天仍轉址到 20240618 版，Effective as of June 18, 2024） |
| 保證擁有必要的權利 | ok | 投稿協議第 3.1 條 |
| Shutterstock 不收 AI 生成作品，理由是智財無法歸給單一個人、無法確認該補償哪些創作者 | ok | submit.shutterstock.com 10594622（July 16, 2025） |
| iStock 不收生成式 AI 視覺作品；只允許對非 AI 原作做有限修圖 | ok，正文措辭收緊（見改動 6） | istockphoto.com AI-Free Imagery Policy：「limited edits to their original, non-AI created work…Both manual and AI-powered post-production tools may be used…We don't permit new elements, subjects, or objects to be added…using AI」 |
| Gumroad 不收月費；直接銷售 10% + 0.50 美元；刷卡 2.9% + 0.30 美元另計；Discover 30% 含金流費 | ok | gumroad.com/pricing；help/article/66（另有當月已付款銷售額達 20,000 美元後降為 5% + 0.50 的優惠，正文未寫，不影響正確性） |
| 2025-01-01 起以 Merchant of Record 身分代收代繳銷售稅（第一輪拿掉「各地」） | ok | gumroad.com/pricing FAQ「We'll collect taxes in regions where we have tax obligations as a merchant of record」 |
| 台灣撥款以新台幣入帳；標準門檻 100 美元，台灣另有新台幣門檻（第一輪改寫） | ok | help/article/13：表列「Taiwan TWD (min 800)」；「You need a minimum balance of $100 USD…Some countries have higher local currency minimums」。今天這句已把 (min X) 解釋為「當地幣別的較高門檻」，第一輪說的矛盾沒有那麼嚴重，但正文仍不寫數字、指向撥款說明，維持 |
| 假設 10 美元：1.50／0.59／7.91；Discover 7 | ok，重算無誤；正文補上算式（見改動 5） | 費率同上 |
| 不得轉售非自己創作的提示詞、模板、電子書與 PLR／MRR；禁止 AI 工具、聊天機器人、生成服務 | ok | help/article/155 |
| Etsy 刊登 0.20 美元、效期 4 個月；交易費 6.5%；金流費依國家；換匯 2.5% | ok | Etsy 115014483627（Zendesk JSON API，HTTP 200；網頁本身 403） |
| 賣家提示詞生成的 AI 作品歸「Designed by a seller」，必須揭露 | ok | Etsy 360024112614 |
| 開新店要用 Etsy Payments，可用國家沒有台灣 → 台灣暫時無法開新店 | ok（仍是兩頁合讀的推論，見未決） | Etsy 115015710408（今天 updated_at 2026-10-05T06:32:36Z，全名單無 Taiwan）；115014503608「If it's not available in your country yet, you won't be able to open a new shop on Etsy at this time」 |
| 自訂 GPT 轉外掛；退場時停止運作並離開 GPT 目錄；新的 GPT 建立會停止；指令→技能、知識檔與連接的應用程式帶過去；自訂動作要重建；新外掛一開始是私人的、原使用者不自動取得權限 | 內容 ok，**範圍錯**（見改動 1） | learn.chatgpt.com/docs/migrate-custom-gpts：頁首寫明「Guidance for Enterprise admins…」「This guide is for ChatGPT Enterprise workspace admins and people migrating GPTs they created」，並寫「public GPTs in affected Enterprise workspaces are included, but public sharing and timelines for other plans may differ」 |
| （新增來源）企業版自訂 GPT 正在退場 | 新增 | learn.chatgpt.com/docs/build-plugins（HTTP 200）：「Custom GPTs in ChatGPT Enterprise are being retired.」 |
| 外掛目錄送審要完成個人或公司驗證 | ok | developers.openai.com/plugins/deploy/submission：「Complete individual or business verification in organization settings to publish under your name or a company name」 |
| 智慧局 1111031：有人類創意投入可受保護、AI 獨立完成原則上不受保護 | ok | tipo.gov.tw 692-16813（更新 114-04-28） |
| 智慧局 1150828c：生成式 AI 產製、無人類創作內容的圖片是否標示製作者及來源、如何標示，著作權法無規範（第一輪改寫） | ok | tipo.gov.tw 692-94326 第五點 |
| 著作權法第 37 條：約定不明部分推定為未授權 | ok | 同上頁「相關法條」 |
| 人工智慧基本法民國 115 年 01 月 14 日公布；第 4 條主詞是政府，第 5 款「人工智慧之產出應做適當資訊揭露或標記」 | ok | law.moj.gov.tw H0160093 |

隨機三分之一（verify-1.md 第 2、5、8、11、14、17、20、23、26、29、32、35、38、41、44、47、50、53、56、59、62、65、68、71 條）全部落在上表或下方未決項；其中第 20、23、26、29、32、35、38、41、50、59 條今天逐字對過無誤，第 2、8、11、47、53、65 條是 GPT 範圍問題，已依改動 1 修正。

### 今天仍讀不到官方原文的

- **Adobe Stock 生成式 AI 投稿規範**（helpx.adobe.com，含 generative-ai-faq、submit-generative-ai-content、ph_en／ae_en 路徑）：curl 與 WebFetch 今天都是 403；web.archive.org 的 CDX 今天 curl 直接 connection reset。改用 WebSearch 限定 helpx.adobe.com 兩次不同查詢，摘要一致寫到：所有生成式 AI 作品必勾「Created using generative AI tools」；畫面像人但不是真人時勾「People and Property are fictional」；描繪、依據或意圖呈現可辨識真人要 model release；「A property release is required if your generative AI content depicts recognizable real property」；不要在提示詞放其他藝術家、名人、知名角色或品牌，也不要模仿知名藝術家或品牌的風格。正文的四點都在這些摘要範圍內，維持；sources 保留官方網址。仍待協調者用一般瀏覽器開一次。
- **OpenAI 說明中心**（help.openai.com 20001519、8798878，openai.com/index/introducing-the-gpt-store）：今天全部 403。2026-12-11 退場日、2027-02-11 延後日、個人方案不能建立 GPT、分潤只限美國少數開發者，仍然只有搜尋摘要，維持「以官方公告為準」。

## 改動（事實）

1. **GPT 退場的適用範圍**：今天讀得到的兩頁一手文件（migrate-custom-gpts、build-plugins）都只講 **ChatGPT Enterprise**，而且寫明其他方案的公開分享與時程可能不同。原稿寫「OpenAI 已宣布把自訂 GPT 轉成外掛並讓它退場」是把企業版的規則擴大成所有方案。改為「ChatGPT 企業版（Enterprise）的自訂 GPT 正在退場、改轉成外掛……其他方案的時程可能不同，以官方公告為準」。同步改 description、摘要第 3 點、導言第一段、GPT 節第一段、表格 GPT Store 列（「企業版自訂 GPT 退場中，轉成外掛」「其他方案時程以官方公告為準」）、diagram-1 第三欄（徽章「企業版自訂 GPT 退場中」、「企業版新的 GPT 建立會停止」、「分潤與其他方案時程／以官方公告為準」）與 `<desc>`。sources 新增 https://learn.chatgpt.com/docs/build-plugins，遷移頁標題括號改成「企業版自訂 GPT 轉外掛、退場後停止運作」（共 20 筆，達上限）。
2. **「把收入押在 GPT Store 已經不實際」刪除**：這是對所有方案的判斷，但一手文件只支持企業版退場；改成「打算把 GPT 當商品經營，先確認自己方案的時程與分潤資格」。
3. **導言「自訂 GPT 則正在退場」**改為「自訂 GPT 則正在轉成外掛」（同 1 的範圍理由）。

## 法遵（B）

- 收入：全文沒有「月入」「被動收入」「躺著賺」「輕鬆賺」、沒有收入截圖或見證。唯一的金額例子以「假設」開頭，**原稿只給結果沒有算式**，已補上（改動 5）。
- 費率：Adobe、Gumroad、Etsy 的數字都對到平台自己的頁面；**原稿正文沒有寫這些費率是哪一天的**（只有表格 caption 有），導言第二段補「費率與規則以 2026 年 10 月各平台公布的版本為準」（改動 4）。
- 法律陳述：著作權（智慧局函釋、著作權法第 37 條）、人工智慧基本法（全國法規資料庫）、美國扣繳（Adobe 投稿協議 5.2 條）都有出處；沒有提到消保法、公平交易法、個資法或台灣稅法，也就沒有無出處的法律主張。
- 推薦：各平台只寫規則與費率；「Adobe Stock 收，Shutterstock 與 iStock 不收」與圖上的綠／橘／紅是投稿規則的事實分類，不是推薦。刪掉 Gumroad 段「能賣的是做好的成品，不是產圖服務的入口」這句重述（改動 7），順便少一句帶價值判斷的話。
- callout「容易和買家起爭議」是寫作建議，沒有法律主張；維持。

## 讀者優先與文風（C）

- 「本文」「這篇」0 次；沒有「查證時」「官網寫」「我們查不到」「本批」「撰稿」；沒有驚嘆號、沒有「總結來說」；台灣用語無誤（檔案、軟體、影片、使用者）。
- 外文第一次出現都有中文（Created using generative AI tools、People and Property are fictional、model／property release、IRS、W-8 表格、Merchant of Record、Designed by a seller、Etsy Payments 在摘要寫成「金流服務 Etsy Payments」、GPT Store、plugin、skill、custom actions）。
- 導言第一段現在是一句話給答案（放哪個平台：圖庫收不收、模板按成交抽成、自訂 GPT 轉外掛）。原第一段的第二句「上架、抽成與標示，平台規則都比法律管得細」與第四個 H2 重複，刪掉。
- 正文在句子裡仍有「以撥款說明頁為準」「以 Adobe Stock 的生成式 AI 投稿規範為準」：這是「以官方為準」的指引，不是敘述查證過程，維持。

## 改動（文字）

4. 導言第二段：「以下依序整理……」縮短為「以下依圖庫、模板與數位下載、GPT Store、標示與授權的順序整理，最後附上架前的檢查清單」，並補費率日期。
5. Gumroad 假設：補上算式「10 × 10% + 0.50 = 1.50」「10 × 2.9% + 0.30 = 0.59」「10 − 1.50 − 0.59 = 7.91」「10 × (1 − 30%) = 7」。
6. iStock：「只允許用 AI 對非 AI 作品做有限修圖，不能加入新的人物或物件」改為「只允許對非 AI 的原作做有限修圖（可用 AI 修圖工具），不能用 AI 加入新的元素、主體或物件」，貼近原文（手動與 AI 修圖都可以；禁止的是用 AI 加入新元素、主體、物件）。
7. 刪除 Gumroad 段末重述句；callout 刪「上架前再回平台說明頁確認」（與表格 caption、檢查清單重複）；刪導言第一段第二句（見上）。

## 機械檢查

- `pack_cli ingest --dry-run`：通過（dry run: nothing written）。
- `intake_check.py`：RESULT PASS；body_length 2,678（批次帶 1,800–3,000；比 2,600 的目標多 78 字，來源是補上的算式與 GPT 範圍說明，已用刪重述句抵掉一部分）；本文／這篇 0；sources 20；diagram-1 數字都在正文。
- 重新渲染 diagram-1.png 並打開看過：第三欄徽章加寬到 280 px，「企業版自訂 GPT 退場中」完整在徽章內，沒有壓線、溢出或重疊。hero.png 看過：攤位、三件商品、三枚吊牌、一行 60 px 字，無 logo、無人臉、無長條或曲線，alt 與畫面一致，未改。

## 未決（交協調者）

- helpx.adobe.com 的 Adobe Stock 生成式 AI 規範頁今天仍 403、Wayback 連不上；正文四點只靠官方網域的搜尋摘要，請用一般瀏覽器確認一次（特別是 property release 那一句）。
- help.openai.com 仍 403：個人方案（Free／Plus／Pro 等）是否也退場、日期與 GPT Store 分潤現況，正文一律「以官方公告為準」。若能讀到 20001519 FAQ 並確認所有方案同日退場，可把「企業版」範圍放寬並補日期（圖與表格也要一起改）。
- Etsy「台灣暫時無法開新店」仍是兩頁合讀：可用國家名單今天無 Taiwan，加上「If it's not available in your country yet, you won't be able to open a new shop」；沒有任何頁面直接點名台灣。
