# 第一輪獨立查核：AI 給了來源就可信

查核日：2026-09-27。查核者未撰寫本片。已讀完整 `video.json` 的 143 句旁白、全部字卡、標題、縮圖及說明欄；重新開啟 [Anthropic Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)（HTTP 200）。重複主張合併列出。

| # | 可查主張與位置 | 原始來源／狀態 | 判定與修正 |
| --- | --- | --- | --- |
| 1 | `mock-answer`、`ci004`–`ci007`、`ci076`–`ci079`：錯誤回答是編輯刻意製作，連結為真的官方頁 | `demo-log.md`；Anthropic 原頁，200 | CONFIRMED 為製作聲明；字卡、旁白和縮圖都明示「示意」，沒有冒稱產品實錄。無改動。 |
| 2 | `real-page`、`ci019`–`ci023`：官方頁標題是 Reduce hallucinations，主題是降低模型錯誤 | Anthropic 原頁，200，頁面標題 | CONFIRMED。短摘錄及中文意思合理。無改動。 |
| 3 | `auditable`、`not-found`、`ci029`–`ci039`、`ci096`–`ci099`：官方建議讓每項主張有引文、找不到支持就撤回 | Anthropic 原頁，200，〈Verify with citations〉 | CONFIRMED。`Make Claude's response auditable` 與畫面英文一致，中文「可被查核」忠實。無改動。 |
| 4 | `context`、`ci044`–`ci047`、`ci056`–`ci059`、`ci108`–`ci111`：方法能降低而不能消除錯誤，重要資訊仍要驗證 | Anthropic 原頁，200，結尾限制段落 | CONFIRMED。修正後對話卡與原文一致。無改動。 |
| 5 | `copy-prompt`、`ci060`–`ci063`：讓模型說不知道、逐項附來源可幫助查核 | Anthropic 原頁，200，〈Basic hallucination minimization strategies〉和〈Verify with citations〉 | CONFIRMED 為文件建議；片中也說不能免掉人工核對。無改動。 |
| 6 | `why-tricky`、`different-mistakes`、`open-link`、`redirect-check`、`ci008`–`ci019`、`ci080`–`ci087`、`ci120`–`ci123`：真實網址不保證相鄰結論，跳轉或舊版可能改變用途 | 本次可開的原頁及編輯查核方法 | OUT OF SCOPE 為通用查核規則，沒有將某個特定產品的轉址說成實際案例。 |
| 7 | `claim-split`、`marker-trap`、`ci024`–`ci031`、`ci124`–`ci127`：示意錯句前半被支持，後半未被支持 | Anthropic 原頁，200，〈Verify with citations〉及結尾限制段落 | CONFIRMED。後半「不需人工核對」與原文限制相反。無改動。 |
| 8 | `paraphrase`、`contradiction`、`ci040`–`ci043`、`ci088`–`ci099`、`ci132`–`ci135`：轉述不可強化原文；無支持句先撤回 | Anthropic 原頁，200，〈Verify with citations〉 | CONFIRMED 為片中示意的核對方法。無改動。 |
| 9 | `date`、`timeliness`、`ci052`–`ci055`、`ci104`–`ci107`：價格、功能、規則須看現行官方頁 | 編輯建議；本片未報現行價格、版本或功能 | OUT OF SCOPE，沒有需核的產品數值。來源頁可能改版，上架前重查。 |
| 10 | `corrected`、`correction-logic`、`ci056`–`ci059`、`ci108`–`ci111`：修正答案「附來源方便核查，重要資訊回原文確認」 | Anthropic 原頁，200 | CONFIRMED。無改動。 |
| 11 | `order-matters`、`fast-routine`、`ci064`–`ci067`、`ci116`–`ci119`：「一分鐘」作為先挑一項重點主張的習慣 | `brief.md` 的編輯方法，非耗時研究 | OUT OF SCOPE。旁白是「先停一分鐘」，沒有承諾每個來源都能在一分鐘內完成查核；縮圖不宣稱量化成效。 |
| 12 | `youtube.title`、`thumbnail`、`youtube.description`：官方連結也可能被誤引，本片三步修正一則錯答 | `video.json` 和 Anthropic 原頁，200 | CONFIRMED：標題與示範內容一致，並清楚標成示意。無改動。 |
| 13 | `article`、`ci068`–`ci071`：說明欄第一行有站內提示詞文章 | `source_guide=ai-chat-prompt-basics` 和產包規則 | NOT YET VERIFIED：待 `package` 後檢查實際 URL 與文章內容。 |

結果：12 組已確認或屬編輯方法，0 個事實更改，0 個官方來源衝突；1 組產包連結待驗。沒有將示意錯答說成真實模型輸出。官方頁的內容與標題會改版，錄音及公開前再查。

聽眾檢查：旁白無超過 40 字句、拉丁字詞、括號或網址；字卡引文為必要短句。縮圖「有連結，也可能說反」不保證所有引用都錯。`brief.md` 的站主觀點仍是提案，送大綱前須確認。事實沒有更改，**無需第二輪查核**；尚未完成音訊、成片與上架包檢查。
