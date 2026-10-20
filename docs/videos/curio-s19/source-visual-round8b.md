# Curio S19 R8b — sealed independent source and visual audit

**2026-10-20 UTC · Source/visual verdict: PASS · No BLOCK.** This is a read-only audit of the exact frozen R8b script, claims and video JSON. The separate script-only blind reader sealed **13/13 YES** for this same script in `docs/videos/curio-s19/blind-seal-round8b.md`; I did not repeat or reinterpret its narrative read. This audit establishes source and planned-visual validity, not rendered-image quality, audio quality, site-owner approval or publication readiness.

## Frozen inputs and method

| Artifact | SHA-256 |
| --- | --- |
| `docs/videos/curio-s19/script.md` | `5cd4402a833139ea9e4c0c4b6458f347eddcc4b441762033f9f0026cf4ef8a49` |
| `docs/videos/curio-s19/video.json` | `a462fff787f1aa016ad343c96682a889184b5aa561e6bca1e5859ac705807f68` |
| `docs/videos/curio-s19/claims.md` | `be479b16da9e7a3909e8c677cf636724719cfb232b48c34f7690dcaa17fc81b4` |
| R8 source/visual audit `source-visual-round8.md` | `d57018e773b0d6c5bffa9e077de47b67656e585976bc27232f86ca1daf5bce6b` |
| R8 per-row/per-still `source-ledger-round8.json` | `93d38046c91a308015971071ddc974ec00a98dc6def5af370f2968708604de79` |
| R8b script-only blind seal | `0a6749b5dc0858408f99e0d0e3a496656aa17b1168ef0909064faccd4b18cf8a` |
| This audit's machine comparison `/tmp/curio-s19-r8b-machine-audit.json` | `b3ca7b30a237df4410aed1f786134fd96c94397c9e445dd0deb4a404b316a965` |

I freshly fetched both complete contemporary newspaper transcriptions at the **fixed Git revisions** used in `claims.md`. The 1887 *Le Rappel* no. 6185 text (`a10e54e67c3f6945d1f0123d76732950889d1447`, local `/tmp/curio-s19-r8b-pinned-0.txt`) hashes `91d3e9397aca543f900c9babd37fd2489097677a3eb378f5944e5af7af14f9ec`. The 1913 *L’Illustration* no. 3666 text (`35610f7d0cc21e2c5877c58628edb25c796f3bd1`, local `/tmp/curio-s19-r8b-pinned-1.txt`) hashes `db280680282f567c9510a13b2fd83b576b0ab66dd8817d5cfca7bd7f06a7a22b`. Both exactly match the pinned source bytes in `research.md` and the R8 audit. The newly fetched texts have 268 and 2,228 lines, respectively. All linked line ranges were checked against those files.

The deterministic comparison found **110/110** ordered narration lines identical between `script.md` and `video.json`, **110/110** IDs and exact texts identical between `video.json` and `claims.md`, unique IDs, **129/129** valid fixed-revision source links across 109 source-bound rows, **100** still scenes and one outro. Every link's repository, revision, file path and `#L` start match its displayed line reference; all cited end lines exist. `et103` is an invitation to subscribe and has no historical citation. R8 had 130 links; R8b has 129 because two irrelevant old references were removed and one useful reference was added. All unlisted links and citation labels are unchanged.

## Four R8b narration and claim changes

| ID | Exact R8b narration and source check | Verdict |
| --- | --- | --- |
| `et062` | 「還記得信裡那些被壓小的名勝嗎？艾菲爾怎麼反駁？」 R83–88 lists Notre-Dame and other monuments as *the protesters' imagined* structures crushed or made smaller; R206–212 starts Eiffel's reply and his Notre-Dame square question. The line explicitly recalls that earlier claim and asks for the reply. Its R8 citations, R83–88 and R206–212, remain apt. | **PASS** |
| `et066` | 「塔的尺度，連艾菲爾自己都能預料嗎？」 R222–225 says no one can judge the tower's artistic effect in advance, **not even Eiffel**, because the dimensions of the foundations then emerging surprised him. This is an accurate question that `ea108` immediately answers. The obsolete R83–92 protest citation was removed; R222–226 remains. It does not assert that the tower was already complete or that Eiffel was unaware of his own plans. | **PASS** |
| `et067` | 「還記得信上那句『無用』嗎？艾菲爾又怎麼回答？」 R52–55 explicitly calls the proposed tower *inutile* in the petition. R228–241 turns to the question of utility and Eiffel's proposed uses. R225–236 was added to the claim row to cover the transition. The wording attributes “useless” to the petition and sets up the next chapter's response. | **PASS** |
| `et071` | 「但說出這些用途，就等於當時已經做成了嗎？」 R236–241 uses future or prospective wording (*promet*, *permettra*, *sera*) for observations, wartime communication and engineering display. The question and `et072`'s “不能” correctly distinguish the 1887 proposal from the 1913 accomplished wireless contact. R164–167, which only concerned the still-unbuilt tower, was dropped; R236–241 remains. | **PASS** |

`et015` remains exactly the R8 audio-corrected line in all three files: 「抗議者寫道，人們早把它叫作『巴別塔』。」 R52–55 says the protesters wrote that the public had already dubbed it *tour de Babel*. The attribution and distinction between protesters' report and the film's own label remain correct. **PASS.**

## Changed still and the unchanged material

`eiffel-066` is the **only** changed prompt, now: “Medium shot in an 1887 drafting studio, one engineer studying a plain tower base model beside rolled plans, soft window light.” Its paired `et066` asks whether Eiffel could foresee the tower's scale; R222–225 reports his surprise at the emerging foundations. A plain cartoon model conveys a construction-scale discussion without asserting that a documented historical model survives or visually declaring a completed tower. The next shot, `eiffel-add108`, retains a surprised engineer at foundations rising above ground. The changed prompt is content-relevant and does not contradict the source or narration. **PASS.** This is prompt review; no generated image was available or assessed.

The R8 ledger's ordered IDs, the other **106/110** narration texts, **107/110** citation-label lists, **99/100** still prompts and the outro card are unchanged byte-for-byte or text-for-text as applicable. The only citation-list changes are `et066` (R83–92 removed), `et067` (R225–236 added) and `et071` (R164–167 removed). The R8 audit reviewed all rows and 100 prompts against these same source bytes; source hashes now match, and the unchanged rows, links, prompt/line pairings and outro inherit that still-valid source equivalence. I additionally checked the core unchanged passages: R89–92 is protesters' imagined twenty-year shadow; R133–140 is Eiffel's reported twenty-year operating right followed by city discretion; R164–169 concerns only the circulated geometry drawing; R206–226 contains his Notre-Dame, Arc and foundation responses; R236–241 lists possible future uses. I1674–1693 records several Paris–Washington **wireless** contacts and a longitude measurement still to be arranged, while I1676–1700 supplies no municipal disposal decision. The script and outro preserve those attribution, chronology and uncertainty boundaries. No prompt depicts a binding demolition order, a proven “radio saved the tower” event, or a literal transatlantic telephone call. **PASS.**

The outro card remains 「艾菲爾說：他有二十年經營權；後來用途有報紙可查」. Its first clause is explicitly attributed to Eiffel's report at R133–140; the second has the 1913 wireless notice at I1674–1696. **PASS.** The newspaper transcriptions do **not** establish the full 1887 agreement, any 1909 demolition order, or a municipal decision caused by radio. This is a source boundary, not a blocker for the claims actually made.

## Gate and scope

`node tools/video/cli.mjs lint --slug curio-s19 --json` exited 0: **0 errors, 0 warnings**, 110 lines, seven chapters, estimated 9.33 minutes. The R8b source/visual gate is **PASS**: 110 aligned rows, 129 valid pinned links, 100 reviewed prompt positions with one changed prompt checked directly, and one supported outro. The separate exact-script blind seal reports **13/13 YES**. No episode file was edited by this audit, and no audio, image, keyframe, approval or publication operation was performed.
