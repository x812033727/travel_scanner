# Claude Code 深入教學：36 篇作者任務書

[回第二階段總目錄](README.md) · [課程資料](curriculum.json) · [來源與驗證規則](source-review.md)

以下保留原課程設計與驗收目標；36 篇正文與練習包已製作，請由各章的「完整原稿」或總目錄開啟。實際測試狀態以交付紀錄為準，未將預覽稿公開發布。

## K．專案規則與工作上下文

<a id="lesson-61"></a>

### 61．替真實專案設計 CLAUDE.md

[完整原稿](../lessons/61.md)

把模糊、過期或重複的規則改成可操作的專案說明。

- 預定網址：`/zh-TW/life/claude-code-project-rules-workshop`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[20 CLAUDE.md 完整教學](../lessons/20.md)、[22 拆分規則與引用其他 MD](../lessons/22.md)、[32 快速讀懂陌生專案](../lessons/32.md)。
- 本篇交付：CLAUDE.md、規則取捨表、三組前後對照。
- 材料包：`config-lab`；本篇須提供可獨立開始的快照。

1. 盤點錯誤規則與真正的建置入口。
2. 區分常駐規則、按需規則及工作流程。
3. 改寫最小規則並啟動全新對話。
4. 用三種任務比對改寫前後行為。

**故障練習：**把模型聲稱讀過檔案當成載入證明；教讀者找實際載入資訊與執行紀錄。

**完成判準：**新對話能找到正確測試命令；錯誤規則已移除；對照紀錄含實際行為。

**作者需查證：**[How Claude remembers your project](https://code.claude.com/docs/en/memory)、[Configure permissions](https://code.claude.com/docs/en/permissions)、[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)、[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[62 Monorepo 的分層 MD 與路徑規則](lesson-briefs.md#lesson-62)、[63 Claude 沒照 MD 做：找出載入與規則衝突](lesson-briefs.md#lesson-63)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)。

[回第二階段總目錄](README.md)

<a id="lesson-62"></a>

### 62．Monorepo 的分層 MD 與路徑規則

[完整原稿](../lessons/62.md)

讓前端、API 與共用目錄使用適合的指引。

- 預定網址：`/zh-TW/life/claude-code-monorepo-rules-workshop`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[21 個人、專案與子目錄規則](../lessons/21.md)、[22 拆分規則與引用其他 MD](../lessons/22.md)、[61 替真實專案設計 CLAUDE.md](lesson-briefs.md#lesson-61)。
- 本篇交付：三目錄練習專案與規則適用矩陣。
- 材料包：`config-lab`；本篇須提供可獨立開始的快照。

1. 畫出 apps/web、apps/api、packages 關係。
2. 為三區設定不同規則及共同底線。
3. 從不同工作目錄啟動並讀取不同檔案。
4. 查證按需載入與不適用規則。

**故障練習：**相對路徑以錯誤目錄解讀；逐個確認引用檔案的基準位置。

**完成判準：**三種讀檔案例各有載入證據；沒有把所有子目錄內容一次塞入根規則。

**作者需查證：**[How Claude remembers your project](https://code.claude.com/docs/en/memory)、[Configure permissions](https://code.claude.com/docs/en/permissions)、[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)、[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[63 Claude 沒照 MD 做：找出載入與規則衝突](lesson-briefs.md#lesson-63)、[66 把個人設定整理成團隊可維護的設定包](lesson-briefs.md#lesson-66)、[88 雙 Worktree 實作與衝突整合](lesson-briefs.md#lesson-88)。

[回第二階段總目錄](README.md)

<a id="lesson-63"></a>

### 63．Claude 沒照 MD 做：找出載入與規則衝突

[完整原稿](../lessons/63.md)

分辨沒有載入、規則矛盾、資料過期與任務描述不足。

- 預定網址：`/zh-TW/life/claude-code-rules-loading-diagnostics`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[23 自動記憶與 /memory](../lessons/23.md)、[24 settings.json 設定教學](../lessons/24.md)、[61 替真實專案設計 CLAUDE.md](lesson-briefs.md#lesson-61)。
- 本篇交付：故障診斷表與四個最小重現案例。
- 材料包：`config-lab`；本篇須提供可獨立開始的快照。

1. 建立錯誤檔名、矛盾規則、舊記憶及錯路徑案例。
2. 一次只改一個變因。
3. 用新的工作階段驗證。
4. 保存根因與修正證據。

**故障練習：**反覆增加強調文字掩蓋衝突；先刪除互斥指令再重測。

**完成判準：**四個案例都能指出具體原因；修正後可重現結果，不能只寫重啟看看。

**作者需查證：**[How Claude remembers your project](https://code.claude.com/docs/en/memory)、[Configure permissions](https://code.claude.com/docs/en/permissions)、[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)、[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[62 Monorepo 的分層 MD 與路徑規則](lesson-briefs.md#lesson-62)、[65 長任務的上下文整理與交接文件](lesson-briefs.md#lesson-65)、[66 把個人設定整理成團隊可維護的設定包](lesson-briefs.md#lesson-66)。

[回第二階段總目錄](README.md)

<a id="lesson-64"></a>

### 64．權限與 Sandbox 邊界實驗

[完整原稿](../lessons/64.md)

用無害案例觀察允許、詢問、拒絕與執行隔離。

- 預定網址：`/zh-TW/life/claude-code-permissions-sandbox-lab`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[24 settings.json 設定教學](../lessons/24.md)、[30 Plan Mode 與權限模式](../lessons/30.md)、[57 專案資料與操作安全](../lessons/57.md)。
- 本篇交付：行為矩陣、測試目錄與設定還原檔。
- 材料包：`config-lab`；本篇須提供可獨立開始的快照。

1. 建立隔離練習資料與最小權限。
2. 分別測試規則判斷及支援環境的 sandbox。
3. 比較合法路徑、界外路徑與本機測試服務。
4. 還原設定並記錄限制。

**故障練習：**某個工具路徑未受設定約束；標明適用工具與 OS，不承諾全面封鎖。

**完成判準：**每個案例記錄預期及實際結果；Windows 原生與 WSL2 分開，不把 MD 當存取控制。

**作者需查證：**[How Claude remembers your project](https://code.claude.com/docs/en/memory)、[Configure permissions](https://code.claude.com/docs/en/permissions)、[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)、[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[76 用 Hook 保護指定檔案並測試路徑邊界](lesson-briefs.md#lesson-76)、[83 MCP 回傳含有指令時：資料與操作權限分開](lesson-briefs.md#lesson-83)、[92 CI 審查助手：權限、fork 與結果附件](lesson-briefs.md#lesson-92)。

[回第二階段總目錄](README.md)

<a id="lesson-65"></a>

### 65．長任務的上下文整理與交接文件

[完整原稿](../lessons/65.md)

讓新的工作階段依檔案接手，而不依賴原對話。

- 預定網址：`/zh-TW/life/claude-code-context-handoff-workshop`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[27 繼續、找回與管理對話](../lessons/27.md)、[28 上下文整理：context、compact 與 clear](../lessons/28.md)、[32 快速讀懂陌生專案](../lessons/32.md)。
- 本篇交付：handoff.md、決策紀錄、未完成工作清單。
- 材料包：`config-lab`；本篇須提供可獨立開始的快照。

1. 建立跨三回合的功能任務。
2. 將事實、假設、已測與待測分開保存。
3. 比較整理前後並建立新工作階段。
4. 只提供交接檔請接手者完成下一步。

**故障練習：**把 compact 摘要當永久規格；以版本控管的任務及決策檔補足。

**完成判準：**新階段能指出版本、工作範圍與下一步；不重做已完成項目；未驗證事項明列。

**作者需查證：**[How Claude remembers your project](https://code.claude.com/docs/en/memory)、[Configure permissions](https://code.claude.com/docs/en/permissions)、[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)、[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[63 Claude 沒照 MD 做：找出載入與規則衝突](lesson-briefs.md#lesson-63)、[90 桌面到手機：離線、中斷與返回工作現場](lesson-briefs.md#lesson-90)、[94 Agent SDK：保存狀態、取消與重新接續](lesson-briefs.md#lesson-94)。

[回第二階段總目錄](README.md)

<a id="lesson-66"></a>

### 66．把個人設定整理成團隊可維護的設定包

[完整原稿](../lessons/66.md)

建立共用範本、個人覆寫與更新檢查方式。

- 預定網址：`/zh-TW/life/claude-code-team-config-maintenance`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[24 settings.json 設定教學](../lessons/24.md)、[61 替真實專案設計 CLAUDE.md](lesson-briefs.md#lesson-61)、[62 Monorepo 的分層 MD 與路徑規則](lesson-briefs.md#lesson-62)。
- 本篇交付：設定範本、變更紀錄與相容性檢查表。
- 材料包：`config-lab`；本篇須提供可獨立開始的快照。

1. 分類可共用設定與個人機器資料。
2. 建立兩位讀者的乾淨設定環境。
3. 模擬設定升級與不相容欄位。
4. 驗證回復及文件更新。

**故障練習：**把組織管理政策當成專案設定可覆寫；分開標示管理權限條件。

**完成判準：**乾淨環境可套用；沒有金鑰或個人絕對路徑；升級與回復各有一次紀錄。

**作者需查證：**[How Claude remembers your project](https://code.claude.com/docs/en/memory)、[Configure permissions](https://code.claude.com/docs/en/permissions)、[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)、[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[63 Claude 沒照 MD 做：找出載入與規則衝突](lesson-briefs.md#lesson-63)、[72 把 Skills 與 Hooks 包成可版本管理的 Plugin](lesson-briefs.md#lesson-72)、[95 比較流程品質、用量與執行時間](lesson-briefs.md#lesson-95)。

[回第二階段總目錄](README.md)

## L．Skills 工程化與共用外掛

<a id="lesson-67"></a>

### 67．把一套工作 SOP 做成可重用 Skill

[完整原稿](../lessons/67.md)

將程式碼審查流程做成有輸入、輸出及停止條件的技能。

- 預定網址：`/zh-TW/life/claude-code-skill-sop-workshop`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[38 建立第一個 SKILL.md](../lessons/38.md)、[39 Skill 參數與附屬材料](../lessons/39.md)、[35 Git、差異審查與 PR](../lessons/35.md)。
- 本篇交付：review-change/SKILL.md 與標準審查報告。
- 材料包：`skill-kit`；本篇須提供可獨立開始的快照。

1. 先手動完成一次小範圍審查。
2. 抽出必要步驟及證據欄位。
3. 以兩份不同 diff 試跑 Skill。
4. 比對步驟是否可重用並刪除任務硬編碼。

**故障練習：**只把長提示詞改檔名；補齊輸入不完整時的處理與明確交付。

**完成判準：**兩個案例都產生檔案位置、影響與驗證狀態；不自動提交或合併。

**作者需查證：**[Extend Claude with skills](https://code.claude.com/docs/en/skills)、[Create plugins](https://code.claude.com/docs/en/plugins)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[68 Skill 參數驗證：缺值、錯誤與危險字元](lesson-briefs.md#lesson-68)、[70 Skill 何時啟動：手動呼叫與自動選用](lesson-briefs.md#lesson-70)、[71 替 Skills 建立回歸案例與評分表](lesson-briefs.md#lesson-71)。

[回第二階段總目錄](README.md)

<a id="lesson-68"></a>

### 68．Skill 參數驗證：缺值、錯誤與危險字元

[完整原稿](../lessons/68.md)

讓技能接收可預期的參數並安全交給輔助程式。

- 預定網址：`/zh-TW/life/claude-code-skill-input-validation`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[39 Skill 參數與附屬材料](../lessons/39.md)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)。
- 本篇交付：參數解析器與至少八組輸入案例。
- 材料包：`skill-kit`；本篇須提供可獨立開始的快照。

1. 定義輸入欄位及限制。
2. 測試缺值、空白、中文路徑及特殊符號。
3. 由輔助程式驗證而非直接拼接 shell。
4. 輸出可辨識的錯誤與修正方式。

**故障練習：**把插值當驗證；用引數陣列或標準輸入傳遞資料。

**完成判準：**所有案例有預期結果；錯誤輸入不執行主工作；合法中文路徑可處理。

**作者需查證：**[Extend Claude with skills](https://code.claude.com/docs/en/skills)、[Create plugins](https://code.claude.com/docs/en/plugins)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[69 拆分大型 Skill 的範本、參考文件與腳本](lesson-briefs.md#lesson-69)、[71 替 Skills 建立回歸案例與評分表](lesson-briefs.md#lesson-71)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。

[回第二階段總目錄](README.md)

<a id="lesson-69"></a>

### 69．拆分大型 Skill 的範本、參考文件與腳本

[完整原稿](../lessons/69.md)

建立能按需讀取的技能目錄。

- 預定網址：`/zh-TW/life/claude-code-skill-resource-design`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[39 Skill 參數與附屬材料](../lessons/39.md)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)。
- 本篇交付：SKILL.md、references、templates、scripts 的範例結構。
- 材料包：`skill-kit`；本篇須提供可獨立開始的快照。

1. 把混在主檔的三類材料分開。
2. 寫明何時讀取哪些參考。
3. 讓腳本輸出短而可核對的摘要。
4. 用小任務與完整任務比對讀取紀錄。

**故障練習：**移檔後連結失效；從乾淨目錄實際檢查每個引用。

**完成判準：**簡單任務不必載入全部參考；必要範本沒有缺漏；相對路徑可移植。

**作者需查證：**[Extend Claude with skills](https://code.claude.com/docs/en/skills)、[Create plugins](https://code.claude.com/docs/en/plugins)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[68 Skill 參數驗證：缺值、錯誤與危險字元](lesson-briefs.md#lesson-68)、[70 Skill 何時啟動：手動呼叫與自動選用](lesson-briefs.md#lesson-70)、[72 把 Skills 與 Hooks 包成可版本管理的 Plugin](lesson-briefs.md#lesson-72)。

[回第二階段總目錄](README.md)

<a id="lesson-70"></a>

### 70．Skill 何時啟動：手動呼叫與自動選用

[完整原稿](../lessons/70.md)

用正反例評估描述與呼叫設定。

- 預定網址：`/zh-TW/life/claude-code-skill-invocation-control`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[38 建立第一個 SKILL.md](../lessons/38.md)、[40 自訂斜線指令與舊格式移轉](../lessons/40.md)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)。
- 本篇交付：觸發評估表與兩種呼叫範例。
- 材料包：`skill-kit`；本篇須提供可獨立開始的快照。

1. 列出應觸發及不應觸發的任務。
2. 設定手動工作流程與背景知識用途。
3. 在全新工作階段重複觀察。
4. 檢查不同執行入口的限制。

**故障練習：**把不可手動選取誤認成 Claude 不能使用；依欄位語意及實測分辨。

**完成判準：**每種案例都有實際觀察；能解釋手動與自動入口差異；不以一次成功宣稱必定觸發。

**作者需查證：**[Extend Claude with skills](https://code.claude.com/docs/en/skills)、[Create plugins](https://code.claude.com/docs/en/plugins)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[69 拆分大型 Skill 的範本、參考文件與腳本](lesson-briefs.md#lesson-69)、[71 替 Skills 建立回歸案例與評分表](lesson-briefs.md#lesson-71)、[93 排程失敗怎麼辦：重複執行、漏跑與停止](lesson-briefs.md#lesson-93)。

[回第二階段總目錄](README.md)

<a id="lesson-71"></a>

### 71．替 Skills 建立回歸案例與評分表

[完整原稿](../lessons/71.md)

讓 Skill 修改後有可比較的品質紀錄。

- 預定網址：`/zh-TW/life/claude-code-skill-regression-testing`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[34 除錯與補測試](../lessons/34.md)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)、[68 Skill 參數驗證：缺值、錯誤與危險字元](lesson-briefs.md#lesson-68)。
- 本篇交付：案例資料集、驗收規則及版本比較報告。
- 材料包：`skill-kit`；本篇須提供可獨立開始的快照。

1. 固定正常、缺資訊與誤觸發案例。
2. 區分可程式檢查與人工判讀項目。
3. 同條件比較兩版 Skill。
4. 記錄模型、版本、重試與失敗樣本。

**故障練習：**只挑成功案例或精確比對整段文字；用結構與行為判準。

**完成判準：**報告包含成功率分母、樣本與失敗原因；不能用模型自評取代外部驗收。

**作者需查證：**[Extend Claude with skills](https://code.claude.com/docs/en/skills)、[Create plugins](https://code.claude.com/docs/en/plugins)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[70 Skill 何時啟動：手動呼叫與自動選用](lesson-briefs.md#lesson-70)、[72 把 Skills 與 Hooks 包成可版本管理的 Plugin](lesson-briefs.md#lesson-72)、[95 比較流程品質、用量與執行時間](lesson-briefs.md#lesson-95)。

[回第二階段總目錄](README.md)

<a id="lesson-72"></a>

### 72．把 Skills 與 Hooks 包成可版本管理的 Plugin

[完整原稿](../lessons/72.md)

讓同伴安裝、升級與回退同一套工作流程。

- 預定網址：`/zh-TW/life/claude-code-plugin-team-distribution`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[45 Plugins 安裝與管理](../lessons/45.md)、[66 把個人設定整理成團隊可維護的設定包](lesson-briefs.md#lesson-66)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)。
- 本篇交付：本機 plugin 包、版本紀錄與遷移說明。
- 材料包：`skill-kit`；本篇須提供可獨立開始的快照。

1. 整理外掛目錄與必要宣告。
2. 在乾淨測試環境安裝。
3. 發布本機第二版並演練設定遷移。
4. 回退並確認命名與資源路徑。

**故障練習：**名稱空間改變導致既有呼叫失效；提供可查證的遷移對照。

**完成判準：**安裝、升級、移除、回退皆有記錄；使用者自有設定保留。

**作者需查證：**[Extend Claude with skills](https://code.claude.com/docs/en/skills)、[Create plugins](https://code.claude.com/docs/en/plugins)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[69 拆分大型 Skill 的範本、參考文件與腳本](lesson-briefs.md#lesson-69)、[71 替 Skills 建立回歸案例與評分表](lesson-briefs.md#lesson-71)、[78 跨平台 Hooks：中文路徑、逾時與遞迴排錯](lesson-briefs.md#lesson-78)。

[回第二階段總目錄](README.md)

## M．Hooks 事件、檢查與故障處理

<a id="lesson-73"></a>

### 73．讀懂 Hook 事件：輸入、輸出與退出碼

[完整原稿](../lessons/73.md)

建立可重播事件的本機測試工具。

- 預定網址：`/zh-TW/life/claude-code-hook-event-test-lab`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[41 建立第一個 Hook](../lessons/41.md)、[42 Hooks 實用案例](../lessons/42.md)。
- 本篇交付：事件 fixtures、runner 與四類結果紀錄。
- 材料包：`hook-lab`；本篇須提供可獨立開始的快照。

1. 保存各事件的最小輸入。
2. 解析 JSON 並只讀必要欄位。
3. 分別輸出正常、拒絕、錯誤與診斷結果。
4. 比較人工重播與 Claude 真正觸發。

**故障練習：**對所有事件使用同一回傳格式；按當前官方事件定義逐一確認。

**完成判準：**腳本重播與真實觸發分開標記；輸出通道與事件語意吻合。

**作者需查證：**[Hooks reference](https://code.claude.com/docs/en/hooks)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[74 只處理變更檔案的格式化 Hook](lesson-briefs.md#lesson-74)、[75 建立可停止的品質檢查 Hook](lesson-briefs.md#lesson-75)、[78 跨平台 Hooks：中文路徑、逾時與遞迴排錯](lesson-briefs.md#lesson-78)。

[回第二階段總目錄](README.md)

<a id="lesson-74"></a>

### 74．只處理變更檔案的格式化 Hook

[完整原稿](../lessons/74.md)

限制格式化範圍並避免事件重複執行。

- 預定網址：`/zh-TW/life/claude-code-hook-scoped-formatting`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[34 除錯與補測試](../lessons/34.md)、[73 讀懂 Hook 事件：輸入、輸出與退出碼](lesson-briefs.md#lesson-73)。
- 本篇交付：檔案選擇器、格式化器與呼叫紀錄。
- 材料包：`hook-lab`；本篇須提供可獨立開始的快照。

1. 先驗證格式化命令本身。
2. 從事件提取及正規化目標路徑。
3. 略過不相關檔案並處理重複事件。
4. 模擬格式工具不存在與非零退出。

**故障練習：**每次修改都重跑全專案；以範圍及呼叫次數證明沒有擴大工作。

**完成判準：**只修改指定類型檔案；第二次執行不產生額外變更；失敗可追蹤。

**作者需查證：**[Hooks reference](https://code.claude.com/docs/en/hooks)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[75 建立可停止的品質檢查 Hook](lesson-briefs.md#lesson-75)、[78 跨平台 Hooks：中文路徑、逾時與遞迴排錯](lesson-briefs.md#lesson-78)、[85 真正走完一次重現、失敗測試與修正](lesson-briefs.md#lesson-85)。

[回第二階段總目錄](README.md)

<a id="lesson-75"></a>

### 75．建立可停止的品質檢查 Hook

[完整原稿](../lessons/75.md)

讓完成檢查能指出失敗並有清楚的退出機制。

- 預定網址：`/zh-TW/life/claude-code-hook-quality-gates`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[34 除錯與補測試](../lessons/34.md)、[73 讀懂 Hook 事件：輸入、輸出與退出碼](lesson-briefs.md#lesson-73)。
- 本篇交付：一次性驗證腳本、Stop 設定與失敗紀錄。
- 材料包：`hook-lab`；本篇須提供可獨立開始的快照。

1. 定義要檢查的真正成果。
2. 測試失敗、修正、成功的完整流程。
3. 限制重試與重複 Stop 觸發。
4. 停用 Hook 並說明 CI 的獨立角色。

**故障練習：**無限要求再測一次；使用明確停止條件，不把 Hook 當不可繞過的 CI。

**完成判準：**刻意失敗被檢出；修正後可正常結束；不可修復情況能退出並留下原因。

**作者需查證：**[Hooks reference](https://code.claude.com/docs/en/hooks)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[74 只處理變更檔案的格式化 Hook](lesson-briefs.md#lesson-74)、[78 跨平台 Hooks：中文路徑、逾時與遞迴排錯](lesson-briefs.md#lesson-78)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。

[回第二階段總目錄](README.md)

<a id="lesson-76"></a>

### 76．用 Hook 保護指定檔案並測試路徑邊界

[完整原稿](../lessons/76.md)

為特定編輯工具設置範圍檢查及清楚的拒絕訊息。

- 預定網址：`/zh-TW/life/claude-code-hook-file-boundaries`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[57 專案資料與操作安全](../lessons/57.md)、[64 權限與 Sandbox 邊界實驗](lesson-briefs.md#lesson-64)、[73 讀懂 Hook 事件：輸入、輸出與退出碼](lesson-briefs.md#lesson-73)。
- 本篇交付：邊界檢查器、假機密檔與路徑案例表。
- 材料包：`hook-lab`；本篇須提供可獨立開始的快照。

1. 定義受保護的練習目錄。
2. 正規化相對路徑與大小寫。
3. 測試正常、越界及別名路徑。
4. 記錄未涵蓋工具並搭配權限機制。

**故障練習：**把單一 Edit Hook 說成所有 shell 寫入都受保護；如實列出覆蓋範圍。

**完成判準：**列出的工具案例結果正確；拒絕訊息能說明原因；假機密內容未進入 log。

**作者需查證：**[Hooks reference](https://code.claude.com/docs/en/hooks)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[78 跨平台 Hooks：中文路徑、逾時與遞迴排錯](lesson-briefs.md#lesson-78)、[83 MCP 回傳含有指令時：資料與操作權限分開](lesson-briefs.md#lesson-83)、[92 CI 審查助手：權限、fork 與結果附件](lesson-briefs.md#lesson-92)。

[回第二階段總目錄](README.md)

<a id="lesson-77"></a>

### 77．任務通知與事件紀錄：有用而不洗版

[完整原稿](../lessons/77.md)

產生可追查、去重且不含敏感內容的通知紀錄。

- 預定網址：`/zh-TW/life/claude-code-hook-notifications-audit`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[42 Hooks 實用案例](../lessons/42.md)、[73 讀懂 Hook 事件：輸入、輸出與退出碼](lesson-briefs.md#lesson-73)。
- 本篇交付：本機通知接收器、JSONL 紀錄與清理指引。
- 材料包：`hook-lab`；本篇須提供可獨立開始的快照。

1. 決定哪些狀態值得記錄。
2. 加入任務識別碼與結果欄位。
3. 使用本機假接收器測重送與重複。
4. 模擬接收器失效並確認主要工作行為。

**故障練習：**把通知成功當工作成功；分開保存執行結果與通知結果。

**完成判準：**同一事件不重複提醒；log 不保存金鑰或完整私人內容；錯誤與主要結果可分辨。

**作者需查證：**[Hooks reference](https://code.claude.com/docs/en/hooks)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[75 建立可停止的品質檢查 Hook](lesson-briefs.md#lesson-75)、[78 跨平台 Hooks：中文路徑、逾時與遞迴排錯](lesson-briefs.md#lesson-78)、[93 排程失敗怎麼辦：重複執行、漏跑與停止](lesson-briefs.md#lesson-93)。

[回第二階段總目錄](README.md)

<a id="lesson-78"></a>

### 78．跨平台 Hooks：中文路徑、逾時與遞迴排錯

[完整原稿](../lessons/78.md)

把 Hook 做成可測試、可停用、可移植的工具。

- 預定網址：`/zh-TW/life/claude-code-hook-portability-recovery`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[73 讀懂 Hook 事件：輸入、輸出與退出碼](lesson-briefs.md#lesson-73)、[74 只處理變更檔案的格式化 Hook](lesson-briefs.md#lesson-74)、[75 建立可停止的品質檢查 Hook](lesson-briefs.md#lesson-75)。
- 本篇交付：跨平台測試矩陣與停用／還原手冊。
- 材料包：`hook-lab`；本篇須提供可獨立開始的快照。

1. 測含空白與中文的專案路徑。
2. 檢查 LF、CRLF、編碼及 shell 選擇。
3. 注入慢速、失敗與重複事件。
4. 驗證停用設定後的正常工作。

**故障練習：**只在開發者機器成功；於支援的乾淨環境重播相同 fixtures。

**完成判準：**實際測過的平台各有輸出；其他平台標待測；故障不形成持續執行的子程序。

**作者需查證：**[Hooks reference](https://code.claude.com/docs/en/hooks)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[72 把 Skills 與 Hooks 包成可版本管理的 Plugin](lesson-briefs.md#lesson-72)、[76 用 Hook 保護指定檔案並測試路徑邊界](lesson-briefs.md#lesson-76)、[77 任務通知與事件紀錄：有用而不洗版](lesson-briefs.md#lesson-77)。

[回第二階段總目錄](README.md)

## N．MCP 工具開發與串接

<a id="lesson-79"></a>

### 79．建立自己的唯讀 MCP 工具

[完整原稿](../lessons/79.md)

讓 Claude 查詢本機練習待辦資料。

- 預定網址：`/zh-TW/life/claude-code-mcp-local-server-workshop`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[43 Claude Code 接 MCP 入門](../lessons/43.md)、[44 MCP 安裝、設定與排錯](../lessons/44.md)。
- 本篇交付：最小 MCP server、假待辦資料與連線紀錄。
- 材料包：`mcp-lab`；本篇須提供可獨立開始的快照。

1. 選擇並固定官方 SDK 版本。
2. 先以測試客戶端列工具及直接呼叫。
3. 接入 Claude Code 的本機設定。
4. 完成查詢並正常關閉程序。

**故障練習：**只看到 Connected 就算成功；必須有一筆可核對工具結果。

**完成判準：**直接呼叫及 Claude 真實呼叫都回傳指定假資料；資料檔沒有被改寫。

**作者需查證：**[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[80 設計 MCP 工具名稱、輸入 Schema 與分頁](lesson-briefs.md#lesson-80)、[82 MCP 排錯實驗室：斷線、逾時與格式錯誤](lesson-briefs.md#lesson-82)、[83 MCP 回傳含有指令時：資料與操作權限分開](lesson-briefs.md#lesson-83)。

[回第二階段總目錄](README.md)

<a id="lesson-80"></a>

### 80．設計 MCP 工具名稱、輸入 Schema 與分頁

[完整原稿](../lessons/80.md)

讓模型能選對工具，也能正確處理空值與大量結果。

- 預定網址：`/zh-TW/life/claude-code-mcp-tool-contracts`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[79 建立自己的唯讀 MCP 工具](lesson-briefs.md#lesson-79)。
- 本篇交付：list_tasks、get_task 契約與邊界測試。
- 材料包：`mcp-lab`；本篇須提供可獨立開始的快照。

1. 區分清單及單筆查詢用途。
2. 定義必要欄位及無效輸入行為。
3. 加入分頁上限和空結果。
4. 用自然語言任務觀察工具選擇。

**故障練習：**回傳大量全文擠滿上下文；提供摘要及明確下一頁資訊。

**完成判準：**空清單、未知 ID、無效參數及多頁結果均有測試；無靜默截斷。

**作者需查證：**[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[81 遠端 MCP 登入、授權範圍與重新認證](lesson-briefs.md#lesson-81)、[82 MCP 排錯實驗室：斷線、逾時與格式錯誤](lesson-briefs.md#lesson-82)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。

[回第二階段總目錄](README.md)

<a id="lesson-81"></a>

### 81．遠端 MCP 登入、授權範圍與重新認證

[完整原稿](../lessons/81.md)

在測試服務演練連線與權限故障。

- 預定網址：`/zh-TW/life/claude-code-mcp-http-auth-workshop`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 75 分鐘。這是編輯估算，試作後校正。
- 先備：[44 MCP 安裝、設定與排錯](../lessons/44.md)、[57 專案資料與操作安全](../lessons/57.md)、[79 建立自己的唯讀 MCP 工具](lesson-briefs.md#lesson-79)。
- 本篇交付：測試服務設定、授權檢查表與撤銷紀錄。
- 材料包：`mcp-lab`；本篇須提供可獨立開始的快照。

1. 區分傳輸方式與認證機制。
2. 接入受控測試服務並確認最小權限。
3. 演練憑證過期及權限不足。
4. 撤銷登入並重查存取。

**故障練習：**將 401、403 及網路錯誤混成同一問題；依階段定位。

**完成判準：**授權前、授權後、撤銷後結果不同且可解釋；不得把 mock 認證當真實 OAuth 完成。

**作者需查證：**[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[80 設計 MCP 工具名稱、輸入 Schema 與分頁](lesson-briefs.md#lesson-80)、[82 MCP 排錯實驗室：斷線、逾時與格式錯誤](lesson-briefs.md#lesson-82)、[83 MCP 回傳含有指令時：資料與操作權限分開](lesson-briefs.md#lesson-83)。

[回第二階段總目錄](README.md)

<a id="lesson-82"></a>

### 82．MCP 排錯實驗室：斷線、逾時與格式錯誤

[完整原稿](../lessons/82.md)

用固定故障重現診斷及復原流程。

- 預定網址：`/zh-TW/life/claude-code-mcp-failure-contract-tests`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[79 建立自己的唯讀 MCP 工具](lesson-briefs.md#lesson-79)、[80 設計 MCP 工具名稱、輸入 Schema 與分頁](lesson-briefs.md#lesson-80)。
- 本篇交付：故障注入器、契約測試與排錯決策表。
- 材料包：`mcp-lab`；本篇須提供可獨立開始的快照。

1. 建立成功連線基準。
2. 依序注入進程退出、逾時及錯誤回應。
3. 記錄客戶端及 server 診斷。
4. 修正後重跑相同操作。

**故障練習：**一律重裝全部工具；用最小直接呼叫縮小故障位置。

**完成判準：**每種症狀有原因及修復證據；重新連線後沒有重複程序或錯用舊結果。

**作者需查證：**[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[81 遠端 MCP 登入、授權範圍與重新認證](lesson-briefs.md#lesson-81)、[83 MCP 回傳含有指令時：資料與操作權限分開](lesson-briefs.md#lesson-83)、[94 Agent SDK：保存狀態、取消與重新接續](lesson-briefs.md#lesson-94)。

[回第二階段總目錄](README.md)

<a id="lesson-83"></a>

### 83．MCP 回傳含有指令時：資料與操作權限分開

[完整原稿](../lessons/83.md)

以無害的對抗案例測試工具資料處理。

- 預定網址：`/zh-TW/life/claude-code-mcp-untrusted-output`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[57 專案資料與操作安全](../lessons/57.md)、[64 權限與 Sandbox 邊界實驗](lesson-briefs.md#lesson-64)、[79 建立自己的唯讀 MCP 工具](lesson-briefs.md#lesson-79)。
- 本篇交付：合成外部內容、預期行為與觀察紀錄。
- 材料包：`mcp-lab`；本篇須提供可獨立開始的快照。

1. 建立含假冒操作指示的工具資料。
2. 設置無害標記檔觀察是否越界。
3. 在最小權限下執行讀取任務。
4. 比對預期與實際行為並保存失敗案例。

**故障練習：**用一句提示宣稱解決所有注入；保留工具權限及隔離層的限制。

**完成判準：**資料來源可追查；越界要求不被當使用者授權；若失敗如實記錄，修正邊界後再驗證。

**作者需查證：**[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[76 用 Hook 保護指定檔案並測試路徑邊界](lesson-briefs.md#lesson-76)、[81 遠端 MCP 登入、授權範圍與重新認證](lesson-briefs.md#lesson-81)、[84 從 Issue 到變更草稿：串起工具與程式碼](lesson-briefs.md#lesson-84)。

[回第二階段總目錄](README.md)

<a id="lesson-84"></a>

### 84．從 Issue 到變更草稿：串起工具與程式碼

[完整原稿](../lessons/84.md)

完成需求讀取、計畫、測試與 PR 說明稿。

- 預定網址：`/zh-TW/life/claude-code-issue-to-draft-pr-workshop`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[35 Git、差異審查與 PR](../lessons/35.md)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)、[79 建立自己的唯讀 MCP 工具](lesson-briefs.md#lesson-79)。
- 本篇交付：假 Issue、功能 diff、測試結果與 PR-body.md。
- 材料包：`mcp-lab`；本篇須提供可獨立開始的快照。

1. 先讀本機 fixture Issue。
2. 整理驗收條件並定位程式。
3. 用既有 CLI 或 MCP 取得需要的資訊。
4. 實作後輸出草稿與證據。

**故障練習：**把可用 MCP 強套所有步驟；在工具比較中說明何時 CLI 已足夠。

**完成判準：**Issue 條件均對應檔案及測試；主練習在本機可完成；選修測試 repo 才建立真正 draft PR。

**作者需查證：**[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[83 MCP 回傳含有指令時：資料與操作權限分開](lesson-briefs.md#lesson-83)、[85 真正走完一次重現、失敗測試與修正](lesson-briefs.md#lesson-85)、[92 CI 審查助手：權限、fork 與結果附件](lesson-briefs.md#lesson-92)。

[回第二階段總目錄](README.md)

## O．開發驗證、多代理與跨裝置

<a id="lesson-85"></a>

### 85．真正走完一次重現、失敗測試與修正

[完整原稿](../lessons/85.md)

定位跨資料層及介面層的待辦狀態錯誤。

- 預定網址：`/zh-TW/life/claude-code-tdd-debugging-workshop`。
- 建議入口：CLI、桌面、IDE；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[34 除錯與補測試](../lessons/34.md)、[55 完整實作：待辦清單網站](../lessons/55.md)。
- 本篇交付：可重現案例、紅綠測試紀錄與最小修正。
- 材料包：`todo-workbench`；本篇須提供可獨立開始的快照。

1. 先在瀏覽器重現並保存輸入。
2. 建立修正前必敗的行為測試。
3. 定位根因後做最小修改。
4. 驗證主要路徑及一個相鄰回歸案例。

**故障練習：**測試只重述實作或 mock 掉錯誤；以使用者可見行為作斷言。

**完成判準：**同一測試修正前失敗、修正後通過；沒有移除驗收條件以通過。

**作者需查證：**[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)、[Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[86 接手缺測試舊專案：先留住行為再重構](lesson-briefs.md#lesson-86)、[87 讓 Subagent 提出可核對的審查發現](lesson-briefs.md#lesson-87)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。

[回第二階段總目錄](README.md)

<a id="lesson-86"></a>

### 86．接手缺測試舊專案：先留住行為再重構

[完整原稿](../lessons/86.md)

用小步變更拆出可測試模組。

- 預定網址：`/zh-TW/life/claude-code-legacy-refactoring-workshop`。
- 建議入口：CLI、桌面、IDE；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[56 接手舊專案與逐步重構](../lessons/56.md)、[85 真正走完一次重現、失敗測試與修正](lesson-briefs.md#lesson-85)。
- 本篇交付：既有行為案例、三個小 diff 與回復點。
- 材料包：`todo-workbench`；本篇須提供可獨立開始的快照。

1. 盤點目前行為與已知缺陷。
2. 建立關鍵行為基準。
3. 逐步抽離資料存取與畫面邏輯。
4. 逐步測試並核對預期保持的行為。

**故障練習：**混合重構與新功能使失敗難定位；拆開提交及驗收。

**完成判準：**每一步可獨立說明及回復；已知缺陷不被誤寫成理想規格。

**作者需查證：**[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)、[Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[62 Monorepo 的分層 MD 與路徑規則](lesson-briefs.md#lesson-62)、[87 讓 Subagent 提出可核對的審查發現](lesson-briefs.md#lesson-87)、[88 雙 Worktree 實作與衝突整合](lesson-briefs.md#lesson-88)。

[回第二階段總目錄](README.md)

<a id="lesson-87"></a>

### 87．讓 Subagent 提出可核對的審查發現

[完整原稿](../lessons/87.md)

設計專責代理的範圍、工具及回報格式。

- 預定網址：`/zh-TW/life/claude-code-subagent-review-workshop`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[46 Subagents 與代理 MD 設定](../lessons/46.md)、[85 真正走完一次重現、失敗測試與修正](lesson-briefs.md#lesson-85)。
- 本篇交付：專責代理 MD、審查報告與主代理核對表。
- 材料包：`todo-workbench`；本篇須提供可獨立開始的快照。

1. 分出正確性與介面兩種讀取任務。
2. 設定必要工具及固定報告欄位。
3. 交付有檔案位置的發現。
4. 由主代理重現、去重及駁回誤報。

**故障練習：**把兩份同樣的意見當兩次獨立測試；追查各自使用的證據。

**完成判準：**每個採納發現有獨立證據；未驗證項目明列；角色完成不等於整體驗收完成。

**作者需查證：**[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)、[Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[71 替 Skills 建立回歸案例與評分表](lesson-briefs.md#lesson-71)、[88 雙 Worktree 實作與衝突整合](lesson-briefs.md#lesson-88)、[89 Agent Teams 的分工、阻塞與成果整合](lesson-briefs.md#lesson-89)。

[回第二階段總目錄](README.md)

<a id="lesson-88"></a>

### 88．雙 Worktree 實作與衝突整合

[完整原稿](../lessons/88.md)

隔離兩項功能，最後完成整合與回歸。

- 預定網址：`/zh-TW/life/claude-code-worktree-integration-workshop`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[35 Git、差異審查與 PR](../lessons/35.md)、[47 Git Worktree 平行工作](../lessons/47.md)、[65 長任務的上下文整理與交接文件](lesson-briefs.md#lesson-65)。
- 本篇交付：兩個工作目錄、獨立埠號與整合檢查表。
- 材料包：`todo-workbench`；本篇須提供可獨立開始的快照。

1. 拆分可獨立工作的兩個功能。
2. 建立 worktree 並分配埠號及暫存檔。
3. 完成後製造並解決小型受控衝突。
4. 在整合分支重跑驗收並清理。

**故障練習：**以為隔離 Git 就隔離資料庫或服務；檢查共用資源與相依。

**完成判準：**兩邊不改到同一工作目錄；保留雙方需求；未提交資料不在清理時遺失。

**作者需查證：**[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)、[Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[86 接手缺測試舊專案：先留住行為再重構](lesson-briefs.md#lesson-86)、[87 讓 Subagent 提出可核對的審查發現](lesson-briefs.md#lesson-87)、[89 Agent Teams 的分工、阻塞與成果整合](lesson-briefs.md#lesson-89)。

[回第二階段總目錄](README.md)

<a id="lesson-89"></a>

### 89．Agent Teams 的分工、阻塞與成果整合

[完整原稿](../lessons/89.md)

比較單代理、專責代理與團隊協作成本。

- 預定網址：`/zh-TW/life/claude-code-agent-teams-integration-lab`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 75 分鐘。這是編輯估算，試作後校正。
- 先備：[48 Agent Teams 協作](../lessons/48.md)、[87 讓 Subagent 提出可核對的審查發現](lesson-briefs.md#lesson-87)、[88 雙 Worktree 實作與衝突整合](lesson-briefs.md#lesson-88)。
- 本篇交付：小型團隊任務表、成本紀錄與整合成果。
- 材料包：`todo-workbench`；本篇須提供可獨立開始的快照。

1. 先測同一小任務的單代理基準。
2. 分派兩個互不覆蓋的責任。
3. 模擬一位卡住與需求變動。
4. 整合測試並正常結束角色。

**故障練習：**新增角色卻沒縮短工作；比較整合時間、錯誤與用量，不能只看並行數。

**完成判準：**支援版本才實測團隊功能；不支援時交付 worktree 替代版，明確標示未實測 Teams。

**作者需查證：**[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)、[Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[65 長任務的上下文整理與交接文件](lesson-briefs.md#lesson-65)、[90 桌面到手機：離線、中斷與返回工作現場](lesson-briefs.md#lesson-90)、[95 比較流程品質、用量與執行時間](lesson-briefs.md#lesson-95)。

[回第二階段總目錄](README.md)

<a id="lesson-90"></a>

### 90．桌面到手機：離線、中斷與返回工作現場

[完整原稿](../lessons/90.md)

確認執行位置，練習接續及故障後的核對。

- 預定網址：`/zh-TW/life/claude-code-cross-device-recovery-workshop`。
- 建議入口：CLI、桌面、手機、網頁；預估閱讀 20 分鐘，實作 75 分鐘。這是編輯估算，試作後校正。
- 先備：[16 Remote Control：接續電腦上的工作](../lessons/16.md)、[17 Dispatch：從手機派送桌面任務](../lessons/17.md)、[18 跨裝置接續工作的完整流程](../lessons/18.md)、[65 長任務的上下文整理與交接文件](lesson-briefs.md#lesson-65)。
- 本篇交付：裝置／執行位置圖與三種中斷紀錄。
- 材料包：`todo-workbench`；本篇須提供可獨立開始的快照。

1. 選一種帳號可用入口建立基準。
2. 查看手機補充指示與電腦執行結果。
3. 分別測手機離線、主機睡眠或程序退出。
4. 返回時核對 session、工作目錄及未提交變更。

**故障練習：**把手機畫面仍在當成本機任務仍運行；以主機程序與實際產出確認。

**完成判準：**選定入口有一次真實裝置接續；其他入口標未測；雲端與本機檔案流向可分辨。

**作者需查證：**[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)、[Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[27 繼續、找回與管理對話](../lessons/27.md)、[88 雙 Worktree 實作與衝突整合](lesson-briefs.md#lesson-88)、[93 排程失敗怎麼辦：重複執行、漏跑與停止](lesson-briefs.md#lesson-93)。

[回第二階段總目錄](README.md)

## P．可追蹤、可恢復的自動化

<a id="lesson-91"></a>

### 91．把 claude -p 接進有驗證的 JSON 流程

[完整原稿](../lessons/91.md)

處理合法結果、錯誤、逾時與不完整輸出。

- 預定網址：`/zh-TW/life/claude-code-structured-cli-pipeline`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[51 非互動執行與 JSON 輸出](../lessons/51.md)、[34 除錯與補測試](../lessons/34.md)。
- 本篇交付：輸入 fixtures、Schema、runner 與錯誤結果。
- 材料包：`automation-lab`；本篇須提供可獨立開始的快照。

1. 定義可機器驗證的輸出契約。
2. 分開 CLI 回傳外殼與業務資料。
3. 解析一般 JSON 及串流事件。
4. 處理逾時與不合法結果並決定退出碼。

**故障練習：**只檢查 JSON 能 parse；仍要驗證欄位、型別與業務條件。

**完成判準：**合成及真實呼叫分開記錄；錯誤不會被當成空成功資料；引號與換行保留。

**作者需查證：**[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)、[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[68 Skill 參數驗證：缺值、錯誤與危險字元](lesson-briefs.md#lesson-68)、[82 MCP 排錯實驗室：斷線、逾時與格式錯誤](lesson-briefs.md#lesson-82)、[94 Agent SDK：保存狀態、取消與重新接續](lesson-briefs.md#lesson-94)。

[回第二階段總目錄](README.md)

<a id="lesson-92"></a>

### 92．CI 審查助手：權限、fork 與結果附件

[完整原稿](../lessons/92.md)

在測試儲存庫跑一次可審閱的工作流程。

- 預定網址：`/zh-TW/life/claude-code-github-actions-review-workshop`。
- 建議入口：CLI、網頁；預估閱讀 20 分鐘，實作 75 分鐘。這是編輯估算，試作後校正。
- 先備：[53 GitHub Actions 整合](../lessons/53.md)、[57 專案資料與操作安全](../lessons/57.md)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。
- 本篇交付：workflow、最小權限表與審查 artifact。
- 材料包：`automation-lab`；本篇須提供可獨立開始的快照。

1. 先建立沒有模型呼叫的基準 workflow。
2. 加入測試帳號的受控呼叫。
3. 處理外部 PR、機密與不可信內容。
4. 下載結果並驗證取消及失敗流程。

**故障練習：**只貼 YAML 就宣稱 CI 完成；保存 run、來源提交與所用 action 版本。

**完成判準：**測試儲存庫有實際 run；外部 PR 不取得秘密；結果以附件交付且不自動合併。

**作者需查證：**[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)、[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[64 權限與 Sandbox 邊界實驗](lesson-briefs.md#lesson-64)、[84 從 Issue 到變更草稿：串起工具與程式碼](lesson-briefs.md#lesson-84)、[93 排程失敗怎麼辦：重複執行、漏跑與停止](lesson-briefs.md#lesson-93)。

[回第二階段總目錄](README.md)

<a id="lesson-93"></a>

### 93．排程失敗怎麼辦：重複執行、漏跑與停止

[完整原稿](../lessons/93.md)

為一次排程建立可追查且不重複寫入的工作。

- 預定網址：`/zh-TW/life/claude-code-scheduled-workflow-reliability`。
- 建議入口：CLI、桌面、網頁；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[52 排程與重複任務](../lessons/52.md)、[77 任務通知與事件紀錄：有用而不洗版](lesson-briefs.md#lesson-77)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。
- 本篇交付：run-state.json、識別碼設計與故障演練。
- 材料包：`automation-lab`；本篇須提供可獨立開始的快照。

1. 先將工作做成可手動重跑。
2. 選定一個支援入口及執行主機。
3. 注入重複觸發與程序中斷。
4. 驗證取消、補跑與重複結果處理。

**故障練習：**把所有入口的排程能力混用；在每個範例標明持久性與主機條件。

**完成判準：**同一工作識別碼不重複產生最終成果；能從紀錄辨別未跑、失敗與成功。

**作者需查證：**[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)、[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[70 Skill 何時啟動：手動呼叫與自動選用](lesson-briefs.md#lesson-70)、[90 桌面到手機：離線、中斷與返回工作現場](lesson-briefs.md#lesson-90)、[94 Agent SDK：保存狀態、取消與重新接續](lesson-briefs.md#lesson-94)。

[回第二階段總目錄](README.md)

<a id="lesson-94"></a>

### 94．Agent SDK：保存狀態、取消與重新接續

[完整原稿](../lessons/94.md)

建立可中斷且可診斷的最小代理程式。

- 預定網址：`/zh-TW/life/claude-code-agent-sdk-stateful-runner`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 75 分鐘。這是編輯估算，試作後校正。
- 先備：[54 Claude Agent SDK 入門](../lessons/54.md)、[65 長任務的上下文整理與交接文件](lesson-briefs.md#lesson-65)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。
- 本篇交付：最小 runner、狀態檔、事件紀錄與恢復測試。
- 材料包：`automation-lab`；本篇須提供可獨立開始的快照。

1. 選定一種官方語言 SDK 並固定版本。
2. 管理開始、執行、失敗與完成狀態。
3. 測試取消與重新啟動。
4. 分辨 session 接續與外部副作用還原。

**故障練習：**只存 ID 卻沒存輸入與版本；保存必要的重現上下文。

**完成判準：**取消後不殘留工作程序；恢復可辨識既有成果；不把 session ID 當通用交易回滾。

**作者需查證：**[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)、[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[82 MCP 排錯實驗室：斷線、逾時與格式錯誤](lesson-briefs.md#lesson-82)、[93 排程失敗怎麼辦：重複執行、漏跑與停止](lesson-briefs.md#lesson-93)、[95 比較流程品質、用量與執行時間](lesson-briefs.md#lesson-95)。

[回第二階段總目錄](README.md)

<a id="lesson-95"></a>

### 95．比較流程品質、用量與執行時間

[完整原稿](../lessons/95.md)

以同一資料集比較兩種工作方法。

- 預定網址：`/zh-TW/life/claude-code-workflow-evaluation-cost`。
- 建議入口：CLI；預估閱讀 20 分鐘，實作 45 分鐘。這是編輯估算，試作後校正。
- 先備：[58 用量、成本與效率調整](../lessons/58.md)、[71 替 Skills 建立回歸案例與評分表](lesson-briefs.md#lesson-71)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。
- 本篇交付：固定案例集、原始數據 CSV 與比較報告。
- 材料包：`automation-lab`；本篇須提供可獨立開始的快照。

1. 先定義正確率及可接受品質。
2. 固定任務、模型版本與計量方式。
3. 比較單代理、多代理或兩種上下文策略。
4. 分析失敗重試與總時間。

**故障練習：**只算成功那次呼叫；把重試、等待與人工整合時間也列入。

**完成判準：**報告有樣本數、原始紀錄與未計入項目；價格注明來源及日期；不做保證省費的結論。

**作者需查證：**[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)、[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[89 Agent Teams 的分工、阻塞與成果整合](lesson-briefs.md#lesson-89)、[94 Agent SDK：保存狀態、取消與重新接續](lesson-briefs.md#lesson-94)、[96 期末實作：可維護的待辦專案工作流程](lesson-briefs.md#lesson-96)。

[回第二階段總目錄](README.md)

<a id="lesson-96"></a>

### 96．期末實作：可維護的待辦專案工作流程

[完整原稿](../lessons/96.md)

整合規則、技能、工具及驗證，交付一次完整變更。

- 預定網址：`/zh-TW/life/claude-code-advanced-capstone`。
- 建議入口：CLI、桌面；預估閱讀 20 分鐘，實作 180 分鐘。這是編輯估算，試作後校正。
- 先備：[55 完整實作：待辦清單網站](../lessons/55.md)、[61 替真實專案設計 CLAUDE.md](lesson-briefs.md#lesson-61)、[67 把一套工作 SOP 做成可重用 Skill](lesson-briefs.md#lesson-67)、[73 讀懂 Hook 事件：輸入、輸出與退出碼](lesson-briefs.md#lesson-73)、[79 建立自己的唯讀 MCP 工具](lesson-briefs.md#lesson-79)、[85 真正走完一次重現、失敗測試與修正](lesson-briefs.md#lesson-85)、[91 把 claude -p 接進有驗證的 JSON 流程](lesson-briefs.md#lesson-91)。
- 本篇交付：需求單、設定包、功能 diff、故障紀錄與交付報告。
- 材料包：`automation-lab`；本篇須提供可獨立開始的快照。

1. 抽取一張待辦功能需求。
2. 依問題選用規則、Skill、Hook 或 MCP。
3. 實作後處理一個指定故障。
4. 整合測試並交付可供審查的版本。

**故障練習：**工具很多卻無法說明用途；每項工具都對應實際需求與可測成果。

**完成判準：**完整驗收表均有證據；能從乾淨下載材料重現；不強制為了湊功能使用所有工具。

**作者需查證：**[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)、[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)。查證日期與實際操作紀錄分開；本文流程尚未實測。

延伸閱讀：[88 雙 Worktree 實作與衝突整合](lesson-briefs.md#lesson-88)、[94 Agent SDK：保存狀態、取消與重新接續](lesson-briefs.md#lesson-94)、[95 比較流程品質、用量與執行時間](lesson-briefs.md#lesson-95)。

[回第二階段總目錄](README.md)
