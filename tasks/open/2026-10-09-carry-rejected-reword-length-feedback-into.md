---
id: 2026-10-09-carry-rejected-reword-length-feedback-into
title: Carry rejected reword length feedback into the remaining bounded round
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T19:23:31Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/automation.test.mjs
---

# Carry rejected reword length feedback into the remaining bounded round

## Why

Embedding English's genuine normal continuation rejected two translator:reword
proposals for4hdb:86 and108 Unicode characters against max_chars78. The first
rejected candidate and length reason were not included in the existing second
round's payload,so that round repeated the same failure. Both actual correction
requests are consumed and the locale genuinely reached SKIP. Preserve that result.
The remaining query's/queries comparison may be a homophone ambiguity; this ticket
does not establish an audible defect or authorize relaxing transcript matching.

## Definition of done

- [ ] An existing remaining reword round receives the same line's prior rejected
      candidate and explicit character-budget reason,and requests a checked fit.
- [ ] Oversize/changed-number answers still refuse without truncation or merge.
- [ ] The two-round cap,request identities,consumed decisions and genuine SKIP
      are preserved;no third model call or automatic redo of this delivered locale.

## Steps

- [ ] Add narrow per-line rejection feedback to the existing bounded second round.
- [ ] Verify invalid and valid answers through the ordinary merge/terminal flow.

## How to verify

Run focused automation tests with78 as the budget and86/108-character replies.
Both oversize proposals must refuse;an otherwise valid in-budget answer may merge.
Verify number preservation,unchanged round counts,no extra model submission and
unchanged genuine SKIP. Reuse the bundled Node runtime on Windows when necessary.

## Notes

Final native outcome remains three genuine SKIPs: EN has one automated flag,
JA five and KO one. Rejected number-changing or over-budget proposals were
not merged, all nine consumed model decisions remain counted, and no new round
was opened. These transcript flags do not establish owner-listened defects.
Repository rejection-feedback work remains unimplemented and unclaimed.


Actual English terminal f5e490fef169aba7f04f020d349367c2b849def928e843c13a137cd1fd2f0d57
and closure summary2f978629d118f9771d4b0d6c648980a1bf461735e4d2e3f7133cfddcbee86c81
are retained outside Git under mokaair-work/stalled-video-completion-20261008/
embedding-audio/listener-round2/selected-language-finishing-20261009.
Source inspection locates rewordDub in flow.mjs and TRANSLATOR_REWORD in prompts.mjs.
Existing2026-09-29 reword support and2026-10-07 outage round-refund tickets do not
cover this repeated oversize feedback. This is a follow-up only;no source change,
paid request,reopened round,manual transcript clearance or owner acceptance occurred.
