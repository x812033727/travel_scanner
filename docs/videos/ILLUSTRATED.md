# 插圖投影片（illustrated slides）：讓全自動影片生動起來

2026-09-29 定案。站主看過現有的全自動投影片影片後說「太死板」，要至少像黑貓研究院（`@qiqiqushi0`：一個問題講到底的說書旁白、每 4–6 秒換一張插圖加運鏡、配樂與音效）或 Gary Chen（`@garychenai`：每 5–10 秒一個畫面物件）那樣生動，或更好。這份寫**做了什麼決定、`video.json` 多了什麼、產線多了哪幾步、雜湊怎麼綁、節奏怎麼量、要花多少錢**；操作步驟在 skill `youtube-video` 的 `references/automated.md`，頻道規格在 [`README.md`](README.md)，漫劇的零件在 [`DRAMA.md`](DRAMA.md)。

## 站主的決定（2026-09-29）

| 項目 | 決定 |
| --- | --- |
| 範圍 | 全自動投影片影片（`format: "slides"`）與 Shorts；漫劇與原來如此事務所不動 |
| 成本 | 加 AI 插圖，每支長片約 US$8–15：每 5–8 秒一張插圖加運鏡，加配樂、音效、動態卡片、轉場與更活的旁白 |
| 燒錄文字 | 不燒錄：長片的字幕只做 CC（Shorts 既有的字幕條是另一個設計決定，保留） |
| 旁白口吻 | 說書式：反常識開場、「你以為…其實…」、章節結尾留懸念、具體場景與比喻；Gemini `voice.style` 有戲、有起伏 |
| 配樂 | 站主提供授權音樂檔（YouTube 音效庫或已購授權），放 `<VIDEO_WORKDIR>/_music/`；不用 Lyria，不需 AI 揭露 |
| 音效 | 站主提供一小組授權音效檔，放 `<VIDEO_WORKDIR>/_sfx/<set>/`，工具依規則自動放 |
| 插圖核准 | 一開始就自動：judge 分數過門檻即核准分鏡，站主只看成片 |
| 第一支試片 | 新開一支：〈Jev 決策模型〉，與 Gary Chen 的參考片同題，可直接並排比較 |

做法是把漫劇路線已有的零件（靜圖運鏡、溶接、配樂床、生圖與 judge、分鏡關卡）接到投影片路線，而不是把科技解說搬去漫劇路線：投影片保有自己的教學撰稿與查核提示詞、pace QA、dubs 狀態、大綱關卡，不會繼承劇本關卡與「一律揭露」。

## `video.json` 多了什麼

| 欄位 | 意思 | 規則 |
| --- | --- | --- |
| `look` | 插圖的畫風預設 | 有 `shot` 就必須有；沒寫時工人依 slug 從五個版畫預設裡輪流挑（§第二輪：`riso-teal`／`riso-navy`／`riso-forest`／`riso-plum`／`linocut-teal`）；`tech-story`（配深色主題：深藍綠底、奶油白、琥珀與一點磚紅；2026-10-03 起寫成版畫師的工單：墨線粗細不勻、網印平塗帶紙紋與套印微偏、手剪的陰影、焦點在畫面中間三分之一而兩側有不對稱的前後景、小小的簡筆人物（點狀眼睛或背影）、霧面；negative 擋文字、logo、真人相貌、寫實、光澤、霓虹光暈、無臉人偶、鏡像對稱）；沒有 `shot` 的投影片不能帶 `look` |
| `shot` 場景 | 一張插圖：`data.prompt`（英文 ≤1000 字，依序寫景別、地點與時間、正在發生的事、視線落點的物件與材質、光從哪來；不寫風格與顏色）、`data.camera`（push in／pull out／pan left／pan right／tilt up／tilt down／drift）、`data.visual: "still"`、`data.transition?`（cut／dissolve，通常不寫） | 只准 still；不得有 `characters`、`fit`、`start_frame`、`end_frame`；shot 的句子不能 `reveal`；連續三張同一種運鏡是 lint 錯誤（§畫面不像 AI） |
| `music` | `{ track, sha256?, gain_db?, duck_db?, fade_in_ms?, fade_out_ms? }`，檔案在 `<work base>/_music/` | 任何格式都可以帶（`prompt` 走 Lyria 也還在，但站主決定用授權檔） |
| `sfx` | `{ set, gain_db?, cues?, sha256? }`，音效組在 `<work base>/_sfx/<set>/`；`cues` 是撰稿自己放的音效、`sha256` 綁音效組的 manifest（§配樂與音效） | 第 1 版音效組：`gain_db` 是整軌的音量，預設 −12 dB；第 2 版（量過的）音效組：每個 cue 各自算到目標響度，`gain_db` 是加在每個 cue 上的微調，沒寫是 0 |
| `thumbnail.data.shot`／`capture` | 縮圖的主體（`README.md` §版型）：`capture` 是一個 `screencast` 景的 id（真實的官方頁截圖，評論該產品時 logo 與介面可以入鏡，站主 2026-10-08 定），`shot` 是一張關鍵影格；`render` 先取 `capture`，沒有才取 `shot`，裁右側鋪在右 60% | 給縮圖的 shot 畫鉤子段落的具體物件、主體放右三分之一；`look` 的 negative **不變**（插圖仍不畫 logo、文字、真人），logo 與介面只從 `capture` 的真實截圖來——`channel-review-20261007/DECISIONS.md` 的「接著做」寫了改縮圖那張的 negative，本票有意沒做：AI 畫的 logo 既不準、也不是合理引用，站主要的是真的 logo，那只有截圖給得了；站主要改再開票。`keyframes` 之後 `render` 才畫得出來 |

音效組的 `manifest.json`（站主寫檔名、來源與授權，`assemble sfx-measure` 補量測；第 1 版沒有 `manifest_version` 與量測欄位，照舊能用）：

```json
{ "manifest_version": 2, "set": "studio-a", "sounds": {
  "stamp":  { "file": "stamp.wav",  "sha256": "…", "source": "YouTube 音效庫", "licence": "https://…",
              "lufs_i": -20.4, "lufs_m": -18.1, "peak_dbtp": -6.3, "seconds": 0.4 },
  "whoosh": { "file": "whoosh.wav", "sha256": "…", "source": "…", "licence": "…", "lufs_i": -24.0, "lufs_m": -22.5, "peak_dbtp": -9.0, "seconds": 1.2, "target_lufs": -20 },
  "pop":    { "file": "pop.wav",    "sha256": "…", "source": "…", "licence": "…", "lufs_i": -22.0, "lufs_m": -20.0, "peak_dbtp": -8.0, "seconds": 0.3 },
  "bell":   { "file": "bell.ogg",   "sha256": "…", "source": "…", "licence": "…", "lufs_i": -19.0, "lufs_m": -17.0, "peak_dbtp": -4.0, "seconds": 0.8 } } }
```

範例：`tools/video/core/fixtures/illustrated/video.json`（含 `brief.md`）。

## 產線多了哪幾步

`core/state.mjs` 的 `ILLUSTRATED_STEPS`：投影片的 12 步在「旁白核准」後多 `keyframes drawn`、`storyboard approved`，在「畫面渲染」後多 `music generated`（沒有 `music` 就沒有這步）。純投影片仍是 12 步。

| 步 | 指令 | 說明 |
| --- | --- | --- |
| 插圖 | `keyframes --slug` | 每個 shot 一張，伺服器的插圖模型有 2K 價時向 Gemini 要 2K（`imageSize`），否則 1K；judge 判定、最多 3 次換 seed；沒有角色所以沒有 look 關卡；伺服器宣告 `judge_checks` 時用九題是非題（§judge 的刻度與判定沿用），否則照舊打分數：rubric 在不燒錄字幕時沒有 `subtitle_band`，插圖投影片多一項 `craft`（像不像人手畫的印刷插畫）。dry-run 印尺寸、一輪與最多 N 次的成本 |
| 分鏡關卡 | `review-push --gate storyboard` | 順序 outline → audio → storyboard → final；站主決定一開始就自動核准（伺服器的 `slides_auto_approve_storyboard`，票 `2026-09-29-video-slides-media-api`） |
| 配樂 | `music --slug` | `music.track` 只核對檔案與 sha，不呼叫伺服器 |
| 合成 | `assemble --slug` | 走漫劇的混合版面：shot＝關鍵影格加運鏡（smoothstep 緩入緩出、位移量隨鏡頭長度放大到 6 秒為止、drift 依場景 id 決定左右）；**單狀態卡片**（title、chapter、big、quote、cta、outro）在 drift 與 push-in 之間輪流漂移，漂移的卡片左右輪流；多狀態卡片維持逐條出現；轉場規則＝撰稿的 `data.transition` 優先，否則第一景與章節卡硬切、前一景最後一句有 ≥600 ms 的停頓節拍才溶接、其餘硬切；配樂床側鏈壓低；音效軌 |

音效的規則（`assemble/sfx.mjs`）：章節卡開始→`stamp`（章節卡即使被撰稿設成溶接也是 stamp，不放 whoosh）；溶接前 5 格→`whoosh`；每個 reveal 狀態開始→`pop`；任兩個音效至少隔 1.5 秒，pop 每 2 秒最多一個，第 0 格不放。撰稿自己的 cue（`sfx.cues`）疊在這些 beat 上；每個 cue 的音量依音效組量過的響度算到目標，合成後再量每個 cue 聽不聽得見，被床蓋住或把旁白壓爆就不過（§配樂與音效）。

## 雜湊怎麼綁

| 檔案 | 綁什麼 | 為什麼 |
| --- | --- | --- |
| `keyframes/manifest.json` | `look_hash` ＋ `pictures_hash`（每個 shot 的 id、prompt、camera） | 改卡片文字不重畫、不重判、分鏡核准不失效；改 camera 或 prompt 只重畫、重判那一張，其他張的請求沒變，連同判定原樣沿用（§judge 的刻度與判定沿用；2026-10-04 之前是全部重判，每張 US$0.01 而且過關的會被判掉） |
| `checks.json` | `speech_hash`、`visual_hash`、`look_hash`、`pictures_hash`（`keyframesHash`：實際用的每張圖的 sha）、`mix_hash`（有配樂時）、`sfx_hash`（有音效時：set、gain、cue 表、`sfx.sha256`）、`sfx_set_hash`（再加每個音效檔的 sha 與第 2 版的目標，給讀檔的人看；§配樂與音效） | 圖重畫、配樂或音效換了，`status` 會說要重新合成，`package` 不會拿舊成片 |
| `timeline.json` | `speech_hash`（含 `voice.style`、`voice.performance`，與每句有寫的 `emotion`；§聲音表演） | 改口吻或表演計畫＝全部重錄＋旁白關卡重審；改一句的提示只重錄那一句 |

## 配樂與音效

配樂是站主放在 `<VIDEO_WORKDIR>/_music/` 的授權檔（上表的 `music`），`assemble` 把它壓在旁白下：側鏈壓低、成片 −14 LUFS、床 ≤ −24 LUFS 否則不過。這一節寫音效。2026-10-05 起音效組有第 2 版（票 `2026-10-05-sfx-library-loudness-cue-sheet`）：之前是三個固定的音效、一個 `gain_db` 蓋全部、不量檔案本身多大聲——smoke 的合成音效（峰值 −21 dBTP）壓 −12 dB 之後在成片裡約 −36 LUFS，比旁白低 20 dB 以上，根本聽不到，而 `checks.json` 說一切都好。做法借自 faceless-shorts（MIT）的形狀：量過響度的音效庫、每支影片一張 cue 表、用量測而不是用耳朵確認聽得到；只借想法，沒有抄程式。

**manifest 第 2 版**（上表的範例）：

| 欄位 | 意思 |
| --- | --- |
| `manifest_version` | 沒寫或 1：第 1 版，三個固定音效、整軌一個 `gain_db`，照舊能用，一個位元組都不用改；2：下面的量測欄位每個音效都要有，缺了 `assemble` 會說去跑 `sfx-measure` |
| `sounds.<name>` | 名字是小寫字母、數字、`_`、`-`（≤32 字）；`stamp`／`whoosh`／`pop` 仍是必要的（規則放它們），其餘隨意加，只有 cue 表叫得到 |
| `lufs_i`／`lufs_m`／`peak_dbtp` | `ebur128` 量的整合響度、最大瞬時響度（400 ms 窗）、真峰值；`sfx-measure` 寫的，不要手填；少了 `lufs_m` 就用 `lufs_i` |
| `seconds` | 檔案長度（ffprobe）；聽得見的檢查用它定每個 cue 的量測窗，第 1 版的組合成時現量 |
| `target_lufs` | 這個音效在成片（−14 LUFS 節目）裡最響的 400 ms 要落在哪；沒寫用預設 `SFX_TARGET_LUFS`：stamp −14（章節卡開頭的停頓裡，跟旁白一樣響）、whoosh −16、pop −16、其餘 −16 |

`node tools/video/cli.mjs assemble sfx-measure --set studio-a [--workdir D]`（或 `--slug S` 量那支影片的組）：每個檔案先變成軌上的樣子（48 kHz 立體聲），尾端補 1 秒靜音（250 ms 的檔不補就一個窗都量不到），過 `ebur128=peak=true`，把 `lufs_i`／`lufs_m`／`peak_dbtp`／`seconds` 與檔案現在的 sha256 寫回 manifest、版本改 2；`source`／`licence` 這些站主寫的欄位不動。最後印 manifest 的 sha256，貼到 `video.json` 的 `sfx.sha256` 就把成片綁到這一組（跟 `music.sha256` 同一個意思）：換了檔案或重量過，`sfx_hash` 跟著變，`status` 會說要重新合成，`package` 不拿舊成片。

**cue 表**（`video.json` 的 `sfx.cues[]`，最多 200 個）：

```json
"sfx": { "set": "studio-a", "sha256": "…",
  "cues": [ { "scene": "door", "sound": "bell" }, { "frame": 1230, "sound": "chime", "gain_db": -3 } ] }
```

每個 cue 寫 `scene`（那一景開始的那一格響）或 `frame`（那一格響）二選一、`sound`（組裡的名字；不在組裡 `assemble` 在碰 ffmpeg 之前就擋）、可選 `gain_db`（−40 到 +12，加在算出來的音量上）。cue 疊在規則的 beat 上：撰稿放的一定響，規則的 beat 跟某個 cue 差不到 1.5 秒就讓路；cue 之間不互相稀釋（撰稿要兩個就兩個，疊在一起的問題由聽得見的檢查抓）。`frame` 超過影片長度在合成一開始就擋，還沒編任何一段。

**每個 cue 的音量**（第 2 版）：成片最後整體線性正規化到 −14 LUFS，所以「成片裡的目標」要換成「軌上的音量」。`assemble` 先把旁白加壓低後的配樂床（沒有床就旁白本身）過一次 `ebur128`，拿到整合響度 `I_under`，`G = −14 − I_under` 就是正規化會加的量；每個 cue 的 gain＝`target_lufs − G − lufs_m ＋ cue.gain_db ＋ sfx.gain_db（微調）`，再用「`peak_dbtp ＋ gain ＋ G ≤ −3 dBTP`」封頂（封頂的 cue 在 `checks.json` 記 `capped: true`）。第 1 版的組沒有量測，維持整軌一個 `gain_db`（預設 −12），cue 自己的 `gain_db` 照加。

**聽得見的檢查**（合成後，不過就擋）：混完之後用同一個時鐘把四樣東西過 `ebur128`（每 100 ms 一行 400 ms 的瞬時響度，真峰值一起）——音效軌本身、音效下面的混音（旁白＋壓低後的床）、壓低後的床單獨一軌（用混音同一條側鏈壓縮器；沒有配樂就沒有這一樣）、整個正規化前的混音。每個 cue 的窗從它那一格到音效結束再加一個窗（0.4 秒），數字都換算成成片裡的值（加上 `G′ = −14 − loudnorm 第一遍量到的 I`）。

| 條件 | 門檻 | 不過時 |
| --- | --- | --- |
| 被床蓋住（masked） | 音效最響的窗 − 床最響的窗 ≥ 6 dB（`SFX_ABOVE_BED_DB`） | `CHECK sound effect stamp at 12.90 s (scene desk) is masked by the music bed: 4.2 dB above it, below 6; …`，`checks.ok=false`、`assemble` 回 1 |
| 把旁白壓爆（clips the voice） | 整個混音在這個窗的真峰值 ＋ G′ ≤ −1 dBTP（loudnorm 的上限；超過它 loudnorm 會悄悄從線性改成動態模式，整支旁白都被壓） | `CHECK sound effect … clips the voice: the mix would peak at 0.3 dBTP after normalization, above -1; …` |
| 量不到 | cue 的窗裡沒有任何一行 | `… was not measured` |

跟旁白的關係只記不擋（`voice_margin_db`＝音效 − 旁白＋床）：pop 的規則是落在 reveal 那一句的第一個字上，要它高過旁白 6 dB 又不壓爆峰值在物理上做不到，所以門檻只對床；要看某個 cue 有沒有被旁白蓋住，讀 `checks.json`。

`checks.json`：`sfx_hash`（`status`／`package`／`dub` 比對的那個：set、gain、cue 表、`sfx.sha256`）、`sfx_set_hash`（再加每個音效檔的 sha256 與第 2 版的目標）、`metrics.sfx = { set, version, events, sounds: {name: 次數}, cues: [{ frame, t, sound, scene, cue?, gain_db, target_lufs, capped?, effect_lufs_m, under_lufs_m, bed_lufs_m, bed_margin_db, voice_margin_db, peak_dbtp, ok }], min_bed_margin_db }`；`assemble` 的最後一行多印「7 sound effects (lowest 29 dB above the bed)」。

實測（`node tools/video/assemble/smoke.mjs --fixture illustrated`；合成音效組由 `synthetic.mjs` 寫成第 2 版，四個 250 ms 的正弦真的用 `ebur128` 量過：`lufs_m` −25.1 到 −26.0、峰值 −21.1 dBTP）：7 個 cue 全部落在目標 ±0.3 LU（stamp −14.0、whoosh −16.0、pop −16.0），床邊距 29–33 dB，混音峰值 −4.7 到 −10.9 dBTP。

沒做：Shorts 還是第 1 版的放法（`shortSfxPlan` 加整軌 `gain_db`，沒有 cue 表、沒有聽得見的檢查；它讀得了第 2 版的 manifest 但不用量測值）；`dub` 照舊重用成片的 `build/sfx.wav`，它的 timeline 只記 `sfx_hash`。

## 節奏怎麼量（`core/cadence.mjs`）

| 常數 | 值 | 意思 |
| --- | --- | --- |
| `MAX_PICTURE_SECONDS` | 8 | 一張畫面（卡片狀態或插圖）最多停多久 |
| `TARGET_AVERAGE_SECONDS` | 6 | 平均多久換一次畫面 |
| `MIN_ILLUSTRATION_SHARE` | 0.5 | 插圖至少佔多少時間，其餘是放數字的卡片 |
| `HOOK_SECONDS` | 20 | 開場章節要在幾秒內落鉤 |

lint 在估計時間軸上把這些當**警告**（撰稿不會因估計被擋；前五支證明撰稿能達標後再升成錯誤）；shot 超過 12 秒仍是錯誤（沿用漫劇的 `MAX_SHOT_SECONDS`）。最終關卡的 QA `pace` 項在合成後的真實時間軸上量：狀態超過 8 秒或插圖不到一半就不過，平均太慢只是警告。

## 揭露

`qa/checks.mjs` 的 `disclosureDecision`：漫劇一律勾；插圖投影片用風格化預設（`tech-story`、`flat-explainer`、`anime-2d`、`ink-wash`）加授權配樂→不需揭露；`cinematic-3d` 這種可能被當成真的畫風，或 Lyria 生成的配樂→勾。注意 [`SHORTS.md`](SHORTS.md) 寫「AI 音樂要揭露」而 [`DESIGN.md`](DESIGN.md) 的規則表寫「只有擬真內容要揭露」，兩份文件對 AI 音樂的說法不一致；本計畫用授權檔所以不觸發，工具採保守的一邊。

## 成本（估計，試片後改成實測）

| 項目 | 每支 10 分鐘 |
| --- | --- |
| 插圖 55–75 張 × gemini-3.1-flash-image **2K** US$0.101 ＋ judge US$0.01，平均 1.3 次 | 約 US$8–11；最壞 3 次 US$18–25 |
| 配樂 | US$0（授權檔） |
| 旁白 Gemini TTS | 不到 US$1 |
| **合計** | **約 US$9–12，最壞 US$19–26** → 投影片的單支上限 20 在最壞情況會擋到；要放寬就在設定分頁改 25 |

2026-10-03 起插圖改要 2K（1K 圖放大 1.25× 再裁切，在 1080p 看得出軟）：Flash 的 2K 是 US$0.101（1K 是 0.067，貴一半），gemini-3-pro-image 的 1K 與 2K 同價 US$0.134，所以用 Pro 畫會變 US$10–14 但不再多付；漫劇的關鍵影格仍是 1K（它們是片段的第一格）。每月圖額度 1500、judge 3000 與漫劇共用，約夠 10 支；每小時生圖 240 次、judge 360 次，一支最多 225 次，工人一小時只跑一支。

## 說書式旁白（票 `2026-09-29-video-storytelling-prompts`）

第一句是反常識的說法或觀眾的問題、20 秒內落鉤；第一章至少一個「你以為…其實…」；每章最後一句是下一章要回答的問題；每章至少一個具體場景或比喻；長短句交替；`pause_after_ms` 節拍（冷開場後 900、「其實」前 600、章末懸念後 1200）；不寫「接下來我們來看」。`voice.style` 範例：「標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，『你以為』放慢放輕，『其實』亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。」站主在 `/admin/videos` 設定分頁貼上就生效（`settle()` 抄進每支新影片）。規則的原文是 `tools/video/automation/register.mjs` 的 `REGISTER_RULES`，工具附在企劃、撰稿、聽稿三個階段的提示詞後（漫劇與原來如此事務所的提示詞不變）。已經寫好的影片用 `node tools/video/cli.mjs restyle --slug <slug>` 改口吻：聽稿模型的 `register` 變體逐句重講，數字、拉丁字詞、字典詞變了的句子退回（`rewrite.mjs`）、lint 不過就整份還原，`brief.md` 與 line id 不動（大綱核准與翻譯的 id 都還有效），改完 `verified=false`，工人下一輪重新查核、重錄、重審旁白；`--dry-run` 只量現況（幾個「你以為」、幾章以問題收尾、幾個節拍），結果寫在 `review/restyle.json`。

## 分期與票

| 期 | 票 | 狀態 |
| --- | --- | --- |
| 1 格式、lint、狀態、審核順序 | `2026-09-29-video-illustrated-slides-schema` | 做完 |
| 2 生圖與配樂階段 | `2026-09-29-video-illustrated-slides-media` | 做完 |
| 3 混合合成、音效 | `2026-09-29-video-illustrated-slides-assemble` | 做完 |
| 3b 配音音軌帶配樂 | `2026-09-29-video-dubs-carry-bed` | 已落地：`dub` 用成片同一套 `measureMixArgs`／`mixArgs`（自己的上傳格式）混配樂床，重用成片的 `build/sfx.wav`；dub 的 timeline 記 `mix_hash`／`sfx_hash`，不符就 stale |
| 4 QA、揭露、文件 | `2026-09-29-video-illustrated-slides-qa-docs` | 做完 |
| 5 伺服器開關、Flash、自動核准分鏡 | `2026-09-29-video-slides-media-api` | 已落地：設定列的 `slides` 物件（`slides_media_enabled` 預設關、`slides_image_model` 預設 gemini-3.1-flash-image、`slides_max_usd_per_video` 20、`slides_auto_approve_storyboard` 預設開、`slides_music_track`、`slides_sfx_set`；migration 0114），教學分頁的「投影片影片的插畫」區塊；`GET /api/video/media/status` 多回 `slides_enabled`、`slides_image`、`slides_max_usd_per_video`；`submit_job` 依 `VideoProject.format` 放行，投影片專案不接片段 |
| 6 工人 | `2026-09-29-video-illustrated-slides-worker` | 開著 |
| 7 說書式提示詞、`restyle` | `2026-09-29-video-storytelling-prompts` | 已落地 |
| 8 Shorts | `2026-09-29-video-shorts-motion-music` | 已落地：`tools/video/shorts/motion.mjs`（一景一段、透明字卡疊在運鏡的圖或漂移的底色上、景間溶接）、schema 2 的 `camera`／`music`／`sfx`、`from-episode` 接插圖投影片（主題 `cut:illustrated`）、頻道聲音的 style 改說書式；細節在 `SHORTS.md` §工具端 |
| 9 試片〈Jev〉 | `2026-09-29-video-pilot-jev-decision-model` | 開著 |
| 10 圖庫照片來源（伺服器端） | `2026-10-05-stock-photo-source-endpoint` | 已落地：§圖庫照片 |
| 11 照片上投影片、說明欄的圖片來源 | `2026-10-05-stock-photo-slides-and-attribution` | 已落地：§圖庫照片 的「工具端」 |

## 試片的數字表（試片後填）

| 項目 | 值 |
| --- | --- |
| 插圖張數／重做次數／judge 一次過比例 | |
| 媒體花費（US$） | |
| 從發起到成片的分鐘數 | |
| 站主審成片的分鐘數 | |
| 最長畫面／平均換畫面秒數／插圖佔比 | |
| 與 Gary Chen `2mtn-Qp59y4` 並排的觀察 | |

## 畫面不像 AI、不單調（2026-10-03）

站主看了插圖投影片的畫面後說「粗糙、單調、畫面無趣、AI 感太重，要更像真人做的」。先量了三支試片稿（`ai-term-token`、`ai-term-context-window`、`ai-term-retrieval-augmented-generation`）的分鏡：97 張裡 97 張都以「flat editorial illustration」開頭並把色盤抄進提示詞、「desk」出現在 51 張、「lamp」在 62 張裡出現 24 張、65 張沒寫景別、有一段連續三張 push in；畫風預設寫的是「flat editorial illustration with a painterly touch… anonymous figures」，所以每張圖都是同一張桌子、同一盞燈、同一個無臉人偶在青綠底上置中。單調與 AI 感是**提示詞和規則**造成的，不是模型挑錯；改了五個地方，一支影片的每一張都會不一樣，而且像印刷品：

| 層 | 改了什麼 | 在哪 |
| --- | --- | --- |
| 畫風 | `tech-story` 改成版畫師的工單：墨線粗細不勻、網印平塗帶紙紋與套印微偏、手剪陰影、焦點在畫面中間三分之一（Shorts 從 16:9 蓋滿 9:16 只留中間約 32% 寬，所以不對稱來自主體兩側的前後景，不是把主體推到一邊）、小小的簡筆人物（點狀眼睛或背影）、霧面；negative 多擋 glossy、airbrushed、smooth gradients、neon glow、lens flare、bokeh、stock vector、corporate flat icon、isometric、faceless mannequin、floating objects、mirror symmetry | `core/drama.mjs` `PRESETS["tech-story"]`（改了 `look_hash`：已有的 tech-story 影片會整支重畫，試片三支當時還沒畫） |
| 撰稿 | shot 的 prompt 照攝影師給插畫家的工單順序寫：景別 → 地點與時間 → 正在發生的事（一個人做一件具體的事，背影、側面或小小的在畫面裡，有簡單的臉，不是無臉人偶）→ 視線落點的物件與材質 → 光從哪來；不寫風格、顏色、「illustration」（look 會加）；主體在畫面中間三分之一（Shorts 只留那一條）；不畫表面是字的東西（打開的書頁、招牌、鐘面、螢幕）；camera 依畫面挑、不跟上一張一樣；transition 不寫；每章一個自己的地點與道具、同一個地點或物件不超過三分之一的 shot；比喻來自觀眾的日常（廚房、夜市、月台、工坊、教室、港口、屋頂），不用科技意象（筆電、螢幕、機器人、電路、大腦、雲、燈泡、頒獎台、沙漏、對話泡泡、發光的東西） | `automation/prompts.mjs` `TEMPLATE_GUIDE`；範例 `core/fixtures/illustrated/video.json` |
| lint | `pictureVarietyProblems`（只對插圖投影片）：連續三張同一種運鏡＝錯誤（撰稿修正迴圈會改）；沒寫景別、把 look 的字抄進 prompt、一個地點或物件出現在超過三分之一的 shot（≥6 張才算）＝每支各一條警告 | `core/drama.mjs`，經 `shotProblems` 進 lint |
| judge | 插圖投影片的關鍵影格多一項 `craft`（權重 1；由影片決定，不看鏡頭有沒有角色，所以 3D 漫劇的空鏡與畫風允許無臉人物的原來如此事務所都不評）：像不像人手為印刷畫的——有紋理與小瑕疵的線與色、不對稱的構圖與一個焦點、有層次、人物有簡單的臉或背對、沒有光澤／光暈／電腦算圖的表面 | `media/keyframes.mjs` `keyframeRubric` |
| 運鏡與剪接 | 運鏡 smoothstep 緩入緩出、位移量隨鏡頭長度放大（6 秒以上滿額、短鏡頭至少一半，速度大致一致）、drift 依場景 id 決定往左或往右、漂移的卡片左右輪流；轉場改成剪接師的習慣：預設硬切，前一景最後一句有 ≥600 ms 的停頓節拍（說書口吻的節拍：冷開場後 900、「其實」前 600）才溶接，章節卡硬切，撰稿的 `transition` 優先。Shorts 仍用線性運鏡（`shorts/motion.mjs` 另一張票的範圍） | `assemble/drama.mjs`（`MOTION_ENCODER_VERSION` v3，舊的運鏡段會重編） |
| 尺寸 | 插圖投影片與原來如此事務所的關鍵影格向 Gemini 要 2K（`ImageJobIn.size`，伺服器放進 `resolution`，Gemini adapter 送 `imageConfig.imageSize`）；只有目錄裡有 `usd_per_image_2k` 的模型才能要（Pro 同價、Flash US$0.101、MiniMax 沒有 → 422）；`GET /api/video/media/status` 的 `image`／`slides_image` 多回 `usd_per_image_2k`，工具據此決定尺寸與估價；作品（`series.json` 的 `image_model`）另指定模型時一律畫 1K、照 1K 估價，因為那個 2K 價是設定裡那個模型的 | `media/stages.mjs` `imageSizeFor`、`apps/api/app/video_media/{schemas,jobs,catalog,meter}.py`、`providers/gemini_images.py` |

要驗的事：試片的第一張 2K 圖（確認 `imageSize` 被 Gemini 接受、檔案約 2048×1152）、judge 的 `craft` 分數分布（太嚴就把權重留 1 但把門檻 `judge_min_score` 看一眼）、以及與第 1 版畫面的並排比較，寫回上面的數字表。

已上線：2026-10-03 04:31Z 隨 `90c52e19e` 部署。API 映像的目錄有 2K 價（Pro 0.134、Flash 0.101、MiniMax 沒有），影片工人的工具讀到 `image` 與 `slides_image` 兩個選擇的 `usd_per_image_2k`。當時正式站的「替投影片影片畫插圖」開關讀起來是關的（`slides_enabled: false`）：在它打開之前，投影片的圖走漫劇的開關與模型（Pro，2K 與 1K 同價），工具的預估卻用 Flash 的 2K 價，帳本記的是伺服器實收（票 `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`）。

## 第二輪：版畫輪替、畫風樣張、審圖與光線（2026-10-03）

同一天站主再說「AI 感太嚴重，影片與投影片的插畫都要更好」。正式站從早上部署到這時沒畫過任何一張插圖投影片的圖（工人說自動草稿關著、每支都在等站主；七支插圖投影片在開關打開前就卡在「插畫沒開」，要站主按重試），所以這一輪先用本機工具經正式站真的畫了樣張再改：第 1 版畫風（`tech-story`，Flash 2K）六張、四種版畫候選各四張、再用其中一張當參考圖畫三張（`mokaair-work/videos/_audition/look-20261003/`，約 US$3）。看到的事：

- `tech-story` 的「墨線加平塗」被模型畫成**童書式的乾淨數位漫畫**：每樣東西都描一圈均勻的線、同一款可愛的臉、一樣的構圖——這就是觀眾讀成 AI 的東西。真正會讀成「人印的」是**版畫的物理痕跡**：網點、套印、油墨沒蓋滿、刻刀的毛邊。四種候選裡 risograph（網點、兩色套印）與 linocut（刻版）最像印刷品；gouache 像 AI 概念畫；pen-and-watercolour 最像人畫，但模型把它畫成**攤開的筆記本**（有頁邊、連價格牌的字都寫上去）。
- 寫「full-bleed, edge to edge」會讓模型**畫出紙邊**（印刷品有留白）；judge 的 `clean` 也抓到一張直式圖兩側補模糊條。所以畫風改寫成「畫面延伸出畫框四邊」、negative 擋 paper border／white margin／pillarbox／blurred side bars。寫「no ink outlines」模型照樣描線，只是 judge 扣 style 分，刪掉。
- 把一張畫好的圖當 `role: "style"` 的參考圖，其餘三張的網點、油墨、人物畫法**完全一致**，而且沒抄場景——這就是同一位插畫家畫一整支的辦法。

改了四層：

| 層 | 改了什麼 | 在哪 |
| --- | --- | --- |
| 畫風輪替 | 五個版畫預設：`riso-teal`（深青綠＋螢光珊瑚橘）、`riso-navy`（墨藍＋芥末黃）、`riso-forest`（深森林綠＋橘）、`riso-plum`（深李紫＋金赭）四組雙色 risograph，與 `linocut-teal`（青黑主版＋赭＋磚紅）。沒寫 `look` 的投影片影片由**slug 決定**用哪一個（`slidesPresetFor`：同一支永遠同一個，因為 look 在 `look_hash` 裡；不同支輪流，所以每支是自己的一刷），撰稿只在題材需要時點名；`tech-story` 保留給點名的影片。預設負面詞 ≤400 字可以抄進 `video.json` | `core/drama.mjs` `SLIDES_PRESETS`、`slidesPresetFor`；`automation/flow.mjs` `settle()` |
| 畫風樣張 | `keyframes` 對插圖投影片**先畫一張樣張**（`STYLE_PLATE_PROMPT`：小鎮街角、下午、兩個人、一隻貓、磚與玻璃與雨後的路；judge 同一套 rubric、最多 3 個 seed、沒過也取最高分），存 `keyframes/plate.json`（綁 `look_hash`，所以改一張 prompt 只重畫那一張、換 look 才重畫樣張與全部）、記進 `keyframes/manifest.json` 的 `plate`；之後每張 shot 都帶它當 `role: "style"` 的參考圖（放在參考圖最後），judge 也拿到它（標籤 `style plate`）並以「同一隻手、同一張紙」評 `style`。站主自己給 `look.style_frames` 時不畫樣張。多一張圖的錢（約 US$0.11–0.41）。伺服器端 Gemini adapter 對 `style` 參考圖改說「最後一張是畫風樣張：用它的技法、線、色、紋理與完成度畫，不取它的場景」，不再對所有參考圖說「保持角色一致」 | `media/keyframes.mjs` `stylePlate`、`readStylePlate`；`apps/api/app/video_media/providers/gemini_images.py` |
| 審圖 | `craft` 改問「是不是人為印刷做的而不是生成的：媒材的痕跡與小瑕疵、沒有把每樣東西描一圈均勻的線、不是到處都一樣細的細節、不對稱構圖一個焦點、簡單的臉或背影、沒有光澤／噴槍／光暈／算圖的完成度」；`clean` 多問「一張圖填滿整個畫框，沒有邊條、邊框、留白或模糊側條」。rubric 每題 ≤400 字（伺服器上限） | `media/keyframes.mjs` `keyframeRubric` |
| 撰稿與 lint | 撰稿：一支影片活在一整天裡，夜景與燈下的圖最多一半；每章至少一張兩三個人互相做事（討價還價、交東西、排隊、教、吵）、一張手裡拿著東西的特寫、偶爾一個小笑點（不該在那裡的貓、唯一一個面向錯邊的人）；`look` 不寫、交給工人。lint：夜景／燈下超過一半＝每支一條警告（≥6 張才算）；景別只在句首或接 shot／view／angle／of 時算景別（「a medium bowl」不算），接受 low-angle、bird's eye、top down、over-the-shoulder 的寫法；「cream」在冰淇淋、鮮奶油、咖啡裡不算色盤，risograph／linocut／gouache／halftone 算抄畫風；複數折成單數（ferries／shelves／boxes／potatoes；shoes 與 series 不動）；連三張同運鏡的錯誤指向真正帶運鏡的欄位（`camera` 或 `motion`） | `automation/prompts.mjs` `TEMPLATE_GUIDE`；`core/drama.mjs` `pictureVarietyProblems`、`SHOT_SIZE`、`LOOK_WORDS`、`DARK_LIGHT`、`motifOf` |

第五層是**裁邊**（`media/trim.mjs`）：寫了負面詞模型還是常把紙邊畫出來（樣張五張有四張），運鏡時紙邊會跟著畫面跑。`keyframes` 對填滿畫框的靜圖（插圖投影片、原來如此事務所、樣張）在 judge 之後用 ffmpeg 讀一張 512×288 的灰階縮圖，從四邊往內走到不再平坦（標準差 >10 或色調差 >8），任一邊超過 0.6% 就取邊內最大的 16:9 框裁掉再放大回原尺寸，存成 `<id>-<seed>-trim.png`；manifest、樣張參考圖與後面的合成都用裁過的檔，judge 看的是原圖（`takes[].margins` 記每邊的百分比）。沒有 ffmpeg 或讀不了的圖就照原樣用。

另外修了票 `2026-10-03-illustrated-slides-lint-heuristics-the-shorts` 的急件：`choiceFor` 只在 `slides_enabled` 時用投影片的模型，開關關著時跟伺服器一樣用漫劇的模型估尺寸與價錢（之前第一張圖就以 `video_media_model_changed` 失敗）。範例的 `race` 兩個跑者改在中間三分之一、`podium` 與 `race` 改成白天；`shorts/motion.mjs` 與 `SHORTS.md` 的 56% 改成 32%。

要驗的事：第一支部署後的插圖投影片在 `keyframes/plate.json` 看樣張與分數、聯絡表上每張圖的網點與油墨是不是同一刷；judge 的 `craft` 分布（樣張時 craft 約 6.5–7，門檻 7，三個 seed 內多半會過一張——實測不成立，見 §judge 的刻度與判定沿用）；七支卡在「插畫沒開」的影片站主按重試後是否畫出來、單支花費（多一張樣張）。

## judge 的刻度與判定沿用（2026-10-04）

第一支真的畫完的插圖投影片（`openai-devday-2026-recap`，74 張、`riso-navy`、Flash 2K）量到 judge 的分數**頂在門檻上**，上一節「三個 seed 內多半會過一張」不成立：

| 163 次出圖（74 張 shot） | 值 |
| --- | --- |
| overall | 最高 7.04、平均 6.74、中位數 6.79、最低 5.54 |
| 過關（`judge_min_score` 7） | 43 次（26%），全部落在 7.00–7.04；沒過的擠在 6.4–6.99 |
| 815 個單項分數 | 471 個剛好是 7、109 個 6.8、41 個 7.2；最高 7.5，8 以上 0 個 |
| 過關卻列了毛病 | 43 次裡 24 次；沒過卻沒列毛病 1 次 |
| 沒過的 31 張留的是哪一張 | 23 張留的不是該張分數最高的那次（工具留最後一張） |
| 花費 | 176 張圖 US$20.27 過 43／74 張（單支上限 25）|

也就是 judge 把「挑不出毛病」打成 7、從不往上，門檻 7 等於「一句意見都不能有」，某一項掉 0.2 就不過。同一張圖再問一次會在 6.9 與 7.0 之間跳：改一張的提示詞讓 74 張已畫好的圖全部重判，5 張原本過的被判掉、3 張原本沒過的過了。兩位看圖的編輯在 18 張沒過的 shot 裡每一張都找到可用的版本。漫劇的設定圖與片段判定也一樣頂在 7（試拍的設定圖 7／7、片段 6.72），所以這是 judge 的刻度問題，不是插圖 rubric 的問題。站主決定門檻數字不動（2026-10-04），所以改的是 judge 怎麼問、工具怎麼用判定。

### 工具端的三件事

| 事 | 之前 | 現在 | 在哪 |
| --- | --- | --- | --- |
| 沒過的 shot 留哪一張 | 最後一張 | 分數最高的那一張（同分取較早的 seed），聯絡表與改提示詞的人看到的是最好的版本；樣張原本就這樣 | `media/keyframes.mjs` `bestTake` |
| 改了別張的提示詞或運鏡 | `pictures_hash` 一變就清空 manifest，每張已畫的圖都再問 judge 一次 | 只有綁定變了（look、生圖模型都沒變）時，逐張比對：每次出圖的快取鍵（提示詞、運鏡、畫風、參考圖、模型、尺寸、seed）與現在會送的相同、判定問的題目（rubric、context、站主門檻的雜湊，記在 `takes[].judged`）也相同，就整筆沿用，沒過的也沿用（同一張圖不問第二次）；沒有 `judged` 的舊判定只在該 shot 已過關時沿用；`--force` 照舊全部重問。漫劇的 `visual_hash` 走同一條規則，另外比對 end frame 的鍵 | `media/keyframes.mjs` `entryStands`、`media/stages.mjs` `imageKey` |
| 單次呼叫的 `min_score` | 可以把這一次的門檻設得比站主的低（沒有工具這樣送） | 只能更高，較低的值被忽略：站主的設定是下限 | `apps/api/app/video_media/admin_api.py` |

### 刻度：用文字定義沒有用，改成是非題

先試「告訴 judge 每個數字是什麼意思」（10＝這一項挑不出毛病、7–8＝可用、0–3＝必須重畫），再試換一種回答的形式，都拿同樣 28 張已記錄的圖重判（模型 gemini-3.8-flash；前兩種經正式站的 judge，其餘經站主同意在正式站 API 容器裡用唯讀腳本換掉系統指示與回答格式，每次照樣計入本月 judge 次數）：

| 問法 | 乾淨的圖得到什麼 | overall 最高 | 過關 | 編輯判可用的 9 張過幾張 | 編輯判該退的 12 張過幾張 |
| --- | --- | --- | --- | --- | --- |
| 當時的判定 | 每項 7 | 7.04 | 9 | 1 | 1 |
| 刻度放請求的 `context` | 每項 7 | 7.04 | 11 | 5 | 2 |
| 「每項從 10 起算」＋每題加註「10 = no fault found.」 | 每項 7 | 7.14 | 10 | 2 | 2 |
| 刻度寫進系統指示（取代「Be strict」那一句） | 每項 7 | 7.17 | 12 | 5 | 1 |
| 每項給等級 none／minor／noticeable／serious | 每項 minor（140 個等級裡 none 0 個、serious 0 個；四隻手臂也只給 noticeable） | — | 25 | 9 | 9 |
| 每項給「扣幾分」 | 每項扣 2–3 分（每張都被編一個小毛病） | 7.86 | 14 | 5 | 2 |
| **每題問一個具體瑕疵「有沒有」** | **沒有任何一題答有** | **10** | **20** | **8** | **5** |

不管要它給分數、等級還是扣分，這個模型都縮在中間的預設值，文字怎麼定義都拉不動兩端；只有低分端對明寫的數字聽話（可讀文字、四隻手臂落到 3）。問「有沒有可讀的字」「有沒有哪隻手超過五指」這種是非題，它才肯表態：乾淨的圖一題都不答有，瑕疵點名點得具體。所以做法是**模型只回答是非，分數由伺服器算**（延續 `verdict()`「overall 由程式重算」）：

- 伺服器：`JudgeCriterion` 多一個 `cost`。rubric 的每一題都帶 `cost` 時，這次呼叫改用 `CHECK_INSTRUCTIONS`、回答是每題一個布林值，該項分數＝沒有瑕疵 10、有瑕疵 10 − `cost`；沒回答或不是 `false` 一律算有瑕疵。overall 仍是加權平均，過關規則不變（overall ≥ 站主門檻、每項 ≥ 4）。不帶 `cost` 的 rubric 和以前逐字相同，漫劇的設定圖、關鍵影格、片段都不受影響。`GET /api/video/media/status` 的 `limits.judge_checks` 告訴工具伺服器會這樣問（`apps/api/app/video_media/judge.py`、`schemas.py`）。
- 工具：插圖投影片在伺服器宣告 `judge_checks` 時改送 `keyframeChecks`（`media/keyframes.mjs`），九題：

| 題 | 問什麼 | 權重／`cost` | 有的話 |
| --- | --- | --- | --- |
| `text` | 讀得出任何字母、單字、數字，或有 logo、浮水印（只像字的塗鴉不算） | 0.25／10 | 該項 0 分，低於每項下限 4：這張一定重畫 |
| `anatomy` | 哪隻畫得夠大的手超過五指，或多出手、臂、腿，臉或身體變形（被遮住或被畫風省略的手指不算） | 0.25／10 | 同上 |
| `detached` | 有東西漂浮、與該連著的地方斷開、重複，或有不屬於場景的小人或物件 | 0.25／10 | 同上 |
| `subject` | 提示詞的主體或它在做的事不見了或明顯不對（次要道具、路人、哪隻手、景別不算） | 0.25／10 | 同上 |
| `frame` | 沒有以一張正的圖填滿畫框：兩側有邊條或模糊條、畫面歪斜、角落露出紙或桌面、被畫成一張印刷品的照片（細的素色邊不算，工具會裁） | 0.25／10 | 同上 |
| `style` | 技法明顯不是樣張那一種（沒有樣張時對照 look 的描述） | 0.25／10 | 同上 |
| `details` | 提示詞要的次要東西少了或不一樣（道具、路人、手勢、景別） | 2／3 | 該項 7 分，只拉低 overall |
| `awkward` | 手、臉或身體彆扭到觀眾第二眼會注意到 | 3／6 | 該項 4 分，只拉低 overall |
| `generated` | 看起來是生成的而不是手印的（每樣東西描一圈均勻的線、到處一樣細、光澤或噴槍感） | 2／6 | 該項 4 分，只拉低 overall |

於是站主的門檻有了可以說出口的意思（overall：全無 10、只有 `details` 9.29、只有 `generated` 8.59、只有 `awkward` 7.88、`awkward`＋`details` 7.18、`awkward`＋`generated` 6.47）：

| `judge_min_score` | 過關的條件 |
| --- | --- |
| 7（現在的設定） | 沒有任何必須重畫的瑕疵；第二眼的毛病可以有一種（外加次要細節不符），但不能同時「彆扭」又「像生成的」 |
| 8 | 再加上：不能有「彆扭」 |
| 9 | 再加上：不能「像生成的」；只容許次要細節不符 |
| 10 | 九題全部答沒有（最接近以前門檻 7 實際要求的「一句意見都沒有」） |

題目是量過的那一版，逐字相同；改任何一題的字都要重量。必須重畫的六題權重刻意很小：它們靠每項下限起作用，權重只是讓這種圖的 overall 不要掉得比「彆扭」還多，沒過的 shot 之間仍能比出哪一張比較好。

### 前後對照（同樣 163 次出圖、門檻 7 不動）

| | 之前（打分數） | 之後（是非題） |
| --- | --- | --- |
| overall | 最高 7.04、平均 6.74、最低 5.54 | 最高 10、中位數 10、平均 9.59、最低 6.88；96 張 10 分、41 張 9.29 |
| 過關的出圖 | 43（26%） | 145（89%） |
| 有過關版本的 shot | 43／74 | 73／74（沒有的那一張三個版本都畫出可讀的「TICKET」） |
| 原本過關的 43 張 | — | 43 張都過 |
| 原本沒過的 120 張 | — | 102 張過；18 張不過，每一張都點得出具體瑕疵：可讀文字 6、漂浮／多出來的東西 7、畫成印刷品照片或露出紙邊 3、多一隻手臂或六指 2 |
| 編輯判可用的 9 張 | 過 1 | 過 9 |
| 編輯判該退的 12 張 | 過 1（六指那張） | 過 4：六指的 `kickboards-3`（judge 沒看出來）、器物上有像「POD」的記號的 `pottery-wide-1`、窯門畫成大開的 `kiln-door-1`、一隻手端盤的 `bell-tray-2`（後三張只被判成次要細節不符） |
| 第一個 seed 就過 | 24／74 | 67／74 |
| 照 seed 順序重演這一輪 | 畫 163 張過 43 張 shot | 畫 83 張過 73 張 shot |
| 門檻改成 8／9／10 | — | 137／137／96 張過（84%／84%／59%） |

同一張圖問兩次（103 張，各判兩次）：過關與否不同的 4 張（3.9%），九題全部答得一樣的 85 張。各題答得不一樣的張數：`awkward` 12、`details` 7、`anatomy` 3、`detached` 2、`frame` 1、`text` 0、其餘 0。會翻的是「彆扭」這種判斷題，它在門檻 7 單獨不決定過關；「有沒有字」從不翻。舊問法沒有這種乾淨的對照，但同一輪重判 74 張 shot 就翻了 8 張。

這是放寬還是收緊：以前的門檻 7 實際要求「judge 一句意見都沒有」，而且它會編意見、同一張圖還會變；現在的 7 是「沒有必須重畫的瑕疵」。要回到「一句意見都沒有」的嚴格度是門檻 10（59% 的出圖、60／74 張 shot），而且那 59% 是穩定的。**judge 看不出來的瑕疵仍然會過**（六指那張兩種問法都過），所以它擋的是看得出來的錯，不是保證每張都好；細的毛病還是靠撰稿照「會過的寫法」寫、靠成片關卡的人看。

花費：共 462 次判定、US$4.62（站主同意的上限 US$5）。量測工具與每一輪的原始回答在本機的 `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration/`（`rejudge.mjs` 經站上重判；`host-build.mjs`＋`host-judge.py` 產生在 API 容器裡跑的唯讀腳本；`checks-report.mjs` 印前後對照；`labels.json` 是編輯判過可用與該退的圖；`host/fa.out` 是全量兩輪的回答）。163 張圖有 58 張本機檔已被後來的重畫蓋掉，只在站上的媒體庫（保留 14 天），要重量得在 2026-10-17 前。

## 成片大小（2026-10-04 實測，票 `2026-10-04-illustrated-slides-finals-fit-the-review`）

第一支在本機做完的網點版畫插圖投影片 `openai-devday-2026-recap`（`riso-navy`、74 張插圖、107 景、13:22）成片是 **895 MB**（67 MB／分鐘、平均 8.9 Mbit/s），`review-push --gate publish` 被站台擋下（413 `video_review_file_too_large`，當時單檔上限 400 MB）。`HANDS-OFF.md` 寫的「成片約 90–100 MB」是純投影片的數字。

**位元組在哪裡**（CRF 18，各段的檔案大小）：

| 段 | 段數 | 時長 | 大小 | 平均位元率 |
| --- | --- | --- | --- | --- |
| 插圖加運鏡（`motion`） | 74 | 422 秒（53%） | 804 MB（90%） | 15.3 Mbit/s，最低 6.6、最高 24.4 |
| 會漂移的單狀態卡片（也是 `motion`） | 11 | 60 秒 | 18 MB | 2.4 Mbit/s |
| 多狀態卡片（`stills`，`-tune stillimage`） | 22 | 321 秒 | 41 MB | 1.0 Mbit/s |
| 聲音（AAC 384 kbps） | | 802 秒 | 33 MB | |

網點與紙紋每一格都被 `zoompan` 重新取樣，CRF 18 照單全收：push-in 平均 19.4、pull-out 18.9、drift 17.5–18.8、pan 12.2–13.0、tilt 10.6–11.7 Mbit/s。YouTube 對 1080p、30 fps、SDR 上傳的建議是 **8 Mbit/s**（[Recommended upload encoding settings](https://support.google.com/youtube/answer/1722171)），運鏡段平均是它的兩倍、最高三倍。

**怎麼量的**：八個鏡頭（43.1 秒；每種運鏡至少一個，CRF 18 下從 6.6 到 24.4 Mbit/s 都有），用 `motionSegmentArgs` 同一條濾鏡鏈輸出無損參考，再用同一組編碼參數只換受測的設定去編，對參考算 VMAF（`libvmaf`，另記每個鏡頭最差 1% 的格）與亮度 PSNR；CRF 18 這樣編出來的大小與正式分段一致（`steamer-lift` 14.12 對 14.13 Mbit/s）。最後一欄是「觀眾看到的」：把每個版本再用 x264 以 4 Mbit/s 轉一次（代替平台轉檔，只量了前五個鏡頭），仍對無損參考算 VMAF。

| 運鏡段的設定 | 平均位元率 | 大小 | VMAF | 最差鏡頭的最差 1% | PSNR-Y | 再轉一次後的 VMAF |
| --- | --- | --- | --- | --- | --- | --- |
| CRF 18（原本） | 16.6 Mbit/s | 100% | 97.7 | 94.2 | 41.4 dB | 93.4 |
| CRF 20 | 12.5 | 75% | 97.3 | 93.3 | 39.8 | |
| CRF 22 | 9.3 | 56% | 96.7 | 92.4 | 38.3 | |
| **CRF 18＋`-maxrate 8M -bufsize 16M`（採用）** | **8.3** | **50%** | **96.7** | **91.0** | **38.4** | **92.4** |
| CRF 23 | 8.0 | 48% | 96.4 | 91.9 | 37.5 | |
| CRF 24 | 6.8 | 41% | 96.0 | 91.2 | 36.7 | 92.5 |
| CRF 20＋`-maxrate 6M -bufsize 12M` | 6.3 | 38% | 95.9 | 89.8 | 37.0 | 92.0 |
| CRF 24＋`-maxrate 6M -bufsize 12M` | 5.6 | 33% | 95.4 | 89.6 | 36.0 | |
| CRF 26 | 5.0 | 30% | 94.9 | 89.6 | 35.2 | 91.9 |
| CRF 28 | 3.7 | 22% | 93.4 | 87.7 | 33.8 | 91.2 |

`-tune film` 拿掉（CRF 23）只差 4% 大小、分數在同一條線上，不是槓桿。P 幀與 B 幀的 PSNR 差在 CRF 18 是 1.4 dB，上限 8 Mbit/s 時 0.55 dB：壓低位元率沒有讓畫面一格一格地閃。

**看畫面**（最吃位元的 `kitchen-wide` 第 112 格，滿版密網點，原生 23.9 Mbit/s）：1:1 看，8 Mbit/s 上限與 CRF 18、無損參考分不出來；放大兩倍，最密的網點區比 CRF 18 多一點不均勻（CRF 18 自己對無損也有）。到「三分之一大小」的設定（6 Mbit/s 上限、CRF 26–28）就不乾淨了：放大兩倍網點成塊，CRF 28 在 1:1 就看得出最密的網點糊成一片灰。所以**三分之一做不到**：整支片要到三分之一，運鏡段得壓到約 3.9 Mbit/s，是 YouTube 建議值的一半。

**決定**：運鏡段維持 CRF 18，加上 YouTube 建議的 8 Mbit/s 上限、兩秒緩衝（`assemble/drama.mjs` 的 `MOTION_MAX_RATE`、`MOTION_RATE_BUFFER`，`MOTION_ENCODER_VERSION` v4）。原本就低於上限的畫面（漂移的卡片、平塗畫風、`three-kilns` 這種 6.6 Mbit/s 的鏡頭）照舊（`three-kilns` 的 PSNR 前後都是 45.5 dB）；超過的鏡頭實測落在 8.4–9.1 Mbit/s（短鏡頭開頭可以先用掉緩衝），最難的三個鏡頭 PSNR 從 39.2 降到 34.3 dB、VMAF 從 98.9 到 97.2。再轉一次之後與 CRF 18 的母片差 1.0 分（轉檔本身就掉 4.8 分）。漫劇的片段段（`CLIP_ENCODER_VERSION`）沒量、沒動。

**改完的大小**：同一支片在複製的工作區用新設定重跑 `assemble`：`final.mp4` **535 MB**（原本的 60%，40 MB／分鐘、整支平均 5.3 Mbit/s），`checks.json` 全過、24,061 格不變。74 段插圖從 804 MB（15.3 Mbit/s）變成 444 MB（8.4 Mbit/s），最高的一段 10.0（2.1 秒的短鏡頭把緩衝用掉），原本就低於上限的 `three-kilns` 與 11 張漂移卡片（合計 18.2 MB）大小差不到 0.2%。107 段裡重編 85 段（插圖與漂移卡片；多狀態卡片沿用快取），在同時跑量測的 8 核筆電上花 32 分鐘。之後估大小用這幾個數字：

| 畫面 | 每分鐘 | 十分鐘 |
| --- | --- | --- |
| 純投影片（卡片與靜態圖） | 約 10 MB | 約 100 MB |
| 插圖投影片（一半時間是運鏡的插圖） | 約 40 MB | 約 400 MB |
| 最壞情況：整支都是頂到上限的運鏡 | 約 70 MB | 約 700 MB |

**站台的單檔上限**：`VIDEO_REVIEW_MAX_FILE_BYTES` 的預設從 400 MB 改成 1.5 GB（`apps/api/app/config.py`）。400 MB 是照純投影片訂的，新設定下 13 分鐘的插圖投影片仍超過它；1.5 GB 容得下最壞情況的 20 分鐘、一般情況的 35 分鐘以上。磁碟成本在 `HANDS-OFF.md` §上傳包與「可以上架」。

**已經做好的成片不用動**：`MOTION_ENCODER_VERSION` 一變，下次 `assemble` 會把那支片的運鏡段全部重編，`final.mp4` 的雜湊跟著變，成片核准要重來。不要為了縮小檔案去重跑已核准的成片（`openai-devday-2026-recap` 就維持 895 MB 那一份）；新設定只用在之後才 `assemble` 的影片。

**順帶看到、沒在這裡修**：運鏡其實是走一步停幾格（關鍵影格是 JPEG 時 `zoompan` 的裁切窗只落在偶數像素上；pan 有一半的相鄰格完全相同），票 `2026-10-04-still-shot-camera-moves-travel-in`。修它會讓每一格都不同、位元率再變，上限會把大小擋住。

## 圖庫照片（stock photos）：Pexels 與 Pixabay（2026-10-05）

產線一直沒有任何真實照片：旅遊攻略的投影片只有深色卡片、版畫插圖或 AI 圖，而 Pexels 與 Pixabay 都有首爾、釜山、濟州的實景照片，授權允許商業使用。票 `2026-10-05-stock-photo-source-endpoint` 做的是伺服器端：兩家的金鑰只存在伺服器（和旁白、生圖一樣，本機工具拿不到），搜尋與抓檔都走 `/api/v1/video/media/stock/*`（`apps/api/app/video_media/stock.py`），原圖進媒體庫並附上版權標示。把照片放上投影片、把來源寫進說明欄是票 `2026-10-05-stock-photo-slides-and-attribution`（下面的「工具端」）。

### 設定

| 項目 | 在哪 |
| --- | --- |
| 設定卡 | `/admin/settings` 的「影片素材」分頁、「圖庫照片（Pexels、Pixabay）」卡（`stock_photos`）：兩個金鑰（`pexels_api_key`、`pixabay_api_key`，加密存在伺服器，設定任一家就能用）、兩個 Base URL（釘在 `api.pexels.com` 與 `pixabay.com`：改成別的網域會被拒絕、存進資料庫的也會被忽略），和「連線測試」：對每一家真的搜一次「Seoul skyline」（免費），回每家的總張數；任一家失敗整個測試算失敗；沒測過的卡顯示「尚未驗證」 |
| 環境變數 | `PEXELS_API_KEY`、`PIXABAY_API_KEY`；`PEXELS_API_BASE_URL`、`PIXABAY_API_BASE_URL` 不用設，正式站啟動時會檢查它們沒離開官方網域 |
| 申請 | Pexels：pexels.com/api（免費；預設每小時 200 次、每月 20,000 次）。Pixabay：pixabay.com/api/docs（免費；預設每分鐘 100 次；原圖 `imageURL` 與 1920 px 的 `fullHDURL` 只給「full API access」的帳號，沒有的拿 1280 px 的 `largeImageURL`） |

### 端點（都要影片工具權杖）

| 端點 | 送什麼 | 回什麼 |
| --- | --- | --- |
| `POST /stock/search` | `{query（≤100 字）, provider?（pexels／pixabay；不寫＝每一家有金鑰的）, orientation?（landscape／portrait／square；Pixabay 沒有 square 篩選，照回）, per_page（1–40，預設 15）, page}` | `{query, candidates[], total{廠商: 張數}, problems[]}`；候選是 `{provider, id, width, height, thumbnail, preview, alt, credit}`，`credit` 是 `{provider, author, author_url, url（照片頁）, license, license_url, text}`；一家失敗、另一家有答，失敗的只列在 `problems`；全部失敗才回錯 |
| `POST /stock/fetch` | `{slug, provider, id}` | `{sha256, size, content_type, width, height, credit}`。伺服器再向廠商要一次這張照片（不信工具給的 URL）、取最大的檔（Pexels `src.original`；Pixabay `imageURL` → `fullHDURL` → `largeImageURL`）、只從廠商自己的主機下載（`images.pexels.com`；`pixabay.com`、`cdn.pixabay.com`），串流進媒體庫（和生成檔同一套：邊收邊算雜湊、從位元組判型別、只收 png／jpeg／webp、上限同 `VIDEO_MEDIA_MAX_FILE_BYTES`）；`width`／`height` 從存下的檔頭讀，不信廠商的數字 |
| `GET /status` | | 多回 `stock: {pexels: bool, pixabay: bool}` 與 `limits.stock_per_page`（40）：工具只在伺服器這樣說時才提供圖庫照片 |

錯誤碼：`video_media_stock_unavailable`（503，沒金鑰）、`video_media_stock_not_found`（404，廠商沒有這張）、`video_media_stock_failed`（502：廠商拒絕金鑰、回應壞掉、檔案不在廠商主機、圖讀不出尺寸）、`video_media_upstream_busy`（429，帶 `Retry-After`），以及媒體庫自己的 `video_media_file_too_large`／`video_media_store_full`／`video_media_unsupported_type`。訊息裡只有廠商名與狀態碼，永遠沒有 URL：Pixabay 的金鑰在查詢字串裡。

不是生成工作：不建 `video_media_jobs` 列（kind 的 CHECK 仍是 image／clip／music）、不記任何月預算（兩家免費），只有每個權杖每小時 150 次的 `video_media_stock` 限制（search 與 fetch 共用；Pexels 免費金鑰一小時 200 次）。檔案和其他媒體檔一樣是快取：14 天後 `prune` 會清，工具要把自己的那份放在工作目錄（下一張票的 `<workdir>/stock/<sha256>.<ext>`）。

### 授權與標示（兩家都要照做）

| | Pexels | Pixabay |
| --- | --- | --- |
| 授權 | [Pexels License](https://www.pexels.com/license/)：免費、可商用、可修改、不必標示 | [Pixabay Content License](https://pixabay.com/service/license-summary/)：免費、可商用、可修改、不必標示 |
| 不可以 | 原樣轉售或在別的圖庫重新發布；暗示人物或品牌背書；把可辨識的人放進負面或冒犯的情境 | 原樣轉售或當成獨立檔案重新發布；暗示背書；把可辨識的人放進負面或冒犯的情境 |
| API 規則 | 可能的話標示攝影師並連回照片頁（「Photo by … on Pexels」）；用到 API 的地方要有顯眼的 Pexels 連結（「Photos provided by Pexels」）；不可整批下載、不可複製 Pexels 本身的功能；快取結果 | 顯示搜尋結果的地方要標示 Pixabay；不可熱連結，必須下載到自己這邊（fetch 做的正是這件事）；API 回應最多快取 24 小時（`webformatURL` 這類網址一天後失效）；不可整批下載；金鑰不可公開 |
| 我們怎麼做 | `credit.text` 就是廠商要的那一句，`stock fetch` 原樣寫進 `assets[].source`，說明欄的「圖片來源」區塊逐張列出（§工具端）；投影片預設不畫字（站主的規則），要畫才寫 `data.credit`；`stock search` 印候選時帶「Photos provided by Pexels」 | 同左；印候選時帶「Images from Pixabay」，並提醒預覽網址一天後失效 |

兩家都不「要求」標示，但都希望有，而且 API 使用規則要求來源可見。說明欄 5,000 位元組的上限：一行標示約 110–130 位元組（「Photo by … on Pexels（Pexels License）：照片頁網址」），區塊的標題與空行 19 位元組；`lint` 不算這些（`core/lint.mjs` 不讀 `assets[]`），只有 `package` 算，所以稿子的 `youtube.description` 要比 `lint` 的上限少留每張約 130 位元組——兩張照片留 300 位元組就夠，超過時 `package` 會說是標示把它推過線。這一段只讀了兩家的公開 API 文件與授權頁，沒有參考任何第三方程式。

### 工具端（2026-10-05，票 `2026-10-05-stock-photo-slides-and-attribution`）

| 項目 | 怎麼做 |
| --- | --- |
| 指令 | `node tools/video/media/cli.mjs stock search --query "Seoul skyline" [--provider pexels\|pixabay] [--orientation landscape\|portrait\|square] [--per-page N] [--page N] [--slug S] [--json]`，印每個候選的廠商、id、尺寸與方向、廠商要的那句標示、照片頁網址、alt，以及兩家 API 條款要的來源字樣；`node tools/video/media/cli.mjs stock fetch --slug S --provider P --id N [--workdir D] [--json]`。`tools/video/cli.mjs` 的指令表還沒有 `stock`，所以是直接跑 `media/cli.mjs`（它自己有 `main`，結束碼同主指令：2 用法、3 要站主、4 外部服務） |
| 檔案 | `stock fetch` 請伺服器抓進媒體庫後，用 `downloadFile` 邊收邊核對雜湊下載到 `<VIDEO_WORKDIR>/<slug>/stock/<sha256>.<png\|jpg\|webp>`（副檔名照伺服器回的 `content_type`）；同一張再抓一次不會重載（檔名就是雜湊，核對過就跳過），壞掉的複本會重載。媒體庫那份 14 天後會被 `prune` 清掉，工作目錄這份才是成片用的 |
| `assets[]` | 每抓一張就在 `docs/videos/<slug>/video.json` 的 `assets[]` 寫（或換掉同路徑的）一筆 `{path: "stock/<sha256>.<ext>", source: credit.text, license: credit.license, author: credit.author, url: credit.url}`：`source` 是廠商自己的措辭（「Photo by … on Pexels」「Image by … from Pixabay」），`author` 只有名字，`url` 是照片頁。沒有 `assets` 的 `video.json` 會在 `scenes` 前面長出來；整個檔案會以工具的格式（兩格縮排）重寫 |
| 投影片 | `screenshot` 範本的 `data.image` 多接受 `stock/<sha256>.<png\|jpg\|webp>`（只有這個寫法，小寫、64 個十六進位字；repo 路徑的規則不變），渲染時從 `https://video.local/work/stock/…` 載入（和關鍵影格同一個假來源）；`data.credit`（選填，一行、≤60 字）畫在照片右下角的深色小膠囊裡，它的 CSS 只在有 `credit` 的那一頁隨頁帶，所以沒寫 `credit` 的截圖頁和 `theme.css` 都一個位元組都沒動，既有影片的畫格鍵不變。直向或方形照片照高度放、置中；超寬的全景會超出版面，渲染會當版面問題報出來，換一張 |
| 畫格鍵 | `render/plan.mjs` 的 `renderPlan` 多吃 `workdir`，照片的位元組和 SVG 一樣雜湊進那一景的鍵：換了照片（同名不同位元組）只重畫那一景；沒給 `workdir`（例如 `render/repeat.mjs`）就不讀、不入鍵 |
| 渲染前的檢查 | `renderProblems(doc, root, {workdir})`：用到 `stock/…` 的景，`assets[]` 裡一定要有同路徑的那筆（沒有就代表說明欄不會有標示，`render` 以 lint 結束碼拒絕），檔案也要在工作目錄裡（沒有就叫你跑 `stock fetch`）。`lint` 只檢查 `data.image`／`data.credit` 的寫法（範本的 `check` 共用），不看工作目錄 |
| 說明欄 | `core/metadata.mjs` 的 `composeDescription` 在參考資料之後、hashtag 之前加「📷 圖片來源」區塊（各語系：圖片來源／图片来源／Image credits／画像の出典／이미지 출처），一張一行：`source（license）：url`（英、韓文用半形括號與冒號）。只列有 `author` 或 `url` 的 `assets[]`——自有圖解（只有 `path`／`source`／`license`）不列，所以列著自有圖解的既有影片，說明欄一個字都不會變，`publish` 關卡綁的 `upload/metadata.json` 也不會失效。`package/metadata.mjs` 每個語系都帶 `doc.assets` 進去；超過 5,000 位元組時的錯誤會註明是標示多了幾個位元組 |
| 錯誤碼 | `video_media_stock_unavailable`（沒金鑰）→ 要站主（結束碼 3）；`video_media_stock_not_found` → 工具的錯（id 寫錯，結束碼 2）；`video_media_stock_failed`、429 → 和 `locate` 一樣重試，耗盡才算外部服務（4）；網站的 web app 還沒轉送 `stock/*` 路由時會收到 `video_media_route_unknown`，工具把它改說成「要部署會轉送這些路由的版本」（結束碼 3） |

web app 的轉送（`apps/web/app/api/video/media/[...path]/forward.ts` 的 `mediaRoute` 白名單）由票 `2026-10-05-web-app-forwards-stock-and-locate` 補上了 `stock/search`、`stock/fetch` 與 `locate`。還沒做：`tools/video/cli.mjs` 的 `AREAS` 沒列 `stock`，加一行就能用主指令跑。

### 沒實測的事

這個容器沒有金鑰：欄位名照兩家的文件寫（Pexels `photos[].src.original`、`photographer_url`、`alt`；Pixabay `hits[].largeImageURL`、`imageWidth`、`user_id`），第一次真的呼叫要看 `search` 的候選數、`fetch` 存下的檔案尺寸與 `credit` 是否對得上照片頁；Pixabay 沒有 full API access 時 `imageWidth`／`imageHeight` 有沒有回來（沒有就以 `webformatWidth`／`webformatHeight` 代替，候選的尺寸會是 640 px 那一檔）。

## judge 的 problems：準確、完整、有解（2026-10-05）

`problems` 原本是自由文字：一張圖可以某一題沒過卻沒有一句話提到它，也可以列一句跟沒過的題無關的意見；改提示詞的人（工人的撰稿修正迴圈、站主、重拍迴圈）拿到的東西不一定能動手。照 CHAI 研究的審稿三規矩（準確：指出在哪裡；完整：同一種毛病整張圖都找過；有解：每個嚴重的發現都附一個修法；OpenMontage 的 reviewer skill 用同一套，AGPL，只借想法）定成契約：

**格式**：每一條 `problems` 都是一行 `<criterion key>: <哪裡有什麼不對> → <一個提示詞層級的修法>`。鍵是 rubric 的 key（`text`、`anatomy`、`identity_jingwei`…），箭頭後面是**可以直接貼進提示詞的字**（`clean: the barista's right hand is a blur → her right hand flat on the counter`），不是建議（「把手改好」）。

| 誰 | 做什麼 | 在哪 |
| --- | --- | --- |
| 伺服器：問法 | 打分數的 `INSTRUCTIONS` 與是非題的 `CHECK_INSTRUCTIONS` 都要求這個格式：鍵照 rubric 寫、指出地方、寫之前把同一種毛病整張找過、最嚴重的放前面；刻度與「答有或沒有」那幾句逐字不動（它們是量過的，§judge 的刻度與判定沿用） | `apps/api/app/video_media/judge.py` `PROBLEM_FORMAT` |
| 伺服器：扣到格式上 | `verdict()` 先算**沒過的題**：是非題是答有的那題（分數低於 10）；打分數是低於門檻的題（`min_score` 與每項下限 4 取大；overall 是加權平均，所以沒過的 take 一定至少有一題，過了的 take 也可能有一題在門檻下）。**丟掉**沒有鍵的行、鍵不是 rubric 的 key 的行、鍵指到沒有沒過的題的行（每項都 7、門檻 7 時的「意見」就是這種）；鍵的寫法寬鬆一點也認（`Text:`、`**anatomy** -`、`identity jingwei:`、直接 `anatomy → …`）。**補上**：沒過卻沒有任何一行提到的題，加一行 `<key>: the judge found it but did not say what or where (asked: <題目>) → write the correction into the prompt`；judge 寫了毛病卻沒給修法的行，箭頭後面補同一句。一行最長 400 字（修法最多 200 字、先裁毛病那段，箭頭後面一定留著）；judge 自己的行最多 20 條，之後接補上的行 | `judge.py` `failed_criteria`、`problems`、`PLACEHOLDER_FIX`、`UNDESCRIBED` |
| 不變的 | `JudgeOut` 的形狀（`scores`／`overall`／`passed`／`problems`／`notes`／`model`）與送後台的 payload（`shots[].judge.overall`／`problems`、分鏡整體的 `judge.problems`、設定圖每張的 `judge.problems`）；後台頁照舊把 problems 接在分數後面顯示 | `schemas.py`、`tools/video/review/sync.mjs` |
| 工具：下一個 take | 每個 take 之前把**它之前的 take** 的修法接在提示詞後面：`<prompt>. Corrections: <修法一>; <修法二>`（`fixesBefore`：箭頭後面那段，依 seed 排、去重；`retakePrompt`，上限 4000 字）。關鍵影格第 1 個 seed 照原提示詞，第 2 個帶第 1 個的修法，第 3 個帶前兩個的；片段同理（2 個 take）；設定圖同一角色第 2 張起帶前面幾張的修法，第二輪帶第一輪全部的；畫風樣張也一樣。帶了的修法記在該 take 的 `fixes`，stdout 印 `<id> take 2: asked with the corrections of the takes before: …` | `media/keyframes.mjs` `fixClauses`、`fixesBefore`、`retakePrompt`；`clips.mjs`、`look.mjs` 匯入同一組 |
| 工具：佔位不貼 | 伺服器補的那句 `write the correction into the prompt` 是給改提示詞的人看的，不是提示詞：工具認得它（`PLACEHOLDER_FIX`，兩邊拼法相同、各自的測試釘住），不貼進下一個 take | `keyframes.mjs` `PLACEHOLDER_FIX` ↔ `judge.py` `PLACEHOLDER_FIX` |
| 工具：快取與沿用 | 快取鍵含提示詞，帶了修法的 take 是另一個請求（會付錢），同樣的修法再跑一次仍從快取拿回；`entryStands` 用同一條規則（前面 take 記下的判定）重算每個 take 的鍵，所以改別鏡的提示詞時，帶著修法的 take 照樣沿用、不重判。舊 manifest 的 `problems` 沒有箭頭，等於沒有修法，行為跟以前一樣 | `keyframes.mjs` `entryStands` |
| 工具：沒過時的提示 | manifest 條目除了 `problems`（每個 take 的每一行，去重）多一個 `fixes`（所有修法，去重），stdout 在 `ERROR <id>: …` 之後印 `  fixes for <id>: …`；匯入的片段沒過也一樣。工人的撰稿修正迴圈照舊讀 `problems`，拿到的每一行現在都帶鍵與修法 | `keyframes.mjs`、`clips.mjs`（含 `clips import`）、`look.mjs`；讀的是 `automation/flow.mjs` `failedTargets` |

**還沒量**：票的 DoD 要在 163 張已記錄的出圖上量「沒過的 take 裡，`problems` 有一行點到沒過那一題的比例」前後對照。量測工具與每一輪的回答在做 DevDay 那台機器的 `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration/`，這個 repo 沒有，而且圖只在站上的媒體庫留到 2026-10-17。要量：部署後用 `rejudge.mjs` 經正式站對同 163 張再判一輪（約 US$1.63，先問站主），對每個沒過的 take 數「`problems` 裡有沒有一行的鍵等於答有的題」；before 用 `host/fa.out` 裡的舊回答，鍵用關鍵字對（`text`／`letter`／`word`、`finger`／`hand`／`arm`、`float`／`detached`、`style`、`frame`／`border`）。系統指示只改了「problems」那一句，是非題的答案照理不受影響，但沒量過之前不能宣稱；量到了把數字寫回這一節。

## 聲音表演（voice performance contract，2026-10-05）

旁白一直是「自然地唸」：Gemini 的 `voice.style` 帶口音與口吻（§說書式旁白的 `STORY_VOICE_STYLE`），漫劇的角色台詞帶 `emotion`，但解說與品牌故事沒有任何東西告訴聲音哪裡放慢、哪裡亮起來、哪裡停。票 `2026-10-05-voice-performance-contract` 把**表演計畫**從稿子一路帶到合成（想法來自 OpenMontage 的 voice-performance director，AGPL，只借想法、沒抄程式）：

| 欄位 | 意思 | 規則 |
| --- | --- | --- |
| `voice.performance` | 整支影片的表演計畫（zh-TW，≤ 200 字）：口吻、速度、哪裡抬起來、哪裡收；寫在站主的 `voice.style` 旁邊，不重複它 | 只在文件的 `voice`（旁白）上，角色的 `voice` 不收（`core/drama.mjs` `validatePerformance`；schema 的 `VOICE_KEYS` 不認這個鍵，所以 drama.mjs 收回它對 `voice.performance` 那一條 unknown-field 錯誤，自己檢查）；與 `voice.style` 相加不得超過 style 的 400 字；Azure 聲音收下但 lint 警告它被忽略 |
| `lines[].emotion` | 這一句的表演提示（zh-TW，≤ 80 字）：壓低、放慢一字一字、問句上揚、揭曉前吸一口氣 | 任何格式的句子都可以帶（之前只有漫劇）；`speaker` 與 `audio_ref` 仍是漫劇才有 |

`voiceFor(doc, line)`（`core/drama.mjs`）組 Gemini 的 style：`voice.style`。計畫。這句的 `emotion`。發音提示，截到 400 字；`performance` 不會成為送出的欄位（`tts/requests.mjs` 的 `voiceFields` 只送 voice／style／model），角色台詞不套旁白的計畫。`planRequests` 本來就按有效聲音切請求，所以帶 `emotion` 的投影片句子自己成一個請求與一個片段快取鍵，鄰句不重錄。

雜湊：`speechHash` 本來就把整個 `doc.voice` 放進去，所以加或改計畫＝全部重錄＋旁白關卡重審；投影片的句子只在**有** `emotion` 時多雜湊那一項，所以沒有計畫也沒有提示的影片 `speech_hash` 逐位元不變（`core/drama.test.mjs` 釘住六個範例的雜湊），既有的 timeline 不會因為這張票變舊。

lint（`core/drama.mjs` `cueCoverageProblems`，經 `core/lint.mjs` 進警告）：稿子一旦參與這份合約（`voice` 有計畫，或任何一句有提示），能收到提示的句子（Gemini 聲音；有角色的漫劇只算角色的台詞，旁白是過場）至少三分之一要帶 `emotion`（`CUE_SHARE_MIN`），不然計畫會被平平地唸過去，lint 印 `N of M lines carry a performance cue`。兩者都沒有的既有影片不警告（警告本來只給人看，工人的修正迴圈只吃錯誤）。`emotionProblems` 對 Azure 聲音上的計畫與每句提示各警告一條，任何格式都查。

撰稿提示（`writer-video.md`／`INSTRUCTIONS.writer`、`writer-drama.md`／`DRAMA_INSTRUCTIONS.writer`、`writer:explainer`、`writer-story.md`）要求：計畫寫在 `voice.performance`，至少三分之一的句子帶提示（鉤子、每個「其實」、每章收尾的問句一定有），提示說的是這句**怎麼唸**，不是它的意思。

還沒接上的（留給後面的票）：

- 工人路線的 `settle()`（`automation/flow.mjs`）把撰稿回來的 `voice` 整個換成設定分頁的聲音，計畫在那裡會被丟掉（句子上的提示留著）；要讓工人路線也帶計畫，`settle()` 要保留 `video.voice.performance`（設定分頁的 `VoiceSettings` 沒有這個欄位）。本機（skill）路線的撰稿代理直接寫 `video.json`，計畫會留下。
- 品牌故事逐章撰稿的工人文字（`automation/story-prompts.mjs`）還沒帶提示的規則；`writer-story.md` 先寫了。
- `dubs/plan.mjs` 的 `dubVoice` 展開 `doc.voice`，計畫會跟進每個語言配音的 style（提示本來就跟進漫劇的配音）；要留給配音還是在那裡拿掉，再決定。
- `voice-audition.md` 的試聽樣稿應該改成最吃表演的一段而不是開頭（票的 DoD 第四項；那份檔案不在票的範圍）。

## 樣張只畫給吃得下的模型；修兩輪沒過的圖保留到成片關卡（2026-10-06）

2026-10-06 查正式站：九支卡住的投影片影片裡有三支（threads-parental、gemini-gems、sec-ai-trading）卡在「rendered as a photorealistic image instead of a 2D risograph illustration; … differ from the style plate」。站主 10-04 把插圖模型換成 MiniMax `image-01`，而伺服器的 MiniMax adapter（`providers/minimax.py`）只轉送 `character` 參考圖，`style` 的樣張它根本沒看到；judge 卻拿樣張比對，每張都打回，改提示詞救不了。站主決定留 image-01、修相容，並且「關鍵影格修兩輪仍沒過就不要再卡住」。

| 改了什麼 | 怎麼做 | 在哪裡 |
| --- | --- | --- |
| 樣張只畫給吃得下的模型 | 目錄的 `MediaModel` 多 `style_references`（兩個 Gemini 圖模型 1、image-01 0），`/media/status` 的 `models.images[].style_references` 帶出來；工具端 `takesStyleReference(status, format)` 讀它（舊伺服器沒這欄時 Gemini 才算 1）。沒樣張時不呼叫 `stylePlate`、不送 `style` 參考圖、manifest 沒有 `plate`、judge 的 `style` 題改用文字版（「與 context 描述的畫風不同」）、judge 檔案不附樣張；stdout 印 `style plate: skipped; minimax/image-01 takes no style reference, the style is judged from the look's text`。參考圖清單變了 → `imageKey` 變 → 受影響的影片重畫一次（image-01 每張 US$0.0035） | `apps/api/app/video_media/catalog.py`、`video_automation/schemas.py`；`media/stages.mjs`、`media/keyframes.mjs` |
| 修兩輪仍沒過 → 保留最好的一張往下做 | `keyframes --accept-best <id,…\|all>`：有圖的 shot 設 `needs_review: false`、`problems` 搬到 `accepted_with_problems`、`judge` 與 `takes` 原樣保留，重畫聯絡表（標籤「保留」）；只有拒絕紀錄沒圖的 shot 拒絕接受（還是要改提示詞）。工人端 `fixPrompts` 在 `rounds >= MAX_PROMPT_FIX_ROUNDS`、kind 是 keyframes、投影片、不是站主退件、每個失敗 shot 都有圖時跑它，記 `auto.json.accepted_pictures = [{id, problems}]`、`notes` 加一行、`prompt_fixes.keyframes` 歸零（站主之後改提示詞重畫，有自己的兩輪）。漫劇、沒圖的 shot、站主退回的分鏡照舊卡住 | `media/keyframes.mjs` `acceptBest`；`automation/flow.mjs` `acceptBestPictures` |
| 分鏡關卡自己過 | `review-push --gate storyboard` 對保留的 shot 送 `accepted: true, needs_review: false`，頂層 `judge.overall`／`problems` 只算其他 shot（全部保留時 `overall: null`），另附 `payload.accepted = [{id, overall, problems}]`；伺服器 `storyboard_check_passed` 對 `accepted: true` 的 shot 略過分數與 problems（圖與 sha 還是要有）。`keyframeProblems` 對有 `accepted_with_problems` 的 shot 不再把 `judge.passed === false` 算成待審 | `review/sync.mjs`；`apps/api/app/video_automation/settings.py`；`core/state.mjs` |
| 成片關卡交給站主 | 工人送成片時帶 `--manual-review`；`review-push --gate final` 自己也會從 manifest 讀 `accepted_with_problems`（有就當 manual review，不靠旗標），`manual_review_reason` 寫「有 N 張插圖未通過 judge（ids），需站主審看成片」、payload 附 `accepted_pictures`、summary 結尾「N 張插圖未通過 judge（ids），需站主審看」，站上就不會從 `payload.qa` 自動核准。QA 的 `assemble` 項掛 `warnings` 列出保留的 shot（不新增項目，`ITEM_IDS` 與伺服器鎖死） | `automation/flow.mjs` `gate`；`review/sync.mjs` `acceptedPicturesOf`；`qa/cli.mjs` |
| 第一稿就知道預算 | 工人給撰稿 `prompt_budget_chars`：由設定的投影片圖模型（`slides.slides_image_model`，開關關著就是漫劇的模型；工具端 `IMAGE_MODEL_VENDORS` 對 id 查 vendor）、這支可能拿到的畫風裡最重的一個（五個版畫預設加 tech-story，撰稿可以自己點名一個，所以不能只算 slug 抽到的那個；10-06 量是 riso-teal）、最長的運鏡詞算，上限 1000；第一稿、lint 修正、劇本退回與提示詞修正的整份改寫都帶同一個數字。撰稿提示詞改成「at most 1000 characters, or at most "prompt_budget_chars" when the payload gives one」。品牌故事的 `fixStoryPrompts` 也帶 `prompt_budget_chars` | `automation/flow.mjs` `draftBudget`、`media/prompt-budget.mjs`、`automation/prompts.mjs`、`automation/story.mjs` |

部署後要驗的事：三支卡在樣張的影片站主按重試後，工人日誌有 `style plate: skipped`、判定改用文字版；一支修兩輪仍沒過的影片日誌有 `N pictures kept with the judge's remarks after 2 prompt fixes`、`auto.json` 有 `accepted_pictures`、分鏡自動核准、成片卡片 summary 列出保留的 shot 並等站主。

### 同日後續：卡片列出保留的圖、summary 不超過 500 字、只有插圖影片能保留

站主 10-06 的決定：有保留圖的成片一律不自動核准，審核卡片要把保留的圖列出來。上面那一版只把它們寫進一行 summary，而且每個 shot id 都寫，圖一多就會被站台退件。

| 改了什麼 | 怎麼做 | 在哪裡 |
| --- | --- | --- |
| summary 不會被站台退件 | 伺服器的 `ReviewIn.summary` 上限 500 字（算碼位），超過回 422，`review-push` 以 lint 碼結束，工人把影片卡住（`submissionFailure`）。成片的 summary 與 `manual_review_reason` 只點名前 5 個保留的 shot，後面寫「等，另 N 張」（`namedPictures`）；完整清單在 `payload.accepted_pictures`。`reviewPush` 送出每一筆審核前都過 `fitSummary`：500 字以內原樣，超過就切到 500 字、最後一個字是「…」（shot id 本身沒有長度上限，這是最後一道防線）；大綱那一筆是工人自己送的（`flow.mjs` `submitOutline`），不經過 `reviewPush`，所以在 `outlineReview` 組好時就過一次。旁白的 summary 在第二轉寫排除的句子多到放不下時只寫句數（`audioSummary`），句子 id 還在 `payload.cleared_lines`。分鏡與其他關卡的 summary 只有數字與固定的幾個代號 | `review/sync.mjs` |
| 只有插圖影片能保留 | `keyframes --accept-best` 對 `illustrated(doc)` 以外的影片（漫劇、解說漫劇）回用法錯誤：只有插圖影片的成片會送站主人工審看（`acceptedPicturesOf`、`acceptBestPictures` 用同一個判斷），漫劇的 shot 要是被保留，分鏡與成片可能一到站就核准、沒有人看過那張圖 | `media/keyframes.mjs` `acceptBest` |
| 卡片看得到 | 成片卡片：`payload.manual_review` 為 true 時最上面顯示「這支成片要由你審看，不會自動核准」與 `manual_review_reason`；沒有 `payload.qa` 時把 `manual_review_qa` 的項目列在同一個「自動品管」清單並標「僅供參考」；`accepted_pictures` 列成「保留的插圖（N 張）」，每張帶 judge 的意見。分鏡卡片：`payload.accepted` 點名（或自己帶 `accepted: true`）的 shot 標「保留」、藍框、分數與意見，跟「待修」的琥珀框分開；還在 `needs_review` 的 shot 不會被標成保留；整塊分鏡沒有分數時（全部保留，`judge.overall` 是 null）不顯示「自動檢查」那一行，不留一個後面沒字的標籤。欄位缺漏或型別不對就不顯示那一塊，卡片照常 | `apps/web/components/admin-video-review-card.tsx`、五語 `admin.json` |
| payload 不會被站台退件 | 伺服器的 `ReviewIn.payload` 上限 262,144 bytes（`MAX_PAYLOAD_BYTES`；量的是 `json.dumps(value, ensure_ascii=False)` 的 UTF-8 長度，逗號與冒號後各多一個空白），超過一樣回 422、影片卡住。judge 的意見是每個 take 的聯集，而且一筆審核帶兩份：成片在 `accepted_pictures` 與 QA `assemble` 項的 `warnings`，分鏡在 `accepted` 與每個 shot 自己的 `judge.problems`。現在：(1) QA 的 `assemble` 項只掛一行 warning，寫保留幾張與前 5 個 id（`keptPicturesWarning`，例：`80 pictures kept … (a, b, c, d, e and 75 more)`），不帶意見。(2) `reviewPush` 送出每一筆審核前過 `fitPayload`：保留圖的意見每張最多 6 行、每行 300 字（算碼位，超過以「…」結尾），後面多的寫成一行「…另有 N 則，全文在 keyframes/manifest.json」（`keptRemarks`）；分鏡裡保留 shot 自己的 `judge.problems` 同樣處理。(3) 照伺服器的算法量（`payloadBytes`），還超過 240,000 bytes 就再縮：每張 2 行；還不夠就每張只留一行「意見因審核資料的大小上限略去，全文在 keyframes/manifest.json」，分鏡裡保留 shot 自己的 `judge.problems` 清空。每個 id 都還在，stdout 會寫縮到哪一步。(4) 縮完仍超過伺服器上限（一般 262,144；長篇動畫的劇本 1,048,576，判斷條件與伺服器相同）就不送，印出 `the storyboard review's payload is N bytes, over the 262144 the site takes…; nothing was sent` 並以 lint 碼結束（工人照「站台退件」處理、寫出原因），不等站台回 422（站台對過大的 payload 只回「payload：格式或內容不正確」，看不出大小）。沒有保留圖的審核內容不動，超過上限一樣不送；待修 shot 的 `judge.problems` 原樣送（退件後工人靠它修提示詞）。完整意見一直在 `keyframes/manifest.json` 的 `accepted_with_problems` | `review/sync.mjs`、`qa/cli.mjs` |

## 沒做、留給後面

- 圖庫照片（§圖庫照片 的「工具端」）還差一件接線：`tools/video/cli.mjs` 的 `AREAS` 沒列 `stock`，現在要直接跑 `media/cli.mjs`（web app 的轉送白名單已由票 `2026-10-05-web-app-forwards-stock-and-locate` 補上）。`lint` 不算說明欄的「圖片來源」位元組（`core/lint.mjs` 不讀 `assets[]`），稿子要自己留；`docs/videos/README.md` §說明欄 的四個部分還沒列第五個「圖片來源」。工人的撰稿提示詞還不會自己去搜照片，目前是代理或站主手動 `stock search`／`stock fetch` 再把路徑寫進 `screenshot` 景。
- 是非題只用在插圖投影片（§judge 的刻度與判定沿用）。漫劇的設定圖、關鍵影格、片段與原來如此事務所的靜圖仍是打分數、也頂在 7：各自量過已記錄的出圖、定好各自的題目再換。judge 漏看的瑕疵（六指、像字的記號）要靠更細的題目或更強的判定模型，也要先量；`subject` 在 163 張裡一次都沒答有，窯門大開那種「主動作不對」被歸到 `details`，這一題的寫法值得再試。
- judge 的 problems 改成「鍵、毛病、修法」之後（§judge 的 problems），163 張的前後對照還沒量；`drama_preflight.mjs` 與 `run_report.mjs` 印的是 `problems`，manifest 的 `fixes` 它們還沒印。
- 樣張沒放進聯絡表（`review/sync.mjs` 用張數切頁，多一格會錯位）；要看就開 `keyframes/plate-N.png`。
- 多狀態卡片（bullets、steps、table 逐條出現）的整景連續運鏡。
- 插圖上沒有章節進度條（chrome 只在卡片上）；要的話把 chrome 截成透明疊層蓋在運鏡段上。
- Shorts 的逐句合成加固定 0.18 秒間隔：口吻改了節奏還是平，要改整景合成再切段（動到 phrase↔clip↔caption↔check 的對應）。
- Shorts 的運鏡還是線性、不隨長度縮放（`shorts/motion.mjs` 在 `2026-09-28-sothatswhy-shorts-from-episode` 的範圍裡）。
- lint 的變化警告只給人看；工人的撰稿修正迴圈只吃錯誤，所以景別、抄色盤、同一地點太多這三條要靠撰稿規則本身。試片三支的舊稿（抄色盤、桌子太多）要重寫提示詞才會變；RAG 那支有一段連續三張 push in，部署後工人會用撰稿修正迴圈改掉。
- 原來如此事務所（`flat-explainer`）的畫風與撰稿規則沒改，只拿到 2K（它的畫風允許無臉人物，不套 `craft`）。
