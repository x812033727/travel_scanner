# H11「四葉」修正版成片送審

日期：2026-10-16（Asia/Taipei）。這份收據綁定更正取樣單位後的新成片；舊版成片與上傳包核准不能沿用。

- 站主已核准修正版劇本 `script.md` SHA-256 `7000C074516D3A30484E794D9D490DFF9412E8A869AD4743D81915CDAC7D6238`，並試聽及在後台核准重錄的 `v0e564e3`「研究人員從四葉取下四份樣本」。其餘 74 句沿用舊音訊；新版旁白時間軸 SHA-256 `CCFF7C2723920387883243FC131FDFD1B6B8D57606DE39EF1A33587B96E36905`。
- `clips` 重用已核准的 70 張 still，0 個付費片段；`assemble` 重建 17,229 格／30 fps＝574.3 秒（9:34.3）的 `final.mp4`，SHA-256 `54EFA17859D4359B84A9266799108B3C0DE0597DDFAAA2F1B4B3F556801FF1BC`。合成檢查為 -14 LUFS，抽比 9 格與投影片相符。
- `captions` 產出目前已選語言的 zh-TW 104、en 84、ja 121、ko 121 cue，四語翻譯均為目前劇本版本。尚無三語配音，字幕暫以繁中旁白時間軸安排；配音完成後需重產字幕。
- `review-push --gate final --manual-review` 的 QA 為 **10／11**；唯一未過是片尾 `outro state 0` 停留 22 秒，超過 15 秒節奏門檻。assemble、render、narration、captions、metadata、facts、links（7／7）、thumbnail、TypeSafe Jev policy、disclosure 均通過。報告 `review/qa.json` SHA-256 `96987FF69F13A58C538716F1A3B6A85A13BFE961139488243450504BDF28A738`。
- 新版 720p 預覽 `review/preview-54efa17859d4359b.mp4` 為 20,220,375 bytes，SHA-256 `EFE33F37E4BEA032F7992218CCD6FF67B975186A6882EA9CDD9B95E32F15EEBF`。`review-push` 成功，`review-pull --gate final` 讀回 **waiting for the owner**；站主可在 `/admin/videos` 或本機 `review/final.html` 查看。未讀回新版核准前不得建立新版上傳包。
- 新版 QA 與送審各一次 TypeSafe Jev 判讀；共用停手帳本各以 US$0.05 保守估算，H11 目前累計 US$2.348／US$8（其中多語增額 US$2 尚未用於付費配音）。供應商最終美元帳單不可得。未上傳 YouTube。
