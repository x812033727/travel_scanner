# Curio S40 R1 source and still audit

## Fixed inputs and scope

- Exact `video.json` SHA-256: `0ba27dd49a63d8f8ed2abc6638bf8f9b772ca60470c460dd87a6aef6d70d9475`.
- 85 scene narration texts match all 85 `script.md` lines exactly by ID; 84 `shot` scenes have nonempty still prompts, followed by one `outro` without a prompt.
- Downloaded the full texts at the exact commits linked in `research.md` and checked SHA-256: Plutarch `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`, Suetonius `082eee2d55230c1f75f9476dae537fc37851487bc1cce5dfaef1ef2a67558b15`, Dio `b0ce5d998a6eb78162fc6658b24b9efd0fd0aa23ce6a9bbe9fd10b584fdf4e83`.
- Evidence references below are original text line numbers: `P` = Plutarch *Antony* `674.txt`; `S` = Suetonius *Augustus* XVII `6400.txt`; `D` = Cassius Dio *Roman History* LI `10162.txt`. The sources are later narratives in English translation, not eyewitness records. `Pass` for narration means it accurately describes or appropriately qualifies what the source says; it does not establish that the ancient event occurred exactly that way. `Pass` for a prompt means it is a compatible cartoon illustration, not proof or a reconstruction of an observed scene.

## Material findings

1. **Narration source caution — [cl029](/workspace/travel_scanner/docs/videos/curio-s40/video.json:630).** P61574–61587 says Octavian thought Cleopatra wished to live and Dolabella sent word privately at her request. It never establishes Octavian's own knowledge or lack of knowledge. “他不知道有人會私下傳消息給她” and the stated causal “前提” are unqualified inference. Rephrase as the attributed private-message development if source strictness is required.
2. **Still mismatch — [cl006](/workspace/travel_scanner/docs/videos/curio-s40/video.json:260).** P61401–61406 says wounded Antony was *carried in others' arms* to the tomb. The prompt's injured commander “approaching” the doorway will plausibly depict him walking by himself, contrary to the narration “被人送到.” Show him carried or supported.
3. **Still role mismatch — [cl017](/workspace/travel_scanner/docs/videos/curio-s40/video.json:437).** P61456–61476 identifies **Proculeius, the entering envoy**, as the man who took the dagger and checked her dress. The prompt makes a “helmeted sentinel” hold the confiscated dagger. Use the Roman envoy, not a sentinel.
4. **Small source precision cautions.** [cl034](/workspace/travel_scanner/docs/videos/curio-s40/video.json:711) specifies “那兩位侍女” at the grave although P61587–61591 says only “her women” there (the two are a reasonable continuity inference from P61405–61406 and P61620–61632). [cl061](/workspace/travel_scanner/docs/videos/curio-s40/video.json:1145) says no snake was “found” inside; P61647–61649 literally says no asp was *seen* there and does not describe a search. Neither alters the main unknown-cause conclusion.

The core death conclusion **passes**. P61638–61654 introduces snake versions with “Some relate” and “Others say,” says “what really took place is known to no one,” and offers no confirmed asp or definitive marks. D7506–7516 also says nobody clearly knows, then distinguishes an asp in a jar or flowers from a poisoned hair needle. S2805–2808 says Cleopatra was *supposed* to have been bitten and Octavian summoned the Psylli. P61651–61654 reports a later triumph image with an asp. The script consistently treats these as rumor, belief, or public imagery rather than a verified bite. The 84 still prompts likewise do not stage an actual witnessed snakebite; versions appear as historians' objects or sketches, and the later serpent is explicitly a statue motif.

## Exhaustive scene audit

`N` = narration/source; `V` = still prompt. `—` means the outro has no still. Where two sources occur, the second supports a cross-author comparison or the burial fact. Notes on flagged rows appear above.

| Scene | Source loci for claim | N | V |
| --- | --- | --- | --- |
| cl001 | P61614–61619 | Pass | Pass |
| cl002 | P61614–61619 | Pass | Pass |
| cl003 | P61638–61642 | Pass | Pass |
| cl004 | P61620–61626 | Pass | Pass |
| cl005 | P61626–61629, P61651–61654 | Pass | Pass |
| cl006 | P61401–61406 | Pass | **Mismatch** |
| cl007 | P61403–61415 | Pass | Pass |
| cl008 | P61415–61432 | Pass | Pass |
| cl009 | P61444–61448; D7429–7435 | Pass | Pass |
| cl010 | P61444–61448; S2805–2808 | Pass | Pass |
| cl011 | P61444–61452 | Pass | Pass |
| cl012 | P61449–61454 | Pass | Pass |
| cl013 | P61456–61460 | Pass | Pass |
| cl014 | P61456–61462 | Pass | Pass |
| cl015 | P61459–61462 | Pass | Pass |
| cl016 | P61463–61467 | Pass | Pass |
| cl017 | P61465–61476 | Pass | **Mismatch** |
| cl018 | P61473–61476 | Pass | Pass |
| cl019 | P61531–61537 | Pass | Pass |
| cl020 | P61535–61538 | Pass | Pass |
| cl021 | P61538–61542 | Pass | Pass |
| cl022 | P61544–61556 | Pass | Pass |
| cl023 | P61555–61560 | Pass | Pass |
| cl024 | P61559–61562 | Pass | Pass |
| cl025 | P61563–61566 | Pass | Pass |
| cl026 | P61565–61573 | Pass | Pass |
| cl027 | P61568–61574 | Pass | Pass |
| cl028 | P61574–61580 | Pass | Pass |
| cl029 | P61574–61587 | **Caution** | Pass |
| cl030 | P61582–61587 | Pass | Pass |
| cl031 | P61583–61587 | Pass | Pass |
| cl032 | P61587–61609 | Pass | Pass |
| cl033 | P61587–61590 | Pass | Pass |
| cl034 | P61405–61406, P61589–61591, P61620–61632 | **Precision** | Pass |
| cl035 | P61591–61609 | Pass | Pass |
| cl036 | P61611–61613 | Pass | Pass |
| cl037 | P61611–61613 | Pass | Pass |
| cl038 | P61611–61614 | Pass | Pass |
| cl039 | P61614–61619 | Pass | Pass |
| cl040 | P61614–61619 | Pass | Pass |
| cl041 | P61616–61619 | Pass | Pass |
| cl042 | P61618–61619 | Pass | Pass |
| cl043 | P61620–61622 | Pass | Pass |
| cl044 | P61620–61622, P61630–61636 | Pass | Pass |
| cl045 | P61620–61636 | Pass | Pass |
| cl046 | P61622–61625 | Pass | Pass |
| cl047 | P61625–61629 | Pass | Pass |
| cl048 | P61627–61630 | Pass | Pass |
| cl049 | P61629–61632 | Pass | Pass |
| cl050 | P61632–61636 | Pass | Pass |
| cl051 | P61630–61636 | Pass | Pass |
| cl052 | P61625–61629, P61655–61658; S2808–2809 | Pass | Pass |
| cl053 | P61627–61654; D7506–7516; S2805–2808 | Pass | Pass |
| cl054 | P61638–61640 | Pass | Pass |
| cl055 | P61638–61642 | Pass | Pass |
| cl056 | P61638–61642 | Pass | Pass |
| cl057 | P61642–61644 | Pass | Pass |
| cl058 | P61644–61645 | Pass | Pass |
| cl059 | P61645–61647 | Pass | Pass |
| cl060 | P61644–61652 | Pass | Pass |
| cl061 | P61646–61649 | **Precision** | Pass |
| cl062 | P61648–61650 | Pass | Pass |
| cl063 | P61651–61654 | Pass | Pass |
| cl064 | P61644–61654 | Pass | Pass |
| cl065 | P61638–61647; D7506–7516 | Pass | Pass |
| cl066 | D7419–7445, D7483–7504 | Pass | Pass |
| cl067 | D7434–7445 | Pass | Pass |
| cl068 | D7483–7498 | Pass | Pass |
| cl069 | D7499–7503 | Pass | Pass |
| cl070 | D7502–7506 | Pass | Pass |
| cl071 | D7506–7507 | Pass | Pass |
| cl072 | D7506–7509 | Pass | Pass |
| cl073 | D7509–7516 | Pass | Pass |
| cl074 | D7509–7516; P61645–61647 | Pass | Pass |
| cl075 | D7506–7507 | Pass | Pass |
| cl076 | D7519–7521 | Pass | Pass |
| cl077 | S2805–2808 | Pass | Pass |
| cl078 | S2805–2808 | Pass | Pass |
| cl079 | D7519–7521 | Pass | Pass |
| cl080 | P61651–61654 | Pass | Pass |
| cl081 | P61651–61654 | Pass | Pass |
| cl082 | P61638–61654; D7506–7516; S2805–2808 | Pass | Pass |
| cl083 | P61644–61654; D7506–7516; S2805–2808 | Pass | Pass |
| cl084 | P61638–61654 | Pass | Pass |
| cl085 | Channel outro, no historical claim | Pass | — |

Narrative craft defects identified in the separate **blind seal** remain: repeated grave beat [cl036–cl037], numbered theory list [cl054, cl057], summary chapter entry [cl066], and repeated rescue / unanswered shallow-mark question [cl075–cl079]. The source audit does not turn those craft defects into new historical claims.
