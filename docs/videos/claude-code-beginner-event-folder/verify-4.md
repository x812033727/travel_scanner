# verify-4：claude-code-beginner-event-folder

查核日 2026-10-21，第 4 輪。查核者不是撰稿者，也不是第 1–3 輪的查核者。沒有跑 git，所以沒辦法對修訂前後做差異；修訂 5 改動太多（190 → 131 句、99 → 79 場景），這一輪把 131 句旁白、所有卡片的 `data`、縮圖、標題、說明欄、標籤全部重查。實跑的主張逐字對 `runlog.txt` 與 `demo/`（卡片上的要求句、CLAUDE.md、SKILL.md 用腳本比對字元，只忽略換行與換行後的縮排）；官方頁今天重抓 `.md` 版（UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，每次間隔 1.2 秒，去掉 `<!-- -->` 再讀），存在 `<work>/_tools/verifier4/`。web search 0／3。

官方頁（2026-10-21，頁面本身沒有更新日期）：

| 代號 | URL | HTTP |
| --- | --- | --- |
| DQ | https://code.claude.com/docs/en/desktop-quickstart.md | 200 |
| D | https://code.claude.com/docs/en/desktop.md | 200 |
| PM | https://code.claude.com/docs/en/permission-modes.md | 200 |
| MEM | https://code.claude.com/docs/en/memory.md | 200 |
| CMD | https://code.claude.com/docs/en/commands.md | 200 |
| COST | https://code.claude.com/docs/en/costs.md | 200 |
| SK | https://code.claude.com/docs/en/skills.md | 200 |
| SCH | https://code.claude.com/docs/en/desktop-scheduled-tasks.md | 200 |
| IM | https://code.claude.com/docs/en/interactive-mode.md | 200 |

## 主張表

| # | 主張 | 位置 | 依據 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | c68：提示框打 `@` 加檔名，把那一份拉進對話 | epgq、folder-at 第 1 列 | DQ「Type `@filename` in the prompt box to pull a specific file into the conversation.」；D「@mention files: type `@` followed by a filename」 | 200 | CONFIRMED | |
| 2 | c68：`@輸出/進度.md` 連資料夾一起指名（用法示意） | kwtd、ctx-at | D 同上；IM 的 `@` 是「File path mention」，路徑可用；caption 已標「用法示意」，進度.md 在 輸出/ 是 pr1 實跑 | 200 | CONFIRMED | |
| 3 | c69：打 `/` 看得到能叫的指令，Skill 也從這裡叫 | imr2、folder-at 第 2 列 | DQ「Type `/` or click **+** → **Slash commands** to browse built-in commands, custom skills, and plugin skills.」；D「invoke one directly: type `/` in the prompt box」 | 200 | CONFIRMED | |
| 4 | 開第一個對話四步：Code 分頁、環境選 Local、Open folder…、打字按 Enter | folder-steps、3z8j、hqqr、zfpy、yfn4 | DQ「click the first control, the environment selector, and select the top entry in the **Local** group. Then click the project folder control beside the environment selector, select **Open folder…**」；D「Type your task and press **Enter**」 | 200 | CONFIRMED | |
| 5 | Code 分頁內建 Claude Code、不用另外安裝；要 Pro、Max、Team 或 Enterprise | 8a3d、folder-plan | DQ「The desktop app includes Claude Code, so you don't need to install Node.js or the CLI」；「requires a Pro, Max, Team, or Enterprise subscription」 | 200 | CONFIRMED | |
| 6 | Chat 分頁不碰檔案 | which-tool 來源欄、第 1 列 | DQ「**Chat**: General conversation with no file access」 | 200 | CONFIRMED | |
| 7 | 「Start with a small project you know well.」 | folder-small | DQ 原句 | 200 | CONFIRMED | |
| 8 | 自動接受的修改只在這個資料夾裡 | folder-scope 第 2 項 | PM「auto-approval applies only to paths inside your working directory or `additionalDirectories`」 | 200 | CONFIRMED | |
| 9 | 打開整個桌面或文件資料夾，裡面的檔讀了不用問 | snrs、folder-trap | PM 模式表 `default`「Reads only」；第 3 輪已查 | 200 | CONFIRMED | |
| 10 | 五個模式各自怎麼做（表）；手動、自動接受編輯、規劃三句 | perm-table、said、3nzx、ema8 | D 模式表（Manual／Accept edits 含 mkdir、mv／Plan「reads files and runs commands to explore, then proposes a plan without editing」／Auto／Bypass「Only use this in sandboxed containers or VMs」） | 200 | CONFIRMED | |
| 11 | 桌面版一打開是哪個模式，查不到寫明的地方 | u22y、perm-unknown | D 只寫 `permissions.defaultMode` 與「remembered per folder」；PM 起始模式表只涵蓋終端機與 VS Code，桌面版指向 Desktop 分頁，該分頁也沒寫起始模式。不確定仍成立 | 200 | CONFIRMED（承認的不確定） | |
| 12 | 模式選單在提示框下面那一排、做到一半也能換；依資料夾記住；規劃模式只算這一次 | gd2z、perm-default | D「switch permission modes at any time using the mode selector in the row under the prompt box」；「remembered per folder … except Plan, which applies to the current session only」 | 200 | CONFIRMED | |
| 13 | 先切 Plan 送出、讀計畫、沒問題再切 Accept edits | perm-rule、perm-go、55xh、zsq5 | D TIP「Start complex tasks in Plan … Once you approve the plan, switch to Accept edits or Manual」 | 200 | CONFIRMED | |
| 14 | 用量圈在模型選擇器旁、看這次用了多少 | u4ry、ctx-tools 第 1 列 | D「Click the usage ring next to the model picker to see your current context window usage」 | 200 | CONFIRMED | |
| 15 | 上下文快滿會自動壓成摘要 | um5h | D「When context fills up, Claude automatically summarizes the conversation」 | 200 | CONFIRMED | |
| 16 | `/compact` 現在就壓縮，可加一句要保留什麼 | uu9z、id4n、ctx-compact | CMD「`/compact [instructions]` … Optionally pass focus instructions」；COST「`/compact Focus on code samples and API usage` tells Claude what to preserve」；D「type `/compact` to trigger summarization earlier」 | 200 | CONFIRMED | |
| 17 | `/clear` 開全新對話，專案的記憶還在 | 62gk、ctx-tools 第 3 列 | CMD「`/clear` starts fresh on a new task while keeping project memory」；D 不支援清單只列終端機面板指令，`/clear` 不在其中 | 200 | CONFIRMED | |
| 18 | CLAUDE.md 每次開對話先讀、放資料夾最上層 | 3ghe、md-why 引文 | MEM「Claude reads them at the start of every session.」；`./CLAUDE.md` | 200 | CONFIRMED | |
| 19 | 越精簡越一致；每份目標 200 行以內 | 4f33、md-much | MEM「The more specific and concise your instructions, the more consistently Claude follows them.」；「target under 200 lines per CLAUDE.md file」 | 200 | CONFIRMED | |
| 20 | Skill 平常只看介紹，用到才讀內文；一直重貼的指示做成 Skill | 7b7i、ce5d、skill-what、skill-choose | SK「Unlike CLAUDE.md content, a skill's body loads only when it's used」；「skill descriptions are loaded into context … full skill content only loads when invoked」；「when you keep pasting the same instructions」 | 200 | CONFIRMED | |
| 21 | 打斜線加名字直接叫 | 955c | SK「The directory name … becomes the command you type」 | 200 | CONFIRMED | |
| 22 | 三種排程表；讀本機檔又不用開著對話就選桌面版 | sched、hz2s | SCH 比較表：Requires machine on No／Yes／Yes；Requires open session No／No／Yes；Access to local files No／Yes／Yes | 200 | CONFIRMED | |
| 23 | 刪檔在自動接受範圍 | risk 來源欄 | PM「`acceptEdits` mode auto-approves … `rm`, `rmdir`, `mv` …」 | 200 | CONFIRMED | |
| 24 | g1：只列了檔名、一個檔都沒打開；第 3 條寫看修改時間最新的 | dqu9、646h、g1-rule | runlog g1：唯一的工具呼叫是 `Bash ls -la`，然後 Write；`demo/g1/CLAUDE.md` 第 5 行與卡片引文逐字相同 | — | CONFIRMED | |
| 25 | 報名表 24 列；缺 Email 3 列、兩個王志明 Email 不同、陳怡君兩次、張書豪取消、一筆測試 | signup-form、pxwh、gf7y | `demo/seed/講座籌備/報名表.csv` 第 2–25 行 | — | CONFIRMED | |
| 26 | c2 只給文字：交出一段文字、0 個檔、沒提 11/01 | p95r、t4kn、paste-vs-folder 左欄 | runlog c2 tools=0；`demo/c2/reply.md` 沒有 11/01 | — | CONFIRMED | |
| 27 | n1 只說「幫我整理報名名單。」也自己讀了活動說明、提到 11/01、名單存成檔、報名表沒動 | zs3t、5xbh、paste-vs-folder 右欄 | runlog n1：Read 活動說明.md；回覆「11/01 前要給場地」；created 報名名單_整理後.csv；C1 sha 不變 | — | CONFIRMED | |
| 28 | 三份大綱的修改時間與內容；照時間排最上面的是舊內容 | m3-table、uy62、icfx、v4ec | seed 三份大綱第 3–4 行；runlog folder before 的 mtime；活動說明 16:30 | — | CONFIRMED | |
| 29 | 11/1 前給場地飲食人數；11/7 前寄確認信 | t4kn、nzzz | 活動說明「11/01 前：把飲食需求彙整給場地」「11/07 前：寄出確認信」 | — | CONFIRMED | |
| 30 | 要求句（versions、purpose、daily、tutor）與卡片 | versions-ask、list-ask、list-ask-log、daily、tutor-ask | 腳本比對 `demo/prompts/*.txt`：四份都相同 | — | CONFIRMED | |
| 31 | pl1：一個檔案都沒動，計畫第一個提醒 | r8fw、perm-plan | runlog pl1 created／changed／removed 都是 none；`demo/pl1/reply.md` 第 3 行（第 3 輪已查） | — | CONFIRMED | |
| 32 | a1：改名、搬進封存，回覆第一句 | ktbf、a1-quote | `demo/a1/reply.md` 第 1 行與引文相同；VERDICT RIGHT。但 a1 有 `permission_denials=3`（兩次 PowerShell 搬檔、一次 PowerShell 讀檔），最後才用 Bash `mkdir && mv` 搬完；說明欄自己說「不開畫面時會直接拒絕，桌面版會停下來問你」，所以在桌面版會有 3 次詢問，「它都直接做」不成立 | — | CHANGED | 「不會。改名、搬進封存它都直接做，回覆第一句就講清楚：…」→「不會。改名、搬進封存都做完了，回覆第一句就講清楚：…」 |
| 33 | pr1：照規矩把進度放進 輸出/，不在最上層；回覆引文 | dmw2、ctx-miss | `demo/pr1/reply.md` 第 1 行；runlog pr1 folder after `./輸出/進度.md` | — | CONFIRMED | |
| 34 | 進度寫做完的、還沒做的、下一步 | urtk、ctx-steps | `demo/prompts/progress.txt` | — | CONFIRMED | |
| 35 | CLAUDE.md 12 行全文、八條的順序與「第三條」 | md-all、md-r1–r5、md-edit、83z3、hrrt、uqir、qy7z、d5e5、zg6v | 腳本比對 `demo/extras/claude-md-specific/CLAUDE.md`：相同、12 行；md-edit 標第 5 行＝第三條 | — | CONFIRMED | |
| 36 | 只寫一句「名單要整理乾淨」跟沒寫一樣：沒日誌、要補資料的人混在名單裡 | qx6k、mg2d、md-vague | `demo/extras/claude-md-vague/CLAUDE.md` 3 行；runlog v1 C7、C8 FAIL，與 n1 相同 | — | CONFIRMED | |
| 37 | p1：寫出三個檔、原檔沒動、素食與過敏人數；卡片 16／3／4 或 5／2 | bbu5、list-stats | runlog p1 created 三個檔、C1 sha 不變；`demo/p1/輸出/處理日誌.md` 第 6、7、27–29 行 | — | CONFIRMED | |
| 38 | pr2：換到新對話寫的草稿，日期、時間、地點對得上；第 15–21 行（全檔 47 行） | fzm9、letter | `demo/pr2/輸出/確認信草稿.md` 47 行，第 15–21 行與卡片相同；活動說明日期、時間、地點 | — | CONFIRMED | |
| 39 | 「活動前一天（11/12）」，講座十四號，它寫的那一天是前兩天 | ijrk、bf6z、letter-slip | 草稿第 34 行逐字相同 | — | CONFIRMED | |
| 40 | 第二批 6 筆 | skill-open、rdqu | `demo/extras/batch2/報名表_第二批.csv` 6 列 | — | CONFIRMED | |
| 41 | signup-check 介紹與六步；全檔 18 行 | skill-desc、skill-s1–s3b、jkeu、saer、c3st、yf8t、ra5q、mc6k、6pwj | 腳本比對 SKILL.md：第 1–5 行、第 7–18 行都相同，18 行 | — | CONFIRMED | |
| 42 | 兩種叫法的要求句 | skill-ask | `demo/prompts/skill-slash.txt`、`skill-auto.txt` | — | CONFIRMED | |
| 43 | k2 沒打斜線，第一個動作就是拿出 Skill | xxz6、skill-pick | runlog k2 第一個 tool_use `Skill {"skill":"signup-check","args":"報名表_第二批.csv"}`，與卡片相同 | — | CONFIRMED | |
| 44 | k1 打斜線，步驟沒寫的想改線上的那位也挑出來請你決定 | w8ig、skill-online | `demo/k1/reply.md` 第 16 行 | — | CONFIRMED | |
| 45 | d1：找不到確認信名單，改用寄信名單；新報名兩位、宋柏均只註記 | ev6t、daily-res | `demo/d1/reply.md`；runlog d1 NOTE | — | CONFIRMED | |
| 46 | t1 在規劃模式問；六步一段段講完，新的一步放在第五步之後 | eazv、y9ec、tutor-ask caption | runlog t1 mode=plan；`demo/t1/reply.md`「加在第 5 步後面，當新的第 6 步」 | — | CONFIRMED | |
| 47 | t1 的提醒 | 9u9t、tutor-caveat | 回覆原文：「你加句子時，最好把欄位名稱寫進去。這樣 Claude 才不會用猜的。」是寫進 SKILL.md 的那一句要帶欄位名，不是「問的時候告訴它」 | — | CHANGED | 「它也提醒：問的時候，連這件事寫在報名表哪個欄位，也一起告訴它。」→「它也提醒：加這一句時，寫明這件事在報名表的哪個欄位，它才不會用猜的。」 |
| 48 | 說明欄：「每張卡片的來源欄寫著是哪一次（例如「實跑 2026-10-21｜2.1.295｜p1」）」 | youtube.description | 沒有任何一張卡的來源欄是這個字串（p1 的是「實跑 2026-10-21｜p1｜輸出/處理日誌.md」）；引號裡的例子要是畫面上真的有的 | — | CHANGED | →「（例如「實跑 2026-10-21｜Claude Code 2.1.295｜a1 的回覆」）」（a1-quote 的來源欄原字串） |
| 49 | 說明欄「怎麼跑的」：19 次、1 次登入失敗、11／7；8、8、9；手動 6 個被拒；自動接受編輯改名一份、搬進封存兩份；g1；k1、k2 六項都過；d1 跑過 1 次 | youtube.description | runlog：n1 8/10、v1 8/10、s1 9/10；m1 `permission_denials=6`；a1 created／removed；k1、k2 B1–B6 PASS；d1 一次（19／11／7 第 3 輪已查） | — | CONFIRMED | |
| 50 | 說明欄「你會學到」各項（四步、@ 與 /、規劃→自動接受編輯、用量圈、/compact、/clear、十二行、十八行、兩種叫法、排程） | youtube.description | 同上第 1–22 項 | 200 | CONFIRMED | |
| 51 | 標題、縮圖、標籤 | youtube.title、thumbnail、tags | 沒有數字或可查的事實（「四個基本功」與 promise／closing 一致） | — | OUT OF SCOPE | |
| 52 | 其餘旁白（問句、轉場、建議：uva6、j47g、8rt7、734w、3dib、mgyy、w9hj、ff34、jpvj、eifj、8bck、azu6、x8va、q2v6、8bv6、7awm、gqpd、bf97、d7tu、k2hr、hygc、te2v、q8bt、8rzj、8wjx、htzr、yv7p、csgn、xkem、ziec、2n7n、wssz、6mi9、x6xg、mysq、kbvh、mwct、2vih、i9gw、cktr、euni、pmzn、fyda、7fdk、ca3e、xx3t、f59b、8v78、4g7t、7ktj、cik3、m8s5、xsvd、s9wj、h63y、59wc、ddfe） | 各行 | 沒有新的事實，或只是前面已查事實的回呼（htzr 回呼 g1、pmzn 對 daily.txt、csgn 對 vague.txt） | — | OUT OF SCOPE | |

## 「我」的句子

- dqu9：g1 實跑（第 24 項）。
- u22y：承認的不確定，今天兩頁都沒寫桌面版的起始模式（第 11 項）。
- dmw2：pr1 實跑（第 33 項）。
- 其餘含「我」的只在引號裡的要求句（zs3t、csgn）或片尾留言（CTA），不是第一人稱經驗。

## 摘要

- 這一輪查的主張：52 條（131 句旁白、所有卡片、說明欄）；c68、c69 官方頁原文都有，句子留著。
- 判定：CONFIRMED 49（含 1 條承認的不確定），CHANGED 3（ktbf、9u9t、說明欄的例子字串），NOT FOUND 0，OUT OF SCOPE 2 組。事實修正 3 處，video.json 與 claims.md（c22、c63、修訂 5 的說明、進度清單）都改了。
- 快要過期的事實：官方頁都沒有標日期，以 2026-10-21 抓到的為準。最容易變的是桌面版介面（提示框下那一排的順序、用量圈、`@`／`/` 選單、模式名稱，D 頁自己寫了舊版介面叫 Ask permissions 等名字）和 PM 的起始模式規則（PM 寫 v2.1.302 起 `claude -p` 沒設模式就從 Manual 開始；片子跑的是 2.1.295，旁白沒講這件事）。
- 觀點不一致：沒有新的。「新手容易踩的坑」、3sdm 的選擇規則、risk 卡的三條、8v78「建議留給你自己按」、fyda、check-how「這個頻道的做法」都是頻道建議，第 2 輪那 4 句「我會建議」要不要收進站主觀點仍等站主決定。
- 聽眾檢查（只回報）：超過 40 字的有 uqir 43、ce5d 42、jkeu 41、ktbf 原本 41（改後 40）；沒有查證式旁白、括號、網址；9u9t 改後 34 字。
- lint：`node tools/video/cli.mjs lint --slug claude-code-beginner-event-folder` 0 errors、0 warnings，估 13.8 分鐘、131 句。
- 懷疑但沒改：
  - r8fw「它一個檔案都沒動」：資料夾裡確實沒動，但 pl1 在資料夾外寫了 Claude Code 自己的計畫檔（`<home>/.claude/plans/`，runlog NOTE）。以觀眾的資料夾來說成立，沒動。
  - folder-scope 第 1 項「讀、寫、改名：都在這個資料夾」：讀資料夾外面的檔，有的模式會先問、有的不問（PM），這一項是簡化；第 2 項才有出處。沒動。
  - d7tu「這個對話已經裝進一整個資料夾的內容」：實跑是一個個分開的 session，這句是情境說法，不是量到的結果。
  - p1、k1、k2、d1 也各有被拒的指令（4、1、1、1 個），旁白沒說它們「不用問」，所以沒碰；觀眾在桌面版照做可能會看到幾次詢問，這件事只有說明欄的手動模式那一句提到。
  - 4f33「越精簡越好」只講了 MEM 那句的一半（specific and concise），卡片引文是全句。
  - 說明欄「travel_scanner 公開 repo」：沒有查 repo 是否公開，也沒有確認那個路徑上線後讀得到。
  - video.json 改了，若成片的收據（review.json 的 SHA256）綁著它，要重產旁白與收據。
- 需要再一輪：否。這一輪事實修正 3 處（規則是超過 3 處才要）。
- 結論：可以叫查核完成。修訂 5 的每一條主張都有判定，沒有懸而未決的事實；兩句被改的都是照實跑紀錄改正，`@` 與 `/` 兩條都有官方頁原文。未決的只有觀點要不要收進站主觀點，那是站主的決定。
