# AI hourly news automation

`apps/api/app/news_automation` finds news on allow-listed sources every hour, drafts a
Traditional Chinese article from the evidence, has a second model check it, translates it
into the other four site languages, asks Jev whether each locale is ready, and then either
parks the five-locale bundle for review or, once a category has earned it, publishes it.
Everything ships switched off. This page is the order in which to switch it on and what
each switch does.

## The moving parts

| Piece | Where | What it does |
| --- | --- | --- |
| `news-scheduler` | compose profile `news`, `app.news_automation.scheduler` | Once a minute: queues a scan for every due source, fails candidates whose job died (see below), re-queues orphaned ones, queues the daily retention cleanup |
| `news-worker` | compose profile `news`, `app.news_automation.worker` | The only consumer of the `news` RQ queue. The general `worker` does not read it, so a candidate's hour of model calls never blocks search or trip routing |
| `/admin/news` | web | Sources, settings, the review queue, runs and the per-category activation gates |
| Admin AI settings | `/admin/settings` → AI 服務 | API keys and the default model per vendor. The news jobs read them the same way the hotspot AI tasks do (`load_runtime_settings`) |

Nothing runs while the `news` profile is down: jobs queued from `/admin/news` (scan now,
retry, re-verify) wait in Redis until `news-worker` starts.

## One candidate, stage by stage

1. **Scan.** The scheduler claims due sources (one catch-up scan after downtime, never a
   replay of every missed hour). Entries whose URL was already seen are not fetched again.
   Each new entry's page is fetched through `SafeNewsFetcher` (HTTPS only, allow-listed
   hosts, public IPs pinned against DNS rebinding, robots.txt honoured and read once per
   host per scan, 2 MB limit). Links from the article to articles on *other websites* that
   are enabled evidence sources are fetched as additional evidence; links to the page's
   own site and to images, video, audio, PDFs or archives are not fetched. A page that
   fails is skipped and listed on the source (`partial`), and the listing's ETag is kept
   back so the next scan tries it again. Exact URL, title or content matches are closed as
   duplicates at once.
2. **Evidence gate.** Evidence from at least two different websites (host without
   `www.`), one of them first-party, or the candidate stops before any model call with
   status `needs_evidence` (`news_evidence_insufficient`). That status is not manual
   review: it has its own 「缺證據」 list in `/admin/news`. Evidence is only gathered at
   the first scan, so running such a candidate again cannot help; it is there to be
   rejected. Pages of one website are one source (owner decision, 2026-09-24); the same
   rule applies to a manual publish.
3. **Duplicate check.** Jev compares the story with the same category's news published in
   the last 30 days — hand-written articles included — and with other candidates.
   Uncertain goes to review (`news_duplicate_uncertain`), where an editor answers it with
   「不是重複，繼續寫」: the answer is stored as a duplicate assessment for that evidence,
   and the rerun skips Jev.
4. **Draft → verify → translate → locale review**, each a recorded pipeline run. The
   writer and the fact-checker are separate settings; the checker gets a fresh request with
   no authoring trace. Translation is one call per locale. A claim citing a page outside
   the evidence, an impossible event date, a failed fact check or a failed locale review
   stops the candidate with status `needs_redraft`: nothing is saved as an article yet, so
   a new draft or a rejection are the only moves. (A re-verified article that fails again
   goes back to manual review instead, where it can still be edited.)
5. **Images.** A hero, a social card and a diagram per locale are rendered locally (no
   source image is copied). They go to the community S3 bucket when one is configured,
   otherwise into `news_assets.content`; `/guides/news-assets/<file>` serves either.
6. **Hard checks** (summary, FAQ, SVG diagram, topic link, crypto disclaimer, forbidden
   purchase/trading/exploit wording, guide lint) on all five locales. A failure also ends
   in `needs_redraft`; the five-locale article is saved only after this step.
7. **Jev** decides each locale. Evidence is re-fetched; any change sends the candidate to
   review. With every locale approved and the category's gate open, the bundle publishes
   atomically; otherwise it waits in `shadow_review`.

The schemas the model stages send are rewritten by `provider_schema.py` into the subset
OpenAI strict mode and Anthropic structured outputs both accept (every property required,
`anyOf` only, no length/number/array bounds). Pydantic still enforces the full model on the
reply, and the dropped bounds are written into the field descriptions.

## Switching it on

1. **Start the services.** `/root/deploy-travel-scanner.sh` passes only
   `--profile hotspots`. Add `--profile news` to that `up --build -d` call (a host change,
   so the site owner decides). Starting the two services by hand once is not enough: the
   next deploy would rebuild everything else and leave them on the old image.
2. **Keys.** The writer and checker vendors and Jev all need their keys in the admin card
   「AI 供應商與金鑰」 (or the environment). Each candidate spends up to six Jev calls
   (one duplicate check, five locale decisions) from `JEV_DAILY_CALL_BUDGET` (default
   200). When the budget runs out, candidates fall back to manual review rather than
   failing.
3. **Sources.** The reviewed list lives in `apps/api/app/news_automation/sources.json`
   (each entry carries a `note` on why it is there). Load it on the host, dry run first:

   ```bash
   docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.sources_cli
   docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.sources_cli --apply --actor-email <admin email>
   ```

   The dry run validates every source from the host and writes nothing. `--apply` creates
   or updates each source through the same service as `/admin/news` (validation, audit
   row); a source that fails validation is kept, disabled, with the reason. Sources in the
   database but not in the file are listed and left alone, and `/admin/news` can still
   disable or edit any of them. A source is `evidence` or `lead_only` (discovery only,
   never counted as evidence), optionally first-party, and may list redirect hosts and
   parser settings (`items_path`, `article_ids`, `include_path_prefixes`,
   `max_entries_per_scan`, …). The evidence gate needs pages from two websites including
   a first-party one, and the scanner only finds the second page through the article's
   own links, so the list pairs press feeds with the first-party hosts they cite. A link
   is followed only when its host is exactly a source's host: a link to
   `www.microsoft.com` does not reach a source on `blogs.microsoft.com`.
4. **Settings.** Pick the writer and checker from the dropdowns (「預設」 follows the admin
   AI settings; 「自訂…」 accepts any id matching `[A-Za-z0-9._:-]{1,128}`). Turn on
   「啟用掃描」 with mode 「影子模式」. Without the admin page, the host can do the same:
   `python -m app.news_automation.settings_cli` (inside the api container) prints the
   settings, which vendor keys and Jev are configured (present/missing only) and the
   source counts; add `--enable --writer-provider … --verifier-provider …` to see the
   change and `--apply --actor-email <admin>` to make it. It refuses to switch the
   scanner on while the chosen vendors lack a key, either is Gemini, or Jev is missing,
   and never touches mode or auto-publish. Changing a vendor, model or prompt/policy version
   resets every category to shadow mode and restarts its clock.
5. **Shadow period.** Review what arrives. Every publish/reject on a candidate that
   reached Jev counts toward the category's gate: at least 14 days, 50 labelled
   candidates, 95 % agreement with Jev and no major error.
6. **Automatic mode**, per category, only once its gate shows 已達標. Reporting a major
   error on a published candidate turns that category's autopilot off again.

## The review queue

`/admin/news` splits candidates into lists by what a person can do with them. Each list
asks the API for its own statuses, pages 50 at a time and keeps its place in the URL
(`?queue=`, `?page=`). Selecting a candidate shows a 「下一步」 box that says in words what
happened and offers only the buttons that can work for it. Every action takes a reason,
which goes into the audit log; common reasons are one click away.

| List | Statuses | What to do |
| --- | --- | --- |
| 待審查 | `manual_review`, `shadow_review` | Decide. These are the only rows the sidebar badge and the 「等你判斷」 card count. |
| 需重寫 | `needs_redraft`, `failed` | Run one again (a whole new draft, spends model calls) or tick several and reject them. |
| 缺證據 | `needs_evidence` | Reject; a rerun cannot add a second website. |
| 已發布 | `published` | Report a major error if one turns up; that category's autopilot switches off. |
| 已退件 | `rejected`, `duplicate` | Nothing; for reference. |

Inside 待審查:

- `shadow_review` — Jev approved all five locales; only shadow mode kept it from
  publishing. Publish or reject.
- `news_jev_manual` — the article is complete but Jev held at least one locale. Publish,
  fix it in the guide editor and 「重新查核」, or reject.
- `news_duplicate_uncertain` — compare with the five closest known titles shown beside
  it; 「不是重複，繼續寫」 or reject.
- `news_evidence_changed` — reject (see Known limits).
- Any other code on an article that already exists — a re-verification that failed; fix
  it in the guide editor and re-verify, or reject.

Only decisions on candidates that reached Jev (`shadow_review`, `news_jev_manual`,
`news_evidence_changed`) count toward the category's gate; rejecting from 需重寫 or 缺證據
is housekeeping. Rejecting several rows sends one audited reject per candidate, in order;
a row that moved on in the meantime is reported and the rest go through.

## When a job dies

Every deploy restarts the worker, which cuts off the candidate it was working on. When
the news worker starts, every candidate still in `drafting`, `verifying`, `locale_review`
or `jev_review` is marked `failed` with `news_processing_stale` (a `stale-recovery` run is
recorded) and re-queued at once: there is one news worker, so nothing can still be
running. The scheduler applies the same recovery to anything in flight for more than 70
minutes (the job timeout is 60). A candidate is re-queued this way at most twice; after
that it waits for 「重新執行」. Until it is recovered, an interrupted candidate holds a
concurrency slot, and with both slots held every other candidate only defers. A stalled
re-verification keeps its marker, so the rerun re-checks the edited drafts instead of
writing new ones. `discovered` candidates older than two hours are re-queued while the
scanner is enabled.

## Known limits

- A candidate held with `news_evidence_changed` cannot be published or rerun into
  shape: stored evidence hashes are never refreshed, so every attempt finds the same
  change. Reject it; later coverage arrives as a new candidate.

- Gemini cannot yet serve as writer or checker: the shared `gemini_response_schema`
  keeps only the first option of an `anyOf`, which collapses the block union.
- Evidence is compared by the hash of the extracted page text. A page whose extracted
  area carries changing text (view counters, "related" lists) will look changed at
  publication; narrow it with the source's `article_ids`/`article_classes`.
