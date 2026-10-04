# verify-1: ai-term-large-language-model

獨立查核者：codex / llm_review，2026-10-04（Asia/Taipei）。不是撰稿者；本輪只寫本報告，修正由撰稿者套用。已逐句讀完整長片旁白、所有字卡及插圖提示、縮圖與 YouTube metadata、claims.md、brief.md、demo.py、demo-log.md，以及兩支 Shorts 的全部文字。沒有用 lint 代替語義審查，也沒有呼叫任何模型或付費 API。

最新 production source 的 video.json SHA-256：`fd454c82e4376a46cacb0ce36f9af4e2bcd8fca75a23fcae520d58afd97bfb82`。下方「實測節奏附錄」已獨立覆核兩個停頓調整及零重錄證據；本報告原有內容與事實結論沿用到此版本。

原完整文字終審綁定 SHA-256（文字、事實、示例與 metadata 均未改動）：

- video.json：`f18c6c619c2e9928c34593f921a63f33e679ce92a0005b70f217c97b3a511a83`
- shorts.json：`e71ab40ca34c01537d6818de33c0259af904ebaa422538d4ad3188e550bc84b5`
- demo.py：`48985f140aeececa13e795466950e7423275658f276054984dfb478ed1bf940d`
- claims.md：`b948e6aeb1b7a322bdd32796c36442f3c09e9b93d15bb520f5b0eb44f8f45831`
- brief.md：`b23f074132fe526115f9908c49d430881f028272b0b064375d64376c3f7c8ca9`

抽取清單先存於 repo 外的 `C:/Users/x8120/mokaair-work/ai-series-continuation-20261004/llm-review/claim-items.json` 與 `claim-items.md`，共 614 個字串。涵蓋 138 句長片旁白、108 個場景的全部 data、縮圖、標題、說明、tags 與 Shorts；本版沒有 say。相同事實的重複表述按下表的 c 編號合併查核；圖像提示、鏡頭、虛構情節與問題式包裝的非事實部分歸 OUT OF SCOPE。所有可查主張都列在下表，另列未在作者 c 表單獨出現的執行版本、日期、metadata 與畫面文字。

## 來源重開

對官方與論文頁使用 `curl.exe -sSL`、固定 User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同 host 至少相隔 1.1 秒；移除 HTML comments 後閱讀。來源快照、`source-fetch.mjs` 與 `source-status.json` 在上述私有目錄。另以 web open 交叉閱讀；搜尋呼叫 0 次。以下都在 2026-10-04 取到 HTTP 200，無重用九月文章的 checked_on 當今日證據。

| 代號 | 官方／研究原始來源 | HTTP | 支持範圍 |
| --- | --- | --- | --- |
| S1 | https://developers.google.com/machine-learning/crash-course/llm | 200 | 語言模型、token 切分、上下文與語言表示 |
| S2 | https://developers.google.com/machine-learning/crash-course/llm/transformers | 200 | Transformer 變體、自注意力、參數與錯誤可能性 |
| S3 | https://huggingface.co/docs/transformers/tasks/language_modeling | 200 | 因果語言模型預測下一 token，不能看未來 token |
| S4 | https://huggingface.co/docs/transformers/llm_tutorial | 200 | 已生成輸出參與接續，解碼策略、輸入／輸出流程 |
| S5 | https://developers.google.com/machine-learning/crash-course/llm/tuning | 200 | 訓練更新權重；提示不改模型參數 |
| S6 | https://ai.google.dev/gemini-api/docs/function-calling | 200 | 模型提出函式與參數；外部程式執行，再送結果回模型 |
| S7 | https://arxiv.org/html/2005.14165v4 | 200 | Brown 等人的 few-shot 原始研究；不更新梯度仍能處理多種任務，能力依任務而異 |
| S8 | https://arxiv.org/html/2005.11401v4 | 200 | Lewis 等人的 RAG 原始研究；檢索材料與參數記憶不同，檢索不等同即時網路搜尋 |
| S9 | https://arxiv.org/html/1706.03762v7 | 200 | Transformer 原始論文；注意力加權、因果遮罩、逐步生成 |

S2 的 full Transformer／masked prediction 教學沒有被泛化為所有 LLM；用 S3、S4、S9 確認本稿限定的因果式生成。S7 僅用於核對「不能由生成機制直接否定推理能力」的邊界，不搬入其模型名、參數數字或跑分。S8 僅作檢索邊界交叉查核；本稿沒有冒稱執行 RAG，也沒有把貼資料等同 RAG 或已聯網。

## 全部主張表

CHANGED 表示本輪提出、作者已套用且本查核者重讀的範圍修正；不是未處理的建議。原創示例的 N/A 表示以所附原始資料／程式和獨立執行確認，沒有假裝它是外部實驗。

| # | 主張 | where | URL／依據 | HTTP | verdict | before → after／核查結果 |
| --- | --- | --- | --- | --- | --- | --- |
| c1 | 人物、失物故事與生活比喻是虛構；插圖不是模型內部實物 | 全部 shot prompts；fictional-label；bakery-mistake | brief.md、全部原創 prompts | N/A | CONFIRMED | 虛構標記存在；比喻沒有被說成實測或模型內部照片。 |
| c2 | 文字通順不證明查到資料，仍可能出錯 | hook、market-scoop、wrap；youtube.title/description；short-1 | S2: https://developers.google.com/machine-learning/crash-course/llm/transformers | 200 | CHANGED | 結尾「可信答案還要資料與執行證據」→「可信回答要有據可查」，另用條件句「若用了工具」核對實際結果；避免每份可信回答都必須執行工具的誤讀。 |
| c3 | demo 沒有網路、帳號或模型呼叫；只證明此資料與規則 | fictional-label、evidence-terminal、demo-not-benchmark；youtube.description | demo.py 全文；獨立 Python all/data 執行 | N/A | CONFIRMED | 僅 argparse/json 與固定資料；沒有模型輸出或模型效果結論。 |
| c4 | L001 是北側櫃台、未領的雨傘；沒有失主姓名／電話欄位 | counter-hands、counter-empty-hook、first-three-jobs、evidence-terminal | demo.py RECORDS/evidence；demo-log.md | N/A | CONFIRMED | 對照原始欄位與輸出一致。 |
| c5 | 王先生、電話與已領走是編輯錯誤示意 | first-three-jobs、invented-name、kitchen-gap | demo.py 欄位；兩張 chat 全文字 | N/A | CONFIRMED | 名稱／電話無欄位支持；已領走與 unclaimed 相反；卡與旁白均標示編輯示意。 |
| c6 | 位置紀錄不能單獨確認所有權 | counter-match、counter-dog | RECORDS 不含所有權／核身欄位 | N/A | CONFIRMED | 限定這份虛構資料；沒有外推法律或真實領物規則。 |
| c7 | 一份回答能同時含生成、查找與計數；有來源仍可由模型生成文字 | three-jobs-card q7mz/xy5h/eyiz；three-column-card；wrap；short-1 | S6: https://ai.google.dev/gemini-api/docs/function-calling | 200 | CHANGED | 三種工作容易被當互斥能力→明說同時存在、工具結果後仍生成文字，三欄核對依據與執行紀錄。 |
| c8 | 未領雨傘是 L001、L003，共兩把 | counter-pair、count-terminal、demo-two-umbrellas、condition-stats；short-2 | RECORDS；獨立 demo.py count 結果 | N/A | CONFIRMED | 確認兩個條件交集與兩個代號，不拿全部六件作答案。 |
| c9 | 提出工具要求不等於執行 | tools-chapter、market-request、tool-three-steps、garden-tool | S6: https://ai.google.dev/gemini-api/docs/function-calling | 200 | CONFIRMED | 官方流程明列應用程式執行與結果返回；沒有憑模型一句話認定完成。 |
| c10 | 常見因果式生成依已有 token 接續；已生成內容參與後續；不能先看未生成後文 | bakery-next-piece、bakery-row、generation-not-all | S3: https://huggingface.co/docs/transformers/tasks/language_modeling ; S4: https://huggingface.co/docs/transformers/llm_tutorial | 200 | CONFIRMED | 有明示因果式範圍，不泛化到全部 LLM。 |
| c11 | LLM 是 Large Language Model 縮寫與模型類別 | generation-chapter、bakery-skill；title/tags/thumbnail | S1: https://developers.google.com/machine-learning/crash-course/llm ; S2 | 200 | CONFIRMED | 沒有把名稱說成某個聊天產品。 |
| c12 | token 不固定等於一中文字，也沒有通用精確字數换算 | bakery-pieces、bakery-uneven、token-card、garden-related-token | S1: https://developers.google.com/machine-learning/crash-course/llm | 200 | CONFIRMED | 麵團明示比喻；没有編造 tokenizer 的計數實測。 |
| c13 | 接續內容受前文與選擇方式影響 | bakery-selection cvvb | S4: https://huggingface.co/docs/transformers/llm_tutorial | 200 | CONFIRMED | 文件的解碼設定支持；稿未聲稱某策略保證正確。 |
| c14 | Transformer／LLM 架構不全相同 | generation-not-all | S2: https://developers.google.com/machine-learning/crash-course/llm/transformers ; S3 | 200 | CONFIRMED | 未說全部都是 encoder+decoder 或全部遮罩訓練。 |
| c15 | 注意力以數學方式處理材料／token 關係 | bakery-relations、bakery-carry、bakery-weigh | S2: https://developers.google.com/machine-learning/crash-course/llm/transformers ; S9 | 200 | CONFIRMED | 原創代名詞示意沒有假冒注意力權重實測。 |
| c16 | 處理上下文不保證每次找對指涉 | attention-boundary、attention-check | S2: https://developers.google.com/machine-learning/crash-course/llm/transformers | 200 | CONFIRMED | 是能力範圍與錯誤可能性的保守界線，沒有錯誤率或絕對能力結論。 |
| c17 | 一般推論貼資料提供上下文，與更新權重的訓練不同 | parameters-context、pottery-brief、market-saved | S5: https://developers.google.com/machine-learning/crash-course/llm/tuning | 200 | CONFIRMED | 只說這輪提供材料，不替個別產品承諾永不保存或永不訓練。 |
| c18 | 參數是訓練調整的運算數值，不是逐筆失物簿 | pottery-adjust、pottery-many-pots、parameters-context | S2: https://developers.google.com/machine-learning/crash-course/llm/transformers ; S5 | 200 | CONFIRMED | 不把每個參數當可一對一翻查的紀錄。 |
| c19 | 失物簿比喻不能推出模型完全不記住事實 | pottery-many-pots fbw8 | S8: https://arxiv.org/html/2005.11401v4 ; 原創比喻範圍 | 200 | CONFIRMED | 全稿未出現「參數完全不含事實」「永遠只會照抄」等延伸。 |
| c20 | 後續對話可見的材料由當次輸入／產品安排；保存再提供與重訓不同 | pottery-bare-table、market-key、memory-rule、memory-product-rule | S4: https://huggingface.co/docs/transformers/llm_tutorial ; S5 ; S6 | 200 | CONFIRMED | 記憶實作保留「要看產品說明」條件，沒有特定產品功能承諾。 |
| c21 | 格式要求是輸入指令，不保證遵守或正確 | pottery-instruction、unknown-rule | S5: https://developers.google.com/machine-learning/crash-course/llm/tuning ; S2 | 200 | CONFIRMED | 提示可調輸出，仍核對結果；沒有保證式宣傳。 |
| c22 | 缺欄位補姓名、未領改已領為可對照的錯誤 | invented-name、kitchen-empty-jar | RECORDS；chat 逐字比對 | N/A | CONFIRMED | 精確指出兩項無依據內容；沒聲稱已觀測模型犯錯。 |
| c23 | 要求來源、未知欄位與缺資料說明 | unknown-rule、check-lines、rewrite-request | brief.md 站主立場 4/6/7 | N/A | OUT OF SCOPE | 編輯操作建議；文本明說仍須核對，無個人實測心得或成功率。 |
| c24 | 不能由生成機制直接裁定完整推理／任務能力 | pottery-capability、pottery-uncertainty、kitchen-task | S7: https://arxiv.org/html/2005.14165v4 ; 任務評估方法 | 200 | CONFIRMED | 原始研究展示多任務能力及限制；稿未宣稱永不能推理或心智等同人類。 |
| c25 | 六筆物件是兩傘、一瓶、一圍巾、一帽、一手套 | demo-six-objects、six-records-table；youtube.description；short-2 | 獨立 demo.py data；RECORDS | N/A | CONFIRMED | 六列物件、順序與代號全部一致。 |
| c26 | L002/L005 已領；其餘四筆未領；六、四、二分別有不同條件 | count-terminal、condition-stats、six-records-table；short-2 | 獨立 demo.py all/data；手工逐列計數 | N/A | CONFIRMED | 已領 2、未領 4、未領傘 2，代號與排除條件正确。 |
| c27 | L001 無 owner_phone，程式輸出 UNKNOWN；沒去搜尋電話 | demo-phone-gap、missing-terminal | demo.py missing；獨立輸出 | N/A | CONFIRMED | 欄位存在檢查與輸出一致。 |
| c28 | 此資料不能回答電話，不推出世界上沒有電話 | demo-empty-palm x483 | 欄位範圍與邏輯 | N/A | CONFIRMED | 沒有把缺資料變成不存在的證明。 |
| c29 | 留條件、代號與結果幫助回查 | demo-trace、three-column-card、rewrite-request | 原創方法；brief.md 立場 4/7 | N/A | OUT OF SCOPE | 編輯建議，不是工具永不出錯的保證。 |
| c30 | 文章圖解有有效連結；六筆資料與結果完整附說明欄 | article-cta.data；ujfe；youtube.description | https://mokaair.com/zh-TW/life/what-is-a-large-language-model ; 本地圖解、description/data | 200 | CHANGED | 僅總索引與尚未發布的 GitHub 404 URL、字卡說另有資料／重跑連結→本篇有效文章 URL，說明欄直接附六筆與結果；字卡改「圖解與六筆示範資料」「附文章連結、資料與結果」，不再承諾不存在的程式下載／重跑連結。 |
| c31 | 確定規則結果不證明模型可靠率 | demo-not-benchmark d6ut；全片／shorts 揭露 | demo.py 邊界；沒有模型呼叫 | N/A | CONFIRMED | 沒有幻覺率、提示成功率、模型成本或性能結論。 |
| c32 | 資料、執行、整理不同階段都要核對條件 | tool-three-steps、market-scoop、kitchen-counterexample | S6: https://ai.google.dev/gemini-api/docs/function-calling ; 原創錯誤示例 | 200 | CONFIRMED | 原創示例支持何種錯誤；没有錯誤頻率或特定模型結論。 |
| c33 | 產品整合提供輸入、工具與輸出，不能把所有功能歸模型 | product-model、market-access、market-key | S6: https://ai.google.dev/gemini-api/docs/function-calling ; S4 | 200 | CONFIRMED | 以「可能」「要看是否」保留實作／權限差別。 |
| c34 | 重複同句不增加獨立外部證據 | kitchen-repeat、kitchen-agree、kitchen-evidence | 邏輯；S2: https://developers.google.com/machine-learning/crash-course/llm/transformers | 200 | CONFIRMED | 稿說「可能」重複同錯；没有相關性百分比或聲稱已跑模型。 |
| c35 | 有來源還需核對支持範圍 | kitchen-bias、garden-check-it | brief.md 立場 4 | N/A | OUT OF SCOPE | 編輯查核方法，與站主立場相符。 |
| c36 | 檢索找材料，工具執行處理，結果仍要核對 | nearby-terms、pzcj | S6: https://ai.google.dev/gemini-api/docs/function-calling ; S8 | 200 | CONFIRMED | 沒有宣稱檢索必然聯網、資料必真、必改權重；也未冒稱本片執行 RAG。 |

## 補充字串與數值查核

| # | 主張／數值 | where | URL／依據 | HTTP | verdict | 結果 |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | 三張 terminal 的 Python 版本 3.14.6 | evidence-terminal/missing-terminal/count-terminal.data.tool_version | 獨立 `python --version` | N/A | CONFIRMED | 實際 Python 3.14.6，沒有引用預期版本當實測。 |
| P02 | 執行日 2026-10-04 | 三張 terminal.data.ran_on；condition-stats.data.source | 本輪 client 日期與獨立執行 | N/A | CONFIRMED | 與 demo-log 日期一致。 |
| P03 | evidence／missing／count 指令与每行輸出 | 三張 terminal.data.command/output | 獨立 `python demo.py all` 和 `data` | N/A | CONFIRMED | 每行與 demo-log 一致；`>` 是乾淨提示符，沒有主機或帳號資訊。 |
| P04 | 章節序號、三種工作／三題／三個陷阱 | chapter.data.number、steps、errors-chapter | 順讀全部 108 場景 | N/A | CONFIRMED | 冷開场後內容從第二章開始，8 章順序正确；各三項都有內容。 |
| P05 | 自有 SVG 圖解與 caption | article-diagram；assets[0] | 讀 SVG title/desc/文字與箭頭；© Mokaair 來源 | N/A | CONFIRMED | 參數和當次材料進模型，外部工具回結果；未把圖片說成模型內部觀測。 |
| P06 | 完整文章與 AI 名詞索引連結 | youtube.description | https://mokaair.com/zh-TW/life/what-is-a-large-language-model ; https://mokaair.com/zh-TW/life/ai-terms-index?utm_source=youtube&utm_medium=video&utm_campaign=ai-term-large-language-model | 200 | CONFIRMED | 兩個實際 metadata URL 都取到 200；本篇 HTML 含正確文章標題。 |
| P07 | Shorts 1 的泡泡／人物／失主資料都是虛構 | shorts.json[0].description/scenes | RECORDS；長片 c3/c4/c7 | N/A | CONFIRMED | 畫面與描述留非模型實測揭露及三種工作重疊邊界；未新增信心百分比。 |
| P08 | Shorts 2 的六、四、二與條件 | shorts.json[1] 全文 | 獨立計數；長片 c8/c25/c26 | N/A | CONFIRMED | 數字、件／把單位與篩選條件一致，保留離線且非模型實測。 |
| P09 | 「AI 名詞十分鐘」與估計 13.8 分鐘 | tags/title；brief/draft-metrics | 企劃名稱、當前 lint estimator | N/A | OUT OF SCOPE | 系列包裝及估算，不是成片量測；本輪沒有確認 WAV 或成片達 8 分鐘。 |
| P10 | 插圖、人、動作、比喻、camera、thumbnail shot | 全部 75 shot 的 data；thumbnail | 作者提示與實際 referenced scene IDs | N/A | OUT OF SCOPE | 文字構圖與場景角色相符；沒有已生成插圖可視覺驗收，不能稱完成畫面或成片。 |

## 獨立執行與聽眾審稿

獨立執行 `python demo.py all` 與 `python demo.py data` 均 exit 0；手工逐列核算與工具輸出一致。原始輸出、版本、demo SHA-256 保存在私有 helper 的 `demo-independent.json`。程式含固定輸出文字，但在輸出前以原始資料檢查紀錄和篩選代號；本輪另逐列核算，所以沒有用作者預期輸出自證通過。這份固定資料示範不是通用失物管理程式、模型測試或已執行任何外部工具整合。

聽眾文字審稿結果：

- 冷開場估計約 11 秒，文字立刻提出「話完整是否代表查到」並帶出證據問題；虛構標記在卡上，後續口播與 metadata 都保留非模型實測界線。七個內容章各用具體生活場景，章末問題銜接，收尾回到開場。實際冷開場時長需 TTS 後跑 chapter 檢查，不能用此估算證明實際至少 10 秒。
- 兩支 Shorts 的文字可獨立看懂，也保留原創資料、離線程式和非模型實測揭露。它們是稿件；本輪未確認直式成片、剪輯、聲音或實測時長。
- 全部 138 句沒有未拆的 40 字以上長句、口播 URL、括號或審查式旁白；LLM、AI、token 在既有發音字典。少量簡字由作者修成繁體；最終 Shorts 的「來自」已重讀。
- 指涉例子「她拿走他的杯子」是原創材料關係示意，不是成功指涉辨識測試。注意力卡另拆「處理上下文」與「不保證找對」；記憶卡也拆出產品條件，聽眾不必一次記下長但書。
- 字卡揭示順序按旁白安排；六筆資料、三組 terminal、6/4/2 stats 與旁白沒有不同數字或條件。實際字卡裁切、可讀性、動畫、配音口氣仍待生成後觀看／聆聽。
- 建議均屬 brief 的站主立場 4/6/7；没有替站主編造個人使用經驗、測試排名或功能心得。沒有意見／立場不符。

最終 `node tools/video/cli.mjs lint --slug ai-term-large-language-model`：exit 0，**0 errors、0 warnings**；估計 13.8 分鐘、138 句、2,929 spoken units。估計不是正文或成片量測。本輪沒有產生旁白、插圖、音樂、成片，沒有核准關卡、上傳或發布。

## 結論與後續邊界

36 個作者主張：30 CONFIRMED、3 CHANGED、3 OUT OF SCOPE、0 NOT FOUND。另外 10 個補充項目：8 CONFIRMED、2 OUT OF SCOPE。本輪的三個範圍／metadata 修正已全部套用，沒有未解決的事實或對外連結主張。

**不需要規定中的第二輪事實查核**：本輪 3 個不同主張的範圍修正，没有超過 3 個事實變動。若之後改機制、數字、示例、工具紀錄或 metadata 承諾，需重查並更新綁定雜湊。

沒有價格、方案、模型排名、參數量、產品限額或效能等近期易過期事實。Python 版本／執行日期只指這次示範，不指觀眾的環境。每個來源 checked_on 已讀為 2026-10-04。

本報告支持此綁定版本的稿件事實與聽眾文字審稿；不證明大綱／媒體關卡已核准、真實旁白聽感、正文或成片至少 8 分鐘、直式素材、語言完成、公開可下載程式、YouTube 上架、G 槽交付或可刪原件。這些需沿既有關卡取得各自證據。

## 實測節奏附錄：兩個 pause 調整與零重錄

2026-10-04T11:09:28Z，獨立 narrow reverify；只更新本報告，不修改其他來源、不呼叫付費 API、不代寫任何音訊批准。此附錄將本報告的 video.json 綁定更新至 **`fd454c82e4376a46cacb0ce36f9af4e2bcd8fca75a23fcae520d58afd97bfb82`**。原 36 項作者主張、10 項補充查核、完整旁白與 Shorts 聽眾文字審稿結論均沿用；本輪沒有新增事實變動。

已讀 Git parent／working diff，video.json **只有兩個欄位新增**：`count-terminal` 的 `ks7c.pause_after_ms=80`、`demo-two-umbrellas` 的 `qizd.pause_after_ms=30`；二者原先未寫，使用預設 300ms。刪回這兩個欄位後，JSON 與 Git parent 完全相同，重新序列化的全檔 SHA-256 精確等於原完整查核 hash `f18c6c619c2e9928c34593f921a63f33e679ce92a0005b70f217c97b3a511a83`。沒有改字、數字、條件、揭示順序、鏡頭、聲音、句子代號、章節或 metadata。

build.mjs 只增加此二 id 的 override，位置在 `setPauseBeats(doc)` 之後。獨立以記憶體替代 writeFileSync 的輸出蒐集器執行建置邏輯，生成的 video.json 及 draft-metrics.json 內容與目前 working files **逐位元組完全相同**，沒有執行真實寫檔；因此再次建置會保留本次修正。draft-metrics 變動只有衍生估秒、後段章節 frame 與 video hash，仍是估算，沒有冒稱實測值。

### 實際音訊與快取證據

已獨立讀取目前 138 個原始 clip WAV；每個檔案的 SHA-256 均與 timeline 的 audio_sha256、合成 cache.sha256 相同，PCM sample 數均與 timeline.audio_samples 一致。使用現有 138 個 clip 的 SHA-256 和實際 sample 數，配上原始 source／speech hash／原測量的 narration SHA 重建**整份原 timeline**，JSON 全檔 SHA-256 精確回到原私有測量檔的 `b9116d49680f4ab264f256ad8b5b05c7c30a86d8572d97367562b7f3730c4f52`。再用目前 WAV 及原停頓組合整軌，SHA-256 精確回到 `e4322bf95c347c6ef012424fa649c7084a3f2da470680b0fcbcf685166c4f614`。這兩個比對支持全部 138 clips 與修正前相同，沒有用「沒有報錯」取代逐檔證據。

全部 108 個 `planRequests` 結果（包括 body、request key、138 個 line key）修正前後完全相同，`staleTakes=[]`。pause 會改 `speech_hash`（`502a51ec8e9a47b0` → `bc923f1be75ed10b`）與整軌時間，但不改任何發送給語音合成的文字／聲音或 take key。

已讀主代理實跑 `llm-tts-refresh.log` 與 state.json：本次 refresh **0 requests synthesized、0 billable characters、108 reused**。目前新 timeline 全檔 SHA-256：`4c6935846a8155b300da0328b480ebe2c018d7fee3694abf40ae73edd64605b0`；目前 dry narration WAV SHA-256：`739f98ea2b78bcf0d2456e13deebb1fddc6e5a380f35311078937fe67ef9f70b`。新整軌只改外加停頓，已用現有 WAV 獨立組合並得到同一 SHA；`audioEvidenceProblems=[]`。

### 新實測章節與節奏

| scene / line | 實際 spoken samples / 秒 | 修改後外加 pause + 固定 scene gap | 實際完整畫面 |
| --- | --- | --- | --- |
| count-terminal / ks7c | 346560 / 7.22 秒 | 80ms + 700ms | 240 frames，**8.0 秒** |
| demo-two-umbrellas / qizd | 348960 / 7.27 秒 | 30ms + 700ms | 240 frames，**8.0 秒** |

保留 700ms 正常轉場 gap；沒有剪除旁白音節、加停頓、加速、放慢或重新合成。兩處不是依一位小數 rounding 過門檻，實際 240 frames / 30fps 均恰 8 秒。

新的 dry body 實測 **836.1666667 秒**；原始 clips spoken 合計 **709.18 秒**。8 章全部至少 10 秒，冷開場第一章實測 **11 秒**，`checkChapters=[]`；無需修改冷開場章節。138 個狀態最長 8 秒，插圖占 dry body **56.2367949%**；`cadenceProblems` 沒有 `over`／`share` 硬性問題。平均 **6.1 秒**仍保留為 `kind=average` 建議，沒有宣稱達到 6 秒目標；現版 final QA 明確不把該平均建議當硬性失敗。新的 lint 為 **0 errors、0 warnings**。

獨立 helper 與完整結果（含 138 個 SHA-256）在私有 `C:/Users/x8120/mokaair-work/ai-series-continuation-20261004/llm-review/narrow-reverify.mjs` 及 `narrow-reverify-results.json`。原測量與主代理 paced 測量也已閱讀並交叉核對。

此附錄確認最新來源的事實查核延續性、實際 PCM／dry narration 計時、章節及節奏硬性問題解除，**不代表已通過 check-audio、聽感驗收或伺服器 audio 核准**；主代理的轉寫／Jev 檢查仍在執行，不能把尚未完成的逐句匹配稱全過。整軌及 timeline hash 改了，需以目前版本走 audio review-push／pull。已生成插圖、成片裁切／可讀性、品牌 presentation timeline、後續 QA、YouTube、G 槽備份與刪除仍需各自證據。
