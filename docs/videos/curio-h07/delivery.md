# H07《鐵面人》製作交付紀錄

2026-10-14 定稿。此檔記錄繁中影片的製作與可重驗證的收據；原始影像、音訊、成片和上傳包保存在外部 `VIDEO_WORKDIR/curio-h07/`，不納入 Git。

## 已完成與核准

- 100 句繁中旁白長 9 分 26 秒。`check-audio` 完成 100/100；站主試聽後核准，後台 audio gate 於 2026-10-14 07:39:56 UTC 記錄核准，`approvals.json` 的本機拉回時間為 07:50:39 UTC。其後未改旁白句子。
- 59 張插畫逐張檢查，41 個程式卡／來源截圖狀態；站主查看三頁分鏡聯絡表後核准，後台 storyboard gate 於 2026-10-14 11:10:48 UTC 記錄核准。核准的 `keyframes/manifest.json` SHA-256 為 `C06C34938FDBBB7F4D049DB07450E19AD841D45223328C9BD13C9212B2BA8A46`。
- H.264 1920×1080、30 fps、AAC 48 kHz 雙聲道，17785 幀，成片 592.900 秒（9 分 52.9 秒，含片頭品牌），237783317 bytes。`qa` 的 11 項全過，包含聲量、節奏、字幕、事實、縮圖和連結；上傳包的 4 項檢查全過。
- 另從實際 `final.mp4` 抽看 scene 74–78、87–91、95–99 共 15 個畫面，按片頭插入後的時間對齊。文字未截斷、無黑畫面，資料卡和插畫的語意接續可讀。這三段各有約 23–25 秒的資訊卡密集段落，是留待站主觀看時評估的節奏點，不冒充全片人工播放驗收。
- 後台 final gate 於 2026-10-14 12:00:27 UTC 因 11 項自動品管全過，依當時設定**自動核准**。這是系統核准收據，不代表站主已看完成片或接受 YouTube 播放效果。
- 生成媒體帳本 `media/ledger.json` 記錄 US$3.348，含 250 次圖片請求與 248 次審圖呼叫；0 秒付費影片片段。這包含退件與重畫，不等於 250 張成片插畫。

## 精確檔案與雜湊

| 外部工作區相對檔案 | SHA-256 |
| --- | --- |
| `final.mp4` | `34652A4982C010A776E42F3AD70E3D09562FBE6BA7D88A16265187BB818D3893` |
| `captions/zh-TW.srt` | `1AD7DCA6F4CF1FC53862ED244B5D02065C97651FE07A02A9B46AD1913D454751` |
| `upload/metadata.json` | `3575FD54E744FC995AE1D0D7A54190AA628CD98BFE00EF0936A0770015514787` |
| `keyframes/manifest.json` | `C06C34938FDBBB7F4D049DB07450E19AD841D45223328C9BD13C9212B2BA8A46` |
| `review/qa.json` | `8E585FEC3CB193C8E45915923A0A36B59DE8B6E90A97C453A031A6B83810CCA5` |

程式碼和文稿的現版雜湊及史實邊界見 [`verify-2.md`](verify-2.md)。外部 `upload/` 目前含 `final.mp4`、`thumbnail.jpg`、繁中字幕、繁中標題說明、metadata 和 `UPLOAD.md`；預覽另在 `review/preview-34652a4982c010a7.mp4`。包裝時 `languages.json` 仍為 `locales: {}`、`decided_at: null`，表示站主未選後續語言。

## 尚待站主控制的關卡

語言版本須依 `/admin/videos` 的實際選擇製作或確認只出繁中。YouTube 私人上傳、實際播放器檢查、排程與公開均未執行；後台 `ready_to_upload` 仍是 false。交付包提供預覽與上傳材料，不能當作已上傳、已發布或站主已驗收播放的證據。
