# Shorts 路線：直式短片從腳本到上架

Shorts 是 1080×1920、30 fps、25–55 秒（Shorts 設定的 `seconds_min`／`seconds_max`）的直式短片：一句旁白一張字卡、繁中字卡加頻道聲音，在後台 `/admin/videos?tab=shorts` 排月曆、自動品管、照站主的授權排上 YouTube。這份只寫**怎麼做**；為什麼這樣設計、YouTube 的規則與站主的決定在 `docs/videos/SHORTS.md`。

工具是 `node <ROOT>/tools/video/shorts/cli.mjs <子指令>`，跟長片的 `tools/video/cli.mjs` 分開：一支 Shorts 一份 JSON 腳本，不用 `video.json`、沒有章節、不套片頭片尾、不受「每集 8 分鐘」的規矩。

## 現在做得到什麼（2026-10-02 的 main）

| 內容線 | 誰做、怎麼做 | 還沒有的 |
| --- | --- | --- |
| **實測**（`lab`，系列 `daily`、`blind`、`prompts`） | 主機工人照題庫自己做（Shorts 設定「讓主機工人自己做 Shorts」開著、選了受測模型）；本機也可以照腳本 `build` | 要看圖、修圖、執行程式、生圖的題目工人不做（`tools/video/shorts/lab.mjs` 的 `UNSUPPORTED`），題庫標「缺素材或工具」 |
| **長片精華**（`cut`，系列是來源長片） | 本機：`from-episode` 從有 shot 的長片（原來如此事務所、插圖投影片）切兩支；別的工具做好的成片用 `import` | 工人的精華步驟（票 `2026-09-28-video-shorts-worker-cut`）還沒有。伺服器已經替公開的教學長片自動開精華題目，但工人與排片都先跳過 |
| **漫劇直式短篇**（`drama`） | 本機：`from-drama` 從已核准的 16:9 成片剪一段，9:16 視窗跟著主角（每鏡問一次站上的 `locate`），字幕走 Shorts 的字幕層；別的工具做好的成片用 `import`。`build` 仍拒絕 `line: "drama"` | 原生 9:16 的漫劇產線（票 `2026-09-28-video-shorts-worker-drama`）與工人的漫劇步驟還沒有 |

不管誰做的，送上站之後都走同一條：成片審核（12 項自動品管）→ 上傳包審核（4 項）→ 片庫 → 月曆的時段 → YouTube。

## 一次性設定

| 項目 | 怎麼做 | 沒做會怎樣 |
| --- | --- | --- |
| 影片工具權杖 | 跟長片同一個：`node tools/video/cli.mjs login` 配對（`automated.md` §一次性設定） | 要找站台的指令結束碼 3 |
| ffmpeg、瀏覽器 | 同長片；Windows ARM64 用 `--channel msedge` | `build` 在付旁白錢之前就停 |
| 頻道立場 | 站主在設定分頁寫（`docs/videos/HANDS-OFF.md` §頻道立場） | `policy` 永遠不過，每支都落到「需要你」 |
| 受測模型 | 站主在 Shorts 設定選 A 組（B 組不選就跟 A 一樣） | 實測線不開工，`shorts/next` 的保留原因寫「還沒選受測模型」 |
| 題庫 | 站主在 Shorts 分頁「題庫」匯入 `docs/videos/ai-shorts/campaign/campaign.json`（15 題，重複匯入不會多出題目）；企劃模型每週補題 | 沒題可排 |

## 腳本格式

範例：`tools/video/shorts/fixtures/smoke/script.json`（第 2 版）；三支試片 `docs/videos/ai-shorts/pilots/` 是第 1 版（只有實測線），雜湊被 `core.test.mjs` 綁著，不要改。格式在 `tools/video/shorts/core.mjs` 的 `validate`。

- 頂層：`schema_version: 2`、`slug`（小寫、3–80 字元）、`format: "shorts"`、`locale: "zh-TW"`、`line`、`series`、`titles`（剛好兩個：使用中與備案，各 ≤ 100 字元、不能有角括號）、`description`。
- 實測線另要 `experiment_summary`（測了什麼）、`limitations`（這次測試說不出什麼）、`evidence`（`[{path, sha256}]`，至少一個）；`series` 只能是 `daily`、`blind`、`prompts`。
- 精華與漫劇另要 `source.slug`（站上那支長片）；`source.url`（YouTube 網址）可省略，`package` 會在長片有影片 id 之後向站上讀；可加 `start_seconds`、`end_seconds`。
- 選填：`hashtags`（≤ 3）、`links`（≤ 5，`{label, url}`，只收 https）、`tags`（≤ 15，各 ≤ 30 字元）、`synthetic_media`（畫面有擬真生成圖時寫 `true`）、`music`、`sfx`（站主放在 `<VIDEO_WORKDIR>/_music/`、`_sfx/<set>/` 的授權檔；Shorts 不生成音樂）。
- `scenes`：3–12 個。每個 `headline` ≤ 36 字元、`narration` 是短句陣列（每句 ≤ 38 字元，一句一張字卡；字幕條一行放 15 個全形字、最多兩行，超過 30 個顯示單位的句子 `layout` 會失敗，38 字只是格式上限）；可加 `kicker`、`body`（≤ 5 列、每列 ≤ 85 字元）、`big`、`note`、`asset`（必須列在 `evidence`）、`camera`（push in／pull out／pan left／pan right／tilt up／tilt down／drift）。`shot` 只給精華用，`from-episode` 會換成長片的關鍵影格。

寫法：

- **開場**：第一句就是題目或反直覺的結果，2 秒內出現重點字卡；不問候、不自我介紹。開場那一句不能跟最近 30 支一樣（`variety`）。
- **結尾導流**：實測線收在結果與限制，導到下一個問題或對應文章；精華與漫劇的說明欄第一行由 `package` 自動放「完整影片：」連結（Shorts 的「相關影片」只能在 Studio 設，API 寫不了）。
- **長度不對就改稿**：旁白超出範圍時 `build` 直接失敗（`edit script to fit`），不會裁旁白；增刪句子，不要改語速。
- 數字照證據寫；實測平手就說平手、模型答錯就照實寫。

## 主幹（一支）

| # | 指令 | 產出 | 過關 |
| --- | --- | --- | --- |
| 1 | `validate --file <腳本>` | — | 格式與證據雜湊都對 |
| 2 | `build --file <腳本> --workdir <VIDEO_WORKDIR> --speech server [--captions karaoke]` | `<VIDEO_WORKDIR>/<slug>/<buildId>-<時間>/`：`script.json`、`evidence/`、`audio/000.wav…`、`timeline.json`、`timing.json`（卡拉 OK 時）、`captions/`（亮字層）、`checks.json`、`contact-sheet.png`、`upload/`（`final.mp4`、`zh-TW.srt`、`cover.png`、`titles.json`、`manifest.json`） | 每次都開一個新的成品目錄；後面的指令都用 `--dir` 指它 |
| 3 | `check-audio --dir <成品>` | `check.json`（綁音檔與逐句原文） | 0 句被標；被標就 `build --file <腳本> --redo <成品> …`，只重錄被標的句子，在新目錄再跑一次 |
| 4 | 查核：另一個代理在新對話對照證據，寫 `verify.json`；`qa --dir <成品> --verify <verify.json>` 會把它放進成品 | `verify.json`：`{ok, document_sha256, checked_by, claims: [{text, ok, note}], problems: []}`，`document_sha256` 是成品裡 `script.json` 的雜湊 | 每個數字與結論都有證據 |
| 5 | `qa --dir <成品>` | `qa.json`（12 項，綁所有輸入的雜湊） | 全過；沒過照下一節修 |
| 6 | `package --dir <成品>` | `upload/metadata.json`、`upload/description.zh-TW.txt`、`package.json`（4 項） | 全過 |
| 7 | `push --dir <成品>` | 站上的影片與審核 | 印出的 `waits` 是空的 |

`push` 先送成片審核（`format: "shorts"`、`shorts_line`、720p 預覽、封面、證據、`payload.qa`）；站上當場核准（Shorts 設定的「品管全過就核准」開著、12 項全過）就接著送上傳包審核；成片還在等站主時，站主核准後再跑一次 `push`。同一份成片重送是安全的：站上回它已經有的那一筆。

任何輸入改了（稿子、旁白、時間軸、字幕、證據、`verify.json`），都從受影響的那一步往下重跑：旁白改了先 `check-audio`，再 `qa` → `package` → `push`。不要只補雜湊、改 `ok` 或拿舊收據重包；`qa` 與 `push` 都會比對輸入快照，對不上就拒絕。

## 指令與結束碼

```bash
node tools/video/shorts/cli.mjs validate     --file <腳本> [--source-base <證據的根目錄>]
node tools/video/shorts/cli.mjs build        --file <腳本> --workdir <VIDEO_WORKDIR> [--speech server|windows|files] [--audio-dir <DIR>] [--channel msedge] [--redo <成品>] [--captions plain|karaoke]
node tools/video/shorts/cli.mjs check-audio  --dir <成品> [--threshold 0.5]
node tools/video/shorts/cli.mjs qa           --dir <成品> [--verify <verify.json>] [--offline]
node tools/video/shorts/cli.mjs package      --dir <成品>
node tools/video/shorts/cli.mjs push         --dir <成品>
node tools/video/shorts/cli.mjs import       --from <DIR> --workdir <VIDEO_WORKDIR>    # DIR 裡要有 final.mp4、zh-TW.srt、meta.json
node tools/video/shorts/cli.mjs from-episode --slug <長片> --workdir <VIDEO_WORKDIR> [--short 1|2] [--check]
node tools/video/shorts/cli.mjs from-drama   --slug <漫劇集> --from <秒> --to <秒> --workdir <VIDEO_WORKDIR> [--episode-workdir <DIR>] [--meta <JSON>] [--captions plain|karaoke]
node tools/video/shorts/cli.mjs tick         # 工人的敲門；手動跑等於讓站上現在做到期的事
node tools/video/shorts/cli.mjs track-init   --dir <DIR> --start YYYY-MM-DD   # 只剩離線用途
node tools/video/shorts/cli.mjs report       --dir <DIR>                     # 只剩離線用途
node tools/video/shorts/smoke.mjs [--workdir <DIR>]   # 不用站台的冒煙測試：替身旁白 → qa --offline → package
```

- `--speech`：`server` 是頻道聲音（經站上合成，聲音與長度範圍來自 Shorts 設定，逐句快取）；`windows` 是本機的 Hanhan，只有 Windows 有，而且**在 Windows 上沒寫 `--speech` 就是它**；`files` 從 `--audio-dir` 讀 `000.wav`、`001.wav`…。要上架的一律 `--speech server`。
- `--captions`：`karaoke` 讓字幕條隨旁白逐組亮字（`docs/videos/SHORTS.md` §工具端的 `karaoke.mjs`）；沒給就讀環境變數 `VIDEO_SHORTS_CAPTIONS`，再沒有就是 `plain`（舊的整句字幕條）。亮字的時間現在是從每句音檔的靜音邊界與字數估的，`timing.json` 寫 `source: "estimated"`，`qa` 的 `captions` 照樣過但帶一條警告；真實字時等 `speech/align`（票 `2026-10-05-speech-align-character-timing`）。
- `--source-base` 預設 `docs/videos/ai-shorts`；證據路徑相對於它。
- `qa --offline` 不連站台：要站台的項目（`policy`、`links`、`variety`，精華與漫劇的 `evidence`）一律記成沒查而不過，只拿來檢查本機能檢查的。
- 結束碼：0 成功；1 檢查沒過或其他錯誤（`check-audio` 有句子被標、`qa`／`package` 有項目沒過）；3 要站主（沒有或失效的權杖）；4 站台或服務連不上（重試四次後）。**`push` 只要沒出錯就回 0**，有沒有送出要看印出的 `final`、`publish` 與 `waits`。
- 中途停：在工作區或 `<VIDEO_WORKDIR>/<slug>/` 放 `STOP`；`build` 在付旁白錢之前與每段之間都會看。

## 三條內容線各自怎麼做

**實測（本機）**：照 `docs/videos/ai-shorts/campaign/README.md` 的題目規格，先把題目、輸入、先寫好的答案與評分方式存成證據檔並算雜湊（凍結），再讓受測模型在全新對話各跑一次，原始回答原樣存成證據，然後寫腳本、查核、照主幹做。腳本只能說證據裡有的事。

**實測（主機工人）**：工人照下一節「工人怎麼做」自己走完，產物在 `<VIDEO_WORKDIR>/_shorts/<slug>/`；本機不用插手，除非它卡住。

**長片精華**：

- 有 shot 的長片：長片撰稿時工人順手寫 `docs/videos/<slug>/shorts.json`（兩支，`slug` 是 `<長片>-short-1|2`）。`from-episode --slug <長片> --check` 先確認每張關鍵影格的雜湊；再 `from-episode --slug <長片> --workdir <VIDEO_WORKDIR>` 建兩個成品（旁白預設 `server`），之後每個成品照主幹 3–7。系列依長片決定（`sothatswhy` 或 `illustrated`），規格在 `docs/videos/so-thats-why/README.md` §Shorts。要在長片的工作檔被清掉（上架滿 7 天）之前做。
- 長片要已經公開，或成片已核准，`evidence` 才會過；長片還沒有 YouTube id 時說明欄缺完整影片連結，`metadata` 與 `links` 不過，等它上架再 `package`、`push`。
- 一支長片最多兩支精華，兩支講不同的事。

**漫劇直式短篇（後製，`from-drama`）**：不生圖、不重畫，從已核准的 16:9 成片直接裁 9:16（設計在 `docs/videos/SHORTS.md` §工具端的 `from-drama.mjs`）。

- 要有：該集工作目錄裡的 `final.mp4`、`timeline.json`、`captions/zh-TW.srt`，以及 `approvals.json` 裡對得上的 `final` 核准（`review-pull` 拉過，或本機 `approve --gate final`）；影片工具權杖；站上要有 `locate`（`GET /video/media/status` 列出 `limits.locate_labels`）。repo 裡有 `docs/videos/<集>/video.json` 時標題、說明、標籤與每鏡的角色名（locate 的標籤）都從它來，沒有就用 `--meta` 給 `{titles, description, ...}`。
- 選段：`--from`／`--to` 是該集的秒數，長度要在 Shorts 設定的範圍內，而且**不能切到句子一半**：切到了工具會拒絕並印出不切到的時間（`use --from 9.5 or --from 12.2`）。句子以 `captions/zh-TW.srt` 為準，所以先看字幕檔挑起訖。
- 做法：每個 shot 問一次 `locate`（有關鍵影格用關鍵影格，沒有就從成片抽鏡頭中段一格），視窗置中在主角的方框上、整鏡不動、換鏡前 15 格線性移到下一鏡；卡片場景置中。聲音剪該集的混音再正規化。字幕是 Shorts 的字幕層（`--captions karaoke` 逐組亮字，`plain` 整句），每句量過安全區；一句超過兩行 15 字會停下來說是哪一句，換一段或改那一句。
- 產物是一般的成品目錄（`<VIDEO_WORKDIR>/<集>-short-<起格>-<訖格>/<buildId>-<時間>/`），`checks.json` 多 `reframe`（每鏡的方框、視窗、移動與 locate 次數）；之後照主幹 3–7（`check-audio` → `qa` → `package` → `push`），`layout` 能過，`evidence` 要該集公開或成片已核准。不要用 `import` 再包一次。

**別的工具做好的成片（精華、漫劇直式短篇）**：`import --from <DIR>`。`meta.json` 是 `{slug, line, series, titles: [a, b], description, source, hashtags?, tags?, links?, synthetic_media?, headlines?}`；字幕當成旁白逐句切音，所以 `zh-TW.srt` 要一句一段、時間不重疊、不超過片長。成片要 30 fps、48 kHz、−14 LUFS，不是就先轉檔再匯入（`ffmpeg -vf fps=30`）。匯入的成品照主幹 3–7；`layout` 永遠不過（量不到字卡位置），由站主在 Shorts 分頁開安全區疊圖看一次再核准。

## 自動品管 12 項：沒過時怎麼修

`qa` 的項目依序如下，伺服器要每一項都在、都過，`final_sha256` 等於這份成片，才算過。

| 項目 | 檢查 | 沒過時 |
| --- | --- | --- |
| `profile` | 1080×1920、30 fps、H.264／AAC 48 kHz、長度在設定範圍、格數等於時間軸（用 ffprobe 重量） | 長度：改稿重 `build`；匯入的成片先轉成 30 fps |
| `loudness` | −14 ± 1 LUFS、真峰值 ≤ −0.8 dBTP | `build` 做兩段式正規化，自己做的成片不會錯；匯入的先正規化再匯入 |
| `layout` | 每張字卡與字幕都量過、在安全區內（內容 x 78–902、下緣 1380 以內，字幕條下緣 1600 以內），素材有載入 | 縮短那張字卡的字或拿掉素材，重 `build`；匯入的交站主看 |
| `narration` | `check.json` 綁的是這些音檔與這些句子，0 句被標 | `build --redo <成品>` 重錄被標的句子再 `check-audio`；還是被標就改寫那一句（意思與數字不變）再 `build` |
| `evidence` | 實測：每個證據檔的雜湊都對。精華與漫劇：來源影片在站上、沒放棄、已公開或成片已核准 | 證據不能重寫：要改就開新條件、新檔案、重新綁定。來源還沒好就等 |
| `facts` | `verify.json` 是這份 `script.json` 的查核、每個主張都 `ok` | 照查核意見改稿，重 `build`，再請新對話查一次 |
| `policy` | Jev 照頻道立場判（`POST /video/automation/judge/policy`）；精華不問「觀眾能照著做的東西」 | 立場空白時永遠不過，交站主寫立場；其餘改內容 |
| `metadata` | 標題 ≤ 100 字元、沒有角括號、兩個標題；說明 ≤ 5,000 位元組；標籤合計 ≤ 500 字元；話題標籤 ≤ 3；精華要有完整影片網址 | 改腳本的欄位重 `build`；精華等長片上架 |
| `captions` | `zh-TW.srt` 每段跟時間軸一致；設定勾的語系也都在。卡拉 OK 字幕的時間是估算的（`checks.json.captions.source: "estimated"`）時仍過，只帶警告 | 重 `build`，不要手改 srt；警告不用修，等對齊票 |
| `links` | 說明欄每個網址回 200（`Mokaair-editorial` User-Agent） | 改 `links` 或說明 |
| `variety` | 開場那一句不跟最近 30 支一樣；字卡結構不跟同系列前一支一模一樣 | 改第一句，或調整場景（句數、`big`、`body`、`asset`、`camera`） |
| `disclosure` | 記下要不要勾「變造或合成內容」與原因；不會讓品管失敗 | — |

連不上的服務（Jev、轉寫、抓網址、站台）一律算沒過，不會因為判斷不了就核准。修不好的交站主：`push` 照樣送，成片審核停在 `/admin/videos` 等站主核准、退回或放棄，這一支不會擋住月曆（時段改用片庫的下一支）。

## 實測的規範

1. **凍結題目**：題目規格、輸入、先寫好的答案、評分方式在跑任何一次之前寫成一個檔案、記雜湊；之後每一步都核對，檔案變了這支就作廢（工人的 `protocol.json` 變了會卡住）。
2. **各跑一次**：每個條件在全新的對話送一次。技術失敗可以再送一次，兩次的紀錄都留；模型答錯不是失敗，是結果，不能重問到對。
3. **照實寫**：數字與時間用程式對答案，其餘才交查核模型判；撰稿只看規格、證據與分數；平手就說平手。受測模型的名稱只寫伺服器回報的，沒有就寫「未回傳」。
4. 不做假的操作畫面；沒有素材或工具的題目跳過，用已備料的題目遞補。

## 工人怎麼做（主機）

每一輪 `auto`：片庫少於 `stock_days` 天的量時 Shorts 排在漫劇與教學之前，否則排在之後；Shorts 只看自己的開關，教學的自動草稿關著也照做（`tools/video/automation/cli.mjs`）。一輪問一次 `GET /video/automation/shorts/next`，依序可能拿到：

- `report`：上週的每週報告。企劃模型只寫判斷（`prompts/shorts-report.md`），報告最後的原值表由程式照抄伺服器的數字；寫了不在表裡的數字或「中位數」「排名」這類自算指標會被退回。
- `plan`：週一或片庫不夠時，把題目排進到下週日的空時段（`prompts/shorts-plan.md`）。工人只留下自己做得了的實測題，排不了的寫進 `<VIDEO_WORKDIR>/_shorts/plans/<日期>.json`。
- `brief`：題庫不夠兩週的配額或站主丟了想法時補題（`prompts/shorts-brief.md`），工人只寫實測題。
- `make`：最早一格還沒做的題目，做一支實測（`tools/video/shorts/lab.mjs`），步驟是 `freeze` → `subject-a` → `subject-b` → `score` → `write` → `verify` → `build` → `audio` → `qa` → `package` → `push`（提示詞 `prompts/shorts-lab.md`；撰稿的答案先過不碰模型的 lint，數字不在證據裡就當場退回重寫）。

自動修（每種最多 2 輪）：`facts`、`layout`、`metadata`、長度交回撰稿；`narration` 第一輪重錄被標的句子、第二輪交撰稿改寫。`build` 做不出來的長度或版面修 2 輪仍不行，這支卡住；`qa` 修完仍有項目沒過就照樣 `push`，成片停在站主那裡（`awaiting`），站主核准後下一輪工人自己送上傳包。同一步連續兩次交不出能用的答案，這支標成卡住，原因寫在 `/admin/videos`；`shorts/next` 會跳過卡住的那支、照常開下一格，站主在影片頁按重試後工人從卡住的那一步接著做。

工作區：`<VIDEO_WORKDIR>/_shorts/<slug>/lab.json`（做到哪一步）、`lab/`（`protocol.json`、`subject-a.json`、`subject-b.json`、`scores.json`、`script.json`、`verify.json`）、每次 `build` 一個成品目錄、`answers/`（不能用的模型回答原文）；`_shorts/shorts-state.json` 記 plan、brief、report 的失敗次數。`_` 開頭的資料夾清理工作區時不動。

## 坑

- **在 Windows 忘了 `--speech server`**：會用 Hanhan 做出不能上架的版本。試片用 Hanhan 的那一版不上架。
- **`push` 回 0 不代表送出**：看 `waits`。`video_shorts_final_review_stale`：工具舊了，更新後重新 `push`。`video_shorts_review_upload_started`：影片已經開始上 YouTube，先到後台與 Studio 核對，不要清掉上傳紀錄。
- **改了說明也要重跑**：`package` 的產物不在 QA 輸入裡，但腳本改了 QA 與查核都失效，要從 `build` 重來。
- **匯入的成片**：24 fps 的會被拒絕（要先轉 30 fps）；`layout` 一定要站主看；沒跑 `check-audio` 的 `narration` 一定不過。
- **卡拉 OK 字幕的亮字會偏**：時間是估的，句子裡有長停頓或拉丁字（`spokenUnits` 把一個拉丁字算兩個單位）時亮得早或晚；工人做的 Shorts 在站上會自動核准，所以預設是 `plain`，站主看過一支 `--captions karaoke` 的樣片再在工人主機設 `VIDEO_SHORTS_CAPTIONS=karaoke`。每次 `build` 都是新目錄（`codeHash`、`MOTION_VERSION` 變了），舊成品要重跑 `check-audio` 與 `qa`；已核准的成片綁 `final_sha256`，不受影響。
- **`from-drama` 的視窗一鏡只看一張圖**：主角在一個鏡頭裡走位，視窗不會跟；方框是 Gemini 答的，第一支先把 `checks.json.reframe.shots` 的方框對著關鍵影格看一次。成片是 608 px 寬的視窗放大 1.78 倍，畫質比原生 9:16 軟；長句（超過兩行 15 字）放不進字幕條，工具會停下來說是哪一句。locate 每鏡 US$0.01，記在站上 judge 的額度，`usage.json` 不報。
- **工人讀不到 `docs/videos/ai-shorts`**：它的 docs volume 比 repo 舊，題目、規格與脈絡一律由 `shorts/next` 給；不要寫依賴那個資料夾的步驟。
- **Jev 的每日次數**跟自動新聞、景點介紹共用；大批 `check-audio` 前先看「AI 供應商與金鑰」卡片。
- **中文參數**：PowerShell 會弄壞命令列上的非 ASCII 字，腳本與 `meta.json` 一律寫檔再傳路徑。
- **本機的 `track-init`、`report`**：排程、成效、花費的正本在後台的 Shorts 分頁；這兩個指令只剩站主用 Studio 匯出檔離線算 #871 的算式時用（`docs/videos/ai-shorts/README.md`）。
