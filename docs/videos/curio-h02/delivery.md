# H02 繁中成片與上傳包

2026-10-12（Asia/Taipei）。採用站主已選的 A：從懷特返島看到留言，追索去向與考古線索。站主已明確核准目前分鏡與成片（含四張保留圖），並選擇只出繁中；兩張審核及語言決定均已在正式站保存並讀回。1080p／11:20.5 成片的繁中上傳包已生成，四項包檢查全過，publish 關卡已核准；後台 `ready_to_upload=true`。尚未上傳或公開於 YouTube。

## 成品

實際工作目錄：`C:\Users\x8120\mokaair-work\videos\curio-h02`。來源、查核與製作紀錄在本目錄；媒體及完整收據保留於工作目錄，不放進 Git。

| 成品 | 實際狀態 |
| --- | --- |
| `final.mp4` | 1920×1080／30fps，20415 frames，680.5 秒（11:20.5），204325624 bytes。完整 SHA-256 `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`。 |
| `build/body.mp4` | 正文672.5秒，原音553.175秒（9:13.175），超過8分鐘要求。完整 SHA-256 `a061ad4c1a6b2ce6cdfa745da88afc8d0bf57a3e6e2c67f656bb1cc173654806`。 |
| `captions/zh-TW.srt`、`.vtt` | 134 cues，0問題；依實際片頭加5秒偏移，`burn_in:false`，影片未燒字幕。 |
| `thumbnail.jpg` | 1280×720，主標「不是咒語」；完整 SHA-256 `93427f863a7eb0a42504aa333c46265b3a8e4970cf3a01045a499a38d1f74b25`。 |
| 後台720p預覽 | `review/preview-d86471c94a661023.mp4`，25101154 bytes；完整 SHA-256 `623f66b9e8ceda9dcda4cab8123ee7235c536628756d394ba3fd290997cecdf1`。後台附件metadata與本機衍生預覽檔一致；遠端consumer播放／bytes仍待驗。 |
| `upload/` | 完整成片、縮圖、繁中說明、134條繁中SRT、metadata及操作說明；未含其他語言或配音。metadata SHA-256 `e616ccd4515b2c7ba382b25903a3f9f73fec4ab0e5fce32e46a5e4a46b07d89e`。 |

品牌套件 `mokaair-brand-package-v2-cc`：150幀片頭、20175幀正文、90幀片尾；實際adopted hash `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`。完整旁白與134個逐句音檔保留，沒有為視覺修正重購旁白。

## 驗證與審核

assemble收據exit 0，`checks.json` 為ok true、problems空；音量−14 LUFS、true peak−0.9 dBFS，42個畫面採樣與來源相符。來源、渲染與134句旁白雜湊均綁現行版本；原音、正文及成片完整decode均exit 0。原獨立full audit為290／299通過，當時八項是尚缺語言／核准／上傳包及QA未全過，另一項正文平均幀率嚴格檢查未過：約30.001104而非exact30，video duration比容器短24.74ms；成片probe為30／20415幀／680.5秒。null muxer的重複DTS警告保留，未宣稱人耳聲畫同步已驗收。原收據SHA `2b50bae4122f6398d78d3f135ca05b0bcd59397057ca030fb01e864891cb4fbe`，詳 `production.md`。

實開19張成片抽樣PNG（16正文點＋4片頭片尾界線，共用最後正文格），175項檢查通過，未見阻塞視覺問題；QC SHA `76ba8578e8374404bdb719f97220d49812dfbecf589af6260d24681acfdb82b4`。這是畫面抽樣，完整播放、聽音、外掛CC顯示仍待驗。實際後台人工審核截圖為 `_audit/h02-final-review-browser.jpg`；海報載入可見，播放操作逾時，未報遠端播放已通過。

警告另以純packet metadata核對：正文20175／成片20415個packets，實際PTS／DTS無重複、DTS無非單調；換算30Hz時各有一次兩個時間點落在同格，重現上述null muxer警告。新收據SHA `997c2d22695a00dfdd4a210ae8c05c1b25fd9bd87bbecbf00ff590563b48423e`；沒有重跑decode、修改成片或覆寫原FAIL。精確CFR與完整聲畫同步仍未驗收。

原 `review/qa.json` 綁上述完整成片SHA，**9／11通過**。assemble、render、narration、pace、metadata、facts、thumbnail、policy、disclosure通過；metadata有七個章節。此歷史報告保留原結果，未重新付費評判不變的旁白；語言決定後另做官方字幕單項覆核及上傳包檢查：

- **captions（原報告未過，現行單項已過）**：站主正式選擇只出繁中，後台 `locales={}`、`locales_decided_at=2026-10-11T22:39:38.663108Z`。依官方 `writeLanguages` 同步後重跑 captions，134 cues；獨立以官方 `captionsItem` 覆核通過，沒有把它改稱全套QA重跑或11／11。
- **links**：18引用中兩個Smithsonian網址對自動GET回403。先前實際Chrome已顯示兩篇文章正文、作者及日期，證據在 `_audit/smithsonian-browser-readback-20261012.json`；不把瀏覽器可讀改寫成自動GET已通過，也不刪除正確引用。

`2026-10-11T22:42:39.555Z` 的實際後台讀回：

| 關卡 | Review ID／綁定 | 狀態 |
| --- | --- | --- |
| 大綱 | `bf2328c0-0b5e-4edb-ac0e-ac951b0278c1`／brief `7475f2d9…` | approved，choice A。 |
| 旁白 | `b958b6ae-0978-4cb1-92e0-ca58829020b2`／timeline `4c9de49b…` | approved。 |
| 分鏡 | `e8cbd0f9-bf91-4a9b-b8f9-8fff70d9a946`／manifest `92961cfc…` | approved，決定時間 `2026-10-11T22:36:39.268917Z`。 |
| 成片 | `a3f6b386-f6ec-41ce-a5e2-9ded114a605b`／final `d86471c9…` | approved，決定時間 `2026-10-11T22:38:46.372034Z`。 |
| 上傳包 | `fb4ff837-1f5b-4a32-8f7e-baa27a251f9d`／metadata `e616ccd4…` | approved，決定時間 `2026-10-11T22:41:53.985239Z`，4項齊全依設定自動核准。 |

站主原答覆為「核准分鏡與成片，只出繁中（建議）」；`review-pull` 已將兩項正式批准綁定目前本機雜湊。三筆歷史audio版本stale不否定當前音訊核准。舊 `_audit/consumer-audit-2026-10-11T21-28-49-609Z.json` 的pending錯誤保留；不覆寫歷史結果。批准與語言收據 `_audit/owner-approval-language-receipt-20261012.json` SHA `cf98d557c041ff595fadb8671ff31c694d0fff1526e2e3f68ed80697d92b9bf7`。

上傳包獨立覆核42／42通過，收據 `_audit/zh-TW-package-independent-readback-20261012.json` SHA `c4cbcb47eb0a3935a47052b44d79d27dfdcfef2e1bb4e7c81192e30df92ed3ca`。官方 `readPackageReport` 四項全過、final完整實拷SHA相同；字幕、七章、說明與來源逐項相符。這是包內檔案與來源驗證，不代替Studio播放器字幕顯示或實際上傳。

publish 的五個附件（成片、縮圖、metadata、繁中說明及SRT）已在正式站讀回；`ready_to_upload=true`、`youtube_video_id=null`。原始 `stage` 字串雖寫 `on YouTube`，它表示下一步，不能當成已上傳證據；瀏覽器實際顯示「可以上架」而「已上YouTube」未勾。畫面證據 `_audit/h02-ready-zh-TW-20261012.jpg`。

最終publish讀回覆核41／41通過，收據 `_audit/final-publish-package-independent-readback-20261012.json` SHA `8e3442f4c7c3761e6d85066739aa74009f5cb4ba7bda8e0f8b41ab9b2ed3455c`。正式附件metadata的五組完整SHA／size／type與本機實檔相同，本機當前audio／storyboard／final／publish批准皆有效；遠端附件consumer GET實際bytes及完整播放仍未另驗。

## 四張保留圖

僅下列實際selected takes保留，原judge、所有候選及fullSHA均在manifest／不可變快照中；不用其他seed的瑕疵判斷現在選用圖。站主本次已核准包含這四張圖的分鏡與成片，原judge偏差仍保留：

| Shot | 實際選用 | 本次實看結論 |
| --- | --- | --- |
| `farewell-grandfather` | `farewell-grandfather-1-trim.jpg` | 年長懷特與搖籃內容可辨，畫風偏差；非其他seed的浮空搖籃。 |
| `farewell-newborn` | `farewell-newborn-1.jpg` | 選用嬰兒閉眼睡眠，畫風偏差；非其他seed的睜眼版本。 |
| `h02-find-origin-not-carrier` | `h02-find-origin-not-carrier-1.jpg` | 無臉／文字的器物來源示意，手托碗底可辨，畫風偏差。 |
| `h02-find-other-explanations` | `h02-find-other-explanations-2-trim.jpg` | 單片陶片與抽屜示意，小背景儲物箱標記偏差；非未選seed的水印。 |

依 `youtube-video` skill及 [ILLUSTRATED.md的保留圖規則](../ILLUSTRATED.md)第453行：「有保留圖的成片一律不自動核准，審核卡片要把保留的圖列出來。」本集審核payload已附完整四張清單與原意見，站主已對現行成片明確核准。

## 接續

1. 本機上傳包位於 `C:\Users\x8120\mokaair-work\videos\curio-h02\upload`；[H02後台](https://mokaair.com/zh-TW/admin/videos?video=curio-h02) 保存正式決定及附件。
2. 實際Studio上傳及公開由站主決定。成片與分鏡批准已完成，不需要重問；上架包完成不表示已上YouTube。
3. 包內metadata類別為27（教育）。共用UPLOAD模板原本誤寫「科學與技術（27）」；本集本機操作說明已只改正該標籤，原檔與前後SHA保存在 `_audit/upload-instruction-label-correction-20261012.json`，未改metadata或五個上傳附件。共用模板修正另由 `2026-10-11-render-upload-checklist-category-labels-from` 追蹤。

詳細來源差異、原134句音訊、付費紀錄與收據在 `production.md`、`audio-rewrite-review.md`、兩份visual review。圖片／評圖ledger重算US$1.9915，無pending jobs或reservation；這不是整片所有供應商費用總額。
