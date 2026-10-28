---
id: 2026-10-28-repair-the-inference-naer-citation-redirect
title: Repair the inference NAER citation redirect
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-28T07:36:31Z
completed_at:
branch:
depends_on:
  - 2026-10-28-localize-twelve-ai-foundation-life-guides
scope:
  - apps/api/app/guides/content/ai-term-inference.json
---

# Repair the inference NAER citation redirect

## Why

The published `ai-term-inference` source at `/sources/8/url` links to
`https://terms.naer.edu.tw/detail/8bc45e654bd178e8380ebefabc5e389b/`.
On 2026-10-28 this returned HTTP 302 with `Location: /`, followed by the
official homepage, whose body contained none of inference, 推論 or 推理.
The current exact official search still supports the terminology; technical
source review passed. Preserve this distinction and repair the citation through
a separate reviewed update instead of silently changing a translation's URL.

## Definition of done

- [ ] A current same-authority term/search URL leads readers to the intended term, with actual body proof rather than a 200 shell.
- [ ] Exact source/target versions and hashes are pinned before changing any locale citation.
- [ ] Body wording, examples, original artwork and unrelated sources remain unchanged.
- [ ] Applicable schema/content checks and reviewed publication/readback succeed.

## Steps

- [ ] Recheck the redirect chain and the canonical/current official term destination.
- [ ] Review the narrow per-locale citation diff after the dependency cohort is authored.
- [ ] Use the normal guarded source-correction/publication process and verify actual citation destinations.

## How to verify

Re-read the old and selected replacement URLs with the editorial User-Agent;
retain status, redirect chain, final URL, title and body hash. Validate the
updated ArticlePack, source/version guards and native publication receipts.

## Notes

Suggested current official search, actually read on October 28:
`https://terms.naer.edu.tw/search/?query_term=inference&query_field=title&query_op=&match_type=phrase`.
Observed homepage body SHA256:
`4e6a4afc3e5829c0e171791a93a0d23b4d0c861e4894ed4d3a7d087c1bdb238b`.
The source audit did not infer permanent route retirement or a SPA defect.
Full redirect/term evidence remains in the owner's external work directory.
The current localization baseline and jobs have not been modified for this
nonblocking citation-maintenance finding. This task is open and unclaimed.
