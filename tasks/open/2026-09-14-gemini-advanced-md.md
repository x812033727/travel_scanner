---
id: 2026-09-14-gemini-advanced-md
title: Gemini 深入教學 69–74：MD 與 CLI 設定實驗
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:10:48Z
completed_at:
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-content-tooling
scope:
  - docs/gemini-series/advanced/content/md
  - apps/api/app/guides/content/gemini-cli-memory-scope-lab.json
  - apps/web/public/guides/gemini-cli-memory-scope-lab
  - apps/api/app/guides/content/gemini-cli-modular-project-rules.json
  - apps/web/public/guides/gemini-cli-modular-project-rules
  - apps/api/app/guides/content/gemini-cli-settings-debug-lab.json
  - apps/web/public/guides/gemini-cli-settings-debug-lab
  - apps/api/app/guides/content/gemini-cli-custom-command-library.json
  - apps/web/public/guides/gemini-cli-custom-command-library
  - apps/api/app/guides/content/gemini-cli-skill-extension-package.json
  - apps/web/public/guides/gemini-cli-skill-extension-package
  - apps/api/app/guides/content/gemini-cli-large-project-context.json
  - apps/web/public/guides/gemini-cli-large-project-context
---

# Gemini 深入教學 69–74：MD 與 CLI 設定實驗

## Why

將 [深入課綱](../../docs/gemini-series/advanced/README.md#catalogue) 的 69–74 篇製作為完整教學。單篇規格及先修由 curriculum.json 決定；這是新作品／故障實驗，不重寫第一階段入門篇。

## Definition of done

- [x] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [x] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [x] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [x] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [x] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。已保存本批審閱雜湊與圖檢紀錄，但原生終端、模型及恢復會話的驗收尚未完成，不可標為可發布。

## Steps

- [x] 69 `gemini-cli-memory-scope-lab`：GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則。成果：以最小專案觀察每份規則何時進入上下文。實際 CLI 載入模組五組觀察；不是雲端遵循率測試。
- [x] 70 `gemini-cli-modular-project-rules`：GEMINI.md 團隊範本：拆分規則、匯入與維護責任。成果：製作可維護的共用規則加前後端專案範本。正常引用、Node 測試與兩種故障案例已執行。
- [x] 71 `gemini-cli-settings-debug-lab`：settings.json 設定除錯：來源優先順序與升級前後比較。成果：定位一項設定為何未生效，保存可重做的診斷程序。八組 0.59.0 載入器實測；其他版本比較僅提供待填量測表，沒有捏造第二個版本。
- [ ] 72 `gemini-cli-custom-command-library`：自訂 CLI 指令庫：程式審查、測試計畫與文件同步。成果：建立三個可重用、可測試的 TOML 指令。
- [ ] 73 `gemini-cli-skill-extension-package`：把 SKILL.md 打包成 Extension：安裝、更新與回退。成果：將文件檢查技能打包成可安裝的本機擴充套件。
- [ ] 74 `gemini-cli-large-project-context`：大型專案的 CLI 上下文：分段任務、Git 差異與恢復。成果：在含多個模組的專案只修改指定範圍並保存恢復點。
- [x] 在 docs/gemini-series/advanced/content/md/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 content-tooling 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [x] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。本批沒有雲端請求。
- [x] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

2026-09-14：原 platform 已拆出完成的 content-tooling，具備本文所需建置／檢查／素材工具。認領前核對所有 active scope 零重疊，--force 僅跨過舊 UI 先修，未跨過別人的 scope；認領後將先修改為已完成工具票。共用 UI 仍待整合，本票不公開新文章。

六篇已由規劃完成為原稿及本機內容包，仍未發布。入口：[本批原稿目錄](../../docs/gemini-series/advanced/content/md/README.md)。正文 2,282–2,657 字；六組封面／圖解、七個 ZIP（六個單篇及一個綜合驗證包）齊備。SVG 為原創概念圖，程式範例附 MIT 授權。不要重建空白文章或把它們再次當成未撰寫題目。

### 已完成的實際驗證

- Windows、Node 24.19.0、Gemini CLI 0.59.0；上游 v0.59.0 tag 以 git ls-remote 核對為 fb0d535af931b27c51e87e5e6ade72905b1e8390。
- 48 筆實際模組／fixture 觀察（69:5、70:4、71:8、72:19、73:9、74:3），詳見 verification/local-cli.json。下載綜合 ZIP 解壓後重新執行，同樣通過。
- 69：記憶載入、JIT、去重、移除匯入後 reload 與不信任工作區。show 的常駐字串不含 JIT 新段落，已明確分欄。
- 70：規則引用正常、Node 測試、遺失引用與衝突命令反例。
- 71：八組真實 loadSettings 觀察。未知鍵保留不代表有效功能；型別錯誤警告也不代表原值已被修正。
- 72：三個 TOML 指令、十八組含中文／引號／shell 字元的參數展開，以及缺 prompt／不信任反例。輸出是提示詞，沒有冒充模型回答。
- 73：真實 SKILL 解析、三種腳本結束碼及 ExtensionManager 安裝／停用／啟用／更新／卸載／回退。
- 74：作者參考修正讓原本故障的測試轉為三項通過，使用者文件差異保留；不是 AI 修改證據。
- 十二張圖的 1600×900 與 360px 預覽逐張目視，文字無裁切；verification/visual-review.json 記錄素材雜湊。這是圖稿檢查，不是網站手機 E2E。
- 六篇 draft check、六篇 pack lint、原 51 頁 check 通過。相關 API 測試 31 passed／15 skipped；跳過項目需要隔離 PostgreSQL。Ruff、8 個 JS 語法、3 個 TOML、2 個 PowerShell 語法通過。JSON 唯一損壞檔為 71 的刻意故障輸入。
- verification/delivery.json 核對 ZIP CRC／成員內容／解壓執行；verification/authoring-review.json 另核對公開目錄副本與原稿相同，保存這次審閱快照。它不是 release 的 87 頁凍結清單。
- 提交前找到 Windows CRLF 與 Git LF 的位元組差異。已讓本批產生器直接輸出 LF、重建七個 ZIP 並重新解壓執行；共享 compiler 的相同修正由獨立 2026-09-14-gemini-content-compiler-lf 任務處理，九項 compiler 測試通過。快照雜湊以最終 LF 檔案重新計算。

### 接手後的未完成驗收

- [ ] 72：在可用且已授權的測試帳號執行三個指令，保存題目、環境、模型版本與實際回答，逐項比對格式／缺檔處理。
- [ ] 73：複驗 Windows 原生 gemini extensions 命令生命週期。Node 24.13.0 安裝、24.19.0 停用都曾先印成功再因 UV_HANDLE_CLOSING 斷言退出 3221226505，詳見 native-cli-limitations.json。模組通過不能關閉這項缺口；先核對狀態再重試。
- [ ] 73：使用已登入 CLI 實際觸發 doc-check 技能，保存腳本呼叫與三種結果；不能只看 metadata 即視為觸發成功。
- [ ] 74：已登入會話實際恢復／壓縮，加入新的使用者文件差異後確認會重新核對；保存 CLI 實際修正與測試記錄。
- [ ] 其他 CLI 版本、macOS／Linux 若要宣稱實測，需補真實紀錄；目前只標文件整理。71 的升級比較仍需第二個明確版本才能填結果。
- [ ] 共用 catalogue、前後篇、先修、搜尋、複製與發布開關整合後，補桌面／手機網站 E2E，以及需 PostgreSQL 的整合測試。
- [ ] 全部六批驗收完成後由 release 任務凍結、dry-run、逐篇發布再開目錄。本批未匯入資料庫、未公開、未修改目前 50 篇 runtime catalogue。

本票保留開放並交回隊列，完整原稿可接續驗收。共享範圍仍由 platform／release 任務管理；不要用本批本機通過數宣稱整套深入系列已完成。
