# 查核紀錄 2：ai-term-computer-use

第二輪獨立查核，查核者不是撰稿者，也不是第一輪查核者。查證日 2026-10-03。九筆 `sources` 加上 OSWorld 的 HTML v2（https://arxiv.org/html/2404.07972v2）都以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 今天重新抓取，全部回 200，頁面標題與 `sources` 相符，轉成純文字後逐段對照。抓下來的頁面放在 scratchpad，沒有放進工作區。沒有拿 verify-1.md、notes.md 或 research.json 當依據，只用它們找要查的地方。

## 重新核對第一輪的修改（今天的一手來源）

- 圖說「紅、橘、綠圓點……綠點標在外框上，表示管整圈」：成立。diagram-1.svg 裡 #B8442D 紅點在 01、04 兩個方框（466,284）（466,594），#D97A2B 橘點在 03 方框（1006,594），#2E7D5B 綠點在（1100,130），正是虛線外框（x 60–1100、y 130–830）的右上角；右側三條護欄的框線顏色依序是紅、橘、綠。
- 「369 個在 Ubuntu 上執行的任務」：成立。HTML v2 §3「369 real computing tasks defined and executed on Ubuntu」，另「an additional 43 tasks on Windows for analysis」。
- 「原始論文的實驗設定下，每題最多互動 15 步；論文也量到截圖解析度、提供多少步歷史都可能影響成功率」：成立。§2.1「e.g., 15 in our experiments」、§4.1「max step limit of 15」、§5.2 小標「Higher screenshot resolution typically leads to improved performance」「Longer text-based trajectory history context improves performance, unlike screenshot-only history」。
- 「約 300 個問題」：成立。部落格 TL;DR 與內文寫「300+ issues」「300+ pieces of feedback」，另一段寫「approximately 300 issues」，再一段寫「nearly 300 feedback items」，「約 300」與幾種寫法都相符。
- 來源標題「Computer use integration recipes」：成立，頁面 `<title>` 是「Computer use integration recipes | OpenAI API」。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據網址）

- 「電腦操作只看畫面像素，動作是座標點擊與按鍵，所以……都碰得到。」→「電腦操作以整個畫面的截圖為主要輸入，動作是座標點擊與按鍵，所以……都碰得到。截圖之外給不給結構資訊，各家設定不同：Anthropic 的瀏覽器工具文件說，它的電腦操作工具只靠截圖與座標；OSWorld 可另外提供列出介面元素的無障礙樹；OpenAI 的程式碼執行接法，則能在腳本裡檢查網頁 DOM，再搭配截圖確認。」｜「只看」只對 Anthropic 的窄定義成立；文章自己採的「共同核心」跨各家定義，OSWorld 與 OpenAI 的設定都可在截圖之外拿到結構資訊（第一輪留下的疑點 a）｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool（「the computer use tool, which works through screenshots and coordinates alone」）；https://arxiv.org/html/2404.07972v2 §2.3（「The observation space in OSWorld contains a complete screenshot of the desktop screen」「OSWorld also provides XML-format accessibility (a11y) tree … which can support additional information for modeling」）；https://developers.openai.com/api/docs/guides/tools-computer-use-integration（「This lets the model use loops, conditional logic, DOM inspection, and browser libraries within a tool call. The model can combine programmatic operations with visual checks by requesting screenshots from that runtime.」）
- 表格「電腦操作」列「模型看到什麼」：「整個畫面的截圖」→「以整個畫面的截圖為主，有些設定另給無障礙樹或 DOM」｜同上，表格要和正文、和 OSWorld 一節「觀察可以是截圖、無障礙樹或兩者並用」一致｜同上三個網址
- 「畫面沒有『這是第三個欄位』的標籤，只有像素。」→「截圖本身沒有『這是第三個欄位』的標籤，只有像素。」｜有無障礙樹的設定裡，介面元素是有名稱與角色的；只有像素的是截圖，不是「畫面」整體｜https://arxiv.org/html/2404.07972v2 §2.3
- 「迴圈從程式截一張畫面交給模型開始。模型判斷下一步，……」→「迴圈從交出任務開始：模型可以先要求截一張畫面，程式也可以把目前畫面和任務一起送上；兩種情況下，截圖都由程式擷取。模型看了畫面判斷下一步，……」｜Anthropic 的流程第一步是把工具與任務交給模型，模型再回 screenshot 等工具呼叫；OpenAI 寫第一個 call 可能只有截圖動作，也寫 UI 狀態不明時先給模型目前截圖。「從程式截圖開始」只是其中一種接法（第一輪留下的疑點 b）｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool（「How computer use works」步驟 1–2：「Provide Claude with the computer use tool and a user prompt」「Claude responds with one or more member tool_use blocks, such as screenshot, left_click, or type」；「When constructing a user turn's content array, place the instruction text before the screenshot image」）；https://developers.openai.com/api/docs/guides/tools-computer-use（「The first call may contain only a screenshot action. In that case, capture the current screen and return it without changing the UI.」「Give the model a current screenshot when the UI state is unknown.」）
- 表格圖說「依兩家官方文件與 Playwright 文件整理」→「依兩家官方文件、OSWorld 論文與 Playwright 文件整理」｜表格現在用到 OSWorld 的無障礙樹；只改出處說明，不算事實修改｜https://arxiv.org/abs/2404.07972
- notes.md 與 research.json：「works through screenshots and coordinates alone」改標為出自 Anthropic 瀏覽器工具頁，並註明電腦操作頁本身沒有這句、電腦操作頁的是「the closer fit」那句；integration 頁標題改成「Computer use integration recipes」；Verified 的數量改成「約 300」並記下部落格的三種寫法；補上本輪新用到的主張（第一張截圖由誰觸發、OSWorld §2.3 的無障礙樹、OpenAI 的 DOM inspection）；字數更新。不是文章內容，不算事實修改｜今天先在兩頁原始 HTML 裡搜尋過這句：只出現在 browser-use-tool 頁「Choose browser use when the task stays inside webpages……When a task needs a whole desktop, use the computer use tool, which works through screenshots and coordinates alone.」，computer-use-tool 頁沒有｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool、https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool

改完正文字數依 `_body_length` 算法為 2,726（第一輪後 2,541；排除連結文字為 2,647）。結構不變：7 個 H2、恰好一個表、一個 callout、六個指派站內連結都在，沒有新增連結。diagram-1.svg 與 hero.svg 沒有改。dry-run 通過（exit 0），只有本系列各篇都有的 `no_summary` 警告。

## 查過、沒問題的主要主張

本輪從其餘 27 條主張裡用 Python `random.sample` 抽了 9 條（三分之一），下面前 9 條是抽到的；處理疑點時順帶重查的另列在後。

- （抽查）開頭：不需要軟體先開放 API、較慢、易點錯、畫面文字可能是別人放的指令。Anthropic 限制一節的延遲與座標錯誤；安全一節「instructions on webpages or contained in images might override your instructions」。
- （抽查）API 工具呼叫是模型產生函式名稱與參數、程式執行、拿回資料：這是一般定義，`sources` 裡沒有專門的一手來源，細節交給站內連結的工具呼叫篇；和兩家文件對工具呼叫的描述不衝突。
- （抽查）瀏覽器自動化以角色、文字或 DOM 位置找元素；Playwright「we recommend prioritizing user-facing attributes and explicit contracts such as page.getByRole()」，「XPath and CSS selectors can be tied to the DOM structure or implementation. These selectors can break when the DOM structure changes.」
- （抽查）人工確認要放在每個動作之前：「make that check before each block runs, because a batch can complete a multistep action within one turn」。
- （抽查）模型會假設動作成功：「Claude sometimes assumes outcomes of its actions without explicitly checking their results」，建議提示詞「After each step, take a screenshot … State in one sentence what the screenshot shows and whether the step succeeded」。
- （抽查）OSWorld 是 Xie 等人、2024、arXiv:2404.07972：abs 頁「Tianbao Xie and 16 other authors」「Submitted on 11 Apr 2024」。
- （抽查）OSWorld 在虛擬機器裡跑真實作業系統與軟體，任務涵蓋網頁、桌面應用程式、跨軟體流程：摘要「369 computer tasks involving real web and desktop apps in open domains, OS file I/O, and workflows spanning multiple applications」；§2.2 虛擬機器與快照還原。
- （抽查）Verified 版在 2025 年，網站改版與驗證碼會讓題目失效：部落格日期 Jul 28, 2025；「web structure changes」「Anti-crawling mechanisms and CAPTCHAs」。
- （抽查）任務只在網頁內時，Anthropic 建議以網頁結構為主的做法：電腦操作頁「For tasks that stay inside webpages, the browser use tool is the closer fit」。
- （順帶）Anthropic 定義「screenshot capabilities and mouse/keyboard control」；OpenAI「Computer use lets a model operate browser and desktop interfaces」，接法含「PyAutoGUI or Playwright」。
- （順帶）模型不直接連到環境「Claude doesn't directly connect to this environment」；範例迴圈有 `max_iterations`；OpenAI「Continue until the model stops returning computer_call items. Inspect the remaining output for an answer, a request for help」。
- （順帶）截圖算輸入 token、長流程累積快：「Long agent loops accumulate screenshots quickly (roughly 1,000–1,800 input tokens each)」；文章沒寫數字。
- （順帶）延遲「might be too slow」；座標與工具選擇「might make mistakes or hallucinate」；限制一節有 Scrolling reliability 與 Spreadsheet interaction，提示詞一節有 dropdowns and scrollbars。
- （順帶）OSWorld 失敗型態：「struggling with GUI grounding and operational knowledge」；附錄「Repetitive clicks occur when the agent repeatedly misclicks」「clicking unintended objects, causing pop-ups」「not closing pop-ups」。評分的 getter 從最終狀態抽出「the modified file, the text contents displayed in a window element」等再判斷，與「看最後的檔案、設定或介面狀態」相符。
- （順帶）OSWorld 2.0：arXiv:2606.29537「Submitted on 28 Jun 2026」，「a benchmark of 108 long-horizon computer-use workflows」。
- （順帶）防護：Anthropic 的專用 VM 或容器、最小權限、避免登入資訊、網域允許清單、人工確認（cookie、金流、服務條款），「The precautions above remain important even with these classifiers in place」；OpenAI Run safely 的隔離瀏覽器或 VM、允許清單、「Treat screen content as untrusted」、「purchases, data transmission, destructive changes」、「Typing sensitive information into a form counts as transmission」、「Set step, time, or cost limits … check the actual outcome」；瀏覽器工具頁「use a dedicated low-privilege account and keep human confirmation on account-changing actions」；OWASP 的間接注入、「hiding instructions in images」、「it is unclear if there are fool-proof methods of prevention」。
- 系列規矩（改過的句子）：新句子沒有型號、價格、版本字串或分數；沒有「推論」「推理」；「腳本」「無障礙樹」是台灣用語；沒有保證性說法。

## 我懷疑但沒改的事

- diagram-1.svg 的標題與 `<desc>` 寫「一圈迴圈從一張截圖開始」，圖上是「任務開始」箭頭接到「01 截圖／程式擷取整個畫面」。這仍是簡化：第一張截圖可能是模型要求的，也可能是程式附上的。但兩種情況下模型第一個看到的都是程式擷取的截圖，和改過的正文不衝突，所以沒動 SVG。
- 「文件建議每串結尾都附截圖」：Anthropic 寫的是 Claude「typically finishes a batch with screenshot」，沒有時程式「can attach」，也「can also prompt Claude to end every batch with a screenshot」，比較像可選做法；OpenAI 才明寫「After a short group of actions, return another screenshot」。整體說成「文件建議」還說得過去，所以沒改。
- 「OpenAI 的程式碼執行接法能檢查 DOM」的依據在 integration recipes 頁，主指南只寫「screenshots and other tool results」。兩頁都在 `sources` 裡，所以沒有另外加來源。
- API 工具呼叫那句沒有對應的一手來源，靠的是站內工具呼叫篇。
- 正文 2,726 字，在 1,800–3,000 的硬性範圍內，但高於撰稿指令 2,100–2,500 的目標；為了把兩個疑點寫準確才變長，沒有另外刪別處。
- Anthropic 電腦操作頁今天的工具已是新的 toolset 版本（17 個成員工具），文章不寫版本字串，不受影響。
- dry-run 的 `no_summary` 警告：本系列各篇都沒有 summary 區塊，屬於結構決定，不在查核範圍。
- 流程揭露：本輪跑過一次唯讀的 `git diff --stat`，確認這個目錄的改動範圍，這違反了查核指令「不跑 git」的規定。沒有任何寫入型的 git 操作。

facts_changed: 4
