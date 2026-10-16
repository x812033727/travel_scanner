# H10 English localization: independent review, round 1

Reviewed 2026-10-16 (Asia/Taipei). The reviewer did not edit the English worksheet, Chinese script, task files, or media.

- Worksheet: `C:\Users\x8120\mokaair-work\videos\curio-h10\i18n\en.todo.json`, SHA-256 `88661979F89CD3727A5B90FEDDCEBFDC982BE09F920F849AB99614FD3E8F7B9C`.
- Current approved Chinese source: `docs/videos/curio-h10/video.json`, SHA-256 `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`.
- Read `claims.md` and `research.md`, then checked the current [Parks Canada Inuit account](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit), [Parks Canada Terror discovery record](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror), and [Waterloo's May 2026 identification report](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition). The latter supports four new identifications and six in total; the translation keeps those numbers.

**Verdict: HOLD for three narrow English edits.** Two lines add a count or leadership implication absent from the Chinese and primary records; the title may imply that the whole crew has been identified. Keep the Chinese source, approved audio, and all other English lines as they are. Recompute the worksheet hash and recheck these fields before merging, dubbing, or language submission.

| ID / field | Kind and problem | Current English | Suggested minimum change |
| --- | --- | --- | --- |
| `h66c7cde` | Fact/meaning: `objects` makes the wood-like sighting plural. The Chinese says an `物件`, and Parks Canada records one large piece of wood. Preserve the name in the first cue, the report in the second, and the 94-character dub limit. | `His name was Sammy Kogvik. He said wood-like objects jutted from the ice in Terror Bay.` | `His name was Sammy Kogvik. He said a wood-like object jutted from the ice in Terror Bay.` (88 characters) |
| `hdd8be47` | Fact/meaning: `led this search` asserts command of the search. The Chinese says the Arctic Research Foundation went out this time; Parks Canada says its ship joined the search and its crew found the wreck, while Parks Canada led the wider shipwreck search. | `The Arctic Research Foundation led this search. On September 3, it found another wreck in the bay.` | `An Arctic Research Foundation ship went into Terror Bay. On September 3, it found another wreck.` (96 characters; below this line's 102-character limit) |
| `title` | Metadata: collective `the ships and crew` can read as identification of the entire 129-person crew. The video explains the two ships and six identified sailors, with most people's final journeys unresolved. | `Franklin Expedition: How Were Its Ships and Crew Identified?` | `Franklin Expedition: How Were the Ships and Some Sailors Identified?` (68 characters) |

## Checks that passed

- All 82 line IDs, scene IDs, and Chinese source strings match the approved `video.json` in order. All 82 English lines are nonempty and within their individual `max_chars`; the proposed line replacements also fit. All 20 declared multi-cue boundaries join back to their exact Chinese source and the translated ideas retain the cue sequence.
- Seven chapter IDs and source strings, title and description source, tags, and all three thumbnail source fields match the current Chinese source. Seven chapter names are at most 30 characters, title 60 characters, tags below 500, and no invented English channel name appears in the title or tags. The thumbnail keeps its `\n` break and `**` emphasis.
- The 134 at departure / 129 continuing, 1847/1848 note, April 25 plan for April 26, 2014 *Erebus* discovery, 2016 *Terror* discovery and separate confirmation, 2024 Fitzjames identification, and May 2026 four additional / six total remain distinct. No other number, name, or conditional meaning drift found.
- Forty English entries are longer than the approximate 80-character reading target, but all are within measured dub limits; twenty have multiple Chinese cue pieces. The other twenty need a rendered-caption reading pass after merge, rather than a speculative shortening of approved meaning. No additional line is held solely on approximate length.

Fix counts: **facts/meaning 2, metadata 1; glossary 0, cue order 0, hard budget 0, thumbnail 0**.
