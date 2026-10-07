# thematic-etf-index-rules 查核第一輪（2026-10-05）

每一列：主張｜結果（ok / fixed / softened / removed）｜來源網址。全部來源今天重新抓取，原始檔與文字檔在 `/home/user/batch-ai-income/_tools/thematic-etf-index-rules/v1/`。讀法：curl -sSL（批次 UA）、HTTP 200、去註解後讀；PDF 用 pdftotext；證交所 www 站 curl 回 307 WAF 頁，改用 WebFetch（topic12.pdf 由 WebFetch 取回原始 PDF 再 pdftotext，e添富 商品頁 /zh/ETFortune/etfInfo/0050 由 WebFetch 讀欄位名稱）；投信投顧公會查詢頁用頁面預設值以 curl POST 一次只讀表頭。

## 來源可達性

- CompilationRules/8（通則 V1.1.2）｜200 PDF｜https://backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/8/tw
- CompilationRules/10（名詞解釋，檔案日期 2021/12/16）｜200 PDF｜https://backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/10/tw
- 各項指數頁｜200｜https://taiwanindex.com.tw/indexes
- 技術通知頁｜200｜https://taiwanindex.com.tw/downloads/technical_notice
- 證券投資信託基金管理辦法（修正 113-12-25）｜200｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400082
- 公開說明書應行記載事項準則（修正 113-12-25；附表四以 cookie＋referer 取得 PDF）｜200｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400091
- 受益憑證辦理申購買回作業要點（113.12.31）｜200｜https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL025323
- 證交所 ETF 專題 topic12｜curl 307 WAF；WebFetch 取回 PDF，內容可讀｜https://www.twse.com.tw/downloads/zh/ETF/topic12.pdf
- 證交所 ETF e添富｜curl 307 WAF；WebFetch 可讀首頁與商品頁｜https://www.twse.com.tw/zh/ETFortune/index
- 投信投顧公會 基礎篇｜200｜https://www.sitca.org.tw/ROC/SITCA_ETF/etf-hub-basic.html
- 投信投顧公會 觀念篇｜200｜https://www.sitca.org.tw/ROC/SITCA_ETF/etf-hub-knowledge.html
- 投信投顧公會 明細資料｜200｜https://www.sitca.org.tw/ROC/Industry/IN2002.aspx?PGMID=IN0202
- 投信投顧公會 各項費用比率｜200（POST 200）｜https://www.sitca.org.tw/ROC/Industry/IN2211.aspx?pid=IN2222_01
- 投信投顧公會 月前十大｜200（POST 200）｜https://www.sitca.org.tw/ROC/Industry/IN2629.aspx?pid=IN22601_04
- 財政部稅務入口網 6208｜200｜https://www.etax.nat.gov.tw/etwmain/tax-info/understanding/tax-q-and-a/national/securities-transaction-tax/filing/KJZD0QV
- ESMA TRV 2025-02-25｜200 PDF｜https://www.esma.europa.eu/sites/default/files/2025-02/ESMA50-43599798-9923_TRV_Article_Artificial_intelligence_in_EU_investment_funds.pdf
- 站內連結：finance-glossary-50-terms、personal-finance-first-steps（指派給的）、ai-concept-stocks-explained（同批 sibling，工作區有 pack.json）｜ok

## 主張

- 標題、description：主題型 ETF 持股由指數編製規則決定；費用、追蹤差距、持股在公開說明書、投信投顧公會、證交所查｜ok｜https://www.sitca.org.tw/ROC/SITCA_ETF/etf-hub-basic.html
- ETF＝指數股票型基金（Exchange Traded Fund）｜ok｜https://www.sitca.org.tw/ROC/SITCA_ETF/etf-hub-basic.html
- 編製規則寫明成分篩選標準與流程、權重分配方式、定期審核與不定期調整｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/8/tw
- 「採樣範圍」是從指數母體再描述的成分篩選範圍；英文 Index Methodology｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/10/tw
- 用交易所產業分類「半導體業」劃範圍、再依市值取前幾名｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/361/tw ；https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/447/tw
- 依產業價值鏈上中下游細分、只收其中幾段｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/587/tw
- 第三方細產業分類挑 AI 產業鏈＋營收占比門檻；合格檔數不足時門檻逐次調降｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/801/tw
- 疊加成交金額、ROE、股利紀錄條件｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/801/tw
- 「最後用殖利率或股價動能排序」→ 規則是股息殖利率、動能、企業價值成長三項加權的多因子綜合分數；改為「殖利率、股價動能等因子的綜合分數」（摘要、清單、警示 callout、圖解同步）｜fixed｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/801/tw
- ESMA：7 個 AI 指數、198 家、16 家在至少 5 個指數、115 家（58%）只在 1 個｜ok｜ESMA PDF p.10–11
- 「原因在於……各家判斷本來就不同」→ ESMA 原文是 may, to some extent, reflect；改為「ESMA 認為這多少反映……」｜fixed｜ESMA PDF p.11
- 權重方式：市值加權、等權重、市值分群固定權重、營收動能調整；單一成分股與前五大上限｜ok｜IndexFiles/361、447、756、801
- 管理辦法第 10 條第 1 項第 8 款：任一上市櫃公司股票＋公司債＋金融債券合計不超過淨資產 10%｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400082
- 第 35 條（第 41 條準用 ETF）：可不受 10% 限制，但超過 10% 者不得超過該成分證券占指數權重；另有例外｜ok（正文已寫「原則上」）｜同上
- 成分股在加權指數權重超過上限時以該權重為上限｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/447/tw
- 「指數通則也保留……調整上限參數的權利」→ 這是一家指數公司的通則 3.4.4，改為「也有指數公司在通則裡保留……」｜fixed｜https://backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/8/tw
- ESMA：AI 指數前十大平均 37%、最大成分股不超過 4–5%、對照市值加權 IT 指數前十大 78%｜ok｜ESMA PDF p.10 Table 2
- 國內幾份半導體與 AI 規則有的每季、有的每半年審核（361、447、756 每年 4 次；587、801 每年 2 次）｜ok｜IndexFiles/361、447、587、756、801
- 緩衝區、替換檔數限制、調整過渡期｜ok｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/756/tw ；IndexFiles/801
- 「國內指數公司在技術通知頁公布……日程表按月公布」→ 國內不只一家指數編製者，改為「以國內一家指數公司為例」；技術通知頁上的日程表是按審核月份各一份（例：2026/09/30 公布「2026 年 11 月指數定期審核日程表」），改為「依審核月份分別公布」（表格同步）｜fixed｜https://taiwanindex.com.tw/downloads/technical_notice
- 重大修改於審核資料截止日 10 個交易日前公告 → 原文是「最近一次」審核資料截止日，重大變更＝影響成分篩選或加權方式（第二碼）、維護方式或計算公式（第一碼）；改為「影響選股、加權或計算公式」「最近一次審核資料截止日」，保留「原則上」（有縮短公告期例外）｜fixed｜https://backend.taiwanindex.com.tw/api/downloadFile/CompilationRules/8/tw
- 回溯測試；回溯結果與實際未必一致；指數報酬未反映買賣費用與稅負｜ok（改寫為同一家公司的通則）｜同上 3.1.2
- 內扣費用從基金資產扣、反映在淨值｜ok｜https://www.twse.com.tw/downloads/zh/ETF/topic12.pdf
- 費用評估表列經理費、保管費年費率；信託契約其他費用另予列明｜ok｜準則第 18 條附表四
- 「指數授權費寫在指數授權契約的重要內容裡」→ 管理辦法第 34 條是信託契約應載明指數授權契約重要內容（含指數授權費）；改寫成信託契約的載明事項｜fixed｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400082
- 「公開說明書另列最近五年度費用率」→ 準則第 20 條只適用追加募集與開放式基金按季更新的公開說明書；改為「按季更新的公開說明書」，表格更新頻率由「隨公開說明書修訂」改「公開說明書按季更新」｜fixed｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400091
- 費用率算法＝應負擔費用總金額／平均淨資產價值｜ok｜同上第 20 條第 3 款
- 各項費用比率：月、季、年；交易直接成本（手續費、交易稅，減申購買回交易費）與會計帳列費用（經理費、保管費、保證費、其他）｜ok｜https://www.sitca.org.tw/ROC/Industry/IN2211.aspx?pid=IN2222_01
- 各項費用比率、月前十大：每月第 10 個營業日更新｜ok｜https://www.sitca.org.tw/ROC/Industry/IN2002.aspx?PGMID=IN0202
- 追蹤差距定義、正值代表 ETF 報酬較高｜ok｜https://www.sitca.org.tw/ROC/SITCA_ETF/etf-hub-knowledge.html
- 追蹤誤差＝追蹤差距的標準差；成因含費用、換股成本、複製方式、匯率、配息｜ok｜https://www.twse.com.tw/downloads/zh/ETF/topic12.pdf
- 公開說明書要載明基金與指數表現差異比較的定義與公式｜ok｜準則第 13 條
- 投信 ETF 專區列追蹤差距／追蹤誤差｜ok｜https://www.sitca.org.tw/ROC/SITCA_ETF/etf-hub-basic.html Q7；觀念篇 Q2
- ETF 每日公告持股；投信每天公告申購買回清單（PCF）｜ok｜etf-hub-basic.html Q3、Q6；https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL025323
- 月前十大列出占基金淨資產價值比例｜ok｜https://www.sitca.org.tw/ROC/Industry/IN2629.aspx?pid=IN22601_04
- e添富 商品頁有「淨值與折溢價」「標的指數」「公開說明書」；每天的折溢價可在證交所查｜ok｜https://www.twse.com.tw/zh/ETFortune/index ；etf-hub-knowledge.html Q1
- 表格「追蹤差距更新頻率：以投信公告為準」｜ok（無共同官方頻率）｜etf-hub-knowledge.html Q2
- ETF 名稱必須顯示追蹤的指數（第 33 條，第 41 條準用）｜ok｜G0400082
- 「指數單張（一頁的指數簡介）」→ 抽查的指數單張是 2 頁 PDF；改為「指數的簡介摘要」；「僅供參考」聲明 ok｜fixed｜https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/544/tw
- 名稱有「主動」的 ETF 不追蹤指數、依經理公司投資策略操作｜ok｜G0400082 第 41-1 條；G0400091 第 6 條第 10 款
- 海外指數 ETF 時差與匯率造成折溢價；資金匯出，發行額度有上限｜ok｜etf-hub-knowledge.html Q1；etf-hub-basic.html Q5
- 券商手續費：投信投顧公會比較表列千分之 1.425（買進賣出都有）｜ok（只以公會比較表的寫法引用）｜etf-hub-basic.html Q3
- 證券交易稅千分之 1，賣出課徵 → 公會表註明債券 ETF 另有免徵規定，改為「賣出股票型 ETF」｜softened（精確化，數字不變）｜https://www.etax.nat.gov.tw/etwmain/tax-info/understanding/tax-q-and-a/national/securities-transaction-tax/filing/KJZD0QV
- 免責 callout：「不是投資建議」原字、「費用、稅負與交易規則」、2026-10-05｜ok｜docs/life-finance-series-brief.md §5
- 表格 caption「資料時間為 2026 年 10 月」｜ok
- 圖解數字：10%（正文有）、2026（表格 caption 有）｜ok；圖解標籤「殖利率或動能排序」改「殖利率、動能等因子排序」，desc 同步｜fixed
- hero：無文字、無數字；alt 與渲染圖一致（文件、漏斗、三乘三九個同大小色塊）｜ok
- 全文未點名任何 ETF、指數商品或發行投信｜ok
