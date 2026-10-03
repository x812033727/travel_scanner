# 聲音寫法試聽：換口音或口吻之前怎麼做

Gemini TTS 沒有口音可選（`docs/videos/DESIGN.md`），口音與口吻全靠 `voice.style` 的字。字一改，每個片段的快取鍵就變、整支重錄，
所以**換寫法先試聽、站主選了才改程式**。2026-10-03 的例子：style 寫「台灣國語」被模型當成重台語腔演，站主聽了 11 段試聽選了
「標準國語，咬字清楚，台北人平常說話的語調」，現在是 `tools/video/core/accent.mjs` 的 `CHANNEL_ACCENT`
（寫法與送合成時的改寫規則見 `docs/videos/README.md` §頻道規格的「口音」列）。

## 不變的規矩

1. **口音字樣只有一處**：`accent.mjs` 的 `CHANNEL_ACCENT`／`CHANNEL_ACCENT_EN`。任何 style、提示詞、文件都不要再寫「台灣國語」「台灣腔」「Taiwanese accent」；
   舊字樣留在正式站設定列或舊 `video.json` 裡沒關係，`tts/requests.mjs` 的 `voiceFields()` 送出前會換掉。
2. **同一段樣稿、同一個聲音、每個寫法至少錄兩次**：Gemini 每次錄音差異很大，單次比較會被運氣騙。
3. **決定權在站主的耳朵**。量測只能排除穩定墊底的寫法，不能選出最好的。
4. 候選寫法要分「口音」（accent，改 `accent.mjs`）和「口吻」（register，改 `register.mjs` 的 `STORY_VOICE_STYLE`、站主貼在後台設定分頁的那段）；
   一次只試一種，不然聽不出是哪個字在作用。

## 步驟

| # | 做什麼 | 關卡 |
| --- | --- | --- |
| 1 | 寫 `sample.txt`（約 100 字、含數字與一個「你以為…其實…」，註明是示意不是數據）和 `candidates.json`（每個候選一個 `id`、`label`、`voice`、`style`）：現行寫法當 A0／B0 對照組、建議的新寫法、完全不寫口音、英文版 | 候選不超過 12 個，站主聽得完 |
| 2 | 每個候選錄兩次：`node tools/video/cli.mjs audition --text-file sample.txt --voices gemini:Sulafat --style "<候選 style>" --workdir <工作區>`（`--style` 一次一個，所以一個候選跑一次；輸出在 `<工作區>/_audition/<時間戳>/`）。本機沒有 `node_modules` 時走不了 CLI（要 pinyin-pro），改直接 import `tools/video/tts/client.mjs` 的 `synthesize` | 每個候選有兩個 wav |
| 3 | `ffmpeg -i x.wav -c:a aac -b:a 128k x.m4a` 轉成手機能播的檔，寫一個 `index.html`（每列：id、label、style 全文、兩個播放器），連同 `candidates.json` 一起交給站主 | 站主能在手機上逐一聽 |
| 4 | （選用）量一個代理指標排除明顯差的：擦音頻譜重心低於 4.8 kHz 的比例，越高表示捲舌越少、越像台語腔；寫法穩定墊底的才排除 | 量測結果寫進交接，不當結論 |
| 5 | 站主選定後：口音改 `accent.mjs`（`CHANNEL_ACCENT` 與英文版），口吻改 `STORY_VOICE_STYLE` 與 `models.py` 的 `DEFAULT_VOICE`，並請站主在 `/admin/videos` 設定分頁重貼 | `tools/video/core/accent.test.mjs` 與 `tts.test.mjs` 綠；`node tools/video/long-form/cli.mjs check` 綠（`models.py` 綁在長片收據裡，見 skill `dev-and-ci` 的 `duration-receipt.md`） |
| 6 | 部署後驗：api 容器的 `DEFAULT_VOICE["style"]` 開頭是新寫法；工人容器 `voiceFields()` 對舊 style 的輸出已改寫；下一支新影片 `video.json` 的 style 以新寫法開頭；站主聽一支成片 | 三個都成立 |

## 改寫法的代價

- 片段快取鍵含 style：含舊寫法的影片下次重跑 `tts` 整支重錄（Gemini 月字數會跳）。`speechHash` 不含改寫後的字，所以已核准的旁白不會自動失效。
- 口吻（`STORY_VOICE_STYLE`）在 `speechHash` 裡：改了全部重錄＋旁白關卡重審。已寫好的影片用 `restyle`（`script-writing.md`）。
- 漫劇角色的 style 由寫手模型寫（`prompts.mjs` 已要求用頻道口音字樣）；設定集裡既有的角色 style 不用改，送合成時會換。

## 來源

2026-10-03 的試聽（11 個候選、兩輪錄音、頻譜量測）與 PR #1168。候選檔與錄音留在站主自己的機器上（影片工作區的 `_audition/` 底下），不進 repo。
