# Curio S19 R8 — independent source and visual audit

2026-10-20 UTC. **Source/visual verdict: PASS. Overall R8 narrative gate: BLOCK (blind panel 12/13).** This audit began after the blind report and machine answers were sealed at `/tmp/curio-s19-r8-blind.md` (SHA-256 `918311adf669f8afcdb1134585969b59a9364323cf0308bbf0b252ab039f117d`) and `/tmp/curio-s19-r8-blind.json` (SHA-256 `811360fb2fbfcaadcf74d53c93b191bc354127651f3404b9e22b104828856e80`). The blind report uses only `script.md` and the supplied panel. Its sole NO is `no_recap`: the unbuilt-tower fact returns at [et066] and [et071] after the explicit [et055] recall. The same wording was present in R7, so this narrative objection was not caused by the R8 edit.

## Exact inputs and source provenance

| Input | SHA-256 |
|---|---|
| `script.md` | `b9d5d83154f03f8aba0445b3c58ea92e81072527dbbeafa83726464682196293` |
| `claims.md` | `69e1b559631c247ad3745a6a95edd934064aea66b4221aef8fd035ab0ff22f6d` |
| `video.json` | `01c829a71250540f4271f9935c6c9adbb893566e332a2bfc98dc03ca4399e011` |
| `research.md` | `f60999f435e77174e8ac12dc4bd6690644fbbddc8bd5af3daf9977b7f6ed4341` |
| R8 panel | `36fcf54a32bb746e746c2ed2296160c6a70f4426dc7088ba365c4c61c1198022` |
| 1887 *Le Rappel* no. 6185, fixed Git revision `a10e54e67c3f6945d1f0123d76732950889d1447` | `91d3e9397aca543f900c9babd37fd2489097677a3eb378f5944e5af7af14f9ec` |
| 1913 *L’Illustration* no. 3666, fixed Git revision `35610f7d0cc21e2c5877c58628edb25c796f3bd1` | `db280680282f567c9510a13b2fd83b576b0ab66dd8817d5cfca7bd7f06a7a22b` |

I fetched both complete newspaper texts afresh from those exact Git revisions into `/tmp/curio-s19-r8-rappel-refetched.txt` and `/tmp/curio-s19-r8-illustration-refetched.txt`; each byte hash matches the research record and the R7 pinned copy. *Le Rappel* R17 and R27–266 and *L’Illustration* I31 and I1672–1700 were read. The primary artifacts available here are fixed transcriptions of contemporary newspapers. The 1887 agreement and municipal disposal records remain unread, as `research.md` records.

## All narration and claim rows

The 110 spoken sentences extracted from `script.md`, 110 ordered `video.json` line IDs/texts, and 110 `claims.md` rows agree exactly, including the 12 `ea` insertions and `et015`. All IDs are unique. The claims have 130 pinned links (106 R, 24 I) over 109 source-bound rows; `et103` is a subscription invitation. Every URL has the proper fixed revision and path, its fragment starts on the cited line, and its cited range exists in the freshly fetched source. The accompanying JSON ledger records every one of the 110 rows, its citations and review status.

| Chapter narration IDs | Rows | Source check |
|---|---:|---|
| [et001]–[et008] | 8 | **PASS.** R17, R27–55, R89–92, R119–143 and I1674–1678 establish the printed protest, unbuilt foundations, quoted fear and later news hook. |
| [et009]–[et027], [ea101], [ea102] | 21 | **PASS.** R44–117 establishes Alphand, signers, imagined damage and twenty-year shadow. [et015] is checked separately below. |
| [et028]–[et037], [ea113] | 11 | **PASS.** R119–151 establishes a *Le Temps* reporter asking Eiffel and Eiffel's attributed Garnier, contract, iron order and visitor comments. |
| [et038]–[et053] | 16 | **PASS.** R133–140 and R153–157 support the 5–6 million francs, 1.5 million grant, exposition operation, *reported* twenty-year city operating right and city's later discretion. |
| [et054]–[et067], [ea104]–[ea108] | 19 | **PASS.** R157–226 supports Eiffel's conditional aesthetic defense, geometrical drawing, wind-derived four curves, Notre-Dame and Arc comparisons, and surprise at foundations. |
| [et068]–[et079], [ea109]–[ea112] | 16 | **PASS.** R52–55 and R236–266 establish possible science and wartime uses and Eiffel's reaction to the petition; I1674–1678 introduces a later, separate event. |
| [et080]–[et103] (sparse legacy IDs) | 19 | **PASS.** I1674–1700 supports several Paris–Washington wireless contacts, over 6,000 km, Paris 80 hp / Washington about 90 hp, and a longitude experiment still pending. R52–55, R133–140 and R164–169 support the comparison and closing questions. |

**R8-only change, [et015]: PASS.** R52–55 says the protesters called the planned tower *inutile et monstrueuse* and wrote that *la malignité publique ... a déjà baptisée du nom de «tour de Babel»*. 「抗議者寫道，人們早把它叫作『巴別塔』」 faithfully attributes the public nickname to what protesters wrote. It does not present “Tower of Babel” as the film's own neutral label. The R7 line said 「抗議信寫道」. A direct R7-to-R8 comparison of `script.md`, `claims.md` and `video.json` finds only that narration wording changed; the script's narrative/speech hashes were regenerated accordingly.

**Chronology and attribution: PASS.** R119–123 says the *Le Temps* reporter went to seek Eiffel's view and starts Eiffel's answer with *Tout d'abord*. It does not date that interview relative to publication. [et027] and [et028] give the topic and reporter without saying it happened afterward. R89–92's “twenty years” is the protesters' imagined shadow; R137–140's twenty years is Eiffel's reported operating right. [et047]–[et049] explicitly limit the legal interpretation to his newspaper account. R236–241 is an 1887 list of *possible* uses; [et071]–[et073] do not recast it as accomplished wireless work. I1676–1693 records actual wireless communication and a future plan to measure longitude. Its quoted *causé* is framed by the title *T.S.F.*; [et083]–[et084] correctly avoid a literal telephone scene. [et095]–[et101] limit absent municipal decisions and demolition orders to the newspapers reviewed and reject an unsupported “radio saved the tower” causal leap.

## All still prompts and outro

The 100/100 English still prompts were inspected in scene order against their paired narration and the sources; the JSON ledger lists each prompt and status. **PASS:** 1887 shots show a petition, print shop, foundations, models and proposed uses; shadows are drawn as imagined ([et022]); the 1913 shots show wireless apparatus, with a telegraph versus telephone drawing at [et084]. Present-day archive shots accompany the limited negative findings [et095]–[et098]. No prompt depicts an actual demolition order, proven radio rescue or literal transatlantic phone call. All 100 prompts are byte-for-byte unchanged from R7.

The 1/1 outro card is **PASS** and unchanged from R7: 「艾菲爾說：他有二十年經營權；後來用途有報紙可查」. Its first clause is attributed to Eiffel's reported statement at R133–140; the second rests on the 1913 notice at I1674–1696. The illustrations are cartoon scene prompts, not reconstructed documents or portraits; text is delivered by narration/card rather than source-looking printed words.

## Checks and gate

`node tools/video/cli.mjs lint --slug curio-s19 --json` exited 0 with **0 errors, 0 warnings**, 110 lines and seven chapters. Source/visual review passes for 110/110 narration and claim rows, 130/130 citation links, 100/100 still prompts and 1/1 outro card. The overall R8 narrative gate remains **BLOCK** because the independently sealed blind panel gave 12 YES / 1 NO. This audit does not establish a binding demolition clause, a municipal keep/demolish decision, or a causal claim that wireless prevented demolition. No episode file, TTS, keyframe or image generation was changed or run for this audit.
