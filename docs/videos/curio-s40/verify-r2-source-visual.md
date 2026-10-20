# S40 R2 independent source and still-prompt audit

2026-10-20. This is a post-seal audit. The blind narrative assessment was written first at `/tmp/curio_s40_r2_fresh_blind_seal.md` (SHA-256 `71f683ea5cacbd7cb02add1da3cbc3e404740e5cf9aa53872506a3f7a5f1c9dd`). I then opened `research.md`, `claims.md`, `video.json`, the applicable skills, and **freshly downloaded all three pinned full texts**. No episode files or paid media were changed or made.

## Reproducible input and lint record

| Input | SHA-256 / result |
|---|---|
| `docs/videos/curio-s40/script.md` | `c6f90cb2b04e80fe71e5b3b0ca15dd1f5e148559a013a908c34fdc608c6df35b` |
| `docs/videos/curio-s40/claims.md` | `2bd8be9e3f2b1b40fdeafbac3c920feb6295117ffbbb272d0201de3bd7eb8c14` |
| `docs/videos/curio-s40/research.md` | `8a3afa5d6e7d0c150cf643322c0cf58f1a7993fd81ca738d0a4113f52dcef3c8` |
| `docs/videos/curio-s40/video.json` | `d0b200ac4027daa5c578595d40a79b3c6cf9f0af36feb47db13bd7dfeba7433f` |
| P: pinned GITenberg Plutarch `674.txt`, commit `6aea7c6d83ee3596f9106d2d832d705aa4ed4620` | `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1` |
| S: pinned GITenberg Suetonius `6400.txt`, commit `bb5afc956095e248b2287cce2a4d3ebe394e5d31` | `082eee2d55230c1f75f9476dae537fc37851487bc1cce5dfaef1ef2a67558b15` |
| D: pinned GITenberg Dio `10162.txt`, commit `06d7e6a6f7fd5f45fbaacc3ade5397085290113b` | `b0ce5d998a6eb78162fc6658b24b9efd0fd0aa23ce6a9bbe9fd10b584fdf4e83` |
| Official `node tools/video/cli.mjs narrative --slug curio-s40 --json` stdout | `5252bd3e2e686b6436169fdf4c785efb05de1de572da573c37476f59553a741b`; embedded narrative `a3ab462ea1b9417c`, speech `1970f8c9b85f175f` |
| `node tools/video/cli.mjs lint --slug curio-s40` | **Exit 0, 0 errors, 0 warnings**; estimated 9.3 min, 86 lines, 1962 spoken units; first chapter 00:00, last 08:21 |

Fresh-source local copies are `/tmp/curio_s40_plutarch_674.txt`, `/tmp/curio_s40_suetonius_6400.txt`, and `/tmp/curio_s40_dio_10162.txt`. The source references below are **full-text line numbers** in those exact bytes, rather than modern page/section guesses. The texts are later English translations of ancient accounts, not witnesses or original-language editions. `P`, `S`, `D` denote these three full texts. P's `Caesar`, S's `he`, and D's `Caesar`/`Octavius` here mean Octavian.

The mechanical cross-check found **86 JSON scenes, 85 still `shot` prompts, 85 historical `claims.md` rows, and one unsourced outro cl086**. All 85 claim IDs exist exactly once, match the corresponding JSON spoken text byte-for-byte, and all 85 shots have a prompt. This does not substitute for the source and visual decisions below.

## Decision and actionable blocks

**BLOCK for release/preproduction lock** until these are resolved. The ancient-source conclusion itself is sound: P 61638–54, D 7506–16, and S 2805–08 all stop short of proving a snake bite. The public triumph image is P's evidence of the *version's display*, not a witness to death.

1. **Unqualified Octavian motive, cl009.** P 61444–48 reports that Octavian feared losing treasure and wanted her for his triumph. The narration at script L43 states his private wants as an independent fact. Keep P as the explicit subject (for example, “普魯塔克說，屋大維想保住陵墓財寶，也想活捉女王”). The cl009 prompt additionally puts **sealed chests outside** a building where P has her still shut in the monument; D 7340–43 locates her money *inside* it. The prompt visually gives Octavian access to treasure before capture. Use a closed monument/guarded entrance without visible accessible treasure.
2. **Suspected becomes detected, cl021.** P 61538–42 says `Caesar, suspecting her purpose`; script L93 says `察覺後`. `懷疑她的企圖` preserves the source's degree of certainty. Its food-bowl still is fine.
3. **Claim citations end before the facts, cl052, cl053, cl072.** P-c is declared as P 61634–54, but permission for the joint burial is P 61655–58 and attendants' burial P 61658–59; cl052/053 claim rows cite P-c. S 2808 also supports the joint burial, but is absent from cl052's row. D-a is declared as D 7320–7503; Dio's “and so died” is D 7504, outside the cl072 claim's D-a range. Expand the P-c/D-a ranges or update the claim row source pointers, and extend the P fragment URL in `video.json` (currently ending at `#L61654`) through P 61659. The downloaded **full file** verifies the events; the block is citation traceability, not that the burial/death claim is false.
4. **Wrong location in still cl033.** The prompt says `from a palace terrace`. This is within the Plutarch sequence: P 61620–22 still calls her location `the monument` when she sends the final letter; P never moves her to a palace. Only Dio later says palace at D 7440–43, and the narration intentionally treats that as a differing account at cl067. This still prematurely merges the versions. Put her at the guarded monument with Antony's tomb distant, without a palace terrace.
5. **Different recorded gesture in still cl026.** P 61564–68 says she caught steward Seleucus **by the hair** and struck him; the still specifies gripping his **sleeve**. The narration's generic `抓住管家` is safe, but the still gives a contrary hand placement for the described encounter. Depict her raised hand and the steward without specifying a grip, or use the reported hair grip. This is a small visual correction; it does not alter the episode's evidentiary conclusion.

The cl029 “認定她終於想活／看錯了” and its reassured-face still follow P 61574–80 **as Plutarch's interpretation**. The adjacent `傳記卻說` gives some attribution. Keep that attribution close if rewriting cl009 or directing the image; neither Octavian's internal belief nor a facial expression is independently observed. Similarly cl047's “猜到” comes from P 61622–26. P 61463–76 directly supports the women and dagger sequence; P 61401–15 directly supports the wounded Antony being **carried to** the monument and then hoisted by Cleopatra **with two women**. The matching prompts focus on selected actors without asserting they acted alone.

The blind narrative gate remains **10/13 yes, 3/13 no** (`one_line`, `payoffs`, `no_recap`). See the sealed file for the exact independent judgments. In particular, the question about preserving the children's kingship at cl012 is never expressly answered, and the Dio account revisits the same transfer/letter/death sequence already narrated in Plutarch's account. Lint's zero warnings does not test those editorial points.

## Row-by-row source and still-prompt check

Each row was checked against its exact narration, `claims.md` pointer, and the still prompt with the same ID. `N PASS` means the claim is supported by the cited full text or is a plainly signposted inference/question; `N BLOCK` means the wording exceeds that evidence. `REF BLOCK` means true in the checked full text but outside the research/claim pin. `V PASS` means the prompt is a content-relevant cartoon illustration without a material contradiction; it does **not** certify a generated image, which does not yet exist here. `V BLOCK` means prompt text itself conflicts with the source. Source line spans are intentionally narrow enough to locate the fact.

| ID | Narration / claim source check | Still prompt check |
|---|---|---|
| cl001 | N PASS · P 61614–16: carrier, basket, tomb guards | V PASS · carrier/basket/sentinel/door |
| cl002 | N PASS · P 61615–17: guards see figs under leaves | V PASS · leaf lift over figs |
| cl003 | N PASS · P 61638–42: asp among figs is explicitly hearsay | V PASS · scroll/basket, no snake asserted |
| cl004 | N PASS · P 61620–28: sealed letter and rapid envoys | V PASS · sealed letter delivery |
| cl005 | N PASS · P 61627–29, 61651–54: door and later triumph image, framed as question | V PASS · statue with snake motif, teaser |
| cl006 | N PASS · P 61398–61406: wounded Antony **carried in arms** to door | V PASS · two servants carry him; no walking Antony |
| cl007 | N PASS · P 61404–14: Cleopatra **and two women** hoist him by ropes | V PASS · queen shown at rope; medium framing does not say she is alone |
| cl008 | N PASS · P 61415–32: dies beside her; author named | V PASS · grieving queen and covered figure |
| cl009 | **N BLOCK** · P 61444–48 reports motive, but line states his private aims without attribution | **V BLOCK** · accessible treasure chests outside; P/D place treasure within closed monument |
| cl010 | N PASS · P 61444–48; S 2805–07: intended living triumph captive | V PASS · empty parade platform as visualized plan |
| cl011 | N PASS · P 61444–52: Proculeius at barred tomb door | V PASS · envoy before barred door |
| cl012 | N PASS · P 61449–54: she asks kingdom for children; wording is a question | V PASS · queen talks through barred door |
| cl013 | N PASS · P 61456–60: door talks continue, window noted | V PASS · envoy looks up at window |
| cl014 | N PASS · P 61456–62: Gallus talks while Proculeius prepares ladder | V PASS · ladder/window; single envoy focus |
| cl015 | N PASS · P 61459–62: Proculeius and two men climb in | V PASS · one climbing man in frame, not stated as sole entrant |
| cl016 | N PASS · P 61463–66: Cleopatra draws dagger, question of success | V PASS · hand toward dagger |
| cl017 | N PASS · P 61465–76: dagger taken, dress checked for poison | V PASS · confiscated dagger and robe |
| cl018 | N PASS · P 61473–76: Epaphroditus told gentle but strict custody | V PASS · chamber watcher |
| cl019 | N PASS · P 61531–37: fasting plan | V PASS · untouched bowl is illustrative |
| cl020 | N PASS · P 61535–38: Plutarch explicitly cites Olympus's narrative; no claim of reading original | V PASS · biographer/scroll, source illustration |
| cl021 | **N BLOCK** · P 61538–42 says *suspecting*, not `察覺` | V PASS · queen hesitating at food bowl |
| cl022 | N PASS · P 61544–48: she rises at Octavian's visit | V PASS · queen rises before commander |
| cl023 | N PASS · P 61556–60: Antony fear defense, Octavian counters | V PASS · exchange at table |
| cl024 | N PASS · P 61559–62: entreaty *as if* seeking longer life | V PASS · guarded commander/pleading queen |
| cl025 | N PASS · P 61562–66: treasure list, steward names omissions | V PASS · steward points to blank list |
| cl026 | N PASS · P 61564–68: she seizes steward; generic narration avoids specifying grip | **V BLOCK** · sleeve grip contradicts P's hair grip |
| cl027 | N PASS · P 61568–74: she says gifts for Octavia/Livia's intercession | V PASS · small jewelry box; cartoon shorthand |
| cl028 | N PASS · P 61574–79: keeps items, promises generous treatment | V PASS · commander gestures to box |
| cl029 | N PASS · P 61574–80: Plutarch reports Octavian's belief and deception; keep author context | V PASS · reassured face represents P's account, not proof of inner thought |
| cl030 | N PASS · P 61582–87: unnamed young companion set up | V PASS · young messenger; note is illustrative, not an extant document |
| cl031 | N PASS · P 61582–87: Dolabella secretly sends requested word | V PASS · young man delivers message; note remains an illustration |
| cl032 | N PASS · P 61585–87: Syria and removal in three days | V PASS · queen with note/travel bundles; symbolic |
| cl033 | N PASS · P 61587–61609: threatened removal and burial plea warrant question | **V BLOCK** · palace terrace belongs to Dio, not P's tomb sequence |
| cl034 | N PASS · P 61587–90: asks for and gets oblations visit | V PASS · request to official |
| cl035 | N PASS · P 61589–92: carried to tomb with women | V PASS · queen and distant attendants approaching tomb |
| cl036 | N PASS · P 61592–61609: attributed lament about removal/burial | V PASS · queen at tomb wall |
| cl037 | N PASS · P 61611–12: garlands and kiss before bath | V PASS · one garland represents wreath offering |
| cl038 | N PASS · P 61611–13: bath preparation | V PASS · water basin |
| cl039 | N PASS · P 61613–14: sumptuous post-bath meal | V PASS · meal table |
| cl040 | N PASS · P 61614–15: same country carrier and basket | V PASS · carrier returns at guarded door |
| cl041 | N PASS · P 61615–17: guard stops him, leaves reveal figs | V PASS · fig inspection |
| cl042 | N PASS · P 61617–19: guards praise figs but refuse offer | V PASS · smiling guard and figs |
| cl043 | N PASS · P 61617–20: carrier admitted | V PASS · basket passed through guarded door |
| cl044 | N PASS · P 61620–22: written/sealed letter after meal | V PASS · sealing letter; blank art avoids fake readable text |
| cl045 | N PASS · P 61620–22: all but two women dismissed, doors shut | V PASS · queen and two attendants by door |
| cl046 | N PASS · P 61620–36: all three insiders dead, no surviving account of private acts | V PASS · closed empty corridor |
| cl047 | N PASS · P 61622–26: burial request, Octavian quickly guesses and acts; narrated thought is P's report | V PASS · reads sealed letter |
| cl048 | N PASS · P 61625–29: first intends to go, sends envoys; guards unaware | V PASS · messenger to door |
| cl049 | N PASS · P 61627–30: queen found dead on bed in royal ornaments | V PASS · messenger halted by draped couch |
| cl050 | N PASS · P 61630–32: Iras at feet, Charmion fixes diadem | V PASS · close crop of Charmion/diadem; Iras not contradicted |
| cl051 | N PASS · P 61632–36: Charmion replies and dies | V PASS · faltering attendant and envoy |
| cl052 | **REF BLOCK** · P 61655–58 proves joint burial, beyond pinned P-c 61654; S 2808 corroborates | V PASS · Octavian hears messenger; burial not falsely shown |
| cl053 | **REF BLOCK** · P 61658–59 proves attendant burials, beyond pinned P-c 61654 | V PASS · two draped biers |
| cl054 | N PASS · P 61627–54: envoys see aftermath; basket theory is later hearsay | V PASS · scholar compares records/basket |
| cl055 | N PASS · P 61638–42: asp among figs/leaves under `Some relate` | V PASS · writer draws snake symbol, no death enacted |
| cl056 | N PASS · P 61638–42: in this version she finds asp and holds arm out | V PASS · storyteller points to sketch; no depicted bite |
| cl057 | N PASS · P 61638–44: hearsay, guard did not report seeing asp | V PASS · scroll versus basket |
| cl058 | N PASS · P 61642–44: vessel and golden spindle variant | V PASS · vessel/spindle on desk |
| cl059 | N PASS · P 61644–45: `what really took place is known to no one` | V PASS · biographer pauses writing |
| cl060 | N PASS · P 61645–47: hollow hair bodkin poison rumor | V PASS · hairpin as source illustration |
| cl061 | N PASS · P 61645–52: physical traces question is fair inference | V PASS · courier sees covered couch, no injury invented |
| cl062 | N PASS · P 61647–49: no poison symptom and no asp inside monument | V PASS · chamber inspection, no snake asserted |
| cl063 | N PASS · P 61648–50: alleged seaward sand trail, qualified | V PASS · line drawn on paper, not a proved trail |
| cl064 | N PASS · P 61651–52: alleged two faint arm punctures | V PASS · two drawn dots, not actual corpse evidence |
| cl065 | N PASS · P 61644–54: cautious source-limited inference | V PASS · vessel/hairpin comparison |
| cl066 | N PASS · P 61644–52; D 7506–16: competing versions, asks Dio | V PASS · snake motif prompts source transition |
| cl067 | N PASS · D 7440–43, 7506–16: Dio palace transfer and unknown death method | V PASS · later historian/scrolls |
| cl068 | N PASS · D 7440–43: moved to palace with usual retinue | V PASS · palace corridor and distant attendants |
| cl069 | N PASS · D 7487–94: gifts and stated willingness to sail | V PASS · queen sorts travel ornaments |
| cl070 | N PASS · D 7495–98: Epaphroditus/officials trust her and relax watch | V PASS · relaxed palace guard |
| cl071 | N PASS · D 7499–7502: sealed burial request handed to Epaphroditus | V PASS · palace attendant receives sealed letter |
| cl072 | **REF BLOCK** · D 7503–04: royal robes and death, but D-a pin ends 7503 | V PASS · robe/scroll symbolizes Dio's account, not an observed death |
| cl073 | N PASS · D 7506–07: slight arm indentations; mechanism undecided | V PASS · historian/scroll, no invented wound image |
| cl074 | N PASS · D 7506–09: rumored asp in jar or flowers | V PASS · jar/flowers comparison |
| cl075 | N PASS · D 7509–16: blood-activated poisoned hair needle claim | V PASS · needle/scroll, no poisoning enacted |
| cl076 | N PASS · P 61645–46 vs D 7509–16: hollow vs coated needle | V PASS · two hairpins beside separate scrolls |
| cl077 | N PASS · D 7519–21: Octavian sees body, applies drugs, summons Psylli | V PASS · marks/physician bag are symbolic, no treatment efficacy claim |
| cl078 | N PASS · D 7506–21, S 2805–08: no diagnosis from rescue, asks S wording | V PASS · reader compares scrolls |
| cl079 | N PASS · S 2805–08: `supposed` asp bite; Psylli sought | V PASS · official summons healer, no visible venom extraction claim |
| cl080 | N PASS · S 2805–08; P 61651–54: living captive failed; image shown | V PASS · empty display platform, parade setup |
| cl081 | N PASS · P 61651–54: Cleopatra figure with asp in triumph | V PASS · parade figure and snake motif |
| cl082 | N PASS · P 61651–54: valid inference that snake account was publicly displayed | V PASS · close snake motif/onlookers |
| cl083 | N PASS · P 61644–54; D 7506–16; S 2805–08: icon is no bite witness | V PASS · reader/statue/scroll |
| cl084 | N PASS · same three spans: none establishes death mechanism | V PASS · three scrolls, no single selected cause |
| cl085 | N PASS · P 61614–19, 61651–54: audience prompt juxtaposes documented basket and image | V PASS · basket versus miniature statue |
| cl086 | N PASS · channel outro, no historical assertion requiring a claim row | V N/A · outro template, not one of 85 still prompts |

**Counts:** historical narration wording **83 pass / 2 block** among 85 claim rows (cl009, cl021); independent reference pointers **82 pass / 3 block** among 85 (cl052, cl053, cl072); the unsourced CTA cl086 passes as an outro. Still prompt text **82 pass / 3 block** among 85 (cl009, cl026, cl033). Counts are separate dimensions and must not be added as if independent scenes. After corrections, rerun `script` if narration changes, then `narrative` and `lint`; regenerate the blind review with a fresh reader because the current sealed judgments belong to the present hashes. Generated image quality and factual content remain untested because no image generation was authorized or run in this audit.
