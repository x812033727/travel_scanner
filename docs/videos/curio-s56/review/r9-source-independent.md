# S56 R9 — independent source and written visual review

2026-10-20 UTC. **HOLD.** This is a fresh check of the frozen R9 text and written scene plan, not a carryover of an earlier review. It does not assess generated stills, audio, narrative ballots, or policy. The author files were read but not changed.

## Frozen inputs

| File | SHA-256 observed | Required match |
| --- | --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` | yes |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` | yes |
| `claims.md` | `5c0a21f8540fdc1448c57ee9d75f90fc8c6241b42d9dc1db2d3b1a0fada33d4d` | yes |
| `video.json` | `645c8c505f840393b3401c4746896a015da081a4ca6027d25ed1378f9ca4834d` | yes |
| `script.md` | `2679f45e2c775e3554ff55896d852f1ae95d9dba9489fd319d2bc15f72c0f0ed` | yes |

## Independently reopened sources

I fetched both fixed raw texts with the repository's editorial User-Agent, checked HTTP 200 and SHA-256, and computed Git blobs using `git hash-object --no-filters` (the checkout's ordinary Git filter changes line endings). The cited GitHub blob URLs, including representative `#L349-L383` and `#L578-L620` deep links, also returned HTTP 200.

| Witness | Fixed raw source | Raw SHA-256 / Git blob observed | Boundary |
| --- | --- | --- | --- |
| F, Thomas D. Foster | [1871 letter in 1923 printing](https://raw.githubusercontent.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt) | `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee` / `565a1a465fb84a2c9035ea82d312ae80b70b52e8` | F204–208 dates the letter October 31, 1871; the 1923 editor says at F161–171 that the original is lost and a family copy survives. It is near-time testimony through a later copy, not a surviving original manuscript. |
| L, Frank J. Loesch | [1925 memoir](https://raw.githubusercontent.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt) | `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011` / `3370a705ac376a115010a8480e3874ab10a6cb5b` | A recollection 54 years after the fire, including remembered times, locations, and causal opinions; it is not a contemporaneous official investigation. |

`claims.md` has **169 distinct claim IDs**, each present once in `video.json`; all 169 spoken strings match exactly, in the same order, in `script.md`. There are 256 source links across those rows, representing 31 distinct source/range combinations. All use the two fixed commits, have a line-range fragment within the respective 943- or 1,193-line raw text, and no row lacks a link. The 136 written scenes contain 133 `shot` illustrations and three `big` cards; the illustration share is 133/136, about 97.8%, with no card run. `look.preset` is `cute-mystery`, the standard music settings are present, and 17 loops are declared. These checks establish coverage and format, not factual truth by themselves.

## Claim-by-claim evidence result

I read the 169 claims against the cited source passages and the scene text, grouped below to make the complete pass inspectable. One line has an unsupported direction; a second supplies an action the letter does not say. The rest do not show a material source contradiction in this written pass.

| Claim IDs reviewed | Primary passages checked | Result |
| --- | --- | --- |
| `s56001`–`s56013` | F349–383, F440–459 | The opening's east-bank/South Side setup and its future questions have a basis in Foster's crossing and later fire. Questions are foreshadowing, not eyewitness claims that a particular ember crossed. |
| `s56014`–`s56039` | F204–256; L75–146 | The Saturday wood-yard fire is separated from Sunday's fire. Loesch explicitly says Saturday's fire did not cross the South Branch and that wind was absent (L134–146); timber streets and tar appear at L94–117. Foster's fading glow was about 4:30 a.m. (F256), so `s56026`'s vague “將近凌晨” is worth making more precise, although its illustration says early morning. |
| `s56040`–`s56065` | F266–330; L156–160 | Sunday bell, Foster's 10:15 departure, strong wind, falling brands, the church roof about 300 yards away, and fire-brigade division are supported as his account. **Precision fix:** `s56061` says “撤出的人只能讓開”; F310–325 says men tried to extinguish the roof, could not, then an engine came and smoke turned to flame. It does not report those people's withdrawal. Remove that action or attribute it explicitly as illustration. |
| `s56066`–`s56088` | F349–383 | Rail cars, first South Branch crossing, eighty yards of water, a new fire about four hundred yards behind him on his bank, another fire's merger, gasworks proximity, awning and wooden-walk spot fires match the letter. `s56077` correctly says no single ember's full river-crossing path is recorded. |
| `s56091`–`s56116` | F376–459; L245–269 | The brick/stone district, packing decisions, City Hall cupola, hired light wagon, burning hotel, northward crossing, and unsafe North Side are supported. The spoken treatment avoids reading stone “melting” literally and keeps the two witnesses apart. |
| `s56117`–`s56144` | L238–404; F440–470 | Loesch's pedestrian tunnel is distinct from Foster's bridge. His boarding-house removals, lakeward refugee seen later with singed hair (L334–342), third return, fire in wooden paving/sidewalks (L378–400), and Foster's ~3 a.m. burning bridge and western retreat are supported. The staged woman in `s56125` is correctly inland rather than at the lake. |
| `s56145`–`s56153` | F465–471; L516–557 | Foster reports burned waterworks and lack of water; Loesch later names the Chicago Avenue pumping station, observes fire advancing north, and offers a hypothetical fire-engine remedy. The text calls the remedy his later opinion; the visual plan does not place him at the pumping-station destruction. |
| `s56155`–`s56172` | L578–620 | Prairie, furrows, fence removal, well water, Tuesday ~1:30 a.m. rain and the untaken wet-wrap escape plan match Loesch's memoir **except the compass direction in `s56155`**, detailed below. The rain is limited to his refuge, not presented as a citywide exact extinguishing minute. |
| `s56173`, `s56174`, `s56176` | F310–325, F349–383, F440–470; L605–620 | The closing spoken synthesis is within the two testimonies' limits. Its written images have time/location problems below. |

### Blocking source precision: `s56155`

Current spoken line: **“西南邊還有火，草地就隔在他們與火之間。”** The sole cited range is Loesch L578–620. At L578–585 he puts the prairie **“in front and to the south of us and west of McCormick Seminary”**; “west” locates the prairie relative to the seminary. At L601–603 he writes **“Our eyes were ever to the south, watching the steady coming on of the fire”**. Neither passage places the fire southwest of the refuge. The nearby prairie as a threatened buffer is supported; **southwest** is not. A narrow sourced line would say **“南邊還有火，草地就隔在他們與火之間。”** The manuscript is frozen, so this is a repair suggestion only.

### Blocking written visual chronology and placement

The prompts below are original illustrations, but their visible time and vantage cues would read as event reconstruction. No generated image was reviewed.

| Scene | Exact current prompt | Source conflict and narrow alternative |
| --- | --- | --- |
| `s56173` | “Wide shot, the traveler looks toward several separated river bridges, soft grey morning light” | Foster crossed at night, then sat with baggage on western open ground until Monday daylight (F440–470). The text does not put him at a viewpoint over several bridges in daylight. Consider a Sunday-night South Side riverbank view with one visible bridge and separate distant fire glows, or a Monday-dawn view of him sitting on luggage on western open ground. |
| `s56174` | “Medium shot, a lone firefighter turns toward a separate roof fire, pale rainy dawn light” | The roof fire and divided brigade cited here happened Sunday night (F310–325, F360–368). Loesch's rain arrived at his refuge about Tuesday 1:30 a.m. (L605–609). Make this the Sunday-night church roof under firelight, without rainy dawn. |
| `s56176` | “Wide shot, a man in a tan coat holds a small case beside a calm river at dawn, pale rainy dawn light” | Foster's documented river crossing and bank-side new fires are at night (F349–383); by Monday dawn he was on western open ground (F459–470). No return to a calm river after rain is recorded. Reuse an explicitly Sunday-night bank view or his documented western dawn position, without a post-rain river return. |

## Disposition

**HOLD** the frozen R9 source/visual gate. The author can repair `s56155`'s compass point, remove the unsupported withdrawal in `s56061`, and replace the three closing prompts' time/location cues, then freeze and hash the revised files for a new independent check. The two fixed witness texts are reachable and adequate for the narrower core story. They do not prove the exact route of any ember across the river, an initial ignition culprit, a citywide water counterfactual, or a citywide minute when rain ended the fire.
