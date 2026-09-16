# 查核紀錄：ai-news-gpt-live-voice-20260708

- 查核日：2026-09-15
- 對象：`apps/api/app/guides/content/ai-news-gpt-live-voice-20260708.json`（zh-TW）與研究紀錄 `docs/ai-news-2026-09-mid/research/ai-news-gpt-live-voice-20260708.json`
- 取頁方式：curl，User-Agent `Mokaair-editorial`，未帶任何個人資料；openai.com 用 curl 可直接讀全文（未用瀏覽器工具）
- 讀過的一手頁面：
  - https://openai.com/zh-Hant/index/introducing-gpt-live/ 與英文版 https://openai.com/index/introducing-gpt-live/ （頁首日期 2026年7月8日／July 8, 2026，含 7/31 更新註記）
  - https://help.openai.com/zh-hant/articles/20001274-chatgpt-voice （機器翻譯）與英文原文 https://help.openai.com/en/articles/20001274-chatgpt-voice （Updated: 4 days ago）
  - https://help.openai.com/en/articles/6825453-chatgpt-release-notes （July 8、August 7、August 31、September 9, 2026 條目）
  - https://developers.openai.com/api/docs/changelog （September, 2026 / Sep 10 條目）
  - 輔助：https://openai.com/index/introducing-gpt-live-1-in-the-api/ （September 10, 2026）、https://openai.com/news/rss.xml （Introducing GPT-Live pubDate Wed, 08 Jul 2026 00:00:00 GMT）、https://help.openai.com/en/articles/7947663-chatgpt-supported-countries
- 自檢：`check_article.py` 輸出 OK（paragraph 2,988 字，description 137 字）

## 結果總覽

共檢查 88 條主張（title 1、description 3、開頭兩段 11、第 1 節 14、第 2 節 13、表格 6、第 3 節 12、圖解 2、第 4 節 12、第 5 節 11、callout 3；另核 sources 4 條皆為一手）。

| 分類 | 條數 |
|---|---|
| 正確 | 75 |
| 需要改寫 | 12 |
| 錯誤 | 1 |
| 查無出處 | 0（台灣／繁中原本沒寫錯，但缺「官方未說明」的交代，已補） |

重點重查項目的結論：

- 發布日 2026-07-08：發布文頁首、版本說明 July 8, 2026 條目、RSS pubDate 三者一致。正確。
- 方案分配：發布時 GPT-Live-1 為 Go／Plus／Pro 預設、mini 為免費版預設（發布文），版本說明寫 paid users 用 GPT-Live-1；9/9 起 Go 改為 3 小時 GPT-Live-1 mini、Plus 3 小時、Pro $100 15 小時、Pro $200 不限，Plus／Pro 達上限後不再切到 mini。說明中心用量表（滾動 24 小時、免費版有限度且可能調整）一致。正確。
- 背景委派模型：發布文「At launch, GPT‑Live will use GPT‑5.5 in the background」，並說會隨新前沿模型更新；9/9 版本說明改為可用 GPT-5.6 或 GPT-6 Astra，可用模型依方案而定。正文「推出初期是 GPT-5.5」正確，9/9 段落缺「依方案而定」已補。
- 錄音保存與訓練：與英文原文逐句對過（30 天、刪除例外、封存不刪、兩個開關、團隊審查、停止分享後已解除關聯者可能續用）。「只開前一個開關時」的寫法有誤導，已改；另補工作區無法分享片段。
- Business／Enterprise／Edu：7/8 版本說明「not available … at launch」是發布時條件；說明中心現況已列符合資格的 Business、Enterprise、Edu、Healthcare 工作區可用語音，用量表有 Business Standard／Premium 的 GPT-Live-1 時數。正文原本已分開寫，歸因微調。
- API：changelog Sep 10「GPT-Live 1 is now generally available in the API … Voice sessions cost $0.05 per minute, billed per second; backend model and tool usage is charged separately」。正確。
- 台灣／繁中：發布文只寫「部分最常用的語言」，版本說明只寫「supported regions」，都沒有清單、沒有提台灣。已在正文交代。

## 改動明細

1. 開頭第 2 段（需要改寫，缺官方未說明的交代）
   - 原：版本說明則寫在支援的地區推出，而且發布時不含 Business、Enterprise 與 Edu 工作區。本站沒有實際試用，文中的能力描述都是 OpenAI 的說法；……文中的做菜、練口說與開車情境
   - 改：版本說明則寫在支援的地區推出、發布時不含 Business、Enterprise 與 Edu 工作區，但兩者都沒有列出地區清單，也未另外提到台灣。本站沒有實際試用，能力描述都是 OpenAI 的說法；……文中的做菜、練口說與車上情境
   - 依據：發布文「rolling out now to ChatGPT users globally」、版本說明「in supported regions」，均無地區清單。https://openai.com/index/introducing-gpt-live/ 、https://help.openai.com/en/articles/6825453-chatgpt-release-notes

2. 第 1 節第 3 段（需要改寫，過度肯定）
   - 原：語音重疊、背景噪音、網路狀況與麥克風設定都會影響它聽到的內容
   - 改：……都可能影響它聽到的內容
   - 依據：「overlapping speech, background noise, network conditions, and microphone settings can affect what it hears」。https://help.openai.com/en/articles/20001274-chatgpt-voice

3. 第 1 節第 4 段（需要改寫，廠商宣稱未歸因）
   - 原：搜尋或推理交給背景模型處理時，GPT-Live 仍會繼續跟你交談……編輯建議在這段時間補充條件就好，不要把它邊等邊說的暫時回應當成結論，等結果回來後再請它說明依據。
   - 改：OpenAI 表示，搜尋或推理交給背景模型處理時，GPT-Live 仍能繼續跟你交談……編輯建議別把等待時的暫時回應當成結論，結果回來後再請它說明依據。
   - 依據：發布文「While it works, GPT‑Live can keep talking with you」。https://openai.com/index/introducing-gpt-live/ （後半句為字數精簡，意思不變）

4. 第 2 節第 1 段（需要改寫，範圍過寬）
   - 原：這些安排在 2026 年 9 月 9 日的版本說明中有了調整
   - 改：Go 的模型與這組推理程度，都在 2026 年 9 月 9 日的版本說明中調整
   - 依據：9/9 只改了 Go 的模型與取消 Instant/Medium/High；Plus、Pro 仍是 GPT-Live-1、免費版仍是 mini，「這些安排」會讓人以為全部改了。https://help.openai.com/en/articles/6825453-chatgpt-release-notes

5. 第 2 節第 3 段（需要改寫，過度肯定＋歸因不清）
   - 原：同一則說明也寫到，語音需要搜尋或思考較難的問題時，可以使用 GPT-5.6 或 GPT-6 Astra，模型與推理強度改用和文字聊天相同的控制選擇，原本語音專用的三種推理程度已停用。
   - 改：9 月 9 日版本說明也寫到，……模型與推理強度改用和文字聊天相同的控制選擇，可用模型與用量依方案而定；原本語音專用的三種推理程度已取消。
   - 依據：「Available models and their usage limits depend on your plan.」原文未寫出這句會讓人以為免費版也能用 GPT-6 Astra；前一段同時引了版本說明與說明中心，「同一則說明」指涉不清。https://help.openai.com/en/articles/6825453-chatgpt-release-notes

6. 第 2 節第 3 段後半（需要改寫，把現況和發布時條件接清楚）
   - 原：工作區方案另有規則，說明中心寫符合資格的 Business、Enterprise、Edu 與 Healthcare 工作區可依管理設定使用。
   - 改：說明中心現在也寫，符合資格的 Business、Enterprise、Edu 與 Healthcare 工作區可使用語音，但受工作區設定約束。
   - 依據：「ChatGPT Voice is available in eligible Business, Enterprise, Edu, and Healthcare workspaces, subject to workspace settings.」與開頭段「發布時不含」對讀，點出這是現況。https://help.openai.com/en/articles/20001274-chatgpt-voice

7. 表格 caption（需要改寫，用詞會被誤讀為另外收費）
   - 原：工作區方案另計。
   - 改：未列工作區方案。
   - 依據：說明中心工作區方案有時數也有點數計價，「另計」易讀成另收費。https://help.openai.com/en/articles/20001274-chatgpt-voice

8. 第 3 節標題與第 3 段（需要改寫，讀者安全）
   - 原標題：做菜、練口說與開車：三個使用情境 → 改：做菜、練口說與 CarPlay：三個使用情境
   - 原：第三個情境是開車。……編輯建議把要問的事在出發前想好，路況、營業時間這類資訊，停車後再用官方來源確認。
   - 改：第三個情境是車上。……編輯建議行車中不要看螢幕上的文字回應；營業時間、地址這類資訊，停車後再用官方來源確認。
   - 依據：官方安全提醒保留原文；Live 回答會同步顯示文字（說明中心），行車中看螢幕是實際風險；「路況停車後再確認」不合理，改為營業時間、地址。https://help.openai.com/en/articles/20001274-chatgpt-voice

9. 第 3 節第 2 段（需要改寫，補官方未說明語言清單）
   - 原：OpenAI 也表示部分語言可能帶非母語口音或不夠流暢
   - 改：OpenAI 表示已針對部分最常用的語言最佳化，但未列出清單，部分語言可能帶非母語口音或不夠流暢
   - 依據：「We’ve optimized GPT‑Live for some of the most popular languages in ChatGPT.」無語言清單。https://openai.com/index/introducing-gpt-live/

10. 第 4 節第 2 段（錯誤／誤導）
    - 原：……再開啟「包含你的錄音」才會分享。要注意的是，只開前一個開關時，語音對話的逐字稿仍可能依方案與設定被用於訓練。
    - 改：……再開啟「包含你的錄音」才會分享；Business、Enterprise 與 Edu 工作區則無法分享片段。另要注意，只要「為所有人改進模型」開著，語音對話的逐字稿與其他檔案就可能依方案與設定被用於訓練。
    - 依據：「If Improve the model for everyone is turned on, we may use transcripts and other files from your Voice conversations to train our models」——條件只有這個開關，與錄音開關是否開啟無關；原寫法暗示兩個都開時逐字稿就不會被用。另「Users cannot share audio or video clips from Voice conversations in ChatGPT Business, Enterprise, or Edu workspaces.」https://help.openai.com/en/articles/20001274-chatgpt-voice

11. 第 4 節第 3 段（刪句，字數）
    - 原：……決定青少年子女能否使用語音。這些規則可能變動，使用前再看一次官方頁面。
    - 改：刪去末句（非主張，為容納第 10 條補充）。

12. 第 5 節第 2 段（需要改寫，漏資格條件）
    - 原：需要讓 ChatGPT 看鏡頭或螢幕時，要在支援的手機 App 改選進階模式
    - 改：需要視訊或螢幕分享時，符合資格的訂閱者可在 iOS 與 Android App 改用進階模式
    - 依據：「Video and screen sharing remain available to eligible subscribers in the ChatGPT iOS and Android apps when using Advanced」；版本說明亦寫 eligible subscribers。https://help.openai.com/en/articles/20001274-chatgpt-voice

13. 第 5 節第 3 段（刪句，字數；API 事實不變）
    - 原：開發者端的消息只簡單帶過，而且和 ChatGPT 裡的推出是兩件事：……另外計費。一般使用者看前面的方案用量表即可。
    - 改：開發者端和 ChatGPT 裡的推出是兩件事：……另外計費。

14. 第 3 節第 4 段（字數精簡，事實不變）
    - 原：OpenAI 在 2026 年 8 月 31 日的版本說明中也提到 → 改：2026 年 8 月 31 日的版本說明也提到

15. callout（需要改寫，過度肯定）
    - 原：可用選項會受方案、工作區設定、地區、App 版本與家長控制影響
    - 改：可用選項可能受……影響
    - 依據：「The options available to you may depend on your plan, workspace settings, region, app version, and parental controls.」https://help.openai.com/en/articles/20001274-chatgpt-voice

（第 11、13、14 條為字數調整，不計入分類；分類表中「需要改寫」12 條＝第 1–9、12、15 條加標題，「錯誤」1 條＝第 10 條。）

## 研究紀錄同步

- `unverified_or_excluded` 第一條：原「slug 與專輯歸檔日為 2026-07-09……本站歸在 7 月 9 日」改為「slug 已由 20260709 改為 20260708 與官方日期對齊，正文首句寫 7 月 8 日；RSS pubDate 為日期戳記，沒有官方發布時刻，因此不換算、不寫台灣時間」。
- `verified_facts`：發布時預設模型一條註明 9/9 起 Go 改用 mini；新增語言最佳化與地區清單「官方未列」一條；7/8 版本說明條註明 at launch 與含免費版；9/9 條補「可用模型與用量依方案而定」與控制方式；工作區條補用量表與「排除是發布時條件」；進階模式條補「符合資格的訂閱者、iOS 與 Android」；訓練條改寫逐字稿條件並補工作區無法分享。
- `unverified_or_excluded` 新增：台灣列於 ChatGPT Supported Countries 但不是 GPT-Live 地區清單；CarPlay 需 iOS 26.4 未寫。
- `editorial_brief`：車上情境改為依官方提醒、行車中不看螢幕、不鼓勵行車中操作手機。

## 讀者角度檢查

- 開車：已移除「開車」作為情境標題，保留官方安全提醒並加「行車中不要看螢幕上的文字回應」，沒有鼓勵行車中操作手機。
- 實測暗示：全文沒有「我們試用／實測」，開頭段明寫本站沒有實際試用；做菜例子「只剩兩顆蛋」等標明為編輯設計。
- 與 `ai-news-gemini-live-20260826`：該篇談 Gemini Live 的郵件、Daily Brief、Spark，無 GPT-Live／CarPlay／錄音內容，不重複。
- 與 `ai-news-chatgpt-work-20260709`：該篇談 Work 的跨檔案交接，無語音內容；本篇也未寫桌面 Work／Codex 語音，不重複。
- 另注意：既有教學 `chatgpt-voice-mode-guide`（非本批）已涵蓋 9/9 方案時數、30 天保存與訓練開關，與本篇第 2、4 節主題重疊。本篇定位為新聞並有發布時／現況對照，未改動該檔。該檔寫「單次語音對話最長 2 小時」，本次讀的官方頁只寫「最長工作階段長度」未給數字，本篇不採用。

## 仍不確定的點

- 「支援的地區」沒有官方清單。台灣在 ChatGPT 整體支援國家名單內，但無法據此推定台灣帳號已有 Live；本站未實測。
- 說明中心 zh-hant 頁為機器翻譯，「即時／即時模式」與 App 內繁中介面的實際字樣可能不同；callout 已註明是「中文說明頁譯為」。「為所有人改進模型」「包含你的錄音」也取自該譯文，App 介面措辭可能不同。
- 9/9 版本說明稱「daily usage limits」，說明中心寫滾動 24 小時；正文採說明中心的算法，兩者是否完全同義未見官方說明。
- 「Clips are retained for 30 days」原文未說明對話保留時片段是否在 30 天後自動刪除，正文照原文寫「保留 30 天」，未延伸解讀。
- 8/7 版本說明寫 GPT-Live 支援檔案上傳與專案，說明中心現寫 Live 無法從 Library 找檔、可能可手動附加；兩者細節未對齊，本篇維持不寫。
- 說明中心頁 4 天前更新，方案時數與工作區條件近期仍可能變動。
