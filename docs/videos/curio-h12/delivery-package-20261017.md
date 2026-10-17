# H12 四語上傳包送審收據

日期：2026-10-17（Asia/Taipei）。本收據記錄本機素材、後台審核與同步；Studio 的播放、語言縮圖和可見度仍須分開讀回。

## 站主試聽與檔案

- 英語：站主對 `9jra` 回覆「聽到 them，英語旁白可以」；日語回覆「日語旁白可以」；韓語對逐句試聽回覆「OK」。因此沿用三條原音軌，不因 ASR 旗標重錄。英／日／韓各 93／93 句機械 QA 完成，分別保留 12／27／20 句旗標與離線轉寫；原始分流見三份 `i18n-audio-qa-*-1.md`。
- 已核准的繁中 `final.mp4` SHA-256 `2B24B5DF98A459CD587364C24D80FB0A7AFADFF4519DE86001B4A7D0E11D047D`。上傳包副本逐位元相同，沒有重製繁中成片。
- 英／日／韓配音 SHA-256 依序為 `8CA592CB0E7D62593A39606DC3DC79B3DA95380F23B13C299049203468DB72AD`、`9115BCF7624D6FC0B8192C8E1445AC965345F76AE49AC3DEDB471DB27B81F197`、`A59E6C751F59831670201F9290C2A357B6AD1B593994599FBAB4C8AE9FC48639`；三份上傳包副本與來源逐位元相同。
- `captions --slug curio-h12` 重建四語字幕：zh-TW 97、en 96、ja 102、ko 99 cues；`captions/manifest.json` 四語 `problems=[]`、`skipped={}`。

## 上傳包與後台

- `package --slug curio-h12` 在 `<home>/mokaair-work/videos/curio-h12/upload/` 產出已核准成片、主縮圖、英／日／韓專屬縮圖、四語標題說明、四語 SRT、三語 m4a 及 `UPLOAD.md`。files、descriptions、captions、disclosure **4／4 通過**；`metadata.json` SHA-256 `6DDB8856C732C835DBD46BB26836F5F1911EED677CCABA2F0C602BB78C6BEEE9`，`language_choice` 三語皆勾 metadata／captions／dub，無 skipped locale。
- `review-push --gate publish` 成功送出後，唯讀 API 讀回最新卡 `9ccad952-cb3b-45f6-8f8b-8ae71f0fda8d`、`content_sha256` `6DDB8856C732C835DBD46BB26836F5F1911EED677CCABA2F0C602BB78C6BEEE9`、**approved**（`2026-10-17T03:33:10.212209Z`）；`review-pull --gate publish` 已將此核准寫入本機。
- `review-push --gate languages` 成功送出；初次唯讀 API 讀回最新卡 `abeb9cc0-20e8-409b-b972-c379072fcfcb`、manifest／`content_sha256` `8E5DD6E09FDC943F0AB6A4FB8A04F0859D8A885144CF044F698CCA5FAF74B61F` 為 **pending**。站主回覆已核准後，唯讀 GET 讀回同一卡 **approved**（`2026-10-17T03:37:04.574729Z`）；本機 `review/languages.json` SHA-256 完全吻合，`review-pull --gate languages` exit 0，根目錄 `approvals.json` 已記錄同一 SHA。
- 語言卡核准時，`status --slug curio-h12` 顯示 upload package 完成、on YouTube 尚未完成。此為上傳前快照；後續後台已有影片 ID，見下節。

## YouTube 私人影片唯讀讀回

- 2026-10-17 07:12 UTC，以本機影片工具權杖對 `GET /api/video/reviews/curio-h12` 做唯讀讀回。最新 `publish` 卡 `9ccad952-cb3b-45f6-8f8b-8ae71f0fda8d`（SHA-256 `6DDB8856C732C835DBD46BB26836F5F1911EED677CCABA2F0C602BB78C6BEEE9`）及最新 `languages` 卡 `abeb9cc0-20e8-409b-b972-c379072fcfcb`（SHA-256 `8E5DD6E09FDC943F0AB6A4FB8A04F0859D8A885144CF044F698CCA5FAF74B61F`）仍為 `approved`。
- 後台顯示 `stage=on YouTube`、`youtube_video_id=QJVtVFecm7I`，連結 <https://www.youtube.com/watch?v=QJVtVFecm7I>；`youtube_publish_at=null`，沒有已排程或已公開的證據。
- `youtube_sync.status=done`、`finished_at=2026-10-17T04:41:15.409775Z`。請求紀錄為 `mode=upload`、`visibility=private`、`accept_private_lock=true`；上傳步驟標示「專案還沒通過稽核，YouTube 會鎖成私人」。這是**網站 API 上傳**的後台紀錄，不能記成站主先前表示將使用的 YouTube Studio 網站上傳；是否真的只能保持私人，仍需查看 Studio 可見度選項。
- 同一筆同步的 `details`、繁中／英／日／韓 `captions` 及主縮圖步驟均記為 `done`。英／日／韓 `dub` 各記為 `uploaded`，但這是後台按鈕狀態，不能獨立證明 Studio 音軌可播放；專屬語言縮圖也尚無 Studio 顯示證據。仍待站主確認試播的是同一影片 `QJVtVFecm7I`，逐一切換四語音軌及字幕，檢查英／日／韓專屬縮圖與可見度選項。本次沒有代傳、重傳、排程或公開。
- 本機 `docs/videos/curio-h12/video.json` 的 `youtube.video_id` 仍為 `null`，因此本機 `status --slug curio-h12` 暫列 `[ ] on YouTube`。這是本機 ID 同步缺口，不推翻後台持久化 ID；已有獨立任務追蹤手動影片 ID 同步，這次不改已核准的 `video.json`。

2026-10-17 後續 Studio 唯讀稽核發現三語音訊與專屬縮圖欄均未顯示已發布項目；見 [Studio 稽核收據](studio-audit-20261017.md)。上文的後台 `uploaded` 狀態仍保留為當時讀回，不代表 Studio 已有可播放音軌。

站主隨後選定由 Studio 網站另建 H12 私人影片，並保留舊 API 片 `QJVtVFecm7I`。新片網址／ID、三語音軌、四語字幕、語言縮圖與四語試播均待完成及讀回；本機上傳包不變，後台目前連結舊 ID 的紀錄也尚未更新。交接詳見同一份 [Studio 稽核收據](studio-audit-20261017.md)。

## 費用與範圍

本次字幕、打包、送審沒有付費供應商呼叫；沒有改任何三語譯文、音檔或已核准繁中成片。共用估算停手帳本讀回 H12 US$6.435／8.50、五集 US$28.4295／41.50，無 active reservation；此為保守估算，非供應商發票。
