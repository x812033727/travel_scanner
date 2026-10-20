# S48｜R4 來源歧義修訂與再審交接

2026-10-20 UTC。R3 獨立審稿人回報[書面畫面 PASS、來源 HOLD](review/r3-source-independent-reported.md)；此頁是作者依回報所做的**限縮修訂與自查**，不撤銷該 HOLD，也不聲稱 R4 已獨立通過。R3 敘事雙盲仍須重新找兩名全新讀者。R2 曾通過的來源／書面畫面覆核只綁 R2 雜湊，同樣不能移作 R4 判定。

| 固定稿 | R3 SHA-256 | R4 SHA-256 |
| --- | --- | --- |
| [brief.md](brief.md) | `be0db246ddf465d5cb148d1d7643786f032e95035ba136d060b2f19eb56c03d4` | `875550d9b245012357c27a2360641f54202003a5e45bde638f19e1f5811ec8bf` |
| [research.md](research.md) | `359bac565ba26f6452b10dac75f4a6687b5280e32ff72f5da948a2065354b57d` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| [video.json](video.json) | `e9fcb7144a5b4c79438a256ae2d2775fd1cf77e0e405a038da7d63f3b77b1786` | `a2f36c1dc2c6a3b1b609ea5630a2e9cf11c9e795bf272956901d6d054bec0501` |
| [script.md](script.md) | `77f1aed38bdfef8523ea0c795f2ba9630980f887e4122cb40390d770e6f366a8` | `0794fe3217bf4aab22158135d4af4ebf834b2cfb37c845a898fad4c0873a7cc6` |
| [claims.md](claims.md) | `8e139d4ed30a15e2635cf873613853f6ff2138684bccfad88992f13ed1043cbc` | `baee71c3df9ded7d8128cf73a92855ec5743fb6f0981745ba060927672aa1183` |

兩份固定原文的本機 SHA 再核：Russell `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；Field `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。

## 對獨立 HOLD 的作者差分

| R3 問題 | R4 限縮改動與固定原文 |
| --- | --- |
| `atl100`、企劃、P16 與主張表把第二條線抵岸寫成確定的 9 月 7 日 | `atl100`、企劃 A 時序與終章、研究 P16、主張表均改為**九月初**；維持 9 月 2 日測通→接上庫存向西續鋪→暴風→抵岸。Field 引句同時寫「Saturday」及「the seventh of September」；1866-09-07 的西曆星期是 Friday，這份後出家族敘事本身矛盾。無獨立同時代資料核日時，不採精確日子：[Field F9720–9750](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9720-L9750)。 |
| `atl035/041` 把原書的 1,186 `miles` 當已確定「英里」 | 問答改成「下一次故障時，放線會跨過一千海里嗎？」→「這時放線已超過一千海里」，保留新 milestone 與回收。Russell 前段的同類放線長度明寫 716 `miles (nautical)`：[R3302–3303](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3302-L3303)；後段只寫 1,186 `miles`：[R3768–3774](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3768-L3774)。即使按較短的陸英里換算，1,186 陸英里約 1,031 海里，仍超過一千。研究 P06/P07 保留單位歧義，企劃問題與主張表同步。沒有把 1,186 標成原文已明示的海里。 |

R4 未更動其他劇情事件或視覺提示詞。歷史版 [verify-3.md](verify-3.md) 與先前審稿收據保留原貌，作為 R3 稽核軌跡；它們提到的精確日期／舊雜湊不得當作現稿依據。

## 本機驗證與待辦

`node tools/video/cli.mjs script --slug curio-s48` 重生 [script.md](script.md)；`lint --slug curio-s48 --json` 為 **0 errors／0 warnings**。JSON 有 100 個 `shot`、20 條懸念、11 章，與 [claims.md](claims.md) **103/103 句文字一致**。本機日曆算得 1866-09-07 是 Friday；1,186 陸英里換算仍超過 1,000 海里。以上只限作者自查。

`estimateTimeline` 含預設停頓，不等於 TTS 實長：

| 語速（單位／分） | 濃縮開場 | 正文（不含片頭／片尾） | 三句片尾 | 全旁白 |
| --- | ---: | ---: | ---: | ---: |
| 250 | 55.4 秒 | 10:55.1 | 15.4 秒 | 12:05.9 |
| 300 | 47.4 秒 | 9:20.2 | 13.2 秒 | 10:20.8 |
| 325 | 44.5 秒 | 8:45.4 | 12.4 秒 | 9:42.4 |

原創 5 秒片頭計畫接在濃縮後；共用 21 秒 `v4-endscreen` 計畫在正片後、末 16 秒留兩個推薦框與訂閱圈。尚未生成動畫、TTS、插畫、組片，也沒有私人上傳後可點測的 Studio 連結。本稿須另一人以此 R4 exact SHA 做**獨立來源／書面畫面差分**，再由兩名**全新**讀者盲讀官方 13 題；不聲稱站台 A 案／劇本已核准或已完成影片。
