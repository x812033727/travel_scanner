# A01 r46 canonical offline six-chapter handoff

Status: **HOLD — new r46 narration and handoff awaiting independent review**. Editorial r46 manifest: `d6b9e59358d7616a97c333368b6533f5f45745f5625887276e91a2095df6d794`. Prior canonical r45 manifest: `73cf375736d13a899e261000d1ad694f876e4f1101e2e9454210c1063dd9e4e4`. Its independent review remains historical; it does not approve r46. All existing r44/r45 files and reports are untouched.

## Exact derivation

The actual current worker parser, pure numberClaims helper and composeStory build six chapters from r46. This preserves 51 scenes, 53 narration lines, eight loop pairs, six public URLs and all 55 claim/source/fact mappings. Fifteen claims remain plan-linked; forty retain fact:null for passage verification. The semantic map is byte-identical to r45; all verdicts remain PENDING. Source equality never substitutes for a semantic fact match.

The build compares each new chapter against its frozen canonical r45 chapter after restoring the five authored narration changes and previous loop table; everything else must match, including all claims, canonical IDs, scene IDs, prompts and manual thumbnail choice. Claim IDs are h1-h8, o1-o10, i1-i7, e1-e10, t1-t11, n1-n9. The real helper is tested again with empty and existing prior rows.

The same title, voice, characters, source URLs and lexicon are retained. The selected now-stow-fail thumbnail still uses the approved explicit line break. The actual composer output is not patched. metadata-delta.json records 55 q-to-canonical ID substitutions, the existing 12 metadata and two representation differences, and exact prior/current per-chapter loop/narration changes. Older source dates remain historical, not fresh checks. Description/tags/source-title/date/layout differences still need a publication decision.

## Current checks and limits

Run build.mjs --check. It verifies all source/output hashes, actual parser normalization, schema, story, cute visuals, lint and the 45-second cadence at 250/275/300 CPM. No lint errors or cadence gaps are permitted. The body estimate at 275 CPM must be 420–480 seconds; real TTS remains unmeasured and may be shorter. These mechanical checks do not replace independent story/source review, real chapter verifier/listener outcomes or audio review.

- hook.thumbnail_shot intentionally points to the later now-stow-fail scene. The hook writer parser strips/rejects that cross-chapter choice; the manual wrapper must preserve and reassert it. composeStory accepts it across the merged scene set.
- readChapterAnswer strips claim IDs/verdicts. Canonical PENDING rows are restored locally; real checkChapter/checkedRows preserves them only if the verifier returns each surviving row's input ID unchanged. Added/dropped claims, missing/duplicate IDs or a writer rewrite void that assumption.
- No auto.json, written/checked/listened state, verifier receipt, listener result, formal script-review JSON or approval is created. Copying these files does not update the live worker state and can trigger a rewrite on retry.
- The inherited hands_off flag is not permission to enable automation. Owner approval of the Rollaboard direction and A01 duration exception does not approve r46 production. Fresh host/admission evidence, the adoption wrapper, independent reviews and real audio/media gates remain required. No host/network/paid operation runs here.

Independent reports must bind this new manifest separately and are not hashed as generated inputs.
