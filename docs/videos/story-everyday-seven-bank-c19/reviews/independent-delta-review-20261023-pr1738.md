# C19 Seven Bank — independent delta review (2026-10-23)

**Verdict: PASS for prior HOLD T01 and T02.** This is a narrow recheck of the changed Treatment against [the prior independent review PR #1736](https://github.com/x812033727/travel_scanner/pull/1736), not a fresh script approval or owner adoption. I reopened the relevant issuer originals and compared the old and new Git blobs; `source-matrix.md` did not change.

## Exact target and integrity

- Author [PR #1716](https://github.com/x812033727/travel_scanner/pull/1716): new head `68bcebdaeb2555bd9f01fe844f129cc775f6092e`, draft with `no-auto-merge` at review time. Previous reviewed head: `cd18d50385ac712a1d8e4b463bdf0c080be5a129`.
- New `treatment.md`: Git blob `ae5db3ce337dba70da3e86054e30ba7825d887a4`; SHA-256 of exact Git blob bytes `9ccbe39e4d56cd02275dc2863320764007604152ef9722097180337159aa3415`. Previous blob was `4ad76ce307ebb53b63b8512d85f163b73401df33`.
- Unchanged `source-matrix.md`: Git blob `22dec9f630cc22bb07c03fe7026e50da55df8fa8`; SHA-256 of exact Git blob bytes `1f4647d2dc177dcf687eb4193b1a1568aac8d6d5f27dee8ff504221720f6b509`.
- Author diff: only `treatment.md`, 9 additions and 9 deletions. This receipt applies only to the new exact head and these two file bytes.

## Holds rechecked

| Prior hold | New wording and primary-source test | Verdict |
| --- | --- | --- |
| **T01 — comparative bank-license motive** | Lines 7, 11, 16 and 26–28 now ask how ATM demand developed into the bank's own-account and partner-ATM businesses, and chapter 2 asks what the bank did after formation. They no longer promise to explain why a partner or joint ATM operator was rejected. [IY Bank's 2002 first disclosure, pp. 2 and 7](https://www.sevenbank.co.jp/corp/disclosure/pdf/IYBank.pdf) directly names both businesses, while [Seven Bank's anniversary account](https://www.sevenbank.co.jp/corp/company/atm-history.html) attributes the founding broadly to customer demand. The chapter 3 caveat still says the disclosure cannot establish the internal alternative-choice rationale. | **PASS** |
| **T02 — backdated fee-driven expansion** | Line 8 now states the 2001 first 66 ATMs, expansion of locations and partners, 2005/2007 milestones, then the **2010** fee income/placement cost example. Chapter 5 uses the same sequence. The [2001 IY Bank release](https://www.sevenbank.co.jp/corp/news/2001/1109_1.html) links partner growth with wider ATM installation without claiming fee funding; [the official history](https://www.sevenbank.co.jp/english/corp/company/history.html) dates the milestones; [Annual Report 2010, financial note 18–19](https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2010092231.pdf) supplies the later fee and placement figures. No remaining sentence says 2010 fees caused or financed 2001–2007 growth. | **PASS** |

## Residual boundaries and presentation

- The 1987 utility-bill service and recurring ATM request remain **issuer retrospective context**, not proof that any individual store ATM caused customer growth. The Treatment still avoids a measured customer-growth claim.
- The official history dates company establishment and banking license in April 2001 before the first 66 ATMs began on May 15; the new opening and chapter 3 preserve that order. The 2002 disclosure concerns own ordinary-deposit account services plus partner access, not a claim that consumer loans launched in 2001.
- The 2010 financial example remains explicitly dated, and the Treatment warns that fee income less ATM placement expense is not per-machine profit. Partner-card customer charges remain distinct from fees paid to Seven Bank.
- The revised thumbnail question, “店裡，還有銀行？”, removes the old false either/or and keeps model prompts generic and free of actual marks or reconstructed historic scenes.
- **Nonblocking title edit:** Title option ② at line 11, “從 66 台提款機，走到一家銀行的日常生意”, could be heard as the ATMs preceding the bank, and “提款機” hides the deposit side. If selected, “一家新銀行，如何從 66 台 ATM 起步？” preserves the documented order and service scope. The body and opening state the chronology correctly, so this is a wording suggestion, not a new HOLD.

**Gate:** The two previously held source-to-story points are resolved for these exact blobs. The owner's Treatment adoption, script-level sentence verification, media spend, QA, import, and upload are separate pending decisions.
