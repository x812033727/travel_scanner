# Independent offline six-chapter handoff review — A01 r45

- Reviewer: `/root/a01_r45_handoff_review` (independent technical reviewer; did not author this handoff).
- Reviewed: 2026-10-19, checks completed at 07:02 UTC.
- Verdict: **CHANGES REQUESTED — one P2 fact-index mapping defect. HOLD remains in force.**
- This is a technical, offline handoff review, not a historical-source verdict, formal chapter verifier/listener result, script approval, host-import approval, or final-media approval.

## Frozen evidence

| Item | SHA-256 / revision |
| --- | --- |
| Handoff `manifest.json` | `b5191f765a719bfac408b317c3d8edbd073884b1cf527a4e89a7c5443c3ceab3` |
| Frozen editorial r45 `manifest.json` | `4bba4d5b429b6de634c3982aa01027b1d0befd84664aef640d533af0302d05ac` |
| Handoff `build.mjs` | `8cd6a76c0d7a84e209125174af71a544d98131091ef2fcf20c96e2c28155def8` |
| `worker-composed-video.json` | `4fad9d8a3948d133acb66ff0fab7021ef2e1d4e9dcec497fa4bef56e50a12011` |
| Main / local HEAD inspected | `e42d93979781b250b53f93e36ff1c901679b39ce` |
| Current `tools/video/automation/story.mjs` | `db7afddc854f6f106fb7198d8f2634ad15f9e6eb5fe8c295efc604413c8ed179` |

I checked all manifest-listed output hashes, all five recorded worker dependency hashes, the build hash, frozen-manifest identity, and lexicon/brief byte equality. The recorded worker files were unchanged from the inspected main revision. I ran the handoff `build.mjs --check` successfully and separately loaded the saved six chapter files, independently compared them with frozen r45, called the real `readChapterAnswer`, `composeStory`, `validateVideo`, and `lintVideo`, and compared the actual composition deeply with the saved worker output. No generated input or output was modified during this review.

## Required correction

### P2 — Do not infer a plan-fact relationship solely from a shared source

At `build.mjs:104–106`, `matchingFacts` selects every `must_verify` row sharing the claim's source index, asserts there is exactly one, and writes that row's index as `fact`. The six plan facts happen to use disjoint source indices, so the assertion passes for all 55 claims even where their statements are different. This proves a source relationship, not the semantic fact relationship the worker expects.

The current worker prompt (`tools/video/automation/story-prompts.mjs:162–163`) defines `fact` as the index of the fact being told, or `null` for a statement added from a source passage. The verifier distinguishes established plan facts from additional statements that must be found in a passage (`story-prompts.mjs:180–202`). The supplied indices therefore have operational meaning beyond routing to a URL.

Two concrete examples:

- `hook.json:99–104`, q003: “Ballis 2007 受訪稱 Plath 日復一日提著沉重行李穿過航站。” is assigned `fact: 2`. Plan fact 2 instead describes other pilots seeing Plath use a wheeled case and asking him to make one, plus a warning about relative dates. It does not state the daily heavy-luggage account.
- `now.json:221–226`, q054: Dash preferred **two** named cases, Travelpro Rollaboard and American Tourister Commuter, is assigned `fact: 5`. Plan fact 5 covers mail order, four-brand tests, earlier wheeled-device experience, and exterior-pocket overload/stowing. It does not state that two-product preference.

These claims remain PENDING and retain the correct source URLs; this finding does not say their historical claims are false or already approved. It means the handoff must not label them as the same pre-existing plan fact merely because they came from the same article. Before using this handoff for a formal worker input, use an explicit, reviewed per-claim fact mapping, with `null` where no matching plan fact exists. Retain the source mapping and PENDING status. Recheck all 55 entries, and update the “unique matching must_verify fact” assertion/documentation accordingly. Merely checking that `plan.must_verify[fact].sources` contains the source does not test this defect.

## Checks that passed

| Chapter | Scenes | Narration lines | PENDING claims | Complete loop pairs stored here |
| --- | ---: | ---: | ---: | ---: |
| hook | 5 | 5 | 8 | 0 |
| origin | 9 | 9 | 10 | 1 |
| idea | 6 | 6 | 7 | 0 |
| engine | 10 | 10 | 10 | 2 |
| turn | 11 | 11 | 11 | 2 |
| now | 10 | 12 | 9 | 3 |
| Total | 51 | 53 | 55 | 8 |

- All six chapter keys, their order, titles, scene ownership, and narration-line ownership match the frozen editorial structure. The 51 scene IDs and 53 line IDs are unique. All narration objects, picture prompts, scene data, and scene claim membership match r45; no cross-chapter scene or claim was misplaced.
- All 55 q-IDs, claim text, scene IDs, source indices and source URLs match the frozen claim table and source alignment. They have exactly `PENDING` verdicts. No CONFIRMED/PLAN/checked/listened result was manufactured. **This structural pass does not waive the semantic fact-index defect above.**
- All eight setup/payoff/what tuples match. Each setup and payoff is a real spoken line, payoff comes later, and each pair is stored in its payoff chapter. The actual composer retains all eight pairs; only their array order changes. Empty loop arrays on hook/idea do not lose the opening hooks in this complete six-chapter composition.
- The actual composer output equals the saved `worker-composed-video.json`, not a post-composition rewrite. It retains the title, voice, characters, six public-source URLs, selected `now-stow-fail` thumbnail shot, `cute-mystery` look, switchable subtitles, and the A01 `[7,8]` target.
- Current schema/story/lint/cute checks return zero errors. Lint has **39 warnings**, matching the declared result: five long-line warnings, one unnamed-shot-size summary, three repeated-style-word summaries, fifteen long-shot warnings, and fifteen craft advisories. These are not evidence that timing, visuals, or finished-media quality has passed. The thumbnail word-split warning is absent.
- The only series-file difference from frozen r45 is the headline's explicit newline. Lexicon and brief are byte-identical.
- Fifteen package files were present before this report. There was no `auto.json`, `verify-1.md`, or formal `script-review.json`. Chapter objects contain no fabricated checker report, listener state, or approval state. The existing nested `series.hands_off: true` was inherited unchanged from the frozen plan; it is configuration, not a new authorization or proof of safe runtime state.

## Metadata delta and future wrapper conditions

The 12 metadata differences and two representation differences are accurately disclosed in `metadata-delta.json`: YouTube description and tags, headline newline, six source display titles, three source-check dates, reordered loop array, and absent-versus-empty outro claims. They are deterministic consequences of the inspected composer and series input. The new description is shorter and omits several editorial caveats; the displayed check dates for sources 0, 1 and 3 come from older plan metadata. They should be consciously resolved before publication/import, as the README already requires; this review does not treat the older dates as fresh source checks.

The later manual wrapper must also handle these actual worker behaviors:

1. `hook.thumbnail_shot = now-stow-fail` is accepted by `composeStory`, but re-running `readChapterAnswer` on hook drops it because it is not a hook scene. I reproduced this: the normalized hook has no thumbnail selection. Preserve and reassert the reviewed manual choice after normalization; the README already identifies this condition.
2. `readChapterAnswer` deliberately strips claim IDs and verdicts. In the actual verifier path, `checkedRows` then calls `numberClaims`, which accepts only a chapter prefix (`h`, `o`, `i`, `e`, `t`, `n`) plus digits; imported `qNNN` IDs will be renumbered on a normal check. The offline q-IDs are preserved here, but are not stable formal-worker IDs. A wrapper must preserve a correspondence and bind the real later receipts to actual recomposed IDs/hashes; it must not reuse a q-ID-bound receipt after renumbering.
3. Existing chapter files alone do not mark a chapter as written: `advanceStory` checks the persisted chapter entry's `written` count and may invoke a writer when it is false. This package correctly does not invent that runtime state. A reviewed adoption wrapper must reconcile live state rather than merely copy files and retry.
4. Real chapter verification/listening may patch text, drop lines, or renumber claims. Any such change needs subsequent recomposition, mapping checks, current narrative review and the appropriate hash-bound pilot script review. Local deterministic recomposition is not a substitute.

The legacy `ALTERNATE_PROPOSAL` caveat remains in the inherited frozen plan while the newer series note records the owner's adopted direction; this is preserved provenance, not a new editorial rejection. The eventual adoption package should state its effective status clearly without changing historical receipts.

## Limits and actions

No host command, network source fetch, model call, TTS, image generation, state mutation, deployment, upload, or paid operation was performed. This review does not attest fresh source availability, account budget, live lock/admission state, actual 420–480 second narration, soundtrack, animation, CC synchronization or final playback. Only this report was added. The reviewed frozen artifacts and their manifests remain unchanged. The P2 fact-index defect must be corrected in a new reviewed handoff revision before this input is considered ready for a formal wrapper; all production/media gates remain HOLD.
