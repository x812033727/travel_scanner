# S38 R8m｜`pf007` 日記譯文卡與開場停頓獨立覆核

2026-10-21 00:59 UTC。**PASS：僅限 R8m 來源、文字卡及聲畫時序的書面方案；整集原生插圖、網站音訊／分鏡審核與成片仍 HOLD。**我未撰寫這次候選、修改創作稿或私有媒體、移動 `STOP`、清帳或執行付費呼叫。

## 精確差分與稿件

實測 `video.json` SHA-256 **`980c371a793bfe3f4d2772d6d002309026a8cbd8874187ab8cd1d8fdeba82065`**，`visualHash` **`98742d01363e5597`**。目前 JSON 的兩格縮排序列化與原始位元組完全一致。我依[作者結構化差分](verify-33-r8m-structured-diff.json)將 `pf005` 的 `pause_after_ms: 1600` 刪除、`pf007` 從 `big` 及三項卡片資料還原為原 `shot`、prompt、`pan left`、`still`，整檔 SHA-256 **精確回到 R8l `2e9ec8c6f2962b420719ef62185d38def7f915bac3fac2e55fb0f16b231c6778`**，舊 `visualHash` 為 `859769ddb7cef27f`。遞迴 JSON 比對只有 pause 一葉、template 一葉、`pf007.data` 三個刪除及三個加入；其餘所有場景、ID、台詞、章節與封面資料相等。

`brief.md`、`research.md`、`claims.md`、`script.md` 的 SHA-256 依序仍為 `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。現行 `pf007` 旁白仍是「她叫醒佩皮斯。他套上睡袍，走到窗邊。」；`claims.md` 把它指向 D2a，`script.md` 同句。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json` 實測 **0 errors／0 warnings**。

## 日記、譯文與卡片

重讀固定 GITenberg `4200.txt` 本地副本，SHA-256 **`3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`**。1666 年 9 月 2 日條目的 [L65795–65801](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65801) 寫 `Jane called us up about three in the morning`，接著 `I rose and slipped on my nightgowne, and went to her window`。卡面「我穿上睡袍，走到她的窗邊」忠實譯述後半動作，保留 *her window* 的「她的」，沒有把窗說成他的；省略起身不改這段動作的意思。`佩皮斯日記・中文譯文` 明示譯文性質，`1666．09．02，佩皮斯日記` 標出日期與來源。畫面不補日記未記的燈具、衣貌或窗外日光。

正文共 **111** 景：`shot` **109**、`big` **2**，計畫插圖占比 **109／111＝98.2%**；兩張連卡只有 `pf006`、`pf007`，低於系列三張上限。`pf007` 引文是插圖不適合畫出的文字，並承接三張原生圖、兩輪修詞均判退的停點，符合此處窄卡片例外。卡面文字為 kicker 10 字、引文含引號 14 字、來源行 16 字；`pf006` 的日期／人名卡也簡短。以現行模板在本機 Chromium **只於記憶體及 `/tmp`** 渲染兩張 1920×1080 靜態預覽；`pf006`、`pf007` 的 renderer layout problems 均為空，目視引文完整分成兩行、來源可讀、未超框。這不是正式 `render` 成果或成片觀看。

## 使用既有 WAV 的實測時序

逐一讀取私有 `audio/pf001.wav` 至 `pf112.wav` 的 PCM sample 數：**112／112** 均為 48 kHz、16 bit、單聲道，且與舊 `timeline.json` 每句 `audio_samples` 完全相等。按工具的 1,600 samples／frame、每句預設 300 ms 停頓和每景末 700 ms gap，舊第一章在 frame **867＝28.90 秒**結束。`pf005` 只把該句停頓改為 1,600 ms，含原 700 ms gap 後該景從 151 增到 190 frame；新第二章始於 frame **906＝30.20 秒**，確實達 30–60 秒開場下限。`pf006` 對應 **213 frame＝7.10 秒**，`pf007` **145 frame＝4.83 秒**，各低於 15 秒單卡上限。新全片純樣本計算 **17,925 frame＝9:57.5**；品牌片頭並未算入這個開場值。`pf005` 句後實際排入 1.6 秒停頓加 0.7 秒景間空隙，開場只高於下限 0.20 秒；正式混音須耳聽這個 2.3 秒節拍，成片 QA 仍待做。

目前私有 timeline 的 `speech_hash` 仍是 **`e1a01fae129afa20`**，且舊本機 audio approval 綁該 timeline SHA；R8m 依現行詞典重算為 **`92a6e6ad374ae77e`**。原 WAV 語音字句可作這次時序計算，但現有 `timeline.json`／`narration.wav` 不是 R8m 的新停頓輸出，舊核准不能代替更新後的音訊與分鏡審核。

## 私有快取、帳本與停點

私有 `STOP` 實測存在。帳本讀值 **US$0.3300**：20 image、18 judge、1 music；其中 `pf003` **US$0.0035 reserved**、沒有已收圖，原整集硬上限仍 **US$4.58**。本輪沒有新增 image／judge。`keyframes/manifest.json` 還綁 R8l `visual_hash=859769ddb7cef27f`，`pf007` 留著舊退件檔，`judge.passed=false`、`needs_review=true`；原生 `pf007-1.jpg` SHA-256 **`7af7fd676c53591cdde88eb2745aa01b6257c77e9032ee0174c98d9f10d4e48f`**，不得在卡片版當作可用圖。`pf001/002/004/005` 的選定檔均存在、SHA 符合舊 manifest 且舊 judge `passed=true`，但 R8m 整體 `visualHash` 已變；新版 keyframes／分鏡須重新核其逐景 request key 與 judge stamp，不能只靠舊 manifest 宣稱已沿用。計畫中的其餘插圖也尚未完成。

**下一停點：**保留 `STOP`，不為 `pf007` 再購圖；以正式工具重建停頓後的時間軸與卡片幀，再檢核沿用圖、實際聲畫節奏及網站關卡。新時間軸、音訊審核、整片原生圖、片頭片尾、連結、組片與 QA 未完成前，S38 不可標為交付。
