# verify-1：claude-md-house-rules（獨立查核，第 1 輪，2026-10-21）

查核者不是撰稿者。方法照 `verifier-video.md`：先把 `video.json` 的每一個字串抽成編號清單（304 條，`<work>/_tools/verify-1/claims-list.md`），再逐條對官方頁與執行紀錄。

- 官方頁五頁 2026-10-21 UTC 14:40 用編輯部 User-Agent 重抓，原檔在 `<work>/_tools/verify-1/pages/`，全部 HTTP 200：memory（813,517 bytes）、skills（1,237,026）、permission-modes（951,126）、desktop-quickstart（463,892）、support.claude.com Projects（238,563）。句子比對用 `pagecheck.py`（去 `<!-- -->`、script、style 與標籤後找原句）。
- 執行紀錄：這支片的 `runlog.txt`（N0、N1、N2）與 `demo/N1/`、`demo/N2/`；沿用的 `docs/videos/claude-code-beginner-event-folder/runlog.txt`（M3、R3 n1、R5 g1、R6 s1、R7 v1、R10 a1、R10b a2）與它的 `demo/`。逐字比對用 `bytecheck.py`（57 項全部 OK；`terminal` 卡的 `output` 陣列照 `templates/terminal/terminal.mjs` 的讀法以換行相接）。
- 教學規則（lint 不查的）與 `paper.json` 用 `rulecheck.py`。
- 沒有用到網路搜尋（0 次）。

## 主張表

編號｜主張｜位置｜來源（URL 或紀錄）｜HTTP｜判定｜改前 → 改後

1｜標題「CLAUDE.md 是什麼、怎麼寫？不用寫程式，八條規矩寫一次，之後只說八個字」：八條、八個字（幫我整理報名名單）、一個問號｜youtube.title｜`claude-md-specific/CLAUDE.md`（8 條）；`prompts/vague.txt`（8 字＋句號）｜—｜CONFIRMED｜—
2｜說明欄：八條（十二行）、200 行以內、報名表 24 列、三份「最終版」、N1／N2 在 2026-10-21 用 2.1.295 的 `claude -p`、帳號預設模型、其餘沿用 g1／a1／a2／n1／v1／s1／M3 同一天同一版本、兩個範本沒有跑過、Memory files 清單沒看過、那句要求全文｜youtube.description｜`runlog.txt` N0–N2 與 Session transcripts（claude-opus-5-5）；上一支 runlog 的 Date 行（2026-10-21 台北）；memory 頁；`prompts/write-claude-md.txt`｜200｜CONFIRMED｜—（「同一天」是台北日期：上一支 UTC 2026-10-20 23:51–2026-10-21 00:05 ＝ 台北 10-21）
3｜tags 十個｜youtube.tags｜—｜—｜OUT OF SCOPE｜—
4｜縮圖：tag「CLAUDE.md 教學」、headline「就是／員工守則」、sub「寫一次，之後只說八個字」、capture `md-page`｜thumbnail.data｜`md-page` 是 screencast 場景｜—｜CONFIRMED｜—
5｜sources 五條 `checked_on: 2026-10-21`｜sources[0–4]｜五頁今天都 200｜200｜CONFIRMED｜—
6｜c1 觀眾每次重講的三句（原始檔別動、放 輸出/、同名不一定同一人）｜open、again｜觀眾的話；n1／N1 沒有守則的結果｜—｜OUT OF SCOPE（設定句）｜—
7｜c2 它寫的第 3 條原文「3. 簡報大綱有多個「最終版」時，以檔案修改時間最新的為準，並在整理時告訴我你採用哪一份；不要自行合併內容。」；caption「第 3 條｜全檔 8 行的第 5 行」｜g1-rule.data.code、caption｜`demo/g1/CLAUDE.md` 第 5 行（全檔 8 行）；上一支 runlog R5 `tool_use Write`｜—｜CONFIRMED（逐字）｜—
8｜c2「它第三條就寫錯了」「以修改時間最新的為準」｜mutx、esq9｜同上；M3：修改時間最新的是 這次絕對最終版，內容 16:00、講者待確認｜—｜CONFIRMED｜—
9｜c3 它只跑了一次 `ls -la`、一個檔都沒打開就寫了｜pznu、draft-check.caption｜上一支 runlog R5 stream summary：工具呼叫只有 `Bash ls -la` 與 `Write`；NOTE「read no file before writing」｜—｜CONFIRMED｜—
10｜c4 它會直接動你的檔案｜zfu6、stakes｜desktop-quickstart「Code: An interactive coding assistant with direct access to your local files」；permission-modes acceptEdits 一節｜200｜CONFIRMED｜—
11｜c5 純文字檔、放在你打開的那個資料夾最上層、記事本打得開、上一層的資料夾也讀得到｜door、kuw7、fx5x、h59b｜memory「You write these files in plain text」「./CLAUDE.md or ./.claude/CLAUDE.md」「CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand」｜200｜CONFIRMED｜—
12｜c6 每次新對話開始就載入，不用你提；每一次新對話都重新讀一遍｜morning、5nwa、643b、day-one、jegb、projects 右欄｜memory「Both are loaded at the start of every conversation」「Claude reads them at the start of every session」｜200｜CONFIRMED｜—
13｜c7 守則每天讀、手冊用到才翻；一直重貼的整套步驟做成 Skill｜booklet、ydzd、answer、jnve｜skills「Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's body loads only when it's used」｜200｜CONFIRMED｜—
14｜c8 網頁版專案指示：專案裡每一場對話都用它｜projects 左欄點 1、7cwc｜Projects 說明頁「Claude will use these instructions for all the chats within the project」｜200｜CONFIRMED｜—
15｜c8 它寫不回你電腦裡的資料夾｜projects 左欄點 2、7cwc｜推論：Projects 頁只講上傳與對話，全頁沒有 local／folder／file access 字樣；desktop-quickstart「Chat: General conversation with no file access, similar to claude.ai」｜200｜CONFIRMED（推論，卡片 source 標兩頁）｜source「Projects 說明頁｜Claude Code memory 頁｜2026-10-21」→「Projects｜memory｜desktop-quickstart 頁｜2026-10-21」（補上撐左欄的那一頁；48 字上限）
16｜c9 換一件事（整理三份最終版）：沒有守則的那次沒有日誌；有守則的那次多了 `輸出/處理日誌.md`，寫「看內容，不看檔名與修改時間」；source「實跑 2026-10-21｜2.1.295（a1、a2）」｜every-job、2ii2、zp3c｜上一支 runlog R10 a1「C8 FAIL 有處理日誌 | (none)」、R10b a2「C8 PASS 輸出/處理日誌.md」；`demo/a2/輸出/處理日誌.md`「判斷依據（看內容，不看檔名與修改時間）」；a1 2026-10-21T00:02Z、a2 00:03Z｜—｜CONFIRMED｜—
17｜c10 screencast：memory 頁「Set up a project CLAUDE.md」一段，錨點 `#set-up-a-project-claude-md`｜md-page.data.steps、caption｜今天的 HTML 有該 id；該段文字含「./CLAUDE.md or ./.claude/CLAUDE.md」「run /context … Memory files」｜200｜CONFIRMED｜—（caption 的「2026-10-21 擷取」是 screencast 卡唯一的出處欄位，screencast 的 data 只有 title／caption／steps，沒有 `source`；視為出處標示，不是來源戳上正文）
18｜c11 觀眾的 CLAUDE.md 全文十二行、八條，三張 code 卡逐字；caption「全文十二行」｜all-rules、write-file、your-line、folder、closing｜`demo/extras/claude-md-specific/CLAUDE.md`（12 行、sha256 8e865483370aa2d4…）；`runlog.txt` N0 `cat CLAUDE.md`｜—｜CONFIRMED（逐字，含兩條折行）｜—
19｜c11 八張 rule 卡的 text ＝ 檔內第 1–8 條（換行取代空白）｜rule-01…rule-08.data.text｜同上｜—｜CONFIRMED｜—
20｜c12 01：沒有這條它也沒動原始檔｜rule-01.sub、ap8n｜n1、v1、s1 的 C1 PASS；N1、N2 前後 `sha256sum 報名表.csv` 四次都是 835aff4e…｜—｜CONFIRMED｜—
21｜c13 02：沒有這條，新檔案落在最上層｜rule-02.sub、yfin｜n1、v1 `./報名名單_整理後.csv` 在根目錄；N1 `ls` 多一個根目錄檔、沒有 輸出/｜—｜CONFIRMED｜—
22｜c14 03：報名表裡兩個王志明，Email 和部門都不一樣｜rule-03.sub、5a3x｜seed 報名表 第 2、8 列：chihming.wang／業務部、cm.wang／研發部｜—｜CONFIRMED｜—
23｜c15 04：有人填了兩次，第二次的 Email 只差大小寫和一個空白｜rule-04.sub、zzdb｜seed 第 1、10 列：`yijun.chen@example.com` 與 ` YiJun.Chen@example.com`｜—｜CONFIRMED｜—
24｜c16 05：備註取消的、測試資料｜rule-05、mima｜seed 第 15 列「不能去了，請幫我取消」、第 6 列 姓名「測試」｜—｜CONFIRMED｜—
25｜c16「每一份報名表裡都有一筆叫測試，對吧？」｜rule-05.sub、55ru｜共同經驗的玩笑｜—｜OUT OF SCOPE｜—
26｜c17 06：有一筆少了結尾；補上就寄到不存在的地方｜rule-06.sub、2utv｜seed 第 17 列 `zihching.hung@example`；N1、N2 都說少了 `.com`｜—｜CONFIRMED（後半是假設句）｜—
27｜c18 07：哪一版最新看內容；不看修改時間｜rule-07、u7a9｜M3；a2 日誌｜—｜CONFIRMED｜—
28｜c19 08：沒有這條它做完就走｜rule-08.sub、u2ai｜n1、v1 C8 FAIL；N1 Verdicts「wrote NO log」｜—｜CONFIRMED｜—
29｜c20 表格：最終版 16:00、真的最終版 16:30、這次絕對最終版 16:00；highlight 第 3 列（修改時間最新的）；source「ls -lt 與 grep，2026-10-21（M3）」｜versions.data｜上一支 runlog M3 `grep -n "時間\|講者"` 三行；`ls -lt` 最上面是 這次絕對最終版 2026-10-20 08:45（台北）；M3 跑在 2026-10-20T18:04Z ＝ 台北 10-21 02:04｜—｜CONFIRMED｜—
30｜c20「修改時間最新的這一份，內容還是舊的」「對得上活動說明的只有真的最終版，兩位講者都已確認」｜puy4、kc5x｜同上：只有 真的最終版 寫「周以安、范可甯（皆已確認）」、16:30｜—｜CONFIRMED｜—
31｜「我自己這一份只有八條，最長的一條兩行」｜fzrx｜檔案 8 條，第 7、8 條各折一行｜—｜CONFIRMED｜—
32｜c21 引句「The more specific and concise your instructions, the more consistently Claude follows them.」、譯文｜concise.data.quote、kfgk｜memory「CLAUDE.md vs auto memory」一節，逐字｜200｜CONFIRMED｜—
33｜c22 一份 200 行以內；再長照做的程度下降｜two-hundred（numeral 200）、dbw8｜memory「Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence.」｜200｜CONFIRMED｜—（頁面寫 target，卡片 kicker「建議上限」對；旁白「上限是一份兩百行以內」少了「建議」，意思在「以內」，沒改）
34｜c23 模糊版只有一句「名單要整理乾淨。」｜one-line 左欄、wxnh｜`demo/extras/claude-md-vague/CLAUDE.md`（3 行，sha256 4195c05a…）｜—｜CONFIRMED｜—
35｜c24 只寫一句跟沒寫一樣：同一個檔名、同樣兩個漏洞；兩欄三點相同｜one-line 兩欄、verdict、w2f5｜上一支 runlog R3 n1 8/10、R7 v1 8/10：同一個根目錄 `報名名單_整理後.csv`，同樣 C7 FAIL（缺資料的人在名單裡）、C8 FAIL（沒有日誌）；NOTE「the same two fails」｜—｜CONFIRMED｜—
36｜「寫到第幾條它開始不照做，我沒有量到；查到的只有那個上限」｜z8an｜不確定句（企劃「我」的句子表）；memory 頁只給 200 行｜200｜CONFIRMED（不確定句）｜—
37｜c25 站主觀點 1：每次都要講的寫進守則、用到才翻的做成手冊｜jnve「以我的用法」、answer、closing.lines[0]｜brief 站主觀點 1（提案，站主未改寫）｜—｜CONFIRMED（有標成看法）｜—
38｜c25 站主觀點 2：規矩要寫到看得出做對沒；「名單要整理乾淨」不寫、「寄不出去的另外列一張表」才寫｜mxa4「我的看法是」、nv4d、verifiable、closing.lines[1]｜brief 站主觀點 2｜—｜CONFIRMED（有標成看法）｜—
39｜c25 站主觀點 3：它生的草稿逐條對著資料夾看過才留｜ptsz「我的看法是」、draft-check｜brief 站主觀點 3｜—｜CONFIRMED（有標成看法）｜—
40｜c26 報名名單：沒有守則時每次要講的三行；有了只說「幫我整理報名名單」；source「實跑 2026-10-21｜2.1.295（s1）」｜life-signup、zexi、8vmx｜上一支 runlog R6 s1（2026-10-20T23:56Z ＝ 台北 10-21 07:56）：`輸出/` 四個檔；`runlog.txt` N2｜—｜CONFIRMED｜—
41｜c27 週報、照片兩份守則：範本，沒有跑過；旁白「可以這樣寫」｜life-weekly*、life-photos*（source「寫法範本，沒有跑過」）｜—｜—｜OUT OF SCOPE（沒有宣稱結果）｜—
42｜c28 `ls`：七個檔，沒有 CLAUDE.md；ran_on 2026-10-21｜ls-before.data、x3n8｜`runlog.txt` N0 `(cd "$W/n" && ls)`、Terminal cards Card 1：7 行逐字｜—｜CONFIRMED（逐字）｜—
43｜c29 沒有守則：指令 `claude -p --permission-mode acceptEdits "幫我整理報名名單。"`；回覆前三個畫面行逐字；tool_version 2.1.295｜run-without.data｜`runlog.txt` N1、Card 2；`demo/N1/reply.md` 開頭｜—｜CONFIRMED（逐字；節錄裡沒有 Email）｜—
44｜c29「存成一個新檔案，直接丟在最上層」「寄不出去的人還留在名單裡，也沒有任何日誌」｜267s、egmm｜N1 `ls`（根目錄 `報名名單_整理後.csv`、沒有 輸出/）；`demo/N1/報名名單_整理後.csv` 第 7、13、15 列（劉思妤、洪子晴、曾詩涵）在名單裡；Verdicts「wrote NO log」｜—｜CONFIRMED｜—
45｜c30 有守則：同一指令；回覆前兩個畫面行＋「處理方式」前三條逐字（含 80 欄折行）｜run-with.data｜`runlog.txt` N2、Card 4（折行處「另外 4 」「不放進名單／。」相同）｜—｜CONFIRMED（逐字）｜—
46｜c30「四個檔案都在輸出資料夾，報名表和活動說明只有讀，沒有改」「取消的、測試的、填兩次的，一條一條照守則處理」｜wdxh、7ft6｜N2 回覆第 1 行與「處理方式」前三條｜—｜CONFIRMED｜—
47｜c30 `ls 輸出`：寄信名單.csv、處理日誌.md、要補資料.csv、飲食需求彙整.md｜ls-output.data、3if7｜`runlog.txt` N2 `ls 輸出`、Card 5 逐字｜—｜CONFIRMED（逐字）｜3if7「寄信名單、要補資料、飲食需求，還有處理日誌，四個檔案。」→「寄信名單、要補資料、飲食需求，還有處理日誌。」（規則修正，不是事實：wdxh 已唸過「四個檔案」，同一次執行的事實只講一次、每章唸出的數字最多兩個）
48｜c31 日誌「做了什麼」第 4 項「4. 沒有 Email 或 Email 格式不對的，原樣列進要補資料，不猜。」；source「實跑 2026-10-21｜2.1.295（N2）」｜log-check.data、maxm｜`demo/N2/輸出/處理日誌.md` 做了什麼 第 4 行；`runlog.txt` N2 `cat 輸出/處理日誌.md` 相同｜—｜CONFIRMED（逐字）｜—
49｜c32 `/context`、Memory files 底下有 CLAUDE.md｜context-check.data、6wwg、uhk9｜memory「To confirm the file loaded, run /context in a session and check the list under Memory files」｜200｜CONFIRMED｜—
50｜c39「桌面版裡那個清單長怎樣，我沒看過」｜tmnc｜`runlog.txt`：兩次都是 `claude -p`，沒有畫面｜—｜CONFIRMED（不確定句）｜—
51｜c33 三個泡泡＝那句要求全文｜ask-draft.data.messages｜`demo/prompts/write-claude-md.txt`；上一支 runlog R5 `## prompt`｜—｜CONFIRMED（逐字）｜—
52｜c34 它寫的六條逐字、highlight 第 3 行、caption「全檔 8 行的第 3 到 8 行」｜draft-check.data｜`demo/g1/CLAUDE.md` 第 3–8 行｜—｜CONFIRMED（逐字）｜—
53｜c35 練習：換掉第 3 條（highlight 第 5 行＝同名不一定同一人）；例子「同一個員工編號才是同一人」；改完同一句再跑、看 處理日誌.md；沒有跑｜your-line.data、qzm5、nbxz｜檔案第 5 行；caption 不宣稱結果｜—｜CONFIRMED（練習，沒有結果宣稱）｜—
54｜c36 守則不是鎖：它是脈絡不是強制設定；要硬擋一個動作是另一種東西｜not-a-lock、mkpc、f5vr｜memory「Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead」｜200｜CONFIRMED｜—
55｜c37 自動接受編輯模式下，搬檔、刪檔它不會問你；source permission-modes 頁｜safety.items[0]、pj7u｜permission-modes「acceptEdits mode auto-approves common filesystem Bash commands: mkdir, touch, rm, rmdir, mv, cp, and sed … applies only to paths inside your working directory」；模式表「acceptEdits: Reads, file edits, and common filesystem commands (mkdir, touch, mv, cp, etc.)」｜200｜CONFIRMED｜—（同頁另寫 rm／rmdir 刪到 critical path、工作資料夾外的路徑仍會問；旁白講的是資料夾內的一般搬檔刪檔，沒改）
56｜c38 原始檔先留副本、做完對日誌（做法建議）｜safety.items[1–2]、pz5n、z3e2｜守則第 8 條；N2 日誌「24 筆的去向」「修正過的欄位」｜—｜OUT OF SCOPE（建議，有依據）｜—
57｜「八條、十二行，之後只說八個字」｜juqf、closing.title｜檔案 8 條 12 行；8 字｜—｜CONFIRMED｜—
58｜sources[4] 標題「Chat has no file access; Code opens your folder」｜sources｜desktop-quickstart 三個分頁的句子｜200｜CONFIRMED｜—

## 教學規則（lint 不查的）與 paper.json

- 執行代號、來源戳：所有 title／kicker／item／caption／旁白都沒有 N1、N2、g1、a1、M3 等代號，也沒有「實跑」「2.1.295」；代號與版本只在 `source`、`ran_on`、`tool_version`。唯一帶日期的正文是 `md-page` 的 caption「…｜2026-10-21 擷取」，screencast 卡沒有 `source` 欄，caption 是它的出處欄（見第 17 條）。
- 「跟沒寫一樣」一族：旁白只有 w2f5 一句（卡片 verdict「只寫一句，跟沒寫一樣」不是旁白）。
- 每章唸出的數字（`rulecheck.py` 列出候選，人工判讀；「一次」「一份」「一條」這類量詞與序數不算）：第 0 章 0（八條、八個字是承諾句的字眼）；第 1 章 1（三份最終版）；第 2 章 3（兩個王志明、兩位講者、「最長的一條兩行」）＋承諾句的「八條」；第 3 章 2（兩百行、兩個漏洞）＋觀眾的假設「三十條」；第 4 章 0（「三句」是指卡上的三行）；第 5 章改後 2（七個檔案、四個檔案）＋承諾句的「八個字」「八條」；第 6 章 0；第 7 章承諾句的八條、十二行、八個字。第 2 章超過兩個，但三個數字各接一個觀眾看得到的事實（兩個王志明在表上、兩位講者是「對得上活動說明」的根據、兩行是「我」的句子），沒有改；列給撰稿決定。
- 標題那句話：hnjp「CLAUDE.md 就是員工守則：寫一次，之後只說八個字」估計 5.6–10.9 秒（`timeline.mjs`，`estimateTimeline`），15 秒內。
- 旁白不講這支片的製作：沒有「這支片」「紀錄」「跑過」「實跑」「查證」；「我試過只寫一句」「我沒有量到」「我沒看過」是企劃允許的「我」的句子。
- `paper.json`：46 個場景的 id 都在 `video.json`；每個場景 `keys` 數 ＝ 1 ＋ reveals（77 句）；最長 key 21 字（ask-draft），沒有超過 24；`numeral` 只在 rule-01…rule-08（01…08）與 two-hundred（200）；`typing: "human"` 在四張 terminal 卡。3if7 改句後 ls-output 的第二句 key「名單、要補資料、處理日誌」仍對得上。
- 最長狀態（估計）：versions 第 2 個狀態 13.6 秒、not-a-lock 13.4 秒、closing 13 秒，都在 15 秒內（QA 以實際時間軸為準）。

## 摘要

- 主張：58 條（對應撰稿 c1–c39 與標題、說明欄、縮圖、sources）；CONFIRMED 51、CHANGED 0（事實）、NOT FOUND 0、OUT OF SCOPE 7（c1、c16 的玩笑、c27 兩個範本、c38 建議、tags）。
- 非事實的修正 2 處：ls-output/3if7 去掉重複的「四個檔案」；projects 的 `source` 補上 desktop-quickstart 頁（48 字限制內改寫）。`claims.md` 末尾加了查核註記。
- 會過期的事實與今天看到的日期：memory 頁（200 行、/context、脈絡不是鎖、每次對話載入、越具體越簡潔）、skills 頁（Skill 內文用到才載入）、permission-modes 頁（acceptEdits 自動通過 mkdir/touch/rm/rmdir/mv/cp/sed）、desktop-quickstart（Chat 無檔案存取）、Projects 說明頁（專案指示用於專案內每一場對話）：全部 2026-10-21 UTC 14:40 看到；Claude Code 版本 2.1.295 是 2026-10-21 的 `claude --version`。
- 站主觀點：三點都標成「我的看法／以我的用法」，與 `brief.md` 站主觀點 1–3 一致；brief 註明這三點是提案、站主未改寫，站主選大綱時要確認。
- 聽稿：沒有超過 40 字的句子（最長 38，winq）；沒有括號、網址；沒有「經查證」「根據官方文件」「本影片」；拉丁字只有 CLAUDE.md、Skill、Email（lint 0 錯誤，都在字典）；揭示都在介紹該項的那一句（逐場看過 again、projects、every-job、versions、concise、one-line、life-*、ls-before、run-without、run-with、ls-output、context-check、ask-draft、safety）。
- lint：`node tools/video/cli.mjs lint --slug claude-md-house-rules` → 0 errors, 0 warnings；估計 8.5 分鐘、95 句、1,859 口語單位。
- 懷疑但沒改：dbw8「上限是一份兩百行以內」（頁面是 target，建議值）；pj7u 沒提 critical path 與工作資料夾外仍會問；第 2 章唸出三個數字；N2 的回覆節錄把第一行在 80 欄折成兩行寫進 `output`，render 若用別的欄寬會再折一次（Card 4 的折法是紀錄的，不是錯）；c8 的「寫不回你電腦裡的資料夾」是兩頁的推論，沒有一句官方原文。
- 第二輪：不需要（事實變更 0，少於三處）。
