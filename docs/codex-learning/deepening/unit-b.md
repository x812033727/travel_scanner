# B｜安裝與電腦：深入製作規格

[返回深入製作總目錄](README.md) · [共同驗收表與批次](review-checklist.md)

完成安裝、登入、定位專案與第一次修改，分開確認每個階段。

**本文件是補強與驗收規格，不是操作完成紀錄。** 本單元六篇已有五語草稿，是否通過以實際審核證據為準。以下時間沿用現有目錄估計，待讀者操作後調整。

## 本輪審核狀態

ID 05、35、36、37、14 已補強輸入位置、環境區分與恢復步驟，見 [B 單元證據](../evidence/unit-b-depth-review.json)；ID 03 沿用[代表稿紀錄](../evidence/representative-depth-review.json)。Windows 建立區塊實測新建成功、同名停止且不覆寫；IDE 精確參考函式通過原測試，還原後重現原錯誤。這些是本機教材參考檢查，沒有執行安裝、登入、IDE 產品操作或其他平台實測，全部仍待完整終審與畫面驗收。

## 單元編輯重點

Windows、macOS、Linux／WSL 各自寫明安裝來源、開啟終端機、版本、路徑、登入、更新及退出；桌面與 IDE 支援狀態以各篇官方來源重新核對。未實測環境明列查證方式。

每篇操作需補足位置、完整輸入、預期結果、分歧處理及至少三項適用的常見問題；下列失敗案例是指定必查情境，不取代完整 FAQ。所有篇章依[共同驗收表](review-checklist.md)核對五語、來源、圖片、連結及還原。

## 本單元目錄

- [ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)
- [ID 35｜Windows CLI 安裝與排錯](unit-b.md#lesson-35)
- [ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36)
- [ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37)
- [ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)
- [ID 14｜IDE 擴充套件入門](unit-b.md#lesson-14)

<a id="lesson-05"></a>

## ID 05｜Codex CLI 安裝與入門

閱讀順序 07；估計閱讀 12 分鐘、操作 25 分鐘。永久 slug：`codex-cli-getting-started`。

先備規劃：[ID 34｜終端機與路徑：找到專案根目錄](unit-a.md#lesson-34)

現有作者稿：[繁中](../deep/zh-TW/05.md) · [英文](../deep/en/05.md) · [日文](../deep/ja/05.md) · [韓文](../deep/ko/05.md) · [五語內容包（含簡中）](../../../apps/api/app/guides/content/codex-cli-getting-started.json)。簡中由固定轉換流程產出，仍須獨立校對。

### 練習起點與逐步內容

**起點材料：** 空白 CLI 練習資料夾、兩行 greeting.txt 與原始副本。

**操作順序：** 依平台選安裝篇；確認版本、登入與位置；要求一次指定行修改。

**預計交付：** 第一次 CLI 工作的完整輸入與檔案差異。

### 成功、失敗與恢復

**成功判準：** 實際檔案只改了指定行，版本與登入狀態可查，能正常退出。

**指定失敗／邊界案例：** 命令不存在、把 shell 命令貼進對話、從錯誤資料夾開始。

**恢復或停止：** 退出後用原始副本還原 greeting.txt，不清除全域設定。

### 圖片與延伸

**需補或核對的圖文：** shell 與 Codex 對話的輸入位置對照圖。 必須記錄來源、環境、日期及五語替代文字／圖說；圖解不能代替產品實際操作證據。無法操作的平台依官方文件查證並標明未實測。

相關規劃：[ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)、[ID 11｜CLI 命令與斜線指令](unit-e.md#lesson-11)、[ID 12｜新手問題排除](unit-j.md#lesson-12)

驗收時對照[本篇官方來源清單](../deep/sources.json)中的 ID 05 與作者稿來源段落；核對文字支持的操作及版本，網址回應正常不等同內容正確。

[返回深入製作總目錄](README.md) · 下一篇：[ID 35｜Windows CLI 安裝與排錯](unit-b.md#lesson-35)

<a id="lesson-35"></a>

## ID 35｜Windows CLI 安裝與排錯

閱讀順序 08；估計閱讀 12 分鐘、操作 25 分鐘。永久 slug：`codex-cli-windows`。

先備規劃：[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)

現有作者稿：[繁中](../deep/zh-TW/35.md) · [英文](../deep/en/35.md) · [日文](../deep/ja/35.md) · [韓文](../deep/ko/35.md) · [五語內容包（含簡中）](../../../apps/api/app/guides/content/codex-cli-windows.json)。簡中由固定轉換流程產出，仍須獨立校對。

### 練習起點與逐步內容

**起點材料：** 一般權限 PowerShell 與新的含空格練習路徑。

**操作順序：** 分開獨立版和 npm 安裝；查看實際執行來源；登入、讀檔並記錄更新方式。

**預計交付：** Windows 安裝、來源與讀檔診斷紀錄。

### 成功、失敗與恢復

**成功判準：** 新終端機能找到預期程式，讀到標記，唯讀前後檔案雜湊相同。

**指定失敗／邊界案例：** PATH 指到另一份安裝；.ps1 政策問題；Windows 與 WSL 位置混淆。

**恢復或停止：** 沿原安裝管道修復或更新；保留其他已安裝工具及原設定。

### 圖片與延伸

**需補或核對的圖文：** Windows 命令來源畫面；遮蔽個人使用者目錄。 必須記錄來源、環境、日期及五語替代文字／圖說；圖解不能代替產品實際操作證據。無法操作的平台依官方文件查證並標明未實測。

相關規劃：[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)、[ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36)、[ID 12｜新手問題排除](unit-j.md#lesson-12)

驗收時對照[本篇官方來源清單](../deep/sources.json)中的 ID 35 與作者稿來源段落；核對文字支持的操作及版本，網址回應正常不等同內容正確。

[返回深入製作總目錄](README.md) · 上一篇：[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05) · 下一篇：[ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36)

<a id="lesson-36"></a>

## ID 36｜macOS CLI 安裝與排錯

閱讀順序 09；估計閱讀 12 分鐘、操作 25 分鐘。永久 slug：`codex-cli-macos`。

先備規劃：[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)

現有作者稿：[繁中](../deep/zh-TW/36.md) · [英文](../deep/en/36.md) · [日文](../deep/ja/36.md) · [韓文](../deep/ko/36.md) · [五語內容包（含簡中）](../../../apps/api/app/guides/content/codex-cli-macos.json)。簡中由固定轉換流程產出，仍須獨立校對。

### 練習起點與逐步內容

**起點材料：** macOS Terminal、獨立練習目錄與原始檔案副本。

**操作順序：** 辨識 shell 與安裝來源；確認 PATH；登入、讀檔、更新及退出。

**預計交付：** macOS 指令與安裝來源檢查表。

### 成功、失敗與恢復

**成功判準：** 新的 Terminal 可找到同一 CLI，練習檔可讀且未被修改。

**指定失敗／邊界案例：** EACCES、不同視窗 PATH 不同、更新後仍選到舊程式。

**恢復或停止：** 只修正已確認的安裝或 PATH 項目，保留 shell 設定備份。

### 圖片與延伸

**需補或核對的圖文：** macOS 畫面有則標示實測，否則保留官方查證標籤。 必須記錄來源、環境、日期及五語替代文字／圖說；圖解不能代替產品實際操作證據。無法操作的平台依官方文件查證並標明未實測。

相關規劃：[ID 35｜Windows CLI 安裝與排錯](unit-b.md#lesson-35)、[ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37)、[ID 12｜新手問題排除](unit-j.md#lesson-12)

驗收時對照[本篇官方來源清單](../deep/sources.json)中的 ID 36 與作者稿來源段落；核對文字支持的操作及版本，網址回應正常不等同內容正確。

[返回深入製作總目錄](README.md) · 上一篇：[ID 35｜Windows CLI 安裝與排錯](unit-b.md#lesson-35) · 下一篇：[ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37)

<a id="lesson-37"></a>

## ID 37｜Linux／WSL CLI 與檔案位置

閱讀順序 10；估計閱讀 12 分鐘、操作 30 分鐘。永久 slug：`codex-cli-linux-wsl`。

先備規劃：[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)

現有作者稿：[繁中](../deep/zh-TW/37.md) · [英文](../deep/en/37.md) · [日文](../deep/ja/37.md) · [韓文](../deep/ko/37.md) · [五語內容包（含簡中）](../../../apps/api/app/guides/content/codex-cli-linux-wsl.json)。簡中由固定轉換流程產出，仍須獨立校對。

### 練習起點與逐步內容

**起點材料：** Linux 或獨立 WSL 練習位置；Windows 主機資料另外標記。

**操作順序：** 辨識目前 OS、架構與 HOME；安裝於實際使用環境；完成相同唯讀練習。

**預計交付：** 主機／WSL 對照與 Linux 操作紀錄。

### 成功、失敗與恢復

**成功判準：** 能說出命令與檔案位於哪個系統，登入和讀檔在同一環境完成。

**指定失敗／邊界案例：** 將 Windows 程式路徑套到 WSL；混用兩邊設定；把不支援環境當成已驗證。

**恢復或停止：** 回到選定系統修復一個原因；不重設整套 WSL 或刪除使用者目錄。

### 圖片與延伸

**需補或核對的圖文：** 主機與子系統的檔案、設定位置圖。 必須記錄來源、環境、日期及五語替代文字／圖說；圖解不能代替產品實際操作證據。無法操作的平台依官方文件查證並標明未實測。

相關規劃：[ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36)、[ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)、[ID 12｜新手問題排除](unit-j.md#lesson-12)

驗收時對照[本篇官方來源清單](../deep/sources.json)中的 ID 37 與作者稿來源段落；核對文字支持的操作及版本，網址回應正常不等同內容正確。

[返回深入製作總目錄](README.md) · 上一篇：[ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36) · 下一篇：[ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)

<a id="lesson-03"></a>

## ID 03｜桌面版：Windows、macOS、Linux

閱讀順序 11；估計閱讀 15 分鐘、操作 25 分鐘。永久 slug：`codex-desktop-getting-started`。

先備規劃：[ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37)

現有作者稿：[繁中](../deep/zh-TW/03.md) · [英文](../deep/en/03.md) · [日文](../deep/ja/03.md) · [韓文](../deep/ko/03.md) · [五語內容包（含簡中）](../../../apps/api/app/guides/content/codex-desktop-getting-started.json)。簡中由固定轉換流程產出，仍須獨立校對。

### 練習起點與逐步內容

**起點材料：** expected 副本及可使用的桌面入口。

**操作順序：** 按 OS 安裝與登入；開練習資料夾；先確認位置，再完成一次小畫面修改與 diff 檢查。

**預計交付：** 各 OS 完整起步流程及一次可驗收修改。

### 成功、失敗與恢復

**成功判準：** 任務指向正確五個檔案，修改可預覽，原有測試與功能仍正常。

**指定失敗／邊界案例：** 開到 ZIP 或父目錄；選到其他環境；誤把下載完成當安裝完成。

**恢復或停止：** 回到正確練習副本；停止不需要的任務並回復本次指定檔案。

### 圖片與延伸

**需補或核對的圖文：** 桌面入口、選資料夾、差異／成果畫面；各平台實測分開標記。 必須記錄來源、環境、日期及五語替代文字／圖說；圖解不能代替產品實際操作證據。無法操作的平台依官方文件查證並標明未實測。

相關規劃：[ID 04｜手機使用：iPhone 與 Android](unit-c.md#lesson-04)、[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)、[ID 13｜桌面版任務與專案管理](unit-f.md#lesson-13)

驗收時對照[本篇官方來源清單](../deep/sources.json)中的 ID 03 與作者稿來源段落；核對文字支持的操作及版本，網址回應正常不等同內容正確。

[返回深入製作總目錄](README.md) · 上一篇：[ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37) · 下一篇：[ID 14｜IDE 擴充套件入門](unit-b.md#lesson-14)

<a id="lesson-14"></a>

## ID 14｜IDE 擴充套件入門

閱讀順序 12；估計閱讀 12 分鐘、操作 30 分鐘。永久 slug：`codex-ide-getting-started`。

先備規劃：[ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)

現有作者稿：[繁中](../deep/zh-TW/14.md) · [英文](../deep/en/14.md) · [日文](../deep/ja/14.md) · [韓文](../deep/ko/14.md) · [五語內容包（含簡中）](../../../apps/api/app/guides/content/codex-ide-getting-started.json)。簡中由固定轉換流程產出，仍須獨立校對。

### 練習起點與逐步內容

**起點材料：** 官方支援編輯器中的 expected 副本。

**操作順序：** 確認擴充套件來源；登入並選專案；帶入檔案或選取範圍；檢查產生的修改。

**預計交付：** IDE 上下文、差異與執行驗證紀錄。

### 成功、失敗與恢復

**成功判準：** 上下文指向實際選取檔案，修改範圍清楚，終端機測試與預覽一致。

**指定失敗／邊界案例：** 擴充套件裝在不同遠端環境；選取內容沒有附帶；編輯器與 CLI 路徑不同。

**恢復或停止：** 重選上下文或工作環境；只撤回本次差異。

### 圖片與延伸

**需補或核對的圖文：** 檔案／選取範圍如何加入任務的實際入口畫面。 必須記錄來源、環境、日期及五語替代文字／圖說；圖解不能代替產品實際操作證據。無法操作的平台依官方文件查證並標明未實測。

相關規劃：[ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05)、[ID 19｜Git、分支、diff 與還原](unit-f.md#lesson-19)、[ID 21｜測試、Code Review 與 PR](unit-f.md#lesson-21)

驗收時對照[本篇官方來源清單](../deep/sources.json)中的 ID 14 與作者稿來源段落；核對文字支持的操作及版本，網址回應正常不等同內容正確。

[返回深入製作總目錄](README.md) · 上一篇：[ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)
