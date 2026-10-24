# S46 R13｜獨立來源與書面畫面差分覆核

2026-10-20 UTC。對 [R13 作者凍結版](../verify-24.md)判定 **旁白來源 PASS／書面畫面 PASS**。這是對 R12 已獨立查核版本的五句定點差分覆核，重新開啟固定原書核對新字句；不是 R13 的盲讀、政策、網站精確版或音訊核准。

| 核對檔案 | SHA-256 |
| --- | --- |
| 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `video.json` | `fe56a4db9704cfbc0305476160209b6dd04eb4e0877e15a8ee37bbd048adba88` |
| `script.md` | `c3631099b2b2013104196ddc63d81e970356af40a74c2d3aebcdf2202b3154b7` |
| `claims.md` | `4eea6ee564a3c872a5124e63ea0425b3f2771a87548c8e198c7c12d55e7d77e2` |

R12 Git 基線恰為 [R12 獨立審核](r12-source-independent.md)所列三檔：`video.json` `5bf36b2d2840523c0a0d1adf9726fe7c4fd46c47ce628ec50cf2ba46fa999cc7`、`script.md` `d5e6f84c7fe1259e870472d7983c09784223cdea4c8d5337c70382126181584c`、`claims.md` `530c496901febc62bc54e79046e3d7ccef8a659da10d9708f2fecacedf7d2355`。逐欄比較後，`video.json` 與 `claims.md` 各只改 `bkw016, bkw027, bkw074, bkw076, bkw077` 的文字；`script.md` 只改同五句及末尾 `narrative`／`speech` 版碼。`brief.md`、`research.md` 未變。其餘 115 句及來源歸屬未變，故沿用 R12 已查部分。

## 五句來源核對

| ID | 固定 1895 年原書 | R13 判定 |
| --- | --- | --- |
| `bkw016` | [L1961–1971](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1961-L1971)：詢問費城四所醫學院期間，在 Allen 的 *private school* 開始解剖學；第一堂實作解剖是人類手腕的示範，並描述肌腱構造。 | 「等醫學院答覆」「私人學校」「第一堂實作課」「人體手腕的構造」均在此範圍，沒有把私人學校說成正式醫學院。 |
| `bkw027` | [L2000–2017](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2000-L2017)：六月二日日記記 Darrach 沉默整五分鐘，之後反覆拒絕說贊成或反對。 | 「那位教授沉默了五分鐘，最後仍不說贊成或反對」與上下句所指的六月二日教授吻合。 |
| `bkw074` | [L2361–2365](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2361-L2365)：十一月十五日她記當日一場 operation 未能在場，並說 Webster 請她避開 *some of his demonstrations*，她因此難過沮喪。 | 「缺席**部分**演示」準確保留 *some*，沒有擴成所有課或所有演示。開場 `bkw006` 的一堂演示與此處較廣的部分演示可並存；新句也明確指名 Webster 和 Blackwell。 |
| `bkw076` | [L2363–2369](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2363-L2369)、[L2397–2404](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2397-L2404)：她寫給 Webster，希望改變避席安排；日記追述她反對缺席任何講課。 | 「希望能參加往後的解剖演示」是對她所求安排的簡要轉述，沒有聲稱信的另一份原件已找到。 |
| `bkw077` | [L2397–2403](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2397-L2403)：十一月二十四日日記寫 *In this note I told him*，追述自己有認真的求學目的、解剖學是嚴肅的學問，並應 *as a student simply* 被對待。 | 「她在日記裡記下信的內容：自己認真學解剖，也希望被當成普通學生」是有據的**間接轉述**；沒有製造引號內的逐字原信，也沒有暗示另有獨立原信影像。 |

## 書面畫面與結構

移除 `video.json` 中各 `lines[].text` 後，R13 與 R12 整份 JSON 相同：**118 景**（112 個 `shot`、5 張 `big` 資料卡、1 個片尾），包括全部提示詞、卡片、縮圖、標題／說明、章節、來源連結和設定。`bkw016` 仍寫私人解剖教室且不畫人體標本；`bkw027` 的教授未作答；`bkw074` 是合起筆記；`bkw076` 是無字信；`bkw077` 只畫她重看折信、未要求可讀文字，沒有把日記或信的內容偽裝成原件，也不與新旁白衝突。這是**書面提示**審核，不是生成圖像驗收。

機械檢查：`video.json`、`script.md`、`claims.md` 的 **120／120** 句文字依場景順序逐字相符；`video.json` 與 `claims.md` 的 120 個 ID 次序一致且無重複。相對 R12 只見上述五句改字。`VIDEO_WORKDIR=/tmp/s46-r13-source-lint-workdir node tools/video/cli.mjs lint --slug curio-s46 --json` 得 **0 errors／1 warning**，唯一 warning 是 R12 已有的片尾未口播訂閱理由。此檢查沒有進行付費呼叫或改動私有 speech journal。

**媒體仍 HOLD。** R12 [完整音檢](../verify-23.md)的五個旗標不會因 R13 文字修正自動消失；R13 須另完成新版盲讀、`explainer` 政策與網站精確版關卡，再合成新句並檢查全 120 句。R11 `bkw044` 的 `held` journal 保留原狀。本報告不核准插圖、配樂、旁白或成片。
