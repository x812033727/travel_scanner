# Published-news source review

The daily news scheduler now queues a bounded source check when news automation is
enabled. This feature is implemented in the branch; deployment and current production
settings have not been verified or changed by this work.

The admin news page has a separate, failure-isolated source-review panel. It exposes
all, overdue and changed-source views with server-side pagination. An unavailable panel
does not block the existing editor. The endpoint requires `content.read`; loading it
does not fetch external sources or write data.

## Coverage and meaning

- News candidates created by the pipeline, subsequently published (including human
  approval), linked to an article and published within the last 90 days are eligible.
  Older and manually imported articles are not silently represented as checked.
- The oldest unchecked/oldest-attempted eligible articles are considered first.
  There are at most 20 reservations per UTC day, across repeated jobs and workers.
  Running and failed attempts count. A PostgreSQL transaction advisory lock protects
  the quota reservation and is released before network I/O.
- Each attempt has a seven-day interval, including failed or interrupted attempts.
  There is no automatic same-day retry. The admin list exposes uncertainty and the
  last attempt time; it does not promise every article was checked today.
- At most four evidence rows per article are probed, first-party rows first. A partial
  check is `unverified`. Each article has 25 seconds and a batch has 540 seconds.
- `changed` means the retained source text differs. `unchanged` means the source text
  matched, not that a product is still available or every fact remains correct.
  Unavailable, disabled, unreadable, incomplete and timed-out sources are unverified.
  An expired validity badge uses the article's existing `valid_until` value only.

## Protected state

The existing SSRF-safe, robots-aware, rate-limited fetcher and publication validator
are reused on transient evidence copies. Real evidence hashes, excerpts, validators
and `retrieved_at` remain untouched, so the 90-day excerpt-retention window is not
extended. Article bodies, locale publication state, validity and revisions are not
modified. Results contain counts/status only in `NewsPipelineRun` receipts; fetched
text, credentials, response headers and exception messages are not copied into them.

No AI models, paid fact checks, translation, redrafting or republication are queued.
The source-review links open the existing candidate editor for a human decision.

## Validation

`test_news_freshness.py` covers preservation of original evidence, unknown vs changed,
partial evidence, timeout, disabled automation and scheduling identity.
`test_news_freshness_integration.py` uses a fresh local PostgreSQL schema to test two
workers competing for the twentieth reservation, repeated runs, pagination beyond
50 results, malformed receipt isolation and unchanged article/evidence data.

The UI tests cover five locales, read-only reload after an unavailable endpoint,
published-candidate navigation and requests for overdue pages. Production deployment
and public validation remain separate from these local/CI checks.
