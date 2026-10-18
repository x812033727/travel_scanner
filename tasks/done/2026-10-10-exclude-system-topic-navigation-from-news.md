---
id: 2026-10-10-exclude-system-topic-navigation-from-news
title: Exclude system topic navigation from news factual verification
status: done
priority: P1
area: api
owner: codex-news-recovery-6f71
claimed_at: 2026-10-10T01:29:00Z
created_at: 2026-10-10T01:27:46Z
completed_at: 2026-10-10T01:40:53Z
branch: codex/news-recovery-20261010
depends_on: []
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_ai.py
---

# Exclude system topic navigation from news factual verification

## Why

The factual verifier currently receives the full saved article, including the topic
navigation link added by the site. In the recovery pilot, Anthropic's biolab article
was held solely because its system-added /life/topics/ai-news link was absent from
source evidence. Other review stages already use the existing for_review projection
to exclude system navigation. Use that same projection for factual verification,
while retaining authored facts and external links.

## Definition of done

- [x] System-added topic navigation does not create an unsupported-fact hold.
- [x] Authored facts and external links remain visible to the verifier.
- [x] The saved document and its existing evidence fingerprint stay unchanged.

## Steps

- [x] Reproduce the incorrect payload with a focused verifier regression.
- [x] Use the existing review projection and run relevant suites and static checks.

## How to verify

Run the focused tests in apps/api/tests/test_news_ai.py and affected news pipeline
and automation suites with the worktree API virtual environment. Run Ruff and mypy
for the changed API modules and tests. Record exact results below before completion.

## Notes

Production pilot candidate: 0f71c3b3-a4e3-4230-9553-8a11439d3d10.
Verifier assessment: 8d3ac94c-e4d7-41a9-80ed-c683fabdcce1.
This task does not bypass verification or alter publication gates. Production
resubmission remains separate from the local repair, merge, and deployment.
- Changed only verify_article's article payload to existing for_review(document).
  The policy projection/fingerprint and original documents remain unchanged.
- Before repair: 15 navigation cases failed, 3 unsupported-authored-content cases
  passed (exit1). After repair: new AI, automation, pipeline, policy and JEV
  suites total 282 passed (exit0); an independent focused run passed all18.
- Full API Ruff passed; mypy app passed470files and tests passed381files (exit0).
  Independent code review found no blocker. git diff --check passed.
- Authored repair is complete in draft PR1411; production resubmission waits for
  the owner-controlled merge/deployment and independent normal review.
