# verify-3：claude-skill-manual-event-folder

查核日 2026-10-21（第 3 輪，與第 1、2 輪不同的代理；不是撰稿者）。範圍：修訂 3 新增或改過的旁白、卡片與說明欄句子（依 `<work>/_tools/writer/revise3.log` 與 claims.md「修訂 3」，再把整份 134 句讀過一次）。實跑事實對 `runlog.txt` 與 `demo/` 逐字比；功能事實對今天重抓的官方頁（`<work>/_tools/verify3/`，UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，每次間隔 1.2 秒）。網頁搜尋 0 次。

官方頁（今天，全部 HTTP 200）：

| 頁 | URL | 狀態 | 頁上日期 |
| --- | --- | --- | --- |
| Use skills in Claude | https://support.claude.com/en/articles/12512180-use-skills-in-claude | 200 | Updated over a month ago |
| 在 Claude 中使用技能（zh-TW） | https://support.claude.com/zh-TW/articles/12512180 | 200（轉到含中文標題的網址） | — |
| How to create custom skills | https://support.claude.com/en/articles/12512198-how-to-create-custom-skills | 200 | Updated this week |
| What are skills? | https://support.claude.com/en/articles/12512176-what-are-skills | 200 | Updated over a month ago |
| Agent Skills overview | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | 200 | — |
| Claude Code skills | https://code.claude.com/docs/en/skills.md | 200 | — |
| Specification | https://agentskills.io/specification | 200 | — |
| Client Showcase | https://agentskills.io/clients | 200 | — |

## 主張表

| # | 主張 | 位置 | 出處 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 只說一句「照平常的方式」，它就自己翻開這一本 | mv44、result 3／3 | runlog CSa–CSc `Skill signup-check`；總表 opened | — | CONFIRMED | |
| 2 | 寄信名單補上新人，缺 Email 的那位另外列出 | 2u43、5bjj | demo/CSa–c/輸出/要補資料.csv 第 4 列宋柏均「沒有 Email」；確認信名單 18 人 | — | CONFIRMED | |
| 3 | 16 人變 18 人；要補資料 3 → 4 | 5bjj、run-stats | demo/start/輸出 16 列；CSa–c 18 列、4 列；總表 B1–B6 PPPPPP | — | CONFIRMED | |
| 4 | 開資料夾在講座籌備的隱藏設定資料夾下，名字＝說明書名字，SKILL.md＋兩個附件 | cs8y、xify、8e2x、nwx7 | runlog M1 `book-lean/.claude/skills/signup-check/` 三個檔 | — | CONFIRMED | |
| 5 | 兩條橫線中間只放名字和介紹 | mxw5 | demo/booklets/book-lean/signup-check/SKILL.md 第 1–6 行 | — | CONFIRMED | |
| 6 | 一本放上去開場多 77，就是封面那兩句 | m7dd | 總表 L0 33,863.5、L1 33,940.5（+77）；L1 opened none | — | CONFIRMED（「就是封面那兩句」是技能清單裡的名字＋介紹，約略） | |
| 7 | 七步寫進 CLAUDE.md，問什麼都多帶 462 | xyia | 總表 LM 34,325.5（+462）；demo/claude-md/claude-md-book.CLAUDE.md 是同樣七步 | — | CONFIRMED | |
| 8 | 每一次來回，每一本的封面都送進去 | pusc | Claude Code skills 頁「Every skill in the skill listing adds to your context on every turn」 | 200 | CONFIRMED | |
| 9 | CLAUDE.md 和專案指示每次整段帶著，說明書平常只帶封面 | zazw | skills 頁「Unlike CLAUDE.md content, a skill's body loads only when it's used」；What are skills?「Projects … always loaded」 | 200 | CONFIRMED | |
| 10 | 另外五本各一件事；每一本封面一句什麼時候用、內文三、四步 | xf3d、cvj3 | demo/shelf5 五本：都有「…時用」；內文 4、4、4、3、4 步 | — | CONFIRMED | |
| 11 | 講者介紹 150 字內、先講現在做什麼再講講題 | t84f | shelf5/speaker-intro 第 2 步 | — | CONFIRMED | |
| 12 | 會議紀錄只留決議、待辦、下次開會；沒講負責人標未指定 | 7fkf | shelf5/meeting-notes | — | CONFIRMED | |
| 13 | 報帳一張收據一列，看不清的金額標待確認 | 6tp8 | shelf5/expense-receipts | — | CONFIRMED | |
| 14 | 活動文案主標和貼文都有字數上限，日期只用活動說明裡寫的 | 59di | shelf5/poster-copy 第 1、2 步（主標 15、貼文 120 字內） | — | CONFIRMED | |
| 15 | 行前提醒信只寫通用草稿、不寫姓名、不寄出 | 6z42 | shelf5/reminder-mail | — | CONFIRMED | |
| 16 | 含糊封面「檢查用的步驟」、名字 checklist | czys | demo/booklets/book-vague | — | CONFIRMED | |
| 17 | 我換成這一句試過：照樣翻開，沒翻錯成行前提醒信 | ccaw、vague 卡 | runlog CVa–c `Skill checklist`；Unexpected 1「the right one each time」；reminder-mail not opened | — | CONFIRMED | |
| 18 | 含糊封面開場少 61 token | vague 卡、說明欄 | CV 平均 34,225.3 對 CS 34,286（差 60.7） | — | CONFIRMED | |
| 19 | 封面要寫清楚：同事、三個月後的你看得懂 | t8d7 | 理由，不是事實 | — | 意見，已標成頻道觀點 | 「要。它翻得開，…」→「要。以這個頻道來說，它翻得開，…」 |
| 20 | 格式檢查通過不代表封面寫得好；含糊的也通過 | my5e | runlog M3 三個都 `✔ Validation passed` | — | CONFIRMED | |
| 21 | 內文七步（逐條） | kcrx、hmuf、pbtx、pgwr、fcnq、r9ms、izcy、2agp | book-lean SKILL.md 第 1–7 步 | — | CONFIRMED（口語改寫，意思逐條相同） | |
| 22 | 兩個王志明，一個業務部、一個研發部 | j945 | demo/start/輸出/確認信名單.csv 第 2、6 列 | — | CONFIRMED | |
| 23 | 每份報名表都有一筆「測試」；這一批叫測試二 | ipd6 | seed 報名表.csv 第 7 列「測試」；第二批「測試二」 | — | CONFIRMED | |
| 24 | 只說一句「第二批來了，照平常的方式檢查一下」 | 82bv | prompts/skill-auto.txt（原文多「報名表」與檔名） | — | CONFIRMED（節略） | |
| 25 | 它做的第一件事就是翻開 signup-check | 5dba | CSa–c 第一筆 tool_use 都是 Skill signup-check | — | CONFIRMED | |
| 26 | 結果一樣；說明書不用每次貼、平常只帶封面、整個資料夾帶得走 | wvcw、four-ways | 總表 CP、CM、CS、CN1 都 PPPPPP；four-ways 卡「寫成說明書 +77 token」；How to create custom skills（ZIP 上傳） | 200 | CHANGED | 「平常也不佔位子」→「平常只帶封面」（同一張卡寫平常帶著 +77） |
| 27 | 第八步：想改線上的列進待回覆，寫下問了什麼，不要自己回答 | r3tb、piu5 | demo/booklets/book-mine 第 8 步 | — | CONFIRMED | |
| 28 | 黃雅婷問的不是報名，是要有人決定的事 | gnqk | 報名表_第二批.csv 備註「改成線上參加可以嗎？」 | — | CONFIRMED | |
| 29 | 加了這一行，多寫出一份待回覆，只有黃雅婷問的那一句 | 2q52、step8-result | W1a、W1b/輸出/待回覆.csv 各一列（W1a 多一欄狀態） | — | CONFIRMED | |
| 30 | 寄信名單裡她沒被重複加進去 | ykf3 | W1a、W1b 確認信名單「黃雅婷」各 1 次 | — | CONFIRMED | |
| 31 | 叫它寫一本：寫進隱藏設定資料夾被擋下、要你同意 | 5jsg、g1-ask 卡 | runlog G1 tool_error「Claude requested permissions to write …」；prompts/write-skill.txt 與卡上原文一致 | — | CONFIRMED | |
| 32 | 放成附件那本，確認信範本一頁都沒讀 | 5j4b | 成果 4 (c)「no CS session touched 確認信範本.md」 | — | CONFIRMED | |
| 33 | 全貼進內文那本一翻開比短的重 | 7khj | 總表 CF +1,288 對 CS +436～+487（2.64–2.95 倍） | — | CHANGED | 「重上好幾倍」→「重上將近三倍」（emotion 欄本來就寫「三倍」加重） |
| 34 | 八次裡有五次回你部門對照找不到 | fag8、appendix-miss 3／8、5／8 | Unexpected 2；demo/CSc、CVa、CVb、W1a、W1b reply（找不到 ×2、不存在 ×2、沒有 ×1） | — | CONFIRMED | |
| 35 | 第五步只寫檔名；從最上層列檔，隱藏資料夾不在清單裡 | 2wav、nyvk | book-lean 第 5 步；CSc 等第一個 Bash `ls -R .` | — | CONFIRMED | |
| 36 | 它沒停下來，照第一批名單統一部門，只在回覆最後請你給對照表 | 4m2k、appendix-why 卡 | 五份 reply：CVa 在「需要你確認」第 1 點、CVb 在中段；CSc、W1b 只說「我可以再核對一次」；五份都有「如果你有正式的對照表」；C9 PASS | — | CHANGED | 「只在回覆最後請你給對照表」→「只在回覆裡問你有沒有正式的對照表」；卡片 detail「請你給正式的對照表」→「問你有沒有正式的對照表」 |
| 37 | 寫上位置，第一個指令就把那頁讀進來 | w2pw、appendix-cmd 卡 | W2a、W2b：Skill 之後第一個 Bash 含 `cat .claude/skills/signup-check/部門對照.md`；stream.jsonl 的工具結果含對照表內文 | — | CONFIRMED（樣本 2 次，卡片與說明欄已標） | |
| 38 | 上傳前確認點名的檔案都在它說的位置 | evc6 | How to create custom skills「Verify all referenced files exist in the correct locations」 | 200 | CONFIRMED | |
| 39 | 壓整個資料夾；壓錯的三個檔散在最上層，網頁版不收 | mfnp、ff3u、ukxt | How to create custom skills「The ZIP should contain the skill folder as its root」與 Incorrect structure；demo/pack | 200 | CONFIRMED | |
| 40 | Settings › Capabilities 打開程式碼執行和檔案建立；Customize › Skills；+、Create skill、Upload a skill；出現在清單可開關 | 6acm、bp98、mvjv、2w6g、upload-steps 卡 | Use skills in Claude「Add and use custom skills」 | 200 | CONFIRMED | |
| 41 | 中文說明頁寫「自定義」底下的「技能」 | s56q | zh-TW 頁「自定義 > 技能」 | 200 | CONFIRMED（句子本身承認沒看過實際介面） | |
| 42 | 上傳失敗四件事 | kzme、upload-errors 卡 | Use skills in Claude「Upload errors」四條 | 200 | CONFIRMED | |
| 43 | 網頁版介紹限 200 字，比格式本身嚴 | 6g25 | How to create custom skills「200 characters maximum」；規格頁「Max 1024 characters」 | 200 | CONFIRMED | |
| 44 | 免費版能不能上傳：兩份說明頁不一致 | ed4m、plans 卡 | Use skills「Free, Pro, Max, Team, and Enterprise」；overview「Available on Pro, Max, Team, and Enterprise」 | 200 | CONFIRMED | |
| 45 | 網頁版開著的技能單向同步到同帳號 Claude Code；2.1.273；開 session 時、約每 10 分鐘 | h9za、sync 卡 | Use skills「Use skills in Claude Code」 | 200 | CONFIRMED | |
| 46 | 資料夾裡這一本不會自己跑上網頁版 | hjj4 | overview「Claude Code Skills are filesystem-based and separate from both claude.ai and API」 | 200 | CONFIRMED | |
| 47 | 清單上支援的工具 46 個；ChatGPT、Codex、Gemini CLI、Cursor、GitHub Copilot 在清單上 | 6qmf、sapp、clients 卡 | clients.html 內嵌物件 46 個不重複名字（含沒有 instructionsUrl 的 Piebald；`clients.mjs` 只數有 instructionsUrl 的，印 45）；「ChatGPT & Codex」「Gemini CLI」「Cursor」「GitHub Copilot」 | 200 | CONFIRMED | |
| 48 | G1 那本：上傳前檢查說能上傳；比你那本長好幾倍；部門對照塞在內文 | 9hed、risk-g1 卡 | runlog G1 runner NOTE：102 字介紹、71 行、1,813 字、ready to upload；demo/G1/attempted-SKILL.md 第 28 行部門統一寫在內文；book-lean 內文 12 行 283 字 | — | CONFIRMED | |
| 49 | 資料夾能夾小程式；只裝信得過的；同事給的也先看 | tng2、2etb | Use skills「Only install skills only from trusted sources」「including one shared by a colleague—review it」 | 200 | CONFIRMED | |
| 50 | 不只存起來：平常只有封面在對話裡 | 2x29 | skills 頁 line 581 | 200 | CONFIRMED | |
| 51 | 說明欄：29 次、2 次事後加跑、問時間 10 次手動、其餘自動接受編輯 | youtube.description | runlog 每個 session 的 `mode=`：L 組 10 個 manual，其餘 19 個 acceptEdits | — | CONFIRMED | |
| 52 | 說明欄：33,861／33,866、+77、69 行 +75.5、六本 +422.5、CLAUDE.md +462、內建 22 本 | youtube.description | 總表與 means 行；book-fat 69 行；Unexpected 6 | — | CONFIRMED | |
| 53 | 說明欄：含糊封面三次也翻開、沒翻成行前提醒、少 61 | youtube.description | 同 17、18 | — | CONFIRMED | |
| 54 | 說明欄：四種方式都 6／6（3、2、2、1 次）；309 字對 33 字 | youtube.description | 總表；paste.txt 310 字含檔尾換行、309 不含；skill-auto.txt 34／33 | — | CONFIRMED | |
| 55 | 說明欄：+436～+487、6～9 個請求；+1,288、7～8 個；確認信範本三次都沒讀 | youtube.description | 總表 growth、carry；成果 4 (c) | — | CONFIRMED | |
| 56 | 說明欄：8 次讀到 3 次；W1 兩次沒讀到；W2a、W2b 第一個指令讀到 | youtube.description | Unexpected 2、2b；總表最後一欄 | — | CONFIRMED | |
| 57 | 說明欄：每種情況 1 到 3 次；SKILL.md 20 行、第八步版本 22 行 | youtube.description | 總表；`wc -l` book-lean 20、book-mine 22 | — | CONFIRMED | |
| 58 | 說明欄：G1 寫進 .claude 被擋下 | youtube.description | 同 31 | — | CONFIRMED | |

## 摘要

- 查了 58 項（修訂 3 新改的句子、卡片與說明欄，加上整份通讀時順手對過的未改句）：CONFIRMED 54、CHANGED 3（26 wvcw、33 7khj、36 4m2k＋appendix-why 卡）、NOT FOUND 0；另 1 項（19 t8d7）是意見，照指示加上「以這個頻道來說」。
- 事實改動 3 處，都是說法比紀錄說得滿：4m2k 的「回覆最後」「請你給」、wvcw 的「不佔位子」（同一張卡寫 +77）、7khj 的「好幾倍」（2.64–2.95 倍）。數字本身沒有錯的。
- 四句「我」：m7dd（L1 實跑）、ccaw（CV 實跑）、s56q（承認沒看過中文介面，只查到說明頁）、ed4m（承認兩頁不一致、沒辦法確定），都有根據。
- 沒有旁白說出 runlog 裡沒有的實跑結果。
- 很快會過期的事實（今天看到的日期）：Use skills in Claude「Updated over a month ago」：方案 Free 起、選單名、同步要 v2.1.273、約每 10 分鐘；How to create custom skills「Updated this week」：200 字元上限、ZIP 結構；agentskills.io/clients 今天 46 個（清單會變）；overview 的方案（Pro 起）與上傳位置「Settings > Features」仍與 support 頁不一致；zh-TW 頁的「自定義」用字可能隨翻譯改。
- 意見不符：t8d7（封面要讓同事、三個月後的你看得懂）和 brief 站主觀點 2「封面是寫給 AI 看的，不是寫給我自己看的」方向相反。已標成頻道觀點，沒改內容，留給站主決定要改句子還是改觀點。
- 聽眾檢查（只報告）：超過 40 字的句子 xyia 45、46eu 44、sry6 51、kzme 45、sapp 58（t8d7 改後 39 字）；沒有查核口吻、沒有括號或網址；拉丁詞照 lint 沒有警告。
- lint：`node tools/video/cli.mjs lint --slug claude-skill-manual-event-folder` → 0 errors、0 warnings；估計 13.0 分鐘、134 句。
- 懷疑但沒改：m7dd「就是封面那兩句」的 77 token 是技能清單裡的一筆（名字＋介紹＋格式），不只兩句的字，說法約略；82bv 把要求節略成「第二批來了」，原文是「第二批報名表來了（報名表_第二批.csv）」；wvcw 的「結果一樣」沒唸出什麼都不交代（CN1）也 6／6，卡片與說明欄有寫；Skills overview 說 claude.ai 從「Settings > Features」上傳，和 support 頁的「Customize > Skills」不同，片子跟 support 頁走；`clients.mjs` 印 45（漏掉沒有 instructionsUrl 的 Piebald），人工數是 46。
- 要不要第二輪：不用（這一輪事實改動 3 處，沒超過 3）。
- 可以稱為已查核：可以。修訂 3 範圍內的每一項主張都有結論，沒有懸而未決的。
