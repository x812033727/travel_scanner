# H12 independent fact receipt — current narration

- Checked: 2026-10-16 (Asia/Taipei).
- Scope: the current `video.json` and `script.md` narration. I read no earlier narrative answers or review files before answering all 13 questions.
- Source binding: `video.json` SHA-256 `9C13AF1222552BCABCFBA4B0BE2D5BC8C3EA912F0A8CB2C93104DD8AC7B39E50`; `script.md` SHA-256 `8E7AF54E37406E9C16705CA074BA5628B8EC5B749ED8B98114AD178B2A5FEADF`.
- Answer file: `<saved-session>/videos/curio-h12/review/narrative-after-deletion-independent.json`; SHA-256 `FB4952538892824AE2C1FFA2765E8D29D90A9FA6BB494F54602841D897CDD92F`.
- Narrative gate: 13 yes, 0 no (all 13 questions, including the reference-only chapter-title question). These are story-structure answers, not a claim that every historical ambiguity is resolved.

## Primary sources inspected

1. [Northern Lighthouse Board, Flannan Isles history](https://www.nlb.org.uk/history/flannan-isles/) reproduces Captain Harvie's 26 December telegram, Joseph Moore's 28 December 1900 letter, and Robert Muirhead's 8 January 1901 report. The observations and accident scenario below are checked against those texts, especially the Moore letter and Muirhead report.
2. [Gibson, *Fires*, Book I (1912), original scan](https://upload.wikimedia.org/wikipedia/commons/a/ab/Fires_%28IA_fires00gibs%29.pdf) shows *Flannan Isle* at printed pages 47–51. The table, untouched food and fallen chair are in the poem at printed pages 49–50. A [text transcription of the 1912 edition](https://www.gutenberg.org/cache/epub/42677/pg42677-images.html) was used to cross-check the scan.
3. [National Records of Scotland, June 2026 exhibition notice](https://www.nrscotland.gov.uk/latest-news/flannan-isles-disappearance-among-records-going-on-display/) and [August 2026 opening notice](https://www.nrscotland.gov.uk/latest-news/scotland-s-lighthouse-history-in-exhibition/) say Moore's letter is on display for the first time.
4. [NRS archival guide](https://nrscotland.gov.uk/learning-and-events/research-guides/lighthouses/?section=the-mystery-of-the-flannan-islands-lighthouse) identifies the relevant correspondence and report in NLC3/1/1, including a 28 December letter about Captain Holman's observation and his 29 December signed statement. It explicitly says NRS does not hold the lighthouse logbook.

## Claim checks

| Narration line IDs | Finding from primary material | Result |
| --- | --- | --- |
| `jjr5`–`xng2`, `xf7d`–`cyaq` | NLB's telegram, Moore letter and Muirhead report support the 26 December relief arrival, missing signal, horn/siren and rocket, Moore's first landing, closed entrance and exterior doors, open kitchen door, cold fire, empty beds, return to boat and cleaned lamp with full oil fountain. The script does not claim the doors were locked. | Supported |
| `anms`–`3w38` | NLB identifies Ducat, Marshall and McArthur; McArthur substituted for Ross on sick leave. Moore reports McArthur's wearing coat left behind and the other two men's sea boots and waterproof clothing in use. Muirhead attributes landing-place inference to Moore; neither document establishes the order in which the men left. | Supported, with inference labelled |
| `cuxc`–`7zvf` | NLB says the written log ended on 13 December; measurements and the light-extinguishing time for the 15th remained on the slate. Muirhead records cleaned cooking equipment and a tidy kitchen and infers an afternoon disappearance. The script correctly presents that timing as reconstruction, not witnessed fact. | Supported, with inference labelled |
| `x5ik`–`ufsf` | Muirhead separates Captain Holman's report of no light near midnight on the 15th from shore observations. He interviewed the two sons who actually watched, examined the Return Book, and observed that poor visibility could hide the light for four or five consecutive nights. The *ship's observation date* and the *date its report reached NLB* are distinct; see the discrepancy below. | Supported except notification-date conflict below |
| `s7g4`–`i3cg` | Muirhead landed on the 29th. His report describes an intact eastern landing, inaccessible western landing, a crane platform 70 ft above sea level, a rope box about 110 ft above sea level, still-coiled ropes, secured crane, displaced railings, stone over 20 cwt (approximately one metric tonne), and lifebuoy attachment still tied with canvas remnants. The script properly avoids turning equipment elevation into a measured wave height or present-day rope condition into a full account of 15 December. | Supported |
| `ecsy`–`hpye` | Muirhead's 8 January report calls the large roller and returning water the *most likely explanation*; it also compares the west wind with the wave scenario. The narration repeatedly marks his scenario as opinion and says the exact moment is unverified. | Supported, with hypothesis labelled |
| `i9ud`–`3ncp` | The 1912 *Fires* scan contains Gibson's untouched dinner and fallen chair. Moore's contemporaneous letter does not record either detail; Muirhead reports a tidy kitchen without establishing the final meal. NRS confirms Moore's letter was first displayed in 2026. The script confines the unresolved status to the men's final fate while allowing the later literary details to be checked. | Supported |

## Source conflict requiring editorial attention

- **Affected narration:** `ds8v`, “可是這個消息，在失蹤被發現之後才傳到燈塔局。” The associated claims row is `H12-C14` in `claims.md` (row 20; scene mapping at row 64). That row correctly separates Captain Holman's passing-ship observation from shore lookout records, but does not itself resolve the notification date.
- **Primary/official evidence for the scripted sequence:** the [NLB history page](https://www.nlb.org.uk/history/flannan-isles/) states that the passing ship's report was not communicated to the Board until after HESPERUS discovered the loss; Muirhead's reproduced report describes the message as received after news of the disaster had been published. The [NRS archival guide](https://nrscotland.gov.uk/learning-and-events/research-guides/lighthouses/?section=the-mystery-of-the-flannan-islands-lighthouse) lists related correspondence dated 28 December and Holman's signed statement dated 29 December.
- **Contrary official summary:** the [NLB station-history page](https://www.nlb.org.uk/lighthouses/flannan-islands/) says the same information was relayed to NLB on 18 December. That conflicts with the NLB history page and the contemporary-record sequence. The ship saw no light on **15 December**; 18 or 28 December concerns **transmission**, not the sighting.
- **Assessment:** The script follows the reproduced contemporary account, so this is not a demonstrated factual error. Because NLB currently publishes both dates, the unqualified narration at `ds8v` carries a material source-conflict risk. If revised, attribute the delay explicitly to Muirhead's report rather than claiming all official sources agree. No script or `video.json` changes were made in this review.

## Limits

The scanned 1912 edition and NLB transcriptions were inspected online; I did not inspect the physical NRS originals or the missing lighthouse logbook. This receipt checks factual narration and the 13-question narrative structure, not visual frames, audio performance, or publication state.
