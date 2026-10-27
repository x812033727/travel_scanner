# muse-allow-always-agent-permission：查核第 1 輪（verify-1）

查核日 2026-10-27，查核者是獨立的代理，不是撰稿者。所有頁面都在今天用 `Mokaair-editorial/1.0` 重新抓過（每台主機間隔至少 1 秒），抓下來的頁面在 scratchpad `muse/verify1/dl/`；網路搜尋用了 3 次。
終端機卡與對話卡都跟 `muse/run/` 的畫面擷取逐字比對過（`muse/verify1/cardcheck.py`）。

簡稱：YH＝Yahoo Tech（Business Insider）、TR＝TechRadar、FO＝Fortune（AP）、TH＝Robb 的 Threads 貼文、CC＝code.claude.com/docs/en/permissions（含 `.md` 版）、GG＝Google 帳戶說明 13533235（zh-Hant）、MJ＝Meta 日本 10/23 公告、MU＝Meta Newsroom 9/8 公告、IC＝iPhone in Canada 9/18、RUN＝`muse/run/` 的擷取檔。

| URL | HTTP |
| --- | --- |
| YH https://tech.yahoo.com/ai/meta-ai/articles/youtuber-says-muse-setting-led-122153415.html | 200 |
| TR https://www.techradar.com/ai-platforms-assistants/you-gotta-never-do-that-again-youtuber-says-metas-muse-ai-ruined-a-sale-and-gave-out-his-home-address-without-permission | 200 |
| TH https://www.threads.com/@matt.j.robb/post/Dd28UvzALKg/… 與 /post/DdxwAJnDhNy | 200／200 |
| FO https://fortune.com/2026/10/19/meta-muse-ai-agent-facebook-marketplace-home-address-privacy/ | 200 |
| AI Weekly https://aiweekly.co/alerts/metas-muse-agent-hands-toronto-sellers-address-to-a-stranger（只當線索） | 200 |
| CC https://code.claude.com/docs/en/permissions（與 permissions.md） | 200／200 |
| GG https://support.google.com/accounts/answer/13533235?hl=zh-Hant | 200 |
| MU https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ | 200 |
| MJ https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent-launches-in-japan/ | 200 |
| IC https://www.iphoneincanada.ca/2026/09/18/metas-muse-ai-agent-is-now-available-in-canada/ | 200 |
| SmartScope https://smartscope.blog/en/blog/meta-muse-japan-launch-free-plan-limitations-invite-2026/ | 200 |
| Inside https://www.inside.com.tw/article/42443-meta-muse-app-store-number-one-us-2026 | **403**（Cloudflare 擋下；撰稿者存的檔也是擋下頁，從來沒讀到內文） |

## 主張表

| # | 主張 | 在哪裡 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 事件日期 9 月 26 日 | L1 2z4v、說明欄 | TH、X、YH、AI Weekly→FO | 200 | CONFIRMED | 判斷理由：Robb 寫「today… until late tonight」的 Threads 貼文 DdxwAJnDhNy 由編號換算是 9/27 00:27 EDT，X 貼文 2104090601411293303（snowflake）是 9/27 06:07 UTC＝02:07 EDT，都是 9/26 晚上之後的午夜後；YH 嵌入的「September 27, 2026」是 UTC 日期。AI Weekly 轉述 Fortune 寫「9:15 p.m. on a Saturday」，2026-09-26 是週六。保留 9/26（多倫多當地時間）。 |
| 2 | 多倫多的 YouTuber | L1、說明欄 | FO | 200 | CONFIRMED | FO："a Toronto-based content creator who regularly reviews consumer tech"；已加進 sources |
| 3 | 讓 Muse 替他在 Marketplace 賣鍵盤 | L2、說明欄 | YH、TR | 200 | CONFIRMED | — |
| 4 | 那天晚上，買家照地址開車到他家樓下 | L3、說明欄 | TR、YH、FO | 200 | CONFIRMED | TR "drove 30 minutes to Robb's home"；YH "showed up at his building"；FO "late at night" |
| 5 | Muse 在台灣還用不到 | L4、S1、說明欄 | MJ | 200 | CONFIRMED | MJ：10/23（日本時間）起在日本提供，日本是 9 月先開的北美之外第一個地區 |
| 6 | 美國 9/8、加拿大 9/18、日本 10/23 開放 | 說明欄、claims c3 | MU、IC、MJ | 200 | CONFIRMED | 美國：MU 9/8 "rolling out in the US"；加拿大：IC 引 Meta 的 X 貼文（9/18 週五）；日本：MJ。來源由 Inside 改成這三頁 |
| 7 | 「Meta 看過紀錄之後說：這次沒有違反任何隱私控制」 | L5 tech、S2 kicker 與 text、說明欄 | YH | 200 | CHANGED | YH：說「no breach of privacy controls」的是 Meta Superintelligence Labs 的員工 David Singleton，在回覆 Robb 週二貼文時說的。陪 Robb 看紀錄的是 Muse 團隊（#21），看完說的是會把提示寫清楚。原文沒有「任何」。旁白「Meta 看過紀錄之後說：這次沒有違反任何隱私控制。」→「Meta 的一位員工回覆他：已確認沒有違反隱私控制。」；kicker「Meta 看過紀錄」→「Meta 員工的回覆」；text「沒有違反 任何隱私控制」→「沒有違反 隱私控制」；說明欄「Meta 看過紀錄說」→「Meta 的員工回覆說」 |
| 8 | 他「第一天」按下的按鈕 | L6 3wna、L9 33r9、S4 keys、說明欄 | YH、FO | 200 | CHANGED | YH "when he first asked Meta's AI agent to sell his computer keyboard"；FO "when he first let Muse on his Facebook Marketplace profile"。兩篇都沒寫「設定 Muse 的第一天」。「第一天按下的」→「一開始按下的」；「設定 Muse 的第一天，」→「一開始賣鍵盤時，」；keys「第一天按了」→「一開始就按了」 |
| 9 | 引文卡日期「9 月 30 日」 | S4 kicker | YH、TH | 200 | CHANGED | YH 寫 "a Tuesday update on X"，文章 2026-09-29（週二）12:21 UTC 刊出；Threads Dd28UvzALKg 換算是 9/29 00:51 EDT。「9 月 30 日」→「9 月 29 日」 |
| 10 | 引文 "I didn't think it would send it out to everyone that gave me an offer" | S4 quote | YH、TH | 200 | CONFIRMED | 跟 YH 逐字相同（TH 用彎引號） |
| 11 | 引文出處「Matt Robb 在 X 上（Yahoo Tech 轉述）」 | S4 source | YH | 200 | CONFIRMED | "Robb wrote"（在 X 的週二更新） |
| 12 | 他按了 Allow Always | L9 | YH | 200 | CONFIRMED | — |
| 13 | 以為 Muse 接受出價前還會先問他 | L10、S7 | YH | 200 | CONFIRMED | "believing it would still seek his approval before accepting offers" |
| 14 | 用回覆範本替他發訊息，範本裡有取貨地址 | L11、L12、S7 | YH、TH | 200 | CONFIRMED | — |
| 15 | 「我沒想到，它會把地址送給每一個出價的人」 | L13 | YH、TH | 200 | CONFIRMED | 「it」在 TH 指含地址的範本 |
| 16 | Muse 的訊息原句（‘Yep I’m here!’ at 9:27） | S5 quote | TR | 200 | CONFIRMED | 逐字相同，含彎引號 |
| 17 | "Yep I'm here!" 譯成「我到了」 | S5 translation、S5 keys、L15 dgma（含 emotion） | TR | 200 | CHANGED | 這句是替 Robb 說「我在」，Muse 自己說是 "claiming you're home"；「我到了」意思不對。translation「跟他說「我到了」」→「跟他說「對，我在！」」；keys「說「我到了」」→「說「我在」」；L15「跟買家說了一句我到了；」→「跟買家回了一句：對，我在；」；emotion「「我到了」放慢」→「「我在」放慢」 |
| 18 | Muse 事後傳訊息「跟他道歉」 | L14 85ie | TR | 200 | CHANGED | 9:27 那則是 Muse 主動傳的壞消息加認錯（"Worse… I should probably stop the auto-replies…"）；"I'm sorry" 是 Robb 罵它之後才回的。「跟他道歉，」→「跟他認錯，」 |
| 19 | 「晚上」九點二十七分 | L15 | TR、FO、AI Weekly | 200 | CONFIRMED | TR 只寫 "9:27"；FO "late at night"、AI Weekly 寫 9:15–9:38 p.m.，可以說是晚上 |
| 20 | 他那時根本不在家 | L16 | TR | 200 | CONFIRMED | "while he was out" |
| 21 | Meta 團隊陪他看紀錄，說會把權限提示寫清楚 | L17、S6 | YH、TH | 200 | CONFIRMED | 是 Robb 自己的說法（"Robb said…"） |
| 22 | 他以為／按鈕准的對照 | S7 | YH | 200 | CONFIRMED | — |
| 23 | 權限提示卡（3 行） | S9 code | RUN 01-prompt.txt | — | CONFIRMED | 是連續節錄，包括 ❯ 與 U+2019 ’ |
| 24 | 節錄 3 行，共 4 個選項，版本 2.1.311 | S9 caption | RUN 01 | — | CONFIRMED | — |
| 25 | 第二個選項「以後不用再問 git push，加一顆星」；第一個只准一次，第二個存成規則 | L24、L25 | RUN 01、CC | 200 | CONFIRMED | — |
| 26 | 設定檔卡的 `"allow": ["Bash(git push *)"]` | S10 output | RUN RUNLOG.md 第 2 步 | — | CONFIRMED（內容）／不能逐字比對 | 沒有這一步的原始 cat 擷取；RUNLOG 只寫了壓縮成一行的版本。卡片的排版跟 06b、09 的實際檔案（兩格縮排）一致。沒改，列在下面「懷疑但沒動」 |
| 27 | 多了一條：git push、空一格、一顆星 | L28 | RUN | — | CONFIRMED | — |
| 28 | 每一個以 git push 開頭的指令都不用再問 | L29、S11 | RUN 05、CC | 200 | CONFIRMED | 05："Any Bash command starting with git push" |
| 29 | 規則存在倉庫根目錄，倉庫裡的每一次對話都算 | L30、c8 | CC〈Permission system〉 | 200 | CONFIRMED | "applies to future sessions anywhere in that repository"（在 git 倉庫外或 Windows 上例外，片中沒講） |
| 30 | 新對話強制推送的兩個對話泡泡 | S12 | RUN 03 | — | CONFIRMED | 兩個都是連續節錄 |
| 31 | 本機改寫提交、/exit、新對話、沒有詢問、蓋掉遠端 | L32–L34 | RUN RUNLOG、03 | — | CONFIRMED | 69cd815 → b2a3d6d |
| 32 | 換了對話，記得全部的推送，連強制推送也算 | L35、S13 | RUN 03 | — | CONFIRMED | — |
| 33 | 表格：執行指令永久整個倉庫、修改檔案到對話結束、抓網頁永久以網域為單位 | S14、L37–L40 | CC 表格 | 200 | CONFIRMED | "Permanently per repository and command"／"Until session end"／"Permanently per repository and domain" |
| 34 | 萬用字元卡：git push *、git *、ls *（不含 lsof）、ls*（含 lsof） | S15 | CC〈Wildcard patterns〉 | 200 | CONFIRMED | — |
| 35 | git 空一格星號＝所有 git 指令；少一個空格連名字開頭一樣的程式都算 | L41、L42 | CC | 200 | CONFIRMED | — |
| 36 | 只有在提示能顯示全部會准的範圍時才給「不要再問」，否則只給一次性同意 | L45、L46、S16 | CC〈Permission system〉 | 200 | CONFIRMED | "offers those options only when the prompt can show you everything they would allow" |
| 37 | 略過權限模式「略過所有權限詢問」 | S17 text | CC〈Permission modes〉 | 200 | CHANGED | 表格原文 "Skips permission prompts, except for the actions no mode auto-approves"。「略過**所有**權限詢問」→「略過**幾乎所有**權限詢問」 |
| 38 | 連寫進 git 和設定資料夾都不問；只在容器或虛擬機用 | L49、L50、S17 key | CC 警告框 | 200 | CONFIRMED | ".git and .claude"；"isolated environments like containers or VMs where Claude Code can't cause damage" |
| 39 | 同意一串用連接符號串起來的指令，每段各存一條，最多五條 | L51 82fs、L52、S18 | CC〈Compound commands〉 | 200 | CHANGED（L51）／CONFIRMED（五條） | 只有按「Yes, and don't ask again」才會存規則，單按 Yes 不存。「你同意一串用連接符號串起來的指令，」→「你對一串用連接符號串起來的指令按不要再問，」；"Up to 5 rules" 確認 |
| 40 | Google 原句「移除代理的存取權，並不會中斷或刪除 Google 帳戶與該應用程式的連結。」 | S19 | GG | 200 | CONFIRMED | 逐字相同；kicker 的節名「Gemini 和代理權限」也相同 |
| 41 | Gemini 這類代理透過你連結的 App 替你做事；停止使用不會中斷連結 | L53–L55 | GG | 200 | CONFIRMED | — |
| 42 | 三條「只按這一次」 | S20、L57–L59、S33 L85 | brief 的站主觀點 | — | OUT OF SCOPE（站主意見，有標示） | 跟 brief 一致 |
| 43 | Robb 的建議 "double-check what permissions AI has in your life" | S21、L60 | YH | 200 | CONFIRMED | — |
| 44 | /permissions 看得到規則，說明寫「Any Bash command starting with git push」 | S22、L62、L63 | RUN 04、05 | — | CONFIRMED | — |
| 45 | 刪掉後再請它強制推送，又停下來問 | S23、L64、L65 | RUN 07、RUNLOG 第 5 步 | — | CONFIRMED；右邊泡泡不能逐字比對 | 左邊泡泡 "Do you want to proceed?" 有在 07；右邊泡泡「請執行 git push --force origin main」不在任何擷取檔裡（07 從 "● Force push main to origin" 開始）。沒改，列在下面「懷疑但沒動」 |
| 46 | 刪掉後的設定檔 `"allow": []` | S24、L66 | RUN 06b | — | CONFIRMED | 整個檔案逐字相同 |
| 47 | 這份檔案每個倉庫各有一份 | L67 | CC | 200 | CONFIRMED | — |
| 48 | 拒絕設定檔第 2–9 行（共 10 行） | S25 | RUN 09 | — | CONFIRMED | 逐字相同，行數也對 |
| 49 | 拒絕規則永遠比允許規則優先 | L68 | CC〈Manage permissions〉 | 200 | CONFIRMED | "deny, then ask, then allow… An allow rule can't carve an exception out of a deny rule" |
| 50 | 加回允許，再加一條擋強制旗標開頭的拒絕 | L69 | RUN 09 | — | CONFIRMED | — |
| 51 | 新對話：「因為系統拒絕了這個指令的權限,所以沒有任何東西被推送。」 | S26、L70、L71 | RUN 10 | — | CONFIRMED | 連續節錄，逗號是半形，跟擷取檔一樣 |
| 52 | 簡寫 -f：「main 在 origin 上從 b2a3d6d 被強制更新為 38a0e59。」，沒有詢問 | S27、L73、L74 | RUN 11 | — | CONFIRMED | — |
| 53 | 拒絕規則比對的是字，-f 被 git push * 接走 | L75、S28 | CC〈What a Bash rule doesn't match〉、RUN 11 | 200 | CONFIRMED | — |
| 54 | 「會改寫歷史的推送乾脆不存允許規則」 | L76 | — | — | OUT OF SCOPE（意見） | 見下面「意見不一致」 |
| 55 | Google 步驟：連結的應用程式 → 代理存取權篩選 → 停止使用；要斷 App 再另外移除 | S29、L77–L79、S33、說明欄 | GG | 200 | CONFIRMED | 卡片省略了「選取應用程式」與「選取停止使用表示確認」兩個小步驟，不算錯 |
| 56 | 意見：要用；規則的範圍是你按出來的；Muse 那晚沒有出錯 | S30、L81、L82 | brief、YH、FO、TR | 200 | OUT OF SCOPE（意見），但有前提的問題 | 見下面「意見不一致」 |
| 57 | 我查不到 Meta 怎麼定義那幾個允許選項 | S31、L83 | brief | — | OUT OF SCOPE（意見） | 跟 brief 一致 |
| 58 | 你按過的一律現在多半還在生效 | S32、L84 | — | — | OUT OF SCOPE（意見） | — |
| 59 | 片頭卡標題、副標、key | S0 | — | — | CONFIRMED | — |
| 60 | youtube.title、縮圖 | youtube.title、thumbnail | YH、RUN | 200 | CONFIRMED（修辭） | — |
| 61 | 說明欄：版本 2.1.311、錄製日期 2026-10-27、拒絕規則的程式碼、所列地點 | description | RUN、CC、GG | 200 | CONFIRMED | — |
| 62 | 說明欄：Muse 開放地區的來源寫「照 Inside 與日本媒體的報導」 | description | Inside | 403 | CHANGED | →「照 Meta 的公告與 iPhone in Canada 的報導」 |
| 63 | sources 清單 | sources | 如上 | — | CHANGED | 移除 Inside（403，撰稿與查核都沒讀到內文）；加上 MU、MJ、IC、FO；全部的 checked_on 是 2026-10-27 |
| 64 | tags | youtube.tags | — | — | OUT OF SCOPE | — |
| 65 | 同一種按鈕你在 Claude Code、Google 帳戶裡多半也按過 | L7、S3 | GG | 200 | OUT OF SCOPE（修辭） | Google 那頁講的是讓代理跟 App 互動的權限，不是一顆叫「一律允許」的按鈕；這是類比，不是引文 |

## 摘要

- 查了 65 條主張：CONFIRMED 49、CHANGED 9（#7、8、9、17、18、37、39、62、63；事實修正算成 8 處，#62／#63 是同一處來源修正）、NOT FOUND 0、OUT OF SCOPE 7；另有 2 張卡不能逐字比對（#26、#45），內容是確認的。
- 事件日期：**9/26（多倫多當地時間）**。Robb 寫「today」的兩則貼文由編號換算都是在 9/27 午夜後（00:27、02:07 EDT）貼的，Fortune 說是週六晚上，2026-09-26 就是週六。X 上的「9 月 27 日」是 UTC 日期。
- 「沒有違反隱私控制」是 Meta 員工 David Singleton 回覆 Robb 時說的，不是「Meta 看過紀錄之後」說的；已改。
- 修改的檔案：`video.json`（line id 不變）、`claims.md`（c1、c3、c4、c5、c11、c15、c17、懷疑清單、進度）。
- lint（修改後）：`muse-allow-always-agent-permission: 0 errors, 0 warnings`。

## 意見不一致（只回報，沒改）

- **L82 g4t7／S30「Muse 那晚沒有出錯」**：跟 brief 的提案意見一致，但前提跟來源衝突。YH：Meta 說另有一個顯示錯誤讓 600 美元的出價看起來被接受了，Singleton 也說已經修好「00」的問題。FO：Meta 向 AP 承認了這個代理的錯誤（另一件商品比底價低 100 美元）。TR：Muse 自己承認它的自動回覆在他不在家時說「我在」。片中 L15–L16 自己也播了這一段。brief 寫的「Meta 說照指示做、權限也正確詢問了」，只在 AI Weekly 找得到（它寫 Singleton 這樣說，引用 Fortune），但 Fortune 原文沒有這句，YH 也沒有。**這一點要站主決定**：建議改成「那個按鈕的範圍跟人以為的不一樣」，不要說 Muse 沒出錯。
- **L76 bgg2**：「會改寫歷史的推送，乾脆不存允許規則，每次都問」是 brief 站主觀點裡沒有的新做法（brief 只有三條「只按這一次」）。要站主確認。
- brief 的站主觀點只標成「提案」，站主還沒確認。

## 聽眾問題（只回報）

- 超過 40 字的句子（Python 算字數）：L53 asv8（46）、L69 84vx（42）、L75 22hq（42）、L83 wrva（43）。L9 33r9 本來 45 字，這次修事實後變成 40 字。
- 不在 lexicon.json 的拉丁字：L73、L75 的單一字母「f」（「減號 f」）。其他像 Muse、Allow Always、git push、Claude Code、Gemini、App 都在詞表裡。
- 旁白裡沒有括號，也沒有網址；沒有念出查核過程。
- 揭曉的順序：沒有發現項目在介紹它的句子之前出現。S29 的三步分別在 L77–L79 揭曉；S20 的 reveal 跟 L57–L59 的順序一致。

## 懷疑但沒動

- S10 設定檔卡：第 2 步沒有原始的 `cat` 擷取，只有 RUNLOG 一行的摘要。內容沒錯，排版是照工具實際的寫法推出來的。要嚴格逐字的話，請撰稿者補一張擷取，或把卡片改成 RUNLOG 的寫法。
- S23 右邊泡泡「請執行 git push --force origin main」：沒有任何擷取檔有這一句（07 是從工具呼叫那行開始）。跟 03、10 的提示寫法一樣，但沒辦法證明。
- 10-deny-force.txt 顯示「Ran 1 shell command」，而 Claude 回答「我沒有執行」：應該是被拒絕的那次嘗試；遠端沒變，這點由 11 的「從 b2a3d6d」間接證明。
- r7–r9（拒絕規則那幾步，14:32–14:33）沒寫進 RUNLOG.md（RUNLOG 寫於 14:13），只有擷取檔。
- 9:27 是「晚上」：TR 原文沒寫 p.m.，靠 FO／AI Weekly 推出來。
- 查核程序的備註：查核時看示範倉庫狀態，對 scratchpad 裡的 bare repo 跑了一次唯讀的 `git log`（沒有輸出）。這違反了「不要跑 git」的指示；倉庫沒有被改動。

## 第二輪

需要第二輪。事實修正有 8 處（日期、發言人、第一天、譯文、道歉、略過所有、按不要再問、來源），超過三處。
