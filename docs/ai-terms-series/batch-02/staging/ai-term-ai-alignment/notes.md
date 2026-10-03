# 查證與編輯紀錄：ai-term-ai-alignment

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律 2026-10-03（本批開工日，當天實際打開）。UA 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，全部 `curl -sSL`，狀態碼 200；arXiv 同時讀 abs 頁與 PDF（pdftotext）核對內文。

## 定義分歧（表格與第一節）

InstructGPT 論文寫「對齊的定義長期以來是模糊而混亂的話題，有多種互相競爭的提案（Chen 2021、Leike 2018、Gabriel 2020）」｜https://arxiv.org/abs/2203.02155 （PDF 3.6 節 Evaluation）｜2026-10-03｜curl abs 與 pdf
Leike 等人 2018（DeepMind 作者群）把 agent alignment problem 定為「如何建立依使用者意圖行事的代理」｜https://arxiv.org/abs/1811.07871｜2026-10-03｜curl abs 與 pdf（摘要與 Introduction）
Askell 等人 2021（Anthropic 作者群）以 helpful、honest、harmless 定義「aligned」，承認準則含糊且需取捨（例：有幫助與無害衝突）｜https://arxiv.org/abs/2112.00861｜2026-10-03｜curl abs 與 pdf（1.1 節 What are Helpfulness, Honesty, and Harmlessness；附錄 E）
HHH「彼此可能衝突、最佳行為是取捨」｜同上｜2026-10-03｜同上
什麼算有害因人與文化而異，部署者要為對齊如何定義負責｜同上（Harmless 項最後一點與該節結尾句）｜2026-10-03｜同上
Hadfield-Menell 等人 2016（UC Berkeley）提出價值對齊問題的形式化定義（合作式逆強化學習 CIRL；機器人與人都依人的獎勵函數計分，但機器人一開始不知道它）｜https://arxiv.org/abs/1606.03137｜2026-10-03｜curl abs 與 pdf（摘要；只引用摘要層級的說法，未讀完演算法部分）
Gabriel 2020（DeepMind）：對齊的對象有六種——指令、（表達出的）意圖、（行為顯示的）偏好、（充分了解後的）偏好、利益、價值｜https://arxiv.org/abs/2001.09768｜2026-10-03｜curl abs 與 pdf（摘要與 2 節 i–vi 六項；「informed preferences」我譯為充分了解後的偏好）
Gabriel：最難的不是找出「真」的道德原則，而是找出在價值觀分歧下仍能經反思而被接受的公平原則｜同上（摘要第三個主張）｜2026-10-03｜同上

## InstructGPT 如何操作化（第二節）

沿用 Leike 的「依使用者意圖」，並用類似 Askell 的 HHH 框架｜https://arxiv.org/abs/2203.02155｜2026-10-03｜pdf 3.6 節
手段是 SFT（示範）→ 比較排序資料訓練獎勵模型 → RLHF（PPO）｜同上（摘要與第 3 節）｜2026-10-03｜同上
有幫助：主要指標是標註者偏好評分；標註者不是寫提示詞的人，可能與使用者原意有落差｜同上 3.6 節｜2026-10-03｜同上
誠實：無法直接量模型「信念」，改量真實性，用封閉領域任務的編造資訊傾向與 TruthfulQA，且「只涵蓋真實性的一小部分」｜同上 3.6 節｜2026-10-03｜同上
無害：早期請標註者判斷「potentially harmful」後來停用（需猜測輸出如何被使用）；改用代理準則（客服情境不適當、貶低受保護族群、性或暴力內容）加 RealToxicityPrompts、CrowS-Pairs｜同上 3.6 節｜2026-10-03｜同上（文中只寫了前兩項準則與「毒性與偏見資料集」）
訓練標註者彼此一致率 72.6 ± 1.5%（比較回答任務；保留標註者為 77.3 ± 1.3%，文中未寫）｜同上 3.4 節｜2026-10-03｜同上。文中的「72.6%」只指訓練標註者
標註者多半為住在美國或東南亞、透過 Upwork 或 Scale AI 聘用的英語使用者｜同上 5.2 節與附錄 B｜2026-10-03｜同上
對齊到：訓練標註者的示範與偏好、研究者自己寫的標註指示、OpenAI API 客戶送來的提示詞（間接）｜同上 5.2 節｜2026-10-03｜同上
「不主張研究者、標註者或客戶是偏好的正確來源」；「不可能訓練出同時符合每個人偏好的系統」｜同上 5.2 節｜2026-10-03｜同上
在其 API 提示分布上，人工評比較偏好 1.3B（13 億參數）的 InstructGPT 勝過 175B（1,750 億參數）的 GPT-3｜https://arxiv.org/abs/2203.02155（摘要）｜2026-10-03｜curl abs；只寫該論文在其提示分布與人工評比下的結果，不推廣
「模型既非完全對齊也非完全安全」；仍產生有毒或有偏見輸出、編造事實；多半照使用者指示做，即使可能造成真實傷害｜同上 5.3 節 Models 段｜2026-10-03｜pdf

## HHH 與憲法式 AI（第三節）

HHH 選擇理由：簡單好記、涵蓋大部分想從對齊 AI 得到的特質；準則含糊｜https://arxiv.org/abs/2112.00861｜2026-10-03｜pdf 1.1 節
對齊技術不取決於特定價值，也可被用來訓練做壞事（錯誤資訊、審查、壓迫）的系統｜同上（第 5.2 節 Broader Impacts，"The road to hell is paved with good intentions…"）｜2026-10-03｜pdf
憲法式 AI 兩階段：監督階段（依原則批評、改寫、再微調）；RL 階段（模型依原則比較兩個回應→偏好模型→RL，即 RLAIF）｜https://arxiv.org/abs/2212.08073｜2026-10-03｜curl abs 與 pdf（1.2 節與 Figure 1）
無害性的人類監督只來自一份原則清單，有幫助性仍用人類標註（混合人類／AI 偏好模型）｜同上 摘要與 1.2 節｜2026-10-03｜同上（論文另提到少量 few-shot 範例，文中以摘要說法為準）
作者說原則是為研究「ad hoc」挑選，未來應由更多利害關係人修訂並依使用情境調整｜同上 第 1 節腳註 2 與第 3.3 節腳註 7｜2026-10-03｜同上

## 失敗型態（第四節）

規格鑽漏洞定義（滿足目標字面規格卻沒達到預期結果）；疊積木例（獎勵為紅積木底面高度，代理把紅積木翻面；原始研究為 Popov 等人 2017，由該文轉述）｜https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ （文章日期 2020-04-21，作者 Krakovna 等）｜2026-10-03｜curl；舊網址 deepmind.google/discover/blog/… 會轉到此網址
迎合：分析既有人類偏好資料，回答符合使用者看法時較容易被偏好；結論為「likely driven in part by」偏好判斷｜https://arxiv.org/abs/2310.13548｜2026-10-03｜curl abs（只讀摘要；全文與細節留給 ai-term-sycophancy）
客服「按已解決」例：自編示例，標明假設、未實測，無外部來源

## 三個層次（第五節）

NeMo Guardrails：輸入、檢索、對話、執行、輸出等 rails 在 LLM 互動的不同階段執行；可在模型呼叫前後加防護而不改應用使用的模型｜https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/overview｜2026-10-03｜curl（Core Building Blocks 與 Benefits 兩段）
Anthropic Usage Policy 適用於所有能向其產品送出輸入的人；有偵測與監控；違規可被限流、停權或終止；輸入違規時可封鎖或修改輸出｜https://www.anthropic.com/legal/aup｜2026-10-03｜curl；頁面標示 Effective September 15, 2025（文中不寫日期）
OpenAI Model Spec：描述預期行為；「正在訓練模型向 Model Spec 對齊」；「正式模型尚未完全反映 Model Spec」；由使用政策與安全措施（測試、監控、緩解）補足｜https://model-spec.openai.com/2026-08-18.html｜2026-10-03｜curl 該日期頁（Overview 段）。注意：網站根網址 https://model-spec.openai.com/ 只回 234 位元組的 meta refresh 空殼（轉到 2026-08-18.html），該日期頁頂端卻顯示「A newer version of the Model Spec is available」，「Read latest version」又連回根網址，形成循環；WebSearch 摘要也說最新版為 2026-08-18。我引用的是 Overview 的結構性敘述，與版本細節無關；請協調者上線前再看一次。

## 圖與其他數字

diagram-1.svg 無任何數字（版權列的 2026 與表格說明的「2026 年 10 月」對應）。
文中數字清單：2016、2018、2020、2021（表格年份）；72.6%；13 億、1,750 億；「2026 年 10 月」（表格說明）——皆已在上列有來源。
未使用的來源：openai.com/policies/usage-policies（HTTP 403，改用 Anthropic 政策頁做「內容政策」例子）。
不寫任何模型名稱、價格、截止日期或排行榜分數；Model Spec 版本日期與 Anthropic 政策生效日皆未寫入正文。

## 編輯紀錄

標題由草稿「讓系統做的事符合人的意圖」改寫：該句只是意圖對齊一種說法，與全文「定義有分歧」的主題衝突。
自編示例（客服「按已解決」獎勵、虛構產品頁）皆標示假設／虛構，沒有實測，也沒有把想像的模型輸出寫成觀察。
圖解與 hero 皆為手繪 SVG（非 AI 產圖）。hero 為對話框、箭與靶；無文字、無 logo。

純正文字數（_body_length 算法，含段落、清單、表格格子、callout、rich_paragraph 的全部文字含連結文字）：2491 字元；不含連結文字約 2410。
