---
id: 2026-10-09-fix-the-powershell-examples-in-the
title: Fix the PowerShell examples in the headless-mode article
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-09T11:49:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/claude-code-headless-json.json
---

# Fix the PowerShell examples in the headless-mode article

## Why

The article `claude-code-headless-json` (〈非互動執行與 JSON 輸出〉) gives PowerShell forms of its
commands. While planning the headless-mode tutorial on 2026-10-09, three forms it uses were
measured, with no model involved, on Windows PowerShell 5.1.26100 (console code page 65001), by
handing the arguments and the piped input to two small Node programs that print what they
received:

1. An empty-string argument is not passed. `-p --tools "" --output-format json` reaches the
   program as four arguments, not five. Git Bash passes the empty string.
2. `--json-schema (Get-Content -Raw schema.json)` reaches the program with every double quote
   removed, so it is no longer JSON. Git Bash's `"$(cat schema.json)"` arrives intact.
3. `Get-Content -Raw inbox.txt | program` with the default `$OutputEncoding` (us-ascii) turns
   every Chinese character into a question mark: a 336-byte file arrived as 341 bytes, of which
   300 were 0x3f. Adding `-Encoding UTF8` still left 100. Only setting
   `$OutputEncoding = New-Object System.Text.UTF8Encoding $false` first and then using
   `-Encoding UTF8` delivered the text, with a three-byte BOM in front.

A reader on Windows who follows the article's PowerShell lines sends Claude Code a different
command from the one the text describes, and for Chinese input a different text.

## Definition of done

- [ ] Each PowerShell example in the article is run as written on PowerShell 5.1 and on
  PowerShell 7, and what the program receives is recorded.
- [ ] Examples that do not deliver what the text says are rewritten, or replaced by a note to
  use Git Bash, and the article says which shells were checked.
- [ ] The article is verified again and republished through the content pipeline.

## Steps

- [ ] Reproduce with two probe programs that print argv and the bytes of stdin.
- [ ] Decide per example: a working PowerShell form, or Git Bash only.
- [ ] Check the sibling articles that reuse the same forms.

## How to verify

Run each rewritten example with a program that echoes its arguments and the bytes of its stdin
in place of `claude`, on both PowerShell versions; they equal what Git Bash delivers.

## Notes

- The measurements are in the brief of the headless-mode tutorial (slug
  `claude-code-headless-hands-on`, section 平台的決定) once that video's folder is in the
  repository; the raw log stayed outside the repo.
- PowerShell 7, cmd, macOS and Linux were not measured.
- Not measured either: what `--tools` means to Claude Code when its empty value never arrives.
