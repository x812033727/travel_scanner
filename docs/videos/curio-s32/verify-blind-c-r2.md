# Curio S32 narrative blind C

- Source read first: `/workspace/travel_scanner/docs/videos/curio-s32/script.md`
- SHA-256 verified before reading: `33668db15d862341bc16585f0f00f6f54d7c8ab7c55ed18074f269f444ce77c7`
- Scope: read-only editorial review of this exact script; no other S32 material consulted for first impression.

## Sealed first impression (before official questions)

The central distinction is clear and valuable: accurate descriptions of Yuan paper money and salt administration corroborate access to information about China, but cannot locate Marco Polo himself. The narrative earns that conclusion through three different checks: the replacement fee in the travelogue and official history (mp031–mp049), Yule's list of omissions and alternative access to knowledge (mp051–mp060), and the divergent Hangzhou tax-account versions (mp069–mp074). The manuscript variants add a genuine turn late in the piece: a phrase that sounds like firsthand service becomes hearsay in another version.

The opening introduces five threads in quick succession (prison, paper money, exchange fee, missing landmark, Hangzhou tax account; mp001–mp008), which makes the paper bill less singular as the visual object. The early premise implies the fee comparison may yield a verdict (mp004–mp005, mp033), but the script correctly stops at incompatible fee units (mp048–mp049); this is intellectually sound, yet the dramatic question receives a deliberately incomplete answer. Midsection momentum weakens where adjacent lines repeat source caveats without a fresh action or image (mp030, mp040, mp048–mp049, mp067–mp068, mp079–mp082). The audience can follow the logic, but several transitions are phrased as questions whose answer arrives almost immediately (mp023–mp024, mp039–mp042, mp045–mp049, mp071–mp074), giving a classroom cadence. The closing takeaway is precise; the audience prompt about checking a travelogue's correct details versus omissions (outro) is approachable, though the manuscript-variant reveal is the most memorable insight and could be more clearly recalled there.

This impression is sealed before reading the rubric, other S32 files, previous reviews, or source material.

## Official 13-question score

The official question text was obtained with `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s32 --json | jq -r '.questions[] | "\(.id): \(.question)"'` after the first impression above was sealed. `Yes` means the script meets the whole question as written. Clip IDs refer to the hashed script.

| Question | Score | Script evidence and editorial judgment |
| --- | --- | --- |
| `scene_first` | **Yes** | `mp001` opens in 1298, in a Genoa prison, with Marco dictating to a recorder; `mp002` names that recorder. `mp003–mp004` move to the paper-money passage rather than greeting the audience or announcing a subject. |
| `no_spoiler` | **Yes** | The first chapter withholds the law's fee (`mp005`), the landmark's name (`mp006`), and the Hangzhou alternative reading (`mp007`). `mp008` leaves the central proof question unanswered. |
| `one_line` | **Yes** | The inquiry progresses from source status (`mp009–mp017`), to the paper-money claim (`mp018–mp033`), to the official-law comparison (`mp034–mp049`), omissions (`mp051–mp060`), the stronger Hangzhou claim (`mp061–mp074`), and textual provenance (`mp076–mp084`). Later returns to the bill (`mp058`, `mp079`) add evidence instead of retelling its original description. |
| `no_toc` | **Yes** | `mp023–mp024` hold the bracket's origin as a question, and `mp075` points to a translator's prefatory page. Neither enumerates forthcoming sections; no chapter contains a verbal table of contents. |
| `chapters_link` | **Yes** | The post-preview restart explicitly recalls the opening preface (`mp009` after `mp008`). Subsequent chapter starts pick up the outstanding layer (`mp017→mp018`), law (`mp033→mp034`), omission (`mp050→mp051`), service claim (`mp060→mp061`), translator's page (`mp075→mp076`), and final question (`mp083→outro`). The law chapter delays its fee answer but opens the requested document. |
| `open_loops` | **Yes** | Hooks recur within short runs of clips: fee/landmark/version (`mp004–mp008`), paper source (`mp016–mp017`), brackets and merchant use (`mp023–mp028`), law/denominations/fee (`mp033`, `mp039`, `mp045`), omissions/service (`mp050–mp060`), salt accounts/version (`mp066`, `mp071`), and brackets/verdict (`mp079`, `mp083`). At narrated script pace there is no evident 90-second stretch without a pending question. |
| `payoffs` | **No** | Most loops resolve concretely: `mp004→mp032` gives 3%; `mp005→mp046` gives 30/20/30 wen; `mp006→mp051` names the Great Wall; `mp007/mp071→mp072–mp074` gives the alternate Hangzhou reading. But `mp023` asks *which version* supplied the bracketed signature/seal/penalty passage. `mp076–mp077` says the editor used an additional French witness and bracketed material unique to “another Italian version,” without identifying that Italian version. The promised source identification remains too vague to check. |
| `no_recap` | **No** | The travelogue's 3% replacement fee is stated at `mp032` and stated again at `mp048`; the second line compares units but does not explicitly call back the earlier reveal in the question's permitted form. Other reprises are more clearly named returns, such as `mp031` and `mp079`. |
| `chapters_are_events` | **No** | The first chapter heading, “牢房裡的一張紙幣” (line 5), is a scene/object rather than something happening. It can also suggest a physical banknote in the prison, while `mp001–mp004` only establish a book passage about one. The other headings are mostly acts or revelations: the preface concedes hearsay, the chronicle records another fee, and the Hangzhou sentence changes. |
| `outro_no_next` | **Yes** | The outro answers the paper-money question, asks the viewer how they read a travelogue, and invites subscription. It does not mention another video, episode, or file (`outro`). |
| `opening_hooks` | **Yes** | After the prison setup (`mp001–mp004`), the opening plants at least three distinct deferred moments: the Yuan law's fee line (`mp005`), an unnamed omitted landmark (`mp006`), and a Hangzhou passage beside another manuscript (`mp007`). `mp008` keeps the overall answer open. |
| `one_thread` | **Yes** | The paper-money proof question is the continuous difficulty (`mp008`, `mp031–mp049`, `mp058–mp060`, `mp079–mp084`). The Hangzhou variant (`mp069–mp074`) tests whether a seemingly stronger first-person claim survives textual comparison, so it advances that same difficulty. |
| `no_detour` | **Yes** | The currency chronology leads to the exchange-rule comparison (`mp034–mp049`); the salt records test the apparent firsthand Hangzhou account (`mp061–mp074`); bracket provenance limits what can be attributed to the travelogue (`mp076–mp082`). Details such as copper printing plates (`mp039`) slow the pace, but no whole section leaves the opening proof question or becomes a bare inventory. |

**Total: 10 Yes, 3 No.**

## Issues to carry forward

1. **Unpaid source-identification hook:** Either name the identifiable Italian witness at `mp076–mp077` or phrase `mp023` as a narrower question that the script's actual answer resolves. This is the clearest narrative defect because the bracket reveal is a late payoff.
2. **Repeated fee number:** `mp048` needs the 3% for comparison, but it is a second delivery of `mp032`'s numeric reveal. A direct named callback would satisfy the rubric and orient the comparison.
3. **First chapter label:** The title at line 5 depicts a bill in a jail although the script depicts a passage in a book (`mp001–mp004`). An action in the documented scene would be clearer and meet the chapter-title criterion.
4. **Pacing pressure, without a full detour:** The opening plants several threads before the bill investigation settles (`mp001–mp008`), and the law chapter spends many beats before the fee result (`mp034–mp046`). This is a watch point for spoken delivery, not an additional binary failure.

No repository file was changed. This review is bound only to the SHA-256 above; it should be rescored if the script changes.
