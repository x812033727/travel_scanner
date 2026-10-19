# A01 integration with main #1577 — 2026-10-19

Status: **r47 successor prepared; merge approval, CI and production gates remain separate**.

PR #1590 at `f43fef783a667eddac177aa9e26d6c8620997f01` passed all 21 GitHub
checks and received merge-only approval against main `63288d02`. Before merge,
main advanced to `14f4c469dda55092380bc9e1a2840b9808015daf` through #1577.
The PR was therefore behind under strict branch protection; its API base SHA
still showed the earlier main, while the remote branch and comparison API
confirmed the new commit. No merge was attempted.

## Local integration check

The local rebase to `413c8d303e85022686481ae3e33e18cbfbc80ad4` preserves every
artifact and pilot-task byte from `f43fef783`. #1577 changes the dependencies
used by the artifact builders: `lint.mjs` now chooses `TIGHT_CADENCE` for a
story, and `narrative.mjs` measures a 45-second interval. This is a real
compatibility difference despite the absence of overlapping edited paths.

The r45 `build.mjs --check` exits 1 at its assertion that narrative warnings
are empty. It reports these five gaps on the current estimated lint timeline:

| From | To | Reported gap |
| --- | --- | --- |
| 00:50 | 02:10 | 80 seconds |
| 03:02 | 03:52 | 50 seconds |
| 03:52 | 04:41 | 49 seconds |
| 04:41 | 05:55 | 75 seconds |
| 06:44 | 07:41 | 57 seconds |

The canonical r45 handoff `build.mjs --check` also exits 1, reporting stale
`metadata-delta.json` because its lint result changed. Neither command writes
the frozen package. These are estimated text-timeline results, not measured
audio or viewer-retention evidence.

## Correction boundary

Retain r44, r45, their source material, original owner choice and all historical
reviews. Prepare a narrow r46 successor that preserves the chosen Rollaboard
story and source-backed events, while giving each affected interval a meaningful
question or reveal with a real payoff. Record each narrative and mapping delta,
then obtain independent reader and source/mapping review. Do not relax the new
cadence check or reinterpret historical PASS reports as current-main receipts.

The owner's A01 420–480 second narration exception remains applicable; the new
skill's generic ten-minute target does not override that direct decision.
## Independent reader outcome

R46 manifest `d6b9e59358d7616a97c333368b6533f5f45745f5625887276e91a2095df6d794`
passes the current 45-second cadence check. Its two independent readers still
identified narrative problems: the opening disclosed the remove-and-stow result,
the final chapter switched from size to a zipper aside, and it repeated known
zipper/stow information while posing an already answered question.

- Reader A: 10/13 overall and 9/12 required answers yes.
- Reader B: 9/13 overall and 8/12 required answers yes.

The exact reports remain beside the frozen r46 manifest. The source-delta PASS
is bounded to unchanged factual content and does not override those narrative
failures. The r47 correction below supersedes r46; r46 is not an adoption input.

## Reviewed r47 successor

R47 editorial manifest is
`323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e`;
canonical handoff manifest is
`3edb9c375bcef6b01adc4e7bd14eec3757dd907d16a175247f8468a063465fb2`.
It changes six lines, moves the final chapter marker to now-aisle and removes
the redundant now-answer/r44l050/q055 summary. Both r46 reader reports remain
untouched. The surviving 54 claim rows and 50 illustration prompts remain
identical; all three original outro sentences remain. The independent reader
reports and bounded source-delta review are next to the frozen r47 manifest.
Both independent readers returned 13/13 yes, including all 12 required answers,
with no remaining or new P1/P2 narrative findings. The separate canonical
handoff review also passed its bounded conversion checks. None is a formal
worker verification or media approval receipt.

The canonical handoff has six chapters, 50 scenes, 52 narration lines and 54
PENDING claims (15 semantic plan links, 39 passage-only). Actual parser
normalization changes now-zipper to turn-01; q047 becomes t12, q048–q054 become
n1–n7, and q055/n9 is removed. Separate handoff review checks this conversion.

Both new builders pass current-main checks, with zero lint errors and 39/38
warnings respectively. All three estimated speeds pass tight45. Body estimates
are 450.4/414.1/383.0 seconds at 250/275/300 CPM. The 275 CPM estimate falls below
420 seconds; actual audio has not been made and the 420–480-second gate remains
unpassed. Frozen manifests retain their creation-time review-pending statuses;
later reviews bind them externally without changing those identities.

Main later advanced to `e2f2bc800d43b4f9914f965a68a89d3eed068eb8` via #1589.
Its flow/automation test and long-form review changes do not alter the hashed
dependencies of these offline builders. Runtime adoption still needs a current
flow/review inspection; this observation is not a production receipt.

Changed content requires renewed exact-head merge approval after review and CI.
No deployment, host write, paid generation, import or upload occurred here.
