# Independent current-script verification, round 3: ai-bug-fix-pr-review

Review date: **2026-10-08, Asia/Taipei**. Reviewer: **bug_fix_fresh_verifier**, different from both the round-2 reviewer and the source-repair writer. This reviewer changed only this report in the repository; helpers and actual execution evidence stay outside it.

**Result: current text VERIFIED, with zero unresolved current factual claims.** This is a full review of the final 133-line / 28-scene source, not a delta-only acceptance. It verifies local demo behavior, retained display content and current official review mechanics. It does not verify historical Claude authorship, historical billing, existing media presence, audio, timing, rendered layout, owner listening, approval, upload or publication.

## Final binding and full coverage

| Item | Binding |
| --- | --- |
| `video.json` | 28840 bytes; SHA256 `7cddf570305b4afa8d87833aec8fac92ab3469648674fd6d17d085fd0dffe0d4` |
| `claims.md` | 3613 bytes; SHA256 `a0e439c36cd833291827c993c64e2ecd8d495fc83228b950fa93c3e7b434c983` |
| `brief.md` | 2226 bytes; SHA256 `511afa8537ca1807ccc84aa25019e0a055349ba1168bcf9f8dd73f2738d749c4` |
| `verify-2-20261008.md` | 59002 bytes; SHA256 `1a334293fabc98dbd262578002f4a546f25647b6c4b5fbb3e0d6b91b3eebd59d` |
| Coverage | 133 text entries; 0 say; 28 scenes; 112 visual-data strings; 7 title/description/tag entries; 3 thumbnail strings; 6 chapter labels: **261 entries** |
| Current verdicts | CONFIRMED 131; CHANGED 2; NOT FOUND 0; OUT OF SCOPE 128 |
| Final extraction | SHA256 `39c950ffe4d80d9177527da4e67508c25ed0523e1badf08f63fb372afc701a79` |
| Final private verdict table | SHA256 `9d2be57bc49a474ea9ec3aa0b5c40343dc3f580a6f79aa04d86fa3b5cefbb832` |
| Actual fresh replay/source receipt | SHA256 `37edaa812e09584cbbb2df55342df27c98915420e88fcf7a8b6e854e50236d69` |

`<repo>` denotes the checkout; `<evidence>` denotes this operation’s private `independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1` folder. These public logical paths reveal no user/machine path. The receipt retains actual argv, stdout/stderr, exit codes and timestamps with explicit ISO offsets. Recorded test times run from `2026-10-08T07:48:50.448705+08:00` through `2026-10-08T07:48:59.066297+08:00`; the offset, rather than a JSON field name, defines the time zone. No provider was invoked to reconstruct historical provenance.

The replay initially froze source `cc5c51a7985b88f5cae26c69d2cbaf43879f0f10a9b8fbef90fec5526459435b` and claims `09cb6c5df74572078d1ca2b32748178a5bd91176cd1aedbd35672f9a9acc140f`. The writer then corrected one spoken frequency-ranking claim and updated progress notes. The final extraction binds the two hashes above; scene IDs, line IDs and all unchanged content were compared again. The immutable first snapshot and final source/claims copies both remain in private evidence.

## Evidence and current official sources

| Key | Source | Verified scope and limits |
| --- | --- | --- |
| E1 | `<repo>/docs/videos/ai-bug-fix-pr-review/demo/` | Read actual baseline source, original two tests, stored patch, four-case acceptance, retained output text and PNG. Current demo bytes match round 2 exactly. Stored filenames containing Claude do not prove the tool author. |
| E2 | `<repo>/docs/videos/ai-coding-tools-same-task/demo/CHALLENGE.md` | Read the exact contract: preserve export/input guards; integer per-person amounts, total unchanged, gap <=1, remainder to earlier positions; built-in Node modules and expected files. This is the actual neighboring local challenge, not an official vendor specification. |
| E3 | `<evidence>/receipt.json`, five actual Node stdout/stderr pairs and private patched files | Independent new replay: baseline 2/2, baseline acceptance 1/4 with expected exit1, patched 13/13 with exit0. A strict unified-diff parser consumed the exact stored patch and matched every context/deleted line; no git or model command ran. |
| E4 | Retained `claude-acceptance-output.txt` and inspected `claude-acceptance.png` | Four test names, pass counts and displayed historical duration strings agree. PNG is a reflow of retained text, not an original terminal screenshot or a fresh-run duration claim. New replay timings differ normally. |
| E5 | [GitHub review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) | Fresh direct official HTTP200; supports commenting on changed lines, approval and requests for changes. The film’s three-gate recommendation is editorial, not a GitHub-mandated rule. |
| E6 | [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) | Fresh direct official HTTP200; current reference context only. It cannot certify the stored patch’s author or the missing historical CLI command, JSON, exit or cost. No version/price/limit claim is spoken. |
| ED | Current source and brief’s proposed teaching method | Questions, labels, personal recommendations, hypothetical risks and intent are marked OUT OF SCOPE rather than promoted into measured vendor/product facts. |

Both official requests used `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`, followed standard redirects and finished at the exact requested URLs with HTTP200. Raw body, headers and comment-stripped parsed text are retained. Parsing excludes script/style/template contents; it does not execute browser JavaScript or evaluate CSS.

| Source response | Observed ISO time | Body bytes / SHA256 | Text bytes / SHA256 |
| --- | --- | --- | --- |
| github-review | `2026-10-07T23:48:59.994139+00:00` | 135493 / `eb717cc3208ff89ee55fbd6dd8902b7040708b2a2b81956269ca3af53af82ec2` | 4051 / `e9561c377f094c0f21a3df582a65d556c96b04ecfbaa78b7e01f36bee4d55200` |
| claude-cli | `2026-10-07T23:49:01.108852+00:00` | 539027 / `918f104b0dd820eb969918624984175941b8bc2992abf2a66080bba51115a15a` | 39844 / `db92da1399e695d3a051eb70a46290fd391abe4a21c197582096aeb54d7fbc65` |

The GitHub page directly supports the two spoken mechanics and the matching slide. The current Claude page supports print/JSON/permission-mode flags, while allowed-tool prompt rules are not a historical execution or hard-sandbox proof. Neither official page proves who authored this retained local patch. Interface mechanics can change; recheck before future UI-specific instructions. Exact local behavior is pinned to the artifact bytes and Node binary.

## Fresh independent local replay

| Actual private command | Exit | Result |
| --- | ---: | --- |
| `<node> --test --test-reporter=spec --test-concurrency=1 fare.test.mjs` | 0 | 2 tests, 2 pass, 0 fail |
| `<node> --test --test-reporter=spec --test-concurrency=1 acceptance.test.mjs` on baseline | 1, expected | 4 tests, 1 pass, 3 fail |
| Exact retained unified diff applied in a private copy | no process exit; strict parser assertions passed | Only fare.mjs and fare.test.mjs; every hunk matches the actual baseline |
| `<node> --test --test-reporter=spec --test-concurrency=1` after patch | 0 | 13 tests, 13 pass, 0 fail: 9 patched-file tests plus 4 acceptance cases |
| Actual before/after example probes | 0 / 0 | 100/3: [33,33,33] -> [34,33,33]; 2/3: [1,1,1] -> [1,1,0]; patched2/5: [1,1,0,0,0]; patched0/4: [0,0,0,0] |

The actual property test loops over 501 totals (0..500 inclusive) and20 people counts (1..20 inclusive): **10,020 combinations**, checking length, sum and gap. It is neither every legal safe integer/count nor a formal proof. The extra patched test file separately covers sampled totals, integer shares, ordering and invalid inputs. The film’s shortened property-code display openly says it omits length checking; the underlying file includes it.

Input guard text is unchanged by the stored patch: total is a nonnegative safe integer; people is a safe integer1..100; invalid input raises RangeError before allocation. The patch replaces rounding with base/remainder allocation and adds seven tests to the original two. Post-hoc acceptance is disclosed by retained authored records; this new deterministic replay is not a blinded model trial, fresh Claude run, model ranking or real billing incident. The retained historical output’s exact original execution metadata remains unavailable; reproducibility confirms displayed behavior, not its missing historical command provenance.

| Frozen demo/challenge artifact | Bytes | SHA256 |
| --- | ---: | --- |
| `demo/fare.mjs` | 424 | `53a822df2b194a252cff62e52b2a0d7418d593537d54b13e054cb794eafc4665` |
| `demo/fare.test.mjs` | 322 | `3ec607b3f151af05ed49d4f2b5597e9bd5ff15c043794aa08d39083092a3ca19` |
| `demo/acceptance.test.mjs` | 1115 | `236c499487e47419157ee7d35bf443ccd95859fa95e0b07cbc6ae3e79302a1ba` |
| `demo/claude.patch` | 2738 | `3d793faef18e5508fe7825d57158a24a60c1c18c62c0ed75672ac2b99ca1db1a` |
| `demo/README.md` | 1097 | `27ff3863a258a7c31345e846d8d1d4eb751159472a5357144a7a2ce6b5379852` |
| `demo/claude-acceptance-output.txt` | 355 | `a74c7a10e44941233f10f52b22477c8f2be317d4a06b566f93e3be0c8bfbba1e` |
| `demo/claude-acceptance.png` | 45733 | `a0ab2d33e04606260f4c1a118013826a94f09db68c816b53527407bce699427a` |
| `../ai-coding-tools-same-task/demo/CHALLENGE.md` | 475 | `80a2ad6b1f3dd7bc6f6e819bc87007e21b2570ee53a683ece0b508b77895655a` |
| Bundled Node binary | private runtime | `3958e4bb3f2d4ef37c938215dfc65a9d3c9d839b5060fec103bd2345fa78e951` |

Original demo, challenge, brief and round-2 report were unchanged after this reviewer’s private replay. Historical readme/brief/comparison wording is retained as historical authored evidence; its Claude-attribution claims do not become independently confirmed merely because local tests pass.

## Nine content corrections and their dependency review

Before is the source bound to round2 (`a17181e2c1058d0582d5968bc2fa143668f86ab5af4f424f5af18a4114a04741`); after is the final source above. Every other current entry was reviewed too. All133 stable line IDs and28 scene IDs/order remain identical. Five spoken texts and four visual strings changed; no new scene, reveal, version, price, count, approval or historical execution claim was introduced.

| Where | Before -> after | Current review |
| --- | --- | --- |
| `v40017.text` | 接下來看 AI 真正交出的修補。 -> 接下來看一份可以重跑的本地修補。 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `patch-source.data.items[2]` | 實際 Claude Code 修補 -> 可重跑的本地修補 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `v40021.text` | 我用自己寫的分攤函式，讓 Claude Code 依照題目修改。 -> 這份本地分攤範例，留下了程式和測試的完整差異。 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `v40022.text` | 它改了程式和測試，工具自寫九個測試都通過。 -> 修補後的九個測試重跑全過，稍後再做事後驗收。 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `diff-core.data.caption` | 從實際 Claude Code 差異節錄 -> 從本地修補差異節錄 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `v4e3002.text` | 在函式裡，AI 把平均四捨五入換成基本分與餘數。 -> 這份修補把平均四捨五入，換成基本分與餘數。 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `red-first.data.right.points[0]` | 自寫 9 項通過 -> 修補測試 9 項通過 | Fresh reviewer requested clarification: says9 patched-file tests, without self-authorship attribution; actual9+4 pass. |
| `test-output.data.caption` | 同一示範的 Claude 修補；原始輸出重排，4／4 通過 -> 同一示範的本地修補；原始輸出重排，4／4 通過 | Local artifact/behavior description now supported by E1/E3; does not assert a verified tool author. |
| `v40109.text` | 尤其輸入驗證最容易在重寫時被無意刪掉。 -> 輸入驗證也可能在重寫時被無意刪掉。 | Fresh reviewer requested factual downgrade: unsupported highest-frequency ranking removed; current wording is a possible risk, not a measured ranking. |

Both source `checked_on` dates changed from2026-09-27 to2026-10-08 and are supported by actual HTTP200 captures. Current `claims.md` discloses missing original CLI provenance, distinguishes local behavior from authorship, states the post-hoc nature of acceptance and separates old media completion notes from current file/receipt presence. The historical brief still refers to Claude provenance; its immutable hash and teaching objective remain unchanged. Treat that attribution as historical planning context, not independent current execution proof.

Seven earlier attribution repairs were supplied by the writer before this formal third round. **This fresh reviewer identified and had the writer resolve two additional fact-dependent wordings** (self-written9-test slide; highest-frequency risk claim). Thus the >3-changes rule does not require a fourth reviewer for this round. The earlier >3 repair set has now received the required different person’s complete review. This report itself makes no source/claims edits. CHANGED below marks those two resolved findings, with exact before/after; it does not mean the current text is unresolved.

## Opinion, listener and verification limits

The three-gate advice and human decision agree with the brief’s teaching position. Title/thumbnail are a question and editorial checklist. The description explicitly describes a local reproducible demo. The opening AI scenario and general statement about tool-written tests (`v40085`) are a hypothetical review context/advice, not evidence that these9 stored tests have a proved Claude author. This distinction is maintained by the source-origin scene and current claims note. No official source contradicts the retained requirement contract; historical brief provenance is qualified as described above.

All133 narration texts are <=40 Unicode code points; there is no separate say, spoken URL or parentheses. Spoken Latin terms are AI, Bug, GitHub, PR, all present in the current pronunciation dictionary. Six chapter labels remain in order; there are no reveal directives. The data item「零元額分攤」is awkward wording, not a changed numeric claim; report-only style observation. No listener/audio/CPS/timing or layout acceptance is inferred from these checks.

The reviewer ran only a free local lint after final binding. Exact actual command: `<node> tools/video/cli.mjs lint --slug ai-bug-fix-pr-review`; exit0. Its output follows; estimates are planning values, not actual media duration, invoices or quota authorization.

```text
ai-bug-fix-pr-review: 0 errors, 0 warnings

Estimate: 10.2 min, 133 lines, 2286 spoken units
Azure billable characters (estimate): 8821, 1.8% of the free tier's 500,000 a month
Chapters (estimated times):
  00:00 綠燈也會漏
  00:18 綠燈不等於正確
  01:47 第一關：需求契約
  03:35 第二關：讀差異
  05:54 第三關：跑回歸
  07:57 合併前的決定
```

Lint stdout SHA256 `6c3bea131762e57bae3955d91ebbbdd91074033fbad2a1be96d75ac0ddee5fe3`; stderr SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. No TTS, ASR, native review/server mutation, hold change, paid provider, media generation, owner-approval action or upload ran in this review. Historical9/28 film/audio completion notes and root’s current render attempts are outside this textual verdict. Locate and bind actual media or use the authorized production flow before claiming audio/final/ready status.

## Full current entry table

Each of261 current entries is listed, including unchanged sentences, all28 scenes and all visual strings. CONFIRMED and resolved CHANGED refer only to the stated evidence scope. OUT OF SCOPE denotes editorial labels/advice/questions/intent, not a hidden missing factual number. Exact Unicode values and full source/claims bindings remain in the private extraction/verdict JSON.

| # | Current entry | Where | Evidence / URL | HTTP | Verdict | Before -> after |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | AI 修好 Bug 就能合併？三個 PR 檢查點 | `youtube.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 2 | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 | `youtube.description` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 3 | AI code review | `youtube.tags[0]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 4 | PR review | `youtube.tags[1]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 5 | Bug fix | `youtube.tags[2]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 6 | 程式碼審查 | `youtube.tags[3]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 7 | 回歸測試 | `youtube.tags[4]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 8 | AI 修補審查 | `thumbnail.data.tag` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 9 | 測試綠了？<br>**先過 3 關** | `thumbnail.data.headline` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 10 | 需求／差異／回歸 | `thumbnail.data.sub` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 11 | 綠燈也會漏 | `opening.chapter` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 12 | AI 修補審查 | `opening.data.tag` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 13 | 測試全綠，還少一分 | `opening.data.title` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 14 | 合併前先過三道關 | `opening.data.subtitle` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 15 | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | `v40000.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 16 | AI 送來一份修補程式，你會直接合併嗎？ | `v40001.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 17 | 我帶你看需求、差異與回歸，三道關都要過。 | `v40002.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 18 | 我們先從那一分為什麼消失開始。 | `v40003.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 19 | 綠燈不等於正確 | `why-green.chapter` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 20 | 第一個畫面 | `why-green.data.kicker` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 21 | 2 個測試通過 | `why-green.data.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 22 | 但不代表需求被測完 | `why-green.data.sub` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 23 | 第一個舊測試，只檢查能整除的金額。 | `v40007.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 24 | 人數不合法也會擋，兩個結果都是綠色。 | `v40008.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 25 | 不整除的路徑沒人問，所以錯誤藏得好好的。 | `v40009.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 26 | 這次示範是真正執行的檔案，不是想像案例。 | `v40010.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 27 | 它證明程式照舊測試運作，沒有證明帳算對。 | `v40011.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 28 | 綠燈實際測了什麼 | `old-test-code.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 29 | javascript | `old-test-code.data.language` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 30 | assert.deepEqual(splitFareCents(120, 3),<br>  [40, 40, 40]);<br>assert.throws(() => splitFareCents(100, 0),<br>  RangeError); | `old-test-code.data.code` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 31 | 原本只有整除和非法人數兩題 | `old-test-code.data.caption` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 32 | 這是起始專案真的跑過的兩個測試。 | `v4e1000.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 33 | 第一個測一百二十分，三人平均分。 | `v4e1001.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 34 | 第二個測零人時要拋出錯誤。 | `v4e1002.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 35 | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | `v4e1003.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 36 | 漏掉的案例 | `bug-example.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 37 | javascript | `bug-example.data.language` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 38 | splitFareCents(100, 3)<br>// 原本得到 [33, 33, 33]<br>// 總和 99，少了 1 | `bug-example.data.code` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 39 | 起始程式與事後測試實際輸出 | `bug-example.data.caption` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 40 | 分一百分給三個人，原始程式回三個三十三。 | `v40014.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 41 | 這不是顯示格式的問題，總和真的少了一分。 | `v40015.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 42 | 如果少掉的一分錢會記入帳務，就算測試全綠也不能合併。 | `v40016.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 43 | 接下來看一份可以重跑的本地修補。 | `v40017.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | 接下來看 AI 真正交出的修補。 -> 接下來看一份可以重跑的本地修補。 |
| 44 | 這個失敗結果已寫進可重跑的驗收檔案。 | `v40018.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 45 | 這份示範的來源 | `patch-source.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 46 | 自有小型程式 | `patch-source.data.items[0]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 47 | 同一句明確需求 | `patch-source.data.items[1]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 48 | 可重跑的本地修補 | `patch-source.data.items[2]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | 實際 Claude Code 修補 -> 可重跑的本地修補 |
| 49 | 這份本地分攤範例，留下了程式和測試的完整差異。 | `v40021.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | 我用自己寫的分攤函式，讓 Claude Code 依照題目修改。 -> 這份本地分攤範例，留下了程式和測試的完整差異。 |
| 50 | 修補後的九個測試重跑全過，稍後再做事後驗收。 | `v40022.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | 它改了程式和測試，工具自寫九個測試都通過。 -> 修補後的九個測試重跑全過，稍後再做事後驗收。 |
| 51 | 這不是正式站的事故，也不是已合併的真實 PR。 | `v40023.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 52 | 它是可以公開重跑的一份本地修補案例。 | `v40024.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 53 | 所以它適合用來練審查，卻不能代表產品事故。 | `v40025.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 54 | 第一關：需求契約 | `gate-one.chapter` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 55 | 先問：修的是哪個需求？ | `gate-one.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 56 | 第一關，不要先看 AI 說它完成了什麼。 | `v40028.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 57 | 先把需求寫成你可以算得出來的條件。 | `v40029.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 58 | 這題要保留輸入規則，不能只修一個範例。 | `v40030.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 59 | 也不能悄悄把分配規則改成另一種做法。 | `v40031.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 60 | 第一關的答案，應該能不靠工具自己口述。 | `v40032.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 61 | 需求契約四條 | `contract.data.title` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 62 | 長度 | `contract.data.steps[0].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 63 | 每人一個整數金額 | `contract.data.steps[0].detail` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 64 | 總和 | `contract.data.steps[1].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 65 | 加起來等於原金額 | `contract.data.steps[1].detail` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 66 | 差額 | `contract.data.steps[2].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 67 | 最多相差一分 | `contract.data.steps[2].detail` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 68 | 順序 | `contract.data.steps[3].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 69 | 餘數先給前面的人 | `contract.data.steps[3].detail` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 70 | 第一條，結果長度要和人數一樣。 | `v40035.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 71 | 第二條，所有人的份額加總，必須等於原來金額。 | `v40036.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 72 | 第三條，任何兩人最多只差一分。 | `v40037.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 73 | 第四條，有餘數時，前面的人先分到。 | `v40038.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 74 | 四條放在一起，才描述完整的分攤行為。 | `v40039.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 75 | 如果只補一百除三，還會漏掉其他金額。 | `v40040.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 76 | 再代一組 | `small-remainder.data.kicker` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 77 | 2 分給 3 人 | `small-remainder.data.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 78 | 正確結果：1、1、0 | `small-remainder.data.sub` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 79 | 只測一百分除三，還可能把規則寫死在特例上。 | `v4e2000.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 80 | 再代入兩分給三個人，正確是前兩位各一分。 | `v4e2001.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 81 | 第三位拿零分，總和仍是兩分。 | `v4e2002.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 82 | 這組資料會立刻露出四捨五入重複分配的問題。 | `v4e2003.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 83 | 原有輸入規則也算契約 | `inputs.data.title` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 84 | 總額：非負安全整數 | `inputs.data.items[0]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 85 | 人數：1 到 100 | `inputs.data.items[1]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 86 | 非法輸入：RangeError | `inputs.data.items[2]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 87 | 還有原本就存在的輸入檢查。 | `v40042.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 88 | 總額不能是負數、小數或超過安全整數。 | `v40043.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 89 | 人數只能是一到一百之間的安全整數。 | `v40044.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 90 | 修補若刪掉這些檢查，就算範例變對也不能過關。 | `v40045.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 91 | 它們不是額外加分題，而是修補前就有的規則。 | `v40046.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 92 | 一個例子，看四個條件 | `contract-case.data.title` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 93 | 原本 | `contract-case.data.left.heading` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 94 | 33、33、33 | `contract-case.data.left.points[0]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 95 | 總和 99 | `contract-case.data.left.points[1]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 96 | 需求 | `contract-case.data.right.heading` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 97 | 34、33、33 | `contract-case.data.right.points[0]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 98 | 總和 100 | `contract-case.data.right.points[1]` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 99 | 把一百分除以三，理想結果是三十四、三十三、三十三。 | `v40049.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 100 | 這組數字同時檢查總和與餘數順序。 | `v40050.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 101 | 只測每個人差不多，還是不夠。 | `v40051.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 102 | 需求契約先寫清楚，才有審查的尺。 | `v40052.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 103 | 換成兩分三人，正確順序也是一、一、零。 | `v40053.text` | E1/E2/E3; exact challenge, input guards and private replay | LOCAL | CONFIRMED | unchanged |
| 104 | 第二關：讀差異 | `gate-two.chapter` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 105 | 逐行看它改了什麼 | `gate-two.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 106 | 第二關，打開實際差異，不只讀工具的完成訊息。 | `v40056.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 107 | 先確認它只改到預期的程式和測試。 | `v40057.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 108 | 接著把新增邏輯代入一百分除三的例子。 | `v40058.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 109 | 最後看它有沒有刪掉原來的保護條件。 | `v40059.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 110 | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | `v40060.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 111 | 修補的核心四行 | `diff-core.data.title` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 112 | javascript | `diff-core.data.language` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 113 | const base = Math.floor(totalCents / people);<br>const remainder = totalCents - base * people;<br>return Array.from({ length: people }, (_, i) =><br>  i < remainder ? base + 1 : base); | `diff-core.data.code` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 114 | 從本地修補差異節錄 | `diff-core.data.caption` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | 從實際 Claude Code 差異節錄 -> 從本地修補差異節錄 |
| 115 | 這份修補先算每人最少要拿多少。 | `v40063.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 116 | 再算剩下幾分，要補給幾位前面的人。 | `v40064.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 117 | 總額一百，分給三人，各拿三十三，還剩一分錢。 | `v40065.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 118 | 第一位多拿一分，其餘兩位維持三十三。 | `v40066.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 119 | 用兩分三人再代一次，就能看到前兩位各多一分。 | `v40067.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 120 | 新邏輯前面的檢查還在 | `validation-stays.data.title` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 121 | 總額先驗證 | `validation-stays.data.items[0]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 122 | 人數先驗證 | `validation-stays.data.items[1]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 123 | 只替換分配算法 | `validation-stays.data.items[2]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 124 | 完整差異顯示，函式前兩段輸入檢查仍然保留。 | `v4e3000.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 125 | 非法金額和非法人數，仍會在分配前被擋。 | `v4e3001.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 126 | 這份修補把平均四捨五入，換成基本分與餘數。 | `v4e3002.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | 在函式裡，AI 把平均四捨五入換成基本分與餘數。 -> 這份修補把平均四捨五入，換成基本分與餘數。 |
| 127 | 這是這份本地差異的範圍，不替其他檔案背書。 | `v4e3003.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 128 | 讀差異時看三處 | `diff-check.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 129 | 輸入驗證保留嗎？ | `diff-check.data.items[0]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 130 | 有改題目以外的檔嗎？ | `diff-check.data.items[1]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 131 | 新測試在驗什麼？ | `diff-check.data.items[2]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 132 | 我在差異裡先找原有驗證，這次沒有被刪掉。 | `v40070.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 133 | 再看檔案清單，只有程式和測試被修改。 | `v40071.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 134 | 新增測試涵蓋不整除、零金額和非法輸入。 | `v40072.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 135 | 這些都是看得見的證據，不是工具的口頭保證。 | `v40073.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 136 | 如果它順手改了部署或帳務設定，應該另外討論。 | `v40074.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 137 | 新增測試也要看斷言，不只看測試名稱。 | `v40075.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 138 | 新測試要讀斷言 | `test-assertions.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 139 | javascript | `test-assertions.data.language` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 140 | assert.deepEqual(splitFareCents(100, 3),<br>  [34, 33, 33]);<br>assert.deepEqual(splitFareCents(2, 5),<br>  [1, 1, 0, 0, 0]); | `test-assertions.data.code` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 141 | 這兩個斷言存在實際修補測試 | `test-assertions.data.caption` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 142 | 新增測試不能只看名字，要看它到底斷言什麼。 | `v4e4000.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 143 | 這份修補測到一百分除三，是三十四、三十三、三十三。 | `v4e4001.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 144 | 也測到兩分分五人，前兩位各一分，其餘拿零。 | `v4e4002.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 145 | 這兩組一起看，比只看測試數量更有意義。 | `v4e4003.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 146 | 範圍說明 | `not-real-pr.data.kicker` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 147 | 本地 patch | `not-real-pr.data.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 148 | 沒有真實 PR 審核紀錄 | `not-real-pr.data.sub` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 149 | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | `v40077.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 150 | 真正的專案還要看相關模組、型別與維運影響。 | `v40078.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 151 | 如果這段程式連著付款系統，範圍會更大。 | `v40079.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 152 | 影片示範的方法，可以帶進真正的審查流程。 | `v40080.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 153 | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | `v40081.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 154 | 第三關：跑回歸 | `gate-three.chapter` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 155 | 測試要能抓到原本的錯 | `gate-three.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 156 | 第三關，把修補放進另外寫的事後驗收。 | `v40084.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 157 | 工具自己寫的測試有用，但不能是唯一標準。 | `v40085.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 158 | 好的驗收測試，應該先在舊版程式重現這個錯誤。 | `v40086.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 159 | 所以我先拿舊碼跑同一份事後驗收。 | `v40087.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 160 | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | `v40088.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 161 | 先紅、再綠 | `red-first.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 162 | 舊碼 | `red-first.data.left.heading` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 163 | 2 個舊測試通過 | `red-first.data.left.points[0]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 164 | 事後 4 類只過 1 類 | `red-first.data.left.points[1]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 165 | 修補 | `red-first.data.right.heading` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 166 | 修補測試 9 項通過 | `red-first.data.right.points[0]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CHANGED | 自寫 9 項通過 -> 修補測試 9 項通過 |
| 167 | 事後 4 類全通過 | `red-first.data.right.points[1]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 168 | 舊碼雖然兩個原測試全過，事後四類只過一類。 | `v40091.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 169 | 這證明新驗收能抓到我們要修的缺陷。 | `v40092.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 170 | 換成修補後，四類事後驗收全通過。 | `v40093.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 171 | 這才是比較有力的紅燈到綠燈證據。 | `v40094.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 172 | 這一步能排除只檢查舊有整除案例的假安全感。 | `v40095.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 173 | 不只測一組數字 | `property.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 174 | javascript | `property.data.language` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 175 | for (let total = 0; total <= 500; total += 1) {<br>  for (let people = 1; people <= 20; people += 1) {<br>    const shares = splitFareCents(total, people);<br>    const sum = shares.reduce((a, b) => a + b, 0);<br>    assert.equal(sum, total);<br>    assert.ok(Math.max(...shares) - Math.min(...shares) <= 1);<br>  }<br>} | `property.data.code` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 176 | 驗收邏輯節錄（畫面改寫、省略長度檢查） | `property.data.caption` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 177 | 驗收不是只寫一百除三。 | `v40098.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 178 | 我還把零到五百的總額，搭配一到二十人跑過。 | `v40099.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 179 | 每組都檢查總和，並確認最大差距不超過一分。 | `v40100.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 180 | 這種性質檢查，能抓到你沒想到的餘數組合。 | `v40101.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 181 | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | `v40102.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 182 | 超出測試範圍的風險，要再根據業務補案例。 | `v40103.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 183 | 事後驗收的實際輸出 | `test-output.data.title` | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution | LOCAL | CONFIRMED | unchanged |
| 184 | docs/videos/ai-bug-fix-pr-review/demo/claude-acceptance.png | `test-output.data.image` | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution | LOCAL | CONFIRMED | unchanged |
| 185 | 同一示範的本地修補；原始輸出重排，4／4 通過 | `test-output.data.caption` | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution | LOCAL | CONFIRMED | 同一示範的 Claude 修補；原始輸出重排，4／4 通過 -> 同一示範的本地修補；原始輸出重排，4／4 通過 |
| 186 | 這是同一份修補在本機跑出的驗收輸出。 | `v4shot0.text` | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution | LOCAL | CONFIRMED | unchanged |
| 187 | 四項綠燈有紀錄，但還要對照需求與完整差異。 | `v4shot1.text` | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution | LOCAL | CONFIRMED | unchanged |
| 188 | 性質測試逐組查三件事 | `property-check.data.title` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 189 | 人數 | `property-check.data.steps[0].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 190 | 輸出長度相同 | `property-check.data.steps[0].detail` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 191 | 總額 | `property-check.data.steps[1].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 192 | 各份額加總不變 | `property-check.data.steps[1].detail` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 193 | 差距 | `property-check.data.steps[2].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 194 | 最大與最小最多差一 | `property-check.data.steps[2].detail` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 195 | 回圈跑每組數字時，不只看總額。 | `v4e5000.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 196 | 它還比對輸出長度，確認沒有漏掉任何人。 | `v4e5001.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 197 | 再找最大和最小份額，差距不能超過一。 | `v4e5002.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 198 | 這三個斷言對每組資料都成立，才算這關通過。 | `v4e5003.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 199 | 再保護原本沒壞的地方 | `inputs-test.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 200 | 零元額分攤 | `inputs-test.data.items[0]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 201 | 總額非法輸入 | `inputs-test.data.items[1]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 202 | 人數非法輸入 | `inputs-test.data.items[2]` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 203 | 零金額要回傳每人零分，不能拋出莫名錯誤。 | `v40105.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 204 | 負數、小數或超大總額，仍然要被拒絕。 | `v40106.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 205 | 零人、超過一百人和小數人數也是一樣。 | `v40107.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 206 | 回歸的意思，就是修新 Bug 也守住舊契約。 | `v40108.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 207 | 輸入驗證也可能在重寫時被無意刪掉。 | `v40109.text` | ED; unsupported frequency ranking removed; general risk caution only | LOCAL | CHANGED | 尤其輸入驗證最容易在重寫時被無意刪掉。 -> 輸入驗證也可能在重寫時被無意刪掉。 |
| 208 | 合併前的決定 | `three-gates.chapter` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 209 | 三道關缺一不可 | `three-gates.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 210 | 把需求、程式差異和回歸測試一起看。 | `v40112.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 211 | 需求契約告訴你什麼叫修好。 | `v40113.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 212 | 差異讓你知道實際改了哪些檔、哪些行。 | `v40114.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 213 | 回歸則證明新舊規則至少在測試範圍內成立。 | `v40115.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 214 | 只缺一道關，審查紀錄就不完整。 | `v40116.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 215 | 準備合併時記下證據 | `review-summary.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 216 | 需求 | `review-summary.data.steps[0].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 217 | 總和、差額、順序、輸入 | `review-summary.data.steps[0].detail` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 218 | 差異 | `review-summary.data.steps[1].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 219 | 兩個預期檔案 | `review-summary.data.steps[1].detail` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 220 | 測試 | `review-summary.data.steps[2].title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 221 | 舊碼紅、修補綠 | `review-summary.data.steps[2].detail` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 222 | 我會在審查紀錄裡放三件事。 | `v40119.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 223 | 第一，需求有哪些明確的驗收條件。 | `v40120.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 224 | 第二，實際差異只改了哪些地方。 | `v40121.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 225 | 第三，哪個測試先紅、修補後又如何變綠。 | `v40122.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 226 | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | `v40123.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 227 | 交給審查者的最小證據 | `review-record.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 228 | 失敗案例與需求 | `review-record.data.items[0]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 229 | 完整差異 | `review-record.data.items[1]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 230 | 重跑指令與測試結果 | `review-record.data.items[2]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 231 | 最後把那個原本失敗的案例寫在審查摘要裡。 | `v4e6000.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 232 | 附上完整差異，不只貼兩行好看的核心程式。 | `v4e6001.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 233 | 再列出重跑指令與通過的測試範圍。 | `v4e6002.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 234 | 下一位審查者不必相信口頭報告，能自己驗證。 | `v4e6003.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 235 | 仍要人判斷的地方 | `limits.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 236 | 需求本身正確嗎？ | `limits.data.items[0]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 237 | 改動範圍完整嗎？ | `limits.data.items[1]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 238 | 風險與回滾可接受嗎？ | `limits.data.items[2]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 239 | 這個小型示範雖然通過驗收，仍不能代替真實業務判斷。 | `v40126.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 240 | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | `v40127.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 241 | 還要有人看改動範圍、資料影響和回滾方式。 | `v40128.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 242 | 負責合併的人，得對這個判斷負責。 | `v40129.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 243 | 合併不是模型替團隊作的事，而是負責者作的決定。 | `v40130.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 244 | 真實團隊流程 | `github.data.kicker` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 245 | 留下可追溯的審查 | `github.data.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 246 | 看差異、留言、要求修改或核准 | `github.data.sub` | E5; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart | 200 | CONFIRMED | unchanged |
| 247 | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | `v40133.text` | E5; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart | 200 | CONFIRMED | unchanged |
| 248 | 也可以要求修改，或在看過證據後核准。 | `v40134.text` | E5; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart | 200 | CONFIRMED | unchanged |
| 249 | 這裡不替任何真實 PR 點核准。 | `v40135.text` | E1/E3; exact local baseline/patch/test artifacts and independent private replay | LOCAL | CONFIRMED | unchanged |
| 250 | 重點是讓下一位審查者找到同一份證據。 | `v40136.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 251 | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | `v40137.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 252 | AI 修好 Bug，就能合併嗎？ | `outro.data.title` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 253 | 拿三關清單檢查你的下一個修補 | `outro.data.cta` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 254 | 需求契約 | `outro.data.lines[0]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 255 | 實際差異 | `outro.data.lines[1]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 256 | 回歸測試 | `outro.data.lines[2]` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 257 | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | `v40140.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 258 | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | `v40141.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 259 | 這次的起始碼、修補和測試，要放在一起核對。 | `v40142.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 260 | 拿你下一個小修補照著試一次，比背規則更有用。 | `v40143.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
| 261 | 這個小練習之後，再把同一方法用到較大的改動。 | `v40144.text` | ED; brief and explicitly proposed three-gate editorial method | LOCAL | OUT OF SCOPE | unchanged |
