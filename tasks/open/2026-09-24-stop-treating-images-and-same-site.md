---
id: 2026-09-24-stop-treating-images-and-same-site
title: Stop treating images and same-site pages as news evidence
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T02:40:18Z
completed_at:
branch:
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

- [ ] Links that are plainly not articles (image, video, audio, PDF and archive
      extensions, and paths under upload/media folders) are dropped before any request.
- [ ] Skipping such links does not mark a scan `partial`.
- [ ] The site owner has decided whether a second page on the primary page's own host
      counts toward the evidence gate, and the scanner and the gate implement that
      decision (for example: same-host links are kept as context but the gate needs a
      second host).
- [ ] The docs describe the rule.

## Steps

- [ ] Filter non-article links in `scan_source` (and add a test with an article that
      links to images and a same-site page).
- [ ] Put the same-host question to the owner with numbers from production: how many
      candidates pass the gate only because of a same-host page.
- [ ] Implement the decision in the gate (`process_candidate`'s evidence check and
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
