# S46 R10｜R9 獨立史料／畫面 HOLD 後的作者窄修

2026-10-20 UTC。[R9 另一位查核者](review/r9-source-independent.md)按固定 1895 年原書對 R9 精確版本判 **來源 HOLD／書面畫面 HOLD**：`bkw044` 把 Blackwell 申請信的 10 月 3 日日期誤說成送達日；`bkw016` 將 Dr. Allen 的私人解剖學校寫成醫學院講堂。其餘 120 句史料與畫面未發現另一項同級缺口。本檔是 **R10 作者自查**，尚非另一人的獨立 PASS。

## 精確 R10 候選

| 對象 | SHA-256 |
| --- | --- |
| Blackwell 1895 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| [brief.md](brief.md) | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| [research.md](research.md) | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| [script.md](script.md) | `02bdc64cce814b1962d3984f8b898b7beb7f51cf273cce7150ec8fdffdbaef8c` |
| [video.json](video.json) | `afbb36551c7fd49f0a001ed0e01e8de03d69cdc628c68cda62b08694716aaff6` |
| [claims.md](claims.md) | `f75d6a2c08e6292fb5a15398fbc5615249f037508db88b2d9a42f59958d444e2` |

## 定點差分與原書

| R10 修改 | 核對來源與限制 |
| --- | --- |
| `bkw044` 旁白／主張由「申請是十月三日送到」改為「她那封申請信的日期是十月三日」。P06 研究摘要與 A 綱一併寫明**沒有送達日**。日期資料卡維持院長回函的 1847 年 10 月 20 日。 | 固定原書 [P06 L2153–2159](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2153-L2159) 的 10 月 20 日回函寫 *acknowledge receipt of yours of 3rd inst.*；`3rd inst.` 修飾 Blackwell 那封信的日期，沒有交代到達日期。原信僅見於她 1895 年自傳轉錄。 |
| `bkw016.data.prompt` 從 `college lecture room` 改為 `modest 1840s private anatomy classroom`，仍只畫一人合上無字教科書、不畫解剖標本。A 綱同步寫 Allen 的私人解剖學校。 | 固定原書 [P02 L1961–1969](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1961-L1969) 明寫她在向費城四所學院詢問期間，於 *private school of Dr. Allen* 學習解剖。畫面只作卡通示意，不假稱在正式醫學院入學後。 |

其他旁白句、loop、來源邊界、標題與說明欄未改。`script --slug curio-s46` 已從 R10 `video.json` 重產精確劇本。

## 形式與停手點

`lint --slug curio-s46 --json` 為 **0 errors／0 warnings**。118 景、112 張 `shot`、120/120 句與 `claims.md` 按 ID／順序／字面相符，19 組 loop。工具估全旁白 **11:42**、開場約 **0:49**；正文 **2,189 漢字**按每秒 4.5 字且不計停頓估 **8:06**，不是 TTS 或成片實測。`git diff --check` 無格式錯誤。

R10 須另一人重新核對這兩項與精確版本的來源／書面畫面，再由兩位此前未讀 S46 的讀者盲讀；政策、站台與媒體關卡另計。沒有網站大綱／劇本核准，未做付費 TTS、插圖、配樂或成片；媒體支出 US$0。原創 5 秒片頭、21 秒動畫片尾與末約 16 秒推薦／訂閱框仍在規格，未組片或啟用可點連結。
