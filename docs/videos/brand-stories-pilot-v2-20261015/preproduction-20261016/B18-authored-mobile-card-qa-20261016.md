# B18 作者章稿：手機尺寸字卡前檢

2026-10-16。這是離線靜態畫面檢查；沒有匯入、配音、產圖、成片或付費呼叫。使用六章候選的官方合稿 `video.json`，以正式 `slideHtml`／`openRenderer.capture` 逐張輸出 19 張 1920×1080 title 卡，再縮為實際 320×180 像素檢視。渲染器回報 **0 項版面、字型或資源錯誤**；這不等於手機可讀性通過。

## 結果

- 19 張的主標均未裁切或重疊；大部分來源徽章與副標在 320×180 仍可辨識。`now-s095` 的兩行年份和 `now-s098` 的實績／當時預估數字沒有互蓋，但後者資訊密集，正式播放仍須看停留時間。
- **`idea-s027` 尚未通過手機可讀性。** 它的來源徽章與主標都列出 J-Net21／發明協會，副標再以三小行寫「兩份沿革記載／J-Net21 記載／發明協會記載」；縮到 320×180 後三行明顯過小。正式採用前，應在隔離的新候選裡精簡或分層呈現這三行，保住兩份來源的歸屬，重新渲染並獨立審查。不要直接改已釘選的作者六章或把來源標示刪掉。
- 已另備 [單卡修訂候選](B18-mobile-card-revision-candidate/README.md)：只把該卡三行重複來源的副標收為「兩份資料，兩種說法」，保留主標與徽章的來源名；正式模板重新渲染 320×180 圖，0 個機械版面問題。[獨立審查](B18-mobile-card-revision-candidate/independent-review-20261016.md)對這一張靜態字卡給出限定 PASS，不回寫原章，也不代表整片手機觀看或外部事實查核通過。
- 這 19 張只是靜態卡。卡片在剪輯中的停留時間、手機實際播放器、中文字幕遮擋、來源是否與當句旁白同步，仍需看片。

## 可重核的輸入與輸出

| 項目 | SHA-256 |
| --- | --- |
| `B18-authored-chapters-candidate/synthetic/docroot/docs/videos/story-conveyor-belt-sushi-v2/video.json` | `3e39c24f64b1a719fa338db39578fbf1e31f1f95058b66c8544f934f3bffff7e` |
| `B18-authored-chapters-candidate/chapters/idea.json` | `159a25dc1a13ac1247467507064625f3599db535500c67a88c490cebaff763b1` |
| `tools/video/templates/theme.css` | `ae26b5b6c920b2d2cfffa45bdc0c181a996c7cd3689cc9769d6186875df360c5` |
| 19 張縮圖聯絡表 `contact-320x180.png` | `c74f9b1a8348db050647cd0250826eb887c0b51342c90326090aafe927b85f2d` |

19 張 PNG、聯絡表與每張的 `problems` 紀錄暫存於 `<local-temp>/brand-b18-mobile-card-qa-20261016/`，未納入 Git；原章稿與所有審查收據均未變動。這項結果是新的畫面 HOLD，不改變先前 37 檔結構覆核的限定 PASS，也不把 #1518 的採用阻擋視為已解決。
