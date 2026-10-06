# AI hourly news automation

`apps/api/app/news_automation` finds news on allow-listed sources every hour, drafts a
Traditional Chinese article from the evidence, has a second model check it, translates it
into the other four site languages, has a third model (the final editor) check every locale
against the evidence, asks Jev whether each locale is ready, and then publishes it or parks
it for review. A parked story can be decided by one more model in the owner's place, the
review judge (owner decision, 2026-10-06).
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
   Only a page from an enabled `evidence` source is attached, fetched under the same host
   allow-list and SSRF checks as every other page; a `lead_only` site's page never is. It
   is attached once: the next scan finds the report already seen and does nothing, and a
   later report linking to a story that has left `needs_evidence` files its own candidate.
   Since the owner's decisions of 2026-09-25 (one evidence page drafts; a first-party page
   publishes on its own) and 2026-09-28 (so does a page from a trusted newsroom), a
   first-party candidate no longer waits for a second site, so nothing attaches one to a
   candidate already drafting. Matching a page to a story by event rather than by link
   (through Jev) is not built; both wait on an owner decision (task
   `2026-10-06-match-news-evidence-by-event`).
   A source with `evidence_from_feed_summary` (the Claude Platform release notes, whose
   entries all link to anchors on one page) is not fetched page by page: each entry's feed
   summary is its evidence, its anchor URL the canonical URL, and revalidation and
   「用最新來源重新查核」 read the entry from the feed again. A URL of that site the feed does
   not list (an aged-out entry, a page linked from another source) is read as a page.
   A source whose dated entries of the last week keep failing for more than six hours is
   reported `stuck` instead of `partial` (the note names those URLs first); `/admin/news`
   lists stuck sources first under a warning, so a publisher that starts refusing the
   scanner is noticed the same day. The `/admin` dashboard's News card counts them too
   (`news_sources_stuck` in the operations pending counts), in red when there are any and
   linked to `/admin/news?tab=sources`; a stuck source is an incident, not a review, so it
   stays out of the Pending total. A switched-off source keeps its last status but is not
   scanned, so neither count includes it. The six hours are `STUCK_AFTER` in
   `scanner.py`, a code constant rather than a per-source setting. Nothing tells the owner
   outside the admin yet: the only senders (community SMTP and LINE push) write to users,
   and a daily summary waits on the owner choosing a channel.
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
   each story before it is translated; since 2026-10-06 the review judge may confirm in
   the person's place, step 8). Only a candidate with nothing but `lead_only` pages
   stops before any model call, with status `needs_evidence`. *Automatic* publication
   needs two websites (host without `www.`) or a first-party page (owner decision,
   2026-09-25: a company's own announcement may go out on its own, reported as its
   statement).
3. **Duplicate check.** Jev compares the story with the same category's news published in
   the last 30 days — hand-written articles included — and with other candidates.
   Uncertain goes to review (`news_duplicate_uncertain`), where an editor answers it with
   「不是重複，繼續寫」: the answer is stored as a duplicate assessment for that evidence,
   and the rerun skips Jev. The review judge's "not a duplicate" (step 8) is honoured the
   same way.
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
   when it is zh-TW), or holds it as `news_final_edit_hold`. Then images (a hero and a
   social card, rendered locally, stored in S3 or `news_assets.content`), hard checks on
   all five locales (summary, FAQ, topic link, crypto disclaimer, forbidden
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
   The fixed editorial-process diagram was removed by owner decision on 2026-09-30;
   a candidate processed again loses that old figure. Publication does not require it.
7. **Automatic mode** skips step 5 when auto-publish is on for the category, Jev answered
   `act` for the zh-TW draft, and the evidence is two websites or a first-party page;
   anything else waits in the review queue, for a person or, with AI review on, for the
   review judge (step 8). There is no shadow gate any more (owner decision,
   2026-09-25, knowing that Jev publishes no accuracy figures for CJK text): the final
   editor and Jev's last call guard every article. A candidate uses up to seven Jev calls
   (duplicate check, zh-TW draft, five locales) from `JEV_DAILY_CALL_BUDGET`. Each rewrite
   the review judge orders (at most two per story) asks the first two again.

   **What `act` means.** Both Jev questions about a draft (the zh-TW one in step 4 and the
   last call in step 6) ask one statement, `ai.PUBLISH_QUESTION`, with no criteria, and
   `act` is a probability of yes at or above `jev_act_confidence` on `/admin/news`.
   Production acts at about 0.5. Jev's answer to this statement has not gone above 0.78 since
   2026-09-24, so 0.9, the default, would never publish. The criteria are left out on
   purpose. Until 2026-10-05 they went out under keys Jev ignores. When #1218 sent them under
   the documented `true`/`false` keys, "Any condition fails or is uncertain" lowered every
   answer by 0.10–0.21, and no draft reached the threshold. That was measured with 21
   production calls on 2026-10-06 (`tasks/done/2026-10-06-news-jev-publish-confidence-fell-below.md`).
   Adding criteria back changes the meaning of the threshold; measure it before doing so.
8. **The review judge** (owner decision, 2026-10-06; `judge.py`). With 「待審查與需重寫交給
   AI 判斷」 on, a story that comes to rest in a hold is put to one more model
   (`judge_provider`/`judge_model`, default Claude Opus 5.5), which answers that hold once
   in the owner's place: publish, reject, send back for a rewrite, or hand back to the
   owner with reasons. The run that left the story in the hold queues the judge for it
   (`jobs.run_judge`, on the same `news` queue); nothing sweeps the lists. The judge is
   shown what the admin detail page shows: the hold and its explanation, the evidence, the
   claims, the text and the check records. It acts only while the scanner, automatic mode,
   that category's auto-publish and its own switch are all on, and the four are read again
   once the model has answered. "The review queue" below lists the holds it answers and
   what each answer does. Three of its answers send the story back through the stages
   above. "Not a duplicate" does what the editor's button in step 3 does; the other two
   are its own:

   - **An approved draft.** Approving a `news_zh_draft_ready` draft takes the place of
     step 5 and of nothing else. The candidate goes back to `discovered` as
     `news_judge_approved` and runs step 6 from the stored draft: the final editor, the
     translations and their reviews, the images, the hard checks, **Jev's last call** and
     the publish button's checks all still run, and any of them can stop the story in a
     new hold. Only stage one is not repeated: no new draft, fact check, duplicate check or
     zh-TW Jev question. The approval counts only while it is the judge's newest verdict,
     was given on the current evidence, and the stored draft still matches its passing fact
     check; otherwise the marker is dropped and the story is drafted afresh. The switches
     are read once more just before publication: if one was turned off while stage two
     ran, the finished article waits as `news_ready_to_publish` for 「五語發布」. The
     publication is recorded without a person: no `human_decision`, an audit row
     `news_candidate_judge_published`, and `judge`, `judge_model` and `judged_stage` in
     the article's automation metadata.
   - **A rewrite with directions.** For a draft stopped in the redraft list the judge may
     write directions, each one change for the writer: drop, narrow, attribute or correct
     something. The candidate goes back to `discovered` as `news_judge_redraft` and is
     drafted again with the directions in the writer's payload as `revision_notes`, which
     the writer is told are data, never instructions, and add no fact or source. The
     `draft` run records which verdict steered it (`judge_notes`). The new draft meets
     every check of steps 3 and 4 again and then goes on as any draft does: out through
     step 7 when that applies, otherwise to `news_zh_draft_ready`, which the judge reads
     as a new hold. A story is rewritten on the judge's directions at most twice. If the
     writer answers such a rewrite by declaring the story not newsworthy, it rests in the
     redraft list as `news_not_eligible` instead of being rejected, marked as handed back
     (「AI 交回」): two models disagree, so the owner decides.

An edited article (「重新查核」 in the guide editor) runs the fact check, the locale reviews
and the hard checks again on the editor's text, but neither the final editor nor Jev's last
call: a person's edits are not rewritten. A confirmed one then publishes, an unconfirmed
one waits as `news_ready_to_publish` for 「五語發布」, or for the review judge.

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
   「AI 供應商與金鑰」 (or the environment). Each candidate spends up to seven Jev calls
   (the duplicate check, the zh-TW draft and the five locales of Jev's last call) from
   `JEV_DAILY_CALL_BUDGET` (default 200), and the first two again for each rewrite the
   review judge orders. When the budget is spent at the duplicate check,
   the candidate goes back to `discovered` as `news_jev_quota_paused` and runs again when
   the budget has room (see "When Jev's daily budget is spent"). Claude needs no key when
   the owner sets 「Claude 連線方式」 on that card to 訂閱帳號: every stage then runs on the
   Claude subscription accounts signed in at `/admin/ai-accounts`, through the host agent that
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
   The review judge's model (「代審模型」, default Claude Opus 5.5) is picked beside those
   three; it is only called while AI review is on (step 6), and a model other than the
   writer's is the better choice.
   Turn on 「啟用掃描」. Without the admin page, the host can do the same:
   `python -m app.news_automation.settings_cli` (inside the api container) prints the
   settings, which vendor keys and Jev are configured (present/missing only) and the
   source counts; add `--enable --writer-provider … --verifier-provider …
   --editor-provider …` to see the change and `--apply --actor-email <admin>` to make it.
   It refuses to switch the scanner on while a chosen vendor cannot be called, one is
   Gemini, or Jev is missing, and never touches mode or auto-publish. `--judge-provider`,
   `--judge-model` and `--judge-enable`/`--judge-disable` set the judge the same way; its
   vendor is held to the same test only while its switch is on. A vendor changed without
   naming a model puts that role's model back to the new vendor's default, as the admin
   page does: the stored id belongs to the vendor being left. Changing a vendor,
   model or prompt/policy version restarts the agreement figures; it no longer switches
   auto-publish off. A change of judge restarts nothing: the figures measure the three
   roles every story runs through.
5. **Automatic mode.** Set the mode to 「自動模式」 and tick 「自動發布」 for each category.
   From then on a candidate that passes every stage publishes itself; the rest wait in the
   review queue. The agreement figures on each card (days, labelled candidates, agreement
   with Jev) are for reference only. Reporting a major error on a published candidate
   turns that category's auto-publish off again.
6. **AI review.** Optional, and off as shipped (`judge_enabled`). Tick 「待審查與需重寫交給
   AI 判斷」 on the settings tab; the box is disabled outside automatic mode, and the
   judge's vendor needs a key like the others. From then on a story that comes to rest in
   a hold the judge answers is judged once, in every category whose auto-publish is on. A
   category whose auto-publish is off, or was switched off by a major-error report, is
   left to the owner. Stories that were already waiting, or that arrive while one of the
   switches is off, are not picked up when it comes on: release them in batches with the
   backlog flags (see "Backfilling stories stopped by old rules"). While the switch is off
   no story is put to the judge, and a settings save from a page loaded before the judge
   existed keeps the stored switch and model.

## The review queue

`/admin/news` splits candidates into lists by what a person can do with them. Each list
asks the API for its own statuses, pages 50 at a time and keeps its place in the URL
(`?queue=`, `?page=`). Selecting a candidate shows a 「下一步」 box that says in words what
happened and offers only the buttons that can work for it. Every action takes a reason,
which goes into the audit log; common reasons are one click away.

| List | Statuses | What to do |
| --- | --- | --- |
| 待審查 | `manual_review`, `shadow_review` | Decide. These are the only rows the sidebar badge and the 「等你判斷」 card count. With AI review on, the review judge answers most arrivals first (see "With AI review on"). |
| 需重寫 | `needs_redraft`, `failed` | Run one again (a whole new draft, spends model calls) or tick several and reject them. With AI review on, the judge answers `needs_redraft` arrivals first; `failed` rows are never put to it. |
| 缺證據 | `needs_evidence` | Reject; only lead-only pages, nothing a draft could cite. |
| 已發布 | `published` | Report a major error if one turns up; that category's autopilot switches off. |
| 已退件 | `rejected`, `duplicate` | For reference. A row the judge closed (badge 「AI 結案」) can be taken back with 「拿回來自己判斷」. |

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
meantime is reported and the rest go through. What the review judge decides is not a
person's decision and counts toward no gate.

### With AI review on

While the scanner, automatic mode, the category's auto-publish and 「待審查與需重寫交給 AI
判斷」 are all on, the run that leaves a story in one of the holds below queues the review
judge for it (step 8 above). The story stays in its list, and in the counts, until the
answer moves it. Each hold is answered once. When the candidate runs again the answer is
cleared, so whatever stops it next is a new hold.

| Hold | The judge may answer | What the answer does |
| --- | --- | --- |
| `news_zh_draft_ready` | publish, reject, hand back | Publish runs stage two as 「確認發布，翻譯其他語言」 does, under the marker `news_judge_approved` (step 8). The judge is told to leave small wording problems to the final editor. |
| `news_duplicate_uncertain` | not a duplicate, duplicate, hand back | It is shown the ten closest known titles. "Not a duplicate" does what 「不是重複，繼續寫」 does, and the rerun honours it instead of asking Jev. "Duplicate" closes the story as `duplicate`. |
| `news_jev_final_hold`, `news_ready_to_publish` | publish, reject, hand back | It reads the Traditional Chinese text and the locales Jev held; the other locales passed their own checks on the text that is saved. A check's record is shown to it only while it describes the saved text: after an edit and 「重新查核」, the final editor's record of the edited locale and Jev's earlier last call are left out. Publish goes through the same checks as 「五語發布」 and applies only while all five saved locales are as they were when it read. It cannot edit: it is told to hand back a factual error it finds, naming the locale and the sentence. |
| `news_final_edit_hold` | reject, hand back | Never publish. The final editor holds only for a claim the evidence does not support, conflicting sources or unsafe content, and the judge cannot fix the text. A locale edited since the final editor read it is shown as held too. A story a person confirmed is not put to the judge in this hold: it could neither publish nor close it. |
| In 需重寫: `news_verification_failed`, `news_claim_source_invalid`, `news_event_date_invalid`, `news_locale_review_failed` | rewrite, reject, hand back | Rewrite sends the story back to the writer with directions, under the marker `news_judge_redraft` (step 8). |

The rest stay with the owner and are never put to the judge, because they need work or a
person's own call rather than a judgement:

- In 待審查: `news_hard_checks_failed` (an article to fix), `news_evidence_changed` (the
  re-check button), a confirmed story that a locale review or the fact check stopped
  (「重新翻譯並發布」), and the old `shadow_review` and `news_jev_manual` rows.
- Also in 待審查: a story that already has its article and was stopped when that article
  was checked again, by the fact check, a locale review or the event-date check
  (`news_verification_failed`, `news_locale_review_failed`, `news_event_date_invalid`).
  Nobody need have confirmed it. Fix the article in the guide editor and press 「重新查核」.
- Also in 待審查: a confirmed story the final editor held (`news_final_edit_hold`). The
  judge may not publish what the final editor held and may not close what a person
  confirmed, so there is nothing for it to decide and it is not asked.
- In 需重寫: `failed` rows; `news_not_eligible` (the writer declined a rewrite the judge
  had ordered); `news_hard_checks_failed` rows from before #1136, which
  `--resume-saved-bundles` is for; and a story that has a saved article or a person's
  decision on it.
- In either list: a story whose evidence excerpts the 90-day retention cleanup has
  cleared. Nothing is left to read a draft or an article against, or to write from.
- Everything in 缺證據.

What holds whatever the model answers:

- **A person wins.** The model is asked without a lock, since a call takes minutes.
  Afterwards the row is locked and compared with what the judge was shown: status, hold,
  evidence, retry count, a person's decision and the judge's own mark. If you pressed a
  button meanwhile, the story ran again, or one of the four switches is now off, the answer
  is dropped and nothing is recorded but the run: stage `judge-zh-draft`,
  `judge-duplicate`, `judge-final` or `judge-redraft` on the runs tab, whose stored
  metadata says `dropped`. A publish answer is also tied to the text: the draft, or all
  five saved locales, must still be what the judge read. For a finished article the
  switches are read once more after the publish checks, which fetch every evidence page
  again and can take minutes.
- **It never writes a person's decision.** `human_decision`, `human_reason` and
  `human_major_error` stay as they are and no `human` assessment is added. The verdict is
  an assessment of its own (「AI 代審」: the model that answered, the verdict and the reasons
  in Traditional Chinese) with an audit row `news_candidate_judged`; a publication adds
  `news_candidate_judge_published`.
- **It never closes a story a person confirmed.** "Reject" and "duplicate" are not offered
  there, and become a hand-back if the model returns one.
- **A publication passes the publish button's checks.** If they refuse it, the story is
  handed back with the refusal as the first reason. When the refusal is changed evidence
  the story moves to `news_evidence_changed`, where 「用最新來源重新查核」 is offered; the
  judge's reasons are then in the 判斷紀錄 table rather than the 「下一步」 box.
- **Text from the old flow is not overwritten.** Where a story holds five stored locales
  and no article, "not a duplicate" and "rewrite" become a hand-back, since either would
  start a new draft over that text. So does "not a duplicate" on a confirmed draft that has
  no article yet.
- **Failures end with the owner, not in a loop.** A reply that fails validation, or an
  input over the stage's size limit, is handed back at once. Any other failed call is
  tried again 30 minutes later, and the third failure for the same hold is handed back.
  Only a call that could not start because no subscription account was free (all full,
  busy or signed out) waits without a limit, since nothing ran. A hold with nothing to
  judge (no verified draft, no saved article) is handed back without a call.

What the owner sees. A row the judge read and left carries the badge 「AI 交回」 in 待審查
and 需重寫. Its 「下一步」 box shows the verdict, the model and the reasons, and the 需重寫
hint counts such rows (「其中 N 筆是 AI 看過後交回給你的」). A hand-back changes nothing
else: the row keeps its hold and every button it had. A rewrite the judge ordered and the
writer declined (`news_not_eligible`) carries the badge and is counted the same way. A row
without the badge has not been judged: it arrived before AI review was on or while a
switch was off, it is one the judge never takes (above), or its judge job was lost (see
"Known limits").

A story the judge rejected or closed as a duplicate moves to 已退件 with the badge
「AI 結案」 and keeps the hold it was closed in. 「拿回來自己判斷」 (`POST …/reopen`) returns
it to the list it came from, under that hold, with the judge's reasons still shown. Taking
a story back decides nothing and queues nothing: it writes an audit row
(`news_candidate_reopened_by_owner`) with your reason and leaves `human_decision` empty.
The hold stays marked as answered, so the judge does not take it up again. Only a row the
judge closed and no person has decided can be taken back. One a person rejected, or one
the duplicate check itself closed, stays closed (`news_candidate_not_reopenable`).

**In 需重寫** the judge decides for a story that has nothing but its evidence. Its
directions for a rewrite are the reasons of its verdict (at most eight are kept, 400
characters each), and besides the evidence they are all the writer is given: the failed
draft's text is not kept. A rewrite without directions, or with directions that would push
the writer's input over the stage limit, is handed back instead. A story gets at most two
rewrites on the judge's directions over its whole life, whatever happens to its evidence;
when a twice-rewritten story is stopped again, it is handed back without a model call. A
failed locale review is answered with a whole rewrite too (see "Known limits"). What rests
in the list afterwards is the owner's: rows handed back (badged, with reasons),
`news_not_eligible` rows where the writer declined the judge's rewrite (badged too), and
the rows the judge never takes. 「重新執行」 on any of them is your own order for a whole
new draft, without directions.

**One website that is neither first-party nor trusted.** From 2026-09-25 such a story
always waited for a person's 「確認發布，翻譯其他語言」. The owner repealed that for judged
stories on 2026-10-06: the judge may approve it, and is told how many websites the evidence
comes from and whether one of them is first-party or a newsroom the owner trusts to stand
alone (`auto_publish_alone` in the source's config). The automatic path of step 7 is
unchanged and still never publishes such a story by itself (`policy.auto_evidence_ok`). A
person is still needed for it in three cases:

- AI review does not apply to the story: its switch, automatic mode or that category's
  auto-publish is off, or the story was already waiting and has not been released from the
  backlog.
- The judge hands it back.
- After the judge's approval, stage two stops it where the judge cannot publish: failed
  hard checks, changed evidence, or a hold by the final editor.

The article must still attribute every claim to that one organisation; the writer, the
fact checker and the final editor are told so as before.

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
writing new ones. The review judge's two markers are kept the same way: under
`news_judge_approved` the rerun still translates the approved draft, and under
`news_judge_redraft` it still drafts with the judge's directions, as long as the verdict
behind the marker stands. `discovered` candidates older than two hours are re-queued while
the scanner is enabled.

A judge job cut off by a restart leaves its hold unanswered and its `judge-…` run marked
running. When the news worker starts, it fails those runs as `news_processing_stale` and
queues the judge again for each hold it would still answer; such runs do not count as
failed calls. Apart from that and the judge's own retry after a failed call, nothing asks
again: a job that died with its run still marked running (at its 30-minute timeout, say)
waits for the next worker start, and one that failed before it recorded a run is not
retried (see "Known limits"). The timeout is 30 minutes because one question on a
subscription account may take two rounds of up to eight minutes each, and a finished
article then has its evidence pages fetched again before it is published.

A second job for a hold that is being judged asks nothing. It steps aside when it finds a
`judge-…` run that is still running, is less than 31 minutes old and began after the story
last ran: that job has the hold. An older run, or one from before the story ran again, is
failed as `news_processing_stale` and the hold is asked about.

## When every subscription account is full

With 「Claude 連線方式」 set to 訂閱帳號, the AI vendors card's 「訂閱帳號都滿時」
(`ai_subscription_fallback`) decides what a call does when every account is full:

- 「改用 MiniMax」 (`minimax`, the default) runs it on MiniMax at once.
- 「等帳號恢復」 (`wait`) is the owner's choice of 2026-09-26. A news candidate goes back to
  `discovered` as `news_subscription_paused`, or keeps its marker (a re-verify, an evidence
  refresh, a resume, or one of the review judge's two), and its job tries again 30 minutes
  later (`jobs.PAUSE_MINUTES`). The accounts take turns A → B → … → A, each used until it
  is full. A review-judge call that finds every account full records no verdict and asks
  about the same hold again after the same 30 minutes, as often as it takes.

## When Jev's daily budget is spent

Jev is limited to `jev_daily_call_budget` calls per UTC day (default 200; the owner raised
production's to 5,000 in the admin on 2026-09-27). When the budget is spent at the duplicate
check, the candidate goes back to `discovered` as
`news_jev_quota_paused` instead of waiting in the review queue as an uncertain duplicate;
nothing is uncertain about the story. The orphan sweep skips it until 00:00 UTC (08:00 in
Taipei) and then queues it again, 20 a minute, so each day runs as many as that day's budget
allows and the rest pause again. Raising the budget in the admin during the day that spent it
does not wait for 00:00 UTC: every minute the scheduler compares today's count with the saved
budget, and while there is room the sweep queues the paused candidates at once. A check that did reach Jev and came back between 0.25 and
0.85 still waits for an editor. Later Jev stages keep their holds: a spent budget at the Jev
final gate is `news_jev_final_hold`, which the owner can publish from, and which the review
judge answers like any other when AI review is on. A candidate that carries a kept marker
(a rewrite the judge ordered, for one) keeps it instead of the paused code, so its
directions are not lost; the ordinary orphan sweep runs it again two hours later.

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
story that may not go out on its own (or the review judge's, with AI review on).

Rows the review judge rejected or handed back (`judge_decision` is set) are not in this
list either: they keep their stop code, and the owner takes them back or runs them again
one at a time. Do not use this flagless list to move the 需重寫 list along once AI review is
on. Its unjudged rows carry three of the same stop codes and would be reopened as plain new
drafts in the actor's name, without the judge's directions or its rewrite limit;
`--judge-redrafts` (below) is for them.

`--jev-quota-holds` takes the uncertain-duplicate holds whose latest duplicate check never
reached Jev because its budget was spent (207 on 2026-09-26). With `--apply` they are marked
`news_jev_quota_paused` rather than queued, and start after the next 00:00 UTC.

`--judge-holds` (the 待審查 list) and `--judge-redrafts` (the 需重寫 list) hand the review
judge the stories that were already waiting when AI review was switched on, or that arrived
while one of its switches was off. A story that arrives with everything on reaches the
judge by itself. Without `--apply` the command writes and queues nothing. It prints how
many stories rest in that list's holds since the day (`held`), how many the judge would be
asked about (`eligible`), the batch with its counts by hold and by category (`rows`,
`by_hold`, `by_vertical`), the four switches, and under `excluded` what is left out and
why: `answered` (already judged, or taken back by the owner), `gate_off` (a switch is off
for that category), `has_article`, `person_decided` (a person's decision on a redraft
row, or a confirmed story the final editor held), `evidence_expired`, `legacy_bundle`
(five stored locales and no article) and `rewrite_cap`. With `judge_enabled` off nothing
is eligible, and a `warning` says so. `--since` is here the day the candidate was created,
since a source may give no publication date. Only one pool flag may be given per run.

`--apply` needs `--limit N` and takes the newest N eligible stories. It queues one judge
job for each and does nothing else: no candidate is reopened or changed, no audit row is
written and no `--actor-email` is needed, because nothing is done in a person's name. The
judge then reads each story afresh and answers it as it would a new arrival. Read the
verdicts of one batch before releasing the next; stories already judged drop out of the
next listing by themselves. The same batch sent again within the same clock hour queues
nothing (`already_queued`). Sent again in a later hour, it queues a second job for every
story that is still unanswered, and a story in `eligible` may be one whose first job is
queued, in its call or waiting to retry. A second job costs nothing where the first is in
its call (it steps aside) or has answered by the time the second runs. Where the first
call failed and is waiting out its 30 minutes, the second job asks at once, and a failure
of that call counts toward the three like any other.

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
- The review judge has no translations-only rerun. When a locale review fails before an
  article exists, the judge can only order a whole rewrite: a new zh-TW draft, the fact
  check and Jev again, then every translation, although the draft had already passed its
  fact check (task 2026-10-06-news-judge-translations-only-rerun).
- Some rows wait for the owner however long AI review has been on. `failed` rows are never
  put to the judge. Legacy stored bundles (five locales on the candidate and no article,
  from before #1136) are left out by the backlog flags, and where one reaches the judge it
  is never sent back for a new draft. The holds that need work are not judged at all:
  `news_hard_checks_failed`, `news_evidence_changed`, a confirmed story stopped in
  translation and an article a re-check stopped (task
  2026-10-06-news-evidence-changed-auto-recheck).
- No sweep feeds the judge. A hold goes unjudged when the enqueue after the candidate's
  run failed (the worker logs "could not be queued for the review judge"), when the judge
  job failed before it recorded a run, or when a switch was off as the story arrived. The
  story then waits in the owner's list without the 「AI 交回」 badge, as if AI review were
  off. A dry run of `backfill_cli --judge-holds` and `--judge-redrafts` lists such stories
  as eligible, and `--apply --limit N` sends them.
- A rewrite's own run asks Jev about duplicates before it drafts. When that answer is
  uncertain the story is held as `news_duplicate_uncertain` and the hold replaces the
  marker. Jev's answer records that the marker was still on the row (`interrupted` in the
  duplicate assessment's details), which it is until the rewrite reaches an outcome. If the
  judge then answers "not a duplicate", the draft that follows is still that rewrite, with
  its directions. That holds also when an earlier run of the rewrite was paused or cut off
  after its draft call had begun, since no draft of it was kept. If the owner answers with
  「不是重複，繼續寫」, it is the owner's own draft, without them, and the rewrite still
  counts toward the limit of two. Once the rewrite has reached an outcome (a stop, a hold,
  or the owner's 「重新執行」), a later duplicate hold does not bring its directions back.
- The judge's instructions have only been run against test doubles (as of 2026-10-06). The
  rules under "With AI review on" are enforced in code whatever the model returns; how well
  it judges is to be read from the first small batches.
