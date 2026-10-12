# H03 English, Japanese and Korean delivery

**EN/JA/KO language delivery is complete for the existing private video `b98IdS1MB78`.** At 2026-10-12T08:13:32.505Z, Studio shows all nine components Published: three audio tracks, three CC tracks and three title/description localizations. Formal audio, native captions/package, approved backend consumer and exact saved Studio text checks all pass. The video remains private under the completed sync; Published here describes its language components. Full player playback and human listening were not performed. Repository handoff: [draft PR 1469](https://github.com/x812033727/travel_scanner/pull/1469), stacked on PR 1456.

The owner authorized metadata, CC and dubbing for all three languages on existing video `b98IdS1MB78`; all nine selections are bound into the approved consumer. Original production is the completed PR 1456 handoff at `2c921b1be0381c4a003bc7fadd08b1952f273346`. This isolated branch preserves the stale untracked 3a3c source.

## Preserved source and cut

| Artifact | SHA-256 / binding |
| --- | --- |
| Current `video.json` | `e73f4c2de44b178c391c59a9c9c603823b5b34f175a55313f8995c04ac765def` |
| Original final, 694.3 seconds | `e786669f5a392fde7f281c617c28f885d25df8b13535b4a37f9e2ae6eaea304e` |
| Original Traditional Chinese CC, 139 cues | `4cf72b2f0d02fe8ff88ff777cc8777e2d2a3f4864ea742949a699fde6e521c59` |
| Unchanged speech / visual hashes | `cba1834e2d1021c3` / `f81bccf24595cb3b` |

The only source edit removes the obsolete Traditional-Chinese-only sentence from `youtube.description`. Spoken lines, scenes, timing, visuals and original final bytes remain unchanged. Native publish renewal and the new language manifest now bind that description change to the same approved final; no replacement final render was needed.

## Reviewed translations and final media

Independent reviews cover all 139 lines, seven chapters and metadata/thumbnail text per locale. Source-bound retake patches have exact-change native merge readbacks; earlier review bytes are retained in each review file.

| Locale | Current translation SHA-256 | Independent review SHA-256 |
| --- | --- | --- |
| EN | `f3820c77ac51a2aa0bd4832e004d5c811e362c7b6667901fcdb7388b9709a136` | `1cd2259c200c917a061d0c69fd8b818d3d7e96fb14e1e908ace8502660eb6db8` |
| JA | `748583eaf4e3330deba42a914e84f4583119cb54e7edeaa61477968dc61d158c` | `5c7aa8e32b18d18a7cbc90a9b69ad75e653c36a95a002ababa4ff3741dbbb2dd` |
| KO | `58adade451f948aac2163cb7f6276b375f3b9160600737269ec6f6b87df8fe67` | `73627a33ff8b173bb4bd4705f6411eabd5c8888690b83593be8e1811e2ad8c65` |

All three final M4A tracks are AAC, 48 kHz stereo, exactly 694.300000 seconds; full decode exits 0 with empty stderr. The final media verifier passes 1,595 checks with 500 stable input pins, binding each current raw clip and intended text to the formal result. Native measured-fit replay confirms 137 windows per locale, zero overruns and unchanged placements; maximum tempos are EN 1.02x, JA 1.19x and KO 1.13x under the native bounded policy.

| Locale | M4A bytes / SHA-256 | CC cues / SHA-256 |
| --- | --- | --- |
| EN | 24,630,715 / `c50e7dcdc5d8fb95e0322c8d46dbcae5812bb3581e95f8f9f1a7c3dc6a403256` | 139 / `d683b67863fb0785169c055d642f49ac4a60b96b18a24060577f6085a2aec981` |
| JA | 28,901,856 / `aea0c2a6ed9e13a125d17e29c9b5dc5fee399dd8a03ab9fe72719fccf6a9e345` | 147 / `587eadb6fcb7960572a5d0c15f0d14bc44a91a79525c5339369510d750f826ab` |
| KO | 24,667,866 / `be8f212e3cf6077d238f1a91d53582029bc735fdb02cf3d7aac8d395510ffe37` | 145 / `501c7ccbc09682b5a92f9165671635c775ce50be4544b01682af1cfc2dfa5b51` |

Caption readback passes 58 checks with 27 stable input pins: all 139 source IDs are covered in order, recomputed native SRT bytes equal the packaged copies, and no overlap, line-length, reading-speed or native caption problems remain. The five-second intro shift occurs once and all cues stay within the original cut. Both Traditional Chinese SRT copies retain the original hash. Native package validation passes all four items.

## Approved backend package

| Gate (approved) | Review ID | Content SHA-256 |
| --- | --- | --- |
| publish | `c367dccd-74a4-4723-aa1f-609d45402a6e` | `935f56ea391e9d39ed062d2db7460c945d5eec44e9e7dc3b1f70f0b1b058fbfe` |
| languages | `376730d3-8a8b-4155-be40-55903354fe4c` | `c1764ab94fb295a3c561a78dcdd348b610d5232f337ec4f2c09ed6e4cc2d6b95` |
| final | `385728b4-7bc8-4798-89fb-a5ea16102df8` | `e786669f5a392fde7f281c617c28f885d25df8b13535b4a37f9e2ae6eaea304e` |

The publish hash is the refreshed metadata content hash, not the final-video hash. The language content hash is the manifest hash. All 11 language attachments were verified: three descriptions, three CC files, three audio files, metadata and manifest. Native `read_approved_package(..., verify_files=True)` accepts the package, retains the exact publish/languages approval pins and all nine choices, and returns four CC tracks (including original zh-TW) plus three matching dubs. Consumer package SHA-256: `4031c41641184a4508ff831e093104ae6d6eae78e0d8625cb5c79cd97aa8d161`.

Persisted language review status is `approved`, with `decided_at=2026-10-12T08:00:26.077356+00:00`. The later UI “already decided” rejection does not establish a new approval or Studio success. The saved backend evidence does not identify the approver. Native pull and the read-only consumer independently establish the current approval state.

Authoritative aggregate: `approved-delivery-20261012T080112779Z.stdout.json`, SHA `07662ba3c414cea5b619844ba5a3a336a6225af6056e6c2b7e919d33c26cb1e9`; matching receipt SHA `c81210d21f0365b63feb2197d917f6d6e9cca8cb0ff5a2d49292e523c05d2405`, actual exit 0, empty stderr. It passes 3,361 checks over 546 stable aggregate pins. Remote verification used one connection, a read-only repeatable-read transaction and rollback; no canonical writes, provider calls or stages. The report explicitly does not verify Studio, current YouTube visibility or playback/listening.

YouTube sync evidence `youtube-sync-complete.json` (captured 08:02:50.458Z, SHA `59ed9aca385bb7d2bd9154918b5a96319f65ea00f17cd61aea0e96c19a476a40`) reports completion for video `b98IdS1MB78`: four metadata locales, EN/JA/KO CC uploaded, existing zh-TW CC retained, thumbnail set and private visibility. The submitted Chinese description equals the approved metadata exactly, with the TC-only sentence absent; see `youtube-sync-reviewed-form.json`, SHA `e19ced25697ef6c6e16fb84bb2c2f1b06939a697d3947a138a1c497e324f1d01`. Audio publication and exact Studio text readback are established by the separate final evidence below.

## Final Studio verification and handoff

Studio publication is directly captured in `studio-final-all-published.json`, SHA `4b3818f9329e6ef6e1c0d47f7179ee345ff56147ded48f39e56c72a7ab0b6623`, with full AX/DOM at the exact video URL. Screenshot `studio-final-published.png`, SHA `a92426469d09c864c1a2a6eb442c7153196a9d203ab91d7c77e8e60677073de3`, independently displays all nine Published cells.

Six saved caption/metadata captures pass 70 guards in `studio-captioned-exact-readback-20261012T081323507Z.stdout.json` (SHA `f5414eb334774b53719a013ad8d3a0f0f0dcc09c7d288afe1495d0de357bfef1`); its receipt (SHA `e8aa8458eb4b7df1aca7c41a4b60cd5586b85a41f7113bbe49569526598842f2`) records actual exit 0 and empty stderr. All 431 CC texts match packaged SRT exactly, preserving spaces, line breaks and order; AX comparison only maps each LF to one ASCII space. Three descriptions match packaged strings exactly. The three titles exactly match the live native caption-label policy, including `｜CC Subtitles`, `｜字幕付き` and `｜CC 자막`. `h03-caption-policy-proof.json` SHA `29a94e9c47c5cb16ae580ccfd2a770df897955c14b0136ba3f15685872b4ce63` pins the production policy/source; no global equivalence to the older checkout is claimed.

Confirmed Windows journal rename failures were recovered with saved answers, backups and native zero-network cache replay; no check verdict was edited. Keep `prepared-recovery-*/applied.json` and [the open Windows journal issue](../../../tasks/open/2026-10-09-windows-speech-journal-rename-failures.md). The separate backed-up JA/KO 502 resolutions use strong client/route/time/upstream correlation, not request-body or billing proof; KO's later clock measurement does not establish historical clock continuity. Their receipts remain `ja-502-resolution.json` and `ko-502-resolution.json`.

Delivery evidence and draft-PR handoff are complete; merge is not part of this delivery. The saved text checker does not certify audio listening, player playback, full Studio cue timing or downloaded Studio SRT bytes. Local fit/timing and source coverage are covered by the separate native media/caption checks above.

Native work and reviews: `C:/Users/x8120/mokaair-work/videos/curio-h03`. Durable proofs, original pins, patches, recoveries and actual exits: `C:/Users/x8120/mokaair-work/video-language-curio-h03`. Reviewed helper details are in external `H03-READBACK-README.md`; final media/caption run receipts and the aggregate supersede earlier preparation-only notes. Nothing here authorizes another episode.
