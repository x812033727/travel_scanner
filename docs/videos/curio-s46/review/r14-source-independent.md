# S46 R14｜獨立史料與書面畫面差分覆核

2026-10-20 UTC。對 R14 作者修訂判 **旁白來源 PASS／書面畫面 PASS**。本次重新開啟固定 1895 年 Blackwell 自傳，獨立核對刪景後相接的原文、`bkw104` 新句與提示詞，並把整份新版與 Git 中已獨立審核的 R12 基線逐欄比較。此裁決只屬下表精確版本，不替代新版敘事盲讀、政策、網站、音訊或生成插畫驗收。

| 核對檔案 | SHA-256 |
| --- | --- |
| 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `video.json` | `e6db00932cd190a614de70e56abb577d1c7fe3fd7b3ffc2df0a0f123d0335577` |
| `script.md` | `d5d01d3c96327060df9e7531aba796af45bedeaa25b8124c5993de528f7a8e40` |
| `claims.md` | `3bb23f35174a424e1f6981cd70926491edb521c758b562bb9a499d19298cfbe8` |

固定原書是 [GITenberg 1895 自傳提交 `16787df4…`](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt)，而非獨立校方原件。R12 的 [獨立全稿基線](r12-source-independent.md)及 R13 的 [五句獨立差分](r13-source-independent.md)均已記錄這個證據層級；本次不把自傳中的轉錄信件升格成原件。

## R14 差分與史料

| 位置 | 獨立核對 |
| --- | --- |
| 刪 `bkw058` | 原書 [L2208–2248](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2208-L2248)確有租屋、掛友人紀念物，但其後同一封家書說首日聽五堂、解剖教授缺席。刪去租屋景不刪除必要因果：`bkw057` 問能否進課，現由 `bkw059` 接首日課堂與解剖未定。 |
| 刪 `bkw086` 及伏筆 | `bkw084` 收束 Webster 演示課；原書 [L2517–2553](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2517-L2553)說她完成第一段課程後仍欠臨床經驗。`bkw087` 已把年份、這項缺口與醫院入門問題說明白；刪除目錄式橋句不會使新增的史實失去來源。`bkw086→bkw087` 是唯一移除的 loop，其餘 18 條均指向現存、先設後答的 ID。 |
| 改 `bkw104` | 原書 [L2657–2674](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)原句是 *was soon on good terms with the nurses*；「病房的護士們卻很快和她相處融洽」忠於時間和關係描述。前句關於年輕住院醫師迴避亦出於同一段，自傳明確作兩者對照。新句刪去了舊 `bkw104` 重述的女病房准入，不新增其他權限、醫療結果或病患情節。 |

與 Git R12 基線比較，`video.json` 僅有 R13 已核的 `bkw016/027/074/076/077` 五句改字、R14 刪除 `bkw058/086`、`bkw104` 文字與**一個**提示詞改動；沒有新增場景或其他提示詞變化。`bkw104` 新提示是 1840 年代病房中**一位**護士立於空白筆記本旁的卡通示意。它不要求可讀病例、病患、多人對話或護理動作，也不假稱有原始照片。單人示意不把旁白的複數護士誤畫成只有一位護士的史實。兩個被刪景的提示詞一併消失，留存的五句 R13 旁白原樣保留。

機械獨立重算：`video.json` **116 景**（110 個 `shot`、5 張 `big` 卡、1 個片尾），**118/118** 台詞 ID 唯一；`claims.md` 118 列按 ID、順序、字面逐字相同；`screenplay(video.json)` 與 `script.md` 位元組相同，110/110 `shot` 提示非空。18 條伏筆均指向現存、先設後答的句子。`estimateTimeline` 以 325 CPM 估濃縮開場 **35.83 秒**、其後正文 **514.87 秒（8:34.87）**；這是文字估值而非 TTS 實長。`lint --slug curio-s46 --json`：**0 errors／1 個舊有片尾未口播訂閱 warning**；`git diff --check -- docs/videos/curio-s46` 通過。

**裁決：旁白史料 PASS；書面畫面 PASS。** R13 的敘事 FAIL 不因這份來源審核消失；R14 仍須兩位新讀者盲讀、同版政策與站台精確版程序。R12 全句音檢仍有五個旗標，舊 `bkw044` 的 HTTP 504 `held` 請求仍須保留，沒有對本版進行 TTS、付費插圖或成片驗收。
