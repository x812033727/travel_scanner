# ai-trading-bot-claims：查核第一輪（2026-10-05）

格式：主張｜結論（ok / fixed / softened / removed）｜來源網址。原文於 2026-10-05 以 curl -sSL 重新讀取，存在 /home/user/batch-ai-income/_tools/ai-trading-bot-claims/v1/raw/。

## 標題、描述、摘要、導言

- 標題「AI 選股」「AI 交易機器人」的宣傳怎麼看：回測、績效宣稱與合法業者（符合指派、無產品名）｜ok｜docs/life-ai-income-investing/README.md
- description：回測落差（過度配適、存活者偏差、交易成本）、投信投顧法對未經許可提供個股建議、販售選股軟體與投資廣告的規定、名冊查詢、與詐騙分界｜ok（範圍與正文一致）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 摘要 1：回測是套進過去行情的假設性績效，事後調參數、少了下市公司、沒扣成本會讓它好看｜ok｜https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.206(4)-1
- 摘要 2：收取報酬、經常性對個股提供分析建議屬須經許可的投顧業務；販售報個股買賣價位的軟體可能涉及非法經營｜ok｜https://www.sitca.org.tw/ROC/Legal/files/%E8%AA%8D%E5%AE%9A%E7%B6%93%E7%87%9F%E8%AD%89%E5%88%B8%E6%8A%95%E8%B3%87%E9%A1%A7%E5%95%8F%E6%A5%AD%E5%8B%99%E4%B9%8B%E5%95%8F%E7%AD%94%E9%9B%86.pdf
- 摘要 3：遇到保證獲利、指定帳戶匯款、交出帳號密碼撥 165 或（02）2737-3434｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1048&parentpath=0%2C5%2C775
- 導言：在台灣收費對個股提供買賣建議需要投顧許可｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 機構全名「中華民國證券投資信託暨顧問商業同業公會」「金融監督管理委員會證券期貨局」｜ok｜https://www.sitca.org.tw/ROC/MemData/MD2001N.aspx?PGMID=AS0701

## 回測與成本

- SEC 投資顧問廣告規則把回測歸為假設性績效（not actually achieved by any portfolio of the investment adviser；backtested 列在 (e)(8)(i)(B)）｜ok｜https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.206(4)-1（一般網址導到 unblock.federalregister.gov，以 eCFR renderer API 讀取，HTTP 200）
- CFTC「要求業者」展示模擬績效附警語｜fixed：17 CFR 4.41(b) 的對象是商品基金經營者、商品交易顧問及其主事者，且可改用期貨公會規定的警語；改為「規定商品交易顧問等期貨業者……條文列出的標準文字寫明」｜https://www.ecfr.gov/current/title-17/chapter-I/part-4/subpart-D/section-4.41（renderer API 讀取）
- 警語內容：不代表實際交易、可能低估或高估流動性不足等因素影響、在已知結果下設計（benefit of hindsight）｜ok｜同上
- 過度配適、存活者偏差、挑期間挑參數、沒扣成本（手續費、證交稅、價差、滑價）｜ok（概念說明，無數字；挑期間對應 SEC 規則 (a)(6)）｜https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.206(4)-1
- 證券交易稅：賣出股票按每次成交價格課千分之三（第 2 條第 1 款）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340078
- 當日沖銷千分之一點五，至民國 116 年 12 月 31 日（＝2027 年 12 月 31 日）（第 2-2 條）｜ok｜同上
- 假設試算：100 萬元 × 千分之三 × 50 次 ＝ 15 萬元｜ok（算式正確，明寫假設）｜同上
- 手續費不寫費率｜ok（沒有官方現行費率頁，未寫數字）｜—
- 實際帳戶紀錄也不代表之後會有類似結果｜ok（4.41 警語 No representation… likely to achieve profits or losses similar）｜https://www.ecfr.gov/current/title-17/chapter-I/part-4/subpart-D/section-4.41
- 機器人理財「演算法上線或變更前」要送公會審查，項目含以歷史資料回測能否達成預期成效｜fixed：補上法源（管理規則第 25-3 條：提供服務或變更演算法須送同業公會審查），作業要點第 2 條寫的是「主要審查事項」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077 ； https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11301204
- 內部連結 robo-advisor-taiwan-explained（本批 sibling，工作區已有 pack.json、hero.svg、diagram-1.svg，今天 dry-run 通過）；連結文字「機器人理財在台灣怎麼管、費用怎麼算」與該篇內容相符｜ok｜https://mokaair.com/zh-TW/life/robo-advisor-taiwan-explained

## 投信投顧法與管理規則

- 第 4 條：證券投資顧問＝取得報酬，對有價證券投資提供分析意見或推介建議（修正日期 112.06.28）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 第 63 條：經許可並核發營業執照後始得營業｜ok｜同上
- 第 107 條：未經許可經營投顧、全權委託業務，五年以下有期徒刑，併科新臺幣 100 萬元以上 5,000 萬元以下罰金｜ok｜同上
- 問答集四要件：分析或建議、取得報酬、對價關係、經常性反覆｜ok｜https://www.sitca.org.tw/ROC/Legal/files/%E8%AA%8D%E5%AE%9A%E7%B6%93%E7%87%9F%E8%AD%89%E5%88%B8%E6%8A%95%E8%B3%87%E9%A1%A7%E5%95%8F%E6%A5%AD%E5%8B%99%E4%B9%8B%E5%95%8F%E7%AD%94%E9%9B%86.pdf
- 問答集第三、四題：個人名義或社群收費（課程費、訂閱費、會員費）提供特定股票買賣時點或價位並經常性為之，與經營投顧業務無異｜ok｜同上
- 問答集第七題：軟體對個別股票給買賣價位、支撐壓力點、停損停利價位可能涉及非法經營；只做基本統計分析非屬之｜ok｜同上
- 問答集第五、六題：一般性證券投資資訊（技術分析理論等）；最後由司法機關依個案判斷｜ok｜同上
- 問答集頁首「證期局 112 年 6 月 13 日證期(投)字第 1120340840 號函洽悉」（sources 標題）｜ok｜同上
- 第 70-1 條主體「非投信投顧事業的投資廣告」｜fixed：照條文改為「不是投信投顧事業的人刊登涉及有價證券投資或業務招攬的廣告」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 第 70-1 條各款：誤信已核准、保證獲利、引用推薦書感謝函過去績效、冒用名人名義｜ok｜同上
- 管理規則第 14 條第 1 項第 6、14 款：持牌投顧不得保證獲利、不得引用過去績效等易使人認為確可獲利之表示（修正日期 113.10.25）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077

## 怎麼查合法業者

- 推廣文件要列明公司登記名稱、地址、電話、營業執照字號｜fixed（措辭照第 14 條第 1 項第 15 款「為推廣業務所製發之書面文件」）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077
- 公會「會員名錄查詢」有投顧名錄、兼營投顧名錄，可輸入公司名稱，詳細資料有住址與電話｜ok｜https://www.sitca.org.tw/ROC/MemData/MD2001N.aspx?PGMID=AS0701
- 「經營事項一覽表」可看各公司核准業務｜ok｜https://www.sitca.org.tw/ROC/MemData/MD1001N.aspx?PGMID=AS0702
- 「全權委託各項資料 → 經營公司」查詢路徑｜ok（公會網站選單；金管會非法投信投顧業類型附件寫同一路徑）｜https://www.sfb.gov.tw/ch/home.jsp?id=1046&parentpath=0%2C5%2C775
- 證期局「證券期貨特許事業」可下載投顧公司名冊、期貨業名冊｜ok（今日頁面列 115_10_01 投顧名冊、1151001 期貨業名冊）｜https://www.sfb.gov.tw/ch/home.jsp?id=1015&parentpath=0%2C4
- 公會電話（02）2581-7288，查合格登錄人員分機 110｜ok｜https://www.sitca.org.tw/ROC/MemData/MD2001N.aspx?PGMID=AS0701
- 證券期貨反詐騙諮詢專線（02）2737-3434，三公會提供合法業者查詢服務｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1048&parentpath=0%2C5%2C775
- 非法業者警示專區未含所有非法業者｜ok｜https://www.sitca.org.tw/ROC/Legal/main2.html
- 投顧要訂書面契約；收受書面契約之日起七日內可書面終止（第 10 條第 2 項、第 3 項第 11 款）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077
- 投顧不得收受客戶資金、代理投資、保管存摺印鑑（第 10 條第 3 項第 8 款、第 13 條第 2 項第 2、7 款）｜ok｜同上
- 全權委託要先交付說明書並給七日以上審閱期（投信投顧法第 60 條）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121

## 表格

- 群組或訂閱收費報個股買賣點：投顧業務須經許可；查投顧、兼營投顧名錄｜ok｜https://www.sitca.org.tw/ROC/Legal/files/%E8%AA%8D%E5%AE%9A%E7%B6%93%E7%87%9F%E8%AD%89%E5%88%B8%E6%8A%95%E8%B3%87%E9%A1%A7%E5%95%8F%E6%A5%AD%E5%8B%99%E4%B9%8B%E5%95%8F%E7%AD%94%E9%9B%86.pdf
- 販售報個股價位的選股軟體：可能涉及非法經營｜ok｜同上
- 代你下單：全權委託投資業務須另經核准（第 4 條第 3、4 項）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 期貨、外匯保證金訊號或自動交易：期貨交易法第 82 條，期貨顧問、期貨經理事業須經許可；期貨業名冊（金管會非法期貨業類型列外幣保證金、以期貨分析系統軟體招收會員）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400100 ； https://www.sfb.gov.tw/ch/home.jsp?id=1046&parentpath=0%2C5%2C775
- 虛擬資產平台：洗錢防制法第 6 條，須完成洗錢防制登記；證期局業者名單（115.9.29 更新）｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1053&parentpath=0%2C8
- 表格 caption「查證於 2026 年 10 月」｜ok｜—

## 詐騙分界

- 假投資流程：LINE 投資群組、先小額獲利、下載 App 投入大筆資金、以洗碼量不足或繳保證金拒絕出金｜ok｜https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e（第一次連線重設，重試 200）
- 冒用財經名人名義成立群組｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1047&parentpath=0%2C5%2C775
- CFTC：AI 無法預測未來或突如其來的市場變化；宣稱 100% 勝率是話術｜ok｜https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/AITradingBots.html
- 「名人推薦影片也可能是深度偽造」（接在 CFTC 句後）｜fixed：CFTC 頁沒有 deepfake；SEC、NASAA、FINRA 聯合警示寫的是用 AI 仿造聲音、製作假影片冒充他人，改寫並歸給聯合警示｜https://www.finra.org/investors/insights/artificial-intelligence-and-investment-fraud
- 警訊清單：保證獲利、穩賺不賠（警政署原文「聽到保證獲利、穩賺不賠必定是詐騙」，以詐騙特徵引用）｜ok｜https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e
- 警訊清單：匯到指定帳戶（三不三要原則「不將款項匯至非法證券期貨業者指定之帳戶」）｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1049&parentpath=0%2C5%2C775
- 警訊清單：交出帳號密碼或集保存摺（非法全權委託態樣）｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1046&parentpath=0%2C5%2C775
- 警訊清單：出金前補繳保證金｜ok｜https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e
- 165 反詐騙諮詢專線可諮詢、檢舉或報案，165 網站可網路報案｜ok｜https://www.npa.gov.tw/ch/app/faq/view?module=faq&id=2144&serno=A1078837
- 檢舉電話（02）8773-4136｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1048&parentpath=0%2C5%2C775
- 警告 callout：交出帳號密碼或集保存摺＝金管會列舉的非法全權委託態樣｜ok；補充 fixed：原句「查不到全權委託資格的業者……不要交」暗示交給有資格的業者可以，補上第 61 條「客戶另與保管機構簽約」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 內部連結 ai-scams-deepfake-taiwan、warning-account-prevention、online-banking-security（指派允許的網址，連結文字與目標文章內容相符）｜ok｜https://mokaair.com/zh-TW/life/ai-scams-deepfake-taiwan
- 免責 callout：含「不是投資建議」、中括號「費用、稅負與交易規則」、查證日 2026-10-05、最後一個區塊｜ok（標題省略「這篇是」以守住本文／這篇 ≤ 1 次）｜docs/life-finance-series-brief.md §5

## 圖

- diagram-1.svg 數字 165、（02）2737-3434、（02）2581-7288 分機 110、（02）8773-4136、2026：正文皆有；七日內書面終止、投顧不得收受資金或代下單｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077
- diagram-1 渲染：無壓線、溢出、互疊，構圖置中｜ok｜—
- hero.svg：無數字、無 logo、無臉、無長條或曲線，一行 60px 文字；alt 與畫面一致｜ok｜—

## sources（20 筆，全部 HTTP 200，checked_on 2026-10-05）

- 1 投信投顧法｜ok（標題補第 61 條）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400121
- 2 投顧事業管理規則｜ok（標題補第 25-3 條）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400077
- 3 問答集 PDF｜ok｜https://www.sitca.org.tw/ROC/Legal/files/%E8%AA%8D%E5%AE%9A%E7%B6%93%E7%87%9F%E8%AD%89%E5%88%B8%E6%8A%95%E8%B3%87%E9%A1%A7%E5%95%8F%E6%A5%AD%E5%8B%99%E4%B9%8B%E5%95%8F%E7%AD%94%E9%9B%86.pdf
- 4 會員名錄查詢｜ok｜https://www.sitca.org.tw/ROC/MemData/MD2001N.aspx?PGMID=AS0701
- 5 經營事項一覽表｜ok｜https://www.sitca.org.tw/ROC/MemData/MD1001N.aspx?PGMID=AS0702
- 6 非法業者警示專區｜ok｜https://www.sitca.org.tw/ROC/Legal/main2.html
- 7 證期局特許事業｜ok（第一次連線重設，重試 200）｜https://www.sfb.gov.tw/ch/home.jsp?id=1015&parentpath=0%2C4
- 8 非法經營態樣｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1046&parentpath=0%2C5%2C775
- 9 詐騙類型｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1047&parentpath=0%2C5%2C775
- 10 投資人申訴方式｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1048&parentpath=0%2C5%2C775
- 11 虛擬資產服務業者｜ok｜https://www.sfb.gov.tw/ch/home.jsp?id=1053&parentpath=0%2C8
- 12 期貨交易法｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400100
- 13 證券交易稅條例｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340078
- 14 刑事警察局假投資｜ok｜https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e
- 15 警政署 165 FAQ｜ok｜https://www.npa.gov.tw/ch/app/faq/view?module=faq&id=2144&serno=A1078837
- 16 selaw 審查小組作業要點｜fixed（標題改成正式法規名稱）｜https://www.selaw.com.tw/Chinese/RegulatoryInformationResult/Article?sysnumber=LW11301204
- 17 eCFR 275.206(4)-1｜ok（原網址導到機器人驗證頁；以官方 renderer API 讀到條文）｜https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.206(4)-1
- 18 eCFR 4.41｜ok（同上）｜https://www.ecfr.gov/current/title-17/chapter-I/part-4/subpart-D/section-4.41
- 19 CFTC AI 交易機器人警示｜ok｜https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/AITradingBots.html
- 20 FINRA 聯合警示｜ok（頁內小標 AI-Enabled Technology Used to Scam Investors, Including "Deepfake" Video and Audio，標題相符）｜https://www.finra.org/investors/insights/artificial-intelligence-and-investment-fraud
