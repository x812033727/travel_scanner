---
id: 2026-10-05-point-the-article-localization-skill-at
title: Point the article-localization skill at the Route B bundle compiler
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-05T09:54:35Z
completed_at:
branch:
depends_on:
  - 2026-09-29-route-b-reviewed-bundle-compiler
scope:
  - .agents/skills/article-localization/SKILL.md
  - .claude/skills/article-localization/SKILL.md
  - .agents/skills/article-localization/references/agent-route.md
  - .agents/skills/article-localization/references/bundle-release.md
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

- [ ] The skill's route table and Route B steps say that a reviewed Route B wave is
      released by compiling it (`prepare_route_b_bundle.py`) and running the
      `publish_bundle.py` phases, and when bare `guides-import` is still acceptable.
- [ ] `agent-route.md` says what the review receipt must pin (per-locale translator,
      reviewer, source and document hashes, images) so a new batch produces compiler
      input from the start.
- [ ] `bundle-release.md` names the compiler as the Route B entry into §5.
- [ ] The `.claude` copy of SKILL.md is byte-identical; no other file is added under
      `.claude/skills/`.

## Steps

- [ ] Read `docs/article-localization/route-b-bundle.md` and the compiler docstring.
- [ ] Edit SKILL.md (both copies), `references/agent-route.md` and
      `references/bundle-release.md`; name files from the repository root.
- [ ] Run `node --test tools/skills.test.mjs` and `npm run check:tasks`.

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
