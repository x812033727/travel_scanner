# verify-1：skills-one-year-monthly-report（第一輪查核）

查核日 2026-10-20（UTC）。查核者是另一個代理，沒有寫這支稿子；只寫這一份檔，沒有動 `video.json`、`claims.md`、`brief.md`。

**查的是哪一版**：`video.json` 在查核期間被撰稿端改了三次（16:33、16:38、16:40）。下面的場景與句子 id 以 16:40:53Z 那一版為準（sha256 `b1c42ec4a959c07fb9aaa0a706c81552fecf2db8249727a5e7146f75b9f6853c`，34 個場景、96 句、lint 0 錯誤 0 警告）；之後再改的，第二輪要重對。

**讀過的檔**：`brief.md`、`claims.md`（c1–c25）、`video.json`（每張卡、每句旁白、標題、說明欄、縮圖、loops）、`runlog.txt`（正式的第三輪，13 個 session）、`runlog-pilot.txt`、`demo/`（seed、skills/good、skills/vague、prompts、results/tally.txt、results/*/meta.txt 與 report.md、validate/validate.log、SKILL.broken.md、SKILL.typo.md、run.sh、batch.sh、tally.mjs、runlog.mjs、expected.json）、`.agents/skills/youtube-video/references/script-writing.md` 的〈含金量〉〈故事主線與鉤子〉〈結尾〉〈給 TTS 唸的稿子〉、`docs/videos/lexicon.json`、站內文章 `apps/api/app/guides/content/claude-skills-explained.json`。另外自己跑了 `node demo/skills/good/monthly-report/scripts/sum.mjs demo/seed/data/2026-09.csv` 與 `node tools/video/cli.mjs lint --slug skills-one-year-monthly-report`。

**開過的官方頁**（今天 16:02–16:16Z 抓下來的副本在查核者的工作區；16:4xZ 再用 curl 確認狀態碼，UA `Mokaair-editorial/1.0`，各主機一次）：

| 頁 | 今天的 HTTP | 備註 |
| --- | --- | --- |
| https://code.claude.com/docs/en/skills（含 `.md` 版） | 200 | 錨點 `#where-skills-live` 存在（`<h2 id="where-skills-live">Choose where skills load`） |
| https://code.claude.com/docs/en/plugins/cli-reference | 200（今天的副本） | `validate` 結束碼 0／1，另有 2；`--strict` 把警告當錯誤 |
| https://www.anthropic.com/news/skills | 200 | 轉到 https://claude.com/resources/articles/skills；datePublished 2025-10-16；更新註記 December 18, 2025 |
| https://agentskills.io/ | 200 | 轉到 /home；Discovery、Activation、Execution 三段 |
| https://support.claude.com/en/articles/12512180-using-skills-in-claude | 200 | 轉到 …/12512180-use-skills-in-claude |
| https://developers.openai.com/codex/skills | 200 | 轉到 https://learn.chatgpt.com/docs/build-skills；`.agents/skills` 四個位置 |

## 必改

| # | 位置 | 問題 | 證據 | 建議改成 |
| --- | --- | --- | --- | --- |
| 必 1 | `skill-head` 的 `2ikd`「開頭三行夾在兩條橫線裡：一個名稱，一句描述。」 | 旁白跟卡片對不上：卡片標題是「SKILL.md 的開頭四行」，兩條 `---` 之間只有**兩行**（`name:`、`description:`）。觀眾看著四行聽到「三行夾在兩條橫線裡」會去數。 | `demo/skills/good/monthly-report/SKILL.md` 第 1–4 行：`---`、`name: monthly-report`、`description: …`、`---` | 「開頭四行：兩條橫線，中間夾著一個名稱、一句描述。」（說明欄「SKILL.md（開頭三行加五條規則）」與企劃的「三行開頭」是同一個算法——把開頭的 `---` 算進去、關的不算——片中不要兩種算法並存；旁白統一講「兩條橫線夾著名稱和描述」最不會錯。） |
| 必 2 | `name-big` 的 `kszc`「救它的是名字：monthly-report，對上了業績整理這句話。」、卡片 kicker「monthly-report 對上了「業績整理」」、`closing` 卡第 2 行「描述寫成廢話照樣被呼叫：名字對上了」、說明欄「名字對上了，所以被呼叫不是描述寫對的證據」 | 比紀錄強。紀錄量到的是：描述換成「專案維護用的說明。」之後 v1–v3 仍被呼叫、6／6。「是名字對上的」是推論（要證明得把名稱也換掉再跑三次，這次沒跑；`claims.md` c18 自己也寫「是站主的判讀」），但旁白與卡片都寫成事實，沒有任何「我判斷」「應該是」的標記。〈意見與事實〉要求意見明說。 | `runlog.txt` §v1–v3：第一筆 `Skill {"skill":"monthly-report"…}`、`skills:` 清單只有 monthly-report 一個專案 Skill；`claims.md` c18、「我懷疑但沒動的事」第一條 | `kszc` →「我的判讀是名字救了它：monthly-report，對上了業績整理這句話。」（29 字）；kicker →「我的判讀：monthly-report 對上了「業績整理」」；`closing` 第 2 行 →「描述寫成廢話照樣被呼叫：靠的應該是名字」；說明欄 →「名字很可能就對上了，所以被呼叫不是描述寫對的證據」。`v39w`「所以被呼叫，不能當成描述寫對的證據」不用改——這一句本來就是紀錄撐得住的結論。 |
| 必 3 | `keep` 章名「同一個資料夾，放進應用程式和 Codex 照樣用」、`cjc4`「同一個資料夾上傳到 Claude 應用程式也能用，開頭只收六個欄位。」、`cdti`「放進 Codex 讀的那個資料夾，同一份檔就能用。」、`upload` 的 `7sjg`「…清單裡打開，就能在對話裡用。」 | 比紀錄強，而且對**這一份** SKILL.md 很可能是錯的。能引用到的只有：claude.ai 上傳只收六個欄位、Codex 讀 `.agents/skills` 底下同一種 SKILL.md（要有 name 與 description）；企劃與說明欄都寫「沒有在應用程式或 Codex 實際載入」。但這份 SKILL.md 第 9、11 行寫死了 `node .claude/skills/monthly-report/scripts/sum.mjs` 與 `.claude/skills/monthly-report/template.md`：搬到 `.agents/skills/` 或上傳到 claude.ai 的沙箱，這兩個路徑都不存在，第 2、3 條規則會指到沒有的檔。「同一份檔就能用」「照樣用」「就能在對話裡用」沒有一次執行撐著，官方頁也只說格式相容，不說檔案裡的路徑會自動對。 | `demo/skills/good/monthly-report/SKILL.md` 第 9–11 行；skills 頁「Using skill frontmatter outside Claude Code」（只講六個欄位）、Codex 頁「Where Codex loads local skills」（只講位置與 name／description）；`brief.md`〈沒有觀察到的事〉第 2 條；`claims.md` c23「這支沒有實際上傳，卡片標引用」 | 章名 →「同一種 SKILL.md，應用程式和 Codex 也收」。`cjc4` →「開頭這幾個欄位，上傳到 Claude 應用程式也收，一共只收六個。」`cdti` →「Codex 讀的是同一種 SKILL.md，放在它的資料夾就找得到。」`7sjg` →「在自訂裡的技能那一頁上傳，清單裡打開，它就會進清單。」並在 `keep` 或 `upload` 補一句把路徑的事講白（這是觀眾照做會踩的坑）：「正文裡寫死的 .claude/skills 路徑，搬過去要改成相對路徑。」卡片出處維持「引用」。 |

## 建議

| # | 位置 | 問題 | 證據 | 建議改成 |
| --- | --- | --- | --- | --- |
| 建 1 | `open` 的 `g8y7`「…寫出四個區段的報表，最後一行是總營收八萬五千兩百九十元。」 | 「最後一行」緊接在「報表」後面，聽起來像報表的最後一行；紀錄裡是**回覆**的最後一行（報表的最後一行是 20,800 元那筆大額交易）。 | `runlog.txt` §s1 [6] TEXT 最後一行「報表已寫到 reports/2026-09.md,總營收 85,290 元。」；§s1 的 reports/2026-09.md 最後一行是「- 2026-09-18 咖啡豆 200g(40 件):20,800 元」 | 「它跑了一支腳本，寫出四個區段的報表，回覆的最後一行是總營收八萬五千兩百九十元。」 |
| 建 2 | `ask` 卡 Claude 那一句「報表已寫到 reports/2026-09.md，總營收 85,290 元」；`bare-reply` 卡「我沒辦法執行 Python 腳本，所以直接用資料手算。」 | 兩張卡都把原句的半形逗號改成全形，`ask` 還拿掉了 s1 原句的句號。〈含金量〉補充條寫「任何字元都不改」，而且 `claims.md` c1 說「s1 的原句…沒有句號」也不對（s1 有句號，s2、s3 沒有）。 | `runlog.txt` §s1 [6]「報表已寫到 reports/2026-09.md,總營收 85,290 元。」；`results/tally.txt` s1 replyLast 同；§b2 [4] TEXT 第一句「我沒辦法執行 Python 腳本,所以直接用資料手算。」 | 照原字放：`ask` 用「報表已寫到 reports/2026-09.md,總營收 85,290 元。」（32 字，在 chat 卡 44 字內）；`bare-reply` 用「我沒辦法執行 Python 腳本,所以直接用資料手算。」；c1 的括號改成「s1 的原句是半形逗號、有句號；s2、s3 沒有句號」。 |
| 建 3 | `bare-reply` 的 `3894`「回來的表多了占比和退貨率，沒有人要求，每次長得也不一樣。」 | 占比三次都有；「退貨率」只有 b1 寫了這個詞（25%），b3 寫的是退貨占銷售總額 4.9%，b2 只列退貨筆數與金額。「每次長得也不一樣」對。 | `runlog.txt` §b1 [4]「退貨率:保溫杯…佔 25%」；§b2 [4] 只有「退貨:-4,380,共 2 筆」；§b3 [4]「退貨合計 4,380,約佔銷售總額的 4.9%」 | 「回來的表多了占比，有一次還多了退貨率，沒有人要求，每次長得也不一樣。」 |
| 建 4 | `layers` 的 `uq9w`「這就是開場只多五十三個 token 的原因。」 | TTS 清單裡「只多六十九」被聽成「至多六十九」，意思反過來。 | script-writing.md §給 TTS 唸的稿子 最後一列 | 「開場多出來的只有五十三個 token，原因就在這裡。」 |
| 建 5 | `rb7e`「這支放在專案裡…」、`6iq3`「這支只用了兩個…」、`si22`「這支沒有寫這一行…」 | 「這支」在頻道的用語裡是「這支影片」，聽起來像在講片子怎麼做的（〈含金量〉：旁白不講這支片是怎麼做的）；TTS 清單裡「這支 hook」也被聽成「只是 hook」。`fumr`「這支腳本」後面有名詞，不用改。 | 同上 | `rb7e`「這個 Skill 放在專案裡，月報跟著店的資料夾走。」`6iq3`「這份 SKILL.md 只用了兩個，剛好都在裡面。」`si22`「這個 Skill 沒有寫這一行；腳本跑得了，是因為那次的核准清單本來就有它。」 |
| 建 6 | `6nfy`「…一個報表檔都沒有寫。」、`8wbc`「…報表檔在不在…」 | 「報告檔」在 TTS 清單裡被聽成「報告黨」，「報表檔」同一個結構。 | 同上 | `6nfy`「什麼都不給的三次，連報表的檔案都沒有寫。」`8wbc`「最後看磁碟：報表的檔案在不在，最後一行對不對。」 |
| 建 7 | `switch-off` 卡下半行 `{ "skillOverrides": { "deploy": "off" } }` 與 `z5x4`「不想改檔案，在設定裡把它關掉也行。」 | 卡片標題是「不要它自己接手」，但 `"off"` 是整個藏起來（你也不能用 `/deploy`）；官方頁對「不改檔案、只擋模型自己叫」給的值是 `"user-invocable-only"`。另外卡片那一行不是官方例子原文（原文是兩個鍵的多行 JSON，`legacy-context: name-only` 加 `deploy: off`），說明文字卻寫「官方 skills 頁的例子」。 | skills 頁〈Remove a skill〉末段：「To keep a personal or project skill but stop Claude from invoking it on its own, set `disable-model-invocation: true` … or `"user-invocable-only"` in `skillOverrides` when you don't want to edit the file」；〈Override skill visibility from settings〉的四值表與 JSON 例子 | 卡片改成 `{ "skillOverrides": { "deploy": "user-invocable-only" } }`，說明文字「…照官方 skills 頁的例子改寫｜引用」；`z5x4`「不想改檔案，在設定裡設成只讓你叫也行。」若站主想保留 `"off"`，旁白要講清楚「關掉是連你也叫不到」。 |
| 建 8 | `validate-b` 的 `46jf`「欄位名打錯一個字母…」與卡片標題 | 錯的檔是 `descriptions:`，是**多打**一個字母，不是打錯。 | `demo/validate/SKILL.typo.md` 第 3 行 | 「欄位名多打一個字母，它只警告，結束碼還是零；加嚴格模式才擋。」卡片標題同樣改「多打一個字母」。 |
| 建 9 | `closing` 的 `qjcw`「Skill 是一個帶著腳本和範本的資料夾，開頭一句描述，Claude 就自己接手。」 | 41 字（〈句子〉說 40 字以上會提醒；lint 這次沒報，仍偏長）；〈結尾〉第 1 句要「用數字回答開場的問題」，這一句沒有數字。 | script-writing.md〈結尾〉 | 「Skill 是一個帶著腳本和範本的資料夾，一句描述，Claude 自己接手，三次全中。」（33 字） |
| 建 10 | `upload` 的 `wbqb`「腳本在那邊會跑在它的沙箱裡，不碰你的電腦。」 | 這句的依據是站內文章（API 與應用程式的技能跑在沙箱），不是卡片出處寫的說明中心；說明中心只寫「Skills require the code execution environment」與安全注意事項。〈含金量〉要每張講事實的卡都標得出出處。 | `claims.md` c23；`claude-skills-explained.json`「API 的技能跑在沒有網路、不能安裝套件的沙箱裡，應用程式依設定可能有完整、部分或沒有網路」 | 卡片 `source` 改成「Claude 說明中心｜Mokaair 文章 查證 2026-10-20｜引用」，或把這一句改成說明中心撐得住的「上傳後要先開程式碼執行，它才跑得起來」。 |
| 建 11 | `exec-quote` 的 `3i9y`「…用途就寫在公告裡：帶著程式碼走。」 | 「寫在公告裡」是出處句型的邊緣（〈含金量〉第 5 條：出處放卡片，旁白直接講事實）。lint 沒報，但可以更直接。 | script-writing.md〈含金量〉5 | 「二〇二五年十月十六號公開那一天，它的用途就是這一條：帶著程式碼走。」 |
| 建 12 | 說明欄「SKILL.md（開頭三行加五條規則）」 | 跟卡片「開頭四行」兩種算法並存（見必 1）。 | `video.json` youtube.description | 「SKILL.md（兩條橫線夾著名稱和描述，加五條規則）」 |

## 附註（查過、要留紀錄的）

| # | 項目 | 結果 |
| --- | --- | --- |
| 註 1 | 計分表（`score`、`vague-score`、`closing`、說明欄） | 與 `demo/results/tally.txt` 逐格相符：b1–b3 0 被呼叫、0 寫檔、0／6；p1–p3 0、3、6／6；s1–s3 3、3、6／6；v1–v3 都被呼叫、都跑腳本、6／6；x1 無 Skill 呼叫、跑腳本、6／6。 |
| 註 2 | 第一個請求的 token（`typed`、`layers`、`call`） | `runlog.txt` 每節 `[first request usage]`：b 2+0+8106=8,108；v 2+0+8124=8,126；s 2+1103+7056=8,161；p 2+1890+6512（p1）與 2+1050+7352（p2、p3）都是 8,404；x 2+2109+6512=8,623。差值 ＋53、＋296、＋515、＋18 都對；同一臂三次相同。 |
| 註 3 | 費用（`4muh`） | 13 次 total_cost_usd 在 0.0235（b2）到 0.0682（p2）之間，「兩到七美分」「貼規則那一邊最貴的一次七美分」成立；說明欄「約 0.02 到 0.07 美元」成立。 |
| 註 4 | Python 與手算（`4a2t`、`7ttk`、`ziq6`、`how` 卡） | b1、b2、b3 各一筆 `python3` 被擋（permission_denials）；p2 兩筆（heredoc 的 python3 與 `python3 -I <SCRATCH>/report.py`）；p1、p3 沒有 Python，`cat data/2026-09.csv` 之後直接寫檔。六次報表或回覆的總營收都是 85,290。16:38 那一版把 `7ttk` 從「其中四次先想寫 Python」改成「貼規則的三次只有一次試了 Python」，兩種說法都對紀錄。 |
| 註 5 | 檔案與行數 | SKILL.md 17 行、sum.mjs 26 行、template.md 16 行、paste.txt 去掉換行 346 字元（13 行）、vague.txt 12 字、slash.txt 23 字、CSV 12 列；good 與 vague 的 SKILL.md 只差第 3 行；正文（第 5–17 行）13 行。 |
| 註 6 | `code` 卡逐字比對 | `skill-head`＝SKILL.md 1–4、`skill-body`＝7–17、`template-a`＝1–8、`template-b`＝9–16、`script-a`＝sum.mjs 9–14、`script-b`＝15–24、`vague-head`＝vague 1–4，全部位元相同；highlight 指的行也對（第二條規則、第五條規則、returns／large 兩行）。 |
| 註 7 | `terminal` 卡 | `tree` 三行＝validate.log 第 3–5 行；`validate-a`、`validate-b` 的輸出把 78 欄斷行接回去後與 validate.log 第 32–36、54–58 行逐行相同；工具版本「2.1.304 (Claude Code)」「sort (GNU coreutils) 9.4」與 log 第 1–2 行相符。`run-script` 的七行＝`sum.mjs` 對 seed 跑出來的前七行（查核者重跑一次相同）。 |
| 註 8 | `run-script` 卡的指令 | s1 實際那一筆是複合指令 `ls data; cat …/template.md; node …/sum.mjs data/2026-09.csv`，卡片只放 node 那一段，輸出是這一段的輸出，沒有改字；v1 的第 3 筆是單獨跑這一行。`claims.md` c6 寫「前 8 行」，卡片是 7 行。可把 c6 改成 7 行，或出處加註「指令取 s1 複合指令的 node 那一段」。 |
| 註 9 | `call` 卡 | JSON 與 s1、s2、s3 第一筆 tool_use 的 name 與 input 相同（`{"skill":"monthly-report","args":"九月"}`）。v1、v3 也相同；**v2 的第一筆是 `{"skill":"monthly-report"}`，沒有 args**。片中沒有任何一張卡或一句旁白說 v 臂帶了「九月」（`pqjp` 講的是 s 臂），所以稿子沒錯；但 `claims.md` c18「v1–v3 都被呼叫（第一筆 Skill，args 九月）」與 `brief.md` V 列「第一筆呼叫同樣是 Skill {…"args":"九月"}」要改成「v2 沒有 args」。 |
| 註 10 | `quote` 卡原句 | 「Skills can include executable code for tasks where traditional programming is more reliable than token generation.」（公告，Powerful 那一點）、「Seeing a skill trigger tells you Claude found it, not that it did what you intended.」（Evaluate and iterate on a skill 第一句）、「allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)」（Available string substitutions 的 render-chart 例子）都逐字相符；`switch-off` 上半 deploy 的 frontmatter 四行與〈Control who invokes a skill〉例子相同。 |
| 註 11 | 引用的事實 | 2025-10-16 公開、2025-12-18 加註開放標準（公告頁）；`name` 不寫用資料夾名、`description` Recommended、「Claude uses this to decide when to apply the skill」、`description`＋`when_to_use` 合計 1,536 字元被截（Frontmatter reference）；叫過的內容「stays there across later turns」「does not re-read the skill file」（Skill content lifecycle）；三層載入（agentskills.io Discovery／Activation／Execution；skills 頁「Description always in context, full skill loads when invoked」）；位置表（Personal「All your projects on this machine」、Project「Sessions in this repository. Commit it so your team gets it too」、Plugin「Wherever the plugin is enabled」）；Codex `$CWD/.agents/skills`、`$REPO_ROOT/.agents/skills`、`$HOME/.agents/skills`，SKILL.md 必須有 name 與 description；上傳只收 `name, description, license, compatibility, metadata, allowed-tools`；刪資料夾就是移除；`/skills`（多處）與「What skills are available?」；Skill not triggering 1–4 與最後一段的 validate；`claude plugin validate` 結束碼 0／1、`--strict`；說明中心「Skills section not visible: Ensure code execution is enabled in Settings > Capabilities」、上傳步驟「Package your skill folder as a ZIP file → Customize > Skills → + → + Create skill → Upload a skill」（`upload` 卡少了「+ Create skill」這一步，可補）。全部與今天的頁一致。 |
| 註 12 | `where` 的 screencast | 錨點 `#where-skills-live` 在今天的頁上存在（h2「Choose where skills load」），`wait` 與 `capture` 的 selector 找得到。`suwq`「家目錄底下的，你每個專案都有」官方表多一句「but not Cowork or cloud sessions」，旁白省略可接受。 |
| 註 13 | 站內文章（`cta`） | `claude-skills-explained.json` 有「技能／專案 Projects／個人指令與自訂樣式／MCP 連接器」的比較表，`qgki` 成立。 |
| 註 14 | 開場、章名、鉤子、結尾 | 開場四句在同一個時刻（十月一號、十二筆、十二個字、第一步呼叫 Skill），之後丟了三個時刻（什麼都不給、描述改廢話、引號沒關）再問「Skill 到底是什麼…」；`loops` 8 個，回收都在埋設之後。章名都是「發生了什麼」。結尾三句：答案、留言題、有理由的訂閱邀請，沒有「下一支」。數字重複：十二（三處，兩處是不同事實）、五十三（`uq9w` 是回呼）、一萬（連著兩句），都在三次以內。沒有「文件寫」「官方說」「以官網為準」「經查證」「本影片」；沒有括號與網址進旁白。 |
| 註 15 | 旁白裡講製作過程的句子 | 沒有「這支影片沒跑過」「尚待驗證」之類；「這次都算對了」「那次的核准清單」是講執行本身，算步驟。唯一的邊緣是「這支」三處（建 5）。 |
| 註 16 | TTS 風險字（除建 4–6 之外） | 「對上了」（`kszc`）接近清單裡「對上就→對象就」，改成必 2 的寫法後仍有「對上了」，可改「跟業績整理這句話對得上」；「來接」（`f5j3`）不在清單裡，先錄再看。英文詞 Claude、Skill、monthly-report、description、SKILL.md、token、Python、repo、Codex、ZIP 都在 `lexicon.json`，lint 0 錯誤。 |
| 註 17 | `brief.md` 裡過期的數字（不是稿子的問題，站主選大綱時會看到） | 執行紀錄表 P 列「paste.txt（335 字）」與大綱 A 第 2 章「12 字對 335 字、＋67 對 ＋285 token」是第二輪前的數字，正式輪是 346、＋53、＋296；第 4 章「SKILL.md 全文（12 行）」正式檔是 17 行；「每一臂的 heredoc 寫檔都被擋下…十二次都一樣」不對：b1–b3 沒寫檔所以沒有 heredoc，v1 直接用 Write（permission_denials 為空），實際是 s1–s3、p1、p3、v2、v3、x1 共 8 次。 |
| 註 18 | 試跑 | `runlog-pilot.txt` 開頭與各節：腳本與範本放在專案的 tools/ 底下，b1 自己找到並跑了腳本、5／6；s2、p2、b2 被中途停掉；稿子與說明欄只用了「設計因此改掉」這一件事，沒有引用試跑的數字。 |

## 結論

**改了再過。** 數字、計分、token、費用、檔案行數、每一張 code／terminal／call／quote 卡都對得上紀錄與今天的官方頁，lint 零錯誤；要改的是三處說得比紀錄強的地方：`2ikd` 把開頭四行講成「三行夾在兩條橫線裡」（跟卡片對不上）、「名字就對上了」在旁白、kicker、片尾卡、說明欄四處都寫成事實而紀錄只撐得起「站主的判讀」、第 7 章「同一個資料夾放進應用程式和 Codex 照樣用／就能用」沒有任何一次執行撐著，而且這份 SKILL.md 寫死的 `.claude/skills/…` 路徑搬過去就會指到沒有的檔。三處都是改字不改結構，改完請第二輪對 16:40:53Z 之後的版本重核一次這三處加建 2、建 7（卡片內容有動）。
