# Skill 就是一本說明書：封面、內文、附件，自己寫一本「報名表檢查」，再放進 Claude

企劃日 2026-10-21（台北時間；官方頁在 UTC 2026-10-20 18:06–18:14 抓的，原檔存在 `<work>/_tools/pages/`）。這份企劃寫在任何會呼叫模型的 session 之前：說明書、練習資料夾的追加檔、讀串流的腳本、封面檢查、打包腳本，企劃已經用不呼叫模型的指令跑過（見「示範或實算」的 M 項）；會呼叫模型的 session 一次都還沒跑。大綱裡寫到 session 結果的句子與數字都是預期，等「要先實作」做完照執行紀錄改；跑不出來的成果那時拿掉。`<work>` 是 repo 外的影片工作區 `<work>`，`T=<work>/_tools`。

## 觀眾

- 誰：跟上一支〈Claude Code 新手教學〉同一群人：上班族、行銷、活動企劃、小店老闆。在網頁或手機上用 ChatGPT 或 Claude 問問題、改文案；不寫程式。看過上一支的人知道講座籌備/ 這個資料夾，也看過有人用 `/signup-check` 檢查第二批報名表；沒看過的人也跟得上，例子在第一章重新交代。
- 已經會：把一段要求貼進對話框；有的人在網頁版的「專案」裡放過常駐指示，或在 Claude Code 寫過 CLAUDE.md。
- 還不會：把「每次都要交代一遍」的一套步驟寫成一個檔、讓 AI 自己在需要時拿出來用；看不出為什麼自己寫的 Skill 沒被用；不知道哪些內容該放進 SKILL.md、哪些放旁邊；不知道怎麼打包上傳到 Claude 網頁版。
- 搜尋的問題：「Claude Skill 是什麼」「Skill 怎麼寫」「SKILL.md 怎麼寫」「Claude 自訂技能 上傳」「Skill 沒有觸發」「Agent Skills 不會寫程式」「ChatGPT Skill」。
- 跟前幾支的差別：上一支（`claude-code-beginner-event-folder`）是「用」：一個寫好的 `/signup-check`、四個基本功、講座從頭整理一遍，開場是「這不就是給工程師用的 Claude 嗎」的天真問題；〈Skills 對 CLAUDE.md〉是給開發者的量測片，例子是發版流程，開場是「搬過去沒有更照做」；〈CLAUDE.md 實作〉是三行慣例跑六次。這一支是「寫」：一個比喻撐全片，教的是那一本說明書本身（封面怎麼寫、內文放什麼、附件放什麼、怎麼打包），量的是觀眾自己看不到的兩件事：沒翻開時它占多少、翻開之後它占多少；開場不是天真的問題，是說明書的封面沒寫好、AI 不翻開。上一支的章節（四個基本功、實戰、家教）、開場與卡片順序都不重複，只在第一章回呼一句。

## 觀眾看完能做到的事

1. **從零寫一本 `signup-check` 說明書（兩行封面、七步內文、兩頁附件），放進講座資料夾的 `.claude/skills/`，之後只說「第二批報名表來了，照平常的方式檢查一下」，它就自己翻開這一本，把兩個新人加進寄信名單、把缺 Email 的宋柏均列進要補資料。** 對象：`講座籌備/.claude/skills/signup-check/`（SKILL.md 20 行全文上兩張卡，附件兩頁各一張節錄）。怎麼知道做對了：串流裡有一筆點名 `signup-check` 的 Skill 呼叫（`skillview.mjs` 的 `VERDICT opened signup-check: YES`）；`batch2.mjs` 的 B1、B4、B5 都過（寄信名單 18 個不同的 Email）；同一句短要求在書櫃上沒有這一本時（CN1）照實比。證明：示範 CSa–CSc（各 1 次），對照 CPa–CPb（每次把七步貼進要求）、CMa–CMb（七步放在 CLAUDE.md）、CN1（沒有任何交代）。級別：跑過（待 CSa–CSc、CPa–CPb、CMa–CMb、CN1）。更高一級（看過）是桌面版 Code 分頁裡同一件事的畫面，這裡不能登入、不列。
2. **把說明書裡代表自己情況的那一行改掉，重跑一次確認：加上第 8 步「想改線上參加的，另外列進 輸出/待回覆.csv，寫下他問了什麼；不要自己回答」，第二批裡問能不能改線上的黃雅婷就出現在待回覆，而且沒有被重複加進寄信名單。** 對象：同一本的第 8 步（兩行，卡片上亮起來）。怎麼知道做對了：`mine.mjs` 的 M1–M4 都過（待回覆.csv 存在、有黃雅婷、寫了「線上」、寄信名單裡她只出現一次）。證明：示範 W1a、W1b。級別：跑過（待 W1a、W1b）。
3. **把封面寫成 AI 翻得開的兩句（做什麼＋什麼時候用，用你平常會說的話），並且用「同一句話跑三次、數它翻開幾次」確認。** 對象：同一本內文，兩種封面：含糊的「檢查用的步驟。」（名字 `checklist`）對寫清楚的兩句（名字 `signup-check`），書櫃上另外放五本別的說明書（講者介紹、會議紀錄、報帳、活動文案、行前提醒）。怎麼知道做對了：三次裡翻開幾次（官方的判讀門檻是超過一半，agentskills.io 的 optimizing-descriptions 頁）；翻開的是不是那一本、還是翻成行前提醒那一本。證明：示範 CSa–CSc 對 CVa–CVc。級別：跑過（待 CSa–CSc、CVa–CVc）。
4. **判斷一段內容該寫進 SKILL.md 還是放成附件，並讀出差多少：確認信範本與部門對照這種「偶爾才用」的內容，放進內文時，說明書一翻開，之後每一次來回都帶著它；放成旁邊的附件，沒用到就不會被讀。** 對象：同一本說明書的兩種寫法：內文 20 行加兩頁附件（book-lean），對附件全部貼進內文的 69 行（book-fat）。怎麼知道做對了：（a）沒翻開的時候，兩種寫法開場的第一個請求一樣大（同一個問活動幾點結束的要求，LFa–LFb 對 L1a–L1b）；（b）翻開之後，69 行那一本讓翻開那一步多出來的量比 20 行那一本多，而且後面每一個請求都帶著（CFa–CFc 對 CSa–CSc 的 `skillview` growth 與 input side 序列）；（c）20 行那一本在檢查報名表時沒有讀確認信範本（`appendix reads`）。證明：示範 L、CF、CS 三組。級別：跑過（待 L0a–LMb、CFa–CFc、CSa–CSc）。

這四件以外：打包上傳到 Claude 網頁版是「留下來」的步驟，不是成果：資料夾怎麼壓（整個資料夾在 zip 的最上層，不是只壓檔案）用不呼叫模型的 `zip.mjs` 實際壓一次、讀回清單（M4），上傳本身引支援文章與它的公開頁截圖，卡片標「引用」。ChatGPT 與其他工具只引官方頁。

## 站主觀點

（提案，待站主選大綱時確認或改寫。這次的發動訊息沒有附頻道立場的原文，所以不寫「套用立場」那一行，也不沿用舊企劃的點號。四點與上一支企劃提案的四點相容：那一支的第 3 點「驗收看檔案、不看它說已完成」、第 4 點「每次都要的規矩寫進 CLAUDE.md，偶爾才做的整套步驟寫成 Skill」，這裡往下接。）

1. 同一套步驟我交代到第三次，就寫成一本說明書；每次都要遵守的規矩才放 CLAUDE.md 或專案指示。
2. 封面是寫給 AI 看的，不是寫給我自己看的：一句它做什麼，一句什麼時候用，用我平常真的會說的那句話寫。
3. 內文只放每一次都要照做的步驟；偶爾才用的範本、對照表放成附件。一本說明書翻開之後，整本都留在那次對話裡。
4. 別人給的說明書，我整個資料夾打開看過一遍，才放上書櫃；看不懂的那一頁，就不裝。

依據：support.claude.com 的〈How to create custom skills〉（description 是 Claude 決定要不要用的依據；「Write clear descriptions… Be specific about when it applies」；附件放 REFERENCE.md 之類的檔、在 skill.md 裡點名）、〈Use skills in Claude〉（「Only install skills only from trusted sources」、裝之前讀過資料夾裡每一個檔）、〈What are skills?〉（Projects 與 custom instructions 是一直載入的，Skill 用到才載入）、code.claude.com 的 skills 頁（翻開後內容留在對話裡、「every line is a recurring token cost」；一直重貼同一段指示就做成 Skill）、agentskills.io 規格（SKILL.md 500 行以內、長的參考資料搬到別的檔）。第 1 點的「第三次」是頻道自己的門檻，不是官方數字；站主不同意就改。

## 示範或實算

製作路線：教學卡片

`category: "tutorial"`。`format: "slides"`，沒有 `shot`；畫面是 `code`、`table`、`compare`、`steps`、`stats`、`bullets`、`quote`、`big`、`chat` 卡片與公開官方頁的 `screencast`。沒有登入畫面、沒有 OBS、沒有假的終端機畫面，`terminal` 卡一張都不用（觀眾不開終端機；實跑的出處寫在卡片的來源欄：「實跑 2026-10-2x｜Claude Code 2.1.295，無介面 session」）。

### 一個比喻撐全片：Skill＝一本說明書（teaching-flow §六）

| 說明書的部位 | 對到的機制 | 在例子裡是什麼 | 證據 |
| --- | --- | --- | --- |
| 一本書 | 一個資料夾，裡面至少一個 `SKILL.md` | `.claude/skills/signup-check/` | 規格頁 |
| 封面 | `SKILL.md` 最上面的 `name` 與 `description` | `signup-check`；「檢查講座的新報名表…有新的報名表進來、或有人說『檢查報名』時用。」 | 規格頁；實跑看 init 清單 |
| 內文 | 封面下面的 Markdown | 七個步驟 | 實跑看翻開那一則訊息 |
| 附件 | 同一個資料夾裡的其他檔 | `部門對照.md`、`確認信範本.md` | 實跑看有沒有被 Read |
| 書櫃 | 開場時列出的技能清單（Claude Code 的 init 清單；網頁版的「自訂 › 技能」） | 六本：signup-check 加五本別的 | 實跑；網頁版引支援文章 |
| 翻開 | Skill 工具被叫、內文整段進入對話 | `Launching skill: signup-check` 那一行與緊接的那一則訊息 | 實跑 |

**哪裡不能照比喻理解**（全片講清楚，各一句，放在它發生的那一章）：
1. 真的說明書是你自己挑來翻；這裡是 AI 只看封面決定要不要翻、翻哪一本（第 4 章，CV 的結果）。
2. 真的說明書看完會闔上；這裡翻開之後整本留在那次對話裡，後面每一次來回都帶著（第 6 章，CF 的結果；skills 頁的 content lifecycle）。
3. 說明書不會自己動手；Skill 的資料夾可以夾小程式，AI 會去執行它（安全那一段；規格頁 `scripts/`）。
4. 你改了說明書，正在進行的那段對話不會重讀（skills 頁「does not re-read the skill file on later turns」；引用，沒有跑）。

### 主例子：講座籌備資料夾的第二批報名表

沿用上一支的虛構資料夾 `講座籌備/`（`make-seed.mjs` 原封不動複製過來，`reuse.sh` 逐檔比對雜湊）：一場 2026-11-14 的講座，第一批 24 列報名表已經整理好（這一支的起點是 `round1`：寄信名單 16 人、要補資料 3 人、處理日誌一份，就是上一支計分腳本寫死的標準答案，`selftest.mjs` 的 good 那一份）。第二批 `報名表_第二批.csv` 6 列：兩個新人（簡郁庭、邱品妍）、王志明重填一次、黃雅婷問能不能改線上參加、一筆「測試二」、缺 Email 的宋柏均。正確答案（`batch2.mjs` 寫死）：寄信名單 18 個不同的 Email；宋柏均進要補資料；王志明與黃雅婷不重複。沒動之前跑 `batch2.mjs`：B2、B3 過、B1、B4、B5、B6 不過（M6 記下）。

書櫃上另外五本（`shelf5`，各自一個資料夾、封面寫清楚、內文三到四步）：`speaker-intro`（講者介紹稿）、`meeting-notes`（會議紀錄）、`expense-receipts`（報帳明細）、`poster-copy`（活動文案）、`reminder-mail`（行前提醒信）。它們是真實的檔，也是第 3 章「拿來做什麼」那份清單的來源；`reminder-mail` 跟報名檢查最像（都碰確認信名單），是含糊封面那一組的干擾項。

### 觀眾要寫的那一本（全文，照這份上卡片）

`講座籌備/.claude/skills/signup-check/SKILL.md`（20 行；`sha256` 前 16 碼 `8331907e77181682`；卡片分兩張：封面 7 行一張、內文 13 行一張）：

```
---
name: signup-check
description: >-
  檢查講座的新報名表：可以寄確認信的加進名單，
  缺資料的另外列出，並寫處理日誌。有新的報名表
  進來、或有人說「檢查報名」時用。
---

# 報名表檢查

1. 讀新的報名表、活動說明.md 和 輸出/確認信名單.csv。
2. 同一個 Email 只留最後一次；同名但 Email 不同是兩個人。
   已經在名單上的 Email 不重複加。
3. 備註寫「取消」的人和測試資料，不放進寄信名單。
4. 沒有 Email 或格式不對的，加進 輸出/要補資料.csv。
5. 其餘加進 輸出/確認信名單.csv；部門寫法對不上時，
   照 部門對照.md 統一。
6. 素食、過敏、其他忌口各幾位，連同做了什麼，
   寫進 輸出/處理日誌.md。
7. 要寫確認信的時候，才照 確認信範本.md 寫。
```

觀眾改的那一行（book-mine，第 8 步，加在最後；SKILL.md 變 22 行，`6f8319939f194993`）：

```
8. 備註裡想改線上參加的，另外列進 輸出/待回覆.csv，
   寫下他問了什麼；不要自己回答。
```

附件兩頁（`部門對照.md` 14 行 `3ab7c23feaa0e84b`：五個部門各一列「報名表上可能寫 → 統一成」與兩條注意；`確認信範本.md` 33 行 `6e769db38145d3b6`：主旨、日期時間地點、交通、飲食、不能來的話、寫信時注意）。卡片各放一張節錄（部門對照的表頭與前兩列；確認信範本的主旨與前六行），說明文字寫全檔行數與它在資料夾裡的位置。

含糊封面那一本（book-vague）：資料夾與名字都是 `checklist`，description 只有「檢查用的步驟。」，內文與附件逐字相同（`daf1484a61ea5c64`）。附件全部貼進內文的那一本（book-fat）：封面相同，第 5、7 步改成「照下面的…」，後面接兩頁附件的全文，69 行（`c8fe7e57477ba580`）。同樣七步放在 CLAUDE.md 的那一份（claude-md-book，16 行，`be810c40ffccf9c6`），兩頁附件鬆放在資料夾裡（appendix-loose）。每次貼上的那一份要求（`prompts/paste.txt`，12 行）是「第二批報名表來了（報名表_第二批.csv），照下面的步驟檢查一下。」加同樣七步。

兩個檔的每一行都是自然語言，旁白照唸（〈含金量〉第 4 條；teaching-flow §二），檔名與路徑不唸、只說它是哪一頁。最寬一行 33 字，`code` 卡 64 字上限之內；放不放得下由出畫面那一步判定，放不下就照規則重排原檔、重跑。

名字的規則（規格頁）：只能小寫英文、數字和連字號，而且要跟資料夾同名；內文、封面的介紹句寫中文沒關係。上一支那一本沒有 `name` 那一行：Claude Code 允許（skills 頁：沒寫就用資料夾名），`claude plugin validate` 也過（M3）；但 claude.ai 上傳要求 `name` 與 `description` 都要有（支援文章），`cover-check.mjs` 對它判「fix before upload」（M2）。這是觀眾從上一支拿到那一本、想上傳網頁版時會踩的坑，第 7 章一句。

### 不用這個方法：…

- **主例子（寫一本說明書）**：觀眾今天最快的做法是**一句普通的提示**：每次把七個步驟貼進要求（CPa–CPb，`paste.txt`）。觀眾裡用過 Claude Code 的，第二個做法是**產品最接近的內建功能**：把七步留在 CLAUDE.md（CMa–CMb；網頁版對應的是專案的常駐指示，支援文章〈What are skills?〉寫明專案是「always loaded」，網頁版本身這裡不能登入、不跑，只引一句）。三邊用同一份第二批報名表、同一個書櫃。預期（等紀錄確認）：三邊都能把第二批檢查對（B1、B4、B5），差別在：（a）貼上那一邊每次要多打 310 字的要求（`paste.txt` 310 字、706 位元組，對 `skill-auto.txt` 34 字、90 位元組；M1 的 `wc -c` 記位元組，字數是企劃用 node 數的），而且觀眾得自己留著那段文字；（b）CLAUDE.md 那一邊不管今天做什麼都帶著七步，同一個問「幾點結束」的要求，第一個請求比沒有交代多 LM−L0 個 token，說明書那一邊只多封面的 L1−L0 個（成果 4 的 L 組）；（c）只有說明書那一邊能整個資料夾壓成 zip 帶去 Claude 網頁版（引用；CLAUDE.md 是 Claude Code 才讀的檔）。片中照量到的講：三邊結果一樣就說一樣，差在你要不要每次貼、它要不要每次帶。
- **控制組**：書櫃上沒有這一本、也沒有貼步驟、只說那句短要求（CN1，1 次）。用來證明 CS 的結果是說明書造成的；CN1 也做對的話照實講「這一批它自己也猜得到」，主例的差別只剩上面的（a）（b）（c）。
- **封面（成果 3）**：不用這個方法就是「隨手寫一句」：CVa–CVc。
- **附件（成果 4）**：觀眾直覺的做法是「全部寫進同一個檔，比較不會漏」：CFa–CFc。

### 猜不到的結果（企劃時的候選，照紀錄定案）

1. **69 行跟 20 行，沒翻開前一樣大**（LF 對 L1）：封面相同，開場的第一個請求應該差不到同一組兩次之間的差距。多數人會以為寫越長、每次越貴。這一項最可能成立，是選項 A 第 2 章的轉折。
2. **封面寫「檢查用的步驟」，三次裡沒翻開、或翻成行前提醒那一本**（CV）：要是發生，這是選項 B 的開場。前一支〈Skills 對 CLAUDE.md〉量過「含糊的也三次都被叫到」（那次書櫃上只有一本、名字叫 release-prep 本身就點題），所以這次刻意把名字也弄含糊、旁邊放五本；仍可能三次都翻開，照實記。
3. **翻開之後一直帶著**（CF 對 CS）：69 行那一本在翻開那一步多出來的量，後面每一個請求都還在。
4. **書櫃從來不是空的**（L0 的 init 清單）：這台機器上的 Claude Code 在沒有放任何一本時，清單裡已經有幾本內建的（上一支 c1 的串流列了 22 本）；數字照 L0 的紀錄講，卡片標「這台機器」。
開場或主例的轉折用證據最強的那一個：CV 有 2 次以上沒翻開 `checklist` 就用第 2 項開場（選項 B），否則用第 1 項當第 2 章的轉折、第 3 項當第 6 章的轉折（選項 A）。

### 「我」的句子從哪裡來（teaching-flow §五）

只用這支片的執行紀錄與真的查不到的事；不編站主的經歷，不寫「很多人跟我說」。

| 句子（預期寫法，數字照紀錄） | 來源 |
| --- | --- |
| 「我在書櫃上放了一本、又放到六本，開場那一下各多了 X 跟 Y 個 token，內文一個字都沒算進去。」 | L1−L0、L6−L0 的 `first=` |
| 「我把同樣七步改放在 CLAUDE.md，問一句幾點結束，它每次都多帶 Z 個。」 | LM−L0 |
| 「封面寫『檢查用的步驟』那一本，我跑了三次，它翻開了 N 次。」 | CVa–CVc 的 `VERDICT opened checklist` |
| 「69 行那一本，一翻開就多了 W 個 token，後面 K 個請求都帶著。」 | CFa–CFc 的 growth 與 `requests carrying it` |
| 「免費版能不能上傳自己寫的，兩份官方頁寫的不一樣，我沒辦法替你確定。」 | 不確定：support〈Use skills in Claude〉列 Free；platform overview 的 claude.ai 一節只列 Pro、Max、Team、Enterprise |
| 「ChatGPT 網頁版能不能直接上傳一本，我在官方頁上沒找到；寫明的是桌面版的側邊欄，和外掛裡帶的。」 | 不確定：learn.chatgpt.com/docs/build-skills |
| 「中文介面上那幾個選單叫什麼，我只查到機器翻譯的說明頁，你自己看一眼『自訂』底下。」（可選） | 不確定：zh-TW 支援文章是「設置 > 功能」「自定義 > 技能」，跟台灣介面用字未必一樣 |

共同經驗的玩笑一句：「每一份報名表裡，都有一筆叫『測試』」——第二批真的有一筆「測試二」。（「最終版、真的最終版」上一支用過，這支不用。）

### 已經跑過的（不呼叫模型；協調者照「要先實作」M 項重跑一次寫進紀錄）

| 項 | 輸入 | 動作 | 預期 | 企劃這次看到的 |
| --- | --- | --- | --- | --- |
| M0 版本 | 這台機器 | `claude --version`、`node --version` | 2.1.295；v24 | `2.1.295 (Claude Code)`、`v24.13.0` |
| M1 沿用與建檔 | 上一支的 `_tools` | `bash reuse.sh`、`node make-seed.mjs`、`node make-booklets.mjs` | 九個沿用檔兩邊雜湊 `same`；`seed written: 13 files`；`booklets written: 24 files` | 同左；雜湊清單見「要先實作」M1 |
| M2 封面檢查 | 四種寫法與上一支那一本 | `node cover-check.mjs …` | 這支四本 `ready to upload`；上一支那一本 `fix before upload`（沒有 name） | 同左；description 60 字（含糊的 7 字），內文 12／61／12／14 行 |
| M3 Claude Code 的驗證 | 三個 skills 資料夾 | `claude plugin validate …` | 三個都 `✔ Validation passed`（含糊的與沒有 name 的也過：它驗格式，不驗封面寫得好不好） | 同左 |
| M4 打包 | book-lean 那一本 | `node zip.mjs …` | 對的 zip 第一層是 `signup-check/`，錯的三個檔散在最上層；中文檔名讀得回來 | 對的 2271 位元組、錯的 2193 位元組；Windows 內建的 .NET ZipFile 讀得開（企劃另外確認）。`tar.exe` 在 Git Bash 裡直接崩潰，所以不用它 |
| M5 讀串流的腳本 | 另一支片（plugins）已經跑過的一個串流 | `node skillview.mjs …/k1.stream.jsonl --expect release-prep` | 書櫃、請求大小、翻開那一筆、那則訊息的長度 | `shelf: 23`、`requests 5`、`opened … tool_result="Launching skill: ship-kit:release-prep"`、`booklet text: 513 chars, 18 lines`、`request 1 -> 2: 11353 -> 12602 (+1249)`、`VERDICT … YES` |
| M6 空跑與起點 | `runs.sh <id> --dry` 十三種組合 | 建出資料夾、印出指令、不開 session；再對起點跑 `batch2.mjs`、`mine.mjs` | 每組 `[dry run: no session was started]`；起點 B2、B3 PASS，其餘 FAIL；mine 只有 M4 PASS | 同左 |
| M7 沿用的計分自測 | `selftest.mjs` | `node selftest.mjs` | good 10/10 RIGHT；bad 2/10 WRONG | 同左 |

### 要先實作

協調者照順序做，每一項的指令、輸出、日期、版本寫進 `docs/videos/claude-skill-manual-event-folder/runlog.txt`。所有指令在 Git Bash 執行；`T=<work>/_tools`。每一個會呼叫模型的 session 都經 `runs.sh <id>`，它呼叫沿用、一字未改的 `session.sh`，固定帶這些旗標：`env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 timeout 600 claude -p --model sonnet --setting-sources project,local --strict-mcp-config --no-session-persistence --permission-mode <模式> --output-format stream-json --verbose`，要求從 `prompts/` 的檔案經 stdin 送進去，工作目錄是 `<work>/run/lab/講座籌備`（每次從種子重建，再疊上那一組的 extras）。`session.sh` 寫下前後雜湊、串流摘要（`inspect.mjs`）、`score.mjs`、`versions.mjs`、`batch2.mjs`，並把資料夾留在 `<work>/run/snap/<id>/`；`runs.sh` 再把 `skillview.mjs`（書櫃、請求大小、翻開了哪一本、那則訊息多長、讀了哪一頁附件）與 `mine.mjs`／`cover-check.mjs` 的結果接在同一份 `<work>/run/logs/<id>.session.log` 後面。同一個 id 跑過就拒絕，不覆蓋；`--dry` 用 `dry-<id>` 的名字，不擋正式的那一次。

**M0 版本**
```
claude --version
node --version
bash --version | head -1
```
預期 `2.1.295 (Claude Code)`、`v24.13.0`。版本不同就照實記下，往下照跑；第 L 組與第 C 組必須同一天、同一版本跑完（token 數會跟版本與系統提示變）。

**M1 沿用與建檔**
```
cd "$T"
bash reuse.sh
node make-seed.mjs
node make-booklets.mjs
(cd seed/extras && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
sha256sum prompts/*.txt make-booklets.mjs skillview.mjs cover-check.mjs zip.mjs mine.mjs runs.sh reuse.sh | cut -c1-16,65-
wc -c prompts/paste.txt prompts/skill-auto.txt
```
預期：`reuse.sh` 九行都是 `same`（session.sh `df015a8fc377a8f1`、inspect.mjs `a52aa90e65b4f178`、score.mjs `ac27b10ad1296b77`、versions.mjs `49f55f5b33666cdf`、batch2.mjs `cd44eba22329ea57`、make-seed.mjs `ddac495c070d109e`、selftest.mjs `b919f557ef9f6cdb`、skill-auto.txt `0dbbb6e005e08d79`、skill-slash.txt `27602d1fa5299756`）；`seed written: 13 files`；`booklets written: 24 files`。extras 雜湊前 16 碼：
```
6e769db38145d3b6 ./appendix-loose/確認信範本.md
3ab7c23feaa0e84b ./appendix-loose/部門對照.md
d93be0d8338f8802 ./batch2/報名表_第二批.csv
c8fe7e57477ba580 ./book-fat/.claude/skills/signup-check/SKILL.md
8331907e77181682 ./book-lean/.claude/skills/signup-check/SKILL.md
6e769db38145d3b6 ./book-lean/.claude/skills/signup-check/確認信範本.md
3ab7c23feaa0e84b ./book-lean/.claude/skills/signup-check/部門對照.md
6f8319939f194993 ./book-mine/.claude/skills/signup-check/SKILL.md
6e769db38145d3b6 ./book-mine/.claude/skills/signup-check/確認信範本.md
3ab7c23feaa0e84b ./book-mine/.claude/skills/signup-check/部門對照.md
daf1484a61ea5c64 ./book-vague/.claude/skills/checklist/SKILL.md
6e769db38145d3b6 ./book-vague/.claude/skills/checklist/確認信範本.md
3ab7c23feaa0e84b ./book-vague/.claude/skills/checklist/部門對照.md
be810c40ffccf9c6 ./claude-md-book/CLAUDE.md
8e865483370aa2d4 ./claude-md-specific/CLAUDE.md
4195c05ae132e13a ./claude-md-vague/CLAUDE.md
966f4ed5c223cfe3 ./round1/輸出/確認信名單.csv
95fcb98985d636d8 ./round1/輸出/處理日誌.md
1c43338f5d7e860f ./round1/輸出/要補資料.csv
b56a76b9edece3ff ./shelf5/.claude/skills/expense-receipts/SKILL.md
f5f0a096da1f9e67 ./shelf5/.claude/skills/meeting-notes/SKILL.md
214d5c6778a5c72b ./shelf5/.claude/skills/poster-copy/SKILL.md
fd93bcc0567ef08c ./shelf5/.claude/skills/reminder-mail/SKILL.md
36feb180130c8dab ./shelf5/.claude/skills/speaker-intro/SKILL.md
cf53f2c9bcd4faf6 ./skill/.claude/skills/signup-check/SKILL.md
```
prompts：`paste.txt 140e6178411ac8fa`、`time.txt 8cd705264d5173a3`、`write-skill.txt 392e0a4e75979d48`；腳本：`make-booklets.mjs eb59e2e044957a72`、`skillview.mjs ea1bf03a993c32d2`、`cover-check.mjs 15d713a4b4978e75`、`zip.mjs d823177f0fbede6d`、`mine.mjs 4a47837fff036b69`、`runs.sh 94355f1626960be2`、`reuse.sh efd2666d5a3570a9`。不一樣就停下來，先查是誰改了檔。

**M2 封面檢查**
```
E="$T/seed/extras"
node "$T/cover-check.mjs" "$E/book-lean/.claude/skills/signup-check" "$E/book-fat/.claude/skills/signup-check" "$E/book-vague/.claude/skills/checklist" "$E/book-mine/.claude/skills/signup-check" "$T/../../claude-code-beginner-event-folder/_tools/seed/extras/skill/.claude/skills/signup-check"
```
預期：前四本 `VERDICT ready to upload`（signup-check 的 description 60 字，200 字上限內）；上一支那一本兩行 `FAIL name …` 與 `VERDICT fix before upload`。

**M3 Claude Code 自己的格式驗證**（不呼叫模型，需要 v2.1.233 以上）
```
claude plugin validate "$E/book-lean/.claude/skills"
claude plugin validate "$E/book-vague/.claude/skills"
claude plugin validate "$T/../../claude-code-beginner-event-folder/_tools/seed/extras/skill/.claude/skills"
```
預期三個都 `✔ Validation passed`。這給第 4 章一句「驗證通過，只代表格式對；封面寫得好不好，它不管」。

**M4 打包**：`node "$T/zip.mjs" "$E/book-lean/.claude/skills/signup-check" "$T/pack"`。預期 `signup-check.zip` 三筆都以 `signup-check/` 開頭、`signup-check-wrong.zip` 三筆在最上層；兩個 zip 都留在 `<work>/_tools/pack/` 給撰稿看。這是「留下來」那一步的唯一實跑；上傳本身引用。

**M5 讀串流的腳本自測**：`node "$T/skillview.mjs" "$T/../../claude-code-plugins-hands-on/run/logs/k1.stream.jsonl" --expect release-prep`。預期同上表 M5 那一列。

**M6 空跑與起點**
```
for id in L0a L1a LFa L6a LMa CSa CVa CN1 CPa CMa CFa W1a G1; do bash "$T/runs.sh" $id --dry | tail -1; done
ls -a "$T/../run/lab/講座籌備/.claude/skills"     # 最後一組 G1 沒有書櫃：預期找不到這個資料夾
bash "$T/runs.sh" CVa --dry > /dev/null; ls "$T/../run/lab/講座籌備/.claude/skills"   # 預期 checklist 加五本
node "$T/batch2.mjs" "$T/../run/lab/講座籌備"; node "$T/mine.mjs" "$T/../run/lab/講座籌備"
```
預期每組 `[dry run: no session was started]`（`session.sh` 這時才建出 `<work>/run/`，企劃跑完空跑後把它刪了，讓協調者從空的開始）；起點 `B2 PASS`、`B3 PASS`、其餘 FAIL、`unique addresses … 16`；mine 只有 M4 PASS。

**M7**：`node "$T/selftest.mjs"`。預期 good `score: 10/10`、`RIGHT`；bad `score: 2/10`、`WRONG or edited`。

下面每一項都是 `bash "$T/runs.sh" <id>`；表裡的「書櫃與資料夾」就是 `runs.sh --list` 那一欄的 extras（每組都有 round1 與 batch2）。順序照表跑：L 組先、C 組 CS 與 CV 交錯，全部同一天。會呼叫模型的共 26 次（L 10、CS／CV 6、CN 1、CP 2、CM 2、CF 3、W 2），另有可選的 G1、G2 兩次，另留 2 次備用；全部 sonnet。

| 項 | id | 模式 | 要求 | 書櫃與資料夾 | 預期與怎麼認出來 | 給哪一件 |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | L0a、L0b | manual | `time.txt`：活動說明.md 寫的講座幾點結束？只回答時間，不要改任何檔案。 | 沒有任何一本、沒有 CLAUDE.md | `skillview` 的 `first=`（開場第一個請求的大小）、`shelf:` 本數與清單（「書櫃本來就有幾本」）；`opened: none`；回覆是 16:30 | 成果 4 的基準；猜不到的結果第 4 項 |
| L1 | L1a、L1b | manual | 同上 | book-lean | `first=`；`shelf` 比 L0 多一本 `signup-check`；`opened: none` | 成果 4（封面的大小＝L1−L0） |
| LF | LFa、LFb | manual | 同上 | book-fat | `first=` 與 L1 比；`opened: none` | 成果 4（a）；猜不到的結果第 1 項 |
| L6 | L6a、L6b | manual | 同上 | shelf5＋book-lean | `first=`；`shelf` 多六本 | 第 2 章「放到六本」 |
| LM | LMa、LMb | manual | 同上 | claude-md-book＋appendix-loose | `first=`（七步每次都在） | 「不用這個方法」（b） |
| CS | CSa、CSb、CSc | acceptEdits | `skill-auto.txt`（沿用上一支）：第二批報名表來了（報名表_第二批.csv），照平常的方式檢查一下。 | shelf5＋book-lean | `VERDICT opened signup-check: YES`；`booklet text: … chars, … lines`（應以 `Base directory for this skill` 開頭、內文七步）；growth 與 `requests carrying it`；`appendix reads`（預期沒有 `確認信範本.md`，`部門對照.md` 讀或不讀照實記）；`batch2.mjs` B1、B4、B5 PASS；`changed:` 不含 `報名表.csv`、`報名表_第二批.csv` | 成果 1、3、4 |
| CV | CVa、CVb、CVc | acceptEdits | 同上 | shelf5＋book-vague | `VERDICT opened checklist: YES/NO`，與 `other booklets opened`（翻成 `reminder-mail` 也記）；`batch2.mjs` 照記 | 成果 3；猜不到的結果第 2 項 |
| CN | CN1 | acceptEdits | 同上 | 只有 shelf5 | `opened:` 哪一本或 none；`batch2.mjs` | 主例的控制組 |
| CP | CPa、CPb | acceptEdits | `paste.txt`（上面那句加七步全文，310 字） | shelf5＋appendix-loose | `batch2.mjs`；`opened:`（預期 none）；`total:` | 「不用這個方法」（a） |
| CM | CMa、CMb | acceptEdits | `skill-auto.txt` | shelf5＋claude-md-book＋appendix-loose | `batch2.mjs`；`first=`；`opened:`；`total:` | 「不用這個方法」（b） |
| CF | CFa、CFb、CFc | acceptEdits | `skill-auto.txt` | shelf5＋book-fat | 同 CS 的每一項；`booklet text` 的字數與行數應是 CS 的三倍上下；growth 比 CS 大 | 成果 4（b）；猜不到的結果第 3 項 |
| W1 | W1a、W1b | acceptEdits | `skill-auto.txt` | shelf5＋book-mine | `VERDICT opened signup-check`；`mine.mjs` M1–M5；`batch2.mjs` | 成果 2 |
| G1（可選） | G1 | acceptEdits | `write-skill.txt`：幫我在這個資料夾寫一個 Skill，放在 .claude/skills/signup-check/SKILL.md：以後每次有新的報名表進來，就照這個資料夾的方式檢查，可以寄確認信的加進 輸出/確認信名單.csv，缺資料的加進 輸出/要補資料.csv，並寫處理日誌。只寫這個檔，不要做其他事。 | 沒有書櫃 | `cover-check.mjs` 對它寫的那一本的判定與全文（`runs.sh` 自動印）；其他檔雜湊不變 | 第 5 章一句「不想從空白開始，可以先叫它寫一本再改」 |
| G2（可選，G1 成立才跑） | G2 | acceptEdits | `skill-auto.txt` | G1 留下的資料夾＋shelf5 | 指令：`bash "$T/session.sh" G2 acceptEdits "$T/prompts/skill-auto.txt" --from-snap G1 --extras shelf5`，接著 `node "$T/skillview.mjs" "$T/../run/logs/G2.stream.jsonl" --expect signup-check`；同 CS 的判讀 | 同上；從那句要求到那個檔再到它被翻開，一條紀錄走完 |

每一項跑完：`[exit 0]`、stderr 0 位元組、init 的模型是 sonnet 系列才算數；`timeout` 到了或不算數的，用備用名額以新 id（原 id 加 `r`，先在 `runs.sh` 的表裡複製那一列改名）重跑，失敗的留在紀錄裡。全部跑完，在紀錄最後寫一張總表：id、`first=`、`shelf` 本數、翻開了哪一本、booklet 字數、growth、`requests carrying it`、appendix reads、`total:`、batch2 B1–B6、mine M1–M5、`total_cost_usd`。L 組與 C 組的回報費用只列，不拿來比（快取會讓同一個開頭第二次比較便宜）。

**成果成立的條件（跑之前講定，跑完不改）**

- 成果 1：CSa–CSc 裡至少 2 次翻開 `signup-check`，而且翻開的那幾次 B1、B4、B5 都 PASS、兩份報名表的雜湊不變。不到：這件拿掉，片子改成只教封面與附件、主例降為引用。成立時再看對照：CP 與 CM 也 B1、B4、B5 全過，就照實講「三種交代方式結果一樣」，主例靠的是「不用每次貼」（310 字對 34 字）、「不用每次帶」（成果 4 的 LM−L0）與「帶得走」（引用）；CN1 也全過，片中加一句「這一批它不靠說明書也猜得到」，不把 CS 的結果講成說明書的功勞。
- 成果 2：W1a、W1b 至少 1 次 M1、M2、M3、M4 全 PASS。都不到：這件拿掉，第 8 步只當練習題，附核對方式（`mine.mjs` 的五項），卡片標「沒有跑出來」不上畫面當結果。
- 成果 3：照官方的判讀門檻（翻開的次數超過一半算有翻）。CS 3 次至少 2 次翻開，而且 CV 比 CS 少 2 次以上：成立，CV 是開場的候選。CV 也有 2 次以上翻開 `checklist`：降級，片中照實講「這次含糊的也翻開了 N 次」，第 4 章的封面寫法改靠引用（支援文章的疑難排解第二條、規格頁的好壞例），數字只講封面占多少（L1−L0）；選項 B 不成立。CV 翻開的是別本（例如 `reminder-mail`）：照實講，這比「沒翻開」更適合當開場。
- 成果 4：（a）LF 兩次的 `first=` 與 L1 兩次相差不超過「同一組兩次之差的最大值＋10」才講「沒翻開前一樣大」，否則照實講差多少、不用這一句當轉折；（b）CF 三次的 growth 都比 CS 三次的大，而且平均差 300 以上才講「翻開之後每次多帶 N」；只有一兩次或差不到 300，講字數（`booklet text` 的 chars 是確定值）不講 token；（c）CS 三次都沒有讀 `確認信範本.md` 才講「沒用到的附件不會被讀」。三項都不成立，這件拿掉，第 6 章只引用 skills 頁的 content lifecycle。
- L 組任何一次翻開了說明書（`opened:` 不是 none）：那一次的 `first=` 仍然有效（翻開在第一個請求之後），照記，另外在總表標明。
- CS 的 init 清單裡沒有 `signup-check`：停下來，先查 `--setting-sources` 與資料夾，不往下跑。

更高一級（看過）：Claude 網頁版與桌面版的「自訂 › 技能」頁、上傳對話框、翻開說明書時的畫面，這台機器不能登入、不能錄，只用支援文章與規格頁的公開頁 `screencast`，卡片標「引用」；這些在片中都不是成果。Codex 沒有安裝，不跑。

## 大綱

三個選項的例子、執行與四件成果都一樣，差在角度、順序與開場。長度以每分鐘 250 字估；三個都在 10–11.5 分鐘。卡片順序都避開前幾支的開頭：上一支是 `title, chat, bullets, big, steps`，〈Skills 對 CLAUDE.md〉是 `title, table, chat, steps, stats`，〈CLAUDE.md 實作〉是 `title, chat, stats, steps, quote`；這一支三個選項都不從 `chat` 開場，全片不用 `terminal`。

### 選項 A：一本說明書從封面講到書櫃，每一個部位都對到一個量得到的機制（推薦）

一行說明：最接近站主指定的參考片結構：一個比喻撐全片，封面、內文、附件、書櫃、翻開各對一個機制，每個部位都有一個這台機器量到的數字；寫一本在中段、上傳在後段、安全一段收尾。和 B 差在開場與主線（B 從一本沒被翻開的說明書倒著查），和 C 差在角度（C 是「三種交代方式」並排的指南，比喻只用一句）。

**開場五句（照唸的寫法，40–55 秒）**
1. （省略「為什麼是現在」：「滿一年了」是參考片的開場，不學；查到的近期變化對這群觀眾不是理由。）
2. 「你可能聽過 Skill，心裡想的是：那是寫程式的人在用的吧？我又不寫程式。」
3. 「它做的事很日常：照你的方式檢查報名表、整理會議紀錄、寫行前提醒信，每一次都照同一套步驟。」
4. 「可是封面沒寫好，AI 連翻都不會翻；內文塞太多，翻開之後整本一直壓在對話裡。」（CV 沒有失敗時，前半句換成「封面寫得含糊，你就不知道它會不會翻」，數字只用 CF 的）
5. 「用一本說明書把它講透：封面、內文、附件，最後你會親手寫出一本報名表檢查，打包放進 Claude。」

案例與結果：「講座籌備資料夾的第二批報名表；一本自己寫的 signup-check（兩行封面、七步內文、兩頁附件），只說『照平常的方式檢查一下』，它就翻開這一本，名單從 16 人變 18 人、缺 Email 的另外列出；封面含糊的那一本翻開 N／3 次；附件塞進內文的那一本，沒翻開前跟 20 行的一樣大、翻開後每次多帶 W。全部是跑過（待 L、CS、CV、CF、W 各組）。」

**觀眾疑問（§三，五次，答案都緊接在同一章）**
- 第 1 章：「MD 這兩個字是不是又要學一種格式？」→ `.md` 就是純文字檔，記事本存得了；只有最上面兩行有規矩。
- 第 2 章：「那為什麼不把所有說明書一次全塞給它？」→ L0／L1／L6 的數字。
- 第 2 章：「我已經有 CLAUDE.md、有專案指示了，不一樣嗎？」→ LM−L0 對 L1−L0；網頁版專案「一直載入」（引用）。
- 第 5 章：「那我每次把這七步貼進去，不也一樣？」→ CP 的結果與 310 字對 34 字。
- 第 7 章：「網頁版跟 Claude Code 用的是同一本嗎？」→ 同一個資料夾壓成 zip；兩份官方頁對「會不會同步」寫法不一樣（「我」的不確定之一）。

**章節**（合計約 665 秒，約 11 分；旁白約 2,770 字）

0. **開場**（50 秒）。`title`：Skill 就是一本說明書｜自己寫一本給 Claude。`big`：「我又不寫程式，要 Skill 幹嘛？」。`bullets`：三個成品（檢查報名表、整理會議紀錄、寫行前提醒信）。`stats`：CS 的「翻開 3／3」、名單「16 → 18」、CV 的「N／3」（出處：實跑那一天）。`big`：承諾句的三個部位「封面・內文・附件」。頻道片頭接在這章之後。收尾：第 1 章的疑問。
1. **一本說明書長什麼樣**（70 秒）。章首句（帶例子狀態，回呼上一支一句）：「上一支裡，第二批報名表是交給一個叫 signup-check 的 Skill 檢查的；這一支把那一本從空白寫出來。」概念五件：是什麼（一個資料夾，裡面一個 SKILL.md，聽起來很專業，其實就是一個純文字檔加兩頁附件）；在例子裡（`steps`：講座籌備 → .claude → skills → signup-check → SKILL.md、部門對照、確認信範本，逐步亮）；`code`：封面那 7 行，旁白唸 description 整句；規則一條（名字只能小寫英文、數字、連字號，跟資料夾同名；介紹句寫中文沒關係，規格頁）；新手坑（上一支那一本沒有名字那一行，在 Claude Code 能用，要上傳網頁版就會被擋，M2）。收尾：「書櫃上擺了這麼多本，它每次都要全部讀一遍嗎？」
2. **平常只看封面：一本、六本、CLAUDE.md 各占多少**（80 秒）。章首句：「signup-check 已經放上書櫃，旁邊還有五本；我先問它一個跟報名無關的問題。」觀眾疑問「為什麼不全塞給它」。`table`：同一句「幾點結束」，五種書櫃（沒有／一本／69 行那本／六本／七步放 CLAUDE.md）的第一個請求大小（L 組，各兩次），亮起 LF 那一列——69 行跟 20 行一樣大，就是轉折。聽起來很專業、其實就是：「漸進式載入」一次。`quote`：規格頁「Metadata (~100 tokens): The name and description fields are loaded at startup for all skills」，譯文（官方估計，對照我量到的 L1−L0）。「我」：放一本、放六本、CLAUDE.md 那三句。`stats`：書櫃本來就有幾本（L0 的 `shelf:`，標「這台機器」）。選擇規則：每次都要遵守的放 CLAUDE.md，偶爾才做的整套放說明書。收尾：「封面這麼重要，那它到底在封面上找什麼？」
3. **拿來做什麼：書櫃上的另外五本**（45 秒）。章首句：「講座籌備資料夾的書櫃上，除了報名檢查，還有五本。」`table`：五本的名字與封面的「什麼時候用」那半句（shelf5 的真實檔），每列一句「沒有它時每次要講什麼 → 有了只要說什麼」；出處標「這支片的練習檔」與支援文章的六種自訂用途（會議紀錄格式、信件範本、品牌規範…）。共同經驗的玩笑：「每一份報名表裡，都有一筆叫『測試』」放在報名那一列。收尾：「可是六本擺在一起，它怎麼知道該翻哪一本？」
4. **封面寫不好，它不翻**（80 秒）。章首句：「我把 signup-check 的封面換成一句『檢查用的步驟』，名字改成 checklist，內文一個字都沒動。」`compare`：左「檢查用的步驟。」右寫清楚的兩句；下方各自「三次翻開幾次」（CV 對 CS）；CV 翻成別本就亮起那一本的名字。「我」：「我跑了三次，它翻開了 N 次。」選擇規則：封面兩句，一句做什麼、一句什麼時候用，用你平常真的會說的那句話（「有新的報名表進來」就是 skill-auto 那句的開頭）。`quote`：規格頁的好壞例（「Helps with PDFs.」是壞例），譯文。新手坑：Claude Code 的格式驗證三本都通過（M3），通過只代表格式對。比喻在這裡失效的那一句：真的說明書是你挑來翻的，這裡是它只看封面決定翻不翻。收尾：「封面寫好了，那內文要怎麼寫？」
5. **自己寫一本：signup-check 的七步**（110 秒）。章首句：「封面定了，現在把每次都要交代的七件事寫進內文。」`code`：內文 13 行（第 1–7 步），旁白逐條唸。`chat`：右「第二批報名表來了，照平常的方式檢查一下。」左 CS 回覆的一句（原文）。`steps`：CS 那一次依序發生的事（翻開 signup-check → 讀新報名表與名單 → 兩人加進名單 → 宋柏均進要補資料 → 寫日誌），出處標那一次。`stats`：名單 16 → 18、要補資料 3 → 4、翻開 3／3。觀眾疑問「每次貼七步不也一樣」：`compare`：每次貼（CP：結果、要求 310 字、每次都要你自己貼）對說明書（CS：結果、要求 34 字）；CN1 的結果一句（做對就照實說「這一批它也猜得到」）。觀眾自己改一行：`code`：第 8 步兩行亮起；`table`：W1 的 mine 五項。可選 G1：「不想對著空白發呆，也可以先叫它寫一本再改」一張 `compare`（它寫的封面對觀眾版，`cover-check` 的判定）。收尾：「部門對照、確認信範本，為什麼不直接寫進內文？」
6. **翻開之後不會闔上：附件放旁邊**（65 秒）。章首句：「同一本說明書，我另外做了一個版本：兩頁附件全貼進內文，從 20 行變 69 行。」`compare`：20 行加附件（CS）對 69 行（CF）：翻開那一步多了多少、後面幾個請求都帶著、確認信範本有沒有被讀（appendix reads）。「我」：「69 行那一本，一翻開就多了 W，後面 K 個請求都帶著。」比喻失效的第二句：說明書看完會闔上，這裡翻開後整本留在那次對話裡；第四句（改了說明書，正在進行的對話不會重讀）一句帶過、引用。選擇規則：每次都要照做的進內文，偶爾才用的放附件、在內文點名「要的時候才看哪一頁」。收尾：「寫好了，怎麼帶進 Claude 網頁版？」
7. **放進 Claude 網頁版與桌面版**（65 秒）。章首句：「signup-check 現在在講座資料夾裡跑得動，接下來把它帶到 Claude 網頁版。」`steps`：設定 › 功能 打開「程式碼執行和檔案建立」→ 自訂 › 技能 →「＋」→ 建立技能 → 上傳技能 → 選 zip（選單名照支援文章，英文 Settings › Capabilities、Customize › Skills、「+ Create skill」、「Upload a skill」；卡片標「引用」）。`screencast`：support.claude.com〈Use skills in Claude〉「Add and use custom skills」那一段。`compare`：對的 zip（第一層是 signup-check/）對錯的 zip（三個檔散在外面），M4 的實際清單；支援文章列的上傳失敗原因（資料夾名跟 name 不同、少了 SKILL.md、名字或介紹有不合規的字）。`bullets`：上傳前兩件事：description 200 字以內（支援文章；規格頁是 1024，網頁版比較嚴）、整個資料夾一起壓。「我」：免費版能不能上傳，兩份官方頁寫的不一樣。觀眾疑問「網頁版跟 Claude Code 同一本嗎」：支援文章寫 2.1.273 以上的 Claude Code 會同步你在網頁版開的技能、單向、約十分鐘檢查一次；platform 的 overview 寫各處不同步——一句講清楚是兩份頁面的說法，不替它決定。收尾：「ChatGPT 那邊看得懂這一本嗎？」
8. **別的工具也看得懂同一本嗎**（40 秒）。章首句：「同一個 signup-check 資料夾，格式是公開的標準。」`stats`：agentskills.io 的支援工具清單 45 個（企劃讀到的數字，撰稿日重數）。`bullets`：ChatGPT 桌面版側邊欄的 Skills、在對話裡打 @ 選一本；Codex 用 $ 叫（官方頁，Codex 這裡沒裝，只點名一次）；Gemini CLI、Cursor、GitHub Copilot 也在清單上。「我」：ChatGPT 網頁版能不能直接上傳一本，官方頁沒寫。收尾：「別人寫好的說明書，可以直接拿來用嗎？」
9. **一段警覺**（25 秒）。`bullets`：說明書的資料夾可以夾小程式，AI 會去執行；別人給的、網路上下載的，整個資料夾每一頁先打開看，看不懂的那一頁就不裝；只放自己寫的或信得過來源的（支援文章與 overview 的 Security considerations）。檢查一個：上傳前在資料夾裡數一下有幾個檔，每一個都打開過。比喻失效的第三句在這裡。
10. **你現在先做這三件**（35 秒）。`steps`：一、挑一件你交代過三次的事，寫兩句封面；二、內文只寫每次都要照做的步驟，範本放旁邊；三、同一句話跑三次，看它翻開幾次。`outro`：答案一句（「Skill 就是一本說明書：AI 平常只看封面，要用才翻開，所以封面要寫給它看，內文只寫每次都要的」）、留言題「你最常重複交代 AI 的那件事是什麼？」、訂閱邀請；Mokaair 文章放說明欄，不講下一支。

範本順序：title, big, bullets, stats, big ｜ steps, code, bullets ｜ table, quote, stats ｜ table ｜ compare, quote ｜ code, chat, steps, stats, compare, code, table ｜ compare ｜ steps, screencast, compare, bullets ｜ stats, bullets ｜ bullets ｜ steps, outro。

主例子在第 1 章出現、第 2–6 章每章量一個部位、第 7 章帶走；四件成果落在第 5 章（成果 1、2）、第 4 章（成果 3）、第 2／6 章（成果 4）。

### 選項 B：從一本沒被翻開的說明書倒著查（只有 CV 有 2 次以上沒翻開 `checklist` 才成立）

一行說明：開場放猜不到的結果「我寫了一本，三次它翻開 N 次」，然後照排查的順序走：先看它在不在書櫃上（init 清單）→ 封面寫了什麼（CV 對 CS）→ 封面占多少、為什麼它只看封面（L 組）→ 內文怎麼寫、它照做了沒（CS、W1）→ 附件該放哪（CF）→ 帶去網頁版與別的工具 → 一段警覺。比 A 更貼近搜尋「Skill 沒有觸發」的人、鉤子更早；代價是「它有用」的結果到第 4 章才出現，而且整個開場押在 CV 上（CV 三次都翻開就不能用）。

**開場五句**
1. （省略。）
2. 「你可能已經照著網路上的教學寫過一本 Skill，然後發現：AI 好像從來沒用過它。」
3. 「它本來該做的是：一看到新的報名表，就照你寫的七個步驟檢查、加名單、列出缺資料的人。」
4. 「我寫了一本封面只有『檢查用的步驟』的，同一句話跑三次，它翻開了 N 次〈CV 的實際結果；翻成別本就講翻成了哪一本〉——說明書寫了，不等於它會用。」
5. 「這支片照四個地方查：書櫃、封面、內文、附件，最後讓同一句話三次都翻開對的那一本。」

案例與結果：「同一個講座資料夾與第二批報名表；開場是 CV 的失敗，第 4 章 CS 翻開 3／3、名單 16 → 18；後段 CF 與上傳。跑過（待各組）。」

**觀眾疑問**：第 1 章「是不是我的 Skill 根本沒裝進去？」（init 清單）；第 2 章「封面不就是個標題嗎？」；第 3 章「那我把封面寫長一點，寫到很詳細？」（description 上限與 L1−L0）；第 4 章「每次貼七步不也一樣？」；第 6 章「ChatGPT 也是看封面嗎？」（learn.chatgpt.com：implicit invocation 靠 description）。

**章節**（合計約 640 秒）
0. **開場**（50 秒）：`title`、`stats`（CV 的 N／3 對 CS 的 3／3）、`compare`（兩個封面）、`big`（「寫了，不等於會用」）。
1. **它在不在書櫃上**（55 秒）：書櫃概念五件；`table`：L0 與 L6 的 init 清單本數；`steps`：資料夾路徑逐步亮。收尾：「在書櫃上，那它看了封面什麼？」
2. **封面：它只看這兩行**（90 秒）：封面概念五件；CV 對 CS 的 `table`（三次各翻開哪一本）；`quote` 規格頁好壞例；`code` 封面 7 行；cover-check 與 M3。收尾：「封面寫長一點會不會比較好？」
3. **它為什麼只看封面**（70 秒）：L 組 `table`、`quote` ~100 tokens、LM 對 L1；選擇規則。收尾：「翻開之後，內文要怎麼寫它才照做？」
4. **內文：七步與你自己的那一行**（120 秒）：`code` 內文、`chat`、`steps`（CS）、`compare`（CP 對 CS）、第 8 步與 W1。收尾：「範本、對照表放哪裡？」
5. **附件：翻開之後不會闔上**（60 秒）：CF 對 CS 的 `compare`。
6. **帶去網頁版與別的工具**（95 秒）：`steps`、`screencast`、zip 的 `compare`、`stats` 45 個工具、`bullets` ChatGPT／Codex；兩句「我」的不確定。
7. **一段警覺**（25 秒）＋**你現在先做這三件**（35 秒）＋`outro`。

範本順序：title, stats, compare, big ｜ table, steps ｜ table, quote, code, bullets ｜ table, quote, stats ｜ code, chat, steps, compare, code, table ｜ compare ｜ steps, screencast, compare, stats, bullets ｜ bullets ｜ steps, outro。

### 選項 C：同一套步驟的三種交代方式，並排比（指南式，比喻一句就走）

一行說明：全片是觀眾今天會用的三種交代方式並排：每次貼進要求（CP）、寫進 CLAUDE.md／專案指示（CM、LM）、寫成一本說明書（CS、L1），每一種同樣四步（你怎麼做、跑出來的結果、它每次帶多少、什麼時候用它）；最後一段才教寫封面與附件、打包上傳。最好查、選擇規則最清楚；代價是「說明書」只當一句局部比喻，參考片那種一個比喻撐全片的順暢感最弱，封面與附件壓成後半的兩段。

**開場五句**
1. 「Anthropic 在 2025 年 10 月 16 日推出 Agent Skills，同年 12 月 18 日把格式公開成標準。」（為什麼是現在：官方日期；跟參考片的「滿一年」不同句、不講週年。）
2. 「你可能會問：我把步驟貼進對話、或寫進 CLAUDE.md，不就好了？」
3. 「三種做法都能讓 AI 照你的步驟檢查報名表、加名單、列出缺資料的人。」
4. 「差在你要不要每次貼、它要不要每次帶、換一個工具還能不能用。」
5. 「同一份第二批報名表，三種交代方式各跑一遍；看完你會有一本自己的說明書，還有一條什麼時候寫成 Skill 的規則。」

案例與結果：「同一個資料夾與第二批報名表；三種方式的 batch2 結果、第一個請求大小、要求的字數並排；最後寫封面（CV 對 CS）與附件（CF）。跑過（待各組）。」

**觀眾疑問**：第 1 組「貼一次又不累？」；第 2 組「網頁版的專案指示也一樣嗎？」（引用：always loaded）；第 3 組「那 Skill 有什麼是 CLAUDE.md 做不到的？」（帶得走、要用才翻開）；第 4 段「封面寫一句不行嗎？」。

**章節**（合計約 630 秒）
0. 開場（50 秒）：`title`、`table`（三種方式 × 三個問題，空格）、`big`。
1. 第一種：每次貼（90 秒）：CP 的結果、每次 310 字、`code` paste.txt 節錄。
2. 第二種：寫進 CLAUDE.md 或專案指示（100 秒）：CM 結果、LM−L0、`quote` 支援文章「always loaded」。
3. 第三種：一本說明書（130 秒）：資料夾與 SKILL.md 全文（兩張 `code`）、CS 結果、L1−L0、L6、LF；CN1 對照；第 8 步與 W1。
4. 寫好一本的兩件事：封面與附件（110 秒）：CV 對 CS、CF 對 CS。
5. 帶走：網頁版、桌面版、別的工具（90 秒）：上傳 `steps`、`screencast`、zip `compare`、45 個工具。
6. 一段警覺（25 秒）＋三件事（35 秒）＋`outro`。

範本順序：title, table, big ｜ compare, code, stats ｜ compare, quote, stats ｜ code, code, table, stats, code, table ｜ compare, compare ｜ steps, screencast, compare, stats ｜ bullets ｜ steps, outro。

### 三個選項共同的收尾

答案一句（Skill 是一本說明書：平常只看封面、要用才翻開；封面寫給 AI 看，內文只寫每次都要的，其他放附件），留言題問觀眾自己的情況（「你最常重複交代 AI 的那件事是什麼？」），訂閱邀請。Mokaair 的對應文章放說明欄；不講下一支片。

### 建議

選 A。它照站主指定的參考片結構走（一個比喻撐全片、每個部位對一個機制、介紹句與內文整段唸、一份集中的用途清單、選單名寫到底、一個承認的不確定、一段安全收尾），而且每個部位都有一個這台機器量到的數字，不是只有比喻；它也不押在單一一組的結果上：CV 沒有失敗時，A 的轉折改用 LF（最可能成立的那一項）。B 只有 CV 失敗才成立，成立時它的開場比 A 強，選大綱時看紀錄再決定。C 的選擇規則最清楚，但比喻退成一句，跟參考片的差距最大。

## 會過期的事實

全部在 UTC 2026-10-20 18:06–18:14（台北 10-21）開過，原檔在 `<work>/_tools/pages/`；撰稿日再開一次（`bash fetch.sh <檔名> <網址>`）。

| 事實 | 官方頁 |
| --- | --- |
| Skills 開放給 Free、Pro、Max、Team、Enterprise；需要開啟程式碼執行；個人方案在 Settings › Capabilities 開「Code execution and file creation」，在 Customize › Skills 開關與上傳；上傳：「+」→「+ Create skill」→「Upload a skill」→ 上傳裝著技能資料夾的 ZIP；上傳失敗常見原因（ZIP 太大、資料夾名與 skill 名不同、少了 skill.md、名字或介紹有不合規的字元）；Claude 沒用你的 Skill 時的四步檢查；Claude Code v2.1.273 以上會單向同步你在 Claude 設定裡開的技能，開 session 時同步、之後約十分鐘檢查一次；只裝信得過來源的技能，裝前讀過資料夾裡每個檔 | https://support.claude.com/en/articles/12512180-use-skills-in-claude |
| 同一篇的繁中機器翻譯：「設置 > 功能」「自定義 > 技能」「+ 創建技能」「上傳技能」（台灣介面用字未確認） | https://support.claude.com/zh-TW/articles/12512180 |
| skill.md 必須有 YAML frontmatter 的 name（64 字元以內）與 description（200 字元以內，Claude 用它決定何時叫）；附件檔放在資料夾裡、在 skill.md 點名；ZIP 的根目錄是技能資料夾本身（附正確與錯誤結構圖）；上傳後的測試四步（試幾種說法、看思考過程確認有載入、沒被用就改 description）；在 Mac 的 Cowork 可以錄影產生技能（Windows 沒有） | https://support.claude.com/en/articles/12512198-how-to-create-custom-skills |
| 技能用漸進式揭露；自訂技能的六種用途（品牌規範、信件範本、會議紀錄格式、在工具裡建任務、資料分析流程、個人工作流程）；Skills 對 Projects（專案是一直載入的背景知識）、對 custom instructions（套在所有對話）；Agent Skills 規格在 agentskills.io 公開 | https://support.claude.com/en/articles/12512176-what-are-skills |
| 三層載入：Metadata 約每本 100 token、一律在開場載入；Instructions 5k token 以內、觸發時載入；Resources 讀到才進脈絡；claude.ai 一節寫「Settings > Features」上傳 zip、Pro／Max／Team／Enterprise（跟支援文章的 Free 與選單名不一致）；自訂技能各處不同步；只用信得過來源的技能 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview |
| 規格：資料夾至少一個 SKILL.md；name 1–64 字、小寫英數與連字號、與父資料夾同名；description 1–1024 字、寫做什麼與何時用（好例與「Helps with PDFs.」壞例）；scripts/、references/、assets/；SKILL.md 500 行以內、長的參考資料搬出去；啟用時整個 SKILL.md 載入 | https://agentskills.io/specification |
| 格式最初由 Anthropic 開發、以開放標準釋出；三階段（Discovery、Activation、Execution） | https://agentskills.io/home |
| 支援工具清單（2026-10-21 解析出 45 個，含 Claude、Claude Code、ChatGPT & Codex、Gemini CLI、Cursor、GitHub Copilot、VS Code、Kiro…；`clients.mjs` 重數） | https://agentskills.io/clients |
| description 決定觸發；同一句跑 3 次算觸發率、超過 0.5 算有觸發；簡單的一步要求可能不觸發 | https://agentskills.io/skill-creation/optimizing-descriptions |
| ChatGPT 與 Codex 用同一個開放標準；單獨的 skill 在 ChatGPT 桌面版、Codex CLI 與 IDE 擴充可用，網頁版只透過外掛帶的 skill；桌面版側邊欄的 Skills；ChatGPT 打 @、Codex 打 $ 或 /skills；也會依 description 自己挑；SKILL.md 要有 name 與 description（`developers.openai.com/codex/skills` 轉址到這一頁） | https://learn.chatgpt.com/docs/build-skills |
| Claude Code：name 選填、預設資料夾名；description 建議寫，清單裡與 when_to_use 合計截在 1,536 字；技能清單的預算是脈絡的 1%；翻開後內容整段進對話、之後不重讀、「every line is a recurring token cost」；壓縮後每本保留前 5,000 token；不觸發的排查；`claude plugin validate`（v2.1.233 以上） | https://code.claude.com/docs/en/skills |
| Agent Skills 發表日 2025-10-16；2025-12-18 公開成開放標準（`anthropic.com/news/skills` 轉址到這一頁） | https://claude.com/resources/articles/skills |
| 這台機器的 Claude Code 版本 | `claude --version`（M0，跑的那天記） |

## 素材

- 沒有來源文章；說明欄連到站上既有的 Claude Code 系列文章，由撰稿時選一篇，不在旁白裡念。
- 練習資料夾：上一支的 `make-seed.mjs`（原封不動，`reuse.sh` 比對雜湊）與這支的 `make-booklets.mjs` 產生的 extras，全部虛構、頻道自有；人名是常見的虛構組合，Email 全在 `example.com`。
- 執行與判讀工具（`<work>/_tools/`）：沿用的 `session.sh`、`inspect.mjs`、`score.mjs`、`versions.mjs`、`batch2.mjs`、`selftest.mjs`；這支新寫的 `runs.sh`、`skillview.mjs`、`cover-check.mjs`、`zip.mjs`、`mine.mjs`、`make-booklets.mjs`、`reuse.sh`；查官方頁用的 `fetch.sh`、`text.mjs`、`clients.mjs`；prompt 在 `prompts/`；官方頁原檔在 `pages/`。
- 可以 `screencast` 的公開官方頁（不登入）：support.claude.com〈Use skills in Claude〉（Add and use custom skills、Troubleshooting）、〈How to create custom skills〉（Package your skill 的對錯結構圖）、agentskills.io/specification（Frontmatter 表、Progressive disclosure）、agentskills.io/clients、learn.chatgpt.com/docs/build-skills。版權屬各自網站，依頻道規格只截公開頁、標出處。
- 結構參考：`docs/videos/reference-study-20261021/README.md` 的俗說 AI 那支（說明書的比喻、介紹句與內文整段唸、集中的用途清單、選單名、承認不確定、一段安全收尾）；只學結構，不引用、不模仿它的句子，它的「找餐廳」例子、「滿一年」開場、記事本那句都不用。
- 前幾支的 brief（開場與卡片順序不重複）：`claude-code-beginner-event-folder`、`claude-code-skills-vs-claude-md`、`claude-code-claude-md-hands-on`。

## 不做的事

- 不重講上一支的四個基本功、實戰、家教；`/signup-check` 用斜線叫上一支示範過，這支不再跑，只在第 1 章回呼一句。
- 不登入 Claude 網頁版或桌面版、不真的上傳；上傳只引支援文章與它的公開頁。
- 不教 `allowed-tools`、`context: fork`、`disable-model-invocation`、hooks、外掛打包、Skills API；說明書裡不放任何程式（`scripts/` 只在安全那一段點到它存在）。
- 不教終端機；實跑用的是無介面 session，畫面上不出現終端機卡。
- 不量開發者那一支量過的「Skill 對 CLAUDE.md 的照做程度」；這支只量封面占多少、翻開後占多少、封面寫法對翻不翻開的影響。
- 不安裝 Codex、不跑 ChatGPT；兩者只引官方頁，Codex 點名一次。
- 不談價錢與方案的費用數字，只說官方頁列的方案。
- 不給任何投資、醫療、法律或選舉建議。
