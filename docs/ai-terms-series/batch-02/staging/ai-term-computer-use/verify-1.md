# 查核紀錄 1：ai-term-computer-use

查核者不是撰稿者。查證日 2026-10-03。全部來源以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 今天重新抓取，九筆 `sources` 都回 200，標題相符（一筆標題補全，見下），轉成純文字後逐段對照。沒有沿用撰稿者的 notes.md 或 research.json 當依據。diagram-1.svg 已渲染成 PNG 看過（放在 scratchpad，沒有放進工作區）。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據網址）

- 圖說「方框上的橘、藍、綠圓點，對應右側三條護欄各管哪一段」→「紅、橘、綠圓點對應右側三條護欄各管哪一段，綠點標在外框上，表示管整圈」｜圖上的圓點是 #B8442D 紅、#D97A2B 橘、#2E7D5B 綠，沒有藍點；綠點在虛線外框的角上，不在四個方框上｜diagram-1.svg（渲染後目視確認）
- 「收了 369 個任務」→「收了 369 個在 Ubuntu 上執行的任務」｜論文的 369 題定義並執行於 Ubuntu，另有 43 題 Windows 任務只做分析；數字要對到論文自己的設定｜https://arxiv.org/abs/2404.07972（HTML v2 §3：「369 real computing tasks defined and executed on Ubuntu」「an additional 43 tasks on Windows for analysis」）
- 「在它的實驗設定下，每題最多互動 15 步，所以設定不同的分數不能直接相比」→「在原始論文的實驗設定下，每題最多互動 15 步；論文也量到截圖解析度、提供多少步歷史都可能影響成功率，所以設定不同的分數不能直接相比」｜光靠 15 步上限推不出「所以不能比」，結論的依據是論文 §5.2 的解析度與歷史長度實驗；也標明 15 步只是原始論文的設定（2.0 版另有不同的步數預算），免得和後面提到的新版混在一起｜https://arxiv.org/abs/2404.07972（HTML v2 §2.1「e.g., 15 in our experiments」、§4.1「max step limit of 15」、§5.2「Higher screenshot resolution typically leads to improved performance」「Longer text-based trajectory history context improves performance, unlike screenshot-only history」）
- 「處理了社群回報的 300 多個問題」→「處理了社群回報的約 300 個問題」｜官方部落格自己的說法不一致：TL;DR 寫「300+ issues」，內文又寫「approximately 300 issues」「nearly 300 feedback items」；「約 300」與三種寫法都相符｜https://xlang.ai/blog/osworld-verified
- 來源標題「OpenAI：Computer use integration（開發者指南；…）」→「OpenAI：Computer use integration recipes（開發者指南；…）」｜頁面實際標題是「Computer use integration recipes」；只改來源標題，不算事實修改｜https://developers.openai.com/api/docs/guides/tools-computer-use-integration

改完正文字數依 `_body_length` 算法為 2,541（原 2,500）；結構不變：7 個 H2、恰好一個表、一個 callout、六個指派站內連結都在。dry-run 通過（exit 0），只有一個 `no_summary` 警告，和本系列其他篇一樣，沒有改。

## 查過、沒問題的主要主張

- 定義分歧（撰稿者自己標記要查的部分）：Anthropic 電腦操作頁寫「screenshot capabilities and mouse/keyboard control」，並說任務留在網頁內時瀏覽器工具「is the closer fit」；瀏覽器工具頁寫它「both through its structure (the accessibility tree, elements, forms, and tabs) and through screenshots and viewport coordinates」，又說電腦操作「works through screenshots and coordinates alone」。OpenAI 指南第一句是「Computer use lets a model operate browser and desktop interfaces」，兩種接法是程式碼執行（「PyAutoGUI or Playwright」）與電腦工具（結構化的滑鼠鍵盤動作）。文章寫「沒有單一標準定義」、兩邊都列出來，並說明本文自己取的核心，符合本系列的規矩。
- 迴圈：模型回 tool_use，應用程式在自己的環境執行並回傳 tool_result，截圖用圖片回傳；「Claude doesn't directly connect to this environment」；範例迴圈有 `max_iterations`，目的是避免無限迴圈；OpenAI 寫「Continue until the model stops returning computer_call items」，並要檢查剩下的輸出裡是不是回答或求助（Anthropic 電腦操作頁；OpenAI 指南）。
- 批次動作：一個回合可以有好幾個動作；「make that check before each block runs, because a batch can complete a multistep action within one turn」；Claude 通常以截圖結束一批，也可以在提示詞要求每批都以截圖結尾；模型「sometimes assumes outcomes of its actions without explicitly checking」，官方建議的提示詞是每步之後截圖，並說明這步有沒有成功（Anthropic 電腦操作頁）。
- 慢與錯：限制一節寫延遲「might be too slow」，建議用在速度不重要的場合；輸出座標與選擇工具時「might make mistakes or hallucinate」；捲動與試算表在限制一節，下拉選單在提示詞建議一節；截圖每張大約 1,000–1,800 個輸入 token，長迴圈累積很快（文章沒寫數字，只寫算輸入 token、累積很快）（Anthropic 電腦操作頁）。
- OSWorld 的失敗型態：卡在 GUI grounding 與操作知識、會重複動作、會被非預期的視窗干擾、重複點擊、彈出視窗（arXiv:2404.07972 摘要、§1、附錄 D）。
- OSWorld 的設定：在虛擬機器裡跑，用快照加設定檔還原起點，每題有自己的執行式評分腳本（會檢查檔案、cookie、無障礙樹）；觀察可以是截圖、a11y 樹、兩者並用（另有 Set-of-Mark）；動作空間是 pyautogui 程式碼，另加 WAIT、FAIL、DONE（§2–§4）。
- OSWorld-Verified 的日期是 2025-07-28（部落格與專案頁一致），內容包含網站結構改變與驗證碼（CAPTCHA）造成的問題。OSWorld 2.0：arXiv:2606.29537，2026-06-28 送出 v1，「a benchmark of 108 long-horizon computer-use workflows」，第一作者是 Mengqi Yuan；專案頁在 2026-06-26 公告。文章寫「2025 年」「2026 年」，都正確。
- 風險與防護：Anthropic 建議專用的 VM 或容器並給最小權限、避免讓模型碰到登入資訊、網域允許清單，有實際後果或需要明確同意的事（cookie、金流、服務條款）由人確認；「The precautions above remain important even with these classifiers in place」。OpenAI 的 Run safely 一節：隔離的瀏覽器或 VM、站台與動作的允許清單、螢幕內容視為不可信、購買、傳送資料與破壞性變更由使用者控制、「Typing sensitive information into a form counts as transmission」、設步數、時間或費用上限，並檢查實際結果。Anthropic 瀏覽器工具頁：「use a dedicated low-privilege account and keep human confirmation on account-changing actions」。
- OWASP LLM01:2025 的間接注入定義（外部來源，例如網站、檔案）、多模態注入（「hiding instructions in images」）、「it is unclear if there are fool-proof methods of prevention」、最小權限、高風險動作要人工核准，都對得上。
- Playwright：「we recommend prioritizing user-facing attributes and explicit contracts such as page.getByRole()」；CSS 與 XPath「can break when the DOM structure changes」。
- 系列規矩：沒有型號、價格、方案、地區、截止日期、分數或排名；「推論」「推理」都沒出現；示例標了「以下是示例，未實測」，沒有寫成觀察到的結果；callout 明寫「也不代表一定不會出錯」，沒有任何保證；用語是台灣用法；圖上的數字只有 01–04 步驟徽章與 2026，正文有 2026。
- 站內連結：claude-computer-use-explained、ai-term-tool-calling、ai-term-sandbox、ai-term-prompt-injection、ai-browsers-guide、ai-terms-index 都在，沒有指派以外的連結。

## 我懷疑但沒改的事

- 表格與「電腦操作只看畫面像素」一句用的是 Anthropic 的窄定義。OSWorld 的代理也能讀無障礙樹，OpenAI 的程式碼執行接法也能檢查 DOM。文章前面已寫明沒有單一定義、本文取共同核心，所以沒改；但讀者可能覺得表格的「只看截圖」和 OSWorld 那段「也可用無障礙樹」前後不一致。
- 「迴圈從程式截一張畫面交給模型開始」是簡化的說法：Anthropic 的流程通常是模型第一步先要求截圖；OpenAI 寫第一個 call 可能只有截圖動作，也建議 UI 狀態不明時先給一張截圖。兩種情況下截圖都是程式截的，所以沒改。
- 撰稿者的 notes.md 與 research.json 把「works through screenshots and coordinates alone」寫成出自電腦操作頁，實際上是在瀏覽器工具頁；research.json 裡 integration 頁的標題也還是舊寫法。這兩個檔不在我可以寫的範圍，正文沒有因此出錯。
- OSWorld-Verified 部落格對問題數量的寫法本身就不一致（300+、approximately 300、nearly 300）。專案頁與 arXiv 對 2.0 某模型分數的寫法也不同，但文章不引用分數，不受影響。
- OSWorld 2.0 的主要指標用的是 500 步預算，和原始論文的 15 步差很多。正文已標明 15 步是原始論文的設定，沒有另外寫 2.0 的步數。
- dry-run 的 `no_summary` 警告：本系列各篇都沒有 summary 區塊，屬於結構決定，不在查核範圍。

facts_changed: 4
