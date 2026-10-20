# S19〈艾菲爾鐵塔〉 R6 independent source and visual audit

Date: 2026-10-20 UTC. This audit was started **after** sealing an independent read of only the expected-hash script and the official 13 narrative questions at `/tmp/curio_s19_r6_fresh_blind_seal.md` (SHA-256 `626550377bfb0e2166c5afe930e04ad8c74a2d6f183d1d5915b497fefba2b5da`). The blind reading answered **13 Yes / 0 No** and supplied 13 separate comprehension answers with script line evidence. This audit did not edit episode files or generate paid media.

## Frozen inputs and checks

| Input | SHA-256 |
| --- | --- |
| `docs/videos/curio-s19/script.md` | `0ba634669a95b549f32e2d3fbc9250a68454ed69099e6940c1e819269836ea75` |
| `docs/videos/curio-s19/video.json` | `b64c32f3d53964061348908a90424eaae7e44161979be46c77e3c6c3f2ee37d3` |
| `docs/videos/curio-s19/claims.md` | `0a0c1368fff47871048fc19edeac8735fd0c5445b31d69eadcfea4b9f4004bfd` |

`node tools/video/cli.mjs lint --slug curio-s19 --json`: **0 errors, 0 warnings**; 110 narration lines, estimated 9.3228 minutes, seven chapters. `video.json` has 101 scenes: 100 still-image prompts and one outro. Programmatic comparison found 110 unique video narration IDs, 110 unique claims rows, and 110 script spoken lines, all in exact text agreement; no missing, orphan, duplicate, or divergent line. There are 130 markdown source links over 109 source-bound rows; the only uncited row is subscription CTA `et103`. Every link points to the correct pinned revision and an existing original-text line; no wrong revision, malformed line anchor, or out-of-range span was found. `video.json`'s two source URLs also use the same pinned revisions.

I independently fetched both pinned files from the fixed Git revisions and compared their full SHA-256 values to `research.md` and the existing local copies:

| Source | Revision / source lines | SHA-256 | Result |
| --- | --- | --- | --- |
| 1887-02-15 *Le Rappel* no. 6185, Project Gutenberg 77985 | `a10e54e67c3f6945d1f0123d76732950889d1447`, 268 lines | `91d3e9397aca543f900c9babd37fd2489097677a3eb378f5944e5af7af14f9ec` | Match |
| 1913-05-31 *L’Illustration* no. 3666, Project Gutenberg 38842 | `35610f7d0cc21e2c5877c58628edb25c796f3bd1`, 2228 lines | `db280680282f567c9510a13b2fd83b576b0ab66dd8817d5cfca7bd7f06a7a22b` | Match |

Full passages were read against all 110 narration/claim rows: *Le Rappel* R40–117 (petition), R119–151 (initial interview), R153–266 (continued interview), and *L’Illustration* I1674–1700 (wireless notice), along with masthead dates R17 and I31. Key numbers match: the petitioners' projected **twenty years** (R89–92); Eiffel's reported **five to six million** franc estimate, **1.5 million** franc state subsidy, and **twenty-year operating right** (R133–140); later repeated Paris–Washington wireless exchanges, **over 6,000 km**, and **80 versus about 90 horsepower** (I1676–1693). Key names and places match: Alphand, Charles Garnier, Ferrié (*commandant*), Notre-Dame, Louvre, Arc de Triomphe, *Le Temps*, Académie des sciences, Paris, and Washington. The script correctly marks Eiffel's scientific uses as proposals, the 1913 radio exchange as a later event, and the absent contract/municipal decision as an evidence limit.

## Twelve audio-driven R5→R6 wording changes

The R6 commit changes exactly the twelve IDs listed in `audio-flags-final.json`; their current text matches `claims.md` and `video.json`. Here is the independent factual-equivalence ruling:

| ID | Ruling | Source check |
| --- | --- | --- |
| `et001` | Pass | 「排出」→「刊出」 correctly describes the printed February 1887 newspaper (R17, R27, R33). |
| `et014` | Pass | 「一進城」→「一建成」 retains the petitioners' imagined completed tower (R48–53, R83–92). |
| `et015` | Pass | 「抗議信寫道」 correctly attributes the Tower of Babel phrase to the petition (R52–55). |
| `et020` | Pass | 「抗議者」 correctly replaces the homophone-prone 「信」; the petition imagines future foreign visitors' mockery (R75–80). |
| `et022` | Pass | 「描繪出的」 retains the distinction between imagined and measured tower shadow (R83–92, R164–167). |
| `et027` | **Block pending wording fix or additional source** | Current script L120 says 「這封抗議信**刊出後**，艾菲爾先回應了什麼？」 and claim `et027` cites R119–123. Those lines say a *Le Temps* reporter sought Eiffel's view on a signed protest and summarize the interview; they do **not** date the interview relative to publication of the petition. The R5 wording 「信已登報；…」 did not make the same explicit before/after claim. A source-bound wording is 「面對這封抗議信，艾菲爾先回應了什麼？」; update script, video, and claim together, then freeze new hashes and redo the required narrative read. |
| `et030` | Pass | 「建築師加尼耶」 adds his role already established in the script; Charles Garnier and the committee claim are in R123–127. |
| `et076` | Pass | 「軍官費里耶」 is consistent with *commandant Ferrié* in I1676; 1887→1913 is over twenty years (R17, I31). |
| `et089` | Pass | 「報紙」 accurately names the 1913 notice that proposes the longitude measurement (I1688–1693). |
| `et096` | Pass | 「這篇報導沒有記載市府的決議」 accurately describes I1676–1700, without claiming to have checked city archives. |
| `et098` | Pass | 「鐵塔免於拆除」 spells out the antecedent; the sentence still refuses an unsupported radio-caused-rescue conclusion (R138–140, I1676–1700). |
| `et101` | Pass | 「我們讀過的報紙裡，找不到到期拆塔令」 keeps the limitation to these two read newspapers (R89–92, R133–140, I1676–1700). |

## Still prompts and visible text

I inspected all 100 English still prompts in scene order against their paired narration and the cited passages. **Still-image prompts pass:** no material visual contradiction in their dates, number of people, sites, objects, prospective uses, or the later wireless event. The prompts treat the petition's shadow as imagined (`eiffel-020`, `eiffel-022`), show a geometric drawing rather than a finished tower at `eiffel-056`, show the tower model's four outer curves at `eiffel-059`, keep the 1887 uses in workshop or planning scenes, and show radio telegraphy rather than a telephone call in 1913. These are declared cartoon illustrations rather than documentary reconstructions. The `cute-mystery` preset and music values match the series guidance; lint found no visual or pacing warnings.

**Visible-text qualification block:** `video.json`'s outro card `data.lines[0]` says 「二十年是經營期限；塔的後來用途有報紙可查」. The first clause drops the careful spoken attribution. R89–92 is the petitioners' **imagined twenty-year shadow**; R133–140 is **Eiffel's reported account** of a separate twenty-year operating right. The 1887 agreement itself has not been read. The card could collapse those two uses of “twenty years” and present his account as the contract's settled wording. A source-bound replacement would begin 「艾菲爾說：二十年經營權」 or otherwise make that attribution and distinction visible. This is a local card text correction, separate from the 100 illustration prompts.

## Gate

- **Blind narrative:** PASS, 13/13, on the exact R6 script hash above.
- **Pinned-source identity and claim alignment:** PASS for fetched hashes, 110/110 exact text mappings, 130 source links, names, numbers, and dated events; **one wording block** at `et027` for unproven publication-before-interview chronology.
- **Still prompts:** PASS, 100/100 reviewed; **one visible-text block** on the outro attribution.
- **Lint:** PASS, 0 errors / 0 warnings.
- **Overall R6 source/visual gate:** **BLOCK pending `et027` and outro card qualification.** Changing the spoken line produces a new script/narrative/speech hash and requires a new exact-hash narrative review. The original 1887 agreement and any municipal keep/demolish decision remain outside the pinned-source evidence, so no claim that a contract required demolition or that radio saved the tower is warranted.
