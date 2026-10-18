---
id: 2026-10-11-expose-upstream-http-status-and-recover
title: Expose upstream HTTP status and recover held-news source validation
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-11T08:37:13Z
completed_at:
branch: claude/youthful-brahmagupta-1giys7
depends_on: []
scope:
  - apps/api/app/news_automation/validation.py
  - apps/api/tests/test_news_refetch_diagnostics.py
---

# Expose upstream HTTP status and recover held-news source validation

## Why

The CFTC candidate e25bc5a4-cca4-4e61-bb77-5b1b45243561 now has a genuine,
audited five-language Guide draft. Its normal reverify passed factual and all
five locale reviews on October 11, but the final judge's publish verdict was
downgraded to manual/news_evidence_changed because the official release could
not be refetched. validation.revalidate_evidence records only HTTPStatusError,
which hides whether the failure was a denied robots request, an article HTTP
status, or a content mismatch. This makes operational recovery ambiguous.

Root's read-only native SafeNewsFetcher diagnostics at 08:35:45 and 08:36:19
UTC both returned article HTTP 403 with Cloudflare headers, with and without
the stored Last-Modified condition. They retained robots, public-IP pinning,
Host/SNI, TLS, source allowlists and response limits. No Evidence, queue or
model state was changed by either diagnostic. A separately accessible web
copy is not a successful native source-current check.

## Definition of done

- [x] Held-source diagnostics retain a bounded, safe upstream status and request
      stage so editors can distinguish transport refusal from changed content.
- [ ] The CFTC source is successfully checked through the native safe fetcher
      before any normal refresh/reverify, or its external access blocker remains
      explicitly documented with preserved drafts, private assets and receipts.
- [ ] No manual Evidence injection, robots/TLS/SSRF bypass, false current-source
      approval, history deletion or lifetime judge-cap reset is introduced.

## Steps

- [ ] Inspect the native conditional and unconditional diagnostics and the final
      candidate/run/assessment/audit state before attempting recovery.
- [x] Add bounded upstream diagnostic metadata without response credentials or
      unrestricted bodies, preserving the existing public error contract.
- [ ] Once official access succeeds, use the normal audited refresh-evidence
      route and independently read its Evidence, audit, retry and exact queue
      identity before continuing the final judge/publication gates.

## How to verify

Run focused news validation regressions for HTTP status, robots refusal and
actual content mismatch, plus API Ruff/mypy. Before a production action, read
the actual candidate and RQ state. A failed or unknown commit/enqueue outcome
must be read back and never blindly replayed. Publication requires successful
native source-current verification and actual locale public-page checks.

## Notes

The immutable receipts are under the existing news-review/20261010-6f71
evidence root: cftc-native-final-stage-v1.json (1ac03376),
cftc-native-official-source-conditional-readonly-v1.json (74ccbd8c), and
cftc-native-official-source-unconditional-readonly-v1.json. The final snapshot
is manual_review/news_evidence_changed, retry5, unpublished, with no live job.
The genuine ingestion audit is 2432c35e-2171-4436-9e83-a1a5b2d38c74 and the
native reverify audit is 9dc7958c-8d58-48d4-a852-1fbc632405d8. Do not replay
either operation or generate another hero. The current hero is private and
source-bound; successful model reviews alone do not authorize publication.
The official URL is https://www.cftc.gov/PressRoom/PressReleases/9307-26.

Collision check at08:58UTC found existing source-fetch task
2026-10-11-news-fetcher-is-refused-by-cloudflare and open PR1440, which edits
only that task's diagnostic Notes. Its author reports that advertising only
HTTP/1.1 through ALPN triggers the CFTC feed challenge, while no ALPN passes;
this is their diagnostic evidence, not a new Root source-fetch success. The
published PR proposes possible HTTP/2/transport work but contains no fetcher
implementation. Track the actual transport fix in that existing task; this
new task covers bounded diagnostic visibility and the CFTC candidate's
separate audited recovery after native source access succeeds. Do not open a
competing fetch.py implementation or claim overlapping active test scope.

At09:54UTC, freshly fetched origin/main27b77 contains the task-only diagnostic
updates merged through PR1440 and PR1441. The later one-off container tests
found CFTC403 with HTTP/2 as well as HTTP/1.1, by name and pinned address;
curl and urllib controls returned200. The existing HTTP2 branch remains
unmerged with no PR and is explicitly recorded as an unsuccessful proposal.
The suggested next transport preserves resolved public-IP pinning, original
Host/SNI/certificate checks, bounds and redirect refusal without httpcore's
ALPN handshake. It is not implemented or deployed. Do not treat HTTP2 or the
two merged diagnostic notes as recovered native CFTC article access, and do
not repeat the earlier probing that reached429. Current production remains
the verified3591 release, and Root has not altered this source or fetcher.

### 2026-10-16 diagnostics in the repo (claude-opus-5-5-pr-tidy)

The first box is done in the repo. The CFTC recovery (second box, third step) is still open and
needs the host: it was not attempted here.

Claimed with `--force` over `2026-10-11-news-fetcher-is-refused-by-cloudflare`. That task's code
landed in #1516, its branch is gone, and its one open step is a host-side `sources_cli` rerun.
Scope moved from `test_news_automation.py`, which draft #1480 extends, to a new
`apps/api/tests/test_news_refetch_diagnostics.py`.

`validation.py`: the four `source_refetch_failed` reasons (two in `refresh_evidence`, two in
`revalidate_evidence`) now come from `_refetch_failed(url, error, stage)`.
- When the fetch says why, the reason keeps its old prefix and adds `:<stage>:<detail>`:
  - `stage` is `listing` (the feed or listing read for a summary source) or `article` (the
    evidence page).
  - `detail` is `http_<status>` for an upstream status, `robots_refused`, `content_type`,
    `too_large`, `redirect` or `unsafe_url`.
- Example: `source_refetch_failed:<url>:HTTPStatusError:article:http_403` is the Cloudflare
  refusal the 08:35/08:36 diagnostics saw.
- Only fixed codes and the integer status are kept, never a body, header or cookie.
- A failure that says nothing more (a timeout) keeps the earlier
  `source_refetch_failed:<url>:<class>` form. The existing exact-string tests and the
  prefix-based handling are unchanged, and nothing in api or web parses these strings.

Ran: the new tests (7/7, covering 403, 503, a robots refusal, content type, non-public address,
an unchanged timeout through both functions, and real changed content still reported as
`source_content_changed`). Also `test_news_automation.py`, `test_news_review_actions.py`,
`test_news_backfill_cli.py` and the new files (314 passed, 6 skipped), `ruff check .`, `mypy app`
and `mypy tests`.

Released after this change so the host recovery can be picked up; nothing else in the repo is
left for it.
