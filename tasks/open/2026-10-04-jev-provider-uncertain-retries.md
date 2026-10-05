---
id: 2026-10-04-jev-provider-uncertain-retries
title: Hold uncertain Jev provider POSTs before retrying or consuming new quota
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-jev-uncertain-retries
claimed_at: 2026-10-05T00:15:11Z
created_at: 2026-10-04T18:03:59Z
completed_at:
branch: claude/jev-uncertain-retries
depends_on: []
scope:
  - apps/api/app/ai/jev.py
  - apps/api/tests/test_jev_client.py
---

# Hold uncertain Jev provider POSTs before retrying or consuming new quota

## Why

JevClient._send retries a provider POST after a timeout and several upstream statuses inside a single application request. A caller-side guard limiting application POSTs therefore cannot establish that an uncertain paid provider request was sent only once. For video audio checking, consume_jev_call runs before Jev.ask, so that one quota entry also does not describe the possible provider wire count. A timeout may follow successful processing; preserve the uncertain outcome before attempting another paid wire.

## Definition of done

- [x] An ambiguous provider send or response-body outcome cannot automatically produce another paid Jev wire, including within one application POST.
- [x] Request-bound uncertainty and known-result evidence distinguishes provider wires, application calls and daily quota consumption.
- [x] Definitively never-sent failures and documented settled failures have bounded recovery; models, credentials, budgets and returned verdicts remain unchanged.

## Steps

- [x] Reconcile the existing active Jev scope before claiming this follow-up.
- [x] Add offline lost-after-send, response-body failure and upstream-status fixtures around the real JevClient loop.
- [x] Provide safe per-call uncertainty handling and document the exact guarantee without widening the quota or retrying an unknown result.

## How to verify

Run apps/api/tests/test_jev_client.py with fake httpx transports. Count actual provider transport calls when a request is processed but its answer is lost; an uncertain input must not wire again. Include known successful result preservation and clearly never-sent controls. Do not reproduce ambiguity against a paid provider.

## Notes

- Source inspection on 2026-10-04: apps/api/app/ai/jev.py:249-315 has an internal POST loop with one timeout retry, up to two 429 retries, three 529 retries and one other 5xx retry. apps/api/app/video_speech/checking.py:235-242 consumes the daily Jev call before asking through that client. This is a source-contract finding, not an observed duplicate bill or provider retry during production.
- The separate 2026-10-04-prevent-automatic-retries-of-paid-video ticket scopes the automation CLI transport only. The paid speech CLI ticket likewise cannot fix the inner provider loop. Keep this implementation narrowly server-scoped.
- Existing 2026-09-22-jev-review-advisory-tool is in-progress under claude-fable-5-1 and includes apps/api/app/ai/jev.py. This new ticket is unclaimed; preserve that scope ownership and coordinate first. The open P3 vendor-doc comment task also mentions that path.
- The Embedding producer has not started paid audio judging and will not claim provider-level one-wire protection from its outer fetch guard. Its separately protected Gemini narration run continues; no shared server code, global setting, model, limit or deployment was changed by filing this ticket.

### 2026-10-05, claude-opus-5-5-jev-uncertain-retries

- **Claim reconciled with `--force`.** Two stale claims covered this scope, and both branches had
  landed: 2026-09-22-jev-review-advisory-tool (claude-fable-5-1, 299 h, branch
  `claude/jev-review-tool` merged as #663 on 2026-09-22; `jev.py` changed again since by #1218;
  its unticked items are the owner's real-key measurement, not code in `jev.py`) and
  2026-10-03-illustrated-slides-round-2-a-family (claude-fable-5-1-illustration-round2, 40 h,
  scope `apps/api/tests`; branch `claude/video-production-tutorial-optimization-f5d1bc` merged as
  #1172 on 2026-10-03; it still needs the receipt rebind and post-deploy checks, neither in this
  scope). Neither ticket file was edited. The P3 vendor-doc comment task named above is
  2026-10-03-jev-comments-drifted-from-vendor-docs, done in #1218; this change builds on it.
- **What `_send` retries now.** A connection that never opened (`ConnectError`,
  `ConnectTimeout`, `PoolTimeout`) is tried once more; before, it raised at once. 429 (two
  retries) and 529 (three) are unchanged and still end in `httpx.HTTPStatusError`. A read or write
  timeout, `ReadError`, `RemoteProtocolError` and any other transport error after the request may
  have left (phase `send`), any 5xx other than 529 (phase `response`), and an answer whose body
  is not JSON or cannot be decoded (phase `body`) raise `JevOutcomeUncertain` after that one
  wire; before, a timeout and a 5xx each got one more POST. `UnsupportedProtocol` and
  `LocalProtocolError` never left the process and are raised as they are. 401/403/400/422 are
  unchanged. The shared attempt count still caps one `ask()` at four POSTs, of which only the
  last can have been processed.
- **The guarantee, as the `_send` docstring states it:** one `ask()` puts at most one
  possibly-processed request on the wire, plus at most three the provider refused (429/529) or
  never received. Retrying 429/529 rests on the vendor naming them as the retryable statuses,
  read here as "turned away, not run"; `_REFUSED_RETRIES` carries a comment saying it is the
  line to change if TypeSafe ever bills them. That reading was not re-checked against TypeSafe
  in this change (no TypeSafe calls were made).
- **Evidence.** `JevOutcomeUncertain` (a `JevError`, not a `JevRequestInvalid`, so no caller
  maps it to 422) carries `phase`, `status`, `wires_sent` for that `ask()`, and
  `request_sha256`. `_send` now serialises the body itself with the same arguments httpx
  0.28.1 uses for `json=` (`ensure_ascii=False`, compact separators, `allow_nan=False`) and
  sends it as `content=`, so the hash is of the bytes actually sent; the existing body-shape
  tests pass unchanged. `JevClient.application_calls` and `JevClient.wires_sent` count
  `ask()` calls that reached the network and POSTs handed to the transport; both only grow,
  so they stay right if one client serves concurrent asks. Daily quota is still one
  `consume_jev_call` per application call, taken by the caller; `checking.py`, models, keys,
  budgets and verdict parsing are unchanged.
- **What callers see.** Every Jev caller already catches `JevError`: `guides/jev_review.py`,
  `hotspots/ai_search.py`, `video_automation/admin_api.py` and `video_speech/admin_api.py` catch
  `(JevError, httpx.HTTPError)`; `news_automation/ai.py` catches `(JevError, TimeoutError)` per
  locale and `Exception` around the loop; the admin probe catches `Exception`. One visible
  difference: in `jev_assessments`, an uncertain outcome now marks only that locale `confirm`
  with reason `JevOutcomeUncertain`, where before the escaping httpx error hit the outer handler
  and marked every locale `confirm`. The admin settings probe now shows
  `Jev 驗證失敗（JevOutcomeUncertain）` for a timeout instead of `ReadTimeout`.
- **Left for a follow-up:** the three video judge endpoints still answer every Jev failure with
  the same 502, dropping the uncertain/settled distinction and the request hash before it
  reaches the CLI transports. Filed as 2026-10-05-jev-judge-endpoints-report-an-uncertain.
- **Verified:** `test_jev_client.py` 35 passed (20 before; 15 new: four lost-after-send
  transport errors, four 5xx statuses, a non-JSON 200, three never-sent errors retried once, a
  second never-sent error not retried, 429 then timeout holding at two wires, and a success
  counted as one wire with its answers unchanged). `ruff check .`, `mypy app` and `mypy tests`
  are clean.
