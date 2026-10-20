# S46 R12｜單句改寫的獨立來源與書面畫面差分覆核

2026-10-20 UTC。對以下**精確 R12 檔案**判 **旁白來源 PASS／書面畫面 PASS**；語音與其後媒體關卡仍 **HOLD**。本次重開固定的 1895 年 Blackwell 自傳，並以已獨立覆核的 [R11 來源／畫面基線](r11-source-independent.md)比較新版；不以作者自查或舊版核准代替這次查核。

| 檔案 | SHA-256 |
| --- | --- |
| 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `video.json` | `5bf36b2d2840523c0a0d1adf9726fe7c4fd46c47ce628ec50cf2ba46fa999cc7` |
| `script.md` | `d5e6f84c7fe1259e870472d7983c09784223cdea4c8d5337c70382126181584c` |
| `claims.md` | `530c496901febc62bc54e79046e3d7ccef8a659da10d9708f2fecacedf7d2355` |

## 來源 PASS

R12 的 `bkw044` 在三檔一致寫「**院長回信寫著，她的申請信日期是十月三日。**」固定原書 [P06 L2153–2159](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2153-L2159) 將 Charles A. Lee 的回信標在 **1847 年 10 月 20 日**，正文是 *acknowledge receipt of yours of 3rd inst.*；「3rd inst.」指 Blackwell 那封來信的日期。上下文稱她向學校提出申請，故此句把它稱為申請信有據。原文**沒有**指出信於 10 月 3 日送達，R12 亦未作此斷言。[P06 研究表](../research.md)及 [A 綱](../brief.md)仍保留這條界線。院長信與學生決議只見於 1895 年自傳的轉錄，本審核不冒稱查得獨立校方原件。

相對 R11 精確版本（`video.json` `f59ec9508ce6f5d61f867e2d2a74c74166a3bde4282b4153c9b71f07469f752b`），逐字差分僅是 `bkw044` 這句：舊句「信還註明，她那封申請信的日期是十月三日。」改為上述新句。`claims.md` 也只改該列；`script.md` 只改該句及重算的末尾 `narrative`／`speech` 版碼。其餘 119 句、P01–P14 來源連結與主張界線、`brief.md`、`research.md` 均未變，沿用 R10 全句及 R11 差分審查的已核部分。機械核對確認 `video.json`、`script.md`、`claims.md` **120／120** 句文字、ID 順序一致，且 120 個 ID 無重複。

## 書面畫面 PASS

對 R11 與 R12 的 `video.json` 移除旁白 `lines[].text` 後作結構比較，兩版完全相同：112 個 `shot` 提示、5 張資料卡、1 個片尾，共 118 景；縮圖、YouTube 標題與說明、來源連結、章節、聲音及其他設定亦未變。`bkw044` 資料卡的「**1847年10月20日**」明示院長**回信**日期，不會把來信日期或送達日混在一起。R10 已核的 `bkw016` 私人解剖學校畫面及其他書面提示保持原樣。新版旁白沒有新增畫面需表現的事實，也沒有與卡片日期衝突。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s46 --json`：**0 errors／1 warning**。唯一 warning 是既有片尾沒有口播訂閱；片尾畫面 CTA 保留。這是書面前製檢查，並非已生成畫面的驗收。

## 媒體 HOLD

[R11 語音紀錄](../verify-21.md)記載 `bkw044` 第三次音檢轉寫遇 HTTP 504，speech journal 原請求處於 `held`，沒有可用答覆。R12 的來源／書面畫面 PASS **不清除**該 journal、不證明 R11 音訊通過，也不證明 R12 已合成、轉寫或完成 120 句音檢。R11 的雙盲、政策及本地選稿均綁 R11 精確版本；新版須按其關卡重新評定。未執行付費呼叫，亦未改動任何影片內容或私有音訊檔。
