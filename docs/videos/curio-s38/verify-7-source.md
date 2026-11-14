# Curio S38 R7 source and still-prompt audit

**Verdict: PASS for this frozen R7 script, claims, and static still-prompt set.** The fresh blind review was sealed first at `/tmp/curio_s38_r7_fresh_blind_seal.md` (13/13 official yes answers and 13 separate comprehension answers). This audit began only after that seal. I made no episode edits and generated no media.

## Exact inputs and integrity

| Input | SHA-256 / result |
| --- | --- |
| GITenberg `4200.txt`, commit `68fcf49f70ee793b989a6fd0464264d55beb4451` | `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` — local checkout HEAD and all three available local copies agree with `research.md` |
| `docs/videos/curio-s38/script.md` | `8aeec7edaaa87f571e66894f0367fc101ec19ad70011bc0e526fef489a073a6d` |
| `docs/videos/curio-s38/video.json` | `bdbdb58148a510327bb290a80990a94d7cc4108ed7b6526a02b984e5c4f3ce32` |
| `docs/videos/curio-s38/claims.md` | `e4920984987d17ed3211f82062bca185f1c75b4f4e9a67569d46b569d992d2f4` |
| `node tools/video/cli.mjs lint --slug curio-s38 --json` | Exit 0; 0 errors, 0 warnings; 112 lines, 8 chapters, estimated 9.9983 minutes |

The September 2–6 diary text was read continuously at `4200.txt` L65795–66175, keeping the later editor's bracketed inserts separate from Pepys's own entries. The `research.md` D2a–D6 labels and `claims.md` evidence column were compared with that text. Machine comparison found exactly 112 ordered unique IDs (`pf001`–`pf112`) in script, claim table and manifest; all 112 spoken texts match exactly in all three, every manifest scene has one matching line, every claim uses an established diary code or `EDIT`, and all 111 `shot` scenes have nonempty still prompts. `pf112` is the sole outro.

## Source and chronological checks

- **2 September witness limits:** Jane's 300-house report stays hearsay (`pf011`–`pf012`; L65804–65806). Pepys first worries about Michell from the Tower (`pf014`; L65807–65812), hears the baker-house origin from the Tower lieutenant (`pf016`–`pf017`; L65812–65815), and sees Michell's house burned only once on the boat (`pf019`; L65816–65819). The king's direction via Pepys is oral (`pf024`–`pf027`; L65835–65845). His later Coventry request is written on 4 September (`pf076`; L66008–66012).
- **2 September order repaired:** The diary has Tom Hater arrive with rescued goods and receive an invitation to lodge (L65939–65943), then recurring fire news prompts Pepys to pack (L65943–65945), moonlight goods go into the garden (L65945–65947), then Hater helps move money and iron chests into the cellar (L65947–65948); Hater gets little sleep later (L65952–65954). Current `pf047`→`pf048`→`pf049`→`pf050` and corresponding prompts now follow that order. The office-held gold bags and papers in L65948–65950 are simply omitted, not mislocated into the cellar.
- **3–4 September:** Pepys moves goods, not an itemized inventory, on 3 September (L65965–65974). On 4 September Batten first pits *his* wine with Pepys's office papers; only in the evening do Pepys and Pen dig another pit for *their* wine and Pepys's `Parmazan` cheese (L65997–66002). `pf067`–`pf073` and the two-pit visuals preserve this ownership and order. The diary then looks back with “This afternoon” to an earlier garden discussion (L66004–66009); R7 omits that flashback and starts `pf075` with Pen's documented **night** trip to arrange workers for the next morning, followed by Pepys's letter and lack of reply (`pf076`–`pf077`; L66010–66012). Thus this scene has no same-day reverse jump.
- **5–6 September:** The house and office survive, and Pepys attributes the nearby stop to blown-up houses and yard workmen (L66083–66093). He saw his cargo watched *on boats* at Deptford on 5 September (`pf089`; L66083–66085), then landed it at Carteret's on 6 September (`pf107`; L66165–66167). His limited “nothing missed I could see, or hurt” is rendered as his observation, not a formal tally (`pf108`). The reviewed entries do not give the buried cheese's size, price, or retrieval (`pf073`, `pf110`). The 6 September “our fears over” phrase has its diaried context at L66168–66170; `pf109` gives no invented writing time.

## Full still-prompt review

All 111 prompts were read against their paired spoken line and the pinned diary. The prompt ledger below records each ID. Notable boundary checks: `pf013`–`pf019` do not make Pepys witness ignition or identify Michell's lost house from the Tower; `pf023`–`pf027` do not depict a written royal order; `pf047`–`pf050` show arrival, packing, garden, cellar in the source order; `pf068`–`pf072` keep the first and second pits distinct; `pf075`–`pf077` show a night departure, written request, and no answer; `pf085` includes his wife in the moonlit boat; `pf089` and `pf106` show goods still on a guarded cargo boat before `pf107` unloads them; `pf108` shows a look at goods, not itemized stocktaking. Blank diary pages avoid fabricated legible historical text.

Two details remain illustration choices rather than new historical assertions: `pf076` uses an unnamed messenger to signal dispatch of the attested letter; the diary does not name a carrier. `pf098` focuses on one guard of goods in Moorfields although the diary says the field was crowded; a future rendered-image review should ensure the image does not imply an empty field. The `pf040` bridge-centered prompt should show fires upstream and downstream, as narrated, rather than suggest two different bridges. None of these prompts states a contrary historical outcome in the frozen text.

This passes the preproduction source and prompt gate only. It does not verify generated stills, recorded speech, or measured duration of the R7 revision.

## Per-line claim and still-prompt ledger

`Pass` means that the specific line's source meaning and its paired prompt were read and found consistent. Diary references below are 1-based lines in the pinned `4200.txt`; `EDIT` marks the two nonhistorical audience/channel lines. The `Still cue` identifies the paired prompt; `—` is the unprompted outro.

| ID | Diary evidence | Claim | Still | Still cue |
| --- | --- | --- | --- | --- |
| pf001 | L66000–66002 | Pass | Pass | Medium shot a seventeenth-century city diarist and one fellow official digging a pit in a walled garden, soft evening light |
| pf002 | L66000–66002 | Pass | Pass | Close shot a secretary lowering a plain piece of hard cheese beside wine vessels into a garden pit, soft evening light |
| pf003 | L65990–66002 | Pass | Pass | Close shot a worried householder looking from a garden pit toward packed household crates, muted evening light |
| pf004 | L66085–66093 | Pass | Pass | Wide shot a clerk watching distant flames beyond rooftops from a walled garden, overcast evening light |
| pf005 | L66000–66175 (silence) | Pass | Pass | Close shot a reader holding an unlettered diary beside a plain cheese shape, soft desk light |
| pf006 | L65795–65803 | Pass | Pass | Medium shot a young maid peering from an upper window toward distant London firelight before dawn |
| pf007 | L65795–65803 | Pass | Pass | Medium shot a sleepy city secretary in a nightgown approaching an upper window, predawn lamplight |
| pf008 | L65795–65803 | Pass | Pass | Close shot a householder judging distant red glow beyond dark rooftops from an upper window, predawn light |
| pf009 | L65795–65803 | Pass | Pass | Medium shot a clerk settling back under a plain blanket as distant glow stays beyond a window, predawn light |
| pf010 | L65795–65803 | Pass | Pass | Medium shot a writer leaning from a window to inspect distant smoke, early grey daylight |
| pf011 | L65804–65807 | Pass | Pass | Medium shot a maid anxiously telling a diarist news in a modest London room, soft morning light |
| pf012 | L65804–65807 | Pass | Pass | Close shot a secretary listening to a maid beside an unlettered note, soft morning light |
| pf013 | L65807–65812 | Pass | Pass | Wide shot a city householder on a tower platform watching burning houses near a stone bridge, overcast morning light |
| pf014 | L65807–65812 | Pass | Pass | Medium shot a worried diarist on a Tower platform looking toward fire at the London Bridge end, grey daylight |
| pf015 | L65809–65824 | Pass | Pass | Medium shot a writer gripping a tower rail while watching smoke rise from a city street, overcast light |
| pf016 | L65812–65815 | Pass | Pass | Medium shot a tower officer speaking to a diarist beside an unlettered city map, grey daylight |
| pf017 | L65812–65815 | Pass | Pass | Medium shot a thoughtful diarist looking out from a Tower window toward distant smoke, grey daylight |
| pf018 | L65816–65824 | Pass | Pass | Wide shot a householder seated in a small boat watching a family load crates onto a flat cargo boat, cloudy daylight |
| pf019 | L65816–65824 | Pass | Pass | Medium shot a worried clerk in a riverboat viewing a burned house near city Bridge, cloudy daylight |
| pf020 | L65816–65824 | Pass | Pass | Medium shot a London resident tipping a household bundle into the Thames, soft daylight |
| pf021 | L65816–65824 | Pass | Pass | Wide shot a riverside resident hurrying toward a boat with smoke behind a house, cloudy daylight |
| pf022 | L65827–65835 | Pass | Pass | Wide shot a secretary in a riverboat watching wind-driven smoke cross city rooftops, cloudy daylight |
| pf023 | L65835–65846 | Pass | Pass | Medium shot a London householder hurrying toward a plain Whitehall palace entrance, midday light |
| pf024 | L65835–65846 | Pass | Pass | Medium shot a clerk speaking earnestly before an English ruler in a plain seventeenth-century chamber, soft light |
| pf025 | L65835–65846 | Pass | Pass | Close shot a writer pointing to a gap between simple house blocks on a blank tabletop plan, lamplight |
| pf026 | L65835–65846 | Pass | Pass | Medium shot a seated ruler speaking firmly to a London diarist in a plain chamber, mild indoor light |
| pf027 | L65835–65846 | Pass | Pass | Medium shot a seventeenth-century duke gesturing toward a blank city plan inside a hall, mild light |
| pf028 | L65860–65867 | Pass | Pass | Medium shot a weary city mayor leaning beside a narrow city street while a householder approaches, grey daylight |
| pf029 | L65860–65867 | Pass | Pass | Close shot an exhausted mayor speaking to a clerk near drifting smoke, muted daylight |
| pf030 | L65860–65867 | Pass | Pass | Medium shot a weary city mayor resting against a plain doorway, grey daylight |
| pf031 | L65860–65867 | Pass | Pass | Medium shot a weary mayor leaving a city street as a diarist watches, grey daylight |
| pf032 | L65875–65877 | Pass | Pass | Wide shot a London resident setting one household chest inside a crowded church, muted daylight |
| pf033 | L65856–65860; L65888–65891 | Pass | Pass | Wide shot one London resident carrying a bundle past a loaded horse cart, overcast daylight |
| pf034 | L65867–65870; L65997–66002 | Pass | Pass | Close shot a clerk observing sealed barrels near a city riverside warehouse, soft grey daylight |
| pf035 | L65877–65888 | Pass | Pass | Medium shot a London writer welcoming one guest at a modest dining room door, soft midday light |
| pf036 | L65877–65888 | Pass | Pass | Medium shot a worried diarist sitting before a plentiful dinner spread while smoke shows through a window, soft midday light |
| pf037 | L65877–65888 | Pass | Pass | Medium shot a concerned woman speaking at a dining-room doorway, muted midday light |
| pf038 | L65888–65893 | Pass | Pass | Medium shot a London porter loading a household crate into a horse cart on a crowded city street, grey afternoon light |
| pf039 | L65897–65904 | Pass | Pass | Close shot a clerk looking from a smoky city street toward the Thames, soft afternoon light |
| pf040 | L65897–65904 | Pass | Pass | Wide shot a writer in a riverboat watching distant fires on both sides of a stone bridge, cloudy afternoon light |
| pf041 | L65908–65919 | Pass | Pass | Wide shot a London diarist looking across cargo boats carrying household crates on the Thames, afternoon light |
| pf042 | L65908–65919 | Pass | Pass | Medium shot a riverside resident steadying a small virginal keyboard instrument inside a low cargo boat, cloudy daylight |
| pf043 | L65922–65927 | Pass | Pass | Close shot a householder shielding his face from drifting sparks on a riverboat, dusk light |
| pf044 | L65922–65927 | Pass | Pass | Wide shot a riverside resident watching sparks pass above separate rooftops, muted dusk light |
| pf045 | L65928–65938 | Pass | Pass | Wide shot a writer watching a distant arc of fire above the London riverbank, dusk light |
| pf046 | L65928–65938 | Pass | Pass | Close shot a tearful diarist looking across the river at distant firelight, muted dusk light |
| pf047 | L65939–65943 | Pass | Pass | Medium shot a fire-displaced guest arriving with a few household bundles at a seventeenth-century London home at night, candlelight |
| pf048 | L65943–65945 | Pass | Pass | Close shot a householder packing his own belongings into a plain wooden chest in a seventeenth-century room, candlelight |
| pf049 | L65945–65947 | Pass | Pass | Medium shot household goods being carried into a small walled garden by moonlight in seventeenth-century London |
| pf050 | L65947–65954 | Pass | Pass | Medium shot a tired guest and householder lowering an iron chest into a plain cellar at night, candlelight |
| pf051 | L65945–65958 | Pass | Pass | Close shot a diarist comparing a locked chest and a plain wooden box by a garden door, lamplight |
| pf052 | L65956–65964 | Pass | Pass | Medium shot a city secretary meeting a horse cart outside his home before dawn, cool grey light |
| pf053 | L65956–65964 | Pass | Pass | Medium shot a householder in a nightgown riding a cart beside a closed chest, predawn light |
| pf054 | L65956–65964 | Pass | Pass | Medium shot a clerk carrying a closed chest into a suburban London doorway, morning light |
| pf055 | L65956–65964 | Pass | Pass | Wide shot a writer standing among household crates in a crowded receiving room, soft morning light |
| pf056 | L65965–65974 | Pass | Pass | Medium shot a London diarist carrying a household bundle out of a home toward a river landing, grey daylight |
| pf057 | L65965–65974 | Pass | Pass | Wide shot a London secretary inspecting a low flat cargo boat at a Thames landing, cloudy daylight |
| pf058 | L65965–65974 | Pass | Pass | Medium shot a porter carrying a wooden crate across a crowded city hill, overcast light |
| pf059 | L65965–65974 | Pass | Pass | Wide shot a clerk holding a box blocked before a crowded narrow city postern, overcast light |
| pf060 | L65965–65974 | Pass | Pass | Medium shot a mother placing a small bundle on a flat cargo boat beside the Thames, soft light |
| pf061 | L65965–65974 | Pass | Pass | Medium shot a diarist carrying a small wooden crate toward a Thames cargo boat, soft daylight |
| pf062 | L65984–65988 | Pass | Pass | Medium shot a tired secretary spreading a simple quilt on an office floor, lamplight |
| pf063 | L65984–65988 | Pass | Pass | Close shot a householder eating a plain cold meal beside packed boxes, soft lamplight |
| pf064 | L65990–66002 | Pass | Pass | Medium shot a clerk looking toward large wine vessels beside a packed garden path, soft night light |
| pf065 | L65990–65992; L65997–66002 | Pass | Pass | Medium shot a London writer carrying a last wooden box toward a flat river cargo boat, overcast morning light |
| pf066 | L65992–65997 | Pass | Pass | Wide shot a diarist watching smoke approach houses along a narrow London street, muted afternoon light |
| pf067 | L65997–66000 | Pass | Pass | Medium shot an older city official studying wine vessels in a walled garden, soft afternoon light |
| pf068 | L65997–66000 | Pass | Pass | Medium shot an older official lowering a wine vessel into a garden pit, afternoon light |
| pf069 | L65997–66000 | Pass | Pass | Close shot a clerk placing tied blank office papers beside a wine vessel in a garden pit, soft light |
| pf070 | L65997–66002 | Pass | Pass | Close shot a worried writer looking over tied blank office papers beside a first garden pit, soft afternoon light |
| pf071 | L65997–66002 | Pass | Pass | Medium shot a diarist and one fellow official digging a second separate pit beside wine vessels in a walled garden, soft evening light |
| pf072 | L65997–66002 | Pass | Pass | Close shot a secretary lowering a plain hard cheese piece beside a wine vessel into a second garden pit, soft evening light |
| pf073 | L65997–66002 | Pass | Pass | Close shot a reader studying an unlettered diary page beside an ordinary hard cheese piece, desk light |
| pf074 | L66004–66009; L66085–66093 | Pass | Pass | Medium shot a worried clerk watching his still-standing office from a garden path, evening light |
| pf075 | L66004–66012 | Pass | Pass | Medium shot a city official leaving a walled garden toward a dark London street, smoky early night light |
| pf076 | L66004–66012 | Pass | Pass | Medium shot a London writer handing a plain folded letter to a messenger at an office doorway, lamplight |
| pf077 | L66004–66012 | Pass | Pass | Close shot a worried diary writer looking toward a closed office doorway beside an empty desk, lamplight |
| pf078 | L66012–66020 | Pass | Pass | Medium shot a London householder eating a plain mutton supper beside packed boxes, night light |
| pf079 | L66012–66020 | Pass | Pass | Medium shot a city householder stepping from a supper table to watch a fiery sky from a garden, night light |
| pf080 | L66020–66026; L66051–66052 | Pass | Pass | Wide shot a writer watching a distant house collapse behind drifting smoke on a London street, night light |
| pf081 | L66020–66026; L66051–66052 | Pass | Pass | Medium shot a diarist observing an open gap between houses and fire from a safe street corner, night light |
| pf082 | L66070–66093 | Pass | Pass | Close shot a worried secretary watching smoke beyond his narrow lane, muted night light |
| pf083 | L66070–66078 | Pass | Pass | Medium shot a worried woman waking a resting householder in a seventeenth-century office, predawn light |
| pf084 | L66070–66078 | Pass | Pass | Wide shot a clerk looking toward smoke beside a church at the foot of his lane, predawn light |
| pf085 | L66070–66078 | Pass | Pass | Medium shot a worried London diarist aboard a small Thames boat with his wife beside him, moonlit predawn |
| pf086 | L66070–66078 | Pass | Pass | Wide shot a diarist in a riverboat watching a broad glow above London rooftops, moonlit predawn |
| pf087 | L66081–66085 | Pass | Pass | Close shot a secretary locking a plain chest inside a suburban room, soft morning light |
| pf088 | L66081–66085 | Pass | Pass | Wide shot a householder seated in a small boat heading back toward a smoky city waterfront, morning light |
| pf089 | L66081–66085 | Pass | Pass | Wide shot a clerk in a small boat viewing a cargo vessel attended by one ordinary watcher at Deptford, morning light |
| pf090 | L66085–66093 | Pass | Pass | Medium shot a relieved writer approaching his intact home beside a smoky street, grey daylight |
| pf091 | L66085–66093 | Pass | Pass | Close shot a diarist placing one hand on an intact office door, soft grey light |
| pf092 | L66085–66093 | Pass | Pass | Medium shot a diarist studying a scorched church entrance near an intact lane, grey daylight |
| pf093 | L66085–66093 | Pass | Pass | Medium shot a workman clearing fallen timber to make a gap ahead of distant flames, daylight |
| pf094 | L66093–66098 | Pass | Pass | Medium shot a clerk looking up toward a nearby church tower from a smoky street, grey daylight |
| pf095 | L66093–66098 | Pass | Pass | Wide shot a writer looking across burned London streets from a church tower, soft grey daylight |
| pf096 | L66093–66098 | Pass | Pass | Medium shot a wary diarist descending a church stairway with distant smoke outside, soft daylight |
| pf097 | L66101–66110 | Pass | Pass | Close shot a walking diarist stepping past glowing street coals, muted daylight |
| pf098 | L66101–66110 | Pass | Pass | Wide shot a displaced London resident guarding household bundles in an open field, grey daylight |
| pf099 | L66111–66115 | Pass | Pass | Close shot a diarist holding a small warped piece of old window glass, soft daylight |
| pf100 | L66117–66121 | Pass | Pass | Medium shot a writer instructing one watchman beside a plain office doorway, night light |
| pf101 | L66117–66121 | Pass | Pass | Medium shot an exhausted diarist sleeping on a simple office quilt, muted night light |
| pf102 | L66127–66146 | Pass | Pass | Wide shot a sleeping secretary beside an office window facing dark London rooftops, predawn light |
| pf103 | L66127–66146 | Pass | Pass | Medium shot a householder noticing smoke from a fresh street fire in daylight |
| pf104 | L66127–66146 | Pass | Pass | Medium shot one London worker beside freshly extinguished smoking timber on a city street, morning light |
| pf105 | L66158–66159 | Pass | Pass | Wide shot a writer looking over a damaged London riverbank from a boat, overcast daylight |
| pf106 | L66083–66085; L66165–66167 | Pass | Pass | Medium shot a diarist viewing cargo crates aboard a flat boat attended by one ordinary watcher at Deptford, daylight |
| pf107 | L66165–66168 | Pass | Pass | Medium shot a secretary directing one porter to unload a wooden chest at a Deptford landing, soft daylight |
| pf108 | L66165–66168 | Pass | Pass | Close shot a relieved householder inspecting an unbroken household chest by a river landing, daylight |
| pf109 | L66168–66170 | Pass | Pass | Close shot an unlettered diary page on a plain desk, soft neutral light |
| pf110 | L66000–66175 (silence) | Pass | Pass | Close shot a reader pausing over an unlettered diary page beside an empty patch of desk, soft light |
| pf111 | EDIT | EDIT | Pass | Medium shot one seventeenth-century householder looking into an empty pit inside a walled garden, soft evening light |
| pf112 | EDIT | EDIT | N/A | — |
