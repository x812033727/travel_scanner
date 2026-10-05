# selling-ai-digital-products — 查核第一輪（2026-10-05）

格式：主張｜判定（ok / fixed / softened / removed）｜來源網址。讀法見 notes.md 文末「查核第一輪」。

## 標題、description、摘要
- 標題「賣 AI 做的數位商品：圖庫投稿、模板與 GPTs 的平台規則」｜ok｜（範圍描述，無事實主張）
- description「GPT Store 分潤只限少數美國開發者，自訂 GPT 預定年底退場」｜softened（改為 OpenAI 正把自訂 GPT 轉成外掛並讓它退場）｜https://learn.chatgpt.com/docs/migrate-custom-gpts
- 摘要：Adobe Stock 收生成式 AI 投稿但要勾選 AI 標示｜ok（勾選規則見下方 Adobe 未決說明）｜https://contributor.stock.adobe.com/ ；https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html
- 摘要：Shutterstock 與 iStock 不收 AI 生成作品｜ok｜https://submit.shutterstock.com/help/en/articles/10594622-content-policy-updates-ai-generated-content ；https://www.istockphoto.com/legal/ai-free-imagery-policy
- 摘要：Gumroad 直接銷售 10% + 0.50 美元、Discover 30%｜ok｜https://gumroad.com/pricing
- 摘要：Etsy Payments 不支援台灣，暫時無法開新店｜ok（兩頁合讀的推論，頁面無 Taiwan 字樣）｜https://help.etsy.com/hc/en-us/articles/115015710408-Countries-Eligible-for-Etsy-Payments ；https://help.etsy.com/hc/en-us/articles/115014503608-How-to-Get-Paid-on-Etsy
- 摘要：GPT Store 分潤只和少數美國開發者測試｜softened（以官方公告為準）｜help.openai.com 403，無可讀官方頁
- 摘要：個人帳號已不能上架新的 GPT｜softened（改為新的 GPT 建立也會停止，各方案時程以官方公告為準）｜https://learn.chatgpt.com/docs/migrate-custom-gpts
- 摘要：自訂 GPT 預定 2026 年 12 月 11 日退場｜softened（退場日期以官方公告為準）｜help.openai.com 403；learn.chatgpt.com 頁面無日期
- 摘要：純 AI 生成、無人類創意投入的成果原則上不受著作權保護｜ok｜https://www.tipo.gov.tw/tw/copyright/692-16813.html

## 導言
- 「GPT Store 對台灣使用者已不是可行的收入管道」｜fixed（改為「自訂 GPT 則正在退場」，原句的地區判斷無官方來源）｜https://learn.chatgpt.com/docs/migrate-custom-gpts

## 圖庫
- Adobe Stock 上傳時勾選「Created using generative AI tools」｜ok（未能直接讀規範頁，見未決）｜https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html
- 有虛構人物或財產時勾「People and Property are fictional」｜ok（同上；措辭改成「有虛構的人物或建物等財產」）｜同上
- 以可辨識真人為本需附 model release｜fixed（補上真實財產需 property release）｜同上
- 提示詞、標題、關鍵字不得含藝術家、真人、虛構角色、受保護作品、政府機關、第三方智財、新聞事件｜softened（只留「不要模仿其他藝術家風格、不提名人或品牌」，完整清單以官方規範為準）｜同上
- 先確認生成工具條款允許商業授權｜softened（併入「其他條件以官方規範為準」；檢查清單保留為一般建議）｜同上
- 同一提示詞不要投多個版本｜removed｜同上（讀不到）
- 作者分成圖片 33%、影片 35%｜ok｜https://contributor.stock.adobe.com/royalties
- 每次下載實拿依買家方案而定｜ok｜https://contributor.stock.adobe.com/royalties
- 非專屬授權、作品仍屬於你｜ok｜https://contributor.stock.adobe.com/ ；https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Adobe-Stock-Contributor-Agreement-en_US-20240618.pdf
- 保證擁有必要權利（3.1 條）｜ok｜投稿協議 PDF（同上）
- 投稿內容會用在 Firefly 等 Adobe 產品｜ok｜https://contributor.stock.adobe.com/
- 非美國人要填 W-8、扣繳稅從款項扣除｜fixed（W-8 是主張租稅協定減免時提交；另補「收款前要完成必要 IRS 表格」）｜投稿協議 PDF 5.2 條
- 表格「要填 W-8 稅務表格」｜fixed（「收款前要完成 IRS 稅務表格」）｜投稿協議 PDF 5.2 條
- Shutterstock 不接受投稿者上傳 AI 生成作品，理由：智財無法歸給單一個人、無法確認該補償哪些創作者｜ok｜https://submit.shutterstock.com/help/en/articles/10594622-content-policy-updates-ai-generated-content
- iStock 不收生成式 AI 視覺作品，只允許對非 AI 作品做有限修圖，不能用 AI 加入新元素｜ok｜https://www.istockphoto.com/legal/ai-free-imagery-policy
- 表格 iStock「只允許 AI 有限修圖」｜fixed（「只允許對非 AI 原作做有限修圖」）｜同上

## 模板與數位下載
- Gumroad 不收月費｜ok｜https://gumroad.com/pricing ；https://gumroad.com/help/article/66-gumroads-fees
- 個人頁或直接連結購買抽 10% + 0.50 美元｜ok｜https://gumroad.com/pricing
- 刷卡手續費 2.9% + 0.30 美元另計｜ok｜https://gumroad.com/help/article/66-gumroads-fees
- Discover 市集抽 30%，已含金流手續費｜ok｜https://gumroad.com/help/article/66-gumroads-fees
- 2025 年 1 月 1 日起代收代繳「各地」銷售稅｜fixed（改為以登記賣方身分代收代繳銷售稅；FAQ 寫只在有稅務義務的地區）｜https://gumroad.com/pricing
- 台灣撥款以新台幣入帳｜ok｜https://gumroad.com/help/article/13-getting-paid
- 餘額至少 100 美元才撥款｜fixed（標準門檻 100 美元，台灣另列新台幣門檻，以撥款說明頁為準）｜https://gumroad.com/help/article/13-getting-paid
- 假設 10 美元：平台費 1.50、刷卡費 0.59、實拿 7.91；Discover 實拿 7｜ok（重算無誤）｜費率同上
- 不得轉售非自己創作的提示詞、模板、電子書與 PLR／MRR 轉售權商品｜ok｜https://gumroad.com/help/article/155-things-you-cant-sell-on-gumroad
- 禁止販售 AI 工具、聊天機器人使用權與圖片或內容生成服務｜ok｜同上
- Etsy 刊登費 0.20 美元、效期 4 個月｜ok｜https://help.etsy.com/hc/en-us/articles/115014483627-What-are-the-Fees-and-Taxes-for-Selling-on-Etsy
- Etsy 交易費 6.5%｜ok｜同上
- 金流手續費依國家而定｜ok｜同上
- 需要換匯時收 2.5%｜ok｜同上
- 賣家用提示詞做的 AI 作品歸在 Designed by a seller，必須揭露用了 AI｜ok｜https://help.etsy.com/hc/en-us/articles/360024112614-What-Can-I-Sell-on-Etsy
- 開新店要用 Etsy Payments，可用國家沒有台灣｜ok｜https://help.etsy.com/hc/en-us/articles/115014503608-How-to-Get-Paid-on-Etsy ；https://help.etsy.com/hc/en-us/articles/115015710408-Countries-Eligible-for-Etsy-Payments

## GPT Store
- 依使用量的收益計畫只和一小群美國開發者測試、不接受新加入｜softened（以官方公告為準）｜help.openai.com 403
- Free、Go、Plus、Pro 個人帳號不能建立或發布新的 GPT；既有的還能使用與編輯｜softened（改為「新的 GPT 建立功能也會停止，各方案時程以官方公告為準」）｜https://learn.chatgpt.com/docs/migrate-custom-gpts
- Business、Enterprise、Edu 工作區看設定與權限｜removed｜help.openai.com 403
- 自訂 GPT 2026 年 12 月 11 日退場、Enterprise 延後到 2027 年 2 月 11 日｜softened（日期以官方公告為準）｜help.openai.com 403；learn.chatgpt.com 無日期
- OpenAI 把自訂 GPT 轉成外掛並讓自訂 GPT 退場｜ok｜https://learn.chatgpt.com/docs/migrate-custom-gpts
- 退場後 GPT 與頁面無法開啟｜fixed（官方文字是 stop running and leave the GPT directory：不再運作、從 GPT 目錄下架）｜同上
- 自訂動作不會轉移｜ok（補：要另外重建；指令變技能、知識檔與連接的應用程式會帶過去）｜同上
- 轉好的個人外掛預設私人｜ok（改為「一開始是私人的，原本的使用者也不會自動取得權限」）｜同上
- 公開要另外完成身分驗證並送審｜ok（改為「上架到外掛目錄，得以個人或公司身分完成驗證並送審」）｜https://developers.openai.com/plugins/deploy/submission
- 小標「個人帳號不能上架，自訂 GPT 年底退場」｜softened（「自訂 GPT 正在轉成外掛」）｜https://learn.chatgpt.com/docs/migrate-custom-gpts
- 表格 GPT Store 三格（個人帳號不能新上架／分潤只限少數美國開發者／預定 2026 年 12 月 11 日退場）｜softened｜同上

## 標示與授權
- 以 AI 為輔助工具、有人類創意投入可受保護；AI 獨立完成原則上不受保護｜ok｜https://www.tipo.gov.tw/tw/copyright/692-16813.html
- 「純 AI 生成的圖，你很難用著作權阻止別人複製」｜ok（由上列解釋推出的說明）｜同上
- 無人類創作內容的 AI 圖片要不要標示、怎麼標，著作權法沒有規定｜fixed（函釋講的是「製作者及來源」的標示，正文補上）｜https://www.tipo.gov.tw/tw/copyright/692-94326.html
- 人工智慧基本法 2026 年 1 月公布｜ok（民國 115 年 01 月 14 日）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093
- 第 4 條把產出的揭露或標記列為原則，主詞是政府推動 AI｜ok｜同上
- 著作權法第 37 條：約定不明的部分推定為未授權｜ok｜https://www.tipo.gov.tw/tw/copyright/692-94326.html
- callout「買家日後在別處看到相同的圖，就可能要求退款」｜removed（無來源，改為「容易和買家起爭議」）｜—
- 表格 caption「查證於 2026 年 10 月」｜ok｜—

## 圖
- diagram-1：Adobe 33%、Gumroad 10% + 0.50 美元、Discover 30%｜ok｜同上各頁
- diagram-1：「提示詞不寫真人、品牌名」｜fixed（「提示詞不提名人、品牌」，與正文一致）｜Adobe 規範頁（見未決）
- diagram-1：GPT 欄「個人帳號不能新上架」「分潤只限少數美國開發者」「2026 年 12 月 11 日」｜softened（「自訂 GPT 將退場」「新的 GPT 建立也會停止」「分潤與退場日期 以官方公告為準」；desc 同步）｜https://learn.chatgpt.com/docs/migrate-custom-gpts
- diagram-1：Etsy「台灣暫時不能開新店」「金流服務不支援台灣」「要揭露用了 AI」｜ok｜Etsy 各頁
- hero.svg：無數字、無 logo、無人臉，一行字 60px｜ok｜—

## sources 與連結
- 改後 19 個 sources，其中 14 個今天 HTTP 200 有本文（Adobe 入口、royalties、協議 PDF、Shutterstock、iStock、Gumroad 4 頁、learn.chatgpt.com 遷移頁、developers.openai.com 送審頁、智慧局 2 頁、全國法規資料庫）｜ok
- Etsy 4 頁網頁 403，用同站 Zendesk JSON API 讀到全文（HTTP 200，updated_at 2026-10-05）｜ok（保留原說明頁網址）
- help.openai.com 2 頁 403，讀不到｜removed；改列 https://learn.chatgpt.com/docs/migrate-custom-gpts（HTTP 200）
- Adobe 生成式 AI 規範頁 403，讀不到｜保留（正文唯一的官方出處，列入未決）
- 站內連結 3 個：ai-image-tools-overview-2026、ai-image-copyright-taiwan、licensed-assets-workflow，都在允許清單內，連結文字與站上標題一致｜ok
