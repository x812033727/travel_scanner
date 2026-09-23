---
id: 2026-09-22-jev-review-advisory-tool
title: Jev review: advisory editorial and overlap checks for content packs
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-22T13:08:10Z
created_at: 2026-09-22T13:08:06Z
completed_at:
branch: claude/jev-review-tool
scope:
  - apps/api/app/guides/jev_review.py
  - apps/api/app/guides/pack_cli.py
  - apps/api/app/ai/jev.py
  - apps/api/app/hotspots/guide_shadow_cli.py
  - apps/api/tests/test_guides_jev_review.py
  - README.md
depends_on: []
---

# Jev review: advisory editorial and overlap checks for content packs

## Why

Two editorial defects keep reaching review by hand, and both are judgements about text
rather than facts -- which is the one thing Jev is good for.

The first is the 2026-09-21 rejection of the 22 Korean food specials. The articles were
accurate and were written to the editor rather than to the traveller: verification
discipline in the body ("the official page does not state it, so we did not label it"),
Korean field names copied out of listings, Korean sentences left untranslated. Regexes
find some of it -- `本文|這篇`, `官方頁(寫|說|的)`, `교통 정보` -- but they cannot see a
paragraph that narrates sourcing in words nobody put on a list, and they never will.

The second is duplicate commissioning. Batch 8 lost three topics to collisions that were
only noticed after two sessions had written them, and batch 4.4 expects 30-50% of its
candidates to turn out to be articles the catalogue already has.

It stays advisory, and that is a decision rather than a first step. TypeSafe publishes
Jev's accuracy for English only and publishes nothing for the other four locales this
product ships in, so `JEV_CJK_AUTOPILOT_ENABLED` is false and `route_answer` can never
return `act` for a Chinese answer. Every answer here is about Chinese text. A check that
may not be trusted to act can still be trusted to sort a reviewer's queue, so this one
flags and ranks and writes nothing: flags never change the exit code, and no pack, image
or database row is touched. The deterministic `signals` column beside every row is the
baseline the model has to beat -- if `flagged_without_signal` is empty, the network call
bought nothing and the regexes alone are the right tool.

There is no Redis budget because there is no shared account to protect. This is one
process a person starts, the call count is known before the first call is sent,
`--max-calls` refuses a plan over it, and the whole measured corpus costs about two
cents. A Redis dependency would only stop the tool running on a laptop or against a
`git archive` export, which is exactly where it earns its keep.

## Definition of done

- [x] `pack_cli jev-review editorial|overlap|compare` runs over a content directory
      (`--dir`, so a `git archive` export of an older version works) and writes no pack.
- [x] `--dry-run` prints the whole plan -- documents, units, calls, estimated input
      tokens and USD -- with `usage.calls == 0`, and constructs no client at all.
- [x] A missing key is refused before a client exists; a plan over `--max-calls` is
      refused before the first request; neither the key nor a response body can reach a
      report or stdout.
- [x] A document too large for one call is halved rather than trimmed, so every unit is
      still answered.
- [x] `overlap` ranks the catalogue lexically, chunks it under the vendor's 255-option
      and state-token caps, takes the maximum noul over every round, and states in the
      report whether the ranking is comparable.
- [x] `compare` pairs two editorial reports by slug and reports wins and losses,
      residual flags, a control group apart from the subjects, and a stratified blind
      TSV sample for hand labelling.
- [x] `USD_PER_INPUT_TOKEN` has one home (`app/ai/jev.py`); `guide_shadow_cli` imports
      it.
- [x] README says the tool exists, that it is offline and advisory, and how to read a
      report.
- [ ] The measurement below has been run with a real key and its numbers written here,
      or the tool is recorded as not meeting the gate.

## Steps

- [x] `app/guides/jev_review.py`: unit extraction, both questions, chunking, merging,
      the budget, the async runner and the three renderers.
- [x] `pack_cli jev-review` with `editorial`, `overlap` and `compare`; UTF-8 stdout,
      `--report`, exit codes 0 / 1 / 2.
- [x] `USD_PER_INPUT_TOKEN` moved into `app/ai/jev.py`.
- [x] `tests/test_guides_jev_review.py` (21 tests) over `httpx.MockTransport`.
- [x] README paragraph in the Jev section.
- [x] Dry runs against the shipped corpus, to prove the plan arithmetic (see Notes).
- [ ] Measure both checks with a real key (needs the owner's `.env`; see Notes).
- [ ] If the gate is met, put `editorial` into the batch-8 and 4.7 intake runbook and
      `overlap` into candidate selection. If it is not, keep the regex column only,
      write the numbers here and leave the tool out of the runbook.

## How to verify

From `apps/api`, with this worktree's venv (`uv sync --frozen`):

```bash
./.venv/Scripts/python.exe -m ruff check .
./.venv/Scripts/python.exe -m mypy app
./.venv/Scripts/python.exe -m mypy tests
./.venv/Scripts/python.exe -m pytest tests/test_guides_jev_review.py \
    tests/test_jev_client.py tests/test_jev_guide_shadow.py \
    tests/test_guides_content_pack.py -q
```

The plan needs no key (`PYTHONIOENCODING=utf-8` on Windows):

```bash
./.venv/Scripts/python.exe -m app.guides.pack_cli jev-review editorial --kind howto --dry-run
./.venv/Scripts/python.exe -m app.guides.pack_cli jev-review overlap \
    --proposal <p.json> --kind howto --kind intel --dry-run
```

The measurement, once a key is in the repository-root `.env`. The labelled corpus is the
rewrite in commit `af86123f` -- 22 Korean specials plus 6 Taiwanese controls, whose slugs
come from `git show --stat=200 --format= af86123f -- apps/api/app/guides/content`:

```bash
git archive af86123f^ apps/api/app/guides/content | tar -x -C <corpus>/before
git archive af86123f  apps/api/app/guides/content | tar -x -C <corpus>/after
cd apps/api
./.venv/Scripts/python.exe -m app.guides.pack_cli jev-review editorial \
    --dir <corpus>/before/apps/api/app/guides/content --slug ... --report before.json
./.venv/Scripts/python.exe -m app.guides.pack_cli jev-review editorial \
    --dir <corpus>/after/apps/api/app/guides/content --slug ... --report after.json
./.venv/Scripts/python.exe -m app.guides.pack_cli jev-review compare \
    --before before.json --after after.json --sample 40 --out sample.tsv \
    --control <the 6 Taiwanese slugs>
```

About 56 calls, roughly $0.02. Every part of the gate has to hold:

- the before side flags >= 40% of units and the after side <= 15%, and at least 20 of
  the 22 Korean articles fall in the pairing.
- hand-labelled precision of flagged units >= 0.80, and >= 0.60 among the residual --
  the flagged rows no regex found, which are the only ones the call is paying for.
- after-side false positives <= 10%, concentrated in the allowed opening 「這篇」; read
  the report with `block_index <= 1` ignored.
- at least 85% of the 374 units the regexes flag on the before side are flagged by Jev
  too.
- the 6 Taiwanese controls stay <= 15% on both sides. A rise there means the question is
  measuring "was this rewritten" rather than "is this editorial voice", and the whole
  result is void.

Overlap, about $0.05: the positive `tech-news-apple-m6-m5-ultra-20260825` against
`--kind life` must put `local-ai-on-mac-mini` in the top 3 with noul >= 0.5; ten
sister-article negatives (one dish, two cities, the sister excluded) must answer `none`
or < 0.5; the three batch-8 topics dropped for collisions are positives and the 20
finished specs are negatives. Gate: >= 80% of positives hit the top 3, >= 90% of
negatives below 0.5.

## Notes

**The key is the owner's to place, and nothing here touches it.** `Settings` reads
`../../.env` relative to the working directory (`app/config.py:92`), so that file is the
repository root's `.env` and the command has to be run from `apps/api`. Until the owner
pastes the same key that is on the admin card into it, every real run stops with
`JEV_API_KEY is not set in the environment or ../../.env; nothing was sent` and sends
nothing. The key never enters a report, a URL or stdout; a provider failure is recorded
as `TypeName: first 160 characters`.

**The chunk arithmetic in the plan counted one side of the request.** The plan measured
about 186 tokens per option for the 167 travel packs and 158 for the 922 lifestyle ones,
and this code still measures 186 and 159 -- but that is the choice question's criteria
entry alone. The state repeats every article as `{id, title, description}`, so one
candidate really costs about 381 (travel) or 327 (life) tokens per request, and the token
ceiling (80% of `JEV_MAX_STATE_TOKENS` = 19,200) binds before `--chunk-size 80` does. The
shipped catalogue therefore plans 4 chunks for travel and 17 for life rather than the 3
and 12 the plan predicted -- 5 and 18 calls per proposal, $0.0028 and $0.0130, against
the $0.0025 and $0.008 the plan budgeted. `test_the_shipped_catalogue_costs_what_the_plan_measured`
pins both numbers, so the day someone shortens the option text or drops the duplication
the test will say so.

**Measured dry runs** (2026-09-22, shipped corpus, no key needed):

- `editorial --kind howto`: 146 documents, 5,030 units, 146 calls, about 1,622,957 input
  tokens, est. USD 0.0682. 355 of those units already carry a regex signal.
- `overlap --kind howto --kind intel`: 167 candidates, 4 chunks (9,747 / 9,667 / 9,654 /
  4,091 state tokens), 5 calls with the final round, about 67,421 input tokens, est. USD
  0.0028.
- `overlap --kind life`: 922 candidates, 17 chunks, 18 calls, about 309,553 input
  tokens, est. USD 0.0130.

The whole corpus is 1,089 documents and about $0.50 for one editorial pass. That is why
`--max-calls` defaults to 50 and why the intake use is `--slug` per batch.

**What the question deliberately does not do.** It does not count. TypeSafe publishes
that Jev does not count reliably, so the counting rules -- one 「這篇」 per article, one
sourcing sentence per section -- stay with the regexes in `signals_for`. The known false
positive is the allowed opening 「這篇」; rather than add a second hop to the question,
ignore `block_index <= 1` when reading a report.

**Excluded unit kinds, and why.** `image.description` transcribes what a diagram already
draws, field names included, so it would be flagged forever and never be wrong. Table
cells are fragments no question about voice can be asked of -- their caption is the unit.
`code` is a command; `link`, `offer` and `partner_link` are labels on a button.

**A stale content directory must not fail as a whole.** Both checks read pack files one
at a time with `json.loads` rather than through `load_packs`, because the measurement
points them at `git archive` exports where one pack that no longer validates would take
the other nine hundred with it. Such a file lands in `skipped` with its reason.

**Local test noise that is not this change.** On Windows, `tests/test_guides_autolink.py`
has one failure and three fixture errors from its own `write_text`/`read_text` calls
without `encoding=`, and `mypy tests` reports `socketserver.UnixStreamServer` undefined
in `tests/support/e2e_deploy_agent.py`. Both are platform-only and green in CI.

**S2 (the production shadow switch) was done on 2026-09-22 ~13:33Z, outside this branch.**
With the owner's explicit approval and after confirming no staged release was between
phases (every `/root/mokaair-localization-*/state.json` was `complete` or activated, no
hold file), `/root/travel_scanner/.env` (backup `.env.bak-20260922-jev`) gained
`JEV_SHADOW_GUIDE_ASSESSMENT=shadow` and only the `worker` service was recreated
(`up -d --no-deps --no-build --force-recreate worker`; `restart` would not re-read the
env file). The key was not added to the file; it stays on the admin card and reaches the
job through `load_runtime_settings`. Afterwards the worker was Up, its environment listed
exactly one new variable name, its log had no error lines, and the other ten services
were untouched. The owner's connection test on the card passed. Shadow rows appear only
when an admin runs the hotspot guide 「AI 搜尋」 (`POST /hotspots/guides/ai-search`); the
first `jev-shadow-report` after the switch showed `runs_with_shadow_rows: 0` because no
such search had been run yet.
