---
id: 2026-10-03-refresh-animation-skill-provider-and-judge-contracts
title: Refresh animation skill provider and judge contracts
status: done
priority: P2
area: tools
owner: codex-animation-skill-integration-20261003
claimed_at: 2026-10-03T14:22:16Z
created_at: 2026-10-03T14:21:48Z
completed_at: 2026-10-03T14:58:07Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - tools/animation-production.test.mjs
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - .agents/skills/animation-camera/references/model-misreads.md
  - .agents/skills/animation-production/SKILL.md
  - .claude/skills/animation-production/SKILL.md
  - .agents/skills/animation-production/references/error-catalogue.md
  - .agents/skills/animation-production/references/cost-model.md
  - .agents/skills/animation-production/references/providers-and-plans.md
  - .agents/skills/animation-production/scripts/drama_preflight.mjs
  - .agents/skills/animation-production/scripts/episode_estimate.mjs
---

# Refresh animation skill provider and judge contracts

## Why

The animation skills and their offline helpers still describe the pre-fix Lite
negativePrompt failure and expect named-look clip identity questions to exceed
400 characters. This conflicts with the adapter and bounded clip rubric already
implemented in this PR. Clearing an approved look's negative field would also
invalidate its hash and approvals unnecessarily. The skills still link to two
implementation tickets under `tasks/open` after those tickets were archived.

On PR head 70174ca194, the Linux tool run selected 1,494 cases: 1,491 passed,
two failed and one skipped. The failures were the stale clip-question assertion
and the skills path check. The advisory npm audit output was not their cause.

## Definition of done

- [x] Offline Lite estimates and preflight accept preserved nonempty avoidance constraints without modifying the source or its approved look/storyboard records.
- [x] Long named-look clips use the actual bounded rubric without a false length finding; a genuinely new keyframe with an overlong identity question is still rejected.
- [x] Both skill entrypoints and their exact Claude mirrors describe this code version's adapter behavior, correct done-ticket paths, and the separate actual-backend deployment boundary.
- [x] Historical per-take evidence, paid amounts and post-mortem bytes remain unchanged; cost, quality, budget, approval, retry and other guards are preserved.
- [x] Focused production/camera and full skill mirror/path tests, both skill-creator validators, syntax and task checks pass locally.
- [x] Independent review of the final source hashes and current-head CI pass before root closes this integration ticket.

## Steps

- [x] Complete fresh 13-path collision gate and normal claim; no force or historic claim removal.
- [x] Capture baseline source hashes and meaningful old-script RED with corrected synthetic fixtures.
- [x] Remove obsolete Lite rejection logic, retain real keyframe guards, and update current guidance without rewriting historical trials.
- [x] Run scoped offline GREEN, validate both skill folders and prove unchanged historical bytes/unrelated assertions.
- [x] Root integrates the independently reviewed candidate into the existing PR and records its exact CI result.

## How to verify

```bash
node --test tools/animation-production.test.mjs tools/animation-camera.test.mjs tools/skills.test.mjs
python -X utf8 <skill-creator>/scripts/quick_validate.py .agents/skills/animation-camera
python -X utf8 <skill-creator>/scripts/quick_validate.py .agents/skills/animation-production
node --check .agents/skills/animation-production/scripts/drama_preflight.mjs
node --check .agents/skills/animation-production/scripts/episode_estimate.mjs
node --check tools/animation-production.test.mjs
node tools/tasks.mjs check
git diff --check
```

Use the configured bundled Node runtime; the author run captured actual
`process.execPath` and `process.version` as v24.19.0. The existing API provider
regressions already verify Lite omission plus preserved avoidance text and
non-Lite parameter retention; this change does not replace them with source regexes.

## Notes

- Fresh collision proof: `<home>/.codex/tmp/animation-skill-integration-20261003/scope-gate.json`, SHA-256 `fedf7f0d5983ed3502df5cd79e0a920f01647e369e01a9eddcbf1aa117f2955e`; 11 source paths plus exact task open/done metadata, 495 refs, 28 worktrees, 32 live heads including disjoint PR #1179. No active collision and no intersection with the 108 duration bindings. Normal claim succeeded. The CLI truncated the requested slug; only the author's just-created template was renamed to this gated exact ID before claiming.
- Final author receipt: `<home>/.codex/tmp/animation-skill-integration-20261003/implementation-receipt.json`, SHA-256 `d48e757c5fd8c46d09921e444316ed2f49abf36f4db5b38027e2d31b3df34f90`. It pins actual runtime/argv, all 11 final source hashes, RED/GREEN receipts and historical-byte proofs.
- Corrected-fixture RED against the exact old scripts: 12 tests, 8 passed / 4 failed, exit 1. Final GREEN: 46 passed / 0 failed / 0 skipped, exit 0 (production 12, camera 28, skills 6). The initial fixture mistakenly passed the whole document to `resolveLook`; it was corrected to `doc.look` before the final old-script RED. Initial logs are retained but superseded.
- Both skill-creator validators passed using explicit `python -X utf8`; the first default Windows cp1252 reads failed before validation and are retained separately. Three Node syntax checks, task check and diff check passed.
- Eight unrelated original test blocks remain byte-for-byte identical. All price assertions outside the obsolete Lite rejection, the later pricing/levers checks, and external-clip acceptance remain exact. The complete model-misreads section-one trial table, original production-run and post-mortem are byte-identical; both SKILL mirrors match exactly.
- This is offline source integration, not a paid retry, deployed backend check or media acceptance. No services, provider requests, production settings, approvals, price constants, limits or quality thresholds were changed. Whole-PR CI remains root-owned and is not inferred from the focused local run.
- Independent review passed for all eleven frozen source hashes, real keyframe rejection, retained guard bodies and historical evidence. Private `independent-review.json` SHA-256 `5f0f3679d2ccbdf00f11e6c76242535e9653bbb28cd502d1d440882a26e2b53a` also confirms both mirrors and all 108 untouched duration bindings. Exact-head whole CI is still required before closure.

2026-10-03 exact-head acceptance: PR head `ba5c6ae01df9eeffd13fc74233f7d37db0553c59`, actual
checkout/GITHUB_SHA `07c25196ba1c0901aad6600a5789584090496642`. All 23 PR checks
passed. [Full-stack job](https://github.com/x812033727/travel_scanner/actions/runs/37130278372/job/111223852163) ran 30 community browser
cases and six real-service recovery cases: zero failures and zero skips.
The final community spec SHA-256 is `21da9cdb3caad36061782af41669a3fc445dae952bbf04e432cf5ce8fe3ced5c`. The standalone
foundation ticket remains review for owner/capacity acceptance; this receipt
does not approve deployment, production access, paid media or publication.
Private canonical receipt SHA-256 `a33b0c59e320d8a65defe2ed7519ddaccf1627e68becc6041bf5352044e8eba7`; complete CI snapshot
SHA-256 `1a94a1b431240bd2e2a7e9623afe53cbbdad3295708d1e78e86f35f236f5f99d`. Earlier failed-head evidence remains preserved.
