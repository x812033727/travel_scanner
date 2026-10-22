# verify-2：claude-skill-manual-event-folder

查核日 2026-10-21（round 2，查核者不是撰稿者，也不是 round 1 的查核者）。九個官方頁今天重抓一次：`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，每個 host 間隔 1.5 秒，去掉 `<!-- -->`、script、style 後讀；原檔、文字與輔助腳本在 `<work>/_tools/verify2/`（`fetch.sh`、`totext.mjs`、`dump.mjs`、`len.mjs`、`len2.mjs`、`pick.mjs`、`edit.mjs`）。實跑主張逐字對 `runlog.txt` 與 `demo/`；code 卡重跑 round 1 的 `codecheck.mjs`。網路搜尋 0 次。

| 頁 | HTTP |
| --- | --- |
| support Use skills in Claude（en） | 200 |
| support How to create custom skills | 200 |
| support What are skills? | 200 |
| support zh-TW 12512180（轉到 …/12512180-在-claude-中使用技能） | 200 |
| platform Agent Skills overview | 200 |
| code.claude.com Extend Claude with skills | 200 |
| agentskills.io/specification | 200 |
| agentskills.io/clients | 200 |
| learn.chatgpt.com Build skills | 200 |

抽樣方法：round 1 判 CONFIRMED 的 78 條（#1–#82 去掉它改過的 #42、#45、#51、#76）用 mulberry32、種子 20261021 做 Fisher–Yates 洗牌，取前 26 條（三分之一）：#3、5、9、10、13、14、16、18、30、31、34、37、46、52、57、58、61、62、63、64、66、70、72、73、77、81。另外加查四個指定的疑點：#6（3a7t）、#23（xyia）、#74–75（sync）；#70（s56q）剛好在樣本裡。編號沿用 verify-1。

## A. round 1 改過的四條

| # | 主張 | 在哪裡 | 出處 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 76 | 清單上支援的工具 46 個 | clients.stats、6qmf | clients.html 內嵌的 `{name:…,description:…}` 物件：46 個、名字不重複（Agentman … pi，含 Piebald）；Gemini CLI、Cursor、GitHub Copilot 各 1 | 200 | CONFIRMED（round 1 的 46 成立） | |
| 45 | 每次貼七步 309 字、其他 33 字；ynwc「三百零九個字」 | four-ways、differences、ynwc | D/prompts/paste.txt 去掉檔尾換行 309 字元（其中 11 個換行、33 個空白、265 個非空白字）；skill-auto.txt 33 字元、0 空白 | — | CONFIRMED（309 是含換行與縮排空白的字元數；見「懷疑但沒動」） | |
| 51 | ykf3「第一次還多一欄狀態：待回覆、未回答；兩次寄信名單裡她都只出現一次」 | ykf3、step8-result | D/W1a/輸出/待回覆.csv 四欄、狀態「待回覆（未回答）」；D/W1b 三欄；兩份確認信名單 yating 各 1 行；RL 執行順序 W1a（00:48:02Z）先於 W1b（00:48:49Z） | — | CONFIRMED | |
| 42 | run-steps 第 2 步「整段共有三個指令被擋下」 | run-steps.steps[1] | RL CSa：`permission_denials=3`；第 1 個在讀檔（「A variable in this command can't be checked」），第 2 個是寫前查檔尾（xxd），第 3 個是 cd＋重導向寫入；第 3 步（最上層 `部門對照.md` exit 1 → `ls -a .claude/skills/signup-check` → cat 讀到）也對 | — | CONFIRMED | |

## B. 抽樣與指定疑點

| # | 主張 | 在哪裡 | 出處 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 只說一句，三次都翻開（3／3） | result、mv44 | RL 第 1525、1816、2100 行 CSa／CSb／CSc `VERDICT opened signup-check: YES` | — | CONFIRMED | |
| 5 | 點名的附件 8 次裡 5 次回說找不到 | result、74qp | RL 總表最後一欄：CSa、CSb、CVc yes；CSc、CVa、CVb、W1a、W1b no；五份 reply.md 都說不存在／找不到 | — | CONFIRMED | |
| 6 | 3a7t「只在回覆最後提一句」 | stakes 3a7t | D/CSc reply 第 21／22 行、W1a 第 11／13 行、W1b 第 16／17 行（在後段）；CVa 第 18／22 行（最後一段第 1 點，後面還有兩點與結語）；CVb 第 13／20 行（中段，後面還有飲食統計） | — | CHANGED | 「只在回覆最後提一句」→「只在回覆裡提一句」 |
| 9 | SKILL.md 純文字，只有最上面幾行有規矩 | md-ask bvat | spec「There are no format restrictions.」 | 200 | CONFIRMED | |
| 10 | 封面第 1–7 行逐字、全檔 20 行 | cover-name、cover-desc、cover-when | codecheck：三張都 MATCH，file has 20 | — | CONFIRMED | |
| 13 | 名字只能小寫英文、數字、連字號，要跟資料夾同名 | name-rule | spec「Lowercase letters, numbers, and hyphens only.」「Must match the parent directory name」 | 200 | CONFIRMED | |
| 14 | 介紹寫中文沒關係 | name-rule | RL M2 book-lean `PASS description non-empty (60 characters)`、`VERDICT ready to upload`；CS 3／3 翻開 | — | CONFIRMED | |
| 16 | 網頁版上傳 name、description 都要有；缺 name 判 fix before upload | no-name 7ei2 | create「name and description fields, which are required metadata」；RL 第 221 行 `VERDICT fix before upload`（第一支的資料夾，name FAIL） | 200 | CONFIRMED | |
| 18 | 平常只看封面，內文不讀 | shelf-ask | cc「a skill's body loads only when it's used」；RL LF 33,939（+75.5）≈ L1 33,940.5（+77） | 200 | CONFIRMED | |
| 23 | xyia「不管問什麼，都多帶四百六十二個」 | xyia、differences、gwue | RL `LM 34325.5 (+462)`（問時間）；另一種要求（檢查第二批）CMa 34,671／CMb 34,669 對 CN1 34,209 ＝ +462／+460，書櫃同為 27 本；cc 頁稱 CLAUDE.md 為「always-loaded guidance」、「Unlike CLAUDE.md content, a skill's body loads only when it's used」 | 200 | CONFIRMED（保留原句：兩種要求都量到 460 上下，加上官方頁說 CLAUDE.md 一直載入） | |
| 30 | 含糊的三次都翻開，沒翻成別本 | vague | RL 第 1671、1956、2240 行 `VERDICT opened checklist: YES (other booklets opened: none)` | — | CONFIRMED | |
| 31 | 開場只省 61 token | vague | CV 平均 34,225.3，CS 平均 34,286 → 差 60.7 | — | CONFIRMED | |
| 34 | 壞例「幫忙處理 PDF」、好例三件事＋什麼時候用 | good-bad | spec「description: Helps with PDFs.」、「Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms…」 | 200 | CONFIRMED | |
| 37 | 第一批兩個王志明：業務部、研發部 | two-wangs、j945 | D/start/輸出/確認信名單.csv 第 3、6 行逐字 | — | CONFIRMED | |
| 46 | 四種方式六項檢查都 6／6 | four-ways | RL 總表 CPa／CPb、CMa／CMb、CSa–c、CN1 都 PPPPPP | — | CONFIRMED | |
| 52 | 兩次寄信名單裡她都只出現一次 | ykf3 | 見 A #51 | — | CONFIRMED | |
| 57 | 翻開後整本留在對話裡；不會重讀 | stays | cc「enters the conversation as a single message and stays there across later turns」「does not re-read the skill file on later turns」 | 200 | CONFIRMED | |
| 58 | 需要附件的八次讀到三次、五次找不到 | appendix-miss、rw2t | 見 #5；八次＝CS 3＋CV 3＋W1 2 | — | CONFIRMED | |
| 61 | 只改第 17 行，卡片第 15–18 行逐字 | appendix-fix | RL W2-setup `17c17`（`照 部門對照.md 統一。` → `照 .claude/skills/signup-check/部門對照.md 統一。`）；codecheck appendix-fix MATCH | — | CONFIRMED | |
| 62 | 改一行之後 2／2，都在第一個指令讀到 | appendix-fixed、w2pw | RL 總表 W2a、W2b `部門對照-seen yes`；第 4084 行 NOTE「read on the first try with Bash」 | — | CONFIRMED | |
| 63 | 引文 `cat .claude/skills/signup-check/部門對照.md` | appendix-cmd | RL 第 1441、1723 行逐字；W2 第 3841、3985 行的第一個 Bash 含同一段 | — | CONFIRMED | |
| 64 | 上傳前確認附件檔都在 | appendix-rule | create「3. Verify all referenced files exist in the correct locations.」 | 200 | CONFIRMED | |
| 66 | 對的 zip 三筆都在 signup-check/ 底下；錯的散在最上層 | zip | D/pack/signup-check.zip.txt、signup-check-wrong.zip.txt | — | CONFIRMED | |
| 70 | s56q「我只查到機器翻譯的說明頁，你看一眼「自訂」底下」 | upload-cast s56q | zh-TW 頁：「導航到自定義 > 技能」「導航到設置 > 功能」；全頁沒有「自訂」，也沒有說自己是機器翻譯 | 200 | CHANGED | →「中文介面上這些選單叫什麼，我只查到中文說明頁，它寫的是「自定義」底下的「技能」。」（仍是「我」的不確定句） |
| 72 | 網頁版介紹限 200 字，規格 1,024；signup-check 60 字 | 6g25 | create「(200 characters maximum)」；spec「Max 1024 characters」；RL M2 60 characters | 200 | CONFIRMED | |
| 73 | 方案兩頁不一致：Free 起／Pro 起 | plans、ed4m | use「Skills are available for users on Free, Pro, Max, Team, and Enterprise plans」；overview「Available on Pro, Max, Team, and Enterprise plans with code execution enabled」 | 200 | CONFIRMED | |
| 74 | 網頁版開著的技能單向同步到同帳號 Claude Code，要 2.1.273 以上；開 session 時、約每 10 分鐘 | sync h9za、b996 | use「needs Claude Code v2.1.273 or later」「Skills sync when a Claude Code session starts, then check for changes about every 10 minutes」「The sync is one-way」；cc〈Skills synced from claude.ai〉同樣寫下載、從不上傳、v2.1.273。overview 寫「Custom Skills do not sync across surfaces」 | 200 | CONFIRMED（兩頁一致的說法為準；overview 那句與它們不一致，見摘要） | claims c69 補上 cc 頁與這個判定（不是事實修改） |
| 75 | 資料夾裡這一本不會自己上網頁版 | sync hjj4 | overview「Claude Code Skills are filesystem-based and separate from both claude.ai and API」；use「never changes anything in it」；cc「never uploads them」 | 200 | CONFIRMED | |
| 77 | Gemini CLI、Cursor、GitHub Copilot 都在清單上 | sapp | clients.html 各 1 筆 | 200 | CONFIRMED | |
| 81 | 站主觀點（第三次門檻、看不懂就不裝、CLAUDE.md／說明書分工、封面兩句、內文／附件） | b5c9、bhpi、md-rule 等 | brief.md 站主觀點第 1–4 點；句子都標「這個頻道的門檻／做法」 | — | CONFIRMED | |

## 摘要

- 查了 33 條：round 1 改過的 4 條（全部 CONFIRMED），抽樣 26 條（種子 20261021，名單見上），加指定疑點 #6、#23、#74、#75。CONFIRMED 31、CHANGED 2（#6 3a7t、#70 s56q）、NOT FOUND 0。
- 這一輪改的事實：
  1. 3a7t「只在回覆最後提一句」→「只在回覆裡提一句」：CVb 把找不到附件放在回覆中段，CVa 放在最後一段的第 1 點，不是最後一句（claims c6 一併改）。
  2. s56q：zh-TW 說明頁的用字是「自定義 > 技能」，頁上沒有「自訂」，也沒有說自己是機器翻譯；改成「我只查到中文說明頁，它寫的是「自定義」底下的「技能」」（claims c65 一併改）。
- 沒改、但判定保留的：xyia 保留原句（理由：檢查第二批那種要求也量到 CM 比 CN1 多 460～462，加上 cc 頁說 CLAUDE.md 一直載入）；同步那張卡保留（support〈Use skills〉與 Claude Code Docs〈Skills synced from claude.ai〉兩頁都說網頁版會單向同步到 Claude Code，overview 的「Custom Skills do not sync across surfaces」是唯一不同的說法；卡片右欄「不會自己跑上網頁版」三頁都支持）。claims c69 補了 cc 頁的出處和這個判定。
- 很快會過期的事實（今天看到的官方日期）：Use skills「Updated over a month ago」：方案（Free 起）、選單名、同步要 v2.1.273、約每 10 分鐘；How to create custom skills「Updated this week」：200 字元上限；agentskills.io/clients 今天 46 筆（清單會變）；overview 的方案（Pro 起）與「do not sync」仍與 support 頁不一致；zh-TW 頁的「自定義」用字可能隨翻譯更新。
- 觀點對不上的地方：沒有。
- 聽眾檢查（只報告）：改過的 s56q 是 40 字（剛好沒有超過 40）；3a7t 25 字；沒有「經查證」「根據官方文件」「本影片」；旁白沒有括號或網址（s56q 的「」是引號，不是括號）。
- lint：`node tools/video/cli.mjs lint --slug claude-skill-manual-event-folder` → 0 errors, 0 warnings（估 15.8 分鐘、174 句、3,518 口語單位）。
- 懷疑但沒動：
  - 「每次貼七步 309 字」算進了 11 個換行和 33 個空白（縮排與英文前後的空格），看得到的字是 265 個；當成字元數是對的，round 1 的修正成立，但觀眾自己數會數到比較少。要不要改成「約三百字」由協調者決定。
  - b996／卡片「開新對話時」對應官方的「when a Claude Code session starts」；在 Claude Code 一個 session 就是一段對話，意思相同，沒改。
  - sync 卡的 source 仍寫「Skills overview」，它支持右欄，但同一頁也寫「do not sync」；如果想避免觀眾去查時看到矛盾，可以把 source 換成 Claude Code Docs，這是出處標示，沒改。
  - 片長估 15.8 分鐘，超過 target_minutes [9, 12]（不是事實問題）。
- 需要第三輪：否。這一輪改了 2 個事實（不超過 3 個），round 1 改的 4 條今天都對得上，沒有未解決的主張；這支腳本可以算查核完成。
