# verify-2：ai-freelance-client-confidentiality 查核第二輪（2026-10-05）

格式：主張｜判定（ok / fixed / softened）｜來源網址｜怎麼讀到的

第二輪的讀法：除了 help.openai.com 之外，每一頁今天都用 curl -sSL 重新讀過（UA `Mokaair-editorial/1.0`，HTTP 200，先去掉 HTML 註解）。存檔在 `/home/user/batch-ai-income/_tools/ai-freelance-client-confidentiality/v2/`。help.openai.com 的情況見下面的「讀法裁定」。

## A. 第一輪改過的項目，逐條重查

1. ChatGPT 個人方案「Free、Go、Plus、Pro」｜ok｜https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt｜讀取代理，原文 "Signed-in ChatGPT Free, Go, Plus, and Pro users"（Updated: 6 days ago）
2. 臨時交談「保持臨時狀態時」不用於訓練；存成一般對話後依帳號設定｜ok｜https://help.openai.com/en/articles/8914046-temporary-chat-faq｜讀取代理（Updated: 15 days ago）。5722486 與 7730893 兩頁也各自寫了同樣的條件，三頁一致
3. 商用列加上 Edu｜ok｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance｜讀取代理："ChatGPT Business, ChatGPT Enterprise, ChatGPT Edu, or our API"
4. 中文介面用語「資料控管」「為所有人改善模型」「臨時交談」｜ok｜https://help.openai.com/zh-hant/articles/7730893-data-controls-in-chatgpt｜讀取代理
5. Claude「幫助改進我們的 AI 模型」、無痕聊天｜ok｜https://privacy.claude.com/zh-TW/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings 、https://privacy.claude.com/zh-TW/articles/10023580-is-my-data-used-for-model-training｜直接（頁面日期 2026年8月3日、2026年3月5日）
6. Anthropic API「原則上 30 天內刪除，另有例外」｜ok｜https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data｜直接（July 1, 2026；四項例外：Files API、另有約定如零資料保留、執行使用政策、法律要求）
7. Gemini「臨時對話」「保留活動記錄」；臨時對話與關閉後都保留 72 小時｜ok｜https://support.google.com/gemini/answer/13594961?hl=zh-Hant｜直接（上次更新 2026 年 9 月 24 日；原文「您的臨時對話及『保留活動記錄』設定停用期間的對話資料，會在您的帳戶中保留 72 小時」）
8. 著作權法第 12 條但書｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017｜直接（「但契約約定以出資人為著作人者，從其約定」）
9. 電子郵件1150828c 是「新聞圖片」｜ok｜https://www.tipo.gov.tw/tw/copyright/692-94326.html｜直接（第五點：新聞圖片係生成式AI產製、無受保護之人類創作內容，是否標示及如何標示「本法亦無規範，貴公司可自行決定」；發布 115-08-28）
10. 個資法 114 年 11 月 11 日修正刪除第 27 條、增訂第 20-1 條，施行日期由行政院定之｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021 、https://law.moj.gov.tw/LawClass/LawHistory.aspx?pcode=I0050021｜直接（生效狀態「最後生效日期：未定」；整編截止日民國 115 年 9 月 24 日；沿革只有總統公布令，沒有行政院定施行日的令）
11. 「獨立創作」保證「容易有爭議」｜ok（維持第一輪的保守寫法）｜https://www.tipo.gov.tw/tw/copyright/719-19274.html｜直接下載範本 DOCX（f1746517130120.docx，第 46 行「甲方保證本著作確為甲方獨立創作之作品」）。正文用「容易有爭議」而不是斷言，配合智慧財產局電子郵件1111031 的「AI 獨立創作原則上無法享有著作權」，屬合理的保守推論
12. 人工智慧基本法第 4 條改寫｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093｜直接（主詞「政府推動人工智慧之研發與應用」；第五款「人工智慧之產出應做適當資訊揭露或標記」）
13. 來源 8798634 換成 7730893｜ok｜7730893 的 Managed workspaces 段寫明 "By default, OpenAI does not use content from ChatGPT Business, Enterprise, Edu, or ChatGPT for Healthcare workspaces to train its models"
14. diagram-1.svg「臨時或無痕對話」｜ok｜重新渲染看過，見 C 節

## A. 第一輪無法確認的項目

15. **讀法裁定：help.openai.com 經 r.jina.ai 讀取。** 今天再試一次：curl 403、`.json` 後綴 403、WebFetch 403、web.archive.org CDX 連線被重設、openai.com/enterprise-privacy 與 consumer-privacy 也被擋。r.jina.ai 回 HTTP 200，內容是原頁今天的全文（含 Updated 日期、標題、FAQ），不是摘要。判定**可以接受**，理由：(a) 它即時抓的就是官方頁本身，跟 Wayback 一樣是第一方頁面的轉存，只是不經存檔；(b) 三個英文頁與兩個 zh-hant 頁互相一致，臨時交談的條件在 5722486、7730893、8914046 三頁寫法相同；(c) API 的部分另有 developers.openai.com 直接讀到（HTTP 200）佐證。sources 仍寫原始官方網址。協調者若不接受這個讀法，受影響的只有表格 ChatGPT 兩列與 callout 第一句。
16. 個資法修正的施行日期｜確認「未定」｜https://www.pdpc.gov.tw/News_Content/20/1010/｜直接（第一輪讀不到的個資會籌備處公告，今天 curl 直接讀到：「修正條文施行日期，將另由行政院依同法第56條第1項定之」）；同處的〈個人資料保護法修法問答集〉PDF Q2 說新法施行日期由行政院在個資會組織法完成立法後另行決定，施行前「仍應依現行」規定。正文「施行日期由行政院另定」正確，不改
17. 「Free、Go、Plus、Pro」出自 Data controls 頁的「已登入個人方案」清單，訓練頁只寫 "services for individuals"｜ok，兩頁合起來足以支持「個人方案（Free、Go、Plus、Pro）」的寫法
18. 實務建議（書面同意、結案刪除、三個判斷的順序）與「施行細則第 8 條沒有點名 AI 服務」｜ok，正文用建議語氣（「最直接的做法是」「可以」），沒有寫成法定義務；施行細則第 8 條全文今天重讀，確實沒有提到 AI 或特定服務

## A. 隨機三分之一（verify-1 第 2、5、8……53 條）

第 2、5、14、20、23、41、53 條已在上面重查。其餘：

19. 第 8 條：API 要主動選擇分享才會用於訓練｜ok｜https://developers.openai.com/api/docs/guides/your-data｜直接（"unless you explicitly opt in to share data with us"）
20. 第 11 條：8798634 換掉｜ok（見第 13 條）
21. 第 17 條：Claude 刪除的對話 30 天內從後端清除｜ok｜https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data｜直接
22. 第 26 條：Google 提醒不要輸入不想讓審查人員看到的機密資訊｜ok｜https://support.google.com/gemini/answer/13594961｜直接（zh-Hant 版：「如有機密資訊不想讓審查員看到……請勿輸入」）
23. 第 29 條：Workspace 未經許可不經人工審查、不用於網域外訓練｜ok｜https://knowledge.workspace.google.com/admin/generative-ai/generative-ai-in-google-workspace-privacy-hub｜直接（Last updated August 14, 2026）；保留期「依組織設定」也有支持（Flexible retention: Admins have control）
24. 第 32 條：範本保密條款與 2 倍懲罰性違約金｜ok｜https://www.tipo.gov.tw/tw/copyright/719-19274.html｜直接下載 DOCX（第 50 行；甲方是著作人，乙方是出資人）
25. 第 35 條：營業秘密法第 2 條第 3 款｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080028｜直接
26. 第 38 條：著作權法第 36 條第 3 項、第 37 條第 1 項｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017｜直接
27. 第 44 條：個資法第 4 條「視同委託機關」｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜直接
28. 第 47 條：個資法第 5 條｜ok｜同上
29. 第 50 條：個資法第 8 條告知事項｜ok｜同上

附帶重讀（不在抽樣內，但正文有用到）：Claude 商用頁的回饋保存 5 年（7996868，August 18, 2026）、個人方案頁的回饋保存 5 年（10023580）、Gemini 回饋經審查後最長保留 3 年，全部 ok。

**事實訂正：0 項。** 第一輪的訂正今天全部站得住。

## B. 法遵檢查

- 收入承諾：全文沒有任何收入、報價或金額例子，沒有「月入」「被動收入」「躺著賺」「輕鬆賺」，沒有截圖或見證。不需要「假設」標示。
- 平台抽成：本篇不談抽成與費率。
- 法律陳述：著作權法第 12、36、37 條，營業秘密法第 2 條，個資法第 2、4、5、8、27（舊）、20-1 條，施行細則第 8 條，人工智慧基本法第 4 條，以及智慧財產局兩則函釋，每一條都對應 sources 裡的法規資料庫或主管機關頁。導言第二段已寫明「個案以契約內容與專業意見為準」，沒有超出條文的法律意見。
- 推薦：三家 AI 並列，只講各自規則；「商用方案優先」指方案類型，不是推薦某一家。
- **改了一處法律陳述的範圍**：「著作權法沒有要求標示。」範圍太大（著作權法第 16 條有姓名表示權，函釋本身也談到利用他人圖片時原則上要標示著作人），改成「著作權法沒有要求標示用了 AI。」，對應函釋第五點真正回答的問題。

## C. 讀者優先與文字

- 「本文」「這篇」0 次；沒有「查證時」「官網寫」「查不到」「本批」「撰稿」；沒有驚嘆號、沒有「總結來說」；台灣用語（資料、軟體、網路、使用者）沒有問題。「查證於 2026 年 10 月」只在表格 caption，是系列慣例。「我們」2 次都在 Claude 的官方介面名稱「幫助改進我們的 AI 模型」裡，屬原文引用。
- 外文：NDA 附「保密協議」、API 附「應用程式介面」；其餘是產品或方案名（ChatGPT、Claude for Work、Workspace、Free／Go／Plus／Pro／Max、Business／Enterprise／Edu），不翻譯。
- **導言第一段改了順序**：原本先寫背景、再用「先講結論：」帶出答案，等於第一句沒有回答問題，而且「先講結論」是寫作過程的話。改成第一句直接給答案，背景句放第二句，內容不變。
- **sources 標題用語統一**：10023580 的標題還寫「無痕對話」，正文與表格已是官方 zh-TW 名稱「無痕聊天」，改成一致。
- 字數：2,592 → 2,591（paragraph／list／table／callout），在 2,200–2,600 目標內。
- 圖：hero.png 與 diagram-1.png 重新渲染並打開看過。hero：一行字 56px「客戶資料先過三關」、三個同大小的打勾圓圈、沒有 logo／臉／遞增長條，alt 與畫面相符。diagram-1：文字都在框內、沒有壓線或互疊，「有／沒有」標籤在線旁，虛線回主線的標籤在線上方，構圖上下平均；圖上唯一數字 2026 在表格 caption。

## 機械檢查

- `pack_cli ingest --dry-run`：exit 0，「dry run: nothing written」。
- `intake_check.py`：RESULT PASS（0 failures；唯一 WARN 是自繪 hero 沒有 hero 標題可比對，預期內）。
