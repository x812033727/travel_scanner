---
id: 2026-10-15-preserve-subscription-busy-semantics-for-durable
title: Preserve subscription busy semantics for durable video jobs
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-15T16:18:49Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/subscription.py
  - apps/api/app/video_automation/ai.py
  - apps/api/tests/test_video_automation_subscription.py
  - apps/api/tests/test_video_stage_jobs.py
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
---

# Preserve subscription busy semantics for durable video jobs

## Why

The account agent returns `subscription_busy` when all suitable accounts stay busy through its queue wait. Video subscription `_failure` has no mapping for that code, so the durable video job becomes generic `video_ai_upstream_failed` / uncertain. A01's idea verifier stopped on this classification instead of a bounded service wait. Preserve enough dispatch evidence to distinguish a slot refusal from an actually uncertain model call; do not merely declare every busy message safe to retry.

## Definition of done

- [ ] A proven pre-dispatch busy refusal keeps its identity and permits an appropriate bounded retry/wait without losing paid uncertainty safeguards.
- [ ] A busy response reached after an earlier account attempt does not falsely assert that no CLI/model ever ran.
- [ ] Actual lost responses stay uncertain, and saved successful results are recovered without a new model call.

## Steps

- [ ] Inspect the deployed agent/API contract and account rotation before deciding what no-call evidence is reliable.
- [ ] Preserve the specific busy outcome and implement bounded service handling with regression tests.
- [ ] Test initial busy, quota/auth rotation then busy, genuine upstream failure and durable late success.

## How to verify

Run focused `tests/test_video_automation_subscription.py`, `tests/test_video_stage_jobs.py` and `tests/test_ai_accounts_agent_runs.py` under `apps/api`, plus affected lint/types. Assert request/receipt identity, dispatch count and retained uncertainty, not only error text.

## Notes

Observed live at `aac8d73fb0e5f2321cf9d929c6ea52e001198b23`: A01 job `a4232619-a9a0-4488-9964-c66d2287b22a`, key `6e79fbbf-f7d1-4d7e-844c-28d705fc1413`, created 2026-10-15 16:09:39 UTC and completed 16:10:49 UTC, `result_json=null`, uncertain/502, detail `every Claude account with room is running another prompt; try again shortly`. Its usage row is failed with 70262 ms and 0/0 tokens. This is not proof that no CLI attempt occurred: `run_prompt` may rotate after quota/auth refusals before a final busy refusal. The host account agent's runs/server hashes differ from the repo copies, so inspect actual deployed code before changing the contract. Original DB job and durable journal are preserved; any A01 recovery must use existing exact-job lookup/archive semantics under the existing authorization. No source fix or shared deployment is performed by filing this task.
