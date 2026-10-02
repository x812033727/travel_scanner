# E1 這次不簽｜完整繁中聲音與剪輯交接

## 故事前提

知棠重生回婚禮簽字前，拒簽撕展示副本、退還新娘婚戒；完整原件留中央桌。後半拍頁碼並另存含附件的完整副本；她不接妹妹閉口禮袋，承川最後阻止外人看附件。原件封存、收據及授權對象細讀留 E2。

## 角色

旁白 Erinome；沈知棠28歲 Kore；顧承川31歲 Puck；沈知夏23歲 Aoede。人物、聲線、named looks沿既有productionSetting來源，現世知棠全程婚紗加頭紗。既有見證人員只出成人手部，沒有新speaker或台詞。

## 站主觀點

先優化並製作前兩集繁中影片與可開關繁中CC。完整繁中全片與CC交站主本人確認後才啟動日韓英；兩集/pilot/自動品管通過均不能代替全片確認。聲音預演不等於動畫，正常演出較短便縮短，不假發聲、慢唸或停格湊長度。

## 執行

33句、32個有聲scene的voice文件只供既有TTS CLI；42個原始shot ID及10個無台詞動作鏡在獨立editorial edit-plan。S35/S39為待實測合併候選，42不是必拍數。前15鏡承接已量測的51秒聲音剪輯，S16從51秒開始；後半時間仍planned，完整影片時長未知。

root將episode-01-voice.video.json、episode-01-brief.md、episode-01-series.json複製到repo外runtime/episode-01/下的video.json、brief.md、series.json，再執行CLI --file。未修改任何舊pilot檔案。本次轉檔不發出付費請求。

## 舊聲音的安全重用

`episode-01-validation.json` 已逐句記錄 L001–L011 的 runtime id、原 WAV 位置、SHA-256 與 line cache key。舊有 11 個 WAV 已讀檔核對雜湊；33 句聲音稿中的前 11 句文字、speaker、emotion、voice、發音設定及實際 request body 均與 pilot 完全一致。`episode-01-dialogue.json` 保留原 `WR-E01-L…` ID 與穩定 runtime id 對照，新 22 個 id 不隨重新編排而改號。

新文件 slug 是 `wedding-reckoning-e01-voice-zh-tw`，所以沿用同一 media root 也不會自動讀到舊 pilot 的 audio 目錄。由主代理將已驗證的 11 個 WAV 及相應 `cache.lines`／`cache.sha256` metadata 複製到新 slug 目錄；只複製記錄中的已驗證項目。先 dry-run 確认應只剩 22 個新 request，不能為省事無差別重錄 33 句。整體 speech hash 會因新增知夏、台詞和場景而改變，因此完整聲音檢閱軌與時間軸需重建，不能拿舊 pilot timeline 當 E1。

```bash
node tools/video/cli.mjs lint --file /workspace/mokaair-work/competition-20261002/runtime/episode-01/video.json --json
node tools/video/cli.mjs tts --file /workspace/mokaair-work/competition-20261002/runtime/episode-01/video.json --workdir /workspace/mokaair-work/competition-20261002/media --dry-run
```

以上 runtime 檔案由主代理從本次三份 `episode-01-` 檔建立；本轉檔代理沒有覆寫 repo 外 runtime、沒有送 TTS 或媒體請求。dry-run 後的實際合成與自動辨字檢查由主代理在本輪授權內執行。自然台灣口音、情緒、角色辨識、混音及真人聽感均需另留驗收紀錄。

## 完整剪輯與 CC

前 15 鏡保留既有 `measured-edit.json` 的實際聲音配置：0–51 秒；11 句乾聲合計28秒，影像尚未生成。S16 從 51 秒直接延續，沒有為舊「前60秒」規劃補 9 秒空白。後續 27 鏡只按正常句速估容量，目前整集參考時窗到153.5秒，不是實測成片長度或保證片長。33句的voice-only估算時間也不是最終影片長度。

先量新增22個WAV，以真實可用語音長度重排後半，再按完整 editorial edit 產繁中SRT/VTT；聲音稿跳過10個無台詞動作鏡，因此它的原生字幕／timeline不能直接貼到完整影片。圖像素材也不能把32個有聲scene當完整42鏡剪輯。無聲鏡保留撕紙、戒指與文件交付等動態行為，使用獨立環境／音效，不放假旁白、重複台詞、虛構發聲或凍結尾格。

S35的拇指穩紙與S39的鬆開頁角沒有獨立資訊增量，已分別標為可併入S34及S38的候選。原shot id與line id仍保留供回溯；先量相鄰兩句及正常停頓，若可以由不超過8秒的同一段有效動態反應承接，才減少一次source生成。若超窗就重排必要反應或精簡同義台詞，不把來源片延長成freeze。42是故事稿對照數，不是必須付費生成42片。

S24–S26只用原場景無台詞成人見證人員的手部。核頁鏡將比較設為既有構圖，單一主動作只翻副本一頁；整理附件、推交副本各自分鏡。S27只拿起副本，手機照片在旁為可比對的既有資訊；附件檢查留S28。S19將手機設在知棠同桌側、前段鏡框外，拿入鏡即可，不新增劇情袋子或換裝。這些是單動作構圖澄清，不改文件持有人或劇情次序。

## 離線驗證結果

`validateVideo` 與載入本集brief/series的 `lintVideo` 都是0 errors；只有原創故事沒有外部事實來源的通用警告，未捏造網頁來源消掉它。已檢查33句對原稿逐字／speaker一致、32有聲scenes、42原shot IDs、10無聲鏡、首段51秒測時、S16無縫銜接、全部來源角色／voice／named looks一致、前11個cache key與已存WAV雜湊一致。詳見 `episode-01-validation.json`。

這些結果只證明文件與聲音重用條件，不代表新22句已合成或聽校、完整E1動畫已生成、嘴型與道具連戲已通過，亦不代表完整繁中全片／CC已交站主本人確認。
