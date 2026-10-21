# Curio S40 R4a independent focused still-prompt audit

2026-10-20. **Disposition: PASS for the five revised still prompts on the exact R4a JSON hash below.** This is a focused visual/source recheck of prompt text; the prior R4 blind narrative seal and 83/83 spoken-claim source audit remain bound to the unchanged script and claims. No media was generated or reviewed, and no production gate was approved here.

## Inputs and scope

| File | Verified SHA-256 |
| --- | --- |
| `docs/videos/curio-s40/video.json` | `f4386a4f14882c5e169f7dabd14023c33beff770d3ac15fc46202246db4afec3` |
| `docs/videos/curio-s40/script.md` | `b255fb2ae6cefbed88b9913e1be046f5ffc0fd35cf1b94d06347460f96f7e7b3` |
| `docs/videos/curio-s40/claims.md` | `ee568874c7b4198186e70eec5683a17a55f969cf657002b01360b8b5c258499c` |
| R4 committed `video.json` (`HEAD`) | `6550826de8efd242c65af210ec6b6687f1da329ffe9e28684714394a0baaf6d2` |
| Local pinned Plutarch `674.txt` | `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1` |

I parsed the working JSON and `git show HEAD:docs/videos/curio-s40/video.json`, then recursively compared typed values. There are exactly **five changed leaves**, `/scenes/18/data/prompt`, `/scenes/30/data/prompt`, `/scenes/31/data/prompt`, `/scenes/32/data/prompt`, and `/scenes/54/data/prompt`, corresponding to `cl019`, `cl031`, `cl032`, `cl033`, and `cl055`. No fields, array lengths, or values elsewhere differ. The other **78/83** still prompts and all scene narration/metadata are unchanged. The baseline hash matches the R4 independent source/visual report.

## Changed-prompt findings

| ID | R4a prompt and primary-source check | Verdict |
| --- | --- | --- |
| `cl019` | A Roman freedman watches beside a guarded stone tomb doorway. Plutarch, *Antony*, pinned `674.txt` L61456–61476 keeps the capture in the monument and says Octavian sent his freedman Epaphroditus to treat her gently while preventing death. The tomb and watch align with the narration; the prior palace location is gone. | **PASS** |
| `cl031` | A young Roman companion discreetly listens to the queen, who is outside the frame. L61582–61585 describes Cornelius Dolabella as a young man among Octavian's companions and says he acted as she had requested. The pillar and visible listening pose are illustrative staging of that request; no document or specific invented message content appears. | **PASS** |
| `cl032` | The companion discreetly speaks through the guarded tomb doorway. L61582–61587 says Dolabella privately sent her word of the planned move. Oral delivery and the exact doorway are illustrative choices: the source does **not** establish whether he spoke in person or used an intermediary. The prompt makes no letter or courier prop a plot fact, and does not add message content. | **PASS**, with this staging limit recorded |
| `cl033` | The queen listens to private news inside the guarded tomb, with empty hands. L61584–61587 supports the private warning about Syria and removal of her and the children within three days; L61620–61622 later places her in the monument. The prompt no longer turns the three-day deadline into three objects or puts a note in her hands. | **PASS** |
| `cl055` | A historian compares scrolls beside an unsealed wicker basket opened to figs under leaves. L61614–61619 explicitly says the carrier moved leaves to reveal figs for the guard's inspection, then was allowed to carry the basket inside. The historian is a symbolic later comparison matching the narration's question, and the prompt does not depict a proven death mechanism. The contradictory seal is gone. | **PASS** |

The five prompts contain no modern prop or costume cue, no certain snake bite or poisoning, and no remaining palace cue in the Plutarch sequence. The still text uses one principal visual action or subject in each frame. The `cl032` contact method is not documented; its direct speech is permissible illustration of “sent her word privately,” rather than independently verified detail, and should not be treated as evidence of a witnessed meeting.

## Machine check and boundary

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s40 --json` exited 0: **0 errors, 0 warnings**, 84 spoken lines, 8 chapters, estimated 9.2578 minutes. This audit reviewed five amended text prompts against the pinned Plutarch translation and surrounding narration. It does not reperform the R4 13-question blind review or 83-claim audit, and does not assess rendered images, actual TTS timing, or paid-media readiness.
