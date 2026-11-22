# 《<系列中文名>》（`<series-slug>`）個別規則與設定

> **新系列啟動範本**：複製本檔為 `docs/videos/shorts-drama/series/<series-slug>.md`，把 `< >` 內容全部填滿後，登記進 [`../README.md`](../README.md) 系列索引、[`../preflight.mjs`](../preflight.mjs)（`SERIES_DIRS` 與專屬規則）與 [`../../rules-sync/manifest.tsv`](../../rules-sync/manifest.tsv)，並跑 `node --test docs/videos/rules-sync/sync.test.mjs docs/videos/shorts-drama/preflight.test.mjs` 驗證。

這份是《<系列中文名>》的**系列個別區**。所有零台詞 Shorts 共用的黃金五拍、9:16 介面安全區、無縫重播迴圈、單人框、第 0 關 AI 避險與四階段審核規則，見共用區：[`../README.md`](../README.md)、[`../WRITING.md`](../WRITING.md)、[`../PRODUCTION-ROUTES.md`](../PRODUCTION-ROUTES.md)、[`../REVIEW.md`](../REVIEW.md) 與 [`../../lessons/shorts.md`](../../lessons/shorts.md)。

---

## 一、系列定位與固定角色（鎖定外觀錨點）

- **題材一句話**：<誰> 在 <哪裡> 想 <做什麼>，結果 <怎麼出錯或反差>，最後 <怎麼反轉收尾>。
- **目標受眾與轉傳動機**：<會讓誰想傳給誰，例如：健身族傳給一起去健身房的朋友／情侶互傳>。
- **雲端硬碟路徑**：`AI/備份/Shorts/<系列中文名>/`
- **主場景**：<寫明封閉、無路人、無字招牌的固定背景設計>。
- **定妝照原則**：所有角色定妝照一律**平靜、閉嘴、無道具、純色背景**。

| 角色 ID | 稱呼與關係 | 英文 `intros` 鎖定錨點（每集照抄，絕不改服裝與毛色） |
| --- | --- | --- |
| `<char1>` | <主角名與身分> | `the photo of <Name>, a real <species> in <distinctive outfit>: keep his/her face, fur and <outfit>, change the pose and place as described` |
| `<char2>` | <配角名與身分> | `the photo of <Name>, a real <species> in <distinctive outfit>: keep his/her face, fur and <outfit>, change the pose and place as described` |

---

## 二、本系列專屬五拍公式（11–16 秒、5–6 鏡）

| 拍點 | 建議秒數 | 本系列固定演法 | 必備剪接與聲音參數 |
| --- | --- | --- | --- |
| **① 鉤子（Hook）** | `1.8 – 2.4s` | <第 1 格直接呈現的異常或衝突，並交代誰、在哪、在幹嘛；不寒暄、不走進場> | 開場物理音效（`@0.0–0.3s`） |
| **② 停頓反應（Micro-Pause）** | `1.0 – 1.5s`（訊號鏡 `≥ 1.5s`，畫出看得出是誰的一角） | <微表情、耳朵貼平、眼珠一飄或慢轉頭> | 轉折處設 `music_off: true`＋`hold: 0.4s` |
| **③ 因果鏡＋誇張結果** | `1.8 – 2.4s` ＋ `2.2 – 3.0s` | <先一顆鏡畫出誰對誰做了那個關鍵動作，再硬切直接呈現完成後的誇張造型或處境> | 英文必寫 `<Name> himself/herself is...` |
| **④ 升級／小破綻** | `1.8 – 2.4s` | <旁人當真配合或出現意外破綻／蓄力前兆> | 具體物理音效打點 |
| **⑤ 結尾反轉＋定格／迴圈** | `1.5 – 2.5s` | <最後補一刀反轉，或無縫接回第 1 格形成 Loop> | 看得到結果與角色反應；`hold ≥ 0.8`＋`music_off: true`＋收尾重音（早於鏡尾 ≥ 0.5s） |

- **系列固定 BGM**：<輕快節奏類型，例如：俏皮撥弦／爵士鋼琴，標註曲檔名>。
- **標題公式（只寫情境鉤子、絕不破梗）**：`<日常衝突情境> #<系列標籤>`。

---

## 三、本系列專屬 AI 避險與禁忌

1. **單人框與分鏡規則**：<是否嚴禁雙人同框？對手戲怎麼拆正反打？>
2. **道具與毛爪避險**：<本系列最常出現的細小道具，如何改放桌上／胸口＋`two furry front paws, no human fingers`？>
3. **場景路人與文字防護**：<本系列場景易出現什麼路人或招牌？強制加哪句正面封閉背景與 `plain, unbranded, no text, no logos`？>
4. **9:16 安全區構圖重點**：<本系列的核心表情與破綻道具放在畫面哪個區域，確保不落入右側 16.5% 按鈕欄與底部 28% 標題區？>

---

## 四、前三支試片規劃（先做 3 支過盲評與實測再擴季）

> 新系列一律先寫 3–5 集五拍卡進階段一 100 分三位獨立盲評（中位數 `≥ 70` 且無 `≥ 2` 位同鏡滑走），挑最高分前 3 支開拍（可走 Colab H3 或 Google Flow Veo 3.1）。

| 集數 | 代號（`slug`） | 一句話前提（誰／在哪／做什麼／出什麼錯／最後怎麼反轉） | 縮圖最強格 | 階段一盲評中位數 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| EP1 | `<series-slug>-e01` | <一句話前提> | <鏡號與畫面> | 待盲評 | 企劃中 |
| EP2 | `<series-slug>-e02` | <一句話前提> | <鏡號與畫面> | 待盲評 | 企劃中 |
| EP3 | `<series-slug>-e03` | <一句話前提> | <鏡號與畫面> | 待盲評 | 企劃中 |

---

## 五、本系列實戰修正與數據紀錄

- 上架 7 天／28 天後，把實測有效的笑點結構與失敗教訓補在這裡，跨系列共用的教訓同步寫入 [`../../lessons/shorts.md`](../../lessons/shorts.md)。
