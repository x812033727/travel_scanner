---
id: 2026-10-23-independently-recheck-c19-v5-seven-visual
title: Independently recheck C19 v5 seven visual prompts
status: in-progress
priority: P2
area: docs
owner: codex-c19-v5-visual-delta-review
claimed_at: 2026-10-23T08:11:39Z
created_at: 2026-10-23T08:11:28Z
completed_at:
branch: codex/c19-seven-bank-v5-visual-delta-review
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/reviews/independent-v5-visual-delta.md
---

# Independently recheck C19 v5 seven visual prompts

## Why

The author fixed seven visual prompts held by independent full review #1769. That review is bound to an older author commit. The new seven-shot delta needs a separate, hash-bound reviewer before the v5 script and visual plan can reach the owner gate.

## Definition of done

- [x] Verify the exact old-to-new diff, unchanged script/source bytes and narrator projection, and 79-line MD/JSON pairing.
- [x] Independently judge all seven new prompts for one visible person performing one action and for no new unsupported fact.
- [ ] Publish a separate draft PR stacked on new author commit `83415c48249250c3cff6e302c1d7a79514377610`.

## Steps

- [x] Compare every JSON field and MD visual row against the #1769-audited author commit.
- [x] Re-read all seven revised prompts beside their current narration and source boundaries; write the independent delta receipt.
- [ ] Commit, push, create and attach the stacked draft PR.

## How to verify

`python` old/new Git blob comparison: only seven `prompt` fields and the matching seven MD rows differ; script/source bytes match old hashes; all 79 IDs, narration, source tags and visual text align. `git diff --check` and `npm run check:tasks` before PR. Verify base, head, draft flag and `no-auto-merge` on GitHub after PR creation.

## Notes

Result: seven revised prompts PASS for text-only visual preflight, bringing v5 paired visual plan to 79/79 PASS with #1769's unchanged 72. This does not attest to rendered MiniMax images or TTS duration. Receipt: `docs/videos/story-everyday-seven-bank-c19/reviews/independent-v5-visual-delta.md`.
