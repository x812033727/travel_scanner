# C19 Seven Bank v7 — independent source and visual review

**Decision: HOLD.** Reviewed the committed `e7afac6d94cb13b733c6040a471840c9c949e931` version of `script.md`, `script-source-notes.md`, `source-matrix.md`, `visual-plan.md`, and `visual-plan.json` only. There are 81 narration lines and 81 paired visuals. Three line-level gates remain: `c190310` source scope, `c190311` visual disclosure timing, and `c190517` visual machine identity. All other lines pass the source and visual tests stated here. This is not a narrative blind read or owner approval, and it does not authorize media generation.

## Bound inputs and mechanical checks

| File | SHA-256 |
| --- | --- |
| `script.md` | `C27DC1BEF9644CE557E590355FDFA79F8D820D908EB2FC6FD242801C54665350` |
| `script-source-notes.md` | `441932338DAEEC8A17387A5458C21707E58BA3D406F5996D0D05CD2096BE20CE` |
| `source-matrix.md` | `F343DE27FD24573C61BA6F5DACC87450B9338ECF454EE7801BA26AC3C7605442` |
| `visual-plan.md` | `6D59D136EBED2584AC6E26207BB547CF312F49F5EEEFD94B338729D46437DAA9` |
| `visual-plan.json` | `882C5BE5CC4D8F11374D84CF7ED5AB8D367598718A5898118267744F0758A6E2` |

The five working files had no diff from this commit at review time. I parsed the four line-bearing files independently: 81 unique IDs in identical order; narration and source tags match exactly across script, notes and JSON; all 70 image prompts and 11 `card_text` values match the Markdown plan exactly. JSON declares `look: {"preset":"cute-mystery"}`, `image_model: "MiniMax image-01"`, 5-second intro after `c190107`, and 21-second v4 outro after `c190612`. The prompts use generic, unbranded props and avoid readable in-image text, real ATM UI, photographs, and purported transaction records. Counts alone cannot certify the 70% *screen time* gate or actual TTS length.

## Original publisher sources read for this review

- **A** — [Seven Bank ATM 20-year chronology](https://www.sevenbank.co.jp/corp/company/atm-history.html), 1987 utility-bill collection and survey; 1999 Sakura Bank/am/pm and E-net precedents; 2001 December sales-proceeds deposits; 2005 second-generation ATM; 2007 overseas-issued card service. This is a later company retrospective.
- **B** — [Seven Bank corporate history](https://www.sevenbank.co.jp/english/corp/company/history.html), 2001, 2005 and 2007 rows. The 2001 dates are April 6 preliminary licence, April 10 incorporation, April 25 business licence, May 7 opening/account applications, and May 15 ATM service. The 2005 10,000 figure is installed ATMs; the 2007 47 figure is prefectures with installations.
- **C** — [IY Bank's November 9, 2001 ATM announcement](https://www.sevenbank.co.jp/corp/news/2001/1109_1.html), main paragraph. It records May 15's 59 Tokyo-23-ward locations/66 ATMs, July 13's already-achieved 1,000 ATMs, and about 16,000 accounts in early November. Its November 11 figure is a forecast, unused here.
- **D** — [IY Bank Disclosure 2002](https://www.sevenbank.co.jp/corp/disclosure/pdf/IYBank.pdf), PDF pp.2–3 and 5–6, especially the separate `金融サービス事業` and `ATM事業` descriptions and early chronology. It does not establish a decision to reject a different corporate structure.
- **E** — [Seven Bank Annual Report 2010](https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2010092231.pdf), PDF pp.10–15, 19–20, 35, 38, 42, 54 and 57. The customer transaction fee is set by the account-holding bank; Seven Bank's ATM usage fee flows from the partner. PDF p.35 states 555 business partners **as of March 31, 2010** (not 555 banks: 97 were banks). PDF p.19 places transaction relay systems in Yokohama and Osaka; p.20 places 24-hour support centres in Tokyo and Osaka and gives the cash-funding/replenishment tradeoff, nearby-business deposits **into the bank's ATMs**, and 1.7 monthly replenishments per ATM as a network metric. PDF p.54 reports FY ended March 31, 2010 ATM-related fee income of ¥85,294 million and ATM-placement fee expense of ¥9,003 million. The latter is not total cost or per-ATM profit.
- **F** — [IY Bank Disclosure 2005](https://www.sevenbank.co.jp/corp/disclosure/pdf/2005_all.pdf), PDF p.25 (printed p.25), `ATM事業の状況`, specifically lines following the 2004 ATM usage paragraph. It explicitly distinguishes **Seven-Eleven-store sales-proceeds deposits started December 2001** from **general-business-company sales-proceeds deposits started FY2003**. This narrows the broader wording of A's retrospective.

## Blocking findings and safe bounds

1. **`c190310` narration/source — HOLD.** 「十二月，銀行開始提供企業營業款入金」 reads as a general-company service in 2001. A confirms a December 2001 sales-proceeds service, but F p.25 says it was **for Seven-Eleven stores**, while the general-business service began in FY2003; D p.4 also describes the general-business service as prospective. Safe bound: say that December 2001 brought sales-proceeds deposits **for Seven-Eleven stores**. If showing cash entering an ATM, describe only a deposit service; neither A, D nor E proves the same deposited banknotes moved directly into the withdrawal cassette. Add F and the two start scopes to the source notes/matrix. The current generic store/ATM image is acceptable once the narration is narrowed.
2. **`c190311` visual — HOLD.** The narration says only that the first disclosure divided work into two lines. Its card names those two lines — 「自家存戶與合作 ATM 網兩門業務」 — before `c190312` narrates them. The visual plan's own rule says a visual should only depict the current line and not reveal the following one. Safe bound: make the `c190311` card read only `2002 · 首次揭露誌` (or a blank disclosure-book image); reserve the two-business explanation for `c190312`.
3. **`c190517` visual — HOLD.** The prompt places a store employee's sales box at a generic 「存款機」. E p.20 specifically describes nearby stores and businesses depositing into **Seven Bank ATMs**. The isolated deposit-machine wording can suggest another device and weakens the mechanism being explained. Safe bound: use a generic, unbranded **ATM deposit opening** in this prompt, as in `c190310`/`c190605`, with no implication that deposited notes feed its withdrawal cassette. Narration itself passes.

## Every line: source / visual decision

`PASS/PASS` means the narration stays within the cited source or is clearly a conceptual question/editorial bridge, and the paired visual has no material source or narration contradiction. `HOLD/PASS` and `PASS/HOLD` isolate the gate. Source letters refer to the original URLs and exact sections above; `concept` denotes an explicitly hypothetical, unmeasured scene or call to action.

| ID | Source / visual | Evidence and boundary |
| --- | --- | --- |
| c190101 | PASS/PASS | A 1987/ATM-demand context; concept night customer, no transaction claim. |
| c190102 | PASS/PASS | D ATM partners; E pp.13–14; concept other-bank card. |
| c190103 | PASS/PASS | D ATM business; E pp.13–14; condition is a question, no universal card acceptance. |
| c190104 | PASS/PASS | E pp.19–20 relay and cash management; concept, no actual card route. |
| c190105 | PASS/PASS | E p.20 insufficient-cash outage risk; explicit hypothetical. |
| c190106 | PASS/PASS | E pp.13–14 free-to-customer possibility and distinct fees; hypothetical. |
| c190107 | PASS/PASS | D ATM business; E pp.13–14; series question, no outcome. |
| c190201 | PASS/PASS | A 1987 register service; concept present-day shop. |
| c190202 | PASS/PASS | A 1987 utility-bill collection; attributed company retrospect, no first-ever claim. |
| c190203 | PASS/PASS | A 1987 after-hours premise; editorial connection. |
| c190204 | PASS/PASS | A register service versus ATM demand; concept customer's goal. |
| c190205 | PASS/PASS | A annual 10,000-person survey retrospective; no vote count/rank invented. |
| c190206 | PASS/PASS | D ATM business and E pp.10, 14; editorial difficulty, not attributed quotation. |
| c190207 | PASS/PASS | A 1999 convenience-store ATM precedents. |
| c190208 | PASS/PASS | A 1999 March Sakura Bank/am/pm and October E-net; card dates/names match. |
| c190211 | PASS/PASS | D and E pp.13–14 partner-card model; concept. |
| c190212 | PASS/PASS | D and E pp.13–14; editorial need for operating network, no rejected-alternative claim. |
| c190213 | PASS/PASS | B 2001 incorporation/launch dates; document is conceptual. |
| c190301 | PASS/PASS | B April 6 preliminary licence. |
| c190302 | PASS/PASS | B April 10 incorporation, April 25 banking licence; card also repeats prior April 6. |
| c190303 | PASS/PASS | B April 10 precedes May 15; inactive ATM is conceptual. |
| c190304 | PASS/PASS | B/C May 7 operations/account applications. |
| c190305 | PASS/PASS | B/C May 7 to May 15 = eight days. |
| c190306 | PASS/PASS | C May 15: 59 locations, 66 ATM units, Tokyo 23 wards; card units correct. |
| c190307 | PASS/PASS | C initial Tokyo-only locations; imagined outside customer. |
| c190308 | PASS/PASS | C July 13 already exceeded 1,000 installed ATMs; blank map not actual siting. |
| c190309 | PASS/PASS | C about 16,000 accounts in early November; line does not convert it to year-end. |
| c190310 | **HOLD/PASS** | A December deposit service; F p.25 limits 2001 to Seven-Eleven stores, general companies FY2003. |
| c190311 | **PASS/HOLD** | D first 2002 disclosure; card exposes the content reserved for c190312. |
| c190312 | PASS/PASS | D pp.2–3 expressly separates own-account financial services and partner ATM business. |
| c190313 | PASS/PASS | D and E pp.13–14; conditionally usable partner card, no acceptance result. |
| c190314 | PASS/PASS | C expansion after 59 points; D p.4 partner and area expansion. |
| c190315 | PASS/PASS | B licence/ATM dates and E p.20 operational work; editorial bridge. |
| c190401 | PASS/PASS | B April 4, 2005 >10,000 **installed ATM units**, correctly labelled on card. |
| c190402 | PASS/PASS | E p.20 replenishment work; no specific cash route. |
| c190403 | PASS/PASS | E p.20 cash/maintenance work; not asserted as a 2005 unit-by-unit record. |
| c190404 | PASS/PASS | E p.20 outage risk; hypothetical machine, no claimed incident. |
| c190405 | PASS/PASS | B July 26, 2005 second generation; generic design. |
| c190406 | PASS/PASS | A 2005 higher-capacity/faster note processing and intended logistics/transaction efficiency. |
| c190407 | PASS/PASS | A 2005 machine versus 2007 overseas-card chronology; no card accepted on screen. |
| c190408 | PASS/PASS | B October 11, 2005 name change; card does not imply creation then. |
| c190409 | PASS/PASS | A 2007 overseas-issued cards; visual avoids suggesting 2005 operation. |
| c190410 | PASS/PASS | E pp.12, 15 later non-store locations; blank station model is a conceptual example. |
| c190411 | PASS/PASS | A 2007 overseas-issued-card withdrawals/balance inquiries; not every card guaranteed. |
| c190412 | PASS/PASS | B December 17, 2007 installation in all 47 prefectures, not every store. |
| c190413 | PASS/PASS | E pp.12, 15 2010 stations and airports; no real location reconstructed. |
| c190414 | PASS/PASS | E p.35 555 **financial-institution partners at 2010-03-31**; p.35 includes 97 banks, so “many banks” is supportable but 555 must not be called banks. |
| c190415 | PASS/PASS | E p.20 Tokyo/Osaka support-centre monitoring and inquiries; no actual interface drawn. |
| c190416 | PASS/PASS | E p.20 remote handling and coordination with security/maintenance; concept, no incident. |
| c190417 | PASS/PASS | E p.20 cash shortage, breakdowns, checks/replenishment and per-ATM trend analysis. |
| c190418 | PASS/PASS | E pp.19–20 goal of reduced stoppage; no guarantee of one unit's uptime. |
| c190501 | PASS/PASS | E p.14 comparative partner maintenance/funding cost statement, not each partner's decision. |
| c190502 | PASS/PASS | E pp.13–14 partner-style screen; blank image deliberately avoids authentic UI. |
| c190503 | PASS/PASS | E p.14 shared-network cost comparison; editorial, not quantified saving. |
| c190504 | PASS/PASS | E p.14 account-holding bank sets customer transaction fees. |
| c190505 | PASS/PASS | E p.14 separate partner-to-Seven-Bank ATM usage fee. |
| c190506 | PASS/PASS | E p.14 separates fee directions; no equality asserted. |
| c190507 | PASS/PASS | E pp.13–14 free customer ATM fee does not imply zero aggregate network income; no per-transaction promise. |
| c190508 | PASS/PASS | E pp.14, 54 show model and aggregate, not partner contract rates. |
| c190509 | PASS/PASS | E p.14 partner network; editorial inference. |
| c190510 | PASS/PASS | E p.54 ¥85,294 million = ¥852.94 **hundred million**, rounds to ¥853 億, FY ended 2010-03. |
| c190511 | PASS/PASS | E p.54 annual aggregate, not a single transaction or ATM. |
| c190512 | PASS/PASS | E p.20 more cash lowers replenishment frequency but raises funding costs. |
| c190513 | PASS/PASS | E p.20 less cash raises replenishment and outsourced service costs. |
| c190514 | PASS/PASS | E p.54 ¥9,003 million = ¥90.03 億 placement-fee **expense**, not total costs. |
| c190515 | PASS/PASS | E pp.38, 42, 54 interest/admin and other expenses; subtraction is not per-unit profit. |
| c190516 | PASS/PASS | E p.20 per-unit usage trends/cash tradeoff; no actual stock rule. |
| c190517 | **PASS/HOLD** | E p.20 nearby stores/businesses deposit sales proceeds into Seven Bank ATMs; prompt says an unspecified deposit machine. |
| c190518 | PASS/PASS | E p.20 network cash-management objective; question and separate boxes avoid direct cassette transfer. |
| c190601 | PASS/PASS | E pp.13–14, 19; card stays uninserted, no transaction outcome. |
| c190602 | PASS/PASS | E p.19 Yokohama/Osaka relay systems, not support-centre cities; abstract diagram only. |
| c190603 | PASS/PASS | E p.19 both relay systems operational with capacity to take all if other down; no switch event claimed. |
| c190604 | PASS/PASS | E pp.19–20 digital relay versus physical cash handling; no wire-carried notes. |
| c190605 | PASS/PASS | E p.20 nearby sales deposits into ATMs as network cash management; no direct cassette claim. |
| c190606 | PASS/PASS | E p.20 says nothing about this machine's banknote origin; line correctly refuses that inference. |
| c190607 | PASS/PASS | E p.20 1.7 replenishments per ATM per month as 2010 network metric, not tonight's guarantee. |
| c190608 | PASS/PASS | D partner service and E pp.13–14, 19–20; conditions prevent universal acceptance claim. |
| c190609 | PASS/PASS | E p.19 bank-system connection; conceptual shop, no particular transaction. |
| c190610 | PASS/PASS | D two businesses and E pp.13–14, 19 partner-network extension; no actual card result. |
| c190611 | PASS/PASS | Conceptual audience question; generic everyday machine. |
| c190612 | PASS/PASS | Series call to action; generic closing visual. |

**No historical “first convenience-store ATM”, no real card acceptance/rejection, no fee equality, no 2010 expense-as-profit, no cash-through-network-cable, and no deposited-note-to-withdrawal-cassette mechanism were found in the other paired lines.**
