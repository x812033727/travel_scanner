# S40 R3 fresh source and still-prompt audit

Audit order: first froze the script-only review in `/tmp/curio_s40_r3_fresh_blind_seal.md` (SHA-256 `9332a96cdbdfd06ea6099ee6db8dccbe6974268b616809b34f2eca228e9fc992`); only then opened `research.md`, `claims.md`, `video.json`, prior context, and the three pinned complete source texts. No S40 episode file was edited and no paid media operation was run.

## Exact inputs and mechanical checks

| Input | SHA-256 |
| --- | --- |
| `script.md` | `b01c0ef524555d798efcb09b2503cffe0f10cdaee9a3bb9867b11a1b8540c1e7` |
| `claims.md` | `4ae1ae3b3f05f3ca96e8b5ca0bf696186991306d2d0951f16a6816426eb9a922` |
| `research.md` | `a35831dc5c00150229c4f0b97cb57439fc76baa62cbfbf48327864a19b90037e` |
| `video.json` | `1a12e15009519b03a0a09cda577fe0be12cc58ea0aa51b002cd20208f6f3394e` |
| Plutarch, pinned `674.txt`, commit `6aea7c6d83ee3596f9106d2d832d705aa4ed4620` | `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1` |
| Suetonius, pinned `6400.txt`, commit `bb5afc956095e248b2287cce2a4d3ebe394e5d31` | `082eee2d55230c1f75f9476dae537fc37851487bc1cce5dfaef1ef2a67558b15` |
| Cassius Dio, pinned `10162.txt`, commit `06d7e6a6f7fd5f45fbaacc3ade5397085290113b` | `b0ce5d998a6eb78162fc6658b24b9efd0fd0aa23ce6a9bbe9fd10b584fdf4e83` |

I downloaded and hashed each complete pinned translation anew. Source loci below are **original full-text line numbers**, not line numbers of a clipped excerpt: `P` = Plutarch, `S` = Suetonius, `D` = Dio. These later English translations support statements *about what the authors wrote*, not certainty about the unwitnessed event.

`node tools/video/cli.mjs lint --slug curio-s40 --json`: **0 errors, 0 warnings**, 84 spoken lines, estimated 9.27 minutes, eight chapters. Structural parse: 84 sequential `cl001`–`cl084` scenes; 83 `shot` scenes with 83 nonempty `still` prompts and one outro; 83 sequential claim rows. Every claim-row narration and every scene narration matches the script text exactly by ID. The outro text also matches. `look.preset` is `cute-mystery`; music is configured; there are 25 declared loops. The blind narrative review is **12/13 yes**, with `payoffs` no.

## Findings requiring action

1. **Narrative payoff block — child kingship.** `cl012` asks Octavian to keep the throne for Cleopatra's children (`script.md` L55; P61452–54). `cl013` answers only whether Proculeius talks her out of the tomb (L59). `cl033` says the children would be sent away (L143; P61582–87), but the script never says whether the throne request was granted or denied. The actual source passage has Proculeius tell her to trust Octavian, **not** grant the request. An explicit “he gave no promise about the throne” at the negotiation could close the local stake without inventing the children's later fate. This is why the sealed `payoffs` judgment is no.
2. **Claim-pointer block, `cl009`.** The narration's tomb-treasure location is supported by P61323–30, and Octavian's treasure/captive motive by P61444–47. Its sole `P-0` research pin starts at P61395. The text is historically supported by the same complete pinned Plutarch translation, but the row's narrow pointer cannot verify “陵墓裡的財寶” by itself. Expand `P-0` to include P61323–30 or add a direct companion pin.
3. **Claim-pointer block, `cl029` and `cl030`.** Both cite `P-a`, whose stated range ends at P61575. Permission to keep the omitted items and the favorable treatment are P61576–78 (`cl029`); Plutarch's reversal that Octavian was deceived is P61579–80 (`cl030`). The full pinned text supports both narrations. Add `P-b` to those rows or extend `P-a` through P61580.

Historical narration wording: **83/83 pass** against the verified complete texts, including its attribution and uncertainty. Narrow research/claim pointers: **80/83 pass, 3 block** (`cl009`, `cl029`, `cl030`). Still-prompt text: **83/83 pass** under the Curio series standard of relevant cartoon illustration without a material source contradiction. This does not certify generated images, because none was generated or reviewed here. Overall **BLOCK** until the narrative payoff and pointer gaps are resolved and a fresh blind review is run on any changed script.

## Source and still check, every row

`N` is source support for the spoken wording; all N entries below pass. `R` is the cited *research range*; an `R!` row needs the pointer fix described above. `V` is prompt-text compatibility; all V entries below pass. Short visual notes identify the inspected subject, not an approved rendered image.

| ID | Exact source locus and N/R judgment | V prompt subject and judgment |
| --- | --- | --- |
| cl001 | P61614–19, N/R pass | Fig bearer at guard, pass |
| cl002 | P61614–19, N/R pass | Guard lifts fig leaves, pass |
| cl003 | P61638–42, N/R pass; snake expressly hearsay | Storyteller and basket, pass |
| cl004 | P61620–28, N/R pass | Courier with sealed scroll, pass |
| cl005 | P61627–29, P61651–54, N/R pass | Snake-bearing triumph statue, pass |
| cl006 | P61401–03, N/R pass | Wounded Antony carried by servants, pass |
| cl007 | P61403–06, N/R pass | Queen pulls rope at high opening, pass |
| cl008 | P61417–32, N/R pass | Queen with covered Antony, pass |
| cl009 | P61323–30 and P61444–47, N pass; **R!** P61323–30 lies outside `P-0` | Biographer sketching monument, pass |
| cl010 | P61444–47, S2805–07, N/R pass | Empty captive platform, pass |
| cl011 | P61444–51, N/R pass | Proculeius at barred tomb door, pass |
| cl012 | P61448–54, N/R pass | Queen speaks through door, pass |
| cl013 | P61448–60, N/R pass | Envoy notices window, pass |
| cl014 | P61403–06, P61456–60, N/R pass | Tomb window and rope, pass |
| cl015 | P61456–61, N/R pass | Envoy points toward ladder, pass |
| cl016 | P61459–62, N/R pass | Envoy climbs ladder, pass |
| cl017 | P61463–67, N/R pass | Queen's hand nears dagger, pass |
| cl018 | P61466–73, N/R pass | Plain-robed envoy holds dagger, pass |
| cl019 | P61473–76, N/R pass | Attendant watches royal chamber, pass; tomb setting could be made more explicit |
| cl020 | P61530–38, N/R pass; a planned fast, not an observed prolonged fast | Queen leaves food untouched, pass |
| cl021 | P61535–38, N/R pass; Plutarch reports Olympus's written account | Biographer with scroll, pass |
| cl022 | P61538–42, N/R pass; Octavian *suspected* and threatened children | Queen resumes meal, pass |
| cl023 | P61544–47, N/R pass | Queen rises before commander, pass |
| cl024 | P61555–61, N/R pass | Queen pleads with commander, pass |
| cl025 | P61561–62, P61574–75, N/R pass | Commander watches plea, pass |
| cl026 | P61563–66, N/R pass | Steward points at list, pass |
| cl027 | P61565–74, N/R pass; Plutarch explicitly says she caught his hair | Queen grasps steward's hair, pass |
| cl028 | P61568–74, N/R pass | Small jewelry box as pleaded gift, pass |
| cl029 | P61574–78, N pass; **R!** P61576–78 outside `P-a` | Commander permits gift box, pass |
| cl030 | P61574–80, N pass; **R!** P61579–80 outside `P-a` | Reassured commander departs, pass |
| cl031 | P61582–85, N/R pass | Young courier with note, pass |
| cl032 | P61582–85, N/R pass | Young Roman brings message, pass |
| cl033 | P61584–87, N/R pass | Queen reads note beside travel bundles, pass |
| cl034 | P61587–61609, N/R pass as question | Guarded tomb and Antony's grave, pass |
| cl035 | P61587–90, N/R pass | Queen petitions official, pass |
| cl036 | P61589–91, N/R pass | Queen and women approach grave, pass |
| cl037 | P61591–61609, N/R pass; attributes graveside speech to biography | Queen by grave wall, pass |
| cl038 | P61611–13, N/R pass | Queen places garland, pass |
| cl039 | P61611–13, N/R pass | Wash basin, pass |
| cl040 | P61612–14, N/R pass | Queen at meal, pass |
| cl041 | P61614–19, N/R pass | Fig bearer approaches again, pass |
| cl042 | P61614–17, N/R pass | Basket inspection, pass |
| cl043 | P61617–19, N/R pass | Guard admires figs, pass |
| cl044 | P61618–19, N/R pass | Basket admitted through guarded door, pass |
| cl045 | P61620–22, N/R pass | Queen seals letter, pass |
| cl046 | P61620–22, N/R pass | Queen closes door with two attendants, pass |
| cl047 | P61620–36, N/R pass as stated inference from the account's deaths | Closed door, no staged eyewitness, pass |
| cl048 | P61622–26, N/R pass | Commander opens letter, pass |
| cl049 | P61625–28, N/R pass | Messenger rushes to guarded door, pass |
| cl050 | P61628–30, N/R pass | Messenger at threshold; no staged bite, pass |
| cl051 | P61630–32, N/R pass | Charmion adjusts diadem in close view, pass |
| cl052 | P61632–36, N/R pass | Failing attendant answers messenger, pass |
| cl053 | P61625–29, P61655–58, N/R pass | Commander hears messenger, pass |
| cl054 | P61657–59, N/R pass | Official and two burial biers, pass |
| cl055 | P61614–19, P61638–45, N/R pass as question | Historian compares scrolls and basket, pass |
| cl056 | P61638–42, N/R pass; alleged snake | Writer sketches tiny snake motif, pass |
| cl057 | P61638–42, N/R pass; explicitly within that version | Storyteller points to sketch, no enacted bite, pass |
| cl058 | P61638–45, N/R pass | Reader weighs basket and scroll, pass |
| cl059 | P61642–44, N/R pass; alternative vessel/spindle | Historian displays vessel and spindle, pass |
| cl060 | P61644–45, N/R pass; Plutarch says no one knows | Biographer halts writing, pass |
| cl061 | P61645–47, N/R pass; hollow hair bodkin report | Writer examines hairpin, pass |
| cl062 | P61645–51, N/R pass as question | Courier watches covered couch, pass |
| cl063 | P61646–49, N/R pass; no visible poison symptom or seen asp | Investigator in chamber, pass |
| cl064 | P61648–51, N/R pass; trail expressly alleged | Writer sketches faint trail, pass |
| cl065 | P61651–54, N/R pass; faint marks expressly alleged | Scholar sketches two tiny marks, pass |
| cl066 | P61648–54, N/R pass as source-limited inference | Reader compares vessel and hairpin, pass |
| cl067 | P61644–47, D7506–16, N/R pass as question | Official with serpent statue motif, pass; indirect bridge to Dio |
| cl068 | D7440–44, D7506–16, N/R pass | Later historian and scrolls, pass |
| cl069 | P61620–29, D7440–44, N/R pass; distinct tomb/palace accounts | Queen enters palace with attendants, pass |
| cl070 | D7491–98, N/R pass; gifts and voyage lull guards | Queen arranges travel ornaments, pass |
| cl071 | D7506–09, N/R pass as question | Dio-like historian with scroll, pass |
| cl072 | D7506–09, N/R pass; water jar or flowers as rumors | Historian compares jar and flowers, pass |
| cl073 | D7509–15, N/R pass; poisoned hair needle report | Writer places needle by scroll, pass |
| cl074 | D7513–16, N/R pass; small scratch then needle into blood is reported supposition | Scholar compares separate sketch and needle, pass |
| cl075 | D7519–21, N/R pass; viewed body and sought revival | Historian's mark sketch and physician bag, pass |
| cl076 | D7506–21, S2805–08, N/R pass as comparison/question | Reader sets aside scrolls, pass |
| cl077 | S2805–08, N/R pass; source says *supposed*, Psylli asked to suck poison | Official summons healer, pass |
| cl078 | P61651–54, S2805–07, N/R pass | Empty triumph platform, pass |
| cl079 | P61651–54, N/R pass; figure in triumph, not death evidence | Queen figure with snake motif, pass |
| cl080 | P61651–54, N/R pass; public victory imagery only | Statue snake detail, pass |
| cl081 | P61651–54, D7506–16, S2805–08, N/R pass as question | Reader with statue replica and scroll, pass |
| cl082 | P61644–54, D7506–16, S2805–08, N/R pass; none certifies bite | Three unlettered scrolls, pass |
| cl083 | P61614–19, P61651–54, N/R pass as audience question | Reader compares fig basket and statue, pass |

## Specific cross-source conclusions

- **Octavian's motive:** Plutarch gives both treasure and triumph at P61444–47; the earlier P61323–30 places valuables in the tombs. Suetonius also says he wanted her alive for his triumph at S2805–07. The script attributes motives to the author instead of asserting access to Octavian's mind.
- **Fasting and physician:** P61530–42 says she hoped to abstain, attributes this to Olympus's narrative, and says Octavian suspected it and used fear for her children. `cl020`–`cl022` retain those limits; they do not claim Olympus's original document was independently inspected.
- **Women and hair grip:** P61403–06 specifies two women hauling Antony; P61565–67 explicitly says Cleopatra grabbed her steward by the hair; P61630–36 names Iras and Charmion and their final actions. `cl007`, `cl027`, and `cl046`–`cl052` and their prompts match.
- **Dio stays distinct:** P61620–29 leaves Cleopatra in the monument; D7440–44 moves her and attendants to the palace. `cl069` states the conflict. D7491–98 adds gifts, proposed sailing, and relaxed watch. D7506–21 reports slight arm marks, jar/flowers snake, poisoned hair needle, and attempted rescue; `cl070`–`cl076` preserve those as Dio's account, not a continuation of Plutarch's observed scene.
- **Death mechanism remains unknown:** P61638–54 says “Some relate,” “Others say,” and “what really took place is known to no one”; D7506–16 likewise says no one clearly knows; S2805–08 says she was *supposed* to have been bitten. The reported sand trail, arm marks, rescue, and later triumph statue cannot diagnose the means. No prompt enacts a bite, poisoning, or confirmed hidden snake in the actual chamber. The statue is shown as an image, not evidence that anyone witnessed the death.

The visual assessment covers prompt text only. `cl019` could state “tomb chamber” more plainly to keep the Plutarch location legible; `cl067` uses a triumph statue as a loose transition to Dio. Neither prompt specifies a contradictory historical action, so both pass under the series rule that only material contradictions block an illustration. A rendered-image review would still be required after authorized production.
