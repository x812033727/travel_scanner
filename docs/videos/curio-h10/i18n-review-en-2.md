# H10 English localization: independent review, round 2

Reviewed 2026-10-16 (Asia/Taipei). The reviewer did not edit the worksheet, source script, tasks, or media.

- Worksheet: `<home>/mokaair-work/videos/curio-h10/i18n/en.todo.json`, SHA-256 `961D57948BACBBD22866C5C5BB3538492E4BC6B2E0E97F876DFA665690C0B26D`.
- Approved Chinese source: `docs/videos/curio-h10/video.json`, SHA-256 `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`.
- The three required fixes are defined in [round 1](i18n-review-en-1.md), which links the relevant Parks Canada and Waterloo primary records.

**Verdict: PASS for English translation quality on these exact hashes.** All three prior HOLDs are fixed, and the complete worksheet remains aligned with the approved Chinese source. This is a translation review; it does not itself merge the locale, synthesize a dub, approve audio, or send a language package to the site.

| Field | Recheck |
| --- | --- |
| `h66c7cde` | `a wood-like object` is singular, preserving the Chinese report and the single object in the [Parks Canada discovery record](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror). The name remains before the sighting, matching the two source cue pieces. English length is 88/94 characters. |
| `hdd8be47` | `An Arctic Research Foundation ship went into Terror Bay` credits the vessel without asserting that the foundation led the wider search. The September 3 discovery stays distinct from Parks Canada's later confirmation. English length is 96/102 characters. |
| `title` | `Franklin Expedition: How Were the Ships and Some Sailors Identified?` limits the people claim to some sailors, not the full 129-person expedition. It is 68/100 characters and has no invented channel translation. |

## Full-sheet recheck

- `parts` is `metadata,captions`. All 82 line IDs, scene IDs, and Traditional Chinese `source` strings match `video.json` in order. Every English line is nonempty, has `max_chars`, and is within its own hard dub limit.
- All 20 declared multi-cue boundaries refer to an existing line and concatenate to that line's Chinese source. The two revised lines retain the source's subject and clause order; no new cue inversion was found in the unchanged lines.
- All seven chapter scene IDs and Chinese source strings match `video.json`; their English text is nonempty and at most 30 characters. The title, description, tags, and three thumbnail source fields match their current Chinese fields. Tags remain below 500 characters; the thumbnail keeps its line break and `**` emphasis.
- The unchanged lines retain the departure 134 / continuing 129 distinction, the 1847 and 1848 note entries, an April 26 **plan**, separate 2014/2016 ship discoveries and identification, Fitzjames in 2024, and four further sailors / six total in May 2026. No additional English fact, glossary, or meaning issue arose in this directed recheck.

Remaining fixes: **meaning 0, facts 0, glossary 0, cue order 0, hard budget 0, metadata 0, thumbnail 0**. Rendered captions and the actual English dub still require their own production checks.
