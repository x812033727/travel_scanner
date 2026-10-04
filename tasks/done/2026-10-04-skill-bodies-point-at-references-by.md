---
id: 2026-10-04-skill-bodies-point-at-references-by
title: Skill bodies point at references by repository-root path, and the Claude copies hold only SKILL.md
status: done
priority: P3
area: tools
owner: claude-opus-5-5-incomplete-tickets
claimed_at: 2026-10-04T16:19:48Z
created_at: 2026-10-04T16:09:26Z
completed_at: 2026-10-04T16:33:48Z
branch: claude/skills-repo-root-links
depends_on: []
scope:
  - tools/skills.test.mjs
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - .agents/skills/animation-production/SKILL.md
  - .claude/skills/animation-production/SKILL.md
  - .agents/skills/backend-conventions/SKILL.md
  - .claude/skills/backend-conventions/SKILL.md
  - .agents/skills/catalog-import/SKILL.md
  - .claude/skills/catalog-import/SKILL.md
  - .agents/skills/catchtable-discovery/SKILL.md
  - .claude/skills/catchtable-discovery/SKILL.md
  - .agents/skills/deploy/SKILL.md
  - .claude/skills/deploy/SKILL.md
  - .agents/skills/dev-and-ci/SKILL.md
  - .claude/skills/dev-and-ci/SKILL.md
  - .agents/skills/hotspot-review/SKILL.md
  - .claude/skills/hotspot-review/SKILL.md
  - .agents/skills/prod-host-ops/SKILL.md
  - .claude/skills/prod-host-ops/SKILL.md
  - .agents/skills/task-board/SKILL.md
  - .claude/skills/task-board/SKILL.md
  - .agents/skills/web-i18n-e2e/SKILL.md
  - .claude/skills/web-i18n-e2e/SKILL.md
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/references
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Skill bodies point at references by repository-root path, and the Claude copies hold only SKILL.md

## Why

`tools/skills.test.mjs` states the contract: Claude Code reads `.claude/skills/<name>/SKILL.md`, a
byte-identical copy of `.agents/skills/<name>/SKILL.md`, and "everything else (references,
scripts) lives once, under `.agents/`, and the body points at it by repository-root path". Two
parts of that are not enforced, and both have drifted:

1. **Skill-relative links.** On origin/main 9318a035f, 12 of the 14 SKILL.md bodies mention 60
   paths relative to the skill directory (`references/runbook.md`, `scripts/who-is-on-it.mjs`).
   Claude Code resolves those against `.claude/skills/<name>/`, where nothing but SKILL.md
   exists, so every one of them is a miss for Claude (Codex, reading `.agents/`, finds them).
   The "every repository path a skill mentions exists" test only looks at paths that start at
   a top-level directory, so it never sees these.
2. **Stray copies.** Because `youtube-video/SKILL.md` links `references/animation-production.md`
   that way, four reference files were copied under `.claude/skills/youtube-video/references/`
   (`animation-production.md`, `drama.md`, `prompts/writer-drama.md`, `prompts/writer-series.md`;
   #1094 and #1161). Nothing compares them: `drama.md` drifted when #1174 changed line 93 of the
   `.agents` copy only, and was resynced by hand in #1216. Earlier tickets (2026-09-26, 09-28,
   09-30) list `.claude/.../references/*` in their scopes and then found the files did not exist,
   so agents are unsure which layout holds.

## Definition of done

- [x] No SKILL.md body names a skill-relative path; each points at `.agents/skills/<name>/...`.
- [x] `.claude/skills/<name>/` holds only `SKILL.md`; the four stray reference copies are gone.
- [x] `tools/skills.test.mjs` fails on either kind of drift (a skill-relative path in a body, or
      any file under `.claude/skills/` other than a SKILL.md copy), with a message that says how
      to fix it.
- [ ] `youtube-video/SKILL.md` (both copies) is bound by the duration receipt: an independent
      reviewer adds the increment, and `node tools/video/long-form/cli.mjs check` passes.

## Steps

- [x] Wait for #1215 (animation-camera SKILL.md) and #1216 (the `.claude` `drama.md` resync) to land.
- [x] Rewrite the links (mechanically, then read every changed line), copy each SKILL.md to `.claude`.
- [x] Delete the four stray copies; extend the test.
- [ ] Receipt increment for the two youtube-video SKILL.md copies.

## How to verify

```bash
node --test tools/skills.test.mjs
node tools/video/long-form/cli.mjs check
find .claude/skills -type f ! -name SKILL.md   # prints nothing
```

## Notes

- Found on 2026-10-04 while closing `2026-10-03-drama-design-documents-say-what-the` (#1216),
  whose agent found the `.claude` `drama.md` copy out of date.
- Claimed with `--force` on 2026-10-04. The overlaps were claims whose work had landed:
  `2026-10-03-video-length-floor-only` (youtube-video SKILL.md; #1186, branch deleted),
  `2026-10-03-video-worker-narration-takes-made-stale` (#1182),
  `2026-10-03-illustrated-slides-round-2-a-family` (#1172), and
  `2026-09-29-video-language-progress-state` (codex; its branch merged as #1208, and the only
  shared paths are the two receipt files, which every receipt-bound change touches).
- 2026-10-04: 60 paths in 12 bodies rewritten by a script (each target checked to exist before
  writing), every changed line read afterwards. One mention in animation-camera ("its
  references/cost-model.md", after naming animation-production) belongs to animation-production
  and now points there. Markdown link targets that were already repository-relative
  (`../../../.agents/...`) were left alone; only their link text changed.
- The new checks were run against the origin/main deploy SKILL.md and the old `.claude` drama.md:
  both fail and name the path and the fix. With the change, `node --test tools/skills.test.mjs`
  passes 7/7.
- Not covered: bare file names without a directory (`visual-quality.md`, `i18n-diff.mjs`) are not
  paths to the test, and reference files are read from `.agents`, where their own relative
  mentions resolve.
- Receipt: the two youtube-video SKILL.md copies changed one line each (the
  animation-production.md link). The increment is added in the same PR by an independent
  reviewer after this ticket closes, which is why the last box stays open here.
