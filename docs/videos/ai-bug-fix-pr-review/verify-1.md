# Independent verification, round 1: ai-bug-fix-pr-review

Checked on 2026-09-27. I did not write this script. The table enumerates every extracted narration, say, slide-data, thumbnail, title, description and tag entry; repeated facts are counted per entry, not as unique research questions. Original extraction and helper code remain in the local independent-verification workdir outside Git.

## Summary

- Extracted entries: 180; CONFIRMED 93, CHANGED 5, NOT FOUND 0, OUT OF SCOPE 82. Three distinct factual corrections: clarified that only the first old test covers divisible totals, replaced a non-existent `sum(shares)` helper with the actual acceptance assertion, and removed an inaccessible description-link promise. Under the >3 rule, a second independent round is not required for these current edits; any new substantive script material needs review.
- Local replay: original two tests pass while `100/3` returns `[33,33,33]`; the separate acceptance suite is 1/4 on baseline and 4/4 on the Claude patch. Claude self-authored tests are 9/9, total replay 13/13. The patch modifies only fare.mjs and fare.test.mjs and retains validation. This was a local patch, not a real PR or a production incident.
- Official [GitHub PR review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) returned HTTP 200 on 2026-09-27 and supports line comments, request changes and approval. The actual decision to merge remains a team judgment. No price/version claim appears in this script.
- Opinion pass: three review gates and human final judgment agree with brief.md. Listener pass: zero lines over 40 Unicode characters; AI, PR, Bug, Claude Code and GitHub occur in the pronunciation dictionary. No spoken URLs or parenthetical citations. Chapter/reveal order is coherent.
- Lint after edits: 0 errors, 0 warnings; 8.1 minute estimate, 107 lines, 1817 spoken units. Actual TTS duration and eleven-point rendered-video QA remain outstanding; estimate may run short of the 8-minute target.
- Publication gate: the source guide article does not contain this new demo. The false description and spoken promise was removed; add and click-check a public permalink in the final upload pack if exact source files are offered.
- Suspected but not changed: this small integer-split example does not establish production billing correctness or a complete PR review. The script discloses that boundary.

## Full claim table

| # | Claim before review | Where | URL / evidence | HTTP | Verdict | Before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AI 修好 Bug 就能合併？三個 PR 檢查點 | youtube.title | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |
| 2 | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。完整檔案及驗收可在對應文章與示範包找到。 | youtube.description | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CHANGED | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。完整檔案及驗收可在對應文章與示範包找到。 -> 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 |
| 3 | AI code review | youtube.tags[0] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 4 | PR review | youtube.tags[1] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 5 | Bug fix | youtube.tags[2] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 6 | 程式碼審查 | youtube.tags[3] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 7 | 回歸測試 | youtube.tags[4] | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 8 | AI 修補審查 | scenes[0].data.tag | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 9 | 測試全綠，還少一分 | scenes[0].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 10 | 合併前先過三道關 | scenes[0].data.subtitle | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 11 | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | v40000.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 12 | 現在 AI 交來修補，你會直接合併嗎？ | v40001.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 13 | 我帶你看需求、差異與回歸，三道關都要過。 | v40002.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 14 | 我們先從那一分為什麼消失開始。 | v40003.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 15 | 第一個畫面 | scenes[1].data.kicker | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 16 | 2 個測試通過 | scenes[1].data.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 17 | 但不代表需求被測完 | scenes[1].data.sub | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 18 | 先看舊的測試，它只檢查能整除的金額。 | v40007.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CHANGED | 先看舊的測試，它只檢查能整除的金額。 -> 第一個舊測試，只檢查能整除的金額。 |
| 19 | 人數不合法也會擋，兩個結果都是綠色。 | v40008.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 20 | 不整除的路徑沒人問，所以錯誤藏得好好的。 | v40009.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 21 | 這次示範是真正執行的檔案，不是想像案例。 | v40010.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 22 | 它證明程式照舊測試運作，沒有證明帳算對。 | v40011.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 23 | 漏掉的案例 | scenes[2].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 24 | javascript | scenes[2].data.language | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 25 | splitFareCents(100, 3)<br>// 原本得到 [33, 33, 33]<br>// 總和 99，少了 1 | scenes[2].data.code | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 26 | 起始程式與事後測試實際輸出 | scenes[2].data.caption | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 27 | 分一百分給三個人，原始程式回三個三十三。 | v40014.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 28 | 這不是顯示格式的問題，總和真的少了一分。 | v40015.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 29 | 如果這一分會進帳務，測試綠燈也不能放行。 | v40016.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 30 | 接下來看 AI 真正交出的修補。 | v40017.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 31 | 這個失敗結果已寫進可重跑的驗收檔案。 | v40018.text | local artifact / editorial (../ai-coding-tools-same-task/demo/fare.mjs + tests + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 32 | 這份示範的來源 | scenes[3].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 33 | "自有小型程式" | scenes[3].data.items[0] | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 34 | "同一句明確需求" | scenes[3].data.items[1] | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 35 | "實際 Claude Code 修補" | scenes[3].data.items[2] | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 36 | 我用自己寫的分攤函式，讓 Claude Code 依照題目修改。 | v40021.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 37 | 它改了程式和測試，工具自寫九個測試都通過。 | v40022.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 38 | 這不是正式站的事故，也不是已合併的真實 PR。 | v40023.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 39 | 它是可以公開重跑的一份本地修補案例。 | v40024.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | CONFIRMED | - |
| 40 | 所以它適合用來練審查，卻不能代表產品事故。 | v40025.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch + local Claude result) | LOCAL / N/A | OUT OF SCOPE | - |
| 41 | 先問：修的是哪個需求？ | scenes[4].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 42 | 第一關，不要先看 AI 說它完成了什麼。 | v40028.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 43 | 先把需求寫成你可以算得出來的條件。 | v40029.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 44 | 這題要保留輸入規則，不能只修一個範例。 | v40030.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 45 | 也不能悄悄把分配規則改成另一種做法。 | v40031.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 46 | 第一關的答案，應該能不靠工具自己口述。 | v40032.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 47 | 需求契約四條 | scenes[5].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 48 | {"title":"長度","detail":"每人一個整數金額"} | scenes[5].data.steps[0] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 49 | {"title":"總和","detail":"加起來等於原金額"} | scenes[5].data.steps[1] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 50 | {"title":"差額","detail":"最多相差一分"} | scenes[5].data.steps[2] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 51 | {"title":"順序","detail":"餘數先給前面的人"} | scenes[5].data.steps[3] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 52 | 第一條，結果長度要和人數一樣。 | v40035.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 53 | 第二條，所有人的份額加總，必須等於原來金額。 | v40036.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 54 | 第三條，任何兩人最多只差一分。 | v40037.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 55 | 第四條，有餘數時，前面的人先分到。 | v40038.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 56 | 四條放在一起，才描述完整的分攤行為。 | v40039.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 57 | 如果只補一百除三，還會漏掉其他金額。 | v40040.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 58 | 原有輸入規則也算契約 | scenes[6].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 59 | "總額：非負安全整數" | scenes[6].data.items[0] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 60 | "人數：1 到 100" | scenes[6].data.items[1] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 61 | "非法輸入：RangeError" | scenes[6].data.items[2] | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 62 | 還有原本就存在的輸入檢查。 | v40042.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 63 | 總額不能是負數、小數或超過安全整數。 | v40043.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 64 | 人數只能是一到一百之間的安全整數。 | v40044.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 65 | 修補若刪掉這些檢查，就算範例變對也不能過關。 | v40045.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 66 | 它們不是額外加分題，而是修補前就有的規則。 | v40046.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 67 | 一個例子，看四個條件 | scenes[7].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 68 | 把一百分除以三，理想結果是三十四、三十三、三十三。 | v40049.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 69 | 這組數字同時檢查總和與餘數順序。 | v40050.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 70 | 只測每個人差不多，還是不夠。 | v40051.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 71 | 需求契約先寫清楚，才有審查的尺。 | v40052.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | OUT OF SCOPE | - |
| 72 | 換成兩分三人，正確順序也是一、一、零。 | v40053.text | local artifact / editorial (../ai-coding-tools-same-task/demo/CHALLENGE.md) | LOCAL / N/A | CONFIRMED | - |
| 73 | 逐行看它改了什麼 | scenes[8].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 74 | 第二關，打開實際差異，不只讀工具的完成訊息。 | v40056.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 75 | 先確認它只改到預期的程式和測試。 | v40057.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 76 | 接著把新增邏輯代入一百分除三的例子。 | v40058.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 77 | 最後看它有沒有刪掉原來的保護條件。 | v40059.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 78 | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | v40060.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 79 | 修補的核心四行 | scenes[9].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 80 | javascript | scenes[9].data.language | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 81 | const base = Math.floor(totalCents / people);<br>const remainder = totalCents - base * people;<br>return Array.from({ length: people }, (_, i) =><br>  i < remainder ? base + 1 : base); | scenes[9].data.code | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 82 | 從實際 Claude Code 差異節錄 | scenes[9].data.caption | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 83 | 這份修補先算每人最少要拿多少。 | v40063.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 84 | 再算剩下幾分，要補給幾位前面的人。 | v40064.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 85 | 一百分除三，基本份額三十三，餘數是一。 | v40065.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 86 | 第一位多拿一分，其餘兩位維持三十三。 | v40066.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 87 | 用兩分三人再代一次，就能看到前兩位各多一分。 | v40067.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 88 | 讀差異時看三處 | scenes[10].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 89 | "輸入驗證保留嗎？" | scenes[10].data.items[0] | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 90 | "有改題目以外的檔嗎？" | scenes[10].data.items[1] | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 91 | "新測試在驗什麼？" | scenes[10].data.items[2] | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 92 | 我在差異裡先找原有驗證，這次沒有被刪掉。 | v40070.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 93 | 再看檔案清單，只有程式和測試被修改。 | v40071.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 94 | 新增測試涵蓋不整除、零金額和非法輸入。 | v40072.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 95 | 這些都是看得見的證據，不是工具的口頭保證。 | v40073.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 96 | 如果它順手改了部署或帳務設定，應該另外討論。 | v40074.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 97 | 新增測試也要看斷言，不只看測試名稱。 | v40075.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 98 | 範圍說明 | scenes[11].data.kicker | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 99 | 本地 patch | scenes[11].data.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 100 | 沒有真實 PR 審核紀錄 | scenes[11].data.sub | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 101 | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | v40077.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | CONFIRMED | - |
| 102 | 真正的專案還要看相關模組、型別與維運影響。 | v40078.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 103 | 如果這段程式連著付款系統，範圍會更大。 | v40079.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 104 | 影片示範的方法，可以帶進真正的審查流程。 | v40080.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 105 | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | v40081.text | local artifact / editorial (../ai-coding-tools-same-task/demo/claude.patch) | LOCAL / N/A | OUT OF SCOPE | - |
| 106 | 測試要能抓到原本的錯 | scenes[12].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 107 | 第三關，把修補放進事先想好的回歸測試。 | v40084.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 108 | 工具自己寫的測試有用，但不能是唯一標準。 | v40085.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 109 | 如果測試沒有先在舊碼上失敗，可能沒測到 Bug。 | v40086.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 110 | 所以我先拿舊碼跑同一份事後驗收。 | v40087.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 111 | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | v40088.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 112 | 先紅、再綠 | scenes[13].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 113 | 舊碼雖然兩個原測試全過，事後四類只過一類。 | v40091.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 114 | 這證明新驗收能抓到我們要修的缺陷。 | v40092.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 115 | 換成修補後，四類事後驗收全通過。 | v40093.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 116 | 這才是比較有力的紅燈到綠燈證據。 | v40094.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 117 | 這一步能排除只檢查舊有整除案例的假安全感。 | v40095.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 118 | 不只測一組數字 | scenes[14].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 119 | javascript | scenes[14].data.language | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 120 | for (let total = 0; total <= 500; total++) {<br>  for (let people = 1; people <= 20; people++) {<br>    const shares = splitFareCents(total, people);<br>    assert.equal(sum(shares), total);<br>  }<br>} | scenes[14].data.code | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CHANGED | for (let total = 0; total <= 500; total++) {<br>  for (let people = 1; people <= 20; people++) {<br>    const shares = splitFareCents(total, people);<br>    assert.equal(sum(shares), total);<br>  }<br>} -> for (let total = 0; total <= 500; total += 1) {<br>  for (let people = 1; people <= 20; people += 1) {<br>    const shares = splitFareCents(total, people);<br>    assert.equal(<br>      shares.reduce((sum, amount) => sum + amount, 0),<br>      total<br>    );<br>    assert.ok(Math.max(...shares) - Math.min(...shares) <= 1);<br>  }<br>} |
| 121 | 實際驗收也檢查份額差距 | scenes[14].data.caption | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CHANGED | 實際驗收也檢查份額差距 -> 實際驗收節錄（省略長度檢查） |
| 122 | 驗收不是只寫一百除三。 | v40098.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 123 | 我還把零到五百的總額，搭配一到二十人跑過。 | v40099.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 124 | 每組都檢查總和，並確認最大差距不超過一分。 | v40100.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 125 | 這種性質檢查，能抓到你沒想到的餘數組合。 | v40101.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 126 | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | v40102.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 127 | 超出測試範圍的風險，要再根據業務補案例。 | v40103.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 128 | 再保護原本沒壞的地方 | scenes[15].data.title | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 129 | "零元額分攤" | scenes[15].data.items[0] | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 130 | "總額非法輸入" | scenes[15].data.items[1] | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 131 | "人數非法輸入" | scenes[15].data.items[2] | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 132 | 零金額要回傳每人零分，不能拋出莫名錯誤。 | v40105.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 133 | 負數、小數或超大總額，仍然要被拒絕。 | v40106.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 134 | 零人、超過一百人和小數人數也是一樣。 | v40107.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | CONFIRMED | - |
| 135 | 回歸的意思，就是修新 Bug 也守住舊契約。 | v40108.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 136 | 尤其輸入驗證最容易在重寫時被無意刪掉。 | v40109.text | local artifact / editorial (../ai-coding-tools-same-task/demo/acceptance.test.mjs + local node --test) | LOCAL / N/A | OUT OF SCOPE | - |
| 137 | 三道關缺一不可 | scenes[16].data.title | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 138 | 現在把三道關合在一起。 | v40112.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 139 | 需求契約告訴你什麼叫修好。 | v40113.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 140 | 差異讓你知道實際改了哪些檔、哪些行。 | v40114.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 141 | 回歸則證明新舊規則至少在測試範圍內成立。 | v40115.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 142 | 只缺一道關，審查紀錄就不完整。 | v40116.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 143 | 準備合併時記下證據 | scenes[17].data.title | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 144 | {"title":"需求","detail":"總和、差額、順序、輸入"} | scenes[17].data.steps[0] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 145 | {"title":"差異","detail":"兩個預期檔案"} | scenes[17].data.steps[1] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 146 | {"title":"測試","detail":"舊碼紅、修補綠"} | scenes[17].data.steps[2] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 147 | 我會在審查紀錄裡放三件事。 | v40119.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 148 | 第一，需求有哪些明確的驗收條件。 | v40120.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 149 | 第二，實際差異只改了哪些地方。 | v40121.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 150 | 第三，哪個測試先紅、修補後又如何變綠。 | v40122.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 151 | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | v40123.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 152 | 仍要人判斷的地方 | scenes[18].data.title | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 153 | "需求本身正確嗎？" | scenes[18].data.items[0] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 154 | "改動範圍完整嗎？" | scenes[18].data.items[1] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 155 | "風險與回滾可接受嗎？" | scenes[18].data.items[2] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 156 | 這次小題的驗收通過，仍不能替真實業務做決定。 | v40126.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 157 | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | v40127.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 158 | 還要有人看改動範圍、資料影響和回滾方式。 | v40128.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 159 | 負責合併的人，得對這個判斷負責。 | v40129.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 160 | 合併不是模型替團隊作的事，而是負責者作的決定。 | v40130.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart; editorial method (editorial method + GitHub Docs) | 200; N/A | OUT OF SCOPE | - |
| 161 | 真實團隊流程 | scenes[19].data.kicker | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 162 | 留下可追溯的審查 | scenes[19].data.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 163 | 看差異、留言、要求修改或核准 | scenes[19].data.sub | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 164 | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | v40133.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 165 | 也可以要求修改，或在看過證據後核准。 | v40134.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 166 | 這裡不替任何真實 PR 點核准。 | v40135.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 167 | 重點是讓下一位審查者找到同一份證據。 | v40136.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 168 | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | v40137.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 169 | AI 修好 Bug，就能合併嗎？ | scenes[20].data.title | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 170 | 拿三關清單檢查你的下一個修補 | scenes[20].data.cta | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 171 | "需求契約" | scenes[20].data.lines[0] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 172 | "實際差異" | scenes[20].data.lines[1] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 173 | "回歸測試" | scenes[20].data.lines[2] | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CONFIRMED | - |
| 174 | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | v40140.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 175 | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | v40141.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 176 | 這次完整起始碼、修補和測試，都可以在說明欄找到。 | v40142.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | CHANGED | 這次完整起始碼、修補和測試，都可以在說明欄找到。 -> 這次的起始碼、修補和測試，要放在一起核對。 |
| 177 | 拿你下一個小修補照著試一次，比背規則更有用。 | v40143.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 178 | 這個小練習之後，再把同一方法用到較大的改動。 | v40144.text | https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (GitHub Docs) | 200 | OUT OF SCOPE | - |
| 179 | thumb | thumbnail.template | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | OUT OF SCOPE | - |
| 180 | {"tag":"AI 修補審查","headline":"測試綠了？\n**先過 3 關**","sub":"需求／差異／回歸"} | thumbnail.data | local artifact / editorial (metadata or editorial framing) | LOCAL / N/A | CONFIRMED | - |


## 2026-09-28 addendum: six new scenes

Six added scenes checked against the baseline tests, challenge, Claude patch and acceptance test. Clarified that the algorithm replacement was within the function; the patch also added tests. The shown assertions exist in the real patch, and the property checks match the actual acceptance loop. Formal second review is prudent after cumulative factual corrections. Lint: 0 errors/0 warnings, 9.9-minute estimate (131 lines, 2233 spoken units).

The earlier table records scene index paths at its original 21-scene snapshot; stable line IDs identify those claims in the current 27-scene script. This addendum uses current scene IDs.

Added entries: 30; CONFIRMED 21, CHANGED 1, NOT FOUND 0, OUT OF SCOPE 8.

| Where | Claim now | URL / local evidence | Verdict | Before -> after |
| --- | --- | --- | --- | --- |
| old-test-code.data | {"title":"綠燈實際測了什麼","language":"javascript","code":"assert.deepEqual(splitFareCents(120, 3),\n  [40, 40, 40]);\nassert.throws(() => splitFareCents(100, 0),\n  RangeError);","caption":"原本只有整除和非法人數兩題"} | ../ai-coding-tools-same-task/demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v4e1000.text | 這是起始專案真的跑過的兩個測試。 | ../ai-coding-tools-same-task/demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v4e1001.text | 第一個測一百二十分，三人平均分。 | ../ai-coding-tools-same-task/demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v4e1002.text | 第二個測零人時要拋出錯誤。 | ../ai-coding-tools-same-task/demo/fare.test.mjs; local node --test | CONFIRMED | - |
| v4e1003.text | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | ../ai-coding-tools-same-task/demo/fare.test.mjs; local node --test | CONFIRMED | - |
| small-remainder.data | {"kicker":"再代一組","text":"2 分給 3 人","sub":"正確結果：1、1、0"} | ../ai-coding-tools-same-task/demo/CHALLENGE.md; baseline fare.mjs | CONFIRMED | - |
| v4e2000.text | 只測一百分除三，還可能把規則寫死在特例上。 | ../ai-coding-tools-same-task/demo/CHALLENGE.md; baseline fare.mjs | OUT OF SCOPE | - |
| v4e2001.text | 再代入兩分給三個人，正確是前兩位各一分。 | ../ai-coding-tools-same-task/demo/CHALLENGE.md; baseline fare.mjs | CONFIRMED | - |
| v4e2002.text | 第三位拿零分，總和仍是兩分。 | ../ai-coding-tools-same-task/demo/CHALLENGE.md; baseline fare.mjs | CONFIRMED | - |
| v4e2003.text | 這組資料會立刻露出四捨五入重複分配的問題。 | ../ai-coding-tools-same-task/demo/CHALLENGE.md; baseline fare.mjs | CONFIRMED | - |
| validation-stays.data | {"title":"新邏輯前面的檢查還在","items":["總額先驗證","人數先驗證","只替換分配算法"]} | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| v4e3000.text | 回到完整差異，函式前兩段檢查沒有被移除。 | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| v4e3001.text | 非法金額和非法人數，仍會在分配前被擋。 | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| v4e3002.text | 在函式裡，AI 把平均四捨五入換成基本分與餘數。 | ../ai-coding-tools-same-task/demo/claude.patch | CHANGED | AI 只把原本的平均四捨五入，換成基本分與餘數。 -> 在函式裡，AI 把平均四捨五入換成基本分與餘數。 |
| v4e3003.text | 這是這份本地差異的範圍，不替其他檔案背書。 | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| test-assertions.data | {"title":"新測試要讀斷言","language":"javascript","code":"assert.deepEqual(splitFareCents(100, 3),\n  [34, 33, 33]);\nassert.deepEqual(splitFareCents(2, 5),\n  [1, 1, 0, 0, 0]);","caption":"這兩個斷言存在實際修補測試"} | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| v4e4000.text | 新增測試不能只看名字，要看它到底斷言什麼。 | ../ai-coding-tools-same-task/demo/claude.patch | OUT OF SCOPE | - |
| v4e4001.text | 這份修補測到一百分除三，是三十四、三十三、三十三。 | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| v4e4002.text | 也測到兩分分五人，前兩位各一分，其餘拿零。 | ../ai-coding-tools-same-task/demo/claude.patch | CONFIRMED | - |
| v4e4003.text | 這兩組一起看，比只看測試數量更有意義。 | ../ai-coding-tools-same-task/demo/claude.patch | OUT OF SCOPE | - |
| property-check.data | {"title":"性質測試逐組查三件事","steps":[{"title":"人數","detail":"輸出長度相同"},{"title":"總額","detail":"各份額加總不變"},{"title":"差距","detail":"最大與最小最多差一"}]} | ../ai-coding-tools-same-task/demo/acceptance.test.mjs; local node --test | CONFIRMED | - |
| v4e5000.text | 回圈跑每組數字時，不只看總額。 | ../ai-coding-tools-same-task/demo/acceptance.test.mjs; local node --test | CONFIRMED | - |
| v4e5001.text | 它還比對輸出長度，確認沒有漏掉任何人。 | ../ai-coding-tools-same-task/demo/acceptance.test.mjs; local node --test | CONFIRMED | - |
| v4e5002.text | 再找最大和最小份額，差距不能超過一。 | ../ai-coding-tools-same-task/demo/acceptance.test.mjs; local node --test | CONFIRMED | - |
| v4e5003.text | 這三個斷言對每組資料都成立，才算這關通過。 | ../ai-coding-tools-same-task/demo/acceptance.test.mjs; local node --test | CONFIRMED | - |
| review-record.data | {"title":"交給審查者的最小證據","items":["失敗案例與需求","完整差異","重跑指令與測試結果"]} | editorial method; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (HTTP 200 on 2026-09-27) | OUT OF SCOPE | - |
| v4e6000.text | 最後把那個原本失敗的案例寫在審查摘要裡。 | editorial method; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (HTTP 200 on 2026-09-27) | OUT OF SCOPE | - |
| v4e6001.text | 附上完整差異，不只貼兩行好看的核心程式。 | editorial method; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (HTTP 200 on 2026-09-27) | OUT OF SCOPE | - |
| v4e6002.text | 再列出重跑指令與通過的測試範圍。 | editorial method; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (HTTP 200 on 2026-09-27) | OUT OF SCOPE | - |
| v4e6003.text | 下一位審查者不必相信口頭報告，能自己驗證。 | editorial method; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart (HTTP 200 on 2026-09-27) | OUT OF SCOPE | - |
