# 查證與編輯紀錄：ai-term-computer-use

格式：主張｜來源網址｜查證日｜讀取方式。全部用 `curl -sSL`（User-Agent 為 Mokaair-editorial/1.0，不帶任何個資），狀態碼 200，頁面轉成純文字後逐段讀；沒有用 Wayback。查證日 2026-10-03。

## 定義與分歧

Anthropic 把電腦操作說成「螢幕截圖加滑鼠與鍵盤控制」，工具是由應用程式在自己環境執行的 client-side toolset｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool｜2026-10-03｜curl 200（docs.claude.com 舊網址轉址到此）
Anthropic 另有只管網頁的瀏覽器工具，同時用網頁結構（無障礙樹、元素、表單、分頁）與截圖座標；同一頁說電腦操作工具「只靠截圖與座標」（原文 works through screenshots and coordinates alone），任務留在網頁內並要在頁面上動作時選瀏覽器工具｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool｜2026-10-03｜curl 200（第二輪查核重新核對：這句只在瀏覽器工具頁）
Anthropic 電腦操作頁說任務留在網頁內時瀏覽器工具較合適（原文 the closer fit）；電腦操作頁本身沒有「只靠截圖與座標」這句｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool｜2026-10-03｜curl 200
OpenAI 指南把「操作瀏覽器與桌面介面」都放在 computer use 底下，兩種接法：程式碼執行（模型寫 PyAutoGUI 或 Playwright 程式）與電腦工具（結構化的滑鼠鍵盤動作）；也可用自己的函式呼叫或 MCP 工具｜https://developers.openai.com/api/docs/guides/tools-computer-use｜2026-10-03｜curl 200（platform.openai.com 舊網址轉址到此）
OpenAI 整合頁（標題 Computer use integration recipes）：自訂 UI 工具可用定位器選元素而非座標，也可回傳可見文字或截圖；程式碼執行工具可做 DOM 檢查與視覺檢查並用（原文 DOM inspection；用來支持表格「有些設定另給 DOM」）｜https://developers.openai.com/api/docs/guides/tools-computer-use-integration｜2026-10-03｜curl 200
文章因此寫成「沒有單一標準定義」，並取「以畫面為依據、用滑鼠鍵盤動作回應」為共同核心；與 brief 把電腦操作與 DOM 型瀏覽器自動化截然二分的說法不完全一致，以來源為準（見 research.json notes）。

## 迴圈與機制

迴圈＝應用程式送請求、模型回 tool_use、應用程式在自己的環境執行並回傳 tool_result（截圖用圖片），直到模型不再要求工具；模型不直接連到環境｜Anthropic computer use tool 頁「How computer use works」「The computing environment」｜2026-10-03｜curl 200
一次回覆可含一串動作（batch），通常以截圖收尾；要人確認的檢查要放在每個動作之前，因為一個回合可完成多步動作｜同上「Batch actions」｜2026-10-03｜curl 200
模型有時假設動作成功卻沒檢查；官方建議提示詞要求每步後截圖並說明畫面顯示什麼、是否成功｜同上「Optimize model performance with prompting」｜2026-10-03｜curl 200
範例迴圈有 max_iterations 上限，避免無限迴圈與意外費用｜同上「Understand the agent loop」｜2026-10-03｜curl 200
迴圈的第一張截圖：模型可以先要求截圖，OpenAI 寫第一個 computer_call 可能只有 screenshot 動作（程式照截、不改畫面）；程式也可以把目前畫面和任務一起送上，Anthropic 寫組 user turn 時指示文字要放在截圖之前，OpenAI 寫 UI 狀態不明時先給模型一張目前截圖。兩種情況截圖都由程式擷取，所以文章不寫「迴圈從程式截圖開始」｜Anthropic computer use tool 頁「How computer use works」「Optimize model performance with prompting」；OpenAI computer use 指南「Execute the requested actions」「Preserve state and return observations」｜2026-10-03｜curl 200
OpenAI：一小串動作後回傳新截圖；繼續到模型不再回 computer_call｜OpenAI computer use 指南「Repeat the computer-use loop」「Use the computer tool」｜2026-10-03｜curl 200
Playwright：定位器建議優先用角色等使用者可見屬性；CSS 與 XPath 綁 DOM 結構，結構改動會壞｜https://playwright.dev/docs/locators｜2026-10-03｜curl 200

## 為什麼慢、容易出錯

延遲對即時人機互動可能太慢，建議用在速度不重要的場合（背景蒐集資料、自動化測試）；座標與工具選擇可能出錯或幻覺；捲動、試算表、下拉選單與捲軸是文件點名的難處｜Anthropic computer use tool 頁「Limitations」與「Optimize model performance with prompting」｜2026-10-03｜curl 200
截圖算圖片輸入；長流程截圖累積很快｜同上「Manage screenshot history」「Pricing」。文章只寫「算輸入 token、累積很快」，不寫每張的 token 數與任何價格。
OSWorld 分析：模型卡在畫面定位（GUI grounding）與操作知識；傾向重複動作；被非預期視窗干擾；重複點擊與彈出視窗／cookie 視窗干擾的質性分析｜https://arxiv.org/abs/2404.07972（摘要與 HTML 版 https://arxiv.org/html/2404.07972v2 的 §5.4 與附錄）｜2026-10-03｜curl 200

## OSWorld 的設定（只寫設定，不寫分數）

369 個任務（Ubuntu），含網頁與桌面應用程式、檔案 I/O、跨多軟體流程；每題有初始狀態設定與專屬的執行式評分腳本｜arXiv:2404.07972 摘要與 §3｜2026-10-03｜curl 200（abs 與 html v2）
在虛擬機器裡執行，以快照與設定檔還原起點｜同上 §2.2｜2026-10-03｜curl 200
觀察空間：截圖、無障礙樹、兩者並用（另有 Set-of-Mark）；動作空間：pyautogui 程式碼表示的滑鼠鍵盤動作，另加 WAIT、FAIL、DONE｜同上 §2.3、§2.4、§4｜2026-10-03｜curl 200。§2.3 寫觀察空間以整個桌面截圖為主，另提供 XML 格式的無障礙樹作為額外資訊；用來支持表格「有些設定另給無障礙樹」
實驗設定：最多 15 步（附錄另寫 30 分鐘上限）｜同上 §2.1 與附錄｜2026-10-03｜curl 200。文章只寫 15 步。
解析度與歷史長度會改變結果（論文 §5.2）｜同上｜2026-10-03｜curl 200。用來支持「設定不同的分數不能直接相比」。
Verified 版（2025-07-28）：處理約 300 筆社群回報（部落格寫法不一：300+、approximately 300、nearly 300，文章寫「約 300」），環境不穩定因素含驗證碼與網站改版；有統一設定的公開評測平台｜https://xlang.ai/blog/osworld-verified｜2026-10-03｜curl 200
OSWorld 專案頁在 2026-06-26 公告 2.0 版｜https://osworld-v1.xlang.ai/（由 https://os-world.github.io/ 轉址）｜2026-10-03｜curl 200；此頁不列為 sources，只用來找到 2.0。
OSWorld 2.0：108 個長流程任務，arXiv 2026-06-28 提交｜https://arxiv.org/abs/2606.29537｜2026-10-03｜curl 200。專案頁寫某模型「接近 14%」，arXiv 摘要寫「接近 13%」，兩處不一致；文章不引用任何分數，所以不受影響。

## 風險與防護（只寫今天看到的）

Anthropic：專用 VM 或容器、最小權限；避免讓模型碰登入資訊等敏感資料；網域允許清單；有實際後果或需明確同意的動作（接受 cookie、金流、同意條款）由人確認；模型可能遵循內容裡與你的指示衝突的指令；已訓練抵抗並用分類器掃描截圖，但上述措施仍重要｜Anthropic computer use tool 頁「Security considerations」｜2026-10-03｜curl 200
Anthropic 瀏覽器工具：頁面提供的一切都是不可信輸入；躲不開已登入狀態時用專用低權限帳號並保留人工確認｜browser use tool 頁「Security considerations」｜2026-10-03｜curl 200
OpenAI：隔離瀏覽器或 VM、站台與動作允許清單；螢幕內容視為不可信；難回復的動作由使用者確認，在表單輸入敏感資料也算傳送；設定步數、時間或費用上限、支援取消、檢查實際結果而不只信模型最後的回答｜OpenAI computer use 指南「Run safely」；整合頁「Handle user confirmation and consent」｜2026-10-03｜curl 200
OWASP LLM01:2025：間接提示詞注入定義；多模態模型可能被圖片裡藏的指令影響；「不確定有沒有萬無一失的防法」；最小權限與高風險動作人工核准｜https://genai.owasp.org/llmrisk/llm01-prompt-injection/｜2026-10-03｜curl 200

## 編輯紀錄

示例（填測試表單）是原創教學設計，已在文內標「示例，未實測」；沒有宣稱任何輸出是觀察到的結果。
不寫產品方案、價格、可用地區、模型名、各家分數；Anthropic 的工具版本字串與 OpenAI 的模型名都不寫。
圖解的數字只有 01 至 04 的步驟徽章與製圖年份 2026；2026 出現在表格圖說的查證年月。
正文字數：`_body_length` 算法（含 rich_paragraph 內的站內連結文字）撰稿時為 2500（排除連結文字 2416）；第一輪查核後 2541；第二輪查核後 2726（排除連結文字 2647）。
SVG 為原創向量插圖，非 AI 產圖。
