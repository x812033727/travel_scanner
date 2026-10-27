# 你按了「一律允許」，AI 就替你把地址給了陌生人：一個按鈕到底准了多少事

企劃日期 2026-10-27。AI／科技時事，**教學卡片短片**（`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，
teaching-flow §十「一個概念」；結構接 `artex-ai-attack-leftover-keys`，例子、開場與卡片順序換掉）。
字卡主語言 zh-TW，產品、設定名稱、引文、指令保留英文（SKILL.md 規矩 14）。站上沒有這則新聞的文章，沒有 `source_guide`。

事實來源（2026-10-27 開過，原始頁存在工作區 `_tools/sources/`）：
當事人 Matt Robb 自己在 Threads 與 X 上的說明（他按了 Allow Always、Muse 用含取貨地址的回覆範本、Meta 團隊看過紀錄後說會把權限提示寫清楚）；
Yahoo Tech（Business Insider）與 TechRadar 的報導（Meta 的 David Singleton 說「沒有違反隱私控制」，Muse 自己的道歉訊息）；
Claude Code 官方文件〈Configure permissions〉（「Yes, and don't ask again」存到哪、存多久、萬用字元怎麼比對、`/permissions`）；
Google 帳戶說明〈管理 Google 帳戶與第三方應用程式之間的連結〉的〈Gemini 和代理權限〉一節（「代理存取權」篩選、移除代理存取權不等於中斷連結）。
Meta 自己的 Muse 權限說明頁 **還沒找到**（第三方指南說選項是 Allow once／this task／this site／Deny，但不是官方頁）：撰稿前要找到，找不到就只引用當事人與 Meta 發言人的話。

## 先搜（news-flow §一；YouTube 搜尋依觀看數、本週，2026-10-27）

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| He used Meta's AI agent Muse for Marketplace sales. Then it set one up behind his back | CBC News | 2:40 | 22 萬 | 6 天前 |
| A Night of Terror with Muse: The Hottest AI Star Since ChatGPT... The Dark Side of Innovation! | 莊也雜談 | 47:26 | 21 萬 | 1 天前 |
| Zuckerberg's "Personal Superintelligence" Underwhelms | Wall Street Millennial | 11:59 | 16 萬 | 5 天前 |
| AI助理争夺战：解析Muse、Grok Bot与Instinct背后的产品布局 | 硅谷101 | 33:29 | 13 萬 | 4 天前 |
| Canada monitoring new Meta AI agent 'Muse' as BMO CEO warns about its risks | Global News | 1:55 | 12 萬 | 4 天前 |
| 【Free!?】AI Assistant "Muse" Finally Lands in Japan! | AIで創作効率化 | 13:21 | 12 萬 | 3 天前 |
| Meta"ナンバー2"が語る「Muse」日本上陸 | TBS CROSS DIG with Bloomberg | 23:44 | 11 萬 | 3 天前 |

讀法：沒有達到「三家各 20 萬」的門檻（只有 CBC 與莊也雜談過 20 萬），但這一群還在長：Muse 剛在日本上線，中文頻道開始做。
新聞台講的是「AI 把地址給了陌生人」；沒有人講**那個按鈕到底准了什麼**，也沒有人給還用不到 Muse 的台灣觀眾一個能做的檢查。
Muse 目前在台灣還不能用（Inside、數位時代等報導，美國、加拿大先開；日本 10 月下旬上線，撰稿時要找 Meta 官方公告），
所以這支的動作放在台灣觀眾已經在用、而且有同一種按鈕的工具上。本週其他群的量測在 `docs/videos/reference-study-20261026-ai-news/README.md`，這一群的原始搜尋結果存在工作區。

## 觀眾

在台灣用 Gemini、ChatGPT 或 Claude，最近開始讓 AI 代理替自己做事（訂位、回訊息、整理信件、寫程式）的人；
用 Claude Code 寫程式、按過很多次「Yes, and don't ask again」的工程師與 vibe coding 新手；看到 Muse 新聞想知道「AI 代理安不安全」的人。
他們搜尋的是「Meta Muse 台灣」「Muse 地址 陌生人」「AI 代理 權限」「一律允許 安全嗎」「Claude Code don't ask again」。
他們以為「一律允許」是「這件事以後不用問我」；不知道它准的是一整類動作，而且有時候一直有效、跨到下一次對話。

## 觀眾看完能做到的事

- 在 Claude Code 裡用 `/permissions` 列出自己按過「Yes, and don't ask again」存下的規則，認出哪一條比自己以為的寬（`Bash(git push *)` 准的是每一種 git push），刪掉或改窄
  （第 5 章；CITED：Claude Code〈Configure permissions〉的表格與萬用字元一節；要先實作：見下）。
- 在 Google 帳戶的「連結的應用程式」用「代理存取權」篩選，找出 Gemini 或 Google 代理能操作的 App，並知道「停止使用」只收回代理的權限、不會中斷 Google 帳戶與那個 App 的連結
  （第 5 章，`steps`＋`quote`；CITED：Google 帳戶說明〈Gemini 和代理權限〉原句）。
- 給代理授權前，用一條規則選範圍：會花錢、會送出個人資料（地址、電話）、會替你回覆別人的動作，只按「這一次」，不按「一律」
  （第 4、6 章，`compare`；依據：Robb 的事件經過與他自己的建議原句 "double-check what permissions AI has in your life"）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，這一段是提案，站主選大綱時確認或改寫。）
我的看法是：Muse 這件事最值得記住的不是「AI 出錯」，是 Meta 說它「照指示做、權限也正確詢問了」——它沒出錯，錯的是那個按鈕的範圍跟人以為的不一樣。
「一律允許」准的是一類動作，不是一件事；而且在有些工具裡，它會一直有效到你自己去刪。
我不會叫大家別用代理；我的做法是：會花錢、會把我的資料送出去、會替我回別人的事，永遠只按「這一次」。
我查不到的：Meta 的權限選項官方怎麼定義（還沒找到 Meta 的說明頁）、Muse 什麼時候來台灣。

## 示範或實算

製作路線：教學卡片短片，`theme: "paper"`。一個生活對照撐全片：**給管理員的大樓門禁卡**——你只是想讓管理員幫你收一個包裹，
給的卻是一張整棟大樓、每天都能刷的卡；卡上不會寫「只能收包裹」。哪裡不能照比喻理解：門禁卡你記得給過誰，這些授權你多半忘了按過。

- 主例（要先實作；站主或撰稿者在一台有 Claude Code 的機器上，乾淨的示範倉庫，不用任何人的帳號畫面）：
  1. 示範倉庫 `perm-demo`（`git init`，一個本機的 bare remote 當 `origin`）。
  2. 在 Claude Code 裡請它 `git push origin main`，出現權限提示時選「Yes, and don't ask again」。
  3. `cat .claude/settings.local.json` → 預期看到一條 `Bash(git push *)` 之類的規則（**觀眾猜不到的結果**：自己只准了一次推送，檔案裡寫的是所有 git push）。
  4. 再請它 `git push --force origin main` → 預期不再問就執行（同一條規則涵蓋）。
  5. `/permissions` → 看到這條規則與它來自哪個設定檔；刪掉後再推一次 → 又會詢問。
  每一步記下指令、輸出、日期與 Claude Code 版本（`claude --version`）。示範結束刪掉倉庫。
- 不用這個方法：觀眾今天最簡單的一步是「被問的時候看清楚再按」。這支片比那一步多的，是：按下去之後**存在哪裡、存多久、准了哪些沒被問到的指令**，以及去哪裡收回。
- 對照（CITED）：Claude Code 文件的表格——Bash 指令的「don't ask again」是 Permanently per repository and command，檔案修改只到 session 結束；
  萬用字元一節——`Bash(git *)` 准每一個 git 子指令，`Bash(ls*)` 沒有空格會連 `lsof` 都准。
- 要先實作：上面五步。Claude Code 的互動提示需要人按，容器裡的 headless 模式不會出現同一個選單；做不到就把第 3、4 步降為 CITED（文件原句），並在 `claims.md` 說明。
- 示範在第 5 章（`terminal`×3、`code`（settings.local.json 全文）、`steps`（/permissions））。

## 大綱

### 選項 A（推薦）：一個按鈕准了多少事——從 Muse 的地址講到你自己的「don't ask again」

角度：整支只講一個概念「一律允許准的是一類動作，不是一件事」，章名是觀眾的問題；跟 B 差在不照事件時間線走，跟 C 差在不做四家產品的比較表。

開場（五句，20 秒內）：「9 月 26 日晚上，一位多倫多的 YouTuber 讓 Meta 的 AI 代理 Muse 替他在 Marketplace 賣一個鍵盤；買家按照 Muse 給的地址，開車到了他家樓下。」／
「你可能會問：Muse 台灣又還不能用，這關我什麼事？」／「有關：Meta 看過紀錄說，Muse 是照指示做、權限也正確問過了——問題出在他第一天按的那個『一律允許』。」／
「同一種按鈕，你在 Gemini、在 Claude Code 裡都按過，有的會一直有效到你自己去刪。」／「接著用他的事件講那個按鈕准了什麼，再到三個地方，把你按過的『一律』找出來。」

案例與結果：「示範倉庫按一次『Yes, and don't ask again』，設定檔寫的是所有 git push，連 --force 都不再問；證據 RUN（待第 5 章實作）＋ CITED（Claude Code 文件）。」

1. 一個按鈕，一個陌生人（55 秒）`title` → `big`（你可能會問）→ `big`（Meta：照指示做、權限有問）→ `big`（同一種按鈕你也按過）。
2. 那個按鈕到底准了什麼？（90 秒）`quote`（Robb：I didn't think it would send it out to everyone）→ `compare`（他以為：以後回覆前還會問我／實際：以後這一類訊息都不問，範本裡有地址）→ `big`（准的是一類動作，不是一件事）→ `compare`（門禁卡對照）。收尾問題：「那是 Meta 的問題，還是按鈕本來就這樣？」
3. 其他 AI 的「一律」也一樣嗎？（80 秒）`table`（Claude Code：Bash 指令永久、檔案修改到 session 結束；Google 代理存取權：到你停用為止；Muse：一律允許）→ `quote`（Google：移除代理存取權不會中斷連結）。收尾問題：「我按過的那些，現在還有效嗎？」
4. 哪些事永遠只按「這一次」？（60 秒）`steps`（花錢、送出個人資料、替你回覆別人）→ `big`（Robb 自己的建議）。
5. 我按過的「一律」，去哪裡收回？（150 秒）`terminal`（git push 的提示）→ `code`（settings.local.json）→ `big`（我只准了一次，它寫的是全部）→ `terminal`（--force 不再問）→ `steps`（/permissions 刪掉）→ `steps`（Google 連結的應用程式 → 代理存取權 → 停止使用）。
6. 我的看法：代理還要不要用（50 秒）`big`（它沒出錯，按鈕的範圍出錯）→ `big`（我查不到的）→ `big`（答案）→ `outro`（留言題：你按過幾次 don't ask again？）。

### 選項 B：那一晚的 3 個小時——照 Robb 的事件時間線走

角度：事件型，照 9/26 晚上 → 9/27 他的貼文 → Meta 的回應 → 他的更新，一格一件事；權限的機制在後半段才講。
開場：「晚上 9 點 15 分，一個買家站在多倫多一棟大樓樓下，手機上是 AI 給他的地址。」
風險：時間細節各家報導不一致（9:15、9:27、8–10 點），觀眾的檢查要到最後一章才出現。

### 選項 C：四個 AI 代理的「一律允許」比一比

角度：Muse、Gemini、ChatGPT agent、Claude Code 各自的權限選項與有效期間排成表，收在一張「該按哪一個」的對照。
風險：ChatGPT 與 Muse 的官方權限說明頁都還沒找到，表會有空格；也容易變成念清單（盲讀的 no_detour）。

## 會過期的事實

- Claude Code 權限行為（存哪裡、存多久、萬用字元）：https://code.claude.com/docs/en/permissions （文件寫了 v2.1.211、v2.1.234 的行為改變，撰稿當天再開）
- Google 代理存取權：https://support.google.com/accounts/answer/13533235?hl=zh-Hant
- Muse 是否在台灣、日本上線：找 Meta Newsroom 官方公告（撰稿前必查）
- Robb 的說明：Threads @matt.j.robb、X @MattRobbt（9/27、9/30）；Meta 的回應：Yahoo Tech、TechRadar 轉述

## 素材

- `screencast`：Claude Code 權限文件頁的表格（公開頁）；Google 帳戶說明頁〈Gemini 和代理權限〉一節（公開頁）
- `terminal`／`code`：第 5 章的示範紀錄（待實作）
- 不放 Robb 的截圖或任何人的帳號畫面；不畫 AI 插圖

## 不做的事

- 不評 Muse 好不好用、不比較各家代理的能力
- 不講 Muse 讀私訊的另一則報導（TechRadar 連結的另一篇，另案）
- 不講報導之間不一致的價格與時間細節（10 美元、600 美元、9:15／9:27），只講事件的形狀
- 不說 Meta 有錯或沒錯，只引 Meta 與當事人各自的話
