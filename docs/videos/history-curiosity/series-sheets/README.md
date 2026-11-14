# 奇聞檔案局：系列固定角色設定圖與兩系列人物區隔（2026-11-14 現行標準）

站主 2026-11-14 定案：**鎖死《奇聞檔案局》專屬人物比例與串場研究員 `Ada` 標準設定圖**，並與《原來如此事務所》（2.5 頭身圓頭大眼雙角色所長＋小問，見 [`../../so-thats-why/series-sheets/README.md`](../../so-thats-why/series-sheets/README.md)）徹底分家——**兩個系列的人物頭身比、剪影、髮型、眼鏡與服裝色盤完全不同，一眼就能分辨是哪個系列**。

## 1. 兩系列人物造型強制區隔表（嚴禁混用）

| 項目 | 《奇聞檔案局》（`curio-*`） | 《原來如此事務所》（`sothatswhy-*`） |
| --- | --- | --- |
| **頭身比與剪影** | **3.5 頭身修長繪本／劇場動畫比例**（`3.5-head slender storybook theatrical anime proportion`：身形修長、青年／成人肩線清楚，**絕不畫成 2.5 頭身圓滾大頭娃娃**） | **2.5 頭身圓頭大眼 Q 版比例**（`2.5-head chibi`：大圓頭、短小身軀） |
| **固定班底角色** | **不開口的檔案局研究員 `ada`**（只入畫翻查線索與反應，全片只有旁白 `Sulafat`） | **開口一問一答的雙角色**：`chief`（所長）＋`kid`（8 歲小問） |
| **髮型與眼鏡** | 黑色微捲齊下巴短髮＋**側分斜瀏海**（無呆毛、無馬尾、無白髮挑染）＋**暗酒紅細圓框眼鏡** | 所長：深棕黑低馬尾＋銀灰挑染＋粗黑圓框眼鏡；小問：亮黑平瀏海短髮＋頭頂翹呆毛、無眼鏡 |
| **服裝與色盤** | **褪色青（`#3B6E75`）雙排釦風衣外套**＋**牛皮紙米白高領毛衣**＋深炭藍長褲＋深棕短靴（呼應 `cute-mystery` 懸疑檔案色盤） | 所長：芥末黃粗針織外套＋白襯衫；小問：深墨藍牛角釦雨衣＋亮黃帽兜 |
| **Repo 標準設定圖** | `docs/videos/history-curiosity/series-sheets/characters/ada/ada-canon-v2.png` | `docs/videos/so-thats-why/series-sheets/characters/{chief/chief-canon-v2.png,kid/kid-canon-v2.png}` |

## 2. 必傳標準設定圖與英文描述句

1. **串場研究員 `ada`**（講到在世／1956 年後過世不可入畫人物，或檔案局翻查帳冊／地圖／證物時出場）：
   - `ImagePaths` **必傳**：`docs/videos/history-curiosity/series-sheets/characters/ada/ada-canon-v2.png`
   - 生圖 Prompt 角色描述句：
     ```text
     the exact same 3.5-head slender theatrical anime female archive investigator Ada from the reference image (visibly slimmer 3.5-head proportion, NOT a round 2-head chibi), wavy jet-black chin-length bob haircut with a sweeping side-parted fringe, thin crimson-red round glasses over calm observant dark brown aligned eyes, clean uncovered ears, muted-teal double-breasted trench coat open over a parchment-cream rib-knit turtleneck sweater, five clean fingers on each hand
     ```
2. **單集可入畫歷史人物**（1956 年以前過世滿 70 年，且在單集跨 ≥ 4 鏡出場）：
   - 開畫關鍵影格前，先以**同樣的 3.5 頭身修長劇場動畫比例**用 `generate_image` 產出一張單人全身無字設定圖（鎖定年代服裝、髮色、鬍鬚／五官），存進該集工作目錄 `characters/<role>.png` 並隨製作檔備份上雲端；該人物出場的每一鏡 `ImagePaths` 必傳該設定圖。

## 3. 畫面不必每鏡都有人（`nobody: true` 佔比 45%–65%）

- **嚴禁為了湊人頭把每一鏡都塞進 Ada 或路人**：歷史器物、航海儀器、火山／船隻／建築場景、無字帳冊封皮與數量視覺比喻鏡頭應設為 `"nobody": true`（佔全集約 **45%–65%**），角色鏡頭（Ada 串場、可入畫歷史人物或匿名時代路人，合計約 **35%–55%**）專注放在關鍵行動、發現異常與情緒轉折拍。
