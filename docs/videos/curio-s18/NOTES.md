# S18 拿破崙：寫稿紀錄

## 狀態（2026-10-19）

- 稿子：[`video.json`](video.json)（78 景：插圖 72、卡片 5、片尾 1；旁白 89 句、lint 估 8.2 分鐘）與它產生的
  [`script.md`](script.md)。`node tools/video/cli.mjs lint --slug curio-s18`：**0 錯誤**，兩個警告：
  - 「about 8.2 minutes; the target is 9-11」：正文仍超過系列要求的 8 分鐘。盲評拿掉了石棺、實驗細節等岔題，
    沒有為了湊時間加回去。
  - 「no sources」：**故意空著**。[`../history-curiosity/topic-checks/S18.md`](../history-curiosity/topic-checks/S18.md)
    34 列全部 UNOPENED。
- **還沒查核。** 這個雲端環境的網路政策擋掉 en.wikisource.org、gallica.bnf.fr、www.napoleon-series.org、archive.org、
  www.britishmuseum.org。數字、換算、漫畫的年份與作品名都是憑記憶寫的，卡片的 `source` 一律標「（待查核）」。
  最要緊的是第 2 列（驗屍報告原文）、第 3、4 列（法制與英制換算）、第 5 列（當時的平均身高）、第 19 列
  （1812 年的「常用單位」把呎改成三分之一公尺，驗屍報告用的是舊呎還是新呎，會改變換算）。
- 沒有生圖、沒有配音、沒有花錢。

## 盲評（`narrative`，13 題，2026-10-19）

每一輪都是一個新開、只讀旁白與題目的代理。第九輪 13 題全過，用 `narrative --answers` 記錄（結果在工作目錄的
`review/narrative.json`，不在 repo）。這一集輪數最多：主角是一個「數字」，原因（單位、外號、近衛軍、漫畫、心理學）
天生是平行的幾條線，讀稿代理一再判成倒敘或清單，最後是照時間排成一條線才過。

| 輪 | 結果 | 沒過的題 | 改了什麼 |
| --- | --- | --- | --- |
| 1 | 7／13 | no_spoiler、one_line、chapters_link、no_recap、chapters_are_events、no_detour | 開場不講兩國讀法差多少；第 4 章接第 5 章的牽強因果拿掉；兩個實驗縮成一句；章名改成事件；加洛迪「投票升官」與石棺 |
| 2 | 11／13 | one_line、no_recap | 第 3、4 章對調成 1796 → 1803–1821；重述的三句刪掉 |
| 3 | 8／13 | no_spoiler、one_line、no_toc、no_recap、no_detour | 「最早的線索／另一條線索」的清單感拿掉；近衛軍搬進漫畫那一章；拿掉英國醫生、六年、售價；加台灣平均身高的比較 |
| 4 | 12／13 | one_line | 1840 年的石棺移到 1821 之後；近衛軍放在 1804 年 |
| 5 | 10／13 | chapters_link、no_recap、no_detour | 第 5 章第一句改成回呼；拿掉「小被聽成矮」的因果與石棺前後的重述 |
| 6 | 10／13 | chapters_link、no_recap、no_detour | 石棺整段拿掉；補問答把 97 秒的空檔切開；加「用公尺就沒有兩種讀法」 |
| 7 | 11／13 | chapters_link、no_recap | 第 5 章第一句先接第 4 章再回呼；「168」只講一次 |
| 8 | 11／13 | chapters_link、no_recap | 第 5 章第一句改成第 4 章的結果（說英語的世界裡他就是小個子），不再宣稱漫畫導致命名 |
| 9 | **13／13** | — | — |

## 下一步

1. 在能開原文的環境逐列查 `topic-checks/S18.md`，再找另一個代理做獨立覆核；照結果改 `video.json`，
   卡片拿掉「（待查核）」，填 `sources` 與 `claims.md`。第 19 列若顯示驗屍報告用的是 1812 年的新呎（三分之一公尺），
   換算會變成約 173 公分（5 × 33.3 ＋ 2 × 2.78 ＋ 4 分），第 2 章要重寫。
2. 查核改了旁白就重跑 `lint` 與一輪新的盲評。
3. 之後照 `curio-episode` skill：旁白 → `check-audio` → 站主聽 → 插圖整集一次報價。
