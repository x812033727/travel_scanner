# R11 fresh blind narrative review A

Source restriction: I read only the `narration` string and 13 official narrative questions returned by the narrative CLI. I hashed `script.md` as raw bytes without reading its prose. I did not read the brief, research, claims, video, tasks, earlier reviews, or other agents' work.

- Script file SHA256: `a9fb4bcc6e271609d79e34d2f4278cdb2c797d0fc8af32b52d4f68b3b1629259`
- Narration string SHA256 (UTF-8): `9811b993b5264414fec15d02ad36101985cfc856706afd9447baba8168dc9b5c`
- Strict verdict: **11 pass, 2 fail** (`payoffs`, `no_recap`).

| Official question | Verdict | Narration evidence |
| --- | --- | --- |
| `scene_first` | Pass | An August 1835 New York newspaper reaches readers and makes a claim in the first four sentences [moon001–moon004]. |
| `no_spoiler` | Pass | The opening leaves its letter, optics, verification, and editorial response as questions [moon004–moon008]. |
| `one_line` | Pass | The same report moves from borrowed authority to mechanism, sightings, fire, reception, and source assessment [moon009, moon030, moon056, moon079, moon100, moon112, moon132]. |
| `no_toc` | Pass | Page references describe the report's sequence; no line announces the video's section plan [moon057, moon065, moon096]. |
| `chapters_link` | Pass | Each boundary continues a concrete object or question [moon008–moon009, moon031–moon032, moon055–moon056, moon078–moon079, moon099–moon100, moon111–moon112]. |
| `open_loops` | Pass | Forward hooks recur throughout, including [moon018, moon044, moon067, moon098, moon126]. |
| `payoffs` | **Fail** | The second-observation hook [moon006] receives only a claim about a selected reprint excerpt [moon118] and Jacobi's dependent quotations [moon130]. The question of *when* observations resume [moon104] gets “not this month; await the phase” [moon105–moon106], then the subject changes [moon107]. |
| `no_recap` | **Fail** | Herschel's southern-sky purpose is given twice [moon010–moon011]. The 1859 reprint is introduced [moon019] and introduced again without an explicit callback [moon112]. |
| `chapters_are_events` | Pass | All seven headings name an event or reveal; the last describes the reprint preserving differing reactions [moon112]. |
| `outro_no_next` | Pass | The ending asks for a detail to check, provides links, and invites subscription; it promises no next installment [moon999a–moon999c]. |
| `opening_hooks` | Pass | Four distinct unresolved moments follow the initial scene [moon004–moon007]. |
| `one_thread` | Pass | The newspaper's claim to astronomical evidence stays central from the opening question to the final explanation [moon008, moon132]. |
| `no_detour` | Pass | Apparent observations, the fire, and the circulation claims all feed the evidence and reception inquiry [moon074, moon089, moon103, moon123–moon125]. |

## Actual answers to the opening hooks

- **Where is the assistant's letter?** [moon004] returns explicitly [moon022]; the account identifies Grant's letter as an unverified role and route in the report [moon023]. This is a payoff.
- **How is the light problem solved?** [moon005] returns as the falling-light problem [moon034]. The report proposes artificial illumination [moon035]; the narration states that illuminating a projected image cannot restore lunar detail [moon041]. This is a payoff.
- **Can the newspaper supply a second observation?** [moon006] returns only with the narrower finding that the selected reprint excerpt supplies none [moon118] and later Jacobi quotations do not add an original page [moon129–moon130]. The broad opening question remains incompletely answered.
- **Did other editors all believe it?** [moon007] is answered by selected praise, disbelief, and satire [moon112–moon122], with a clear warning that this is not a complete census [moon114]. This is a payoff.

## Actual answers at chapter boundaries

- The question of how a story looks like astronomy [moon008] leads to the borrowed real name [moon009].
- The heavy telescope tube [moon031] leads to the alleged lens and darkroom design [moon032].
- The first projected image [moon055] is answered with rocks, valleys, and crystals [moon056].
- The cliff shapes [moon078] become winged creatures [moon079] and then humanlike figures [moon082].
- The observatory smoke [moon099] becomes the mirror's concentrated-sunlight fire [moon100–moon103].
- The editors' response question [moon111] leads to the reprint's mixed selected reactions [moon112–moon115].

Other local questions generally resolve promptly. The remaining notable gap is the explicit request for *when* new lunar observations will resume [moon104], since a delay and lunar-phase condition [moon105–moon106] do not supply a resumed observation or date.
