---
id: 2026-10-26-pending-narrative-writer-recovery
title: Recover pending narrative rewrites without buying another panel or writer run
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-26T08:26:30Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Recover pending narrative rewrites without buying another panel or writer run

## Why

A new tutorial reached a genuine failed storytelling panel. Its native fixScript writer job was still running when the scoped step returned RUN_PENDING. Calling the next generic step ran the panel again before consuming that job; the second panel returned a different failure note. The client then treated the first writer request as stale, fetched its completed result into archive, and started another writer job for the changed note. This spends another panel/writer operation without adopting the first completed rewrite.

## Definition of done

- [ ] A pending script-repair writer job is resumed from its exact saved request before another panel or replacement writer is sent.
- [ ] Changed source inputs still hold or require proper reconciliation; failed storytelling checks are never marked passed to recover a result.
- [ ] A regression test covers RUN_PENDING, an alternate subsequent panel answer, exactly one writer dispatch, actual returned result adoption and unchanged retry limits.

## Steps

- [ ] Coordinate with existing active owners of flow.mjs before claiming this scope; no competing core change was made by the discovering controller.
- [ ] Make the native continuation preserve its exact repair intent across pending jobs and use the real source-bound receipt on resume.
- [ ] Test source changes, terminal/uncertain/gone jobs, actual failed lint, crash boundaries and normal future panel rechecks after adoption.

## How to verify

Run focused automation tests and required tools checks. A second invocation while the original saved writer is running must not call the narrative reader or dispatch another writer. After adoption, the genuinely rewritten script must still pass real verify/listener/narrative/demo gates.

## Notes

- Actual case: ai-pdf-quotes-to-comparison, external work /workspace/work/ai-pdf-01, branch codex/ai-pdf-comparison-20261026, draft PR1864 no-auto-merge.
- First source-bound writer request4608ed31112bd4b764dbb2da5a5772730eb28d48b7f147edc2b4ae3b7c02e367, job896e050a-14d6-477c-a00e-1ddb1d74fde8, was genuinely succeeded and archived at run-receipts/archive/4608ed31112bd4b764dbb2da5a5772730eb28d48b7f147edc2b4ae3b7c02e367-d6544532-e2db-4348-9b9d-2f3721dc888f.json. Its result remains preserved, not declared adopted.
- Second exact requestd253a26d360a52891c4e343b1a0ec4114e3e5e3db69fb8f97a6dbf7083efa9c4, jobc04e0dc3-6130-476d-ac35-dd1caeace90f. Root stopped generic steps after identifying the drift and is preparing an exact GET-only recovery adapter.
- Current source freshIds is deterministic; an earlier audit guess that random IDs caused this case was corrected. The observed source-input difference is the second panel owner_note (round1 no_recap/no_detour, round2 no_recap). Do not report an unverified cause.
- This is a real orchestration mistake disclosed to the owner. No reset, fake approval, transcription retry or language-cap change was used. Runtime recovery must not buy another job or hide the original failed panel.
