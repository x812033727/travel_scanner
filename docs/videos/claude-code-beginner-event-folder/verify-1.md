# verify-1：claude-code-beginner-event-folder

查核日 2026-10-21，第 1 輪，查核者不是撰稿者。沒有跑 git。

方法：先把 `video.json` 每一句 `text`（沒有一句有 `say`）、每張卡的 `data`、縮圖、`youtube.title`、`description`、`tags` 抽成清單（`<work>/_tools/verifier/dump.txt`）。實跑的主張逐字對 `runlog.txt` 與 `demo/`；code 卡與引用句用腳本（`<work>/_tools/verifier/cards.js`）和 `demo/` 的原檔逐字元比對。功能的主張今天重抓官方頁（UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，每頁間隔 1.2 秒，HTML 與 `.md` 兩種都抓，全部 HTTP 200，去掉 `<!-- -->` 後讀），存在 `<work>/_tools/verifier/pages/`。沒有用 web search（0／5）。

官方頁（2026-10-21，全部 HTTP 200，無重新導向；頁面本身沒有更新日期）：

| 代號 | URL |
| --- | --- |
| DQ | https://code.claude.com/docs/en/desktop-quickstart |
| D | https://code.claude.com/docs/en/desktop |
| PM | https://code.claude.com/docs/en/permission-modes |
| ME | https://code.claude.com/docs/en/memory |
| CM | https://code.claude.com/docs/en/commands |
| CO | https://code.claude.com/docs/en/costs |
| SK | https://code.claude.com/docs/en/skills |
| MCP | https://code.claude.com/docs/en/mcp |
| ST | https://code.claude.com/docs/en/desktop-scheduled-tasks |
| OAI | https://developers.openai.com/codex（重新導向到 https://learn.chatgpt.com/docs，200） |

實跑的依據寫成 `RL Rn`（`runlog.txt` 的項目）與 `demo/…`，HTTP 欄寫「—」。

## 主張表

| # | 主張 | 位置 | 依據 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 練習資料夾虛構、Email 都是 example.com | open、signup-form.source、description | demo/seed/講座籌備/報名表.csv、活動說明.md 第 16 行；RL M1 13 個雜湊 | — | CONFIRMED | |
| 2 | 它會打開資料夾、讀報名表和活動說明、改名搬進封存、寫名單和確認信草稿 | verbs | RL R4 p1、R10 a1、R14 pr2 | — | CONFIRMED | |
| 3 | g1 只列了檔名、一個檔都沒打開；第 3 條原文 | g1-rule、dqu9、646h | RL R5（唯一工具呼叫 `ls -la`，接著 Write）；demo/g1/CLAUDE.md 第 5 行逐字比對 FOUND | — | CONFIRMED | |
| 4 | 修改時間最新的那一份內容是舊的 | g1-old、dr6i | RL M3 `ls -lt` 與 grep | — | CONFIRMED | |
| 5 | 五個基本功的承諾 | promise | 結構，無事實 | — | OUT OF SCOPE | |
| 6 | 報名表 24 列；缺 Email 3 列；兩個王志明 Email 不同；陳怡君兩次；張書豪取消；一筆「測試」 | signup-form、cza5、gf7y、f86u | demo/seed/講座籌備/報名表.csv（24 筆資料列；第 4、10、20 列沒有 Email） | — | CONFIRMED | （「每一份報名表裡都有一筆叫測試」見下方懷疑） |
| 7 | c2 引用句「24 筆填表紀錄合併成 21 個人，其中 16 人可以直接寄信。」 | c2-list | demo/c2/reply.md 逐字 FOUND；RL R2 | — | CONFIRMED | |
| 8 | 只拿到文字也排出 16 個能寄的人 | byk3 | RL R2（16 人表） | — | CONFIRMED | |
| 9 | c2 交出 0 個檔、沒提 11/01、沒看到活動說明 | paste-vs-folder 左欄、p95r、t4kn | RL R2 NOTE（grep 11/01 沒有；空資料夾、`--tools ""`） | — | CONFIRMED | |
| 10 | p1 三個檔寫進 輸出/、原始報名表雜湊不變、日誌寫了 11/01 前要給場地的數 | paste-vs-folder 右欄、k8cy、7gct | RL R4 created 三檔、C1 PASS 835aff4efdfd433b；demo/p1/輸出/處理日誌.md 第 26 行 | — | CONFIRMED | |
| 11 | Chat 分頁不碰檔案；Code 分頁才有本機檔案存取 | which-tool、3sdm、356m、y9bk | DQ「Chat: General conversation with no file access, similar to claude.ai」「Code: … direct access to your local files」 | 200 | CONFIRMED | |
| 12 | OpenAI 那邊的同類工具叫 Codex | which-tool、4fh3 | OAI：OpenAI 的開發者文件標「Guides and product docs for ChatGPT and Codex」 | 200 | CONFIRMED（只證明產品存在與歸屬；功能沒查） | |
| 13 | 開資料夾的步驟：Code 分頁 → 環境選 Local → Open folder… → 打字按 Enter | folder-steps、3z8j–yfn4、folder-shot | DQ Start your first session（「select the top entry in the Local group」「Open folder…」）；D「Type what you want Claude to do and press Enter to send」；`#start-your-first-session` 錨點存在 | 200 | CONFIRMED | |
| 14 | Code 分頁內建 Claude Code、不用另外安裝；要 Pro、Max、Team 或 Enterprise | folder-plan、8a3d、xsq7 | DQ「The desktop app includes Claude Code, so you don't need to install Node.js or the CLI」「requires a Pro, Max, Team, or Enterprise subscription」 | 200 | CONFIRMED | |
| 15 | 只說八個字，它也自己打開活動說明 | folder-scope、3i6w | RL R3 n1 `tool_use Read 活動說明.md`；「幫我整理報名名單」8 字 | — | CONFIRMED | |
| 16 | 自動接受編輯不問就能改的是工作資料夾裡的檔 | folder-scope、xfnv | PM「auto-approval applies only to paths inside your working directory or `additionalDirectories`」 | 200 | CONFIRMED | |
| 17 | pr1 打開了 11 個檔，連兩張圖 | folder-reads、kgnr | RL R13：Glob 之後 11 個 Read（含兩張 PNG）；當時資料夾有 15 個檔，沒讀 報名表.csv、輸出/寄信名單.csv | — | CHANGED | 「它把資料夾裡十一個檔全打開了」→「它打開了資料夾裡十一個檔」（stats 卡本來就只寫「11 個 它打開的檔」，不動） |
| 18 | 新手坑：打開整個桌面它全讀得到 | folder-trap、snrs | 沒有實跑；能力推論，與 PM 的範圍說明一致 | — | OUT OF SCOPE（見懷疑） | |
| 19 | 先從一個你很熟的小專案開始（引用與翻譯） | folder-small、vkes | DQ Tip「Start with a small project you know well.」 | 200 | CONFIRMED | |
| 20 | versions.txt 全文 | versions-ask | demo/prompts/versions.txt，去掉卡片換行後逐字 MATCH | — | CONFIRMED | |
| 21 | 桌面版五個模式的說明 | perm-table、said–kqtt | D Choose a permission mode 模式表（Manual／Accept edits 含 mkdir、touch、mv／Plan／Auto 有開放才出現／Bypass「Only use this in sandboxed containers or VMs」） | 200 | CONFIRMED | |
| 22 | 模式選單在提示框下面那一排、做到一半能換；依資料夾記住；Plan 只算這一次 | perm-default、t9pa、gd2z | D「switch permission modes at any time using the mode selector in the row under the prompt box」「remembered per folder … except Plan」；PM Desktop 分頁同義 | 200 | CONFIRMED | |
| 23 | 桌面版一打開是哪一個，官方頁沒寫明 | perm-default、u22y | PM Which mode a session starts in：表只涵蓋終端機與 VS Code，桌面版指向 Switch permission modes 的 Desktop 分頁，那裡只寫 defaultMode 與記住的規則 | 200 | CONFIRMED | |
| 24 | pl1 九個檔一個都沒變、交出計畫、選真的最終版 | perm-runs 第 1 列、3q3u | RL R8 folder before/after 9 個雜湊與 mtime 全同；reply | — | CONFIRMED | |
| 25 | m1 6 個動作要人同意（被拒）、一個檔都沒動 | perm-runs 第 2 列、mvtb | RL R9 `permission_denials=6`、folder after 不變 | — | CHANGED（旁白） | 「有六個動作停在等人同意」→「有六個動作要人同意，全被擋下」：不開畫面的 session 是直接拒絕，「停在等」是桌面版的預期，不是這次看到的 |
| 26 | a1 兩份搬進封存、一份改名，改名的是真的最終版 | perm-runs 第 3 列、kr3n | RL R10 VERDICT RIGHT；folder after | — | CONFIRMED | |
| 27 | 計畫開頭的提醒（引用句） | perm-plan、dj2h | demo/pl1/reply.md 逐字 FOUND（第二段，粗體） | — | CONFIRMED（「開頭」見懷疑） | |
| 28 | 計畫存在使用者資料夾的 .claude/plans/；講座籌備 9 個檔雜湊不變 | plan-file、a5dm | RL R8 `tool_use Write <home>\.claude\plans\…`；folder before/after | — | CONFIRMED | |
| 29 | 被擋下：p1 4、s1 3、a1 3、a2 3；跑程式、PowerShell、多段 Bash；整理名單的兩次改用寫檔工具 | perm-accept、7gwr、yitb、dux8 | RL R4、R6、R10、R10b `permission_denials` 與 tool_error；p1、s1 之後用 Write | — | CONFIRMED | |
| 30 | 自動接受編輯不問就做：改檔、建資料夾、搬檔、複製、刪檔 | accept-scope、akxx | PM「auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`」 | 200 | CONFIRMED | |
| 31 | 先 Plan 送出、讀計畫、再切 Accept edits 照做 | perm-rule、vdg7、qvep | D Best practice「Start complex tasks in Plan … switch to Accept edits or Manual to execute it」 | 200 | CONFIRMED | |
| 32 | 上下文快滿時自動壓成摘要（引用與翻譯） | ctx-auto、ctx-what、2aer | D「When context fills up, Claude automatically summarizes the conversation and continues working.」；CO auto-compaction | 200 | CONFIRMED | |
| 33 | 模型選擇器旁的用量圈看這次用了多少 | ctx-tools 第 1 列、u4ry | D「Click the usage ring next to the model picker to see your current context window usage」 | 200 | CONFIRMED | |
| 34 | /compact 現在壓成摘要、可加一句要保留什麼 | ctx-tools 第 2 列、uu9z | CM `/compact [instructions]`「Optionally pass focus instructions」；CO custom compaction instructions；D `/compact` | 200 | CONFIRMED | |
| 35 | /clear 開全新的對話、專案記憶還在 | ctx-tools 第 3 列、62gk | CM「`/clear` starts fresh on a new task while keeping project memory」 | 200 | CONFIRMED | |
| 36 | 寫進度 → 開新對話 → 先讀進度再草擬確認信 | ctx-steps、urtk、kvzv | RL R13 pr1、R14 pr2；demo/prompts/progress.txt、continue.txt | — | CONFIRMED | |
| 37 | 進度.md 第 16–24 行（全檔 37 行）卡片全文；餐點人數還沒給場地、四個人要補資料 | ctx-progress、f34t | demo/pr1/輸出/進度.md 第 16–24 行逐字 MATCH，全檔 37 行 | — | CONFIRMED | |
| 38 | 進度.md 在 輸出/；回覆引用句；pr2 先讀最上層失敗→搜整個資料夾→讀到 | miss-where、ctx-miss、miss-search、wqdq、v239、787t | demo/pr1/reply.md 逐字 FOUND；RL R14 `Read 進度.md` → File does not exist → `Glob **/*` → `Read 輸出\進度.md` | — | CONFIRMED | |
| 39 | CLAUDE.md 每次 session 開始都讀；是脈絡不是強制設定（兩句引用） | md-why、md-context、3ghe、8gu9 | ME「Claude reads them at the start of every session.」「Claude treats them as context, not enforced configuration.」；位置 `./CLAUDE.md` | 200 | CONFIRMED | |
| 40 | 12 行 CLAUDE.md 全文與逐條唸的內容、各張的 highlight | md-all、md-r1–md-r5、md-edit、8wjx、83z3–d5e5 | demo/extras/claude-md-specific/CLAUDE.md 逐字 MATCH，12 行，sha256 前 16 碼 8e865483370aa2d4 | — | CONFIRMED | |
| 41 | 只寫一句的那一份，全檔 3 行 | md-vague、7rum | demo/extras/claude-md-vague/CLAUDE.md MATCH，3 行，4195c05ae132e13a | — | CONFIRMED | |
| 42 | 十項檢查節錄 5 項；跑之前寫好、從檔案判定 | md-checks、zhp7 | RL M2（selftest，C1–C10 名稱）、每次的 score 區塊 | — | CONFIRMED | |
| 43 | 同一句在三個資料夾：8、8、9 | md-runs、enuy、z4ta、5vd2、wu36、description | RL R3 `score: 8/10`、R7 `8/10`、R6 `9/10` | — | CONFIRMED | |
| 44 | 沒有 CLAUDE.md 那次沒寫日誌、要補資料的三人混在名單裡 | md-runs、dbwi | RL R3 C7、C8 FAIL 與 NOTE | — | CONFIRMED | |
| 45 | 十二行改變三件；沒過的是部門寫法，回覆直接說沒統一 | md-changed、dgqg、wb5r | RL R6 C7、C8 PASS，C9 FAIL；reply「部門寫法:…我沒有統一。」 | — | CONFIRMED | |
| 46 | 越具體越精簡越一致；每份目標 200 行以內 | md-much、4f33 | ME「The more specific and concise your instructions, the more consistently Claude follows them.」「target under 200 lines per CLAUDE.md file」 | 200 | CONFIRMED | |
| 47 | 頻道建議：只放每次都要的、寫得出怎麼算做對的 | md-rule、3qqw | brief 站主觀點第 4 點 | — | OUT OF SCOPE（觀點，標了「這個頻道的建議」，與 brief 一致） | |
| 48 | g1 六條沒有 輸出/、同名、日誌；第 3 條跟你的第七條相反；你的規矩在第 7、8 行 | md-g1、gucw、eksp | RL R5 NOTE 逐條比對；12 行檔的第七條在第 9–10 行（md-r4 的 highlight [9,10]），第 7、8 行是第五、六條 | — | CHANGED（卡片） | 右欄「第 7、8 行：看內容對不對得上」→「第 7 條：看內容對不對得上」 |
| 49 | 練習：改第 3 條、同樣八個字重跑、看處理日誌 | md-edit、md-check、zg6v、6s29、csgn、y34h | 練習，不是實跑結果；第 3 條在第 5 行（highlight [5]） | — | OUT OF SCOPE | |
| 50 | 照修改時間排：10/20、10/18、10/05 與各自內容 | m3-table、q95g、icfx、v4ec、u6x7 | RL M3（台北時間 08:45、22:10、21:30；grep 三行） | — | CONFIRMED | |
| 51 | 打開大綱讀過的 4／4 選了真的最終版；g1 寫規矩前打開 0 個檔 | m3-who、7kgt、qey9 | RL R8、R9、R10、R10b 都選真的最終版；但 R13 pr1 也讀了三份大綱（並以真的最終版為準），所以「打開大綱讀過的那四次」少算一次 | — | CHANGED | 旁白「打開大綱讀過的那四次，四次都照內容…」→「整理大綱的那四次都打開讀過，四次都照內容…」；stats label「打開大綱讀過的」→「整理大綱、打開讀過的」 |
| 52 | a1 回覆第一句（引用）；a2 也選對並留日誌 | a1-quote、pf63、fgmk | demo/a1/reply.md 第 1 行逐字 FOUND；RL R10b C8 PASS、VERDICT RIGHT | — | CONFIRMED | |
| 53 | 只說動作對講目的；purpose.txt 全文與 highlight | list-say、list-ask、list-ask-log、2n7n、wssz、6mi9、x6xg | demo/prompts/vague.txt、purpose.txt MATCH | — | CONFIRMED | |
| 54 | p1 依序：一個指令讀兩個檔、想跑小程式被擋 4 次、改用寫檔工具寫三檔、回覆說沒跑程式建議看筆數 | list-steps、dgp2、z2ah、7zrx、2i58 | RL R4 stream summary、reply「我沒能跑 Python 腳本,是手動核對 24 列後直接寫入的。建議你開 CSV 看一下筆數。」 | — | CONFIRMED | |
| 55 | 日誌數字 16、3、素食 4（劉思妤若來 5，建議先報 5）、海鮮過敏 2，期限在同一段 | list-stats、6edf、y9ad、3jad | demo/p1/輸出/處理日誌.md 第 6–7、26–29 行 | — | CONFIRMED | |
| 56 | 確認信草稿第 15–21 行（全檔 47 行）；日期、時間、地點對；地址、取消方式留空 | letter、letter-blank、4d2n、dnpn | demo/pr2/輸出/確認信草稿.md 第 15–21 行 MATCH、47 行；第 19、32 行【請補上】；活動說明.md | — | CONFIRMED | |
| 57 | 「活動前一天（11/12）會再寄一封行前提醒。」；講座 14 號，12 號是前兩天 | letter-slip、ijrk、bf6z | demo/pr2/輸出/確認信草稿.md 第 34 行逐字；活動說明.md 第 3 行 | — | CONFIRMED | |
| 58 | 第二批 6 筆 | skill-open、rdqu | demo/extras/batch2/報名表_第二批.csv 6 筆 | — | CONFIRMED | |
| 59 | Skill 內文用到才載入；平常只看介紹（引用與翻譯） | skill-what、7b7i、uqww | SK「Unlike CLAUDE.md content, a skill's body loads only when it's used」「skill descriptions are loaded into context … full skill content only loads when invoked」 | 200 | CONFIRMED | |
| 60 | 放哪裡：規矩 CLAUDE.md；重貼的指示、長成流程的段落做成 Skill | skill-choose、ce5d、e3dj、k8gk | SK「Create a skill when you keep pasting … or when a section of CLAUDE.md has grown into a procedure」；ME「Keep it to facts Claude should hold in every session」 | 200 | CONFIRMED | |
| 61 | SKILL.md 第 1–5 行、第 7–18 行（全檔 18 行）全文與 highlight；存在 .claude/skills/signup-check/ | skill-head、skill-desc、skill-when、skill-s1–s3b、qyw3、jkeu、saer、c3st–6pwj | demo/extras/skill/.claude/skills/signup-check/SKILL.md 逐字 MATCH，18 行，第 6 行空白，cf53f2c9bcd4faf6；SK 位置表 Project `.claude/skills/<skill-name>/SKILL.md` | 200 | CONFIRMED | |
| 62 | description 幫 Claude 判斷什麼時候自動載入（引用） | skill-auto、9hhb | SK「the `description` helps Claude decide when to load the skill automatically」 | 200 | CONFIRMED | |
| 63 | 兩種叫法的原文；兩次技能清單都有 signup-check；k2 第一個動作是 Skill 工具呼叫（引用 JSON） | skill-ask、skill-pick、955c、743t、ubzr、xxz6 | demo/prompts/skill-slash.txt、skill-auto.txt；RL R11、R12 init skills 第一個是 signup-check；R12 第一個 tool_use Skill 逐字 | — | CONFIRMED | |
| 64 | 兩次六項全過；兩個新人、王志明沒重複、測試二不在、宋柏均進要補資料、18 個 Email、黃雅婷改線上被提出 | skill-run、h5hp、dkmu、fise | RL R11、R12 second batch B1–B6 PASS | — | CONFIRMED | |
| 65 | k1 回覆引用句；部門只套在新加的兩筆、舊名單問你要不要一起改 | skill-dept、qsm5 | demo/k1/reply.md 逐字 FOUND（半形逗號照原文） | — | CONFIRMED | |
| 66 | 接上前先確認信得過；會抓外部內容的可能被提示注入 | trust 第 3 項、vjir、mkj6 | MCP「Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk」 | 200 | CONFIRMED | |
| 67 | 別人給的 Skill 先讀；連接器只接會用的 | trust 第 1、2 項、u29s、cxbq | 卡片標「頻道建議」；brief 站主觀點沒有這兩條 | — | OUT OF SCOPE（觀點，見觀點不一致） | |
| 68 | 連接器就是有圖形設定的 MCP 伺服器；能讀行事曆、發訊息 | connect、mpg2、vjir | D「Connectors are MCP servers with a graphical setup flow.」「Claude can read your calendar, send messages」；`#connect-external-tools` 錨點存在 | 200 | CONFIRMED | |
| 69 | ＋ → Add connectors 打開目錄；Settings > Connectors 管理或拔掉 | connect-steps、s4ma、bdds | D Connect external tools | 200 | CONFIRMED | |
| 70 | 三種排程比較：開電腦、開對話、讀檔、最短間隔 | sched、4vmi、5cge、rtnu、x8et | ST Compare scheduling options 表（Requires machine on No/Yes/Yes；Requires open session No/No/Yes；Access to local files No/Yes/Yes；Minimum interval 1 hour/1 minute/1 minute） | 200 | CONFIRMED | |
| 71 | 9 點的任務、電腦睡一整天可能 11 點才跑（引用與翻譯） | sched-quote、ayze | ST「A task scheduled for 9am might run at 11pm if your computer was asleep all day.」；`#missed-runs` 存在 | 200 | CONFIRMED | |
| 72 | 要讀你的檔就用桌面版排程 | sched-quote、2kxy | ST 比較表 | 200 | CONFIRMED | |
| 73 | daily.txt 全文與 highlight | daily、daily-out、pmzn、2reg | demo/prompts/daily.txt MATCH | — | CONFIRMED | |
| 74 | d1：兩個新報名、宋柏均另外註記、找不到確認信名單改用寄信名單；因為 s1 存成寄信名單 | daily-res、p72q、c9ng、52ry | RL R15 reply；demo/d1/輸出/每日報名摘要.md；RL R6 created 輸出/寄信名單.csv | — | CONFIRMED | |
| 75 | 檔名對不上，每天的檢查就接不起來 | name-rule、fyda | RL R15：d1 找到 寄信名單.csv 當替代，照樣列出兩個新報名；「接不起來」與紀錄不符 | — | CHANGED | 「每天的檢查就接不起來」→「它只能自己找替代的檔」 |
| 76 | tutor.txt 全文；在規劃模式問，它只回答、不動任何檔 | tutor-ask、eazv、ryau | demo/prompts/tutor.txt MATCH；RL R16 mode plan、一個 Read、雜湊不變 | — | CONFIRMED | |
| 77 | t1 三句引用；建議加在第 5 步後當新的第 6 步；沒打開報名表、不知道寫在哪一欄 | tutor-explain、tutor-quote、tutor-caveat、y9ec、zapm、ycje | demo/t1/reply.md 三句逐字 FOUND | — | CONFIRMED（「再給一句」見懷疑） | |
| 78 | 它讀得到也改得到一切；刪檔在自動接受範圍；其餘是頻道建議 | risk、xx3t、f59b、8v78 | PM（同 #30）；其餘見觀點不一致 | 200 | CONFIRMED（事實部分） | |
| 79 | 檢查：日誌說幾筆檔案就差幾筆；驗收看檔案不看「已完成」 | check、check-how、4g7t、7ktj、iexi | brief 站主觀點第 3 點；RL R4 reply 也建議看筆數 | — | OUT OF SCOPE（觀點，標了「這個頻道的做法」，一致） | |
| 80 | 三件事、片尾 | three、closing | 觀點與總結，與 brief 第 1、3、4 點一致 | — | OUT OF SCOPE | |
| 81 | 標題「四個基本功整理一整個資料夾」、縮圖「零程式也能用」、tags | youtube.title、thumbnail、tags | 與內文一致，無數字 | — | CONFIRMED | |
| 82 | 說明欄：2026-10-21、Windows 11、2.1.295、sonnet、claude -p、19 次其中 1 次登入失敗 | youtube.description | RL 開頭、M0、R1、總表（19 sessions，c1 exit 1） | — | CONFIRMED | |
| 83 | 說明欄：每次都從同一份練習資料夾重建 | youtube.description | RL：k1、k2（from p1）、pr1、pr3、d1（from s1）、pr2（from pr1）、t1（from k1）共 7 次從快照開始 | — | CHANGED | 「每次都從同一份練習資料夾重建。」→「…重建，接續的 7 次從前一次跑完的資料夾開始。」（claims.md 開頭同步） |
| 84 | 說明欄：每一句要求也都完整放在畫面上 | youtube.description | progress.txt、continue.txt、write-claude-md.txt、chat-purpose.txt 沒有完整上畫面（ctx-steps、g1-rule、c2-list 只講大意） | — | CHANGED | →「名單、三份最終版、排程與家教的要求句，和叫 Skill 的兩種說法，都完整放在畫面上；寫進度、接著寫信、請它寫規矩、只貼文字的那幾句只講大意。」 |
| 85 | 說明欄：CLAUDE.md 12 行、SKILL.md 18 行完整出現；8、8、9；十項檢查從檔案判定；每種情況跑 1 次；排程那一句跑過 1 次；連接器沒接；Codex 沒裝 | youtube.description | #40、#61、#43、RL M2、R15；各 session 一次 | — | CONFIRMED | |
| 86 | 說明欄：手動模式不開畫面時直接被拒；桌面版會停下來問 | youtube.description | RL R9；DQ「Manual: Claude proposes each change and waits for your approval」 | 200 | CONFIRMED | |

## 摘要

- 檢查的主張：86 條；CONFIRMED 72，CHANGED 7，NOT FOUND 0，OUT OF SCOPE 7。
- 事實修正 7 處：kgnr（拿掉「全」）、mvtb（「停在等人同意」→「全被擋下」）、md-g1 卡（「第 7、8 行」→「第 7 條」）、m3-who（旁白與 stats label：pr1 也讀了大綱）、fyda（d1 自己找到替代檔，不是「接不起來」）、說明欄兩處（快照接續的 7 次；要求句不是每一句都完整上畫面）。`claims.md` 的 c9、c14、c21、c40、c43、c61 與開頭的共同條件同步改；`sources` 的 `checked_on` 已是 2026-10-21，不用改。沒有任何一句的 `say` 要改（全片沒有 `say`）。
- 快要過期的事實：方案名單（Pro、Max、Team、Enterprise）、Auto 模式「有開放才出現」、桌面版「提示框下面那一排」的新版面（DQ 自己寫了舊版面的分支）、排程比較表的最短間隔與「需要 Claude Desktop 1.1.5368 以上」、PM 寫明 v2.1.302 起 `claude -p` 沒指定模式時從 Manual 開始（這次每次都有傳 `--permission-mode`，不受影響，但片中的實跑是 2.1.295）。官方頁都沒有標更新日期，以 2026-10-21 抓到的版本為準。
- 觀點不一致：trust 卡第 1、2 項（別人給的 Skill 先讀、連接器只接會用的）與 risk 卡「原始檔先另外留一份」「寄信、刪檔自己按」標成「頻道建議」，但 brief 的站主觀點四點裡沒有（第 3 點只有「原始檔只讀不改」）；旁白 u29s、cxbq、f59b、8v78 也沒有標成觀點。另外 brief 的站主觀點本身寫著「提案，待站主確認」。沒有改寫。
- 聽眾檢查（只回報）：超過 40 字的句子 3 句：vdqi（41）、y9bk（42）、dkmu（42）。旁白沒有「經查證」「根據官方文件」「本影片」、括號或網址；vdqi「這支片給你…」與 4fh3「這支只講 Claude Code」提到影片本身，屬承諾句，不算製作過程。lint 0 警告，沒有未登錄的拉丁詞警告。
- lint：修改後 `node tools/video/cli.mjs lint --slug claude-code-beginner-event-folder` 0 errors、0 warnings，估 21.5 分鐘、220 句。
- 懷疑但沒改：
  - dj2h／perm-plan kicker「計畫開頭就先提醒」：pl1 回覆第一句其實是「我還沒動任何檔案，計畫已寫好…」，提醒在第二段；說成「開頭」略寬。
  - f86u「每一份報名表裡，都有一筆叫「測試」」：此時片中只介紹了一份報名表，第二批那一筆叫「測試二」。
  - y9ec「再給一句能直接貼進去的話」：t1 實際給了兩句（新的第 6 步，和改寫的第 7 步）。
  - snrs「打開整個桌面，連私人的檔它也讀得到」：沒有實跑，是由 PM 的範圍與 pr1 讀 11 個檔推出的能力說法。
  - perm-table「Plan 只讀」：D 的原文是「reads files and runs commands to explore」，也會跑探索用的指令。
  - runlog R13 的 runner NOTE「It read 11 files (all the text files and both PNGs)」本身不對（沒讀 報名表.csv、輸出/寄信名單.csv），claims.md c14 已註明；runlog 沒改（不在可改範圍）。
  - 「Unexpected results」第 1 條也漏了 pr1 讀過大綱。
  - md-changed 右欄兩點幾乎同義（「部門寫法沒有統一」／「回覆裡說：部門寫法沒有統一」），屬版面。
  - 撰稿者已列的：長度 21.5 分鐘超過目標；所有 session 繼承桌面版子 shell 的環境變數；c2 不是網頁版本身。
  - Codex 只查到 OpenAI 的文件把它列為產品，「同類工具」沒有逐項比對。
- 需要第二輪：是（事實修正 7 處，超過 3 處）。第 2 輪要重查 #17、#25、#48、#51、#75、#83、#84，並抽查已確認的三分之一。
- 這份稿在第 2 輪完成前不算查核完成。
