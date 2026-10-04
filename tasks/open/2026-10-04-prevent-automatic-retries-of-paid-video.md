---
id: 2026-10-04-prevent-automatic-retries-of-paid-video
title: Prevent automatic retries of paid video judge requests
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-04T16:08:05Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Prevent automatic retries of paid video judge requests

## Why

The automation client's model runs distinguish an uncertain paid outcome from a request that never reached the server. Its judgePolicy and judgeOutline methods call the same request helper without the paid flag, so thrown fetch errors and general 5xx answers can trigger another paid judge POST. The policy and outline endpoints consume one Jev call before asking the provider. Losing an answer can therefore consume the quota again. This is a source finding, not evidence of an observed duplicate charge.

## Definition of done

- [ ] Policy and outline judge calls are never blindly resubmitted after an ambiguous transport or response-body failure.
- [ ] Definitive never-sent and server-settled failures retain bounded recovery, and read-only GETs remain retryable.
- [ ] Any persisted or reused answer stays bound to the exact request, current stance and applicable question set; a failed verdict is preserved unchanged.

## Steps

- [ ] Audit every cost-bearing automation method and its request flags, including response-body failures and gateway errors.
- [ ] Add uncertainty handling or source-bound reconciliation without changing models, budgets, approvals or global settings.
- [ ] Add fake lost-after-send and lost-response-body tests proving at most one paid POST for an uncertain input, plus safe-recovery controls.

## How to verify

Run `node --test tools/video/automation/client.test.mjs` and relevant QA caller tests. Use fake transports; do not reproduce an ambiguous outcome against a paid provider. Assert that the judge methods retain the original returned answer and that an unknown outcome cannot be retried by the same caller.

## Notes

- `tools/video/automation/client.mjs:87` defaults request paid=false; judgePolicy at267 and judgeOutline at274 omit that option. The protections for model stage runs do not establish protection for these judge methods.
- `apps/api/app/video_automation/judge.py:571-588` consumes the Jev quota before asking; judge_policy at628-653 and judge_outline at592-605 use that path.
- The separate paid speech ticket covers `tools/video/tts/client.mjs`, a different transport. Keep these fixes independently scoped.
- During this LLM continuation, only private normal-CLI transport guards are being prepared. Shared automation code is unchanged; no duplicate quota consumption is claimed.
