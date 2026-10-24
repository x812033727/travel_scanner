# S53 R9｜移除找地重述，作者五檔凍結

2026-10-20 UTC。[R8 隔離雙盲合併](r8-isolated-merge.md)對 R8 劇本判 **HOLD**：兩位讀者均以 `no_recap` 指出開場 `s53003` 的找地前提在 `s53041` 重述；B 另指出 `s53069`／`s53093` 再講租地或買地。R9 只修這條敘事鏈並用 CLI 重生 `script.md`。此為作者差分稿，仍須獨立來源和新稿盲評；R8 盲評檔案未改動。

## 精確五檔 SHA-256

| 檔案 | R9 SHA-256 |
| --- | --- |
| [brief.md](../brief.md) | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| [research.md](../research.md) | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| [claims.md](../claims.md) | `11f814d0f01ddeb7ec0d1a705d1f7c30b55506a512919249bf70eaae099c692f` |
| [video.json](../video.json) | `7dec1a984c326ae9c44860b14993fbe6c1d1e606368e80594968c9e2194862f1` |
| [script.md](../script.md)（CLI 重生） | `dd5a82bbe3a036210ad03a2125e049f9d370a4119dabff746fe0150ee240345e` |

## 只改的場景

- `s53003` 從找新地改成「有住戶要帶走的，是自己住的整棟小屋。」固定 [1913 年調查 R L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994) 明載住戶可按條件搬走自己的小屋；這句只預告可能的整屋遷移，不先講地塊條件或搬屋結果。原本匿名公園工作者指向一排小屋的概念插畫仍對應口播，沒有展示未獲證據支持的搬運工具。
- 刪除 `s53041` 及對應主張列。`s53039` 已報完工總數、`s53040` 已說公地期限未延長，接 `s53042` 問完工後還有多久，`s53043` 直接回答不到五個月。找地條件留給 `s53068` 提問、`s53069` 第一次說明須證明已買或租地。
- `s53093` 從再次說可買或租地，改成「有地產商向救濟部門提出，要成批買下小屋。」並將畫面改為匿名地產商在救濟辦公室櫃台提出**無字概念申請**；`s53094` 接著問部門是否答應，`s53094a` 保留原來的拒絕與理由。固定 [1913 年調查 R L4998–5011](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4998-L5011) 直接記地產商申請成批收購及部門拒絕；插畫不是保存的真實申請書或特定人物紀實。

## 作者驗證與待辦

固定 R／C 原文 SHA-256 與 [research.md](../research.md) 一致；R9 改動的口播和主張皆有上列固定原文支持。`video.json` 為 **124 景／126 句／16 個 loops**，逐 ID、順序和字串與 `claims.md` 的 126 列完全相符，`screenplay(doc)` 與 CLI 重生 `script.md` 位元組一致。卡片、其餘畫面、其餘口播及 `s53096` 的「一九〇八年六月下旬」維持 R8；`git diff --check` 通過。

`node tools/video/cli.mjs lint --slug curio-s53 --json` 為 **0 errors／1 narrative warning**。同一提醒來自 `s53082`、`s53096`、`s53101` 各說「一九〇八年」，但三句各指營地結束、部分小屋搬修結束、訪查開始，明確年份保留以防 1907／1908 混淆。`estimateTimeline` 以 250／325 CPM 預估濃縮開場 **49.93／40.53 秒**、`s53010` 至 `outro` 前正文 **594.27／484.30 秒**（最快 **8:04.30**）、全旁白 **661.27／538.53 秒**；這不是 R9 真實語音或成片時長。

另一位工作者須按以上精確 hash 覆核 R9 來源與書面畫面；兩位未讀 R9 稿的讀者須隔離完成官方十三題，按 OR 規則合併。R8 B 對 `s53062` 後接 `s53038` 的內部年序曾提出疑慮，R8 官方 OR 該項仍過；本輪只修雙人共同的 `no_recap` HOLD，沒有改變那段順序。沒有付費旁白、插圖、配樂、發布或站主核准。
