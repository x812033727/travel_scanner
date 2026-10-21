# verify-3：claude-code-beginner-event-folder

查核日 2026-10-21，第 3 輪。查核者不是撰稿者，也不是第 1、2 輪的查核者。沒有跑 git。

範圍：第 2 輪改過的 6 處事實（verify-2.md 第三節五處＋說明欄 11／7 那一句），加上 claims.md c14 的檔數（14 個）。實跑的主張逐字對 `runlog.txt` 與 `demo/`；官方頁今天重抓 `.md` 版（UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，間隔 1.2 秒），存在 `<work>/_tools/verifier3/`。web search 0／3。

官方頁（2026-10-21，頁面本身沒有更新日期）：

| 代號 | URL | HTTP |
| --- | --- | --- |
| PM | https://code.claude.com/docs/en/permission-modes.md | 200 |
| SEC | https://code.claude.com/docs/en/security.md | 200 |
| D | https://code.claude.com/docs/en/desktop.md | 200 |

## 主張表

| # | 主張 | 位置 | 依據 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 計畫裡的第一個提醒就是「要注意：最新修改時間的那份，內容其實是舊的。」，對照活動說明選了真的最終版 | dj2h、perm-plan kicker／quote | demo/pl1/reply.md：第一段是狀態說明（還沒動檔、請回覆「執行」），第二段開頭粗體「**要注意：最新修改時間的那份，內容其實是舊的。**」，卡片句子逐字相同（去掉粗體記號）；接著對照 `活動說明.md`，結論「只有**真的最終版**對得上」。plan-file.md 也是 Context 之後第一節就是同一個發現 | — | CONFIRMED | |
| 2 | 裡面混了一筆叫「測試」的資料 | f86u | demo/seed/講座籌備/報名表.csv 只有第 7 行一筆「測試」（備註「表單測試，請刪除」） | — | CONFIRMED | |
| 3 | 把介紹和六個步驟一段段用白話講完，再寫好新的一步，連順延的那一步也改好 | y9ec | demo/t1/reply.md：先解釋第 1–5 行的名片與第 7 行標題，再逐一解釋六步；給新的第 6 步一段，並把原本第 6 步改寫成第 7 步（加「以及想改線上的有幾位」）。tutor-explain 的引用句「讀現有名單，是為了知道誰已經在上面了。」逐字在第 1 步那段 | — | CONFIRMED | |
| 4 | 新手容易踩的坑：打開桌面或整個文件夾，裡面連私人的檔，它讀都不用問你；卡片「裡面的檔讀了不用問」 | snrs、folder-trap、c67 | PM 模式表 `default`｜「Reads only」（不問就能做的只有讀）；PM「Claude still runs actions that need no approval in Manual mode, such as file reads inside your working directories」（這句在 dontAsk 一節，但講的是 Manual 的規則）；SEC「asks you before its file tools read or write outside the folder where it was started」 | 200 | CONFIRMED（事實部分） | 旁白、卡片不動；claims.md c67 補註引文出處與模式表那一列 |
| 5 | Plan 列「讀檔、跑查看的指令，只提計畫，核准前不改檔」；ema8 同義 | perm-table Plan 列、ema8 | D 模式表「Claude reads files and runs commands to explore, then proposes a plan without editing your source code」；PM「Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source … edits stay blocked until you approve the plan」 | 200 | CONFIRMED | |
| 6 | 說明欄：跑了 19 次，1 次登入失敗不算；18 次裡 11 次從同一份練習資料夾重建，7 次接續 | youtube.description | runlog `## <id> … from=`：c1、c1b、c2、n1、p1、g1、s1、v1、pl1、m1、a1、a2、k1、k2、pr1、pr2、pr3、d1、t1 共 19 次（dry-1～3 是 `--dry`，沒有啟動 session）；c1 回「Failed to authenticate」；其餘 from=seed 11 次（c1b、c2、n1、p1、g1、s1、v1、pl1、m1、a1、a2），接續 7 次（k1、k2←p1，pr1、pr3、d1←s1，pr2←pr1，t1←k1） | — | CONFIRMED | |
| 7 | c14：pr1 當時資料夾 14 個檔，讀了 11 個，沒讀的是 報名表.csv、輸出/寄信名單.csv，CLAUDE.md 自動載入 | claims.md c14、kgnr、folder-reads | runlog pr1「folder before」列出 14 個檔；`Glob **/*` 之後 11 個 Read，含兩張 png；沒 Read 的正是 CLAUDE.md、報名表.csv、輸出/寄信名單.csv | — | CONFIRMED | |

## 摘要

- 這一輪查的主張：7 條（第 2 輪的 6 處修正＋c14）。
- 判定：CONFIRMED 7，CHANGED 0，NOT FOUND 0。事實修正 0 處；claims.md 只改 c67 的依據註記與進度清單。video.json 沒改。
- 快要過期的事實：官方頁沒有標日期，以 2026-10-21 抓到的為準；這一輪碰到的只有權限模式的說法（PM、D 模式表），第 2 輪列過的其他項目沿用。
- 觀點不一致：這一輪範圍內沒有新的；「新手容易踩的坑」仍是頻道的判斷，沒有統計（第 2 輪已記）。第 2 輪那 4 句「我會建議」仍待站主確認是否收進站主觀點。
- 聽眾檢查（只回報）：範圍內句子都在 40 字以內（snrs 38、y9ec 37）；沒有查證式旁白、括號、網址。
- lint：`node tools/video/cli.mjs lint --slug claude-code-beginner-event-folder` 0 errors、0 warnings，估 21.7 分鐘、220 句。
- 懷疑但沒改：
  - y9ec 的「改好」指的是它在回覆裡寫好改過的句子，不是改了 SKILL.md；下一句 ryau 之前已講「它只回答，不動任何檔」，回覆開頭也寫「我沒有改任何檔案」，聽起來可以接受。
  - dj2h 的「這件事」指畫面上的引用句；回覆第一段（還沒動檔、請你確認）也可算一種提醒，但不是警告，「第一個提醒」可以接受。
  - snrs 的「文件夾」在台灣口語可能被聽成一般資料夾，不一定是「文件」資料夾；屬用字，沒動。
  - 第 2 輪引的 PM 句子位在 dontAsk 一節，已在 c67 註明，並補上同頁模式表的 Manual 一列。
- 需要再一輪：否。這一輪事實修正 0 處（≤ 3）。
- 結論：這份稿的事實部分可以叫查核完成（三輪，所有主張都有判定、沒有懸而未決的事實）；未決的只有觀點那 4 句要不要收進站主觀點，那是站主的決定，不是事實問題。
