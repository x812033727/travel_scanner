# ai-freelance-getting-started — 查核第一輪（2026-10-05）

格式：主張｜判定（ok / fixed / softened / removed）｜來源網址。Upwork、Fiverr 說明頁直接讀回 403，改讀同站 Zendesk 公開 API（/api/v2/help_center/en-us/articles/<id>.json，HTTP 200，html_url 與 sources 網址相同）；其餘頁面 curl -sSL 讀到 HTTP 200。

## 平台：出任務（Tasker）
- 出任務前身是 518 外包（518 外包 → Tasker 出任務（2019）→ 出任務）｜ok｜https://www.tasker.com.tw/about-us
- case.518.com.tw 轉址到 tasker.com.tw（同一平台）｜ok｜https://case.518.com.tw/
- 案主刊登（一般）案件免費｜fixed（原寫「刊登案件與基本提案免費」，主詞不清；改為「案主刊登一般案件免費，接案者基本提案免費」）｜https://www.tasker.com.tw/features/taskergo
- 接案者基本提案免費｜ok（收費總覽）｜https://www.tasker.com.tw/features/taskergo
- 成交不抽成、無第三方金流服務費｜ok｜https://www.tasker.com.tw/features/taskergo
- 搶先提案要買 T Points 開通 TaskerGo｜ok｜https://www.tasker.com.tw/features/taskergo
- T Points 與新台幣 1:1｜ok｜https://www.tasker.com.tw/features/taskergo
- TaskerGo 30 天效期方案 600 點起（BASIC 30 Days Pass 提案額度 600；方案頁「30 天效期・$600 起」）｜ok（措辭改「30 天效期的方案」）｜https://www.tasker.com.tw/features/taskergo ；https://www.tasker.com.tw/pricing
- 免費帳號每月只能解鎖 1 次聊聊，不限次數要付費訂閱｜fixed（初稿漏寫，正文與表格補上）｜https://www.tasker.com.tw/pricing
- 回覆案主訊息是否扣點（FAQ 說 T Points 用於回覆案主訊息，與「基本提案免費」並存）｜softened（以官方公告為準）｜https://www.tasker.com.tw/features/taskergo
- 2025 年 7 月起停止代收付，雙方自行協議付款｜ok｜https://www.tasker.com.tw/features/taskergo
- 網站有免費的合約書範本產生器｜ok（「免費產生合約書」，五種範本，PDF／Word）｜https://www.tasker.com.tw/toolbox/contract

## 平台：PRO360 達人網
- 瀏覽案件免費｜ok｜https://www.pro360.com.tw/pro/faq/
- 每次（手動）報價扣儲值金，金額依服務類別而定，報價時會提示｜ok｜https://www.pro360.com.tw/pro/faq/ ；https://www.pro360.com.tw/pro/guide/how-pro360-work/
- 成交不抽成｜ok｜https://www.pro360.com.tw/pro/faq/
- 客戶直接付款給專家，平台不再收其他費用｜ok｜https://www.pro360.com.tw/pro/guide/how-pro360-work/

## 平台：Upwork
- 服務費每份合約 0% 到 15%｜ok｜https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee
- 提案或收到邀約時就看得到費率｜ok｜同上
- 費率「合約開始後固定」｜fixed（來源：送出提案、邀約或合約後即鎖定；改「送出提案或邀約後就鎖定」，正文與表格）｜同上
- 想每小時實拿 20 美元、費率 10%，開 22.22 美元｜ok｜同上
- Connects 每個 0.15 美元｜ok｜https://support.upwork.com/hc/en-us/articles/211062898-Understanding-and-using-Connects
- 每個案件需要的 Connects 數不同｜fixed（補上，避免讀者以為一次提案一個）｜同上
- 固定價：客戶先存入里程碑款項｜ok｜https://support.upwork.com/hc/en-us/articles/211063718-How-payments-for-milestones-and-fixed-price-contracts-work
- 提交後客戶最長 14 天審核｜ok｜同上
- 核准後 5 天安全期才可提領｜ok｜同上
- 時薪制計費週期週一到週日｜fixed（補「以世界協調時間 UTC 計」）｜https://support.upwork.com/hc/en-us/articles/211063698-How-to-manage-the-weekly-billing-cycle
- 週期結束後 10 天可提領｜ok｜同上

## 平台：Fiverr
- 接案者拿到客戶已結清款項的 80%｜ok｜https://help.fiverr.com/hc/en-us/articles/34069565843985-How-Fiverr-works-for-freelancers
- 訂單完成後 14 天結清期，部分資格可縮短｜ok（Top Rated、Fiverr Pro 等）｜同上
- 交付後客戶 3 天未回應視為完成｜ok（有實體寄送的 14 天，正文未寫）｜同上
- 客戶在下單前或開始時要求不用 AI，接案者必須遵守｜ok｜https://help.fiverr.com/hc/en-us/articles/34998793899665-Using-AI-on-Fiverr-Guidelines-for-freelancers-and-clients
- AI 爭議看明顯錯誤或 AI 幻覺、是否客製｜ok｜同上
- 違反信任時訂單可能取消、客戶全額退款、帳號可能停權｜fixed（來源寫 permanently suspended，改「永久停權」）｜同上

## 法規
- 完全由 AI 演算完成、無人類創意投入的生成圖無法享有著作權（電子郵件1140522c，114-05-22）｜ok｜https://www.tipo.gov.tw/tw/copyright/692-34252.html
- 圖解「AI 只做發想，成品要有你的實際創作」（有人類實際創意投入仍可受保護）｜ok｜同上
- 著作權法第 12 條：未約定歸屬時著作財產權歸受聘人，出資人得利用｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0070017&flno=12
- 國內案主給付報酬時可能依所得類別先扣繳稅款｜ok（各類所得扣繳率標準第 2 條執行業務報酬 10%、第 13 條 2,000 元以下免扣繳；正文不寫數字）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340028

## 假設數字與計算
- 報價＝想實拿÷（1－抽成比例）｜ok（與 Upwork 範例 20÷0.9＝22.22 一致）｜https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee
- 800×4＝3,200；＋200＝3,400；3,400÷0.8＝4,250（明示為假設）｜ok（算術核對）｜—

## 摘要、描述、標題、表格、圖
- 摘要「出任務與 PRO360 成交不抽成，改收提案或報價的費用」｜fixed（出任務另有訂閱方案，改「搶先提案、訂閱或報價等費用」）｜https://www.tasker.com.tw/pricing
- 摘要「Upwork 0% 到 15%、Fiverr 80%」｜ok｜同上述 Upwork、Fiverr 來源
- description、title｜ok（內容與正文一致，無數字）｜—
- 表格四列逐格｜出任務、Upwork 兩格 fixed，其餘 ok｜同上述來源
- 表格 caption「查證於 2026 年 10 月」｜ok｜—
- diagram-1.svg：唯一數字 2026（頁尾），流程內容與正文一致｜ok｜—
- hero.svg：單行「AI 接案入門」，無 logo、人臉、長條、曲線、金幣｜ok｜—

## 連結與讀者優先
- 站內連結：只有 article inline 指向 ai-tools-choose-by-task、website-income-models、ai-hallucination-fact-check（皆在允許清單、目錄中存在），沒有 link 區塊｜ok｜—
- ai-hallucination-fact-check 的 inline 文字與該文標題不一致｜fixed（改為實際標題）｜—
- 「Upwork 說明頁舉的例子是」在句中敘述來源｜fixed（改「以 Upwork 為例」）｜—
- sources 15 筆：9 筆直接 HTTP 200；6 筆 Upwork／Fiverr 直接讀 403，以 Zendesk API 200 確認同一篇內容與網址｜ok｜—
