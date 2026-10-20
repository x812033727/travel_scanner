# Curio S37 R8 independent source and visual audit

## Verdict and frozen inputs

**Source fidelity: PASS (91/91 spoken rows). Still-prompt fidelity: PASS (88/88 prompts). 1:1 narration alignment: PASS. Loop metadata: FAIL at two payoff pointers. Overall R8: correction required before an unqualified final pass.** The loop errors do not change the spoken story or the blind narrative seal (13 Yes / 0 No), because the script itself supplies the answers shortly afterward.

| Input | SHA-256 |
|---|---|
| `docs/videos/curio-s37/script.md` | `a838e16572f4a40c3d79c5874087900a8e8b808fceb35db9a03642bcc3412a62` |
| `docs/videos/curio-s37/video.json` | `a83c3d0aa14ea6bb4bf09392f86d95c31101b9175e38afb50961aa692a45765b` |
| `docs/videos/curio-s37/claims.md` | `ce7491625af59f27549fe4621e18917082946602474a99c1ea72e4f9f27d997a` |
| Freshly fetched pinned `2811.txt` | `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` |

I first read only the script and official `narrative --json` output, then sealed all 13 Yes/No judgments with script citations in `/tmp/curio_s37_r8_fresh_blind_seal.md`. After sealing, I read `research.md`, `claims.md`, `video.json`, and freshly fetched `2811.txt` at GITenberg commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. The fetched hash matches the research note. The file identifies William Melmoth as translator and F. C. T. Bosanquet as editor/reviser (file lines 13–15, 41–43). This audit therefore checks the two letters as transmitted by that pinned English translation; it does not resolve Latin manuscript variants or the eruption's exact calendar date.

## Every spoken claim row

The table enumerates all 91 `claims.md` rows in script order. Each ID was checked against the pinned translation passages shown, including the question framing, not merely matched to a source label. `pl100`–`pl101` are editorial invitations. All 89 historical/question rows are supported at the stated witness level: the nephew stays at Misenum; his uncle's final minutes at Stabiae are subsequently reported, not witnessed by him.

| Script section; IDs checked | Pinned source lines | Finding |
|---|---|---|
| Road preview: `pl001`, `pl002`, `pl003`, `pl004`, `pl005`, `pl006` | 3519–3527; 3541–3554; 3600–3617; 3655–3658; 3676–3691 | The mother-and-son road escape, uncle's outward voyage, mother's request and witness question are grounded. The lines preview outcomes without claiming the boy saw Stabiae. |
| Cloud and departure: `pl007`, `pl008`, `pl009`, `pl010`, `pl020`, `pl011`, `pl012`, `pl013`, `pl014`, `pl015`, `pl016`, `pl017`, `pl018`, `pl019`, `pl114` | 3519–3554; 3634–3636 | Misenum fleet, mother's cloud notice, pine form and color, uncertain origin, light vessel, invitation/refusal, Rectina's plea, galleys, and nephew's studies all follow the letter. `pl020` correctly attributes the later description to the young writer. |
| Earthquake and book: `pl047`, `pl048`, `pl021`, `pl049`, `pl050`, `pl051`, `pl046`, `pl052`, `pl023`, `pl053` | 3634–3652 | Bath, supper, uneasy sleep, unusually violent quake, mother and son finding each other, courtyard, stated age 18, Livy excerpts, and visiting Spanish friend are supported. `pl052` adds the small gesture “停住腳步”; the translation says the friend *joined* them and saw the book, without explicitly saying he stopped short. This does not change the event. |
| Leaving and shore: `pl054`, `pl025`, `pl055`, `pl026`, `pl115`, `pl056`, `pl057`, `pl058`, `pl027`, `pl059` | 3652–3668 | Faint morning light, unsafe narrow court, departure, following crowd, ordered carriages, level-ground rocking despite large stones, receding sea and stranded sea animals all match. `pl059` renders the letter's “On the other side” as a look across the bay; the coastal geography makes this reasonable, though the precise head movement is illustrative. |
| Black cloud, mother, road: `pl060`, `pl028`, `pl061`, `pl111`, `pl062`, `pl063`, `pl064`, `pl065`, `pl029`, `pl110`, `pl067`, `pl068`, `pl069`, `pl070`, `pl030`, `pl071`, `pl072`, `pl031`, `pl073` | 3666–3697 | Flashes and flames, the friend's *conditional* opinion of the uncle's wishes, Capreae/headland obscuration, mother's age and fear of holding up her son, the hand-taking, light ash, pursuing mist, departure from the main road, and sudden blackness are preserved. `pl029` condenses “age and corpulency” to age/difficulty escaping without changing the stated reason. |
| Voices, rumor, ash: `pl074`, `pl032`, `pl075`, `pl112`, `pl033`, `pl076`, `pl077`, `pl034`, `pl078`, `pl079`, `pl080`, `pl081`, `pl092`, `pl082` | 3694–3715 | Calls for relatives, fears of final night, religious reactions, the **false** Misenum collapse/fire rumor, mistaken fire light, heavy ash and Pliny's account of his own composure all match. The world-ending thought remains a reported fear, not an objective disaster claim. |
| Day and return: `pl083`, `pl035`, `pl036`, `pl084`, `pl085`, `pl037`, `pl113`, `pl086`, `pl087` | 3715–3727 | Darkness dissipates, eclipse-like sun, ash-covered objects, return to Misenum, ongoing quake, anxious night, frightening predictions and waiting for uncle's news are supported. |
| Later letters and outro: `pl088`, `pl045`, `pl043`, `pl089`, `pl091`, `pl099`, `pl100`, `pl101` | 3600–3618; 3625–3630; 3720–3727 | The uncle falls at the Stabiae shore; his body is found on day three without violence marks. “Noxious vapour” is explicitly Pliny's conjecture, and the script says so. Letter LXV distinguishes eyewitness from immediate reports; LXVI answers Tacitus's renewed question about Misenum. The location conclusion follows both letters. Last two lines are editorial questions/CTA. |

Chronology remains coherent after the deliberate opening preview: cloud and rescue preparations at Misenum; the nephew's decision to remain; bath and night quake; dawn departure; receding shore, dark cloud, mother's appeal, darkness and ash; return to Misenum; later written account. The letter's “24th of August” at line 3520 is not spoken or visualized as a settled date. No Pompeii street episode is assigned to young Pliny.

## Every still prompt

I inspected all 88 `template: shot` prompt strings against their spoken line and the same source passages. The next table covers every still ID once. Each prompt is an illustrative framing; where it omits a clause (such as the crowd in `pl002`), it does not contradict it. The sole `pl099` scene is an outro card and has no still prompt; its thumbnail uses `pl002` and asks a location question.

| Still IDs inspected | Visual fidelity finding |
|---|---|
| `pl001`, `pl002`, `pl003`, `pl004`, `pl005`, `pl006` | Roadside mother/son and dark cloud establish Misenum-side escape; `pl003` shows an older fleet commander at a ship rail, not the young nephew aboard. The preview images do not depict a witnessed death. |
| `pl007`, `pl008`, `pl009`, `pl010`, `pl020`, `pl011`, `pl012`, `pl013`, `pl014`, `pl015`, `pl016`, `pl017`, `pl018`, `pl019`, `pl114` | The older scholar/commander looks at the pine-shaped cloud and receives a blank note; the younger scholar remains at a blank tablet/scroll; the older commander boards the galley. No prompt puts the younger man on the rescue ship. |
| `pl047`, `pl048`, `pl021`, `pl049`, `pl050`, `pl051`, `pl046`, `pl052`, `pl023`, `pl053` | Lamplit bed/courtyard, book, visitor and shaking buildings match the nephew's Misenum memoir. `pl052` shows him *holding* an open blank scroll while the visitor enters, avoiding a dropped-book or thrown-book implication; `pl023` shows the reproof. Blank scrolls avoid fabricated legible primary text. |
| `pl054`, `pl025`, `pl055`, `pl026`, `pl115`, `pl056`, `pl057`, `pl058`, `pl027`, `pl059` | Dawn, narrow court, following crowd, stopped cart, stone supports, widened shore and stranded creatures follow LXVI. `pl057` visibly braces a **stopped** cart with large stones and still shows it rocking. `pl059` looks toward a cloud across the bay, without inserting a Pompeii street. |
| `pl060`, `pl028`, `pl061`, `pl111`, `pl062`, `pl063`, `pl064`, `pl065`, `pl029`, `pl110`, `pl067`, `pl068`, `pl069`, `pl070`, `pl030`, `pl071`, `pl072`, `pl031`, `pl073` | Flashes, friend urging escape, cloud hiding the island, mother's plea, son's hand-taking, slight ash, moving mist, departure from crowded road and lights-out darkness track the letter. `pl029` depicts an older mother asking the son to move ahead, not an accomplished solo escape. The faint `pl031` rim light is explicitly non-diegetic, so it does not assert daylight remained. |
| `pl074`, `pl032`, `pl075`, `pl112`, `pl033`, `pl076`, `pl077`, `pl034`, `pl078`, `pl079`, `pl080`, `pl081`, `pl092`, `pl082` | Listener/crowd pictures illustrate voices and fear. The false Misenum disaster is shown through worried speakers/listeners and an adult letter writer, never as actual collapsed or burning Misenum. Ash is brushed from clothing; no unrecorded fatality is staged. |
| `pl083`, `pl035`, `pl036`, `pl084`, `pl085`, `pl037`, `pl113`, `pl086`, `pl087` | Dim returning sun, ash coating objects, mother and son returning to a coastal house and then waiting through a quake-struck night match LXVI. A house interior and garden wall are illustrative objects, not claimed archaeological reconstructions. |
| `pl088`, `pl045`, `pl043`, `pl089`, `pl091` | All five show the **adult letter writer at a desk**. No prompt puts young Pliny at Stabiae, shows him watching the uncle collapse, displays a body, or depicts a modern autopsy. This correctly separates later report and conjecture from his own Misenum memories. |

All 88 still scenes have a nonempty `data.prompt` and `data.visual: "still"`; there are 89 scenes in total including the one outro card. The prompts use generic Roman dress, blank writing surfaces, limited facial/action detail and subdued lighting. They do not claim a particular eruption month/day, an eyewitness Pompeii street view, or an established medical cause of death. This is a prompt audit, not an inspection of rendered or generated images.

## Mechanical checks and loop exceptions

The script has 89 numbered scene headings and 91 spoken lines; `claims.md` has 91 rows; `video.json` has 89 scenes carrying 91 `lines`; the narrative CLI emits 91 timed cues. Heading IDs equal scene IDs in order; claim IDs and text equal video line IDs and text in order; script spoken text equals video line text; timed cue IDs/text equal video lines, with monotonic cue times through `09:09`. IDs are unique at each relevant level. No 1:1 text or ordering mismatch was found. The three frozen hashes were rechecked after these comparisons.

Two of the 22 declared `loops` have a payoff ID that precedes the actual answer:

| Loop | Why the declared payoff misses | First answer in the script |
|---|---|---|
| `pl053 → pl054` | `pl053` asks if the narrow courtyard can still be used at daybreak; `pl054` merely says daylight is faint (script lines 133, 139). | `pl025` says nearby buildings are shaking and the courtyard is too narrow to stay safely (line 143; source 3652–3655). |
| `pl030 → pl071` | `pl030` asks if they can see the ground after the mist overtakes them; `pl071` describes the preventive choice to leave the crowd **while they can still see** (script lines 237, 241; source 3689–3691). | `pl072` says daylight disappears after they sit down (line 245; source 3691–3693); `pl031` strengthens the answer with the shut-room, lights-out comparison. |

Suggested metadata-only fixes: `pl053 → pl025` and `pl030 → pl072`. The remaining 20 loop pointers are defensible answers to their declared questions. No repository files were edited by this reviewer.
