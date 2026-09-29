---
id: 2026-09-27-news-evidence-hashes-page-chrome-so
title: News evidence hashes page chrome, so TechCrunch, Verge and CoinDesk stories never publish
status: done
priority: P1
area: api
owner: claude-opus-5-5-evidence-hash
claimed_at: 2026-09-28T12:08:30Z
created_at: 2026-09-27T14:14:25Z
completed_at: 2026-09-28T12:59:30Z
branch: claude/news-evidence-body-hash
depends_on: []
scope:
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/models.py
  - apps/api/tests/test_news_automation.py
  - apps/api/migrations/versions/0112_news_evidence_body_hash.py
  - apps/api/tests/test_migration_0112_news_evidence_body_hash.py
  - apps/api/app/news_automation/sources.json
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

- [x] Re-rendered page chrome does not hold an article: a player id, a reordered popular list,
      relative times, rail headlines, a re-wrapped link, or UI labels in another language.
- [x] A real edit to the story still fails closed. That means a changed number or sentence, or
      an added update paragraph, in the headline or body.
      `test_evidence_is_refetched_and_changed_content_fails_closed` keeps passing.
- [ ] (Follow-up task `2026-09-28-apply-news-source-configs-and-re`.) The three
      articles above, re-checked once after the fix is deployed, reach
      `news_ready_to_publish` or publish, or fail for a reason other than
      `source_content_changed`.

## Steps

- [x] Extractor, in feeds.py `_ArticleParser` / `extract_article` (feeds.py:151-269). Skip the
      subtrees of `script`, `style`, `noscript`, `template`, `svg`, `iframe`, `nav`, `aside`,
      `footer`, `form` and `button`. Allow per-source `exclude_tags` / `exclude_ids` /
      `exclude_classes` in `config_json`. Fix two bugs found with synthetic HTML:
      1. A self-closing void tag (`<br/>`, `<meta/>`) directly in the region ends the capture.
         `handle_startendtag` calls `handle_endtag`, which pops by depth.
      2. End tags pop by depth without checking the tag name, so an unclosed `<p>` or `<li>`
         inflates or truncates the region.
- [x] Hash only the story body, in a new versioned column. Do not reuse `content_hash`: every
      stored row would stop matching and hold every waiting candidate at deploy.
      - Add `policy.body_fingerprint`: normalise the text (NFKC, whitespace, and joining the
        lines split at links), then hash the story paragraphs plus the JSON-LD `articleBody`
        when present. Never use `articleBody` alone, because publishers leave it stale.
      - Store it beside `content_hash` (models.py, plus a migration).
      - Compare it when both sides have it, and fall back to `content_hash` for legacy rows.
      - Keep a minimum body size. An empty or tiny body would make both hashes match
        trivially, and a real edit would slip through.
- [x] Keep the scanner's cross-URL duplicate check working (scanner.py:238-256, which uses
      `NewsCandidate.content_hash`); a stable body hash should make it better, not worse.
- [x] Tests with fixtures shaped like each of the three pages (no network): chrome churn keeps
      the hash, body edits change it.
- [ ] After deploy, apply the three source configs and re-check the three articles with
      `/admin/news` "重新查核" (moved to `2026-09-28-apply-news-source-configs-and-re`).

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

## What was done (2026-09-28, claude-opus-5-5-evidence-hash)

- The extractor part had already landed in PR #892: `_ArticleParser` keeps an open-element
  stack by name (an end tag closes to its nearest namesake), treats `<br/>` and other
  self-closing tags as empty elements, and skips `SKIPPED_TAGS` plus per-source
  `exclude_tags` / `exclude_ids` / `exclude_classes`.
  `test_extractor_keeps_the_story_past_self_closing_tags_and_skips_page_chrome` covers both
  bugs. The old parser stays as `_LegacyArticleParser` for `validation._legacy_match`.
- `feeds.read_article` returns an `Article`: the old title/text/links plus the body-fingerprint
  inputs. Each story element (`p`, `li`, `h1`-`h6`, `blockquote`, `pre`, `td`, `th`, `dd`, `dt`,
  `figcaption`) inside the region and outside skipped chrome is one line, its text taken whole,
  so a link moved onto other words does not split it. The first `<h1>` outside skipped chrome
  is the headline (a narrow region often starts below it). JSON-LD `articleBody` is read from
  `application/ld+json` scripts, `@graph` included. `extract_article` is unchanged for callers,
  and the page text (so `content_hash`) is byte-for-byte what it was.
- `policy.body_fingerprint` hashes `body-v1`, the headline, the story lines and the
  `articleBody`, each NFKC-normalised with whitespace collapsed, and stores `body-v1:<sha256>`.
  It returns None when the story lines hold under 400 characters (`MIN_BODY_CHARACTERS`, the
  `articleBody` never counts toward it) or under half of the region's text
  (`MIN_BODY_COVERAGE`, so loose `<div>` text cannot hide behind a few captions).
- Migration `0112_news_evidence_body_hash` adds nullable `body_hash` (`String(80)`) to
  `news_evidence` and `news_candidates` (indexed there). No backfill: a stored row cannot be
  re-hashed without its page.
- `revalidate_evidence` and `refresh_evidence` compare the body hash when the stored row and the
  current page both have one of the current version, else `content_hash`, and a row without a
  body hash may still match the legacy extraction. Revalidation never writes `body_hash`;
  the editor's re-check (`refresh_evidence`) does, so a waiting candidate moves to the story
  hash only through a fetch that re-verified it.
- The scanner stores the body hash on the candidate and each evidence row and also treats an
  equal `NewsCandidate.body_hash` as an exact duplicate.

## What I learned

- Per-source config is still needed: the story-element rule alone does not stop rails built
  from `<li>` or `<p>`. Checked against live pages (three per feed, fetched 12:05Z and again
  12:57Z on 2026-09-28 with the app's `USER_AGENT`, the second pass cache-busted): with the new
  extractor but no config, CoinDesk changed 3 of 3 and TechCrunch 2 of 3 in both hashes; with
  the configs in `sources.json`, all 9 kept both hashes.
  - TechCrunch: `article_tags: []`, `article_classes: ["entry-content"]`. `<main>` holds the
    Related and Latest in AI cards ("16 hours ago") and a rotating event promo.
  - The Verge: `exclude_classes: ["duet--layout--rail", "duet--layout--article-recirc"]`
    (Most Popular inside `<article>`; More in AI and Top Stories).
  - CoinDesk: `article_tags: []`, `article_classes: ["document-body"]`,
    `exclude_classes: ["premium-hide"]`. The paragraphs themselves carry live price chips
    (`BTC$83,034.73`, rendered `$83 363,33` in a Russian-locale render), all under
    `premium-hide` with the figcaptions and the video slot.
- Changing a source's config changes the `content_hash` its pages extract to, so evidence
  stored under the old config (no body hash) is held at publish until the editor's re-check
  stores a body hash. The three articles need that re-check anyway.
- Python's `Path.write_text` on Windows writes CRLF; write bytes when editing repo files from a
  script.
