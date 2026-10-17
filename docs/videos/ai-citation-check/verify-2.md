# 第二輪獨立事實覆核：AI 給了來源就可信？

覆核日：2026-10-07（Asia/Taipei）。覆核者：`llm_language_path`，不是本片撰稿者，也不是第一輪查核者。此次依認領後的限定授權，只新增本紀錄；不修改已核准的 `video.json`、`brief.md`、`claims.md`、`demo-log.md` 或翻譯。

**結果：核心來源、示意標示與延伸文章內容 PASS，0 個事實修正；實際上傳包說明欄第一行仍為 PENDING_PACKAGE_CHECK。** 這是文字與來源覆核，不能據此宣稱整支影片完成驗證、音訊可接受、畫面可接受、已上傳或可公開。

## 核對範圍與固定來源

逐一讀取原稿 36 場、143 句旁白（`ci001` 至 `ci143`，依場次排列）、每場 `data`、6 個章節、縮圖文字、YouTube 標題、說明、標籤與來源欄；另讀 `brief.md`、`claims.md`、`demo-log.md` 和 `verify-1.md`。相同主張在下表合併，但核對包含其各次出現。旁白沒有 `say` 覆寫。

| 固定檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `video.json` | 24329 | `a9b9eb260a2d61a6f430fdb74e2193a6327fb3267aa7c430b39105235f8d3cd2` |
| `brief.md` | 4212 | `82c127758c451209330ad591e41c2fae2fb0f1a3ec57bb3bf015ea4ace8eab02` |
| `claims.md` | 2697 | `686e31e4f080c21cba4d9cfc55740585609df8cf7d262c3e07a789c9cb1c9c66` |
| `demo-log.md` | 1299 | `a50901a8fee551af310c743ef4e8275f8129fefc58fff2f104d9e6894eba45c4` |
| `verify-1.md` | 4574 | `b2563cd62d40ea168a46daf1d300d2a180e791e096df081e78dccbdc97be4ed0` |
| `apps/api/app/guides/content/ai-chat-prompt-basics.json`（CTA 內容依據） | 25574 | `0c9f72e7f6df06bdeee014fb3c365942f25286ab43e2132fd60eea0e043ae3a4` |

## 本日實際開啟的來源與 metadata

HTTP 檢查使用 `curl.exe -sSL`、`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，跟隨轉址；內文另外以網頁工具或公開頁面 GET 讀取。讀取 HTML 時移除註解，不以搜尋摘要確認主張。以下三個正式路徑均回傳 200，最終網址與列出的網址相同。查閱時間截至 `2026-10-07T16:44:27+08:00`，隨後完成站內文章內文核對。

| 代號 | 本日開啟的完整原始網址 | 頁名／發布者 | HTTP | 日期及用途 |
| --- | --- | --- | ---: | --- |
| S1 | <https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations> | Reduce hallucinations／Claude Platform Docs，Anthropic | 200 | 頁面沒有可確認的發布或更新日；2026-10-07 是本次查閱日。核對基本策略、逐項引用與結尾限制。 |
| S2 | <https://www.anthropic.com/engineering/building-effective-agents> | Building Effective Agents／Anthropic Engineering | 200 | 頁面標發布日 2024-12-19，並有工具環境已變、另看現行方案的提示。這是此次另行要求開啟的背景來源，未新增至影片的來源欄。 |
| S3 | <https://mokaair.com/zh-TW/life/ai-chat-prompt-basics> | 提示詞入門：把問題問清楚的五個原則，改前改後對照著學／Mokaair | 200 | 核對本日實際公開內文與原則五、查證警語；本次查閱日不當成文章發布或更新日。 |

S1 現行內容仍要求逐項找到支持引文，缺少支持時撤回；其限制段仍保留關鍵資訊須驗證的條件。S2 是有日期背景的工程文章，不能替代 S1 對本片引用示範的直接證據，也不支持「附引用就不需人工查核」。本片沒有報現行模型版本、產品價格、介面功能或框架清單，因此 S2 的工具更新提示不構成本片的事實變更。

S3 的公開 HTML 確認包含原則五、允許不確定、為主張找出處／找不到撤回、列出假設與資料缺口，以及具體事實回官方來源查證。未對延伸文章所有產品數值或全部其他主張做新一輪查核；本次只核對本片對它的描述。

## 完整主張表

`CONFIRMED` 包含可確認的製作聲明，並在列內說明其證據類型；通用方法與編輯立場標 `OUT OF SCOPE`，不冒充實測成效。所有「前 → 後」均為原文保持不變。

| # | 主張及出現位置 | 來源／HTTP | 判定 | 前 → 後及限制 |
| --- | --- | --- | --- | --- |
| 1 | 錯答為編輯刻意製作，不是真實模型輸出。`mock-answer.data.messages`、`mock-purpose.data`、`ci004`–`ci007`、`ci076`–`ci079`；`marker-trap`、`corrected` 同屬示意。 | 固定 `demo-log.md`、`brief.md`、原稿；本地 | CONFIRMED（製作聲明） | 不變。字卡明示「教學示意」「錯誤示意」「示意段落」「原示意錯句」；不據此指控特定商用模型。 |
| 2 | 本片所附頁面是真實官方文件，頁題與降低錯誤的主題相符。`real-page.data`、`ci019`–`ci023`、`ci078`。 | S1，200 | CONFIRMED | 不變。本日正式網址可開，頁面標題及發布者一致。 |
| 3 | 逐項引用讓回覆可以查核。`auditable.data.quote/translation/source`、`source-function.data`、`ci029`、`ci032`–`ci033`、`ci128`–`ci131`。 | S1，200 | CONFIRMED | 不變。英文短摘錄 `Make Claude's response auditable` 與原文相同，中文意思未擴張成正確保證。 |
| 4 | 每個主張應找支持引文，找不到應撤回。`not-found`、`missing-proof`、`paraphrase.data`、`ci034`–`ci039`、`ci092`–`ci099`。 | S1，200 | CONFIRMED | 不變。撤回缺證據的主張，沒有偷換成補一個相似網址即可。 |
| 5 | 示意錯句的前半「引用有助查核」有支持，後半「不必人工核對」未被支持且與限制相反。`claim-split`、`marker-trap`、`not-found`、`ci024`–`ci031`、`ci036`–`ci039`、`ci124`–`ci127`。 | S1，200 | CONFIRMED | 不變。將錯誤主張當成待拆解示範，沒有把它當成官方立場。 |
| 6 | 降低錯誤不等於消除錯誤，重要資訊仍應核對；修正答案保留此限制。`context`、`corrected`、`correction-logic`、`ci044`–`ci047`、`ci056`–`ci059`、`ci108`–`ci111`。 | S1，200 | CONFIRMED | 不變。未宣稱引用或提示詞能免除必要查證。 |
| 7 | 允許說不知道、要求主張對應來源可協助核對；仍不能保證正確。`copy-prompt.data`、`ci060`–`ci063`、`ci070`–`ci071`。 | S1，200；S3，200 | CONFIRMED（建議與編輯推論分開） | 不變。「比較省力」「較容易」是本片的質性編輯推論，不是官方量化效果或無錯保證。 |
| 8 | 提示詞入門文章教要求來源、列出缺口與允許說不知道。`article.data.title`、`ci069`–`ci071`。 | S3，200；固定本地文章 | CONFIRMED | 不變。公開內文與本地內容均支持本片描述；其查證警語保留人工核對。 |
| 9 | 上傳說明欄第一行有該文章。`article.data.sub`、`ci068`。 | 實際新上傳包，尚未由本覆核者讀取 | PENDING_PACKAGE_CHECK | 不變。必須在產包後確認實際 `upload/metadata.json.description` 第一行；不能以 `source_guide` 或程式規則冒充已產出的交付證據。 |
| 10 | 拆小主張、逐句比對、保留條件與力道，未支持或相反就停下修正。`one-to-one`、`search-method`、`paraphrase`、`contradiction`、`context-window`、`certainty-scale`、`weaker-words`、`date-and-topic`；`ci040`–`ci043`、`ci048`–`ci051`、`ci088`–`ci099`、`ci100`–`ci103`、`ci132`–`ci143`。 | 本片編輯方法；S1 提供示範的直接文本 | OUT OF SCOPE（方法） | 不變。不是所有引用錯誤的完整分類，也不宣稱能發現全部錯誤。 |
| 11 | 網址、來源描述或搜尋摘要不能單獨證明相鄰結論；轉址後還需核對頁名和內文。`why-tricky`、`different-mistakes`、`open-link`、`page-or-summary`、`redirect-check`、`link-vs-proof`；`ci008`–`ci023`、`ci080`–`ci087`、`ci120`–`ci123`。 | 本片編輯檢查方法；S1 本日可開 | OUT OF SCOPE（方法） | 不變。表格為一般情況，沒有冒稱這次 S1 已轉址、某產品已連錯頁或曾觀察到特定產品事件。 |
| 12 | 價格、規則、功能等變動資訊要看現行來源；舊來源不必然適用今日決策。`date`、`timeliness`、`ci052`–`ci055`、`ci104`–`ci107`。 | 本片編輯建議；S3 查證警語 | OUT OF SCOPE（方法） | 不變。本片不報當前價格、版本或新舊差額；沒有把查閱日當成更新日。 |
| 13 | 原來源曾於 2026-09-27 開啟。`sources[0].checked_on`、`youtube.description`、`brief.md`、`demo-log.md`。 | 固定 2026-09-27 製作紀錄／`verify-1.md`；本地 | CONFIRMED（歷史紀錄存在） | 不變。本輪不能重演或獨立證明當天網路回應；確認的是留存紀錄及本日內容仍支持核心說法，不把本日重查寫回舊日期欄。 |
| 14 | 三步法、「一分鐘」與挑一句練習是編輯提供的查核習慣。`three-questions`、`order-matters`、`fast-routine`、`practice`、`answer`；`ci001`–`ci003`、`ci012`–`ci015`、`ci064`–`ci067`、`ci072`–`ci075`、`ci112`–`ci119`。 | `brief.md` 與本片編輯方法；本地 | OUT OF SCOPE（方法／時間安排） | 不變。沒有查核耗時實測、成功率或完整查完任意問題的保證；原稿的「先停一分鐘」按先挑重點的習慣理解。 |
| 15 | 標題「AI 給了來源就可信？三步抓出錯誤引用」、縮圖「有連結，也可能說反／一則示意回答當場拆解」、說明、四個標籤與示範一致。`youtube.*`、`thumbnail.data`、`hook.data`。 | 原稿、示意紀錄、S1，200 | CONFIRMED | 不變。未冒稱實際商用模型失誤、實測比例、最新產品功能或所有引用均不可信。 |
| 16 | 原稿 `source_guide=ai-chat-prompt-basics` 對應正式文章路徑；原生產包規則會將文章連結放在說明最前。 | `tools/video/core/metadata.mjs:94–104,130–141`；`tools/video/package/metadata.mjs:49–66`；本地 | CONFIRMED（靜態規則） | 不變。預期連結為 `https://mokaair.com/zh-TW/life/ai-chat-prompt-basics?utm_source=youtube&utm_medium=video&utm_campaign=ai-citation-check`。規則成立仍不等於第 9 項實際產包已驗。 |
| 17 | 另行要求開啟的工程背景文有 2024-12-19 發布日與工具環境變動提示；它不是本片核心引用的原頁。 | S2，200 | CONFIRMED（本輪來源辨別） | 不變。沒有把 S2 日期、模型清單或工程示範搬入原稿，也未將它列成原稿已引用的來源。 |

第 10、11、12、14 項涉及的通用方法不包含需補造的數字、產品事故或研究結果。`target_minutes=[8,12]` 與 brief 的約 600／605 秒是製作目標，沒有當成已量測成片長度；語音設定、分類號與其他工作設定不屬本片向觀眾提出的教學事實。

## 原示範與日期的限制

刻意寫錯的句子不是模型實錄，亦未在本輪呼叫模型取得「再次重現」的輸出。`demo-log.md` 是製作示意紀錄；本輪的實際動作只有讀取凍結稿件、讀取官方／自有公開頁面、核對內容與來源雜湊。沒有 TTS、ASR、圖片生成、媒體修改或付費 API 呼叫。

2026-09-27 是原稿聲明的歷史開啟日，不是現行文件發布日。本次查閱日是 2026-10-07。S1 未顯示可核對的更新日；S2 的 2024-12-19 是發布日，不能當成所有現行段落最後更新日；S3 內文中的 2026 年 9 月與來源 `checked_on` 也不因此改成今日。這些日期語義保持分開。

`brief.md` 仍留有「提案，待站主確認」的歷史文字。本輪沒有代站主確認其個人立場或覆寫批准狀態。原稿採用的「引文是可檢查的線索」立場與 brief 提案一致，沒有加上站主親身經驗。

## 聽眾文字檢查與交付待辦

143 句旁白逐句檢查最長 25 字，沒有超過 40 字，沒有拉丁字詞、括號或網址，也沒有 `say` 覆寫。字卡有兩處必要的短英文引文；可讀性、畫面與音訊仍需成片檢查，這不是本輪實際觀看或聆聽的結果。

本輪沒有執行原生 `lint`、音訊或成片檢查；不可引用舊查核的 `lint` 結果代表新工作區本次已完成檢查。由產線主操作者附本次實際檢查收據。

產包後，主操作者須讀取實際 `upload/metadata.json`：確認繁中 `description` 第一行連到 S3（含本片 UTM），而不是只看到 `source_guide`；並確認來源段保留 S1，歷史日期沒有冒充本日更新。新包的 hash／讀取結果應附在正式交付紀錄；第 9 項完成前，不宣稱整支影片或完整上傳包已驗證。

本輪統計：17 組，12 組 CONFIRMED、4 組 OUT OF SCOPE、1 組產包待驗；CHANGED 0、NOT FOUND 0、來源衝突 0。沒有修改固定源檔，無因事實修正而要求重做旁白。後續需要的是產包依賴確認與正常音訊／成片／交付檢查，沒有第三輪事實修稿需求。

## 2026-10-07 視覺修訂後的獨立比對

原稿查核及上表雜湊指向最初的 `a9b9eb260a2d61a6f430fdb74e2193a6327fb3267aa7c430b39105235f8d3cd2`（24329 bytes）。主操作者於 `2026-10-07T09:03:31.423Z` 套用視覺修訂，現行 `video.json` 為 `c1e01a5a8797445bd147606ad8ae87427c9adb9aa0f57a959474d30a01b968b0`（24669 bytes）。原查核紀錄及歷史日期保持不變。

本覆核者另讀取私有 `visual-candidate/original-video.json`、`candidate-video.json`、`proof-applied.json`，並獨立比對實際 repo 稿件：現行稿與候選稿的 JSON 物件完全相同；差異只有 8 場的 template/data 重排及 31 句的 reveal 設定。逐場比對所有原字卡字串均保留，沒有新增或刪除主張。36 場順序、6 個章節、143 句的 ID、文字、停頓及其他旁白欄位、voice、全部 YouTube metadata、縮圖、來源與歷史日期均相同。

獨立以同一現行 `docs/videos/lexicon.json`（SHA-256 `862d277aaf4359e9e07b5f3281f59eabb240f5ea3227c174f692cf2d0237f675`）重算前後原生純函式計畫：36 個 TTS 請求的完整物件、voice、body 與全部逐句 key 完全相同；有效字典依賴前後均為空陣列，speech hash 與實際 timeline 皆為 `399237f659e75fc5`。143 個現行 raw WAV 的完整 SHA-256 均吻合原量測 timeline，各 cache key 亦仍有效；沒有因這次視覺重排而需要重錄旁白。

在原量測 18596 frames／30 fps 與完全相同的逐句邊界上，獨立重算為 67 個實質畫面狀態，最長 14.9 秒，超過 15 秒者 0；template/data 與 reveal 容量檢查錯誤 0。**前後文字與來源事實比對 PASS。** 這是純函式與實際檔案比對，不是渲染、播放、聆聽或站主驗收，也沒有執行供應商呼叫或修改媒體。新上傳包說明欄首行仍待第 9 項的實際產包檢查。
