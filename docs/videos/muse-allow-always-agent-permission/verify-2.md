# muse-allow-always-agent-permission：查核第 2 輪（verify-2）

查核日 2026-10-27。查核者是獨立的代理，沒有寫這支稿，也沒有做第 1 輪。所有來源今天用 `Mokaair-editorial/1.0` 重新抓過，同一台主機的兩次抓取至少隔 1 秒，比對前先拿掉 `<!-- -->`。抓下來的頁面在 scratchpad 的 `muse/verify2/dl/`，比對腳本在 `muse/verify2/`（`cardcheck.py`、`ids.py`、`sample.py`、`lens.py`）。網路搜尋用了 2 次，沒有重跑 Claude Code，也沒有跑任何 git 指令。

簡稱：YH＝Yahoo Tech（Business Insider）、TR＝TechRadar、FO＝Fortune（AP）、TH＝Robb 的 Threads 貼文、CC＝code.claude.com/docs/en/permissions（含 `.md` 版）、GG＝Google 帳戶說明 13533235（zh-Hant）、MU＝Meta Newsroom 9/8、MJ＝Meta 日本 10/23、IC＝iPhone in Canada 9/18、SS＝SmartScope、MS＝security.muse.ai（Meta 的〈How We Built Safety Into Muse〉，從 MU 連過去）、RUN＝`muse/run/` 的擷取檔。

| 來源 | HTTP（2026-10-27 14:48–14:52 UTC） |
| --- | --- |
| YH https://tech.yahoo.com/ai/meta-ai/articles/youtuber-says-muse-setting-led-122153415.html | 200 |
| TR https://www.techradar.com/ai-platforms-assistants/you-gotta-never-do-that-again-youtuber-says-metas-muse-ai-ruined-a-sale-and-gave-out-his-home-address-without-permission | 200 |
| TH https://www.threads.com/@matt.j.robb/post/Dd28UvzALKg/… 與 /post/DdxwAJnDhNy | 200／200 |
| FO https://fortune.com/2026/10/19/meta-muse-ai-agent-facebook-marketplace-home-address-privacy/ | 200 |
| CC https://code.claude.com/docs/en/permissions 與 permissions.md | 200／200 |
| GG https://support.google.com/accounts/answer/13533235?hl=zh-Hant | 200 |
| MU https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ | 200 |
| MJ https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent-launches-in-japan/ | 200 |
| IC https://www.iphoneincanada.ca/2026/09/18/metas-muse-ai-agent-is-now-available-in-canada/ | 200 |
| SS https://smartscope.blog/en/blog/meta-muse-japan-launch-free-plan-limitations-invite-2026/ | 200 |
| MS http://security.muse.ai | 200 |

抽查的種子：`20261027`。verify-1 的 65 條裡有 49 條 CONFIRMED，用 `random.Random(20261027).sample` 抽 17 條（三分之一，無條件進位）：#2、3、4、6、10、12、13、16、20、32、33、38、45、47、48、51、55。

## 主張表

### A. verify-1 標成 CHANGED 的 9 條

| # | 主張（現在的寫法） | 在哪裡 | 來源 | HTTP | 判定 | 說明 |
| --- | --- | --- | --- | --- | --- | --- |
| A1（v1#7） | 「Meta 的一位員工回覆他：已確認沒有違反隱私控制」；kicker「Meta 員工的回覆」；卡片「沒有違反 隱私控制」 | L5 tech、S2、說明欄 | YH | 200 | CONFIRMED | YH："In a reply to Robb's Tuesday post, David Singleton, a Meta Superintelligence Labs staffer, said that Meta had confirmed there was "no breach of privacy controls."" |
| A2（v1#8） | 「一開始」按下的按鈕；「一開始賣鍵盤時，他按了 Allow Always」；keys「一開始就按了 Allow Always」 | L6、L9、S4 | YH、FO | 200 | CONFIRMED | YH "when he first asked Meta's AI agent to sell his computer keyboard"；FO "when he first let Muse on his Facebook Marketplace profile" |
| A3（v1#9） | 引文卡日期「9 月 29 日」 | S4 kicker | YH、TH | 200 | CONFIRMED | YH "a Tuesday update on X"，`datePublished` 2026-09-29T12:21:53Z；2026-09-29 是週二；TH Dd28UvzALKg 由編號換算 9/29 00:51 EDT（`ids.py`，自己重算） |
| A4（v1#17） | 譯文「對，我在！」、keys「說「我在」」、L15「跟買家回了一句：對，我在」 | S5、L15 | TR | 200 | CONFIRMED | TR："my auto-reply told him ‘Yep I’m here!’ at 9:27 when you clearly weren’t available … stop the auto-replies from claiming you’re home" |
| A5（v1#18） | 「Muse 事後自己傳訊息跟他認錯」 | L14 85ie | TR | 200 | CONFIRMED | 9:27 那則是 Muse 主動傳的（"Bad news on the MX Keys Mini pickup… Worse…"），"I'm sorry" 是 Robb 回罵之後才有；「認錯」合 |
| A6（v1#37） | 「略過**幾乎所有**權限詢問」 | S17 | CC〈Permission modes〉 | 200 | CONFIRMED | "Skips permission prompts, except for the actions no mode auto-approves" |
| A7（v1#39） | 「你對一串用連接符號串起來的指令按不要再問，…各存一條規則，最多五條」 | L51 82fs、L52、S18 | CC〈Compound commands〉 | 200 | CONFIRMED | "When you approve a compound command with "Yes, and don't ask again", Claude Code saves a separate rule for each subcommand that requires approval… Up to 5 rules" |
| A8（v1#62） | 說明欄「照 Meta 的公告與 iPhone in Canada 的報導」：美國、加拿大、日本開放，台灣還不能用 | 說明欄、S1、L4 | MU、IC、MJ | 200 | CONFIRMED | MU 9/8 "rolling out in the US"；IC 引 Meta 9/18（週五）的 X 貼文 "Made it to Canada"；MJ 10/23 起在日本，「北米以外で、初めての提供地域」。搜尋 1 次沒找到台灣上線的消息 |
| A9（v1#63） | sources 清單 10 筆、checked_on | sources | 如上 | 200 | CONFIRMED | 10 筆今天都抓得到，checked_on 2026-10-27 就是今天，不用改 |

### B. 撰稿者在 verify-1 之後改的地方

| # | 主張 | 在哪裡 | 來源 | HTTP | 判定 | 說明 |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 「Muse 那晚也出了錯」 | L82 g4t7 | TR、YH、FO | 200 | CONFIRMED | Muse 自己的訊息認了 9:27 的自動回覆在他不在時說「我在」（TR）；Robb 說 Meta 告訴他另有顯示錯誤讓 600 美元的出價看起來被接受，Singleton 說已修好「00」的問題（YH）；FO：Meta 向 AP 承認了另一件商品的錯誤 |
| B2 | 「地址送得出去，是因為一個按鈕准的範圍，跟人以為的不一樣」 | L82 g4t7 | YH、TH | 200 | CONFIRMED | TH："By doing that it granted Muse permission to send messages on my behalf going forwards using a template… Which also included the pickup address… I didn’t think it would send it out to everyone that gave me an offer"；YH "Robb said Meta has since explained what happened: he had clicked an "Allow Always" setting" |
| B3 | 看法卡「錯的不只是 AI／還有按鈕的範圍」、key「照規則做，規則是你按出來的」 | S30 | 同 B1、B2 | 200 | CONFIRMED（前提）＋意見 | 前提跟來源一致；跟 brief 的提案意見不同，見下 |
| B4 | 「Gemini 這類代理，能透過你連結的 App 替你做事」 | L53 asv8 | GG | 200 | CONFIRMED | 「如果允許 Gemini 或 Google AI 代理與連結的應用程式互動，代理就能透過該應用程式為您完成任務」 |
| B5 | 「把允許加回去，再加一條拒絕：git push 加強制旗標開頭的，都擋」 | L69 84vx | RUN 09 | — | CONFIRMED | 09：allow `Bash(git push *)`、deny `Bash(git push --force *)` |
| B6 | 「強制推送有一個簡寫，減號 F；我改用這個寫法請它推送」 | L73 eb6y | RUN 11 | — | CONFIRMED（念法）／見懷疑清單 | 11 第一行「請執行 git push -f origin main」。念出來一樣，但旁白文字是大寫 F，實際旗標是小寫 -f |
| B7 | 「擋住的只是那幾個字；簡寫的減號 F，被 git push 星號那條允許接走了」 | L75 22hq | RUN 11、CC〈What a Bash rule doesn't match〉 | 200 | CONFIRMED | 11：沒有詢問，b2a3d6d → 38a0e59；CC："It doesn't match the same program invoked in a different form, so a deny or ask rule… isn't a security boundary" |
| B8 | 「我查不到的是：Meta 怎麼定義 Muse 那幾個允許選項，我還沒找到它的說明頁」 | L83 wrva、S31 | MS | 200 | OUT OF SCOPE（站主自己的查找狀況），列進懷疑清單 | Meta 自己的 MS 頁寫了 "Muse has support for obtaining one-time, session-scoped, task-scoped, time-bounded, or perpetual permission"、授權 "bound to the particular connector/destination and use case"。它沒有寫「Allow Always」這個按鈕對應哪一種，所以「怎麼定義那幾個選項」嚴格說仍查不到；但「還沒找到它的說明頁」容易被觀眾一查就推翻 |
| B9 | S10 設定檔卡：`{ "permissions": { "allow": [ "Bash(git push *)" ] } }`（兩格縮排，7 行） | S10 | RUN 02b、RUNLOG 補記 | — | CONFIRMED（內容）；逐字只對得上事後補記 | 卡片跟 02b-settings.txt 逐字相同（`cardcheck.py`）。但 02b 的時間是 14:46:55，跟 RUNLOG 補記同一刻，補記自己寫「當時沒有另存檔案」：這是撰稿者事後照記憶補的，不是當下的擷取。內容跟 RUNLOG 第 2 步一致，排版跟工具真的寫出來的 06b（14:32 的 cat）一樣 |
| B10 | S12 對話卡：「請執行 git push --force origin main」／「強制推送已完成。main 已從 69cd815 強制更新到 b2a3d6d」 | S12 | RUN 03 | — | CONFIRMED | 兩個泡泡都是 03 的連續節錄 |
| B11 | S23 對話卡：「請執行 git push --force origin main」／「Do you want to proceed?」 | S23 | RUN 07、RUNLOG 補記 | — | CONFIRMED（左）；右邊只有 RUNLOG 補記 | 左邊在 07。右邊不在任何擷取檔裡：補記說每次請求都是這句原文，但它指的「03、10、11 的第一行」是另外三次請求，不是 07 這一次 |
| B12 | S26 對話卡：「請執行 git push --force origin main」／「因為系統拒絕了這個指令的權限,所以沒有任何東西被推送。」 | S26 | RUN 10 | — | CONFIRMED | 右邊是 10 第一行；左邊是 10 的連續節錄（從句中「因為」開始，前面省了「我沒有執行 git push --force origin main,」），半形逗號照原樣 |
| B13 | S27 對話卡：「請執行 git push -f origin main」／「main 在 origin 上從 b2a3d6d 被強制更新為 38a0e59。」 | S27 | RUN 11 | — | CONFIRMED | 兩個泡泡都在 11 |

### C. 抽查 verify-1 的 CONFIRMED（種子 20261027，17 條）

| # | 主張 | 來源 | HTTP | 判定 | 說明 |
| --- | --- | --- | --- | --- | --- |
| C1（v1#2） | 多倫多的 YouTuber | FO | 200 | CONFIRMED | "a Toronto-based content creator who regularly reviews consumer tech" |
| C2（v1#3） | 讓 Muse 替他在 Marketplace 賣鍵盤 | YH、TR | 200 | CONFIRMED | YH "sell his computer keyboard on Facebook Marketplace"；TR "MX Keys Mini" |
| C3（v1#4） | 那天晚上，買家照 Muse 給的地址開車到他家樓下 | YH、TR、FO | 200 | CONFIRMED | YH "showed up at his building"；TR "drove 30 minutes to Robb's home"、"I'm in an apartment with security"；FO "late at night" |
| C4（v1#6） | 美國 9/8、加拿大 9/18、日本 10/23 | MU、IC、MJ | 200 | CONFIRMED | 見 A8；2026-09-18 是週五，跟 IC 的 "on Friday" 一致 |
| C5（v1#10） | 引文 "I didn't think it would send it out to everyone that gave me an offer" | YH、TH | 200 | CONFIRMED | 跟 YH 逐字相同 |
| C6（v1#12） | 他按了 Allow Always | YH | 200 | CONFIRMED | "he had selected an "Allow Always" option" |
| C7（v1#13） | 以為 Muse 接受出價前還會先問他 | YH | 200 | CONFIRMED | "believing it would still seek his approval before accepting offers" |
| C8（v1#16） | Muse 訊息原句（含彎引號） | TR | 200 | CONFIRMED | 逐字相同 |
| C9（v1#20） | 他那時根本不在家 | TR | 200 | CONFIRMED | "while he was out"；"when you clearly weren’t available" |
| C10（v1#32） | 換了對話，記得全部的推送，連強制推送也算 | RUN 03、RUNLOG | — | CONFIRMED | /exit 後的新 session，沒有詢問，69cd815 → b2a3d6d |
| C11（v1#33） | 表格：執行指令永久整個倉庫、修改檔案到對話結束、抓網頁永久以網域為單位 | CC | 200 | CONFIRMED | "Permanently per repository and command"／"Until session end"／"Permanently per repository and domain" |
| C12（v1#38） | 連寫進 git 和設定資料夾都不問；只在容器或虛擬機用 | CC | 200 | CONFIRMED | "including for writes to protected paths such as `.git` and `.claude`… Only use this mode in isolated environments like containers or VMs where Claude Code can't cause damage"。L50 的「壞了也沒關係」是意譯，原文是「Claude Code 造成不了損害」，意思沒偏 |
| C13（v1#45） | 刪掉後再請它強制推送，又停下來問 | RUN 07 | — | CONFIRMED | 見 B11 |
| C14（v1#47） | 這份檔案每個倉庫各有一份 | CC | 200 | CONFIRMED | "saves the rule to `.claude/settings.local.json` at the root of the git repository" |
| C15（v1#48） | 拒絕設定檔第 2–9 行（共 10 行） | RUN 09 | — | CONFIRMED | 逐字相同，09 共 10 行 |
| C16（v1#51） | 「因為系統拒絕了這個指令的權限,所以沒有任何東西被推送。」 | RUN 10 | — | CONFIRMED | 見 B12 |
| C17（v1#55） | Google 步驟：連結的應用程式 → 代理存取權 → 停止使用；要斷 App 再另外移除 | GG | 200 | CONFIRMED | 「前往 Google 帳戶的「連結的應用程式」頁面」「選取「代理存取權」篩選器」「選取「停止使用 <應用程式名稱>」」；移除連結另有「移除存取權」 |

### D. 查核時順帶發現

| # | 主張 | 在哪裡 | 來源 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | c1 的依據「Fortune（經 AI Weekly 轉述）寫買家「9:15 p.m. on a Saturday」到達」 | claims.md c1（旁白沒有用到） | FO、AI Weekly（verify-1 存檔） | 200 | CHANGED（只改 claims.md） | Fortune 原文沒有 9:15，也沒有 Saturday，只寫 "late at night"；這句是 AI Weekly 自己的說法。改成「AI Weekly 寫…並說是 Fortune 報導的，但 Fortune 原文…沒有」。9 月 26 日本身不受影響：Threads DdxwAJnDhNy（9/27 00:27 EDT）寫「today… until late tonight」，X 2104090601411293303（9/27 02:07 EDT），兩個時間都是重算的 |

## 摘要

- 查了 40 條：CONFIRMED 38、CHANGED 1（D1，只改 claims.md c1 的依據，旁白、卡片、說明欄、標題、縮圖都沒動）、NOT FOUND 0、OUT OF SCOPE 1（B8，站主自己的查找狀況）。verify-1 改過的 9 條今天都對得上，撰稿者之後改的 g4t7 兩半句（「也出了錯」「按鈕准的範圍」）都有來源。
- 修改的檔案：`claims.md`（c1 的依據、`## 進度` 加一行）。`video.json` 沒有改。
- lint（修改後）：`muse-allow-always-agent-permission: 0 errors, 0 warnings`。

## 意見不一致（只回報，沒改）

- **L82 g4t7／S30**：現在寫「Muse 那晚也出了錯；…錯的不只是 AI，還有按鈕的範圍」。brief 的站主觀點寫的是「它沒出錯，錯的是那個按鈕的範圍」，兩者方向不同。新寫法跟來源一致，舊的不一致，但這是站主的看法，要站主確認改過的版本。（另外：GadgetReview、Dexerto 等報導寫 Singleton 說之前調查類似回報時，Muse「following direct instructions and correctly asked for permission」；本輪沒有開這些頁，片中也沒有用這句。）
- **L76 bgg2**：「會改寫歷史的推送，乾脆不存允許規則，每次都問」不在 brief 的三條做法裡，跟 verify-1 回報的一樣，還沒有站主確認。
- **L83 wrva／S31**：brief 寫「我查不到的：Meta 的權限選項官方怎麼定義（還沒找到 Meta 的說明頁）」，片子照寫；但 Meta 的 security.muse.ai 有寫授權種類（見 B8）。站主可能想改這張「我查不到的」。
- brief 的站主觀點仍標成「提案」。

## 聽眾問題（只回報）

- 照字元數超過 40 字的句子（含標點與空格）：L53 asv8（44）、L82 g4t7（41）、L83 wrva（41）。lint 的算法（不算標點，英文字另計）沒有警告。撰稿者說縮短的四句裡，84vx（38）、22hq（39）已經在 40 以內，asv8 還是 44。
- 拉丁字都在 lexicon.json 裡（「F」是撰稿者加進去的）。
- 「減號 F」：念出來沒問題，但字幕照旁白文字顯示，會讓人以為旗標是大寫 `-F`（git push 的強制簡寫是小寫 `-f`，卡片 S27 寫對了）。
- 旁白裡沒有括號，也沒有網址，沒有念出查核過程。
- 揭曉順序：沒有發現某一項在介紹它的句子之前出現（S20、S29 的 reveal 跟 L57–L59、L77–L79 一一對應）。

## 懷疑但沒動

- **S10 設定檔卡（B9）**：02b-settings.txt 是 14:46 跟 RUNLOG 補記一起寫的事後補記，不是當下的擷取。內容沒問題，逐字排版沒有當下的證據。
- **S23 右邊泡泡（B11）**：只有 RUNLOG 補記說請求原文是「請執行 git push --force origin main」，07 的擷取裡沒有。
- **wrva／S31（B8）**：Meta 的 security.muse.ai 有寫授權種類，包括 perpetual；它沒有把「Allow Always」對到其中一種。要不要改這句是撰稿者或站主的事，改的話會動到看法章，所以我沒改。
- **「減號 F」大小寫**：見上面的聽眾問題。改回小寫的話，要先確認 lexicon 的比對會不會把小寫 f 也當成已登錄。
- 10-deny-force.txt 的輸入框裡留著「! git push --force origin main」：從 11 的「從 b2a3d6d」可以看出沒有送出。

## 能不能算查核完成

可以算查核完成：沒有 NOT FOUND，旁白、卡片、說明欄沒有錯的事實。上架前有兩件事要站主決定：看法章跟 brief 的提案不同（g4t7、bgg2），以及 wrva「還沒找到它的說明頁」要不要因為 security.muse.ai 而改寫。
