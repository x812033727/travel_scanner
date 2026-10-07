# ai-freelance-getting-started — 查證紀錄

查證日一律 2026-10-05。格式：主張｜來源網址｜查證日｜怎麼讀到的。

讀法說明：
- Upwork、Fiverr 的 help center 網頁對本環境回 403；兩站都是 Zendesk，改讀官方的公開 JSON API
  `https://<host>/api/v2/help_center/en-us/articles/<id>.json`（HTTP 200，內容即同一篇說明頁本文，
  回應內含 `html_url` 與 `updated_at`）。sources 寫原始說明頁網址。
- 其他頁面用 `curl -sSL`（UA：Mokaair-editorial/1.0）直接讀，HTTP 200，去掉 `<!-- -->` 註解與 script 後讀本文。
- 腳本：/home/user/batch-ai-income/_tools/ai-freelance-getting-started/zd.py、page.py

## 平台：出任務（Tasker）

- 出任務品牌歷程：518 外包 → Tasker 出任務（2019）→ 出任務；由數字科技股份有限公司經營｜https://www.tasker.com.tw/about-us｜2026-10-05｜curl 200，「公司沿革與品牌歷程」段
- case.518.com.tw 直接轉址到 www.tasker.com.tw（518 外包網即出任務）｜https://case.518.com.tw/｜2026-10-05｜curl -L，effective URL = https://www.tasker.com.tw/
- 發案端刊登一般案件免費；接案端基本提案免費，搶先提案需購買 T Points 開通 TaskerGo；成交目前不抽成、無第三方金流服務費｜https://www.tasker.com.tw/features/taskergo｜2026-10-05｜curl 200，「出任務收費總覽」，頁尾「本頁最後更新：2026/07/31」
- 2025/7 關閉第三方金流：停止代收付與第三方金流服務費，回歸雙方自行協議付款｜同上｜2026-10-05｜「出任務收費制度演進」第 3 點
- T Points 與新台幣 1:1、無使用期限｜同上｜2026-10-05｜FAQ
- TaskerGo BASIC 30 Days Pass 提案額度 600；方案頁「TaskerGo 搶先提案 30 天效期・$600 起」｜同上；https://www.tasker.com.tw/pricing｜2026-10-05｜curl 200
- 提案額度最晚 2 天內 100% 返還（案主回覆或到期自動婉拒）｜https://www.tasker.com.tw/features/taskergo｜2026-10-05｜（正文未用）
- FAQ「接案者一定要購買 T Points 嗎？需要購買 T Points，T Points 將用於兌換 TaskerGo 爭取搶先提案的優勢以及回覆案主的訊息」——與同頁「基本提案免費」並存；正文寫「基本提案免費，搶先提案要用 T Points」｜同上｜2026-10-05｜FAQ（見 doubts）
- 專家訂閱方案：免費 $0/月；月方案 $1,080/月；季方案 $880/月；年方案 $680/月（自動續訂）｜https://www.tasker.com.tw/pricing｜2026-10-05｜curl 200 方案表（正文未用，初稿寫過後刪掉）
- 合約產生器：5 種外包合約範本，免費下載 PDF／Word｜https://www.tasker.com.tw/toolbox/contract｜2026-10-05｜curl 200

## 平台：PRO360 達人網

- 註冊成為專家後瀏覽需求免費，只有報價時扣儲值金，金額依類別區分，報價時會提示扣多少（正文：報價時會先提示）｜https://www.pro360.com.tw/pro/faq/｜2026-10-05｜curl 200 FAQ
- 成交不抽成：「將不會有任何抽成，不論是事後還是事前，我們只有在您報價時會收取報價費用」｜同上｜2026-10-05｜FAQ
- 成功取得案件後客戶直接付費給專家，PRO360 不再收取其他費用；推廣服務是只有客戶主動聯繫才收費｜https://www.pro360.com.tw/pro/guide/how-pro360-work/｜2026-10-05｜curl 200

## 平台：Upwork

- Freelancer Service Fee 每份合約 0% 到 15%；提案或收到邀約時就會顯示；合約開始後固定不變｜https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee｜2026-10-05｜Zendesk API 200，updated_at 2026-10-04
- 例：想每小時實拿 20 美元、費率 10%，要向客戶開 22.22 美元｜同上｜2026-10-05｜「Can you show me examples」段
- Connects 每個 0.15 美元、以組合販售；每個案件需要的 Connects 數不同｜https://support.upwork.com/hc/en-us/articles/211062898-Understanding-and-using-Connects｜2026-10-05｜Zendesk API 200
- 固定價：客戶須先存入每個里程碑款項；提交後客戶最長 14 天審核（不回應自動放款）；核准後 5 天安全期（five-day security hold）才可提領｜https://support.upwork.com/hc/en-us/articles/211063718-How-payments-for-milestones-and-fixed-price-contracts-work｜2026-10-05｜Zendesk API 200
- 時薪制：計費週期週一 00:00 至週日 23:59（UTC），週期結束後 10 天款項可提領｜https://support.upwork.com/hc/en-us/articles/211063698-How-to-manage-the-weekly-billing-cycle｜2026-10-05｜Zendesk API 200
- 提領方式與手續費依地區不同，在 Settings > Withdrawals 查看（正文未用，不在 sources）｜https://support.upwork.com/hc/en-us/articles/211063978-What-are-the-PayPal-fees-and-timing-for-withdrawals｜2026-10-05｜Zendesk API 200

## 平台：Fiverr

- 訂單完成後接案者拿到客戶已結清款項的 80%；14 天結清期後才可提領（Top Rated、Fiverr Pro 等計畫較短；正文寫「部分資格可縮短」）｜https://help.fiverr.com/hc/en-us/articles/34069565843985-How-Fiverr-works-for-freelancers｜2026-10-05｜Zendesk API 200，updated_at 2026-10-05
- 交付後客戶有三天回應，未回應即視為完成（有實體寄送的 14 天）｜同上｜2026-10-05｜FAQ 段
- 提領：PayPal 手續費 0 美元（最低 1 美元）；Bank Transfer（經 Payoneer）1 美元（最低 20 美元）；Payoneer 帳戶 3 美元｜https://help.fiverr.com/hc/en-us/articles/360010530058-Withdrawing-your-earnings-managing-payout-methods｜2026-10-05｜Zendesk API 200 表格（正文未用，不在 sources）
- AI 規定：各類別都允許使用 AI；接案者對交付成果完全負責；未經修改的通用 AI 產出不符品質標準；客戶在下單前或開始時明確要求不用 AI，接案者必須遵守｜https://help.fiverr.com/hc/en-us/articles/34998793899665-Using-AI-on-Fiverr-Guidelines-for-freelancers-and-clients｜2026-10-05｜Zendesk API 200
- 爭議時看：客戶是否事先說明 AI 期望、交付是否沒有明顯錯誤或 AI 幻覺、是否客製；認定違反信任時訂單可能取消、客戶全額退款、帳號可能永久停權｜同上｜2026-10-05｜「What happens if there's a dispute?」段

## 法規與主管機關

- 著作須由自然人創作；AI 只當輔助工具且有人類實際創意投入，成果可受保護；完全由 AI 演算獨立完成、無人類精神投入者無法享有著作權（電子郵件1140522c，令函日期 114-05-22）｜https://www.tipo.gov.tw/tw/copyright/692-34252.html｜2026-10-05｜curl 200
- 著作權法第 12 條：出資聘人完成之著作，未約定著作財產權歸屬者歸受聘人享有，出資人得利用該著作｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0070017&flno=12｜2026-10-05｜curl 200
- 各類所得扣繳率標準（修正日期 110-06-30）第 2 條：執行業務者之報酬按給付額扣取 10%；第 13 條：每次應扣繳稅額不超過 2,000 元者免予扣繳｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340028｜2026-10-05｜curl 200。正文只寫「可能依所得類別先扣繳稅款」，不寫數字（接案收入歸哪一類所得因案而異）

## 假設數字（正文明示為假設，不是行情）

- 目標時薪新台幣 800 元、AI 起草 1 小時、查證與改寫 2 小時、溝通與修改 1 小時、AI 訂閱分攤 200 元、平台抽成 20%：3,200＋200＝3,400；3,400÷0.8＝4,250。全部是示範算法用的假設。

## 正文用語對照（給查核）

- 「出任務（Tasker，前身是 518 外包）」：依 about-us 品牌歷程與 case.518.com.tw 轉址。指派把 518 外包網與 Tasker 出任務列成兩個平台名，官方頁顯示是同一個平台改名，正文只寫一次。
- 「30 天方案 600 點起」：TaskerGo 頁 BASIC 30 Days Pass 提案額度 600；pricing 頁「30 天效期・$600 起」。T Points 與新台幣 1:1，所以寫「點」。
- 「每週一到週日為一個計費週期」：Upwork 以 UTC 計，正文未寫時區。
- 「經濟部智慧財產局的解釋」：電子郵件1140522c 的問題是 ChatGPT 生成的圖畫；正文寫「生成圖」，未延伸到文字。
- 站內連結用 rich_paragraph 的 article inline（slug：ai-tools-choose-by-task、website-income-models、ai-hallucination-fact-check），不用 link 區塊，避免 raw_internal_url 警告；三個 slug 都在 content 目錄存在。

## 圖

- diagram-1：四個問題的決策流程，圖上唯一的阿拉伯數字是頁尾 2026（表格 caption「查證於 2026 年 10 月」有）。
- hero：對話框、筆電與文件、放大鏡加勾號、價格吊牌，單行文字「AI 接案入門」64px。沒有長條、曲線、金幣、logo、人臉。
- 兩張都用 render_svg 渲染成 PNG 打開看過；修過的地方：決策框文字垂直置中、向下箭頭換成同色箭頭、hero 對話框尾巴改成單一路徑、吊牌繩改成穿過孔的環。

## 查核第一輪（2026-10-05，獨立重查）

逐條紀錄在 verify-1.md。讀法：Tasker、PRO360、TIPO、全國法規資料庫用 curl -sSL 直接讀（HTTP 200）；
Upwork、Fiverr 說明頁直接讀回 403（Cloudflare），Wayback CDX 連線被重置，改讀同站 Zendesk 公開 API
（HTTP 200，回應的 html_url 等於 sources 網址；updated_at：Upwork 211062538 2026-10-04、211062898 2026-10-05、
211063718 2026-10-04、211063698 2026-10-04；Fiverr 34069565843985 2026-10-05、34998793899665 2026-10-04）。

改動：
- 出任務免費帳號「解鎖聊聊 1次/月」，訂閱方案（月 1,080 元、季 880 元/月、年 680 元/月）無限次｜https://www.tasker.com.tw/pricing｜2026-10-05｜方案比較表。初稿只寫「基本提案免費」，讀者會以為免費就能和案主談；正文與表格補上，月費數字不寫。
- TaskerGo 頁 FAQ 說 T Points 也用於「回覆案主的訊息」，與收費總覽「基本提案免費」並存；正文寫「回覆案主訊息是否另外扣點，以官方公告為準」。
- 出任務「刊登一般案件完全免費」是發案端；正文改成「案主刊登一般案件免費，接案者基本提案免費」。
- Upwork 服務費：「Once a proposal, offer, or contract is sent, the Freelancer Service Fee is locked in」，正文與表格由「合約開始後固定」改成「送出提案或邀約後就鎖定」。
- Upwork 時薪計費週期以 UTC 計（Monday 00:00 UTC 至 Sunday 23:59 UTC），正文補「以世界協調時間 UTC 計」。
- Upwork Connects 每個案件需要的數量不同（"The number of Connects you'll need varies per job"），正文補上。
- Fiverr AI 爭議：帳號 "may be permanently suspended"，正文改「可能被永久停權」。
- 讀者優先：「Upwork 說明頁舉的例子是」改「以 Upwork 為例」；站內連結 inline 文字改成該文實際標題。
- 摘要：出任務收費不只提案，改「搶先提案、訂閱或報價等費用」。
- 正文 2,714 字（intake band 1,800–3,000），比 §10.6 的 2,600 目標多一些，因為補了聊聊限制。

## 跨篇核對（2026-10-05）

- hero 與 ai-concept-stocks-explained 太像（都是文件＋放大鏡＋橘色吊牌）：放大鏡改成螢幕內的綠色勾號圓章，價格吊牌改成計算機；`<desc>` 與 hero alt 同步更新。
- 新增姊妹篇連結：ai-translation-subtitle-freelance（第一節末）、ai-freelance-client-confidentiality（報價合約清單後）。
