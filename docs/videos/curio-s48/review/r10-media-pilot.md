# S48 R10 — predeclared three-shot native image pilot

**Declared before any image generation, 2026-10-20 UTC.** The exact R10 spoken script SHA-256 remains `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd`. The official R10 audio check covers 102/102 lines with zero flags; narration WAV SHA `d638c1b9dc9b9a4165b8adddfd6f873fba6de16cc3b5e9b26f730659de00878c`, timeline SHA `a0c87443f00d78a97a683548dc0d262c1e8919e57ee54e0fa43fd0e1947f61d4`. The local audio choice is bound to that timeline in `approvals.json` under the owner's standing recommended preference. The website audio card for the same timeline is `hand_pushed` and **pending**, a separate decision.

## Cost ceiling and staged decision

The CLI's `keyframes --takes 3 --dry-run` quoted **99 shots, no end frames**, MiniMax `image-01` at 1K: about **US$1.34** for one take of all shots, up to **US$4.01** if each needs three. `music --dry-run` quoted a 600-second Gemini Lyria 3.5 track at about **US$0.08**. The server's per-video media cap is US$200 and its current S48 media ledger is US$0.00.

I set a tighter **US$5.00 whole-episode media ceiling** for this S48 version: all keyframe images, image judging, any allowed prompt repair, and eventual music must fit inside it. This is the remaining media ledger ceiling; prior speech and transcription are already incurred and are not priced in the media CLI quote. No clip generation is in this plan. The pilot itself has a **US$0.15 ceiling** including a possible single scoped repair round. The scoped dry run quoted **about US$0.04** for one take of these three shots. The actual ledger will be checked after each paid run; reaching a cap stops generation. The 99-shot run remains unstarted until this pilot is reported.

## Three varied, source-checked prompts

| Shot | What the native image must show | Source boundary checked before generation |
| --- | --- | --- |
| `atl001` | Medium outdoor view on the Great Eastern's bow: one generic 1860s worker guides a plain dark line over a hauling wheel. | Russell's firsthand August 2 account describes the bow recovery and line over the machinery, [R3782–3815](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3782-L3815). The worker is an illustrative figure, not a named portrait; no seafloor view or exact instrument numerals. |
| `atl017` | Close interior view: an electrician watches a **reflected light spot** on a blank scale in the vessel's testing room. | Russell describes Thomson's tiny mirror, reflected ray, scale, and July 24 first fault at 84 miles, [R2894–2918](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L2894-L2918). No needle gauge, numeric scale, or visible electric current in the sea. |
| `atl070` | Wide shore view at Heart's Content: a generic worker stands beside the **new 1866 line** after its Newfoundland landing. | Field's later book quotes the arrival diary and July 27 telegram, [F8990–9060](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L8990-L9060) and [F9110–9135](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9110-L9135). The worker is illustrative; this is the new cable, before the old cable is salvaged. No invented legible harbor sign or message. |

The pilot spans a shipboard action, an optical instrument in a dark room, and a wide harbor scene. The three exact current prompt strings fit the provider's limits: 107/1072, 92/1070, and 116/1070 characters after style and camera allowances. The fixed Russell and Field local texts match their research hashes. The private pre-media snapshot is `/workspace/.video-work/curio-s48/review/media-preflight-r10.json` (SHA `059fd969da82b07b7f38badcb402cf9863fba6de7ddf2c1a8cac4a25b9e90184`); its zero-cost ledger snapshot and dry-run logs sit beside it.

## Native KEEP rule

Each **original full-resolution image** will be opened independently, not judged from a contact sheet or the server's score. Mark KEEP only when its main event/object is clearly right, its historical/technical cues stay inside the boundaries above, the 1860s cartoon reads cleanly at native size, the 16:9 frame has no side bars or fake text/logo, body parts are coherent, and the lower subtitle band does not hide the focal action. The server judge is supporting evidence, not a substitute for this inspection.

At least **two of three native originals must be KEEP** before a later decision about the other 96 shots. If fewer than two pass, make **one precise prompt-only repair** to the rejected shot prompts, check those changes against the sources, and run **one scoped retry at most**. Then inspect native originals again. If fewer than two pass after that retry, stop image work and preserve the passed R10 audio. No spoken line, script, or audio binding may change during the pilot.

## First native pilot inspection — 0/3 KEEP

The scoped `--takes 1` command returned exit code 1 after generating two frames. `atl001` had a MiniMax `ReadTimeout`, leaving no original to judge or charge. The media ledger after this round is **US$0.027**, including two images and two judge calls. The original 1280×720 JPEGs and trimmed selections, manifest, and ledger are archived in the private `review/media-pilot-r10-first/` directory before any repair.

| Shot | Original SHA-256 | Native verdict and observed reason |
| --- | --- | --- |
| `atl001` | No image | **REJECT**: the provider timed out; no frame to approve. |
| `atl017` | `8e16dd3941cfd400af59993f757fc43ad69f76dfcf0b9deda94c6f0eeaa3a36f` | **REJECT**: a generic glowing object/cone sits by the worker. There is no legible blank scale, tiny mirror apparatus, or reflected light spot moving on the scale. The frame misses the technical event even though the server scored it 9.29/10. |
| `atl070` | `467bfdd00d1a0d2d37c3ec01862acfb312d2e65cbcbc8dd3120487a7b5691cc0` | **REJECT**: the foreground worker wears a modern hardhat and orange safety vest, with a modern small vessel behind him. No newly landed submarine cable is clear. The wrong era and missing object outweigh the server's 9.29/10. |

The result triggers the one predeclared prompt-only repair and scoped retry. These rejected files are retained for comparison and are not native KEEP candidates.

## One prompt-only repair, checked before retry

I changed only `data.prompt` in `atl001`, `atl017`, and `atl070`. Replacing those three new strings with their prior strings in the current `video.json` reproduces the frozen R10 `video.json` SHA `ae0c8fd27d8abf7cc3d1dc192640336d12e5a5919db28d7b658671db35821e10` byte for byte. The repaired `video.json` SHA is `dd91631217153e3fec5e0117dea73faa30811991fce3a211aad7d99615cca018`; `script.md`, narration WAV, and timeline remain at the exact hashes stated above. Lint is **0 errors, 0 warnings**.

| Shot | Precise repair and pinned source recheck |
| --- | --- |
| `atl001` | The new prompt names the Great Eastern's 1865 bow, a cable rising from the sea over hauling machinery, and period work clothing. Russell's pinned text (SHA `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`) says the cable came over the bow and through the picking-up apparatus at [R3782–3815](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3782-L3815). The generic deckhand and wheel are illustrative; no precise crew identity or recovered seafloor view is asserted. |
| `atl017` | The new prompt puts a **blank scale and reflected light spot** at the center, with a small mirror instrument nearby and no glowing object in the electrician's hands. Russell [R2894–2918](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L2894-L2918) explicitly describes Thomson's reflected ray from a tiny mirror moving along a scale in the ship's testing room. The arrangement is an illustrative simplification, with no fabricated numeric reading. |
| `atl070` | The new prompt makes the landed dark cable the foreground subject, keeps the worker small and fully visible in 1866 period clothing, and excludes the modern gear seen in the rejected image. Field's pinned text (SHA `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`) quotes the Heart's Content arrival, harbor vessels, telegraph station, and arrangements to land the new shore end at [F8990–9060](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L8990-L9060). The worker is illustrative. |

The retry dry run is scoped to the same three shots, **one take each at seed offset 1**. It reports prompt sizes 232/1072, 296/1070, and 298/1070 characters, with about **US$0.04** additional cost. The existing US$0.027 plus this estimate is below the predeclared US$0.15 pilot ceiling. This is the one allowed retry; no further prompt change or image generation follows its native inspection.

## Retry native inspection — 0/3 KEEP; image work stopped

The single scoped retry made three 1280×720 original JPEGs. The CLI exit code was 1 because `atl017` failed its server judge, while the other two each received 9.29/10. I opened **all three originals at native resolution**. The server's score does not override the visual problems below.

| Shot | Original SHA-256 | Native verdict and observed reason |
| --- | --- | --- |
| `atl001` | `f2024ccfaf6ac585af5f986c2d62c6243883cdfd9e44471c1cf6d8cf75cfeab2` | **REJECT**: the center wheel is a ship's steering helm, not bow cable-hauling machinery. The dark strand sweeps out of a person's hair at the right and does not read as a cable coming from the sea over the wheel. The server itself flags the wrong wheel in its details despite an overall 9.29/10. |
| `atl017` | `01b8ea0d747ee8dc6d83a57e81fb1747eb4bc3e0822b8b16b43493c0fb61ac62` | **REJECT**: a tiny detached-looking person sits under an oversized blank slab, another head-like shape floats behind it, and the light spot is centered rather than reaching the end of a scale. There is no clear mirror-to-scale reflected ray. The server judge scored 6.88/10 and also flagged anatomy and the light position. |
| `atl070` | `57c42f823814af6620f76c87fac04916092aecc3d93f5fc74f36ec7bf352128e` | **REJECT**: the supposed submarine cable reads as a broad raised roadway or seawall, several feet wide, extending toward the harbor. Its scale and appearance do not establish a landed telegraph cable. Two figures stand beside it. The server judge scored 9.29/10 but only flagged the extra person. |

The final S48 media ledger is **US$0.0675**: six image requests (one failed at US$0), five judged images, zero clip seconds, zero music, and no reservations. The exact retry originals, trimmed selections, manifest, and ledger are preserved privately in `review/media-pilot-r10-retry/` (manifest SHA `e09247fe42d3702bd48c3539a8fa74f32da54d120bf9df0286f2c7cab72c6036`; ledger SHA `c6ffa9dea6cdc1b50a73f39706f45a5879bef05314eea86117f3316be633ca54`). No full 99-shot draw, clip, or music request has been made. Under the predeclared threshold and retry limit, **stop image work here**. The R10 spoken script SHA, narration WAV SHA, timeline SHA, and zero-flag official check artifacts remain unchanged. The locally delegated audio choice and pending website audio card remain separate.
