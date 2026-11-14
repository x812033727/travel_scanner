# 旁白解說系列的共用區：奇聞檔案局與原來如此事務所

兩個系列都是「插圖＋旁白」的長片，用同一套工具（`tools/video`）、同一條關卡（大綱 → 稿子 → 聲音 → 設定圖 →
分鏡 → 成片 → 上架 → 語言）。這份把兩邊各自學到、卻沒有寫在同一處的做法統一起來。站主 2026-11-08：「我想要統一
備份的跟共同規則還有一些事情，奇聞跟原來如此」。

| 檔案 | 內容 |
| --- | --- |
| [`../AI-DRAMA-DRIVE.md`](../AI-DRAMA-DRIVE.md) | **備份（2026-11-10 起）**：所有檔案傳到雲端硬碟 `AI劇/<名稱>/<代碼>/製作檔/`，不再推分支 |
| [`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md) | 已停用的備份分支規則（要備份什麼的清單仍適用） |
| [`backup/`](backup/) | 備份工具（推分支、核對、涵蓋檢查） |

系列自己的規則：
- 奇聞檔案局：skill [`curio-episode`](../../../.agents/skills/curio-episode/SKILL.md)、
  重做的規則與交接在分支 `claude/eloquent-hypatia-fxsz7j` 的 `docs/videos/curio-redo-handoff/`（`RULES.md`、`HANDOFF.md`）。
- 原來如此事務所：[`../so-thats-why/dialogue-pilot-20261103/README.md`](../so-thats-why/dialogue-pilot-20261103/README.md)
  第 9、10 節與同資料夾的 `HANDOFF.md`。

AI 劇（種田、祖媽）的同類文件在 [`../drama/`](../drama/)（PR #2047）。分支命名與核對方式跟它一致，
這樣三種片的備份可以用同一套工具還原。

## 兩個系列統一的做法

兩邊做法不同的地方統一如下（站主 2026-11-08 確認，見最後一節）。系列文件跟這裡衝突時以這裡為準。

| 項目 | 奇聞原本 | 原來如此原本 | 統一後 |
| --- | --- | --- | --- |
| 什麼時候備份 | 站主確認整支完成後一次推完 | 每過一關推一次 | 每過一關（分鏡、成片、上架、語言）推一次；之後才產生的檔案（八語縮圖、重錄、站上抓回的）補進同一條分支 |
| 備份放哪 | 跟稿子混在工作分支的 `docs/videos/<slug>/media/` | 專用分支 `claude/backup-<slug>` | 專用分支 `transfer/<slug>`，跨集共用放 `transfer/<系列>-shared`（[`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md)） |
| 備份範圍 | 列舉：逐句錄音、插圖與 manifest、配音、字幕、時間軸、核准紀錄、縮圖、成片 | 整個工作目錄（只排除 `LEASE*`）放 `workdir/`，`upload/` 以外的額外檔案用 `src:dest` 指定，分支根目錄 `README.md` 每次備份記一行 | 重製時什麼都不用重做（站主 2026-11-08）：整個工作目錄不挑檔，加 `upload/`、站上抓回的檔案、實際用的那份 checkout 裡的稿子（含未提交的修改）、scratchpad 的腳本與紀錄；繁中加八語的縮圖、語音、字幕、敘述逐格核對 |
| 分批推送 | — | 每批 ≤ 900 MB 推一次，`MANIFEST`／`README` 放最後一批（P23 一次 3.96 GiB 被拒） | GitHub 單次推送上限 2 GiB：`tobranch.sh` 每約 1.5 GB 一個 commit 推；`LEASE*`（鎖檔紀錄，重製用不到）不放 |
| 大檔切塊 | 約 90 MB 一段，附 sha256 | `backup.py` 把超過 90 MB 的檔切成 90 MiB `<name>.partNN`，大小、sha256、塊數記在分支根目錄 `MANIFEST.tsv`，推完從遠端抓回重算 | 超過 95 MB 的檔切 90 MiB `.partNN`，旁邊放 `.SPLIT`（sha256、大小、還原指令），跟 #2047 相同；原來如此下一次備份起照這個格式（PR #2048 討論） |
| 刪工作目錄的條件 | 站主確認完成、語言關卡已送審、逐檔核對 | 逐檔核對雜湊後才刪 | 三件都要：站主確認這支完成（三個後台關卡都決定了）、逐檔核對 0 不符、**另一個沒參與製作的代理**到 GitHub 核對涵蓋 0 漏 |
| 插圖放大檢查 | 獨立代理把每張切四格 2 倍看字、臉、人、Ada 一致 | 獨立代理逐張放大看眼睛 | 兩邊合併：每張全圖＋四格 2 倍，看字、記號、貓、無人景的臉與人、角色一致（含眼睛、五指）、暖深褐收尖細線與厚塗水粉質感、四邊最外層像素零白邊、地圖／地球儀方位與時代道具考證、圖文矛盾；檢查的代理沒畫過這些圖 |
| 生圖工具與畫風（2026-11-14 定案） | 早期走 MiniMax `image-01` 平塗卡通 | 同左 | **兩個系列全面停用 MiniMax 生圖**：關鍵影格一律由代理內建 `generate_image`（`AspectRatio: "16:9"`）套用**「劇場級動畫光影 × 厚塗水粉質感」**英文基底句生成，再用 `keyframes import --provider external --usd 0` 匯入；遇到 `gemini-3.1-flash-image` 配額冷卻時先跑翻譯與八語配音，絕不退回 MiniMax。`video.json` 頂層仍保留 `look: { "preset": "cute-mystery" }`（奇聞）／`"cute-cartoon"`（原來如此）供系列身分與 lint 檢查 |
| 角色設定圖鎖定（2026-11-14 定案） | 串場 Ada 固定一張；單集歷史人物未建卡易每鏡換臉換衣 | `chief`／`kid` 系列設定圖 | 凡有角色出場，`ImagePaths` **必傳**角色設定圖（原來如此傳 `characters/chief/*.png`／`characters/kid/*.png`；奇聞除串場研究員外，單集內跨 ≥ 4 鏡出場的可入畫歷史人物也必須先產固定設定圖鎖死髮色、髮型與主色服裝）；重繪既有鏡頭時一併傳入前一版圖檔鎖定骨架與道具位置 |
| 評審被推翻時 | W03：重畫、改提示詞，三次不過換成物件畫面 | 不准用 `--accept-best`；三個 take 都不過的鏡頭由沒畫過圖的代理放大逐張挑，挑中的用 `repin.py` 固定成 `accepted_with_problems`；每次重跑 `keyframes` 都用累積的 `pins.json` 再固定一次 | 2026-11-14 起全面走內建 `generate_image`＋獨立子代理四格 2 倍放大審查後 `keyframes import --provider external --usd 0` 匯入；放大審查抓到破綻就以 `ImagePaths` 帶原構圖重繪修正，**任何一次改動 `video.json` 後都要確認外部匯入清單未失效** |
| 縮圖 | `thumbnail.data.layout: "e"`＋`focus`（左字右圖，#2044、#2045、#2046） | `thumbnail.data.subject: "right"`（插圖縮到右側 38%）；P15 在畫完圖後改縮圖，整份 manifest 失效要重跑＋repin＋重核分鏡 | 各用自己系列的版型，規則統一：**主體不被字擋**、**大字與副標嚴禁直接破梗因果答案**（只寫反常識衝突或硬數字）、**右圖必有誇張清楚表情或強烈視覺反差**（禁止選闔上的空白書本、空房間、單一靜態死物）、**縮圖的圖、文字、`subject` 在畫關鍵影格之前定好**（只有奇聞的 `layout: "e"`、`focus`、`brand` 事後可改，#2046）；八語縮圖逐張看過才打包 |
| 八語縮圖 | 做上架包時看 | `i18n-merge` 後一定跑 `render --thumbnails-only` | `i18n-merge` 後一定 `render --thumbnails-only`，八張逐張看過才 `package` |
| 八語標題後綴 | 偶爾漏翻系列名 | 同左 | `i18n/<locale>.json` 的外語標題一律保留 [`../packaging-refresh-20261111/README.md`](../packaging-refresh-20261111/README.md) §譯名的定版系列後綴（`…｜Curio Archive`、`…｜So That's Why` 等）；字幕尾巴由工具補 |
| 語速、停頓與分鏡（對話做片） | S42 漏寫 `pauses`／`still_motion`、92 句拆 73 景 | P23 50 景單句、語速 3.8 字／秒 | 中文（`zh-TW`）固定用 Gemini（奇聞 `Sulafat`；原來如此 `Sulafat`＋`Leda`），八語配音（`en,ja,ko,es,pt,id,vi,th`）固定用 MiniMax（`dub --provider minimax`）。對話做片不經主機 `settle()`，`video.json` **必明寫** `"pauses": {"line_ms": 0, "scene_ms": 150}`、`"still_motion": "beat"`；`voice.style` 寫「一秒五個字以上，句與句緊接、不拖長尾音」，實測語速 **≥ 4.4 字／秒**（不足時加 `voice.tempo` 微加速）；同角色同節拍 **2–3 句併進同一個 `scene.lines[]`**，禁止全集一句一景 |
| 說明欄、清單與置頂留言 | 查核算式與「不畫誰的臉」寫進說明欄 | 縮圖與說明欄先講完答案 | 說明欄前兩行鉤子＋受眾不破梗；內部查核算式與入畫限制留 `claims.md`，禁止塞進 `youtube.description`；最末由工具自動附 `#奇聞檔案局`／`#原來如此事務所`（`metadata.mjs` 保留 `\p{M}` 泰語／印地語組合母音，且泰文等 3-byte 語系組完說明欄應壓在 `< 4,500` UTF-8 bytes，避免逼近 5,000 bytes 硬上限）；交付必附**低門檻二選一置頂留言草稿**與加入系列播放清單提醒 |
| 第一次品管前 | — | 先 `review-push --report-only`（否則「有示範」被當教學片） | 兩邊都照做 |
| 上架包自檢 | 用 `package/check.mjs` 的 `readPackageReport(workdir)`，不直接呼叫 `checkPackage` | — | 兩邊都照做 |
| 配音片頭片尾 | 讓 `dub` 工具自己加；各語字幕跟著片頭往後移 | 時間軸一動就 `dub` 八語重跑（沿用快取） | 兩條都照做 |
| 送審後核對 | `review-files --dry-run` 逐個比對 `dub_*`、`thumbnail_*`、`captions_*` 的 sha | `review-files --dry-run --gate languages` 確認 8 配音、8 縮圖、8 字幕都在 | 兩條都照做 |
| 送審順序 | — | 成片 → 上架等站主核准 → 才送語言包 | 兩邊都照做；而且送審要接在備份成功之後：`backup && review-push`，**不能用 `;`**（P23 備份失敗時用 `;` 照樣送上後台） |
| 英文名稱 | 照原文念（站主 2026-11-05） | 照原文念，不寫中文音譯的 `say`（`dialogue-pilot-20261103/README.md`，借自 #2027） | 寫英文、念英文，不硬翻成中文音譯；只有台灣慣用的正式中文名例外（站主 2026-11-08「如果是英文就用英文不要硬翻譯 不然會怪怪的」）；新詞進 `lexicon.json` |
| 回報語言 | 繁體中文 | 繁體中文 | 繁體中文 |

## 兩邊都踩過、都要防的坑

- **`keyframes --shot … --force` 會把整份 `keyframes/manifest.json` 換成只剩那幾景**（奇聞 H24，2026-11-08）。
  只重畫幾景：改提示詞後跑不帶 `--force` 的 `keyframes --shot`；原來如此的 `repin.py` 也會被 `--shot` 丟掉，最後要再固定一次。
- **評審每次判法不同**：重建清單會讓已核准、已放大檢查過的圖被判不過（H24 重建時 25 景）。用
  `keyframes import --provider external --note …` 放回驗證過的那張；之後只要改了任何提示詞，import 的圖都會被丟掉，
  所以**先改完提示詞，最後才 import**。
- **兩支同時畫圖會撞到網站每小時上限**（每個權杖每小時 240 張圖、360 次評審）：一次只讓一支畫圖，另一支做旁白或組裝。
- **背景工作會被收掉**：容器重開或閒置都會。用 `nohup setsid` 跑，回來先 `pgrep`；畫圖可以中斷後重跑，已畫的吃快取。
- **已有核准成片的 slug 不能直接送新成片**：站上那支如果做過換版（例如換 CC 片頭），新成片只能由站主在後台「成片換版」送，
  工具先用 `tools/video/review/renewal.mjs stage` 產生收據（[`../BRANDING.md`](../BRANDING.md)〈已核准、尚未上傳的長片換版〉）。
  已上 YouTube 的不能換版，要開新 slug。
- **改了 `thumbnail` 會讓分鏡核准失效**：只有 `layout: "e"`、`focus`、`brand` 不算進畫面雜湊（#2046）。換縮圖的標題文字要在分鏡送審前定好。
- **`check-audio` 的轉寫會聽錯專有名詞**（「山葉」聽成「商業」）：重錄兩次還被標，量音長（字數 ÷ 秒數）確認沒有漏字，
  列給站主親耳聽；能用時加 Whisper 第二個轉寫（`automated.md`）。
- **配樂太短**：`music` 回來比片短時用 `music --loop`，不另買。
- **改成物件鏡頭要一起拿掉舊的 FIX 文字**：有人或小孩的鏡頭改成 `scene()` 物件鏡頭時，舊的 FIX／重寫字串還在，
  模型會把人畫回去（原來如此 P23）。
- **提示詞超出預算的鏡頭不會畫**：原來如此小孩鏡頭約 840 字上限（含 KIDDESC＋KIDFIX）。畫圖前先 `keyframes --dry-run`
  看每鏡的 `prompt budget: X of Y`。
- **備份會把整集再存一份到本機 `.git`**：舊版推分支的寫法每推一次就留一份物件，推了幾輪 H24、B01 後 `.git` 長到 12 GB、容器額度用完，連配音都寫不進去（奇聞 2026-11-08）。[`backup/`](backup/) 現在用暫存物件目錄，推完就刪；已經堆起來的用 `git update-ref -d refs/remotes/origin/transfer/…` 再 `git prune --expire=now` 清掉（分支已在 GitHub、核對過才清）。
- **一次推送超過 2 GiB 會被 GitHub 拒絕**：一集工作目錄常超過（P23 3.96 GiB），所以分批推（[`backup/`](backup/)）。

## 不統一、各系列自己定的

- **誰核准稿子、聲音、設定圖、分鏡**（站主 2026-11-08「分開」）：奇聞照原本，站主在 /admin/videos 逐關按
  （大綱、設定圖兩關另有站主原話的固定 note，見 skill）；原來如此照原本，獨立代理查核、盲評、評分後 Claude
  `approve --note`。成片、上架、語言三關兩邊都由站主在後台決定。
- 角色：奇聞只有不說話的研究員 Ada（設定圖固定用 `curio-redo-handoff/ada-sheet/`）；原來如此有所長與小問兩個說話的角色。
- 結構：奇聞照黑貓研究院十步；原來如此是問答對話。
- 入畫規則：奇聞在世或 1956 年後過世的人不入畫、用物件代稱；原來如此照它自己的規則。
- 配樂：奇聞每集 `music` 生成（太短就循環）；原來如此用系列配樂床：P15 起是 `sothatswhy-bed-r2.m4a`（用 P02 的付費原檔重做，sha256 `9bb4ba6f…`），更早的集數用 `sothatswhy-p02-bed.m4a`。
- 縮圖版型與字數上限（見上表）。

## 站主已決定（2026-11-08）

1. 奇聞的稿子、聲音、設定圖、分鏡四關要不要改成「獨立代理把關後 Claude 核准」→「分開」：兩個系列各照原本，
   不統一（見上一節）。
2. 備份分支改用 `transfer/<slug>`、`transfer/<系列>-shared` →「可以」。已有的 `claude/backup-sothatswhy-*`、
   奇聞 W03 在 `claude/eloquent-hypatia-fxsz7j` 的 `media/` 保留不動，從下一次備份起用新名字。
3. 刪工作目錄前多一道「另一個代理核對涵蓋」→「好」。
