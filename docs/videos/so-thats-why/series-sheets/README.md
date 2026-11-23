# 原來如此事務所：系列固定角色設定圖（2026-11-14 現行標準）

站主 2026-11-14 定案：**鎖死《原來如此事務所》雙角色的「2.5 頭身大頭可愛比例（`2.5-head chibi`）＋劇場級動畫光影 × 厚塗水粉質感」標準設定圖**，並與《奇聞檔案局》（3.5 頭身修長比例研究員 `Ada`，見 [`../../history-curiosity/series-sheets/README.md`](../../history-curiosity/series-sheets/README.md)）嚴格區隔，**兩系列人物造型與頭身比完全不同，嚴禁混用或憑文字自由發揮**。

## 1. 必傳標準設定圖路徑（Repo 內正式基準檔）

任何對話或代理呼叫內建 `generate_image` 繪製**有角色的鏡頭**時，`ImagePaths` **必須傳入下方 Repo 內的正式 V2 設定圖**（不可省略 `ImagePaths`，也不可傳入同資料夾早期 `0c3a400c8e981d84.png`／`f8dac008f296a6a3.png` 舊版 MiniMax 失敗檔——舊檔僅保留供早期集數 `series-store.mjs` 雜湊相容，其中舊所長耳垂掛著像耳環的黃鉛筆、舊小問為半閉豆豆眼與無指圓手）：

| 角色 ID | 角色名稱 | 頭身比 | Repo 內唯一標準設定圖（`ImagePaths` 必傳） | 固定造型特徵（嚴禁增減） |
| --- | --- | --- | --- | --- |
| `chief` | **所長** | **2.5 頭身**（`2.5-head chibi` 圓頭短身） | `docs/videos/so-thats-why/series-sheets/characters/chief/chief-canon-v2.png` | 深棕黑髮帶**一束清晰銀灰挑染**，右側低馬尾垂在右肩前；**粗黑圓框眼鏡**＋大而有神的對焦暖棕圓眼；**雙耳乾淨露出、零耳環、零耳後鉛筆**（已移除舊版易變懸浮雙頭尖或耳環的耳後鉛筆）；芥末黃粗針織排釦外套＋白色翻領襯衫＋深墨藍長褲＋暖棕皮鞋；雙手各 5 指分明 |
| `kid` | **小問** | **2.5 頭身**（`2.5-head chibi` 圓頭孩童） | `docs/videos/so-thats-why/series-sheets/characters/kid/kid-canon-v2.png` | 8 歲好奇女孩，亮黑齊下巴短鮑伯頭＋整齊平瀏海＋**頭頂一撮翹呆毛**；**大而圓亮的深棕雙眼帶白色高光**（嚴禁畫成半閉愛睏小點眼）、粉紅腮紅、乾淨雙耳無飾品；深墨藍牛角釦連帽雨衣外套（**亮芥末黃帽兜自然垂在領口**，不戴上）＋深藍長褲＋純白運動鞋；**雙手空手不拿筆記本**、各 5 指分明 |

## 2. 每鏡生圖必帶的角色英文描述句

傳入上述 PNG 至 `ImagePaths` 時，生圖 Prompt 仍須寫明 `2.5-head chibi` 比例與關鍵服裝（避免模型把大頭比例拉長成 6–7 頭身寫實大人）：

- **所長 `chief`**：
  ```text
  the exact same 2.5-head chibi friendly office chief woman from the reference image (big round head, compact cute chibi body), dark brown-black hair with one silver-grey streak tied in a low side ponytail over her right shoulder, bold round black-framed glasses over large expressive warm brown aligned eyes, clean uncovered ears with bare earlobes, warm mustard-yellow chunky knitted button cardigan over a crisp white collared shirt, five clean fingers on each hand
  ```
- **小問 `kid`**：
  ```text
  the exact same 2.5-head chibi curious 8-year-old girl from the reference image (big round child head, compact cute chibi body), short glossy black bob haircut with straight bangs and one playful cowlick on top, large wide-open bright round dark brown aligned eyes with white catchlights and rosy cheeks, dark ink-navy toggle raincoat jacket with bright mustard-yellow hood resting down around the collar, holding nothing unless specified, five clean fingers on each hand
  ```

## 3. 畫面不必每鏡都有人（`nobody: true` 佔比 45%–65%）

- **嚴禁把全集畫成滿滿的大頭站樁講話**：純原理解釋、結構剖面、日常物件微距與數量對照鏡頭一律設 `"nobody": true`（`characters: []`），佔全集約 **45%–65%**；`chief` 與 `kid` 合計約佔 **35%–55%**，留給開場怪事反應、提問猜測、關鍵轉折揭曉與片尾互動。

## 4. 工具 `look` 關卡還原方式

雲端或本機新開一集工作目錄（`<VIDEO_WORKDIR>/<slug>`）跑 `look` 關卡時，除了相容舊雜湊的 `_series/sothatswhy/characters/` 外，可直接將 `chief-canon-v2.png` 與 `kid-canon-v2.png` 放入工作目錄供本集 `ImagePaths` 與備份留存：

```bash
mkdir -p "${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/sothatswhy"
cp -r docs/videos/so-thats-why/series-sheets/characters "${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/sothatswhy/"
```
