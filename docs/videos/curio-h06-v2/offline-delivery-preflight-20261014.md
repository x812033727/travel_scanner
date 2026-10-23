# H06 v2｜成片前的免費素材與字幕預檢

**2026-10-14 圖卡更新：**下表的「現行版本」指開場兩鏡改卡前的快照。現行 `video.json` SHA、已重跑的離線字幕收據、候選時間軸與圖卡預覽見 [運河圖卡交接](native-canal-cards-20261014.md)。原史照卡與病院史照封面概念仍只是隔離預覽；無圖縮圖也不是成品。

日期：2026-10-14。這份紀錄先補已核旁白之後、付費分鏡之前可以獨立驗證的產物；後續一張**另獲站主授權**的 MiniMax 小樣結果記在文末。媒體留在外部 `<VIDEO_WORKDIR>/curio-h06-v2/`。下列字幕、來源卡及縮圖概念的本機預檢沒有改 `video.json`、`timeline.json`、`narration.wav` 或核准檔，也沒有寫正式 `frames/`、`captions/` 或 `final.mp4`；後續小樣只更新圖像媒體、manifest 與費用收據。

## 綁定的現行版本

| 項目 | SHA-256／雜湊 |
| --- | --- |
| `video.json` | `52e29bceaa443ce740ba0db5ff9eb64cca27613340828f813c56dcee00d2607a` |
| `timeline.json` | `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84` |
| `narration.wav` | `528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a` |
| `speech_hash`／`narrative_hash` | `9ae95e3507d3809f`／`02a39e4e1fb460a7` |

現行 `approvals.json` 有 `audio` 核准紀錄，綁上述時間軸 SHA；`status` 讀回 `narration approved` 與 `storytelling panel: passed`。這不延伸至任何圖像、最終字幕或成片關卡。

## 正文繁中字幕預覽

用目前工具的 `localeTexts`、`buildCues`、`checkCues`、`toSrt` 和 `toVtt`，依正式旁白時間軸產生 **正文專用預覽**，放在外部 `review/preassembly-captions-body-only-20261014/`。該目錄留 `make-preview.mjs`、`zh-TW-body-preview.srt`、`zh-TW-body-preview.vtt` 和 `receipt.json`，可按收據重算。

- 104/104 句各有字幕，104 cue；`checkCues` 為 0 問題，SRT 讀回的時間與文字逐 cue 相符。
- 正文為 15,028 幀／30 fps＝500.933 秒；預覽第一 cue 於 0 ms 開始，最後一 cue 於 499,510 ms 結束。
- SRT SHA-256：`c4c7bb509e45d34e65cf8617532def8e6869a8bb083471c09287b48824370231`；VTT SHA-256：`74411a7dd5fb22fcee01b2905f38042150bb3fcbe7b5e8b753ce2cadf7890866`。PowerShell 獨立讀檔雜湊與 `receipt.json` 相符。

**這不是可上傳的最終 CC。** `node tools/video/cli.mjs captions` 會要求 `final.mp4` 已按選定品牌片頭片尾合成，並以品牌後的播放時間軸輸出正式字幕；目前沒有成片，故未執行該指令，也未把 `status` 的「captions written」改成完成。後續必須重新產出正式字幕，對照最終 MP4 起訖、片頭插入點與口播同步後才可交付。

## 三張既有歷史照片的來源卡

`renderProblems(doc, root, {workdir})=[]`。對 `video.json` 現行三個 `photo` 景，沿用專案原生 `renderPlan` 與本機 Edge renderer，**只在外部 `review/source-photo-card-preview-20261014/` 輸出三張靜態預覽**，沒有走正式 `render` 階段。原檔、預覽 PNG 和版面問題逐項記在該目錄 `receipt.json`；三張預覽的 `layout_problems` 均為空。人工逐張開圖確認照片載入、可見標題、年份、「非現場／非原件」註記及館藏 credit 沒有被裁切。來源與權利沿用 [assets-provenance.md](assets-provenance.md) 已核資料，本輪只重新校驗本機位元組與畫面呈現，沒有重新宣稱網站授權狀態。

| 景 ID | 來源原圖 SHA-256 | 預覽 PNG SHA-256 |
| --- | --- | --- |
| `berlin-hospital-window` | `666a3939101ff4d3e5d5f85c24bd71df5fa63827e7b2aee6bab87a5a75f55e4c` | `176803290d6f642de816ab8aff6cbfa1a7a0121e980ae9ede6df14c76ebf1d2d` |
| `berlin-family-places` | `39cf832726b47d988e1d6dbf4ea2787b714dd08dc73e601cfba4bed1955d778f` | `0be773352972dc7673a6c1534bd587dae90f7abd3a7876af3c7c8dc474894a05` |
| `hospital-album-hands` | `ba40562cefefe55b768a99da74b1ab91da785d8a5a6976d41e2a3ae89c22f2be` | `ab0f5c6f23b56e2c38a48885addfb2c98b580d13deb4887ab619997ffc7367b1` |

這只證明來源卡在單張靜圖上可讀。相鄰鏡頭轉場、實際播放長度、全片聯絡表與成片 QA 仍未驗證。

## 有來源的縮圖概念，尚非可交付縮圖

為避免將退件運河圖誤作封面，另用**同一張已登記的 1885 年 Dalldorf 病院照片**及本機 `thumbnailHtml`，在外部 `review/source-thumbnail-concept-20261014/` 做一張 1280×720 的 JPEG 概念圖。沿用「她是／公主？」與「法院與 DNA 怎麼說」，並在左上清楚標「1885 年病院史料照」，使照片不被誤讀為 1920 年救援現場或安德森肖像。來源原圖 SHA 與上表首列相同；概念 JPEG SHA-256 `b546ff62a0cfbb92ec3a333f36888df3c1b3cc5ed464b4bf5e34f20ea1b92ffa`，169,309 bytes，renderer 版面問題為 0。人工開圖確認照片主體、標籤與大字可見，製作腳本與收據在同目錄。

**此圖是非正式設計方案，不是當前工具會產出的縮圖。** 現行上架流程的 `thumbnail.data.shot` 只能取已核 shot 的關鍵影格，或改用 `data.capture` 取 screencast still；它沒有「直接指定史料照」的已驗證路徑。要正式採用史料照方案，須先設計並驗證來源圖導入方式與縮圖 QA，不能把這張概念圖塞進舊或新 manifest 或上傳包。後續新 `hook-canal-rail` 小樣也已退件，故目前**沒有可維持原縮圖指向的合格開場圖**。未來若改成純色無圖縮圖，需修改 `video.json.thumbnail` 並重做視覺雜湊及縮圖檢查；本輪未動核准綁定欄位。

## 舊圖清單不能誤用

新小樣之前的 `keyframes/manifest.json` 是舊版本收據（檔案 SHA-256 `23cb0c66d086377196d4151b469e5ccff32469825e807466a41422c3b2643aa4`），其 `look_hash=dd05e380962e92b7`、`pictures_hash=046720f1333f63b4`，與現行 `d57461da98a0ba9b`、`09fd4baed7f1480e` **兩者皆不相符**。它已封存為外部 `review/pilot-single-20261014/manifest-before.json`。後續新 manifest 雖綁現行 look/pictures hash，只有一張**退件**的 `hook-canal-rail`，其餘 50 個 shot 沒有可用新圖；仍不足以核准當前分鏡。 `status` 的缺圖清單只逐項列缺檔，未列出的舊 `hook-hospital-door` 仍不等於有效圖。

`hook-canal-rail` 的舊裁切圖 SHA-256 `c6ac3f47fcf6e8373a5d626f08e948020636ee0b3a352212d1c23bc14ec0d82b` 含來源未支持的人物，已由人工退件；舊 manifest 的 judge 雖寫 `passed=true`，備註同時指出畫出人物，不可進片或當縮圖。`hook-hospital-door` 的 `17e388e0807ee107220a11ad1a1e70e4a7a9ec496aba60ef94dfa9d69d6c33f9` 僅舊 look 歷史候選，還需與新開場相鄰鏡頭實看。新 `hook-canal-rail` 圖的失敗與收據見下節；`thumbnail.data.shot=hook-canal-rail` 現在仍指向退件來源，縮圖不能據此產出或交付。保留新舊檔與原收據追溯，不把舊圖遷入新 manifest。

## 一張新小樣的結果與可執行邊界

站主只授權 H06 一張 MiniMax 小樣，`hook-canal-rail` 已送出一次。原圖 SHA-256 `57285728a07a103b06ed94da8dfcffa4fbe9e5c98d80b0c1702235d256f4b16a`、裁切圖 `3b50bc6fbcec7253873d02e44c774d96a3ad71814fa6493f6c42d2a5390e4188`；請求鍵 `f2790fe93cdec0da`。judge 整體 9/10，卻因核心主體是山灣而給 `subject=0`、`passed=false`；人工開圖另見底部虛構小字，故退件。現行 manifest SHA-256 `a9b9a08abb9153b0487c3db1f67a8131cc08f957f94fe78f8195459060c614c0`，`needs_review=true`，`thumbnail_source` 指向這張退件。完整人審與費用詳見 [visual-pilot-01.md](visual-pilot-01.md) 第四輪；外部 `review/pilot-single-20261014/postflight-sha256.json` 與六個逐檔副本留存原始證據。

不再重試同提示或把退件當圖。離線優先方案是原生、**明標非現場**的運河三色帶與姓名空欄；目前 `shot` 至少 7,514／15,028 幀，前兩鏡若都轉卡僅剩 7,560 幀、比下限多 **46 幀**，並非穩健餘裕。完整路線、是否需新增正式 keyframe 匯入能力及變更模板後的盲評／音訊核准代價，見 [offline-visual-route-20261014.md](offline-visual-route-20261014.md)〈退件後的離線替代方案〉。本輪只規劃，未改已核准結構。

## 剩餘關卡

一張有界小樣已退件，這項授權已用完，不等於擴批。須先離線決定可由現行工具驗證的開場視覺路線，再取得與來源及畫風相符、人工接受的連續小樣，接著才可能補 51 鏡、審分鏡、正式 `render`、`assemble`、按品牌時間軸正式 `captions`、可用縮圖、全片 QA 與完整觀看、包上傳檔。 `youtube.description` 仍稱「可愛卡通插圖」，新 look 是 2D 印刷風格；確定實圖後應在上架文案階段按實際畫面修訂，現階段未改它或任何核准綁定欄位。
