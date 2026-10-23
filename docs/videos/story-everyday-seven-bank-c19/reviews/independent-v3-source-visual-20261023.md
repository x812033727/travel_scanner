# C19 Seven Bank v3 — independent full source and paired-visual audit

**Result: HOLD, 77/79 narration-source rows PASS and 78/79 standalone visual-plan rows PASS; 79/79 structural pairing PASS.** This is an independent review of the exact author PR #1742 commit ed2d5f5242475fa5dd571bd5dc9a2b4410b0e895, after the v3 reorder. The earlier v2 receipt was not reused. Review date: 2026-10-23 (Asia/Taipei). No image was generated; actual rendered images, TTS duration, finished illustration time share, listener blind reads, owner script approval, cost approval, import, upload and publication are separate gates.

## Frozen inputs

SHA-256 below is of each Git blob's bytes at ed2d5f5242475fa5dd571bd5dc9a2b4410b0e895, computed from git show HEAD:path in a clean sparse worktree.

| File within docs/videos/story-everyday-seven-bank-c19/ | SHA-256 |
| --- | --- |
| script.md | 68EE62A86E23199CB29CEE484587F50E2EB3AD89C7501319F81EAC9C047146A1 |
| script-source-notes.md | 43AAC856B4ADC4E56C4E6F0BAF1FDD40C2ED550D8D9E17C2651D4B8B05280E10 |
| visual-plan.md | 0A0C9535AAC21C43980B1D4AD705502FA4FADCEADB428FD871EE8C8F0854C57E |
| visual-plan.json | 039CB84B7F306C0584E73F98F013DB09BF770F1F052206E45A136F59873C04AA |

## Primary source key and exact checks

- **S1** — [Seven Bank, ATM 20th-anniversary chronology](https://www.sevenbank.co.jp/corp/company/atm-history.html): 1987 utility-bill collection and recurring 10,000-person customer surveys under the 1987 entry; Sakura Bank/am/pm in March 1999 and E-net in October 1999; merchant-sales deposits in December 2001; 2005 second-generation machine purpose; 2007 overseas-issued card withdrawal and balance inquiry. This is the bank's retrospective, not a preserved 1987 questionnaire.
- **S2** — [Seven Bank, corporate history](https://www.sevenbank.co.jp/english/corp/company/history.html): preliminary license 2001-04-06, IY Bank established 04-10, operating license 04-25, banking/account applications 05-07, ATM service 05-15, money transfers 06-18; over 10,000 installed ATMs 2005-04-04, second-generation ATMs 07-26, formal rename 10-11; overseas-issued card service in July 2007 and all 47 prefectures reached 12-17. The separate dates matter.
- **S3** — [Seven Bank Annual Report 2010](https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2010092231.pdf): PDF p.10, “Services for Business Customers,” says deposited merchant proceeds can replenish ATM cash; PDF pp.12–15 list locations and the partner model; PDF p.13 says partner ATM screens match; PDF p.14 says partners set customer transaction fees, may lower their own maintenance/funding costs, and shows Seven Bank's ATM usage-fee path and 555 partners. The spread is dated “As of March 31, 2010” on PDF p.13; the separate location table on p.15 says June 30 and is not used to date the 555. PDF p.54 notes 18–19 give FY ended 2010-03-31 ATM-related fee income ¥85,294 million and ATM placement fee expense ¥9,003 million. PDF p.5 return-on-ATM-cash formula includes interest and administrative expenses, so neither figure is per-ATM profit.
- **S4** — [Seven Bank Integrated Report 2024](https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2024073101.pdf): PDF p.16 dates ATM Teller and ATM Notification launch to September 2023; note 1 defines account applications, registered-information changes and one-to-one information. The p.16 paragraph says 70% of ATM Teller transactions occurred when bank tellers were closed: the denominator is **ATM Teller transactions, not all ATM transactions or all +Connect activity**. PDF p.18 describes cash top-up and document-reading uses; its model calls top-up “basically free” to users and dates nine +Connect adopters to July 2024. The report describes the later counter-service motivation, not the 2001 founding decision.
- **S5** — [IY Bank 2005-06-03 name-change announcement](https://www.sevenbank.co.jp/corp/news/2005/060801.html): explains IY = Ito-Yokado group, Seven naming to evoke Seven-Eleven, 24/365 service and the new group name; the announcement projected October 11, while S2 verifies it actually happened then.
- **S6** — [IY Bank 2002 first disclosure magazine](https://www.sevenbank.co.jp/corp/disclosure/pdf/IYBank.pdf): PDF pp.2–3 says this is its first disclosure and separately defines the bank's own account/financial-services business and the ATM business serving other institutions' customers. It does not prove a management decision to reject a partner-operated ATM alternative.
- **S7** — [IY Bank 2001-11-09 deployment announcement](https://www.sevenbank.co.jp/corp/news/2001/1109_1.html): body paragraph 1 records 66 ATMs at 59 Tokyo 23-ward sites on May 15, over 1,000 by July 13, and roughly 16,000 opened accounts **in early November 2001**. Its headline and next paragraph project 2,005 machines for November 11; the script does not treat that future figure as achieved on November 9.

## Row-by-row verdict

“Image” means a proposed unbranded conceptual prompt only; “card” means controlled post-production text. PASS on a rhetorical/bridging row means it neither adds an unsupported empirical claim nor lets its paired image imply one. The source and visual columns were checked against the exact same ID in all four frozen files.

| ID | Narration/source check | Paired visual check | Result |
| --- | --- | --- | --- |
| c190101 | S1/S6 context; anonymous night-shop opening is an explicit concept, not a dated transaction. | Image: generic unmarked shop and ATM. | PASS |
| c190102 | S6 two-business structure permits a partner's card; no first-day or named-card claim. | Image: blank card and screen. | PASS |
| c190103 | S1/S6 question about partner access, no asserted internal motive. | Image: generic shop and distant anonymous bank. | PASS |
| c190104 | S2/S7 place formation/license before ATM start. | Image: closed blank folder and idle model, no premature result. | PASS |
| c190105 | S2/S5 support later 2005 threshold and name change. | Image: generic map and nameless folder, no future number revealed. | PASS |
| c190106 | S3 later-year fee model is clearly introduced as a later annual report. | Image: sealed fee envelope, no fee recipient revealed. | PASS |
| c190107 | S1/S2/S6 frame the supported central question. | Image: abstract links to unmarked institutions, no false literal network map. | PASS |
| c190201 | S1 1987 entry supports utility-bill collection, explicitly as retrospective. | Image: blank bill at fictional register. | PASS |
| c190202 | S1 says utility collection was usable outside bank hours. | Image: conceptual closed bank/open shop split. | PASS |
| c190203 | S1-derived editorial connection, no measured effect. | Image: blank bill beside goods. | PASS |
| c190204 | S1/S6 service contrast posed as a question, no universal no-ATM claim. | Image: empty conceptual shelf area, no real store record. | PASS |
| c190205 | S1 1987 entry reports recurring 10,000-person surveys and ATM requests high on the list; no rank or percentage is invented. | Image: blank opinions, no numeric poll result. | PASS |
| c190206 | S1 bill counter versus requested self-service ATM is an editorial transition. | Image: clearly separate register and idle model. | PASS |
| c190207 | S1 1999 entries disprove a convenience-store ATM first claim. | Image: two generic shops/machines, no brand identity. | PASS |
| c190208 | S1 March 1999 Sakura Bank/am/pm entry. | Card: says prior cooperation, does not claim firstness. | PASS |
| c190209 | S1 October 1999 E-net start. | Image: second unmarked map piece; no market-share suggestion. | PASS |
| c190210 | S1 two 1999 precedents support “not the invention.” | Image: later token placed after existing tokens. | PASS |
| c190211 | S1/S2/S6 support posing network-operator question; no claim that management rejected a partner ATM. | Image: generic shop model separated from network map. | PASS |
| c190212 | S2 dates 2001 licenses and subsequent ATM operation. | Image: idle model and blank date sheet. | PASS |
| c190213 | S2 supports the coming preliminary-license answer. | Image: unopened document, not a fabricated license facsimile. | PASS |
| c190301 | S2: preliminary license 2001-04-06. | Image: blank preliminary document, no official seal. | PASS |
| c190302 | S2: formation 04-10 and full banking license 04-25, correctly ordered. | Card: all three dates and license stages match S2. | PASS |
| c190303 | S5 says IY came from Ito-Yokado group; S2 places Seven rename in 2005. | Image: blank folder, no early Seven branding. | PASS |
| c190304 | S2: bank/account applications 05-07, ATM service 05-15. | Image: fictional account-document exchange, no real applicant. | PASS |
| c190305 | S2 separates bank opening from ATM activation. | Image: inactive generic machine, no simulated transaction. | PASS |
| c190306 | S7: 05-15, 66 machines, 59 sites, Tokyo 23 wards; machines and sites are not conflated. | Card: date, ward scope and two denominators exact. | PASS |
| c190307 | S2: money-transfer service began 06-18; S1's coarse May retrospective does not override precise history. | Image: generic symbol after blank date cards, no actual interface. | PASS |
| c190308 | S7 dated 11-09 retrospectively says 1,000 exceeded by 07-13; no use of November 11 projection. | Image: abstract map pieces, no invented location pattern. | PASS |
| c190309 | S7 paragraph 1: about 16,000 accounts in **early November 2001**, not year-end; ATM count and account count remain distinct. | Image: account folders beside map, no false numeric graph. | PASS |
| c190310 | S1 dates sales-proceeds deposit launch to **December 2001**; S3 p.10 is explicitly a later explanation of ATM cash replenishment. | Image: sealed sales box beside model, not a literal 2001 transaction. | PASS |
| c190311 | S6 pp.2–3 calls itself the first disclosure and separates two businesses. | Card: “2002 first disclosure, two businesses” is bounded. | PASS |
| c190312 | S6 p.2 defines own financial service versus ATM use for partner-institution customers. | Image: two distinct blank props. | PASS |
| c190313 | S6 supports the plain-language two-business summary, without a first-day partner count. | Image: blank card and institution folders. | PASS |
| c190314 | S7 initial Tokyo scope and S2 later scale make this a bounded question. | Image: small abstract Tokyo map, no real sites. | PASS |
| c190315 | S2 later 10,000-ATM threshold is only foreshadowed. | Image: unplaced tokens, no count displayed early. | PASS |
| c190401 | S2: installed ATMs exceeded 10,000 on 2005-04-04. | Card: identifies ATMs, not stores or transactions. | PASS |
| c190402 | S2 count unit supports the explicit denominator caution. | Image: separate machine/store tokens. | PASS |
| c190403 | S3 pp.10/54 and S1 2005 generation show cash logistics and maintenance are operating concerns; no per-site spend is stated. | Image: generic replenishment worker, no real route or bill. | PASS |
| c190404 | S1 2005 second-generation efficiency rationale; question adds no achieved-savings claim. | Image: old models and unopened new box. | PASS |
| c190405 | S2: second generation introduced 2005-07-26. | Image: original unbranded machine shell, no actual model copy. | PASS |
| c190406 | S1 2005 entry says larger/faster note-handling aimed to improve transport/transaction efficiency; explicitly attributed. | Image: conceptual cash boxes, no measured savings. | PASS |
| c190407 | S5 contemporaneous 2005 naming explanation; question does not impute founding motive. | Image: blank folders and generic shop. | PASS |
| c190408 | S2: formal Seven Bank name on 2005-10-11. | Card: year and old/new names correctly scoped. | PASS |
| c190409 | S5 announcement gives familiar store/group naming and 24/365 association; does not guarantee every machine never closes. | Image: generic shop, blank clock/calendar. | PASS |
| c190410 | S3 2010 p.12/15 shows later outside-group locations; wording does not date them to rename day. | Image: conceptual station machine, no real site. | PASS |
| c190411 | S1 2007 entry supports overseas-issued card withdrawals and balance inquiry; no “every foreign card” claim. | Image: anonymous traveler, blank card/screen. | PASS |
| c190412 | S2: all 47 prefectures reached 2007-12-17; no every-store inference. | Card: only 47 prefectures with sites. | PASS |
| c190413 | S3 pp.12/15 names stations and airports in 2010. | Image: anonymous station/airport pair, no real signage. | PASS |
| c190414 | S3 p.14 shows **555 partner financial institutions**, p.13 spread dates count to **2010-03-31**; not a 2024/current count. | Card: 2010-03 and 555 institutions, not machines. | PASS |
| c190501 | S3 p.14 says partners can reduce maintenance/funding costs versus owning their own ATMs; does not say this caused an individual partnership. | Image: two generic operating options, no contract outcome. | PASS |
| c190502 | S3 pp.13–14 says partner customers see the partner's same ATM screen. | Image: wholly blank screen; avoids replicating actual UI. | PASS |
| c190503 | S3 p.14 depicts distinct customer fee and network usage fee; question sets distinction. | Image: separate unmarked fee paper, no false payer arrow. | PASS |
| c190504 | S3 p.14 says the account-holding institution sets customer ATM transaction fees. | Image: blank price paper; no current or universal price. | PASS |
| c190505 | S3 p.14 diagram sends ATM usage fees from partner to Seven Bank. | Card: identifies payer but no contract price. | PASS |
| c190506 | S3 p.14 diagram separates the two fee paths; no assertion of equal amounts. | Image: two nonintersecting abstract routes. | PASS |
| c190507 | S3 p.14 permits fee-free customer use alongside partner network fees as a model; line says only that free-to-user does not prove no network income, not that every free transaction pays a fixed fee. | Image: blank screen and institution link, no fee amount. | PASS |
| c190508 | S3 p.14 does not itemize each contract's price; line is a limit on public evidence. | Image: closed blank contract folder. | PASS |
| c190509 | S3 p.54 annual aggregate introduced as a question. | Image: unopened blank annual-report folder. | PASS |
| c190510 | S3 p.54 note 18: ¥85,294 million = ¥852.94 億 ≈ ¥853 億 for year ended 2010-03-31. | Card: FY end and rounded amount correct. | PASS |
| c190511 | S3 p.54 calls the value fee income, not profit. | Image: separate income paper and ATM model. | PASS |
| c190512 | S3 p.10 explicitly says deposited merchant sales proceeds can replenish ATM cash; this is a **2010 operational description**, not a claim all 2001 sites did so. | Image: sealed proceeds box and abstract model connection, no actual logistics path. | PASS |
| c190513 | S3 p.54 note 19: ATM placement fee expense ¥9,003 million = ¥90.03 億 ≈ ¥90 億 for the same FY. | Card: same FY and expense description. | PASS |
| c190514 | S3 p.5/p.54 make subtraction insufficient for per-machine profit. | Image: unfinished blank calculation. | PASS |
| c190515 | S3 p.5 return formula includes interest and G&A beyond placement expenses; p.54 figures are aggregates. | Image: extra blank folders, no invented amounts. | PASS |
| c190516 | S3 p.54 reports annual totals, not per-machine P&L. | Image: annual report and separate blank ATM models. | PASS |
| c190517 | S4 p.16 later +Connect work began 2023, after 2010 section; no causal claim. | Image: generic service-window symbol beside ATM. | PASS |
| c190518 | S4 p.16 defines ATM Teller as counter-procedure channel, not total replacement. | Image: separate anonymous counter and ATM models. | PASS |
| c190601 | S4 p.16 dates ATM Teller and ATM Notification launches to 2023-09. | Image: blank partnership folder and ATM, no future rollout depiction. | PASS |
| c190602 | S4 p.16 note 1 permits account applications and registration changes at ATM Teller. | Image: blank application forms; no actual UI. | PASS |
| c190603 | S4 p.16 note 1 defines one-to-one ATM Notification; no response statistic or content invented. | Image: unmarked message symbol and blank screen. | PASS |
| c190604 | S4 p.18 describes later cash top-up for electronic money/QR-code payment accounts; wording says “by 2024 report,” not first launched then. | Image: generic payment prop and sealed cash envelope. | PASS |
| c190605 | S4 p.18 model calls top-up basically free to users, payment-company-set, distinct from bank-card ATM fee model. | Image: separate blank service cards, no universal free claim. | PASS |
| c190606 | S4 p.18 supports document-reading services; question explicitly resists every-machine coverage inference. | Card: 2024 report and service category, no universal availability. | PASS |
| c190607 | S4 p.16/p.18: **nine +Connect adopting banks as of July 2024**. After lines on cash top-up and document reading, the audible phrase “這組合作服務” does not identify +Connect and can transfer nine to those other services. | Card: “九家銀行採用” likewise omits +Connect scope; the 2024-07 date alone is insufficient. | HOLD |
| c190608 | S4 p.16 attributes declining branch-counter availability and daily-use ATM rationale to bank's 2024 description; no backdating to 2001. | Image: generic closed bank counter and lit shop ATM. | PASS |
| c190609 | S4 p.16: **70% of ATM Teller procedure transactions** outside bank-teller hours in that report. The spoken “這類辦事交易” follows several newer functions and does not itself pin the ATM Teller denominator; a viewer could hear all +Connect or all ATM procedures. | Image itself is safe: night shop and closed bank, no percentage chart. The paired line remains on HOLD. | HOLD |
| c190610 | S2 licenses/start dates, S6 two-business model and S7 first rollout support direct answer; no unsupported “why not partner ATM” reason. | Image: abstract institution links, no real network map. | PASS |
| c190611 | Editorial comment question tied to cross-institution service, no new factual claim. | Image: generic machine and abstract links. | PASS |
| c190612 | Editorial subscription request, no factual next-episode promise. | Image: generic closing scene, no channel copy inside generated image. | PASS |

## Visual and workflow checks

- Exact ordered ID sets, narration and author source text agree 79/79 across script, source notes and visual JSON. Visual-plan Markdown type/text agrees with JSON kind/prompt or card_text 79/79. JSON has 66 image shots and 13 cards; maximum consecutive cards is 2. Look preset is exactly cute-mystery; image model is image-01. Intro follows c190107 for 5 seconds; 21-second v4 outro follows c190612.
- Text-only prompt audit: no brand/logo/trademark, real person, real bank-card design, real ATM interface, report facsimile, readable generated text, real mapped site, or invented visual causal arrow was found. Cards supply dates/brand/numbers as post-production type and stay within the voiced fact. This is a plan audit, not a pass on pixels that do not yet exist.
- The script and notes preserve the key temporal boundary: 1987/1999 retrospective context, 2001 bank and first deployment, 2002 business disclosure, 2005/2007 expansion, 2010 model and FY figures, 2023–24 newer features. The 2001 notice's November 11 forecast was excluded. Two 2024 spoken labels still need tightening as specified below.
- No paid media request, TTS, import, upload, merge, or publication was run. Actual narration >=480 seconds and finished image time >=70% remain unmeasured.

## HOLD and narrow author-facing repairs

1. **c190607 narration and post-production card:** name the specific **+Connect** adopter scope in the spoken sentence and card. The 2024 report says nine banks had adopted +Connect by July 2024, not that nine had adopted every cash-top-up, identity-reading or other ATM function. A narrow option is: “到二〇二四年七月，報告說，採用 +Connect 這組合作服務的銀行有九家；這是當時的合作數，不是每台功能清單。” Card option: “2024-07 · +Connect 採用銀行 9 家（當時）”. Preserve the report's distinction between +Connect adoption and each bank's enabled functions.
2. **c190609 narration:** name the **ATM Teller / ATM 櫃員服務** transaction denominator in the spoken sentence. A narrow option is: “公司在二〇二四年報裡說，ATM 櫃員服務的辦事交易約七成發生在銀行櫃台關門後；最初那個時間差，還在。” The existing generic image is acceptable. Avoid substituting “全網 ATM 交易” or Notification response rate; the latter is a separate 70–80% figure on the same PDF page.

The independent reviewer did not change the author branch. Recheck the final wording and paired card after an author revision; this receipt is tied to the four frozen blobs above and is not approval of a later revision.

## Reproducible local checks

- Frozen Git blobs: four SHA-256 values above matched exactly.
- Structural comparison: 79 unique ordered IDs in each of script, notes, visual Markdown and JSON; narration/source fields match; MD visual type and prompt/card text match JSON; 66/13 kinds; maximum card run 2.
- npm run check:tasks: exit 0, “Validated 2077 task file(s).” Existing unrelated stale-claim/overlap warnings did not fail the check. The fresh worktree has only committed author-head files, so an author's untracked done-task duplicate was not part of this result.
- git diff --check: pending after this receipt is added.
