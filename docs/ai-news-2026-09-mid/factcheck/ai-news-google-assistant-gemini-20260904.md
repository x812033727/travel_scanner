# 查核紀錄：ai-news-google-assistant-gemini-20260904

- 查核日：2026-09-15
- 查核對象：`apps/api/app/guides/content/ai-news-google-assistant-gemini-20260904.json`（zh-TW）與研究紀錄 `docs/ai-news-2026-09-mid/research/ai-news-google-assistant-gemini-20260904.json`
- 取頁方式：curl，User-Agent `Mokaair-editorial`，請求不含任何個人資料。說明中心頁以 `?hl=en` 與 `?hl=zh-Hant` 對照；社群討論串內容由頁面內嵌資料解碼讀取。
- 自檢：`check_article.py` 輸出 `OK`，正文段落 2,985 字（原 2,974）。

## 主張數與判定

共拆出 102 條可查主張（title 1、description 5、開頭兩段 11、第 1 節 12、第 2 節 11、表格與 caption 14、第 3 節 15、圖解 caption 3、第 4 節 15、第 5 節 7、callout 4、sources 4）。

| 判定 | 條數 |
|---|---|
| 正確 | 80 |
| 需要改寫（過度肯定、歸因不清、易誤導） | 16 |
| 錯誤 | 2 |
| 查無出處 | 4 |

sources 維持原本 4 條（已達上限，且四條各有別處沒有的依據），URL 都能開、內容與標題相符。

## 重點核對結果（正確，未改）

- 9 月 4 日原文：`On Sept. 4th, 2026 most users will no longer be able to use or switch back to Google Assistant on your phone or tablet.`；配對周邊 `like watches running Wear OS, headphones or earbuds compatible with Gemini, vehicles running Android Auto`；`We have sent an email with more details to users whose mobile device or peripheral will be impacted.`；下半段 2025 年底計畫延到 2026 年。發文 2025-12-19、更新 2026-08-05（UTC）。https://support.google.com/gemini/thread/396052272?hl=en
- 發文者身分：署名 `Community Manager - Gemini Apps Team`；Google 說明社群的標章說明寫 `Google Employees: Guides and Community Managers who work at Google`。可以寫成 Google 員工發的公告，但它是社群公告，不是說明中心文章或部落格。https://support.google.com/communities/answer/7424249?hl=en
- 其他裝置：`Other devices with Google Assistant built-in — such as Smart Displays, smart speakers, TVs, cars, and Pixel Tablets — will continue to be directly powered by Google Assistant.` https://support.google.com/gemini/answer/14554984?hl=en&co=GENIE.Platform%3DAndroid
- 不支援功能：Podcasts、news and radio stations、some third-party music providers；Interpreter mode 要切回 Assistant；例行程序要連結 Google Home、部分啟動條件與動作不支援、天氣只剩語音與文字回應。https://support.google.com/gemini/answer/14579631?hl=en
- 兒童與工作帳號：13 歲或所在國家適用年齡、未滿 13 歲需家長核准、Android Work Profile 不能用（14579026）；Family Link 可以關閉（14554984）；受監護帳號不能用 Hey Google 與 Voice Match（14579631）；工作或學校帳號少了 quick voice action（14554984、14579631）。
- 活動記錄與位置：Web & App Activity／Keep Activity、切換後另一邊的資料不會自動刪除、位置權限跟著 Google 應用程式。https://support.google.com/gemini/answer/14554984?hl=en&co=GENIE.Platform%3DAndroid
- 台灣：同時列在 `Where you can download the Gemini app from the Google Play Store` 與 `Where you can switch to Gemini through Google Assistant` 兩份名單；`Chinese (Simplified / Traditional)` 沒有星號。https://support.google.com/gemini/answer/14579026?hl=en&co=GENIE.Platform%3DAndroid
- 裝置條件：2 GB RAM 以上、Android 9 以上，Android Go 不支援。同上頁。
- 本站實測：文中寫明沒有實測，生活情境也標了是編輯設計的例子，沒有暗示試用。
- 與 `ai-news-gemini-spark-20260519` 是否重複：該篇沒有提到 Assistant 或助理換手，沒有重複。

## 改動清單（原文 → 改後 → 依據）

1. **description**（改寫：主詞偏移、「暫留」過度推定）
   「Google 公告 2026 年 9 月 4 日起，多數 Android 手機與平板無法再使用或切回…受影響與暫留的裝置…換手前可先檢查的設定」
   → 「Google 在 Gemini 說明社群公告，2026 年 9 月 4 日起多數使用者無法在手機或平板上使用或切回…受影響與未列入的裝置…換手前後可檢查的設定」
   依據：原文主詞是 most users，不是多數裝置。https://support.google.com/gemini/thread/396052272?hl=en

2. **第 1 段**（改寫：歸因不清）
   「Google 在 Gemini 應用程式社群發布的官方公告寫道」
   → 「Google 的 Gemini 應用程式團隊社群管理員在官方說明社群發布公告，寫道」
   依據：https://support.google.com/gemini/thread/396052272?hl=en 、https://support.google.com/communities/answer/7424249?hl=en

3. **第 2 段**（改寫＋查無出處）
   「公告沒有列出各國推送順序，也沒寫台灣何時輪到，實際換手時間以裝置上的通知為準」
   → 「公告沒有說明是否分批、各國先後，也沒有單獨提到台灣，你的裝置目前由哪個助理回應，以畫面實際顯示為準」
   依據：本文 sources 裡沒有一條提到分國推送，也沒有提到換手通知。原寫法預設「按國家輪流推送」，而一手頁的「通知」只出現在自願改用 Gemini 的情境（14554984）。

4. **第 1 節第 1 段**（精確化）
   「保留了較早的說明」→「保留了 2025 年 12 月發文時的說明」
   依據：討論串頁面資料的發文時間是 2025-12-19。https://support.google.com/gemini/thread/396052272?hl=en

5. **第 1 節第 2 段**（改寫）
   「本文查核的頁面沒有說明，以官方後續公告為準」→「公告沒有說明」
   依據：Google 在 2025-03-14 的部落格註腳寫過，不符最低需求的裝置 `Google Assistant functionality will not change at this time`，所以不能說「官方從沒說過」。但這是 2025 年的說法，9 月 4 日公告沒有重申，因此只寫公告沒有說明。https://blog.google/products/gemini/google-assistant-gemini-mobile/

6. **第 1 節第 3 段**（改寫：把推測寫成結論、矛盾範圍寫窄了）
   「說明中心的『開始使用』頁面仍保留…切回步驟…比較穩妥的理解是切回選項可能在推送到你的裝置後消失，不要把『不習慣再切回來』當成退路」
   → 「『開始使用』頁仍保留切回步驟，『能做什麼』頁也還寫著功能不支援時可以切回，社群公告寫的卻是 9 月 4 日起多數使用者無法再切回。兩份官方內容不一致，說明頁的切回步驟不一定適用，別把切回當成退路。」
   依據：14579631 的 Tip 寫 `If Gemini can't help with something Google Assistant can do, you can switch to Google Assistant`；14554984 的 `Switch to Google Assistant` 小節。

7. **第 2 節第 1 段**（改寫：原文只是舉例，不是完整清單）
   「社群公告點名…還有執行 Android Auto 的車輛。公告把 Android Auto 車輛和手錶、耳機放在同一類…」
   → 「社群公告點名手機與平板，並舉出與手機配對的周邊為例：…也就是說…透過 Android Auto 回應語音指令的也會是 Gemini」
   依據：原文用的是 `like watches running Wear OS…`。

8. **第 2 節第 2 段**（錯誤＋易誤導）
   (a) 「Pixel Tablet 在鎖定或 Hub 模式時」→「Pixel Tablet 鎖定時（包括 Hub 模式）」
   依據：`Pixel Tablets that are locked, including in Hub Mode`（14554984）；`when your Pixel Tablet is locked, including when in Hub Mode`（14579631）。Hub 模式是鎖定狀態的一種，原文寫成兩種並列的情況。
   (b) 「暫時保留 Assistant 的是非行動裝置」→「沒有列入這次換手的是非行動裝置」，並加上「這段說的是手機換成 Gemini 時不會連帶改變的裝置」，把「說明頁把車輛列在非行動裝置」改成「其中的車輛指內建 Google Assistant 的車」。
   依據：說明頁那句話的前提是 `When you use Gemini as your primary mobile assistant`，講的是手機換手會不會連帶影響。Google 部落格 2026-04-30 另外寫到 `Gemini is replacing Google Assistant in cars with Google built-in`，會先從美國英文使用者開始。若照原文寫成「仍由 Assistant 支援」而不附前提，讀者會誤以為內建 Google 的車不會換成 Gemini。https://blog.google/products-and-platforms/platforms/android/cars-with-google-built-in-gemini-tips-2026/

9. **第 2 節第 3 段**（跟著第 8 點修正）
   「電視、音箱與智慧螢幕沒有列入」→「電視、音箱、智慧螢幕與內建 Google 的車輛都沒有列入」

10. **表格第 1 列**（改寫：過度肯定）
    「多數改由 Gemini，無法切回」→「多數使用者無法再用或切回」
    依據：原文的「無法切回」只針對 most users。

11. **表格 Wear OS 列**（錯誤：歸因錯誤）
    「型號支援以製造商說明為準」→「公告未列支援型號」
    依據：Wear OS 手錶能不能用 Gemini 看的是 Google 自己的說明頁（研究紀錄查到的條件是 Wear OS 4 以上），不是製造商說明。這條不在 sources 上限內，所以只寫公告沒有列出型號。

12. **表格 Android Auto 列**（查無出處）
    「開車指令以官方說明為準」→「開車前先試常用指令」
    依據：本文 sources 裡沒有 Android Auto 指令的官方說明可以指向，改成不需要出處的操作建議。

13. **表格最後一列**（改寫）
    「車輛本身的系統」→「內建 Google 的車輛」
    依據：14554984 寫的是 `devices with Google Assistant built-in … cars`。

14. **表格 caption**（查無出處）
    「實際換手時間以裝置畫面通知為準」→「各裝置實際狀態以畫面顯示為準」
    依據：同第 3 點。

15. **第 3 節第 1 段**（改寫：把舉例寫成完整清單，漏掉「目前」）
    「說明中心直接列出兩類…不支援的項目…常出國的讀者要特別留意口譯模式，因為切回選項在換手後可能不再提供」
    → 「說明中心列出 Gemini 當主要助理時不支援的功能，舉的例子有兩類：…頁面寫目前不支援；二是口譯模式（繁中說明頁譯作『翻譯模式』）…因為多數使用者已無法切回」
    依據：`some features and services … aren't supported. This includes:`、`aren't currently supported in Gemini`（14579631 en）；繁中版把 Interpreter mode 譯作「翻譯模式」（14579631 zh-Hant）。台灣讀者用繁中頁搜尋時會找到「翻譯模式」，所以括號註明。

16. **第 3 節第 3 段**（查無出處）
    「智慧家庭控制、傳訊息與通話、提醒事項、開車時的指令，說明頁提到 Gemini 能用語音處理其中一部分，例如快速傳訊息或開燈；…以官方說明為準」
    → 「說明頁舉的語音快速動作例子是傳訊息與開燈；提醒事項、通話、開車時的指令在台灣以繁體中文使用時哪些完整可用，查核的頁面沒有逐項列出」
    依據：14579631 只寫 `Use your voice to take quick actions, like sending a message or turning on your lights`，沒有提到提醒事項或開車指令。原寫法會讓人以為說明頁談過這些項目。

17. **第 4 節標題**（改寫：事件日已過）
    「換手前可以先做的幾項檢查」→「換手前後可以做的幾項檢查」
    依據：查核日 9/15 已在 9/4 之後，公告寫的是多數使用者已經換手。清單內容本身正確、實用，沒有改。

18. **第 5 節第 1 段**（補充，屬台灣讀者需要的名稱對照）
    句尾加上「繁中版說明頁把喚醒詞寫作『Ok Google』」
    依據：https://support.google.com/gemini/answer/14554984?hl=zh-Hant&co=GENIE.Platform%3DAndroid

19. **第 5 節第 2 段**（改寫：同第 3 點）
    「9 月 4 日的公告也沒有寫台灣的推送時間。台灣使用者何時換手、換手後每項指令能否使用，官方未說明，以裝置上的通知與實際回應為準」
    → 「9 月 4 日的公告也沒有單獨提到台灣。台灣帳號換手後每項指令能否使用，官方未說明，以實際回應為準」

20. **第 5 節第 3 段**（改寫：「趁還沒換手」預設讀者還沒換手；並為字數上限刪一句）
    「可以趁還沒換手，把依賴的功能列成清單…；家人手機陸續換手時，也能拿同一份清單幫忙檢查」
    → 「可以把依賴的功能列成清單…；已經換成 Gemini 的人也可以照清單補查」

研究紀錄同步：verified_facts 補上社群管理員的 Google 員工身分、like 舉例、Pixel Tablet 鎖定含 Hub 模式與說明頁的前提、「能做什麼」頁也寫可以切回、This includes 與 currently、翻譯模式、Ok Google；unverified_or_excluded 補上 Assistant 社群公告（9 月 3 日版本）、內建 Google 車輛的部落格、2025 年部落格註腳、Gemini Go，以及排除 Product Expert 撰寫的社群指南。

## 另找的更正式公告

- blog.google、Android 官方部落格：沒有找到專為 9 月 4 日換手發布的文章。相關的只有 2025-03-14〈The Assistant experience on mobile is upgrading to Gemini〉（原始計畫）和 2026-04-30 談內建 Google 車輛的文章。
- support.google.com/assistant：Assistant 社群有一則署名 `Community Manager - Google Assistant` 的公告〈Important Update: Transitioning from Google Assistant to Gemini on Mobile〉（頁面資料顯示 2026-08-06 UTC 發布）。內容寫 `starting on September 3`、`may take a few weeks to reach everyone`，移除後手機、平板與配對裝置都無法切回；內建 Google 的車輛 `will continue to function beyond September 3, 2026`；不影響 Nest 與 Home 音箱、螢幕。https://support.google.com/assistant/thread/457649886?hl=en
- Android Auto 說明頁（6348083）只寫 `Gemini is replacing Google Assistant on most mobile devices`，沒有日期。
- Assistant 社群指南 441911995 的作者是 Product Expert，不是 Google 員工，不採用。

## 仍不確定的點

1. **日期差一天**：Gemini 社群公告寫 9 月 4 日，Assistant 社群公告寫 9 月 3 日起開始移除；媒體引述郵件是 9 月 4 日。文章只把 9 月 4 日歸因於 Gemini 社群公告，沒有寫出這個落差（sources 已滿 4 條）。如果之後要補，建議用 Assistant 社群公告換掉其中一條，或在 callout 註明。
2. **分批時程**：「可能要幾週才會輪到每個人」只在 Assistant 社群公告出現，文章沒有寫。台灣帳號是否已經全部換手，本站沒有實測。
3. **切回步驟**：說明中心兩頁仍寫可以切回，公告寫多數使用者不行。哪些人屬於「少數」、那些步驟對誰還有效，官方都沒有說明。
4. **不符條件的舊機**：2025 年部落格說功能「暫時不變」，2026 年的現況官方沒有更新。Android Go 裝置另有 Gemini Go，文章沒有展開。
5. **內建 Google 的車輛、電視、音箱**：美國英文的車已經開始升級 Gemini；台灣與繁體中文何時升級，官方沒有說明。
6. **繁體中文的 Ok Google 與各項指令**：中文沒有標星號，只代表不在不支援清單上，不能證明台灣繁中介面每項語音動作都能用。
7. **Assistant 時期的提醒**：會不會出現在 Gemini 可以管理的清單裡，本文依據的頁面沒有寫。
8. **Wear OS 3 手錶**：9 月 4 日之後的狀態，官方頁沒有說明。
