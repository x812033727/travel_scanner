# verify-1：ai-freelance-client-confidentiality 查核第一輪（2026-10-05）

格式：主張｜判定（ok / fixed / softened / removed）｜來源網址

讀法：help.openai.com 的三頁對 curl、WebFetch 和 `.json` 後綴都回 403，web.archive.org 連線被重設，所以用 r.jina.ai 即時讀原頁全文（HTTP 200，頁面顯示 Updated 日期）。其餘各頁都用 curl -sSL 直接讀（HTTP 200，先去掉 HTML 註解）。存檔在 /home/user/batch-ai-income/_tools/ai-freelance-client-confidentiality/v1/。

## ChatGPT／OpenAI

1. ChatGPT 個人方案可能用對話訓練模型（description、summary、表格）｜ok｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance
2. 個人方案名稱「Free、Plus、Pro」｜fixed → 「Free、Go、Plus、Pro」｜https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt
3. 設定名稱「Improve the model for everyone（為所有人改進模型）」｜fixed → 官方中文介面用語「為所有人改善模型」｜https://help.openai.com/zh-hant/articles/7730893-data-controls-in-chatgpt
4. 關閉路徑「設定 → 資料控制（Data controls）」｜fixed → 官方用語「設定 → 資料控管」｜https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt
5. 暫時對話（Temporary Chat）不用於訓練｜fixed → 官方名稱「臨時交談」；加上限定條件「保持臨時狀態時」｜https://help.openai.com/en/articles/8914046-temporary-chat-faq
6. 暫時對話最多保留 30 天｜fixed → 補上「存成一般對話後改依帳號設定」（原頁：存成一般對話後，該對話改依帳號的模型改善設定）｜https://help.openai.com/en/articles/8914046-temporary-chat-faq
7. 商用方案 Business、Enterprise、API 預設不訓練｜fixed → 原頁還列了 Edu，已補上｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance
8. API 要主動選擇分享才會用於訓練｜ok｜https://developers.openai.com/api/docs/guides/your-data
9. API 濫用監控紀錄預設最多保留 30 天｜ok｜https://developers.openai.com/api/docs/guides/your-data
10. 退出訓練後按讚或倒讚，整段對話仍可能被用來訓練（summary、callout）｜ok｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance
11. 來源 8798634（Business 工作區資料預設不訓練）｜ok（內容屬實），但 sources 已滿 20 筆，所以 removed，由 7730893 取代，該頁也寫明受管理工作區預設不訓練｜https://help.openai.com/en/articles/8798634-managing-data-sharing-and-privacy-in-chatgpt-business

## Claude／Anthropic

12. 個人方案 Free、Pro、Max｜ok｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
13. 個人方案只有使用者選擇允許時才用於訓練，被安全系統標記的對話例外｜ok｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
14. 設定 → 隱私（Privacy）裡的「模型改進開關」｜fixed → 官方 zh-TW 名稱「幫助改進我們的 AI 模型」｜https://privacy.claude.com/zh-TW/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings
15. 無痕對話（Incognito chats）不用於訓練｜fixed → 官方 zh-TW 名稱「無痕聊天」；事實本身 ok｜https://privacy.claude.com/zh-TW/articles/10023580-is-my-data-used-for-model-training
16. 選擇允許時，去識別化資料最長保留 5 年｜ok｜https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data
17. 刪除的對話 30 天內從後端清除｜ok｜https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data
18. 商用產品（Claude for Work、API 等）預設不訓練｜ok｜https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training
19. 商用產品在主動送出回饋或選擇允許時才可能用於訓練｜ok｜https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training
20. API 的輸入與輸出 30 天內刪除｜softened → 「原則上 30 天內刪除，另有例外」（例外包括 Files API、零資料保留協議、違反使用政策、法律要求）｜https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data
21. 個人與商用方案的回饋都會讓整段對話保存最長 5 年（callout）｜ok｜https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training 、https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training

## Gemini／Google

22. Keep Activity 開著時用於改進服務與訓練，部分對話經人工審查｜ok；標籤改成官方 zh-TW「保留活動記錄」｜https://support.google.com/gemini/answer/13594961
23. 關掉 Keep Activity 或改用暫時對話｜fixed → 官方用語「臨時對話」｜https://support.google.com/gemini/answer/13594961?hl=zh-Hant
24. 關掉後仍保留 72 小時｜ok；補上臨時對話同樣保留 72 小時｜https://support.google.com/gemini/answer/13594961
25. 人工審查過的對話最長保留 3 年｜ok｜https://support.google.com/gemini/answer/13594961
26. Google 提醒不要輸入不想讓審查人員看到的機密資訊｜ok｜https://support.google.com/gemini/answer/13594961
27. 審查過的對話已與帳號脫鉤，刪除活動記錄也不會一起刪掉｜ok｜https://support.google.com/gemini/answer/13594961
28. 個人帳號送出的回饋經審查後，連同相關對話最長保留 3 年（callout）｜ok｜https://support.google.com/gemini/answer/13594961
29. Workspace：未經許可不經人工審查，也不用於網域外的模型訓練｜ok｜https://knowledge.workspace.google.com/admin/generative-ai/generative-ai-in-google-workspace-privacy-hub
30. 公司或學校帳號可能適用不同的資料處理條款（長期案件用客戶的商用帳號）｜ok｜https://support.google.com/gemini/answer/13594961

## 合約與著作權

31. 智慧財產局提供「出資聘人完成著作契約」範本｜ok｜https://www.tipo.gov.tw/tw/copyright/719-19274.html
32. 範本的保密條款：客戶首次公開發表前，接案者不得公開內容｜ok（DOCX f1746517130120.docx，甲方是著作人，乙方是出資人）｜https://www.tipo.gov.tw/tw/copyright/719-19274.html
33. 違反時最高相當於報酬 2 倍的懲罰性違約金｜ok（範本條款，不是法定規則）｜https://www.tipo.gov.tw/tw/copyright/719-19274.html
34. 範本的保證條款：確為獨立創作、沒有抄襲或侵權，違反時自負法律責任並賠償｜ok｜https://www.tipo.gov.tw/tw/copyright/719-19274.html
35. 營業秘密法第 2 條「所有人已採取合理之保密措施」是要件之一｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080028
36. 著作權法第 12 條：以受聘人為著作人｜fixed → 補上但書：契約可約定以出資人為著作人｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017
37. 第 12 條：著作財產權依約定歸屬，未約定歸受聘人，出資人得利用｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017
38. 第 36 條、第 37 條：約定不明的部分推定為未讓與、未授權｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017
39. 智慧財產局電子郵件1111031：以 AI 為工具且有人類創意投入的可受保護；AI 獨立創作原則上無法享有著作權｜ok｜https://www.tipo.gov.tw/tw/copyright/692-16813.html
40. 主要由 AI 產出時，「獨立創作」的保證站不住｜softened → 「容易有爭議」（沒有來源直接這樣說，屬推論）｜https://www.tipo.gov.tw/tw/copyright/719-19274.html
41. 電子郵件1150828c：生成式 AI 圖片是否標示，著作權法沒有規範，可以自行決定｜fixed → 函釋問的是「新聞圖片」，已改｜https://www.tipo.gov.tw/tw/copyright/692-94326.html
42. 人工智慧基本法第 4 條第 5 款「透明與可解釋」：產出應做適當資訊揭露或標記；主詞是推動 AI 的政府｜ok（原句文法已改順）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093

## 個資法

43. 第 2 條個人資料的定義（姓名、出生年月日、聯絡方式、財務情況等）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
44. 第 4 條：受委託者在本法適用範圍內「視同委託機關」｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
45. 施行細則第 8 條：受託者只能在委託機關指示的範圍內處理個資｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022
46. 施行細則第 8 條：監督事項包括複委託的對象，以及委託結束時個資的返還與刪除｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022
47. 第 5 條：不得逾越特定目的之必要範圍｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
48. 現行第 27 條：非公務機關應採行適當之安全措施，防止竊取、竄改、毀損、滅失或洩漏｜ok（民國 112 年 5 月 31 日版本）｜https://law.moj.gov.tw/LawClass/LawOldVer.aspx?pcode=I0050021
49. 民國 114 年 11 月 11 日修正時「改列」第 20-1 條，施行日期由行政院定之｜fixed → 修正刪除第 27 條、增訂第 20-1 條（文字也改了），所以改成「改由新增的第 20-1 條規範」。施行日期仍未定，沿革頁沒有行政院令｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021 、https://law.moj.gov.tw/LawClass/LawHistory.aspx?pcode=I0050021
50. 第 8 條：直接向當事人蒐集時應告知目的與利用方式等事項｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021

## 其他

51. 表格 caption「查證於 2026 年 10 月」｜ok（查證日 2026-10-05）｜—
52. diagram-1.svg 唯一的數字 2026 在正文出現｜ok；圖上「暫時或無痕對話」fixed → 「臨時或無痕對話」｜—
53. hero.svg：一行字「客戶資料先過三關」（56px），沒有數字、logo 或遞增長條；alt 與圖相符｜ok｜—
54. 站內連結三個（ai-at-work-policy-checklist、ai-and-copyright-law-taiwan、ai-image-copyright-taiwan）都在指派清單內，標題與站上現有文章一致｜ok｜https://mokaair.com/zh-TW/life/ai-at-work-policy-checklist 、https://mokaair.com/zh-TW/life/ai-and-copyright-law-taiwan 、https://mokaair.com/zh-TW/life/ai-image-copyright-taiwan
55. 實務建議（三個判斷、報價單寫明三件事、結案刪除）不是來源規定，正文沒有寫成法定義務｜ok｜—

## sources 狀態

- 20 筆的 checked_on 都是 2026-10-05。
- help.openai.com 的 3 筆：直接讀回 403（Cloudflare），透過讀取代理讀到 200 和全文。其餘 17 筆直接讀都是 HTTP 200，內容也是實際頁面。
- 換掉的來源：8798634（Business）換成 7730893（Data controls in ChatGPT）。
- body_length 從 2,633 變成 2,592（修訂後先漲到 2,844，再刪掉表格裡重複的英文標籤和較長的句子）。dry-run 通過，intake_check PASS（只有一個預期中的 WARN：自繪 hero 沒有 hero 標題可比對）。
