# S46 R9｜獨立來源與書面畫面覆核

2026-10-20 UTC。重新開啟固定的 Elizabeth Blackwell 1895 年自傳，逐句核對 R9 `script.md`、`video.json`、`claims.md` 的 120 句旁白與 P01–P14 原文，並通查 112 個 `shot` 提示、5 張資料卡、縮圖、標題、說明及 `brief.md`。本次判定為 **來源 HOLD／書面畫面 HOLD**；R8 的 PASS 不移用到此精確版本。

| 對象 | 本次 SHA-256 |
| --- | --- |
| 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `research.md` | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| `brief.md` | `a968c73c1467a508d2e49b631bcfcae7c5ff573debd21aa8b594b19eb1a66539` |
| `claims.md` | `35c2f299bb94e8394f4bf89f62af3cb29b6db25c8c2b8a092e25dd0627e77fdc` |
| `video.json` | `1a8eea0a21dbecb60786bd11d15428e4e77c641c5b8f2f9982c729de4077e4ed` |
| `script.md` | `044658dcc14548f4abd066037e0125da4bdb4c004682301f4e67e1586a53f51c` |

`video.json`、`script.md`、`claims.md` 的 120 個 ID、順序和旁白字面逐一相符，無重複 ID；`bkw060` 已從三檔刪除。所有歷史主張列均有 P01–P14 引文；頻道邀請 `bkw999c` 不需史料。`lint --slug curio-s46 --json` 回報 0 errors／0 warnings。這些形式檢查不能解除下面兩項史料與畫面問題。

## 來源 HOLD：`bkw044` 把信的日期說成抵達日期

`bkw044` 在三檔均說「信還註明，她的申請是十月三日**送到**的。」固定原書 [L2153–2159](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2153-L2159) 的院長回信日期是 1847 年 10 月 20 日，並寫 *acknowledge receipt of yours of 3rd inst.*：他收到的是 Blackwell **10 月 3 日那封信**，沒有交代信何日送達。把 `bkw044` 及相應主張改為「信還註明，她那封申請信的日期是十月三日」即可保留節點，又不虛構到達日。`bkw044` 資料卡顯示的是院長回信的 10 月 20 日日期，本身沒有這個錯誤。這是本次全句覆核發現的舊句錯誤，即使 R8 曾判 PASS，也使 R9 精確版不能判來源 PASS。

R9 新改的 `bkw069` 則符合原書界線：[L2436–2442](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2436-L2442) 只說有些學生曾以為**申請**是敵校騙局，[L2185–2204](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2185-L2204) 的決議記一致歡迎，兩處都沒有個別投票理由。`bkw068→069` 沒把猜測寫成玩笑表決。`bkw096` 的請願後一致准許住院對應 [L2534–2542](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2534-L2542)，沒有聲稱正式逐人投票；新 `bkw097` 是病房資訊能否取得的前瞻問句，後由 `bkw100–103` 對應 [L2657–2664](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2664) 回答。`bkw098` 的三樓房間對應 [L2544–2552](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2544-L2552)。其餘逐句主張未發現另一項須擋下的原文歸屬或行號缺口。

## 書面畫面 HOLD：`bkw016` 畫成學院講堂

`bkw016` 旁白正確說 Blackwell 等費城學院答覆時在**私人**解剖課學習；原書 [L1961–1969](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1961-L1969) 明說是 Dr. Allen 的 *private school*。但目前 `data.prompt` 寫 `in a 1840s college lecture room`，容易讓插圖把她在正式醫學院入學前的私人學習畫成學院課堂。將場景改為 `in a modest 1840s private anatomy classroom`，保留單人、無可讀文字且不畫人體解剖，即可對齊原文。

其餘書面提示沒有發現同等級的證據越界。尤其 `bkw068` 的資料卡只寫「懷疑的是申請」、`bkw069` 只畫單人與空白文件；`bkw096` 是單人遞交空白請願，沒有票箱、董事表決或偽造議事記錄；`bkw097` 為單人進醫院長廊、`bkw098` 為她在院內房間整理書本，都沒有預畫後續床頭卡內容。`bkw023` 仍為單人口頭面談、無提問信。縮圖只問「歡迎票？」；說明欄說明 1895 自傳轉錄與 AI 卡通示意。本判定只涵蓋**書面畫面計畫**，沒有核查生成圖片。

請作者改 `bkw044` 的 `video.json`／`claims.md` 旁白及 `bkw016` 的 `video.json` 提示，重生 `script.md`、重算受影響雜湊和 lint，再讓另一位對精確新版覆核。此報告不表示敘事盲讀、站台、音訊、生成圖片或成片通過。
