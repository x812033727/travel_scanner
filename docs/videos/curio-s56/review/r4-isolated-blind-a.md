# S56 R4 isolated blind narrative review A

2026-10-20 UTC. I read repository instructions and the official storytelling-panel workflow, checked the five R4 author hashes, then reviewed only the payload printed by `node tools/video/cli.mjs narrative --slug curio-s56`. I did not read research or source reviews, previous narrative reviews, or another reader's answers. I made no author-file edits.

## Frozen author files

All five SHA-256 hashes match `review/r4-author-fix.md`:

| File | SHA-256 |
| --- | --- |
| `script.md` | `b76995caa74f0a1f65b068d9e115659d7c48678600b80e9ff502e641a6505152` |
| `video.json` | `9516fc7c0d76c011d39e00be5262e6011a2b2a8597636074334c88ba901447ff` |
| `claims.md` | `1d267cb9365eab571b3b94f13de5ebc136e323bc0d80869db0abac3874ccc1d3` |
| `brief.md` | `a17b3ac122723c1229bdb1bcf1af2c546b7665407bad5677a24658ad50583dfd` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |

## Audience answers

Full line-specific evidence is in [r4-isolated-blind-a.json](r4-isolated-blind-a.json).

| # | Panel question | Answer | Key evidence |
| --- | --- | --- | --- |
| 1 | `scene_first` | Yes | Foster stands on the east bank after crossing, with the main fire across the river [s56001]–[s56004]. |
| 2 | `no_spoiler` | Yes | Opening questions [s56006]–[s56013] defer the east-bank fire, burning bridge, and refuge outcomes. |
| 3 | `one_line` | Yes | After the preview, events move from the prior night [s56014] through Sunday [s56040], Monday [s56145], and Tuesday [s56166]. |
| 4 | `no_toc` | Yes | Forward questions name events and physical threats [s56009]–[s56013]; narration does not announce a content list. |
| 5 | `chapters_link` | Yes | The river question [s56069] leads to the crossing [s56070]; the water question [s56144] leads to the destroyed waterworks [s56145]. |
| 6 | `open_loops` | Yes | Unanswered threats recur throughout, including roofs [s56051], the river [s56069], and grass [s56156]. |
| 7 | `payoffs` | Yes | The opening's rear-house and north-resident questions receive named callbacks [s56073], [s56129]. |
| 8 | `no_recap` | **No** | Foster's belief that the sturdy city district would stop the fire is stated at [s56090] and again at [s56095], without a callback. |
| 9 | `chapters_are_events` (reference) | Yes | Titles describe burning wood carried ahead, a new fire behind the river, the northern bridge burning, and rain arriving. |
| 10 | `outro_no_next` | Yes | The ending resolves the river-boundary question [s56172]–[s56176] without naming another video. |
| 11 | `opening_hooks` | Yes | The opener plants separate outcomes for rear houses [s56007], stone district [s56010], bridge [s56011], and north resident [s56012]. |
| 12 | `one_thread` | Yes | The concrete problem is whether any boundary protects the evacuees, from the river [s56003] through stone [s56090] and grass [s56156]. |
| 13 | `no_detour` | Yes | Wood streets [s56034]–[s56039] and the grassland defense [s56157]–[s56167] each test that safety problem. |

**Verdict: FAIL, 11 of 12 required questions yes.** Question 9 is reference-only and yes. The official CLI accepted the JSON and returned exit code 1 solely for `no_recap`; there were no answer-format notes. The repeated safety belief at [s56095] is the narrow repair target. Any narration change requires a new blind pass against a new hash freeze.
