# Curio S40 R4 fresh source and still-prompt audit

**Disposition: BLOCKERS in still prompts only** (`cl019`, `cl031–cl033`, `cl055`). The 83 narration/claim/source rows pass the pinned English-source check. No episode file was edited or media generated.

## Chain of custody and counts

- Blind narrative seal: `/tmp/curio_s40_r4_fresh_blind_seal.md`; 13 official questions answered Yes with line-ID evidence before opening research or metadata. `narrative --slug curio-s40 --json` exited 0, so there was no tool-process refusal to confuse with an editorial verdict.
- `script.md` SHA-256: `b255fb2ae6cefbed88b9913e1be046f5ffc0fd35cf1b94d06347460f96f7e7b3`.
- `video.json` SHA-256: `6550826de8efd242c65af210ec6b6687f1da329ffe9e28684714394a0baaf6d2`.
- Pinned full-text hashes match `research.md`: Plutarch `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`; Suetonius `082eee2d55230c1f75f9476dae537fc37851487bc1cce5dfaef1ef2a67558b15`; Dio `b0ce5d998a6eb78162fc6658b24b9efd0fd0aa23ce6a9bbe9fd10b584fdf4e83`.
- Exactly 83 numbered narration rows `cl001–cl083` align verbatim across script, claims, and scene lines; `cl084` is the separate outro. Exactly 83 `still` prompts, one per `cl001–cl083`. No missing/duplicate IDs or mismatched text.
- Lint: `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s40` exited 0, **0 errors / 0 warnings**, estimated 9.3 minutes.

## Narration, source, and claim check: PASS, 83/83

| IDs checked | Pinned primary-source passage and finding |
| --- | --- |
| `cl001–cl005` | Plutarch `L61614–61628` gives the fig inspection, sealed letter, messengers, and door; `L61638–61654` marks the hidden asp as a report and the triumph asp figure as a later display. Opening withholds the result. |
| `cl006–cl019` | Plutarch `L61398–61430` gives Antony's transport, rope hoist, and death; `L61432–61476` gives Proculeius, the tomb door/window/ladder, dagger, and Epaphroditus's keep-alive orders. Suetonius `L2805–2807` independently states the hoped-for live triumph. |
| `cl020–cl030` | Plutarch `L61526–61580` gives Olympus's written account, fasting, threat involving the children, Octavian's visit, list, Seleucus, permitted gifts, promised treatment, and the biographer's deceived-Octavian judgment. The script treats that judgment as the biographer's. |
| `cl031–cl044` | Plutarch `L61582–61619` gives Dolabella's private word, Syria/three-day departure, Antony's tomb visit, bath, meal, and the inspected fig basket. It does not say Dolabella used a written note. |
| `cl045–cl055` | Plutarch `L61620–61636` gives the sealed letter, dismissed attendants, discovery, Iras and Charmion; `L61655–61659` gives Octavian's burial order. |
| `cl056–cl066` | Plutarch `L61638–61654` explicitly alternates asp in figs, asp in vessel with golden spindle, and poison in hollow hair bodkin; says no one knows what happened; qualifies the sand trail and two faint arm punctures as reports. Script does not promote either to a proven method. |
| `cl067–cl077` | Dio `L7440–7443` moves Cleopatra to the palace, `L7491–7498` gives gifts/ship/coaxed guards, `L7506–7521` says method unknown and gives shallow marks, jar/flowers asp, poisoned hair needle, scratch, and rescue attempt. Suetonius `L2805–2808` uses “supposed” of the asp and mentions the Psylli. |
| `cl078–cl083` | Plutarch `L61651–61654` gives a triumph figure with asp, a public representation rather than an autopsy; Suetonius `L2805–2808` says Octavian wanted her alive in the triumph. All three authors leave the precise method unconfirmed. |

**Specific citation-range repairs confirmed:** `cl009`'s feared loss of tomb treasure and live capture are in `P-0`, especially Plutarch `L61445–61448` (the army's approach is `L61328–61331`). `cl029`'s permitted gifts and promise are in `P-a`, `L61574–61578`; `cl030`'s belief and the biographer's contrary conclusion are in `P-a`, `L61575–61580`. The ranges in `research.md` include all three. The source at `L61452–61454` says Cleopatra *asked* that the kingdom go to her children and Proculeius only told her to trust Caesar. No child-kingship promise appears in the script, claims, or prompts.

## Still prompts and period/sequence fidelity: 78 pass, 5 need correction

All 83 prompts were read against their matching narration and the pinned passages. The accepted prompts use ancient tomb/stone doorway, figs, rope, scroll, Roman official, court, and later historian imagery; `cl056–cl066` and `cl071–cl074` show alternative death methods through writers, sketches, and props, without staging a certain fatal bite or needle act. `cl069` correctly reserves the palace relocation for Dio's account. No plainly modern object or costume is specified in the accepted prompts. This judges prompt wording only, not generated frames.

| ID(s) | Prompt blocker and source conflict | Suggested repair |
| --- | --- | --- |
| `cl019` | “palace attendant standing watch outside a private royal chamber” risks moving Plutarch's captivity to a palace before the explicit Plutarch/Dio location contrast at `cl069`. Plutarch `L61473–61476` instead sends Epaphroditus, Octavian's freedman, to keep her alive after the tomb entry. | Keep this frame at/inside the guarded tomb and depict a Roman freedman or guard receiving the keep-alive order; reserve palace corridors for Dio at `cl069`. |
| `cl031–cl033` | A “sealed blank note,” Dolabella “offering a small unlettered note,” and the queen “studying a blank note” turn the private message into a physical document and frame Dolabella as a courier. Plutarch `L61582–61587` identifies him as a young man among Octavian's companions who sent word privately, without specifying writing. Three travel bundles at `cl033` also risk implying three objects rather than a three-day deadline. | Show Dolabella as Octavian's young companion discreetly relaying news or use neutral symbolic scroll imagery without a hand-delivered letter; show the three-day deadline without invented bundles. |
| `cl055` | The “sealed basket” is unsupported. Plutarch `L61614–61619` says the small basket was opened enough to show figs under leaves and then carried in. A seal would change what the guard could inspect, a central evidentiary point. | Use an unsealed wicker basket with figs/leaves beside the historian's scrolls. |

The remaining 78 prompt IDs inspected and accepted: `cl001–cl018`, `cl020–cl030`, `cl034–cl054`, `cl056–cl083`. That includes the later triumph snake image at `cl079–cl080`, treated as an image of a version and not proof of the death mechanism. `cl075`'s generic physician's bag is an optional art-direction risk because a modern doctor's bag could be generated; an ancient medical kit or no bag would be clearer, though the frame is a historian's symbolic desk rather than a sourced event.

**Sequence check:** The cold open `cl001–cl005` returns to earlier tomb events at `cl006`, advances through captivity, Dolabella, visit, basket, letter and discovery at `cl055`, and then compares ancient reports in `cl056–cl083`. The storyboard generally respects this sequence; the `cl019` palace cue is the location exception that should be removed before image generation. Research is based on pinned later English translations, not firsthand records or a Greek/Latin critical text, and the script states that limit in its conclusion.
