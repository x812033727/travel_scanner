# Curio S38 R8 independent source and visual audit

Date: 2026-10-20. Blind narrative seal was completed first in `/tmp/curio_s38_r8_fresh_blind_seal.md`, using only script and official 13-question JSON. This report was made after that seal. I did not edit episode files or generate media.

## Exact version and checks

| Evidence | SHA-256 / revision |
| --- | --- |
| `docs/videos/curio-s38/script.md` | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` |
| `docs/videos/curio-s38/claims.md` | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` |
| `docs/videos/curio-s38/video.json` | `3dbe6dd23eedef3ff999801f6e548ab69ea480ee8a2b00095e78e1d48ec837b9` |
| GITenberg `The-Diary-of-Samuel-Pepys---Complete_4200/4200.txt` | Git commit `68fcf49f70ee793b989a6fd0464264d55beb4451`; local SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` |

I read the diary's contiguous September 2–6 entries at `4200.txt` L65795–66175, separating Pepys's diary prose from later bracketed editorial material. Mechanical comparison found **112/112** matching IDs and verbatim Chinese lines across script, claims, and `video.json`; IDs occur once and in order. There are **111/111** populated `shot` prompts plus one outro scene. Every claim reference uses a defined evidence code. `node tools/video/cli.mjs lint --slug curio-s38` exited 0: **0 errors, 0 warnings**, 112 lines, estimated 10.0 minutes. These checks were run on the hashes above.

## 112-line claim and chronology coverage

Inclusive ID ranges below cover `pf001` through `pf112` exactly once. Diary line numbers refer to the pinned `4200.txt`; `Q` means an editorial question bounded by the cited diary facts, and `E` means an explicit editorial invitation/outro.

| IDs | Diary lines | Independent check |
| --- | --- | --- |
| 001–005 | 65997–66002, 66070–66093, 66166–66175 | The first pit belongs to Batten; Pepys and Pen dig **another** pit in the evening for their wine, and Pepys adds his Parmazan cheese. The house's fate and absence of later cheese outcome are held as questions. |
| 006–010 | 65795–65803 | Jane wakes him about 3 a.m.; he wears a nightgown, sees a seemingly distant fire behind Mark Lane, sleeps again, and sees what looks like less fire around seven. |
| 011–012 | 65804–65807 | “Above 300 houses” is Jane's **hearsay**, not his count; he goes to check. |
| 013–015 | 65807–65812 | He sees fire from a Tower high place and is troubled for Michell and Sarah on the bridge. The script does not say the Tower view confirmed their house burned. |
| 016–017 | 65812–65815 | The Tower lieutenant **tells** him the Pudding Lane baker origin. The script marks this as heard rather than witnessed. |
| 018–022 | 65816–65831 | From the boat he sees Michell's house burned, goods moved to lighters or thrown into water, residents fleeing late, and high wind driving the fire inward. `pf022` is Q. |
| 023–027 | 65835–65845 | He goes to Whitehall, **orally** tells King and Duke what he saw and urges house demolition; King orders him to tell the mayor, Duke offers soldiers. No written royal order is claimed. |
| 028–031 | 65860–65866 | Mayor appears spent, says people will not obey and fire overtakes demolition, says he needs rest and not more soldiers. `pf028` is Q grounded in this meeting. |
| 032–034 | 65856–65860, 65867–65877 | Churches take household goods; loads fill streets; Thames Street has pitch/tar and warehouses of oil and wine. The final question about Pepys's wine is a forward editorial hook. The street-load detail is a general evacuation image, not a separately timed post-mayor action. |
| 035–037 | 65877–65888 | He is home around noon for a prearranged and unusually good dinner; Mrs Batelier inquires after Woolfe and Stanes during dinner, and diary says their houses burned. The script does not claim she learned this at the table. |
| 038–040 | 65888–65901 | The **second** Canning Street removal happens after dinner; then Pepys takes a boat and sees fire farther both below and above the bridge. This order is correct. |
| 041–042 | 65908–65919 | Thames is full of boats and lighters with goods; many have a pair of virginals. “Small household keyboard” is an intelligible gloss. |
| 043–046 | 65922–65938 | Wind-facing sparks, ignition across separated houses, a dusk arc of fire, and his tears are all in the diary. |
| 047–051 | 65939–65954, 65956–65958 | On returning home Pepys finds Tom Hater with a few saved goods from his burned house, invites him to lie there, then growing fire news forces packing. Goods move by moonlight into garden; **money and iron chests** go to cellar with Tom's help; Tom lies down briefly but rests little. Gold bags and account papers are separately moved to the office, so `pf050` does not conflate their storage. `pf051` anticipates next morning's first wagon load. `pf047`'s “來投宿” compresses Pepys's invitation and Tom's brief rest; do not depict a completed uninterrupted night's lodging. |
| 052–055 | 65956–65964 | Lady Batten sends cart about 4 a.m.; Pepys rides in nightgown with money and plate to Sir Rider's at Bednall Green; Rider's house is full of other people's goods. |
| 056–061 | 65965–65974 | Pepys and wife continue getting goods away, Tooker gets a lighter, they carry goods across Tower Hill, neighbor woman with child gets small goods aboard, Pepys carries some himself. The postern was impassable **with goods** in the crowd; `pf059` is a mild spoken compression, and its still correctly shows a person blocked with a box. |
| 062–064 | 65984–65988, 65997–66002 | Couple lay in office and ate prior dinner remains without fire or dishes. The difficult-to-move wine is a question whose answer comes the next day. |
| 065–070 | 65990–66000 | September 4 transfer occupies the morning into afternoon; fire reaches near Howell's in Tower Street. Batten cannot move **his** wine and digs the first pit; Pepys puts office papers there. `pf065` infers wine still present before burial, warranted by later action. |
| 071–073 | 66000–66002 | In evening Pepys and Pen dig another pit for **their** wine, and Pepys adds `my Parmazan cheese`. Diary gives no size or price. |
| 074–077 | 66004–66012 | Office feared endangered; earlier afternoon discussion leads Pen to go that night to arrange yard workmen for next morning, while Pepys writes Coventry seeking demolition permission and receives no reply. `pf074` is the narrator's question after the burial, not an assertion that the garden discussion happened afterward. |
| 078–081 | 66012–66026, 66051–66052 | Night meal is mutton shoulder without napkin; Pepys watches fiery sky and then Tower Street demolition. His account says demolition stopped fire **where done**, and the script keeps the stop local. |
| 082–084 | 66070–66074 | Forward question then around 2 a.m. September 5 his wife wakes him because fire reaches Barking Church at the lane's foot. |
| 085–089 | 66074–66085 | He decides **presently** to take wife away, takes gold and companions by Proundy's boat **down to Woolwich**; moonlit city seems almost wholly on fire. He locks gold at Shelden's, assigns wife/companion to guard, returns, and sees goods watched in lighters at Deptford. “乘船沿河往下游走” is a faithful oral simplification of downriver travel to Woolwich, with no false destination or reversal. It does not claim September 5 goods were already unloaded. |
| 090–093 | 66085–66093 | House and Office survive; Pepys hesitates to ask until he sees. Barking Church dial and porch burn; he credits demolition and King's yard workmen with a **local** stop. |
| 094–096 | 66094–66098 | He climbs Barking steeple, sees desolation and other fires, and leaves soon because afraid. |
| 097–099 | 66102–66115 | Walking among hot coals to Moorefields, refugees guarding goods there, and a melted/buckled glass piece from Mercers' Chapel are diary details. |
| 100–102 | 66117–66125, 66127–66146 | Men watch at office overnight; he sleeps well about midnight. `pf102` is Q answered by next day's separate fire. |
| 103–104 | 66127–66146 | A new fire breaks out at Bishopsgate early September 6; Pepys goes with men and they put it out quickly. No arson rumour is repeated as fact. |
| 105–108 | 66158–66159, 66166–66167, 66083–66085 | Riverfront buildings/churches are gone. September 5 watched lighters are distinct from September 6 **landing/unloading** at Carteret's; “nothing missed I could see, or hurt” supports only his visual assessment, and `pf108` preserves that limit. |
| 109–112 | 66168–66175; E | `our fears over` belongs to September 6. No cheese recovery outcome appears in the checked September 2–6 entries; `pf110` states that bounded absence. `pf111–112` are editorial invitation/outro. |

## 111 still-prompt coverage

I read each English `data.prompt` for `pf001–pf111` beside its exact Chinese line and corresponding diary span above. Inclusive groups below cover every still ID exactly once. The prompt review checks date and light, whether a visual upgrades hearsay to eyewitness knowledge, whether it changes the two pits or goods locations, and whether it turns a watched boat into an unloaded one. Cartoon props and omitted off-camera people are accepted where they do not contradict narration or source.

| Prompt IDs | Visual result |
| --- | --- |
| 001–017 | Yard pit and predawn/morning fire sequence match. `pf013–014` show fire at bridge from Tower but **do not** show Michell's house as already identified there. `pf016` shows an officer speaking, preserving oral provenance. `pf012` has an unlettered note as background prop; it should not be treated as Jane's written report. |
| 018–034 | Boat, lighters, displaced residents, Whitehall conversation, tired mayor, church goods and flammable warehouses follow the source. `pf025` and `pf027` use blank schematic plans as cartoon staging during **spoken** counsel; they do not depict a royal written order or Pepys carrying a written report. Production should keep the dialogue visually primary. |
| 035–051 | Dinner images precede `pf038`'s afternoon street removal. Dusk river fire, Tom arriving at night, moonlit garden, and Tom with Pepys lowering an **iron chest** into cellar track L65877–65954. `pf051`'s chest/box near a garden door is a transitional question image, not a claim that the office gold/account papers were stored in the cellar. |
| 052–064 | Predawn cart, nightgown, receiving house, lighter, Tower Hill, and office bedding match. `pf059` specifically shows goods blocked at the postern. `pf060` leaves the child out of frame but does not contradict the neighbor/mother action. |
| 065–082 | First pit is Batten's wine with office papers; `pf071–072` explicitly show a **second separate pit** for wine and small plain cheese. Letter, mutton supper, distant house demolition and local gap are depicted without invented fire-wide victory. `pf076` includes an unmentioned messenger as generic letter delivery, not a source claim. |
| 083–093 | 2 a.m. alarm, moonlit **boat** with wife, Woolwich security, return via watched Deptford lighters, intact house/office and burned church entry all track L66070–66093. The prompts do not show goods unloaded on September 5. |
| 094–102 | Barking tower view, hot coals, Moorefields displaced people, buckled glass and night watch follow the diary. |
| 103–111 | Separate morning fire, damaged waterfront, **later** unloading at Deptford and visual inspection are distinct. Blank diary pages do not fabricate legible writing; `pf111`'s empty pit illustrates the viewer's hypothetical closing question, not a claim that Pepys recovered the cheese. |

**Source/visual verdict: PASS.** No line or still prompt introduces a material contradiction with the pinned diary or the dated sequence. The minor staging and wording compressions identified above do not change the reported facts. This is approval of the preproduction script and prompts on these hashes, not evidence that generated images, speech, or final video have been reviewed.
