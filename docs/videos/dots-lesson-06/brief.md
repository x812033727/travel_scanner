# 第 06 課製作 brief：雲端與本機電腦：檢視、接管、交還與撤銷

狀態：文字製作包已備妥；真實畫面、旁白音訊、剪輯成片與公開核對均待完成。

觀眾學習成果：找出任務使用的電腦，完成接管與交還並確認登入狀態不會自動同步。

格式：逐步畫面示範，以真實 dots 介面截圖按操作順序串接；保留 Mokaair 品牌，使用台灣口音繁中旁白。
長度：目標整片 8–15 分鐘；旁白正文與示範正文至少 480 秒，片頭片尾不能補足正文。
口播估計：535.7 秒（每分鐘 250 單位）；此值是排稿估計，尚未測量音訊或成片。

| 製作項目 | 當前狀態 |
| --- | --- |
| 逐課真實 dots 操作與結果 | 待驗收收據綁定 |
| 真實截圖與遮罩 | 待擷取／逐張覆核 |
| 台灣口音音訊 | 待合成或錄製與聆聽 |
| 成片、字幕與實際章節 | 待剪輯及對時 |
| 縮圖、上傳與公開 | 待完成；尚未上傳／公開 |

畫面製作：依 shots.csv 的步驟取真實畫面，加入可讀的游標指引、必要重點放大與文字疊字。操作結果必須實際開啟；原創教學圖不能替代產品介面或實測結果。
製作交接：[全套交接紀錄](../../dots-series/HANDOVER.md)；本課擷取順序與逐段指示在 [shots.csv](shots.csv)。

文章預定網址（尚未公開）：https://mokaair.com/zh-TW/life/dots-lesson-06
總目錄預定網址（尚未公開）：https://mokaair.com/zh-TW/life/dots-guide

錄音前重查官方來源與帳號條件；錄製日期留白，完成錄製後才填實際日期。所有原始截圖、影音檔與私有驗收收據保存在 repo 外。
upload-draft.md 和 shots.csv 的時間僅為估計；不得用來宣稱成片章節或字幕同步已驗收。
完成真實影音覆核後才產出繁中 SRT、實際章節與最終上架包。YouTube 上傳及按下發布由站主在 Studio 完成。

## 接續既有畫面產線

現有入口為 tools/video/render/plan.mjs、tools/video/render/cli.mjs；素材與場景使用 tools/video/core/schema.mjs 的既有格式。逐步游標、框選、點擊波紋與放大由 tools/video/screencast/scene.mjs 提供，不新增影片引擎。

screencast 場景的 data.steps 使用 goto、wait、click、fill、capture、mask；capture 可帶 focus 與 zoom（1–2.5）。每個 capture 對應一個狀態，台詞 reveal 合計為截圖張數減一，第一句不 reveal。範例格式在 tools/video/screencast/fixtures/tutorial/video.json。

擷取產物位於 repo 外 <workdir>/<slug>/screencast/<key>/manifest.json，含 viewport、scale、captured_at；每張 capture 含 file、sha256、target（x/y/w/h）、press、zoom、masks。renderer 依這些真實擷取資料繪製游標與重點效果。登入頁由站主使用既有登入 profile，需逐張遮罩並覆核。

單張 screenshot 場景使用 data.image（已遮罩、位於 apps/web/public/ 或 docs/videos/ 的 PNG/JPEG/WebP）、data.highlight（x/y/w/h 百分比）及 caption；這個模板提供框選。桌面 App 原始錄影與截圖維持在 repo 外，人工剪輯完成後可依既有 import 流程交入 final.mp4 與 meta.json。

目前阻擋：02、03 尚待真實試拍及畫面／旁白節奏核對；未建立本課 video.json 與對應 capture manifests，未有音訊／成片。先完成兩課樣本驗收，再製作其餘成片；作者稿通過不能代替試拍。

完成真實操作、來源覆核並把稿件映射為既有 video.json 後，先執行本機檢查與配額預估：

```powershell
node tools/video/cli.mjs lint --slug dots-lesson-06
node tools/video/cli.mjs tts --slug dots-lesson-06 --workdir C:/Users/x8120/mokaair-work/dots-videos --dry-run
```

音訊與 capture manifests 依既有關卡就緒後，才接續既有 render、assemble、captions、qa、package。此製作包尚未執行這些媒體階段；不送出付費請求或自行使用登入 profile。
