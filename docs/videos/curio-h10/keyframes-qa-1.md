# H10 分鏡插畫 QA：首次全頁目視 HOLD

日期：2026-10-16（Asia/Taipei）。此收據只對以下位元組有效：`video.json` SHA-256 `2BD58534971AEE99AA2EBAA7428C92C1C2331FC9C0174E4391B55BE8967CB1D4`、`script.md` SHA-256 `A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`、`keyframes/manifest.json` SHA-256 `032E070876C93D793637440C94D8D8D3452F4FCFC9C4EBBB983F0BB7C05F9A50`。本機 MiniMax image-01 圖片和 Gemini 九題評審顯示 **73／73 有圖、73／73 judge passed、0 `needs_review`**。這些機械結果與以下逐頁目視發現並存；不能把這份 manifest 當作分鏡整體已驗收。

| 頁 | 本機聯絡表 | SHA-256 |
| --- | --- | --- |
| 1 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-01.png` | `187BB54D795ABCD2FFC88B1CDAD35CA0651B857E0A6C4F3DFAFABDD23AF978C9` |
| 2 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-02.png` | `3202C765FCF785C4304026C94A8E1564218B2F12BF8F72C30CFC4F20BF17B927` |
| 3 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-03.png` | `B71F5E0E181995F399EF9E5F79549190C754FE04FC6D1C204D0975920C211397` |
| 4 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-04.png` | `429630B08085C1AB4E3751788A5C67B5FCE7BA3DAD527C8BA1D2704F70050CED` |

## 只需定向修的八鏡

下表檢查的是 manifest **選中**的圖片，不是同目錄內未選用的其他 take。第一組與旁白中的特定事件、地點或物件相矛盾；第二組違反無字畫面要求，或會讓觀眾誤讀為真實搜索畫面。修圖時只改這八鏡，保留其餘 65 鏡已付費且已通過的快取圖片。

| 鏡頭 | 選中圖片 | 旁白／應呈現 | 實際畫面與 HOLD 理由 |
| --- | --- | --- | --- |
| `tease-map` | `tease-map-2-trim.jpg` | 因紐特人在海圖上標出沉船位置 | 人物趴在海岸樣的大面積地形上持巨型紅筆；沒有可辨海圖，唯一被敘述的標圖動作變成在海岸上畫。 |
| `ship-cannot-move` | `ship-cannot-move-1.jpg` | 兩艘遠征船受海冰阻住，海圖上的航線走不通 | 三個人坐在無冰的暖色小艇／沙岸，沒有受困船隻；視覺把困冰情境反轉。 |
| `rae-accounts` | `rae-accounts-1-trim.jpg` | 1854 年 John Rae 記錄因紐特人在北極海岸的見聞 | 畫面出現東亞庭院、綠樹與東亞式屋簷，替歷史地點和文化脈絡帶入錯誤訊號。 |
| `plan-written` | `plan-written-3-trim.jpg` | 1848 年補記計畫往加拿大北極的巴克河走 | 選中地圖顯示東南亞海岸及菲律賓群島形狀；將計畫路線放到錯誤洲別。 |
| `fork-shape` | `fork-shape-1-trim.jpg` | 2014 年岸上鐵件形似自行車的前叉 | 手持物是明顯三齒園藝叉，會把這件關鍵線索描繪成另一種物件。 |
| `oreilly-location` | `oreilly-location-3-trim.jpg` | 從無標籤海圖比較 O’Reilly Island 附近位置 | 背景圖有可見的假中文字及假英文地名；`no lettering` 提示未達成，不能讓偽標籤冒充真實地圖資訊。 |
| `identity-scope` | `identity-scope-1-trim.jpg` | 身分確認與未能重建的經歷界線 | 鏡中的姓名卡有可見的假中文字；在身分主題上尤其容易被當作真名，與空白卡提示相反。 |
| `next-day` | `next-day-1.jpg` | 2014 年聲納在海底看到沉船輪廓 | 螢幕是有上層結構、浮於水面的完整現代船圖樣，不像海底沉船的聲納輪廓，容易誤導發現方式。 |

其他圖的景別、手勢、抽象海圖與道具省略按 `curio-episode` 的已過評審圖驗收原則保留；此處沒有把卡通插圖當成史料照片逐件要求考證。`tease-metal` 選中圖仍呈現岸上鐵件，`metal-recall` 仍呈現彎曲鐵件，雖手勢不完全對應提示詞，未列為史實衝突。此輪沒有呼叫付費產圖、沒有修改圖像或稿件，也**沒有執行 `review-push --gate storyboard`**；待八鏡定向修復及新 manifest 重查後才送後台。站主分鏡核准尚不存在。
