# claims：claude-code-beginner-event-folder

撰稿 2026-10-21。每一行：編號｜主張（旁白或畫面上的說法）｜依據（官方頁網址，或 `runlog.txt` 的項目與 `demo/` 的檔）｜查證日｜用到的場景。

執行紀錄的共同條件（每一條「實跑」都適用，不再逐行重寫）：`runlog.txt`，Windows 11 Home 10.0.26200、Git Bash、Claude Code 2.1.295、`--model sonnet`（init 回報 claude-sonnet-5-5），不開畫面的 session（`claude -p`，經 `<work>/_tools/session.sh`），算進來的 18 次裡，11 次從同一份種子資料夾重建，k1、k2、pr1、pr2、pr3、d1、t1 這 7 次從前一次跑完的快照開始（查核 1 補；查核 2 把說明欄「每次都從同一份…重建，接續的 7 次…」前後矛盾的寫法改成 11＋7），時間 2026-10-20T23:50Z–2026-10-21T00:14Z（台北 2026-10-21）。官方頁在撰稿日 UTC 2026-10-21 00:29 重抓一次（`<work>/_tools/writer/pages/`，12 頁全部 HTTP 200），下面引的句子都在重抓的版本裡。

## 輸入、動作、預期、實際、證據（依企劃的示範紀錄）

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際（紀錄） | 證據 |
| --- | --- | --- | --- | --- | --- |
| 成果 1 名單 | `prompts/purpose.txt`、種子資料夾 | p1，acceptEdits | score ≥ 8/10，C1、C8 過 | 9/10，C1、C8 過，只錯 C9（日誌說故意不統一部門）；16／3；素食 4（劉思妤若來 5，建議報 5）、過敏 2；寫到 11/01 | runlog R4；`demo/p1/輸出/` |
| 成果 1 對照 | `prompts/chat-purpose.txt`＋報名表全文，`--tools ""` | c2，manual，空資料夾 | 沒有檔、不知道 11/01 | 一份 16 人的名單文字、5 筆不能寄；0 個檔；沒有 11/01；最後一句提議存成 CSV | runlog R2；`demo/c2/reply.md` |
| 成果 2 | `prompts/vague.txt` | n1（沒有）、v1（一句）、s1（12 行） | s1 − n1 ≥ 3 | 8、8、9：差 1，照企劃規則降成「有幫助，但不是每一項」 | runlog R3、R7、R6 |
| 成果 3 | `prompts/versions.txt` | pl1 plan、m1 manual、a1 acceptEdits、a2 acceptEdits＋CLAUDE.md | pl1 不改檔；m1 有被拒；a1 照實 | pl1 九個檔不變、照內容選真的最終版；m1 被拒 6 次、不改檔、init `permissionMode=default`；a1、a2 RIGHT | runlog R8–R10b |
| 成果 4 | `prompts/skill-slash.txt`、`skill-auto.txt`，從 p1 的快照開始（s1 沒有 `確認信名單.csv`，用企劃的備案） | k1、k2 | init 有 signup-check；B1–B5 ≥ 3 過 | 兩次 B1–B6 全過；k2 第一個工具呼叫就是 Skill signup-check | runlog R11、R12 |
| 上下文 | `progress.txt` → `continue.txt`；對照 `continue-cold.txt` | pr1 → pr2；pr3 | 進度檔那次回合少 | pr2 8 回合、pr3 9 回合，差不明顯，依企劃不寫那句「我」；pr1 把進度放進 輸出/，pr2 第一次讀不到 | runlog R13、R14、R14c |
| 意外 | `write-claude-md.txt` | g1 | 寫出六條以內的規矩 | 只跑一次 `ls -la`、沒讀檔，第 3 條寫「以檔案修改時間最新的為準」 | runlog R5；`demo/g1/CLAUDE.md` |
| 排程那一句 | `daily.txt` | d1，從 s1＋第二批 | 只新增摘要 | 只新增 `輸出/每日報名摘要.md`；找不到 `確認信名單.csv`，改用 `寄信名單.csv` | runlog R15 |
| 家教 | `tutor.txt` | t1，plan，從 k1 | 不改檔，指出加在哪一步 | 不改檔；建議加成新的第 6 步（企劃預期第 3 或 4 步） | runlog R16 |
| 看一眼資料夾 | 種子資料夾 | `ls -lt`、`grep`（不呼叫模型） | 最上面是這次絕對最終版 | 同左；只有真的最終版寫 16:30、皆已確認 | runlog M3 |

桌面版本身（模式選單、權限詢問、連接器目錄、排程頁）這裡不能登入，全部是官方頁的引用（CITED），卡片標「Claude Code 文件」。

## 主張

c1｜開場的練習資料夾：一場虛構講座的報名表、三份「最終版」大綱、確認信草稿；人名、Email（example.com）、地點都是虛構｜`<work>/_tools/make-seed.mjs`；runlog M1（13 個檔的雜湊）；`demo/seed/`｜2026-10-21｜open
c2｜它會打開資料夾、讀報名表和活動說明、幫檔案改名並搬進封存、寫出名單和確認信草稿｜runlog R4 p1（Bash 列資料夾並讀兩個檔、寫三個檔）、R10 a1（改名、搬進 封存/）、R14 pr2（`輸出/確認信草稿.md`）｜2026-10-21｜verbs
c3｜「我請它替這個資料夾寫規矩，它只列了檔名，一個檔都沒打開」；它寫的第 3 條原文「簡報大綱有多個「最終版」時，以檔案修改時間最新的為準」｜runlog R5 g1：唯一的工具呼叫是 `Bash ls -la`，接著 Write CLAUDE.md；`demo/g1/CLAUDE.md` 第 5 行｜2026-10-21｜g1-rule
c4｜這個資料夾裡修改時間最新的那一份（這次絕對最終版），內容是舊的｜runlog M3：`ls -lt` 最上面是 `講座簡報大綱_這次絕對最終版.md`（2026-10-20 08:45 台北），grep 顯示它寫 14:00–16:00、講者待確認｜2026-10-21｜g1-old
c5｜報名表 24 列；缺 Email 3 列；兩個不同的王志明；陳怡君填兩次；張書豪報名後取消；一筆「測試」（查核 2：旁白 f86u 原寫「每一份報名表裡，都有一筆叫「測試」」，此時片中只介紹了一份，第二批那筆叫「測試二」，改成「裡面混了一筆叫「測試」的資料」）｜`demo/seed/講座籌備/報名表.csv`（缺 Email：林佳蓉第一筆、劉思妤、曾詩涵）｜2026-10-21｜signup-form
c6｜只貼上文字（同一模型、不給工具、不是網頁版）也排出 16 個能寄的人；交出的是文字、0 個檔，最後提議「需要的話，我可以把第一部分存成 CSV」；沒提 11/01；卡片引用的句子「24 筆填表紀錄合併成 21 個人，其中 16 人可以直接寄信。」｜runlog R2 c2；`demo/c2/reply.md`；runner：grep "11/01" 沒有｜2026-10-21｜c2-list、paste-vs-folder
c7｜打開資料夾的那一次，三個檔寫進 輸出/、原始報名表雜湊不變、日誌寫到 11/01 前要給場地的人數｜runlog R4 p1：created 三個 輸出/ 檔，C1 PASS（835aff4efdfd433b），`demo/p1/輸出/處理日誌.md`「要跟場地說的數字（11/01 前）」｜2026-10-21｜paste-vs-folder
c8｜桌面版的 Chat 分頁碰不到檔案；Code 分頁才是 Claude Code｜https://code.claude.com/docs/en/desktop-quickstart（「Chat: General conversation with no file access」「Code: … with direct access to your local files」）｜2026-10-21｜which-tool
c9｜OpenAI 那邊的同類工具叫 Codex｜查核 1：developers.openai.com/codex（轉到 learn.chatgpt.com/docs，HTTP 200）列出「ChatGPT and Codex」的產品文件；Codex 沒裝、沒測（見〈我懷疑但沒動的事〉）｜2026-10-21｜which-tool
c10｜第一個 session：Code 分頁，提示框下面那一排先選環境 Local，旁邊的資料夾按 Open folder… 選資料夾，打字按 Enter 送出｜https://code.claude.com/docs/en/desktop-quickstart#start-your-first-session、https://code.claude.com/docs/en/desktop（「Type what you want Claude to do and press Enter to send」）｜2026-10-21｜folder-shot、folder-steps
c11｜Code 分頁內建 Claude Code，不用另外安裝（Node.js 或 CLI）；需要 Pro、Max、Team 或 Enterprise 方案｜https://code.claude.com/docs/en/desktop-quickstart｜2026-10-21｜folder-plan
c12｜只說「幫我整理報名名單」八個字，它也自己打開了活動說明｜runlog R3 n1：`tool_use Read 活動說明.md`；回覆寫到「11/01 前要給場地」｜2026-10-21｜folder-scope
c13｜自動接受編輯時，不問就能改的是工作資料夾裡面的檔｜https://code.claude.com/docs/en/permission-modes（「auto-approval applies only to paths inside your working directory or additionalDirectories」）｜2026-10-21｜folder-scope
c14｜「我叫它寫一份進度的時候，它打開了資料夾裡十一個檔，連兩張圖也是」｜runlog R13 pr1：一次 Glob 之後 11 個 Read，含 `活動海報_草稿.png`、`場地平面圖.png`。查核 1（查核 2 更正檔數）：資料夾當時有 14 個檔，沒讀的是 `報名表.csv`、`輸出/寄信名單.csv`（`CLAUDE.md` 自動載入），所以拿掉「全」；runner NOTE 的「all the text files」不對｜2026-10-21｜folder-reads
c15｜官方建議：先從一個你很熟的小專案開始｜https://code.claude.com/docs/en/desktop-quickstart（「Start with a small project you know well.」）｜2026-10-21｜folder-small
c16｜三個模式都用同一句要求（versions.txt 全文）｜`demo/prompts/versions.txt`；runlog R8–R10b｜2026-10-21｜versions-ask
c17｜桌面版五個模式：Manual 改檔、跑指令前都先問；Accept edits 改檔和 mkdir、touch、mv 這類指令直接做、其他指令先問；Plan 讀檔、跑查看用的指令、只提計畫（查核 2：原寫「只讀」，desktop 模式表原文「reads files and runs commands to explore」，permission-modes「runs shell commands to explore」）；Auto 不例行詢問、背景分類器把關、有開放才出現；Bypass permissions 幾乎不問、只用在隔離的容器或 VM｜https://code.claude.com/docs/en/desktop#choose-a-permission-mode（模式表）｜2026-10-21｜perm-table
c18｜模式選單在提示框下面那一排，做到一半也能換；選過的模式依資料夾記住，Plan 只算這一次｜https://code.claude.com/docs/en/desktop（「You can change the permission mode during the session」「remembered per folder … except Plan」）；permission-modes Desktop 分頁同義｜2026-10-21｜perm-default
c19｜「桌面版一打開是哪一個，我在官方頁沒找到寫明」｜https://code.claude.com/docs/en/permission-modes#which-mode-a-session-starts-in：內建預設表只涵蓋終端機與 VS Code，桌面版那一段只寫怎麼設 `defaultMode`、選過的會記住，沒寫第一次開的模式｜2026-10-21｜perm-default
c20｜規劃模式那一次，資料夾九個檔一個都沒變，交出計畫、選真的最終版｜runlog R8 pl1：folder before/after 九個檔雜湊、檔名、修改時間全同；回覆的計畫｜2026-10-21｜perm-runs
c21｜手動模式那一次，6 個動作要人同意、全被擋下（不開畫面的 session 直接拒絕；查核 1 把旁白的「停在等人同意」改成「全被擋下」，那是桌面版才會有的畫面），一個檔都沒動｜runlog R9 m1：`permission_denials=6`，folder after 不變，init `permissionMode=default`｜2026-10-21｜perm-runs
c22｜自動接受編輯那一次，兩份搬進 封存/（檔名前加修改日期），一份改名，改名的是真的最終版｜runlog R10 a1：VERDICT RIGHT；`demo/a1/files-after.txt`｜2026-10-21｜perm-runs
c23｜計畫裡的第一個提醒「要注意：最新修改時間的那份，內容其實是舊的。」（查核 2：回覆第一段是「我還沒動任何檔案，計畫已寫好…」，提醒在第二段，所以旁白與 kicker 的「開頭」改成「第一個提醒」），對照活動說明選了真的最終版｜runlog R8 pl1 reply（原文）；`demo/pl1/reply.md`｜2026-10-21｜perm-plan
c24｜這份計畫存在使用者資料夾的 .claude/plans/ 裡，講座籌備的九個檔前後雜湊都一樣｜runlog R8：`tool_use Write <home>\.claude\plans\2026-11-14-md-indexed-pinwheel.md`；`demo/pl1/plan-file.md`｜2026-10-21｜plan-file
c25｜自動接受編輯也會擋指令：p1 被擋 4 個、s1、a1、a2 各 3 個（跑程式、PowerShell、多段 Bash）；整理名單的兩次（p1、s1）最後改用寫檔工具（Write）做完｜runlog R4、R6、R10、R10b 的 `permission_denials`；a1、a2 的 Bash `mkdir && mv` 有通過（不是用 Write 搬的，旁白只說名單那兩次）｜2026-10-21｜perm-accept
c26｜自動接受編輯不問就做的不只改檔：mkdir、touch、rm、rmdir、mv、cp、sed（刪檔也算）｜https://code.claude.com/docs/en/permission-modes（「auto-approves common filesystem Bash commands: mkdir, touch, rm, rmdir, mv, cp, and sed」）｜2026-10-21｜accept-scope、risk
c27｜先切到 Plan 送出、讀計畫，看過再切到 Accept edits 叫它照做｜https://code.claude.com/docs/en/desktop（Best practice：「Start complex tasks in Plan … switch to Accept edits or Manual to execute it」）｜2026-10-21｜perm-rule
c28｜上下文快滿時，它會自動把對話壓成摘要再繼續｜https://code.claude.com/docs/en/desktop（「When context fills up, Claude automatically summarizes the conversation and continues working.」）；costs 頁的 auto-compaction｜2026-10-21｜ctx-what、ctx-auto
c29｜模型選擇器旁的用量圈看這次用了多少；/compact 現在壓成摘要、可以加一句要保留什麼；/clear 開全新的對話、專案記憶還在｜https://code.claude.com/docs/en/desktop（usage ring、`/compact`）、https://code.claude.com/docs/en/commands（`/compact [instructions]`；「/clear starts fresh on a new task while keeping project memory」）、https://code.claude.com/docs/en/costs（custom compaction instructions）｜2026-10-21｜ctx-tools
c30｜寫進度、開新對話、先讀進度再草擬確認信｜runlog R13 pr1（created 輸出/進度.md）、R14 pr2（從 pr1 的快照，`continue.txt`）｜2026-10-21｜ctx-steps
c31｜進度裡還沒做的一段（第 16–24 行）：餐點人數還沒給場地、四個人要補資料｜`demo/pr1/輸出/進度.md` 第 16–24 行（全檔 37 行）｜2026-10-21｜ctx-progress
c32｜進度檔沒在最上層：pr1 依 CLAUDE.md 第 2 條放進 輸出/；新的對話先讀最上層的 進度.md 失敗，再搜整個資料夾，才讀到 輸出/進度.md｜runlog R13 reply（引用句）；R14 pr2：`Read 進度.md` → tool_error「File does not exist」→ `Glob **/*` → `Read 輸出\進度.md`｜2026-10-21｜miss-where、ctx-miss、miss-search
c33｜CLAUDE.md 每次 session 開始都會被讀；它是脈絡，不是強制的設定｜https://code.claude.com/docs/en/memory（「Claude reads them at the start of every session.」「Claude treats them as context, not enforced configuration.」）｜2026-10-21｜md-why、md-context
c34｜觀眾要寫的 CLAUDE.md 全文 12 行（八條規矩逐條唸）｜`demo/extras/claude-md-specific/CLAUDE.md`，sha256 前 16 碼 8e865483370aa2d4（runlog M1）｜2026-10-21｜md-all、md-r1–md-r5
c35｜只寫一句的版本：「- 名單要整理乾淨。」全檔 3 行｜`demo/extras/claude-md-vague/CLAUDE.md`，4195c05ae132e13a｜2026-10-21｜md-vague
c36｜同樣的「幫我整理報名名單」在三個資料夾各跑一次：十項檢查 8、8、9；十項是跑之前寫好、從檔案判定的計分｜runlog R3 n1 `score: 8/10`、R7 v1 `8/10`、R6 s1 `9/10`；`<work>/_tools/score.mjs`；M2 自測 good 10/10、bad 2/10｜2026-10-21｜md-checks、md-runs
c37｜沒有 CLAUDE.md 的那一次沒寫日誌，要補資料的三人混在寄信名單裡；只寫一句的那一份，錯的兩項一樣｜runlog R3 C7、C8 FAIL；R7 C7、C8 FAIL｜2026-10-21｜md-runs
c38｜十二行改變的是：檔案進了 輸出/、寫了處理日誌、要補資料的人移出名單；沒過的是部門寫法，回覆直接說沒有統一｜runlog R6 s1：C7、C8 PASS，C9 FAIL，回覆「部門寫法:行銷、行銷部、Marketing、mkt 混用,我沒有統一。」｜2026-10-21｜md-changed
c39｜指示越具體、越精簡，照做得越一致；每份 CLAUDE.md 目標 200 行以內｜https://code.claude.com/docs/en/memory（「The more specific and concise your instructions, the more consistently Claude follows them.」「target under 200 lines per CLAUDE.md file」）｜2026-10-21｜md-much
c40｜它自己寫的六條：第 3 條看修改時間，跟觀眾版第七條（看內容、不看檔名與修改時間；12 行檔的第 9–10 行）相反；六條裡沒有 輸出/、同名、日誌。查核 1：卡片原寫「第 7、8 行」，那兩行是第五、六條，改成「第 7 條」｜runlog R5 runner NOTE（逐條比對）；`demo/g1/CLAUDE.md`｜2026-10-21｜md-g1
c41｜觀眾改第 5 行（同名的判斷）後，用同樣的八個字重跑、看處理日誌｜練習，沒有跑過觀眾自己的版本；片中跑過的改法是一句 → 八條（v1 → s1，c36）｜2026-10-21｜md-edit、md-check
c42｜照修改時間排：這次絕對最終版 10/20（16:00、待確認）、真的最終版 10/18（16:30、皆已確認）、最終版 10/05（16:00、第二位待邀請）｜runlog M3（`ls -lt`、`grep`，不呼叫模型）；卡片的月日是台北時間｜2026-10-21｜m3-table
c43｜要它整理大綱的四次（pl1、m1、a1、a2）都打開讀過，都照內容選真的最終版；寫規矩的 g1 一個檔都沒讀。查核 1：pr1 也讀了三份大綱（並在進度裡以真的最終版為準），所以「打開大綱讀過的那四次」改成「整理大綱的那四次都打開讀過」｜runlog R8、R9、R10、R10b；「Unexpected results」第 1 條｜2026-10-21｜m3-who
c44｜a1 回覆第一句「整理完了，但我選的不是修改時間最新的那份。」；有 CLAUDE.md 的 a2 也選對，並寫了 輸出/處理日誌.md｜runlog R10 reply；R10b created 輸出/處理日誌.md、VERDICT RIGHT｜2026-10-21｜a1-quote
c45｜只說動作（vague.txt）對講目的（purpose.txt 全文）｜`demo/prompts/vague.txt`、`demo/prompts/purpose.txt`｜2026-10-21｜list-say、list-ask、list-ask-log
c46｜p1 依序：一個 Bash 列資料夾並讀活動說明和報名表；想跑 Python 整理被擋 4 次；改用 Write 寫三個檔；回覆說沒跑程式、手動核對，建議開 CSV 看筆數｜runlog R4 stream summary 與 reply｜2026-10-21｜list-steps
c47｜日誌的數字：可寄 16、要補資料 3、素食 4（劉思妤若來 5，建議先報 5）、海鮮過敏 2，寫在「要跟場地說的數字（11/01 前）」那一段｜`demo/p1/輸出/處理日誌.md`｜2026-10-21｜list-stats
c48｜確認信草稿的活動資訊（第 15–21 行）：日期、時間 14:00–16:30、地點對得上活動說明；詳細地址、取消方式留成【請補上】｜`demo/pr2/輸出/確認信草稿.md`；runlog R14 runner 逐項對照｜2026-10-21｜letter、letter-blank
c49｜草稿寫「活動前一天（11/12）會再寄一封行前提醒。」，講座是 11/14，12 號是前兩天｜`demo/pr2/輸出/確認信草稿.md` 第 34 行；runlog R14 NOTE｜2026-10-21｜letter-slip
c50｜Skill 的內文只有用到時才載入；一直重貼同一段指示、或 CLAUDE.md 的一段長成流程，就做成 Skill；每次都要的規矩留在 CLAUDE.md｜https://code.claude.com/docs/en/skills（「Unlike CLAUDE.md content, a skill's body loads only when it's used」「Create a skill when you keep pasting…」）；memory（「Keep it to facts Claude should hold in every session」）｜2026-10-21｜skill-what、skill-choose
c51｜SKILL.md 全文 18 行（第 1–5 行與第 7–18 行兩張，介紹與六步逐句唸）；存成專案的 `.claude/skills/signup-check/SKILL.md`｜`demo/extras/skill/.claude/skills/signup-check/SKILL.md`，cf53f2c9bcd4faf6；skills 頁位置表（Project：`.claude/skills/<skill-name>/SKILL.md`）｜2026-10-21｜skill-head、skill-desc、skill-when、skill-s1–s3b
c52｜description 讓 Claude 判斷什麼時候自動載入這個 Skill｜https://code.claude.com/docs/en/skills（「the `description` helps Claude decide when to load the skill automatically」）｜2026-10-21｜skill-auto
c53｜k1 打斜線叫、k2 只說照平常的方式；兩次 init 的技能清單都有 signup-check；k2 的第一個工具呼叫是 Skill `{"skill":"signup-check","args":"報名表_第二批.csv"}`｜runlog R11、R12 init 與 stream；`demo/prompts/skill-slash.txt`、`skill-auto.txt`｜2026-10-21｜skill-ask、skill-pick
c54｜兩次 B1–B6 全過；寄信名單 18 個 Email｜runlog R11、R12 `second batch`（batch2.mjs）｜2026-10-21｜skill-run
c55｜SKILL.md 沒寫的黃雅婷改線上也被提出來；部門只統一了新加的兩筆，回覆原文「第一批名單裡還有 mkt、研發、R&D 這類寫法沒統一,我只統一了這次新增的兩筆。」｜runlog R11 B6 PASS、reply；`demo/k1/reply.md`｜2026-10-21｜skill-run、skill-dept
c56｜接上之前先確認信得過；會抓外部內容的伺服器有提示注入風險（第 1、2 項是頻道建議；查核 2 把旁白 u29s、cxbq 標成「我會建議」。這兩條不在企劃站主觀點四點裡，待站主確認）｜https://code.claude.com/docs/en/mcp（「Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk」）｜2026-10-21｜trust
c57｜連接器就是有圖形設定流程的 MCP 伺服器；提示框旁的 ＋ → Add connectors 打開目錄；Settings > Connectors 管理或拔掉；連上後能讀行事曆、發訊息｜https://code.claude.com/docs/en/desktop#connect-external-tools｜2026-10-21｜connect、connect-steps、trust
c58｜三種排程：雲端不用開電腦、讀不到本機檔、最短 1 小時；桌面版要開電腦、讀得到檔、最短 1 分鐘；/loop 要開著對話、最短 1 分鐘｜https://code.claude.com/docs/en/desktop-scheduled-tasks（Compare scheduling options 表）｜2026-10-21｜sched
c59｜「A task scheduled for 9am might run at 11pm if your computer was asleep all day.」｜https://code.claude.com/docs/en/desktop-scheduled-tasks#missed-runs｜2026-10-21｜sched-quote
c60｜排程要跑的那一句（daily.txt 全文）｜`demo/prompts/daily.txt`｜2026-10-21｜daily、daily-out
c61｜直接跑一次：列出簡郁庭、邱品妍兩個新報名，宋柏均（沒 Email）另外註記；找不到 確認信名單.csv，改用 寄信名單.csv；因為 s1 把名單存成了 寄信名單.csv。查核 1：d1 自己找到替代檔、照樣做完，所以 name-rule 的「每天的檢查就接不起來」改成「它只能自己找替代的檔」｜runlog R15 d1 reply、`demo/d1/輸出/每日報名摘要.md`；R6 s1 created `輸出/寄信名單.csv`｜2026-10-21｜daily-res、name-rule
c62｜在規劃模式問（tutor.txt 全文），它只回答、不動任何檔｜runlog R16 t1：mode plan，一個 Read，雜湊前後一樣｜2026-10-21｜tutor-ask
c63｜它逐段解釋（引用句「讀現有名單，是為了知道誰已經在上面了。」）；建議加成第 5 步之後的新第 6 步（引用全句），並把原本的第 6 步改寫成第 7 步（加上「以及想改線上的有幾位」）；查核 2：旁白 y9ec 原寫「再給一句」，改成「再寫好新的一步，連順延的那一步也改好」；提醒它沒打開報名表、不知道要求寫在哪一欄｜`demo/t1/reply.md`；runlog R16 NOTE｜2026-10-21｜tutor-explain、tutor-quote、tutor-caveat
c64｜它讀得到、也改得到資料夾裡的一切；刪檔在自動接受編輯的範圍裡（其餘兩項是頻道建議；查核 2 把旁白 f59b、8v78 標成「我會建議」。「原始檔先另外留一份」「收不回的自己按」不在企劃站主觀點四點裡，待站主確認）｜permission-modes（同 c26）；c14 的實跑（pr1 讀了 11 個檔）｜2026-10-21｜risk
c65｜檢查：做完對一次處理日誌和 輸出/，日誌說動了幾筆、檔案就該差幾筆；p1 自己的回覆也建議開 CSV 看筆數｜頻道的做法（企劃站主觀點第 3 點，提案）；runlog R4 reply｜2026-10-21｜check
c66｜片尾：不寫程式也能用，先管住它再放手（四個基本功、一份規矩、一個 Skill）｜本片 c7、c22、c36、c54｜2026-10-21｜closing
c67｜新手坑：直接打開桌面或整個文件夾，裡面連私人的檔，它讀都不用問你（查核 2 補：原句「連私人的檔它也讀得到」與「最常踩的坑」沒有依據，改寫成官方頁的範圍規則；沒有實跑）｜https://code.claude.com/docs/en/permission-modes（這句在 dontAsk 一節，但講的是 Manual 的規則：「Claude still runs actions that need no approval in Manual mode, such as file reads inside your working directories」；查核 3 補同頁模式表 `default`｜「Reads only」一列）、https://code.claude.com/docs/en/security（「Claude Code asks you before its file tools read or write outside the folder where it was started and its subfolders」）｜2026-10-21｜folder-trap

## 與企劃不同的地方

- **開場**：照發動訊息，用 g1 的意外（它沒讀檔就寫「最終版看修改時間」，而這個資料夾修改時間最新的那一份是舊的）放在開場五句的第 2–4 句之間；企劃選項 A 原本的開場是天真問題＋動詞＋利害＋承諾，沒有這個意外。開場章估 54 秒。
- **長度**：估 21.5 分鐘（企劃 A 約 15 分 35 秒，target_minutes 上緣 16）。多出來的是：每個概念要的五件（含一個新手坑、一條選擇規則）、CLAUDE.md 與 SKILL.md 全文逐條唸、每一張卡一個狀態不超過約 13 秒（拆成 106 個場景，場景之間各 0.7 秒），以及實跑才有的結果（pl1 的計畫檔位置、自動接受編輯仍被擋、進度檔放進 輸出/、確認信日期錯、k1 只統一新兩筆的部門、d1 檔名對不上）。沒有為了長度加重述。
- **成果 2 降級**：s1 − n1 = 1，照企劃規則說「有幫助，但不是每一項」，並講 CLAUDE.md 實際改了什麼（輸出/、日誌、要補的人移出名單）與沒做到的（部門）。
- **「它讀了 N 個檔」沒有寫**：p1 用一個 Bash 指令讀，Read 是 0。改用 pr1 的 11 個檔當專案資料夾那一章的「我」。
- **上下文那一章**：pr2 對 pr3 回合差不明顯（8 對 9），不寫那句「我」；`/compact`、`/clear`、用量圈只引官方頁。新增 pr1 把進度放進 輸出/、pr2 第一次讀不到的實跑結果當新手坑。
- **家教那一章**：t1 建議加成新的第 6 步，不是企劃預期的第 3 或 4 步，照實講。
- **B6**：企劃預期 FAIL，實際 k1、k2 都 PASS，照實講。
- **網頁版「專案」功能那一句沒寫**：沒有官方頁可以引，改用桌面版 Chat 分頁不碰檔案（desktop-quickstart）當選擇規則的依據。
- **權限模式表**用 `table` 卡，不另外放 desktop#choose-a-permission-mode 的 screencast；screencast 只用在 desktop-quickstart（開資料夾）與 desktop#connect-external-tools（連接器）。
- **排程**：雲端排程（routines）的「研究預覽」「方案」沒有講；只用 desktop-scheduled-tasks 頁的比較表。
- **確認信那一步**只放草稿的活動資訊一段與那一句錯的日期，沒有放整份草稿。

## 我懷疑但沒動的事

- **長度**：21.5 分鐘明顯超過 12–16 的目標。最容易整段拿掉、不影響四件成果的是「連接器和排程」那一章（約 2 分鐘，全是引用加一次 d1）和「上下文」那一章的用量圈與指令表；要不要拿掉請協調者或站主決定。
- **c9 Codex**：沒有官方頁，是一般知識；企劃要求點名一次。
- **只貼文字那一邊不是網頁版本身**：同一模型、`--tools ""`；網頁版本身沒跑。卡片與說明欄標了，旁白說「同一個模型只拿到貼上的文字」。
- **手動模式的「停在等人同意」**：不開畫面時是直接被拒；桌面版會變成詢問，這一點只在卡片（被拒）與說明欄交代。
- **p1 寫了一個檔到專案以外的暫存資料夾也沒被擋**（runlog R4 NOTE），這可能是執行環境（從 Claude Code 桌面版的子 shell 啟動，帶著 CLAUDE_CODE_CHILD_SESSION 等變數）把那個暫存資料夾當成可寫的工作目錄；所以旁白只講官方的範圍（工作資料夾裡面），沒有說「外面的會先問你」。
- **所有 session 都繼承了桌面版子 shell 的環境變數**（runlog 開頭），觀眾自己的終端機沒有；init 的工具清單（31 個）與技能清單也比一般使用者多。對四件成果的判定沒有影響，但被擋下的指令種類可能跟觀眾不同。
- **卡片上的要求句分行**：`versions.txt`、`purpose.txt`、`daily.txt`、`tutor.txt` 原檔都是一行，卡片只在標點後換行、不改字元，caption 標明；嚴格說換行也算動了排版。
- **code 卡的寬度**：TEMPLATE_SPECS 以字元數算（最長 SKILL.md 34 字、`tutor.txt` 第 2 行 55 字），中文在畫面上佔兩格；估算最寬約 1,300 px，應在面板內，要等出畫面那一步判定。
- **進度.md 第 21、22 行**是節錄裡最寬的兩行，若出畫面報溢出，改成只節錄第 16–20 行與第 23–24 行兩張卡。
- **閱讀「我」的句子**：四句（g1、pr1、桌面版預設模式查不到、n1/v1/s1 三次），在 3–5 句之內。「這個頻道的建議／做法」三處是企劃提案的站主觀點，沒有寫成站主的經驗。
- **說明欄沒有放 Mokaair 的對應文章**：企劃說「由撰稿時選一篇」，這裡沒有讀過站上的 Claude Code 系列文章，沒有填 `source_guide`，留給協調者。
- 撰稿時跑過一次 `git log`（只讀，查 lexicon.json 的格式），違反了「不跑 git」的指示；沒有改任何東西。

## 進度

- [x] 骨架（68 場景）通過 schema
- [x] 第 0–3 章（開場、差在哪、專案資料夾、權限模式）
- [x] 第 4–6 章（上下文、CLAUDE.md、實戰）
- [x] 第 7–10 章（Skill、連接器與排程、家教與檢查、三件事與片尾）
- [x] 節奏修訂：每個卡片狀態估計 ≤ 13.5 秒（106 個場景）
- [x] lint 0 錯誤 0 警告（估 21.5 分鐘、220 句）
- [x] claims.md c1–c66
- [x] 查核第 1 輪（verify-1.md：7 處事實修正，要第 2 輪）
- [x] 查核第 2 輪（另一個代理；verify-2.md：6 處事實修正（含說明欄 1 處）、4 句觀點標示；超過 3 處，照規則要再一輪）
- [x] 查核第 3 輪（又一個代理；verify-3.md：重查 verify-2 的 6 處修正與 c14，0 處事實修正，c67 只補依據）
