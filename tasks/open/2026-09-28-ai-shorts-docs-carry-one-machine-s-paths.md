---
id: 2026-09-28-ai-shorts-docs-carry-one-machine-s-paths
title: The AI Shorts documents carry one machine's paths
status: in-progress
priority: P3
area: docs
owner: claude-sonnet-ai-shorts-paths
claimed_at: 2026-09-30T15:41:50Z
created_at: 2026-09-28T04:26:00Z
completed_at:
branch: claude/ai-shorts-docs-paths
depends_on: []
scope:
  - docs/videos/ai-shorts/README.md
  - docs/videos/ai-shorts/campaign/README.md
  - docs/videos/ai-shorts/delivery-2026-09-28.md
  - docs/videos/ai-shorts/delivery-2026-09-28.json
---

# The AI Shorts documents carry one machine's paths

## Why

repo 是公開的。PR #871 的四份文件裡寫著這台開發機的絕對路徑（使用者資料夾底下的工作區）：

- `docs/videos/ai-shorts/README.md` 的指令範例（`--workdir`、`--dir`）。
- `docs/videos/ai-shorts/campaign/README.md` 的指令範例。
- `docs/videos/ai-shorts/delivery-2026-09-28.md` 的三個 MP4 連結（點了只在這台電腦上有用）。
- `docs/videos/ai-shorts/delivery-2026-09-28.json` 的成片目錄、聯絡表與日誌路徑。

skill 的檢查（`tools/skills.test.mjs`）只擋 skill 裡的本機路徑，文件沒有人擋。路徑本身不是機密，但它把本機的帳號名稱寫進公開的 repo，而且別的機器照抄指令會失敗。

2026-09-28 規劃 Shorts 區時發現的。

## Definition of done

- [x] 兩份 README 的指令範例改用佔位的寫法（例如 `<工作區>/shorts`），並說明工作區要在 repo 外。
- [x] 交付收據（`.md` 與 `.json`）的路徑改成相對於工作區的路徑；檔案的 SHA-256 不變。收據是歷史紀錄：只改路徑的前綴，其餘一字不動，並在檔案開頭註明改過什麼。
- [x] `git grep -n "Users/" docs/videos/ai-shorts` 沒有結果。

## Steps

- [x] 改四個檔。
- [x] 跑 Shorts 的測試，確認沒有測試綁著這幾個檔的雜湊。

## How to verify

```bash
git grep -n "Users/" docs/videos/ai-shorts
node --test tools/video/shorts/*.test.mjs
```

## Notes

- `tools/video/shorts/core.test.mjs` 綁的是 `pilots/*.json` 與 `experiments/*` 的雜湊，不含這四個檔；動手前再確認一次。
- 要不要順便把「文件裡不能有本機路徑」做成檢查，另外討論；這張票只改現有的四個檔。
- 2026-09-30 認領：`2026-09-28-sothatswhy-shorts-from-episode`（claude-opus，2026-09-28T09:34Z 認領，已過 24 小時，遠端沒有那條分支）的 scope 與這張票同含 `docs/videos/ai-shorts/README.md`，故用 `--force` 認領；那張票在遠端沒有分支、也沒有動到這個檔的痕跡。
- 實際替換 21 處：`README.md` 5 處（`--workdir` 3、`--dir` 2）、`campaign/README.md` 2 處、`delivery-2026-09-28.md` 3 處、`delivery-2026-09-28.json` 11 處（三支各 directory／final／contact_sheet、日誌 1、追蹤示例目錄 1）。全都改成 `<VIDEO_WORKDIR>/…`（指令範例）或相對於 `<VIDEO_WORKDIR>` 的路徑（收據）；整個 `docs/videos/ai-shorts/` 再搜 `C:\`、`C:/`、`/Users/`、`/home/`、帳號名稱、`mokaair-work` 都沒有殘留。
- 收據開頭的註明：`.md` 加一行「路徑註記」，`.json` 加 `paths_note` 欄位（JSON 沒有註解可用；檔案仍是合法 JSON，用 `json.load` 確認）。`.md` 的三個 MP4 原本是連到本機檔案的連結，改成行內程式碼路徑，不再是連結。
- SHA-256：`code_sha256`、`document_sha256` 與各檔的雜湊都是內容雜湊，沒有一個涵蓋路徑文字，也沒有測試讀這兩份收據（全 repo 只有 README 與已完成的 pilot 票連到 `.md`），所以全部原封不動。
- 驗證：`node --test tools/video/shorts/*.test.mjs` 122 通過、0 失敗（本機 Node 24.13.0，先接上主 checkout 的 node_modules，缺 `pinyin-pro` 時 bindings／pipeline 兩檔會失敗，與這次改動無關）；`npm run check:tasks` 通過（只有既有的重疊警告）。沒有跑整套 `npm run test:tools`，因為沒有測試讀這幾份文件，而且這台的 Node 24.13.0 已知會讓部分工具測試崩潰。
