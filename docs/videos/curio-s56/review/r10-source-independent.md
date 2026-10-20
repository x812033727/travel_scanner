# S56 R10 — independent source and written-scene review

2026-10-20 UTC. **HOLD: one spoken action and two opening scene prompts need narrow repairs.** I reviewed the frozen R10 files and the fixed source texts independently. This verdict covers historical claims, citation mapping, chronology and written visuals only. It is not a narrative ballot, policy classification, audio check, generated-art review or release approval. I did not change the creative files.

## Frozen inputs and source identity

| Input | SHA-256 observed | Required SHA-256 matched |
| --- | --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` | yes |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` | yes |
| `claims.md` | `4fc2b9887afe5805340c553d7c099658ce5231d8f27b836c621842477f14a172` | yes |
| `video.json` | `e54a6dfde678a536e81eac36c13360782e5e1efad6c2c30c694cefc5e01098f8` | yes |
| `script.md` | `286b7d50bc21ee8c8c5f61d99a3744f988ca1cbdac2c80bef05237a74f585153` | yes |

I checked the local Git checkout at the exact commits named in [research.md](../research.md), recomputed the full-text hashes and Git blobs, and read the cited passages. `git show HEAD:<text>` in each source checkout hashes to the same bytes as its working text.

| Witness | Fixed commit | Text SHA-256 / Git blob observed | Evidentiary limit |
| --- | --- | --- | --- |
| F, Thomas D. Foster, [letter](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt) | `60c777551301c30942acf749d4bb37ca32752353` | `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee` / `565a1a465fb84a2c9035ea82d312ae80b70b52e8` | Dated 1871-10-31 at F204–208; the 1923 editor says at F161–171 that the original is lost and a family copy survived. The printed text is near-time testimony through that copy, not an extant 1871 manuscript. |
| L, Frank J. Loesch, [memoir](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt) | `08931a6f2629fd4b8be37b1ec548857d48d17eb9` | `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011` / `3370a705ac376a115010a8480e3874ab10a6cb5b` | Published in 1925, 54 years after the fire. Times, mechanisms and counterfactuals are his recollection or later judgment, not an official investigation. |

The 154 `claims.md` IDs are unique and match the 154 `video.json` spoken lines exactly. The 154 lines appear in the same order and with the same text in `script.md`; its 121 scene headings match the 121 JSON scenes. All 154 claim rows have fixed-commit citations: 234 citation links, 30 distinct source/range links, zero wrong commits, zero reversed or out-of-bounds line ranges. These mechanical checks establish coverage, while the passage reading below assesses meaning.

## All 154 spoken claims against their mapped passages

The ranges below partition the **154 spoken IDs** in order, including IDs skipped by the author. I checked each line and its row in `claims.md`; questions were assessed as foreshadowing, while assertions were tested against the fixed text.

| Spoken IDs reviewed | Lines | Passages checked and result |
| --- | ---: | --- |
| `s56001`–`s56013` | 13 | F349–383, F440–459; L134–144. Foster crosses from the West Side to the South Side, then sees the main fire across water and a separate fire behind him on his own bank. East bank is a defensible geographical rendering of this South Side crossing, and the opening questions do not claim a witnessed ember trajectory. The two case props in this opening are separately held below. |
| `s56014`–`s56039` | 24 | F204–256; L75–146. The Saturday wood-yard fire and Sunday discussion remain distinct from the later Great Fire. Loesch explicitly says Saturday's fire had no wind and stopped before crossing the South Branch (L134–146). Foster gives about 4:30 a.m. for seeing its glow fade and falling asleep (F256). Loesch's employment, lodging, dry weather, wood supports, wood walks and tarred pine-block streets have support at L75–117. |
| `s56040`–`s56065` | 25 | F266–330; L156–160. Foster gives Sunday 10:15 p.m. as his departure time, not the official start time; the 30 engines, falling brands up to two feet, church roof about 300 yards away, two minutes from black smoke to flames, and engine division are his account. Loesch remembers the southwest wind. No line now invents the roof workers' withdrawal. |
| `s56066`–`s56088` | 23 | F349–383. The railway cars burn before Foster's first river crossing. After crossing, he estimates 80 yards of water, notices a new fire about 400 yards behind him on **his** bank, says engines were drawn off and then the older fire crossed and joined it. He sees small wooden houses, a nearby gasworks, burning awnings and wooden walks. `s56077` correctly withholds any claim that he watched a specific ember cross the full river. |
| `s56091`–`s56116` | 26 | F376–459; L245–269. The commercial buildings, Foster's initial confidence, packing and later departure, Loesch's Court House bell, Foster's City Hall cupola, wagon and hotel fire are grounded. F420–438 does **not** support the urging action in `s56112`, detailed below. The vague “only a short way” in `s56091` is a narrative transition rather than a quantified distance; avoid turning it into a map or measured route. `s56107`'s “它” follows the Court House bell, but Foster's object is the **City Hall** cupola (F407–411); spelling out 市政廳 in a future narration edit would remove the referent ambiguity. |
| `s56117`–`s56144` | 28 | L238–404; F440–470. Loesch uses the pedestrian tunnel to the North Side (L288–304), unlike Foster's bridge; his boarders remove possessions, the lakeward woman is seen *later* with singed hair, and on the third return he sees sudden fire in pavement and walks after 1 a.m. Monday (L378–404). Foster then reports about 3 a.m. at the burning North Side bridge, takes a wagon west, waits on luggage until dawn and sees North Side smoke. The spoken order preserves these separate witnesses and does not assert that Loesch watched the main river-crossing instant. |
| `s56145`–`s56151` | 7 | F465–471; L537–557. Foster links unchecked North Side fire with burned waterworks and lack of water; Loesch's later memoir names the Chicago Avenue pumping station, observes no attempt to stop the northward fire, and proposes an **unproved** fire-engine-and-water counterfactual. Monday wandering between North and Fullerton and residents burying furniture occur at L537–545. Streets, walks, houses and fences feeding the fire occur at L547–557. |
| `s56153`–`s56170` | 5 | L516–522, L578–620. Loesch returned before sunset to the refuge reached early Monday. He puts dry prairie **in front and south** of the group (L578–585) and watches fire approach from the **south** (L601–603). The Tuesday rain is his remembered “about 1:30” (L605–609) before fire tested the prairie; the narration limits the safety judgment to that refuge. No surviving scene asserts that rain extinguished the entire city at one minute or that the abandoned wet-wrap plan was tested. |
| `s56173`, `s56174`, `s56176` | 3 | F349–383, F440–470. The deliberate return to the opening river restores the supported sequence: new fire on the South Side/east bank → engines drawn from the river defense → West Side fire subsequently crossing to join it. Foster's text says he inferred crossing from the new fire and describes the later merger; neither narration nor prompt draws a continuous ember path. The final Foster image is after his third crossing, on West Side ground at Monday dawn, not after Loesch's Tuesday rain. |

### Blocking spoken action: `s56112`

Current R10 narration, exactly: **「箱子上了車，他立刻付錢，催車往北側走。」** Its `claims.md` row points to F420–428 and F447–459. Foster says, “**[I] told him, I would pay him the minute I got the things on board**” (F425–426), then “**[he] put the packages on and I paid him. Just as I was leaving the place took fire**” (F427–428). He later recounts crossing the bridge and reaching the North Side (F430–459). He never says he **urged the driver** or gave him a northbound instruction. `催車` asserts that extra action as fact. A narrow repair can keep the documented loading, payment and northward travel while removing `催`; the author should choose the final wording and update the row. This is a source HOLD, not a claim that the wagon went somewhere else.

## All 121 written scenes

I read each scene's template, text and image prompt, including all 118 `shot` illustrations and three `big` cards. The chapter group counts below total 121 and record the complete written-scene sweep; the two opening prompts below fail chronology. `look.preset` is `cute-mystery`; the cards say Loesch's 1925 recollection, Foster's estimated 80 yards and Foster's reported ~3 a.m., each matching its attribution. No written scene shows a continuous ember crossing, fire flowing on the river, a literal stone-melting mechanism, Loesch witnessing the pump station fail, or a proven dry-hose counterfactual.

| Scene group (inclusive first–last scene ID) | Scenes | Written-image result |
| --- | ---: | --- |
| East-bank opening, `s56001`–`s56013` | 11 | East-bank/night setup matches F349–368. **HOLD `s56011` and `s56013` for the prematurely packed case.** The other nine scenes remain illustrative without an invented river-fire route. |
| Previous night's fire, `s56014`–`s56040` | 18 | Saturday bridge is east approach, wood-yard fire remains west, and 1925 card marks Loesch's later memoir. Firelit Saturday night and Sunday wood-street illustrations do not turn this into Sunday's new fire. |
| Falling brands and church, `s56042`–`s56069` | 20 | The 10:15 departure, brands, church, divided engines, rail cars and first bridge crossing are shown in the same order as F266–358. The revised church prompt shows smoke becoming flame and does not invent the roof workers' exit. |
| New fire behind the river, `s56070`–`s56091` | 16 | The card attributes 80 yards to Foster; separate east-bank fire and then joined fires are staged without a particular brand's full flight. Gasworks, awning and wooden-walk spot fires remain local illustrations. |
| Stone district and hotel, `s56093`–`s56116` | 17 | Foster's belongings appear after packing begins; the wagon crosses toward the North Side. Loesch and Foster do not meet. The duplicate words “dark vest in a dark vest” in `s56106` are a harmless prompt typo, not a history HOLD. |
| North Side and West Side, `s56117`–`s56144` | 24 | Loesch's tunnel, boarding house, later sighting of the singed woman inland, night street fire and Foster's ~3 a.m. bridge are separate. The West Side open-ground and black-smoke shots are Monday dawn, as F459–470 says. |
| Water loss, prairie and callback, `s56145`–`s56176` | 15 | Loesch at a 1925 desk is used for his pumping-station recollection and hypothetical remedy; he is not depicted at its destruction. The prairie is south of the refuge, the rain occurs early Tuesday morning, and `s56170` shows Tuesday dawn. `s56173`/`s56174` explicitly return to the Sunday-night South Branch; `s56176` returns to Foster's Monday-dawn West Side position. |

### Blocking opening prop chronology: `s56011`, `s56013`

- `s56011` prompt, exactly: “**Wide shot, the traveler holds a small case beside a wooden bridge approach, faint fire glow**”.
- `s56013` prompt, exactly: “**Close shot, a hand grips a small case beside the river railing, low fire glow**”.

Both are in the opening when Foster has first reached the South Branch's South Side/east bank, before he returns to the Briggs House. At F349–358 he carries **other people's** boxes and bundles into railway cars on the West Side, then crosses the river; F360–383 puts him on the opposite bank and *only later* back at the hotel to pack. His **own small valise** first appears when he starts packing it at F388–393. In a Foster point-of-view opening, the repeated held case presents that later packed item too early and reverses the luggage sequence. A narrow visual repair can remove the case from both prompts, leaving the bridge and river hook intact. It should not add a route for fire across the water.

## Chronology and next gate

The account's underlying order is Saturday 7 October wood-yard fire → Sunday 8 October Foster departs at 10:15 p.m. → church and first South Branch crossing before his 1 a.m. packing at the hotel → Loesch reaches his North Side boarding house by the tunnel and sees wood paving burn after 1 a.m. Monday → Foster's ~3 a.m. North Side bridge and West Side dawn → Loesch's Monday daytime northward wandering and pre-sunset refuge → his remembered ~1:30 a.m. Tuesday rain. The final two east/west bank shots are an explicitly narrated callback, not new events after Tuesday.

**Verdict: HOLD this exact R10 source and written-scene gate** until the author repairs `s56112`, `s56011` and `s56013` and freezes new file hashes for a new independent check. The Council/City Hall pronoun in `s56107` is a precision suggestion for an edit, not a separate blocking historical contradiction. No paid media or other gate was run in this review.
