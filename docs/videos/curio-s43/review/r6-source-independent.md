# S43 R6 — independent source and written visual audit

**Verdict: PASS for the R6 source and written-prompt gate.** This is a local audit of text and prompts only; generated images, audio, and site output were outside scope.

## Frozen R6 candidate and witnesses

| File | SHA-256 |
| --- | --- |
| `research.md` | `06a5fbec636bd1bc026b93437aa3fe4d11567fa0a95cf4ac370e3a9d2af9a9d4` |
| `claims.md` | `87ac90ac011aba5b161becb59abfe2ed91dce4ef93b6b60520736fa78e9f6f6f` |
| `video.json` | `44720707b498d16c9d8e8bb4baff277f6314e36a12d7ac752f1b5d2f4a4a9240` |
| `script.md` | `b60bec26143f61fb9cff2805149b9e7597d76a37cb3eca0eea0532431f62b1f1` |

The pinned local PRIMARY text hashes equal `research.md`: L `/tmp/s43-life-letters.txt` `c795bf75dde25565205b8d3ec696e92cebc9019da7dd28d01936fa15bc334dec`; A `/tmp/s43-darwin-auto.txt` `eb2c4e03f7eff1ac5c6fdaa865099e8238df712d04e820c24d7768f6961cde96`; V `/tmp/s43-beagle.txt` `24b8d915eb5f61c091ee66403096bb3a950e3c0cb310caf086b6be0cc86781f1`.

## Four R5 HOLD items resolved

1. **`dn015` Henslow companion versus cabin.** R6 says `能在船上作伴的紳士`; L5631–43 says Fitz-Roy sought a naturalist as a companion and a gentleman. It does not say they would share a cabin. R6 boundary and Cambridge-study prompt keep the cabin out. The later cabin offer is independently reported by Darwin at L5951–53 and belongs to `dn065`.
2. **`dn032` Peacock letter contents.** R6 says Darwin declined in his letter to Henslow and *said* he had also written to Peacock. L5712–24 shows the refusal to Henslow; L5738–40 mentions a letter to Peacock without preserving its contents. R6 narration and boundary do not place refusal wording in the missing Peacock letter. The blank-envelope prompt makes no facsimile claim.
3. **`dn077c` telescope and compass.** R6 uses `望遠鏡和羅盤` in scene narration, `claims.md`, and research point 6b. L6231–35 says `a good telescope, with compass, 5 pounds`, which supports procuring both, but does not prove an attached compass. The prompt shows a plain telescope only. L6115–17 directly supports the earlier decision to buy nothing before matters settled.
4. **`dn014` small ship citation.** R6 adds L5965–68 to the L5620–57 companion citation. L5965–67 explicitly says `small vessel`; a cramped wooden cabin is labeled illustrative in the claim boundary. Henslow's 24 August letter does not itself supply ship size.

## Full claim, narration, citation, and date review

I checked the current 92 shot narrations, their claim boundaries, and written prompts against the cited L/A/V passages, including the edited-letter caveat. There are 93 scene objects: 92 `shot` scenes and one outro. All 92 shot IDs occur once, in identical order, with identical narration in `video.json`, `script.md`, and `claims.md`; each shot's line ID matches its scene ID. The three outro sentences also match video and script, and the three claims outro boundaries cover them.

The 92 claim rows have **106** scene citations: 89 L, 14 A, and 3 V. All URLs use the expected pinned commits, files, and valid nonempty line ranges. The L correspondence is Francis Darwin's later edited transcription, A is an edited 1876 memoir, and V is Darwin's later published voyage account. The current text retains those witness limits. Henslow's two-year duration and Peacock's proposed route remain forecasts; no line says the Admiralty approved a final South Sea route at that stage. The Henslow 24 August date and September 9 letter date are stated in the source headers; bracketed and uncertain dates in the selected L edition are identified as editorial in `research.md` and the claim preface. The father's `common sense` quotation is expressly a later memoir recollection, not a preserved 1831 quote.

Specific closing/payoff checks: **`dn026`** rests on Darwin's contemporary report of his father's objections at L5715–24, including `unfitting me to settle down as a Clergyman`; it is not a claim that his father foretold Darwin's later career. **`dn074a`** rests on Darwin's September 6 report at L6121–25 that Fitz-Roy told him to get written Admiralty freedom to leave `as soon and whenever I like`; R6 explicitly says the cited letters do not show whether he obtained it. These two payoffs have a factual basis under those attribution limits.

The September 9 turn is also correctly scoped. L6137–53 records the parcel thanks, Beaufort's *reported* victuals-books remark, and Darwin's unresolved South Sea condition; it gives neither a surviving parcel inventory nor the ledger nor final route instructions. L6220–35, later in that same letter, records another Fitz-Roy visit, driving and shopping, Darwin's `You may consider it settled that I go`, its accident caveat, and the purchases. `dn074d2–dn077c` and research point 6b preserve that sequence and make the decision Darwin's own. A891–99 presents the nose story as something Darwin heard after becoming intimate with Fitz-Roy; the outro correctly limits the absence of a nose rejection to the cited contemporary letters. V63–78 supports thanks and accommodations; V147–53 supports the two gale-driven returns, ten-gun brig, and 27 December 1831 sailing; A938–45 supports Darwin's own retrospective career and uncle-carriage judgment.

## Written visual prompts

I inspected all 92 written shot prompts against their narrations and claim boundaries. They show at most one adult historical person in a frame, or no historical person; elderly memoir Darwin is distinct from the 22-year-old voyager. `dn014–015` do not turn the initial companion condition into a shared-cabin offer; `dn007/057/058/076` do not display or assign Darwin Fitz-Roy's missing Wood letter; `dn032` does not invent Peacock-letter text; `dn074a` does not depict an issued Admiralty guarantee; `dn074e` uses an unmarked illustrative ledger; `dn077c` does not depict an attached compass; `dn078–083` avoid a formal nose examination. Charts and globes leave the route unfinalized. The exterior prompts at `dn027/086/087` now specify an `1831 British naval brig`, consistent with V147–53 and resolving the R5 vessel-design advisory at the written-prompt level. Exact image fidelity remains a later generated-image check.

No repository files were edited. No paid, media, or site tools were called, and no other R6 audits were inspected.
