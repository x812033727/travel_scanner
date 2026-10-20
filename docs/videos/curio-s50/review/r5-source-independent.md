# S50 R5｜固定來源、企劃與書面畫面獨立差分覆核

2026-10-20 UTC。**R5 對 R4 的來源與書面畫面差分 PASS。** 這是五份精確內容檔的文字審核；不是新一輪故事盲讀、Jev 政策 PASS、站台核准、官網直接覆核或生成媒體驗收。R4 完整政策回覆的 sponsored 0.33／門檻 0.30 仍是 FAIL；R5 中性片尾只是待整稿重評的改稿假設。

| R5 檔案 | 重新計算 SHA-256 |
| --- | --- |
| `brief.md` | `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b` |
| `research.md`（R4 已獨立修正，R5 未動） | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `5e4ee9c6aacd0aab79d0f5ca5847229150dacfa451b32df0a25c55ef2eaedf64` |
| `script.md` | `009d4ed8204dcd541fc7cfb05cad73d3081ae75fb96a2f9faa71d4361b0a7ad8` |
| `video.json` | `f994e4fee7268364caf049d3fd4a69e00011b06991c77acff03919b5e21ecc67` |

我沒有參與 R5 作者改稿。以**記憶體中反轉差分、沒有改磁碟內容**驗證：`brief.md` 只把「刊本留下的城區受損數字」「測量員後來留下受損數字」各反轉一次，即得 R4 SHA `60040a61dcf7b2b4b62bba30773537d4c559104724a7f6d83926082211d983e1`；`claims.md` 只反轉 `fire999c` 的台詞和註解，即得 R4 SHA `41ebfffe54f72c0fda9f1fd563d90613efb2dbb6757e2d49a8f2e832558b4805`；`video.json` 只反轉 `fire999c` 台詞並移除新增頻道 URL，即得 R4 SHA `0fa7b40caee68e8d475827ca551d14b15eac14d7f85fec68c0497cd4f80d7a1f`。因此 `video.json` 其餘 118 句、113 張 `shot` 的提示詞、三張來源卡、縮圖、章節及結束畫面文字均為 R4 原值。`script.md` 由新版 JSON 重生，末尾還有隨稿變動的敘事／語音短碼；逐句比對如下。

## 直接來源與 R5 兩處企劃修補

固定原文字節 SHA 再算：Pepys `/tmp/new-pepys/4200.txt` 為 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`；1667 年證詞刊本 A `/tmp/curio-s50-A63385/A63385.xml` 為 `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`；Vincent `/tmp/curio-s50-A64990/A64990.xml` 為 `36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`。我重讀 A [L147–183](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L147-L183)、Farriner 答辯 [L465–480](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L465-L480)、Pepys 9 月 2 日塔樓段 [L65788–65828](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65788-L65828)、Vincent 起火街路 [L2174–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2174-L2206)。

A [L153–170](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L153-L170) 在散文中引「測量員已刊出的數字」，列城牆內燒毀 373 英畝、城外 63 英畝 3 roods、城內未燒 75 英畝 3 roods、燒毀 13,200 棟屋，並署 Jonas Moore、Ralph Gatrix。它**沒有**寫測量員何時走入街區、勘查路線或所用量具。R5 A 方案的「刊本留下的城區受損數字」與濃縮開場的「測量員後來留下受損數字」均停在刊本可證層級；`fire008` 口播也停在這一層。**兩處企劃修補 PASS。** `research.md` 已把同段未燒面積列正確，其 R4 獨立一行覆核見 [r4-research-diff-independent.md](r4-research-diff-independent.md)。

## 片尾、畫面與連結

`fire999c` 現稱「當年的日記和證詞刊本固定版連結，都放在說明欄供你核對。」`video.json.youtube.description` 確有 Pepys 的固定 Git commit 連結及 A 1667 證詞刊本的固定 Git commit 連結；Vincent 固定版、Gazette、London Museum 的既有 URL 亦保留，並只增添與 S45／S46／S48／S49／S51 同一個 `https://www.youtube.com/channel/UCR0rRWT4blMDUwEMx-TZ57Q` 頻道 URL。新句是可由描述欄履行的連結承諾，沒有增添起火原因或測量行為的史實主張。**`fire999c` 來源／連結對應 PASS。** 這不預測 Jev 會如何評整稿的業配分數。

R4 已核的書面畫面在 R5 沒變：`fire008` 高處眺望、`fire074–076` 泛稱測量員、`fire078` 望向完整街屋都只可作卡通示意；尤其 `fire075` 的「walks past burned timber house frames」**不得**標成 A 刊本證實的實測現場。`fire073` 仍是讀者翻沒有可讀字的印本，未畫量尺。實際生成圖若出現可讀假原件、精確地圖或被當成火源證據的火星，須在原尺寸退圖。`outro.data.cta` 仍寫「訂閱奇聞檔案局」，企劃仍列原創 5 秒片頭及共用 21 秒 `v4-endscreen`、最後 16 秒兩推薦框與訂閱圈；這些是書面規劃，尚非已渲染畫面或 Studio 可點擊連結。

Gazette `fire037` 與 London Museum `fire108` 仍只由倉庫 [P17 題卡](../../history-curiosity/topic-checks/P17.md) 的 2026-10-12 來源查核支持。`research.md`、`claims.md`、來源陣列及 YouTube 說明欄都明示本雲端連線代理 CONNECT 403，正式官網覆核待做；我沒有取得這兩站原頁，**不給直接官網 PASS**。`fire108` 仍用「可能」，`fire037` 仍說是「官方公報」而非國會裁決；與 R4 保守來源層級相同。

## 機械核對及適用界線

`video.json` 有 **119 個唯一旁白 ID**；`claims.md` 為 119 列且 ID／台詞／順序全同；`script.md` 的 119 句旁白按順序全同。`node tools/video/cli.mjs lint --slug curio-s50 --json` 為 **0 errors、1 warning、119 lines**；唯一警告是片尾沒有**口播**訂閱提醒，不能把仍有視覺 CTA 誤報成口播。`git diff --check` 通過。R4 預估開場 39–48 秒及正文至少約 8:40 可作前製參考，實際正文時長仍須 TTS 實測。

`brief.md` 末段「下一關」仍寫 R3 劇本／R3 修訂狀態，是**過時流程文字**，不作 R5 閘門紀錄；對外送大綱卡前應與目前 R5 精確稿及本站待審狀態對齊，更新後重綁 brief hash。R5 兩名全新隔離讀者、完整新稿 Jev 政策檢查、網站 outline/script 卡及所有媒體關卡須各自進行；R4 的敘事 PASS、政策 FAIL 與 `hand_pushed pending` 卡片不能移植為 R5 核准。本報告沒有進行付費呼叫、畫圖、配音或成片。
