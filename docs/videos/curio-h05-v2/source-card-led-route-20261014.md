# H05 v2｜來源圖卡主導的正式分鏡（2026-10-14）

## 正式組片、縮圖與成片關卡收據（2026-10-14，15:41 台灣時間）

本節是目前工作目錄的最新讀回；下方尚稱「未組片」、「未定稿」及「沒有 MP4」的段落，均保留為當時的製作快照。正式時間軸仍是後台已於 2026-10-14T06:53:12.315Z 核准的 `c43d09a858bfd8a39882510b52e3b8cda79563be07c978854387940489f6ac76`，89 景／102 句，正文 15,381 格（8:32.70）；縮圖改動沒有重錄旁白或改動該時間軸。

- 現行 `video.json` SHA-256 `8be6f72e58b21a419f27162241baee9b63e46ed955def110211d12092d588c62`。縮圖改用 `thumbnail.data.asset` 引用 `diagrams/thumbnail-original.png`（SHA-256 `bb262440f0340c1ea9db197b36a35916217293e5d8d046e076d8ffcffb19cb5d`），素材表記載 Mokaair 原創與 `thumbnail-original.svg` 原件。三捆為抽象示意，圖上標「示意」，沒有冒充 FBI 贖鈔原照或河岸發現現場。正式 `thumbnail.jpg` 為 1280×720，SHA-256 `84ea0ccaeda44c7c4268a616764a029b72fc19dc3da0a59dd8f4c2f7f4eeaee3`；1280×720 及 320×180 候選均已實看，手機尺寸仍可讀「5,800」與問題副標。
- 縮圖重繪後重新組片，`checks.json` 的 `ok=true`、`problems=[]`，0 個片段需重新編碼。正式 `final.mp4` 為 16,161 格／30 fps＝8:58.70（含 150 格品牌片頭與 630 格片尾），SHA-256 `32cdc6403dbd321300c3a53ed2d2953696a3aa79da9ede5e977c00423499eb79`；89 景的 267 個抽格與對應圖卡比對，最低 PSNR 39.18 dB；整體 -14.1 LUFS、true peak -0.9 dBTP。繁中 `captions/zh-TW.srt` 為 102 cue，SHA-256 `d68fc3a6d2432c3c9b02bb6b818347498ef03e8f70d3b272b2f4ef92becef76c`。這些數值是本機檔案及機械品檢結果，不能取代站主完整看聽或 YouTube 播放器檢查。
- 最新 `review/qa.json` 綁上述 MP4 SHA，**10／11 項通過**。組片、渲染、旁白核准、節奏、字幕、上架文字、查核、縮圖、頻道立場與揭露項通過；`links` 一項未過：來源清單 10 個連結中，7 個 `www.fbi.gov`、`archives.fbi.gov`、`faa.gov` 官方網址在本機 editorial GET 均回 HTTP 403。同輪已透過獨立瀏覽器開啟這七個官方頁面，證明當時頁面可由瀏覽器讀取；**本機自動連結檢查仍是失敗，不能記成 11／11**。Wikimedia Commons 路徑中的括號已作 URL 編碼，本機 fetch 回 200；連結擷取器曾截斷括號網址的獨立缺陷另開 `tasks/open/2026-10-14-video-qa-truncates-source-urls-with.md`，不影響這七個 403 的誠實計數。
- `review-push --gate final` 已送出上述成片 SHA、實際 **10／11** 報告與預覽；後台回覆 **pending**。成片尚未核准，上傳包尚未產生，YouTube 尚未上傳。站主須完整看聽並決定是否接受該連結檢查限制；核准後再用 `review-pull` 讀回同一 SHA。這裡沒有把等待送審或瀏覽器可開頁面寫作成片核准。

## 字幕安全區逐景標記與新圖卡渲染（2026-10-14）

依現行來源圖卡版逐景檢查，`compare`、`stats`、`steps` 的 `data.source` 與 `photo` 的 `data.caption` 共 49 景使用模板底部來源行；舊模板在 1920×1080 的來源行落於 y=902–948，跨入底部 15% 字幕保留區（y≥918）。本輪只在這 49 景的 `data` 加入 `cc_safe: true`，讓模板將內容底線上移至 y=868；沒有變更旁白、場景 ID、版型種類、揭露順序或來源文字。`open-note` 的 SVG 內頁尾 y=873–900、`burial-edge` 內部最低文字 y=701–730，另列入實際字幕覆蓋抽查。

修改後 `video.json` SHA-256 為 `284131bd7381489eedbf9db0474d38c18473faf432b5de10c9edd0c43dd7d43b`；`lint --json` 零錯誤、零警告，現行獨立敘事審查仍為 11／11 PASS。`timeline.json` SHA-256 **仍為 `c43d09a858bfd8a39882510b52e3b8cda79563be07c978854387940489f6ac76`**，與後台讀回的正式音訊核准完全相同（`approvals.json` 2026-10-14T06:53:12Z）。下文「待審」是此次核准前的歷史快照。

`render --slug curio-h05-v2` 本機 exit 0，102 個狀態全數新繪、0 個重用，耗時 659 秒；`frames/manifest.json` 記 89 景／102 狀態、SHA-256 `cef4358047d70263488474bc27f8940dd8956b628f7a03224119c053cd695529`，`contact-sheet.png` SHA-256 `a0b29753710cf04cf482e5a64c53d9c41f4300739caa3b2fa9ee69f9430faf98`。聯絡表已作整體目視檢查：深色來源卡與 FBI 物證照片交錯、無顯著超框或虛構人物畫面；渲染器未報版面錯誤。`captions --slug` 另依核准時間軸產生繁中 102 cue，SRT SHA-256 `5905f129ddb7d8b7882e9853fd67633733366a5f07b06b9afa408a9e7e4c1dcf`。`status` 現顯示旁白核准、圖卡渲染、字幕完成；尚未組片。

字幕 QA 記在工作目錄 `review/cc-overlay-qa-20261014/`，其 `report.json` 綁本節的影片、時間軸、圖卡 manifest 與 SRT SHA。以目前 102 cue 的字句與時窗，模擬 1920×1080 48px／1280×720 32px、底部置中最多兩行的黑底 CC；逐景掃描 89 景／102 狀態，**來源行的直接字形遮擋為 0 景**。實看 `discovery-date`、`tie-original`、`delivery-table` 在兩種尺寸的字幕覆蓋樣張，來源文字與物證說明仍可讀。`open-note` 的實際 cue 為單行，文字未碰撞；用另一句兩行字幕作壓力測試時，只蓋到 SVG 最下方奶油色紙面，沒有蓋到「非當年原件」及其他但書。`burial-edge` 的實際兩行 cue 蓋到外層紙卡底框與深色裝飾帶，圖內的材料、處理條件、3–4 mm 結果、非原鈔／非河水等文字仍在字幕上方。這是**本機字幕位置模型**，不是 YouTube 播放器實測；正式成片與播放器仍須再看。

`thumbnail.jpg` SHA-256 `a1b927d88e0d0dea1b9eb6b233c51484fc8d002c76dead695f181f471a73d5c9`。1280×720 與 320×180 抽看後，主數字「5,800」在小圖清楚，副標仍可辨；右側約六成完全空白，視覺上像尚未放入主體。**縮圖尚未視為定稿**；可優先研究沿用本片已有來源、已標授權的 FBI 贖鈔照片作主體，不增購或生成新圖，也未在本輪改縮圖資料。下步是在縮圖定稿後組片，正常速度看聽完整 8:32.70，再做正式 QA／成片關卡。

## 102 句音訊重綁與待審收據（2026-10-14）

上述零費用刪句完成後，已用原有 WAV 重建正式時間軸：`video.json` SHA-256 `3f4ed2287400b2a772062b7a1b0ca2843e41c2e36ddd95c0c0de6047b2bb5e80`、`script.md` SHA-256 `c12d764f3dcc2dad2f60b398269b250bd7e7d8589f1c82bfa3c36577f80a68a4`、新 `timeline.json` SHA-256 **`c43d09a858bfd8a39882510b52e3b8cda79563be07c978854387940489f6ac76`**。時間軸為 89 景、102 句、30 fps／15,381 格，即 **8:32.70**；新 `narration.wav` SHA-256 `191ab6a8df30d8465ced445f7beca0076550e9f2513ff142deeb1eadf572bf49`（49,219,244 bytes）。

逐句 ID 與目前 `video.json` 順序一致；相較來源圖卡修改前快照，只移除 `[h5v042]`、`[h5v053]`、`[h5v068]`、`[h5v110]`。保留 102 句的單句 WAV SHA-256 與取樣數均和快照相同，逐檔雜湊也與新時間軸記錄相符；句間影格連續，末句結束於第 15,381 格。`check-audio` 檢查 102／102，使用既有證據：**0 新轉錄、0 新 Jev 呼叫**；69 句逐字相符、13 句同音或語助詞差異、9 句由第二轉錄清除，11 句仍標記 `[h5v003]`、`[h5v034]`、`[h5v039]`、`[h5v061]`、`[h5v082]`、`[h5v084]`、`[h5v085]`、`[h5v093]`、`[h5v097]`、`[h5v099]`、`[h5v102]`。這 11 句音檔沒有重錄，舊版雖曾由站主聽審，**新播放順序仍須聽完整段**。

`review-push --gate audio` 已提交新時間軸；隨後 `review-pull` 讀回 **waiting for the owner（exit 3）**。後台尚未對 `c43d09a8…` 核准，先前 `d01d2405…` 的核准不適用。此輪沒有付費合成或新增音訊判審。下列「新時間軸尚未重建」等文字是更早的歷史快照，以本節為準。

## 最新窄修收據（2026-10-14）

站主選擇零費用的去重範圍後，只刪除旁白 `[h5v053]`、`[h5v068]`、`[h5v110]`，並刪去 `[h5v068]` 的唯一場景 `tie-brand`。`discovery-date` 保留日期、三捆與 20 美元面額的資料卡，將舊「插畫重建」標題改成「來源資料卡」；`tie-original` 的 FBI 原照圖說承接「跳離飛機前摘下黑領帶」，並掛 `c27`。片尾保留 `[h5v109]` 和 `[h5v111]`。除這三句外，其他口播文字未改。

目前 `video.json` SHA-256 `3f4ed2287400b2a772062b7a1b0ca2843e41c2e36ddd95c0c0de6047b2bb5e80`，重產 `script.md` SHA-256 `c12d764f3dcc2dad2f60b398269b250bd7e7d8589f1c82bfa3c36577f80a68a4`；**89 景、102 句、六章**，圖卡類型為 `big` 28、`photo` 6、`diagram` 8、`steps` 10、`quote` 2、`stats` 15、`compare` 19、`bullets` 1、`shot` 0。新 `narrative_hash=59c8fdd94bfabe98`、`speech_hash=ea11af6360013a22`。`lint --json` 為 0 errors／0 warnings，估算正文 8.3628 分鐘；`tts --dry-run` 為 97 requests、**0 to synthesize／0 billable characters now**。沒有執行付費 TTS 或時間軸重建，舊 `timeline.json` 與其核准不能當作這一版的核准。下文 91 景／106 句及舊 SHA 是改卡當時快照。

## 站主決定與邊界

站主看聽舊隔離預覽後，決定 H04–H06 改走來源圖卡主導的投影片，調整原先插畫至少佔一半的規格。本輪 H05 把 **54 個未有人工接受圖片的 `shot` 全部撤出正式分鏡**，沒有補做第七張 MiniMax，也沒有花圖像或語音費用。`arrival-cabin`、`aircraft-search` 的退件與舊小樣照原紀錄保存；不把機器判圖 PASS 解讀為可用圖片。`night-clouds` 先前只是單張氣氛候選，也不列為正式圖。

這是場景**畫面**修訂。`video.json` 仍有 91 景、106 句、原場景順序與逐句旁白。前一版時間軸的 15,912 格／30 fps＝8:50.4 保持為核對基準；新的正式時間軸尚未在本輪重建。前一版 `timeline.json` SHA-256 `d01d24050ec6cd6a7d5cd720b677ccb64b7bfdbd5368c02b0b08327206f5d391` 已獲站主在後台核准，**不涵蓋這次改卡後的新版雜湊**。

## 可執行的畫面配置

目前 `video.json` 共有 `big` 30、`photo` 6、`diagram` 8、`steps` 10、`quote` 2、`stats` 15、`compare` 19、`bullets` 1，`shot` **0**。原生深色卡片在物件照片與八張原創來源圖之間穿插，避免整段使用相似的奶油色圖卡。每張新卡的標題、數字與對照只重述現有旁白、[FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[2016 年聲明](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)或 [Kaye、Meltzer（2020）論文](https://www.nature.com/articles/s41598-020-70015-z)已查的事實；疑問卡保持疑問，不畫出不存在的現場、人物、鈔票或顯微照片。完整逐景資料以 `video.json` 為準。

| 敘事段落 | 視覺轉換 |
| --- | --- |
| 紙條與公事包 | 機票原照、領帶原照、紙條／公事包／階梯原創來源圖，和深色疑問卡；不重建匿名人物的臉、酒杯或機艙物件。 |
| 西雅圖交付與第二段航程 | 用兩步事件卡標示落地、交付、乘客下機、再起飛；FBI 案件頁有記錄的數額與人數沿用現有統計卡。夜間落點用「不明」文字卡，不畫推定降落地。 |
| 搜尋與河岸發現 | 保留 `norjak`、機身搜尋的來源 SVG；兩位空服員描述、候選名單、物證門檻以對照／數字卡呈現。贖金原照只標為事後物證陳列，不標成挖掘現場。 |
| 領帶與未破案聲明 | FBI 領帶原照加上「樣本 ≠ 身分」對照；探員的生還看法與遺體未找到的事實分開，2016 年資源轉移不說成破案。 |
| 一張原鈔研究 | 用年份、單張材料、河水對照與季節差異的資料卡；約 30 公里標為**兩地位置差**，不畫成漂流路線。原創埋沙對照卡說明現代鈔票、人工混合水與 3–4 mm，並明示非原始贖鈔。 |

三張 FBI 物證照片仍由 `assets[]` 逐張綁公有領域來源與 URL。`note-handoff.svg` 原本漏列於素材表，這輪補列為 Mokaair 原創來源示意圖。`youtube.description` 已將「其餘為情境插圖」改成來源示意圖與原生資料卡的準確說明。`look` 已刪；縮圖原本引用的 `boy-bank` 未通過圖片不再使用，現採 `layout: c`、`tone: navy` 的文字主體候選。縮圖仍須在 1280×720 及 320×180 實看並由成片品管決定。

## 離線檢查與 CC 限制

- `node tools/video/cli.mjs lint --slug curio-h05-v2`：**0 errors／0 warnings**。`renderProblems` 以正式 repo 和既有工作目錄讀素材，回傳 `[]`。
- 以原 106 句／15,912 格的**唯讀時間軸**計算新場景：106 個狀態，最長 7.8 秒、平均 5.0 秒，`cadenceProblems=[]`。這是時間窗相容性檢查，未重建正式音訊證據。
- 倉庫 `slideHtml`／`openRenderer` 抽畫埋沙圖卡與新 `briefcase-latches`、`distance-not-drift`、`archive-many-folders`、`simple-story-changed` 四張原生卡，Chromium 回報五張 `layout_problems=[]`；抽看的對照／統計文字可讀。這是靜格抽查，未代替 91 景聯絡表或正常速度有聲預覽。
- `burial-edge-control-source-card.svg` 增加下方深色帶（SVG SHA-256 `89fca64ef5b650698a879ba51e6a04a7144de1ac2e0310f5a77546b46ed0780e`）。以 `h5v101` 兩行模擬 CC 做 1920×1080 及 1280×720 靜格後，圖內事實字與來源腳註均在字幕上方，無機械版面錯誤。模板 `.t-diagram .paper` 仍在 SVG 外加約 18px 奶油色邊，字幕框會壓到邊框；SVG 無法消除這條邊。其他原生 `stats`／`steps`／`compare` 的來源行靠近畫面下緣，開啟兩行 CC 時可能被遮住；正式 CC 安全區與播放器覆核仍是待辦，不能報為全片通過。

現行 `video.json` SHA-256 `52a2316d9e98fab1f0302db2fe8703cefde2d6d9d4c1e840f683cfa5fcb44bbf`。沒有改 `script.md`、既有 WAV、`narration.wav`、工作目錄 `timeline.json`、`approvals.json`、判圖 manifest 或帳本。

## 接下來的關卡

1. 針對改卡後現行稿，重新取得獨立 11 題敘事盲審；再以既有 WAV 重建正式時間軸，逐句核對 ID、順序、影格及總音檔雜湊，並取得**新時間軸 SHA** 的後台音訊核准。核准不能沿用 `d01d2405…`。
2. 渲染全部來源卡與三張檔案照片，目視聯絡表；製作 720p 有聲草剪，正常速度聽看轉場、兩行 CC、來源行與字幕安全區。若模板邊框或來源行真的碰撞，另開只影響這支片的版型修正並重走雜湊核准。
3. 再做縮圖、正式字幕、成片 QA、站主成片審查及上傳包。**目前尚無可交付 MP4。**
