# S61 R1｜作者交接與固定稿

2026-10-22 UTC。**作者候選，尚未獨立覆核或取得站台核准。** 題目為 1917 年哈利法克斯港首爆後的第二次爆炸警報。S01–S60 題目、題庫及任務未見同題。曾考慮 1859 年 Carrington 事件，但本環境未取得可固定核讀的同期天文與電報原始記錄，故改採這個有固定全文的題目。

## 固定來源與稿件

唯一已固定全文為 Samuel Henry Prince，*Catastrophe and Social Change*（1920），GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34` 的 `37580.txt`，raw SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。研究、行號與來源層級見 [research.md](../research.md)。本書明言其目的為災後社會研究，非完整災難史；作者參與過 1917 年救援，同時轉引其他人的描述。對海軍火藥庫灌水而避免再爆炸的因果，片中一律歸給 Prince；尚未得到獨立軍方值勤卷宗。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `de0c48e97ee3652f6a573800c692535d19a09daddfc6ffe6df4763ae2e3abf01` |
| `research.md` | `bc666f28e7c53d4e7951aa7c2031b1d5195598f7e0d730754bcc055159c3752b` |
| `video.json` | `54c44520fb12e0b5a82d8f6a1443a8e23b45d64168dc465448aed74e3e743766` |
| `script.md` | `698990fdcca3a566b5d38f34955e38dd86ee9f742195f686469f9315e1d46cff` |
| `claims.md` | `4cf21255556663e5fe0d2b05d2323edff5ad2c94291674d2158d5fb7a43d6f3c` |

`script.md` 由 `node tools/video/cli.mjs script --slug curio-s61` 生成，narrative hash `e5563c0c54de1148`。七章、107 句、14 組設問回收；104 個正文場景中有 95 個原創插圖鏡頭、9 張工具排字資訊卡（插圖比率 91.35%，最多連續一張卡）。第一章 10 句，工具估 57 秒，後接預定 5 秒頻道動畫；全段旁白工具估 10.281 分鐘。實際語音長度待 TTS 及實聽量測。

作者機械核對：107／107 句與 `claims.md` 完全相同，95／95 個 shot prompt 在逐句表中完全相同，95 個 prompt 彼此不同；每句有固定全文錨點，來源檔 SHA 相符。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json` 回傳 **0 error、0 warning**。`npm run check:tasks` 通過 2,416 件任務檔案驗證；其輸出另有既有的逾時認領與其他範圍交疊警告，沒有 S61 專屬錯誤。

## 交接與未完成的媒體關卡

- 由不同工作者逐一覆核固定來源、107 句斷言、95 張書面插圖提示與 9 張排字卡，尤其不要把 Prince 的轉引當親見，也不要把火藥庫「可能再爆」畫成真的第二次爆炸。
- 兩位獨立盲讀者按系列敘事題檢查，經正式合併／政策檢查後才送站台選案、劇本及語音核准；任何稿件修改使此 SHA 清單失效。
- 片尾預定 `v4-endscreen` 21 秒，最後 16 秒為 Studio 兩個實際推薦影片元素與訂閱元素；Short 擷取與回連需等長片可連結。此檔沒有成片、品牌動畫實體、語音、圖片、配樂、上傳或可點連結，亦未動用付費額度。
