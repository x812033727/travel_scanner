---
id: 2026-09-27-news-evidence-hashes-page-chrome-so
title: News evidence hashes page chrome, so TechCrunch, Verge and CoinDesk stories never publish
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-27T14:14:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/models.py
  - apps/api/tests/test_news_automation.py
---

# News evidence hashes page chrome, so TechCrunch, Verge and CoinDesk stories never publish

## Why

Before a news article publishes, `validation.revalidate_evidence` (validation.py:160-211)
fetches each evidence page again, runs `feeds.extract_article`, and compares
`policy.content_fingerprint` of the text with the stored `content_hash`. Any difference holds the
article as `news_evidence_changed`. The editor's re-check stores the new hash and runs the
verification again, and the publish revalidation then fails again.

On 2026-09-27 three articles went round this loop:

- `ai-news-openai-agent-image-leak-20260925` (TechCrunch)
- `ai-news-sony-umg-suno-lawsuit-20260925` (The Verge)
- `crypto-news-kalshi-sixth-circuit-ruling-20260925` (CoinDesk)

In each case the evidence was refreshed at 11:01Z or 11:48Z. The article passed verification,
the locale reviews and Jev by 12:24–12:34Z, and the revalidation right after Jev
(pipeline.py:980-1006) said the pages had changed.

The publishers did not edit these articles. The extracted text changed because of page chrome.
A workflow refetched each page 3 to 11 times with the app's own fetcher and extractor, diffed
the text against the stored excerpt, and had a second agent try to refute each finding. None
was refuted.

- **TechCrunch:** the story `<div class="entry-content">` holds a JW Player embed. Its inline
  `<script>` carries an element id from PHP `uniqid()`, which encodes the render time, and
  `_ArticleParser` keeps script text. The WordPress VIP edge re-renders about every 30 minutes,
  despite `max-age=300`. With that one line removed, the stored and current hashes match. There
  is no ETag or Last-Modified, and If-Modified-Since returns 200, so the 304 shortcut never
  applies.
- **The Verge:** the capture is all of `<main id="content">`. It includes the traffic-ranked
  "Most Popular" rail, which sits inside `<article>` itself, plus the "More in AI" and "Top
  Stories" rails. The rail reorders several times an hour. The ETag is Next.js's hash of the
  full HTML, so a re-render also defeats the 304 path. The current text differs from the stored
  text only in the five Most Popular items.
- **CoinDesk:** `<main>` includes "Latest Crypto News", whose server-rendered relative ages
  ("21h", "22h", "1 day ago") change on the hour, and new stories enter the list. The uncached
  SSR sometimes renders the byline and newsletter labels in Russian (1 of 3 renders). The pages
  are `no-store`, with no validators. Rebuilding the stored text from the excerpt plus today's
  JSON-LD hashes exactly to the stored `content_hash`. The only difference is lines 54-82 of the
  list.

The same holds for any source without an `article_*` selector, so it is not only these three.
Suncatcher (`tasks/done/2026-09-27-a-ready-news-article-whose-evidence.md`, a Verge page) hit it
first.

## Definition of done

- [ ] Re-rendered page chrome does not hold an article: a player id, a reordered popular list,
      relative times, rail headlines, a re-wrapped link, or UI labels in another language.
- [ ] A real edit to the story still fails closed. That means a changed number or sentence, or
      an added update paragraph, in the headline or body.
      `test_evidence_is_refetched_and_changed_content_fails_closed` keeps passing.
- [ ] The three articles above, re-checked once after the fix is deployed, reach
      `news_ready_to_publish` or publish, or fail for a reason other than
      `source_content_changed`.

## Steps

- [ ] Extractor, in feeds.py `_ArticleParser` / `extract_article` (feeds.py:151-269). Skip the
      subtrees of `script`, `style`, `noscript`, `template`, `svg`, `iframe`, `nav`, `aside`,
      `footer`, `form` and `button`. Allow per-source `exclude_tags` / `exclude_ids` /
      `exclude_classes` in `config_json`. Fix two bugs found with synthetic HTML:
      1. A self-closing void tag (`<br/>`, `<meta/>`) directly in the region ends the capture.
         `handle_startendtag` calls `handle_endtag`, which pops by depth.
      2. End tags pop by depth without checking the tag name, so an unclosed `<p>` or `<li>`
         inflates or truncates the region.
- [ ] Hash only the story body, in a new versioned column. Do not reuse `content_hash`: every
      stored row would stop matching and hold every waiting candidate at deploy.
      - Add `policy.body_fingerprint`: normalise the text (NFKC, whitespace, and joining the
        lines split at links), then hash the story paragraphs plus the JSON-LD `articleBody`
        when present. Never use `articleBody` alone, because publishers leave it stale.
      - Store it beside `content_hash` (models.py, plus a migration).
      - Compare it when both sides have it, and fall back to `content_hash` for legacy rows.
      - Keep a minimum body size. An empty or tiny body would make both hashes match
        trivially, and a real edit would slip through.
- [ ] Keep the scanner's cross-URL duplicate check working (scanner.py:238-256, which uses
      `NewsCandidate.content_hash`); a stable body hash should make it better, not worse.
- [ ] Tests with fixtures shaped like each of the three pages (no network): chrome churn keeps
      the hash, body edits change it.
- [ ] After deploy, re-check the three articles with `/admin/news` "重新查核".

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_review_actions.py -q
```

## Notes

- Alternatives considered and why they were not the first choice:
  - **Re-verify automatically at publish when only `source_content_changed`:** a bounded safety
    net. It costs one verifier call and one Jev call per publish of a churning page, and
    changes the owner's review rules, so it needs the owner's sign-off.
  - **Refetch inside the job instead of at the button:** shrinks the 45–90 minute gap. It does
    not help pages that change on every render.
  - **Skip revalidation for N minutes after a refresh:** lets an edit inside the window through
    unchecked. Only an owner-approved stop-gap.
  - **Similarity threshold:** unsafe. One changed number leaves the ratio near 0.99, and link
    re-wraps split sentences into fragments that a line rule cannot guard.
  - **Quote-per-claim fingerprints:** a diagnostic only. The claim ledger is not updated by
    later edits, and an added correction paragraph slips through.
- Per-source config alone is not enough:
  - CoinDesk's `article_classes: ["document-body"]` with `article_tags: []` was stable across
    renders.
  - TechCrunch's churn is a script inside `entry-content`, so it needs the extractor to skip
    scripts.
- The hash covers up to 40,000 characters but the stored excerpt is 8,000 (see
  `2026-09-27-news-evidence-excerpts-stop-at-8`). A cleaner extract also frees that excerpt
  budget for the story.
- The raw data (evidence rows, source configs, run history), the per-site repro scripts and the
  diffs came from the 2026-09-27 session. None of it is in the repo.
