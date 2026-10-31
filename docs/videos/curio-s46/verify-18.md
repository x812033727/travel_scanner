# S46 R9｜R8 雙盲 FAIL 後的作者窄修

2026-10-20 UTC。[R8 獨立來源與書面畫面](review/r8-source-independent.md)對 R8 精確版本 PASS；[兩位新盲讀者](review/r8-blind-merged.md)均為 11/13，均判必答 `payoffs`、`no_recap` No：`bkw060` 引出醫學書哪裡取得卻沒有回收，`bkw096→097` 相鄰重述病房許可。本檔僅記 **R9 作者差分自查**，R8 的獨立 PASS 不轉移成 R9 PASS。

## 精確 R9 候選

| 對象 | SHA-256 |
| --- | --- |
| Blackwell 1895 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| [brief.md](brief.md) | `a968c73c1467a508d2e49b631bcfcae7c5ff573debd21aa8b594b19eb1a66539` |
| [research.md](research.md) | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| [script.md](script.md) | `044658dcc14548f4abd066037e0125da4bdb4c004682301f4e67e1586a53f51c` |
| [video.json](video.json) | `1a8eea0a21dbecb60786bd11d15428e4e77c641c5b8f2f9982c729de4077e4ed` |
| [claims.md](claims.md) | `35c2f299bb94e8394f4bf89f62af3cb29b6db25c8c2b8a092e25dd0627e77fdc` |

## 差分與固定原書自查

| 修改 | 作者核對的原文與敘事作用 |
| --- | --- |
| 刪 `bkw060` 整景、旁白與主張表列。 | [P08 L2237–2248](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2237-L2248) 的信確實說她沒有書、也不知去哪裡找，但固定章節沒有給取得結果。此旁枝與「學生歡迎票能否帶她完成課堂到文憑」無必要關係；刪除後 `bkw059` 解剖教授尚未到、`bkw061` 示範員猶豫、`bkw062` 課堂如何落實的問題直接銜接 `bkw063` 教授迎接。其餘源文保留。 |
| `bkw069` 不再重述 `bkw068` 的敵校騙局，而直接說沒有個別投票理由，因此不能斷言表決動機。 | [P11 L2436–2442](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2436-L2442) 的 1895 回憶只說有些學生曾懷疑**申請**是敵校騙局；[P07 L2181–2207](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2181-L2207) 所轉錄決議只記一致歡迎，不記逐人理由。此處是來源可見範圍，不宣稱實際投票心理。 |
| `bkw097` 從「她得到住院許可；可真正進病房時，臨床資訊還拿得到嗎？」縮為「真正進病房後，臨床資訊還拿得到嗎？」；主張表同步。 | `bkw096` 已依 [P12 L2524–2542](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2524-L2542) 完整交代請願後她獲准住院；不須下一句再說一次。[P13 L2657–2669](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2669) 才記住院醫師停止填床頭卡，故 `bkw097` 保留向病房資訊的前進問題，於 `bkw102–103` 回收。原書沒有正式董事表決程序的詳細記載；仍不畫票箱或表決。 |

沒有新增原書範圍以外的旁白事實或新畫面；除刪除 `bkw060` 插圖外，其他提示詞原樣。`script --slug curio-s46` 已依 R9 JSON 重產。章節工具時碼與正文估算已同步更新於 `brief.md`，其他來源分析維持 R8。

## 形式與停手點

`lint --slug curio-s46 --json` 為 **0 errors／0 warnings**。118 景、112 張 `shot`、120/120 句與 `claims.md` 按 ID／順序／字面相符，19 組 loop。工具靜態估全旁白 **11:42**、開場約 **0:49**；正文 **2,187 漢字**按每秒 4.5 字且不計停頓估 **8:06**，不是 TTS 或成片實測。`git diff --check` 無格式錯誤。

R9 須另一位重新做來源／書面畫面差分、兩位此前未讀 S46 的讀者對同一版本完整盲讀，再處理政策與站台精確版本關卡。沒有網站大綱／劇本核准，未製作付費 TTS、插圖、配樂或成片；媒體支出 US$0。原創 5 秒片頭、21 秒動畫片尾與末約 16 秒推薦／訂閱框仍在製作規格，未組片或啟用可點連結。
