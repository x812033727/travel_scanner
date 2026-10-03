# 查證與編輯紀錄：ai-term-ai-alignment

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律 2026-10-03（本批開工日，當天實際打開）。UA 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，全部 `curl -sSL`，狀態碼 200；arXiv 同時讀 abs 頁與 PDF（pdftotext）核對內文。
本檔已依兩輪查核（verify-1.md、verify-2.md）改過的正文同步，下列每條都對應目前 `pack.json` 的寫法。

## 定義分歧（表格與第一節）

InstructGPT 論文寫「對齊的定義長期以來是模糊而混亂的話題，有多種互相競爭的提案（Chen 2021、Leike 2018、Gabriel 2020）」｜https://arxiv.org/abs/2203.02155 （PDF 3.6 節 Evaluation）｜2026-10-03｜curl abs 與 pdf
Leike 等人 2018（DeepMind 作者群）把 agent alignment problem 定為「如何建立依使用者意圖行事的代理」；理由是使用者對任務目標只有隱含的理解，所以獎勵函數難設計（"the user only has an implicit understanding of the task objective"）。表格 Leike 列照這兩點寫；「不只照字面」那種區分指令與意圖的框架是 Gabriel 的，不是 Leike 的｜https://arxiv.org/abs/1811.07871｜2026-10-03｜curl abs 與 pdf（摘要與第 1 節 Introduction）
Askell 等人 2021（Anthropic 作者群）以 helpful、honest、harmless 定義「aligned」，承認準則含糊且需取捨（例：有幫助與無害衝突）｜https://arxiv.org/abs/2112.00861｜2026-10-03｜curl abs 與 pdf（1.1 節 What are Helpfulness, Honesty, and Harmlessness；附錄 E）
HHH「彼此可能衝突、最佳行為是取捨」｜同上｜2026-10-03｜同上
什麼算有害因人與文化而異，部署者要為對齊如何定義負責｜同上（Harmless 項最後一點與該節結尾句）｜2026-10-03｜同上
Hadfield-Menell 等人 2016（UC Berkeley）提出價值對齊問題的形式化定義（合作式逆強化學習 CIRL；機器人與人都依人的獎勵函數計分，但機器人一開始不知道它）｜https://arxiv.org/abs/1606.03137｜2026-10-03｜curl abs 與 pdf（摘要與第 1 節；演算法部分未用）
Gabriel 2020（DeepMind）：對齊的對象有六種——指令、（表達出的）意圖、（行為顯示的）偏好、（充分了解後的）偏好、利益、價值｜https://arxiv.org/abs/2001.09768｜2026-10-03｜curl abs 與 pdf（摘要與 2 節 i–vi 六項；「informed preferences」我譯為充分了解後的偏好）
Gabriel：核心難題（"the central challenge"）不是找出「真」的道德原則，而是找出在價值觀分歧下仍能經反思而被接受的公平原則｜同上（摘要第三個主張）｜2026-10-03｜同上

## InstructGPT 如何操作化（第二節）

沿用 Leike 的「依使用者意圖」，並用類似 Askell 的 HHH 框架｜https://arxiv.org/abs/2203.02155｜2026-10-03｜pdf 3.6 節
手段是 SFT（示範）→ 比較排序資料訓練獎勵模型 → RLHF（PPO）｜同上（摘要與第 3 節）｜2026-10-03｜同上
有幫助：主要指標是標註者偏好評分；標註者不是寫提示詞的人，可能與使用者原意有落差｜同上 3.6 節｜2026-10-03｜同上
誠實：無法直接量模型「信念」，改量真實性：封閉領域任務（輸出不該含輸入沒有的資訊，例如摘要、封閉領域問答，見第 1 節）裡編造資訊的傾向，加上 TruthfulQA；且「只涵蓋真實性的一小部分」。正文寫成「摘要這類只該依輸入內容作答的任務」｜同上 3.6 節與第 1 節｜2026-10-03｜同上
無害：早期請標註者判斷「potentially harmful」後來停用（需猜測輸出如何被使用）；改用代理準則（客服情境不適當、貶低受保護族群、性或暴力內容）加 RealToxicityPrompts、CrowS-Pairs｜同上 3.6 節｜2026-10-03｜同上（文中只寫了前兩項準則與「毒性與偏見資料集」）
訓練標註者（產出訓練資料的那批人）彼此一致率 72.6 ± 1.5%；另找的保留標註者為 77.3 ± 1.3%（文中未寫）。論文沒有說明這個比率是在哪一種標註任務上量的，所以正文不寫「比較回答時」；5.2 節把同一數字寫成「約 73%」，並說他們在許多例子上意見不一｜同上 3.4 節與 5.2 節｜2026-10-03｜同上
標註者多半為住在美國或東南亞、透過 Upwork 或 Scale AI 聘用的英語使用者｜同上 5.2 節與附錄 B｜2026-10-03｜同上
對齊到：產出訓練資料的標註者給的示範與偏好、研究者寫給標註者的指示（論文說是對齊到研究者自己的偏好，透過標註指示）、OpenAI API 客戶送來的提示詞（間接）｜同上 5.2 節｜2026-10-03｜同上
「不主張研究者、標註者或客戶是偏好的正確來源」；「不可能訓練出同時符合每個人偏好的系統」｜同上 5.2 節｜2026-10-03｜同上
在其 API 提示分布上（"on our prompt distribution"），人工評估較偏好 1.3B（13 億參數）InstructGPT 的輸出，勝過 175B（1,750 億參數）的 GPT-3。正文依系列規矩不寫 GPT-3，改寫成「沒經過這套微調的基礎模型」，設定寫成「以論文取自 API 的提示做人工評估」｜https://arxiv.org/abs/2203.02155（摘要）｜2026-10-03｜curl abs；只寫該論文在其提示分布與人工評估下的結果，不推廣
「模型既非完全對齊也非完全安全」；仍產生有毒或有偏見輸出、編造事實；多半照使用者指示做，即使可能造成真實傷害｜同上 5.3 節 Models 段｜2026-10-03｜pdf

## HHH 與憲法式 AI（第三節）

HHH 選擇理由：簡單好記、涵蓋大部分想從對齊 AI 得到的特質；準則含糊｜https://arxiv.org/abs/2112.00861｜2026-10-03｜pdf 1.1 節
對齊技術的進展不綁定特定價值（"do not depend on any specific choice for these values"），也可被用來訓練做壞事（錯誤資訊、審查、壓迫）的系統｜同上（第 5.2 節 Broader Impacts，"The road to hell is paved with good intentions…"）｜2026-10-03｜pdf
憲法式 AI 兩階段。監督階段：拿誘導有害內容的紅隊提問讓只練過有幫助性的 RLHF 模型回答，再請它依原則批評、改寫自己的回應；每一步從 16 條原則隨機抽一條，可反覆多輪；最後用改寫結果（加上有幫助性的樣本）微調一個預訓練模型（3.1、3.2 節；摘要寫 "the original model"，正文不寫是哪一個模型）。RL 階段：由另一個獨立的回饋模型（通常是預訓練模型）依隨機抽出的原則判斷兩個回應哪個較無害→與人類的有幫助性標註混合訓練偏好模型→RL，即 RLAIF（4.1 節）｜https://arxiv.org/abs/2212.08073｜2026-10-03｜curl abs 與 pdf（1.2、3.1、3.2、4.1 節與 Figure 1）
無害性方面人的監督只來自一份原則清單和少量 few-shot 提示範例，有幫助性仍用人類標註（混合人類／AI 偏好模型）｜同上 1.2 節（"human supervision will come entirely from a set of principles … along with a small number of examples used for few-shot prompting"）；摘要的說法省略了範例｜2026-10-03｜同上
作者說原則是為研究「以相當臨時且反覆調整的方式」挑選（"fairly ad hoc and iterative"），未來應由更多利害關係人修訂並依使用情境調整｜同上 第 1 節腳註 2 與第 3.3 節腳註 7｜2026-10-03｜同上

## 失敗型態（第四節）

規格鑽漏洞定義（滿足目標字面規格卻沒達到預期結果）；疊積木例：設計者要紅積木疊到藍積木上，獎勵是紅積木「底面」的高度（原文另有 "when it is not touching the block" 的條件，正文省略），代理把紅積木翻過來讓底面朝上拿分。原文沒有「離地」二字，第二輪查核已刪；原始研究為 Popov 等人 2017，該文引用，正文寫成「文中引用一個疊積木實驗」｜https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ （文章日期 2020-04-21，作者 Krakovna 等）｜2026-10-03｜curl；舊網址 deepmind.google/discover/blog/… 會轉到此網址
迎合：分析 hh-rlhf 資料集裡有幫助性的部分，用 Bayesian logistic regression 在「其他條件相同」下比較特徵，回答符合使用者看法時較容易被偏好（4.1 節）；結論為「likely driven in part by」偏好判斷｜https://arxiv.org/abs/2310.13548｜2026-10-03｜curl abs 與 pdf（摘要與 4.1 節；細節留給 ai-term-sycophancy）
客服「按已解決」例：自編示例，標明假設、未實測，無外部來源

## 三個層次（第五節）

對齊「多半在訓練階段做」：不寫成「發生在訓練階段」，因為 Askell 等人把提示詞（prompting）也當成對齊介入來測試（摘要 "simple baseline techniques … such as prompting"）｜https://arxiv.org/abs/2112.00861｜2026-10-03｜pdf 摘要
NeMo Guardrails：輸入、檢索、對話、執行、輸出等 rails 在 LLM 互動的不同階段執行；可在模型呼叫前後加防護而不改應用使用的模型｜https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/overview｜2026-10-03｜curl（Core Building Blocks 與 Benefits 兩段）
Anthropic Usage Policy 適用於所有能向其產品送出輸入的人；有偵測與監控；違規可被限流、停權或終止；輸入違規時可封鎖或修改輸出｜https://www.anthropic.com/legal/aup｜2026-10-03｜curl；頁面標示 Effective September 15, 2025（文中不寫日期）
OpenAI Model Spec：描述預期行為；「正在訓練模型向 Model Spec 對齊」；「正式模型尚未完全反映 Model Spec」；Model Spec 只是其中一部分，由使用政策（規範人怎麼用 API 與 ChatGPT）與安全措施（測試、監控、緩解）補足，後兩者是 Model Spec 以外的文件與流程｜https://model-spec.openai.com/2026-08-18.html｜2026-10-03｜curl 該日期頁（Overview 段）。版本：https://model-spec.openai.com/version-manifest.json 今天回 `{"latest_version": "2026-08-18"}`，與頁面 `data-model-spec-version` 相同；GitHub CHANGELOG 最上面一筆也是 v2026.08.18。頁面原始 HTML 裡的「A newer version of the Model Spec is available」橫幅預設 `hidden`，只有 manifest 的版本和頁面不同時，頁上的腳本才會打開它，所以讀者今天看不到。根網址只是 meta refresh 空殼，不當來源。OpenAI 改版後這頁會開始顯示橫幅，上線前再看一次 manifest，必要時換成新日期頁並重核 Overview。

## 圖與其他數字

diagram-1.svg 無任何數字（版權列的 2026 與表格說明的「2026 年 10 月」對應）。
文中數字清單：2016、2018、2020、2021（表格年份）；72.6%；13 億、1,750 億；「2026 年 10 月」（表格說明）——皆已在上列有來源。
未使用的來源：openai.com/policies/usage-policies（HTTP 403，改用 Anthropic 政策頁做「內容政策」例子）。
不寫任何模型名稱、價格、截止日期或排行榜分數；Model Spec 版本日期與 Anthropic 政策生效日皆未寫入正文。InstructGPT 是指派點名的論文名，保留。

## 編輯紀錄

標題由草稿「讓系統做的事符合人的意圖」改寫：該句只是意圖對齊一種說法，與全文「定義有分歧」的主題衝突。
自編示例（客服「按已解決」獎勵、虛構產品頁）皆標示假設／虛構，沒有實測，也沒有把想像的模型輸出寫成觀察。
圖解與 hero 皆為手繪 SVG（非 AI 產圖）。hero 為對話框、箭與靶；無文字、無 logo。
第一輪查核（verify-1.md）：改 Leike 列、72.6% 的設定、憲法式 AI 的人類監督（補 few-shot 範例）、對齊「多半」在訓練階段、Model Spec 與使用政策的關係，並補「本文採用的說法」一句。
第二輪查核（verify-2.md）：憲法式 AI 兩階段補上紅隊提問、每輪隨機抽一條原則、可反覆、第二階段由另一個模型判斷；疊積木例刪掉原文沒有的「離地」，說清楚是翻面讓底面朝上；其餘為給一般讀者的措辭調整。

純正文字數（_body_length 算法，含段落、清單、表格表頭與格子、callout、rich_paragraph 的全部文字含連結文字）：2771 字元；不含連結文字約 2702。
