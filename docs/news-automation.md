# AI hourly news automation

`apps/api/app/news_automation` finds news on allow-listed sources every hour, drafts a
Traditional Chinese article from the evidence, has a second model check it, translates it
into the other four site languages, has a third model (the final editor) check every locale
against the evidence, asks Jev whether each locale is ready, and then publishes it or parks
it for review.
Everything ships switched off. This page is the order in which to switch it on and what
each switch does.

## The moving parts

| Piece | Where | What it does |
| --- | --- | --- |
| `news-scheduler` | compose profile `news`, `app.news_automation.scheduler` | Once a minute: queues a scan for every due source, fails candidates whose job died (see below), re-queues orphaned ones, queues the daily retention cleanup |
| `news-worker` | compose profile `news`, `app.news_automation.worker` | The only consumer of the `news` RQ queue: one container running a pool of `NEWS_WORKER_PROCESSES` RQ workers (default 3). The admin's global and per-vertical concurrency still decide how many candidates run at once. Run exactly one such container, because it fails every in-flight candidate when it starts. The general `worker` does not read the queue, so a candidate's hour of model calls never blocks search or trip routing |
| `/admin/news` | web | Sources, settings, the review queue, runs, and the per-category auto-publish switches with Jev's agreement figures |
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
   A first-party page that *refuses* the scanner (HTTP 401 or 403: `openai.com/index/*`
   answers every request with a Cloudflare challenge) is not skipped forever when its entry is
   dated within
   the last 72 hours and the feed carries a summary: it becomes a candidate in
   `needs_evidence` (`news_page_refused`) holding that summary as its only `lead_only`
   evidence. Nothing is drafted from it; it is there so the story shows up in the review
   queue, to be written by hand from the publisher's other pages or rejected. Before this
   (2026-09-30), every OpenAI announcement was skipped every hour and never seen.
   Such a story does not wait for a person when a later scan reads a page from an
   `evidence` source that links to it (a press report linking to the refused announcement,
   compared without query string, fragment or trailing slash): that page and the evidence
   linked from it are attached to the waiting candidate, which goes back to `discovered`
   and is queued, and the report itself is closed as `duplicate`
   (`news_attached_as_evidence`) instead of filing the same story twice. This applies to
   any candidate in `needs_evidence`, including one that had only `lead_only` pages.
   A source with `evidence_from_feed_summary` (the Claude Platform release notes, whose
   entries all link to anchors on one page) is not fetched page by page: each entry's feed
   summary is its evidence, its anchor URL the canonical URL, and revalidation and
   「用最新來源重新查核」 read the entry from the feed again. A URL of that site the feed does
   not list (an aged-out entry, a page linked from another source) is read as a page.
   A source whose dated entries of the last week keep failing for more than six hours is
   reported `stuck` instead of `partial` (the note names those URLs first); `/admin/news`
   lists stuck sources first under a warning, so a publisher that starts refusing the
   scanner is noticed the same day.
   **Old entries.** Each source has a freshness window, `max_entry_age_hours` in its config
   (72 hours unless set; `0` or `null` switches it off, and a value that is not a number
   keeps 72). A source's **first scan** (`last_scanned_at` empty) records every listed
   entry older than the window (72 hours when it is off), or undated, as seen (`rejected`,
   `news_baseline`) without fetching it, so adding a source files only its news of the
   last days, never its back catalogue. On every later scan a dated entry older than the
   window is left out before its page is fetched: no request, no candidate, nothing
   stored, so switching the window off or widening it reads it after all. Those entries are
   counted in the source's note ("Left out 3 feed entries older than 72 hours, without
   fetching them") but do not make the scan `partial` or keep the listing's ETag back:
   `partial` still means a page failed. Before this (2026-10-02) an old entry that reached
   the scanner (a republished post, a renamed URL, a page that failed until now) became a
   candidate like a new one; the switch-on on 2026-09-24 filed 87 candidates from the first
   three sources, most of them old posts.
   **Undated entries** (HTML listings, a feed item without a date) are judged by the
   listing instead: the first scan records them as seen, and after that an undated entry
   is one the listing did not show before, so it is read as new. Reading the article's own
   date after the fetch was the other option; it was not taken because it cannot save the
   request and would need a date extractor per publisher.
   Every fetch uses `fetch.tls_context()`: it verifies the chain, the expiry and the host
   name, but not Python 3.13's strict X.509 profile, which the TWCA chain of Taiwan's
   government sites fails ("Missing Subject Key Identifier"). Before this no `gov.tw` page
   could be read at all. Listings can be narrowed with `include_query_contains` (sites that
   serve every page from one script, like the FSC's `/ch/home.jsp`) and
   `include_title_keywords` (a publisher mostly outside the three verticals).
2. **Evidence gate.** At least one page from an evidence source (owner decision,
   2026-09-25: every enabled source is an official or trusted feed, and a person confirms
   each story before it is translated). Only a candidate with nothing but `lead_only` pages
   stops before any model call, with status `needs_evidence`. *Automatic* publication
   needs two websites (host without `www.`) or a first-party page (owner decision,
   2026-09-25: a company's own announcement may go out on its own, reported as its
   statement).
3. **Duplicate check.** Jev compares the story with the same category's news published in
   the last 30 days — hand-written articles included — and with other candidates.
   Uncertain goes to review (`news_duplicate_uncertain`), where an editor answers it with
   「不是重複，繼續寫」: the answer is stored as a duplicate assessment for that evidence,
   and the rerun skips Jev.
4. **Stage one: Traditional Chinese draft.** The writer drafts in Traditional Chinese
   (and may declare the story not newsworthy: marketing, event recaps, rumours, hiring).
   With a single source it must attribute every claim to that organisation. The
   fact-checker, in a fresh request with no authoring trace, checks it against the
   evidence; a claim citing a page outside the evidence, an impossible event date or a
   failed check stops it with status `needs_redraft`. Jev then answers once, about the
   zh-TW draft only (`would_publish`). The candidate waits in manual review as
   `news_zh_draft_ready` with only the zh-TW draft stored; nothing is translated, drawn
   or saved as an article. The writer's slug is kept on its `draft` pipeline run.
5. **The owner confirms** with 「確認發布，翻譯其他語言」 (`POST …/approve`): a human
   `publish` decision and assessment, an audit row, and the candidate is queued again.
6. **Stage two: translate, final edit, check, Jev's last call, publish.** One
   translation call per locale and a locale review of each. Then the final editor
   (`editor_provider`/`editor_model`, default Claude Opus 5.5) reads each of the five
   locales with the evidence and the verified zh-TW text (`final-edit-<locale>` runs). It
   makes the text clear for general readers, removes notes meant for editors, and may not
   add a fact; it passes a locale, returns a corrected one (kept, with the sources locked
   to the evidence, and recorded as that locale's review, and as the zh-TW verification
   when it is zh-TW), or holds it as `news_final_edit_hold`. Then images (a hero, a social
   card and a diagram per locale, rendered
   locally, stored in S3 or `news_assets.content`), hard checks on all five locales
   (summary, FAQ, SVG diagram, topic link, crypto disclaimer, forbidden
   purchase/trading/exploit wording, guide lint, at least one source website), and the
   article is saved. **Jev's last call** (`jev-final`) asks about all five saved locales;
   only `act` on every one publishes, through the same checks as the publish button
   (`service.publication_bundle`): evidence re-fetched and unchanged, verification and
   locale reviews matching the current text. Anything else waits as
   `news_jev_final_hold`, and a Jev quota that ran out counts as anything else. Both holds
   keep the saved article, so 「五語發布」 still publishes it as a person's decision. A
   failed locale review keeps the confirmation and waits in manual review for
   「重新翻譯並發布」. A failed hard check saves the article too, unpublished, and waits in
   manual review as `news_hard_checks_failed` with each locale's problems in the lint, so
   an editor fixes it in the guide editor and presses 「重新查核」 instead of paying for a
   new draft; Jev's last call is not asked, and the publish button refuses it until the
   checks pass. Changed evidence waits for 「用最新來源重新查核」 (below).
7. **Automatic mode** skips step 5 when auto-publish is on for the category, Jev answered
   `act` for the zh-TW draft, and the evidence is two websites or a first-party page;
   anything else waits for a person. There is no shadow gate any more (owner decision,
   2026-09-25, knowing that Jev publishes no accuracy figures for CJK text): the final
   editor and Jev's last call guard every article. A candidate uses up to seven Jev calls
   (duplicate check, zh-TW draft, five locales) from `JEV_DAILY_CALL_BUDGET`.

An edited article (「重新查核」 in the guide editor) runs the fact check, the locale reviews
and the hard checks again on the editor's text, but neither the final editor nor Jev's last
call: a person's edits are not rewritten. A confirmed one then publishes, an unconfirmed
one waits as `news_ready_to_publish` for 「五語發布」.

The schemas the model stages send are rewritten by `provider_schema.py` into the subset
OpenAI strict mode and Anthropic structured outputs both accept (every property required,
`anyOf` only, no length/number/array bounds). Pydantic still enforces the full model on the
reply, and the dropped bounds are written into the field descriptions.

## Switching it on

1. **Start the services.** `/root/deploy-travel-scanner.sh` has passed `--profile news`
   to its `up --build -d` call since 2026-09-24, beside `--profile hotspots` and
   `--profile video`, so an ordinary deploy starts both services and rebuilds them with
   everything else. The script is not in git; when in doubt, run
   `grep -- --profile /root/deploy-travel-scanner.sh` on the host. Starting the two
   services by hand once is not enough: the next deploy would rebuild everything else and
   leave them on the old image.
2. **Keys.** The writer and checker vendors and Jev all need their keys in the admin card
   「AI 供應商與金鑰」 (or the environment). Each candidate spends up to two Jev calls
   (the duplicate check and the zh-TW draft) from `JEV_DAILY_CALL_BUDGET` (default 200).
   When the budget runs out, the duplicate check answers "uncertain" and the candidate
   waits in manual review rather than failing. Claude needs no key when the owner sets
   「Claude 連線方式」 on that card to 訂閱帳號: every stage then runs on the Claude
   subscription accounts signed in at `/admin/ai-accounts`, through the host agent that
   the news-worker reaches over its socket (`app/ai/subscription.py`). A stage waits up to
   two minutes for a busy account. There is no usage cap (the owner's choice of
   2026-09-26): the accounts take turns A, B, C and back to A, and one is left only when its
   5-hour or weekly window is full. When every account is full, the stage falls back to
   MiniMax, and its run records MiniMax's model.
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
   `max_entries_per_scan`, `max_entry_age_hours`, …). Every source in the file keeps the
   72-hour window; raise it only for a feed that adds posts days after their own date.
   One evidence page is enough to draft; automatic
   publication needs a second website, which the scanner only finds through the article's
   own links, so the list pairs press feeds with the first-party hosts they cite. A link
   is followed only when its host is exactly a source's host: a link to
   `www.microsoft.com` does not reach a source on `blogs.microsoft.com`.
4. **Settings.** Pick the writer, checker and final editor from the dropdowns (「預設」
   follows the admin AI settings; 「自訂…」 accepts any id matching `[A-Za-z0-9._:-]{1,128}`).
   Turn on 「啟用掃描」. Without the admin page, the host can do the same:
   `python -m app.news_automation.settings_cli` (inside the api container) prints the
   settings, which vendor keys and Jev are configured (present/missing only) and the
   source counts; add `--enable --writer-provider … --verifier-provider …
   --editor-provider …` to see the change and `--apply --actor-email <admin>` to make it.
   It refuses to switch the scanner on while a chosen vendor cannot be called, one is
   Gemini, or Jev is missing, and never touches mode or auto-publish. Changing a vendor,
   model or prompt/policy version restarts the agreement figures; it no longer switches
   auto-publish off.
5. **Automatic mode.** Set the mode to 「自動模式」 and tick 「自動發布」 for each category.
   From then on a candidate that passes every stage publishes itself; the rest wait in the
   review queue. The agreement figures on each card (days, labelled candidates, agreement
   with Jev) are for reference only. Reporting a major error on a published candidate
   turns that category's auto-publish off again.

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
| 缺證據 | `needs_evidence` | Reject; only lead-only pages, nothing a draft could cite. |
| 已發布 | `published` | Report a major error if one turns up; that category's autopilot switches off. |
| 已退件 | `rejected`, `duplicate` | Nothing; for reference. |

Inside 待審查:

- `news_zh_draft_ready` — a verified Traditional Chinese draft; the preview shows zh-TW
  only, with Jev's answer and the gate's progress. 「確認發布，翻譯其他語言」, 「重新執行」
  for a new draft, or reject.
- `news_duplicate_uncertain` — compare with the five closest known titles shown beside
  it; 「不是重複，繼續寫」 or reject.
- Confirmed, then a locale review stopped it — 「重新翻譯並發布」 or reject.
- `news_hard_checks_failed` — the five-locale article is saved but unpublished; the lint
  lists each locale's problems. Fix it in the guide editor (links in the preview) and
  「重新查核」, or reject. A confirmed one publishes once the edited article passes; an
  unconfirmed one then waits as `news_ready_to_publish`. Until task
  2026-10-02-offer-re-verify-on-news-articles lands, the page offers 「重新查核」 only on
  unconfirmed ones; a confirmed one shows 「重新翻譯並發布」, which translates again over
  the edits.
- `news_ready_to_publish` — an edited, re-verified article nobody has confirmed yet;
  「五語發布」 or reject.
- `news_evidence_changed` — a source page changed after the check, so the old check
  cannot publish it. 「用最新來源重新查核」 (`POST …/refresh-evidence`) fetches every
  evidence page again under the same host and source rules. The fetch sends no ETag, so a
  stale one cannot hide the change. The current text replaces the stored excerpt and hash,
  but only when every page reads; otherwise nothing changes and the error names the page.
  An earlier "not a duplicate" answer carries over to the new evidence. The saved
  five-locale article then runs as `news_evidence_refreshed`: the fact check, the locale
  reviews and Jev's last call run again on the new text. The story publishes on its own
  when it may (the automatic-mode rules), or when the owner already confirmed it and Jev
  acts on every locale; otherwise it waits as usual. Reject it if you do not want it.
- `shadow_review`, `news_jev_manual` — candidates from before 2026-09-25 that went
  through the old five-locale stage; publish or reject.

Only decisions on candidates Jev assessed count toward the category's gate (stage-one
drafts and the older five-locale holds): confirming a draft is a publish decision,
rejecting it a reject. Rejecting from 需重寫 or 缺證據 is housekeeping. Rejecting several
rows sends one audited reject per candidate, in order; a row that moved on in the
meantime is reported and the rest go through.

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

## When every subscription account is full

With 「Claude 連線方式」 set to 訂閱帳號, the AI vendors card's 「訂閱帳號都滿時」
(`ai_subscription_fallback`) decides what a call does when every account is full:

- 「改用 MiniMax」 (`minimax`, the default) runs it on MiniMax at once.
- 「等帳號恢復」 (`wait`) is the owner's choice of 2026-09-26. A news candidate goes back to
  `discovered` as `news_subscription_paused`, or keeps its re-verify marker, and its job
  tries again 30 minutes later (`jobs.PAUSE_MINUTES`). The accounts take turns A → B → … →
  A, each used until it is full.

## When Jev's daily budget is spent

Jev is limited to `jev_daily_call_budget` calls per UTC day (200 in production). When the
budget is spent at the duplicate check, the candidate goes back to `discovered` as
`news_jev_quota_paused` instead of waiting in the review queue as an uncertain duplicate;
nothing is uncertain about the story. The orphan sweep skips it until 00:00 UTC (08:00 in
Taipei) and then queues it again, 20 a minute, so each day runs as many as that day's budget
allows and the rest pause again. Raising the budget in the admin during the day that spent it
does not wait for 00:00 UTC: every minute the scheduler compares today's count with the saved
budget, and while there is room the sweep queues the paused candidates at once. A check that did reach Jev and came back between 0.25 and
0.85 still waits for an editor. Later Jev stages keep their holds: a spent budget at the Jev
final gate is `news_jev_final_hold`, which the owner can publish from.

## Backfilling stories stopped by old rules

`python -m app.news_automation.backfill_cli --since YYYY-MM-DD` (inside the api container)
lists the candidates published since that day that stopped for a reason the pipeline no
longer applies:

- evidence from one website (the rule until 2026-09-25);
- a failed MiniMax check, translation or hard check;
- a claim citing a page outside the evidence.

Stories with a first-party page come first, since only those may publish on their own.
Rejections for editorial reasons are not in the list. Add `--apply --actor-email <admin>`,
and optionally `--limit N`, to reopen them as new drafts, with an audit row each, and queue
them. The current pipeline then decides each one, including the owner's confirmation for a
story that may not go out on its own.

`--jev-quota-holds` takes the uncertain-duplicate holds whose latest duplicate check never
reached Jev because its budget was spent (207 on 2026-09-26). With `--apply` they are marked
`news_jev_quota_paused` rather than queued, and start after the next 00:00 UTC.

## Known limits

- Gemini as writer or checker has not been tried against the live API. The shared
  `gemini_response_schema` used to keep only the first option of an `anyOf`, which told
  Gemini every block was a heading; it now sends all 13 block types as an `anyOf`. The
  settings CLI still refuses Gemini until one live stage shows the API accepts that
  schema (task 2026-10-02-confirm-a-live-gemini-news-stage).
- Evidence is compared by the hash of the extracted page text. A page whose extracted
  area carries changing text (view counters, "related" lists) will look changed at
  publication; narrow it with the source's `article_ids`/`article_classes`.
- The freshness window trusts the feed's date. The parser takes the first of `published`,
  `updated`, `pubDate` or `date` it finds, and an `updated` date (or a post republished
  with a new date) can be newer than the event, so the window is not a freshness guard for
  the writer. An undated listing that renames its article URLs makes every listed entry
  look new.
