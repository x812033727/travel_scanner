# ai-interview-preparation 查核第二輪（2026-10-05）

第二輪查核者（非撰稿者、非第一輪查核者）。全部來源今天重新以 curl -sSL 抓取（User-Agent：Mokaair-editorial/1.0），原始檔與文字檔在 `_tools/ai-interview-preparation/v2/`，讀前去掉 HTML 註解、script、style（`_tools/ai-interview-preparation/html2text.py`）。改稿腳本：`v2/edit_r2.py`、`v2/edit_r2b.py`。

主張｜判定｜來源網址｜讀法

## A1. 第一輪改過或無法確認的事實

- 公司法第 393 條第 2、3 項：名稱、所營事業、所在地、董監姓名及持股、經理人、資本額等第 1 至 9 款，任何人得至主管機關資訊網站查閱；條文不限未上市櫃公司，第一輪的「沒有上市櫃的公司也一樣」正確｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080001｜curl 200，修正日期 114/12/26；第 5 條中央主管機關為經濟部，支撐正文「經濟部的」
- Gemini Live「同一個對話可以切回文字模式」｜**fixed**｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant ；https://support.google.com/gemini/answer/15274899?hl=zh-Hant&co=GENIE.Platform%3DiOS｜curl 200 兩頁逐段比對：「切換 Live 和非 Live 對話模式」整節只在 Android 版說明頁；iPhone／iPad 版只有「結束對話會製作轉錄稿」與「繼續先前的 Live 對話」。第一輪的句子把 Android 才有寫的功能套到三種裝置，改成「結束對話後可以查看轉錄稿，Android 版還能在同一個對話直接切換成文字模式」
- 「被問到婚姻或懷孕計畫這類問題，可以表明不提供；認為因此受到差別待遇，可以申訴」｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001 ；https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090006｜第 5 條第 1 項（婚姻為歧視事由）、第 2 項第 2 款（不得違反意思要求非屬就業所需隱私資料）、施行細則第 1 條之 1（懷孕計畫列為個人生活資訊）、第 6 條第 4 項第 1 款（地方主管機關認定就業歧視）；句子沒有說「違法」，最後一段保留「是否違法由主管機關認定」，維持第一輪的軟化寫法
- 移除 findbiz.nat.gov.tw｜ok（同意移除）｜https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do｜今天 curl 仍回 HTTP 403 Cloudflare「Sorry, you have been blocked」；Wayback CDX 連線被重設
- 「商工登記公示資料查詢服務」名稱｜ok｜https://gcis.nat.gov.tw/mainNew/index.jsp｜curl 200，頁面有以此為名、連到 findbiz 網址的連結；入口網屬經濟部商業發展署
- 公開資訊觀測站涵蓋上市、上櫃、興櫃與公開發行公司，可查公司基本資料、營收、重大訊息、財務報告｜ok｜https://shl.twse.com.tw/page/library/tips/2.html｜curl 今天仍回 Empty reply；WebFetch 讀到全文：「揭露上市公司、上櫃公司、興櫃公司及公開發行公司公開資訊之網站」，列出公司基本資料、營收資訊、財務報告、重大訊息，網站擁有者臺灣證券交易所。「每月」營收由證券交易法第 36 條第 1 項第 3 款「每月十日以前，公告並申報上月份營運情形」支撐
- 六都勞工主管單位名稱｜ok｜https://eeweb.mol.gov.tw/front/202 ；https://eeweb.mol.gov.tw/front/476｜curl 200 兩頁：臺北市、桃園市勞動局，新北、臺中、臺南、高雄勞工局；其他縣市有勞工處、社會處、勞工及青年發展處等，正文「其他縣市另有勞工處、社會處等名稱」成立
- 正文字數｜changed｜—｜第一輪 2,606；本輪改稿後 2,640（多了個資提醒、日期與 Claude 的區分，刪了兩處重複），仍在 1,800–3,000 內，比 2,600 目標多 40 字，理由是補的都是事實精確度或使用者保護

## A2. 抽查（verify-1.md 的條列，從第 2 行起每三行一條）

- 描述：公司資料回公開資訊觀測站與商工登記核對｜ok｜同上兩頁
- summary：讓 AI 扮演面試官、一次問一題並給回饋｜ok｜https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03｜curl 200；Prompt Pack #6「Ask me 3 interview questions, one at a time. After each answer, give me one thing I did well and two ways to make it stronger.」
- OpenAI Academy 教材給就業輔導員（employment specialists），Goodwill Keystone 與 OpenAI Academy 合製｜ok｜同上｜December 3, 2025，Last updated on May 29, 2026
- 雇主名稱、地點、薪資、法律或福利資訊要查證｜ok，但正文已刪（與下一句「數字、人名、產品名逐一回原始資料核對」重複），source 標題改寫｜同上
- Gemini Live 網頁版目前不能用｜ok｜兩頁 Gemini 說明｜Android「Gemini Live 現階段並不支援 Gemini 網頁應用程式」；iOS「目前無法在 Gemini 網頁應用程式使用 Gemini Live」。正文加上「到 2026 年 10 月」
- 公開資訊觀測站｜ok｜見 A1
- 商工登記公示資料查詢服務名稱｜ok｜見 A1
- Anthropic：申請文件先自己寫初稿再用 AI 潤飾｜**fixed（精確度）**｜https://www.anthropic.com/candidate-ai-guidance｜curl 200，Last updated Jul 10, 2025。原文是「first draft yourself, then use Claude to refine it」；帶回家測驗是「Complete these without Claude」，只有即時面試是「no AI assistance」。正文原寫成三處都是「AI」，改為 Claude／任何 AI 分開寫，並加「2025 年 7 月更新」
- 圖解與 callout：沒寫明就先問招募窗口、答覆前不要用｜ok（建議，非事實主張）｜—
- 施行細則第 1 條之 1 三類隱私資料與必要範圍｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090006｜修正日期 113/06/18，逐字比對
- 表：第 5 條第 1 項 30 萬至 150 萬元並公布名稱｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001｜第 65 條第 1、3 項；修正日期 114/01/20
- 表：第 2 項第 2、3、6 款 6 萬至 30 萬元｜ok｜同上｜第 67 條第 1 項
- 六都勞動局／勞工局｜ok｜見 A1
- 勞工諮詢申訴專線 1955｜ok｜https://www.mol.gov.tw/｜curl 200，頁尾「勞工諮詢申訴專線：1955」
- hero：無數字、一行字、alt 與畫面一致｜ok｜—｜重新渲染 hero.png 並打開看：大樓加橘色放大鏡、筆電螢幕上青綠問號框與藍框回答框、綠色盾牌白勾，字「面試前，先和 AI 練一輪」，無 logo、無人臉、無上升長條
- 新增 front/202 來源｜ok｜見 A1

順帶複核（不在抽樣但改稿時碰到）：就業服務法第 5、6、75 條，性別平等工作法第 7、34、38 條之 1（修正日期 112/08/16），證券交易法第 36 條（113/08/07），就業平等網申訴流程（front/703），勞動部違反勞動法令事業單位查詢系統，全部 curl 200 與正文一致。

## B. 法遵審查（辦公效率批）

- 實測：全文沒有實測結果、分數或「實測」字樣｜ok
- AI 工具功能只照官方說明並附日期：Gemini Live 的裝置、網頁版不支援、轉錄稿與切換模式依 Google 說明頁，正文加「到 2026 年 10 月」；Android 才有的功能標明 Android｜fixed
- 公司的 AI 規則：Anthropic 例子加更新年月，區分 Claude 與任何 AI；正文明說能否使用由應徵公司決定，沒寫就問、答覆前不用，callout 說明把 AI 即時答案當成自己的回答的後果，沒有任何規避偵測或作弊的建議｜ok（精確度 fixed）
- 法規：就業服務法第 5、6、65、67、75 條，施行細則第 1 條之 1，性別平等工作法第 7、34、38 條之 1，公司法第 393 條，證券交易法第 36 條，條號、項款、罰鍰區間全部與全國法規資料庫今天的條文一致｜ok
- 提示詞以「範本」呈現（code 區塊 label「模擬面試提示詞範本」），沒有宣稱效果｜ok
- 每個 AI 產出旁都要有人工確認：模擬回饋（自己改）、空窗期說法（改成自己的話）、公司整理（逐一回原始資料核對）、反問（建立在讀過的資料上）都有；申訴經過的時間序原本只有「整理成事實」，補上「再逐條對照留存的資料」｜fixed
- 個資：模擬面試要求貼履歷卻沒提醒去識別，依 OpenAI Academy「Protect privacy – no SSNs, bank info, full addresses」補一句「貼上履歷前，先刪掉身分證字號、銀行帳號與完整住址」｜fixed
- 工具推薦：只點名 Gemini Live，理由是官方說明把「口語練習」列為用途，沒有比較或貶抑其他工具｜ok

## C. 讀者優先與文風

- 「本文」「這篇」0 次｜ok
- 外來詞第一次出現附中文：AI（人工智慧）、OpenAI Academy 原本只註「OpenAI 的線上學習平台」，改為「AI 公司 OpenAI 的線上學習平台」；Gemini Live、Anthropic、HIV 已有；新加的 Claude 寫成「它的 AI 助理 Claude」｜fixed
- 句子裡敘述出處：「勞動部就業平等網列出的就業歧視申訴流程是」改「就業歧視申訴的處理流程是」；「OpenAI Academy 的教材也提醒……」一句與下一句重複，刪除｜fixed
- 重複：「找不到或寫得不清楚，就寫信問招募窗口」與 summary、callout 重複，刪去｜fixed
- 「最划算的用法」暗示成本比較而無依據，改「最適合的用法」｜fixed
- 導言第一段第一句回答問題；台灣用語；無驚嘆號、無贅語、無查證敘述｜ok
- 正文 2,640 字（1,800–3,000 內）｜ok

## D. 機械檢查

- `pack_cli ingest --dry-run`：dry run: nothing written（通過）
- `intake_check.py`：RESULT PASS（0 failures；body_length=2640；diagram-1 每個數字正文都有；本文/這篇 = 0）
- diagram-1.png 重新渲染並看過：三欄對齊、無壓線、無溢出、文字與正文一致
