# claims：claude-md-house-rules

撰稿 2026-10-21。每一行：編號｜主張（旁白或卡片上的說法）｜依據（官方頁網址，或執行紀錄的項目與 `demo/` 的檔）｜查證日｜用到的場景。

執行紀錄的共同條件：
- 這支片自己的 `runlog.txt`：N0、N1、N2，2026-10-21 UTC 14:03–14:06，Windows 11 Home 10.0.26200、Git Bash（MINGW64）、Claude Code 2.1.295，不開畫面的 `claude -p --permission-mode acceptEdits`，帳號預設模型（session 紀錄寫 claude-opus-5-5），`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`。畫面上的指令與輸出逐字取自它的「Terminal cards」一節；回覆全文與產出的檔在 `demo/N1/`、`demo/N2/`。
- 沿用 `docs/videos/claude-code-beginner-event-folder/runlog.txt`（同一台機器、同一版本 2.1.295、`--model sonnet`、`session.sh`，2026-10-20T23:51Z–2026-10-21T00:05Z UTC）：M3、g1、n1、v1、s1、a1、a2；產出的檔在那個資料夾的 `demo/`。旁白裡的「我」句子來源一律是這兩份紀錄、企劃的站主觀點，或照實說不確定。
- 官方頁三頁（memory、skills、permission-modes）企劃日 UTC 13:53–13:56 抓的原檔在 `<work>/_tools/pages/`；撰稿時 2026-10-21 UTC 14:16–14:20 再抓一次（`<work>/_tools/writer/*-today.html`、`projects.html`、`desktop-quickstart.html`，全部 HTTP 200），引用的句子在今天的頁面上都還在。
- 模型：N1、N2 是帳號預設模型，不是 sonnet；旁白沒有提任何模型名。

## 輸入、動作、預期、實際、證據（依企劃的示範紀錄）

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際（紀錄） | 證據 |
| --- | --- | --- | --- | --- | --- |
| 成果 1 | 種子資料夾＋12 行 CLAUDE.md，「幫我整理報名名單。」 | N2（有守則）對 N1（沒有守則） | N2 有 `輸出/處理日誌.md`、N1 沒有 | N2：`輸出/` 四個檔（寄信名單 16 人、要補資料 4 筆、飲食需求彙整、處理日誌），原檔雜湊不變；N1：根目錄一個 `報名名單_整理後.csv`、沒有 `輸出/`、沒有日誌、原檔雜湊不變 | `runlog.txt` N1、N2、Verdicts；`demo/N1/`、`demo/N2/輸出/` |
| 成果 2 | 同一句，模糊版 CLAUDE.md（「- 名單要整理乾淨。」） | v1 對 n1 對 s1 | v1 跟 n1 一樣 | v1、n1 都是根目錄 `報名名單_整理後.csv`、同樣兩項沒做到（C7 缺資料的人在名單裡、C8 沒有日誌）；s1 有 `輸出/` 與日誌 | 上一支 runlog R3、R6、R7 |
| 成果 3 | 「幫我替這個資料夾寫一份 CLAUDE.md…六條以內。寫完不要做其他事。」 | g1（不重跑） | 寫出六條以內 | 一次 `ls -la`、沒有 Read，寫了 6 條；第 3 條「以檔案修改時間最新的為準」；這個資料夾修改時間最新的是舊稿（M3） | 上一支 runlog R5、M3；`demo/g1/CLAUDE.md` |
| 差別一 | versions.txt（整理三份最終版） | a1（沒有 CLAUDE.md）對 a2（有） | 有守則的多一份日誌 | 兩次都選對（真的最終版）；只有 a2 多了 `輸出/處理日誌.md`，裡面寫「判斷依據（看內容，不看檔名與修改時間）」 | 上一支 runlog R10、R10b；`demo/a2/輸出/處理日誌.md` |
| 看一眼資料夾 | 種子資料夾，不呼叫模型 | `ls -lt`、`grep` | 最上面是這次絕對最終版 | 同左：這次絕對最終版 2026-10-20，內容 16:00、講者待確認；只有真的最終版 16:30、皆已確認 | 上一支 runlog M3 |
| 練習 | 改第 3 條（同名的判斷）後同一句再跑 | 沒有跑 | — | 卡片只給核對方法（看 處理日誌.md），不宣稱結果 | your-line 的 caption |
| 週報、照片 | 守則寫法範本 | 沒有跑 | — | 卡片 `source` 標「寫法範本，沒有跑過」；旁白只寫「可以這樣寫」，不宣稱結果 | life-weekly*、life-photos* |

桌面 app 裡 `/context` 的 Memory files 清單這台機器沒登入、沒看過：全部是官方頁的引用（CITED），卡片標「引用」，旁白照實說沒看過。

## 主張

c1｜觀眾每開一次新對話都重講的那段規矩：原始檔別動、整理好的放 輸出/、同名不一定同一人（觀眾自己的話，不是執行紀錄）｜企劃「觀眾」一節；n1／N1 沒有 CLAUDE.md 時的結果就是沒講的後果｜2026-10-21｜open、again
c2｜「我請它自己替這個資料夾寫一份規矩，它第三條就寫錯了」：第 3 條原文「3. 簡報大綱有多個「最終版」時，以檔案修改時間最新的為準，並在整理時告訴我你採用哪一份；不要自行合併內容。」（全檔 8 行的第 5 行）｜上一支 runlog R5 g1：`tool_use Write CLAUDE.md`；`docs/videos/claude-code-beginner-event-folder/demo/g1/CLAUDE.md` 第 5 行｜2026-10-21｜g1-rule、draft-check
c3｜它只跑了一次 `ls -la`、一個檔都沒打開就寫了｜上一支 runlog R5 stream summary：唯一的工具呼叫 `Bash ls -la`，接著 `Write`；NOTE (runner)「read no file before writing」｜2026-10-21｜g1-rule、draft-check
c4｜它會直接動你的檔案（Code 分頁直接存取本機檔案；acceptEdits 下改檔與 mkdir、mv、rm 不問）｜https://code.claude.com/docs/en/desktop-quickstart（Code: An interactive coding assistant with direct access to your local files）；https://code.claude.com/docs/en/permission-modes（acceptEdits 一節）｜2026-10-21｜stakes
c5｜CLAUDE.md 是純文字檔，放在你打開的那個資料夾最上層（./CLAUDE.md）；它上一層的資料夾裡的也在啟動時載入，子資料夾的用到才載｜https://code.claude.com/docs/en/memory（CLAUDE.md files are markdown files… You write these files in plain text；A project CLAUDE.md can be stored in either ./CLAUDE.md or ./.claude/CLAUDE.md；CLAUDE.md … in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand）｜2026-10-21｜door、md-page
c6｜每次新對話開始就載入，不用你提；每一次新對話都重新讀一遍｜https://code.claude.com/docs/en/memory（Both are loaded at the start of every conversation；Claude reads them at the start of every session）｜2026-10-21｜morning、projects、day-one
c7｜守則每天讀、手冊用到才翻：一直重貼的整套步驟做成 Skill；Skill 的內文用到才載入｜https://code.claude.com/docs/en/skills（Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's body loads only when it's used）｜2026-10-21｜booklet、answer
c8｜網頁版的專案指示：專案裡每一場對話都用它；它寫不回你電腦裡的資料夾（網頁版沒有檔案存取；本機檔案存取是桌面 app 的 Code 分頁）｜https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects（Claude will use these instructions for all the chats within the project）；https://code.claude.com/docs/en/desktop-quickstart（Chat: General conversation with no file access, similar to claude.ai）｜2026-10-21｜projects
c9｜換一件事（整理三份最終版）：沒有守則的那次做完沒有日誌；有守則的那次多了 `輸出/處理日誌.md`，寫「判斷依據（看內容，不看檔名與修改時間）」｜上一支 runlog R10 a1（C8 FAIL 有處理日誌：(none)）、R10b a2（C8 PASS 輸出/處理日誌.md）；`demo/a2/輸出/處理日誌.md`｜2026-10-21｜every-job
c10｜官方頁「Set up a project CLAUDE.md」那一段（screencast）｜https://code.claude.com/docs/en/memory#set-up-a-project-claude-md｜2026-10-21｜md-page
c11｜觀眾要寫的 CLAUDE.md 全文 12 行、8 條、最寬 29 字，逐字上卡；sha256 前 16 碼 8e865483370aa2d4｜`runlog.txt` N0 `cat CLAUDE.md` 與「Every file in both folders」的雜湊；`docs/videos/claude-code-beginner-event-folder/demo/extras/claude-md-specific/CLAUDE.md`｜2026-10-21｜folder、rule-01…rule-08、all-rules、write-file、your-line、closing
c12｜01 只讀不改：沒有這條它也沒動過原始檔（n1、v1、s1、N1、N2 的 報名表.csv 雜湊都是 835aff4efdfd433b…），但你每次都得交代｜上一支 runlog R3、R6、R7 的 C1 PASS；`runlog.txt` N1、N2 的 `sha256sum 報名表.csv`｜2026-10-21｜rule-01
c13｜02 放 輸出/：沒有這條，新檔案落在最上層｜上一支 runlog R3 n1、R7 v1（`報名名單_整理後.csv` 在根目錄）；`runlog.txt` N1 `ls`｜2026-10-21｜rule-02
c14｜03 同名不同人：報名表裡兩個王志明，Email（chihming.wang、cm.wang）和部門（業務部、研發部）都不同｜`docs/videos/claude-code-beginner-event-folder/demo/seed/講座籌備/報名表.csv`；`demo/N2/輸出/寄信名單.csv` 備註「與研發部王志明是不同人」｜2026-10-21｜rule-03
c15｜04 同 Email 兩次以最後一次為準：陳怡君填兩次，第二次只差大小寫和開頭一個空白｜同上報名表；`demo/N2/輸出/處理日誌.md`「陳怡君的 Email 比對：兩次寫法差在大小寫和開頭空白（`yijun.chen` vs ` YiJun.Chen`）」｜2026-10-21｜rule-04
c16｜05 取消與測試不寄：張書豪 10/06 備註取消；一筆姓名「測試」｜同上報名表；`demo/N2/輸出/處理日誌.md`「24 筆的去向」｜2026-10-21｜rule-05
c17｜06 缺 Email 不猜：洪子晴的 Email `zihching.hung@example` 少了結尾；n1、N1 把三個缺資料的人留在名單裡｜同上報名表；`demo/N1/reply.md`「洪子晴的 Email … 看起來少了 .com」；`demo/N2/輸出/要補資料.csv`｜2026-10-21｜rule-06
c18｜07 哪版最新看內容：三份最終版，修改時間最新的內容是舊的｜上一支 runlog M3（見 c20）｜2026-10-21｜rule-07
c19｜08 留日誌：沒有這條就沒有日誌（n1、v1、N1 都沒有）｜上一支 runlog R3、R7 C8 FAIL；`runlog.txt` N1 Verdicts「wrote NO log」｜2026-10-21｜rule-08
c20｜三份最終版內容裡的結束時間：最終版 16:00、真的最終版 16:30、這次絕對最終版 16:00；修改時間最新的是這次絕對最終版（2026-10-20）；只有真的最終版「皆已確認」｜上一支 runlog M3：`ls -lt` 與 `grep -n "時間\|講者"`｜2026-10-21｜versions
c21｜「The more specific and concise your instructions, the more consistently Claude follows them.」（卡片原文；譯文「指示越具體、越簡潔，它越照做」）｜https://code.claude.com/docs/en/memory（CLAUDE.md vs auto memory 一節）｜2026-10-21｜concise
c22｜一份 CLAUDE.md 的建議上限 200 行以內；再長照做的程度下降｜https://code.claude.com/docs/en/memory（Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence）｜2026-10-21｜two-hundred
c23｜「我試過只寫一句：名單要整理乾淨。」模糊版 CLAUDE.md 全檔 3 行（4195c05ae132e13a）｜`docs/videos/claude-code-beginner-event-folder/demo/extras/claude-md-vague/CLAUDE.md`；上一支 runlog R7 v1｜2026-10-21｜one-line
c24｜只寫一句跟沒寫一樣：v1 與 n1 同一個檔名（`報名名單_整理後.csv` 在根目錄）、同樣兩個漏洞（C7 缺資料的人混在名單裡、C8 沒有日誌）；這是全片唯一一句量測句｜上一支 runlog R3 n1 8/10、R7 v1 8/10，NOTE「the same two fails」｜2026-10-21｜one-line
c25｜站主觀點（企劃提案，站主未改寫）：規矩要寫到看得出做對沒；「名單要整理乾淨」不寫、「寄不出去的另外列一張表」才寫；每次都要講的寫進守則、用到才翻的做成 Skill；它生的草稿逐條對著資料夾看過才留｜`brief.md` 站主觀點 1–3｜2026-10-21｜verifiable、answer、draft-check
c26｜報名名單：沒有守則時每次要講原始檔別動、放 輸出/、同名不同人、缺 Email 另列、留日誌；有守則後只說「幫我整理報名名單」（八個字），得到 輸出/ 的名單、要補資料、處理日誌｜上一支 runlog R6 s1（`輸出/` 四個檔）；`runlog.txt` N2｜2026-10-21｜life、life-signup
c27｜週報資料夾、照片資料夾兩份守則是寫法範本，沒有跑過；卡片 `source`「寫法範本，沒有跑過」，旁白只說「可以這樣寫」｜—（沒有執行）｜2026-10-21｜life-weekly、life-weekly-say、life-photos、life-photos-say
c28｜`ls`：沒有守則的資料夾七個檔案，還沒有 CLAUDE.md（輸出逐字）｜`runlog.txt` N0 `(cd "$W/n" && ls)`、Terminal cards Card 1｜2026-10-21｜ls-before
c29｜沒有守則、打「幫我整理報名名單。」：回覆第 1–3 行逐字（「名單整理好了，存成 `報名名單_整理後.csv`，原始的 `報名表.csv` 沒有改動。」「**原本 24 筆，整理後是 19 位有效報名**…」）；新檔案在最上層；寄不出去的三個人留在名單裡（19 位含他們）；沒有 輸出/、沒有日誌。卡片只節錄前 3 個畫面行（38 行），第 6 行有測試用的 Email，terminal 卡不收｜`runlog.txt` N1 reply、`ls`、Verdicts；`demo/N1/reply.md`、`demo/N1/報名名單_整理後.csv`｜2026-10-21｜run-without
c30｜有守則、同一句：回覆第 1–2 畫面行逐字（「…4 個檔案都在 `輸出/`，報名表.csv 和活動說明.md 我只有讀，沒有改。」）與「處理方式」前三條（已取消、測試資料、同一個 Email 填兩次）；`ls 輸出` 四個檔：寄信名單.csv、處理日誌.md、要補資料.csv、飲食需求彙整.md｜`runlog.txt` N2 reply、`ls 輸出`、Terminal cards Card 4、5；`demo/N2/`｜2026-10-21｜run-with、ls-output
c31｜N2 的 `輸出/處理日誌.md`「做了什麼」第 4 項原文「4. 沒有 Email 或 Email 格式不對的，原樣列進要補資料，不猜。」（守則第 6 條的回音）｜`runlog.txt` N2 `cat 輸出/處理日誌.md`；`demo/N2/輸出/處理日誌.md`｜2026-10-21｜log-check
c32｜確認它讀到了：在對話裡打 `/context`，看 Memory files 底下有沒有 CLAUDE.md（引用）｜https://code.claude.com/docs/en/memory（To confirm the file loaded, run /context in a session and check the list under Memory files）｜2026-10-21｜context-check
c33｜請它先生草稿的那句要求全文：「幫我替這個資料夾寫一份 CLAUDE.md，只放每次整理這個資料夾都要遵守的規則，六條以內。寫完不要做其他事。」（三個泡泡在標點處切開，一字不改）；這句走到 g1 的檔｜`docs/videos/claude-code-beginner-event-folder/demo/prompts/write-claude-md.txt`；上一支 runlog R5 `## prompt`｜2026-10-21｜ask-draft
c34｜g1 寫的六條逐字（全檔 8 行的第 3–8 行；第 3 條亮起）｜`docs/videos/claude-code-beginner-event-folder/demo/g1/CLAUDE.md`｜2026-10-21｜draft-check
c35｜練習：把第 3 條（同名不同人）換成自己名單的判斷方式，例如「同一個員工編號才是同一人」，改完同一句再跑一次，看 處理日誌.md；沒有跑，卡片不宣稱結果｜—｜2026-10-21｜your-line
c36｜守則不是鎖：它是脈絡，不是強制設定；要硬擋一個動作是另一種東西（PreToolUse hook，片中不講名字）｜https://code.claude.com/docs/en/memory（Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead）｜2026-10-21｜not-a-lock
c37｜自動接受編輯模式下，搬檔、刪檔它不會問你（mkdir、touch、rm、rmdir、mv、cp、sed 在工作資料夾內自動通過）｜https://code.claude.com/docs/en/permission-modes（acceptEdits mode auto-approves common filesystem Bash commands: mkdir, touch, rm, rmdir, mv, cp, and sed … applies only to paths inside your working directory）｜2026-10-21｜safety
c38｜原始檔先留一份副本在別的資料夾；做完對一次日誌，它說動了幾筆檔案就該差幾筆（做法建議，不是官方句；日誌的「動了幾筆」是守則第 8 條要求的）｜守則第 8 條；`demo/N2/輸出/處理日誌.md`「修正過的欄位」「24 筆的去向」｜2026-10-21｜safety
c39｜「桌面版裡那個清單長怎樣，我沒看過」：這台機器沒登入桌面 app；/context 的畫面只有官方頁的文字｜`runlog.txt`（兩次執行都是 `claude -p`，沒有畫面）；企劃「我」的句子表｜2026-10-21｜context-check

沒有數字的主張：c8（網頁版專案寫不回資料夾，是產品性質的推論，兩頁各撐一半，卡片標引用）、c27、c35（沒有跑）。

## 與企劃不同的地方

- 開場章從企劃的 25 秒寫到約 42 秒：lint 對開場章的下限是 30 秒，而且 big 卡「它會動你的檔案／最後寫出你自己的八條」兩句放不進 25 秒；收尾問題「它到底是什麼？」移到第 1 章第一句（教學路線允許下一章用它開頭）。
- 第 2 章的玩笑「最終版、真的最終版、這次絕對最終版」從第 07 條移到緊接的 table 第一個狀態：第 07 條整條唸完已經 31 字，再加玩笑一個狀態會超過 13 秒。
- 第 4 章週報與照片兩個範本：企劃要旁白「明說是範本，不是跑出來的結果」；2026-10-11 的規則不讓旁白講這支片的製作（哪一段有沒有跑），所以旁白改成「可以這樣寫」、不宣稱結果，標示留在卡片 `source`（「寫法範本，沒有跑過」）與說明欄。
- 第 5 章終端機 N1 的回覆只節錄前 3 個畫面行（企劃寫 8 行）：第 6 行有 `test@example.com`，terminal 卡不收 Email，節錄整行、照順序、在它之前停。
- 第 7 章 outro 只放三句（答案、留言題、訂閱）；企劃的第四句「桌面 app 裡 Memory files 清單我沒看過」移到第 5 章 `/context` 那張 steps 卡，因為結尾三句共用一個畫面、要在約 45 個口語單位內。
- 「有了守則，它就安全了嗎？」從第 5 章末移到第 6 章第一句（第 5 章最後一張 code 卡三句會超過 15 秒）。
- 第 1 章「比喻停在哪裡」：企劃寫「新同事會記得昨天的事，它不會」；自動記憶開著時它會留筆記（memory 頁），而這支不講自動記憶，所以旁白改成確定的那一半「它每一次新對話，都重新讀一遍這份檔案」。
- `ls` 兩張 terminal 卡的 `tool_version` 寫「Git Bash (MINGW64), Windows 11」（印出輸出的程式），`claude -p` 兩張寫「2.1.295 (Claude Code)」。
- 新版型的欄位（theme、keys、icon、numeral、typing）不在 schema 裡，照發動訊息寫到旁邊的 `paper.json`，`video.json` 保持 schema 乾淨。
- 說明欄連到站上文章 `claude-code-claude-md-guide`（`source_guide`），片中沒有 cta 卡，旁白不念。

## 我懷疑但沒動的事

- 估計 8.5 分鐘（1,863 口語單位、95 句）。合成後實際長度可能比估計長 7%（2026-10-04 的量測）或短（文件寫實測約每分鐘 300 字）；若 tts 之後不足 8 分鐘，第 6 章可以加一條「做之前」的動作（例如先在規劃模式看一次），不加重述。
- 最長的狀態估 13.6 秒（versions 第 4 個狀態，兩句）、13.4 秒（not-a-lock）、13 秒（closing）；加 7% 仍在 15 秒內，但 QA 的 pace 項以實際時間軸為準。
- 非文字狀態：77 個狀態裡 big（帶 icon／numeral）、terminal、screencast、table 共 40 個，剛過一半；若 render 把 table 的 4 個狀態算成文字，就差 3 個。
- `rule-07` 那張 big 的 `text` 兩行、最長 18 字，紙底版型放不放得下由 render 判定；放不下就把「活動說明.md」那一段換行。
- N1 的 19 位「有效報名」包含三個寄不出去的人（旁白「寄不出去的人還留在名單裡」）：N1 的 csv 把他們標成待確認，不是獨立的一張表；查核時請對 `demo/N1/報名名單_整理後.csv`。
- `projects` 那張 compare 的右欄「它直接在資料夾裡動手」與左欄「寫不回你電腦裡的資料夾」：後者沒有一句官方原文，是 Projects 頁（只有上傳與對話）加 desktop-quickstart（Chat 沒有檔案存取）的推論；卡片 `source` 標兩頁。
- 字典沒有新詞：旁白裡的拉丁字只有 CLAUDE.md、Skill、Email，都已在 `lexicon.json`。
- `/context`、`Memory files`、`acceptEdits` 只在卡片上，旁白沒念。

## 進度

- 46 個場景、8 章、10 條 loops 全部寫完；`video.json`、`paper.json`（46 個場景、77 句 keys）、`claims.md` 已存。
- lint：0 錯誤、0 警告；估計 8.5 分鐘。
- 沒有 `shorts.json`（教學卡片，沒有 shot）。

## 查核第 1 輪（2026-10-21，獨立查核者；全表在 `verify-1.md`）

- 五個官方頁 2026-10-21 UTC 14:40 再抓一次（`<work>/_tools/verify-1/pages/`，全部 HTTP 200）：c4–c8、c10、c21、c22、c32、c36、c37 引用的句子都在今天的頁面上，逐字相符。
- 終端機與檔案的逐字核對（`<work>/_tools/verify-1/bytecheck.py`，57 項全過）：三張 code 卡的十二行＝`claude-md-specific/CLAUDE.md`；八張 rule 卡＝檔內八條；g1 第 3 條＝`demo/g1/CLAUDE.md` 第 5 行、六條＝第 3–8 行；三個泡泡＝`prompts/write-claude-md.txt`；`ls`、兩次 `claude -p` 的回覆節錄、`ls 輸出`＝`runlog.txt` 的 Terminal cards（`output` 陣列以換行相接，80 欄折行處與 Card 4 相同）；日誌第 4 項＝`demo/N2/輸出/處理日誌.md`；表格三個時間＝上一支 M3 的 grep。
- 改了兩處，都不是事實變更：`ls-output` 的 3if7 拿掉句尾「，四個檔案」（wdxh 已唸過同一個數字，同一次執行的事實只講一次；第 5 章唸出的數字少一個）；`projects` 的 `source` 補上 desktop-quickstart 頁（c8 左欄「寫不回你電腦裡的資料夾」的依據是 Projects 頁＋desktop-quickstart 頁，原本只標 memory 頁；`source` 限 48 字，所以寫成「Projects｜memory｜desktop-quickstart 頁｜2026-10-21」）。
- 沒查到可以推翻的：c8 的推論（Projects 說明頁只講上傳與對話，沒有一句提到本機資料夾；desktop-quickstart 寫 Chat 分頁「no file access, similar to claude.ai」），維持引用、卡片標推論。
- 名詞：memory 頁寫「target under 200 lines」是建議值，卡片 kicker「建議上限」對；旁白 dbw8「上限是一份兩百行以內」少了「建議」兩字，意思仍在「以內」，沒改。permission-modes 頁另寫「rm 與 rmdir 刪到 critical path 仍會問」，pj7u 說的是工作資料夾內的一般搬檔刪檔，沒改。

## 修訂 1（2026-10-21，盲評第 1 輪之後）

盲評讀者 13 題答了 8 題（沒過的：no_spoiler、one_line、payoffs、no_recap、chapters_are_events）。事實與引句一個都沒改（查核第 1 輪 0 錯誤）；改的是哪一句在哪一章講、講到哪裡。腳本在 `<work>/_tools/revise-1/revise.mjs`（改稿）與 `states.mjs`（每個狀態的秒數）。

旁白的改動（行 id｜改前 → 改後）：

- 開場 g1-rule：`code` 卡（它寫的第 3 條整句亮起）改成 `big` 卡「第三條，錯了」（icon warning），條文不再出現在開場。mutx 不變；esq9「亮起來這一行：好幾份最終版，以修改時間最新的為準。」刪掉 → 新句 x939「錯在哪，等一下打開它寫的那份。」（前向鉤子；loops 的 mutx → pznu 不變）。
- 第 5 章 draft-check：pznu「它看了一眼檔案清單，一個檔都沒打開，第三條就寫：看修改時間。」→「它一個檔都沒打開，第三條就寫：以修改時間最新的為準。」；新句 k2tt「照這條挑，挑到的是這次絕對最終版，舊稿。」（第一次說出它寫的原文、它會選到哪一份）；ptsz 不變，搬到新的 `big` 場景 draft-keep（kicker「它生的草稿」、icon checklist，c25、c3），因為三句擠在一個狀態超過 15 秒。
- 第 2 章 rule-02：yfin「少了這一條，新檔案就落在最上層，跟原始檔混在一起。」→「有了這一條，整理好的東西，你只要去一個地方找。」（卡片 sub 同改；claims 去掉 c13）。rule-08：u2ai「沒有這一條，它做完就走，你不知道它動了什麼。」→「做完要驗收，翻的就是這一份。」（sub 同改；claims 去掉 c19）。
- 第 5 章 run-without：267s「它整理好了，存成一個新檔案，直接丟在最上層。」→「它存了一個叫報名名單整理後的檔，丟在最上層，沒有輸出資料夾。」；egmm「寄不出去的人還留在名單裡，也沒有任何日誌。」→「名單留了十九個人，沒有 Email 的三個也在，待確認那欄記一筆，沒有日誌。」（claims 加 c13、c19）。
- 開場 stakes：ub5b「用員工守則這個對照把它搞懂，最後寫出你自己的八條。」→「用員工守則把它搞懂，最後把這八條存進你的資料夾，再改成你的。」承諾改成正文真的做到的事；loops：ub5b → winq（存檔），另加 ub5b → qzm5（改一行）。
- 第 6 章 not-a-lock：f5vr「要硬擋住一個動作，那是另一種東西，今天不講。」→「真的要擋，是權限設定的事，守則管不到。」（claims 加 c37）。
- 最後一章改名「一句話的答案」→「今天先做哪一件？」；jnve「以我的用法：每次都要講的，寫進守則；用到才翻的，做成手冊。」刪掉 → jqq7「今天先做一件：把你每次重講的那一段打進記事本，存成 CLAUDE.md，放最上層。」（一件行動，teaching-flow §七；卡片 kicker「今天先做一件」、icon file；claims c25、c5）。
- outro：juqf「八條、十二行，之後只說八個字。」刪掉 → zxai「它回的話不會跟我一樣，差多少我沒跑第二次。」（不確定句，見 c40）；tg3h「你每次重講的那一段是什麼？留言告訴我。」→「你每次重講的那段是什麼？留言告訴我。」、xpud「喜歡拿真的資料夾做的教學，就訂閱。」→「喜歡拿真資料夾做的教學，就訂閱。」（各少一字，讓這個狀態回到 15 秒內：14.2 秒）。
- 第 5 章 context-check：6wwg「想確認它有沒有讀到，在對話裡打卡片上這個指令。」→「想確認它有沒有讀到，在對話裡打一個斜線，選 context。」；uhk9「記憶檔案的清單裡有 CLAUDE.md，就是讀到了。」→「它會列出這場對話載入了什麼，記憶檔案那一欄有 CLAUDE.md，就是讀到了。」；tmnc「桌面版裡那個清單長怎樣，我沒看過，你看到了告訴我。」→「桌面版裡這張清單長什麼樣，我沒看過，你看到了告訴我。」卡片兩步的 detail 同改（「打一個斜線，從選單選 context」「記憶檔案那一欄；有，就是讀到了」）。
- 第 5 章 ask-draft：5t6h「你也可以請它先生一份草稿，像這樣說。」→「也可以先請它生一份草稿，這樣說：幫我替這個資料夾寫一份 CLAUDE.md。」（唸出那句要求的第一個子句；三個泡泡的原文不變；卡片 title「請它先生一份草稿」→「先請它生一份草稿」，避免聲音把「先生」唸成稱呼）。
- 第 4 章：3qfd「左邊這三句，就是你現在每個星期都在重講的。」→「你每個星期一，是不是都在重講左邊這三句？」；ia3m「寫進守則之後，只剩一句：幫我做這週的週報。」→「寫進守則，之後開口就是：幫我做這週的週報。」；grze「這三句寫一次。」→「沒寫原始檔不要刪，每一批你都得盯著它刪了什麼。」；45hv「之後每一批，只說：幫我整理這批照片。」→「寫好這三條，每一批只說：幫我整理這批照片。」「沒有…每次要講／有了…只說」的對照只在 tygm 說一次。
- 為了長度回到 8:30 以內（上面加了約 40 秒）：643b「所以那段規矩，你寫一次就好，不用每次重講。」刪（hnjp 已說）；`folder` 場景（7zni「裡面每一條，都來自這個資料夾真的發生過的狀況。」）刪，md-page 已經說了最上層放一個檔；2ii2 去掉開頭「而且」；jegb 去掉句尾「這份檔案」；h59b「記事本就打得開；放在它上一層的資料夾，也讀得到。」→「記事本就打得開。」（上一層也載入這件事留在 c5 與 door 卡）；ap8n「沒有這一條它也沒動過原始檔，但你每次都得交代一遍。」→「沒有這條它也沒動過原檔，但你每次都得交代。」；kc5x「對得上活動說明的只有真的最終版，兩位講者都已確認。」→「對得上活動說明的，只有真的最終版。」（第 2 章唸出的數字回到兩個：兩個王志明、兩行）；x3n8「打開講座籌備資料夾，裡面七個檔案，還沒有 CLAUDE.md。」→「打開講座籌備資料夾，報名表和活動說明都在，還沒有 CLAUDE.md。」；wdxh 去掉「四個」（第 5 章唸出的數字：十九、三，加承諾句的八個字；「六條以內」只在卡片）。

主張的增補：

c40｜「它回的話不會跟我一樣，差多少我沒跑第二次。」：N1、N2 各只跑一次；觀眾打同一行用的是自己帳號的預設模型（不確定句，§五第 3 種）｜`runlog.txt` 開頭 Cost 行「no second run was made so that the folders hold exactly one run each」、Model 行「A viewer typing the plain line gets their own default model」｜2026-10-21｜closing

- c2 現在分兩處：g1-rule 只說「第三條就寫錯了」；draft-check 才唸原文「以修改時間最新的為準」（`demo/g1/CLAUDE.md` 第 5 行）。c3（沒開檔）只在 draft-check、draft-keep。
- c20 多一句用法：k2tt「照這條挑，挑到的是這次絕對最終版，舊稿」依上一支 runlog M3（`ls -lt` 最上面是 這次絕對最終版 2026-10-20；內容 16:00、講者待確認）。
- c29 補證據：egmm 的「名單留了十九個人，沒有 Email 的三個也在，待確認那欄記一筆」：`demo/N1/reply.md` 第 3 行「整理後是 19 位有效報名」、第 16–17 行（劉思妤、曾詩涵沒有 Email；洪子晴少了 .com）；`demo/N1/報名名單_整理後.csv` 20 行＝表頭＋19 列，欄名「待確認事項」，第 8、14、16 行是這三個人（「缺 Email，無法寄確認信」「Email 格式不完整（缺 .com？）」）；`runlog.txt` N1 NOTE「kept the three without a usable Email in the list, flagged」；沒有 輸出/：N1 `ls`。c13、c19 的用到場景改為 run-without。
- c33：5t6h 唸的是那句要求的第一個子句，卡片三個泡泡仍是全文。
- c36 修訂：f5vr 的「權限設定」是籠統說法，指守則以外、Claude Code 設定裡能擋動作的那一層：memory 頁指名的是 PreToolUse hook（片中不講名字），permission-modes 頁是模式決定哪些動作自動放行、哪些要問（接著 pj7u 那一句）。卡片 not-a-lock 的 kicker／sub 不變。
- c25：最後一章的一件行動（jqq7）依站主觀點 1；「放最上層」依 c5。
- 字典：`docs/videos/lexicon.json` 加 `context: null`（6wwg、卡片「選 context」）。null 表示讓聲音照英文唸；這一輪沒有合成，tts 之後要聽一次，不對就改成拼音寫法。

結果：46 個場景（少 folder、多 draft-keep）、8 章、11 條 loops；`paper.json` 46 個場景、77 句 keys（每個場景 1＋reveals）。lint 0 錯誤、0 警告；估計 8:27（507.9 秒、1,856 口語單位、94 句）；標題那句話 hnjp 在 10.9 秒說完；最長的狀態 closing 14.2 秒、context-check 13.6 秒（其餘 13 秒以內）。旁白的「跟沒寫一樣」一句（w2f5）；「我」句 10 句，跟修訂前同數（jnve 換成 zxai）。非文字狀態：g1-rule 改成 big＋icon、新 draft-keep 是 big＋icon、少一張 folder，比修訂前多一個。

## 修訂 2（2026-10-21，盲評第 2 輪與聽稿之後）

盲評讀者 B 13 題答了 11 題（沒過的：no_recap、one_thread）；聽稿另列了 §九 量測句、TTS 唸法與第 4 章的套路。事實與引句一個都沒改；改的是哪一句留、怎麼唸。腳本在 `<work>/_tools/revise-2/revise.mjs`（改稿；跑完自檢 loops 與 `paper.json` 的 keys 數）。

場景刪了三個：`every-job`（2ii2「守則管的是每一件事：同一個資料夾，換一句要求，整理三份最終版。」、zp3c「沒有守則的那次做完就走；有守則的那次，多了一份處理日誌。」：在觀眾看到任何一次執行之前插進一次沒看到的執行，而且先講了 ls-output 才要揭曉的日誌）、`life-weekly`（imba）、`life-photos`（9afu）。c9（a1／a2）這一輪沒有場景用到，留在表裡備查；說明欄沿用紀錄的括號裡拿掉 a1／a2。

旁白的改動（行 id｜改前 → 改後）：

- no_recap：zexi「報名名單：以前每次要交代原始檔別動、放輸出、缺資料另外列。」→「報名名單，以前每一次都要先交代：缺 Email 的另外列一張表。」（一個具體子句，不再重列 jxiu 與第 2 章的規矩）；k2tt「照這條挑，挑到的是這次絕對最終版，舊稿。」→「照這條挑，挑到的就是這次絕對最終版。」（只留新事實：錯的那條會挑到哪一份；「內容是舊的」的理由只在 puy4 說）；puy4「…修改時間最新的這一份，內容還是舊的。」→「…修改時間最新的這次絕對最終版，內容還是舊的。」（點名檔名，聽稿第 26 項）。
- one_thread：ydzd「守則每天讀，手冊用到才翻：一直重貼的整套步驟，做成 Skill。」→「守則每天讀，手冊用到才翻：每次整理名單都要重複貼上的那整套步驟，才做成 Skill。」（掛在名單的例子上；c7 不變）；7cwc「能，專案裡每一場對話都會用它，但它寫不回你電腦裡的資料夾。」→「能啊，但它沒辦法把整理好的名單寫進講座籌備這個資料夾。」（c8 的「每一場對話都用它」只留在卡片左欄；gcwb「常駐指示」→「一直生效的指示」，卡片 title 同改，左欄點 2「寫不回」→「沒辦法寫進」）；f5vr「真的要擋，是權限設定的事，守則管不到。」刪，併進 mkpc「沒有。守則是脈絡，不是鎖，它不保證每一條都照做。」→「沒有。守則是脈絡，不是一把鎖；真的要擋住它，是權限設定的事。」（c36、c37 不變；卡片 text「守則不是鎖」→「守則不是一把鎖」）；k7jg 去掉開頭「我前面說過，」。
- §九 量測句：zxai「它回的話不會跟我一樣，差多少我沒跑第二次。」刪（c40 這一輪沒有場景用到，不確定性由 z8an 一句承擔）；every-job 整個刪（見上）；w2f5、z8an 留。剩下的量測一族：w2f5、z8an 兩句（wxnh「我試過只寫一句」是它們的前句，不算）。
- 第 5 章 run-without：267s「它存了一個叫報名名單整理後的檔，丟在最上層，沒有輸出資料夾。」→「它把整理好的名單存成一個檔案，叫報名名單整理後，丟在最上層。」＋新短句 5ps7「沒有輸出資料夾。」（同一個狀態）；egmm「名單留了十九個人，沒有 Email 的三個也在，待確認那欄記一筆，沒有日誌。」→ 兩句：egmm「沒有 Email 的三個人，它留在名單裡，寄信那天才知道寄不出去。」、新句 hwwh「沒有日誌，它做了什麼你只能信它說的。」。依據不變（c29：`demo/N1/報名名單_整理後.csv` 19 列含劉思妤、曾詩涵、洪子晴，「待確認事項」欄；N1 沒有日誌）；「十九」與「待確認那欄」這一輪不唸（第 5 章唸出的數字剩「三個人」與承諾句的「八個字」）。聽稿建議的「寄出去就是三封退信」沒照用：兩筆根本沒有 Email、一筆是 `@example` 少結尾，寄不出去是對的，「三封退信」不是紀錄裡的事；改成「寄信那天才知道寄不出去」，接 nv4d「寄不出去的另外列一張表」。
- 第 5 章 context-check：tmnc「桌面版裡這張清單長什麼樣，我沒看過，你看到了告訴我。」刪（c39 這一輪沒有旁白用到；卡片 `source` 仍標「引用」、說明欄仍寫沒看過）；uhk9「…記憶檔案那一欄有 CLAUDE.md…」→「…記憶檔案這個欄位底下有 CLAUDE.md…」（卡片 step 2 detail 同改）；新第三步（reveal）kaqd「沒有的話，先看檔名是不是打成 CLAUDE.md，再看它是不是放在最上層。」（一個排除動作，依 c5：檔名 CLAUDE.md、放在你打開的那個資料夾最上層；卡片加 step「沒有？先看檔名和位置／檔名是 CLAUDE.md，放在最上層」，claims 加 c5）。
- 第 2 章八條裡的短句：rule-05 在 55ru「…對吧？」之後加 yt2x「每一份都有。」。
- TTS 唸法（聽稿第 12–41 項）：y4xc「只讀不改」→「只能讀，不能改」；ap8n「原檔」→「原始檔案」；6ivh「列進要補資料」→「另外列進要補資料這張表」；2utv「有一筆少了結尾」→「有一筆 Email 少了結尾」；u7a9「看內容對不對得上活動說明」→「看內容跟活動說明對不對得上」；kc5x「對得上活動說明的」→「跟活動說明對得上的」；mrmq「輸出的處理日誌」→「輸出資料夾裡的處理日誌」；fzrx「最長的一條兩行」→「最長的一條也只寫了兩行」；dbw8「再長」→「寫得再長」；winq「新檔」→「開一個新檔案」；hxm6「檔名照這樣打」→「檔名就打 CLAUDE.md」；3if7 加動詞「裡面有…還有一份處理日誌」；maxm「回音」→「回應」；5t6h「生一份草稿」→「寫一份草稿」（卡片 title、draft-keep kicker「它生的草稿」→「它寫的草稿」、ptsz 同改）；pznu「一個檔」→「一個檔案」（caption 同改）；qzm5「改一行：亮起來的這一條」→「改一條：畫面上標出來的這一條」（paper key、說明欄同改）；pj7u「搬檔、刪檔」→「搬動檔案、刪除檔案」（卡片 item 同改）；z3e2「對一次日誌」→「核對一次日誌」（卡片 item 同改）；xpud「真資料夾」→「真的資料夾」。第 12、20、27、28 項（待確認那欄、舊稿、換一句要求、放輸出）所在的句子已刪或改寫，不另改。3qfd 的「左邊」照聽稿第 42 項留著。
- 第 4 章（約 37 秒）：tygm「同一個句型：沒有守則時你每次要講的，有了之後你只要說一句。」刪，`life` 卡改成 kicker「生活裡怎麼用」、text「三個資料夾」、sub「報名名單、週報、照片」，只留 78v3 的問句；報名名單是真的那個例子（zexi、8vmx）；週報只剩問觀眾的 3qfd 與 ia3m（兩句）；照片只剩 grze「照片資料夾，沒寫原始檔不要刪，每一批你都得盯著它刪了什麼。」與 45hv（兩句；沒有那條會出什麼事）。c27 的兩張 compare 卡仍標「寫法範本，沒有跑過」。
- outro：刪 zxai 之後 lint 要三句，第一句加一個動作 rh48「存好之後，開一個新對話，打同樣八個字。」（接最後一章 jqq7 的下一步，不是總結；依 c6、c26），再 tg3h、xpud。

主張的註記：c9、c39、c40 這一輪沒有場景用到（留表備查）；c8 的「每一場對話都用它」只在卡片；c29 的用法見上；c5 多一個用到的場景 context-check；c27 少 life-weekly、life-photos。字典沒有新詞（拉丁字仍只有 CLAUDE.md、Skill、Email、context）。

結果：43 個場景（少 every-job、life-weekly、life-photos）、8 章、11 條 loops 不變；`paper.json` 43 個場景、73 句 keys（每個場景 1＋reveals，最長 ≤ 24 字）。lint 0 錯誤、0 警告；估計 8:10（490.3 秒、1,795 口語單位、91 句）；標題那句話 hnjp 在 10.9 秒說完；「跟沒寫一樣」一句（w2f5）；最長的狀態 closing 13.7 秒、rule-06 13.3 秒、your-line 13.1 秒（其餘 13 秒以內）；「我」句 10 句（mutx、gcwb、fzrx、bwng、wxnh、z8an、mxa4、nv4d、ptsz、tg3h）。storytelling panel 要重跑（舊的 hash 對的是修訂 1 的稿）。

## 修訂 3（2026-10-21，第三位讀者 12/13 後）

- jegb「比喻停在這裡…」改成「只有一點不像…所以才要寫下來」（不再重講 5nwa 的「每次讀一遍」）；afr9 章首句帶例子的狀態；zexi 不再重講「缺 Email 另外列」；ptsz 去掉第二個「我的看法是」。文字改動，狀態與數字不變。

## 修訂 4（2026-10-21，第四位讀者 11/13 後）

- w2f5 的「兩個漏洞」說成具體的兩件（缺資料混在名單、沒有日誌）；7ft6 改成 N2 日誌「哪裡沒把握」那一筆（沒硬塞進名單）；mkpc「脈絡」改「提醒」；k2tt 刪（重講 puy4）。數字與引文不變。

## 修訂 5（2026-10-21，第五位讀者 12/13 後）

- yt2x 改「我這一份也有一筆」（原「每一份都有」像兩個人對話）；3if7 說明飲食需求那份是活動說明要給場地的；7cwc 主詞改成「網頁版」。文字改動，數字不變。
