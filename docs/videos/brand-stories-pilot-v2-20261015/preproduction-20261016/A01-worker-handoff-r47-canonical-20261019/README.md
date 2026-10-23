# A01 r47 canonical offline handoff

Status: **HOLD — narrative review and actual duration have not passed**.

Editorial manifest: `323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e`. Prior r46 canonical manifest: `0277e782be1b99b93cff70f51f01a771b4ec9f3b2b36b34c146fadd1a4a11378`. The prior handoff is a frozen input; this build does not claim that it had an independent review. Both failed r46 narrative reports remain unchanged and do not approve r47.

## Exact conversion

The current `readChapterAnswer`, actual pure `numberClaims` and `composeStory` build six chapters, 50 scenes, 52 narration lines, 54 PENDING claim rows and eight loop pairs. All retained claim text, source/fact relationships, public URLs, prompts and lexicon stay unchanged. Fifteen claims remain plan-linked and thirty-nine retain `fact:null` for direct passage checking. Removing q055 removes a duplicate summary, not its underlying facts.

The last chapter now starts at `now-aisle`. The preceding zipper scene stays in its original chronological position but belongs to `turn`. The actual writer parser assigns its `now-zipper` ID to `turn-01`. Its narration ID remains r44l042, its claim remains q047 in the editorial map, its source is index 5, and its fact is null. Canonical q047 changes from n1 to t12; q048–q054 change from n2–n8 to n1–n7. q055 / n9 / now-answer is removed. The other canonical claim IDs are unchanged: h1–h8, o1–o10, i1–i7, e1–e10, t1–t11. Exact maps are in claim-id-map.json and metadata-delta.json.

The build tests normal `numberClaims` again with empty and existing previous rows. It also restores the six previous narration lines, the zipper scene/claim ownership and original IDs, removed summary scene/claim, and previous loop descriptions, then compares every complete chapter with frozen r46. This is an equivalence check of the declared delta, not a historical verifier verdict.

The actual composer output is not patched. Apart from the documented scene-ID and canonical-claim-ID conversions, it reproduces editorial narration, scene order, chapter markers, prompts and loop content. Existing composer differences in description, tags, source titles/dates and thumbnail line break are listed separately. They still need a publication decision; old source dates do not become fresh checks.

## Checks and remaining gates

Run `node build.mjs --check`. It verifies frozen hashes, actual parser normalization, schema, story, cute visuals, lint and 45-second cadence at 250/275/300 CPM. Body estimates are 450.4 / 414.1 / 383.0 seconds. The 275 CPM estimate is below 420 seconds. `duration_gate_passed` is false; actual body audio must still satisfy 420–480 seconds. No padding, slower delivery or artificial pauses were added.

- `hook.thumbnail_shot` intentionally selects the later `now-stow-fail` shot. The hook writer parser cannot preserve this cross-chapter selection; an eventual manual wrapper must preserve/reassert it. The composer accepts the merged scene selection.
- The writer parser strips claim IDs/verdicts. This offline conversion restores canonical PENDING rows. Real verifier handling preserves those IDs only if it returns every surviving input ID unchanged; missing, duplicate, added or dropped rows invalidate that assumption.
- No worker `auto.json`, written/checked/listened state, verifier receipt, listener result, formal script-review JSON or owner approval is created. Copying these files alone cannot authorize adoption or prevent a retry from rewriting chapters.
- The inherited hands-off flag is not permission to enable automation. Fresh host/admission evidence, a guarded adoption wrapper, independent narrative/source review, real audio duration and final-media review remain required. No host, network or paid operation runs here.

Independent reports bind this manifest separately and are not included as generated inputs.
