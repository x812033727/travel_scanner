# Curio S37 R7 — independent source and written-prompt audit

## Verdict and scope

**Source verdict: correction needed before release.** The R7 rewrite of `pl020` makes the nearby pronoun `他` refer naturally to the uncle, then credits *him* with a conjecture made while writing the letter. The pinned text's first-person writer is **young Pliny**. Two further spoken lines and several prompt details merit precision edits, itemized below. I reviewed **91/91 spoken claim rows** and **88/88 written still prompts**; I did not request or inspect generated media. No repository file or Git index was changed.

The blind narrative result was sealed *before* I opened research, claims, video JSON, source, prior reports, or Git diff: `/tmp/curio_s37_r7_fresh_blind_seal.md`, SHA-256 `b67038d13817ca819a5b21f758f7d1d73e9164075c7390161f7c920dbcf7f764`, **13 Yes / 0 No**. That is a narrative verdict, not a source verdict.

| Input | SHA-256 / identity |
| --- | --- |
| `docs/videos/curio-s37/script.md` | `b8c6cca751dc9801d09f8f4cb17b632e73cd7cf5b9ece13094c7550511490359` |
| `docs/videos/curio-s37/research.md` | `1ec72d72d9b22aa4ba06654ee07886a78b5a754605b404e0140d0e0776b42bbd` |
| `docs/videos/curio-s37/claims.md` | `2beae04c177796443055a56e0c6ef10e1a40b5163e4b812cdfe0b3a5b9d6730a` |
| `docs/videos/curio-s37/video.json` | `31eb25bf7130bbcbd1e1a6f9f0bfbe78154dcf13d527e27738ea5dd4a05c7de2` |
| Fresh pinned Pliny fetch | GITenberg `Letters-of-Pliny_2811`, commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`, `2811.txt`, SHA-256 `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` (matches `research.md`); saved at `/tmp/curio_s37_pinned_pliny_2811.txt`. Letters LXV–LXVI occupy lines 3500–3732. |

The pinned text identifies William Melmoth's English translation revised by F. C. T. Bosanquet. `research.md` correctly calls out that this is neither checked Latin nor a critical edition. The narration omits the translation's unverified exact eruption date (source L3520), does not make the false Misenum fire/collapse rumours into fact (L3702–05), and labels the fatal gas theory as Pliny's conjecture (L3606–09). The metadata description preserves these limits.

## Corrections and precision notes

| Priority | ID / location | Evidence and assessment | Source-faithful direction |
| --- | --- | --- | --- |
| **Fix** | `pl020`, script L51; claim row L17; video line in scene 11 | The immediately preceding `他` describes the uncle going up to view the cloud (`pl010`, script L47); `pl009` likewise refers to him. R7 changed `pl020` from impersonal `信裡猜…` to `寫信時，他猜…`. A listener now hears that the uncle wrote the letter and guessed about earth and ash. The letter is young Pliny's first-person account (source L3500–02, L3531–36). Moreover, source `I imagine` at L3531–34 qualifies the pine shape's cause; the earth/cinders explanation follows at L3535–36 and is not expressly called a guess. The unchanged `pl020` still prompt shows the grey-haired uncle watching the cloud, which reinforces that pronoun reading. | Name the writer: e.g. `小普林尼在信裡說，雲色一會兒亮、一會兒暗，和混進去的泥土與灰有關。` Keep any image of the uncle as his observation, not as the writer of the letter. |
| **Clarify** | `pl003`–`pl004`, script L17–21; claim rows L9–10 | `這封信後來會寫到…` followed by `還會寫到…` sounds like one letter contains both the uncle's rescue voyage and the mother's demand that her son flee. The former is LXV (source L3537–50); the latter is LXVI (L3679–86). `pl006` later says `同一組信` (script L29), partly curing this, but the opening can be exact from the start. This issue predates R7. | Use `這組信` at `pl003`, or distinguish `一封…另一封…`. |
| **Tighten** | `pl029`, script L213; claim row L56 | The mother says her **age and corpulence** make escape impossible (source L3679–83). `她說自己年長又走得慢` converts that into a reported claim that she walks slowly, which the letter does not state. It preserves the story's general point but adds a specific self-description. This issue predates R7. | Say `她說自己年長，難以逃走；兒子年輕…` or translate the second physical limitation accurately. |
| **Tighten** | `pl057`, script L163; claim row L44; still prompt scene 38 | Source says they could not steady the chariots **even by supporting them with large stones** (L3660–63). It does not identify the wheels as the point of support or who placed the stones. Spoken `支住車輪` and the still's crouching youth at a cart wheel add plausible details as reported fact. This issue predates R7 and is low impact. | `有人拿大石塊支著馬車，也沒能讓它穩下來`; a prompt can show stones bracing a cart without assigning the act to the youth or specifying the wheel. |
| **Prompt fidelity** | `pl052` and `pl023`, still prompts scenes 29–30 | Source says the visiting friend observed the young Pliny **sitting by his mother with a book in his hand**, then reproved both (L3648–51). Both prompts place the scroll and tablet on a bench, and neither shows the youth holding the book. The written prompts do not explicitly deny a second book offscreen, so this is a missed source-defining detail rather than a clear contradiction. Unchanged from R6. | Have the youth visibly hold the book when the visitor arrives and reproves him. |
| **Prompt caution** | `pl027` and `pl059`, still prompts scenes 40–41 | Source reports the exposed shore and stranded sea creatures, then a black cloud `on the other side` (L3663–68). It does not specify that the youth moved onto the newly exposed shore. `pl059` says `looking up from the shore`, making that exact position more certain than the source. This is illustrative inference, not an established contradiction. Unchanged from R6. | Keep a shoreline in view without requiring the boy to stand on it. |

R7 changed spoken text for `pl008`, `pl009`, `pl020`, `pl017`, `pl051`, `pl052`, `pl055`, `pl026`, `pl059`, `pl085`, and `pl099` (confirmed in the working diff against committed R6). I checked each new wording against the source: **`pl020` is the material regression**; the other ten changed lines remain source-consistent. The 88 prompts did not change in this diff.

## All 91 spoken rows checked against the pinned text

The IDs below enumerate all 91 rows in `claims.md`, in narration order. `EDIT` is audience copy, not a historical event. Source line references point to the pinned `2811.txt`; qualified rows are discussed above. No other spoken contradiction was found.

| Claim IDs audited | Source lines | Result |
| --- | --- | --- |
| `pl001, pl002, pl003, pl004, pl005, pl006` | 3537–50; 3600–17; 3655–59; 3676–91 | Opening montage maps to the two letters. `pl003` singular-letter precision note. Its road, crowd, rescue, mother, death, and witness hooks otherwise follow the source. |
| `pl007, pl008, pl009, pl010, pl020, pl011, pl012` | 3519–36 | Fleet command, mother's alert, the uncle's meal/book and view of the pine cloud, changing colour, mountain uncertainty, and later Vesuvius identification match. **`pl020` attribution requires correction.** |
| `pl013, pl014, pl015, pl016, pl017` | 3537–45 | Initial light vessel, nephew's declined invitation for assigned writing, Rectina's note/villa and sea escape all match. |
| `pl018, pl019` | 3546–54; 3634–35 | Change to rescue galleys and the nephew staying behind match. |
| `pl114, pl047, pl048, pl021, pl049, pl050, pl051, pl046, pl052, pl023, pl053` | 3634–52 | Studies, bath/supper, disturbed sleep, worsening quake, mother, court, age 18, Livy extracts, Spanish visitor's rebuke, continued reading and dim morning match. `pl052`'s pause is harmless staging. |
| `pl054, pl025, pl055, pl026, pl115` | 3652–61 | Faint dawn, narrow unsafe court, departure, crowd pressure, stopping outside the houses and the previously ordered chariots match. |
| `pl056, pl057, pl058, pl027, pl059` | 3660–68 | Shaking chariots, stone supports, receding sea, extended shore, stranded animals and dark cloud match. `pl057` specifies an unsupported wheel placement. |
| `pl060, pl028, pl061, pl111, pl062, pl063, pl064` | 3666–78 | Cloud flashes and flame, Spanish friend's conditional plea, the mother's and son's answer, his exit, and cloud concealing Capreae and the Misenum promontory match. The friend's description of the uncle's wishes remains **his conjecture**, as the script says. |
| `pl065, pl029, pl110, pl067, pl068` | 3679–86 | Begging/urging/commanding, mother-son refusal and hand, her reluctant compliance and self-reproach match. `pl029`'s reported walking speed needs tightening. |
| `pl069, pl070, pl030, pl071, pl072, pl031, pl073` | 3686–97 | Initially light ash, pursuing mist, leaving the crowded road, sitting, room-like darkness and the question about locating relatives match. |
| `pl074, pl032, pl075, pl112, pl033` | 3694–3701; 3711–15 | Shouting, recognition by voice, fear for family, death wishes, pleas to gods, and end-of-world **beliefs** match, with no belief promoted to established disaster fact. |
| `pl076, pl077, pl034, pl078, pl079, pl080, pl081, pl092, pl082` | 3702–15 | The town damage/fire rumours are explicitly false; glow and distant fire, returning darkness, heavy ash and Pliny's personal interpretation match. |
| `pl083, pl035, pl036, pl084, pl085, pl037, pl113, pl086, pl087` | 3715–27 | Return of daylight and dim sun, tired eyes, ash cover, return to Misenum, uneasy night/quake, fearful predictions and waiting for news match. R7's `原來的城鎮` is the previously named Misenum. |
| `pl088, pl045, pl043, pl089, pl091, pl099` | 3563; 3600–17; 3625–30; 3720–27 | Uncle's Stabiae death, third-day intact remains, **conjectural** cause, firsthand versus immediate-report boundary, Tacitus's second request, and younger Pliny at Misenum rather than Pompeii match. R7's `海灣對岸的軍港` is compatible with Misenum fleet base. |
| `pl100, pl101` | `EDIT` | Audience question and subscription invitation; no new historical assertion. |

## All 88 written still prompts checked

Every ID below has a nonempty `still` prompt in `video.json`; the numbers are scene positions. These are judgments about written prompts only. The outro scene 89 contains spoken `pl099`–`pl101` and has no still prompt.

| Scene positions / still prompt IDs | Source lines | Visual result |
| --- | --- | --- |
| 1–6: `pl001, pl002, pl003, pl004, pl005, pl006` | 3537–50; 3655–59; 3676–91 | Coastal bay, boy and mother, uncle and ship, road/cloud. No nephew aboard or Pompeii location. |
| 7–13: `pl007, pl008, pl009, pl010, pl020, pl011, pl012` | 3519–36 | Uncle, mother, viewing point and cloud fit. `pl020` image of uncle studying the cloud makes the **spoken** writer-pronoun regression especially easy to hear; the image itself does not depict him writing. |
| 14–18: `pl013, pl014, pl015, pl016, pl017` | 3537–45 | Small vessel, nephew staying with writing, Rectina note. No false voyage by the nephew. |
| 19–20: `pl018, pl019` | 3546–54 | Rescue galley and uncle leaving harbor fit. |
| 21–31: `pl114, pl047, pl048, pl021, pl049, pl050, pl051, pl046, pl052, pl023, pl053` | 3634–52 | Study, disturbed sleep/quake, court, Livy extracts and visitor fit the sequence. Scenes 29–30 omit the book visibly in the youth's hand; see prompt fidelity note. |
| 32–36: `pl054, pl025, pl055, pl026, pl115` | 3652–61 | Faint dawn, shaking buildings, departure, crowd and chariot at a distance fit. |
| 37–41: `pl056, pl057, pl058, pl027, pl059` | 3660–68 | Chariot, stones, sea withdrawal, shore animals and cloud fit. Scene 38 specifies wheel bracing; scenes 40–41 infer the youth's exact shore footing. |
| 42–48: `pl060, pl028, pl061, pl111, pl062, pl063, pl064` | 3666–78 | Cloud flashes, Spanish visitor, road and island concealment fit; no alleged Misenum fire is depicted. |
| 49–53: `pl065, pl029, pl110, pl067, pl068` | 3679–86 | Mother's appeal, son's hand and reluctant movement fit. The prompts do not visually claim a particular cause of her slower escape. |
| 54–60: `pl069, pl070, pl030, pl071, pl072, pl031, pl073` | 3686–97 | Ash, pursuing mist, leaving the crowded road and sudden abnormal darkness fit. The faint rim/ambient light is an illustrative way to show figures. |
| 61–65: `pl074, pl032, pl075, pl112, pl033` | 3694–3701 | Voices and fear are depicted as human reactions in the darkness, not proof of a world's end. |
| 66–74: `pl076, pl077, pl034, pl078, pl079, pl080, pl081, pl092, pl082` | 3702–15 | Rumour shown as speech/listening, not actual town damage; glow, distant fire, darkness and ash follow the account. |
| 75–83: `pl083, pl035, pl036, pl084, pl085, pl037, pl113, pl086, pl087` | 3715–27 | Sunlight returns weakly, ash appears, then night at Misenum. `pl085`'s house is illustrative; source only specifies return to the town. |
| 84–88: `pl088, pl045, pl043, pl089, pl091` | 3563; 3600–17; 3625–30 | Adult letter writer visualizes later reporting and preserves the eyewitness boundary. No corpse, shore death witnessed by nephew, or verified toxicology is pictured. |

## Alignment check

Independent parsing found **91 script spoken lines, 91 distinct `claims.md` IDs, 91 video spoken lines, 89 scenes, and 88 unique nonempty still prompts**. The script, claim, and video spoken texts match in order with **zero mismatches**; `pl099`–`pl101` are the three distinct IDs in the one outro scene. Each claim tag points to a defined source segment or `EDIT`. The source and prompt findings above are content judgments, separate from that mechanical alignment.
