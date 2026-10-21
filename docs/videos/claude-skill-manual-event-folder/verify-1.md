# verify-1：claude-skill-manual-event-folder

查核日 2026-10-21（round 1，查核者不是撰稿者）。官方頁都在今天用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重抓（每個 host 間隔 1.5 秒，去掉 `<!-- -->` 後讀），原檔與抽出的文字在 `<work>/_tools/verify1/`；主張清單先抽到 `<work>/_tools/verify1-claims-raw.txt`。實跑主張逐字對 `runlog.txt` 與 `demo/`（code 卡以 `_tools/verify1/codecheck.mjs` 逐行比對原檔）。網路搜尋 0 次。

官方頁今天的狀態：

| 頁 | URL | HTTP |
| --- | --- | --- |
| Use skills in Claude | https://support.claude.com/en/articles/12512180-use-skills-in-claude | 200（頁面標「Updated over a month ago」） |
| How to create custom skills | https://support.claude.com/en/articles/12512198-how-to-create-custom-skills | 200（「Updated this week」） |
| What are skills? | https://support.claude.com/en/articles/12512176-what-are-skills | 200 |
| 在 Claude 中使用技能（zh-TW） | https://support.claude.com/zh-TW/articles/12512180 | 200（轉到 …/12512180-在-claude-中使用技能） |
| Agent Skills overview | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | 200 |
| Extend Claude with skills | https://code.claude.com/docs/en/skills | 200 |
| Specification | https://agentskills.io/specification | 200 |
| Client Showcase | https://agentskills.io/clients | 200 |
| Build skills | https://learn.chatgpt.com/docs/build-skills | 200 |

## 主張表

縮寫：RL＝runlog.txt，D＝demo/；「官方」欄的 HTTP 都是上表的 200。

| # | 主張 | 在哪裡 | 出處 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Skill 是指示、程式、資源的資料夾，需要時才載入（說明書的比喻底） | open zmxa；c1 | support What are skills?「Skills are folders of instructions, scripts, and resources that Claude loads dynamically」 | 200 | CONFIRMED | |
| 2 | 書櫃上有報名檢查、會議紀錄、行前提醒信 | uses | D/shelf5/meeting-notes、reminder-mail，D/booklets/book-lean | — | CONFIRMED | |
| 3 | 只說一句，三次都翻開這一本（3／3） | result、run-stats、mv44 | RL CSa–CSc `VERDICT opened signup-check: YES` | — | CONFIRMED | |
| 4 | 寄信名單 16 → 18；缺 Email 的那位另外列出 | result、2u43、run-stats、5bjj | RL M6 起點 16；CSa–c B5 PASS；D/CS*/輸出 18 個 @ | — | CONFIRMED | |
| 5 | 點名的附件 8 次裡 5 次回說找不到 | result 74qp、appendix-miss | RL 總表最後一欄（CSc、CVa、CVb、W1a、W1b = no）；五份 reply.md 都說不存在／找不到 | — | CONFIRMED | |
| 6 | 找不到時不停下來，照自己的猜法做完，只在回覆最後提一句 | stakes 3a7t | D/CSc、CVa、CVb、W1a、W1b reply.md | — | CONFIRMED（見「懷疑但沒動」：CVb、W1a 那句不在最後一句） | |
| 7 | 一本說明書＝一個資料夾：講座籌備/.claude/skills/signup-check/，裡面 SKILL.md＋兩頁附件 | folder | RL CSa folder before；D/booklets/book-lean | — | CONFIRMED | |
| 8 | 上一支裡第二批交給 signup-check 檢查 | y2w4 | docs/videos/claude-code-beginner-event-folder/video.json skill-ask、skill-run | — | CONFIRMED | |
| 9 | SKILL.md 是純文字，有規矩的只有最上面幾行 | md-ask bvat | spec「There are no format restrictions」（Body content） | 200 | CONFIRMED | |
| 10 | 封面第 1–7 行逐字、全檔 20 行，亮第 2、3–5、5–6 行 | cover-name、cover-desc、cover-when | D/booklets/book-lean/signup-check/SKILL.md（codecheck MATCH） | — | CONFIRMED | |
| 11 | 介紹的全文（旁白 fzhb、9j2b、4tea 照唸） | cover-desc、cover-when | 同上第 4–6 行 | — | CONFIRMED | |
| 12 | 介紹要寫做什麼＋什麼時候用 | fxfg、cover-rule | spec「Describes what the skill does and when to use it」；create「A clear description of what the skill does and when to use it」 | 200 | CONFIRMED | |
| 13 | 名字只能小寫英文、數字、連字號，要跟資料夾同名 | name-rule hwqf、fsk8 | spec name：「Lowercase letters, numbers, and hyphens only」「Must match the parent directory name」 | 200 | CONFIRMED | |
| 14 | 介紹寫中文沒關係 | name-rule | RL M2 PASS（60 characters）、M3 passed、CS 3／3 翻開 | — | CONFIRMED | |
| 15 | 少了 name：Claude Code 拿資料夾名代替 | no-name abdn | code.claude.com skills frontmatter「name … Defaults to the directory name」 | 200 | CONFIRMED | |
| 16 | 網頁版上傳要 name 和 description 都有；上傳前檢查判 fix before upload／這本 ready to upload | no-name 7ei2 | create「name and description fields, which are required metadata」；RL M2 | 200 | CONFIRMED | |
| 17 | 「活動說明.md 寫的講座幾點結束？…」回 16:30，一本都沒翻 | time-ask | D/prompts/time.txt（逐字）；D/L1a/reply.md「16:30」；RL L1a opened none | — | CONFIRMED | |
| 18 | 平常只看封面，內文一頁都不讀 | shelf-ask 9qbz | RL LF＝L1（+75.5 對 +77）；cc「a skill's body loads only when it's used」 | 200 | CONFIRMED | |
| 19 | 沒放：33,861／33,866；約三萬三千八百多 | size-table、a4xv | RL 總表 L0a、L0b | — | CONFIRMED | |
| 20 | 一本 20 行：33,940／33,941，+77 | size-table、m7dd | RL 總表、`first= means L1 33940.5 (+77)` | — | CONFIRMED | |
| 21 | 69 行：33,940／33,938，+75.5（旁白「七十五個上下」） | size-table、za92 | RL 總表、`LF 33939 (+75.5)`；book-fat 69 行 | — | CONFIRMED | |
| 22 | 六本：34,286／34,286，+422.5；旁白「四百二十二個，一本約七十個」 | size-table、5msh | RL `L6 34286 (+422.5)`；422.5／6＝70.4 | — | CONFIRMED | |
| 23 | 七步在 CLAUDE.md：34,328／34,323，+462 | size-table、xyia、claude-md、differences gwue | RL `LM 34325.5 (+462)`；D/claude-md/claude-md-book.CLAUDE.md 含同樣七步 | — | CONFIRMED | |
| 24 | 引文「Metadata (~100 tokens): The name and description fields are loaded at startup for all skills」 | progressive | spec Progressive disclosure（逐字） | 200 | CONFIRMED | |
| 25 | 每次來回每本封面都送進去 | shelf-stop | cc「Claude Code loads a listing of skill names and descriptions into context」；RL CS first= 34,285–34,287 對 CN1 34,209 | 200 | CONFIRMED | |
| 26 | 書櫃 22 → 23 → 28 | shelf-count | RL L0／L1／L6 skillview `shelf:` | — | CONFIRMED | |
| 27 | 網頁版專案指示一直載入 | claude-md | What are skills?「Projects provide static background knowledge that's always loaded」 | 200 | CONFIRMED | |
| 28 | 另外五本的用途與規則（150 字、三段＋未指定、待確認、15／120 字、通用草稿不寄出、11/12） | uses-table、t84f–6z42 | D/shelf5/*/SKILL.md 逐條 | — | CONFIRMED | |
| 29 | 含糊封面：名字 checklist、介紹「檢查用的步驟。」，內文一字不動，書櫃上有 reminder-mail | vague czys、u5xg | D/booklets/book-vague（內文與 book-lean 第 8 行起 diff 相同；附件 cmp 相同）；RL CV extras 含 shelf5 | — | CONFIRMED | |
| 30 | 含糊的三次也都翻開，沒翻成行前提醒 | vague ccaw、7wge | RL CVa–c `VERDICT opened checklist: YES (other booklets opened: none)` | — | CONFIRMED | |
| 31 | 開場只省 61 token | vague | RL CV 34,223／34,228／34,225 對 CS 34,286／34,287／34,285，平均差 60.7 | — | CONFIRMED | |
| 32 | 引文「Check that the skill's description field clearly explains when it should be used.」 | why-cover | support Use skills › Troubleshooting › Claude isn't using a skill（逐字） | 200 | CONFIRMED | |
| 33 | 它決定翻不翻、翻哪一本只看封面 | t8d7、pick-stop | create「Claude uses this to determine when to invoke your skill」 | 200 | CONFIRMED | |
| 34 | 壞例「幫忙處理 PDF」；好例抽文字表格、填表、合併；處理 PDF、提到表單時用 | good-bad | spec description：Poor「Helps with PDFs.」、Good「Extracts text and tables … fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms…」 | 200 | CONFIRMED | |
| 35 | `claude plugin validate` 三本都 ✔ Validation passed | validate | RL M3 | — | CONFIRMED | |
| 36 | 內文第 9–20 行逐字，七步照唸 | body-1 至 body-7 | D/booklets/book-lean SKILL.md（codecheck MATCH，亮的行對得上） | — | CONFIRMED | |
| 37 | 第一批兩個王志明：chihming.wang 業務部、cm.wang 研發部 | two-wangs、j945 | D/start/輸出/確認信名單.csv 第 3、6 行 | — | CONFIRMED | |
| 38 | 每一份報名表都有一筆「測試」；這批叫測試二 | body-3 ipd6 | `_tools/seed/講座籌備/報名表.csv` 第 7 行「測試」；D/start/報名表_第二批.csv 第 6 行「測試二」 | — | CONFIRMED | |
| 39 | 「才」：今天不用寫信 | body-7 tr6z | D/CSa/reply.md 最後一句「我沒有寫確認信，技能說明要寫的時候才寫。」 | — | CONFIRMED | |
| 40 | 那一句要求全文；回覆第一句全文 | ask | D/prompts/skill-auto.txt、D/CSa/reply.md（逐字） | — | CONFIRMED | |
| 41 | 第一個動作就是翻開 signup-check | ask 5dba | RL CSa 第一個 tool_use 是 Skill | — | CONFIRMED | |
| 42 | CSa 的步驟：翻開 → 讀檔（擋下的指令）→ 部門對照最上層找不到、說明書資料夾讀到 → 改三個檔（兩人進名單、宋柏均進要補資料）→ 提醒黃雅婷 | run-steps | RL CSa tool_use 序列：被擋的 3 個是讀檔時 1 個（變數）、寫檔時 2 個（xxd、cd＋重導向） | — | CHANGED（卡片第 2 步把三個都放在讀檔那一步） | steps[1].detail「三個指令被擋下」→「整段共有三個指令被擋下」；旁白 ycuu「中間三個指令被擋下」不動 |
| 43 | 要補資料 3 → 4 | run-stats | D/start/輸出/要補資料.csv 3 人；D/CSa–c 4 人 | — | CONFIRMED | |
| 44 | 六項檢查三次都過，原始報名表一字沒改 | run-stats a8na | RL 成果 1 NOTE（兩個雜湊不變） | — | CONFIRMED | |
| 45 | 你要打的字：每次貼七步 310 字、其他 34 字 | four-ways、differences、ynwc | D/prompts/paste.txt 310 字元、skill-auto.txt 34 字元，都含檔尾一個換行；要求本身 309、33 字（「第二批報名表來了（報名表_第二批.csv），照平常的方式檢查一下。」是 33 字） | — | CHANGED | 「310 字」→「309 字」（four-ways、differences）；「34 字」×3 →「33 字」；ynwc「三百一十個字」→「三百零九個字」 |
| 46 | 四種方式六項檢查都 6／6；三種交代方式結果一樣；不交代也猜得到 | four-ways wvcw、wmqu | RL 總表 CP、CM、CS、CN1 全 PPPPPP；成果 1 NOTE | — | CONFIRMED | |
| 47 | CN1 看第一批的名單和日誌推出做法 | t5dc | D/CN1/reply.md 第一段 | — | CONFIRMED | |
| 48 | 只有說明書能整個資料夾帶去網頁版 | differences vnha | support Use skills「Upload a ZIP file containing your skill folder」 | 200 | CONFIRMED | |
| 49 | 第 8 步兩行逐字、全檔 22 行 | step8、step8-b | D/booklets/book-mine（codecheck MATCH） | — | CONFIRMED | |
| 50 | 待回覆.csv 卡片原文（含「狀態｜待回覆（未回答）」）；跑兩次都多一份、只有一列 | step8-result、2q52 | D/W1a/輸出/待回覆.csv 四欄；D/W1b/輸出/待回覆.csv 三欄（沒有狀態欄） | — | CONFIRMED（卡片＝W1a） | |
| 51 | 狀態寫待回覆、未回答（接在「跑兩次」之後，聽起來兩次都有） | ykf3 | 同上：只有 W1a 有狀態欄 | — | CHANGED | 「狀態寫待回覆、未回答；寄信名單裡她也只出現一次。」→「第一次還多一欄狀態：待回覆、未回答；兩次寄信名單裡她都只出現一次。」 |
| 52 | 她在寄信名單裡只出現一次 | ykf3 | RL W1a、W1b mine M4 PASS；兩份名單 yating 各一行 | — | CONFIRMED | |
| 53 | G1 的要求（六段接起來＝全文；說明欄也有全文） | g1-ask、youtube.description | D/prompts/write-skill.txt（146 字逐字） | — | CONFIRMED | |
| 54 | G1 寫進 .claude 被擋下、要你同意 | g1-result 5jsg | RL G1 tool_error「…but you haven't granted it yet.」、reply「只要你允許寫入這個路徑」 | — | CONFIRMED | |
| 55 | 它想寫的：介紹 102 字、內文 71 行、部門對照寫進內文；你寫的：60 字、12 行、附件 | g1-result | RL G1 第二條 NOTE（cover-check 102 characters、body 71 lines）；D/G1/attempted-SKILL.md 第 28 行；RL M2 book-lean | — | CONFIRMED | |
| 56 | 翻開前一樣大；翻開那一步短的 +436～+487、長的 +1,288（將近三倍）；之後 6～9／7～8 個請求帶著；確認信範本三次沒碰；長的六項三次過 | fat、dwrx、7khj、mq68、5j4b | RL 總表 growth、carry；成果 4 (a)(b)(c)；1288／453＝2.84 | — | CONFIRMED | |
| 57 | 翻開後整本留在對話裡；改了說明書，進行中的對話不會重讀 | stays | cc「enters the conversation as a single message and stays there … does not re-read the skill file on later turns」 | 200 | CONFIRMED | |
| 58 | 需要附件的八次讀到三次（3／8），五次找不到（5／8） | appendix-miss、rw2t | RL 總表最後一欄；Unexpected 2 | — | CONFIRMED | |
| 59 | CVa 回覆原文「部門對照.md 不存在。」 | appendix-quote | D/CVa/reply.md「需要你確認 1.」 | — | CONFIRMED | |
| 60 | 找不到的五次：從最上層列檔，.claude 不在清單；照第一批名單統一；請你給對照表；部門那一項照樣過 | appendix-why | RL CSc、CVa、CVb、W1a、W1b 的第一批 Bash 都是 `ls -R .` 加根目錄的 `部門對照.md`；五份 reply；Unexpected 2（C9 PASS） | — | CONFIRMED | |
| 61 | 只改第 17 行，卡片第 15–18 行逐字 | appendix-fix | RL W2-setup diff `17c17`；D/booklets/book-loc（codecheck MATCH） | — | CONFIRMED | |
| 62 | 0／2（W1）對 2／2（W2）；兩次都在第一個指令讀到 | appendix-fixed、w2pw | RL Unexpected 2b、W2a／W2b NOTE（翻開後第一個 Bash 就含 cat，內容有回來） | — | CONFIRMED | |
| 63 | 引文 `cat .claude/skills/signup-check/部門對照.md`；新人部門照對照表統一，檢查全過 | appendix-cmd、bdns | RL 第 3841、3985 行 tool_use；D/W2a、W2b reply（業務→業務部、Marketing→行銷部）；B1–B6 6／6 | — | CONFIRMED | |
| 64 | 附件怎麼點名：寫位置、寫什麼時候看、上傳前確認檔都在 | appendix-rule | 第 1 點 RL W2；第 3 點 create「Verify all referenced files exist in the correct locations」 | 200 | CONFIRMED | |
| 65 | 進內文／放附件的選法 | appendix-choose、ra5x | spec「Move detailed reference material to separate files」；cc「every line is a recurring token cost」 | 200 | CONFIRMED | |
| 66 | 對的 zip 三筆都在 signup-check/ 底下；錯的散在最上層 | zip | RL M4、D/pack/*.txt | — | CONFIRMED | |
| 67 | 網頁版不收檔案散在最上層的結構 | zip ukxt | create Package your skill「The ZIP should contain the skill folder as its root」、Incorrect structure | 200 | CONFIRMED | |
| 68 | 上傳步驟：Settings › Capabilities 開 Code execution and file creation → Customize › Skills →「+」→「+ Create skill」→「Upload a skill」→ 出現在清單可開關 | upload-steps、6acm–2w6g | support Use skills：How to enable skills、Add and use custom skills（逐項） | 200 | CONFIRMED | |
| 69 | screencast 錨點 #h_a4222fa77b 是「Add and use custom skills」 | upload-cast | use.html `id="h_a4222fa77b">Add and use custom skills` | 200 | CONFIRMED | |
| 70 | 中文選單名只查到機器翻譯的說明頁，看「自訂」底下 | upload-cast s56q | zh-TW 頁用「設置 > 功能」「自定義 > 技能」；頁面沒有寫它是機器翻譯 | 200 | CONFIRMED（「我」的不確定句；用詞見「懷疑但沒動」） | |
| 71 | 上傳失敗四個原因 | upload-errors | support Use skills › Upload errors（四條） | 200 | CONFIRMED | |
| 72 | 網頁版介紹限 200 字，比規格嚴（規格 1,024）；signup-check 60 字 | upload-errors 6g25 | create「200 characters maximum」；spec「Max 1024 characters」；RL M2 60 characters | 200 | CONFIRMED | |
| 73 | 方案：Use skills 寫 Free、Pro、Max、Team、Enterprise；overview 寫 Pro、Max、Team、Enterprise | plans、ed4m | support Use skills 第二段；overview ### claude.ai「Available on Pro, Max, Team, and Enterprise plans」 | 200 | CONFIRMED | |
| 74 | 網頁版開著的技能單向同步到同帳號的 Claude Code，要 2.1.273 以上；開 session 時同步、約每 10 分鐘查一次 | sync h9za、b996 | support Use skills › Use skills in Claude Code；cc「requires Claude Code v2.1.273 or later」 | 200 | CONFIRMED | |
| 75 | 資料夾裡這本不會自己上網頁版 | sync hjj4 | overview「Claude Code Skills are filesystem-based and separate from both claude.ai and API」 | 200 | CONFIRMED | |
| 76 | 公開標準；清單上支援的工具 45 個 | clients、6qmf | clients 頁今天 46 筆（name 陣列：Junie … OpenClaw，含 Piebald）；撰稿者的 clients.mjs 正規式要求 instructionsUrl，漏掉沒有這欄的 Piebald；撰稿時的原檔 pages/clients.html 也是 46 筆；What are skills?「Agent Skills open standard」 | 200 | CHANGED | stats「45」→「46」；6qmf「四十五個」→「四十六個」 |
| 77 | Gemini CLI、Cursor、GitHub Copilot 都在上面 | clients sapp | clients 頁 | 200 | CONFIRMED | |
| 78 | ChatGPT 桌面版側邊欄有 Skills、打 @；Codex 打 $ 或 /skills；網頁版單獨一本不行、透過外掛；照介紹自己挑 | chatgpt | Build skills：「Standalone skills are available in the ChatGPT desktop app, Codex CLI, and IDE extension. Skills bundled in plugins are also available … ChatGPT on the web」「open Skills in the sidebar」「type @」「run /skills or type $」「Implicit invocation」 | 200 | CONFIRMED | |
| 79 | 資料夾能夾小程式，AI 會執行 | risk tng2 | spec「scripts/ … executable code that agents can run」；create Add scripts | 200 | CONFIRMED | |
| 80 | 只裝自己寫的或信得過的來源；同事給的也先看；每個檔都打開看 | risk 2etb、fnmw | support Use skills「Only install skills only from trusted sources」「including one shared by a colleague—review it before enabling」「reading the contents of the files」；overview「Use Skills only from trusted sources」 | 200 | CONFIRMED | |
| 81 | 站主觀點：第三次的門檻、看不懂的就不裝、CLAUDE.md 與說明書的分工、封面兩句、內文／附件 | three b5c9、risk bhpi、md-rule、cover-rule、appendix-choose | brief.md 站主觀點第 1–4 點 | — | CONFIRMED（標成「這個頻道的門檻／做法」） | |
| 82 | 說明欄：29 次（2 次事後加跑）、Windows 11、2.1.295、sonnet、手動 10 次其餘自動接受編輯、1 到 3 次、G1 被擋、W2 2 次、只寫檔名 8 次讀到 3 次、20 行與 22 行 | youtube.description | RL 開頭、總表（L 組 10 次 manual，其餘 19 次 acceptEdits）、Unexpected 2、2b | — | CONFIRMED | |
| 83 | 標題、縮圖、tags | youtube.title、thumbnail、tags | 無數字 | — | OUT OF SCOPE | |

## 摘要

- 主張 83 條：CONFIRMED 78、CHANGED 4（#42、#45、#51、#76；#45 一組數字算一條）、NOT FOUND 0、OUT OF SCOPE 1。
- 改過的事實：
  1. 支援工具 45 → 46（clients 卡、6qmf、claims c71 與「與企劃不同」那一行）。
  2. 你要打的字 310／34 → 309／33（four-ways、differences、ynwc、claims c39、c46、示範表、「與企劃不同」）：撰稿者數的是檔案字元，含檔尾換行。
  3. ykf3：「狀態」欄只有 W1a 有，W1b 的 待回覆.csv 只有三欄；改成「第一次還多一欄狀態…兩次寄信名單裡她都只出現一次」（claims c48）。
  4. run-steps 第 2 步：CSa 的三次拒絕只有一次在讀檔，兩次在寫檔；細節改成「整段共有三個指令被擋下」（claims c41）。
- 很快會過期的事實（今天看到的官方日期）：Use skills in Claude「Updated over a month ago」：方案清單（Free 起）、選單名 Settings › Capabilities、Customize › Skills、「+」→「+ Create skill」→「Upload a skill」、Claude Code 同步要 v2.1.273、約每 10 分鐘；How to create custom skills「Updated this week」：200 字元上限；agentskills.io/clients 46 筆（清單會一直變）；learn.chatgpt.com Build skills 的 @、$、/skills 與「網頁版只透過外掛」；overview 的方案（Pro 起）與 Use skills（Free 起）至今仍不一致。
- 觀點對不上的地方：沒有。觀點句都標成「這個頻道的門檻／做法」或「所以…」的選擇規則，與 brief 站主觀點第 1–4 點一致。
- 聽眾檢查（只報告）：超過 40 字的句子 2 句：y2w4（41 字）、mvjv（42 字）；沒有「經查證」「根據官方文件」「本影片」；旁白沒有括號或網址；沒看到揭曉早於引出句。
- lint：`node tools/video/cli.mjs lint --slug claude-skill-manual-event-folder` → 0 errors, 0 warnings（估計 15.8 分鐘、174 句、3,518 口語單位）。
- 懷疑但沒動：
  - s56q「我只查到機器翻譯的說明頁，你看一眼『自訂』底下」：zh-TW 頁沒有寫自己是機器翻譯（看用詞像簡中轉繁），而且頁上的選單是「自定義 > 技能」，不是「自訂」；「自訂」是台灣介面的猜測。這句已經是「我」的不確定句，所以沒改；建議協調者決定要不要改成「說明頁寫的是『自定義』，台灣介面的字我沒看過」。
  - stakes 3a7t「只在回覆最後提一句」：CSc、W1b 是在後段提，CVa、CVb、W1a 是放在「需要你確認／要你看一下」那一段，後面還有飲食統計或其他事項，不一定是最後一句。意思（沒停下來、提一句、照猜法做完）成立。
  - xyia「不管問什麼，都多帶四百六十二個」：只量了問時間那一種要求（L 組）；C 組 CM 的 first= 比 CN1 多 460 上下，方向一致，與 cc 頁 CLAUDE.md 每次載入相符，沒改。
  - 支援頁說網頁版技能會同步到 Claude Code，overview 卻寫「Custom Skills do not sync across surfaces」；卡片只講支援頁那一個方向，與 overview 的「Claude Code Skills … separate from claude.ai」不衝突，沒改。
  - W2 只跑 2 次，兩次都用 Bash cat 讀（不是 Read）；卡片已標「之後加跑的兩次」。
  - 片長估 15.8 分鐘，超過 target_minutes [9, 12]（不是事實問題）。
- 需要第二輪：是（本輪 4 個事實修改，超過 3 個）。
