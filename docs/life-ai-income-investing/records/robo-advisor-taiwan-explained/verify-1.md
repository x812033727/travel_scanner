# robo-advisor-taiwan-explained 查核第一輪（2026-10-05）

格式：主張｜結果（ok / fixed / softened / removed）｜來源網址。所有網址 2026-10-05 以 curl -sSL 取得，HTTP 200。

L77 = https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077 （證券投資顧問事業管理規則，修正日期 113.10.25）
L121 = https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121 （證券投資信託及顧問法）
NORM = https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11301200 （公會作業規範，113.11.21）
TPL = https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11301203 （公會委任契約範本，113.11.21）
PANEL = https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11301204 （審查小組作業要點）
TRI = https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11300227 （三方合約範本，113.03.13）
OLD = https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW10875160 （舊作業要點，113.11.21 廢止）
FSC1118 = https://www.sfb.gov.tw/ch/home.jsp?id=88&parentpath=0%2C3&mcustomize=lawnews_view.jsp&dataserno=202411180001
FSC1025 = https://www.sfb.gov.tw/ch/home.jsp?id=88&parentpath=0%2C3&mcustomize=lawnews_view.jsp&dataserno=202410250003
LY = https://ppg.ly.gov.tw/ppg/SittingAttachment/download/2023022320/94902142681905139004.pdf
MW = https://moneywise.fsc.gov.tw/tabf/FW/FW8_page_A.html （表格圖 FW_img/FW08-A01.png）
IF38 = https://ifund.sfi.org.tw/data.php?id=38 ；IF26 = https://ifund.sfi.org.tw/data.php?id=26
ROBO = https://www.sitca.org.tw/ROC/RoboAdvisor/index.html ；MEM = https://www.sitca.org.tw/ROC/MemData/MD2001N.aspx?PGMID=AS0701

## 標題、描述、導言

- 機器人理財的正式名稱是自動化投資顧問服務，屬證券投資顧問業務｜ok｜L77 第 25-1 條；L121 第 4 條
- 只有投顧與兼營投顧業務的證券經紀商、期貨經紀商、信託業、投信能提供｜ok｜L77 第 25-1 條第 1 項
- 用線上問卷、演算法產生組合建議、依約定調整比例｜ok｜L77 第 25-1 條第 2 項；NORM 第 4、6 條
- 組合裡買的是基金、ETF 這類商品｜ok｜NORM 第 8 條第 1 項第 2 款（二）；TPL 前言
- 依 2024 年修正的管理規則與公會作業規範｜ok｜L77（修正日期 113.10.25）；NORM

## 台灣怎麼管

- 台灣自 2017 年（106 年）開放這項服務｜ok｜LY 壹
- 起初由公會作業要點規範（106.06.30 發布）｜ok｜LY 貳、二、（一）
- 2024-10-25 金管會在管理規則增訂專章｜ok｜FSC1025（金管證投字第1130385193號）；L77 第五章之一
- 同年 11 月舊要點廢止｜ok｜OLD 沿革（113.11.21 中信顧字第1130055095號函，自即日廢止）
- 公會改訂作業規範與委任契約範本｜ok｜NORM、TPL 沿革（113.11.21 訂定）
- 定義：經由網路互動，以全無或極少人工服務，提供透過演算法由系統自動產生的投資組合建議｜ok｜L77 第 25-1 條第 2 項；NORM 第 2 條
- 實收資本額新臺幣 5,000 萬元以上｜ok｜L77 第 25-2 條第 4 款
- 提存營業保證金新臺幣 500 萬元｜ok｜L77 第 25-2 條第 4 款
- 設置專責單位與內部稽核人員｜ok｜L77 第 25-4 條第 1、2 項
- 提供服務或變更演算法要送公會審查，公會設審查小組｜ok｜L77 第 25-3 條；NORM 第 3 條
- 審查演算法方法論、歷史資料回測能否達成預期成效、對外揭露是否充分｜ok｜PANEL 第 2 條第 2 款（一）
- 人工服務只能協助完成問卷或解釋建議，不得調整或擴張系統建議｜ok｜NORM 第 2 條第 2 項；ROBO
- summary：客服只能協助填答或解釋，不能改動系統建議｜ok｜NORM 第 2 條第 2 項

## KYC 與投資組合

- 問卷評估投資目的與期間、知識、經驗、財務狀況、承受風險程度｜ok｜NORM 第 4 條第 2 款；L77 第 10 條第 1 項
- 題目具體明確、矛盾回答要有處理機制｜ok｜NORM 第 4 條第 3 款
- 依風險承受程度配對相對應的組合建議｜ok｜NORM 第 4 條第 4 款
- 定期請你更新；不符風險屬性時繼續或調整都要經同意；沒更新照原建議繼續｜ok｜NORM 第 4 條第 5 款
- 組合參數、篩選、挑選由系統公平客觀執行；辨識利益衝突並訂防範程序｜ok｜NORM 第 5 條；L77 第 25-4 條第 3 項第 9 款
- 系統看不到其他金融機構資產、稅務概況、購屋計畫、目標改變｜ok｜NORM 第 8 條第 1 項第 4 款；TPL 第四點

## 再平衡

- 執行方式只有兩種：每次先經同意，或事先約定達門檻且符合條件時由電腦系統自動執行｜ok｜FSC1118 一、（一）；NORM 第 6 條第 2 項第 1 款
- 執行時機：定期（月、季、半年、年度）或不定期（客戶指定或達預設條件）｜ok｜NORM 第 6 條第 3 項第 1 款
- 執行門檻：個別標的或整體組合損益達預設標準，或偏離最近一次設定比例達預設標準｜ok｜FSC1118 一、（二）
- 約定條件：維持原標的與比例；或金管會核准或申報生效的基金、名單不超過 30 檔、比例變動絕對值合計不超過 60%｜ok｜FSC1118 一、（三）；NORM 第 6 條第 3 項第 2 款
- summary 第三點「自動執行時，基金名單不超過 30 檔、比例變動合計不超過 60%」｜fixed（條件是二擇一，改成「只限維持原標的與比例，或在不超過 30 檔的基金名單內、比例變動合計不超過 60%」）｜FSC1118 一、（三）
- 超出約定條件要先經同意；更換基金名單要重新約定｜ok｜NORM 第 6 條第 3 項第 2 款第 2 目 3、第 3 款（二）
- 再平衡後即時通知交易結果｜ok｜L77 第 25-5 條第 2 項；NORM 第 6 條第 2 項第 6 款
- 「要提供終止自動再平衡的管道」｜fixed（機制涵蓋兩種服務方式，改成「要建置讓你終止再平衡服務的機制」）｜NORM 第 6 條第 2 項第 7 款
- 告知再平衡可能產生的各項成本｜ok｜NORM 第 6 條第 2 項第 3 款
- 管理規則禁止投顧保管或挪用客戶款項｜ok｜L77 第 13 條第 2 項第 7 款
- 自動再平衡在契約約定範圍內不受「不得代理他人從事有價證券投資」限制｜ok｜L77 第 25-5 條第 3 項、第 13 條第 2 項第 2 款
- 三方合約範本：資金在與證券商約定的交割銀行帳戶或資金管理帳戶，投顧依約傳送交易指示｜ok｜TRI 第二條、第三條
- diagram-1 第四步「經證券商執行交易」、底列「資金留在你與證券商約定的帳戶」、caption「資金始終留在你自己的帳戶」、image alt「經證券商下單」｜fixed（把三方合約這一種模式畫成唯一模式；改成「由證券商等機構執行」「投顧不保管你的錢，只依約傳送交易指示；經證券商下單時，資金留在你與證券商約定的帳戶」，desc、alt、caption 同步）｜L77 第 13 條第 2 項第 7 款、第 25-1 條；TRI
- diagram-1 上的數字 30、60%、2026｜ok（正文都有）｜FSC1118；表格 caption

## 費用

- 契約要寫明報酬、費用的數額、給付方式與計算方法｜ok｜L77 第 10 條第 3 項第 5 款
- 委任契約範本可選的收費項目：顧問費、手續費、再平衡服務費、調整服務費、其他｜ok｜TPL 第七點
- 假設試算 10 萬元 ×（0.5% + 0.4%）＝ 900 元，標明為假設｜ok（算術；不是任何業者費率）｜—
- 表：經理費、保管費從基金資產內扣、反映在淨值｜ok｜IF38（證基會投資人教育網）
- 表：經理費以資產百分比計算｜ok｜MW 表格圖（以總資產百分比計算）
- 表：經理費、保管費看公開說明書｜ok｜IF26
- 表：「申購依金額訂費率，其餘依基金或銷售機構規定」｜softened（後半句官方表上沒有；改成「申購手續費依申購金額訂適用費率；買回與轉換費用依各基金規定」）｜MW
- 表：信託管理費是透過銀行以信託方式投資基金時由銀行收取｜ok｜MW
- 表：交易稅、手續費加計在扣款金額內｜ok｜TRI 第三條二、（二）2、3
- 表 caption：查證於 2026 年 10 月｜ok｜—
- 收到書面契約之日起 7 日內可書面終止，業者只能請求相當報酬，不得請求損害賠償或違約金｜ok｜L77 第 10 條第 3 項第 11 款、第 4 項
- 範本：非經你同意，終止時不得扣除契約未列明的費用｜ok｜TPL 第十點（三）1
- 資產變現所需時間屬使用前告知事項｜ok｜NORM 第 8 條第 1 項第 1 款

## 做得到與做不到

- 初次使用前必須告知限制｜ok｜NORM 第 8 條
- 產品範圍可能只有基金或 ETF、不含個股，ETF 未必涵蓋全部｜ok｜NORM 第 8 條第 1 項第 2 款（二）；ROBO
- 系統對利率等基本假設可能與現實不符｜ok｜NORM 第 8 條第 1 項第 2 款（一）
- 廣告不得為保證獲利或負擔損失之表示｜ok｜L77 第 14 條第 1 項第 6 款
- 不得與客戶約定收益共享或損失分擔｜ok｜L77 第 13 條第 2 項第 3 款
- 可在公會會員名錄查投顧或兼營投顧（今天查詢兼營投顧名錄，含銀行、證券商、期貨商、投信）｜ok｜MEM
- 未經許可經營證券投資顧問業務，投信投顧法第 107 條訂有刑責｜ok｜L121 第 107 條第 1 款
- 爭議可向公會申訴或向金融消費評議中心申請評議｜ok｜TPL 第十四點

## 免責、連結、來源

- 最後一個區塊是免責 callout，含「不是投資建議」、中括號「費用、稅負與交易規則」、查證日 2026-10-05｜ok｜docs/life-finance-series-brief.md §5
- 站內連結只有 finance-glossary-50-terms 與 personal-finance-first-steps（指派允許的兩個）｜ok｜docs/life-ai-income-investing/README.md
- sources 16 筆全部 HTTP 200 且內容與引用相符，checked_on 2026-10-05｜ok｜如上
- selaw 是否官方：公會首頁「投信投顧法規」選單直接連到 selaw 的公會法規列表，視為公會第一方文本｜ok｜https://www.selaw.com.tw/Chinese/LegalSystemInquiry/LawSystemQueryList/8103
