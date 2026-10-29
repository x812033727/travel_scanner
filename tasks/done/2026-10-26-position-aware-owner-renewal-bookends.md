---
id: 2026-10-26-position-aware-owner-renewal-bookends
title: Support position-aware owner renewal bookends
status: done
priority: P2
area: tools
owner: codex-bookend-renewal
claimed_at: 2026-10-26T02:23:12Z
created_at: 2026-10-26T02:22:44Z
completed_at: 2026-10-26T02:40:14Z
branch: codex/ai-editable-animation-20261025
depends_on: []
scope:
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal.test.mjs
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal-handoff.test.mjs
---

# Support position-aware owner renewal bookends

## Why

The existing owner renewal flow only accepted an intro before the body, while narrated channel videos place it after the opening condensation. A completed but unuploaded tutorial cannot use ordinary assemble to change an approved cut. Support a real position-aware candidate and normal source handoff, preserving the original approvals, upload guards and stopped-snapshot contract.

## Definition of done

- [x] A staged after-first-chapter candidate is bound to its actual retained body timeline and exact scene/chapter boundary.
- [x] Normal handoff verifies every retained picture and both sample-aligned audio ranges, emits the real applied intro offset and refuses provenance tampering.
- [x] Legacy/start/manual import/range contracts and owner-only submit guards remain intact.
- [x] Targeted tests and independent review pass; required broader checks were executed and the unrelated environment failures are recorded without claiming a full-suite pass.

## Steps

- [x] Check collisions and claim only the four renewal modules/tests.
- [x] Add optional stage --timeline; require it for after-first placement, snapshot/upload its actual bytes and bind SHA/placement in the candidate.
- [x] Extend normal handoff with the actual second-chapter cut, raw packet/Annex-B range preservation and 48kHz sample-trim audio comparison.
- [x] Add real H.264/B-frame split tests and failures for unbound timeline, unsafe cut, changed source and false media proof.
- [x] Obtain final independent review and relay actual result to original film controller.

## How to verify

Run `node --test tools/video/review/renewal.test.mjs tools/video/review/renewal-handoff.test.mjs` and `git diff --check`. Parent runs `npm run test:tools`, `npm run test:docs-videos` and task validation after the final source tree is stable.

## Notes

- Parent controller codex-ai-video is preparing the actual candidate separately. This task changes no media, provider requests, canonical auto.json/approvals, server routes or owner decisions.
- `stage ... --timeline /actual/retained/body/timeline.json` is required for an after-first pin. It derives the insertion from chapter[1] and a real scene boundary, refuses crossing/invalid body lines and binds the exact timeline SHA. The original body timeline remains unchanged.
- Only normal/native source handoff gained piecewise placement. Manual import and approved-final-body-range modes remain start-only because their retained caption/body contracts are different.
- Numeric intro_at_frame is not part of the branding hash; every new stage/handoff use recomputes it from the normalized pin and retained timeline, then compares the candidate, receipt, checks and actual media proof.
- Packet proof uses each real PTS (including B-frame decoder ordering). After-first ranges require exact keyframes even if raw bytes match; Annex-B fallback compares both ranges including parameters/SEI. The audio verifier rejoins candidate ranges on exact48k sample boundaries before the unchanged -35dB difference threshold/fulldecode/profile checks.
- Initial claim including BRANDING.md was refused because two unrelated stale tasks overlap that doc; no override was used. The task was narrowed to the four files, then claimed normally. Documentation of the new CLI option is in its usage string and this task.
- Two actual independent OpenAI Codex agents reviewed the diff; no Claude/human review is claimed. Their final findings (missing receipt timeline identity equality and non-keyframe raw-match risk) were fixed with rejection tests before final execution.
- Work logs outside repo: `/workspace/work/ai-animation-01/renewal-position-targeted-tests.log`; baseline99tests passed before new coverage, later111passed before final hardening. Final result to be recorded after actual run.

- Final verification: targeted114/114pass,0fail,0skip after preserving explicit `intro_at: "start"` and refusing unknown positions. Full docs-videos236/236pass. Full tools invocation completed with2746total,2735passed,6failed,5skipped; all6failures are unchanged a01-capture outside-Git fixtures returning OUT_INSIDE_REPOSITORY/CAPTURE_INSIDE_REPOSITORY because this round's managed sandbox exposes synthetic `/tmp/.git` and `/workspace/.git` ancestor directories. A focused unchanged capture-test reproduction gives the same failures. No guard or synthetic path was weakened/removed and no path trick was attempted. This is an environment limitation, NOT a full-suite pass. The final one-line placement fix and new rejection coverage were independently retested114/114.
- Final source SHA: renewal.mjs `c839d16d387f26c623ae6b249c6682e0bb47ebc1fbd55b34d2158fd1a39a88ca`; renewal-handoff.mjs `871fb86a0d6f9097632ddc74a655f647168b44d660bd892f92e332c291bde29c`. No commit was made by this delegate.
- Actual full candidate exercise by independent audit_intro_outro_reference also passed:17687retained body packets, raw-packet-exact at934, audio difference−59.79dB, full AV decode615.566667s. This is actual media evidence, separate from static code review and synthetic tests; work report `visual-qa/independent-native-retained-media.json`.
