# ai-trading-bot-claims — 查證紀錄

查證日一律 2026-10-05。格式：主張｜來源網址｜查證日｜怎麼讀到的。

讀法說明：
- 全部用 `curl -sSL`（UA：Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)，加 --retry），
  確認 HTTP 200 後去掉 `<!-- -->` 註解與 script／style 再讀本文。腳本：/home/user/batch-ai-income/_tools/ai-trading-bot-claims/page.py（網頁、PDF 用 pdftotext）、docx.py（金管會附件 .docx）。
  抓下來的原文在 /home/user/batch-ai-income/_tools/ai-trading-bot-claims/raw/。
- eCFR 的一般網址會被導到 unblock.federalregister.gov（機器人驗證頁，不算來源），改讀 eCFR 官方 renderer API
  （https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-17?part=4&section=4.41 與 ?part=275&section=275.206(4)-1，HTTP 200）；sources 仍寫 eCFR 原始網址。
- investor.gov（SEC 投資人教育站）與 iosco.org 對本環境回 403；web.archive.org 連線被重設。SEC 與 NASAA、FINRA 的聯合警示改讀 FINRA 站上的同一篇（HTTP 200）。
- twse.com.tw 對本環境回 307 安全阻擋頁，沒有使用證交所頁面。3434.twsa.org.tw（證券商公會的非核准業者警示專區）curl 無回應、WebFetch 503，未使用。
- WebSearch 只用來找網址，內容一律回官方頁讀原文。

## 回測與績效宣稱（第一節）

- 假設性績效＝not actually achieved by any portfolio of the investment adviser；包含 model portfolios、backtested（application of a strategy to data from prior time periods when the strategy was not actually used）、targeted or projected returns｜https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.206(4)-1｜2026-10-05｜eCFR renderer API，(e)(8)；正文「SEC 的投資顧問廣告規則把回測歸為假設性績效，也就是沒有實際投資組合真正達成過的結果」
- 同規則 (a)(6)：不得以不公平平衡的方式納入或排除績效、呈現期間；(d)(1) 毛績效須並列淨績效（扣費）；(d)(4) related performance 須含全部相關投資組合｜同上｜2026-10-05｜正文「挑期間、挑參數」「沒扣成本」是依此舉例，未逐條寫進正文
- CFTC 17 CFR 4.41(b)(1) 警語全文：simulated or hypothetical performance results have certain inherent limitations… do not represent actual trading… may have under-or over-compensated for the impact… of certain market factors, such as lack of liquidity… designed with the benefit of hindsight. No representation is being made that any account will or is likely to achieve profits or losses similar to these being shown｜https://www.ecfr.gov/current/title-17/chapter-I/part-4/subpart-D/section-4.41｜2026-10-05｜eCFR renderer API（API 自動導向 subpart=D）；正文「模擬不代表實際交易，可能低估或高估流動性不足等因素的影響，而且是在已知結果的情況下設計出來的」與「就算換成實際帳戶的紀錄……不表示之後會有類似結果」
- 存活者偏差的定義：The disappearance of failed companies from performance indexes so that they present misleading results｜https://www.sec.gov/investor/locinvestorbehaviorbib.pdf｜2026-10-05｜curl 200，pdftotext，詞彙表（美國國會圖書館為 SEC 所編，2010）；概念說明，未列入 sources
- 過度配適、挑期間的說明是概念解釋，以 CFTC 警語的 benefit of hindsight 與 SEC (a)(6) 為依據，不是數字
- 證券交易稅：向出賣有價證券人按每次交易成交價格課徵，股票千分之三｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340078｜2026-10-05｜curl 200，第 2 條第 1 款（修正日期民國 114 年 1 月 2 日）
- 當日沖銷（同一帳戶同一營業日現款買進與現券賣出同種類同數量上市櫃股票）：證券商受託買賣自 106.4.28、自行買賣自 107.4.28 起至民國 116 年 12 月 31 日（＝2027 年 12 月 31 日）止，按千分之一點五課徵｜同上｜2026-10-05｜第 2-2 條
- 假設試算：100 萬元 × 千分之三 × 50 次 ＝ 15 萬元｜（自算，假設值）｜2026-10-05｜正文明寫「假設」
- 手續費：沒有寫費率。證交所的舊函（79 年核定千分之一．四二五）見於 twse-regulation 法規知識庫，但之後改為券商自訂費率，現行規則沒查到官方頁，所以正文只寫「手續費」不寫數字
- 投信投顧公會自動化投資顧問服務審查小組：審查申請以自動化工具提供服務或變更演算法之案件，主要審查事項含「以歷史資料回測時能否達成預期成效」｜https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11301204｜2026-10-05｜curl 200，第 2 條（法規正式名稱：中華民國證券投資信託暨顧問商業同業公會證券投資顧問事業以自動化工具提供證券投資顧問服務審查小組之設置及作業要點，113.11.21 訂定；sources 標題已改成正式名稱）
- 管理規則第 25-3 條：提供自動化投資顧問服務及變更所使用之演算法者，應檢具書件送同業公會審查；113.10.25 修正施行前已提供者無須重審，但演算法變更仍須審查｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077｜2026-10-05｜curl 200（查核第一輪補上；正文改寫成依第 25-3 條「提供或變更演算法須送審」，原稿「演算法上線或變更前」沒有法源條號）

## 證券投資信託及顧問法與管理規則（第二節）

- 第 4 條第 1 項：證券投資顧問＝直接或間接自委任人或第三人取得報酬，對有價證券、證券相關商品或其他經主管機關核准項目之投資或交易有關事項，提供分析意見或推介建議｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121｜2026-10-05｜curl 200（修正日期民國 112 年 6 月 28 日）
- 第 4 條第 3、4 項：業務種類含證券投資顧問業務、全權委託投資業務，應報請主管機關核准（表格「全權委託投資業務，須另經核准」）｜同上｜2026-10-05｜curl 200
- 第 6 條第 1 項：非依本法不得經營證券投資信託、證券投資顧問及全權委託投資業務｜同上｜2026-10-05｜curl 200（正文未寫條號）
- 第 63 條第 1 項：應經主管機關許可並核發營業執照後始得營業｜同上｜2026-10-05｜curl 200
- 第 107 條第 1 款：未經許可經營證券投資顧問業務、全權委託投資業務等，處五年以下有期徒刑，併科新臺幣一百萬元以上五千萬元以下罰金｜同上｜2026-10-05｜curl 200
- 第 70-1 條第 1 項：非投信投顧事業之投資廣告不得（一）使人誤信已經核准（二）投資分析同時招攬（三）保證獲利或負擔損失之表示（四）引用推薦書、感謝函、過去績效或其他易使人誤認確可獲利之文字（五）冒用著名人士或公司名義推介｜同上｜2026-10-05｜curl 200；第 2 項網路平台應載明委託刊播者、出資者（正文刪去）
- 第 60 條：簽全權委託投資契約前要交付全權委託投資說明書，並有七日以上期間供客戶審閱全部條款｜同上｜2026-10-05｜curl 200
- 管理規則第 10 條：接受委任提供分析意見或推介建議應訂書面契約；契約應記載「不得收受客戶資金或代理從事證券投資行為」（第 8 款）、「客戶得自收受書面契約之日起七日內，以書面終止契約」（第 11 款）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077｜2026-10-05｜curl 200（修正日期民國 113 年 10 月 25 日）
- 管理規則第 13 條第 2 項第 2 款（代理他人從事有價證券投資）、第 7 款（保管或挪用客戶之有價證券、款項、印鑑或存摺）｜同上｜2026-10-05｜curl 200
- 管理規則第 14 條第 1 項第 6 款（保證獲利或負擔損失之表示）、第 14 款（引用推薦書、感謝函、過去績效或其他易使人認為確可獲利之類似文字或表示）、第 15 款（推廣業務書面文件未列明公司登記名稱、地址、電話及營業執照字號）｜同上｜2026-10-05｜curl 200
- 問答集：經營投顧業務四要件（提供分析意見或推介建議、取得報酬、對價關係、經常性反覆）；第三題個人名義亦可能構成；第四題社群收費（課程費、訂閱費、會員費）提供特定股票買賣時點、支撐壓力點或價位並經常性反覆為之，與經營投顧業務無異；第六題一般性證券投資資訊（基本統計分析、技術分析理論）；第七題程式軟體含對個別有價證券提供買賣價位、支撐壓力點、停損停利價位等功能者可能涉及非法經營，僅基本統計分析者非屬之；各題均註明須依個案由司法機關判斷｜https://www.sitca.org.tw/ROC/Legal/files/%E8%AA%8D%E5%AE%9A%E7%B6%93%E7%87%9F%E8%AD%89%E5%88%B8%E6%8A%95%E8%B3%87%E9%A1%A7%E5%95%8F%E6%A5%AD%E5%8B%99%E4%B9%8B%E5%95%8F%E7%AD%94%E9%9B%86.pdf｜2026-10-05｜curl 200，pdftotext；頁首「金融監督管理委員證券期貨局 112 年 6 月 13 日證期(投)字第 1120340840 號函洽悉」

## 期貨與虛擬資產（表格）

- 期貨交易法第 82 條：經營期貨信託、期貨經理、期貨顧問事業或其他期貨服務事業，須經許可並發給許可證照｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400100｜2026-10-05｜curl 200（修正日期民國 112 年 6 月 28 日）
- 第 112 條第 5 項第 5 款：未經許可擅自經營期貨經理、期貨顧問事業，七年以下有期徒刑，得併科新臺幣三百萬元以下罰金｜同上｜2026-10-05｜curl 200（正文最後刪去刑度，只留第 82 條）
- 金管會「非法期貨業類型」：外匯保證金自動交易平台、非法代操、以期貨分析系統軟體招收會員（系統出現買賣訊號或設定自動下單）屬違法經營期貨顧問／經理事業｜https://www.sfb.gov.tw/ch/home.jsp?id=1046&parentpath=0%2C5%2C775｜2026-10-05｜頁面 curl 200；附件 https://www.fsc.gov.tw/userfiles/file/%E9%9D%9E%E6%B3%95%E6%9C%9F%E8%B2%A8%E6%A5%AD%E9%A1%9E%E5%9E%8B20241008.docx（第一次連線被代理切斷，重試後 200，解壓 document.xml 讀文字）
- 期貨業名冊含期貨經理事業與期貨顧問事業清單（統計日期 115 年 10 月 1 日）｜https://www.sfb.gov.tw/ch/home.jsp?id=1015&parentpath=0%2C4｜2026-10-05｜頁面 curl 200；下載附件 ODS（1151001期貨業名冊.ods）解壓 content.xml 讀到兩段標題
- 洗錢防制法第 6 條第 1 項：提供虛擬資產服務之事業或人員未完成洗錢防制登記者，不得提供虛擬資產服務；第 4 項刑責｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0380131｜2026-10-05｜curl 200（單條頁第一次回 MOJ 錯誤頁，改讀全文頁 200；修正日期民國 113 年 7 月 31 日）；sources 以證期局頁代表，未另列
- 證期局「提供虛擬資產服務之事業或人員」頁：引第 6 條第 1 項，列已完成洗錢防制登記之業者名單（115.9.29 更新）｜https://www.sfb.gov.tw/ch/home.jsp?id=1053&parentpath=0%2C8｜2026-10-05｜curl 200（正文不點名任何業者）

## 合法業者怎麼查（第三節）

- 投信投顧公會「會員名錄查詢」：名錄類別有投信名錄、投顧名錄、兼營投顧名錄、境外基金總代理人、全權委託業者名錄；可輸入公司名稱；公司詳細資料有負責人、住址、電話、傳真｜https://www.sitca.org.tw/ROC/MemData/MD2001N.aspx?PGMID=AS0701｜2026-10-05｜curl 200；詳細資料頁 MD2002.aspx 200（未列 sources，不點名公司）
- 公會聯絡電話 (02)2581-7288；投資人申訴（查詢－證投顧合格登錄人員）專線分機 110，查詢時務請備妥公司及人員名稱｜同上｜2026-10-05｜curl 200，頁尾
- 「經營事項一覽表」可依業務別看各公司核准經營的業務（證券投資顧問事業、以委任方式兼營全權委託投資業、期貨顧問事業等）｜https://www.sitca.org.tw/ROC/MemData/MD1001N.aspx?PGMID=AS0702｜2026-10-05｜curl 200
- 「統計資料 → 全權委託各項資料 → 經營公司」頁存在｜https://www.sitca.org.tw/ROC/Industry/IN4002.aspx?PGMID=IN0402｜2026-10-05｜curl 200（sources 筆數上限，未列；金管會「非法投信投顧業類型」附件也寫了這條查詢路徑）
- 金管會「非法投信投顧業類型」：社群招攬付費會員盤中推介、販售交易程式（宣稱無風險套利、勝率高、預測價位）屬非法經營投顧；投資人交付集保帳戶存摺及密碼由非法業者下單屬非法全權委託；查詢路徑：公會網站「關於公會/會員名錄/經營事項一覽表」、「統計資料/全權委託各項資料/已獲准經營公司」｜https://www.sfb.gov.tw/ch/home.jsp?id=1046&parentpath=0%2C5%2C775｜2026-10-05｜附件 https://www.fsc.gov.tw/userfiles/file/%E9%9D%9E%E6%B3%95%E6%8A%95%E4%BF%A1%E6%8A%95%E9%A1%A7%E6%A5%AD%E9%A1%9E%E5%9E%8B.docx，curl 200
- 證期局「證券期貨特許事業」：投顧公司名冊（115.10.1 更新）、期貨業名冊（115.9.30 更新）可下載 EXCEL／ODS｜https://www.sfb.gov.tw/ch/home.jsp?id=1015&parentpath=0%2C4｜2026-10-05｜curl 200（舊頁 id=776 註明已改版到此頁）
- 公會「非法業者警示專區」註明：本警示專區未含所有非法業者資料｜https://www.sitca.org.tw/ROC/Legal/main2.html｜2026-10-05｜curl 200
- 證券期貨反詐騙諮詢專線（02）2737-3434（三思三思），由投保中心提供反詐騙諮詢，證券期貨三公會提供合法業者查詢服務；檢舉電話 (02)8773-4136（週一至週五 9:00–17:00）｜https://www.sfb.gov.tw/ch/home.jsp?id=1048&parentpath=0%2C5%2C775｜2026-10-05｜curl 200

## 詐騙分界（第四節）

- 假投資：網路社群或交友軟體主動認識，加入 LINE 投資群組，初期小額獲利，以資金越多獲利越多引誘至投資網站或下載 APP 投入大量資金，以洗碼量不足、繳保證金、IP 異常等理由拒絕出金；聽到「保證獲利」「穩賺不賠」必定是詐騙｜https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e｜2026-10-05｜curl 200
- 證期局詐騙類型：假冒合法金融機構發簡訊招攬加 LINE 群組；假冒財經名人成立群組；假投資平台 App 宣稱插隊搶漲停並保證獲利｜https://www.sfb.gov.tw/ch/home.jsp?id=1047&parentpath=0%2C5%2C775｜2026-10-05｜curl 200（正文只用冒用財經名人一項）
- 三不三要：不將款項匯至非法證券期貨業者指定之帳戶等｜https://www.fsc.gov.tw/userfiles/file/%E9%98%B2%E5%88%B6%E9%9D%9E%E6%B3%95%E8%AD%89%E5%88%B8%E6%9C%9F%E8%B2%A8%E6%A5%AD_%E4%B8%89%E4%B8%8D%E4%B8%89%E8%A6%81%E5%8E%9F%E5%89%87.docx｜2026-10-05｜由證期局 id=1049 頁連出，curl 重試後 200（未列 sources；正文「要你把錢匯到對方指定的帳戶」依此）
- 165 反詐騙諮詢專線可諮詢、檢舉或報案；可利用 165 官方網站網路報案｜https://www.npa.gov.tw/ch/app/faq/view?module=faq&id=2144&serno=A1078837｜2026-10-05｜curl 200
- CFTC：AI technology can’t predict the future or sudden market changes；scammers claim AI-created algorithms can generate huge returns or yield 100 percent “win” rates；建議考慮 fees, spreads, subscription costs 對報酬的影響｜https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/AITradingBots.html｜2026-10-05｜curl 200（正文不寫 CFTC 案例的金額與人數）
- SEC、NASAA、FINRA 聯合警示（2024-01-25）：未註冊平台宣稱使用 AI、保證高報酬低風險是典型警訊、以 AI 製作 deepfake 影音冒充｜https://www.finra.org/investors/insights/artificial-intelligence-and-investment-fraud｜2026-10-05｜curl 200（investor.gov 版本 403）；正文改為「聯合投資人警示也提到，詐騙者會用 AI 仿造聲音、製作假影片來冒充他人」（查核第一輪：原文並未說名人推薦影片是深度偽造，且原句接在 CFTC 後面，像是 CFTC 說的；CFTC 頁沒有 deepfake 字樣）

## 用過但最後刪掉的

- 金管會 2024-06-20 發布「金融業運用人工智慧(AI)指引」，屬行政指導，可解釋性指金融機構可清楚說明 AI 系統如何運作及預測或決策背後之邏輯｜https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0%2C2&mcustomize=news_view.jsp&dataserno=202406200001&dtable=News｜2026-10-05｜curl 200。為壓字數刪去，未列 sources。

## 圖

- diagram-1.svg 上的數字：165、02、2737、3434、2581、7288、110、8773、4136、2026；正文都有（2026 在表格 caption 與免責 callout）。intake_check「every number on the diagram is in the text」ok。
- diagram-1：由上往下四個問題的判斷流程，答「是」往右（停止付款、一般性投資資訊、可能涉及非法經營、假設性績效），四題都否到「再看契約」；右下角虛線框放查詢與檢舉電話。渲染 PNG 已開圖檢查，無壓線、無溢出，右下空白已補。
- hero.svg（機械關卡重畫，2026-10-05）：一面深色圓角外框的後照鏡，頂端短桿接一顆青綠色晶片（AI）；鏡中是走過的路：淺藍天空兩朵白雲、淺綠地面一條灰色道路延伸到畫面中央的地平線、白色分隔線、路旁四棵樹；下方一行字「回測只看得到過去」60px（對應正文「回測是把一套買賣規則套進過去的行情」）。沒有長條、曲線、金幣、臉孔、logo；道路往正中央的消失點收窄，不做往右上升的斜線。舊版（螢幕＋對話框＋名冊＋藍色放大鏡＋打勾）和同批 ai-concept-stocks-explained（文件上藍色放大鏡框住一列）、ai-freelance-getting-started（螢幕、對話框、放大鏡、打勾）構圖重複，存於 _tools/ai-trading-bot-claims/hero-v1-magnifier.svg。hero alt 已同步改寫，渲染 PNG 與 400 px 縮圖都開圖看過。
- diagram-1 的 alt 補上右下角的人員資格查詢與檢舉電話框。

## 機械關卡（2026-10-05）

- pack_cli ingest --dry-run：通過；唯一警告 finance_claim_language（保證獲利、穩賺）出現在「不得表示保證獲利」的法條轉述與「常見的詐騙徵兆」清單，屬財經 brief §2 第 3 點允許的引用。
- intake_check：0 FAIL。WARN「查證日」來自免責 callout 模板固定句；WARN「no hero title」只適用 Commons 照片，本篇是自繪 hero。正文 2,737 字（1,800–3,000 區間內）。

## 查核第一輪（2026-10-05，獨立查核）

全部來源重新以 curl -sSL 讀取（腳本 /home/user/batch-ai-income/_tools/ai-trading-bot-claims/v1/fetch.py，原文存 v1/raw/）。逐條結果見 verify-1.md。改動：
- CFTC 17 CFR 4.41(b)：適用對象是 commodity pool operator、commodity trading advisor 及其 principal，且可改用期貨公會（NFA）規定的警語；正文由「要求業者」改為「規定商品交易顧問等期貨業者……條文列出的標準文字寫明」。
- 深度偽造：CFTC 頁沒有提到 deepfake；FINRA 聯合警示寫的是用 AI 仿造聲音、影片冒充家人或公司執行長，不是「名人推薦影片」。正文改寫並明確歸給 SEC、NASAA、FINRA 的聯合警示。
- 第 70-1 條主體改照條文：「不是投信投顧事業的人刊登涉及有價證券投資或業務招攬的廣告」。
- 警告 callout 補上第 61 條：合法全權委託要簽全權委託投資契約，客戶另與保管機構簽約；原句「查不到全權委託資格的業者……不要交」會讓人以為交給有資格的業者就可以。
- 管理規則第 14 條第 1 項第 15 款的對象是「為推廣業務所製發之書面文件」，正文照改。
- sources：投信投顧法標題補第 61 條、管理規則標題補第 25-3 條、selaw 標題改成正式法規名稱（FINRA 標題「含深度偽造影音」與頁內小標相符，不改）。
- sfb.gov.tw id=1015 與 cib.npa.gov.tw 第一次連線被重設，重試後 HTTP 200。eCFR 一般網址今天仍導到 unblock.federalregister.gov，renderer API 200。

## 查核第二輪（2026-10-05）

全部來源重新以 curl -sSL 讀取（腳本 /home/user/batch-ai-income/_tools/ai-trading-bot-claims/v2/fetch.py、v2/docx.py，原文存 v2/raw/，全部 HTTP 200；eCFR 一般網址仍導到 unblock.federalregister.gov，改讀 renderer API）。逐條結果見 verify-2.md。改動：
- 第 61 條但書與第 62 條末項有自行保管的例外：callout 改為「原則上客戶還要另與保管機構簽約」，結尾改為「對方查不到全權委託資格，獲利說得再好也不要把錢或帳戶交出去」。
- 詐騙徵兆清單的引言明寫「常見的詐騙徵兆」，「保證獲利、穩賺不賠」改成「對方說保證獲利、穩賺不賠」（財經 brief §2 第 3 點的引用條件）。
- 導言第一段改成一句話回答；「持牌」改台灣用語；「條文列出的標準文字」改「標準警語」；過度配適「就失靈」改「就可能失靈」。
- 刪掉第 60 條（全權委託說明書與七日審閱期）一句以壓字數，投信投顧法來源標題同步拿掉第 60 條。正文 2,782 → 2,737 字。

## 跨篇核對（2026-10-05）

- 證交稅寫法改成與 thematic-etf-index-rules 一致的阿拉伯數字（千分之 3、千分之 1.5），數值不變：證券交易稅條例第 2 條第 1 款千分之三、第 2-2 條當沖千分之一點五至民國 116 年 12 月 31 日（2027-12-31）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340078｜2026-10-05
- 管理規則第 25-3 條（自動化投資顧問服務及演算法變更送同業公會審查）、投信投顧法第 107 條（五年以下、併科一百萬元以上五千萬元以下）今日重讀相符｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400077&flno=25-3、https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400121&flno=107｜2026-10-05
