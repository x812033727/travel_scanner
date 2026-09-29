# Independent second-round fact review — free-vs-paid-ai-plans-2026

Reviewer: `codex-p1-news` / `audit_video`, different from both the original author and first-round reviewer. Checked: **2026-09-29**.

**Second-round review completed; publication remains BLOCKED by CTA evidence and owner/editorial decisions. This is not production, audio, final-edit or publication approval.**

Reviewed `video.json` SHA-256: `7124a51516a02ee92f30b17980542d2e18cca88e8f05dd3908aadf98659f7b42`. No script or claim-register changes in this round; the hash is unchanged.

## Method and coverage

Read the full first-round claim table and changed-field appendix, current `video.json`, historical and corrected sections of `claims.md`, and the brief. Independently extracted all string fields, including spoken text, slide data, thumbnail, title, description and tags, to the external `plans-round2-extraction.json` artifact before comparing the findings. The old register is historical evidence, not the current approved assertions.

Rechecked all six CHANGED groups (`c5`, `c6`, `c7`, `f13`, `f14`, `f17`), all four removed/unconfirmed groups (`c2`, `c9`, `c12`, `f15`), and the still-unresolved CTA (`f18`). The confirmed pool was `[c3,c4,c8,c11,f16]`; Python `random.Random(20260929).sample(pool, 2)` selected **c11 and c8**, which is at least one third. Also checked the other three confirmed groups while reading their source pages. Opinion groups c1/c10 were reviewed without rewriting the owner's stance.

Used the `youtube-video` verifier instructions and OpenAI Docs. Performed one official-domain OpenAI documentation search, then opened the actual pricing page. Independently opened all seven official pages below today and read the relevant bodies; checked the same-day raw-HTTP receipt and the available comment-stripped source text. No search snippet or previous reviewer verdict was treated as proof. The transient web `find("128")` miss was resolved by opening the **Context windows** table; both its body and the saved text contain 32k / 128k / 1 million.

## Claim decisions

“Removed” means the unsupported assertion is absent from the current spoken/visual/metadata extraction, not that the opposite has been proved.

| ID | First-round disposition / current claim | Location | Source / raw HTTP | Second-round verdict | Result |
|---|---|---|---|---|---|
| c2 | Removed daily three-file assertion | `free-limits.xb2w`, table row 0 | [OpenAI pricing](https://learn.chatgpt.com/docs/pricing), 200 | NOT FOUND; removal confirmed | The permitted source does not establish that daily cap. Current script asks viewers to inspect their account limit; no numerical cap remains. |
| c5 | Changed Go/Plus price and Codex access | `entry-plans` rows 0–1; `6iqr`, `tjm4`, `jnxh`; `five-users.kax6` | [OpenAI pricing](https://learn.chatgpt.com/docs/pricing), 200 | CONFIRMED | Go $8/month and Plus $20/month; Free/Go desktop Luna is subject to rollout, while Plus lists additional surfaces and Sol/Luna. “Codex requires Plus” is gone. Do not extend this Codex table into a claim about every ChatGPT chat model. |
| c6 | Changed annual arithmetic | `entry-plans.dbei`; `annual` data and narration | [Claude pricing](https://claude.com/pricing), 200 | CONFIRMED | Pro is $20 monthly or $200 paid annually, and includes Claude Code. $200/12 ≈ $16.67; $20×12−$200=$40, or $3.33/month. All current occurrences agree. |
| c7 | Changed unsupported absence of annual option | `entry-plans`; `gemini-perks`; `annual.buep` | [Google Taiwan plans](https://gemini.google/tw/subscriptions/), 200 | CONFIRMED | Taiwan Plus NT$165/month, 2× stated usage, video generation and 200 Flow credits appear on the page. The script no longer infers that other billing periods cannot exist. |
| c9 | Removed universal App/web price and missing Taiwan-price assertions | `twd-note`; `three-things` | No universal official evidence; n/a | NOT FOUND; removal confirmed | Current wording recommends checking the same plan, period, tax and checkout total. It no longer asserts a specific price difference or absence of localized prices. |
| c12 | Removed blanket cancellation/refund guarantees | `cancel`; `upper-tier.data.right` | [Claude pricing FAQ](https://claude.com/pricing), 200; no three-provider proof | NOT FOUND; removal confirmed | Claude itself lists regional and purchase-channel qualifications. The script now asks viewers to inspect applicable terms; no universal refund/expiry promise remains. |
| f13 | Changed free/paid model generalization | `model-tier` data; `2xji`, `nbjf`, `ipyc`, `47pj` | [Claude pricing comparison](https://claude.com/pricing), 200 | CONFIRMED | Free includes Sonnet/Haiku; Pro includes Opus. Current narration is a Claude example and makes no blanket capability claim for all free models. |
| f14 | Removed “only provider with Taiwan dollar prices” | `entry-plans.a88i` | [Google Taiwan plans](https://gemini.google/tw/subscriptions/), 200 | CONFIRMED | Positive Taiwan-price observation remains; exclusivity is gone. |
| f15 | Removed population claim about never needing higher tiers | `upper-tier.8ffa` | No population evidence; n/a | NOT FOUND; removal confirmed | Current sentence explicitly starts with a personal recommendation. |
| f17 | Removed “two choices for every user” | `five-users.cjpd`, `data.steps` | Current script; n/a | CONFIRMED | Current wording does not assert a count; the five rows may contain different numbers of alternatives. |
| c8 | Random confirmed sample: Gemini Pro and regional prices | `entry-plans`; `gemini-perks`; `context-stats` | [Taiwan](https://gemini.google/tw/subscriptions/), [US](https://gemini.google/subscriptions/), [limits](https://support.google.com/gemini/answer/16275805); 200 each | CONFIRMED | Taiwan Pro NT$650, 4× and 1,000 Flow credits; US Plus/Pro $4.99/$19.99. These are regional prices, not a currency conversion. |
| c11 | Random confirmed sample: Max | `upper-tier.gczp`, `j8z4`, data | [Claude pricing](https://claude.com/pricing), 200 | CONFIRMED | Max starts at $100/month. Its 5×/20× usage comparison is per five-hour session in the FAQ, not a promise of that multiplier for every weekly/model limit. $100/$20=5 for the stated entry-price comparison. |
| c3 | Additional check: Claude limits | `free-limits`; `claude-limits`; `writer-case` | [Free help](https://support.claude.com/en/articles/8114491-get-started-with-claude), [Pro help](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan); 200 each | CONFIRMED | Five-hour session resets and Pro's additional cross-model weekly cap are explicitly documented. No fixed number of messages is inferred. |
| c4 | Additional check: context capacities | `free-limits`; `context-stats` | [Gemini limits](https://support.google.com/gemini/answer/16275805), 200 | CONFIRMED | 32k, 128k and 1 million match the plan table. 1,000,000/32,000=31.25. Capacity is not a guarantee that every detail will be recalled. |
| f16 | Additional check: monthly options | `switch-cost` | [OpenAI](https://learn.chatgpt.com/docs/pricing), [Claude](https://claude.com/pricing), [Google Taiwan](https://gemini.google/tw/subscriptions/); 200 each | CONFIRMED | The three cited individual-plan pages list monthly options. This does not prove equal refund rights or migration costs. |
| c1 | Free-first recommendation | `one-question`; `wrap` | Editorial judgment; n/a | OUT OF SCOPE | An opinion, not a measured guarantee that free plans suffice for every viewer. Owner acceptance remains necessary. |
| c10 | Five user recommendations | `five-users`, especially `g5f8` | No independent quality comparison; n/a | OUT OF SCOPE | “重視品質選 Claude Pro” sounds like an unqualified quality ranking and conflicts with the brief's avoid-ranking stance. Reported for owner/editorial decision; not silently rewritten as fact. |
| f18 | Article coverage, first-line link and continuing updates | `cta.iej3`, `cq7t`, `qat2`; `wrap.data.cta`; `youtube.source_guide` | Production article not inspected; n/a | NOT FOUND; unresolved publication gate | Must verify actual published article contents and packaged link, qualify the update promise, or remove the unsupported CTA before publication. No production request was added. |

## Editorial and listener findings

- Existing editorial gates remain: statements that two weeks determine the answer, that every occasional user has enough free capacity, that switching has little cost, and the quality recommendation above are not independently demonstrated facts. The brief retains superseded file-cap, Codex-only-on-Plus and annual-price wording; owner acceptance must use the corrected script. The brief was not changed.
- The opening says “只要三分鐘”, but lint estimates **8.3 minutes** and the user-type decision section starts around **04:16**. This is a pacing/promise issue, reported for the owner rather than changed in a factual pass.
- The long narration lines remain `g5f8` and `kax6` (>40 characters). No narration URLs or parenthetical expressions were found. Lint reports no unregistered pronunciation tokens. Reveal timing, audio intelligibility and rendered layout still require production checks.
- The first-round report's Flash 3.8 promotion expiry paragraph belongs to the separate API-price film; this plans script contains no such promotion. It is not evidence for this video.

## Validation and conclusion

`node tools/video/cli.mjs lint --slug free-vs-paid-ai-plans-2026` exited **0**, with **0 errors and 0 warnings**; 102 lines, 1,888 spoken units, estimated 8.3 minutes. No generation or paid service was called.

18 claim groups reviewed: **11 confirmed**, **5 not found** (four safely removed; CTA still unresolved), **2 editorial/out of scope**, **0 newly changed fact groups**. The mandatory independent second round is fulfilled for the first-round fact changes; no additional round is triggered by edits in this review. This does **not** make the script unconditionally verified while the CTA and owner/editorial gates remain unresolved.

All prices, access rules and plan limits are a **2026-09-29 snapshot** and must be rechecked before narration/publication. No fixed future validity is promised. Final media, captions, language selection, owner approval and actual publication are still separate unfinished steps.

External evidence: `C:/Users/x8120/.codex/tmp/p1-audit-20260929/plans-round2-extraction.json`, `video-source-http.json`, and relevant `round2-source-*.txt` captures. These are local review artifacts; no media, credentials or production records were added to the repository.

## Commit-byte receipt

Final `video.json` SHA-256 with repository LF line endings: `7124a51516a02ee92f30b17980542d2e18cca88e8f05dd3908aadf98659f7b42`. Use this final hash for handoff and invalidate any older media/approval bound to a different script.
