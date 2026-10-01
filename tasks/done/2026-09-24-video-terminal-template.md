---
id: 2026-09-24-video-terminal-template
title: 影片產線 T10：模擬終端機版型
status: done
priority: P3
area: tools
owner: claude-opus-5-5-terminal-template
claimed_at: 2026-10-01T07:04:43Z
created_at: 2026-09-24T00:41:18Z
completed_at: 2026-10-01T07:29:06Z
branch: claude/video-terminal-template
depends_on:
  - 2026-09-24-video-pilot-ai-model-choice
scope:
  - tools/video/templates/terminal
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/templates/fixtures/showcase/video.json
  - tools/video/core/schema.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/automation/prompts.mjs
  - .agents/skills/youtube-video/references/automated.md
---

# 影片產線 T10：模擬終端機版型

## Why

Claude Code、Codex 這類終端機工具的教學需要「模擬終端機」版型：逐字打出指令、再顯示輸出。輸出必須來自真的執行（附日期與工具版本），查核代理才能核對，不能憑空寫。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [x] `terminal` 版型：提示字元不露使用者名稱與主機名、逐字打字動畫、輸出分段出現。
- [x] 輸出檔記錄執行日期與版本，lint 檢查有這兩欄。
- [x] 用一段 Claude Code 教學跑通。

## Steps

- [x] 版型與打字動畫（Web Animations 固定時間點截影格）。
- [x] 輸出記錄格式。

## How to verify

```bash
node --test tools/video/templates/terminal/*.test.mjs
VIDEO_BROWSER_CHANNEL=msedge node tools/video/cli.mjs render --file tools/video/templates/terminal/fixtures/claude-code/video.json --workdir <scratch>
```

## Notes

- 2026-10-01 claim 用了 `--force`：相依的 `2026-09-24-video-pilot-ai-model-choice` 還開著，只是因為站主還沒上傳試播片；它要驗證的產線之後已經做出十幾支影片。
- 資料格式（`tools/video/templates/terminal/terminal.mjs`）：`{ title?, prompt?: "$"|">", command, output: 1–6 段（一段可多行，每次 reveal 出現下一段）, ran_on: "YYYY-MM-DD", tool_version }`。`ran_on`（真的日期）與 `tool_version`（要有數字，例如 `2.1.285 (Claude Code)`）缺一就擋，lint 與 render 共用同一個 `TEMPLATE_SPECS.check`；兩者都畫在視窗下方「Ran on … · …」，觀眾也看得到輸出有多舊。
- 提示字元只能是 `$` 或 `>`，所以畫面上不會出現使用者或主機名；指令或輸出裡有家目錄（`/home/x`、`/Users/x`、`C:\Users\x`，`~`、`/Users/Shared` 可以）、`user@host:` 提示、email 也擋。
- 過長一律擋、不自動折行：指令一行 ≤78 欄、輸出每行 ≤80 欄（中日韓字算兩欄）、合計 ≤8 行、不能有 tab。用壓力測試確認過最壞的情況（兩行標題＋8 行 80 欄、兩行標題＋6 行 60 欄的大字）都在畫面下方 12% 以上、render 沒有版面問題。指令＋輸出 ≤6 行且每行 ≤60 欄時字放大成 40px（手機好讀），否則 30px。
- 動畫：第一個狀態每格（1/30 秒）打一個字（字元 span 的 font-size 從 0 跳到 1em，所以游標跟著走、中文也行）；指令長就壓進 renderer 的 18 格過場內。該狀態要顯示的輸出在最後一鍵的下一格出現；之後每個 reveal 一格一行印出下一段。游標停在指令後面，直到第一段輸出出現。
- CSS 放在 terminal 投影片自己的 `<style>`（跟縮圖的做法一樣），沒有改 `theme.css`，所以其他影片的畫格 key 都沒變；`templates.test.mjs` 有測。
- 為什麼動到 scope 目錄以外的檔案：`templates.mjs` 要註冊版型與 renderer、`schema.mjs` 的 `TEMPLATES` 要列入、`lint.mjs` 的 reveal 上限要算 `output`、showcase 要有每一種版型（`templates.test.mjs` 的規則）、`prompts.mjs` 的版型說明要告訴規劃代理「只能用真的執行結果、不能自己寫輸出」（showcase 會送給它）、`automated.md` 的版型清單。
- 跑通：2026-10-01 在本機執行 `claude --version`（輸出 `2.1.285 (Claude Code)`）與 `claude --help | head -n 4`，原樣放進 `tools/video/templates/terminal/fixtures/claude-code/video.json`（三章、兩個 terminal 場景、lint 0 錯 0 警告），用 msedge render 出 8 個狀態、看過聯絡表與打字中的畫格（第 7 格是 `claude ` 加游標）。渲染圖沒有 commit。
- 沒做：`docs/videos/README.md` 的版型表本來就只列 11 種、寫「15 種」，這次沒動（不在 scope）。
