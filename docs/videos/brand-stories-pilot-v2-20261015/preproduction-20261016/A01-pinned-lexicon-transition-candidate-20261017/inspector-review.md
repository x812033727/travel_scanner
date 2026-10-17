# Independent offline inspector increment review

Reviewer: `codex-independent-a01-lexicon-1017`. Date: 2026-10-17 (Asia/Taipei).

Verdict: **PASS within this narrow read-only inspector increment; 0 P1 / 0 P2 found. Production remains HOLD.** This report supplements `independent-review.md` and preserves that historical review unchanged. It is not authorization JSON, an owner receipt or proof of a genuine 81st event.

## Reviewed files

| File | SHA-256 |
| --- | --- |
| inspect-pinned.mjs | a5c04757fbc8c67e922bcd4ce0477bf433482bcc1df8a4d00b4037f347ac55a6 |
| transition.test.mjs | 10a790fd84e481a45dce9b9ccb205e100e8a35bd6e438a7ac9efa84a9f57cb55 |

Also confirmed the three original runtime/fixture hashes still match the earlier report: transition.mjs `a2944f89e60f18a58d1c2b7b84dfa0cd75bfda2174b349d04cd654f65081929a`; snapshot-format.mjs `a666d5e74b3ce450fc8d8bc52c97626c1a7eb3cd30b31ef0867442a6a6ed2b95`; synthetic-fixture.mjs `f401f0265c80a7294eeb9f6fa7de1ed0b942f8fc00813f3d1575eacdcddd0766`.

## Findings and executed checks

The inspector delegates exact captured-transition verification to the existing `verifyPinnedTransition`. Success adds `inspection: EXACT_PINNED_CAPTURE_PASS` and `release_allowed: false`; the underlying result still carries production HOLD and installation/paid false. Failure emits only an uppercase error code or `PINNED_CAPTURE_INVALID`, never the caught message, stack, source JSON or chapter/state contents. The CLI accepts exactly the three ordered before/after/historical-file flags, rejects extra or write-like arguments and emits a structured HOLD report on malformed arguments. It contains no file-writing or production action path.

Independently ran bundled Node 24.19 `node --test transition.test.mjs`: **5 passed, 0 failed**. The revision now includes an explicit changed-review fixture, retaining the old receipt hash and requiring rejection; it also checks success HOLD flags, incomplete capture HOLD, argument rejection, and a spawned CLI --apply process with exact exit 2 and JSON HOLD assertions. The suite was independently rerun after this final CLI assertion was added, again 5/5 passing. Existing historical-evidence, partial-publication/shared-drift and state-preservation cases remain green.

Independently invoked the real CLI with `--apply` via Node `spawnSync` to inspect its exact child exit status: **2**, stdout is only a JSON HOLD report with `INSPECTION_ARGUMENTS_INVALID`, and stderr is empty. PowerShell's outer command can report a different native-command wrapper status; the child status above is the directly observed CLI code. Parse-error data suppression was inspected in code; no new claim is made that a separate malformed-chapter CLI fixture was executed.

## Limits

Success proves the supplied local before/after capture matches the offline exact-transition verifier; it does not authenticate receipt identities, establish owner authorization, resolve the uncertain job, enforce atomic docs/work publication or release production. No actual production 81-event capture was supplied or created during this increment review. The actual-capture plan SHA and original 80-event read-only evidence remain documented in the earlier review and were not reclassified as installed evidence. A fresh capture, guarded adoption/recovery protocol, deployed pinned-source reader, revised 81-to-82 narrative transition and the remaining content/media gates are still required.

This review changed only this new Markdown report. It did not modify implementation, historical review, host files, paid state, branches or merge/deployment state.
