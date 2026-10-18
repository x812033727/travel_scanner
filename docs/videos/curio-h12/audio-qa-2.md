# H12 新版旁白 QA 與送審（2026-10-16）

本收據只對應已核准的 `script.md` SHA-256 `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B`、`video.json` SHA-256 `D16413FCD54ED2AA5FCFD12B88054FCF8B211AA96110C1514184467615AD3BF1`，以及本輪 `timeline.json` SHA-256 `792DC6C9D010FA7EE94884F7631CD3362D1496AF600A2BF7A14381A0D767F699`（`speech_hash` `6839b804e36ff7c7`）。舊時間軸 `EA4FB643…` 的站主音訊核准不適用本輪。

時間軸為 93 句、91 景、30 fps、總長 14,958 幀＝**08:18.600**；`ending-outro` 起於 14,526 幀，故片尾前旁白正文為 **08:04.200**，高於 8 分鐘硬門檻 4.2 秒。這是音訊實測；成片仍須另行品管。

本輪只新錄 `z4u3` 與 `ds8v`，其餘 91 段 WAV 的修改時間均早於舊音訊在後台核准的 `2026-10-16T10:02:51Z`。現行 93 段 WAV 的 SHA-256 全部與 `timeline.json` 逐句 `audio_sha256` 一致，沒有遺失或不符。`z4u3.wav` SHA-256 `FC202D0909E023FF97D60B5F0AC18FF97BF56BCB4650104E09B2014A843FFCD9`；`ds8v.wav` SHA-256 `91906FEEB2A5D14D10D6197BE6A1C5CCB6FAAE6E20D209C6318F778A359AFABA`。已刪的 `d4uq` 不在新時間軸。

`check-audio` 對現行 93 句得到 55 句逐字吻合、10 句同音／標點規則接受、7 句差異判讀接受、21 句仍列旗標。`review/check.json` SHA-256 `6C4ED6F28C5D636381CE93785DDB2070C45DB3601C18446373F0B54B60DABA7E`；`review/check-flags.json` SHA-256 `D6BA9FC338C55FF3A8D8DB9D18E41EF761B3A6DB47A01AE4B0281C837352F4E0`。`check.json` 另保留一列已刪 `d4uq` 的快取轉寫，**不屬於**現行 93 句或上述統計。21 個現行旗標 ID 全數包含於上一版 23 句旗標；消失的是改錄的 `z4u3` 與已刪的 `d4uq`。21 句的 WAV 全部早於前次站主試聽核准，沒有新旗標音檔。

新句 `z4u3`：「外套能告訴我們誰先離站嗎？」自動轉寫逐字吻合；`ds8v` 稿為「但繆爾黑德在報告裡說……」，Gemini 轉寫成「但繆爾赫德在報告裡說……」，其餘語意相同、未列旗標。人名差異無法單靠轉寫確認實際讀音，請站主**只優先試聽新錄的 `z4u3`、`ds8v`**；既有 21 旗標沿用上版已試聽的原 WAV。逐句頁 `review/audio.html` 已重建，SHA-256 `99FD9829B6616317A082AED336478EBE4C9087E65F97B01EF26344B7A9BA50D3`。

`review-push --gate audio` 已把新版音訊送至 `/admin/videos`，回應 `pending`；隨後 `review-pull --gate audio` 讀回「舊版核准已失效、現行版等待站主」。**尚未核准新音訊，也未開始 H12 插畫。** 本輪分流與送審沒有新增付費呼叫或修改共用費用帳本。
