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
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-platform
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

- [ ] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [ ] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [ ] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [ ] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [ ] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 69 `gemini-cli-memory-scope-lab`：GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則。成果：以最小專案觀察每份規則何時進入上下文。
- [ ] 70 `gemini-cli-modular-project-rules`：GEMINI.md 團隊範本：拆分規則、匯入與維護責任。成果：製作可維護的共用規則加前後端專案範本。
- [ ] 71 `gemini-cli-settings-debug-lab`：settings.json 設定除錯：來源優先順序與升級前後比較。成果：定位一項設定為何未生效，保存可重做的診斷程序。
- [ ] 72 `gemini-cli-custom-command-library`：自訂 CLI 指令庫：程式審查、測試計畫與文件同步。成果：建立三個可重用、可測試的 TOML 指令。
- [ ] 73 `gemini-cli-skill-extension-package`：把 SKILL.md 打包成 Extension：安裝、更新與回退。成果：將文件檢查技能打包成可安裝的本機擴充套件。
- [ ] 74 `gemini-cli-large-project-context`：大型專案的 CLI 上下文：分段任務、Git 差異與恢復。成果：在含多個模組的專案只修改指定範圍並保存恢復點。
- [ ] 在 docs/gemini-series/advanced/content/md/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [ ] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇目前只是規劃，沒有可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。
