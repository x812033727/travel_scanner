---
id: 2026-09-25-add-prod-host-ops-skill
title: Add the prod-host-ops skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-prod-host-ops
claimed_at: 2026-09-25T15:10:24Z
created_at: 2026-09-25T15:10:10Z
completed_at: 2026-09-25T15:27:00Z
branch: claude/skill-prod-host-ops
depends_on: []
scope:
  - .agents/skills/prod-host-ops
  - .claude/skills/prod-host-ops
---

# Add the prod-host-ops skill

## Why

Operating the live site outside a deploy -- reading the nginx edge, chasing a 429 or a
sporadic POST 502, diagnosing the AI planner or the news worker, changing settings through
the admin or the host CLIs, publishing the legal pages, checking an affiliate button -- was
spread over `ops/nginx/README.md`, `docs/news-automation.md`, `ops/ai-accounts/README.md`
and several personal memory notes. Each session re-derived it, and some of it had gone
stale (the AI cards moved off `/admin/settings`). A repo skill loads the procedure on
demand, shared by Codex and Claude Code.

## Definition of done

- [x] `.agents/skills/prod-host-ops/` has a SKILL.md (frontmatter, numbered rules, a
      situation table, commands, a pointer table) and five references: nginx edge and the
      keep-alive 502, AI settings and planner diagnosis, news operations, admin browser
      driving with legal pages and clickout checks, and the AI accounts agent.
- [x] `.claude/skills/prod-host-ops/SKILL.md` is a byte-identical copy.
- [x] SSH, classifier and deploy rules are linked to skill `deploy`, not repeated.
- [x] No machine paths, personal addresses, host IPs or secrets.

## Steps

- [x] Read the source memory notes and the three repo docs.
- [x] Check every command, path, endpoint and symbol against the code on main.
- [x] Write SKILL.md and the references, copy SKILL.md for Claude Code.
- [x] `node --test tools/skills.test.mjs`.

## How to verify

`node --test tools/skills.test.mjs` passes (6/6). Load the skill and follow one row of its
situation table: every path it names exists and every command matches the CLI's argparse.

## Notes

- The AI cards (`ai_vendors`, `ai_planner`, `ai_guide_search`, `hotspot_intros`,
  `gemini_guides`) now live at `/admin/ai-accounts?tab=api&provider=<id>`
  (`apps/web/lib/admin-settings-ownership.ts`), not `/admin/settings` -> AI 服務.
- `ops/nginx/README.md` check 2 says `cd /srv/travel-scanner/current`; the production host
  keeps the repo at `/root/travel_scanner`.
- `ops/nginx/README.md` and the `/ads.txt` comment in `mokaair.conf.example` say
  `05-crawler-ranges.conf` is built from googlebot.json only; the generator and the file
  include special-crawlers.json as well.
- `docs/news-automation.md` step 1 still says the deploy script passes only
  `--profile hotspots`; the host script was changed to add `--profile news`.
