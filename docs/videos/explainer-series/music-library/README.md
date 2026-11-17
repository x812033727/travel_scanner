# 奇聞檔案局與原來如此事務所的配樂庫（Flow Music，2026-11-17）

站主 2026-11-17：「用 Flow Music 幫奇聞檔案局跟原來如此規劃做一系列的全部底樂還有相關的音樂配樂音效等，
用內建瀏覽器製作，製作完傳到雲端硬碟存起來，以後要用就可以用。」

這份記錄規劃了哪些曲目、每首的提示詞、實際做出來的檔案在哪裡、怎麼接進產線。

## 工具與帳號

- 網站：<https://www.flowmusic.app>（原 ProducerAI）。在 Claude 桌面版的內建瀏覽器裡操作，
  登入帳號是站主選的 s812033727（Flow Music 名稱 `twocypress84`，方案 MEMBER）。
- 模型：Lyria 3.5（Instrument 選單裡的預設值，標示為旗艦模型）。
- 授權：第三方說明指出 Flow Music 的付費方案（Starter／Plus／Member）明列可商用，
  站方首頁寫「免費無限下載」。上架營利前仍要以站主帳號裡看到的條款為準。
- **AI 揭露**：這些都是 AI 生成的音樂。`qa/checks.mjs` 的 `disclosureDecision` 對授權檔不會勾揭露，
  但它判斷不出 `_music/` 裡的檔案是不是 AI 做的。用這套配樂的影片，上傳時要照 YouTube 的「經過修改或合成的內容」
  規則自己判斷要不要勾（見 [`../../ILLUSTRATED.md`](../../ILLUSTRATED.md) 末段關於 AI 音樂兩份文件說法不一致的註記）。

## 檔案放哪裡

| 位置 | 內容 |
|---|---|
| 雲端硬碟 `AI/備份/AI劇/奇聞檔案局/_共用/製作檔/curio-music-library/flow-music-20261117/` | 奇聞檔案局的全部曲目、短音樂、音效、`manifest.json`；跟既有的 `curio-music-library/_music/`（W01、W02 的 Lyria 底樂）放在一起 |
| 雲端硬碟 `AI/備份/AI劇/原來如此事務所/_共用/製作檔/sothatswhy-music-library/flow-music-20261117/` | 原來如此事務所的全部曲目、短音樂、音效、`manifest.json`（照奇聞的命名新開） |
| 本機暫存 `~/mokaair-work/videos/_music-library/flow-music-20261117/{curio,sothatswhy}/` | 從 Flow Music 下載後先放這裡，量過、改好檔名再複製到雲端硬碟 |

放在 `_共用/製作檔/` 是照 [`../../AI-DRAMA-DRIVE.md`](../../AI-DRAMA-DRIVE.md)：「跨集共用的（參考圖、音效、配樂庫、試鏡、腳本）放 `AI劇/<名稱>/_共用/製作檔/`」。
| 本機 `~/mokaair-work/videos/_music/` | 要用的那首複製過來；`video.json` 寫 `"music": {"track": "<檔名>", "sha256": "…"}` |
| 本機 `~/mokaair-work/videos/_sfx/<set>/` | 音效組（第 2 版 manifest，見 `ILLUSTRATED.md` §配樂與音效），用 `assemble sfx-measure` 補量測 |

檔名規則：`<系列>-<種類>-<名稱>.mp3`，系列是 `curio` 或 `sothatswhy`，種類是 `bed`（底樂，約 3 分鐘）、
`cue`（短音樂：開場、轉場、揭曉、結尾，5–30 秒）、`sfx`（音效）。符合 `MUSIC_TRACK`（小寫英數、`.-_`）。

## 混音的共同要求（寫在每一首的提示詞裡）

底樂墊在旁白下面（`gain_db` −20、`duck_db` −10，`assemble` 要求床 ≤ −24 LUFS）。所以每一首都要：
純音樂、沒有人聲、沒有搶旁白的獨奏主旋律、不要大爆點、速度穩定、結尾乾淨收住，長度約 3 分鐘。
不夠片長時照產線用 `music --loop` 的規則循環。

## 曲目清單

### 奇聞檔案局（curio）

現行設定 `CURIO_MUSIC` 的提示詞是「light, curious, a little mysterious, no vocals」，總主題延續這個方向。
九個分類各一首底樂，讓同一分類的集數有一致的聲音。

| 檔名 | 用途 | 提示詞重點 |
|---|---|---|
| `curio-bed-archive` | 總主題，任何一集都能用 | 夜裡翻舊檔案：撥弦、鋼片琴、單簧管、刷鼓、低音提琴，92 BPM D 小調 |
| `curio-bed-h-cold-case` | H 歷史懸案 | 黑色偵探：低音弦樂、時鐘滴答感、鋼琴單音、低音提琴走句，84 BPM |
| `curio-bed-s-portrait` | S 歷史人物與名場面 | 古典宮廷感但輕：大鍵琴、弦樂四重奏，96 BPM |
| `curio-bed-m-wonder` | M 奇異現象與自然 | 驚奇：木琴、豎琴、空氣感長音，88 BPM |
| `curio-bed-f-dark-fairytale` | F 童話神話與怪談原版 | 黑暗童話：音樂盒、走音鋼琴、3/4 圓舞曲，80 BPM |
| `curio-bed-l-urban-legend` | L 都市傳說與消失地名 | 詭異 lo-fi：走音鋼琴、黑膠雜音、慢鼓組，78 BPM |
| `curio-bed-g-haunting` | G 靈異與超自然公案 | 幽靈氛圍：玻璃琴、拉弓顫音，不放驚嚇音效，70 BPM |
| `curio-bed-p-prophecy` | P 預言與末日 | 不祥：低沉長音、慢心跳脈衝、遠方鐘聲，72 BPM |
| `curio-bed-u-signal` | U 外星太空與未知訊號 | 復古科幻：特雷門琴、類比合成器脈衝、無線電雜訊，90 BPM |
| `curio-bed-w-brand` | W 商業與品牌奇聞 | 輕快紀錄片：撥奏吉他、輕搖擺、木管，104 BPM |
| `curio-bed-tension` | 揭曉前的鋪陳段 | 緩慢加壓：持續低音、漸強弦樂，不爆 |
| `curio-bed-epilogue` | 結尾回顧 | 溫暖收尾：鋼琴、柔和弦樂 |
| `curio-cue-hook` | 開場鉤子後的一記 | 5–8 秒神秘重音 |
| `curio-cue-chapter` | 換章節 | 5–8 秒翻頁感短樂句 |
| `curio-cue-reveal` | 真相揭曉 | 8–10 秒明亮的揭曉和弦 |
| `curio-cue-riser` | 鉤子前加壓 | 8 秒上升音 |
| `curio-cue-outro` | 片尾 | 15–20 秒收尾主題 |
| `curio-sfx-*` | 音效 | 翻頁、蓋章、打字機、抽屜、時鐘、咻聲（Flow Music 做得出來才放） |

### 原來如此事務所（sothatswhy）

2.5 頭身 Q 版的科學解說，所長和小孩對話。方向是活潑、好奇、溫暖，比奇聞亮、比奇聞跳。
七個分類各一首。

| 檔名 | 用途 | 提示詞重點 |
|---|---|---|
| `sothatswhy-bed-office` | 總主題 | 活潑：撥弦、烏克麗麗、鐵琴、輕拍手，108 BPM C 大調 |
| `sothatswhy-bed-physics-chem` | 物理化學與日常材料 | 實驗室：冒泡感合成器、木琴，100 BPM |
| `sothatswhy-bed-biology` | 生物動物與植物 | 大自然：長笛、單簧管、輕打擊，96 BPM |
| `sothatswhy-bed-earth-space` | 地球天氣與太空 | 驚奇：柔和合成器琶音、弦樂，90 BPM |
| `sothatswhy-bed-digital` | 數位科技與通訊工程 | 輕電子：少量 8-bit 音色加真樂器，112 BPM |
| `sothatswhy-bed-kitchen` | 飲食與廚房科學 | 溫暖爵士：刷鼓、鋼琴、低音提琴，100 BPM |
| `sothatswhy-bed-body` | 人體感官與日常行為 | 逗趣：低音管、單簧管、撥弦，104 BPM |
| `sothatswhy-bed-city` | 建築交通與商業制度 | 輕快進行曲感：小鼓、銅管輕吹、鐵琴，112 BPM |
| `sothatswhy-bed-thinking` | 提問、想一想的段落 | 思考：滴答節奏、撥弦，慢一點 |
| `sothatswhy-bed-wrapup` | 總結 | 溫暖收尾 |
| `sothatswhy-cue-intro` | 開場 | 5–8 秒輕快片頭樂句 |
| `sothatswhy-cue-question` | 丟出問題 | 3–5 秒「咦？」的上揚樂句 |
| `sothatswhy-cue-aha` | 原來如此！ | 3–5 秒燈泡亮起的明亮和弦 |
| `sothatswhy-cue-oops` | 搞笑失誤 | 3–5 秒滑稽下行 |
| `sothatswhy-cue-transition` | 換段 | 3–5 秒輕快轉場 |
| `sothatswhy-cue-outro` | 片尾 | 15–20 秒收尾主題 |
| `sothatswhy-sfx-*` | 音效 | 波一聲、叮、彈簧、咻、拍手（Flow Music 做得出來才放） |

## 製作紀錄（2026-11-17 → 11-18）

**結果**：Flow Music 上 132 首（奇聞 71、原來如此 61），全部下載為 M4A（約 160 kbps、48 kHz），已複製到上面兩個雲端硬碟資料夾。
奇聞另外多 6 個 WAV，是其中 6 首早期下載的原檔（同一首歌的另一種格式，不另算曲數），所以奇聞的音檔是 77 個。
本機 sha256 與雲端硬碟逐檔比對一致（奇聞 79 檔＝77 個音檔＋`manifest.json`＋`README.md`；原來如此 63 檔＝61＋2）。

| 系列 | 底樂 M4A | 短音樂 | 音效 | 曲數合計 | 另外 |
|---|---|---|---|---|---|
| 奇聞檔案局 | 44（22 首 × 2 版） | 14 | 13 | 71 | 6 個 WAV 原檔（總主題、H、S、結尾的早期下載，與其中 6 個 M4A 是同一首） |
| 原來如此事務所 | 38（16 首 × 2 版、2 首 × 3 版） | 12 | 11 | 61 | — |

每個檔的 Flow Music 歌曲 ID、實際用的提示詞（Flow Music 改寫過的 `sound_prompt`）、長度、整合響度、峰值都在 `manifest.json`。
除了上面清單，第二波另外補了題材與情緒的底樂：奇聞的深夜檔案、調查、古文明、東亞、中古歐洲、深海、戰爭、荒謬、悲劇、氛圍底噪；
原來如此的實驗、睡前、發明、下雨、海洋、運動、節慶、輕懸疑。短音樂多了提問、反轉、片頭、悲傷（奇聞）與鼓聲、答錯、答對、噹啷、倒數、魔法（原來如此）。

**實測**

- 底樂 120–182 秒，整合響度 −19.4 到 −13.1 LUFS；組片時照 `gain_db` −20、`duck_db` −10 壓在旁白下，比片長短就照 `music --loop` 循環。
- **短音樂沒有照要求的秒數**：要 3–10 秒，Lyria 3.5 一律生成約 1 分鐘（35–67 秒）。用的時候取前段或剪出需要的部分，還沒剪。
- **音效不是單一一聲**：要 1–4 秒的單一音效，生成的是約 1 分鐘、多段聲音夾靜音（例如翻頁每隔幾秒一段）。要先試聽、
  依靜音切成單一一聲，才能做成 `_sfx/<set>/` 的第 2 版音效組。`sothatswhy-sfx-splash` 整合響度只有 −44.5 LUFS，幾乎是靜音，要試聽確認。
- 批次訊息（一則訊息要 5–8 首）每首只出一個版本，單首訊息出兩個版本；所以批次做的底樂另外補了第二版。

**做法與坑（給下次）**

- Claude 桌面版的內建瀏覽器每次下載都要站主按允許，也不能把頁面的登入憑證拿出來給 curl 用（自動模式擋），所以無人值守時改用 Claude in Chrome。
- Chrome 會擋同一個頁面接連觸發的下載（「下載多個檔案」），站主在網站設定把 flowmusic.app 的「自動下載」改成允許後才行；
  改成在頁面裡把多首打包成一個 zip 下載一次。
- Chrome 會凍結看不見的分頁：頁面上排的佇列會停。要由代理每 5 分鐘重新載入頁面並執行一次「下載新曲＋送下一批」。
- 頁面裡用 `/__api/clips/user/<id>?public_only=false` 列出帳號全部曲目（標題、長度狀態、提示詞），
  `/__api/download/audio/<clip>?format=m4a|mp3|wav` 下載，帶頁面自己的 authorization 標頭，憑證不離開頁面。WAV 約 34 MB、下載很慢（約 2 分鐘一首），M4A 約 3.5 MB、4 首並行幾秒。
- 同一個標題 Flow Music 可能生成兩首（`sothatswhy-bed-body (Take 2)`、`-invention`、`-earth-space`），照標題命名會互相蓋掉；這三組的另一首存成 `-take3`。
- 曲目在 Flow Music 上的隱私是 `unlisted`、`allow_public_use: true`（預設值），沒有改。
