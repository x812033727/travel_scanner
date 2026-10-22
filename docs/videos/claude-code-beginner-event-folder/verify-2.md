# verify-2：claude-code-beginner-event-folder

查核日 2026-10-21，第 2 輪。查核者不是撰稿者，也不是第 1 輪的查核者。沒有跑 git。

範圍：第 1 輪改過的 7 條（#17、#25、#48、#51、#75、#83、#84）；第 1 輪確認過的 72 條裡隨機抽三分之一（24 條，用固定種子 20261021 洗牌後取前 24 條：#8、11、12、13、14、21、22、23、26、31、35、36、37、41、42、43、52、53、54、56、57、72、77、78）；第 1 輪留下沒解決的 5 個懷疑（dj2h、f86u、y9ec、snrs、Plan「只讀」）；以及沒標成觀點的旁白（u29s、cxbq、f59b、8v78）。編號沿用 verify-1.md 的主張表。

方法：重新把 `video.json` 抽成清單（`<work>/_tools/verifier2/dump.txt`）。實跑的主張逐字對 `runlog.txt` 與 `demo/`；引用卡的句子用腳本（`<work>/_tools/verifier2/q.js`）對 `demo/` 原檔比對，10 張全部 FOUND。官方頁今天重抓 `.md` 版（UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，每頁間隔 1.2 秒），存在 `<work>/_tools/verifier2/pages/`。web search 0／5。

官方頁（2026-10-21，全部 HTTP 200；頁面本身沒有更新日期）：

| 代號 | URL | HTTP |
| --- | --- | --- |
| DQ | https://code.claude.com/docs/en/desktop-quickstart.md | 200 |
| D | https://code.claude.com/docs/en/desktop.md | 200 |
| PM | https://code.claude.com/docs/en/permission-modes.md | 200 |
| SEC | https://code.claude.com/docs/en/security.md | 200 |
| ME | https://code.claude.com/docs/en/memory.md | 200 |
| CM | https://code.claude.com/docs/en/commands.md | 200 |
| CO | https://code.claude.com/docs/en/costs.md | 200 |
| SK | https://code.claude.com/docs/en/skills.md | 200 |
| MCP | https://code.claude.com/docs/en/mcp.md | 200 |
| ST | https://code.claude.com/docs/en/desktop-scheduled-tasks.md | 200 |
| OAI | https://developers.openai.com/codex（重新導向到 https://learn.chatgpt.com/docs） | 200 |

## 一、第 1 輪改過的 7 條

| # | 主張 | 位置 | 依據 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 17 | pr1 打開了資料夾裡 11 個檔，連兩張圖 | kgnr、folder-reads | RL R13：`Glob **/*` 之後 11 個 Read（含 活動海報_草稿.png、場地平面圖.png）；folder before 有 14 個檔，沒讀的是 報名表.csv、輸出/寄信名單.csv，CLAUDE.md 自動載入 | — | CONFIRMED（第 1 輪的修正對） | 旁白不動；claims.md c14 的「當時有 15 個檔」改成 14 個 |
| 25 | m1 六個動作要人同意，全被擋下，一個檔都沒動 | mvtb、perm-runs 第 2 列 | RL R9 `permission_denials=6`、init `permissionMode=default`、folder after 不變；回覆「核准前我沒有改動任何檔案」 | — | CONFIRMED | |
| 48 | md-g1 右欄「第 7 條：看內容對不對得上」 | md-g1 | demo/extras/claude-md-specific/CLAUDE.md：第七個條目在第 9–10 行；demo/g1/CLAUDE.md 第 3 條在第 5 行 | — | CONFIRMED | |
| 51 | 整理大綱的那四次都打開讀過，四次都選真的最終版 | 7kgt、m3-who | RL R8 pl1、R9 m1、R10 a1、R10b a2 都有三份大綱的 Read；a1、a2 VERDICT RIGHT；pl1、m1 的回覆都判斷真的最終版 | — | CONFIRMED | |
| 75 | 檔名對不上，它只能自己找替代的檔 | fyda | demo/d1/reply.md「`輸出/` 裡沒有 `確認信名單.csv`,我改用同資料夾的 `寄信名單.csv` 比對」 | — | CONFIRMED | |
| 83 | 說明欄：快照接續的 7 次 | youtube.description | RL 的 `from=`：k1、k2（p1）、pr1、pr3、d1（s1）、pr2（pr1）、t1（k1）共 7 次；其餘 12 次 from=seed，含登入失敗的 c1 | — | CHANGED（寫法） | 第 1 輪的句子前半說「每次都從同一份練習資料夾重建」、後半又說 7 次不是，前後矛盾 →「算進來的 18 次裡，11 次從同一份練習資料夾重建，7 次接著前一次跑完的資料夾。」claims.md 開頭同步 |
| 84 | 說明欄：哪些要求句完整上畫面 | youtube.description | demo/prompts：purpose、versions、daily、tutor、skill-slash、skill-auto、vague 都完整在卡上；progress、continue、write-claude-md、chat-purpose 只講大意；continue-cold（pr3）片中沒用 | — | CONFIRMED | |

## 二、抽查第 1 輪確認過的 24 條

| # | 主張 | 位置 | 依據 | HTTP | 判定 |
| --- | --- | --- | --- | --- | --- |
| 8 | 只拿到文字也排出 16 個能寄的人 | byk3 | demo/c2/reply.md 第 3 行「其中 16 人可以直接寄信」；RL R2「一、可直接寄確認信（16 人）」 | — | CONFIRMED |
| 11 | Chat 分頁不碰檔案；Code 分頁才有本機檔案存取 | which-tool、356m | DQ「General conversation with no file access」「direct access to your local files」 | 200 | CONFIRMED |
| 12 | OpenAI 那邊的同類工具叫 Codex | which-tool、4fh3 | OAI 頁面標「ChatGPT and Codex」的文件；功能沒有逐項比對 | 200 | CONFIRMED（只到產品存在與歸屬） |
| 13 | 環境選 Local → Open folder… → 打字按 Enter | folder-steps | DQ「select the top entry in the **Local** group」「select **Open folder…**」；D「Type what you want Claude to do and press **Enter** to send」 | 200 | CONFIRMED |
| 14 | 內建 Claude Code、不用另外安裝；Pro、Max、Team 或 Enterprise | folder-plan | DQ「don't need to install Node.js」「Pro, Max, Team, or Enterprise」 | 200 | CONFIRMED |
| 21 | 桌面版五個模式表 | perm-table | D 模式表第 91–95 行 | 200 | CONFIRMED，但 Plan 列見第三節 |
| 22 | 提示框下面那一排；依資料夾記住；Plan 只算這一次 | perm-default | D「mode selector in the row under the prompt box」「remembered per folder … except Plan」 | 200 | CONFIRMED |
| 23 | 桌面版一打開是哪一個，官方頁沒寫明 | u22y | PM 第 11 行只講終端機與 VS Code 的內建起始模式；PM 第 243–245 行、D 第 87 行只講 defaultMode 與記住的選擇 | 200 | CONFIRMED |
| 26 | a1 兩份進封存、一份改名，改名的是真的最終版 | kr3n | RL R10 VERDICT RIGHT | — | CONFIRMED |
| 31 | 先 Plan、讀計畫、再切 Accept edits | perm-rule | D「Start complex tasks in Plan」 | 200 | CONFIRMED |
| 35 | /clear 開新對話、專案記憶還在 | 62gk | CM「starts fresh on a new task while keeping project memory」 | 200 | CONFIRMED |
| 36 | 寫進度 → 新對話 → 先讀進度再寫信 | ctx-steps | demo/prompts/progress.txt、continue.txt；RL R13、R14 | — | CONFIRMED |
| 37 | 進度.md 第 16–24 行、全檔 37 行 | ctx-progress | demo/pr1/輸出/進度.md，`wc -l` 37，第 16–24 行與卡片逐字相同 | — | CONFIRMED |
| 41 | 只寫一句的那一份，全檔 3 行 | md-vague | demo/extras/claude-md-vague/CLAUDE.md 3 行 | — | CONFIRMED |
| 42 | 十項檢查節錄 5 項，跑之前寫好、從檔案判定 | md-checks | RL M2 selftest C1–C10 | — | CONFIRMED |
| 43 | 8、8、9 | md-runs | RL 第 732 行 n1 `score: 8/10`、第 1173 行 v1 `8/10`、第 1066 行 s1 `9/10` | — | CONFIRMED |
| 52 | a1 回覆第一句 | a1-quote | demo/a1/reply.md 第 1 行逐字 | — | CONFIRMED |
| 53 | vague.txt、purpose.txt 全文 | list-say、list-ask | demo/prompts 原檔，卡片只在標點後換行 | — | CONFIRMED |
| 54 | p1 依序四步、回覆說沒跑程式、建議看筆數 | list-steps | RL 第 795、801 行「我沒能跑 Python 腳本,是手動核對 24 列後直接寫入的。建議你開 CSV 看一下筆數。」 | — | CONFIRMED |
| 56 | 確認信草稿第 15–21 行、全檔 47 行 | letter | demo/pr2/輸出/確認信草稿.md，47 行，第 15–21 行逐字相同 | — | CONFIRMED |
| 57 | 「活動前一天（11/12）會再寄一封行前提醒。」 | letter-slip | 同檔第 34 行逐字 | — | CONFIRMED |
| 72 | 要讀你的檔就用桌面版排程 | 2kxy | ST 比較表「Access to local files｜No (fresh clone)｜Yes｜Yes」；「Use **Desktop tasks** when you need access to local files」 | 200 | CONFIRMED |
| 77 | t1 三句引用 | tutor-explain、tutor-quote、tutor-caveat | demo/t1/reply.md 三句逐字 FOUND | — | CONFIRMED（y9ec 見第三節） |
| 78 | 它讀得到也改得到一切；刪檔在自動接受範圍 | risk、xx3t | PM「auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`」 | 200 | CONFIRMED（事實部分；觀點見第四節） |

## 三、第 1 輪留下的懷疑：這一輪的判定

| # | 主張 | 位置 | 依據 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 27 | 計畫開頭先提醒 | dj2h、perm-plan kicker | demo/pl1/reply.md 第一段是「我還沒動任何檔案，計畫已寫好，請你確認。…」，粗體提醒在第二段；計畫檔 plan-file.md 的第一段是 Context | — | CHANGED | dj2h「計畫開頭就先提醒這件事：…」→「計畫裡的第一個提醒就是這件事：…」；kicker「規劃模式的計畫，開頭先提醒（pl1）」→「規劃模式的計畫，第一個提醒（pl1）」；claims c23 同步 |
| 6 | 每一份報名表裡都有一筆叫「測試」 | f86u | 這時片中只介紹了 報名表.csv（第 7 行「測試」）；第二批那筆叫「測試二」（報名表_第二批.csv 第 6 行）；「每一份報名表」是沒有依據的通則 | — | CHANGED | 「還有，每一份報名表裡，都有一筆叫「測試」。」→「還有，裡面混了一筆叫「測試」的資料。」；claims c5 註記 |
| 77b | t1 再給一句能直接貼進去的話 | y9ec | demo/t1/reply.md：給了新的第 6 步一段，加上把原本第 6 步改寫成第 7 步（「以及想改線上的有幾位」）一段，共兩段 | — | CHANGED | 「…一段一段用白話解釋完，再給一句能直接貼進去的話。」→「它把介紹和六個步驟一段段用白話講完，再寫好新的一步，連順延的那一步也改好。」；claims c63 同步 |
| 18 | 新手最常踩的坑：打開桌面，連私人的檔它也讀得到 | snrs、folder-trap | 沒有實跑；「最常」沒有任何來源。官方頁的規則：PM「Claude still runs actions that need no approval in Manual mode, such as file reads inside your working directories」；SEC「asks you before its file tools read or write outside the folder where it was started and its subfolders」 | 200 | CHANGED | 旁白 →「新手容易踩的坑，是直接打開桌面或整個文件夾：裡面連私人的檔，它讀都不用問你。」；kicker「新手最常踩的坑」→「新手容易踩的坑」；text「打開整個桌面／它就**全都讀得到**」→「打開整個桌面／裡面的檔**讀了不用問**」；場景加 claims ["c67"]，claims.md 新增 c67 |
| 21b | Plan「只讀、只提計畫」 | perm-table Plan 列、ema8 | D 模式表「Claude reads files and runs commands to explore, then proposes a plan without editing your source code」；PM「Claude reads files, runs shell commands to explore, and writes a plan」；pl1 也真的跑了 PowerShell 與 Bash 的查看指令 | 200 | CHANGED | 表格「只讀、只提計畫，核准前不改檔」→「讀檔、跑查看的指令，只提計畫，核准前不改檔」；ema8「規劃模式只讀、只提計畫，你核准之前，它不改檔。」→「規劃模式會讀檔、跑查看用的指令，只提計畫，你核准之前不改檔。」；claims c17 同步 |

## 四、觀點標示

| 位置 | 原句 | 判定 | 改後 |
| --- | --- | --- | --- |
| u29s（trust 第 1 項） | 別人給的 Skill，先打開讀每一步，像剛剛那份一樣。 | 觀點，旁白沒標；不在站主觀點四點裡 | 我會建議，別人給的 Skill 先打開讀每一步，像剛剛那份一樣。 |
| cxbq（trust 第 2 項） | 連接器只接你真的會用的那幾個。 | 同上 | 連接器，我會建議只接你真的會用的那幾個。 |
| f59b（risk 第 1、2 項） | 只打開那件事的資料夾，原始檔先另外留一份。 | 同上（第 3 點只有「原始檔只讀不改」） | 我會建議，只打開那件事的資料夾，原始檔先另外留一份。 |
| 8v78（risk 第 3 項） | 寄信、刪檔這種收不回的事，留給你自己按。 | 同上 | 寄信、刪檔這種收不回的事，我會建議留給你自己按。 |

卡片（trust 的 source「第 1、2 項：頻道建議」、risk 的 source「其餘：頻道建議」）原本就標了，沒改。這四條建議仍然不在 brief 站主觀點的四點裡（而且那四點本身標著「提案，待站主確認」）：旁白現在標成觀點，跟事實分開了，但要不要把它們收進站主觀點，由站主決定。md-rule（3qqw）與 check-how（iexi）標「這個頻道的建議／做法」，和第 4、3 點一致，沒動。

## 摘要

- 這一輪查的主張：36 條（第 1 輪改過的 7 條、抽查 24 條、懷疑 5 條），另外 4 句觀點標示。
- 判定：CONFIRMED 30，CHANGED 6，NOT FOUND 0。
- 事實修正 6 處：dj2h＋perm-plan kicker（「開頭」→「第一個提醒」）、f86u（拿掉「每一份報名表」）、y9ec（「一句」→新的一步加順延的那一步）、snrs＋folder-trap 卡（拿掉「最常」，改成官方頁的範圍規則：打開的資料夾裡讀檔不用問）、perm-table Plan 列＋ema8（「只讀」→「讀檔、跑查看的指令」）、說明欄（「每次都…重建，接續的 7 次…」→ 18 次裡 11＋7）。claims.md 的開頭、c5、c14（檔數 15 → 14）、c17、c23、c56、c63、c64 同步，新增 c67，進度清單加第 2、3 輪。沒有一句有 `say`，`say_for` 不用設；`sources` 的 `checked_on` 已是 2026-10-21。c67 另引的 security 頁沒有加進 `sources`（主要依據 permission-modes 已在裡面）。
- 觀點標示 4 句：u29s、cxbq、f59b、8v78 加上「我會建議」。
- 快要過期的事實（官方頁都沒有標日期，以 2026-10-21 抓到的為準）：方案名單（Pro、Max、Team、Enterprise）；Auto 模式「有開放才出現」；「提示框下面那一排」是新版面（DQ 自己寫了舊版面的分支）；PM 第 11 行「v2.1.283 起終端機與 VS Code 預設從 auto 開始」，桌面版仍沒寫明（u22y 照舊成立）；排程比較表的最短間隔。
- 觀點不一致：u29s、cxbq、f59b、8v78 的建議不在 brief 站主觀點的四點裡（已標成觀點，沒有改寫內容），由站主決定要不要收進站主觀點或刪掉。
- 聽眾檢查（只回報）：改過的句子都在 40 字以內（最長 snrs 38 字）。第 1 輪報的超過 40 字三句（vdqi、y9bk、dkmu）還在，沒動。旁白沒有「經查證」「根據官方文件」「本影片」、括號或網址。
- lint：修改後 `node tools/video/cli.mjs lint --slug claude-code-beginner-event-folder` 0 errors、0 warnings，估 21.7 分鐘、220 句。
- 懷疑但沒改：
  - Codex 只查到 OpenAI 的文件把它列為產品，「同類工具」沒有逐項比對（沿用第 1 輪）。
  - xx3t「它讀得到、也改得到資料夾裡的一切」：PM 說寫入受保護路徑（如 `.claude/settings.json`）仍會先問；「改得到」指有能力、不是不問就改，聽起來可以接受，沒動。
  - 「新手容易踩的坑」仍是頻道的說法，沒有統計；拿掉了「最常」這個比較級。
  - runlog R13 runner NOTE「all the text files」不對（第 1 輪已記；runlog 不在可改範圍）。
  - 長度 21.7 分鐘超過 12–16 分鐘的目標（撰稿者已列）。
- 需要再一輪：是。這一輪事實修正 6 處，超過 3 處；下一輪重查第三節的 6 處修正即可。
- 這份稿還不能叫查核完成：所有主張都有判定、沒有懸而未決的事實，但照規則這一輪的修正要再查一次，觀點那 4 句也還在等站主確認。
