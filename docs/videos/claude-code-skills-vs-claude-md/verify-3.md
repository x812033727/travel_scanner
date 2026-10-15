Checked by an independent agent that did not write the script, on 2026-10-11. It read the script as it stood before the changes listed at the end of this file (branch head `be6458021`). Everything from the heading below down to "What the writer changed" is that agent's report, unchanged; the last section was added by the writer afterwards and says what was changed for each finding and what was left.

The film was first made as `claude-code-skills-hands-on` on 2026-10-10 and rewritten under the new slug `claude-code-skills-vs-claude-md` on 2026-10-11. Both reports in this file were written while the folder still had the old name; their text is unchanged, and the files they name are the ones in this folder.

# Independent fact-check of the rewritten Skills script (2026-10-11)

Verdict: pass_after_fixes. Claims checked: 188.

## Recomputed

Recomputed from the per-run lines of the 23 session logs in runlog.txt (tally "first request" and drift "requests to the model"). In every 2026-10-11 session the per-request figures sum to the session total.

First request (input + cache write + cache read):
- No procedure: no1 8,753 (1 run).
- One Skill: sk 8,818 / 8,811 / 8,812, mean 8,813.67, +60.67 (range +58 to +65). Card +61: correct.
- Same procedure in CLAUDE.md: md 9,240 / 9,238 / 9,240, mean 9,239.33, +486.33. Card +486: correct.
- Five Skills: skf 9,041 / 9,042 / 9,039, +287.67. Card +288: correct.
- Five procedures in CLAUDE.md: mdf 9,909 / 9,907 / 9,908, +1,155.00. Card +1,155: correct.
- CLAUDE.md minus Skill: 425.67 (five procedures 867.33). Overhead ratio 486.33 / 60.67 = 8.0.

Requests per session:
- sk 4, 4, 4; md 3, 3, 3; sx 3, 3, 3; skl 4, 4, 4; mdl 3, 3, 3.
- skf 4, 4, 5; mdf 3, 3, 3; no1 4; hand1 5.

Whole session, input tokens:
- sk 39,606 / 39,524 / 39,566, mean 39,565.33.
- md 30,284 / 30,307 / 30,297, mean 30,296.00.
- sk minus md 9,269.33 (pairwise 9,217 to 9,322). In each pair the Skill-call request (8,811 to 8,818) is 94.6% to 95.6% of the difference.
- sx 30,397 / 30,390 / 30,433, mean 30,406.67; sx minus md 110.67.
- Look request: skl 39,150.33 against mdl 29,390.67, difference 9,759.67.
- Five procedures: skf 44,453.0 against mdf 32,431.7, difference 12,021.3.

Break-even:
- 9,269.33 / 425.67 = 21.78 (script's 9,269 / 425 = 21.81; narration's 9,200 / 425 = 21.65).
- The same division on the five-procedure pair gives 13.9, on the look pair 22.8.

Steps:
- F1 to F5 are 3/3 in sk, md, skf, mdf, sx and in s and v (2026-10-09).
- Control n1-3 + no1: version 4/4, README 4/4, CHANGELOG 2/4, release note 0/4, last line 0/4.
- Skill tool called: sk 3/3, skf 3/3 (release-prep only), skl 3/3, always as call 1; md, mdf, mdl, sx 0/3.
- Look: seed files changed 0/6, new files 0/6.

Reported cost (listed in the log, not compared by the film): sk mean $0.04744, md $0.03997, sx $0.04227.

Files and cards:
- 14 code cards, 8 terminal cards, 3 chat cards and 2 quote cards match demo/ and the run log character for character (0 mismatches of 27).
- The nine lines of typed-cmd.sh are the nine lines recorded for hand1.
- sha256 prefixes of all demo files equal those printed in the session logs.

## Findings

### 1. [must_fix] scene `rule`, narration lines jfcy and ca57 (and w3yy); card row 3 and the card's source line

- Claim as written: 「九千兩百除以四百二十五，大約二十二。」「超過二十二個請求才用一次，讓它自己叫才比較省。」
- Problem: The arithmetic is right (9,269 / 425 = 21.8) but the second sentence states a threshold as a rule. It is one 3-run average divided by another (the 425 itself rests on a single baseline run), and the 9,269 is not a property of a Skill: about 95% of it is one extra round that re-reads everything already in the conversation, which here was 8,811 to 8,818 tokens because the session had six tools, no MCP and a four-file project. The film's own other pairs give other break-evens, and the count weights cached and fresh input tokens the same while the film declines to compare cost. A viewer applying 22 to their own project has no evidence for it.
- Evidence: runlog.txt 5887-5896 ("9269.3 / 425.7 = 21.8", arithmetic on means). Per-request figures: sk1 8818+9302+10092+11394 against md1 9240+9925+11119, extra 9,322 of which the Skill-call request is 8,818 (94.6%); pairs 2 and 3: 95.6%, 95.1%. Five-procedure pair from runlog 5875-5877: 44,453 against 32,432 = +12,021, divided by 867.3 = 13.9. Look pair: 9,759.7 / 427.7 = 22.8. claims.md c67 and 「我懷疑但沒動的事」 already call it two averages divided, not measured.
- Smallest fix: ca57: 「照這次量到的兩個平均來估，大約隔二十二個用不到的請求才打平；這是這個小專案的估計，不是門檻。」 Add 「22 是估計」 to the card's source line. Leave w3yy as is or prefix it 「這次量到」.

### 2. [must_fix] scene `rule`, card row 4 with the card's header and source line; narration line gvba

- Claim as written: 列：「被呼叫 3 次，一步都沒做（只要它看時）」→「一定要成立的那一步，交給 Hook」；出處「實際跑過 2026-10-11｜9,269＝39,565−30,296｜各 3 次」；旁白「Skill 被呼叫了也可以一步都不做；一定不能漏的那一步，改用 hook 來做。」
- Problem: This rule does not follow from the measured result beside it. In skl1 to skl3 leaving the five steps undone was the correct response, since the request asked only for a look. Whenever the release was actually requested, every instructed session did all five steps. No run shows a required step being skipped, and no hook that enforces a step was run (the only hook is the logger). The conclusion comes from the official Hook-vs-Skill comparison, yet the card files it under 「量到的 → 所以」 with a 「實際跑過」 source. Rules 1 to 3 do follow from their rows.
- Evidence: runlog.txt 5879-5885 (look: seed file changed 0/3 and 0/3, release carried out 0/3 and 0/3); 5860-5870 and 2138-2160 (all five steps: CLAUDE.md md1-3, mdf1-3, c1 = 7/7; Skill called by Claude sk1-3, skf1-3, s1-3, v1-3, o1, hand1 = 14/14; slash sx1-3, x1 = 4/4). Official features-overview, tab "Hook vs Skill": "Determinism | Always fires on its event; the trigger is guaranteed | Claude interprets the instructions; outcome can vary" (fetched 2026-10-11, 28,566 bytes, same size the runner recorded). claims.md has no claim line citing this for `rule`.
- Smallest fix: Append to the card source 「第 4 列的『所以』：官方 features-overview，引用，沒有跑過」. gvba: 「Skill 被呼叫了，做不做還是它自己判斷；一定不能漏的那一步，官方的建議是交給 hook。」 Add the citation to claims.md.

### 3. [should_fix] scene `rule` row 3; scene `closing` third line; scene `five` table

- Claim as written: 「Claude 自己叫：多 1 個請求、9,269 個 token」；「Claude 自己叫多 1 個請求；用 /名稱 叫不會」
- Problem: Exact for sk1-3 and skl1-3 (4 against 3). But of the ten sessions that day in which Claude called the Skill itself, two sent 5 requests (skf3 and hand1). The five-Skill arm is 4, 4, 5 with whole sessions 40,603 / 40,468 / 52,288 against 32,422 / 32,378 / 32,495. The film shows hand1's 5, but the five-procedure request counts and session totals appear on no card, so 「多 1 個請求」 reads as a constant.
- Evidence: runlog.txt 5874-5877 ("requests to the model 4 4 4 | 3 3 3 | 3 3 3 | 4 4 5 | 3 3 3"); 5980-5983 ("eight sent 4 requests and two (skf3, hand1) sent 5; the nine CLAUDE.md sessions all sent 3"); skf3 session log: call 10 Edit releases/v0.3.1.md, requests 9039, 9523, 10313, 11517, 11896.
- Smallest fix: Rule row 3: 「Claude 自己叫：多 1 個請求、9,269 個 token（sk1–3；十次裡有兩次多 2 個）」, or add a row 「送了幾個請求｜3、3、3｜4、4、5」 to the `five` table.

### 4. [should_fix] scene `scope`, card items and narration line u6y3

- Claim as written: 「Claude Code 2.1.295，不開畫面的 session」「一個模型：sonnet（claude-sonnet-5-5）」「Windows 11 的 Git Bash」「每一種 3 次；CLAUDE.md 最長 59 行」；「換了模型或平台，這些數字會變；比五十九行更長的 CLAUDE.md，結果也可能不同。」
- Problem: The condition that most directly sets the whole-session figures is missing: every session ran with six built-in tools, no MCP servers and a four-file project, so the conversation started at about 8,750 tokens. The 39,565, 30,296 and 9,269 figures are multiples of that starting size.
- Evidence: tally output in every session log: "built-in tools offered (6): Edit Glob Grep Read Skill Write", "MCP servers 0, MCP tools 0"; no1 first request 8,753 (runlog.txt 5290-5338); whole sessions are sums of 3 or 4 requests of 8.8k to 11.4k each.
- Smallest fix: Add one item, for example 「只開六個工具、沒有 MCP：對話一開始約 8,750 個 token」, replacing or merging 「Windows 11 的 Git Bash」 with the first item if the card is full.

### 5. [should_fix] scene `vs-md` verdict; scene `rule` narration nmsp; scene `s-heads` narration f5ah

- Claim as written: 「照不照做，兩邊一樣；選的是大小」；「五個步驟兩邊一樣，不用為了讓它更照做而搬。」；「寫了什麼，它就做什麼，放哪裡都一樣。」
- Problem: 3/3 against 3/3 (and again with five procedures) shows that no difference was observed in twelve sessions of one model on one five-step procedure. It cannot show the two placements are equally reliable in general; three runs per arm would not separate, say, 90% from 100%. The counts are stated honestly elsewhere; these three sentences drop the 「這幾次」.
- Evidence: runlog.txt 5860-5870: F1 to F5 are 3/3 in sk, md, skf, mdf; n = 3 per arm, one model, one request sentence.
- Smallest fix: 「照不照做，這幾次兩邊一樣；選的是大小」；「這幾次五個步驟兩邊一樣，不用為了讓它更照做而搬。」；「寫了什麼，它就做什麼；放哪裡，這幾次都一樣。」

### 6. [should_fix] scene `look-score`, narration line 268x

- Claim as written: 「兩邊都沒有動任何一個檔案，都回答沒有漏記。」
- Problem: The first half is recorded for all six sessions. The second half has reply text in the repository for two of six only (skl1, mdl1). For skl2, skl3, mdl2 and mdl3 the repository holds the last line of each reply, none of which says nothing is missing, plus one summary sentence by the runner.
- Evidence: runlog.txt 5801-5806 (drift: none | none | no for all six); full replies at 4588 (skl1 「沒有發現漏記」) and 4750 (mdl1 「CHANGELOG 沒有漏記」), also demo/results/2026-10-11.skl1.reply.txt and mdl1.reply.txt; last lines only at 5851-5854; runner's sentence at 4428 ("All six replies say nothing is missing").
- Smallest fix: Add the four replies to demo/results (the run log says the raw streams are kept in <work>/run/logs), or cut the sentence to 「兩邊都沒有動任何一個檔案。」

### 7. [note] scene `look-call`, narration lines 7dqv and 9kyr

- Claim as written: 「Skill 那一邊，三次都先把 Skill 叫了起來。」「引數是它自己填的，裡面寫著：使用者只要求先檢查。」
- Problem: The second sentence follows 「三次都」 but describes skl1 only. skl2's argument reads differently and skl3 passed no argument. The card kicker does say skl1.
- Evidence: runlog.txt 4423-4425: skl1 {"skill":"release-prep","args":"0.3.1 — 使用者只要求先檢查 CHANGELOG 有沒有漏記的"}; skl2 args "0.3.1 — 只檢查 CHANGELOG 有沒有漏記的"; skl3 {"skill":"release-prep"}.
- Smallest fix: 「這一次的引數是它自己填的，裡面寫著：使用者只要求先檢查。」

### 8. [note] scene `chk-req`, narration line dsax

- Claim as written: 「它把範本的標題照抄進發版說明，再回頭改成版本號碼，多了一趟。」
- Problem: The fifth request and the extra Edit are recorded. What the Edit changed ("# vX.Y.Z" to "# v0.3.1") is stated only in the runner's prose note; no stream line for hand1 is in the repository.
- Evidence: runlog.txt 6052-6053 (call 10 Write releases/v0.3.1.md, call 11 Edit releases/v0.3.1.md); 6077 (requests 8820, 9305, 10176, 11399, 11793); 6088-6090 (runner note giving old_string and new_string).
- Smallest fix: None needed for the script; paste the two event lines for calls 10 and 11 into the run log if a later reader should be able to check it.

### 9. [note] scenes `six` (line efj4), `cost` (line 3g5h), `vs-md` card points, `rule` row 2, `closing` line 2gv9

- Claim as written: 「CLAUDE.md 每個請求多帶四百八十六個 token，Skill 六十一個。」「每個請求多帶 486 個 token」「每個請求多帶 61 個 token」
- Problem: The measured value is the first request of each session (the `six` and `cost` cards say so; `vs-md` and `rule` say 「每個請求」 under a 「實際跑過」 source). The statement holds: later requests in the recorded streams re-read the whole first request, and the official context-cost table says the same. For the Skill it holds only until the Skill is invoked, which the film covers with 「用到的那一次」.
- Evidence: sk1 stream: request 2 cache_read 8816 after a first request of 8818; md1: request 2 cache_read 9238 after 9240 (runlog.txt 2946-2978, 3113-3138). features-overview "Context cost by feature": "CLAUDE.md | Session start | Full content | Every request"; "Skills | ... | Low (descriptions every request)". claims.md c52 cites neither.
- Smallest fix: Cite the features-overview context-cost row in claims.md c52; optionally write 「第一個請求量到 +486」 on `vs-md` and `rule` to match `six` and `cost`.

### 10. [note] scene `body-0`, narration line wc33; scene `md-file-1`, narration line wzhx

- Claim as written: 「內文是從 CLAUDE.md 那一段搬過來的，只改了第四步。」；「每一步都對應一個檔案，和一個看得到的結果。」
- Problem: Small imprecisions. Besides step 4 (2 of 11 body lines), the heading level changed from 「## 發版準備」 to 「# 發版準備」 and the three-heading list at the bottom of CLAUDE.md was dropped. Step 5 corresponds to the reply's last line, not to a file.
- Evidence: My line-by-line comparison of demo/variants/release-prep.specific.skill.md 9-19 with CLAUDE.release.md 5-15: 2 of 11 differ (same as check-five.mjs, runlog.txt 2744); SKILL.md line 7 against CLAUDE.release.md line 3.
- Smallest fix: Optional: 「步驟只改了第四步」；「前四步各對應一個檔案，第五步對應回覆的最後一行。」

### 11. [note] scene `vague-score`, narration line 7dzy

- Claim as written: 「五個步驟三次也都做到，和寫好的那一份沒有任何一項不同。」
- Problem: True for the scored items. The scoring rule for step 5 accepts a half-width colon, and on 2026-10-09 the last lines were not character-identical across the two arms, although the procedure says 「固定寫：下一步：git tag vX.Y.Z」. The 2026-10-11 runs behind the main comparison all wrote the full-width form.
- Evidence: demo/tally.mjs line 27: NEXT_STEP = /^[\s>*_`-]*下一步[：:]/; last lines: s1, s2, v1, v2, v3 「下一步:git tag v0.3.1」, s3 「下一步：git tag v0.3.1」; runlog.txt 2817-2818 ("on 2026-10-09 nine of ten wrote a half-width colon").
- Smallest fix: None required; 「計分的項目沒有任何一項不同」 would be exact.

### 12. [note] item 4 overall: scenes `loads`, `places-shot`, `fm-2`, `validate-cmd`, `cmd-2`, `cmd-3`, `slash-ask`, `slash-score` (zzw5), `check-order`, `keep`, `trust`

- Claim as written: 官方說明類：Skill 分三次載入、CLAUDE.md 每個 session 整份載入、位置表、when_to_use 是 Claude Code 自己加的、validate 檢查 frontmatter、--setting-sources project,local 不載入個人 Skill、明列工具要含 Skill、/名稱 放訊息最前面、CLAUDE.md 沒有斜線入口、skillOverrides "off"、commit .claude/skills/、刪資料夾、allowed-tools 與 -p
- Problem: No contradiction and nothing not found. 21 statements confirmed against pages fetched 2026-10-11 with a neutral user agent and no other header. Two rest partly on inference, both disclosed in claims.md: 「個人的 Skill 不會載入」 has no control run without the flag, and the order on `check-order` is the film's own.
- Evidence: skills.md (107,130 bytes): line 574 "full skill content only loads when invoked"; 159-164 location table under id="where-skills-live"; 402 when_to_use "Appended to `description` in the skill listing"; 428 outside Claude Code only name, description, license, compatibility, metadata, allowed-tools; agentskills.io/specification has 0 occurrences of when_to_use; 579 "put its name at the start of your message"; 602 "Workspace trust doesn't gate this field ... even in a `-p` run"; 329 "delete the skill's directory"; 885-890 skillOverrides "off"; 961 "Commit `.claude/skills/` to version control"; 1171 validate, "Requires Claude Code v2.1.233 or later". features-overview.md line 101 "Loads | Every session, automatically | On demand" and "Can trigger workflows | No | Yes, with /<name>". cli-reference.md line 129 --setting-sources. agent-sdk/claude-code-features line 79 ("user" covers user skills); agent-sdk/skills line 48 (include "Skill" in an explicit tools list). Debug logs: "managed: 0, user: 0" in all 22 sessions.
- Smallest fix: None.

## Summary

The central claim holds on the recorded evidence, so the film stands once two sentences and cards on the last table are corrected. I ran no new sessions and changed nothing in the repository.

**What a reader can rely on**
- **Steps:** both placements did all five steps in 3 of 3 sessions, and again with five procedures.
- **First request:** CLAUDE.md added 486 tokens and the Skill 61, over a single 8,753-token baseline run.
- **Skill called by Claude:** 4 requests against 3, and 39,565 against 30,296 tokens, in the three paired runs.
- **Slash call:** 3 requests and 30,407 tokens.
- **Look request:** the Skill was called 3 of 3 times and no file changed in any of the six sessions.
- **Cards:** every file, command and terminal output shown matches demo/ and the run log exactly, and the nine typed lines are the ones recorded as run.
- **Documentation:** all 21 statements about Claude Code's behaviour are confirmed by the official pages; none is contradicted or missing.

**What a reader cannot rely on**
- **The 22-request break-even.** It is two small-sample averages divided, and the 9,269 is mostly one extra round re-reading an 8.8k-token starting context in a six-tool, four-file project. The film's own five-procedure pair gives about 14.
- **The fourth rule (give must-hold steps to a Hook).** It is official guidance, not something measured here: no required step was ever skipped and no enforcing hook was run.
- **"One more request" as a constant.** Two of the ten sessions where Claude called the Skill itself took two more.
- **"The two sides are the same" as a general statement.** Three runs per arm show only that no difference was observed.

One evidence gap: four of the six look-request replies are not in the repository, so "all answered nothing is missing" rests on the runner's summary for those. More broadly, the raw streams are not in the repository; everything was checked against the run log's transcriptions, which are internally consistent.

## What the writer changed for each finding (2026-10-11, after the report above)

No headless session was run for any of this. Nothing was synthesized or rendered. The script went from 54 scenes and 120 narration lines to 57 and 125; the lint ends with 0 errors and 0 warnings. This section has not been checked by a second independent reading.

1. **Must fix, the break-even: applied.** Scene `rule`: line ca57 now reads 「照這兩個平均來估，大約隔二十二個用不到的請求才打平。」 and a new line qygu follows it, 「這是這個小專案的估計，不是門檻。」. Line w3yy is prefixed 「這三次量到的是：」. The card's source reads 「實際跑過 2026-10-11｜各 3 次｜22 個請求是估計，不是門檻」. `claims.md` c67 now calls it an estimate and gives the other two pairs' figures (13.9 and 22.8) and what the 9,269 is made of. The description and `brief.md` say the same.
2. **Must fix, the Hook rule: applied by splitting the card.** The four-row table mixed three measured rows with one cited conclusion. `rule` now holds the three measured rows only (title 「搬不搬，看量到的這三件事」). The fourth rule is its own scene, `rule-hook`, a quote card with the official sentence "Use a hook when the action must happen the same way every time and doesn't need Claude to think." and the source 「Claude Code 文件｜features-overview｜Hook vs Skill｜2026-10-11｜引用，沒有跑過」. Line gvba reads 「一定不能漏的那一步，官方的建議是交給 hook。」, after a new line 8tpx, 「Skill 被呼叫了，做不做還是它自己判斷。」. `claims.md` has a new claim c71 with the citation and the statement that no run here skipped a required step or ran an enforcing hook; c64 no longer supports the rule.
3. **Should fix, "one more request" as a constant: applied in three places.** `rule` row 3 reads 「Claude 自己叫：多 1 個請求、9,269 個 token（十次裡兩次多 2 個）」. The `five` table has a fourth row, 「送了幾個請求｜3、3、3｜4、4、5」, with a new line iank. The outro's third line reads 「Claude 自己叫多 1 到 2 個請求；用 /名稱 叫不會」. Line haev in the opening says 「這三次」. `claims.md` c53 carries the eight-and-two count.
4. **Should fix, the condition behind the session sizes: applied.** `scope` has a fifth item, 「只開六個工具、沒有 MCP：對話一開始約 8,750 個 token」, and line u6y3 names more tools as something that changes the numbers. `claims.md` c69 and the description say it too.
5. **Should fix, 「這幾次」: applied, in four sentences.** `vs-md` verdict 「照不照做，這幾次兩邊一樣；選的是大小」; nmsp 「這幾次五個步驟兩邊一樣，不用為了讓它更照做而搬。」; f5ah 「寫了什麼，它就做什麼；放哪裡，這幾次都一樣。」; and the outro's first sentence, 2gv9, which had the same shape. `rule` row 1's conclusion also begins 「這幾次沒有差」.
6. **Should fix, the four replies: applied by adding the evidence.** The replies of skl2, skl3, mdl2 and mdl3 were saved unchanged from the kept streams as `demo/results/2026-10-11.<name>.reply.txt`; all six are now in the repository and line 268x stands as written. `runlog.txt`, Runner note 2, item 1; `claims.md` c65.
7. **Note, line 9kyr: applied.** 「這一次的引數是它自己填的，裡面寫著：使用者只要求先檢查。」
8. **Note, hand1's extra Edit: applied in the run log.** The two event lines of calls 10 and 11 are pasted in `runlog.txt`, Runner note 2, item 3. The script is unchanged here.
9. **Note, "every request": applied.** `vs-md` and `rule` now say 「第一個請求量到」, as `six` and `cost` do. `claims.md` c52 cites the official context-cost rows and the second-request cache reads. The narration keeps 「每個請求」, which the finding says holds.
10. **Note, small imprecisions: applied.** wc33 「…步驟只改了第四步。」; wzhx 「前四步各對應一個檔案，和一個看得到的結果。」. `claims.md` c56 names the two other differences (the heading level, the list moved into the template).
11. **Note, line 7dzy: applied.** 「五個步驟三次也都做到；計分的項目，和寫好的那一份沒有一項不同。」 `claims.md` c38 gives the colon detail.
12. **Note, the cited statements: nothing to change.**

Also added, from the two blind readings rather than from this report: two terminal cards, `chk-first` and `chk-whole`, with a one-line command each that reads the token counts out of the stream. They were typed in hand1's project folder on the stream hand1 left, without a model, and their sums equal what `tally.mjs` prints for the same stream (and for four other kept streams). `runlog.txt`, Runner note 2, item 2; `claims.md` c70. `yours` now names size beside the request count.

Changed in the same commit and missing from this list when it was first written (the second reading below found it): to keep the composed description under 5,000 bytes, three things were cut from `youtube.description`. The line 「・session 從 Claude Code 桌面版開的 Git Bash 啟動（CLAUDE_EFFORT 設成 high）；一般終端機沒有試過。」 was removed, which took a disclosed run condition out of `video.json`; the two file names in the bullet about the demo folder's neutral names were shortened to 「variants/ 底下的中性檔名」; and the sentence naming `tally.mjs` and `drift.mjs` was dropped. The first of these is put back in a shorter form after the second reading; see the end of this file.

Left as it was, because it needs a new run:
- Turning the 22-request estimate into a measured figure (a project with more tools and a longer conversation, both arms).
- A control run without `--setting-sources` for 「個人的 Skill 不會載入」 (finding 12 notes it rests on the documentation and on the per-session counts).
- The CLAUDE.md arm with the `# vX.Y.Z` title line written in, to make the two arms' instructions exactly equivalent (`claims.md`, c60).
- Any session in which a required step is skipped or an enforcing hook is run; the Hook rule stays a citation.

Not addressed by this section: the raw streams are still outside the repository, as the report's last paragraph says; the run log's transcriptions are what a reader can check.

## The second independent reading (a second independent agent, 2026-10-11)

A second agent, which wrote neither the script nor the first report, read the changes made after the fact-check: branch head `765508af7` against `be6458021`. Its report follows unchanged, down to "What the writer changed after the second reading".

# Second independent reading of the changes made after the fact-check (2026-10-11)

Read at branch head 765508af7 against be6458021. Verdict: pass. Claims checked: 206.

## Findings

### 1. [should_fix] video.json, youtube.description, the block 「怎麼跑的」 (not narration, not a card)

- As it now stands: Now: 「・Windows 11、Git Bash、Node.js v24.13.0、Claude Code 2.1.295，全部 --model sonnet（claude-sonnet-5-5）、不開畫面。2026-10-09 跑 12 次，2026-10-11 跑 23 次，沒有重跑；紀錄在 runlog.txt。」 The line that stood at be6458021, 「・session 從 Claude Code 桌面版開的 Git Bash 啟動（CLAUDE_EFFORT 設成 high）；一般終端機沒有試過。」, is gone.
- Problem: A run condition that the fact-checked version disclosed was dropped, and the writer's change list in verify-3.md does not mention it. Nothing in video.json now says that every session inherited CLAUDE_EFFORT=high from the desktop app's shell and that an ordinary terminal was not tried. The nine typed lines do not set that variable, so a viewer who types them runs under a condition the film's runs did not have. Nothing the description still says is false; a caveat is missing.
- Evidence: Comparing the description line by line, base against head: the strings CLAUDE_EFFORT, 桌面版 and 一般終端機 are in the base video.json and absent from the head. runlog.txt lines 10-14 ("Git Bash started by the Claude Code desktop app ... CLAUDE_EFFORT=high") and line 5992 ("# hand1 | start 2026-10-11T11:54:06Z | CLAUDE_EFFORT=high"). brief.md line 592: 「它對不開畫面的 session 有沒有作用，沒有量過。」 The reason is room: linting a scratch export of the branch head, the composed description is 4,982 of 5,000 bytes, and putting the old line back verbatim gives "5105 bytes once composed, at most 5000".
- Smallest fix: Put the condition back in a form that fits. Tested on a scratch copy (lint 0 errors, 0 warnings): change 「全部 --model sonnet（claude-sonnet-5-5）、不開畫面。」 to 「全部 --model sonnet（claude-sonnet-5-5）、不開畫面，從桌面版開的 Git Bash 啟動（CLAUDE_EFFORT=high）。」 and drop 「不放也行，畫面上的 grep 數得出來。」 from the hook bullet. This can be done after recording; it touches no narration and no card.

### 2. [note] scene `yours`, narration line 64ts; the same wording in youtube.description (「你會學到」, third bullet)

- As it now stands: 「數三件事：步驟做到幾次、Skill 有沒有被呼叫、請求有幾個、各有多大。」 and 「再數三件事：Skill 工具被叫了幾次、送了幾個請求與各有多大、檔案改了哪些」
- Problem: 「各有多大」 reads as the size of each request. The two new cards show how to read the first request and the whole session, not each request, and the description no longer points to tally.mjs or drift.mjs, which print the per-request sizes. A small imprecision in an instruction, not a claim about a result.
- Evidence: chk-first reads only the first line that contains "assistant" (grep -m1); chk-whole reads the result line's totals. The base description's sentence 「tally.mjs 與 drift.mjs 列出工具呼叫、五步的結果、請求數與 token」 is not in the head.
- Smallest fix: Optional, and only worth doing before the narration is recorded: 「數三件事：步驟做到幾次、Skill 有沒有被呼叫、請求有幾個、一共多大。」; in the description 「送了幾個請求、一共多大」.

### 3. [note] scene `chk-first`, data.command

- As it now stands: grep -m1 assistant ../stream.jsonl | tr ',{' '\n\n' | grep -m3 input_tokens
- Problem: The card is correct as run. For a viewer it relies on one thing outside the command: the stream's first line (the init event) must not contain the string "assistant". That line carries the viewer's own folder path and user name (fields cwd and scratchpad_path) and the names of skills, agents, plugins and slash commands. A project kept in a folder such as ai-assistant, or a project skill with that word in its name, makes the command print nothing, with no error. chk-whole has no such dependence in the streams I read (num_turns is on exactly one line in all 23).
- Evidence: Fields of hand1's init line read from the kept stream: cwd, scratchpad_path, skills, agents, plugins, slash_commands. On all 23 kept 2026-10-11 streams the first "assistant" line is the first assistant event (line 2; line 4 or 5 in the six look streams, after system/thinking_tokens lines). claims.md c70 already says the two commands were tried only on Claude Code 2.1.295 streams. The stricter pattern, grep -m1 '"type":"assistant"' ../stream.jsonl | tr ',{' '\n\n' | grep -m3 input_tokens, prints the same three lines on hand1's stream.
- Smallest fix: None required. If the writer wants it sturdier, use the stricter pattern; the card then has to be re-typed on hand1's kept stream and recorded in runlog.txt (no model needed), since cards show commands as run.

## Recomputed

THE TWO NEW CARDS
- chk-first. Card command: grep -m1 assistant ../stream.jsonl | tr ',{' '\n\n' | grep -m3 input_tokens. It equals runlog.txt line 6127 character for character (one occurrence in the log). Card output equals lines 6128-6130: "input_tokens":2 / "cache_creation_input_tokens":3452 / "cache_read_input_tokens":5366. Sum 2 + 3,452 + 5,366 = 8,820, which is tally.mjs's "first request ... = 8820 tokens" for hand1 (line 6058) and the first of the five request sizes on line 6077. Narration x4n9 says 八千八百二十: correct. tool_version "grep (GNU grep) 3.0" is line 6138; ran_on 2026-10-11 matches the 12:41:09Z header on line 6123.
- chk-whole. Card command: grep num_turns ../stream.jsonl | tr ',{' '\n\n' | grep -m3 input_tokens. It equals line 6132 (one occurrence). Output equals lines 6133-6135: 10 / 6425 / 45058. Sum 10 + 6,425 + 45,058 = 51,493 = tally's "whole session: 51493" = 8,820 + 9,305 + 10,176 + 11,399 + 11,793. Narration mkte says 五個請求，五萬一千多個: correct.
- Re-run by me, no model: the kept work folder is on this machine, outside the repository. In <work>/hand/unit-kit, on ../stream.jsonl (31 lines, byte-identical to hand1.stream.jsonl), both commands typed exactly as on the cards print the same three lines each, exit 0. grep -c assistant gives 13, the first line has 0 hits, num_turns is on 1 line.
- All 23 kept streams of 2026-10-11 (hand1 plus 22), parsed with my own script and spot-checked with the real commands on eight: the first command's three numbers equal the first request's size in 23 of 23, and the second command's three numbers equal the sum over distinct message ids in 23 of 23.
- Would a viewer get the same kind of output: yes, plausibly. ../stream.jsonl is the file the nine typed lines write, and both commands work on every arm's stream (Skill, CLAUDE.md, slash, look, no procedure). The numbers will differ, and the cache write and cache read split moves from run to run. The one dependence particular to a stream is in the third finding.

HEADLINE FIGURES, recomputed from the kept streams
- Whole session: sk 39,606 / 39,524 / 39,566, mean 39,565.3, requests 4, 4, 4. md 30,284 / 30,307 / 30,297, mean 30,296.0, requests 3, 3, 3. Difference 9,269.3. sx 30,397 / 30,390 / 30,433, mean 30,406.7, requests 3, 3, 3.
- First request: no1 8,753. sk 8,818 / 8,811 / 8,812 (+60.7). md 9,240 / 9,238 / 9,240 (+486.3). skf 9,041 / 9,042 / 9,039 (+287.7). mdf 9,909 / 9,907 / 9,908 (+1,155.0).
- Requests elsewhere: skf 4, 4, 5; mdf 3, 3, 3; skl 4, 4, 4; mdl 3, 3, 3; hand1 5. Of the ten sessions in which Claude called the Skill itself, eight sent 4 and two sent 5 (skf3, hand1).
- Break-even: 9,269.3 / 425.7 = 21.8. Five procedures: 12,021.3 / 867.3 = 13.9. Look request: 9,759.7 / 427.7 = 22.8.
- In video.json, 3／3 appears 28 times before and after; 486, 61, 30,407, 3、3、3 for the slash call and 4、4、4 are unchanged in every scene that had them. 39,565, 30,296 and 9,269 each lost one occurrence, all from the old source line of `rule` (「9,269＝39,565−30,296」), which the estimate note replaced. No headline figure reads differently anywhere.

THE TWELVE FINDINGS, as the script now stands (every listed change is in video.json)
1. ca57 「照這兩個平均來估，大約隔二十二個用不到的請求才打平。」; new qygu 「這是這個小專案的估計，不是門檻。」; w3yy 「這三次量到的是：讓 Claude 自己叫，每用一次多九千兩百多個 token。」; `rule` source 「實際跑過 2026-10-11｜各 3 次｜22 個請求是估計，不是門檻」. Fixes the finding; nothing new.
2. `rule` title 「搬不搬，看量到的這三件事」 with three measured rows. New quote card `rule-hook`; 8tpx 「Skill 被呼叫了，做不做還是它自己判斷。」; gvba 「一定不能漏的那一步，官方的建議是交給 hook。」. Fixes the finding; details under the quote card below.
3. `rule` row 3 「Claude 自己叫：多 1 個請求、9,269 個 token（十次裡兩次多 2 個）」; `five` row 「送了幾個請求｜3、3、3｜4、4、5」 with iank 「請求數是三個對四個；五個 Skill 那一邊，有一次是五個。」; outro 「Claude 自己叫多 1 到 2 個請求；用 /名稱 叫不會」; haev 「可是 Claude 自己叫 Skill 的這三次，都多送一個請求。」. All match the streams.
4. `scope` item 「只開六個工具、沒有 MCP：對話一開始約 8,750 個 token」; u6y3 「換了模型、平台，或是開更多工具，這些數字會變；更長的 CLAUDE.md，結果也可能不同。」. All 35 session logs print six tools and no MCP servers; no1 is 8,753. That more tools change the numbers is an inference, which claims.md c69 says; it is a caveat, not a result.
5. `vs-md` verdict 「照不照做，這幾次兩邊一樣；選的是大小」; nmsp 「這幾次五個步驟兩邊一樣，不用為了讓它更照做而搬。」; f5ah 「寫了什麼，它就做什麼；放哪裡，這幾次都一樣。」; 2gv9 「這幾次五步兩邊都全中；差的是每個請求四百多個 token。」; `rule` row 1 「這幾次沒有差，不用為了更照做而搬」.
6. The four reply files are in demo/results; 268x 「兩邊都沒有動任何一個檔案，都回答沒有漏記。」 stands (see the replies below).
7. 9kyr 「這一次的引數是它自己填的，裡面寫著：使用者只要求先檢查。」. In the kept streams skl1's args are 「0.3.1 — 使用者只要求先檢查 CHANGELOG 有沒有漏記的」, skl2's 「0.3.1 — 只檢查 CHANGELOG 有沒有漏記的」, and skl3 passed none.
8. The two event lines in runlog.txt (6154-6155) equal events 22 and 27 of hand1's kept stream: a Write whose content starts "# vX.Y.Z", then an Edit from "# vX.Y.Z" to "# v0.3.1".
9. `vs-md` points 「第一個請求量到 +486 個 token」 and 「第一個請求量到 +61 個 token」; `rule` row 2 「第一個請求量到：CLAUDE.md +486，Skill +61 個 token」. The context-cost rows that c52 cites are at lines 227 and 229 of the page I fetched.
10. wc33 「內文是從 CLAUDE.md 那一段搬過來的，步驟只改了第四步。」 (my diff of the two files: only the two lines of step 4 differ); wzhx 「前四步各對應一個檔案，和一個看得到的結果。」.
11. 7dzy 「五個步驟三次也都做到；計分的項目，和寫好的那一份沒有一項不同。」.
12. Nothing changed, as the writer says.

THE QUOTE CARD
Fetched 2026-10-11T12:57Z: https://code.claude.com/docs/en/features-overview.md, HTTP 200, 28,566 bytes (the size the runner recorded at 12:00Z), user agent "docs-reader/1.0", no other header. Line 174 is the tab "Hook vs Skill". Line 185: "**Use a hook** when the action must happen the same way every time and doesn't need Claude to think. For example: ...". The card's quote is that first sentence, word for word, without the bold. The translation is faithful. The source line reads 「Claude Code 文件｜features-overview｜Hook vs Skill｜2026-10-11｜引用，沒有跑過」, so the card says it is cited and not run. Line 189 of the same tab ("If a rule must hold every time, make it a hook rather than a prompt instruction.") supports gvba directly. Line 181 ("Claude interprets the instructions; outcome can vary") supports 8tpx, together with the three look sessions.

THE REPLIES
All six files under demo/results equal the result text in the kept streams (640, 849, 622, 585, 512 and 495 characters). skl1: 「以現有程式碼來看，沒有發現漏記。」 skl2: 「CHANGELOG 沒有發現漏記。」 skl3: 「目前看不出有漏記。」 mdl1: 「CHANGELOG 沒有漏記。」 mdl2: 「CHANGELOG 沒有發現漏記。」 mdl3: 「CHANGELOG 沒有漏記。」 Each adds that the folder has no git history to compare against. None of the six sessions made an Edit or Write call.

NARRATION AND LINT
Eighteen narration sentences are new or reworded: haev, wzhx, wc33, x4n9, mkte, f5ah, iank, 7dzy, 9kyr, nmsp, w3yy, ca57, qygu, 8tpx, gvba, 64ts, u6y3, 2gv9. Each states what the evidence shows, or marks an estimate or a result of these runs. None talks about what was or was not run, recorded, seen or verified. Linting an export of the branch head in the scratch folder gives 0 errors and 0 warnings, 11.7 minutes, 125 lines.

WHAT I COUNTED (206): 56 changed sentences and fields across the twelve findings; 57 checks on the two cards (10 on the cards and log, 46 on the kept streams, 1 on the stricter pattern); 6 on the quote card; 12 on the replies; 18 narration sentences; 45 figure comparisons and recomputations; 12 others (lint, nine description lines, the six-tool count, the effort setting).

## Summary

The script is ready to be recorded: no narration sentence or card has to change first.

- **The twelve fixes:** every change the writer lists is in video.json, each fixes what its finding says, and none adds a claim the evidence does not support.
- **The two new terminal cards:** both commands match the run log character for character, and their outputs sum to 8,820 and 51,493, as the tally script prints. I re-ran both on the kept stream without a model and got the same lines, and they give the right figures on all 23 kept streams.
- **The quote card:** it is the official sentence word for word, and it is labelled as cited, not run.
- **The four added replies:** they are the streams' own text, and all six replies say nothing is missing.
- **Headline figures:** 3 of 3 on both sides, 486 against 61, 39,565 against 30,296, 9,269 and the slash call's 3 requests read the same everywhere.

One thing should be put back before publishing. The description lost the line saying the sessions were started from the desktop app's Git Bash with CLAUDE_EFFORT=high, and the writer's change list does not mention it. It was cut for the 5,000-byte limit; a wording that fits is in the finding, and it touches no narration.

Two optional notes: 「各有多大」 in line 64ts promises per-request sizes the cards do not show, and the first new command prints nothing if the viewer's folder path contains the word "assistant".

I changed nothing in the repository and ran no session.

## What the writer changed after the second reading (2026-10-11, before any speech was synthesized)

No session was run. The lint ends with 0 errors and 0 warnings, 57 scenes, 125 lines.

1. **Should fix, the run condition: applied in the wording the reader tested.** `youtube.description`, 「怎麼跑的」, first bullet: 「全部 --model sonnet（claude-sonnet-5-5）、不開畫面，從桌面版開的 Git Bash 啟動（CLAUDE_EFFORT=high）。」 The sentence 「不放也行，畫面上的 grep 數得出來。」 was dropped from the hook bullet to make room. The omission from the first change list is now recorded above, in "What the writer changed for each finding".
2. **Note, 「各有多大」: applied, because it is narration.** Line 64ts reads 「數三件事：步驟做到幾次、Skill 有沒有被呼叫、請求有幾個、一共多大。」; the description's third bullet reads 「送了幾個請求、一共多大」. `claims.md` c68 follows.
3. **Note, the stricter pattern on `chk-first`: left.** The reader's stricter command, `grep -m1 '"type":"assistant"' ../stream.jsonl | tr ',{' '\n\n' | grep -m3 input_tokens`, is 86 columns; a terminal card's command holds 76. The shortest quoted form, `grep -m1 '"assistant"' …`, is 79. So the card keeps the command as it was run (75 columns) and nothing was re-typed. The dependence the reader names (the stream's first line must not contain the word assistant, which a folder or skill name could put there) is added to `claims.md` c70.

## After both readings: the move to the new slug (2026-10-11)

Not read by either agent above. No narration line and no card changed.

- The folder was renamed from `claude-code-skills-hands-on` to `claude-code-skills-vs-claude-md` and `video.json`'s `slug` follows. The demo link in `youtube.description` names the new folder; that made the composed description 5,003 bytes, so its first words went from 「想照著做：…都在」 to 「照著做：…在」.
- `brief.md`: the 大綱 section now offers two options the outline tool sends in full, D (recommended, the one the script follows) and E (the same results as three numbered points); the three options of 2026-10-09 are a short note. The first paragraphs carry the rename and the owner's two decisions of 2026-10-11.
- `claims.md` and the two task files point at the new folder. `runlog.txt` got a note about the rename and nothing else; recorded commands that name the old folder are as they were run.
