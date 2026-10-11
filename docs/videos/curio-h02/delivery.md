# H02 成片與待審事項

2026-10-12（Asia/Taipei）。採用站主已選的 A：從懷特返島看到留言，追索去向與考古線索。1080p 成片及繁中 CC 已生成並送審；分鏡與成片待站主決定，上傳包尚未生成。YouTube ID 在最新後台讀回中仍為 null。

## 可審看的成品

實際工作目錄：`C:\Users\x8120\mokaair-work\videos\curio-h02`。來源、查核與製作紀錄在本目錄；媒體及完整收據保留於工作目錄，不放進 Git。

| 成品 | 實際狀態 |
| --- | --- |
| `final.mp4` | 1920×1080／30fps，20415 frames，680.5 秒（11:20.5），204325624 bytes。完整 SHA-256 `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`。 |
| `build/body.mp4` | 正文672.5秒，原音553.175秒（9:13.175），超過8分鐘要求。完整 SHA-256 `a061ad4c1a6b2ce6cdfa745da88afc8d0bf57a3e6e2c67f656bb1cc173654806`。 |
| `captions/zh-TW.srt`、`.vtt` | 134 cues，0問題；依實際片頭加5秒偏移，`burn_in:false`，影片未燒字幕。 |
| `thumbnail.jpg` | 1280×720，主標「不是咒語」；完整 SHA-256 `93427f863a7eb0a42504aa333c46265b3a8e4970cf3a01045a499a38d1f74b25`。 |
| 後台720p預覽 | `review/preview-d86471c94a661023.mp4`，25101154 bytes；完整 SHA-256 `623f66b9e8ceda9dcda4cab8123ee7235c536628756d394ba3fd290997cecdf1`。後台附件metadata與本機衍生預覽檔一致；遠端consumer播放／bytes仍待驗。 |

品牌套件 `mokaair-brand-package-v2-cc`：150幀片頭、20175幀正文、90幀片尾；實際adopted hash `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`。完整旁白與134個逐句音檔保留，沒有為視覺修正重購旁白。

## 驗證與審核

assemble收據exit 0，`checks.json` 為ok true、problems空；音量−14 LUFS、true peak−0.9 dBFS，42個畫面採樣與來源相符。來源、渲染與134句旁白雜湊均綁現行版本；原音、正文及成片完整decode均exit 0。獨立full audit為290／299通過，八項是尚缺語言／核准／上傳包及QA未全過，另一項正文平均幀率嚴格檢查未過：30.001103668而非exact30，video duration比容器短24.74ms；成片probe為30／20415幀／680.5秒。null muxer的重複DTS警告保留，未宣稱人耳聲畫同步已驗收。原收據SHA `2b50bae4122f6398d78d3f135ca05b0bcd59397057ca030fb01e864891cb4fbe`，詳 `production.md`。

實開19張成片抽樣PNG（16正文點＋4片頭片尾界線，共用最後正文格），175項檢查通過，未見阻塞視覺問題；QC SHA `76ba8578e8374404bdb719f97220d49812dfbecf589af6260d24681acfdb82b4`。這是畫面抽樣，完整播放、聽音、外掛CC顯示仍待驗。實際後台人工審核截圖為 `_audit/h02-final-review-browser.jpg`；海報載入可見，播放操作逾時，未報遠端播放已通過。

警告另以純packet metadata核對：正文20175／成片20415個packets，實際PTS／DTS無重複、DTS無非單調；換算30Hz時各有一次兩個時間點落在同格，重現上述null muxer警告。新收據SHA `997c2d22695a00dfdd4a210ae8c05c1b25fd9bd87bbecbf00ff590563b48423e`；沒有重跑decode、修改成片或覆寫原FAIL。精確CFR與完整聲畫同步仍未驗收。

`review/qa.json` 綁上述完整成片SHA，**9／11通過**。assemble、render、narration、pace、metadata、facts、thumbnail、policy、disclosure通過；metadata有七個章節。未通過項目保留原結果：

- **captions**：尚無本集正式語言選擇；工具預設要求zh-TW／en／ja／ko，現已完成繁中，英／日／韓未製作。額外語言依站主每支選擇；沒有為略過檢查而偽造空選擇。
- **links**：18引用中兩個Smithsonian網址對自動GET回403。先前實際Chrome已顯示兩篇文章正文、作者及日期，證據在 `_audit/smithsonian-browser-readback-20261012.json`；不把瀏覽器可讀改寫成自動GET已通過，也不刪除正確引用。

`2026-10-11T21:28:26.297Z` 的實際後台讀回：

| 關卡 | Review ID／綁定 | 狀態 |
| --- | --- | --- |
| 大綱 | `bf2328c0-0b5e-4edb-ac0e-ac951b0278c1`／brief `7475f2d9…` | approved，choice A。 |
| 旁白 | `b958b6ae-0978-4cb1-92e0-ca58829020b2`／timeline `4c9de49b…` | approved。 |
| 分鏡 | `e8cbd0f9-bf91-4a9b-b8f9-8fff70d9a946`／manifest `92961cfc…` | pending；52張passed圖的原soft remarks使正式checker回false，已另開待辦。 |
| 成片 | `a3f6b386-f6ec-41ce-a5e2-9ded114a605b`／final `d86471c9…` | pending；manual_review=true，QA僅供參考。 |

stage文字「storyboard approved」不等於分鏡review已核准；`review-pull` 的native exit 3明示分鏡與成片等待站主。三筆歷史audio版本stale不否定當前音訊核准。`_audit/consumer-audit-2026-10-11T21-28-49-609Z.json` 的四個gate錯誤僅是這兩個review未approved、未有decided_at；全部7個附件的角色／size／本機SHA都相符。此metadata讀回沒有取代遠端實際下載驗證。

## 四張保留圖

僅下列實際selected takes保留，原judge、所有候選及fullSHA均在manifest／不可變快照中；不用其他seed的瑕疵判斷現在選用圖。未通過judge的偏差需要站主在實際成片中審看：

| Shot | 實際選用 | 本次實看結論 |
| --- | --- | --- |
| `farewell-grandfather` | `farewell-grandfather-1-trim.jpg` | 年長懷特與搖籃內容可辨，畫風偏差；非其他seed的浮空搖籃。 |
| `farewell-newborn` | `farewell-newborn-1.jpg` | 選用嬰兒閉眼睡眠，畫風偏差；非其他seed的睜眼版本。 |
| `h02-find-origin-not-carrier` | `h02-find-origin-not-carrier-1.jpg` | 無臉／文字的器物來源示意，手托碗底可辨，畫風偏差。 |
| `h02-find-other-explanations` | `h02-find-other-explanations-2-trim.jpg` | 單片陶片與抽屜示意，小背景儲物箱標記偏差；非未選seed的水印。 |

依 `youtube-video` skill及 [ILLUSTRATED.md的保留圖規則](../ILLUSTRATED.md)第453行：「有保留圖的成片一律不自動核准，審核卡片要把保留的圖列出來。」本集審核payload已附完整四張清單與原意見；大綱A核准未代替成片核准。

## 接續

1. 站主在 [H02後台審核頁](https://mokaair.com/zh-TW/admin/videos?video=curio-h02) 看分鏡及成片，再決定是否核准與本集語言；完整decode及成片抽樣已完成，原未過結果與警告保留。
2. 核准讀回後才執行package、四項上傳包檢查及publish送審；實際Studio上傳／公開由站主決定。

詳細來源差異、原134句音訊、付費紀錄與收據在 `production.md`、`audio-rewrite-review.md`、兩份visual review。圖片／評圖ledger重算US$1.9915，無pending jobs或reservation；這不是整片所有供應商費用總額。
