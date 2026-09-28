# 原來如此事務所：畫面識別與片頭

2026-09-28 起草。站主決定**不用吉祥物**（2026-09-28）：這個系列沒有任何固定角色，辨識度由畫風、色盤與「蓋章」這個動作承擔。這份寫全系列共用的 `look`、片頭 3 秒、結尾蓋章與章節卡；片頭三張關鍵影格做一次、每集重用，選定後雜湊記在最後一節。

## 系列畫風

每集 `video.json` 的 `look`：

```json
{
  "preset": "custom",
  "style": "flat editorial illustration, bold clean outlines, limited palette of warm cream #F6EFE3, ink navy #1F2A44, stamp red #D8452F and mustard #E8B64C, soft paper grain, simple shapes, generous negative space, friendly and clear, 16:9 composition, no gradients heavier than two tones",
  "negative": "photorealistic, 3d render, cinematic lighting, text, letters, watermark, logo, brand marks, mascot, recurring cartoon character, extra fingers, deformed hands, cluttered background",
  "candidates": 3
}
```

- 色盤：奶油紙底、墨藍、印章紅、芥末黃。**印章紅只給答案與蓋章**，觀眾看到紅色就知道答案要來了。
- 人物：需要人的畫面用簡化的無臉或極簡五官人物、剪影，不做跨集重複出現的角色，也就不需要設定圖（`characters` 留空，只有旁白）。
- 手：盡量不畫手指特寫；要拿東西時用手部剪影或只畫物件。
- 真實人物、公司 logo、產品外觀：不用 AI 生成相似的臉或 logo，改用剪影、泛稱物件與文字卡；需要真實圖片時走 `screenshot` 模板並標出處。
- 文字一律由卡片場景或合成疊字，不讓圖片模型寫字（`negative` 擋文字）。

## 片頭 3 秒（每集相同，做一次重用）

| 時間 | 畫面 | 運鏡（`camera`） | 聲音 |
| --- | --- | --- | --- |
| 0.0–1.0 秒 | 事務所木門，門上毛玻璃（字由卡片疊上：原來如此事務所／各語系名稱） | `push-in` | 敲門兩聲 |
| 1.0–2.0 秒 | 門打開，空的木桌上一封寫著問號的信（問號由合成疊上） | `drift` | 開門聲 |
| 2.0–3.0 秒 | 紅色印章從畫面上方落下，在信上蓋出「受理」（字由卡片疊上）；畫面裡沒有人 | `push-in` | 蓋章「咚」 |

## 結尾蓋章（每集最後 3 秒）

答案卡（`big` 或 `quote` 卡片，墨藍底）被同一個紅色印章蓋上「原來如此」（該語系的口號，見 [README](README.md)），配同一個「咚」。這一格也是 Shorts 最後導回長片的畫面。

## 章節卡

每章一張：奶油色檔案夾，頁籤是芥末黃、印著章節序號，檔案夾封面是章節標題（`chapter` 卡片疊字）。全系列同一個構圖，只換字。

## 選定紀錄

| 項目 | 值 |
| --- | --- |
| 片頭關鍵影格 1（門） | （檔名與 SHA-256，圖檔留在 repo 外的 `VIDEO_WORKDIR`） |
| 片頭關鍵影格 2（桌上的信） | |
| 片頭關鍵影格 3（蓋章） | |
| 站主確認日期 | |
