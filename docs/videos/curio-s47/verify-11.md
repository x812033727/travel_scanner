# S47｜網站待審與旁白製作關卡

日期：2026-10-20 UTC。這份紀錄接續 [R6 前製裁決](verify-10.md)。當時 `brief.md` 的 A／B 標題是 `### A｜`、`### B｜`，本地 `review-push` 的選項擷取器只辨識 `### 選項 A：` 形式。推送前**僅改這兩個標題的 Markdown 標記**，讓網站收到 A／B 兩個選項，沒有改動選項名、鉤子、主張、來源、口播或畫面提示詞。

新 `brief.md` SHA-256：`51ba34023a71aeb78e7868aa76cb60a4eac481dfaef31653afa6fbc179a54c4b`；原版是 `d4eefcb524fc68217f5b9a122039e07537bb92ec34226f447c85bec2d1295f06`。`research.md` `493d6bf8e73d9832c05300b2c9643e7e53c1448ac2215c54e2f32f9ad10fa357`、`script.md` `0dd8a74680d53b3133401b03495454df79564c23a0335dace21c8f13e38d3603`、`video.json` `3d8e87514a92de3ac42a2c3fadb23d5e1e0a54033be36daf27a9265506e15d45`、`claims.md` `9675fb565211d4d2cc80a038aa18ea29db62a396bcf8cb0a7d6d214b77a090ae` 逐位元不變；Jev 政策請求中的完整口播及站主觀點亦不變。前次來源／書面畫面 PASS 仍是舊五檔雜湊的原始收據；下段單獨記錄兩標題的獨立技術差分，不改寫舊收據。

協調者隨後**獨立唯讀**把目前 `brief.md` 兩個標題 `### 選項 A：`／`### 選項 B：` 在記憶體中還原成 `### A｜`／`### B｜`，重算出的 SHA-256 **精確等於**原先經獨立來源／書面畫面覆核的 `d4eefcb5…`；並重核 `script.md`、`video.json`、`claims.md` 均仍是當時 R6 雜湊。因此確認此輪只有標記格式差分，沒有修改獲 PASS 的事實陳述或書面畫面。原審核收據本身保持原版雜湊，不改寫歷史紀錄。

## 網站與本地授權

先 `review-pull`，網站回「找不到這支影片」。兩個標題修好後，選項擷取器讀到 **A、B**；`review-push --gate outline` 送出新 `brief.md`，Jev 推薦 **A，0.99**，網站因本片是人工推送而列 **pending**。`review-push --gate script` 送出上列精確 `script.md`，也列 **pending**；接著 `review-pull` 回 `outline: waiting for the owner`、`script: waiting for the owner`。Jev 的「依設定自動核准」是其推薦判語，**不是網站這兩關已核准**。

站主先前指示「以推薦的決定、不用再問」，據此在私有工作檔 `/workspace/.video-work/curio-s47/approvals.json` 留下**本地委派**紀錄：選企劃 A 綁定新 `brief.md` SHA，採 R6 劇本綁定上列 `script.md` SHA；兩筆 note 均明說「site hand_pushed pending, not owner/site approval」。此本地紀錄供工具按精確檔案續作，不能寫成站主已在網站按下核准。

## 旁白預檢

`tts --dry-run`：100 個請求，100 個待合成，預估 2740 計費字元；`gemini:Sulafat` 頻道聲音可用，網站本月顯示剩餘 8,615,368 字元。正式 `tts` 隨後成功：**100 個請求合成、2740 計費字元、0 個沿用**；每句 WAV 存在 `/workspace/.video-work/curio-s47/audio/`，speech journal 用於斷線保護。`timeline.json` SHA-256 `6d233902775aa7105df04a0f17fc55595569008f339c86eba6c2b104c877f752`，`narration.wav` SHA-256 `6219b5b2c50d3686a64af8715f2f27fd56c2baefa313dc2b3e8b254ca7bd17e8`。

以實際合成片段建立的 `timeline.json` 及 `ffprobe` 量得旁白總長 **678.77 秒（11:18.77）**：`wr001–008` 濃縮開場 **54.20 秒**，`wr009–097` 正文 **610.07 秒（10:10.07）**，三句片尾 **14.50 秒**。原創 5 秒片頭尚待合成時置於開場後；21 秒品牌片尾動畫亦尚待合成，最後約 16 秒須留推薦／訂閱框。量到的是旁白時間軸，**不是最終剪輯時長**。

[第一次完整官方音訊檢查](review/r6-audio-check-1.md)已查 **100/100 句、0 未查**，但 **22 句被標記，結束碼 1**。其中 11 句的轉寫差異可能牽動事件、控制動作或來源歸屬；也有多句可能只是轉寫選字。沒有可用的獨立覆聽證據，故不能判斷哪些是真正 TTS 錯字，更不能宣稱音訊通過。此輪停止在音訊關卡，不進付費插圖或配樂。
