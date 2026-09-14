# Codex 深入教學製作進度

更新：2026-09-14。有效規格為[總目錄＋60 篇、五語](depth-plan.md)。目前是本機製作與驗證，尚未執行 PR、合併、匯入、正式發布或部署。

依使用者「全部完成後再開 PR 部署」指示，先完成全套內容、共用功能與驗收，再進入 PR 和發布流程。不提前開部分內容 PR。

## 最新數量

**37 篇五語深化草稿、10 篇短篇待深化、13 篇待撰寫；正式深入驗收 0/60。** 現有 48 個內容包、240 份語言文件（含目錄）；目標 61 個內容包、305 份語言文件。深化稿與正式驗收是不同狀態。

閱讀順序 01–37 的作者稿已編譯齊全，另有 Skills 代表稿。32 篇採四語平行作者模組，5 篇代表稿採原始 Markdown；簡中轉換保留程式碼原文。原有 32 篇網址保留，13 篇待寫項目沒有空白內容包。所有新內容維持草稿；ready 只表示材料存在，導覽仍檢查 API 的當前語言發布清單。

## 已編入的深入稿

| 閱讀順序 | 永久 ID | 主題及材料 |
| --- | --- | --- |
| 01–06 | 01、02、33、34、06、07 | 基本概念、帳號、平台選擇、終端機路徑、第一個網站、提示詞 |
| 07–10 | 05、35、36、37 | CLI 總覽及 Windows、macOS、Linux／WSL；標記、備份、讀取與還原 |
| 11–12 | 03、14 | 桌面及 IDE；待辦故障副本、帶入上下文、精確修正與測試 |
| 13–16 | 04、38、39、40 | 手機總覽、iPhone、Android、Remote 主機設定與版本標記 |
| 17–18 | 15、41 | 雲端環境、GitHub PR 準備；交接紀錄、舊內容辨識與 Handoff |
| 19–20 | 09、10 | 互連 Markdown、巢狀程式碼；AGENTS.md 專案規則 |
| 21–24 | 42、43、16、44 | 規則層級、文件分工、config.toml、四種設定故障與修正 |
| 25、37 | 11、23 | 指令分類、完整 SKILL.md 與技能驗收材料 |
| 26–30 | 45、22、17、08、18 | 續接、過期交接驗證、模型比較、Plan 篩選練習、權限 |
| 31–33 | 13、46、47 | 任務整理、程式地圖、六項功能驗收與同名任務畫面 |
| 34–36 | 20、19、21 | 最小 Bug 重現、Git 保留與撤回、Review 的測試缺口及 PR 草稿 |

作者稿在 [deep/zh-TW](deep/zh-TW)、[deep/en](deep/en)、[deep/ja](deep/ja)、[deep/ko](deep/ko)；來源在 [sources.json](deep/sources.json)。繁中編譯正文約 1,818–3,007 字；手機代表稿因必要平台與解除流程略超 3,000 字，保留內容。日韓稿保有相同操作、限制、程式碼及驗收步驟。

## 本輪可重現證據

| 檢查 | 已確認結果 | 範圍與證據 |
| --- | --- | --- |
| CLI 批次整頁 | 240 項通過 | [15 篇＋目錄](evidence/depth-browser-cli-batch.json)，五語 × 360／390／1280px |
| IDE／手機／Markdown 整頁 | 90 項通過 | [5 篇＋目錄](evidence/depth-browser-platform-batch.json)，五語與三寬度；後續小幅校字另經編譯驗證 |
| 雲端／跨裝置整頁 | 60 項通過 | [15、41、更新的 40 篇＋目錄](evidence/depth-browser-cloud-batch.json)，五語及三寬度 |
| 網址篩選返回 | 12 回合通過 | [history-browser.json](evidence/history-browser.json)，4 倍 CPU 減速檢查 Next 路由歷史 |
| Windows 終端機 | 4 項通過 | [terminal-basics.json](evidence/terminal-basics.json)，真實 PowerShell 路徑操作 |
| Windows CLI 材料 | 7 項通過 | [cli-basics.json](evidence/cli-basics.json)，原檔保留、重複建立拒絕、標記讀取與還原；CLI 僅 version／help |
| Markdown 材料 | 4 項通過 | [markdown-practice.json](evidence/markdown-practice.json)，雙向實檔、缺檔、缺結尾負面案例；非 VS Code UI 或模型執行 |
| 網站指定修改 | 6 項通過 | [basics-browser.json](evidence/basics-browser.json)，實際開啟明確套用的參考修改 |
| 範例網站操作 | 通過 | [practice-browser.json](evidence/practice-browser.json)，操作、焦點及儲存錯誤；expected 核心 3 項通過，空清單三種篩選另已核對 |
| 刻意故障材料 | 符合預期 | start／broken 各 2 通過、1 預期失敗，保留為故障練習 |
| 規則實際載入 | 5 項通過 | [rule-discovery.json](evidence/rule-discovery.json)，CLI 實際輸入診斷；沒有模型請求或遵從聲稱 |
| 文件／設定材料 | 12 項通過 | [docs-config-practice.json](evidence/docs-config-practice.json)，原始程式不變、正常／錯誤／修正樣本 |
| 規則與文件整頁 | 45 項通過 | [rules batch](evidence/depth-browser-rules-batch.json)，42 篇之後另修正實測差異並重驗 |
| 設定與載入整頁 | 60 項通過 | [config batch](evidence/depth-browser-config-batch.json)，16、44、更新後 42 篇及目錄，含正文一致性與包雜湊 |
| 工作階段與 Plan 材料 | 16 項通過 | [session-plan-practice.json](evidence/session-plan-practice.json)，精確範例、故障／修正／還原及唯讀比較；無模型呼叫 |
| 工作階段批次整頁 | 90 項通過 | [session batch](evidence/depth-browser-session-batch.json)，45、22、17、08、18 與目錄，五語／三寬度；08 後續增加 HTTP 說明並於下一批重驗 |
| 專案管理與閱讀整頁 | 60 項通過 | [project batch](evidence/depth-browser-project-batch.json)，13、46、更新 08 與目錄，五語／三寬度 |
| 功能參考畫面 | 6 項通過 | [feature-browser.json](evidence/feature-browser.json)，精確 start 單函式修正；三寬度同名 ID、順序、取消完成、保存及空清單 |
| Git 與 Review 材料 | 9 項通過 | [git-practice.json](evidence/git-practice.json)，獨立 Git 庫、精確指令、CSS 保留、revert；Review 前 3 過、新增 2 敗、修復 5 過 |
| 功能篇整頁 | 30 項通過 | [feature batch](evidence/depth-browser-feature-batch.json)，47 篇和目錄，五語／三寬度，含真實參考圖片 |
| Bug／Git／Review 整頁 | 60 項通過 | [review batch](evidence/depth-browser-review-batch.json)，20、19、21 篇與目錄，五語／三寬度，含正文及程式碼一致性 |
| 作者編譯器 | 7 項通過 | test_compiler.py：精確程式碼、巢狀 fence、失敗不部分覆寫、過期內容 check 拒絕 |
| API 與文章包 | 9 項通過 | test_codex_learning.py：五語結構、來源、圖片、連結、先備與程式碼一致 |
| 內容稽核 | 0 錯誤、63 警告 | [content-audit.json](evidence/content-audit.json)，保留短稿與長文等編輯問題 |
| 路由修正前端 | 11 項通過 | 獨立 Codex 元件兩個測試檔；ESLint、TypeScript、i18n 通過 |
| 正式建置 | 通過 | 篩選路由修正後 build 成功、293 靜態頁；最終整合後仍須重新建置 |

編譯器先解析全批並用真實 API schema 驗證，再寫入內容包；來源與內容包 SHA-256 核對後才計入深化稿。這確認編譯完整性，不能取代編輯審核。

瀏覽器使用 localhost 假發布 API，沒有資料庫寫入。檢查全部渲染程式碼、首個複製按鈕、五語網址、上下目錄連結與水平溢出；Windows 剪貼簿只正規化 CRLF。已目視檢查 [390px Markdown](evidence/deep-codex-markdown-basics-390.png) 與 [1280px IDE 教學](evidence/deep-codex-ide-getting-started-1280.png)。它們是文章頁，沒有冒充 Codex 或 VS Code 介面。

## 仍需完成的驗收

CLI 0.154.0-alpha.6.2 的真實診斷發現：空 ui/AGENTS.override.md 沒有回退載入同層 AGENTS.md；改名後恢復。42 篇已記錄此版本差異和五種載入結果，原始私人輸入完全未保存。

五篇代表稿已具完整材料，但產品操作與編輯審核尚未全部完成：桌面平台安裝和介面、實體手機配對與停用、AGENTS.md 新工作階段載入、CLI 互動斜線操作、Skills 選擇與觸發。可取得的平台繼續補證據；無法實測的環境依核准規格標示「依官方文件查證」，不以其他平台畫面替代。

原創 SVG 為流程示意圖，實作成果截圖來自 Windows／Edge 153.0.4234.32、2026-09-14、虛構資料。390px 是響應式視窗，不能稱為實體手機實測。參考修改、模型操作、雲端執行、發布和部署分開記錄。

## 與 Claude Code 系列的整合

已對齊批准的 60 篇／十單元、同等深度、共用 Small Steps 主線及每十篇檢查點。本輪唯讀確認「規劃 Claude Code 教學目錄」已完成並結案：其工作目錄記錄 PR #485 已合併，合併提交 35a2d258b51d2a1ac9aff91dc5f7ed5a8df823ec。共用文章、API schema、系列 API 與後台編輯器已可供整合。本輪未修改對方工作目錄或傳送任務訊息；此處尚未合併主分支，不把他方完成當成本系列已整合。

仍待接入：inlines／article reference、code label 與語言清單、系列 API、集合頁 SEO、桌面側欄和手機章節目錄，以及閱讀／操作時間呈現。現有 Codex spans 與對方格式差異已列在[整合契約](depth-plan.md)，整合時保留舊文章相容性。

## 接續工作

1. 已保存雲端／跨裝置批次 60 項整頁通過報告，繼續下一單元。
2. 20、19、21 內容與參考材料完成；整頁檢查後先保存本機 checkpoint 並整合 #485 共用系統，再從 48、49 技能材料與驗收繼續剩餘 23 篇。
3. 補代表稿驗收及可取得的產品操作證據；整合共用功能並檢查五語內容和路線。
4. 全部完成後才開 PR、核對 CI 與合併，再匯入、發布、部署及檢查公開網址。

初版 32 篇短稿的 485 項前端等歷史通過數保留於 [README](README.md)，不作為新內容驗收。任務與重建入口見 README 及 tasks/open/2026-09-14-codex-depth-content.md。

整合範圍已合併至主任務 2026-09-14-codex-learning-series，由 codex-integration-fc2e 認領；深度內容子任務已 release。CLAUDE 共用提交已可接入，尚未合併進此目錄。
