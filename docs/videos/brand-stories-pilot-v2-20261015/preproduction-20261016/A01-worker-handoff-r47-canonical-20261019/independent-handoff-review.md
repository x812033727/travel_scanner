# Independent review of A01 r47 canonical handoff

Reviewer: `a01_r46_reader_a`. Date: 2026-10-19. This reviewer did not author the canonical builder, chapters, claim mappings, or metadata delta. The review was read-only apart from creating this report.

## Bound inputs and result

| Artifact | SHA256 |
| --- | --- |
| This canonical package's `manifest.json` | `3edb9c375bcef6b01adc4e7bd14eec3757dd907d16a175247f8468a063465fb2` |
| Frozen r47 editorial `manifest.json` | `323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e` |
| Previous r46 canonical `manifest.json` | `0277e782be1b99b93cff70f51f01a771b4ec9f3b2b36b34c146fadd1a4a11378` |
| Reviewed canonical `build.mjs` | `a085e4352602c33633b58137cc08350028e4d2ec6a051be26bb058565b8c4e61` |
| Authored `semantic-fact-map.json` | `5623151453e32902d90e8fb67820c7e4c374a477cdd0e271b4674f39e17c8349` |
| Actual worker `numberClaims` helper source | `e1c9bea7bfb065c63d28bbda099679757b10901ee606faf6b8a7e64638e58cbe` |

**PASS for offline canonical conversion fidelity. No unexplained P1/P2 conversion defect was found.** The six chapter files and the actual `composeStory` result preserve the frozen r47 story content under the declared scene/claim ID mappings. All 54 claims remain **PENDING**: 15 carry a plan-fact relationship, and 39 retain `fact: null`.

**This is not a formal historical verifier result, worker narrative receipt, script-review approval, duration approval, or host-import approval.** The package remains an offline handoff with `duration_gate_passed: false` and `host_import_or_paid_media_authorized: false`. Nothing in this review promotes a claim to `PLAN` or `CONFIRMED`, writes worker progress, or permits reuse of old approval receipts under the changed IDs.

The canonical directory is `docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019`. Sibling editorial and prior canonical directories are identified by the bound manifests above. All paths below are relative to the repository or package, as indicated.

## Material read and executed

Read the canonical builder, all six actual `story/chapters/*.json` files, `claim-map.json`, `claim-id-map.json`, `semantic-fact-map.json`, `fact-mapping.md`, `series.json`, `metadata-delta.json`, the manifests, and README. The complete frozen r47 manuscript and `video.json` had already been independently read for the r47 narrative report and were loaded again for exact comparison here. The current worker implementations of `chapterSceneIds`, `readChapterAnswer`, `numberClaims`, and `composeStory` were read directly in `tools/video/automation/story.mjs`.

Executed from the repository root:

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019/build.mjs --check
```

**Actual exit code: 0.** Output reported the assigned canonical manifest SHA256, six chapters, 50 scenes, 52 lines, 54 canonical PENDING claims, 15 plan-linked / 39 passage-only rows, 12 metadata differences, three structural representation differences, zero lint errors, and **38 lint warnings**. The command ran in `--check` mode; the builder's `--write` branch was not invoked.

Separate read-only assertions, independent of the builder's result summary, checked:

- The manifest hash, all frozen canonical output hashes, builder and semantic-map hashes, and every declared worker dependency hash.
- Every actual chapter scene and claim through the current `readChapterAnswer` parser, allowing the parser's documented stripping of claim ID/verdict fields.
- All 54 rows against frozen r47 `candidate/claims.md`: claim text, source URL, scene mapping, source index, fact relationship, and PENDING state.
- All scene data, narration objects, line IDs, templates, scene order, chapter markers, and claim membership against frozen editorial `candidate/video.json` after the explicit ID mappings.
- A fresh call to the actual `composeStory` with the six stored chapter files, producing an object deeply equal to `worker-composed-video.json`.
- Exact source-URL order and all eight loop setup/payoff/description triples, with loop array order allowed to differ.
- Complete editorial-to-worker object equality after applying only the 12 recorded metadata differences and three declared structural representation differences. **Unreported differences: 0.**

These checks produced PASS without writing temporary audit files or changing the frozen inputs.

## Parser, numbering, and composition

`readChapterAnswer` uses `chapterSceneIds` to retain unique scene IDs beginning with the current chapter key. For a scene assigned to `turn`, `now-zipper` does not match that prefix. The next free parser ID is therefore **`turn-01`**. The parser also rewrites the row's `scene` reference to the normalized ID. This is an actual parser result, not an arbitrary handoff rename.

The builder groups editorial scenes by the actual `chapter` markers. In r47, the final chapter starts at `now-aisle`; the preceding zipper scene belongs to `turn`. It passes the chapter's valid line-ID list to the parser, and `r44l042` stays unchanged. It asserts that parser normalization has not truncated or changed narration, prompts, camera data, or source/fact fields.

The writer parser returns claim content, source, scene, and fact fields, stripping ID and verdict. The builder consequently supplies canonical PENDING rows separately. It extracts and executes the current worker's pure `numberClaims` implementation, rather than copying a similar numbering algorithm. The helper assigns the chapter's prefix to noncanonical q-IDs and retains valid, unique canonical IDs on a later pass. The executed builder checks both an empty previous-row list and existing canonical previous rows.

`composeStory` walks the six chapter keys in order, puts each chapter title on its first scene, and attaches claim IDs by each row's normalized scene. It filters only `NOT FOUND` claims, so the present PENDING rows remain references; inclusion is not verification. The rebuilt result agrees exactly with the stored worker composition.

## Six chapters and exact migration

| Chapter | Scenes | Lines | Claims | Plan-linked | `fact:null` |
| --- | ---: | ---: | ---: | ---: | ---: |
| hook | 5 | 5 | 8 | 4 | 4 |
| origin | 9 | 9 | 10 | 1 | 9 |
| idea | 6 | 6 | 7 | 3 | 4 |
| engine | 10 | 10 | 10 | 4 | 6 |
| turn | 12 | 12 | 12 | 2 | 10 |
| now | 8 | 10 | 7 | 1 | 6 |
| **Total** | **50** | **52** | **54** | **15** | **39** |

| Editorial identity | Previous r46 worker identity | Current r47 worker identity |
| --- | --- | --- |
| `now-zipper`, narration `r44l042` | First scene of `now` | Last scene of `turn`, parser ID `turn-01`; narration ID/text preserved from r47 |
| q047, zipper claim | n1 | **t12**, scene `turn-01`, source 5, fact null |
| q048 | n2 | **n1**, `now-aisle` |
| q049 | n3 | **n2**, `now-cabin-edge` |
| q050 | n4 | **n3**, `now-stow-fail` |
| q051 | n5 | **n4**, `now-pocket` |
| q052 | n6 | **n5**, `now-space` |
| q053 | n7 | **n6**, `now-empty` |
| q054 | n8 | **n7**, `now-verdict` |
| q055 / `now-answer` / narration `r44l050` | n9 | **Removed**, matching the frozen r47 deletion |

All earlier claim identities remain unchanged: h1–h8, o1–o10, i1–i7, e1–e10, and t1–t11. The current `now` chapter has n1–n7 and no n8/n9. q055 is absent from the current claim-ID map, semantic map, claim rows, and composed scenes. The former summary's underlying fit/removal facts remain represented by the retained ending claims and narration.

The builder also restores the declared r47 changes in memory—six narration edits, zipper scene ownership, prior claim IDs, deleted summary, and loop descriptions—and compares the entire restored chapters with frozen r46. Its successful `--check` confirms that declared successor relationship; it does not establish the historical truth of either manuscript.

## Claim and fact semantics

All 54 complete claim texts and their source-URL relationships match frozen r47. The retained semantic decisions equal the preceding canonical semantic map with q055 removed; the change in chapter ownership did not turn q047 into a plan fact or change the semantic decisions for q048–q054.

The plan links represent these statement relationships:

| Plan fact index | Linked editorial claims | Relationship checked offline |
| --- | --- | --- |
| 0 | q004, q010, q019 | Undated checkpoint account, difficult separation, and the missing physical bridge to the integrated product |
| 1 | q006, q020, q025, q029 | Company product account, early crew adoption, and garage-to-warehouse growth |
| 2 | q007, q026 | Other pilots seeing the product and asking Plath to make one |
| 3 | None | The patent rows retain null because their specific details exceed the short plan statement |
| 4 | q033 | The attributed Sharkey account and crew/passenger observation |
| 5 | q001, q035, q041, q046, q049 | Dash's test cohort and the specific commercial-case loading/storage problem |

These are semantic associations with provided plan statements, not findings that every detail in a compound claim has been independently proved. In particular, **q003 remains null**: Plath's repeated heavy carrying is not the same assertion as fact 2's colleagues requesting cases. **q054 remains null**: Dash's final preferred products are not established by fact 5's test/fit summary. The retained null decisions for zipper performance, exact pocket details, quotes, test methods, and personal experiences likewise preserve the need to inspect source passages.

Each null row still has its concrete source index and corresponding URL. `fact:null` therefore means “no complete plan-fact shortcut established for this row”; it does not mean false, unsupported, excluded from review, or already verified. All canonical chapter verdicts and mapped row statuses remain PENDING, including the 15 linked rows.

The key narrative boundaries remain intact in both text and prompts: the undated screw-fixed hard-case/trolley sample is distinct from the later integrated product, the physical modification history is not supplied, the 1989 patent is not a first-sale date, and the 1993 commercial case belongs to Dash's reported test. The category-level aisle statement is not converted into a witnessed step-by-step itinerary for her individual case. This review did not open external sources or issue a new source-check date.

## The 12 metadata differences

The following are the complete metadata allowlist. Each recorded before/after value was checked against the actual editorial and worker objects, then the remaining whole objects were compared for equality.

| Path | Actual change and boundary |
| --- | --- |
| `youtube.description` | Composer uses `info.logline` plus `plan.question`; the longer editorial description's provenance and illustration caveats are not reproduced there. This is a real publication-text difference, not exact text preservation. |
| `youtube.tags` | Composer derives tags from subject/category/names; the editorial hand-picked tag list changes. |
| `thumbnail.data.headline` | `會滾卻放不下？` becomes `會滾\n卻放不下？`; words and punctuation are preserved, with a layout break. |
| `sources[0].title` | ABC label changes to the plan publisher wording, including USA TODAY attribution. |
| `sources[0].checked_on` | `2026-10-18` becomes the plan's `2026-09-28`. |
| `sources[1].title` | Detailed Travelpro description becomes `Travelpro`. |
| `sources[1].checked_on` | `2026-10-18` becomes the plan's `2026-09-28`. |
| `sources[2].title` | Global Traveler title takes the plan wording and 2007 interview label. |
| `sources[3].title` | Patent title takes the plan's applicant wording. |
| `sources[3].checked_on` | `2026-10-18` becomes the plan's `2026-10-16`. |
| `sources[4].title` | RNPA title takes the plan wording distinguishing Sharkey p.48 from the research-only Emmer material. |
| `sources[5].title` | Los Angeles Times label takes the plan's author/date wording. |

All six URLs and their order are unchanged. The video title and selected thumbnail scene are exact. The changed dates are inherited metadata, not new research receipts. Description, tags, and source-label/date differences remain an explicit publication decision; this offline conversion review does not silently approve replacing the editorial publication text.

The three additional structural representation differences are separate from those 12 metadata entries:

1. Loop array ordering changes with chapter composition; the eight setup/payoff/description triples are identical.
2. `scenes[41].id` changes from `now-zipper` to `turn-01` under the parser rule above.
3. The empty `claims: []` property on the final outro is omitted by the composer; neither form assigns a claim to that outro.

The 54 scene claim references also change from q-IDs to the canonical IDs exactly as the map specifies. No narration, picture prompt, camera field, scene placement, chapter title, or source URL changes beyond the declared representation rules were found.

## Checks that remain open

- **Formal checking:** No current worker verifier was run. No checked/listened state, `verify-1.md`, formal script-review JSON, or owner approval was created. The independent r47 narrative report remains a separately bound editorial review; it is not manufactured into a worker receipt by this conversion.
- **Actual duration:** Manifest and metadata retain `duration_gate_passed: false`. Body text estimates remain 450.4 / 414.1 / 383.0 seconds at 250 / 275 / 300 CPM. Actual narration must satisfy the existing 420–480-second requirement; this review does not approve an estimate or prescribe padding.
- **Diagnostics:** The run has zero lint errors but 38 warnings: five long narration lines, one missing-shot-size aggregate, three recurring-style-word aggregates, 14 estimated long-shot warnings, and 15 craft diagnostics. They were not removed or waived by the conversion. Zero schema/story/cute-visual errors and zero estimated tight45 cadence problems are structural results, not finished-media quality or playback evidence.
- **Cross-chapter thumbnail:** `hook.thumbnail_shot = now-stow-fail` is deliberately supplied after chapter parsing. The hook-only parser cannot preserve that later-chapter choice, while the merged composer can. Any eventual guarded adoption route must preserve/reassert it; this report does not authorize that route.
- **Claim identity at adoption:** Current n1 is former q048, while former n1/q047 is now t12. A future verifier/adoption path must use this bound map and current rows. Reusing old n-ID receipts or incomplete verifier responses would not be justified by the successful empty/existing-row helper checks.
- **Host admission:** No runtime `auto.json`, scheduling, imported project, upload package, paid asset, or host operation was created. `hands_off` in an inherited series file is not operational authorization. Copying this offline package alone is not demonstrated to be a supported host import.

The observed holds are explicit and consistent with the package's purpose. Within the assigned offline-conversion scope, no unexplained content loss, source/fact remapping, or hidden metadata change remains. Only this hash-bound independent report was added.
