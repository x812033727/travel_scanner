---
id: 2026-09-28-ten-drama-plan-audit-findings
title: Resolve ten drama planning audit findings before production
status: review
priority: P2
area: docs
owner: codex-ten-drama
claimed_at: 2026-09-28T14:34:44Z
created_at: 2026-09-28T13:59:39Z
completed_at:
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - docs/videos/series-plans/binge-five-20260928
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Resolve ten drama planning audit findings before production

## Why

2026-09-28 audit of the current ten drama works found contradictions between
story rules, episode outlines, continuity notes and packaging. Both validators
pass, so their structural checks do not catch these editorial defects.

A read-only production snapshot at 2026-09-28T13:57:22Z confirmed all ten works
exist, each with six review documents. All sixty Markdown/structured document
bodies match this checkout. Every work is in setting, hands_off is false, and
the target episode/request/project/media-job counts are zero. These are current
plans awaiting review, not completed films. No production write was made.

## Definition of done

- [x] Resolve the confirmed story and packaging inconsistencies below in the
  editable sources, regenerate artifacts, and independently review changed stories.
- [x] Correct the production handoff instructions without implying hands_off is
  a generation or spending stop switch.
- [x] Preserve historical review receipts; obtain fresh source-bound receipts
  for any changed Codex story instead of relabeling old approvals.
- [x] Record local versus imported document versions. Updating production review
  documents is a separate authorized operation, not an automatic part of this fix.

## Steps

- [x] Reload: synchronize world rewind versus self-only rewind. Claude
  reload-first-day/setting.mjs:41 says the world resets and only the lead remembers;
  chapter-3.mjs:162,171 makes the ninth-floor rewind restore only her, while the
  villain remembers killing her. The ninth-floor exception must be explicit in
  setting.mjs:47 and appropriately established before its payoff.
- [x] Ghost: make the visibility rule coherent. Claude ghost-at-his-side/source.mjs:42
  grants shadow sight to life lenders, but Lu Zheng is a lender (:197,524) and is
  explicitly unable to see Qingyan (:329,533), only gaining sight at death (:762).
  Define an earned exception or align the scenes and continuity list (:975).
- [x] Ghost: preserve aged appearance. source.mjs:664 ages Lu Zheng ten years from
  the initial apparent age 51, but :761 restarts the final aging at 51. No intervening
  rejuvenation is specified. Also align the E18 lamp lighter: :557 says Wujiu
  (沈無咎), while the continuity note :977 assigns it to Qingyan.
- [x] Throne: resolve the same-note contradiction in Claude
  taste-of-the-throne/source.mjs:1440: require three knocks in E33, yet forbid
  anyone knocking three times after E30. The E33 scene itself includes the knocks (:1206).
- [x] Wedding: align the opening with E1 and props. Codex
  wedding-reckoning/source.mjs:541 tears an unsigned authorization page and keeps a
  complete copy; :565,596,610 stops signing and preserves the complete original.
  Packaging (:2886,2906) promises tearing. Specify which sheet is torn and which
  survives; do not let different writers infer incompatible versions.
- [x] Empress: correct packaging.md:22 claiming all officials eat disaster porridge.
  The E1 outline shows the heroine drinking and putting a bowl before the chancellor;
  source.mjs:605 explicitly says he does not take a bite. Change the promise or
  deliberately add and review the missing event.
- [x] Train: align packaging.md:15,25 literal ticket text with the actual clue.
  It says the ticket reads 還沒到站/尚未到站, while setting.md:24,26 and the opening
  rely on destination 17 versus platform stamp 04. Avoid generating a new prop inscription.
- [x] Correct remaining prose corruption: city-owes-a-light/source.mjs:1278
  送回撥度席 and :2804 33–34 整合立; seventh-passenger/source.mjs:1467 壓回撥查;
  remembered-by-rival/source.mjs:1010,1655 uses 程式 where 程序 is intended.
- [x] Correct reload-first-day/setting.mjs:19: 2026-02-11 is Wednesday, not Monday.
- [x] Correct Claude README.md:48: hands_off=false controls automatic approvals;
  a newly POSTed empty series can still trigger paid setting planning. README.md:49
  also describes PUT/edit_doc as importing into a fresh work, but the service requires
  an existing document. Refer to the reviewed importer workflow from PR #929 and
  distinguish its preloaded review documents from a plain create request.

## Second pass: additional confirmed findings

- [x] Before the Hammer: distinguish the original death date from the new
  timeline's accelerated danger. source.mjs:9 says she dies on release after
  three years in prison; E16 :777 still says three years, but :783,796 calls the
  original death night only 44 days away. E28 :1109,1122 calls the coming first
  day of the month the original death date, six days away. Rule :103 permits
  this life's events to accelerate, not retroactive changes to her memories;
  E18 :839 still says the letter arrived three years early. The season's
  90-day timeline (:1509) supplies no intervening three-year jump.
- [x] Three Needles: establish how the eleventh herb order becomes known.
  chapter-2.mjs:172,196 leaves the last two positions unknown and only the first
  ten established. E19-20 (:205-231) cover Huo's examination and finding Sisi,
  without acquiring another position. E20 carry :242 suddenly says eleven are
  known and only the last one is missing; chapter-3.mjs:8,43,56 inherits this.
- [x] Three Needles: chapter-3.mjs:9-10 says Huo collapses on day three, whereas
  setting.mjs:102, E28 (:181-182) and E30 (:226-227) require day four. Align the
  chapter summary with the scenes and fixed poisoning rule.
- [x] Three Needles: reconcile E21's duplicate versions of one event.
  chapter-3.mjs:19 describes the third needle, moving finger and monitor with
  Jiang Man saying the readings did not change; :23 describes the same beat
  with her saying they changed. The later rebuttal (:20,24) also relies on a
  recorded change. Do not leave the writer to select between conflicting fields;
  an explicitly staged transient response would need to be stated consistently.
- [x] Throne: align the opening's central rule. source.mjs:40 requires swallowing
  poison before reporting its name, but premise :8, cold_open :305 and E1
  :328,330 say the rule requires swallowing and staying silent. Explain whether
  naming the poison, naming its source, or speaking at all is prohibited.
- [x] Reconcile episode cast lists with visible action and dialogue. Ghost E36
  source.mjs:869-870 has Han Song enter and block arrows, but :876 omits him.
  E37 :884,888 has Han Song block arrows and Lao You replace oil and speak;
  :892 still lists only wujiu/qingyan/zongdan/aqi. Before the Hammer E20
  source.mjs:883-889 stages Shen Huaizhou and Zhao Ma in addition to the four
  listed at :898. Three Needles E40 chapter-4.mjs:227,229 stages Sisi speaking
  and A Dou present, while :239 omits both. These scenes require at least six
  named participants, conflicting with the authoring validator's 2-4 listed
  characters. Revise staging or deliberately review a larger cast; silently
  appending IDs will fail the current authoring limit.

The cast discrepancy reaches production: tools/video/automation/series.mjs:257
filters the episode brief using beats.characters. The writer also receives the
full series cast, so this is a contradictory contract and casting/budget risk,
not proof that generation must crash or that it can never recover the names.

Second-pass checks used the youtube-video workflow and dev-and-ci guidance for
isolated, offline reproductions. No source or generated artifact changed. The
previous validator results remain a structural baseline, not clearance of these
new semantic findings.

## Third pass: further confirmed findings

- [x] Reload E1: align character knowledge at the episode boundary.
  chapter-1.mjs:18 explicitly shows the panel saying a memory has been erased,
  after the lead notices she forgot her grandmother's birthday (:17). The carry
  at :26 still says she does not know memory is the cost. Distinguish knowing
  there is memory loss from later learning which memories the system selects.
- [x] Reload E2: align deaths, attempts and the packaging claim.
  chapter-1.mjs:30-31 says she dies three times entering the door. :33,36 shows
  two deaths followed by success on the third entry. packaging.mjs:29 explicitly
  promises three deaths on screen in episode 2; E1's earlier death cannot satisfy
  that episode-specific promise. Correct the count or stage the missing death.
- [x] Reload E27: distinguish what Shao Qing already knew from the new reveal.
  setting.mjs:42 says he stopped saving after seeing 6/7 in the fifth cycle.
  chapter-3.mjs:113-114 instead says that field is hidden from him and he has
  never seen the line; :117 builds the payoff around that ignorance. Knowing
  the count and not knowing the seventh save's penalty are compatible, but the
  current scene explicitly denies the former too.
- [x] Ghost: correct the key inscription's character count. source.mjs:572-573,
  581 set up four characters, :597 calls 借予沈無咎 four characters, and E27
  :714 explicitly says all four can now be read. 借予沈無咎 is five characters.
  Align the obstructed inscription shots, carries and spoken reveal together.

Lower-priority packaging/shot synchronization:

- [x] Throne thumbnail A source.mjs:1421 says 第一口有毒 while the same entry
  specifies the banquet's third mouthful; cold_open :307 explicitly says the
  first two had no detectable taste. Align thumbnail text with the promised shot.
- [x] Before the Hammer source.mjs:1471 promises the exact line
  這只盞是我簽的，也是假的 within 30 seconds. The 25-30 second cold_open at :355
  instead uses 我簽的時候，你就在旁邊 and cuts to black; the promised line is
  assigned to E1's cliffhanger. Align the timing promise and opening plan.
- [x] Three Needles packaging.mjs:19 places all three needles in the old man's
  wrist, while setting.mjs:414 places the second needle at the chest. This is a
  fictional shot-layout consistency issue, not a medical accuracy assessment.

Third-pass coverage: two reviewers checked Reload and Ghost's 80 complete
episodes and the ten works' mysteries, chapter summaries, openings, endings and
packaging. No additional high-confidence cross-document contradiction was found
in the five Codex works. A reveal schedule's final proof was not treated as the
first mention of a clue.

Excluded from confirmed findings: Lao Deng's appearance at the fifth-floor
entrance does not prove qualification by crossing its summit; Shao Qing's
tattoo may be reapplied in different cycles, so its reset is not a proved error.
Ghost's blood-written farewell charm versus the borrowed-life restriction needs
an explicit mechanism clarification (source.mjs:38,588,821,825), but the later
scene deliberately uses it to infer surviving native life; do not claim a
confirmed extra power without resolving that intended exception.

## How to verify

Run both read-only validators and their existing regression suites:

```text
node docs/videos/series-plans/binge-five-20260928/validate.mjs --require-reviews
node docs/videos/series-plans/claude-binge-five-20260928/validate.mjs
node --test docs/videos/series-plans/binge-five-20260928/validate.test.mjs
node --test docs/videos/series-plans/claude-binge-five-20260928/validate.test.mjs
node tools/tasks.mjs check
```

Audit baseline: all ten validators pass, Codex 17 tests and Claude 10 tests pass.
Read changed scenes plus preceding setup and subsequent carry-forward, not only
the changed line. Rebuilding without renewed editorial review is insufficient.

## Notes

- Read-only audit covered all 400 episode summaries/carry fields, setting rules,
  packaging and detailed scenes around each suspected issue. Three independent
  agents split the two story batches and shared production contract.
- First-pass Three Needles clearance is superseded by the second-pass findings
  above. Before the Hammer's fourth-cup naming remains ambiguous: E35 includes
  four props, E36 names another fourth
  cup, but historical-cup counting might exclude a modern counterfeit. Clarify
  using prop IDs; do not label this an established continuity failure.
- Ghost E24 source.mjs:665,669 has Qingyan turn a list, while :40,218 only
  permits touching charm paper. The list's material is never specified. Record
  this as a prop-identity clarification (for example, explicitly charm paper),
  not a confirmed new supernatural ability or an established ordinary-paper
  violation.
- The second independent pass over all 200 Codex episodes found no additional
  high-confidence contradiction beyond this ticket's original findings. Rejected
  candidates include City's E22 remote written report, Wedding's parallel
  18:02-18:10 viewpoints, Empress's staged grain delivery dates, and Rival's
  three abyss loans. This is review evidence, not a guarantee of no remaining
  defects or a judgment about finished-film quality.
- Editorial judgment, not a proved defect: the Codex stories frequently resolve
  different genres through document verification and accountability. The shared
  compare tool measures 15 consecutive wins for Wedding, 9 for City and Empress,
  6 for Train, 4 for Rival. Consider genre-specific action and reversals during
  scripting; these labels do not prove poor viewer retention.
- Do not infer production state from validator backend_created:false: that output
  is authoring-scope metadata. The live snapshot above confirms later import.
- Browser inventory timed out, so rendered admin-page acceptance remains unverified.
  Existing follow-up on codex/import-reviewed-drama-plans is
  2026-09-28-verify-imported-review-pages-and-reconcile; do not duplicate its full
  media/browser scope or modify its owner's active worktree.
- At initial audit filing, only findings were recorded. The later local repair is
  recorded below; production review status, generation and publication remain unchanged.

## Repair implementation, 2026-09-28

- Implemented in isolated branch `codex/ten-drama-audit-fixes` under the claimed
  ten-drama content / preloaded-approval / listener tasks. The owner explicitly
  approved parallel backend repairs despite other task claims; no other branch
  or owner claim was changed.
- Report: `docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260928.md`.
- Local source/documents and code are revised; historical production/import
  receipts are unchanged. No deployment, production update, approval, generation
  or publication has been performed by this repair.

### Verification and handoff

- Content: both ten-work validators pass; 34 generator/continuity tests pass;
  independent revised-source receipts and all 60 current document hashes checked.
- API: 80 focused tests pass, including SQLite transaction coverage; 5 PostgreSQL
  integration tests remain skipped locally. Ruff and touched-file mypy pass.
- Worker/tool suite: 578 pass, 1 existing Windows/Bash environment skip.
- The branch is ready for code review; it has not been merged or deployed. The
  independent production/browser follow-up remains with its existing owner.
