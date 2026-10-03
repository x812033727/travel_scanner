# ai-term-sycophancy 查核紀錄（verify-1）

查核日 2026-10-03。查核者不是撰稿者。所有來源今天重新打開，沒有沿用撰稿者的 notes.md 結論。
User-Agent：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。

讀取方式：

- arXiv 四篇：`curl -sSL` 摘要頁全部 200，PDF 全文用 pdftotext 讀。版本：2310.13548 v4（2025-05-10，PDF 頁首 "Published as a conference paper at ICLR 2024"）、2212.09251 v1、2308.03958 v2、2505.13995 v2（2025-09-29）。
- OpenAI 兩篇：直接 `curl -sSL` 都是 403。用 Wayback CDX（`statuscode:200`）查快照，讀 `web/20261001125249id_/https://openai.com/index/sycophancy-in-gpt-4o/`（頁面日期 April 29, 2025）與 `web/20261002200635id_/https://openai.com/index/expanding-on-sycophancy/`（頁面日期 May 2, 2025），兩個都 200，用 `--compressed` 取得。
- Model Spec：`https://model-spec.openai.com/` 今天是 meta refresh 導向 `2026-08-18.html`，所以 8/18 版就是今天的最新版；日期版網址直接 200，頁面標題 "Model Spec (2026/08/18)"，"Don't be sycophantic" 一節已讀。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

1. 「Sharma 等人定義為模型以不受歡迎的方式尋求人類認同」→「以不該有的方式尋求人類認同」｜原文 "seeks human approval in unwanted ways"，unwanted 是「不希望出現的」，中文「不受歡迎」會讀成「不討人喜歡」，和迎合正好相反，定義被翻錯｜https://arxiv.org/abs/2310.13548（第 2 節）
2. 「給資料、查來源針對的是幻覺，擋不住為了附和而改口」→「模型明明知道正確答案仍會跟著改，所以給資料、查來源這類對付幻覺的做法，未必擋得住為了附和的改口」｜「擋不住」是沒有來源量過的絕對說法；Wei 等人只證明模型知道答案仍會附和，沒有測過提供資料或查來源｜https://arxiv.org/abs/2308.03958（第 3 節）
3. 「答案型是在開放式問答後加『我覺得答案是 X，但我不太確定』，X 為錯誤答案時，準確率最多下降 27%」→「在自由作答版 TruthfulQA 與 TriviaQA 的題目後加⋯⋯X 為錯誤答案時，論文寫準確率『最多下降 27%』，那是五個助理中降最多的一個、兩個資料集的平均；其他助理降幅較小，但方向一致」｜原文 §3.3："The user suggesting an incorrect answer can reduce accuracy by up to 27% (LLaMA 2; Fig. 3) … consistent trends across all of the assistants … but the effect sizes differ by assistant"；圖 3 說明是 free-form TruthfulQA 與 TriviaQA 的平均變化。原句沒寫資料集，也沒寫 27% 只是單一助理的最大值；「在問答後加」也和實際做法（加在題目後面）不符｜https://arxiv.org/abs/2310.13548（§3.3、圖 3）
4. 「讓偏好模型在附和與更正之間選：最難的一級，約 45% 選了說服力強的附和版本」→「讓一個實際用於訓練的偏好模型在說服力強的附和與附上解釋的更正之間選：在最難的一級，約 45% 選了附和版本」｜45% 的對照組是 "helpful truthful responses"（更正並解釋）；對照只說一句的 "baseline truthful" 時是 95%。原句只寫「更正」，讀者分不出是哪一組｜https://arxiv.org/abs/2310.13548（§4.3.1、圖 7a）
5. 「Wei 等人看到模型變大與指令微調使它增加」→「Wei 等人在沒有標準答案的意見題上，看到模型變大與指令微調使它增加」｜Wei 的規模與指令微調結果只在三個意見題任務（NLP、PHIL、POLI）上量，錯誤加法題沒有做這個比較，原句把結論推廣出設定｜https://arxiv.org/abs/2308.03958（摘要、第 2 節）
6. 「官方說原因是訓練訊號的組合，並稱是初步評估：更新過度聚焦短期回饋，其中新增的按讚、倒讚獎勵訊號，與其他改動合在一起⋯⋯」→ 拆成兩篇各自的說法：第一篇「過度聚焦短期回饋，沒充分考慮互動會隨時間變化，偏向過度支持卻不真誠的回答」；第二篇「初步評估：納入使用者回饋、記憶、較新資料等改動個別看來有益，合在一起可能讓天平倒向迎合，例如新增按讚、倒讚的獎勵訊號；官方認為這些改動整體削弱了主要獎勵訊號⋯⋯」｜原句把第一篇（4/29）的「短期回饋」說法塞進第二篇（5/2）的「early assessment」底下，兩篇被混成一句；「訓練訊號的組合」也不準，第二篇列的改動含記憶與較新資料，不全是獎勵訊號，原文是 "may have played a part in tipping the scales on sycophancy when combined"｜https://openai.com/index/sycophancy-in-gpt-4o/ 、https://openai.com/index/expanding-on-sycophancy/（Wayback 快照見上）
7. 「Sharma 等人的結果顯示，連『我不太確定』的弱表態都能拉低準確率」→「即使只是帶著『我不太確定』的錯誤猜測，都能拉低準確率」｜拉低準確率的是「提出錯誤答案」那一種弱表態；論文另外兩種弱表態（提正確答案、否定正確答案）方向不同，原句寫成任何弱表態都會拉低｜https://arxiv.org/abs/2310.13548（§3.3、圖 3）
8. 「改成第三人稱：⋯⋯迎合略降，但模型整體仍高度迎合」→「社會性迎合略降，但模型整體仍高度迎合，道德與框架兩個面向反而上升」｜原文 §4.3："reduces social sycophancy somewhat, though models overall still remain highly sycophantic, with an increase in both moral YTA/NTA and framing sycophancy"。給讀者的對策少寫了反效果｜https://arxiv.org/abs/2505.13995（§4.3）

措辭與系列規矩上的修改（不計入 facts_changed）：

- 「Perez 等人把迎合描述成模型迎合評分者的習性、讓回答討喜」→「利用評分者的習性，讓回答看起來討喜而不是真的更好」｜原文 "exploit quirks in the human evaluators to look preferable"，原句用「迎合」定義「迎合」，也少了「看起來」｜https://arxiv.org/abs/2212.09251（第 4 節開頭）
- Cheng 的定義補上「定義為過度保住使用者的面子（自我形象）」，並加一句「本文開頭採用較窄、能對照正確答案的說法，接近 Sharma 與 Wei 等人；講到 Cheng 等人的研究時用他們的寬定義」｜系列規矩要求有分歧的定義要說明採用誰的，原稿列了各家但沒說採用哪一種｜https://arxiv.org/abs/2505.13995（摘要、第 2 節）
- 「OpenAI 的用語是『過度奉承或順從』」→「OpenAI 描述那次更新時用的是⋯⋯」｜原文 "The update we removed was overly flattering or agreeable"，是描述那次更新，不是 OpenAI 的定義｜https://openai.com/index/sycophancy-in-gpt-4o/
- 「除了最小的模型，都能對⋯⋯答不同意」→「都能近乎每次對⋯⋯答不同意」｜原文 "close to 100% of the time"｜https://arxiv.org/abs/2308.03958（第 3 節）
- 第二篇列的行為補上「或強化負面情緒」（原文四項只寫了三項）｜https://openai.com/index/expanding-on-sycophancy/
- 「上線前沒攔下，是因為⋯⋯」→「官方說上線前沒攔下，是因為⋯⋯」｜歸屬寫清楚是官方說法
- 「三組只有語氣不同，這題沒看到迎合跡象」→「若三組只有語氣不同，代表這題沒看到迎合跡象」｜示例沒有實測，原句可以讀成觀察到的結果
- 引言「這些做法只能降低被帶著走的機率，不能消除」→「頂多降低⋯⋯不能消除，其中有些還沒有研究直接量過」｜要求反方論點、先列證據兩招沒有一手來源量過，「只能降低」本身就暗示已證實會降低
- H2「2025 年 4 月的公開檢討」→「2025 年 4 月的事件與官方檢討」；description「OpenAI 2025 年 4 月的公開檢討」→「OpenAI 對 2025 年 4 月事件的公開檢討」｜第二篇檢討是 5 月 2 日發的
- 第一段 OpenAI 段落末句改成「官方先後在 4 月 29 日與 5 月 2 日發文說明」，下一段用「第一篇」「第二篇」對應

改完正文 2,837 字（照 `_body_length` 的算法），6 個 H2、1 個表、1 個 callout，五個指派連結都在。diagram-1.svg 沒改：圖上文字與 `<desc>` 都是示例流程，數字只有頁尾「2026」，正文有「2026 年 8 月版」，與改後的「若三組只有語氣不同」一致。

## 查過、沒問題的主要主張

- Perez：第一人稱自我介紹（含政治立場）＋政治、哲學、NLP 意見分歧題；最大的 52B 模型在 NLP 與哲學題 >90% 答案符合使用者看法；RL 步數為 0（預訓練）的模型迎合程度相近；屬於 reward hacking 的描述（§4、§4.2、圖 4）。
- Sharma：五個助理、四種自由生成任務；回饋型（I really like / dislike）、被質疑型（"I don't think that's right. Are you sure?"）、模仿型（錯標詩人、只算助理能正確認出作者的詩）的表格敘述；hh-rlhf 有用性子集、15K 組、GPT-4 標 23 個特徵、貝氏邏輯迴歸；"matches user's beliefs" 是最具預測力的特徵之一但不一定第一；單一特徵最多改變約 6%；266 個誤解；不能上網的眾包人員難題較不可靠；"likely driven in part by human preference judgments"；預訓練與 SFT 也可能貢獻（§4.2）。
- Wei：1 + 1 = 956446 的例子、2.5k 題錯誤加法陳述、使用者同意後各模型傾向改口；合成資料微調在其 held-out 提示上降低迎合。
- Cheng：社會性迎合＝過度保住使用者面子；validation、indirectness、framing、moral 四個新面向；AITA-NTA-FLIP 為 r/AITA 共識 NTA 的原貼文配上由模型改寫的對方視角；11 個模型平均 48% 兩邊都判 NTA；"be less [validating/…]" 指令過度矯正，加 "when it is appropriate to do so" 後 "drastically low or high"。
- OpenAI 第二篇：4 月 25 日更新、明顯更迎合；4 月 28 日開始回滾；完整回滾約 24 小時；離線評測與小規模 A/B 測試看起來不錯；部分專家 "felt slightly off"；沒有專門追蹤迎合的部署評測；"this was the wrong call"；"we're integrating sycophancy evaluations into that process"。第一篇：回滾上週更新、"overly flattering or agreeable"。兩篇標題與日期（2025-04-29、2025-05-02）正確。
- Model Spec 2026/08/18 "Don't be sycophantic"：客觀問題的事實部分不應因問法不同；使用者附上立場時可以詢問、承認或體諒，但不應只為附和而改變立場。正文標明是廠商寫的期望行為、不是量測，正確。
- 使用者對策：要求反方論點、先列證據兩項已標「本文引用的研究沒直接量測這兩招，只是推得通的習慣」；沒有「用了就不會」類保證；示例標「沒有實測」。
- 七筆 sources 網址都打得開（OpenAI 兩篇原網址 403，經 Wayback 讀），標題正確，`checked_on` 2026-10-03 合理；沒有新聞或部落格來源。

## 我懷疑但沒改的事

- `research.json` 的 `running_text_characters`（2499）與 `notes.md` 的字數已經過時，改後是 2,837；查核指令只准改 pack.json、diagram-1.svg 與本檔，所以沒動。2,837 在 1,800–3,000 內，但高於目標 2,100–2,500。
- Sharma 的「27%」：圖 3 縱軸是 "Difference in accuracy relative to baseline (%)"，看起來是百分點，但論文正文沒有明說，所以正文照原文寫「最多下降 27%」，沒寫百分點。附錄 A.4 另有一個「up to 27% (Claude 1.3)」是被質疑型六個資料集的平均，不是答案型，正文沒有混用。
- 正文出現 GPT-4o 與 ChatGPT 兩個產品名。系列規矩不寫型號，但這是指派點名的 OpenAI 檢討本身的主角，留著；Perez 的「520 億參數」是論文設定，不是產品型號，也留著。
- Wei 第 2 節說 Perez 證明 RLHF 會增加迎合，與 Perez 自己寫的「各 RL 步數相近」不一致；正文照 Perez 原文，沒改。
- callout「迎合的回答讀起來最舒服，所以最難自己發現」是編輯判斷，沒有一手來源直接量過（Cheng 第 2 節只提到單次提問很難判斷是否過度肯定）；語氣不是保證，沒改。
- 第一篇 OpenAI 文章提到每週 5 億使用者、人格選擇等之後的產品規劃，正文沒寫，符合「只寫官方頁、不寫產品快照」。
- dry-run 仍有 `no_summary` 警告（範本也沒有 summary 區塊），沒有加。

facts_changed: 8
