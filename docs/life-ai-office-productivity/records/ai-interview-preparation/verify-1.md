# ai-interview-preparation 查核第一輪（2026-10-05）

主張｜判定｜來源網址

## 標題、描述、summary

- 標題「用 AI 準備面試：模擬問答、公司研究與不能做的事」與指派一致｜ok｜docs/life-ai-office-productivity/README.md
- 描述：公司資料回公開資訊觀測站與商工登記核對｜ok｜https://shl.twse.com.tw/page/library/tips/2.html ；https://gcis.nat.gov.tw/mainNew/index.jsp
- 描述：面試或測驗進行中能不能用 AI 以應徵公司規則為準｜ok｜https://www.anthropic.com/candidate-ai-guidance
- 描述：向縣市政府勞工主管單位申訴、撥 1955 諮詢｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001 （第 6 條）；https://www.mol.gov.tw/
- summary：讓 AI 扮演面試官、一次問一題並給回饋｜ok｜https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03
- summary：上市櫃看公開資訊觀測站，其他公司查商工登記公示資料｜ok｜https://shl.twse.com.tw/page/library/tips/2.html ；https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080001
- summary：就業服務法禁止以婚姻、年齡、性別等理由歧視求職人，不得違反意思要求非屬就業所需的隱私資料｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001

## 模擬面試

- OpenAI Academy 教材是給就業輔導員（employment specialists，與 Goodwill Keystone 合製）｜ok｜https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03
- 扮演友善的用人主管、一次問一題、共三題、每題一個優點與兩個改進（Prompt Pack #6）｜ok｜同上
- 空窗期：寫下原因與現在準備好做什麼，整理成口頭說法（Prompt #5）｜ok｜同上
- 雇主名稱、地點、薪資、法律或福利資訊要查證｜ok｜同上
- Gemini Live 可在 Android 手機或平板、iPhone、iPad 的 Gemini 行動應用程式使用｜ok｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant ；https://support.google.com/gemini/answer/15274899?hl=zh-Hant&co=GENIE.Platform%3DiOS
- Gemini Live 用途包括口語練習｜ok｜同上
- Gemini Live 網頁版目前不能用｜ok｜同上
- 結束 Live 對話會產生轉錄稿；原寫「貼回文字對話」，說明頁寫同一對話可切回文字模式｜fixed｜https://support.google.com/gemini/answer/15274899?hl=zh-Hant
- 錄下他人聲音前要徵得同意（Gemini Live 使用須知）｜ok｜同上

## 公司研究

- 公開資訊觀測站涵蓋上市、上櫃、興櫃與公開發行公司，可查公司基本資料、每月營收、重大訊息、財務報告｜ok（curl 回 Empty reply，WebFetch 讀到全文）｜https://shl.twse.com.tw/page/library/tips/2.html
- 證券交易法第 36 條：定期公告財務報告、每月 10 日以前公告上月營運情形、編製年報｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400001
- 公司法第 393 條：名稱、所營事業、所在地、董監、經理人、資本額，任何人得至主管機關資訊網站查閱；原句寫成只適用沒有上市櫃的公司｜fixed｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080001
- 入口名稱「經濟部商工登記公示資料查詢服務」｜ok（findbiz 本身 403；由商業發展署入口網的連結名稱確認）｜https://gcis.nat.gov.tw/mainNew/index.jsp
- 勞動部違反勞動法令事業單位（雇主）查詢系統可查公布的處分｜ok｜https://announcement.mol.gov.tw/

## 面試當下

- Anthropic：鼓勵用 AI 研究公司、練習回答、準備提問｜ok｜https://www.anthropic.com/candidate-ai-guidance
- Anthropic：申請文件先自己寫初稿再用 AI 潤飾｜ok｜同上
- Anthropic：帶回家測驗與即時面試不用 AI，除非公司另外說明｜ok｜同上
- Anthropic：需要 accommodations 及早告知 recruiter（正文：特殊安排面試前先提出）｜ok｜同上
- 圖解與 callout：沒寫明就先問招募窗口、答覆前不要用（建議，非事實主張）｜ok｜—

## 就業服務法與性別平等工作法

- 就業服務法第 5 條第 1 項的十八種歧視事由，逐字比對｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001
- 第 5 條第 2 項第 1、2、3、6 款（不實廣告；留置證件或要求隱私資料；扣留財物或保證金；經常性薪資未達新臺幣 4 萬元未揭示薪資範圍）｜ok｜同上
- 施行細則第 1 條之 1 隱私資料三類與各項目、不得逾越特定目的必要範圍｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090006
- 「被問到婚姻或懷孕計畫可以婉拒回答」無主管機關原文｜softened｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001 ；https://eeweb.mol.gov.tw/front/203
- 性別平等工作法第 7 條：招募、甄試不得因性別或性傾向差別待遇，但工作性質僅適合特定性別者除外｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0030014
- 表：第 5 條第 1 項 30 萬至 150 萬元並公布名稱（第 65 條第 1、3 項）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001
- 表：性平法第 7 條 30 萬至 150 萬元並公布名稱（第 38 條之 1 第 1 項、末項）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0030014
- 表：第 5 條第 2 項第 1 款 30 萬至 150 萬元（第 65 條）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001
- 表：第 2 項第 2、3、6 款 6 萬至 30 萬元（第 67 條）｜ok｜同上
- 法規修正日期：就業服務法 114/01/20、施行細則 113/06/18、性平法 112/08/16、公司法 114/12/26、證交法 113/08/07｜ok｜各法規資料庫頁

## 申訴管道

- 就業歧視認定由直轄市、縣（市）主管機關掌理（第 6 條第 4 項第 1 款）；罰鍰由直轄市及縣（市）主管機關處罰（第 75 條）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0090001
- 臺北市、桃園市為勞動局；新北、臺中、臺南、高雄為勞工局；其他有勞工處、社會處等｜ok（新增 front/202 佐證）｜https://eeweb.mol.gov.tw/front/202 ；https://eeweb.mol.gov.tw/front/476
- 性平法第 34 條：求職者得向地方主管機關申訴｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0030014
- 就業歧視申訴流程：受理、訪談與實地查訪、似有歧視提評議委員會、成立做成行政處分｜ok｜https://eeweb.mol.gov.tw/front/703
- 勞工諮詢申訴專線 1955｜ok｜https://www.mol.gov.tw/

## 圖上的數字與文字

- diagram-1：1955（正文有）、2026（表格 caption 有）｜ok｜https://www.mol.gov.tw/
- diagram-1：一優點兩改進、公開資訊觀測站與商工登記、勞動局／勞工局／勞工處、權益受損三例，與正文一致｜ok｜同上各條
- hero：無數字，一行字 ≥ 40px，alt 與畫面一致（看過渲染圖）｜ok｜—

## sources 與站內連結

- 16 筆 sources 全部 curl 200 有正文（shl.twse.com.tw 今天以 WebFetch 讀到）｜ok｜—
- findbiz.nat.gov.tw（403）與 mops.twse.com.tw（安全阻擋殼頁）不能當來源｜removed｜https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do ；https://mops.twse.com.tw/mops/#/web/home
- 新增勞動部就業平等網縣市主管機關連絡資訊｜fixed｜https://eeweb.mol.gov.tw/front/202
- 站內連結只有 chatgpt-for-resume-cover-letter、ai-tools-choose-by-task、ai-hallucination-fact-check，皆在允許清單，連結文字與現有標題一致｜ok｜—
- dry-run 通過、intake_check PASS，正文 2,606 字｜ok｜—
