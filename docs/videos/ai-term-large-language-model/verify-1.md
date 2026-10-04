# verify-1: ai-term-large-language-model

獨立查核者：codex / llm_review，2026-10-04（Asia/Taipei）。不是撰稿者；本輪只寫本報告，修正由撰稿者套用。已逐句讀完整長片旁白、所有字卡及插圖提示、縮圖與 YouTube metadata、claims.md、brief.md、demo.py、demo-log.md，以及兩支 Shorts 的全部文字。沒有用 lint 代替語義審查，也沒有呼叫任何模型或付費 API。

最新 production source 的 video.json SHA-256：`2a9bfa4e99d17d1805891f70c56e78416101bc94255c330e96ee62555e14408a`；shorts.json：`b70535ce3c920a88c451cbc589ed63f9a9e16168a9c15d9806828fb8915a06a0`；timeline.json：`3b57a6f54b78cd5267c6a6b2898bd87e5650121a7da8dbceb78d81f03b6f7e02`。下方附錄保留歷史覆核；最後「兩卡及 Shorts 完整圖片附錄」綁定當前來源。本報告原有事實結論沿用到未改動的文字；分鏡與實際成片關卡仍須綁最新證據，沒有因來源審稿而核准圖片。

原完整文字終審綁定 SHA-256（其後僅兩個停頓、一處同義口播及兩鏡插圖提示調整，見附錄；事實、示例與 metadata 未改動）：

- video.json：`f18c6c619c2e9928c34593f921a63f33e679ce92a0005b70f217c97b3a511a83`
- shorts.json：`e71ab40ca34c01537d6818de33c0259af904ebaa422538d4ad3188e550bc84b5`
- demo.py：`48985f140aeececa13e795466950e7423275658f276054984dfb478ed1bf940d`
- claims.md：`b948e6aeb1b7a322bdd32796c36442f3c09e9b93d15bb520f5b0eb44f8f45831`
- brief.md：`b23f074132fe526115f9908c49d430881f028272b0b064375d64376c3f7c8ca9`

抽取清單先存於 repo 外的 `<home>/mokaair-work/ai-series-continuation-20261004/llm-review/claim-items.json` 與 `claim-items.md`，共 614 個字串。涵蓋 138 句長片旁白、108 個場景的全部 data、縮圖、標題、說明、tags 與 Shorts；本版沒有 say。相同事實的重複表述按下表的 c 編號合併查核；圖像提示、鏡頭、虛構情節與問題式包裝的非事實部分歸 OUT OF SCOPE。所有可查主張都列在下表，另列未在作者 c 表單獨出現的執行版本、日期、metadata 與畫面文字。

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

獨立 helper 與完整結果（含 138 個 SHA-256）在私有 `<home>/mokaair-work/ai-series-continuation-20261004/llm-review/narrow-reverify.mjs` 及 `narrow-reverify-results.json`。原測量與主代理 paced 測量也已閱讀並交叉核對。

此附錄確認最新來源的事實查核延續性、實際 PCM／dry narration 計時、章節及節奏硬性問題解除，**不代表已通過 check-audio、聽感驗收或伺服器 audio 核准**；主代理的轉寫／Jev 檢查仍在執行，不能把尚未完成的逐句匹配稱全過。整軌及 timeline hash 改了，需以目前版本走 audio review-push／pull。已生成插圖、成片裁切／可讀性、品牌 presentation timeline、後續 QA、YouTube、G 槽備份與刪除仍需各自證據。

## 聽稿改寫附錄：9fyu 同義措辭

2026-10-04T11:38:30Z，獨立 narrow reverify。最新 production source 的 video.json SHA-256 更新至 **`bc87f8b12c07a0039d60dec9f185dccefe5b3f38e65959298bcb5cc249badc5d`**；本輪只修改本查核報告，不呼叫付費 API、不修改其他來源或音訊、不代寫音訊核准。

與基準 commit `08a2c84f4`（source `fd454c82e4376a46cacb0ce36f9af4e2bcd8fca75a23fcae520d58afd97bfb82`）逐項比對，video.json **只有 kitchen-gap / 9fyu.text 改動**：

- before：「其實清單裡缺失主，填個王先生只會讓錯誤更完整。」
- after：「其實清單沒寫物品主人，填王先生只會讓錯誤更完整。」

把此一句替回原文字後，完整 JSON 與基準深度相等，重新序列化的全檔 SHA-256 精確回到 `fd454c82e4376a46cacb0ce36f9af4e2bcd8fca75a23fcae520d58afd97bfb82`。因此其他旁白、所有data字卡／鏡頭／prompts、六筆示例、數字／條件、voice、pause、reveal、章節、縮圖、metadata與assets均沒有內容變更。claims.md、demo.py、demo-log.md、shorts.json、brief.md 與基準逐位元組相同；line-ids.txt 只有 Git LF／working CRLF 的既有格式差別，正規化後內容相同、Git diff 空；video內 **138個id與順序完全相同**。

已重新語義讀取六筆 `RECORDS`，以 Python AST literal 直接核對所有六列只有 `id/item/location/status` 四種欄位，無物品主人姓名或 owner_phone。新句「清單沒寫物品主人」準確限定於這份虛構清單，沒有推出物品在現實中不存在主人；「王先生」在改寫前後均一次，仍是編輯刻意補入、未受資料支持的虛構姓名。相鄰 `invented-name` 字卡及兩句口播仍明說新增失主與未領改已領都是錯誤；c5／c22 事實、非模型實測揭露及原 verdict **CONFIRMED** 維持。沒有新增機制、數值、人物事實、工具結果或可用產品能力。

已實跑 repo 的 `rewriteProblems(before, after, {lexicon})`，結果 **[]**；數字與拉丁字詞前後均無，字典詞沒有增減，「王先生」另外人工及程式確認保持同一出現次數。新句22 spoken units，原21；整片計畫估算變為2930 units。這是聽稿用語變化，不是第四個事實主張修正，不改原36項及補充10項的查核結論，也不因此觸發第二輪事實查核。

build.mjs 只有同一行文字替換；保持兩個實測 pause override 在 `setPauseBeats(doc)` 後。獨立以記憶體輸出蒐集器執行建置邏輯，產生的 video.json 與 draft-metrics.json 和目前working檔案 **逐位元組完全相同**，沒有真實寫入來源。衍生metrics只改units、估秒、後段章節frame及source hash。新的 lint **0 errors / 0 warnings**。

`planRequests` 獨立比較確認，只改 `kitchen-gap` 的一個request及 **9fyu 的take key**；其餘137個take key均相同。覆核瞬間 `staleTakes=['9fyu']`；speech_hash 由 `bc923f1be75ed10b` 變 `5e45b34feaa17c8c`，因此主代理可依正常ledger只重錄此句、重用其餘137句。新的語音實際結果、clipSHA、整軌／timelineSHA、逐句轉寫與章節／節奏仍需重錄後重新量測；不能把舊「零重錄」附錄或舊PCM秒數直接當此最新音訊已審。原節奏附錄的零重錄證據指當時兩個pause調整，後續有限重錄屬另一階段。

獨立helper與完整結果在私有 `<home>/mokaair-work/ai-series-continuation-20261004/llm-review/listener-rewrite-reverify.mjs`、`listener-rewrite-reverify-results.json`。主代理的 `review/rewrites.json` 正規ledger、實際新take與遠端audio批准須各自留存。本附錄允許事實查核延續至最新source；不宣稱138/138聲音已過、實聽驗收、成片、上架、G槽交付或可刪原件。

## 兩鏡視覺提示附錄：長版歷史，保留音訊、局部重畫

2026-10-04T12:03:20Z，獨立 narrow reverify；本轮只修改本報告並保存私有證據，不 rebuild 實際來源、不修改 manifest、音訊、cache、checks 或批准，不呼叫付費 API。當時 video.json SHA-256 為 **`bb0aca6bfe791dc02a3e268076abedce385ae6b3a8cc42fe4ab839e498734043`**；此長版後因供應商合併提示長度限制而縮寫，見最後附錄。

與主代理保留的 `llm-before-visual-fix.json`（SHA `bc87f8b12c07a0039d60dec9f185dccefe5b3f38e65959298bcb5cc249badc5d`）比較，完整 JSON **僅 counter-arrival.data.prompt、counter-handoff.data.prompt 改變**。把二者替回原 prompt 後，JSON 深度相等且重新序列化全檔 SHA 精確回到基準。75 鏡中其餘 **73 個完整送圖提示**相同；全部 138 句 text/id/順序/pause/reveal、各場景 claims、voice、look、章節、字卡、thumbnail 與 YouTube metadata 均相同。claims.md、demo.py、shorts.json、brief.md 全檔 SHA 仍精確等於本報告原終審綁定。36 項主張及補充10項結果不變，未新增事實修改。

build.mjs 用 `promptOverrides` 僅覆寫這兩個 id；其餘 helper 與鏡頭產出不變。以記憶體 writeFileSync 蒐集器執行建置邏輯，產生的 video.json 和 draft-metrics.json 與實際 working files 逐位元組相同，沒有寫入來源。actual lint **0 errors / 0 warnings**。

### 原聲音與計時保持綁定

獨立比較兩個版本的 **108 個 planRequests（含所有 request body/key 及138 line keys）完全相同**；speech_hash 維持 `5e45b34feaa17c8c`，look_hash 維持 `ed4c2594703d65d6`，`staleTakes=[]`。以目前 WAV 的 audio_samples 計算兩版本 measured timeline core，結果完全相同；全部章節仍 `checkChapters=[]`。

讀取當前音訊並比對兩鏡修正之前的 `llm-final-audio-audit.json`，下列檔案完整 SHA-256 均未變：

- timeline.json：`11b705bbc348d15b1cff8f955bcbf9657aa455fc6c558e0e7cc730e778c9d17d`。
- narration.wav：`1441cbb8403d7c8499e9040307d759cb71f8749dc1c85407ab46804d40155b2d`。
- audio/cache.json：`e5aa88122db54aa2b7a000d531929b5a57a79427255958f9d77defbee39f523d`。
- review/check.json：`584654c967595978334779080a460c10414fad19c4ee7d3479ff0a392a5000af`。
- review/check-flags.json：`9be341f7ca0da0268f1bec1d91ee64efe8529760de6319e4ff17a7a6ab49a0e3`。

`audioEvidenceProblems=[]` 已對實際138個clip及整軌的 SHA／sample長度執行驗證；`currentAudioCheck` 仍有138個與當前clip雜湊相符的check。本輪沒有重新聆聽或代寫批准，但此次視覺修正沒有使既有音訊／計時證據失效，無需 TTS 重錄或音訊 refresh。

### 兩鏡修法與實圖限制

已独立看原 `plate-1/2/3.jpg`、`counter-arrival-1.jpg`、`counter-handoff-1.jpg`。三張plate有字／偽字，plate-1另有仿簽名；三個原紀錄均 text=0、passed=false，未清除問題或改分。stylePlate仍保留最高分take1作參照；**plate不是播放場景**，不能將plate字痕直接說成成片有字。此批 manifest 使用 MiniMax image-01；現有 adapter 只轉傳role=character，沒有style reference或seed字段，因此也不能斷言plate內容直接污染生成。它仍被送給judge作風格比較。

真正有播放素材問題的是 arrival 入口偽字、晴日強影與志工／傘架靠右，以及 handoff 把原要求橫放於手間的傘画成頭上完全展開直立傘。兩個新prompt分别要求雨滴／灰天／柔影、空白未標示表面、兩人與動作道具整組在中央三分之一，以及已收合、束帶固定、腰高水平的傘。場景、人物關係、口播含義和虛構揭露仍相同。全域look、其他73鏡、旁白與事實資料均未改。

目前 fault-check 的text問題排除只像字而未形成字母的痕跡，subject問題又排除次要道具／旁人／精確構圖，details缺失可在overall9.29時通過；所以judge pass不取代實圖判斷。**本輪沒有宣稱全75張實圖合格**。兩張replacement的實際像素、無偽字／簽名、閉傘姿態及中央9:16裁切仍需重畫後看；handoff被thumbnail與第一支Short引用，更需要驗裁切後仍看得見兩人手勢和整把閉傘。

pictures_hash正常由 `0ed8c4863968a47f` 變 `a925690ffb4b7568`，visual_hash由 `56a9c16630c0c525` 變 `259647d3b2c4574a`。同look／model／reference／bar下其餘未改shot的image keys與judge stamps可由正常entryStands保留，**不能保留舊storyboard整份manifest hash當作新圖已批准**。新分鏡批准須綁實際重畫後manifest；成片、直式片、品牌presentation、QA、YouTube、G槽備份與刪原件仍是獨立關卡。

私有 `<home>/mokaair-work/ai-series-continuation-20261004/llm-two-shot-source-audit.json` 保存完整結果；helper為 `llm-review/two-shot-source-audit.mjs`。風格路徑與schema限制的完整分析另在 `llm-review/llm-visual-style-audit.md`。本附錄支持最新來源事實結論及不重錄的音訊綁定延續，不代表分鏡或成片完成。

## 兩鏡提示縮版附錄：供應商長度與最新綁定

2026-10-04T12:07:49Z，獨立唯讀窄覆核。當前 video.json SHA-256：**`87fae04fd747036b6016a1bf7508f694223b89081a7ea697fae7556441b3f605`**。本輪只改本報告，沒有 rebuild 來源、TTS、媒體修改、付費或API呼叫。

前次長版只核單一scene prompt的schema長度，漏算MiniMax最終合併Style、Camera與Avoid；長版合併為1644／1640字元，超過實際供應商要求的1500。現將兩鏡縮為423／439個ASCII字元，保留雨天／灰天柔光、空白表面／無signs與字形、兩人手與道具整組在中央三分之一，以及handoff收合、束帶固定、腰高水平傘。前次長版的事實／音訊不變結論仍是有效歷史證據，但不是可成功送出的圖片請求。

| shot | scene prompt ASCII字元 | Style | Negative | 加Style／Camera後 | 再加 `. Avoid: ` 與Negative的實際供應商prompt |
| --- | --- | --- | --- | --- | --- |
| counter-arrival | 423 | 519 | 373 | 968 | **1350** |
| counter-handoff | 439 | 519 | 373 | 985 | **1367** |

獨立將完整原始 `scene.data.prompt + '. Style: ' + look.style + '. Camera: ' + scene.data.camera` 與實際 `shotPrompt` 結果逐字比對，均完全相等；未觸發4000字元slice。再依MiniMaxImages.request_body的實際組合式加入`. Avoid: `及全373字元Negative，得到上表1350／1367，均嚴格少於1500，沒有暗截斷，也沒有刪style、camera或negative來假装符合。來源兩prompt與私有縮版提案逐字相同；lint仍 **0 errors / 0 warnings**。

將当前兩prompt逆替回 `llm-before-visual-fix.json` 的BC基準，完整JSON深度相等、序列化SHA精確回到 `bc87f8b12c07a0039d60dec9f185dccefe5b3f38e65959298bcb5cc249badc5d`。因此**只有counter-arrival.data.prompt、counter-handoff.data.prompt**變動；其餘73個完整送圖提示、138句旁白及id／順序／pause／reveal、claims、voice、look、metadata、章節、字卡、thumb與所有其他資料均不變。claims／demo／Shorts／brief的原終審SHA再核仍相同。36項及補充10項事實結論沿用，沒有額外事實變動。

build.mjs記憶體蒐集器的video.json和draft-metrics.json輸出仍與當前working檔案逐byte相同，未寫來源。108個配音planRequests及138個line keys前後全等；speech_hash仍`5e45b34feaa17c8c`、look_hash仍`ed4c2594703d65d6`，`staleTakes=[]`。依當前audio_samples重建兩版本measured timeline core仍全等。timeline、narration、cache、check與flags完整SHA均與前一附錄列出的音訊證據一致；138clips及整軌SHA／sample綁定再驗`audioEvidenceProblems=[]`，currentAudioCheck仍138，章節check=[]。無需重錄或audio refresh，沒有改任何音訊review hash來取得通過。

當前pictures_hash為`e04741e22fea96fc`、visual_hash為`ac3092e9d3b164a0`。它們正常隨縮版兩prompt更新，不能沿用長版或BC的storyboard整份manifest hash當新分鏡批准；不變鏡可走正常request／verdict重用。前次實圖限制完全維持：plate不是播放鏡、既有judge問題未刪、未聲稱75張實圖全過；新兩圖、無偽字、正確閉傘姿態與中央9:16裁切須看實際replacement後才能驗收。

最新完整私有證據：`<home>/mokaair-work/ai-series-continuation-20261004/llm-two-shot-short-source-audit.json`；helper為`llm-review/two-shot-short-source-audit.mjs`。長版歷史的`llm-two-shot-source-audit.json`保留原雜湊，未冒稱它屬縮版。來源查核延續不等於新圖已畫好、分鏡批准、成片、發布或G槽交付。

## handoff近拍提示附錄：只改一鏡、音訊維持

2026-10-04T12:18:00Z，獨立唯讀窄覆核；最新source SHA-256：**`d9e0929ca0ee0b26f5bf357a2f637564031c7eb91e6b4e7687744a02d4a55990`**。只修改本報告及保存私有證據，不改其他來源、TTS、媒體、manifest或批准，不呼叫API。

將handoff.prompt替回`llm-before-handoff-closeup.json`後，完整JSON及序列化SHA精確回到前版`87fae04fd747036b6016a1bf7508f694223b89081a7ea697fae7556441b3f605`；**本次僅counter-handoff.data.prompt改變**。再將arrival／handoff替回BC基準，JSON及SHA仍精確回到`bc87f8b12c07a0039d60dec9f185dccefe5b3f38e65959298bcb5cc249badc5d`。因此其他73鏡、138句旁白／IDs／順序／pause／reveal、claims、voice、look、章節、字卡與metadata均不變；36項及補充10項事實結果沿用。新的近拍正面描寫兩對手、緊捆狹長綠布、束帶、水平傘軸與彎木柄，移除「No open canopy」等可能強化展開傘的詞；只收窄插圖構圖，不新增人物或數據主張。

handoff提示453個ASCII字元；加完整Style519與原Camera後為999，再加`. Avoid: `及全Negative373後為**1381，嚴格少於1500**。原始完整合併字串與shotPrompt逐字相同，未觸發slice。arrival仍423字元、供應商合併1350；其request key仍`dd16eb1d10450f0a`，目前cached圖SHA為`e72884a08850794ef127b5af1808545f58484d801d13d05c3902e6c353df9f60`，實際檔案雜湊有效、needs_review=false。同model／references／bar下可正常重用，不因本次handoff改稿重買arrival。

108個TTS requests及138個line keys全等；speech_hash仍`5e45b34feaa17c8c`、look_hash仍`ed4c2594703d65d6`。measured timeline core完全相同，timeline／narration／cache／check／flags全檔SHA與前述最新音訊證據相同；138clips與整軌SHA／samples有效，currentAudioCheck=138、staleTakes=[]、audioEvidenceProblems=[]、checkChapters=[]，lint **0 errors／0 warnings**。記憶體建置蒐集器也逐byte再現當前video及metrics，不寫來源。

當前pictures_hash=`3df99b0742dfc545`、visual_hash=`d215b19233361e90`。主代理已另外保留前次三張handoff pilot原件及manifest/cache/ledger；本報告未刪問題或改評分，沒有將該次失敗pilot說成通過。本次近拍replacement仍須實看收合姿態、無字表面、中央9:16裁切及thumb／Short引用；未宣稱75張全圖合格。新storyboard須綁真實新manifest，音訊hash維持原證據。

最新私有審計：`<home>/mokaair-work/ai-series-continuation-20261004/llm-handoff-closeup-source-audit.json`；helper為`llm-review/handoff-closeup-source-audit.mjs`。前版附錄與審計保留歷史。本次來源覆核不代表圖片／分鏡／成片批准、發布或G槽交付。

## 26鏡材料修法附錄

2026-10-04T13:23:11Z，來源差異與音訊完整性覆核者：codex / ai_inventory。本附錄是對凍結來源、保存原件與既有音訊的獨立比對；原完整文字的事實審查仍由上述 llm_review 報告承擔。主代理確認無未解決的來源／音訊差異後，明確授權重新綁定本報告。本輪沒有製作音訊、生成圖片、重評 judge、修改 manifest 或媒體，也沒有將圖片判為核准。

本次 video.json 由 `d9e0929ca0ee0b26f5bf357a2f637564031c7eb91e6b4e7687744a02d4a55990` 變為 **`1eeba48414e32f1778d33f6bdbf0758c23ec00403d651a9f56773554f6a0ae88`**。完整 JSON 葉節點差異只有 26 個 `shot.data.prompt`；其餘 49 個 shot 的 prompt 逐字相同，既有 counter-arrival／counter-handoff 兩鏡修法保留。26 鏡為 bakery-carry、pottery-apprentice、pottery-new-clay、pottery-brief、pottery-bare-table、pottery-limit、demo-six-objects、demo-one-umbrella、demo-cap-out、demo-tools-question、market-request、market-empty-crate、market-boundary、market-key、market-access、market-saved、market-two-roles、market-errors-question、kitchen-counterexample、kitchen-repeat、kitchen-agree、garden-three-baskets、garden-related-token、garden-own-acceptance、garden-follow-up、garden-closing。

移除各 shot 的 data.prompt 後，其餘完整 JSON 的 canonical SHA-256 前後都是 `c24627b94c3f4d87f5302b01b766856ddc8d8a74c61f86cabc87d1dac96d5bd8`。全部 138 個完整旁白 line object（ID、文字、播放順序、停頓及其他欄位）相同，canonical SHA-256 為 `256a93c0ac4518d2e9c55770e0fc7fcc268cf9ed1d38b58200096e65f5736c52`；voice、look、非 prompt 字卡／章節／metadata／camera 與其他欄位不變。brief.md、claims.md、shorts.json 在本次長片來源核對時均與保存版 SHA 相同；原有事實結論與離線示例適用於未改動的文字。authoring ID pool 共 160 個，只消耗 138 個，22 個為未使用保留 ID；冷開場原本便讓 fictional-label 在 counter-arrival 前播放，並非本次改順序，不宣稱未被保存的 22 個 reserve ID 具有前後原件證據。

主代理的 `visual-resume-2030-before-fixes-2026-10-04T13-13-17-635Z` 保存收據含 67 個檔案，本次逐一核實路徑、大小及 SHA，**67／67 有效**，包含舊 source/build、原圖與相關原始評分／證據。舊 build 在攔截檔案寫入的記憶體環境執行，精確重現 D9 來源；目前 build 用相同方法執行兩次，video.json 與 draft-metrics.json 都逐位元重現目前檔案。實際 register／timeline 計算函式照常使用，只攔截輸出，沒有重寫來源。build.mjs SHA-256 為 `83f1fa5d68a87f2f414650ca7a2f87a8b375231c1fffc307fc21a2ed085c33a7`，draft-metrics.json 為 `9051865cabca5e69195010556daa921139f2751407ae3063ffa1edc60bbd608e`。

138 個 WAV 均重新計算完整檔 SHA，逐一核對 timeline／cache／既有獨立音訊審計，PCM 格式及樣本數也一致；138 個 cache request keys 有效，沒有 stale request take。speech_hash 在新舊 source 與 timeline 都是 `5e45b34feaa17c8c`。目前音訊檢查 138／138 effective pass，check-flags 為空；14 項先前 Whisper 第二意見的 raw 檔 SHA、舊檢查 clip SHA 與 heard 文字來源可對回，沒有重新呼叫 ASR。時間軸、整軌、cache／check／flags 與保存版及原音訊審計一致，audioEvidence 無問題：

- timeline.json SHA-256：`11b705bbc348d15b1cff8f955bcbf9657aa455fc6c558e0e7cc730e778c9d17d`，正文 835.1 秒，實際旁白 708.1 秒。
- narration.wav SHA-256：`1441cbb8403d7c8499e9040307d759cb71f8749dc1c85407ab46804d40155b2d`，mono 48 kHz／16 bit，40,084,800 samples。
- audio/cache.json SHA-256：`e5aa88122db54aa2b7a000d531929b5a57a79427255958f9d77defbee39f523d`。
- review/check.json SHA-256：`584654c967595978334779080a460c10414fad19c4ee7d3479ff0a392a5000af`。
- check-flags.json SHA-256：`9be341f7ca0da0268f1bec1d91ee64efe8529760de6319e4ff17a7a6ab49a0e3`。

本機 approvals 原件及 SHA 也與保存版一致，audio-approved 仍綁上述 exact timeline；本次沒有重新 GET 後台，也不把本機快照說成新後台核准。原 llm-final-audio-audit 與 rewrite ledger 的歷史 full source SHA 原封保留；本次 prompt 變更對音訊的有效性，另由上述 138 句／voice／pause、speech hash、實際 WAV／PCM 與時間軸證明。

**視覺仍待修／待審。** 上一輪完整 keyframes 保留 75 個 selected，原工具 8 個 needs_review 仍是 pottery-apprentice、pottery-brief、pottery-bare-table、pottery-limit、market-boundary、market-access、market-saved、garden-related-token；所有原 judge 問題及失敗 take 保留。實看還發現 demo-six-objects 多餘物件、demo-one-umbrella 假字與物件錯置、demo-cap-out 假字且排除動作未呈現、kitchen-counterexample 盤數不符、kitchen-repeat 混流、kitchen-agree 三個非空罐、garden-three-baskets 額外第四籃、garden-follow-up 未留空籃、garden-related-token 寫實且三物件映射不符、garden-closing 可能讀成兩把傘，以及 demo-tools-question 背景印字狀痕跡。這些像素證據不會因 prompt 改寫或分數重評而自行消失；新材料必須實際生成後再看。demo-two-umbrellas 長片原圖可辨認兩把，但中央 9:16 裁切會失去關鍵邊緣，Shorts 全圖呈現仍待來源變更與實際 render／QA。

本次技術核對結果為 **PASS，來源／音訊未解決問題 0 項**；這不代表視覺、分鏡、成片或站主批准，不代表發佈或 G 槽備份／刪除。三鏡新圖 pilot 尚未納入本附錄。完整逐檔與逐鏡差異證據在私有 `llm-material-fix-source-audit-2030.json`／`.md`，舊像素審計及原件保留。

## Short 2 雙傘全圖卡呈現附錄

2026-10-04T13:32:08Z，codex / ai_inventory 獨立窄覆核。此附錄綁定 shorts.json SHA-256 **`2313ae08e1d403158b23c89740f2687c38cec6bdf17be2d76c9578e1cb6707cb`**；長片 source 仍為 `1eeba48414e32f1778d33f6bdbf0758c23ec00403d651a9f56773554f6a0ae88`。相對原 `e71ab40ca34c01537d6818de33c0259af904ebaa422538d4ad3188e550bc84b5`，僅 Short 2 第四場景的 demo-two-umbrellas shot／camera 改為現有 asset 加完整 SHA evidence，其他所有場景、旁白、headline／big／note 與 metadata 完全相同，兩支 validate 均無錯誤。

現有 selected 圖 `keyframes/demo-two-umbrellas-2.jpg` 的 bytes、manifest 與 evidence SHA-256 三方同為 `6a665211331580c3d56d851718b9a8263cc933deb7f365a07e42a65d64c60a0a`，needs_review=false。沒有 camera 的 asset 使用正常 branded card／object-fit:contain，episodeShort 不再補上移動裁切。實際查看私人 preview PNG（SHA-256 `61bd68e103b7e2b9e49c1330244897684b1eddd5efa65595744ac4b716c5d859`），兩個完整彎柄及兩隻握持的手都能辨識，字卡／字幕未遮住圖片。雨傘下段仍受原圖下緣限制；這份單 cue 靜態證據只確認全圖卡解開中心裁切的關鍵限制。

正常 Short 全流程 TTS、render／QA、播放及來源批准仍待執行，本附錄不宣稱 Short 成片或站主核准。未新增付費媒體、改 manifest、重評原 judge 或刪除失敗歷史。私人 `llm-short-contained-audit-2030.json`／`.md` 保存精確差異與 SHA 證據；後續兩景免費字卡 blueprint 尚未套用，不在這份窄審範圍。

## 免費資料卡、六筆揭項與更新音訊綁定附錄

2026-10-04T13:47:40Z，codex / ai_inventory。主代理明確授權在完整來源／PCM、六狀態實圖與正常 audio gate 收據核對後重新綁定本報告。本次窄審 **PASS，來源／音訊／本次卡片呈現未解決問題 0 項**。原完整事實審查仍沿用 llm_review；本附錄不把局部卡片靜態核對寫成整支視覺或成片核准。

目前長片來源 **`9f25b680fe634f7023f88e3f91fd50ceabd29d687592ef2ff1be35312d7a957c`**。從 26 prompt 版 1eeb 到目前，完整 JSON 精確等於三個場景的呈現修正：demo-six-objects 改成 table、market-request 改成 steps，整份 data 複用原有六筆清單／要求—執行—回傳；six-records-table 只改 data，前三個揭項單元各呈現原句的一對紀錄，後三個呈現原句的條件／已領保留／虛構限制。其餘 105 個場景完全不變。從前兩卡版 0a279 到目前，只有原表格 data 改，另外 107 場景精確相同。原 138 個完整 line objects（含 ID、text、pause、reveal 及播放順序）、voice、look、全部仍存在的 73 個 shot data／camera 都相同；前置 demo-six-objects 的獨立六列清單未被一起改成成對表格。全部旁白 canonical SHA 仍 `256a93c0ac4518d2e9c55770e0fc7fcc268cf9ed1d38b58200096e65f5736c52`。

目前 Shorts SHA-256 **`92e301343264c30801ffe2871d5f473bed7e39774f7068098da8e4b3ea3e48f8`**。相對雙傘全圖版 2313，僅 Short 2 首景 remove shot／camera，成為受支援的 branded card；全部旁白、headline／note／數字、其他場景與 metadata 不變。第四景雙傘 explicit asset／evidence 仍綁圖 SHA `6a665211331580c3d56d851718b9a8263cc933deb7f365a07e42a65d64c60a0a`，沒有重買。純來源 validate／episodeShortsProblems、卡片 template 檢查均無錯；正常 Shorts 媒體解析、完整 TTS／播放／QA 與最終批准仍待完成。

舊／新 builder 在攔截寫入的記憶體環境逐位元再現各凍結來源，新 builder 兩次都重現9f25與metrics。current build.mjs SHA為 `b4f118d9c2de6930595bb8cc5206b6eeae057bff9cd4fa7c10947915ce917368`；metrics SHA `ba63a147002f8c0d169d53a0fb3715868e77d7f5910a756c80829532376844f0`。沒有藉更動 shotIndex 讓後續camera輪序漂移。前兩卡22原件與本次表格前5原件的收據均逐一有效，原始媒體／ledger／judge問題在保存快照完整保留。

實際 normal-renderer 的 V1 六張PNG確實曾回報內容超框53px、title即使60%仍放不下；未掩蓋或當作通過。V1私有恢復包透過精確可逆資料patch重建，完整video SHA回到 `3f31671855bd6d35ce1ad2deba2dd269c64b6b1c9149d62ea16c7c4d19690e89`，build與metrics也對回原V1審計；10／10恢復檔及failed PNG bytes／SHA有效，恢復builder同樣byte exact。V2只縮title並把前三對的9個換行分隔改成單行「／」，其他資料、句子與六個reveal不變。

V2六個1920×1080 normal-renderer PNG已全部實際 view_image，逐檔核SHA及前後穩定；renderer六個problems都為空。state0同步呈現L001雨傘未領／L002水瓶已領，state1新增L003雨傘／L004圍巾皆未領，state2新增L005帽子已領／L006手套未領；state3／4／5分別新增按問題篩選、已領紀錄保留、代號與位置可回查及沒有真實失主資料。配對順序清楚，當下口播所講紀錄可見，最後六行未超框／重疊。此證據只確認本張卡六個靜態狀態，不代表完整影片播放或站主驗收；完整PNG SHA保存在私人 `llm-record-reveal-source-audit-2030-v2.json`。

108個正常TTS requests、138個每句keys與前版完全相同；138個WAV全檔SHA、PCM格式／samples逐一對回timeline、cache與原獨立音訊審計。speech hash仍 `5e45b34feaa17c8c`，138／138 effective check，flags=[]、staleTakes=[]、audioEvidenceProblems=[]；沒有新ASR或重錄。root正常執行 `tts --refresh-evidence`，exit0、**0 requests synthesized／0 billable characters／108 reused**。新timeline **`086c5b2c46fb0cc306896d22b708ea31cbf4741a7097601338ec523148306a83`** 對舊11b完整JSON只差 scenes[46].template shot→table與scenes[64].template shot→steps，其他時點／line／音訊證據完全相同。

narration.wav仍 `1441cbb8403d7c8499e9040307d759cb71f8749dc1c85407ab46804d40155b2d`，40,084,800 samples；cache／check／flags全檔SHA皆與前音訊附錄一致。正文835.1秒，73shots／108scenes／138states，最長8.0秒、平均6.0秒；插圖按實測frames算54.600247%，cadenceProblems=[]，仍高於50%。

正常audio submit／pull均exit0，既有paired GET-only收據 `llm-supported-cards-audio-readback-2030.json` 確認新timeline086c的audio review為approved（2026-10-04T13:44:24.612810Z）；本機正常pull在13:44:44.344Z追加同一exact SHA批准，保留舊11b歷史。後台stage為narration approved，ready_to_upload=false。這是系統依設定的音訊核准，不是站主對完整視覺或成片的接受，本覆核者沒有另呼叫後台。

完整73鏡新storyboard仍未完成，其他真實原圖語義／字樣／肢體／風格／裁切失敗與原needs_review、failed takes、judge問題持續保留。兩卡修法是更換不忠實的呈現，不把其原圖片說成通過，也沒有藉刪問題或重評分清零。後續正常keyframes／storyboard／render／assemble／QA／final需依當前來源完成；不宣稱成片、發佈、G槽交付或刪除資格。本次只更新本報告及私人審計，沒有改其他來源、工具、媒體、manifest或旗標。

## 九卡呈現及三提示獨立補充審稿（2026-10-04 22:30）

codex / backup_audit 與 llm_remaining_visual 的私有完整審計由主代理原樣採納結論，沒有把局部審稿寫成成片核准。九卡審計 `llm-nine-freecards-independent-supplement-2030.json` SHA-256 `6c4720fe914aca1d5db795d511bc7a31dd50682cef6779aaafe67824264d1ad5`；三提示付費前審計 `llm-three-prompt-prepay-independent-2030.json` SHA-256 `1f3146417e68b847396de62e7c8e38dd5a32ae711ddee68504452e72dfc55267`。前者綁 9f25 → 1ad01d，後者綁 1ad01d → **`eafefe5847d332e4b1566a81a9a1e6c24463c037c75297364781df281187eb6c`**。

九卡只改九景 template/data，其餘 99 景、138 完整 line objects／reveal／pause／voice/look、108 請求與 138 keys 全同；九卡 16 個实际 renderer states 逐句語義通過。前五卡的 12 個 PNG 與後四卡的四個 PNG 已獨立實看，字fit／layout／glyph 問題為空，原私有 proposal byte exact 套用；沒有以 HTML 語義冒充像素檢查。四新卡保留「不保證」與「若用工具」，沒有新增能力或必然編造的宣稱。demo-one-umbrella 逐字複用既有真離線 trace，另一位覆核者獨立執行兩行輸出 exact，model_called=false。

三提示版本只改 demo-cap-out、kitchen-agree、garden-follow-up 的 prompt，與先審私人提案 exact matching。其餘 105 景／66 shot 完整 objects 與所有旁白、停頓、voice/look、requests、事實／來源都不變。新舊 builder 私有副本各兩次 source 與 metrics byte exact。schema／template／render／episodeShortsProblems=[]；全部合併 MiniMax prompt 實算低於 1,500，最大 1,381，三改景 1,353／1,301／1,336，未截斷。只允許正常針對三鏡小樣，不核准尚未生成的圖。

正文 835.1 秒、實際口播 708.1 秒、138 states、單畫面最長八秒／平均六秒；插圖 51.66247555%，cadenceProblems=[]，沒有增停頓補時。正常零合成 refresh 精確只有八個 timeline.scene.template 改動；新 timeline **`4e1864fba7fabae05367977ca0d38b784757d26b533e3743dbe96e348b3c8925`**，其餘時點／音訊／chapters 完全相同。138 WAV 的完整 SHA／PCM／samples／timeline／cache／current check 均與既有獨立音訊證據相符，138 effective pass、flags0、14 second opinions 仍綁未換的 take。整軌仍 `1441cbb8403d7c8499e9040307d759cb71f8749dc1c85407ab46804d40155b2d`，speech `5e45b34feaa17c8c`，40,084,800 samples。

正常 audio push／pull／GET 已讀回4e1864 exact核准（2026-10-04T14:23:50.220422Z；本機14:24:18.798Z），沒有代人核准。保存38原件與補存四份 cache/review 逐檔 SHA 有效，七個失敗圖及所有原判決保留。此窄審來源／已有效音訊 PASS 不代表完整分鏡、Shorts／成片 audiovisual QA、final／publish／languages／owner接受、G可還原備份或刪除资格；後續三圖真實像素另審。

## 兩卡及 Shorts 完整圖片附錄（2026-10-04 23:10）

最新長片來源 **`2a9bfa4e99d17d1805891f70c56e78416101bc94255c330e96ee62555e14408a`**。獨立 `backup_audit` 的 `llm-final67-source-audio-independent-2030.json` SHA `073263c995db3b3fc597e7d414129404e73fd70db572665774e0dfecb4052e83` 通過限定 source/audio/manifest 核对，未解問題零：eafefe 到 2a9 只有 demo-cap-out table 与 garden-follow-up steps 的 template/data；106 其餘景、138 完整句子／reveal／pause、108 requests／138 keys／voice/look／頂層及 claims 完全不變，新舊 private builder 各兩次 byte exact。水瓶 L002 與帽子 L005 均已領，另一位覆核者獨立離線重算；沒有新模型呼叫。兩個 normal-renderer PNG 已 root 與獨立覆核者實看，無溢出；私有 `llm-last-two-freecards-proposal-2030/preview-independent-2030.json` SHA `836b54412ab382ca8bdba2b90cc3470533ff7c2d84dcd3bf2ce51624801eb80b`。原兩張失敗圖、六個付費 takes 及全部原判保留。

正文835.1秒、实音708.1秒、138 states、最長八秒／平均六秒、插圖50.1576657486%，cadence/schema/template/render/audioEvidence Problems=[]。正常 refresh 仍0synth／0billable／108reuse，timeline **`3b57a6f54b78cd5267c6a6b2898bd87e5650121a7da8dbceb78d81f03b6f7e02`** 對4e1864精確只兩個scene.template字段；138 WAV／PCM／cache／check／14同take第二意見均未變，flags0，narration1441cbb8403d7c8499e9040307d759cb71f8749dc1c85407ab46804d40155b2d。正常 audio 核准14:48:55.899493Z，pull14:50:04.677Z，root GET同SHA。

正常 keyframes 完整67鏡整理 exit0、0新生成，67原圖完整 entry／judge byte-equivalent，picture hash e24bc7ae75d0db0b；manifest **`b008c55cf9bf913d010870c66ae5cfe06db0d823a34cf09bf9f52066bfe50c31`** 精確移出兩張已改卡的歷史 entries並重新產生三張24／24／19 contact sheets。ledger/cache/jobs字節不變，累計US$2.268、174 images／168 judges，沒有 pending jobs／STOP。67/67 actual selected fullSHA能對回先前真實 view_image 審稿；覆蓋表 `llm-67-selected-pixel-coverage-2030.json` SHA bc1db5038f14278aaf47b72c8fb16b875de1cc74f7960d6d1f5a76b9ea632297。這是實看覆蓋，**不是67圖的接受率**：51圖60條原警告與 garden-three-baskets 的參與人物／裁切 HOLD 全保留；沒有刪 judge.problems、重評分追分或代人核准。正常67全板於15:01:39.984653Z送審，exact b008 的 review 目前 **pending**、decided_at=null；後台列表 stage 字串不取代這項當前核准狀態。

最新 Shorts **`b70535ce3c920a88c451cbc589ed63f9a9e16168a9c15d9806828fb8915a06a0`**：先從92e301移除兩個已改卡的 shot refs，全部20句／headlines／big／notes／metadata不變；再僅 Short1 scene0與scene3改 supported contained assets，新增兩筆 current selected fullSHA evidence，其餘八scene與Short2 exact。全束傘／完整彎柄／接物手及三籃完整rim在兩個真正 normal sceneHtml→backgroundChain／segmentArgs→ffmpeg 的isolated first-frame PNG 都可見，字幕標準區域沒有重疊，四caption DOM fit Problems=[]。root與獨立覆核實看；`llm-short1-two-contained-proposal-2030/preview-independent-2030.json` SHA68e66ffb354501e9ddbc44a6943e9099c2bd33fc46b7ccff548a0b7e0620f357，另有獨立schema/evidence覆核。原黃色環／束帶位置、单人物≠两邻居等原判未因contain消除；沒有incoming dissolve，完整Short播放／TTS／QA仍未完成。三筆共享全圖assets須留到其消費者完成。

正常 local fullfilm render 已開始，後續assemble/captions/QA/package僅供可看的本機待審稿；不越過 pending storyboard 門檻送final/publish，不宣稱selected languages已決定或完成，不啟動上傳／发布，沒有G備份或刪除資格。原完整fact conclusions適用未改的文字；此附錄不核准完整影像／聲音播放、站主接受或上架。
