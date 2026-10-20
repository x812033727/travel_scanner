# S45 R8｜實音長度與完整音檢：HOLD

2026-10-20 UTC。這是**精確 R8 劇本**的語音回條，不是旁白核准，也不是影片完成。內容關卡：R8 [獨立來源／書面畫面](review/r8-source-independent.md) PASS、[兩名全新敘事讀者](verify-15.md)合併 PASS、[分類正確政策](verify-16.md) PASS。`script.md` SHA-256 `6210aa1a85ca1e69ee01a3cfe9ce5a970336b262cdc3beb8cd1e944f1da1603e`、`video.json` `c3fa833ef6f60de7e3ef90e1fc7436d72add3c6a30d3756b6a97bfbaaa28d4ce`，合成前後未改；網站精確 R8 outline/script 仍為 `hand_pushed pending`，本地核准標成 LOCAL delegated，沒有冒稱站台核准。

## 語音、時長與帳目

在已配對的雲端環境，用 `Gemini Sulafat` 跑一次 R8 `tts`：**102/102** 句、102 請求成功，2,558 個 Gemini 免費層可計字元。工具的 speech journal 在每句答案存入 `audio/cache.json` 後釋放已確認請求；結束時沒有 held entry。保留的語音檔在 `/workspace/.video-work/curio-s45/`，不進 Git。時間軸 speech hash `55a55d546b528fa5`；一次窄範圍補錄後 `timeline.json` SHA-256 `20c4dac3d58e325ef42b6da6a068c2e772a8122000320bc36961c38204bbccb1`，`narration.wav` SHA-256 `b404762d84d59f6324a64a5c7f6e2e9e87e667f1a48858b68e14d867b8695b6a`。實測濃縮開場 **45.60 秒**，開場後至片尾前主體 **582.30 秒（9:42.3）**，片尾前口播 627.90 秒，全段旁白加停頓 646.97 秒；正文超過 480 秒。這些是語音時間軸，尚未加 5 秒頻道片頭、21 秒視覺片尾或完成影片。

第一次完整 `check-audio` 轉寫 **102/102**，29 句逐字吻合、47 句只有同音／語助差異、1 句 Jev 判可接受、**25 句官方旗標**（exit 1）。保留原回條在工作目錄 `review/check-r8-first.json` SHA `d2b1dd6d884f4913490af4c2cb6eca1b078012f23f071d6defef6f4340737618`，`review/check-flags-r8-first.json` SHA `f6e2e69a4eda93a08da64dd7cc411ec3a9d6373f15c61e020ed852a6feacccd8`。

先按語意風險選 **4** 句一次定點補錄，不重錄其他 98 句：`bly031` 醫院與假扮、`bly032` 醫師／律師、`bly088` 陪審團／培訓團、`bly095` 未宣誓／衛生室。`tts --redo` dry-run 顯示 4 請求、約 130 字元；實跑成功 4 請求、**130** 個可計字元，其他 98 句吃快取。累計本輪 TTS **2,688** 個免費層字元。四句原始 WAV 備份於 `review/audio-r8-first/`：`bly031` SHA `66cb9e6e594c50b35768a8270fda48674fd89d02c4cf00ac07e0726f70636b05`、`bly032` `3a0d4323076eb9eb961bfcdc8429034ce1ff90be16dc2a554ee9615feb5328f6`、`bly088` `fd769ab00d946479ffedfaeb27cdfc68020b8e8cf99d68a39712a74c09f5b4a9`、`bly095` `73a3fe4ec6079faa7607f6a6f4a23e6b9cf74eeb8a01a1973781e80382a32fd8`。沒有重送不確定請求，journal 最後空白。

第二次**完整** `check-audio`：102/102，29 逐字、49 同音／語助、1 Jev 可接受、**23 官方旗標**（exit 1）；只新轉寫 4 補錄片段並做 1 次 Jev 判讀。`bly031`、`bly032` 已解除旗標；`bly088` 仍把「陪審團」記成「培訓團」，`bly095` 讀到「未宣誓」，但把「衣物」記成「醫務」。第二次原回條在 `review/check-r8-after-risk-redo.json` SHA `3dc706f6e1bc3e159b331697b42cb85ed452803673d20cd04abd87797a73496d`，`review/check-flags-r8-after-risk-redo.json` SHA `52fc2e7b1587d1acc9742c06945e559bbcaad7219b15ea0bd`。23 個 ID：`bly006/010/015/020/027/042/044/045/052/054/059/061/063/069/083/085/086/088/095/097/098/999a/999c`。轉寫中的「她／他」「布萊寫／布萊雪」多為同音字；**不能因這個推測把官方 23 旗標宣稱清零**，也不能忽略 `bly088/095` 的意義風險。

曾嘗試 `check-audio --second-opinion` 用本機 `faster-whisper` 的 `small` 模型獨立聽 25 句，但模型需從 Hugging Face 下載，雲端代理回 `403 Forbidden`（`httpcore2.ProxyError: 403 Forbidden`）；本機沒有可用模型。`hf-mirror.com` 與 OpenAI Azure edge 的 HEAD 也回 403。已停止下載，該次執行 **0 新轉寫、0 Jev 呼叫、沒有排除旗標**。沒有假稱取得獨立音訊證據。

## 判定與下版交接

**R8 音訊 HOLD**。在官方旗標仍為 23、又無第二路聽證時，停止 MiniMax 插圖、配樂、分鏡核准與成片；不靠同一份稿子無差別反覆補錄。先準備 R9 只針對這 23 句的來源安全口語措辭，保留事實、時序、三個開場懸念及 8 分鐘正文。任何台詞修訂都使 R8 敘事／政策／本地精確劇本核准與現有語音證據對新版失效；要另做獨立來源、兩名新敘事盲讀與新政策判讀後，才能對 R9 再做 TTS。上述工作目錄音檔是 **R8** 的原始媒體，不可冒充 R9 旁白。
