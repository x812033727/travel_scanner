# ai-interview-preparation 查證記錄

查證日一律 2026-10-05。讀法：curl -sSL（User-Agent 為 Mokaair-editorial/1.0），確認 HTTP 200 且不是殼頁後，去掉 HTML 註解、script、style 再讀正文（`_tools/ai-interview-preparation/html2text.py`）；PDF 用 pdftotext -layout。原始檔留在 `/home/user/batch-ai-office/_tools/ai-interview-preparation/raw/`。Wayback Machine 在這個環境連不上（CDX 與 WebFetch 都被斷線或拒絕），所以 403 的官方站改用同一機關的其他官方頁交叉確認，方式逐條寫在下面。

主張｜來源網址｜查證日｜讀法

## 就業服務法（全國法規資料庫，修正日期民國 114 年 01 月 20 日）

- 第 5 條第 1 項：雇主對求職人或所僱用員工，不得以種族、階級、語言、思想、宗教、黨派、籍貫、出生地、性別、性傾向、年齡、婚姻、容貌、五官、身心障礙、星座、血型或以往工會會員身分為由歧視｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001｜2026-10-05｜curl 200（第一次回 805 bytes 錯誤頁，重試取得 107,168 bytes 全文頁），讀條文
- 第 5 條第 2 項：雇主招募或僱用員工不得 一、不實廣告或揭示；二、違反意思留置國民身分證、工作憑證或其他證明文件，或要求提供非屬就業所需之隱私資料；三、扣留財物或收取保證金；四、指派從事違背公序良俗之工作；五、聘僱外國人提供不實資料；六、提供職缺之經常性薪資未達新臺幣四萬元而未公開揭示或告知其薪資範圍｜同上｜2026-10-05｜同上（正文清單只列第 1、2、3、6 款）
- 第 6 條：主管機關中央為勞動部、直轄市為直轄市政府、縣（市）為縣（市）政府；第 4 項第 1 款直轄市、縣（市）主管機關掌理就業歧視之認定｜同上｜2026-10-05｜同上
- 第 65 條：違反第 5 條第 1 項、第 2 項第 1 款、第 4 款、第 5 款等，處新臺幣三十萬元以上一百五十萬元以下罰鍰；違反第 5 條第 1 項經處罰鍰者，應公布其姓名或名稱、負責人姓名｜同上｜2026-10-05｜同上
- 第 67 條：違反第 5 條第 2 項第 2 款、第 3 款、第 6 款等，處新臺幣六萬元以上三十萬元以下罰鍰｜同上｜2026-10-05｜同上
- 第 75 條：本法所定罰鍰，由直轄市及縣（市）主管機關處罰之｜同上｜2026-10-05｜同上

## 就業服務法施行細則（全國法規資料庫，修正日期民國 113 年 06 月 18 日）

- 第 1-1 條：隱私資料包括 一、生理資訊：基因檢測、藥物測試、醫療測試、HIV 檢測、智力測驗或指紋等；二、心理資訊：心理測驗、誠實測試或測謊等；三、個人生活資訊：信用紀錄、犯罪紀錄、懷孕計畫或背景調查等；雇主要求提供隱私資料，應尊重當事人權益，不得逾越基於經濟上需求或維護公共利益等特定目的之必要範圍，並應與目的間具有正當合理之關聯｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090006｜2026-10-05｜curl 200 讀條文（pcode 由 N0090003 起逐一試開，N0090006 的法規名稱為就業服務法施行細則）

## 性別平等工作法（全國法規資料庫，修正日期民國 112 年 08 月 16 日）

- 第 7 條：雇主對求職者或受僱者之招募、甄試、進用、分發、配置、考績或陞遷等，不得因性別或性傾向而有差別待遇；但工作性質僅適合特定性別者，不在此限｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0030014｜2026-10-05｜curl 200 讀條文
- 第 34 條第 1 項：受僱者或求職者發現雇主違反第七條至第十一條等規定時，得向地方主管機關提起申訴｜同上｜2026-10-05｜同上
- 第 38-1 條第 1 項：雇主違反第七條至第十條、第十一條第一項、第二項，處新臺幣三十萬元以上一百五十萬元以下罰鍰；同條末項：應公布其名稱、負責人姓名、處分期日、違反條文及罰鍰金額｜同上｜2026-10-05｜同上

## 公司研究的公開資料

- 公司法第 393 條第 2 項、第 3 項：公司名稱、所營事業、所在地、執行業務或代表公司之股東、董事監察人姓名及持股、經理人姓名、資本總額或實收資本額等，主管機關應予公開，第一款至第九款任何人得至主管機關之資訊網站查閱（公司法修正日期民國 114 年 12 月 26 日）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080001｜2026-10-05｜curl 200 讀條文
- 證券交易法第 36 條：已發行有價證券之公司，每會計年度終了後三個月內公告並申報年度財務報告，第一、二、三季終了後四十五日內公告財務報告，每月十日以前公告並申報上月份營運情形；發生對股東權益或證券價格有重大影響之事項，應於事實發生之日起二日內公告並申報；應編製年報（證券交易法修正日期民國 113 年 08 月 07 日）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400001｜2026-10-05｜curl 200 讀條文（正文只用「定期公告財務報告、每月 10 日以前公告上月營運情形、編製年報」）
- 公開資訊觀測站是揭露上市公司、上櫃公司、興櫃公司及公開發行公司公開資訊之網站；可查公司基本資料（產業類別、主要經營業務、實收資本額）、每月營收、重大訊息、財務報告｜https://shl.twse.com.tw/page/library/tips/2.html｜2026-10-05｜curl 200，臺灣證券交易所自己的投資人教育網站（宅在家學習網）
- 公開資訊觀測站本身｜https://mops.twse.com.tw/mops/#/web/home｜2026-10-05｜curl 對 mops.twse.com.tw 回「因為安全性考量，您所執行的頁面無法呈現」的阻擋頁（HTTP 200 但是殼頁，不當來源讀）；WebFetch 取得頁面標題「公開資訊觀測站」，內容是單頁應用程式讀不到選單。正文的功能描述全部取自上一行的證交所頁
- 公開資訊觀測站由證期局指導、證交所與櫃買中心等共同建立，91 年 8 月 1 日建立、現行版本 99 年 7 月上線｜https://dsp.tpex.org.tw/storage/education_event/113/5.%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E5%84%AA%E5%8C%96%E5%85%AC%E9%96%8B%E8%B3%87%E8%A8%8A%E8%A7%80%E6%B8%AC%E7%AB%99%E8%AA%AA%E6%98%8E.pdf｜2026-10-05｜curl 200 下載 PDF，pdftotext 讀前言（最後一版正文刪掉建置單位那句，此來源未放進 sources）
- 商工登記公示資料查詢服務（經濟部）｜https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do｜2026-10-05｜curl 與 WebFetch 都回 HTTP 403（安全阻擋頁）；改讀經濟部商業發展署的全國商工行政服務入口網 https://gcis.nat.gov.tw/mainNew/index.jsp（curl 200，頁尾為商業發展署署本部地址），該頁以「商工登記公示資料查詢服務」為名連到上面這個網址。正文只寫它是查登記資料的入口，可查哪些項目改以公司法第 393 條為準
- 勞動部「違反勞動法令事業單位（雇主）查詢系統」：可依縣市、事業單位名稱（負責人）、處分日期、法規名稱查詢；快速連結含勞動基準法／最低工資法／性別平等工作法、職業安全衛生法、就業服務法等｜https://announcement.mol.gov.tw/｜2026-10-05｜curl 200 讀首頁

## AI 工具與應徵公司的 AI 規則

- OpenAI Academy「Helping Job Seekers with ChatGPT」（Goodwill Keystone 與 OpenAI Academy 為就業輔導員製作；December 3, 2025，Last updated on May 29, 2026）：10 分鐘模擬面試流程與 Prompt Pack #6「Act as a friendly hiring manager… Ask me 3 interview questions, one at a time. After each answer, give me one thing I did well and two ways to make it stronger.」；Prompt #5 空窗期說法（原因、離開多久、現在準備好做什麼，寫成 2–3 句書面說法與一段面試口頭稿）；「Verify important facts – especially employer names, locations, pay, or legal/benefits info」｜https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03｜2026-10-05｜curl 200 讀正文
- Anthropic「How to collaborate with Claude during our hiring process」（Last updated Jul 10, 2025）：申請時先自己寫初稿再用 Claude 潤飾；take-home assessments 除非另行說明不得使用；準備面試時鼓勵用來研究公司、練習回答、準備提問；live interviews「no AI assistance unless we indicate otherwise」；需要 accommodations 及早告訴 recruiter｜https://www.anthropic.com/candidate-ai-guidance｜2026-10-05｜curl 200 讀正文。正文把它當「有公司把規則寫在招募頁」的一個例子，不推論到其他公司
- Gemini Live（Android 版說明頁）：用途含「口語練習：以更自然口語的方式排練，為重要時刻做好準備」；需求為 Android 手機或平板電腦與 Gemini 行動應用程式；「Gemini Live 現階段並不支援 Gemini 網頁應用程式」；結束對話會關閉工作階段並製作轉錄稿；「請尊重他人隱私，徵得同意後才能在 Live 對話提及對方，或是錄下對方的聲音」｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant｜2026-10-05｜curl 200 讀正文
- Gemini Live（iPhone 和 iPad 版說明頁）：需求為 iPhone 或 iPad 與 Gemini 行動應用程式；目前無法在 Gemini 網頁應用程式使用｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant&co=GENIE.Platform%3DiOS｜2026-10-05｜curl 200 讀正文
- 沒有採用：Google Interview Warmup（grow.google/certificates/interview-warmup/ 今天被轉址到 grow.google/grow-your-career/articles/interview-tips/ 的一般面試技巧文章，工具頁看起來已不在）；ChatGPT 語音功能說明（help.openai.com 的 Voice 文章回 403，`.json` 讀法改址後回 404，因此正文不寫 ChatGPT 語音）

## 申訴管道

- 勞動部就業平等網「就業歧視申訴流程」：受理收件 → 訪談與實地查訪（勞資雙方及關係人）→ 初步判斷 → 似有就業歧視者提就業歧視評議委員會，未涉及者循勞資爭議程序 → 歧視成立做成行政處分及個案追蹤｜https://eeweb.mol.gov.tw/front/703｜2026-10-05｜curl 200 讀正文（頁上另附的 PDF 為圖檔，沒有文字層）
- 各地方政府申訴聯絡窗口清冊：臺北市政府勞動局、新北市政府勞工局、高雄市政府勞工局、臺中市政府勞工局、臺南市政府勞工局、桃園市政府勞動局，其餘縣市為勞工處、勞工及青年發展處、社會處、社會及勞動處等｜https://eeweb.mol.gov.tw/front/476｜2026-10-05｜curl 200 讀表格（清冊名稱是違反性別平等工作法的申訴窗口；正文用它說明各縣市勞工主管單位的名稱）
- 勞工諮詢申訴專線：1955｜https://www.mol.gov.tw/｜2026-10-05｜curl 200，勞動部全球資訊網首頁頁尾「勞工諮詢申訴專線：1955」（24 小時、免付費等描述只出現在舊新聞稿，正文不寫）

## 圖上的數字

- diagram-1.svg 只有 1955（正文兩處）與頁尾 2026（表格 caption「條文查證於 2026 年 10 月」）。
- hero.svg 沒有數字，只有一行字「面試前，先和 AI 練一輪」。

## 查核第一輪（2026-10-05，獨立查核）

全部來源重新以 curl -sSL（同一 User-Agent）抓取，原始檔在 `_tools/ai-interview-preparation/v1/`；逐條結果見 `verify-1.md`。改動：

- 公司法第 393 條｜原句「沒有上市櫃的公司，依公司法第 393 條……」讀起來像只適用未上市櫃公司；條文適用所有公司，改成「依公司法第 393 條，沒有上市櫃的公司也一樣……在主管機關的資訊網站查閱」（條文第 3 項用語）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080001｜2026-10-05
- Gemini Live 轉錄稿｜原句「貼回文字對話」改成「同一個對話可以切回文字模式」：說明頁寫「無須發起新對話，對話過程中即可無縫切換 Live（語音）和非 Live（文字）模式」｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant｜2026-10-05
- 婚姻、懷孕計畫的提問｜「可以婉拒回答，覺得因此被差別對待就可以申訴」沒有主管機關原文支持（就業平等網常見問答 https://eeweb.mol.gov.tw/front/203 也查無相關題目），改成只陳述條文推得出的「可以表明不提供；認為因此受到差別待遇，可以申訴」，「是否違法由主管機關認定」留在最後一段
- sources 移除 findbiz.nat.gov.tw（今天 curl 回 HTTP 403 Cloudflare 阻擋頁、WebFetch 也 403、Wayback CDX 連線被重設）與 mops.twse.com.tw/mops/#/web/home（curl 回「因為安全性考量，您所執行的頁面無法呈現」的 800 bytes 阻擋頁，WebFetch 只拿到標題，屬殼頁）。正文對兩個服務的描述改由已讀到全文的來源支撐：公開資訊觀測站＝臺灣證券交易所宅在家學習網（curl 今天回 Empty reply，改用 WebFetch 讀到全文：「揭露上市公司、上櫃公司、興櫃公司及公開發行公司公開資訊之網站」，可查公司基本資料、財務報告、每月營收、重大訊息）；商工登記公示資料查詢服務＝經濟部商業發展署全國商工行政服務入口網上的連結名稱（curl 200）加公司法第 393 條
- sources 新增勞動部就業平等網「縣市主管機關連絡資訊」https://eeweb.mol.gov.tw/front/202（curl 200，頁面日期 2014-11-23）：臺北市政府勞動局、新北市政府勞工局、臺中市政府勞工局、臺南市政府勞工局、高雄市政府勞工局、桃園市政府勞動局，其他縣市為社會處、勞工處、勞工及青年（發展）處等，與 front/476 的六都名稱一致；兩頁只在南投縣不同（社會及勞動局／社會及勞動處），正文沒有寫南投
- 1955｜勞動部首頁頁尾「勞工諮詢申訴專線：1955」今天仍在；就業平等網頁尾另寫「免付費電話：1955」，正文仍不寫免付費，維持原句
- 正文字數 2,586 → 2,606

## 查核第二輪（2026-10-05，換人）

全部來源重新 curl -sSL 抓取，原始檔在 `_tools/ai-interview-preparation/v2/`；逐條結果見 `verify-2.md`。改動：

- Gemini Live 切換文字模式｜「切換 Live 和非 Live 對話模式」一節只在 Android 版說明頁，iPhone／iPad 版沒有；改成「結束對話後可以查看轉錄稿，Android 版還能在同一個對話直接切換成文字模式」，並加「到 2026 年 10 月，網頁版還不能用」｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant ；https://support.google.com/gemini/answer/15274899?hl=zh-Hant&co=GENIE.Platform%3DiOS｜2026-10-05｜curl 200 兩頁逐段比對
- Anthropic 應徵者指引｜原文帶回家測驗是「without Claude」、即時面試才是「no AI assistance」、申請文件是「use Claude to refine」；正文改為分開寫，並加「2025 年 7 月更新」（頁面 Last updated Jul 10, 2025）｜https://www.anthropic.com/candidate-ai-guidance｜2026-10-05｜curl 200
- 個資提醒｜依 OpenAI Academy「Protect privacy – no SSNs, bank info, full addresses, or highly sensitive details」補「貼上履歷前，先刪掉身分證字號、銀行帳號與完整住址」｜https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03｜2026-10-05｜curl 200
- 公開資訊觀測站｜shl.twse.com.tw 今天 curl 仍 Empty reply，WebFetch 讀到全文，內容與第一輪相同
- findbiz.nat.gov.tw 今天 curl 仍 403（Cloudflare），Wayback CDX 連線被重設；gcis 入口網 curl 200 有同名連結
- 文風：刪兩處重複（OpenAI 查證提醒、招募窗口），申訴流程不再敘述出處，申訴整理加人工對照一步，「最划算」改「最適合」，OpenAI 加註「AI 公司」
- 正文字數 2,606 → 2,640；dry-run 與 intake_check 通過

## 跨篇核對（2026-10-05）

- 本批其他五篇都是辦公文件主題，沒有和面試準備直接相關、適合互連的；改在「公司研究」一節最後加連到站內已上線的 ai-financial-report-reading（公開資訊觀測站的財報與每月營收怎麼交給 AI 讀）。
- 重跑 dry-run 與 intake_check：0 FAIL，body_length=2695。
