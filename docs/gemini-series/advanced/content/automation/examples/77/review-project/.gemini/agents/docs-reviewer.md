---
name: lesson-docs-reviewer
description: Review the synthetic docs/limits.md against the stated 0 to 10 requirement.
kind: local
tools: [read_file, grep_search]
model: inherit
max_turns: 4
timeout_mins: 2
---
只讀 docs/limits.md 與 src/limit.mjs，不修改檔案。需求是數字限制在 0 到 10。
回傳 JSON：agent、status（complete 或 failed）、findings。
每筆 findings 包含 file、從 1 開始的 line、該行完整 quote、check、recommendation。
若文件與需求不同，分開引用原文和需求，不將程式中的錯誤當成正確規格。
