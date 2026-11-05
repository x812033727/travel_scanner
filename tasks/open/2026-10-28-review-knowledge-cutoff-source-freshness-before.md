---
id: 2026-10-28-review-knowledge-cutoff-source-freshness-before
title: Review knowledge-cutoff source freshness before localization
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-28T14:05:33Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-knowledge-cutoff.json
  - apps/web/public/guides/ai-term-knowledge-cutoff
---

# Review knowledge-cutoff source freshness before localization

## Why

The public knowledge-cutoff life guide is missing en, ja, ko and zh-CN. Its
thirteen primary references include model-specific and time-sensitive claims.
The October 28 candidate review deliberately excluded it until a complete current
source audit can distinguish historical examples from claims needing correction.
Prepared jobs are not evidence that the source has passed editorial review.

## Definition of done

- [ ] The complete source, all thirteen references and original artwork have a dated, independently reviewed claim ledger with no unresolved blocking issue.
- [ ] Any required source changes have an exact independently approved native source-correction receipt; unchanged values and image bytes are preserved.
- [ ] Fresh source/version/target bindings support four independently reviewed translations and artwork through the existing localization pipeline.
- [ ] Content checks and a guarded PR pass; a separate release task owns production authorization, backup, publication and public acceptance.

## Steps

- [ ] Recheck ownership, current source and target absence; claim before content edits.
- [ ] Read all thirteen primary references and review every source claim against actual original artwork.
- [ ] Resolve any source corrections before translating; preserve the original prepared jobs and baseline.
- [ ] Complete native translation, independent review, assembly/install/replay and scoped checks.
- [ ] Create an unclaimed release task for the final reviewed cohort.

## How to verify

Follow article-localization: build_baseline.py, source_correction.verify_review
if needed, pipeline.py, render.mjs, assemble_bundle.py and install_bundle.py.
Record actual dated primary-source responses and claim-level conclusions outside
Git. Schema success or the existing image review alone does not clear source text.

## Notes

- The bounded production snapshot at 2026-10-28T13:31:16 UTC found this article
  public, active and unexpired, with a clean source matching the repository and
  no target-language rows. Snapshot SHA256:
  `254a9d71289f11eae001b9d9174341b8de19d87ad4c9a16d31fca67476f1199f`.
- The original seven-article baseline SHA256 is
  `d62d596e344498f584795b0be3eaa8c81b3f0ce82bbbafe10cf2ef889867bd11`.
  Four prepared jobs remain outside Git without any model attempt. Do not
  assume their historical source pins remain current when work resumes.
- The seven-article actual image review is retained with SHA256
  `885aaae8a427f89937e7ad8d1f99a6c7bc0802cf051c776260ceed45559f3db4`.
  This is not a complete primary-reference audit or publication authorization.
- This article is excluded from the two-concept eight-translation bundle.
