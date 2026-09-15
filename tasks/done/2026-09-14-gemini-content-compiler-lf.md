---
id: 2026-09-14-gemini-content-compiler-lf
title: Gemini content compiler preserves LF across platforms
status: done
priority: P1
area: tools
owner: codex-gemini-compiler-lf
claimed_at: 2026-09-14T12:04:38Z
created_at: 2026-09-14T12:04:36Z
completed_at: 2026-09-14T12:06:12Z
branch: codex/gemini-advanced-platform
depends_on: []
scope:
  - docs/gemini-series/build.py
  - docs/gemini-series/advanced/platform/test_build.py
---

# Gemini content compiler preserves LF across platforms

## Why

Windows 的 Path.write_text 預設輸出 CRLF，但 repository 的 .gitattributes 將文字保存與簽出為 LF。內容包、SVG 與驗收收據因此會在 Git 正規化後改變雜湊，練習 ZIP 若包入 CRLF 來源，亦可能與新 checkout 的 LF 原稿不同。編譯器應在所有平台直接產生 repository 的換行格式。

## Definition of done

- [x] 原系列與深入系列的 JSON、SVG、目錄及建置收據明確產生 LF，Windows 不再產生 CRLF。
- [x] 實際編譯器回歸案例用 CRLF 原稿圖檔，核對內容包、SVG 與報告的輸出位元組沒有 CR。
- [x] 原第 36 篇重建內容不變；九項實際編譯器測試通過。

## Steps

- [x] 所有文字 write_text 使用 newline="\n"，不更動輸入解析與文章語意。
- [x] 新增跨平台換行回歸案例，執行 Python 測試與 Ruff；本次 MD 草稿重新建置。

## How to verify

apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/platform/test_build.py（9 passed）

apps/api/.venv/Scripts/ruff.exe check docs/gemini-series/build.py docs/gemini-series/advanced/platform/test_build.py

node tools/gemini-series.mjs check --draft --track md；node tools/gemini-series.mjs check（6 篇草稿及原 51 頁）

## Notes

2026-09-14，在 Windows 真正重現 CRLF 輸出後修正。MD 練習與配圖產生器、ZIP 重建與驗收快照由各自已認領的 2026-09-14-gemini-advanced-md 票處理，未跨共享 scope。本票不發布文章、不改現有 runtime catalogue，沒有改全域 Git 設定來繞過差異。
