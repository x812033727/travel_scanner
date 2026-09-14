# Codex 深入製作與驗收總目錄

更新：2026-09-14。這是作者與編輯使用的規劃入口，將既有 **60 篇、十單元** 拆成可執行的補強規格。沿用與 Claude Code 系列對齊的深度，保留 Codex 五語、平台差異、截圖及既有網址；不新增重複篇章。

**目前 60 篇五語草稿已編譯，最終深入驗收為 0/60。** 下列正常／失敗案例、圖文及交付物都是逐篇應核對的要求，不表示本輪已重新操作、完成五語終審或發布。精確現況見[製作進度](../progress.md)。

五篇代表稿已依此規格完成一輪定向補強；新增內容與教材驗證見[代表稿審核紀錄](../evidence/representative-depth-review.json)。全篇五語終審、產品操作證據與最終頁面仍待完成，不能先勾選整篇通過。

[系列維護首頁](../README.md) · [完整課程及穩定 ID](../depth-plan.md) · [作者模板](../article-template.md) · [驗收表與六次檢查](review-checklist.md)

本輪已接續 A 單元六篇及 B 單元五篇，見 [A 審核紀錄](../evidence/unit-a-depth-review.json)與 [B 審核紀錄](../evidence/unit-b-depth-review.json)。累計 16 篇完成定向補強，並非最終驗收通過；其餘 44 篇的規格仍列於下方，下一個補強單元為 C。

## 怎麼找

- 零基礎從 A → B → D 開始；需要手機操作接 C。
- 日常使用從 E → F；可重用流程接 G；工具與分工接 H。
- 自動化與 CI 看 I；網站、資料整理與維護看 J。
- 下表的 ID 永久不變，閱讀次序另列。搜尋 `AGENTS.md`、`config.toml`、`/plan`、`codex exec` 可透過此頁的功能索引定位。

| 單元 | 本次深化目的 | 六篇規格 |
| --- | --- | --- |
| A 基本概念 | 先建立正確的工作位置與驗收觀念，讓新手能選入口、找到檔案並提出第一個可驗證需求。 | [開啟單元](unit-a.md) |
| B 安裝與電腦 | 完成安裝、登入、定位專案與第一次修改，分開確認每個階段。 | [開啟單元](unit-b.md) |
| C 手機與跨裝置 | 能指出工作在哪台主機、哪份檔案和哪個版本執行，並完成一次可追蹤交接。 | [開啟單元](unit-c.md) |
| D MD 與設定 | 分清文件語法、代理規則、參考資料與應用程式設定，能驗證一次變更並還原。 | [開啟單元](unit-d.md) |
| E 指令與工作階段 | 知道文字應輸入哪個介面，能續接工作、整理上下文並選擇合適的執行條件。 | [開啟單元](unit-e.md) |
| F 日常開發 | 用同一個小專案完成閱讀、功能、除錯、Git 與審查，留下可交接證據。 | [開啟單元](unit-f.md) |
| G Skills 與 Plugins | 把可重複流程整理成技能，能驗證資源、輸入、帳號連接與實際工具結果。 | [開啟單元](unit-g.md) |
| H 工具與平行工作 | 完成工具連線診斷、工作目錄隔離、證據導向的分工與整合。 | [開啟單元](unit-h.md) |
| I 自動化與輸出 | 讓視覺修改、排程與非互動工作都有可判斷的結果、錯誤與停止方式。 | [開啟單元](unit-i.md) |
| J 實戰與維護 | 從完整需求交付網站與 CSV 工具，再能維護、保護資料、評估用量與自行排錯。 | [開啟單元](unit-j.md) |

## 按功能快速跳轉

| 需求 | 規格入口 |
| --- | --- |
| 三種系統安裝 | [ID 35｜Windows CLI 安裝與排錯](unit-b.md#lesson-35)、[ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36)、[ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37)、[ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03) |
| 手機與 Remote | [ID 38｜iPhone／iPad：接續 Codex 工作](unit-c.md#lesson-38)、[ID 39｜Android：接續 Codex 工作](unit-c.md#lesson-39)、[ID 40｜Remote 設定、排錯與解除連接](unit-c.md#lesson-40)、[ID 41｜跨裝置交接：核對檔案與環境](unit-c.md#lesson-41) |
| MD、AGENTS.md 與設定 | [ID 09｜Markdown 與 MD 檔入門](unit-d.md#lesson-09)、[ID 10｜AGENTS.md 專案規則](unit-d.md#lesson-10)、[ID 42｜AGENTS.md 層級與覆寫驗證](unit-d.md#lesson-42)、[ID 16｜config.toml 設定教學](unit-d.md#lesson-16)、[ID 44｜設定優先順序與故障排除](unit-d.md#lesson-44) |
| /plan、續接與交接 | [ID 11｜CLI 命令與斜線指令](unit-e.md#lesson-11)、[ID 08｜Plan 模式：先規劃再實作](unit-e.md#lesson-08)、[ID 45｜工作階段、接續與分岔](unit-e.md#lesson-45)、[ID 22｜上下文與工作交接](unit-e.md#lesson-22) |
| Git、Bug 與 PR | [ID 19｜Git、分支、diff 與還原](unit-f.md#lesson-19)、[ID 20｜修 Bug 的完整流程](unit-f.md#lesson-20)、[ID 21｜測試、Code Review 與 PR](unit-f.md#lesson-21) |
| SKILL.md、插件與 MCP | [ID 23｜Skills 與 SKILL.md](unit-g.md#lesson-23)、[ID 48｜Skill 的腳本、參考文件與材料](unit-g.md#lesson-48)、[ID 49｜Skill 觸發與結果測試](unit-g.md#lesson-49)、[ID 24｜Plugins 與外部服務](unit-g.md#lesson-24)、[ID 25｜MCP 設定與連線排除](unit-h.md#lesson-25)、[ID 52｜MCP 連線診斷與故障復原](unit-h.md#lesson-52) |
| worktree、子代理與整合 | [ID 27｜Worktree 與多任務隔離](unit-h.md#lesson-27)、[ID 28｜子代理與工作分工](unit-h.md#lesson-28)、[ID 53｜子代理分工與品質檢查](unit-h.md#lesson-53)、[ID 54｜平行工作後的整合與驗收](unit-h.md#lesson-54) |
| 排程、codex exec、JSONL 與 CI | [ID 29｜排程、自動化與提醒](unit-i.md#lesson-29)、[ID 30｜codex exec 與腳本整合](unit-i.md#lesson-30)、[ID 55｜JSON 輸出與結果驗證](unit-i.md#lesson-55)、[ID 56｜把 Codex 接入 CI 工作流程](unit-i.md#lesson-56)、[ID 57｜自動化失敗、重試與停止](unit-i.md#lesson-57) |
| 完整實戰 | [ID 31｜實戰：製作小網站](unit-j.md#lesson-31)、[ID 32｜實戰：製作資料整理工具](unit-j.md#lesson-32)、[ID 58｜實戰：維護既有專案](unit-j.md#lesson-58) |

## 60 篇逐篇入口

每篇已列：材料、操作順序、交付物、正常判準、指定失敗、還原、圖片需求、先備與相關篇，並連到現有四語作者檔及含簡中的內容包。這些是本機規劃連結；網站公開連結仍由各語言發布資料控制。

### A｜基本概念

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 01 | [ID 01｜Codex 是什麼？與 ChatGPT 的差別](unit-a.md#lesson-01) | 入口選擇表與一張環境關係圖。 |
| 02 | [ID 02｜帳號、登入、方案與額度](unit-a.md#lesson-02) | 遮蔽帳號的狀態判讀表。 |
| 03 | [ID 33｜平台選擇：找到適合的 Codex 入口](unit-a.md#lesson-33) | 個人起步路線與平台選擇表。 |
| 04 | [ID 34｜終端機與路徑：找到專案根目錄](unit-a.md#lesson-34) | 路徑對照表與成功／失敗命令紀錄。 |
| 05 | [ID 06｜完成第一個小專案](unit-a.md#lesson-06) | 需求、變更差異、測試結果與畫面。 |
| 06 | [ID 07｜如何把需求說清楚](unit-a.md#lesson-07) | 模糊與完整提示詞對照，以及驗收清單。 |

[閱讀本單元完整規格](unit-a.md) · [返回單元索引](#怎麼找)

### B｜安裝與電腦

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 07 | [ID 05｜Codex CLI 安裝與入門](unit-b.md#lesson-05) | 第一次 CLI 工作的完整輸入與檔案差異。 |
| 08 | [ID 35｜Windows CLI 安裝與排錯](unit-b.md#lesson-35) | Windows 安裝、來源與讀檔診斷紀錄。 |
| 09 | [ID 36｜macOS CLI 安裝與排錯](unit-b.md#lesson-36) | macOS 指令與安裝來源檢查表。 |
| 10 | [ID 37｜Linux／WSL CLI 與檔案位置](unit-b.md#lesson-37) | 主機／WSL 對照與 Linux 操作紀錄。 |
| 11 | [ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03) | 各 OS 完整起步流程及一次可驗收修改。 |
| 12 | [ID 14｜IDE 擴充套件入門](unit-b.md#lesson-14) | IDE 上下文、差異與執行驗證紀錄。 |

[閱讀本單元完整規格](unit-b.md) · [返回單元索引](#怎麼找)

### C｜手機與跨裝置

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 13 | [ID 04｜手機使用：iPhone 與 Android](unit-c.md#lesson-04) | 手機操作與實際工作位置的對照表。 |
| 14 | [ID 38｜iPhone／iPad：接續 Codex 工作](unit-c.md#lesson-38) | iOS 操作紀錄與一個離線判讀案例。 |
| 15 | [ID 39｜Android：接續 Codex 工作](unit-c.md#lesson-39) | Android 連接流程與廠牌差異說明。 |
| 16 | [ID 40｜Remote 設定、排錯與解除連接](unit-c.md#lesson-40) | Remote 設定與三類故障診斷表。 |
| 17 | [ID 15｜雲端任務與 GitHub](unit-c.md#lesson-15) | 雲端版本、環境、差異與 PR 檢查表。 |
| 18 | [ID 41｜跨裝置交接：核對檔案與環境](unit-c.md#lesson-41) | 跨裝置交接卡與版本不一致案例。 |

[閱讀本單元完整規格](unit-c.md) · [返回單元索引](#怎麼找)

### D｜MD 與設定

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 19 | [ID 09｜Markdown 與 MD 檔入門](unit-d.md#lesson-09) | 包含完整語法範例的 README.md。 |
| 20 | [ID 10｜AGENTS.md 專案規則](unit-d.md#lesson-10) | 可重用 AGENTS.md 與遵守／未遵守的驗證紀錄。 |
| 21 | [ID 42｜AGENTS.md 層級與覆寫驗證](unit-d.md#lesson-42) | 根／子目錄／override 的實驗對照表。 |
| 22 | [ID 43｜規則、說明與上下文文件怎麼分](unit-d.md#lesson-43) | AGENTS.md、README、設計與交接的分工圖。 |
| 23 | [ID 16｜config.toml 設定教學](unit-d.md#lesson-16) | config.toml 修改前後與來源判讀紀錄。 |
| 24 | [ID 44｜設定優先順序與故障排除](unit-d.md#lesson-44) | TOML 排錯流程圖與三個案例。 |

[閱讀本單元完整規格](unit-d.md) · [返回單元索引](#怎麼找)

### E｜指令與工作階段

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 25 | [ID 11｜CLI 命令與斜線指令](unit-e.md#lesson-11) | 可搜尋的命令索引與五種輸入方式例題。 |
| 26 | [ID 45｜工作階段、接續與分岔](unit-e.md#lesson-45) | 工作階段選擇與恢復上下文的紀錄。 |
| 27 | [ID 22｜上下文與工作交接](unit-e.md#lesson-22) | 可供另一個人接手的 handoff.md。 |
| 28 | [ID 17｜模型、推理深度與速度](unit-e.md#lesson-17) | 設定比較表與選擇理由。 |
| 29 | [ID 08｜Plan 模式：先規劃再實作](unit-e.md#lesson-08) | 初版／修訂版計畫與實作驗收條件。 |
| 30 | [ID 18｜權限、沙盒、網路與金鑰](unit-e.md#lesson-18) | 權限範圍表與一個授權失敗案例。 |

[閱讀本單元完整規格](unit-e.md) · [返回單元索引](#怎麼找)

### F｜日常開發

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 31 | [ID 13｜桌面版任務與專案管理](unit-f.md#lesson-13) | 任務命名規則與三項工作的狀態表。 |
| 32 | [ID 46｜先讀懂一個既有專案](unit-f.md#lesson-46) | 附檔案與函式依據的專案導覽。 |
| 33 | [ID 47｜實作功能：完成待辦篩選](unit-f.md#lesson-47) | 篩選功能、邊界測試與前後畫面。 |
| 34 | [ID 20｜修 Bug 的完整流程](unit-f.md#lesson-20) | Bug 報告、最小差異與回歸紀錄。 |
| 35 | [ID 19｜Git、分支、diff 與還原](unit-f.md#lesson-19) | Git 三種狀態圖與指定變更的處理紀錄。 |
| 36 | [ID 21｜測試、Code Review 與 PR](unit-f.md#lesson-21) | Review 清單與可交付 PR 描述。 |

[閱讀本單元完整規格](unit-f.md) · [返回單元索引](#怎麼找)

### G｜Skills 與 Plugins

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 37 | [ID 23｜Skills 與 SKILL.md](unit-g.md#lesson-23) | 完整 SKILL.md 與正常／失敗呼叫紀錄。 |
| 38 | [ID 48｜Skill 的腳本、參考文件與材料](unit-g.md#lesson-48) | 可重用的技能資料夾與帶證據的報告。 |
| 39 | [ID 49｜Skill 觸發與結果測試](unit-g.md#lesson-49) | 技能測試矩陣與修正紀錄。 |
| 40 | [ID 24｜Plugins 與外部服務](unit-g.md#lesson-24) | 插件連接與撤銷的四階段紀錄。 |
| 41 | [ID 50｜Plugin 連線與工具不可用排錯](unit-g.md#lesson-50) | 插件故障診斷表與恢復案例。 |
| 42 | [ID 51｜提示詞、規則與交接範本索引](unit-g.md#lesson-51) | 附適用條件與最小範例的範本索引。 |

[閱讀本單元完整規格](unit-g.md) · [返回單元索引](#怎麼找)

### H｜工具與平行工作

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 43 | [ID 25｜MCP 設定與連線排除](unit-h.md#lesson-25) | MCP 設定、探索、請求與回覆紀錄。 |
| 44 | [ID 52｜MCP 連線診斷與故障復原](unit-h.md#lesson-52) | MCP 診斷決策樹與對應訊息。 |
| 45 | [ID 27｜Worktree 與多任務隔離](unit-h.md#lesson-27) | 工作目錄歸屬表與隔離實驗紀錄。 |
| 46 | [ID 28｜子代理與工作分工](unit-h.md#lesson-28) | 分工說明、兩份回報與整合結論。 |
| 47 | [ID 53｜子代理分工與品質檢查](unit-h.md#lesson-53) | 主張、來源、實測與判定四欄矩陣。 |
| 48 | [ID 54｜平行工作後的整合與驗收](unit-h.md#lesson-54) | 整合差異、測試結果與衝突處理紀錄。 |

[閱讀本單元完整規格](unit-h.md) · [返回單元索引](#怎麼找)

### I｜自動化與輸出

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 49 | [ID 26｜瀏覽器、截圖與圖片協作](unit-i.md#lesson-26) | 視覺修改說明、前後圖片與文字量測。 |
| 50 | [ID 29｜排程、自動化與提醒](unit-i.md#lesson-29) | 排程設定、試跑、修改與停止紀錄。 |
| 51 | [ID 30｜codex exec 與腳本整合](unit-i.md#lesson-30) | 非互動任務的輸出、錯誤與狀態檔。 |
| 52 | [ID 55｜JSON 輸出與結果驗證](unit-i.md#lesson-55) | 可重現驗證器與三份故意破壞的輸出副本。 |
| 53 | [ID 56｜把 Codex 接入 CI 工作流程](unit-i.md#lesson-56) | CI 工作流程、驗證器與執行證據清單。 |
| 54 | [ID 57｜自動化失敗、重試與停止](unit-i.md#lesson-57) | 失敗分類、恢復決策與重試紀錄。 |

[閱讀本單元完整規格](unit-i.md) · [返回單元索引](#怎麼找)

### J｜實戰與維護

| 順序 | 教學規格 | 具體交付物 |
| --- | --- | --- |
| 55 | [ID 31｜實戰：製作小網站](unit-j.md#lesson-31) | 五份網站原始檔、需求、測試與操作說明。 |
| 56 | [ID 32｜實戰：製作資料整理工具](unit-j.md#lesson-32) | CSV 程式、測試、輸入輸出及防覆寫紀錄。 |
| 57 | [ID 58｜實戰：維護既有專案](unit-j.md#lesson-58) | 最小重構差異、新舊測試與交接說明。 |
| 58 | [ID 59｜專案資料、金鑰與練習隔離](unit-j.md#lesson-59) | 資料界線表、合格摘要與公開前核對表。 |
| 59 | [ID 60｜用量與效率：減少重工](unit-j.md#lesson-60) | 兩種提示詞的比較紀錄與減少重工的下一步。 |
| 60 | [ID 12｜新手問題排除](unit-j.md#lesson-12) | 可搜尋的症狀總表、診斷筆記與修復案例。 |

[閱讀本單元完整規格](unit-j.md) · [返回單元索引](#怎麼找)

## 接下來的製作順序

1. 先對照 [ID 03｜桌面版：Windows、macOS、Linux](unit-b.md#lesson-03)、[ID 10｜AGENTS.md 專案規則](unit-d.md#lesson-10)、[ID 04｜手機使用：iPhone 與 Android](unit-c.md#lesson-04)、[ID 11｜CLI 命令與斜線指令](unit-e.md#lesson-11)、[ID 23｜Skills 與 SKILL.md](unit-g.md#lesson-23) 五篇代表稿，補齊逐步細節、五語對照與適用環境證據；建立可沿用的審核樣本。
2. 依閱讀順序分六組、每組十篇補強與審核；原三大批每批二十篇不變。具體 ID 見[批次表](review-checklist.md#批次與完成條件)。
3. 整套補上最終頁面與產品介面證據；五語內容、圖片、連結、複製與手機版面全部驗收後，才開 PR、合併、匯入、發布及部署。

可以先做作者稿差異、翻譯、來源與練習資料核對；受阻的預覽與實機項目保留待驗收，不以文件完成替代。這份規劃未改動文章發布狀態。
