# Independent verification, round 1: ai-coding-tools-same-task

Checked on 2026-09-27. I did not write this script. The table enumerates every extracted narration, say, slide-data, thumbnail, title, description and tag entry; repeated facts are counted per entry, not as unique research questions. Original extraction and helper code remain in the local independent-verification workdir outside Git.

## Summary

- Extracted entries: 177; CONFIRMED 110, CHANGED 9, NOT FOUND 0, OUT OF SCOPE 58. Four distinct factual corrections: initial test coverage, post-run authorship of acceptance tests, Gemini login attribution, and inaccessible demonstration links. **Second independent round required** (>3 factual changes).
- Local replay: Claude 13/13 total (9 self-authored + 4 acceptance); Codex 9/9 (5 + 4). Gemini baseline 3/6 (2 original + 1/4 acceptance), with no Gemini patch. The baseline failures are not a Gemini model result. Raw CLI error reports `IneligibleTierError: UNSUPPORTED_CLIENT`. Google's [specific deprecation page](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals), last updated 2026-09-02, says Gemini CLI stopped accepting Google sign-in for individual free, Pro and Ultra tiers on 2026-06-18; enterprise access remains. The Gemini CLI general authentication guide still lists individual sign-in, so the official pages conflict. The dated, specific deprecation statement and matching local error govern this video.
- The acceptance file was written and copied after the three CLI runs: local result logs finish by 23:33:18 and acceptance copies were created at 23:34:11 or later; the author also confirmed this chronology. It is an independent post-run check, **not a preregistered blind test**. Those timestamps are local provenance, not an immutable audit log.
- Vendor names and auth availability can change. Official pages observed 2026-09-27/28: [Claude CLI](https://code.claude.com/docs/en/cli-reference) HTTP 200, [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) HTTP 200, [Gemini specific deprecation](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals) HTTP 200, [Gemini team's announcement](https://github.com/google-gemini/gemini-cli/discussions/28017) HTTP 200. The [general Gemini authentication guide](https://geminicli.com/docs/get-started/authentication/) also returned 200 but contradicts the deprecation. Recheck versions, login behavior and any price before recording/publication.
- Opinion pass: the no-ranking, run-your-own-small-task stance agrees with brief.md. Listener pass: zero lines over 40 Unicode characters; Claude Code, Codex, Gemini CLI and token occur in the pronunciation dictionary. No spoken URLs or parenthetical citations. Chapter/reveal order is coherent.
- Lint after edits: 0 errors, 0 warnings; 8.3 minute estimate, 105 lines, 1883 spoken units. Actual TTS duration and eleven-point rendered-video QA remain outstanding; estimate may run short of the 8-minute target.
- Publication gate: the source guide article does not contain these new demo files, and the current upload description has no public demo URL. False spoken/link promises were removed. Add and click-check an actual public demo link in the final upload pack if viewers are to reproduce this exact run.
- Suspected but not changed: single-run wall times and tool-reported token/cost values are not cross-account product benchmarks; actual invoices were not inspected. Raw local CLI records remain outside Git and are not available to viewers.

## Full claim table

**2026-09-28 correction:** The c6 source interpretation in the first-pass table is superseded by Google's dated [deprecation page](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals). It confirms the individual Google-login discontinuation; API-key and Standard/Enterprise paths remain separate. The video author is updating the Gemini narration and claims. Earlier scene-index references describe the 21-scene draft; the addendum below identifies new scenes by stable ID.

| # | Claim before review | Where | URL / evidence | HTTP | Verdict | Before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Claude Code、Codex、Gemini CLI 同題實測：兩支修好，一支卡登入 | youtube.title | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; https://geminicli.com/docs/get-started/authentication/; local runs (metadata or editorial framing) | 200, 200, 200; LOCAL | CONFIRMED | - |
| 2 | 三支 AI 程式工具接同一個小型任務，真實結果是兩支完成、一支卡在登入。開發者可以跟著起始檔、差異與事後驗收，建立自己的比較方法。<br>這是一次小型實作示範，預設模型與帳戶條件不同，不當成能力排名；用量估算也不是實際帳單。 | youtube.description | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 3 | Claude Code | youtube.tags[0] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 4 | Codex | youtube.tags[1] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 5 | Gemini CLI | youtube.tags[2] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 6 | AI coding tools | youtube.tags[3] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 7 | 程式代理 | youtube.tags[4] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 8 | 實測與選工具 | scenes[0].data.tag | local artifact / editorial (comparison.md + local CLI logs) | LOCAL / N/A | OUT OF SCOPE | - |
| 9 | 同一題，三支工具 | scenes[0].data.title | local artifact / editorial (comparison.md + local CLI logs) | LOCAL / N/A | CONFIRMED | - |
| 10 | 兩支修好，一支卡在登入 | scenes[0].data.subtitle | local artifact / editorial (comparison.md + local CLI logs) | LOCAL / N/A | CONFIRMED | - |
| 11 | 三支工具做同一題，兩支修好、一支卡登入。 | v30000.text | local artifact / editorial (comparison.md + local CLI logs) | LOCAL / N/A | CONFIRMED | - |
| 12 | 一起看差異和測試，再決定哪支適合你。 | v30001.text | local artifact / editorial (comparison.md + local CLI logs) | LOCAL / N/A | OUT OF SCOPE | - |
| 13 | 先看真實結果，再談選擇。 | v30002.text | local artifact / editorial (comparison.md + local CLI logs) | LOCAL / N/A | OUT OF SCOPE | - |
| 14 | 先說清楚 | scenes[1].data.kicker | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 15 | 這不是排行榜 | scenes[1].data.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 16 | 只有一次、小型、帳戶不同 | scenes[1].data.sub | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 17 | 先講限制：這只是一次小型試跑，不是能力排名。 | v30007.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 18 | 三支工具的預設模型、權限和帳戶條件都不同。 | v30008.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 19 | 所以我不會用秒數說哪一支比較聰明。 | v30009.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 20 | 真正要學的是，怎麼把自己的試跑設計得可核對。 | v30010.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 21 | 你最好先把這個方法套在自己的工作上，再決定付費。 | v30011.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 22 | 綠燈卻少了一分 | scenes[2].data.title | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 23 | 題目很小，把一筆整數分給幾個人。 | v30014.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 24 | 一百個分，分給三人，總和仍要是一百。 | v30015.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 25 | 多出來的分，要依照陣列順序先給前面的人。 | v30016.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 26 | 這個規則簡單到能一眼看懂，也容易抓錯。 | v30017.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 27 | 如果最後算不回原來的總額，這個函式就沒有完成工作。 | v30018.text | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 28 | 原本的分攤程式 | scenes[3].data.title | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 29 | javascript | scenes[3].data.language | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 30 | const each = Math.round(totalCents / people);<br>return Array(people).fill(each); | scenes[3].data.code | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 31 | 原本兩個測試都會通過 | scenes[3].data.caption | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 32 | 原本程式先除人數，再把同一個數字給每個人。 | v30021.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 33 | 整除的時候沒事，不整除就可能多分或少分。 | v30022.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 34 | 更有趣的是，起始的兩個測試都是綠燈。 | v30023.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 35 | 它們只測整除，沒有測最會出錯的餘數。 | v30024.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CHANGED | 它們只測整除，沒有測最會出錯的餘數。 -> 一個測整除，一個測非法人數，都沒測餘數。 |
| 36 | 方法很直觀，所以也能清楚看見錯在哪一行。 | v30025.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 37 | 起始問題 | scenes[4].data.kicker | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 38 | 100 ÷ 3 | scenes[4].data.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 39 | 原本輸出 33、33、33；合計 99 | scenes[4].data.sub | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 40 | 直接代入一百分、三個人，原本輸出是三十三、三十三、三十三。 | v30028.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 41 | 加起來只有九十九，一分不見了。 | v30029.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 42 | 這是接下來三支工具收到的同一個問題。 | v30030.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 43 | 如果只看舊測試的綠燈，你會錯過它。 | v30031.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 44 | 這一分如果是旅伴共同分帳，就會變成真實爭議。 | v30032.text | local artifact / editorial (demo/fare.mjs + demo/fare.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 45 | 公平起點至少固定這三樣 | scenes[5].data.title | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 46 | "相同起始檔案" | scenes[5].data.items[0] | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 47 | "相同題目文字" | scenes[5].data.items[1] | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 48 | "相同事後驗收" | scenes[5].data.items[2] | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 49 | 我把同一份起始檔案，複製到三個空資料夾。 | v30035.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 50 | 三邊收到的提示文字完全相同。 | v30036.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 51 | 工具執行完才放入事後驗收，避免偷看到答案。 | v30037.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CHANGED | 工具執行完才放入事後驗收，避免偷看到答案。 -> 工具都執行完，我才另外寫一份事後驗收。 |
| 52 | 這樣至少能知道每次改動從哪裡開始。 | v30038.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | OUT OF SCOPE | - |
| 53 | 我也沒有把個人帳單或真實旅客資料放進示範。 | v30039.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 54 | 三份起點都先提交，才能比對改過的地方。 | v30040.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 55 | 共同題目 | scenes[6].data.title | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 56 | text | scenes[6].data.language | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | OUT OF SCOPE | - |
| 57 | Read CHALLENGE.md and complete the task.<br>Report what changed and the test result. | scenes[6].data.code | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 58 | 三支 CLI 都收到同一句提示 | scenes[6].data.caption | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 59 | 真正的題目寫在同一份挑戰檔裡。 | v30042.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 60 | 它要求保留輸入驗證，總和必須精準，差額最多一分。 | v30043.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 61 | 還要把多餘的分，依序給前面的人。 | v30044.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 62 | 最後請工具自己加測試，並回報測試結果。 | v30045.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 63 | 輸入驗證的規則也寫清楚，不讓工具自己猜。 | v30046.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 64 | 同一題，實際跑一次 | scenes[7].data.title | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 65 | 現在看實際結果，我會把不能比較的地方一起講。 | v30049.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | OUT OF SCOPE | - |
| 66 | 本機跑的是當天已安裝的三支命令列工具。 | v30050.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 67 | 原始紀錄留在工作資料夾，公開差異放在示範包。 | v30051.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CHANGED | 原始紀錄留在工作資料夾，公開差異放在示範包。 -> 原始紀錄留在工作資料夾，兩份差異放在示範包。 |
| 68 | 這段沒有把別人的網路評測拿來當我的實測。 | v30052.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 69 | 以下每個數字都只屬於這次操作，不是廠商承諾。 | v30053.text | local artifact / editorial (comparison.md + local file timestamps + author confirmation) | LOCAL / N/A | CONFIRMED | - |
| 70 | Claude Code：完成修補 | scenes[8].data.title | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 71 | "改程式和測試" | scenes[8].data.items[0] | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 72 | "自寫測試 9 項通過" | scenes[8].data.items[1] | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 73 | "事後驗收 4 項通過" | scenes[8].data.items[2] | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 74 | Claude Code 在這次執行中，改了程式和測試。 | v30056.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 75 | 它把總額分成商數與餘數，前面的人拿多的一分。 | v30057.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 76 | 工具自寫的九個測試通過，事後四類驗收也通過。 | v30058.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 77 | 這只能說它完成了這一題，不能推論別的題。 | v30059.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 78 | 請留意，工具自寫測試的數量不是測試品質分數。 | v30060.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 79 | 第一份實際差異 | scenes[9].data.title | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 80 | javascript | scenes[9].data.language | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 81 | const base = Math.floor(totalCents / people);<br>const remainder = totalCents - base * people;<br>return Array.from({ length: people }, (_, i) =><br>  i < remainder ? base + 1 : base); | scenes[9].data.code | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 82 | 節錄自實際 Claude Code patch | scenes[9].data.caption | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 83 | 看它的核心差異：先取每人的基本分，再算剩餘幾分。 | v30063.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 84 | 陣列前面的索引先拿到那一分。 | v30064.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 85 | 原來的非法輸入檢查沒有被刪掉。 | v30065.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 86 | 你可以拿公開的完整差異，逐行自己看。 | v30066.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | CHANGED | 你可以拿公開的完整差異，逐行自己看。 -> 完整差異不能只看核心四行，也要逐行檢查。 |
| 87 | 分配規則看起來短，但總額不變才是主要契約。 | v30067.text | local artifact / editorial (demo/claude.patch + local Claude result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 88 | Codex：也完成修補 | scenes[10].data.title | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 89 | "改同兩個檔案" | scenes[10].data.items[0] | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 90 | "自寫測試 5 項通過" | scenes[10].data.items[1] | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 91 | "事後驗收 4 項通過" | scenes[10].data.items[2] | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 92 | Codex 也改了同樣的兩個檔案。 | v30070.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 93 | 它用取餘數的寫法分配，核心條件相同。 | v30071.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 94 | 工具自寫的五個測試通過，事後四類驗收也通過。 | v30072.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 95 | 測試項目數不同，不等於其中一支比較可靠。 | v30073.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 96 | 我仍然會檢查它有沒有順手改掉題目外的內容。 | v30074.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 97 | 第二份實際差異 | scenes[11].data.title | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 98 | javascript | scenes[11].data.language | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 99 | const remainder = totalCents % people;<br>const each = (totalCents - remainder) / people;<br>return Array.from({ length: people }, (_, i) =><br>  each + (i < remainder ? 1 : 0)); | scenes[11].data.code | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 100 | 節錄自實際 Codex patch | scenes[11].data.caption | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 101 | 第二份差異先取餘數，再算基本分。 | v30077.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 102 | 這兩種寫法在我們的驗收範圍內，都保住了總額。 | v30078.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | CONFIRMED | - |
| 103 | 但不能只看程式像不像，還要跑自己的案例。 | v30079.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 104 | 差異和測試一起保存，下一個審查者才追得上。 | v30080.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 105 | 它和上一份修補寫法不同，最後都要回到需求。 | v30081.text | local artifact / editorial (demo/codex.patch + local Codex result + node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 106 | Gemini CLI 本次結果 | scenes[12].data.kicker | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | OUT OF SCOPE | - |
| 107 | 尚未讀題 | scenes[12].data.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 108 | 帳戶與用戶端登入失敗 | scenes[12].data.sub | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 109 | Gemini CLI 這次沒有開始解題。 | v30084.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 110 | 登入回報目前的個人免費層不支援這個用戶端。 | v30085.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CHANGED | 登入回報目前的個人免費層不支援這個用戶端。 -> 這次登入回報用戶端不支援，還沒讀到題目。 |
| 111 | 它沒有產生任何修補，所以我不會替它編一個結果。 | v30086.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 112 | 這只說明本機帳戶的可用性，無法評價修題能力。 | v30087.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 113 | 看到錯誤訊息後，我停止了這一輪，沒有偷偷換帳戶。 | v30088.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 114 | 先分清兩種結果 | scenes[13].data.title | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 115 | 能不能啟動，是選工具時第一個現實條件。 | v30091.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | OUT OF SCOPE | - |
| 116 | 沒有執行成功，就不能把原始錯誤程式當成工具的答案。 | v30092.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 117 | 另一邊的兩份修補，也只是這一次的輸出。 | v30093.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 118 | 這張表把可用性和解題結果分開。 | v30094.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | CONFIRMED | - |
| 119 | 等帳戶問題解決，才有資格把第三份差異放進表格。 | v30095.text | https://geminicli.com/docs/get-started/authentication/; local CLI error (local Gemini error + official Gemini authentication) | 200; LOCAL | OUT OF SCOPE | - |
| 120 | 不要只信工具自寫測試 | scenes[14].data.title | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 121 | 現在看第三個共同條件：事後驗收。 | v30098.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 122 | 它在三支工具開工前就由我另外寫好。 | v30099.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CHANGED | 它在三支工具開工前就由我另外寫好。 -> 它是在三支工具都執行完後才另外寫成。 |
| 123 | 工具沒有看過這四類檢查。 | v30100.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 124 | 通過它，比只看工具自己寫的測試更有說服力。 | v30101.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CHANGED | 通過它，比只看工具自己寫的測試更有說服力。 -> 它比只看工具自寫測試多一層檢查，但不是事前盲測。 |
| 125 | 這正是為什麼測試資料不能只由答題工具決定。 | v30102.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 126 | 四類事後驗收 | scenes[15].data.title | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 127 | {"title":"一百除三","detail":"結果 34、33、33"} | scenes[15].data.steps[0] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 128 | {"title":"餘數與零","detail":"順序和零金額"} | scenes[15].data.steps[1] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 129 | {"title":"大量組合","detail":"總和與差額性質"} | scenes[15].data.steps[2] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 130 | {"title":"非法輸入","detail":"維持原有檢查"} | scenes[15].data.steps[3] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 131 | 第一個案例，就是一百分分給三個人。 | v30105.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 132 | 第二個看兩分給三人，以及零金額。 | v30106.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 133 | 第三個跑很多組金額和人數，檢查總和與最大差距。 | v30107.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 134 | 第四個確認非法輸入仍然被拒絕。 | v30108.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 135 | 這幾類檢查可以直接複製到自己的練習專案。 | v30109.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 136 | 這次的驗收結果 | scenes[16].data.title | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 137 | "Claude Code：4／4" | scenes[16].data.items[0] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 138 | "Codex：4／4" | scenes[16].data.items[1] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 139 | "Gemini CLI：沒有修補" | scenes[16].data.items[2] | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 140 | 跑完後，Claude Code 與 Codex 的修補都過了四類。 | v30112.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 141 | Gemini CLI 沒有修補，原始程式只過其中一類。 | v30113.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 142 | 後者是起始碼的結果，不能列成工具失敗率。 | v30114.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 143 | 拿結果做影片時，這個註解不能剪掉。 | v30115.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 144 | 請不要把沒開始的一欄，塗成紅色叉叉當失敗。 | v30116.text | local artifact / editorial (demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 145 | 用量不等於實際付款 | scenes[17].data.title | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 146 | 再來談成本。先別急著把三個方案放在同一張價目表。 | v30119.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | OUT OF SCOPE | - |
| 147 | Claude Code 的輸出有一筆美元估算值。 | v30120.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 148 | Codex 的這次輸出有 token 用量，沒有美元帳單。 | v30121.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 149 | Gemini 沒進到模型執行，自然沒有可比用量。 | v30122.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 150 | 付費方案與額度會更新，公開前還要再看當天官網。 | v30123.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | OUT OF SCOPE | - |
| 151 | 我把價格和這次的輸出用量刻意分欄記錄。 | v30124.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 152 | 這次只能記下什麼 | scenes[18].data.title | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 153 | Claude Code 這次報的約零點三美元，是工具估算值。 | v30126.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 154 | 訂閱帳戶是否因此多付錢，不能從這筆數字得知。 | v30127.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 155 | Codex 的輸入有大量快取，光看總 token 更會誤導。 | v30128.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | CONFIRMED | - |
| 156 | 要算真實成本，得用你自己的帳單和工作量。 | v30129.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | OUT OF SCOPE | - |
| 157 | 如果是固定月費，單次工作沒有唯一可歸屬價格。 | v30130.text | https://code.claude.com/docs/en/cli-reference; https://learn.chatgpt.com/docs/codex/cli; local CLI usage (local CLI usage JSON/JSONL + vendor docs) | 200, 200; LOCAL | OUT OF SCOPE | - |
| 158 | 你可以照這個順序選 | scenes[19].data.title | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 159 | {"title":"先確認能用","detail":"登入與權限"} | scenes[19].data.steps[0] | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 160 | {"title":"再比同一題","detail":"起點與提示固定"} | scenes[19].data.steps[1] | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 161 | {"title":"最後看差異","detail":"自己的驗收測試"} | scenes[19].data.steps[2] | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 162 | 我的做法是先確認三支工具在自己的帳戶真的能用。 | v30133.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 163 | 再拿一個小而明確的工作，固定起點與提示。 | v30134.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 164 | 最後把差異、測試和實際花費一起留下。 | v30135.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 165 | 如果工作有機密，就先換成不含真實資料的樣本。 | v30136.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 166 | 同一張清單也適合你已有的工具，無須全部換掉。 | v30137.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 167 | 怎麼選？先做自己的同題試跑 | scenes[20].data.title | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 168 | 到說明欄拿示範檔案 | scenes[20].data.cta | local artifact / editorial (editorial method) | LOCAL / N/A | CHANGED | 到說明欄拿示範檔案 -> 照三步重跑同題任務 |
| 169 | "先看能否啟動" | scenes[20].data.lines[0] | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 170 | "再看差異與驗收" | scenes[20].data.lines[1] | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 171 | 三款工具怎麼選？先看能不能啟動，再看同題差異。 | v30140.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 172 | 這次兩支完成，一支卡在登入，不代表能力名次。 | v30141.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 173 | 示範檔、兩份差異和驗收測試，都在說明欄的文章裡。 | v30142.text | local artifact / editorial (editorial method) | LOCAL / N/A | CHANGED | 示範檔、兩份差異和驗收測試，都在說明欄的文章裡。 -> 重跑時，把起始檔、兩份差異和驗收測試放在一起看。 |
| 174 | 下一次把你自己的小任務代入，答案才跟你有關。 | v30143.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 175 | 先拿你的需求重跑，才是真正有用的選擇依據。 | v30144.text | local artifact / editorial (editorial method) | LOCAL / N/A | OUT OF SCOPE | - |
| 176 | thumb | thumbnail.template | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 177 | {"tag":"AI 工具實測","headline":"同題試跑\n**2 完成 1 卡住**","sub":"看差異，比排行榜有用"} | thumbnail.data | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |


## 2026-09-28 addendum: six new scenes

Six added scenes checked against original files, patches, CLI error, the 2026-09-02 Google deprecation page and local timestamps. The two-patch narration incorrectly imposed the same operation order on Codex; corrected. The timing scene now accurately says the separate acceptance tests were written after all three runs, copied into each folder, and were not a preregistered blind test. In the login scene, the observed `UNSUPPORTED_CLIENT` error is consistent with Google's June 18 end of consumer Google sign-in; the earlier general authentication guide contradicts this. Formal round 2 must still be done by another checker. Lint: 0 errors/0 warnings, 10.3-minute estimate (129 lines, 2326 spoken units).

The earlier table records scene index paths at its original 21-scene snapshot; stable line IDs identify those claims in the current 27-scene script. This addendum uses current scene IDs.

Added entries: 30; CONFIRMED 21, CHANGED 1, NOT FOUND 0, OUT OF SCOPE 8.

| Where | Claim now | URL / local evidence | Verdict | Before -> after |
| --- | --- | --- | --- | --- |
| input-contract.data | {"title":"原有函式怎麼限制輸入","steps":[{"title":"金額","detail":"非負安全整數分"},{"title":"人數","detail":"1 到 100 位"},{"title":"輸出","detail":"每人一個整數分"}]} | demo/fare.mjs; demo/CHALLENGE.md | CONFIRMED | - |
| v3e1000.text | 起始程式不是只有一行除法，前面還有輸入檢查。 | demo/fare.mjs; demo/CHALLENGE.md | CONFIRMED | - |
| v3e1001.text | 金額要是非負的安全整數，單位是分。 | demo/fare.mjs; demo/CHALLENGE.md | CONFIRMED | - |
| v3e1002.text | 人數必須是一到一百之間的安全整數。 | demo/fare.mjs; demo/CHALLENGE.md | CONFIRMED | - |
| v3e1003.text | 比較工具時，不能只修餘數，還要把這些規則留下。 | demo/fare.mjs; demo/CHALLENGE.md | CONFIRMED | - |
| old-tests.data | {"title":"工具看到的兩個舊測試","language":"javascript","code":"assert.deepEqual(splitFareCents(120, 3),\n  [40, 40, 40]);\nassert.throws(() => splitFareCents(100, 0),\n  RangeError);","caption":"整除與非法人數，都沒有碰到餘數"} | demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v3e2000.text | 工具能看到的舊測試，第一個是整除案例。 | demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v3e2001.text | 一百二十分分給三人，每人四十，這本來就會過。 | demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v3e2002.text | 第二個只確認零人時會丟出錯誤。 | demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v3e2003.text | 兩個測試都沒有問一百分怎麼分給三人。 | demo/fare.test.mjs; local node --test | CONFIRMED | - |
| two-patches.data | {"title":"兩份修補的共同點","left":{"heading":"Claude Code","points":["Math.floor 取基本分","用減法算餘數"]},"right":{"heading":"Codex","points":["先取模數","再算基本分"]}} | demo/claude.patch; demo/codex.patch | CONFIRMED | - |
| v3e3000.text | 兩份差異用了不同運算順序，結果不是靠文字像不像判斷。 | demo/claude.patch; demo/codex.patch | CONFIRMED | - |
| v3e3001.text | 兩份都算出基本份額和餘數，再把多的一分交給前面的人。 | demo/claude.patch; demo/codex.patch | CHANGED | 共同點是先找基本份額，再把餘數交給前面的人。 -> 兩份都算出基本份額和餘數，再把多的一分交給前面的人。 |
| v3e3002.text | 把兩分交給三人時，應該是一、一、零。 | demo/claude.patch; demo/codex.patch | CONFIRMED | - |
| v3e3003.text | 你可以拿這組數字，逐行代入兩份實際差異。 | demo/claude.patch; demo/codex.patch | OUT OF SCOPE | - |
| login-evidence.data | {"kicker":"本機錯誤類別","text":"UNSUPPORTED_CLIENT","sub":"沒有模型輸出，沒有修補差異"} | local gemini-result.json; https://geminicli.com/docs/get-started/authentication/ (HTTP 200 on 2026-09-27) | CONFIRMED | - |
| v3e4000.text | 這次看到的是用戶端和帳戶之間的登入錯誤。 | local gemini-result.json; https://geminicli.com/docs/get-started/authentication/ (HTTP 200 on 2026-09-27) | CONFIRMED | - |
| v3e4001.text | 程式碼並沒有交給模型，所以沒有模型回答。 | local gemini-result.json; https://geminicli.com/docs/get-started/authentication/ (HTTP 200 on 2026-09-27) | CONFIRMED | - |
| v3e4002.text | 原本錯誤程式在事後測試裡失敗，仍是起始碼的失敗。 | local gemini-result.json; https://geminicli.com/docs/get-started/authentication/ (HTTP 200 on 2026-09-27) | CONFIRMED | - |
| v3e4003.text | 若要完整比較第三支，必須在可用帳戶上重新跑。 | local gemini-result.json; https://geminicli.com/docs/get-started/authentication/ (HTTP 200 on 2026-09-27) | OUT OF SCOPE | - |
| acceptance-timing.data | {"title":"事後驗收何時加入","items":["三支 CLI 結束後撰寫","複製進各資料夾","再跑相同四類測試"]} | local CLI log/file timestamps; author confirmation | CONFIRMED | - |
| v3e5000.text | 這份驗收是在三支工具結束後才另外寫的。 | local CLI log/file timestamps; author confirmation | CONFIRMED | - |
| v3e5001.text | 因此它不是事前註冊的盲測，這點要講清楚。 | local CLI log/file timestamps; author confirmation | OUT OF SCOPE | - |
| v3e5002.text | 但工具生成修補時，確實看不到這份新檔。 | local CLI log/file timestamps; author confirmation | CONFIRMED | - |
| v3e5003.text | 我把同一份驗收複製進三份資料夾，再逐一執行。 | local CLI log/file timestamps; author confirmation | CONFIRMED | - |
| selection-sheet.data | {"title":"自己的試跑記錄表","steps":[{"title":"起點與版本","detail":"留檔案雜湊及 CLI 版本"},{"title":"成果","detail":"差異和驗收輸出"},{"title":"花費","detail":"帳單與工具用量分欄"}]} | editorial method | OUT OF SCOPE | - |
| v3e6000.text | 如果你要重做這個比較，我建議先記檔案雜湊。 | editorial method | OUT OF SCOPE | - |
| v3e6001.text | 工具版本和權限模式也要寫在同一張表。 | editorial method | OUT OF SCOPE | - |
| v3e6002.text | 成果欄放差異和驗收輸出，不寫主觀的好壞分數。 | editorial method | OUT OF SCOPE | - |
| v3e6003.text | 花費欄把帳單金額與工具報的用量分開。 | editorial method | OUT OF SCOPE | - |
