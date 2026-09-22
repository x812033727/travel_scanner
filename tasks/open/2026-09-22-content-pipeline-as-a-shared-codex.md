---
id: 2026-09-22-content-pipeline-as-a-shared-codex
title: Content pipeline as a shared Codex/Claude skill
status: review
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-22T13:45:51Z
created_at: 2026-09-22T13:45:45Z
completed_at:
branch: claude/skill-token-efficiency-16c9e3
depends_on: []
scope:
  - .agents/skills/content-pipeline
  - .claude/skills/content-pipeline
  - tools/skills.test.mjs
  - AGENTS.md
---

# Content pipeline as a shared Codex/Claude skill

## Why

內容產線（撰稿 → 查核 → 翻譯 → 審稿 → 機械檢查 → `pack_cli ingest` → PR → 部署 →
`guides-import --dry-run` → `--publish` → 逐頁驗證）的步驟與坑，到 2026-09-22 為止散在三個地方：
Claude 的個人記憶（38 KB 的內容產線記憶檔，加上每個 session 都載入的 17 KB 索引；Codex 完全看不到）、
repo 外的批次工作區（撰稿／查核提示與 `intake_check.py`，硬寫第八批的 slug 表與絕對路徑，每批重寫一次，
Codex 做韓國美食時又另寫了一份）、以及四份互相複製的上線 runbook。上線後的逐頁驗證腳本只剩在一個已結束
session 的 scratchpad 裡。

做成兩個 harness 都能載入的 skill：常駐的只有名稱與描述，本文用到才載入，檢查包成腳本不佔 context；
Codex 與 Claude Code 讀同一份。

## Definition of done

- [x] `.agents/skills/content-pipeline/`（Codex 讀的正本）與 `.claude/skills/content-pipeline/SKILL.md`
      （Claude Code 讀的逐字複本）存在；`npm run test:tools` 比對兩份、檢查 frontmatter 只用兩邊都認的 key、
      每個引用的 repo 路徑存在、沒有機器路徑與個人 email。
- [x] 三個腳本（`intake_check.py`、`shared_check.py`、`verify_public.py`）對已上線的內容包跑得通，
      規則從 `app.guides` 匯入而不重抄。
- [ ] 新開的 Claude Code 與 Codex session 各自看得到 `content-pipeline`（合併後在主 checkout 驗）。
- [ ] Claude 端的記憶檔縮短、指向 skill（合併後做，不進 git）。

## Steps

- [x] 開票、認領、`uv sync --frozen`、root `npm ci`。
- [x] SKILL.md（127 行）、references 六份、prompts 兩份、`agents/openai.yaml`。
- [x] `intake_check.py` 從批次工作區的版本一般化：`--manifest` 取代硬寫的 slug 表，字數預設用 repo 的
      `TEXT_RANGE`／`INTEL_TEXT_RANGE`，加 `lint_document` 與 `check_svg`／`missing_diagram_numbers`。
- [x] `shared_check.py` 改讀 `--rules` JSON；`verify_public.py` 重寫成循序、1.3 秒間隔。
- [x] `tools/skills.test.mjs`；AGENTS.md 加一句。
- [ ] 開 PR、合併。
- [ ] 合併後：主 checkout `git pull`，開新 Claude Code session 確認 `/content-pipeline`；
      開 Codex 確認 `$content-pipeline`，而且 worktree 裡只看到一個。
- [ ] 合併後：縮短 Claude 記憶（內容產線、新聞第四批、韓國美食、AI 新聞批次、reader-first 五條 hook
      各一行；38 KB 記憶檔只留歷史與決定）。

## How to verify

```bash
npm run test:tools                                   # 含 tools/skills.test.mjs
cd apps/api && PYTHONUTF8=1 .venv/Scripts/python.exe "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ../../.agents/skills/content-pipeline
cd apps/api && uv run ruff check --config pyproject.toml ../../.agents/skills/content-pipeline/scripts
cd apps/api && PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug sentosa-day-guide --from-content
cd apps/api && .venv/Scripts/python.exe ../../.agents/skills/content-pipeline/scripts/verify_public.py --slug sentosa-day-guide --locale zh-TW --sitemap
```

測試要會咬人：把 `.claude/skills/content-pipeline/SKILL.md` 尾端加一個換行、或在 references 塞一個
`C:\Users` 路徑，`npm run test:tools` 要紅。

## Notes

- 2026-09-22 實測：`intake_check.py --from-content` 對 `sentosa-day-guide` PASS；對
  `busan-milmyeon-food-guide` FAIL 一條「本文／這篇」出現 2 次（規則上限 1）。那是內容問題不是腳本問題，
  內容目錄不在本票 scope，留給美食特輯的後續票。
- Codex 的 `quick_validate.py` 用 `read_text()` 沒指定編碼，在 Windows 會以 cp1252 讀中文而崩潰；
  加 `PYTHONUTF8=1` 就過。這是驗證器的問題，Codex 本身讀 skill 沒事。
- YAML 的坑：description 是純量，裡面不能有「冒號加空格」，否則 js-yaml 與 PyYAML 都會當成 mapping 而失敗。
- 為什麼是逐字複本不是薄殼：Claude 在 context 壓縮後只會重新掛回「它載入的那個檔」的前 5,000 token，
  三行薄殼會讓程序在第一次壓縮後消失；自動觸發也會多一步 Read。
- 為什麼不用 symlink：本機 `core.symlinks=false`，Windows checkout 會把 symlink 變成純文字檔。
- 五語系新聞的腳本留在 `docs/news-2026-batch-4/`（已在 repo），skill 只指路，不複製第五份；
  四份 `docs/ai-news-*` 分岔的整併另開票。
- 批次工作區的 `_tools/` 正被 batch-8 的協調 session 使用：只複製、沒動。合併前開的 worktree 沒有這個 skill，
  batch 8 到上線都得用原本的檔。
- 後續票候選：(1) 整併新聞腳本分岔；(2) `.gitignore` 加 `.claude/worktrees/` 與 `.claude/settings.local.json`
  （目前只靠本機 `.git/info/exclude`）；(3) 把讀者優先計數併進 `pack_cli lint` 當 warning（與
  `2026-09-21-91-ci` 協調）；(4) Codex 的模型／用量量測補進角色表。
