# H10 English localization: independent audio-flag wording review, round 3

Reviewed 2026-10-16 (Asia/Taipei) against the approved Chinese `video.json` (SHA-256 `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`) and the English worksheet at `<home>/mokaair-work/videos/curio-h10/i18n/en.todo.json` (SHA-256 `12D3DBF03A11AD6DB89D616EDFA21FF44E2D98FA74F1D7172DE3C4B3983CD3A4`). The merged `i18n/en.json` has SHA-256 `99EF6F2F11DDFC72DDD94072B82C66E86126A2EBDFCB691F1614514C901AD7E3` before this receipt is committed.

**Verdict: PASS for these three English wording changes.** All other 79 English line texts and all `source_hash` fields are unchanged. This review covers translation and source meaning only; the three English audio clips still require targeted synthesis and audio QA. The previous English dub and its eight audio flags are not approved by this receipt.

| Line | Approved Chinese meaning | Revised English | Length / maximum | Check |
| --- | --- | --- | --- | --- |
| `h5cac1f4` | The first report stops on its writing date; the later added words tell what followed. | “The report stops on that day. What happened next appears in words added later.” | 78 / 84 | Keeps the later writing on the same paper without the spoken `addition`/`edition` ambiguity. Does not claim a separate document or that the first report stayed true after May 1847. |
| `h72b4789` | Writing added the following year says the ships had been abandoned. | “Words added the following year tell a different story: both ships were abandoned.” | 81 / 85 | The 1848 entry follows the May 1847 entry; its ships were already abandoned when it was written. |
| `hb624337` | The April 25 addition records a plan to head to Back's Fish River the next day. | “The April 25 entry records a plan to head for Back's Fish River the next day.” | 77 / 81 | The next day is April 26. `records a plan` does not assert the journey occurred or attribute penmanship to both signers. |

The [Canadian Museum of History's Victory Point Note description and transcription](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) identify two messages on one sheet: May 1847, then April 1848. Its later entry records both ships deserted on April 22 and a proposed start on April 26 toward Back's Fish River. The amended English follows those dates and keeps the plan separate from a verified departure. Adjacent English lines still identify the same note and explicitly explain that “tomorrow” means April 26 and that the note records a plan.

The correction is limited to the three lines that Gemini/Jev and offline Whisper both rendered as `edition` when the English text said `addition`. New spoken-wording QA must use the revised translation hash and check the regenerated clips; old transcription flags are diagnostic evidence, not proof that the revised audio is good.
