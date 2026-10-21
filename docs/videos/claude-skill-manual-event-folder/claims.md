# claims：claude-skill-manual-event-folder

撰稿日 2026-10-21。「實跑」的出處是同一資料夾的 `runlog.txt`（27 次企劃內的無介面 session，UTC 00:27–00:50，加上事後加跑的 W2a、W2b，UTC 01:33–01:35；都是 Claude Code 2.1.295，sonnet，2026-10-21）與 `demo/`；官方頁是 brief 列的頁面，原檔在 `<work>/_tools/pages/`（UTC 2026-10-20 18:06–18:14 抓，台北 2026-10-21），撰稿時照原檔重讀。格式：`編號｜主張（旁白或卡片上的說法）｜出處｜查核日｜場景`。

## 主張

c1｜Skill 是一個資料夾，裡面是指示、程式與資源，Claude 需要時才載入（「Skill 就是一本說明書」的比喻底）｜https://support.claude.com/en/articles/12512176-what-are-skills（Skills are folders of instructions, scripts, and resources that Claude loads dynamically）；https://agentskills.io/specification（Directory structure）｜2026-10-21｜open
c2｜講座籌備的書櫃上有報名表檢查、會議紀錄、行前提醒信等說明書，每本寫一次、照它做｜實跑：demo/booklets/book-lean、demo/shelf5/meeting-notes、demo/shelf5/reminder-mail（make-booklets.mjs，M1 雜湊）｜2026-10-21｜uses
c3｜只說「第二批報名表來了（報名表_第二批.csv），照平常的方式檢查一下。」，三次都翻開 signup-check（3／3）｜實跑：runlog.txt Item CSa、CSb、CSc 的 `VERDICT opened signup-check: YES`；總表 opened 欄｜2026-10-21｜result、ask、run-stats
c4｜寄信名單從 16 人變 18 人；缺 Email 的宋柏均另外列進要補資料｜實跑：M6 起點 `unique addresses … 16`；CSa–CSc `B4 PASS`、`B5 PASS`、`unique addresses … 18`｜2026-10-21｜result
c5｜內文點名的附件 部門對照.md，需要它的 8 次（CS×3、CV×3、W1×2）裡有 5 次回說「不存在」或「找不到」（CSc、CVa、CVb、W1a、W1b）｜實跑：runlog.txt「Unexpected results」第 2 條；總表最後一欄；demo/CSc、CVa、CVb、W1a、W1b/reply.md｜2026-10-21｜result
c6｜找不到附件時沒有停下來：在回覆裡提一句（CSc、W1a、W1b 在後段；CVa 在最後一段「需要你確認」的第 1 點，後面還有一點；CVb 在中段「兩件事要你確認」，後面還有飲食統計；verify-2 把「回覆最後」改成「回覆裡」），照第一批名單的寫法統一部門做完（C9 仍 PASS）｜實跑：demo/CSc/reply.md「需要你確認 2.」、CVa「部門對照.md 不存在。我照名單原本的寫法統一」；runlog Unexpected 2「All of them still unified the departments from the first batch's list (C9 PASS)」｜2026-10-21｜stakes
c7｜一本說明書＝`講座籌備/.claude/skills/signup-check/`，裡面 SKILL.md、部門對照.md、確認信範本.md｜實跑：M1 extras 雜湊（book-lean 三個檔）；CSa「folder before」清單｜2026-10-21｜folder
c8｜上一支裡，第二批報名表交給一本叫 signup-check 的 Skill 檢查（回呼一句）｜docs/videos/claude-code-beginner-event-folder/video.json 場景 skill-ask、skill-run（k1、k2）｜2026-10-21｜folder
c9｜SKILL.md 是純文字：最上面是 YAML frontmatter，下面的 Markdown 內文沒有格式限制｜https://agentskills.io/specification（SKILL.md format；Body content: There are no format restrictions）｜2026-10-21｜md-ask
c10｜SKILL.md 第 1–7 行（封面）照原檔上卡；全檔 20 行，sha256 前 16 碼 8331907e77181682｜實跑：demo/booklets/book-lean/signup-check/SKILL.md；M1｜2026-10-21｜cover-name、cover-desc、cover-when
c11｜介紹兩句：做什麼＋什麼時候用；旁白照唸 description 全文｜https://agentskills.io/specification（description: Should describe both what the skill does and when to use it）；https://support.claude.com/en/articles/12512198-how-to-create-custom-skills（A clear description of what the skill does and when to use it）｜2026-10-21｜cover-desc、cover-when
c12｜名字只能用小寫英文、數字、連字號，要跟資料夾同名；介紹寫中文沒關係｜規則：https://agentskills.io/specification（name field）；中文介紹：實跑 M2 `PASS description <= 200 characters`、M3 `✔ Validation passed`，CS 三次都用它翻開｜2026-10-21｜name-rule
c13｜封面少了 name 那一行（前一支的 SKILL.md）：上傳前檢查判 `fix before upload`；網頁版上傳要 name 與 description 都有；這一本 `ready to upload`｜實跑：M2 cover-check.mjs 輸出（兩行 FAIL name）；規則：https://support.claude.com/en/articles/12512198-how-to-create-custom-skills（Required metadata fields）｜2026-10-21｜no-name
c14｜在 Claude Code 少了 name 照樣能用，拿資料夾名代替｜https://code.claude.com/docs/en/skills（frontmatter 表：name … Defaults to the directory name）｜2026-10-21｜no-name
c15｜「活動說明.md 寫的講座幾點結束？只回答時間，不要改任何檔案。」書櫃上有 signup-check，回覆 16:30，沒有翻開任何一本｜實跑：demo/prompts/time.txt；demo/L1a/reply.md；L1a `opened: none`｜2026-10-21｜time-ask、shelf-ask
c16｜一本說明書都沒放：開場第一個請求 33,861／33,866 token｜實跑：總表 L0a、L0b first=｜2026-10-21｜size-table
c17｜放一本 20 行說明書：33,940／33,941，比沒放多 77｜實跑：總表 L1a、L1b；`first= means … L1 33940.5 (+77)`｜2026-10-21｜size-table、claude-md、four-ways、fat
c18｜69 行（附件貼進內文）那一本：33,940／33,938，多 75.5，跟 20 行的一樣大（LF 對 L1 最大差 3，門檻 15）｜實跑：總表 LFa、LFb；「The four outcomes」成果 4 (a)｜2026-10-21｜size-table、fat
c19｜放六本：34,286／34,286，多 422.5，一本約 70｜實跑：總表 L6a、L6b；Unexpected 5（Six covers cost 422.5）｜2026-10-21｜size-table
c20｜同樣七步寫在 CLAUDE.md：34,328／34,323，多 462，問什麼都帶著｜實跑：總表 LMa、LMb；LM−L0 = 462｜2026-10-21｜size-table、claude-md、four-ways、differences
c21｜漸進式載入：名字和介紹每本約 100 token，一開場就全部載入（引用原文上卡）｜https://agentskills.io/specification（Progressive disclosure: Metadata (~100 tokens)）｜2026-10-21｜progressive
c22｜比喻對不上的第一處：每一次來回，書櫃上每本的封面都跟著送進去（真的書櫃要走過去才看）｜https://code.claude.com/docs/en/skills（Claude Code loads a listing of skill names and descriptions into context）；實跑旁證：CS 三次 first= 34,285–34,287 對 CN1 34,209｜2026-10-21｜progressive、shelf-stop
c23｜書櫃從來不是空的：一本都沒放時這台機器的 Claude Code 列 22 本內建技能；放 signup-check 變 23，再放五本變 28｜實跑：L0、L1、L6 skillview `shelf:`；Unexpected 6｜2026-10-21｜shelf-count
c24｜CLAUDE.md 每一次請求都整段帶著，說明書平常只帶封面、要用才翻開內文｜實跑：LM−L0 = 462 對 L1−L0 = 77；https://code.claude.com/docs/en/skills（Unlike CLAUDE.md content, a skill's body loads only when it's used）｜2026-10-21｜claude-md
c25｜網頁版專案的指示一直載入（卡片標「引用」）｜https://support.claude.com/en/articles/12512176-what-are-skills（Projects provide static background knowledge that's always loaded）｜2026-10-21｜claude-md
c26｜書櫃上另外五本的「什麼時候用」與內文規則（講者介紹 150 字、會議紀錄三段與「未指定」、報帳看不清標待確認、文案主標 15 字與貼文 120 字、行前提醒只寫通用草稿不寄出）｜實跑：demo/shelf5/*/SKILL.md（M1 雜湊）｜2026-10-21｜uses-table
c27｜（撰稿時刪除：官方的六種自訂用途清單，為了片長拿掉；沒有任何場景用到）｜—｜2026-10-21｜—
c28｜含糊的封面：名字 checklist、介紹只有「檢查用的步驟。」，內文與附件逐字相同；書櫃上同時有 reminder-mail｜實跑：demo/booklets/book-vague（daf1484a61ea5c64）；CV 的 extras 含 shelf5｜2026-10-21｜vague
c29｜同樣的一句要求跑三次，這次含糊的也翻開了 3 次；都是 checklist，沒有翻成 reminder-mail；B1–B6 全過｜實跑：CVa–CVc `VERDICT opened checklist: YES (other booklets opened: none)`；成果 3 降級的紀錄｜2026-10-21｜vague
c30｜含糊封面開場只省 61 token（CV first= 34,223–34,228 對 CS 34,285–34,287）；寫清楚的兩句三次也都翻開，檢查也都過｜實跑：Unexpected 1；總表｜2026-10-21｜vague
c31｜它決定翻不翻、翻哪一本，看的是封面的介紹（比喻對不上的第二處：不是你挑書）｜https://support.claude.com/en/articles/12512198-how-to-create-custom-skills（description … Claude uses this to determine when to invoke your skill）；https://support.claude.com/en/articles/12512176-what-are-skills（Claude determines which skills are relevant）｜2026-10-21｜why-cover、pick-stop
c32｜Claude 沒用你的 Skill 時，要查介紹有沒有寫清楚什麼時候用（引用原文一句上卡）｜https://support.claude.com/en/articles/12512180-use-skills-in-claude（Troubleshooting › Claude isn't using a skill）｜2026-10-21｜why-cover
c33｜壞例「Helps with PDFs.」；好例寫做什麼（抽文字與表格、填表、合併）＋什麼時候用（處理 PDF、提到 PDF 或表單）（卡片是中譯）｜https://agentskills.io/specification（description field 的 Good／Poor example）｜2026-10-21｜good-bad（修訂 1：卡片仍是規格頁的 PDF 好壞例；旁白改用這支自己的兩個封面當好壞例，出處是 c11、c28）
c34｜Claude Code 自己的格式檢查 `claude plugin validate`：兩句封面、含糊封面、沒有 name 的三本都 `✔ Validation passed`｜實跑：M3｜2026-10-21｜validate
c35｜內文第 9–20 行照原檔上卡，七步逐條照唸｜實跑：demo/booklets/book-lean/signup-check/SKILL.md｜2026-10-21｜body-1 至 body-7
c36｜第一批的寄信名單裡有兩個王志明：chihming.wang（業務部）與 cm.wang（研發部）｜實跑：demo/start/輸出/確認信名單.csv 第 3、6 行；selftest C2｜2026-10-21｜body-2、two-wangs
c37｜第二批有一筆「測試二」（test2@example.com，部門寫「測試」）｜實跑：demo/start/報名表_第二批.csv 第 6 行｜2026-10-21｜body-3
c38｜第七步的「才」：檢查時它沒有寫確認信；CSa 回覆最後一句「我沒有寫確認信，技能說明要寫的時候才寫。」｜實跑：runlog CSa reply｜2026-10-21｜body-7
c39｜那一句要求的全文（33 字；檔案 34 字元含結尾換行，查核 1 改）｜實跑：demo/prompts/skill-auto.txt｜2026-10-21｜ask
c40｜CSa 第一個工具呼叫就是 Skill signup-check；回覆第一句「第二批 6 筆已檢查完。2 人加進寄信名單，1 人列入要補資料，其餘 3 筆沒有動。」（卡片照原文）｜實跑：runlog CSa stream summary 與 reply｜2026-10-21｜ask
c41｜CSa 依序：翻開 signup-check → 讀報名表與名單（全程 3 個 Bash 指令被擋：讀檔時 1 個、寫檔時 2 個；查核 1 把卡片第 2 步改成「整段共有三個指令被擋下」）→ 部門對照在資料夾最上層兩次找不到，再到說明書資料夾讀到 → 用 Edit 改三個輸出檔（簡郁庭、邱品妍進名單，宋柏均進要補資料）→ 回覆提醒黃雅婷問能不能改線上、要有人回｜實跑：runlog CSa 的 tool_use 序列、permission_denials=3、NOTE (runner)｜2026-10-21｜run-steps
c42｜CS 三次：寄信名單都 18 個 Email；要補資料從 3 變 4｜實跑：CSa–CSc B5、B4；起點 要補資料 3 人（劉思妤、曾詩涵、洪子晴，selftest C7）｜2026-10-21｜run-stats
c43｜事先寫好的六項檢查（batch2.mjs B1–B6）三次都全過；兩份原始報名表雜湊不變（835aff4efdfd433b、d93be0d8338f8802）｜實跑：成果 1 的 NOTE｜2026-10-21｜run-stats
c44｜每次貼七步（CPa、CPb）、七步寫在 CLAUDE.md（CMa、CMb）、寫成說明書（CS）都 6／6：「三種交代方式結果一樣」；什麼都不交代（CN1）也 6／6：「這一批它不靠說明書也猜得到」｜實跑：總表；成果 1 的 NOTE；Unexpected 4｜2026-10-21｜four-ways
c45｜CN1 是看第一批的輸出檔和日誌推出平常的做法｜實跑：demo/CN1/reply.md 第一段｜2026-10-21｜four-ways
c46｜差別：貼上那一邊每次 309 字（706 位元組的檔案去掉結尾換行；查核 1 由 310 改）對 33 字（90 位元組，查核 1 由 34 改）、得自己留著；CLAUDE.md 問什麼都帶 462；只有說明書能整個資料夾帶去 Claude 網頁版（引用）｜實跑：M1 `wc -c`、node 字數（paste.txt 310、skill-auto.txt 34，都含檔尾一個換行；打的字是 309、33）；LM−L0；引用：https://support.claude.com/en/articles/12512180-use-skills-in-claude（Upload a ZIP file containing your skill folder）｜2026-10-21｜four-ways、differences
c47｜觀眾加的第 8 步（兩行）照原檔上卡；全檔 22 行，6f8319939f194993｜實跑：demo/booklets/book-mine/signup-check/SKILL.md；M1｜2026-10-21｜step8、step8-b
c48｜加了第 8 步，W1a、W1b 兩次都多一份 輸出/待回覆.csv，只有一列：黃雅婷、改成線上參加可以嗎？；只有 W1a 多一欄「狀態」寫「待回覆（未回答）」，W1b 只有三欄（卡片是 W1a 那份的原文；查核 1 把旁白 ykf3 改成「第一次還多一欄狀態」）｜實跑：W1a、W1b mine.mjs M1–M5 PASS；demo/W1a/輸出/待回覆.csv｜2026-10-21｜step8-result（2026-10-21 拆成兩個狀態：表格加一列 W1b 的原文，W1b 的檔沒有「狀態」欄，卡片寫「（沒有這一欄）」；證據 demo/W1b/輸出/待回覆.csv）
c49｜她在寄信名單裡只出現一次｜實跑：mine.mjs M4 PASS（W1a、W1b）｜2026-10-21｜step8-result
c50｜叫它自己寫一本的那一句要求（拆成六段上卡，全文在說明欄）｜實跑：demo/prompts/write-skill.txt；runlog G1 ## prompt｜2026-10-21｜g1-ask
c51｜結果沒寫成：寫進 .claude/skills/signup-check/SKILL.md 被擋下（「Claude requested permissions to write to … but you haven't granted it yet.」），回覆要你允許；資料夾裡沒有 SKILL.md｜實跑：runlog G1 tool_error、reply、cover-check `FAIL SKILL.md exists`｜2026-10-21｜g1-result
c52｜它想寫的那本：介紹 102 字、內文 71 行、部門對照直接寫進內文（沒有附件），cover-check `ready to upload`；你的那本：介紹 60 字、內文 12 行、部門對照放成附件｜實跑：runlog G1 第二條 NOTE；demo/G1/attempted-SKILL.md 第 28 行；M2｜2026-10-21｜g1-result
c53｜翻開前，20 行與 69 行兩本開場一樣大（+77 對 +75.5）｜實跑：成果 4 (a)｜2026-10-21｜fat
c54｜翻開那一步：20 行那本 +487、+436、+436；69 行那本三次都 +1,288，約 2.8 倍（平均差 835）｜實跑：總表 growth；成果 4 (b)；Unexpected 3｜2026-10-21｜fat
c55｜翻開後一直帶著：20 行那本之後 9、9、6 個請求，69 行那本 7、7、8 個；比喻對不上：翻開後整本留在對話裡；改了說明書，進行中的對話不會重讀（後者引用）｜實跑：總表 carry；https://code.claude.com/docs/en/skills（Skill content lifecycle: enters the conversation as a single message and stays there … does not re-read the skill file on later turns）｜2026-10-21｜fat、stays
c56｜20 行那本三次檢查都沒碰 確認信範本.md｜實跑：成果 4 (c)（no CS session touched 確認信範本.md by any tool）｜2026-10-21｜fat
c57｜部門對照：只寫檔名的 8 次裡 3 次讀到（CSa、CSb 用 Bash cat；CVc 用 Read），5 次沒讀到；跟 W2 同一本、只差第 17 行的 W1a、W1b 是 0／2｜實跑：總表最後一欄；Unexpected 2、2b｜2026-10-21｜appendix-miss、appendix-fixed
c58｜CVa 回覆原文一句：「部門對照.md 不存在。」｜實跑：demo/CVa/reply.md「需要你確認 1.」｜2026-10-21｜appendix-quote
c59｜原因：第 5 步只寫檔名沒寫位置；session 先從資料夾最上層找（`ls -R .` 看不到 .claude）；找不到就照第一批名單統一部門、回覆最後請你給對照表；結果仍對是因為第一批名單已統一（C9 PASS）｜實跑：Unexpected 2；CSa 的 Bash 指令序列；CSc、CVa、CVb、W1a、W1b 的 reply｜2026-10-21｜appendix-quote、appendix-why
c60｜改一行就讀到：W2 用的 SKILL.md（book-loc，3d129d4036c107cf）是加了第 8 步的那一本只改第 17 行：「   照 部門對照.md 統一。」→「   照 .claude/skills/signup-check/部門對照.md 統一。」，其他行不變（卡片放第 15–18 行原文）；寫上位置之後 W2a、W2b 兩次都在第一個 Bash 指令讀到部門對照（2／2），都翻開 signup-check、沒翻別本，B1–B6 6／6、mine M1–M5 5／5，growth +500、之後 6／7 個請求帶著，確認信範本沒碰｜實跑：runlog.txt「Item W2 (added) W2-setup」的 diff 與雜湊、W2a、W2b 段落、Unexpected 2b、總表 W2a／W2b 兩列；demo/booklets/book-loc、demo/W2a、demo/W2b｜2026-10-21｜appendix-fix、appendix-fixed、appendix-rule
c61｜怎麼選：每次都要照做的進內文，偶爾才用的範本、對照表放附件｜https://agentskills.io/specification（Move detailed reference material to separate files）；https://code.claude.com/docs/en/skills（every line is a recurring token cost）；實跑旁證 c54–c56｜2026-10-21｜appendix-choose
c62｜壓縮：對的 signup-check.zip 三筆都在 signup-check/ 底下（2,271 位元組）；錯的三個檔散在最上層（2,193 位元組）｜實跑：M4；demo/pack/*.txt｜2026-10-21｜zip
c63｜ZIP 的根要是技能資料夾本身；檔案直接散在 ZIP 最上層是錯的結構｜https://support.claude.com/en/articles/12512198-how-to-create-custom-skills（Package your skill: Correct／Incorrect structure）｜2026-10-21｜zip
c64｜個人方案：Settings › Capabilities 打開 Code execution and file creation → Customize › Skills → 「+」→「+ Create skill」→「Upload a skill」→ 上傳裝著技能資料夾的 ZIP；之後出現在清單，可開可關（引用，沒有登入、沒有上傳）｜https://support.claude.com/en/articles/12512180-use-skills-in-claude（How to enable skills；Add and use custom skills）｜2026-10-21｜upload-steps、upload-cast
c65｜中文介面的選單名只查到中文說明頁：頁上寫「設置 > 功能」「自定義 > 技能」；頁面沒有說自己是機器翻譯，台灣介面的實際用字沒有確認（「我」的不確定句；verify-2 把「機器翻譯的說明頁」「自訂」改成頁上看得到的「自定義」底下的「技能」）｜https://support.claude.com/zh-TW/articles/12512180｜2026-10-21｜upload-cast
c66｜上傳失敗常見四個原因：ZIP 太大、資料夾名跟 skill 名不同、少了 skill.md、名字或介紹有不合規的字元｜https://support.claude.com/en/articles/12512180-use-skills-in-claude（Upload errors）｜2026-10-21｜upload-errors
c67｜網頁版介紹上限 200 字元，規格是 1,024；signup-check 的介紹 60 字｜https://support.claude.com/en/articles/12512198-how-to-create-custom-skills（200 characters maximum）；https://agentskills.io/specification（Max 1024）；實跑 M2（60 characters）｜2026-10-21｜upload-errors
c68｜免費版能不能上傳：support〈Use skills in Claude〉列 Free、Pro、Max、Team、Enterprise；Claude 文件 overview 的 claude.ai 一節只列 Pro、Max、Team、Enterprise（「我」的不確定句）｜https://support.claude.com/en/articles/12512180-use-skills-in-claude；https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview（### claude.ai: Custom Skills … Available on Pro, Max, Team, and Enterprise plans）｜2026-10-21｜plans
c69｜網頁版開著的技能，會單向同步到同一個帳號登入的 Claude Code（需要 v2.1.273 以上）；開 session 時同步，之後約每 10 分鐘查一次｜https://support.claude.com/en/articles/12512180-use-skills-in-claude（Use skills in Claude Code：「The sync is one-way」「about every 10 minutes」「needs Claude Code v2.1.273 or later」）；https://code.claude.com/docs/en/skills（Skills synced from claude.ai：下載、從不上傳，v2.1.273）。overview 的「Custom Skills do not sync across surfaces」與這兩頁不一致，verify-2 判定以兩頁一致的說法為準，overview 只拿來支持 c70｜2026-10-21｜sync
c70｜資料夾裡這一本不會自己跑上網頁版，要另外上傳（Claude Code 的技能在檔案系統裡，跟 claude.ai 分開）｜https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview（Custom Skills do not sync across surfaces … Claude Code Skills are filesystem-based and separate from both claude.ai and API）｜2026-10-21｜sync
c71｜格式是公開標準；支援工具清單有 46 個（查核 1 由 45 改：clients.mjs 的正規式要求 instructionsUrl，漏數了沒有這欄的 Piebald；2026-10-21 重抓的頁與撰稿時的原檔都是 46 筆 name），Gemini CLI、Cursor、GitHub Copilot 都在上面｜https://agentskills.io/clients（撰稿日以 `_tools/clients.mjs pages/clients.html` 數出 `clients: 45`；原檔 grep 有 Gemini CLI、Cursor、GitHub Copilot）；https://support.claude.com/en/articles/12512176-what-are-skills（Agent Skills open standard）｜2026-10-21｜clients
c72｜ChatGPT 桌面版側邊欄有 Skills，ChatGPT 打 @ 選一本；Codex 打 $ 或 /skills；單獨的 skill 在 ChatGPT 桌面版、Codex CLI 與 IDE 擴充，網頁版只透過外掛帶進來（沒有安裝、沒有測試）｜https://learn.chatgpt.com/docs/build-skills｜2026-10-21｜clients（修訂 1：旁白只說 ChatGPT 和 Codex 在清單上，細節在說明欄）
c73｜ChatGPT 與 Codex 也會照 description 自己挑（implicit invocation）｜https://learn.chatgpt.com/docs/build-skills（Implicit invocation … when your task matches the skill description）｜2026-10-21｜（修訂 1：chatgpt 場景刪除，旁白不再講；未上畫面）
c74｜說明書的資料夾可以夾小程式，AI 會去執行（比喻對不上的第三處）｜https://agentskills.io/specification（scripts/: Contains executable code that agents can run）；https://support.claude.com/en/articles/12512198-how-to-create-custom-skills（Add scripts）｜2026-10-21｜risk
c75｜只裝自己寫的或信得過來源的；同事給的也先讀過每一個檔再開｜https://support.claude.com/en/articles/12512180-use-skills-in-claude（Only install skills only from trusted sources … including one shared by a colleague—review it before enabling）；https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview（Use Skills only from trusted sources）｜2026-10-21｜risk
c77｜寫上位置對只寫檔名：2／2 對 0／2（同一本只差這一行的 W1）、對企劃內只寫檔名的 3／8；W2 只跑兩次（卡片標「之後加跑的兩次」）｜實跑：runlog Unexpected 2b、W1 對 W2 的 NOTE｜2026-10-21｜appendix-fixed
c78｜W2a、W2b 第一個 Bash 指令裡讀附件的那一段：`cat .claude/skills/signup-check/部門對照.md`；兩次都把兩個新人的部門統一成業務部、行銷部｜實跑：runlog W2a 第 3841 行、W2b 第 3985 行的 tool_use Bash（節錄）；demo/W2a/reply.md「業務」→業務部、「Marketing」→行銷部｜2026-10-21｜appendix-cmd
c79｜別人寫的那一本先打開來讀：G1 想寫的 SKILL.md 上傳前檢查判 ready to upload，但內文 71 行（你那本 12 行，所以「長好幾倍」），部門對照整段寫在內文裡；看不懂的那一頁就不裝（頻道做法）｜實跑：runlog G1 第二條 NOTE（cover-check 對 runner/g1-attempt：description 102、body 71 行、VERDICT ready to upload）；demo/G1/attempted-SKILL.md 第 28 行；M2（12 行）｜2026-10-21｜risk-g1
c76｜答案句：它平常只看封面，要用才翻開｜c21、c24 的出處｜2026-10-21｜closing

站主觀點（標成「這個頻道的做法／門檻」，不是站主自己的經歷）：「交代到第三次就寫成說明書」（three）、「看不懂的那一頁就不裝」（risk）；第 2、3 點落在 cover-rule、appendix-choose 的選擇規則，那兩處另有 c11、c61 的出處。

## 示範紀錄（輸入、動作、預期、實際、證據）

| 示範 | 輸入 | 動作 | 預期（brief） | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| 主例 CS | shelf5＋book-lean，skill-auto.txt | `runs.sh CSa/CSb/CSc`（acceptEdits） | 至少 2 次翻開 signup-check，B1、B4、B5 過 | 3／3 翻開，B1–B6 6／6，18 個 Email，報名表雜湊不變 | runlog CS 三段、總表 |
| 簡單做法 CP | shelf5＋appendix-loose，paste.txt（309 字） | `runs.sh CPa/CPb` | B1、B4、B5 過 | 6／6；沒有翻開任何一本 | 總表 |
| 最接近的內建功能 CM | shelf5＋claude-md-book＋appendix-loose，skill-auto.txt | `runs.sh CMa/CMb` | B1、B4、B5 過 | 6／6 | 總表 |
| 控制組 CN1 | 只有 shelf5，skill-auto.txt | `runs.sh CN1` | 照實記 | 6／6（照第一批推出做法） | 總表、demo/CN1/reply.md |
| 封面 CV | shelf5＋book-vague | `runs.sh CVa/CVb/CVc` | CV 比 CS 少 2 次以上才成立 | 3／3 翻開 checklist：成果 3 降級 | 成果 3 的 NOTE |
| 大小 L 組 | 五種書櫃，time.txt | `runs.sh L0a…LMb`（manual） | LF≈L1；LM−L0 對 L1−L0 | LF−L1 最大 3；+77、+75.5、+422.5、+462 | 總表 first= means |
| 附件 CF | shelf5＋book-fat | `runs.sh CFa/CFb/CFc` | growth 比 CS 大、平均差 ≥300 | +1,288×3 對 +436～+487，平均差 835 | 成果 4 (b) |
| 自己的一行 W1 | shelf5＋book-mine | `runs.sh W1a/W1b` | M1–M4 至少一次全過 | 兩次 M1–M5 全過 | mine.mjs 段落 |
| 附件寫上位置 W2（事後加跑） | shelf5＋book-loc（book-mine 只改第 17 行），skill-auto.txt | `runs.sh W2a/W2b`（acceptEdits） | 部門對照讀到 | 2／2 第一個指令就讀到；B1–B6 6／6、M1–M5 5／5 | runlog Item W2 (added)、Unexpected 2b |
| 叫它寫 G1 | 沒有書櫃，write-skill.txt | `runs.sh G1` | 寫出一本，cover-check 判定 | 寫入被擋、沒有檔；想寫的內容 102 字介紹、71 行內文 | G1 段落與兩條 NOTE |
| 打包 M4 | book-lean | `node zip.mjs` | 對的第一層是 signup-check/ | 同預期 | M4 |
| 上傳 | — | 引用支援文章與公開頁 screencast | — | 沒有登入、沒有上傳 | c64 |

## 與企劃不同的地方

- 開場不用企劃第 4 句「封面沒寫好，AI 連翻都不會翻」：CV 3／3 翻開，成果 3 降級。開場的意外改用執行紀錄裡沒有預料到的「點名的附件 8 次裡 5 次找不到」（Unexpected 2），在第 6 章回收，並用來寫附件章的做法。
- 開場第 2 句的天真問題改成「Skill，不就是把一段提示存起來，下次再貼嗎？」：企劃那句「那是寫程式的人在用的吧」跟上一支的開場同一個意思。
- 第 4 章照成果 3 降級的條件寫：「這次含糊的也翻開了三次」，封面寫法靠引用（疑難排解、規格好壞例），數字只講封面大小與省下的 61 token。
- 第 5 章照成果 1 的條件逐字講「三種交代方式結果一樣」「這一批它不靠說明書也猜得到」，主例的差別只講 309 對 33 字、462 token、帶得走（引用）。
- 第 3 章不放官方的六種用途清單（為了片長）；「每一份報名表裡都有一筆叫測試」的玩笑移到第 5 章第三步。
- G1 照實講成「叫它寫可以當草稿」，結果是寫入被擋、它想寫的內容把部門對照寫進內文；不跑 G2（紀錄沒跑）。
- 附件章多一段「改一行就找到」：企劃沒有這組 session；協調者事後加跑 W2a、W2b（只改第 5 步第 17 行，寫上附件位置），結果 2／2 讀到。附件章因此以「八次裡五次找不到」開場、以這一行的修正收尾（appendix-fix、appendix-fixed、appendix-cmd）；「附件怎麼點名」的第 1 點改成實跑，第 2、3 點仍引規格頁與支援文章。
- 第 7 章的「網頁版跟 Claude Code 會不會同步」沒有寫成不確定：兩份頁面的說法其實相容（網頁版→Claude Code 單向同步；資料夾裡的不會上網頁版），所以照兩邊的事實講。不確定的「我」只用兩句：免費版方案、中文選單名。
- 「上一支」只回呼一次（第 1 章第一句）；少了 name 的那一本在旁白裡不說是上一支的，卡片出處寫「左：前一支的檔」。
- 選項 A 的 stats「46 個工具」：撰稿日數成 45，查核 1 照頁面上 46 筆改成 46。
- 片長估 15.7 分鐘，超過 target_minutes [9, 12] 的上限。

### 修訂 1（2026-10-21，盲評 8／13 之後）

- no_spoiler：開場的兩個結果停在數字前。2u43 改成「寄信名單補上了新人」，74qp 改成「它點名的那頁附件，它回你：找不到。」；十六變十八第一次說在 5bjj（新 loop 2u43 → 5bjj），八次裡五次第一次說在 fag8／ug7s。開場的 stats 卡數字不動。
- no_recap／one_line：四百六十二只留 xyia，gwue 改成回呼「前面那筆常駐的量」；「八次讀到三次」只留 fag8，rw2t 改成 W1 的 0／2；六十九只留在卡片上（za92、vee6 改寫）；掃過全片，兩個字以上的數字都只說一次。
- one_thread：好壞封面的旁白改用 signup-check 的兩句對 checklist 的「檢查用的步驟。」（rvj7、sry6）；卡片仍是規格頁的 PDF 例子，當引用的出處。
- no_detour：ChatGPT、Codex 那一章併進上傳章：clients 場景拿掉章名，只留兩句（標準與四十六個工具；ChatGPT 和 Codex 也在清單上）；chatgpt 場景刪除（is8w、tvg4、28ea、u9ih），細節移到說明欄；dnqy 移到風險章第一句。
- 02:44–03:29 的節奏：旁白只說三個 token 數（七十七、四百二十二、四百六十二），三萬三千八百、七十五、每本七十、規格的一百只留在卡片上（a4xv、za92「幾乎沒差」、5msh、ksu8）；h69p 只說二十八。「我」仍是五句。

### 修訂 2（2026-10-21，盲評第二輪 9／13 之後）

- no_spoiler：74qp 改成停住的問句「可是它點名的那頁附件，它找得到嗎？」，「找不到」第一次出現在附件章（ug7s）；2wav 回呼改成「開頭問的那頁附件」；loop 74qp → 2wav 保留。開場 stats 卡的「5／8 它說找不到」沒動（卡片事實不改）。
- one_line：rvj7 改成回呼「壞的，就是剛剛那句。」，好例由 sry6 講。
- no_recap：結尾答案句 2x29 改成「一本說明書，平常只有封面在對話裡，翻開才算。」
- one_thread：風險章改用 G1 想寫的那一本當「別人寫的那一本」：新場景 risk-g1（bullets，章名移到這裡；dnqy、新句 kxdt、9hed），原 risk 場景的規則與「看不懂的那一頁就不裝」照留（c79）。
- 節奏：第 2 章旁白只說七十七、四百六十二兩個 token 數；5msh 改「差不多就是六個封面」，mrna 改「本來就有二十幾本」，h69p 不說二十八；pusc、ugm9 拿掉「比喻在這裡要小心／又對不上了」，比喻停止對應的地方各用一句平鋪的事實講。
- 之後 cards 的 kicker「比喻對不上的地方」沒改（畫面文字）。

### 修訂 3（2026-10-21，站主看第一支成片：「砍量測、改教動作」；teaching-flow §九）

旁白改成每章教動作、每個動作接一句執行裡發生的事；量測的數字與次數搬到卡片的來源欄與說明欄「怎麼跑的」。量測族的句子只留三句：ccaw（含糊的封面它照樣翻開，所以封面寫給人看）、fag8（只寫檔名，八次裡五次找不到）、w2pw（寫上位置，第一個指令就讀進來）。每章唸出的數字最多兩個（第 2 章只唸七十七、四百六十二）。估計 15.9 → 12.9 分鐘。

拿掉的場景：time-ask、shelf-count、run-steps、differences、g1-result、appendix-fixed（卡片連同旁白；數字進說明欄）。

不再被旁白或畫面用到的主張（留在本檔當紀錄，說明欄仍寫到的標「說明欄」）：
- c15 問時間的那一句與 16:30（time-ask 刪除）
- c23 書櫃 22／23／28（shelf-count 刪除；說明欄寫 22）
- c27 （修訂前就刪）
- c41 CSa 依序做了什麼（run-steps 刪除）
- c45 CN1 是看第一批推出做法（說明欄：「這一批它不靠說明書也猜得到」）
- c73 ChatGPT／Codex 照介紹自己挑（修訂 1 起不講）
只從旁白拿掉、卡片仍顯示的數字：c16、c18、c19（size-table 的 33,861、+75.5、+422.5）、c30（61 token）、c42、c43（run-stats）、c44（four-ways 的 6／6，旁白只剩一句「結果一樣」）、c53、c54（fat 卡的 +77、+1,288 等；旁白說「重上好幾倍」）、c57（appendix-miss 的 3／8；旁白說「八次裡有五次」）。

留下的主張各自撐的是哪個動作或事實：
- c1–c2 開場的比喻與用途；c3–c5 開場的結果卡（旁白只說「它就自己翻開」「補上了新人」「找得到嗎？」）；c6 開場的問題「找不到時停下來還是猜」與 4m2k 的回答。
- c7–c14 第 1 章的動作：開資料夾（c7）、寫名字與兩句介紹（c9–c12）、少了 name 的坑（c13、c14）；c8 回呼上一支一句。
- c17、c20、c21、c22、c24、c25 第 2 章的選擇：一本封面七十七（c17）、CLAUDE.md 四百六十二（c20）、平常只看封面（c21）、每次來回封面都送進去（c22，比喻停止對應一句）、CLAUDE.md／專案指示一直帶著（c24、c25）。
- c26 第 3 章五本的寫法；c28、c29 含糊封面照樣翻開（ccaw）；c31–c34 封面寫法與格式檢查的坑。
- c35–c40 第 5 章七個步驟、兩個王志明、測試二、「才」字、那一句要求與它第一件事就翻開；c42 名單十六變十八（5bjj）；c44、c46 那一句結論「結果一樣」與差別。
- c47–c49 第八步與它多寫出的待回覆；c50、c51 叫它寫一本與寫入被擋（j4wr、5jsg）。
- c55、c56 附件放旁邊用不到就不讀、翻開後留在對話、改了不重讀；c58、c59、c6 找不到的原因與它自己猜；c60、c77、c78 改一行寫上位置、第一個指令就讀進來；c61 怎麼選。
- c62–c70 壓縮與上傳、選單名的不確定、上傳失敗四件事與兩百字、方案的不確定、同步；c71、c72 四十六個工具與 ChatGPT、Codex 在清單上。
- c52、c79 風險章打開 G1 那一本；c74、c75 資料夾可夾程式、只裝信得過的；c76 結尾。

## 我懷疑但沒動的事

- step8-result 已拆成兩個狀態（各約 7–8 秒）；最長的狀態是 body-6、clients 的 13.3 秒，加 7% 約 14.2 秒，在 15 秒內。
- 寫上位置的修正只跑了 2 次（W2a、W2b），而且兩次都用 Bash cat 讀，不是 Read；樣本小，卡片標了「之後加跑的兩次」。
- 怎麼把資料夾壓成 ZIP（Windows 右鍵「壓縮成 ZIP 檔」、Mac「壓縮」）沒有上卡：紀錄只有 zip.mjs，官方頁沒寫作業系統的做法。觀眾若真的要照做，這一步缺一張卡。
- 「Settings › Capabilities」與「Customize › Skills」是支援文章的英文名；網頁版實際介面沒看過。
- 第 2 章 time-ask 的回覆卡用 L1a（書櫃上只有 signup-check 一本），旁白說「signup-check 上了書櫃」，對得上；但 L 組是 manual 模式，C 組是 acceptEdits，兩組的 token 數不互比。
- 「CLAUDE.md 問什麼都帶著 462」是從問時間的 L 組量的；C 組 CM 的 first= 34,669–34,671 也比 CN1 多 460 上下，方向一致，沒有另外上卡。
- run-steps 第 2 步寫「三個指令被擋下」：CSa 的三次拒絕分散在讀檔與寫檔之間（第三次是 cd＋重導向寫檔），卡片位置是概略的。
- 說明欄建議連一篇站內文章（brief：撰稿時選一篇）；這份沒設 `source_guide`（發動訊息說沒有來源文章），候選是 `claude-skills-explained`，由協調者決定。
- 發音字典的 11 個新詞寫在 lexicon-additions.json，沒動 lexicon.json；`null` 的那幾個要試聽確認。

## 進度

- 修訂 3 之後 61 個場景、11 章，loops 24 條（新增 3a7t → 4m2k）。video.json 直接改（revise1.mjs、revise2.mjs、revise3*.mjs；逐句前後對照在 `<work>/_tools/writer/revise3.log`）。
- lint：0 錯誤、0 警告（發音字典的新詞已由協調者併入）。
- 估計 12.9 分鐘、134 句、2,881 口語單位；最長的卡片狀態估 13.3 秒（body-6）。
