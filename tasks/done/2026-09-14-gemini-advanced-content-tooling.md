---
id: 2026-09-14-gemini-advanced-content-tooling
title: Gemini 深入系列：獨立內容建置與凍結發布清單工具
status: done
priority: P1
area: tools
owner: codex-gemini-platform
claimed_at: 2026-09-14T11:19:47Z
created_at: 2026-09-14T11:19:46Z
completed_at: 2026-09-14T11:37:35Z
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
scope:
  - tools/gemini-series.mjs
  - tools/gemini-series.test.mjs
  - docs/gemini-series/build.py
  - docs/gemini-series/render-art.mjs
  - docs/gemini-series/advanced/platform
---

# Gemini 深入系列：獨立內容建置與凍結發布清單工具

## Why

原 platform 任務與 Claude Code 教學任務共用元件 scope 重疊，無法認領。先拆出完全不重疊的內容工具，讓六批深入原稿可獨立建置與檢查，同時保持正式目錄 50 篇不變。

## Definition of done

- [x] 支援 51–86 固定篇序與六批限定建置，不改正式 catalogue。
- [x] 編譯完整原稿、跨篇／章節連結、TOML 等程式碼與下載素材，整批预檢後輸出。
- [x] 支援桌面與 360px 圖解渲染並標示尚待人工檢查。
- [x] 限定 36 篇加明列 02／49 更新篇及 hub 最後寫入，發布前凍結內容與下載雜湊。
- [x] 內容改動、乾跑失敗、公開內容不符或任何既有子篇不可讀時停止，不提前寫入目錄。
- [x] 舊 51 頁檢查、原第 36 篇重建與既有工具測試通過；附作者文件與驗證紀錄。

## Steps

- [x] 建立 frozen identity contract 與 editor-only draft projection。
- [x] 更新 compiler、renderer、check／freeze／dry-run／publish 工具。
- [x] 加入真實編譯器隔離測試及發布順序／檔案變動反例測試。
- [x] 用合成資料實際渲染桌面與手機預覽並檢視，沒有生成正式深入教學頁。

## How to verify

- `node --test tools/gemini-series.test.mjs`：17 passed。
- `npm run test:tools`：56 passed。
- `apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/platform/test_build.py`：8 passed。
- Ruff 對 build.py 與 test_build.py：passed。
- `node tools/gemini-series.mjs check`：原 51 頁通過。
- `npm run check:tasks`：425 票通過；只剩既有 stale／其他任務重疊警告。
- 實際渲染與限制：[verification.json](../../docs/gemini-series/advanced/platform/verification.json)。

## Notes

工具工作已完成於本地分支，尚未推送、合併、部署或公開新文章。正式 catalogue 維持 50 篇。原 `2026-09-14-gemini-advanced-platform` 仍 open，其共用 UI／伺服器開關不能在這張工具票標完成。內容作者可依新工具開始編寫；其他批次尚未完成時，完整跨篇檢查預期會報 missing pack，不能放占位文章跳過。

Windows 渲染需使用已安裝 Playwright headless shell 設定 CHROMIUM_BIN；renderer 用固定響應樣式避開停用 JavaScript 時 addStyleTag 等待。合成圖片只作工具 smoke 證据。
