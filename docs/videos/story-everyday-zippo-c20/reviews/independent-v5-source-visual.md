# C20 Zippo v5 — independent full source and paired-visual audit

Reviewed 2026-10-23 (Taipei). **HOLD: spoken 59 PASS / 1 HOLD; paired visuals 56 PASS / 4 HOLD.** This is a review of author draft PR [#1728](https://github.com/x812033727/travel_scanner/pull/1728) at exact commit `836e2c8c1bf2d0f72e320892a2ddd50638d4088b`. The earlier v4 verdict does not transfer. No author text was changed by this review.

## Bound inputs and parity

| Author file | SHA-256 |
| --- | --- |
| `script.md` | `CFDD9230E5D44C645D800EE6B35F3E72C083CC4CA7737B0ABDB434B413B423BB` |
| `script-source-notes.md` | `2958CAFFF2B0C1C55DADFDC9383B7D6E7A65CEF4F78A8ED553C28EA4F0559179` |
| `visual-plan.md` | `451B1E58A03F9DE99735DB97BD4616D6946B85C1BCA698B1C9004E4D6EAEBD03` |
| `visual-plan.json` | `3CC77E415E963542073197462F06E66ADC4C0467331AE330A42070EA9A610902` |

Independent row comparison found **60 spoken rows, 60 source-note IDs, 60 visual Markdown rows, and 60 JSON shots**, in the same ID order. JSON narration and source tags match the script, and JSON image `prompt` / card `card_text` matches the visual Markdown text. Counts are 53 images and 7 cards. JSON `look` is exactly `{"preset":"cute-mystery"}`; the stated 5-second opening follows `c200107` and the existing 21-second closing follows `c200610`. This establishes text parity only; no TTS duration, rendered-image suitability, or 70% image-time result has been measured.

## Primary evidence reopened

| Code | Primary source and scope |
| --- | --- |
| H | Zippo [company history](https://kb.zippo.com/the-history-of-zippo), especially its retrospective 1930s origin, 1933 product/US$1.95/guarantee, and patent paragraphs; Zippo's [600-millionth page](https://zippo.com/pages/600-millionth-zippo-lighter) separates 1932 founding from 1933 first lighter. These are later company accounts, not 1933 witness records. |
| P | [US patent 2,032,695 original scan](https://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf): filed 1934-05-17, issued 1936-03-03, two named inventors, telescoping insert/case, hinge, windscreen, wheel/flint, fewer protrusions. The patent does not show an actual historic repair procedure. |
| D | Zippo [date-code knowledge-base page](https://kb.zippo.com/zippo-lighter/date-codes): mid-1950s start for quality control and identifying patterns in returned batches; later useful to collectors; earlier products cannot be assigned the later code format. |
| US | Zippo US [warranty and repair](https://kb.zippo.com/warranty-repair), [not lighting](https://kb.zippo.com/zippo-lighter/not-lighting), [broken hinge](https://kb.zippo.com/zippo-lighter/hinge-broke), and [worn decoration](https://kb.zippo.com/zippo-lighter/worn-deco). The [US pocket-lighter instruction sheet](https://productinstructions.zippo.com/Documents/English_USA/01_Windproof_Lighters/01_Windproof_Instructions_EN.pdf) says the factory restores first-class mechanical condition, while finish is outside the guarantee. Its direct PDF fetch timed out in this pass; the directly readable knowledge-base pages independently support the relevant boundaries. |
| UK | Zippo UK's current [windproof-lighter repair page](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter): case-only repair excludes the insert; inside units normally get a new replacement and the old unit is returned only if requested on the form; UK customers use insured, trackable shipping to the stated receiving point before transfer to the European repair clinic. This is **UK-specific**. |
| A | Zippo US [Double Arc repair FAQ](https://kb.zippo.com/arc-repair-faqs-and-guidance) gives a two-year warranty window. Zippo's [Double Arc product page](https://zippo.com/products/double-arc-rechargeable-insert) sells the insert separately and also states a two-year warranty. These are distinct from a traditional windproof insert and do not establish terms outside this US-facing material. |
| V | Repository [Curio episode image-prompt rule](../../../../.agents/skills/curio-episode/SKILL.md), §「插圖提示詞怎麼寫」, requires one person doing one action and warns against two or three people interacting in one MiniMax frame. The author visual-plan preface also disallows documentary-looking recreations, readable text, logos, real likenesses, smoking, and ignition instructions. |

The V path above is intended as a repository-relative reference to `.agents/skills/curio-episode/SKILL.md`; its specific rule is at lines 76–91. All current-policy claims below are limited to the cited market and product. Narrative questions and generic conceptual scenes were checked for the factual implication a viewer would actually take from the paired frame.

## Every line and paired frame

`S` is the spoken-claim verdict and `V` the visual/card verdict. The code column gives the primary evidence for the factual content; `concept` means an expressly anonymous illustrative scene or editorial inference bounded by the cited source. Each visual was checked against its paired line, not just its prompt alone.

| ID | Evidence and claim/depiction check | S | V |
| --- | --- | --- | --- |
| c200101 | US/UK; explicitly hypothetical, undiagnosed worn case | PASS | PASS |
| c200102 | H/US; traditional windproof lifetime function promise | PASS | PASS |
| c200103 | P/US/UK; separates visible finish, hinge, internal mechanism | PASS | PASS |
| c200104 | US; old finish alone is not a mechanical diagnosis | PASS | PASS |
| c200105 | P/UK; conditional retention/replacement question | PASS | PASS |
| c200107 | US/UK; asks function versus retention without asserting outcome | PASS | PASS |
| c200201 | H; expressly attributed later company recollection | PASS | **HOLD** |
| c200202 | H; windscreen and two-handed old design | PASS | PASS |
| c200203 | H; thin shell dent and pocket-use editorial inference | PASS | PASS |
| c200204 | H; attributed redesign with rectangular hinged case | PASS | PASS |
| c200205 | H; one-hand case opening, no ignition demonstration | PASS | PASS |
| c200206 | H; 1932 company founding versus 1933 first lighter | PASS | PASS |
| c200207 | H; 1933 US$1.95 and initial promise attributed to company | PASS | PASS |
| c200208 | H/US; future-repair promise as editorial interpretation | PASS | PASS |
| c200209 | H; generic counter, no claimed historical transaction | PASS | PASS |
| c200210 | P; conceptual transition to internal construction | PASS | PASS |
| c200211 | P; component overview | PASS | PASS |
| c200212 | P; patent as documentary construction source, blank prop | PASS | PASS |
| c200213 | P; poses the insert/case question | PASS | PASS |
| c200301 | P; exact filing month and two inventors, no assigned individual contribution | PASS | PASS |
| c200302 | P; 1936 grant and hinged lighter, factual postproduction card | PASS | PASS |
| c200303 | P; sliding insert and exterior case | PASS | PASS |
| c200304 | P; windscreen, wheel/flint and hinge; no operation shown | PASS | PASS |
| c200305 | P; fewer protrusions as design purpose, not tested performance | PASS | PASS |
| c200306 | P/UK; separable structure, no false completed repair | PASS | PASS |
| c200307 | P; exterior hinge versus insert location | PASS | PASS |
| c200308 | P; expressly rejects inference of historical repair method | PASS | PASS |
| c200309 | P/US/UK; distinct components and current failure categories | PASS | PASS |
| c200310 | P/D; conditional bridge to returned batches | PASS | PASS |
| c200311 | D; date codes start later and were not originally collector marks | PASS | PASS |
| c200401 | H/D; first promise predates mid-1950s codes | PASS | PASS |
| c200402 | D; start period and original quality-control purpose | PASS | PASS |
| c200403 | D; returned item's code can identify production batch | PASS | PASS |
| c200404 | D; conditional pattern-finding, no claim of a faulty real batch | PASS | PASS |
| c200405 | D/US; code is not a diagnostic verdict | PASS | PASS |
| c200406 | D; later collector use follows original factory use | PASS | **HOLD** |
| c200407 | D/US; code is not expiry; early item lacks modern format | PASS | PASS |
| c200408 | D/US; dating versus actual fault; no fabricated diagnosis | PASS | PASS |
| c200409 | P/UK/US; asks present-day component-flow question | PASS | PASS |
| c200501 | UK; market-scoped case/insert separation | PASS | PASS |
| c200502 | UK; case-only shipment excludes insert | PASS | PASS |
| c200503 | UK; normal insert replacement rather than internal repair | PASS | PASS |
| c200504 | UK; old insert return requires advance form note; explicitly UK only | PASS | PASS |
| c200505 | UK; conditional imagined old case/new mechanism, not proof of actual job | PASS | PASS |
| c200506 | H/P/UK; historical patent and modern UK process kept separate | PASS | PASS |
| c200507 | US; US traditional windproof mechanical coverage | PASS | PASS |
| c200508 | US; separates consumables from mechanical fault, without operating steps | PASS | PASS |
| c200509 | US; consumables not promised as lifetime free supply | PASS | PASS |
| c200510 | US; broken hinge is a covered mechanical issue | PASS | PASS |
| c200511 | US; decoration wear outside lifetime guarantee; US card labeled | PASS | PASS |
| c200512 | US; under-one-year customer contact is an option, not a free-refinish promise | PASS | PASS |
| c200513 | US; cosmetic-versus-mechanical editorial comparison | PASS | PASS |
| c200514 | UK; insured tracked shipping and two-stage routing limited to UK | PASS | PASS |
| c200515 | US/A; asks whether another insert inherits old guarantee | PASS | PASS |
| c200601 | A; separately sold Double Arc, US two-year repair rule stated orally | PASS | **HOLD** |
| c200602 | US/A; no automatic transfer of traditional guarantee | PASS | PASS |
| c200607 | US/UK/A; returns to unresolved hypothetical conventional case | PASS | PASS |
| c200608 | US/UK; US function/finish and UK insert outcome merged without market marker | **HOLD** | PASS |
| c200609 | Editorial audience question; no promise of a customer election in the words | PASS | **HOLD** |
| c200610 | Subscription invitation, no external factual claim | PASS | PASS |

## Holds and minimum repair directions

1. **Spoken `c200608` — market scope (US + UK).** The US pages establish mechanical function coverage and the finish exclusion; the [UK page](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter) establishes normal insert exchange and the limited old-insert return procedure. Saying a generic *today's lifetime promise* does not keep every original piece can make the UK workflow sound universal, especially in the direct answer to the episode's main question. Revise this one spoken sentence to label the jurisdictions explicitly, for example: 「終身免費修保住的是傳統防風款的機械功能；英國現行流程可能換掉內膽，美國終身保證也不涵蓋磨損的外觀。」 Retain the oral/main-question answer and its no-automatic-original-parts conclusion, with the UK example visibly scoped.
2. **Visual `c200201` — two fictional adults in one generated historical scene.** The [Curio image rule](../../../../.agents/skills/curio-episode/SKILL.md) requires one person doing one action and warns against two/three-person interaction. The [company history](https://kb.zippo.com/the-history-of-zippo) is retrospective; the picture must not imply a documented friend/Blaisdell likeness or an actual recorded meeting. Show one anonymous adult examining a generic awkward old lighter at a 1930s-style table. Keep the company-history attribution in the narration.
3. **Visual `c200406` — split frame with a worker and a collector.** The same one-person/one-action rule applies even when two people are placed on separate halves of a single generated shot. Show one anonymous collector examining an abstract bottom mark, with blank quality-control materials to suggest its earlier factory role. Do not add a second paid shot without a revised approved shot/cost plan.
4. **Card `c200601` — jurisdiction falls off the standalone card.** The [US Double Arc FAQ](https://kb.zippo.com/arc-repair-faqs-and-guidance) is the direct evidence for two years, and the oral line does say “美國維修說明”. The standalone visible card `Double Arc 內膽 · 兩年保固` does not. Use `美國站 Double Arc 內膽 · 兩年保固` (or equally explicit US marker) so the frame itself does not imply global terms.
5. **Visual `c200609` — an old and a new insert posed as two viewer choices.** The narration is an open values question. Beside it, an old/new insert arrangement with a hand between them can imply that a UK repair customer may elect either complete original-part preservation or replacement; the [UK process](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter) instead normally replaces inside units and only says the old insert can be returned on request. Keep a single worn generic case and one indistinct separated component, with one pensive anonymous viewer; remove the old/new alternatives and any implied guaranteed outcome.

`c200206` is supportable via the separate 1932/1933 company timeline already linked in `source-matrix.md`; `script-source-notes.md` could expose that exact link beside M01 for easier reviewer navigation, but this is nonblocking because the source matrix is present and the fact checks out. No alleged sales, profit, waste reduction, or historical repair method was introduced by the v5 narration. This verdict does not constitute owner script approval, paid generation approval, measured spoken duration, imported media QA, upload, or publication.
