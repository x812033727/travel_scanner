# A01 round13 敘事回收候選 — HOLD

這是從 [round12](../A01-round12-candidate/README.md) 衍生的**隔離離線候選**。`build.mjs` 逐一核對 round12 六章、series、source map 與 manifest 的雜湊，再依 [`delta.json`](delta.json) 只改四句旁白與三個問題／回收標記；其餘 104 句、79 鏡、series 與所有 round12 原檔維持原樣。這份檔案沒有替換正式機 A01，也不是新的審稿或影片成品。

| 敘事問題 | 此輪改法 | 來源邊界 |
| --- | --- | --- |
| 片頭問輪板為何省力，答案在畫面已可看出。 | `hook-03/6h2q` 改問輪板的辦法能否搬到行李箱；`origin` 的 loop 仍以 `origin-13/3zkh` 回收四腳輪與繩子樣品。 | [Sadow 接受 ABC News 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)記述機場輪板與試作；問題本身不聲稱把實體輪板變成箱子。 |
| 開場家庭箱子與後面館藏箱子的指代不夠清楚；下一章一開始先報來源，敘事被打斷。 | `origin-06/83ew` 明稱「開場那只」，`origin-r12-01/r12o01` 先進入 1928 年發問再交代館方引述。 | [溫尼特卡歷史學會](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)記錄 Anita 的遊記引文及館藏物件；沒有聲稱直接核對 1933 年原書。 |
| 「商店肯進貨嗎」被標在首次拒絕處回收。 | `idea` 的 `b6mn` payoff 從 `j9sw` 移到 `76ur`，該句點名試走樣品的副總裁作出進貨決定。 | [Sadow 本人訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)把首次拒絕、Jerry Levy 試走和要求採購分開敘述；不把後來的銷量說成可核數字。 |

這些是作者依獨立唯讀編輯意見做出的修稿，**四句與整片都尚待另一名審查者對精確位元組做事實、聽感和正式敘事覆核**。round9 的 `chapters_link`、`payoffs`、`one_thread` FAIL 是歷史真結果，不能因本地 lint 通過就改成 PASS。#1517 的新敘事規則已合併但尚未部署，正式機沒有重跑 panel。

## 機械預覽

`node build.mjs --write` 只在本資料夾寫六章、source map、validation 和 manifest；`--check` 逐位元組重算。首次本機產生結果：79 鏡／108 句、0 lint error／40 warnings、0 cute-story 規則錯誤。新警告包括 `origin-r12-01` 約 10.6 秒的靜圖停留；實際聲畫節奏須另審，必要時重新設計鏡頭。沒有生成插畫、音訊或 MP4。

| 文字估計字速 | round12 正文 | round13 正文 | 與 540–660 秒正文帶 |
| --- | ---: | ---: | --- |
| 250 units／分鐘 | 647.6 秒 | 650.9 秒 | 暫在帶內，距上限僅約 9 秒 |
| 300 units／分鐘 | 553.3 秒 | 556.1 秒 | 暫在帶內 |
| 320 units／分鐘 | 525.8 秒 | 528.4 秒 | 仍低於下限 |

因此**不以加空鏡、停頓或固定補稿宣稱片長合格**。實際 TTS 長度決定是否需要來源充分、可增可刪的內容。較晚的 Plath 專利可作候選材料，但必須明標 1989 年申請的設計，不能回填成 1987 年原型構造；這一輪沒有加入。

進入 A01 正式流程前仍須完成詞典來源鏈與正式機 writer 協調、實稿逐句審查、真實 verifier/listener/panel、試作預算與媒體安全關卡、TTS 量時和站主看成片。這個候選**不授權**主機寫入、腳本審稿收據、付費工作、B18／後五集或 YouTube 上傳。
