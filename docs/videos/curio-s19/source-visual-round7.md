# S19〈艾菲爾鐵塔〉 R7 independent source and visual audit

2026-10-20 UTC. **Verdict: PASS** for the frozen R7 narration, source claims, still prompts, and outro card. No episode file or paid media was changed by this audit. This review started only after I sealed the independent script-only reading at `/tmp/curio_s19_r7_fresh_blind_seal.md` (SHA-256 `f2af90b00a696ab132df916ff72ec156819ec63d07d108cc13844e574b64abc3`). That seal gave 13 Yes / 0 No plus 13 cold-viewer comprehension answers. The corresponding validator-ready 13-answer JSON is `/tmp/curio_s19_r7_fresh_blind_answers_valid.json` (SHA-256 `479c97307f103b966628967812f700721395a1ffebb3654f2dd39752535104b0`); direct `panelVerdict` returned `passed: true`, 13 answers, no truncation. The first machine JSON lacked the CLI's bracketed-line-ID syntax, so the audio QA agent preserved its rejected input-format receipt; this did not change the blind verdict or script.

## Exact inputs and mechanical checks

| Input | SHA-256 |
| --- | --- |
| `docs/videos/curio-s19/script.md` | `9067354cd8409e3202d0562f12006374a05f297c6d95c645d220d2c8bed2d6df` |
| `docs/videos/curio-s19/video.json` | `c8d1d20af1a94f527282cc39464369e30c6ebbc02e14c250a6e0cf82045e0` |
| `docs/videos/curio-s19/claims.md` | `f9032510e531e5459cd72353b322009ab002709f71714320498626bf291d9629` |
| `docs/videos/curio-s19/research.md` | `f60999f435e77174e8ac12dc4bd6690644fbbddc8bd5af3daf9977b7f6ed4341` |
| `docs/videos/curio-s19/audio-flags-final.json` | `c7a8cac75073cbfc8282f01402bf3740127b7f4e38b4445158edc35d81d2f829` |

`node tools/video/cli.mjs lint --slug curio-s19 --json` exited 0 with **0 errors / 0 warnings**; it reports 110 lines, seven chapters, and 9.3189 estimated minutes. I compared the 110 ordered `video.json` narration IDs and texts, the 110 `claims.md` rows, and the 110 spoken sentences extracted from `script.md`: all IDs are unique and every paired sentence agrees exactly. The claims contain **130** pinned newspaper links over **109** source-bound rows; `et103` is only the subscription CTA. Every link has the correct Git revision/path, starts at its stated source line, and names a line or range within the fixed text. Both `video.json` source URLs use the matching revisions.

I refetched the two complete texts from their fixed Git revisions, checked them against the prior local copies, and reread the passages. Hashes match the research record:

| Source | Fixed revision; passage read | SHA-256 |
| --- | --- | --- |
| 1887-02-15 *Le Rappel* no. 6185, Project Gutenberg 77985 | `a10e54e67c3f6945d1f0123d76732950889d1447`; R17, R27–266 | `91d3e9397aca543f900c9babd37fd2489097677a3eb378f5944e5af7af14f9ec` |
| 1913-05-31 *L’Illustration* no. 3666, Project Gutenberg 38842 | `35610f7d0cc21e2c5877c58628edb25c796f3bd1`; I31, I1672–1700 | `db280680282f567c9510a13b2fd83b576b0ab66dd8817d5cfca7bd7f06a7a22b` |

## All 110 narration and claim rows

I checked every row, including questions and editorial interpretation, against its source passage. The chapter coverage is **8 + 21 + 11 + 16 + 19 + 16 + 19 = 110** rows:

| Narration IDs, in chapter order | Rows | Source and finding |
| --- | ---: | --- |
| `et001`–`et008` | 8 | R17, R27–55, R89–92, R119–143, R164–167; I1674–1678. The opening establishes the dated publication, unbuilt tower, petitioners' accusation and projected shadow, then leaves results open. |
| `et009`–`et027`, with `ea101`, `ea102` | 21 | R44–117 and R119–123. Alphand, writer/painter/sculptor/architect signers, named landmarks, future foreign visitors, twenty-year imagined shadow and paper protest are faithful to the petition. `et027` is addressed separately below. |
| `et028`–`et037`, with `ea113` | 11 | R119–151. The *Le Temps* reporter's question, Garnier's signature/committee role, Eiffel's “one year earlier” argument, contracts/ordered iron and predicted visitors are all attributed to Eiffel. |
| `et038`–`et053` | 16 | R119–140 and R153–157. Cost **5–6 million francs**, state grant **1.5 million francs**, exposition operation, subsequent Paris City **20-year operating right**, and post-term city disposal match Eiffel's **reported** account. The reporter then raises keeping the tower after the fair. No contract text or demolition duty is claimed. |
| `et054`–`et067`, with `ea104`–`ea108` | 19 | R157–226. Eiffel's “too early” answer, widely circulated geometrical drawing, hypothesized beauty, wind-calculated four curves, scale, Notre-Dame square and Arc de Triomphe examples are kept as his rebuttal or an imagined objection, not measured outcomes. |
| `et068`–`et079`, with `ea109`–`ea112` | 16 | R52–55, R236–266; I31, I1674–1678. Meteorology, astronomy/physics, wartime linkage and engineering progress are 1887 proposals; Ferrié's later Academy note is introduced separately. The 1887 interview does not mention wireless. |
| `et080`–`et103` (with omitted legacy ID numbers as in file) | 19 | I1674–1700, plus R52–55, R89–92, R133–140, R164–169 for comparison/ending. The notice reports **several** Paris–Washington wireless exchanges, **over 6,000 km**, Paris **80 hp** and Washington **about 90 hp**; longitude measurement is still planned. “Causé” is correctly explained as wireless communication, with no telephone scene. The notice records no municipal keep/demolish decision. `et103` is an uncited CTA. |

**Chronology check:** `et027` at script line 120 now says 「面對這封抗議信，艾菲爾先回應了什麼？」. R119–123 says a *Le Temps* reporter sought Eiffel's view of a signed protest, and R123 starts his summarized reply with *Tout d'abord*. The R7 line identifies the topic and first answer; it makes **no claim that the interview happened after publication**. `et028` at line 126 names that reporter and likewise does not date the interview. The earlier R6 wording 「刊出後」 was not proved by R119–123 and is absent from R7. The story order is a reading order, not an asserted interview date.

**Twenty-year and survival boundary:** R89–92 is the petitioners' projected twenty-year oppressive shadow. R133–140 is Eiffel's separate **reported** twenty-year operating right and his statement that, at expiry, Paris City could dispose of the tower. The actual 1887 agreement and municipal decisions were not among these two read newspapers. Accordingly `et047`–`et049`, `et095`–`et101`, and the title do not claim a binding demolition order, nor that later radio use alone saved the tower. The 1913 notice proves a later recorded use, not a causal rescue.

## Twelve audio-driven R5→R7 rewrites

The R5 baseline is commit `c6f3d247`, whose `script.md` SHA-256 is `a68cc615c3d79ad7b1cac7002d5a20179b2f6cc09b1e739071e4f479e0d7eb5a`. Comparing its 110 `video.json` sentences to R7 finds **exactly 12 changed IDs**, identical to the 12 entries in `audio-flags-final.json`; all other narration texts are unchanged. Each R7 wording agrees with its pinned passage:

| ID | R7 factual-equivalence decision |
| --- | --- |
| `et001` | **Pass.** 「刊出」 accurately describes the dated Paris printing (R17, R27, R33, R40–42). |
| `et014` | **Pass.** 「一建成」 keeps the petitioners' future scenario (R48–53, R83–92). |
| `et015` | **Pass.** 「抗議信寫道」 explicitly attributes “Tower of Babel” to the petition (R52–55). |
| `et020` | **Pass.** 「抗議者」 identifies who imagined foreign visitors' mockery (R75–80). |
| `et022` | **Pass.** 「描繪出的」 retains the imagined-versus-measured distinction (R83–92, R164–167). |
| `et027` | **Pass after R7 correction.** 「面對這封抗議信」 retains Eiffel's initial reply without asserting an unproved post-publication sequence (R119–123). |
| `et030` | **Pass.** “Architect Garnier” is consistent with Garnier's signature and committee role (R108, R123–127). |
| `et076` | **Pass.** “Officer Ferrié” follows *commandant Ferrié*; 1913 is over twenty years after 1887 (I31, I1676; R17). |
| `et089` | **Pass.** 「報紙」 is the 1913 notice that suggests a longitude measurement (I1688–1693). |
| `et096` | **Pass.** 「這篇報導沒有記載」 correctly limits the negative claim to the notice (I1674–1700). |
| `et098` | **Pass.** “Tower saved from demolition” is expanded only inside an explicit unsupported-causation warning (R138–140, I1674–1700). |
| `et101` | **Pass.** 「我們讀過的報紙裡，找不到」 limits the missing order to the two reviewed newspapers (R89–92, R133–140, I1674–1700). |

## All 100 still prompts and the outro card

I inspected **100/100** English still prompts in scene order against their paired narration and source context: `eiffel-001`–`eiffel-098` as numbered in `video.json`, including the inserted `eiffel-add101` etc., then the one `outro` scene. There is **no material visual contradiction**. The 1887 prompts show petition, newsroom, unbuilt foundations, drawings, hypothetical shadow and Eiffel's design/planning statements; the later prompts show a 1913 wireless telegraph station and contemporary archive comparison. `eiffel-022` explicitly says the shadow is *imagined*; `eiffel-056` shows a geometry drawing; `eiffel-059` shows the four outer curves; `eiffel-084` contrasts telegraph and telephone drawings rather than depicting a telephone call. Illustrations are cartoons, not evidence reconstructions. Source-negative reasoning appears in present-day archive imagery without inventing a municipal decree. A comparison to the R5 baseline found **0 changed still prompts**.

The **outro visible text passes**: `data.lines[0]` is 「艾菲爾說：他有二十年經營權；後來用途有報紙可查」. “艾菲爾說” ties the right to his reported interview (R133–140), while the later-use clause is grounded in the 1913 wireless notice (I1674–1696). It no longer makes the R6 card's unqualified claim that the contract itself established the twenty-year term. The `cute-mystery` preset and music values match the series settings; lint raised no visual warnings.

## Gate and limits

- **Blind story panel:** PASS, 13/13, on the exact R7 script hash.
- **Pinned sources:** PASS, both newly fetched SHA-256 values match the cited records.
- **Narration and claims:** PASS, 110/110 text-aligned and source-bounded, with 130/130 pinned links valid; no unsupported post-publication ordering at `et027`.
- **Still prompts and outro card:** PASS, 100/100 still prompts and 1/1 card reviewed; the operating term is attributed on screen.
- **Lint:** PASS, 0 errors and 0 warnings.
- **Overall R7 source/visual gate:** **PASS.** Audio synthesis, listening, still-image generation, and owner production gates are separate and were not performed here. The unread original agreement and municipal records still prevent stronger claims about mandatory demolition or radio-caused survival.
