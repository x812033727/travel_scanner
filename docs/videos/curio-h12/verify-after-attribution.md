# H12 independent review after attribution change

Checked 2026-10-16 (Asia/Taipei). I read the complete current `script.md` and the 13 questions from `node tools/video/cli.mjs narrative --slug curio-h12 --json` before opening claims, earlier reviews, or historical sources. The resulting independent answers were saved first; no narrative verdict was imported or submitted. This receipt covers the current narration, not its pictures, audio, or publication.

## Exact binding and narrative result

| Artifact | SHA-256 |
| --- | --- |
| `docs/videos/curio-h12/video.json` | `D16413FCD54ED2AA5FCFD12B88054FCF8B211AA96110C1514184467615AD3BF1` |
| `docs/videos/curio-h12/script.md` | `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B` |
| `C:\Users\x8120\mokaair-work\videos\curio-h12\review\narrative-after-attribution-independent.json` | `AFCC0B1B8DB8B28BF86E8645CC70DD70364F21B63BD1C4E3F78004C8A419CEC4` |

The current panel rules hash is `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`. The answer file contains all 13 IDs in panel order, with a quoted line ID for each. Local `panelVerdict()` readback: **13 yes, 0 no, 0 advisory; passed**. This is a narrative-structure verdict. I confirmed deleted line `d4uq` is absent from both current script and `video.json`; `ds8v` is present with the attributed wording. The review file was not imported into `review/narrative.json`.

## Primary material checked

1. [Northern Lighthouse Board (NLB) history](https://www.nlb.org.uk/history/flannan-isles/) reproduces Captain Harvie's 26 December telegram, Joseph Moore's signed 28 December 1900 letter, and Robert Muirhead's signed 8 January 1901 report. I checked the present script against the relevant full passages, including the awkwardly transcribed sentence in Muirhead's report about Captain Holman's message.
2. The separate [NLB lighthouse station page](https://www.nlb.org.uk/lighthouses/flannan-islands/) gives a different notification date for that passing-ship report. It remains a contrary official summary.
3. The [National Records of Scotland (NRS) archival guide](https://nrscotland.gov.uk/learning-and-events/research-guides/lighthouses/?section=the-mystery-of-the-flannan-islands-lighthouse) lists the 28 December letter concerning Holman's sighting, his 29 December signed statement, and Muirhead's 8 January report in NLC3/1/1. The [NRS exhibition announcement](https://www.nrscotland.gov.uk/latest-news/scotland-s-lighthouse-history-in-exhibition/) says Moore's letter was displayed for the first time in 2026; its stated exhibition dates ended in September 2026.
4. The [1912 scanned edition of Wilfrid Wilson Gibson's *Fires*](https://upload.wikimedia.org/wikipedia/commons/a/ab/Fires_%28IA_fires00gibs%29.pdf) has its 1912 title page and lists *Flannan Isle* beginning on printed page 47. The [1912-edition text](https://www.gutenberg.org/cache/epub/42677/pg42677-images.html) reproduces the untouched dinner and overturned chair. The script identifies them as details in a poem, not observations from Moore's letter.

## Factual and inference checks

| Script lines | Source comparison | Result |
| --- | --- | --- |
| `jjr5`–`xng2`, `xf7d`–`cyaq` | The 26 December relief, absent flag and reply, horn and rocket, Moore's first solo landing, closed entrance gate and outer doors, open kitchen door, unused fire, empty beds, return to the boat, second search, and cleaned, fueled lamp appear in the NLB documents. The script avoids claiming any door was locked. | Supported |
| `anms`–`3w38` | The three names and McArthur's sick-leave substitution are in NLB. Moore records McArthur's coat left behind and the other men's sea boots/waterproofs absent. Muirhead uses Moore's clothing knowledge to infer movement toward a landing. Neither establishes departure order; the script says so. | Supported; inference bounded |
| `cuxc`–`7zvf` | NLB distinguishes the log's last written entry on 13 December from observations and the 15 December light-extinguishing time left on a slate. Muirhead records washed cookware and a tidy kitchen and infers an afternoon disappearance. The stopped clock supplies no date. The narration labels the afternoon as an investigation's inference, not an eyewitness account. | Supported; inference bounded |
| `x5ik`–`ufsf` | Muirhead separately reports Holman's passing-ship observation near midnight on 15 December and the shore lookout Return Book. He spoke with the two sons actually doing the lookout and says poor visibility sometimes hid the light for four or five nights. No sighting is equated with proof that the light was unlit. | Supported, subject to the `ds8v` conflict below |
| `s7g4`–`i3cg` | Muirhead arrived on 29 December; his western inspection records the 70 ft crane platform, the rope box about 110 ft above sea level, the earlier winter's lost crane, the current secured crane, still-coiled ropes, twisted railings, a stone over 20 cwt (about one metric tonne), and the lifebuoy's untouched ties with canvas remnants. These are equipment positions and observations, not a measured wave height or evidence that someone used the lifebuoy. | Supported; physical evidence separated from reconstruction |
| `ecsy`–`hpye` | The 8 January report explicitly presents the large roller and returning water as Muirhead's *most likely explanation* and compares the westerly wind. The narration uses “推想” and says the last instant cannot be confirmed. | Supported as attributed hypothesis |
| `i9ud`–`3ncp`, `qv4y` | Gibson's 1912 poem contains the untouched meal and fallen chair; Moore's 1900 letter records neither. The cleaned kitchen cannot establish the final meal. NRS confirms the letter's first display in 2026. The close keeps the exact fate unresolved while treating later story details as checkable. | Supported |

## The `ds8v` source conflict

Current `ds8v`: “但繆爾黑德在報告裡說，這則消息是在失蹤被發現後，才傳到燈塔局。” The [NLB full history](https://www.nlb.org.uk/history/flannan-isles/) explicitly says the passing ship's report was communicated to the Board after HESPERUS discovered the disappearance. Muirhead's reproduced report says the message was received **after news of the disaster had been published**, a still later marker. The [NRS inventory](https://nrscotland.gov.uk/learning-and-events/research-guides/lighthouses/?section=the-mystery-of-the-flannan-islands-lighthouse) lists related correspondence on 28 December and Holman's signed statement on 29 December. Thus the revised line is a defensible, source-attributed summary of this record sequence; it is not a quote of Muirhead's exact “after publication” wording.

The [NLB station page](https://www.nlb.org.uk/lighthouses/flannan-islands/) instead says the information was relayed to NLB on **18 December**, before the 26 December discovery. I cannot reconcile the two NLB pages from the publicly displayed text, and the NRS inventory does not prove that no earlier message existed. **Residual risk:** keep the verbal attribution to Muirhead and do not state the notification date as an uncontested fact. The sighting itself was on 15 December; the conflict concerns when the Board learned of it. No further script edit is required to meet that boundary.

No other current high-risk narration claim contradicted the cited primary material. I did not inspect the physical NRS originals or the missing lighthouse logbook. No paid calls, media generation, import, or publication were performed in this review.
