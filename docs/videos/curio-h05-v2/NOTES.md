# H05 v2｜離線製作交接
**2026-10-14 三鏡小樣最新：** 正式 `timeline.json` SHA-256 `db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee` 已在 `approvals.json` 及 `status` 讀回音訊核准；下段「待站主核准」是送出時快照。站主限額授權 `open-threat`、`open-tail`、`open-boy` 各一張 MiniMax 圖與一次判圖，已恰好完成 3 張＋3 次、增加 US$0.0405、帳本總計 US$0.1755。`open-threat` 判圖 PASS 但人工退件，`open-tail` 判圖 FAIL 且人工退件，`open-boy` 判圖 10 分但人工與主製作代理獨立目視均退件（腳下無來源橘紅斑塊）；完整原圖、裁圖、判圖、請求 key、封存與費用見 [visual-pilot-05-20261014.md](visual-pilot-05-20261014.md)。**沒有可核准的連續三鏡，停止付費擴批。**

**2026-10-14 現行關卡：**`open-note` 原生圖卡已保留；敘事盲審先在 `payoffs` 指出 h5v029、h5v103 未點名回扣，兩句窄修後換一名獨立讀者重審，**11/11 通過**（narrative hash `31f279e4aaa020c5`）。正式 `video.json` SHA-256 `472db853bc021374430ce5d80387442544cf72cd195f10e9e06aa86b07c94095`、`timeline.json` SHA-256 `db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee`；只重錄兩句、53 計費字元，100 段沿用，108/108 句檢查中兩句新錄音逐字對上，原 12 句標記不變。正文 540.133 秒；61 個 `shot` 佔 58.5658%，最長狀態 7.833 秒，節奏問題 0。**新版音訊已送後台待站主核准，尚未讀回核准。**細節與舊版界線見 [敘事回扣與正式語音](narrative-payoff-repair-20261014.md)。下方把舊版稱為「現行」的段落，均是當時快照。

**2026-10-14 最新候選：** 人工退件的 MiniMax `open-note` 已改為有 `c04` 來源依據、標示非當年原件的原生 SVG 示意卡。`video.json` SHA-256 `c14695ef580539006621e24e1f3f25e0d9ffcb2ba399eea9fdd7d69aa2edbd1f`，narrative hash `e900e3c896cee888`，speech hash 仍為 `7d8cb6cb30ba87d9`。用 108 句原 WAV 樣本的隔離 dry-run 證明 16,073 格總長、全部逐句與場景時窗不變；插圖占比 58.74%、節奏 0 問題。隔離圖卡人工實看清楚，但尚待獨立審查；正式時間軸與後台音訊核准仍綁舊版，不能把下文舊版 `[x]` 當作新版通關。新圖、雜湊、字幕重算與餘下關卡見 [open-note-diagram-revision-20261014.md](open-note-diagram-revision-20261014.md)。下方舊 SHA 與已核准狀態依時間保留作**改卡前的歷史快照**。

## 目前狀態

**改卡前畫面更新：** 三輪各三張 MiniMax 開場圖均不可用；第三輪三張 judge **全 FAIL**（9.00／9.00／9.71），人工實看有假字、額外人物／道具及擬真風格漂移，原 manifest SHA-256 `6b4046143e1cb552d00039c4c1a45f13818ac8ffd9bc2cfdd0108b32963dcedf5`、圖與帳本已封存，停止同一路線盲抽。主稿已採用「原生場域卡 → FBI 機票原件照片 → 305 號航班原生卡」前三景。片尾同一 `outro` 場景現以三項逐句揭示，原 8.2 秒單畫面已消除：實際時間軸 `cadenceProblems=[]`，最長畫面 7.3 秒、插圖占比 59.45%。開場 15.2 秒及片尾 8.17 秒離線預覽、畫面與來源 SHA、音訊綁定、50% 規則限制見 [visual-pilot-03.md](visual-pilot-03.md)；第二輪原始紀錄見 [visual-pilot-02.md](visual-pilot-02.md)。

繁中 CC 的正文時間預檢及現行 46 張原生卡／來源照片狀態的隔離渲染、雜湊與尚待實看的 CC 安全區關卡見 [offline-media-preflight-20261014.md](offline-media-preflight-20261014.md)。預檢字幕尚未納入品牌片段，也不是正式可上傳 CC。其後唯一 `open-note` MiniMax 小樣雖獲自動 PASS，人工實看退件，費用與原件封存見 [visual-pilot-04.md](visual-pilot-04.md)；不擴批。

本資料夾是 `curio-h05-v2` 的新候選腳本，與 `curio-h05` 舊企劃、核准及外部工作目錄分開。2026-10-14 已產出 `brief.md`、`claims.md`、`video.json`、`script.md`。現行 `video.json` SHA-256 為 `74102087ca465c7c73044e1182671641965cc19cbd6f4d0470d11fcb9c16e6e3`；`lint` 為 **0 errors、0 warnings**，93 景、108 句、六章，靜態估算正文 **8.745 分鐘**。現行敘事 hash `65c64491d8a53b77` 的獨立 11 題盲評已記錄 **11/11 PASS**，`status` 讀回 `storytelling panel: passed`；先前 `e0d2eb7016aea429` 的通過紀錄只屬舊版。現行實際旁白時間軸 **535.767 秒（8:55.8）**，語音 hash `7d8cb6cb30ba87d9`，`narration.wav` SHA-256 `8b519d908e7b85d7d214288d3bf8c7ebb5bc897456a4b32c74143cff50253ba3`。三個片尾揭示狀態曾使核准失效；站主其後於後台核准新 `timeline.json` SHA-256 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984`，`approvals.json` 與目前 `status` 均讀回 `[x] narration approved`。108 句原 WAV 與逐句時間未因揭示狀態改變；12 句標記是站主聽審核准的內容。

第一輪 hash `4f7298fac213e1c5` 的獨立盲評未通過：開場過早透露鈔票、兩處章節銜接重複或跳躍、開場提問未點名回收、兩組數字重複，以及結尾章名像功能標籤。第二輪 hash `ba9dce2d2f788f99` 仍未通過章節銜接及重複事實。後續窄修加入 FBI 案件史與 2020 年原論文可追溯的事件細節，再依獨立盲評消除乘客下機、降落傘數量及落點限制的重述；`3be74c4b985cd1a7` 已通過 11 題。每輪結論只適用其各自雜湊。

`source-v1.json` 與 `source-claims-v1.md` 為 2026-10-13 舊稿的唯讀快照，`research-*.md` 為舊稿查核材料的完整複本；`asset-register.md` 已更新為 v2 的實際複製與驗雜湊紀錄。新稿已固化於 `video.json` 與 `script.md`，暫時組稿程式已移除。這些來源快照只是可追溯材料，不能當成新稿的核准。

獨立事實查核 `verify-1.md` 的原始 35 組事實主張為 33 confirmed、2 changed、0 not found；後續窄修有改稿者增量來源核對與本輪獨立來源抽查，並非把舊逐欄清單冒稱為現行稿的全量重審。大綱、現行敘事與音訊關卡均已通過；`tts` 曾從既有音檔快取重建 v2 `timeline.json`，**0 次合成、0 計費字元**。先前 speech/transcribe POST 結果不明的持有狀態（請求 SHA-256 前綴 `903424`）已保留原始收據；查不到供應商逐次計費結果，當時經站主授權只重試一次。新時間軸另獲站主核准，不沿用舊檔雜湊的核准。原件照複製及驗 SHA 已完成；三輪各三張 MiniMax 開場小樣均不能作為可用圖組，現有三景混合畫面已進主稿並有離線預覽。尚無核准的完整圖組、成片、字幕或上傳包；播放與站主驗收也未完成。舊稿音訊、視覺、核准以及 `say_for` 雜湊不得直接移轉到新 slug。

**2026-10-14 大綱快照補註：** [brief.md](brief.md) 第 33 行「不是大綱關卡核准」及第 72 行「聲音仍待製作」描述的是送審前的候選稿狀態。現行 `approvals.json` 已將選項 A 的大綱核准綁到該 brief 的 SHA-256 `4d83268083771b7ad744e4130c31bb9587f0e2bc5c7a3337adbec91675fbdda7`；後續 TTS、轉錄恢復、複查和音訊核准見下方最新狀態。三張 FBI 原件照已在 v2 外部工作目錄驗雜湊；原定 65 張 MiniMax 插圖中，三輪各三張開場小樣已生成但均不可採用。為保留大綱核准雜湊，本輪不改送審時的 brief 原文；後續狀態以本筆與新關卡收據為準。

## 來源核對與界線

- 2026-10-14 重新讀取 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)：1971-11-24 現金單程票、305 班機、紙條聲稱炸彈、20 萬美元與四具降落傘、36 名乘客在西雅圖獲釋、晚上八點多跳離飛機、五週年時考慮逾 800 人與多數排除、1980 年找回 5,800 美元並以序號相符、D.B. 為後來媒體稱呼。頁面 2016 更新欄說資源轉移。
- 2026-10-14 重新查詢 [Kaye、Meltzer 2020 原論文](https://www.nature.com/articles/s41598-020-70015-z) 可擷取的摘要、方法與結論文字，包括單張原鈔、11 月 13 日及 3 月 1 日的現代對照、埋沙後灌入含藻水的紙邊滲入結果；寫稿時出版社原站直接開啟曾跳轉登入，獨立覆核者同日成功讀到完整正文。作者以矽藻組合推論較符合五月至六月的浸水，未推出年份、抵岸日、搬運路線或人的身分。論文摘要將尋回金額約寫 6,000 美元，影片的 5,800 美元採 FBI 的精確金額。
- 2026-10-14 重新取得 [FBI 2016 年聲明](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) 的全文文字：資源調整與公告日期、民眾逸聞未達證明門檻、特定贖金或降落傘實物仍可送交 FBI。機票物件頁本輪仍只取得搜尋摘錄，另沿用 2026-10-12 `research-history.md` 的親讀紀錄。新稿未加入未查核的嫌疑人傳聞。
- 本稿不從「沒有找到人」推到生還或死亡；不把 2020 年單張鈔票研究推及全部 20 萬美元；不把約 30 公里說成漂流距離；不把 2016 年資源轉移說成已定案。

## 外部照片與發音交接

`video.json.assets[]` 保留機票、贖金、領帶三張檔案照的來源、權利、尺寸和 SHA。2026-10-14 已從 `<home>/mokaair-work/videos/curio-h05/stock/` 複製到 `<home>/mokaair-work/videos/curio-h05-v2/stock/`，來源和目的地三檔 SHA 均與 `asset-register.md` 相符，舊檔未覆寫。隔離候選中機票照片框、caption 與 credit 已渲染並人工看過；啟用 CC 時下緣 caption 是否被播放器遮住、其他兩張物證正式照片框仍待核對。其餘情境圖尚未產生。

舊工作樹 `a18a` 的來源快照包含三組後補發音選擇：`丹庫柏` 唸 `丹庫博`、`迪比庫柏` 唸 `D B 庫博`、`矽藻` 唸 `細藻`（矽藻出現兩句）。新腳本改了句子，故沒有複用舊 `say_for`。本輪以新句文字 hash 為 `h5v085`、`h5v088` 設定 `say_for` 並重錄；顯微鏡句複查解除標記，河岸男孩句仍被 ASR 標記，後已連同其他標記交站主聽審並獲核准。其餘人名與術語維持既有發音選擇，不因 ASR 同音字直接重錄。

## 已重綁關卡與下次製作

1. 現行 `65c64491d8a53b77` 的獨立敘事盲評已通過 11/11；保留舊 `e0d2eb7016aea429` 的通過與來源抽查作歷史證據。若新增主張需重新綁來源。
2. 片尾三狀態曾改變 `timeline.json` SHA；站主已在後台核准新時間軸 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984`，本機 `status` 讀回 `[x] narration approved`。原 WAV 及每句時間未改，無需付費重錄。
3. 停止同一 MiniMax 提示分支重抽。檢視 `visual-pilot-03.md` 的開場與片尾局部預覽，尤其 FBI 機票照片的 CC 安全區和片尾逐句增項。全片來源照片／圖表與 AI 空景分工仍須先處理 `shot` 50% 覆蓋，再擴批。另按現行品牌規格核對 `_branding/current.json`，片頭接在濃縮章後、片尾接新的品牌結束畫面。新 MP4 須重新跑字幕、配音選擇、上傳包與最終 QA；站主仍須實際播放與決定上傳。

## 音訊恢復收據（2026-10-14）

原 speech/transcribe POST 504 的請求 SHA-256 `903424892690e20f777383999651b83f9e49a424281ab7268d29ffbdc51930dc`；原始 held JSON 已複製並驗 SHA，供應商逐次用量無法查定。依站主授權只清除該筆 held 狀態並重試一次。恢復後首輪 `check-audio` 108/108、22 句標記；本地 Whisper medium 第二意見清除 10 句。之後 `h5v085`、`h5v088` 僅改配音唸法重錄；現行敘事盲評指出兩句重複「一張原鈔」，因此 `h5v084` 窄修為「河岸鈔票的研究」並重錄，保留 `h5v087` 對樣本範圍的限制。現行獨立盲評 **11/11 PASS**，答案 SHA-256 `91f67896ca692e8fe2e66dc0fdc20968691149c7a47201eb8a87aa9042467a13`。

當輪 `video.json` SHA-256 `fbb4616bc2822e0ea90edf6612fa8718758f98b384f765b9efb0bc9108ae8768`；`script.md` SHA-256 `c3cdaa5b13225e73027538698baf627b1d22203d20e07556b0ea87423f7c9b30`。外部 `timeline.json` SHA-256 `66996c424a387b5a73f8132a713056a3371a16fca26c7b617358b767c76b8adc`，**16073 幀／30 fps = 535.767 秒**，speech hash `7d8cb6cb30ba87d9`。現行 `check-audio` 108/108、**12 句標記**，`review/check.json` SHA-256 `0a6919f89b039d2f3e3b17d206b53d1c17604d00e8d4fccc7a1e9c2c255616b0`，`review/check-flags.json` SHA-256 `98f760d6df2209f1b13a6ee6d5a03a3cf9e6908fda077fcad409dad089996e54`。標記為 `h5v003`、`h5v034`、`h5v039`、`h5v061`、`h5v082`、`h5v084`、`h5v085`、`h5v093`、`h5v097`、`h5v099`、`h5v100`、`h5v102`；多為專名及同音字辨識歧義，不能自動核准。外部 `_receipts/` 保留原始 held、恢復紀錄與各輪檢查快照。`review-push --gate audio` 上傳當時回報 **pending**、`review-pull --gate audio` 當時讀回 **waiting for the owner**；站主其後完成聽審，`review-pull` 回報 **audio: approval recorded**，最新 `status` 讀回 **[x] narration approved**。

## 開場三鏡舊小樣實看與離線修正（2026-10-14）

以完整 JPEG 檢視外部 `keyframes/` 三張選取圖；這是逐張靜圖檢視，尚無連續成片實速驗證。舊 `manifest.json` SHA-256 `df7046c0241fb2222230319a229a5a499516d3d4e1ebe8792da1323f59499b2d`，綁舊 `look_hash=61f7f42d4d9f84fc`、`pictures_hash=4058fe3f0dee7913`，保留作為失敗收據，不拿來核准新版。

| 鏡頭與舊圖 SHA-256 | 原 judge | 人工實看與下輪修正 |
| --- | --- | --- |
| `open-counter`：`open-counter-1-trim.jpg` `ed5ce49452e6ab2cc91962085532341da6f1d0621bf7ab0cb9cd4980409caa91` | 6.88，FAIL；風格 0、領帶缺席、持錢包手不自然 | 成人寫實比例與模糊店員，不能作為 chibi 風格基準。改為寬景側面的小比例匿名人物，白襯衫與細黑領帶可見，櫃檯先保持空白。 |
| `open-ticket`：`open-ticket-1.jpg` `ed765cdd737f01f47680cfa8eb4343435571ddb48d653a47b5b6caa1fbf7a439` | 6.88，FAIL；風格 0、店員未遞票、前景手變形 | 特寫讓巨大的手壓過現金與機票，動作也讀不成收票。改為中景兩個小人物；現金與無字背面機票分置櫃檯兩側，手藏在櫃檯後，以交換後的物件位置交代付款。 |
| `open-aisle`：`open-aisle-1.jpg` `52582f49b0b4a40d4cba62539a5281987e280240554185c57bc06eff3e229693` | 9.29，PASS；仍記正面露臉 | 實看人物臉與成人比例仍過於具體，整組風格不連續。改為客艙寬景嚴格背面，匿名小人物停在空座旁，不再要求手持票。 |

本輪僅修改 `video.json` 的 `look.style` 和 `open-counter`、`open-ticket`、`open-aisle` 三筆 `data.prompt`，不改 line、章、場景 ID、camera、語音或 `script.md`。新 `video.json` SHA-256 `a259ccfba2c5bac01f013992d9a5cdac6379c94dee45ff8e04a49e1690158df9`；`script.md` SHA-256 仍為 `c3cdaa5b13225e73027538698baf627b1d22203d20e07556b0ea87423f7c9b30`，敘事 hash 仍為 `e0d2eb7016aea429`。新 `look_hash=b95bff7b9ed305af`、`pictures_hash=0bb81a00d04a8db6`；三張舊圖對新 look 已過期。`lint --json` 為 0 errors／0 warnings；三鏡 `keyframes --dry-run --shot open-counter,open-ticket,open-aisle --takes 1` 通過，MiniMax image-01 1K、每鏡一次總預估約 US$0.04。另對 65 鏡做一次全量 dry-run 與提示詞預算核對，65/65 均低於 MiniMax 1,500 字限制且沒有被截斷，單輪預估 US$0.88；這是離線預檢，未發送新付費圖像請求。新提示是否能解決舊缺陷，須重做三張後實看與按正常 judge 判定；這次文字修訂本身不是圖像驗收。

## 2020 年研究方法卡局部品檢（2026-10-14）

對照 [Kaye、Meltzer 原論文方法段](https://pmc.ncbi.nlm.nih.gov/articles/PMC7400570/)：十一月對照將兩張現代鈔票直接浸入哥倫比亞河十五分鐘，從邊緣取五份樣本；埋沙滲入試驗則把兩疊各五張乾燥現代鈔票埋入沙中，灌入濃度 1 kg/L 的矽藻土混合水，並非天然河水或原始贖鈔。`modern-controls` 的副標與 `burial-experiment` 的標題、步驟現在明示這些界線；旁白句子未改。

以現行主稿對兩張卡單獨使用同一離線 Chromium renderer 畫出 1920×1080 靜格，兩張各 **0 個版面問題**；人工打開 PNG 確認文字完整、清楚且沒有越界。收據與畫面在外部工作目錄 `_receipts/method-card-qc-20261014/`：`modern-controls-0.png` SHA-256 `bcfd7edfa6103d7d8e882670e0fb7d1bb2e71d094bb6d01175a7508f53818730`；`burial-experiment-0.png` SHA-256 `2ef1a58747da6a021e9b129aed92d6c15a48d226b129c4bc8d027bcb4c8e74f3`。這是兩張卡的局部版面品檢，尚非全片渲染。`narrativeHash=65c64491d8a53b77`、`speechHash=7d8cb6cb30ba87d9`，實際 `timeline.json` SHA-256 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984` 與 `narration.wav` SHA-256 `8b519d908e7b85d7d214288d3bf8c7ebb5bc897456a4b32c74143cff50253ba3` 未變；總長 16073 格，兩卡分別占 166、165 格。`lint --json` 仍為 0 errors、0 warnings。

## 62 個插圖鏡頭的來源路線稽核（2026-10-14）

完整 62 鏡分類、13 個提示詞窄修、原始來源與下一輪代表小樣，記在 [visual-route-audit-20261014.md](visual-route-audit-20261014.md)。此輪 `video.json` SHA-256 從 `f90cc5e16c1da87b46d9a59ffc4be8af4d313778ad3c88750350d36ae2b8ab7e` 變為 `74102087ca465c7c73044e1182671641965cc19cbd6f4d0470d11fcb9c16e6e3`；只改 `open-note`, `open-tail`, `captain-note`, `demand-question`, `agency-alert`, `second-flight-night`, `sand-find`, `tie-brand`, `tie-storage-box`, `tip-standard`, `control-limit`, `layers-sample`, `simple-story-changed` 的 `data.prompt`。敘事與 speech hash、已核准的 `timeline.json` 與 WAV 均未改。實際 108 狀態平均 5.0 秒、最長 7.3 秒、插圖時間 59.45%，`cadenceProblems=[]`；`lint` 0/0，62 鏡 dry-run 無提示詞超額。MiniMax 不接受本稿 style reference，先前 9 張開場樣張均未通過人工採用；本次提示詞預檢不能代替新圖及實速小樣驗收，仍先停在 `needs_revision`，不擴批。

## 最新狀態：三張原生卡接入與音訊核准讀回（2026-10-14）

`open-threat`、`open-tail`、`open-boy` 三張人工退件的付費插圖已在主稿改為[原創 SVG 來源卡](visual-recovery-three-native-cards-20261014.md)，原圖與帳本仍保留。改後獨立盲審 11／11 PASS，現行 `narrative_hash=25c823ca2e556693`；script lint 零錯誤、零警告。三卡接入時 `video.json` SHA-256 `d9f63fe9b019228f21ec02cb0b8029956ae8beed314342a9e841c77c5b2e9bba`；`speech_hash=0b7b642f114d257f` 未變。

以 `tts --refresh-evidence` 僅用已核對快取重建，**0 次合成、0 計費字元**；108 句 WAV、旁白總檔 SHA 與逐句時長皆未變。新的 `timeline.json` SHA-256 `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`。舊轉錄 108／108 句仍能按音檔 SHA 沿用，12 句標記未改，未重跑外部 check-audio。`review-push --gate audio` 已送新時間軸音訊卡；站主聽審後，主製作代理執行 `review-pull --gate audio` exit 0，正式 `approvals.json` 記錄本時間軸 SHA 已核准（2026-10-14T04:07:53.585Z）。詳細快照、驗證與送審／讀回收據見 [音訊關卡紀錄](mixed-three-card-audio-gate-20261014.md)。

已依單張授權完成 [`night-clouds` 氣氛圖小樣](night-clouds-one-shot-pilot-20261014.md)：`video.json` 新 SHA-256 `05abe8cf0cd4680a12e911feb118e6d3dec88c20dbba0f8b8e7ac65b51d0d870`，敘事／口播 hash 仍相同，音訊時間軸及核准仍有效。1 次 MiniMax 圖與 1 次 judge 新增 US$0.0135；模型 10/10 PASS，人工只接受為單鏡候選，前後鏡實速銜接及明亮雲緣的風格仍待驗，未送 storyboard。
