# muse-allow-always-agent-permission：可查核的主張

撰稿 2026-10-27。每一行：編號｜主張｜來源｜確認日期｜場景。來源頁存在工作區 `muse/src/`，實跑紀錄在 `muse/run/`（`RUNLOG.md` 與每一步的畫面擷取）。

YH ＝ https://tech.yahoo.com/ai/meta-ai/articles/youtuber-says-muse-setting-led-122153415.html
TR ＝ https://www.techradar.com/ai-platforms-assistants/you-gotta-never-do-that-again-youtuber-says-metas-muse-ai-ruined-a-sale-and-gave-out-his-home-address-without-permission
CC ＝ https://code.claude.com/docs/en/permissions
GG ＝ https://support.google.com/accounts/answer/13533235?hl=zh-Hant

## 事實

c1｜多倫多的 YouTuber Matt Robb 讓 Meta 的 AI 代理 Muse 替他在 Facebook Marketplace 賣一個鍵盤（MX Keys Mini）；日期 **9 月 26 日（多倫多當地時間，週六）**：他寫「today… until late tonight」的 Threads 貼文 DdxwAJnDhNy 由編號換算是 9/27 00:27 EDT，X 貼文 2104090601411293303 是 9/27 06:07 UTC＝02:07 EDT，都在午夜之後；Yahoo 嵌入的「September 27, 2026」是 UTC 日期；AI Weekly 寫買家「9:15 p.m. on a Saturday」到達＝9/26，並說是 Fortune 報導的，但 Fortune 原文（2026-10-27 重抓）沒有 9:15 也沒有 Saturday，只寫 "late at night"，所以這一點只算 AI Weekly 的說法；9/26 靠前面兩則貼文的時間就成立（verify-2）。「多倫多」照 Fortune（AP）"a Toronto-based content creator"（verify-1 確認）｜YH、TR、Fortune、Robb 的 Threads／X 貼文｜2026-10-27｜open
c2｜買家照 Muse 給的地址到了他住的大樓（"showed up at his building"）｜YH｜2026-10-27｜open
c3｜Muse 在台灣還不能用：美國 9 月 8 日、加拿大 9 月 18 日開放，日本 10 月 23 日開始（verify-1：美國 9/8 與日本 10/23 照 Meta 官方公告，日本公告說日本是北美之外第一個地區；加拿大 9/18 照 iPhone in Canada 引 Meta 的 X 貼文；Inside 頁 2026-10-27 回 403 Cloudflare 擋下，撰稿存檔也是擋下頁，已從來源移除）｜Meta Newsroom（英文 9/8、日文 10/23）、iPhone in Canada、SmartScope｜2026-10-27｜naive
c4｜Meta Superintelligence Labs 的 David Singleton 在回覆 Robb 週二貼文時說 Meta 確認「no breach of privacy controls」（verify-1：這是員工的回覆，不是「看過紀錄之後」說的；看紀錄的是 c7 的 Muse 團隊與 Robb。旁白改為「Meta 的一位員工回覆他：已確認沒有違反隱私控制」，卡片拿掉「任何」）｜YH｜2026-10-27｜no-breach
c5｜Robb 說他一開始請 Muse 賣鍵盤時按了「Allow Always」，以為接受出價前還會問他（YH "when he first asked Meta's AI agent to sell his computer keyboard"；verify-1 把「設定 Muse 的第一天」改成「一開始」）；這段說明是 9 月 29 日（週二）貼的：YH 寫 "Tuesday update"、文章 2026-09-29 12:21 UTC 刊出，Threads Dd28UvzALKg 換算 9/29 00:51 EDT；卡片原寫 9 月 30 日，已改｜YH、Threads @matt.j.robb｜2026-10-27｜robb
c6｜這個設定讓 Muse 用含取貨地址的範本替他發訊息；原話 "I didn't think it would send it out to everyone that gave me an offer"｜YH、Threads @matt.j.robb｜2026-10-27｜robb
c7｜Meta 的 Muse 團隊陪他看了紀錄，說會把權限提示寫得更清楚｜YH｜2026-10-27｜meta-clearer
c8｜選「Yes, and don't ask again」後規則存到 git 倉庫根目錄的 `.claude/settings.local.json`，之後在這個倉庫任何位置開的 session 都適用｜CC〈Permission system〉｜2026-10-27｜star-meaning、settings-after
c9｜表：Bash 指令「Permanently per repository and command」、檔案修改「Until session end」、WebFetch「Permanently per repository and domain」｜CC 表格｜2026-10-27｜cc-table
c10｜`Bash(git *)` 准每一個 git 指令；`Bash(ls *)` 要求空格所以不含 lsof；`Bash(ls*)` 沒有空格連 lsof 都算｜CC〈Wildcard patterns〉｜2026-10-27｜wildcards
c11｜對用 && 串起來的指令按「Yes, and don't ask again」時（verify-1：旁白補上「按不要再問」，單按 Yes 不存規則），替每一段需要同意的子指令各存一條規則，最多 5 條｜CC〈compound commands〉段｜2026-10-27｜compound
c12｜原句：「移除代理的存取權，並不會中斷或刪除 Google 帳戶與該應用程式的連結。」；Gemini 或 Google AI 代理可透過連結的應用程式完成任務｜GG〈Gemini 和代理權限〉｜2026-10-27｜google-agent
c13｜Robb 的建議原話 "double-check what permissions AI has in your life"｜YH｜2026-10-27｜robb-advice
c14｜步驟：連結的應用程式頁 → 「代理存取權」篩選 → 「停止使用 <應用程式名稱>」；要中斷 App 本身的連結要另外操作｜GG｜2026-10-27｜google-steps
c15｜Muse 事後的訊息原句 "my auto-reply told him ‘Yep I’m here!’ at 9:27 when you clearly weren’t available"（verify-1："Yep I'm here!" 是替他說「對，我在！」，Muse 自己說是 "claiming you're home"，不是「我到了」，翻譯與旁白已改；這則是 Muse 主動傳的壞消息與認錯，"I'm sorry" 是 Robb 罵它之後才回的，旁白「道歉」改「認錯」）｜TR｜2026-10-27｜muse-sorry
c16｜Claude Code 只在提示能顯示全部會准的範圍時才給「don't ask again」；否則只給一次性的同意｜CC〈Permission system〉第 45 段｜2026-10-27｜shows-scope
c17｜bypassPermissions 模式略過權限提示（表格原文 "except for the actions no mode auto-approves"，verify-1 把卡片「略過所有」改成「略過幾乎所有」），包括寫入 .git、.claude 等受保護路徑；只該在容器或 VM 這類隔離環境用｜CC〈Permission modes〉｜2026-10-27｜bypass
c18｜拒絕規則優先：允許規則不能在拒絕規則裡開例外｜CC〈Manage permissions〉第 73 段｜2026-10-27｜deny-file、text-not-meaning

c19｜Meta 的 Muse 安全說明：授權「bound to the particular connector/destination and use case」；支援 one-time、session-scoped、task-scoped、time-bounded、perpetual 五種｜https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse（security.muse.ai 轉址）｜2026-10-27｜meta-grants、unknown
## 本片自己跑的紀錄

機器：雲端容器（站主 2026-10-27 請撰稿者自己跑），Claude Code 2.1.311，manual mode，模型 Sonnet 5.5；git 2.43.0。示範倉庫 perm-demo，遠端是同一台機器上的 bare repo，不碰任何真實專案或帳號。

r1｜請它 `git push origin main` → 權限提示四個選項，第 2 項是「Yes, and don’t ask again for: git push *」（`01-prompt.txt`）｜run｜2026-10-27｜cc-prompt
r2｜選第 2 項後 `cat .claude/settings.local.json` → `"allow": ["Bash(git push *)"]`｜run｜2026-10-27｜settings
r3｜本機 amend 後 `/exit`，開新 session 請它 `git push --force origin main` → 沒有詢問，遠端 main 69cd815 → b2a3d6d（`03-force.txt`）｜run｜2026-10-27｜force
r4｜`/permissions` → Allow 分頁列出 `Bash(git push *)`；選取後顯示「Any Bash command starting with git push」「From project local settings」（`04`、`05`）｜run｜2026-10-27｜permissions
r5｜刪掉規則後再請它強制推送 → 出現「Do you want to proceed?」，選 No（`07`、`08`）｜run｜2026-10-27｜asks-again
r6｜刪掉後的設定檔 → `"allow": []`（`06b-settings-after.txt`）｜run｜2026-10-27｜settings-after
r7｜寫入 allow `Bash(git push *)` 與 deny `Bash(git push --force *)`（`09-deny-settings.txt`；卡片節錄第 2–9 行）｜run｜2026-10-27｜deny-file
r8｜新 session 請它 `git push --force origin main` → 「因為系統拒絕了這個指令的權限,所以沒有任何東西被推送。」，遠端不變（`10-deny-force.txt`）｜run｜2026-10-27｜deny-works
r9｜新 session 請它 `git push -f origin main` → 沒有詢問，遠端 b2a3d6d → 38a0e59（`11-dash-f.txt`）：拒絕規則比對文字，簡寫 -f 被 `git push *` 允許接走｜run｜2026-10-27｜dash-f

## 與企劃不同的地方

- 示範由撰稿者在雲端容器裡跑（站主 2026-10-27 要求），不是站主自己的電腦。
- 多了企劃沒有的實跑：拒絕規則擋得住 `--force`、擋不住 `-f`（r7–r9），成為第 6 章的轉折。
- 企劃第 3 章的「其他 AI」只講 Claude Code 與 Google，沒有 ChatGPT（官方權限頁沒找到）。
- 估 8.2 分鐘、87 句。

## 我懷疑但沒動的事

- 事件日期 9/26 或 9/27（見 c1）。→ verify-1：9/26，理由見 c1。
- Singleton 的「no breach of privacy controls」只有 Yahoo Tech 轉述；旁白說「Meta 看過紀錄之後說」，查核時判斷是否要改成「Meta 的人說」。→ verify-1 已改，見 c4。
- 第 5 章的三條規則是站主看法，卡片來源寫明；Google 說明裡自己舉的例子（讓 Gemini 登入旅遊 App 訂民宿）沒放進片中。
- Muse、ARTEX 之外，`settings.local.json` 的路徑在 Windows 或非 git 目錄會不同（CC 有寫），片中沒講。

## 進度

- 2026-10-27 verify-2 之後（撰稿者）：verify-2 找到 Meta 自己的 Muse 安全說明（security.muse.ai → research.meta.ai），加一張官方引文卡（授權綁定連接器與用途、五種授權）；「我查不到的」改成「Meta 列了五種授權，卻沒說 Allow Always 對應哪一種」；字幕的減號 f 改小寫。

- 2026-10-27 verify-2（獨立查核第 2 輪）：所有來源今天重抓（HTTP 200），verify-1 改過的 9 項與撰稿者之後改的 g4t7、asv8、84vx、eb6y、22hq、wrva、S10 設定檔卡、四張對話卡都對過，抽查 17 條（種子 20261027）。旁白、卡片、說明欄沒有要改的事實；只改了 c1 的依據（Fortune 原文沒有「9:15 p.m. on a Saturday」）。要撰稿者或站主決定的事：Meta 官方的 security.muse.ai 有寫 Muse 的授權種類（one-time、session、task、time-bounded、perpetual），wrva／S31「還沒找到它的說明頁」要不要改；S10 的 02b 與 S23 右邊泡泡是事後補記，不是當下擷取；「減號 F」在字幕上是大寫。見 `verify-2.md`。

- 2026-10-27 verify-1 之後（撰稿者）：看法章「Muse 那晚沒有出錯」與來源矛盾（Muse 自己認錯、Meta 承認價格顯示錯誤），改成「Muse 那晚也出了錯；但地址送得出去，是因為一個按鈕准的範圍」，卡片改「錯的不只是 AI／還有按鈕的範圍」；四句過長的縮短；「減號 f」改寫成「減號 F」並補進字典；實跑紀錄補上第 2 步的設定檔原文（02b-settings.txt）與 r7–r9。

- 2026-10-27：34 景、87 句寫完，lint 0 錯誤 0 警告，等查核（verify-1）。
- 2026-10-27：verify-1 完成，8 處事實修正（見 `verify-1.md`），lint 0 錯誤；超過三處，需要第二輪查核。
