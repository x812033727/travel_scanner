---
id: 2026-10-04-jev-provider-uncertain-retries
title: Hold uncertain Jev provider POSTs before retrying or consuming new quota
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-04T18:03:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/ai/jev.py
  - apps/api/tests/test_jev_client.py
---

# Hold uncertain Jev provider POSTs before retrying or consuming new quota

## Why

JevClient._send retries a provider POST after a timeout and several upstream statuses inside a single application request. A caller-side guard limiting application POSTs therefore cannot establish that an uncertain paid provider request was sent only once. For video audio checking, consume_jev_call runs before Jev.ask, so that one quota entry also does not describe the possible provider wire count. A timeout may follow successful processing; preserve the uncertain outcome before attempting another paid wire.

## Definition of done

- [ ] An ambiguous provider send or response-body outcome cannot automatically produce another paid Jev wire, including within one application POST.
- [ ] Request-bound uncertainty and known-result evidence distinguishes provider wires, application calls and daily quota consumption.
- [ ] Definitively never-sent failures and documented settled failures have bounded recovery; models, credentials, budgets and returned verdicts remain unchanged.

## Steps

- [ ] Reconcile the existing active Jev scope before claiming this follow-up.
- [ ] Add offline lost-after-send, response-body failure and upstream-status fixtures around the real JevClient loop.
- [ ] Provide safe per-call uncertainty handling and document the exact guarantee without widening the quota or retrying an unknown result.

## How to verify

Run apps/api/tests/test_jev_client.py with fake httpx transports. Count actual provider transport calls when a request is processed but its answer is lost; an uncertain input must not wire again. Include known successful result preservation and clearly never-sent controls. Do not reproduce ambiguity against a paid provider.

## Notes

- Source inspection on 2026-10-04: apps/api/app/ai/jev.py:249-315 has an internal POST loop with one timeout retry, up to two 429 retries, three 529 retries and one other 5xx retry. apps/api/app/video_speech/checking.py:235-242 consumes the daily Jev call before asking through that client. This is a source-contract finding, not an observed duplicate bill or provider retry during production.
- The separate 2026-10-04-prevent-automatic-retries-of-paid-video ticket scopes the automation CLI transport only. The paid speech CLI ticket likewise cannot fix the inner provider loop. Keep this implementation narrowly server-scoped.
- Existing 2026-09-22-jev-review-advisory-tool is in-progress under claude-fable-5-1 and includes apps/api/app/ai/jev.py. This new ticket is unclaimed; preserve that scope ownership and coordinate first. The open P3 vendor-doc comment task also mentions that path.
- The Embedding producer has not started paid audio judging and will not claim provider-level one-wire protection from its outer fetch guard. Its separately protected Gemini narration run continues; no shared server code, global setting, model, limit or deployment was changed by filing this ticket.
