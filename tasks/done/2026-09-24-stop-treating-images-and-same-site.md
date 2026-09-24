---
id: 2026-09-24-stop-treating-images-and-same-site
title: Stop treating images and same-site pages as news evidence
status: done
priority: P2
area: api
owner: claude-opus-5.5
claimed_at: 2026-09-24T04:10:05Z
created_at: 2026-09-24T02:40:18Z
completed_at: 2026-09-24T04:10:26Z
branch: claude/news-evidence-distinct-sites
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_pipeline.py
  - docs/news-automation.md
---

# Stop treating images and same-site pages as news evidence

## Why

After the scanner's first production run (2026-09-24), Apple Newsroom's scan reported
"Skipped 76 page(s)", Microsoft's 7 and NVIDIA's 4. Every skipped URL was an image
(`/newsroom/images/...`, `/wp-content/uploads/...jpg`). `scan_source` fetches every link
inside the article whose host is an enabled evidence source, and the article's own host
always qualifies. So each image link costs a robots check and a rate-limited request
(the Apple scan took over three minutes), then fails the content-type check, and the
source is marked `partial` for something that is not a failure.

The same rule decides what counts as corroboration. A link from an official post to
another page on the same site (a related announcement, a product page) is stored as a
second `evidence` row, so a first-party post can pass the "two sources, one first-party"
gate on its own site's pages. The writer's and checker's instructions ask for "at least
two verifiable sources"; whether two pages of one company are two sources is a policy
decision that has not been made explicitly.

## Definition of done

- [x] Links that are plainly not articles (image, video, audio, PDF and archive
      extensions, and paths under upload/media folders) are dropped before any request.
- [x] Skipping such links does not mark a scan `partial`.
- [x] The site owner has decided whether a second page on the primary page's own host
      counts toward the evidence gate, and the scanner and the gate implement that
      decision (for example: same-host links are kept as context but the gate needs a
      second host).
- [x] The docs describe the rule.

## Steps

- [x] Filter non-article links in `scan_source` (and add a test with an article that
      links to images and a same-site page).
- [x] Put the same-host question to the owner with numbers from production: how many
      candidates pass the gate only because of a same-host page.
- [x] Implement the decision in the gate (`process_candidate`'s evidence check and
      `publish_candidate`) and the scanner.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_pipeline.py -q
```

On the host after deploying: the next Apple Newsroom scan finishes in about a minute and
reports no skipped image pages.

## Notes

- Seen in the production source list right after the scanner was switched on; the
  `last_error` notes on the sources show the image URLs.
- A candidate's evidence rows keep their host, so the production numbers for the
  same-host question can be read from `news_evidence` without a code change.
- Owner decision (2026-09-24, after the first production numbers: only 1 of about 60
  processed candidates had stopped at the evidence gate): pages of one website do not
  count as a second source. A website is the host without a leading `www.`; separate
  hosts of one company (blog.google, deepmind.google) are separate websites.
- Implemented as `evidence_site` / `evidence_sufficient` in `policy.py`, used by the
  pipeline gate (before any model call), by `publish_candidate`, and for the hard
  checks' source count. The scanner no longer fetches same-site links at all, so they
  are not kept as context either; and it drops image, video, audio, PDF and archive
  links by extension. Candidates already holding only same-site evidence stop at the
  gate when next processed, and a manual publish of one is refused.
