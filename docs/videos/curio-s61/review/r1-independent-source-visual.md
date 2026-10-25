# S61 R1｜獨立史料與書面畫面覆核

2026-10-22 UTC。**HOLD：修正一個跨稿件的軍種歸屬後再重覆核。**我沒有參與 S61 作者稿，也沒有改企劃、旁白、證據表或分鏡；本輪沒有呼叫 TTS、MiniMax、配樂或成片工具。

## 固定文本與覆核範圍

我另從固定 Git commit `befb706982ba1be631a52d4f686be301c2de7f34` 下載 Samuel Henry Prince 1920 年 *Catastrophe and Social Change* 的 `37580.txt`，與作者暫存檔逐位元相同；兩份 SHA-256 都是 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。核讀 P01–P13 錨點，特別是初爆和船隻 L793–841、L843–953，第二警報與疏散 L950–979、L1363–1400，火藥庫 L1822–1835，消防及救援 L1955–1979、L2028–2069，風雪 L974–980，當晚電報 L2312–2319。

| 檔案 | 本輪 SHA-256 |
| --- | --- |
| `brief.md` | `de0c48e97ee3652f6a573800c692535d19a09daddfc6ffe6df4763ae2e3abf01` |
| `research.md` | `bc666f28e7c53d4e7951aa7c2031b1d5195598f7e0d730754bcc055159c3752b` |
| `video.json` | `54c44520fb12e0b5a82d8f6a1443a8e23b45d64168dc465448aed74e3e743766` |
| `script.md` | `698990fdcca3a566b5d38f34955e38dd86ee9f742195f686469f9315e1d46cff` |
| `claims.md` | `4cf21255556663e5fe0d2b05d2323edff5ad2c94291674d2158d5fb7a43d6f3c` |

我逐句對 107 個 `video.json` 旁白 ID、`script.md` 與 107 行 `claims.md`：字句相同、每句有固定全文錨點；95 個插圖提示詞在證據表中逐字相同且互不重複。另讀 9 張資訊卡及片尾文字。初爆、約二十分鐘間隔、第二警報、居民往 Common 疏散、警報解除、消防員留守、電報及醫療列車、帳棚與後續風雪，均可在列出的固定錨點找到；稿子正確區分第二警報和**沒有發生**的第二次爆炸，並把「灌水避免再爆」表述成 Prince 的歸因，沒有冒稱獨立軍方卷宗。

機械檢查：`curio-s61` lint **0 errors、0 warnings**；工具估正文 10.281 分鐘、107 句、七章，首章從 00:00 到 00:57（57 秒），14 組伏筆。104 個正文場景有 95 張插圖與 9 張資訊卡，插圖占 91.35%，最多連續 1 張資訊卡；`look` 只寫 `cute-mystery`，配樂規格符合系列定案。企劃安排濃縮開場後 5 秒頻道片頭、21 秒 `v4-endscreen`（最後 16 秒留 Studio 元素）及 Short 回連，但**現階段只有方案**，沒有實際片頭片尾、可點連結、旁白或圖像成品可驗收。

## HOLD：把「海軍造船廠」錯接成「海軍砲兵隊」

Prince 固定全文 L1832–1834 的原文是：

> For the flooding of the powder magazine **in the naval yard** an **entire battery** volunteered. This was why the second explosion did not actually occur.

`in the naval yard` 修飾火藥庫的位置；`entire battery` 沒交代這支砲兵單位是否屬海軍。整份固定文本沒有稱它為 naval battery 或 naval gunners。R1 卻在 `brief.md` 一句答案、`research.md` P08、`video.json`／`script.md` 的 `s61058`、`claims.md` 同句及 YouTube 說明寫成**海軍砲兵隊**。鏡頭 `s61058` 的 `naval gunner`，以及 `s61009`、`s61054`、`s61063`、`s61098`、`s61102` 的 `naval worker` 又把未證明的軍種帶到畫面。這是史實屬性錯接，不是插畫允許的無關細節。

請只把部隊稱為「一支砲兵隊／一整支砲兵隊」，火藥庫仍可明說在海軍造船廠；相關鏡頭改成不顯示軍種的砲兵志願者或工作者。不要補造命令、值勤時刻、供水機制或實際火距。重新生成 `script.md`、更新 `claims.md`、企劃、研究與說明欄，再由不同工作者對新雜湊獨立重查。書面視覺 HOLD 解除及兩位盲讀通過前，不宜把本稿送去付費旁白或原生出圖。
