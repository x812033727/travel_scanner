# Independent Brazilian Portuguese caption and metadata review

Reviewer: OpenAI Codex AI review agent `/root/review_latin`; not the translator. This is an AI review, not a human or Claude review.

Reviewed all 101 lines, 8 chapters, title, description, 6 tags and all 3 thumbnail fields against video.json, claims.md, lexicon.json, worksheet boundaries and all 107 zh-TW SRT cues. Brazilian você register is consistent. All current lines pass strict budgets; title is 77/90 characters.

| id | problem | current | suggested |
| --- | --- | --- | --- |
| b13c3e | “Código não traduz” makes a general claim about code; the source specifically says changing the sample language code does not translate the contents. Keep the current-only support condition and the code-changing limitation explicit. Suggested text: 65/67 characters. | Campo idioma: só chinês tradicional por ora; código não traduz. | Idioma: só chinês tradicional por ora; mudar o código não traduz. |
| f6f6be | The source identifies the highlighted cells as changing. “As células mudaram” drops that distinction and can suggest that the grid cells themselves changed. State that the highlighting changed; retain the five valid outcomes. Suggested text: 66/72 characters. | Lembra da pergunta inicial? As células mudaram: cinco cumprem o alvo. | Lembra da pergunta inicial? O realce mudou: cinco células válidas. |
| 8f5f2e | “Dois dados têm ordem” is unnatural and unclear. The mathematical distinction is that order matters when counting the outcomes; keep both ordered sums in the same order. Suggested text: 59/64 characters. | Conte um mais seis e seis mais um à parte: dois dados têm ordem. | Conte um mais seis e seis mais um à parte: a ordem importa. |
| thumbnail:tag | Restore the educational meaning of AI 教學動畫. The current tag only says animation with AI; adding didática remains short (20 characters). Suggested text: 20 characters. | Animação com AI | Animação didática AI |

Upstream fact warning, separate from these translation fixes: video.json/SRT line `005752` asserts an existing frames-only option, but claims.md c10 says evidence was not found and requests revised narration asking AI to add one. The Portuguese translation follows video.json; resolve the upstream conflict before release.

Verdict: ready after the fixes — meaning 2, facts 0, glossary 0, cue order 0, readability 1, budget 0, metadata 0, thumbnail 1. All 3 line suggestions pass their strict budgets; the tag suggestion is 20 characters and does not alter the emphasized headline.
