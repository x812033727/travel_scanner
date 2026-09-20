---
id: 2026-09-20-fix-localization-mcp-preflight-overrides
title: Fix localization MCP preflight overrides
status: done
priority: P1
area: tools
owner: codex-article-localization
claimed_at: 2026-09-20T03:02:36Z
created_at: 2026-09-20T03:02:34Z
completed_at: 2026-09-20T03:05:09Z
branch: codex/article-localization-mcp-preflight
depends_on:
  - 2026-09-20-five-language-article-release-tooling
scope:
  - tools/article-localization
---

# Fix localization MCP preflight overrides

## Why

The desktop Codex configuration can inject MCP servers outside the user config file.
A field-only `enabled=false` CLI override creates an incomplete higher-precedence server
entry and Codex rejects it as an invalid transport before translation starts.

## Definition of done

- [x] Every effective MCP server gets a minimal, non-secret transport override plus
      `enabled=false` in the translation child.
- [x] Unknown or incomplete transports fail closed before any model call.
- [x] The child inventory proves all servers are disabled.
- [x] Ruff and pipeline tests pass.

## Steps

- [x] Reproduce the failure with an injected desktop server.
- [x] Generate safe stdio and streamable HTTP transport overrides.
- [x] Add regression tests and verify a real child preflight.

## How to verify

`uv run --project apps/api ruff check tools/article-localization` and
`uv run --project apps/api python tools/article-localization/test_pipeline.py`.

## Notes

The override must not copy MCP environment maps, headers, bearer tokens or other
credential-bearing fields. Only the transport discriminator needed for Codex config
validation may be repeated; the server remains disabled.
