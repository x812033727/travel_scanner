---
id: 2026-10-05-point-the-article-localization-skill-at
title: Point the article-localization skill at the Route B bundle compiler
status: done
priority: P2
area: docs
owner: claude-opus-5-5-article-localization-skill-route-b
claimed_at: 2026-10-05T13:11:12Z
created_at: 2026-10-05T09:54:35Z
completed_at: 2026-10-05T13:26:50Z
branch: claude/article-localization-skill-route-b
depends_on:
  - 2026-09-29-route-b-reviewed-bundle-compiler
scope:
  - .agents/skills/article-localization/SKILL.md
  - .claude/skills/article-localization/SKILL.md
  - .agents/skills/article-localization/references/agent-route.md
  - .agents/skills/article-localization/references/bundle-release.md
  - .agents/skills/article-localization/references/pitfalls.md
---

# Point the article-localization skill at the Route B bundle compiler

## Why

The `article-localization` skill still says Route B publishes with a dry-run and then
`guides-import --slug ... --publish`, "with no journal". Ticket
`2026-09-29-route-b-reviewed-bundle-compiler` added
`docs/article-localization/prepare_route_b_bundle.py` and its operator page
`docs/article-localization/route-b-bundle.md`: a reviewed Route B wave can now be
compiled into the schema-1 bundle and published through `publish_bundle.py` with its
durable journal, live-state guards and hold checks. An agent that reads only the skill
will keep using the unguarded path, or will look for Route A job artifacts that a
Route B batch never had.

## Definition of done

- [x] The skill's route table and Route B steps say that a reviewed Route B wave is
      released by compiling it (`prepare_route_b_bundle.py`) and running the
      `publish_bundle.py` phases, and when bare `guides-import` is still acceptable.
- [x] `agent-route.md` says what the review receipt must pin (per-locale translator,
      reviewer, source and document hashes, images) so a new batch produces compiler
      input from the start.
- [x] `bundle-release.md` names the compiler as the Route B entry into §5.
- [x] The `.claude` copy of SKILL.md is byte-identical; no other file is added under
      `.claude/skills/`.

## Steps

- [x] Read `docs/article-localization/route-b-bundle.md` and the compiler docstring.
- [x] Edit SKILL.md (both copies), `references/agent-route.md` and
      `references/bundle-release.md`; name files from the repository root.
- [x] Run `node --test tools/skills.test.mjs` and `npm run check:tasks`.

## How to verify

`node --test tools/skills.test.mjs` passes (mirror and path rules). Reading only the
skill, a new agent can find the compiler command, its three pinned inputs and the
handoff to `publish_bundle.py` without opening the ticket.

## Notes

Split out of `2026-09-29-route-b-reviewed-bundle-compiler`, whose scope did not include
the skill. The compiler's v1 limits (missing locales only, no hubs, no source
corrections, no aliases) should be stated where the route is chosen, so nobody compiles
a wave that needs one of them. The release plan
`docs/work-status-2026-09-29-article-release-plan.md` also lists "Route B guard driver"
as missing; updating that record belongs with whoever next prepares a wave.

### 2026-10-05 skill update (claude-opus-5-5-article-localization-skill-route-b)

- Read `route-b-bundle.md` and checked every statement against
  `prepare_route_b_bundle.py` itself (field sets, refusals, output) and against
  `publish_bundle.py` for the hand-off. `who-is-on-it` found no active task and no open
  PR on these paths.
- `SKILL.md` (both copies, byte-identical): the route table now has a review-evidence
  row, and Route B releases through `prepare_route_b_bundle.py` and the same
  `publish_bundle.py` phases. The v1 limits sit right under the table: public, unexpired,
  unheld articles; only locales with no database row in the baseline; at most 20 slugs;
  full five-language packs; no source locale, hub, published-text correction or `aliases`
  on a selected locale. Bare `guides-import --publish` is kept only for what neither the
  compiler nor Route A takes (aliases are the case the code names). The release ticket has
  to say why, and the owner has to see that reason first. The skill also names the
  same-image rehearsal (`2026-10-05-rehearse-a-compiled-route-b-wave`) as the gate before
  the first production write. Main-flow rows 2, 4 and 9 and the command block carry the
  compiler command, its three pins and the hand-off.
- `agent-route.md`: a new section 3 covers the `route-b-review-v1` receipt: top-level
  keys, every target field, what each must pin and what the compiler refuses. Section 4
  gives the asset path and size rules. Section 6 covers freezing a
  `route-b-candidate-v1` from merged Git blobs, then the compile, review, publish steps
  and a bare-import fallback. Sections were renumbered; nothing outside the skill cited
  them.
- `bundle-release.md`: the title and intro say Route B joins at section 5, and
  section 5 opens with the compiler as Route B's entry. Fixed a stale line found while
  checking: it said `publish_bundle.py` does not read `publish_holds.json`, but since
  PR #966 (`452cdd051`) the publisher re-reads the deployed list at dry-run and, in
  `publish-articles` and `publish-hubs`, at phase entry and before every publish
  operation (`require_unheld_publications`).
- Scope: added `.agents/skills/article-localization/references/pitfalls.md`. Its line
  about holds repeated the same stale claim, and its classifier line now says the
  compiled Route B release also needs the snapshot and `publish_bundle.py` inside the
  container. No file other than `SKILL.md` was added under `.claude/skills/`.
- Checks: `node --test tools/skills.test.mjs` 7 passed, 0 failed;
  `cmp` of the two SKILL.md copies is clean; `npm run check:tasks` passes.
- Not done here: `docs/work-status-2026-09-29-article-release-plan.md` still lists the
  Route B guard driver as missing. The Notes above leave that record to whoever next
  prepares a wave.
