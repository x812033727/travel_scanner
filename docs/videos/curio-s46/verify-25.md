# S46 R14｜敘事雙盲失敗後的作者窄修

2026-10-20 UTC。R13 [兩名隔離讀者的正式合併結果](review/r13-official-panel-merged.json)為 **FAIL**：兩人都在 `no_toc` 指向 `bkw086`、在 `no_detour` 指向 `bkw058`；A 另在 `no_recap` 指向 `bkw104` 重講 `bkw099` 已交代的女病房許可。這份 R14 是作者候選，不是新版獨立審核或媒體核准。

| 處置 | 原因與來源界線 |
| --- | --- |
| 刪 `bkw058` 的租屋及友人紀念物景、旁白、主張列 | 1895 自傳 [P08](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2208-L2248)確有此事，但它沒有推進「表決後能否完成醫學訓練」。`bkw057` 的上課問題現在直接由 `bkw059` 的首日五堂課及缺席的解剖教授承接。 |
| 刪 `bkw086` 景、旁白、主張列與 `bkw086→087` loop | 「接下來，她還想補哪一段」像宣布下一段內容；`bkw087` 已直接按 [P12](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2517-L2553)交代 1848 年缺病房臨床經驗，並問學生入學決議能否打開醫院那扇門。 |
| `bkw104` 縮為「病房的護士們卻很快和她相處融洽。」 | 刪去與 `bkw099` 重複的女病房許可；保留 [P13](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)中與年輕住院醫師迴避形成對照的護士關係。該景提示詞改為一名穿樸素 1840 年代衣裙與圍裙的護士站在空白筆記本旁，沒有假造病例文字、另一名人物的動作或可辨病患。 |

固定原書仍是 GITenberg 1895 自傳提交 `16787df4911754c8e0401d12c896b943768f5d8d` 的 `65496-0.txt`；本地固定檔 `/tmp/curio-s48-blackwell-primary/65496-0.txt` SHA-256 `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6`。`brief.md`、`research.md` 未改。R13 因五個音檢旗標而改的 `bkw016, bkw027, bkw074, bkw076, bkw077` **逐字保留**；其餘所有存留台詞也未改。

| R14 凍結檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `video.json` | `e6db00932cd190a614de70e56abb577d1c7fe3fd7b3ffc2df0a0f123d0335577` |
| `script.md` | `d5d01d3c96327060df9e7531aba796af45bedeaa25b8124c5993de528f7a8e40` |
| `claims.md` | `3bb23f35174a424e1f6981cd70926491edb521c758b562bb9a499d19298cfbe8` |

機械檢查：對 Git R12 基線，現版僅比 R13 原有五句改字多出兩景刪除、`bkw104` 旁白與單一提示詞修改，以及一個 loop 刪除。`video.json`、`script.md`、`claims.md` 的 **118/118** 句 ID 與旁白逐字相符且無重複；**116 景**（110 插圖、5 資料卡、1 片尾）、18 loops，沒有懸空 loop。`lint --slug curio-s46 --json` 得 **0 errors／1 個 R11 起已有的片尾未口播訂閱 warning**；`git diff --check` 通過。CLI 靜態估全片旁白 **11:39**；正文 2,180 漢字以每秒 4.5 字、不計停頓估 **8:04**，不是 R14 實錄時長。

下一步：另一位工作者按固定原書覆核 `bkw104` 與書面畫面、兩名此前未讀 R14 的讀者對精確 `script.md` 重新做 13 題敘事盲讀；再取 `explainer` 政策與站台精確版關卡。R12 五個音檢旗標、R11 `bkw044` 的 HTTP 504 `held` journal 都不能當成 R14 音檢通過；不得重送那個 held 請求。通過上述關卡後，才重唸仍需新音檔的句子並對全部 118 句做官方音檢。插圖、配樂及成片尚未開始。
