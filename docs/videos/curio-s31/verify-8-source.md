# Curio S31 R5 — fresh source and visual audit

This report follows the blind narrative seal at `/tmp/curio_s31_r5_fresh_blind_seal.md`. The seal was written before reading `research.md`, `claims.md`, `video.json`, earlier reviews, or source texts. No S31 author files or media were edited by this reviewer.

## Pinned material and method

| Artifact | Verified SHA-256 |
| --- | --- |
| `docs/videos/curio-s31/script.md` | `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2` |
| `docs/videos/curio-s31/claims.md` | `83063009c6fec93840e0e6043118f7ed2df691b3e38651bc1590f12ad0ec2127` |
| `docs/videos/curio-s31/video.json` | `4a0d0bc19c5b2ebbf6982a58a6c1331b6527b6fca4d02a5230e15edeae74c754` |

I reopened the four complete digital transcriptions at the GitHub commit pinned in `research.md` (`4a6d6f2088825f132521d848c2ea86cf9c9a7620`), downloading fresh copies from `raw.githubusercontent.com` to `/tmp/curio-s31-r5-fresh-{fanchuan,newtang,oldtang,baiji}.txt`. Each fresh full-file SHA matched the research note:

| Text | Verified full-file SHA-256 | Relevant pinned lines |
| --- | --- | --- |
| Du Mu, 《樊川文集》 | `f6a2c78a1da55168b03e7556ac4a57c7c7f64c74b63ffe4af2d56558cceb42d1` | 257–263 |
| 《新唐書》 | `c9b7a46b1f4f1c3950c40a5e4b30f3ccb3bfd19acd2d638d38359d0db7f5f559` | 1015, 3533, 3562, 10103 |
| 《舊唐書》 | `ff840f4e9f94cdee86f3e6db86b99ecb923fea56046d30803d2576459400c0fd` | 14198 |
| Bai Juyi, 《白氏長慶集》 | `6074f3b5cc14e45b4c1c18edfddd7ec814709038f8351bb7cbcde17b66ddbb81` | 6047–6048 |

The source and claim boundary was checked for every `ly001`–`ly097` row. An independent structural comparison also found exactly 97 numbered script lines, 97 claim rows, 97 video scenes, 96 `visual: still` prompts, and one outro. The script, claim, and scene narration text and IDs agree exactly, in order; emotion directions agree where present. All seven video source URLs point at the same pinned commit. There were **zero ID, text, source-code, or scene coverage mismatches**.

## Source findings for all 97 claim rows

All 97 rows are supported as either a direct quotation/paraphrase, a clearly framed question, or an explicit limit on what the cited text can prove. The following contiguous coverage accounts for each row exactly once; cross-source comparisons were checked against every source code written on the corresponding claim row.

| Claim rows | Result and checked source boundary |
| --- | --- |
| `ly001`–`ly024` (24 rows) | Du Mu's three poems support Chang'an looking back, sequential palace gates, red dust, one poetic rider, the consort's smile, lychees at the last turn, the second poem's `數騎漁陽探使` and 《霓裳》, and the third poem's Lushan dance. The text does not enumerate who knew, count horses across a complete journey, or give an itinerary. `ly006` is a forward question tied to NBG; `ly007` to NBL; `ly008` to BJ; `ly009` and `ly019` explicitly compare sources. The reading of the poems as court satire is an identified interpretation of the three-poem sequence, not a courier-log claim. |
| `ly025`–`ly044` (20 rows) | NBG line 10103 directly has competing offerings and rewarded officials, then `妃嗜荔支，必欲生致之，乃置騎傳送，走數千里，味未變已至京師`. The officials are adjacent in the text, but not identified as suppliers of this lychee delivery. `騎傳` supports mounted transmission, not named relay stations or a horse count. `數千里` gives a broad distance phrase, not a route, duration, or speed. `味未變` describes taste on arrival at **the capital**; it does not document delivery to the poem's Huaqing gate or palace custody. The Du Mu/NBG comparison at `ly038`–`ly042` correctly leaves shipment identity and dates unproven. |
| `ly045`–`ly058` (14 rows) | NBL line 1015 states that on Yang Guifei's birthday, while Xuanzong was at Mount Li, a small music troupe played at Changsheng Hall; a new tune had no name, and when southern lychees arrived it was named 《荔枝香》. This is **birthday music, not a recorded banquet**, and supplies only `南方` as a direction. NGZ line 3562 lists Guangzhou tribute `荔支`; NGR line 3533 lists Rongzhou `荔枝煎`. Neither geography entry identifies the consort's particular fresh-fruit shipment. No text links the birthday music arrival to NBG's relay shipment. |
| `ly059`–`ly072` (14 rows) | BJ lines 6047–6048 describe Ba Gorge lychees, tree and fruit form, red shell and pale flesh, sweet-sour liquid, and purpose of the illustration. BJ states `若離本枝一日而色變二日而香變三日而味變四五日外色香味盡去矣`: **color first, aroma second, taste third**. The text is dated Yuanhe 15 (820), later than Yang Guifei. JTB line 14198 quotes the same decay sequence and reports Bai sending wood-lotus and lychee pictures to court friends; it is a dependent quotation, not a second independent fruit experiment. The script treats art's inability to carry scent as a question/observation, never as the source's measured result. |
| `ly073`–`ly084` (12 rows) | These rows compare BJ's after-picking fruit description with NBG's taste-at-capital result. The texts give no shared shipment marker, picking/handoff/arrival dates, or transport interval; they therefore cannot yield a courier speed. Bai's `巴峽` identifies the fruit in his own description, not the consort's orchard. The script states these limits rather than merging the two accounts. |
| `ly085`–`ly096` (12 rows) | The final map inference stays within NBG's `京師` arrival and `騎傳` wording. DM, NBL, geography, and BJ lack a common batch identifier or route-station record. The map retains one capital point and source note, with no asserted origin, relay line, speed, date, or palace receipt. |
| `ly097` (1 row) | `EDITORIAL` subscription sentence; no historical factual claim or next-episode claim. |

## Visual audit of all 96 still prompts

I read each still prompt `ly001`–`ly096` alongside its scene narration and claim row. The prompts use generic illustrated people, books, fruit, and maps; the video description expressly labels the images as AI cartoon aids rather than historical reconstructions. They do not depict a birthday banquet, named orchard, complete route, ice or other specific preservation method, a measured speed, or taste changing before color and aroma. The map ending does not draw an unsupported line.

| Still prompts | Finding |
| --- | --- |
| `ly001`–`ly020` (20) | Poem and question visuals stay illustrative. A covered basket and a possible handoff are staging devices, not evidence of container design or a documented individual courier exchange. |
| `ly021`–`ly044` (24) | Historical-account and comparison visuals avoid a drawn route and keep `京師` distinct from the poem's gate scene. **Nonblocking note:** `ly021` shows one mounted messenger although Du Mu writes `數騎` (several); showing several distant riders would track the spoken line more closely. |
| `ly045`–`ly058` (14) | Music-hall and geography visuals contain no banquet and do not label Guangzhou or Rongzhou as the consort's source. **Nonblocking note:** `ly049` shows a musician physically receiving a basket inside the hall. NBL says southern lychees arrived during the music account but gives no recipient or delivery room. A separated fruit image or news of its arrival would avoid implying that detail. |
| `ly059`–`ly072` (14) | Bai's drawing, fruit, and decay visuals track a later fruit description. The three-day line is not illustrated as a three-day courier clock; no prompt turns aroma into taste. |
| `ly073`–`ly084` (12) | Two texts, baskets, and blank maps remain unlinked. No prompt visually fixes one batch or assigns Ba Gorge as court origin. |
| `ly085`–`ly096` (12) | The tentative mark is rubbed out, then only one dot remains. No map line, station sequence, or origin is supplied. |

The two prompt notes are staging precision issues, not contradictions in the 97 spoken claims or source mappings. All checks refer to the pinned hashes above; a later prompt edit creates a new video hash requiring a focused recheck of the changed prompts.
