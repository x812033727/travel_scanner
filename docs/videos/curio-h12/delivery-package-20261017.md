# H12 四語上傳包送審收據

日期：2026-10-17（Asia/Taipei）。本收據記錄本機素材和後台審核；YouTube Studio 上傳、播放驗證及公開排程仍須分開讀回。

## 站主試聽與檔案

- 英語：站主對 `9jra` 回覆「聽到 them，英語旁白可以」；日語回覆「日語旁白可以」；韓語對逐句試聽回覆「OK」。因此沿用三條原音軌，不因 ASR 旗標重錄。英／日／韓各 93／93 句機械 QA 完成，分別保留 12／27／20 句旗標與離線轉寫；原始分流見三份 `i18n-audio-qa-*-1.md`。
- 已核准的繁中 `final.mp4` SHA-256 `2B24B5DF98A459CD587364C24D80FB0A7AFADFF4519DE86001B4A7D0E11D047D`。上傳包副本逐位元相同，沒有重製繁中成片。
- 英／日／韓配音 SHA-256 依序為 `8CA592CB0E7D62593A39606DC3DC79B3DA95380F23B13C299049203468DB72AD`、`9115BCF7624D6FC0B8192C8E1445AC965345F76AE49AC3DEDB471DB27B81F197`、`A59E6C751F59831670201F9290C2A357B6AD1B593994599FBAB4C8AE9FC48639`；三份上傳包副本與來源逐位元相同。
- `captions --slug curio-h12` 重建四語字幕：zh-TW 97、en 96、ja 102、ko 99 cues；`captions/manifest.json` 四語 `problems=[]`、`skipped={}`。

## 上傳包與後台

- `package --slug curio-h12` 在 `<home>/mokaair-work/videos/curio-h12/upload/` 產出已核准成片、主縮圖、英／日／韓專屬縮圖、四語標題說明、四語 SRT、三語 m4a 及 `UPLOAD.md`。files、descriptions、captions、disclosure **4／4 通過**；`metadata.json` SHA-256 `6DDB8856C732C835DBD46BB26836F5F1911EED677CCABA2F0C602BB78C6BEEE9`，`language_choice` 三語皆勾 metadata／captions／dub，無 skipped locale。
- `review-push --gate publish` 成功送出後，唯讀 API 讀回最新卡 `9ccad952-cb3b-45f6-8f8b-8ae71f0fda8d`、`content_sha256` `6DDB8856C732C835DBD46BB26836F5F1911EED677CCABA2F0C602BB78C6BEEE9`、**approved**（`2026-10-17T03:33:10.212209Z`）；`review-pull --gate publish` 已將此核准寫入本機。
- `review-push --gate languages` 成功送出；初次唯讀 API 讀回最新卡 `abeb9cc0-20e8-409b-b972-c379072fcfcb`、manifest／`content_sha256` `8E5DD6E09FDC943F0AB6A4FB8A04F0859D8A885144CF044F698CCA5FAF74B61F` 為 **pending**。站主回覆已核准後，唯讀 GET 讀回同一卡 **approved**（`2026-10-17T03:37:04.574729Z`）；本機 `review/languages.json` SHA-256 完全吻合，`review-pull --gate languages` exit 0，根目錄 `approvals.json` 已記錄同一 SHA。
- `status --slug curio-h12` 顯示 upload package 完成、on YouTube 仍未完成。後台語言卡核准及 CLI 的成功訊息不證明 Studio 三語音軌已上傳。下一步依 `upload/UPLOAD.md` 由站主在 Studio 上傳私人影片、三語配音與專屬縮圖，貼回影片 ID 後再核對播放。

## 費用與範圍

本次字幕、打包、送審沒有付費供應商呼叫；沒有改任何三語譯文、音檔或已核准繁中成片。共用估算停手帳本讀回 H12 US$6.435／8.50、五集 US$28.4295／41.50，無 active reservation；此為保守估算，非供應商發票。
