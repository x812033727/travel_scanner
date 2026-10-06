# verify-1：ai-concept-stocks-explained 查核第一輪（2026-10-05）

讀法：17 個 sources 全部今天 `curl -sSL`（批次 UA）重抓，HTTP 200，去 `<!-- -->` 後讀文字；法務部頁面第一次回錯誤頁的重抓到正文；PDF 用 pdftotext，櫃買中心觀測站手冊另轉圖看第 17、19、21 頁截圖。mops.twse.com.tw 今天仍回 WAF「FOR SECURITY REASONS」頁，web.archive.org 連線被重設。

主張｜判定｜來源

- 「AI 概念股」不是官方分類，證交所產業類別沒有 AI 類｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 證交所把上市公司分成 33 種產業類別，含半導體業、通信網路業、資訊服務業、數位雲端（逐項數過 33 類）｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 法規名稱「上市公司產業類別劃分暨調整要點」、版本 114.06.09｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 最近二個會計年度財報都顯示單一業務營收占比超過 50% → 歸入該類（要點三第一項第一款）｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 無一過半、三個部門各占 20% 以上且採多角化經營 → 綜合類；其餘 → 其他類｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 證交所每年依最近二個會計年度財報定期調整（要點五）｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 「產業類別反映的是公司過去兩年主要靠什麼賺營收」｜softened（改「大致反映」：要點五另有股本 2% 不予調整與證交所逕行調整的例外）｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007104
- 上櫃與興櫃公司由櫃買中心另訂產業類別定義，沒有獨立 AI 類｜ok｜https://dsp.tpex.org.tw/storage/co_download/table/%E4%B8%8A(%E8%88%88)%E6%AB%83%E5%85%AC%E5%8F%B8%E7%94%A2%E6%A5%AD%E9%A1%9E%E5%88%A5%E5%AE%9A%E7%BE%A9.pdf
- 櫃買中心數位雲端類定義把人工智慧列為技術例子之一（第 5 點「如區塊鏈、人工智慧等」）｜ok｜同上
- 證交所產業分類股價指數以各產業類別內的公司為成分股｜ok｜https://www.twse.com.tw/downloads/zh/products/indices/IndexS03.pdf
- 「（類股指數）」別稱｜removed（文件只用「產業分類股價指數」）｜https://www.twse.com.tw/downloads/zh/products/indices/IndexS03.pdf
- 來源標題「加權指數系列指數編製要點（2023.06 修訂）」｜ok（文件自訂簡稱「加權指數系列指數」，修訂日 2023.06）｜https://www.twse.com.tw/downloads/zh/products/indices/IndexS03.pdf
- 指數公司編製反映特定主題或投資策略的指數（通則 1.4）｜fixed（原文泛稱所有指數公司，改「以國內一家指數公司的指數通則為例」）｜https://taiwanindex.com.tw/downloads/compilation_rule （通則 PDF：backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/8/tw，檔案日期 2026/07/02）
- 每檔指數另訂編製規則，載明編製目標、成分篩選標準與流程、權重分配方式、定期審核與不定期調整（通則 2.1.2）｜ok（措辭對齊原文）｜同上
- 指數介紹頁最下方提供編製規則下載｜fixed（「以國內的指數公司為例」泛稱改為指向同一家，「下方」改「最下方」照 FAQ）｜https://taiwanindex.com.tw/promotion_and_service/investors_zone
- 有 ETF 追蹤的指數，成分股可在發行投信的申購買回清單（PCF）查到｜ok｜https://taiwanindex.com.tw/promotion_and_service/investors_zone
- 表格「主題指數：定期審核加不定期調整」｜ok（另有按月公布的定期審核日程表）｜https://taiwanindex.com.tw/downloads/technical_notice?category_id=3
- 表格「產業類別：證交所每年定期調整；公開劃分要點與類別定義」｜ok｜FL007104、櫃買中心定義 PDF
- 表格 caption「資料時間為 2026 年 10 月」｜ok｜（查證日）
- 公開資訊觀測站由證交所與櫃買中心等單位共同建置，可查上市、上櫃、興櫃與公開發行公司公開資訊｜ok｜https://dsp.tpex.org.tw/storage/education_event/113/5.%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E5%84%AA%E5%8C%96%E5%85%AC%E9%96%8B%E8%B3%87%E8%A8%8A%E8%A7%80%E6%B8%AC%E7%AB%99%E8%AA%AA%E6%98%8E.pdf
- 路徑 單一公司 → 營運概況 → 每月營收 → 月營業收入資訊｜ok（手冊第 19 頁截圖；現行網站被 WAF 擋，正文已寫名稱可能調整）｜同上
- 路徑 單一公司 → 電子文件下載 → 財務報告書／年報及股東會相關資料｜ok（第 17 頁截圖）｜同上
- 路徑 重大訊息/公告 → 重大訊息查詢 → 歷史重大訊息，輸入公司代號與年度；同一排有法說會分頁｜ok（第 21 頁截圖麵包屑與分頁列；手冊文字寫「當日重大訊息」，與截圖不一致，正文照介面截圖）｜同上
- 證交法第 36 條：每月 10 日以前公告並申報上月份營運情形｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400001&flno=36
- 施行細則第 5 條：營運情形指合併營業收入額等事項｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400002&flno=5
- 「所以這裡只看得到整家公司的營收」｜softened（改為「申報的是整家公司的營收，不要求按產品拆分，通常看不出」；現行頁面沒看到；diagram-1 第二框同步改）｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400002&flno=5
- 年報準則第 18 條：所營業務主要內容及營業比重、主要產品重要用途、最近二年度任一年度占銷貨總額 10% 以上客戶與比例、契約約定不得揭露得以代號｜ok（法規名稱補全為「公開發行公司年報應行記載事項準則」）｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400022&flno=18
- 財報編製準則第 15 條：附註揭露部門財務資訊（產品或勞務類型、收入、損益）｜ok（現行有效版第 26 款、117 會計年度起新版第 27 款，內容相同；名稱補全為「證券發行人財務報告編製準則」）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400050 、https://law.moj.gov.tw/LawClass/LawOldVer.aspx?pcode=G0400050&lnndate=20250319&lser=001
- 第 22 條：個體財務報告得免編部門資訊，要看合併財報｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400050
- 年報準則沒有規定產品怎麼分類｜ok（第 18 條只要求列營業比重，未規定分類）｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400022&flno=18
- 重大訊息處理程序第 3 條：詳述事實、原因、財務業務影響、估計影響金額與因應措施；對外說明一致，不得偏頗、誇耀、類似廣告宣傳、提供尚未確定的消息｜ok（法規名稱補全）｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007111
- 第 6 條第一項第二款：媒體報導足以影響行情或與事實不符，應立即輸入說明，至遲不得逾發現後 2 小時｜ok｜同上
- 第 4 條第一項第十二款：法說會日期、時間、地點與相關資訊，及以其他方式發布尚未輸入觀測站的財務業務資訊為重大訊息｜ok｜同上
- 處理程序版本 115.09.30｜ok｜同上
- 證交所每日收盤後分析上市有價證券交易，異常時公告交易資訊（第 4 條）｜ok｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007225
- 連續或一段期間內多次被公布 → 處置有價證券；人工管制撮合；向投資人收取全部價金或證券（第 6 條）｜ok｜同上
- 作業要點版本 115.08.03｜ok｜同上
- 證交所網站「公布注意有價證券」「公布處置有價證券」兩頁｜ok（頁面標題相符）｜https://www.twse.com.tw/zh/announcement/notice.html 、https://www.twse.com.tw/zh/announcement/punish.html
- 證交法第 155 條第一項第六款禁止散布流言或不實資料；第二項證券商營業處所買賣準用｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=G0400001&flno=155
- 刑事局假投資手法：假借股票等名義拉進投資群組、先小額獲利、引誘投入大量資金、找理由拒絕出金｜ok｜https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e
- 清單項標題「群組與私訊」｜fixed（來源沒有「私訊」，寫的是透過網路社群或交友軟體認識被害人；改「投資群組」並補接觸管道）｜同上
- 站內連結文字「營收、部門、本益比這些詞」｜fixed（目標文章 finance-glossary-50-terms 沒有「部門」；改「營業收入、本益比這些財經名詞」）｜repo apps/api/app/guides/content/finance-glossary-50-terms.json
- 站內連結只指向 finance-glossary-50-terms、online-banking-security、personal-finance-first-steps（皆在允許清單）｜ok｜指派
- online-banking-security 有假投資群組與帳戶盜用內容；personal-finance-first-steps 有收支與緊急預備金｜ok｜repo content JSON
- diagram-1 數字 50%、10 日、10%、2 小時、2026 都在正文｜ok｜intake_check
- diagram-1 第二框「只看得到整家公司的營收變化」｜softened（改「申報的是整家公司營收／不按產品拆分」，desc 同步）｜G0400002 第 5 條
- hero.svg：只有「AI」兩字、無數字、無 logo、無上升長條或曲線；alt 與畫面相符｜ok｜渲染 PNG 目視
- 免責 callout：「不是投資建議」原字、中括號「費用、稅負與交易規則」、日期 2026-10-05、為最後一個區塊｜ok｜life-finance-series-brief §5
- 全文未點名任何公司、股票代號、ETF 或指數商品｜ok｜全文檢索
- 17 筆 sources 全部 HTTP 200 且有實際內容、checked_on 2026-10-05｜ok｜見上
