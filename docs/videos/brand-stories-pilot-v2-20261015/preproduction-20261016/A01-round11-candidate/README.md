# A01 round 11 offline image-prompt candidate — HOLD / UNREVIEWED

This sibling of [`A01-round10-candidate`](../A01-round10-candidate/README.md) addresses the four voice/image prompt failures in the independent round 10 editorial review. It also separates the visual jobs of `turn-15` → `now-01` → `now-02b`. A separate [independent prompt-text review](../A01-round11-independent-review/README.md) found the six new prompts aligned with their narration; **actual images, story review and media production remain HOLD**. It is not a host import, a new story review receipt, a picture approval, or permission to generate media. The round 9 narrative panel remains FAIL (`chapters_link`, `payoffs`, `one_thread`), and the round 10 independent editorial verdict remains HOLD. Round 11 has not had a real image test.

| File | Purpose |
| --- | --- |
| `candidate/chapters/*.json` | All six complete chapters, derived byte for byte from round 10 except the six `data.prompt` fields below. |
| [`exact-delta.json`](exact-delta.json) | Full before/after prompt strings and bound chapter hashes. |
| [`manifest.json`](manifest.json) | Base and candidate SHA-256s, review boundary and changed-shot review invalidation. |
| [`verify.mjs`](verify.mjs) | Read-only exact-delta, compose, lint and timeline check using the repository renderer. |
| [`validation.json`](validation.json) | Mechanical output only; no narrative, image or media judgement. |

## Six prompt changes

| Scene | Image now needs to show | Reason |
| --- | --- | --- |
| `origin-01` | An anonymous mother pulling the completed two-wheel case by its extended wooden handle at the doorway. | Narration `zc7k` says the mother sets off pulling the case; the old image showed a son about to carry it. |
| `idea-01` | One anonymous store buyer pushing the caster-wheel sample back, with a clear refusal expression. | The buyer rejects the sample in `j9sw`/`ugak`; the old salesman gesture reversed who refused whom. |
| `idea-05` | A curious, undecided man in the same kind of wood-paneled executive office, taking the sample strap before a trial. | The question in `s7me` must not reveal another rejection before `idea-06` shows the trial. |
| `turn-15` | One upright two-wheel case, with the unwheeled base corners visible. | The question in `arxr`/`4e5m` concerns whether four wheels can fit under an upright case; the old flat four-wheel case and line of upright cases competed for attention. |
| `now-01` | A neutral demonstration of an upright four-wheel case pushed **straight forward**. | The 1997 `7asx` line says Samsonite **presented** a push/pull upright case; the old retail-shop prompt implied unverified 1997 store sales. |
| `now-02b` | A separate upright case with swivel casters turning and the demonstrator moving it **sideways**. | The 2000 `5tik` line introduces multidirectional wheels. This must read differently from 1997 forward pushing; `now-03` then shows the use in an airport. |

The actions above are anonymous illustrative views, not reconstructions of a recorded buyer gesture, executive trial frame, named inventor, or exact 1997 launch image. The `look` still supplies the cute illustration style; no brand logo, text, supposed historic photo, or generated asset is included here.

## Review boundary

Only `origin-01`, `idea-01`, `idea-05`, `turn-15`, `now-01`, and `now-02b` prompt bytes changed. All 92 narrated line IDs and texts, claim rows, source/fact indexes, loops, camera values, existing verdicts and historical chapter reports are retained from round 10 as **history**. The six changed shots' prior visual review state is invalid for round 11; no shot approval or image receipt is carried forward. The round 10 text/claim candidate itself remains unreviewed for formal worker adoption, and its old `PLAN` notes cannot be read as a fresh round 11 result.

Before any paid image or audio work: resolve the narrative and script-review gates on the actual candidate, then check a source-bound continuous visual pilot and actual TTS duration. The independent review covers prompt words only; it does not inspect generated pixels. The unchanged round 10 mechanical estimate was about 520.33 seconds, below the 9–11 minute target; this prompt-only edit cannot lengthen the narration. No media, host action, commit, push or upload is part of this package.
