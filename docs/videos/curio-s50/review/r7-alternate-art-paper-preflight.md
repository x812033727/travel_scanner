# S50 R7｜停工後的新三景插圖書面預檢

2026-10-20 UTC。**新候選的史料／書面畫面界線 PASS；新圖、評審及原圖驗收 NOT RUN。** [既有兩輪原圖裁決](r7-pilot-second-native.md)是 **0／3 KEEP、STOP**；本頁另立一套紙上方案，不延長已用盡的舊方案重試，也不改 `video.json`、`look`、旁白或任何媒體。網站劇本／音訊卡仍是 `hand_pushed pending`。

## 核對基線

- 凍結創作 SHA-256：`brief.md` `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b`、`research.md` `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95`、`claims.md` `4e07795ddf55b4b686431851664cb1c686333233417e378b87b9e96c1180bedc`、`video.json` `603dc5bbde9737dcce0cb2327cdb4db698bfd5fac7dba07e21e3bf86278a1cc1`、`script.md` `5f9ae7f8b89b5f898c982dd51215c5d148901820bf715e10e6d43f8872ef782b`。現版有 **113 個插圖景**。
- 我重新下載 [1667 年證詞刊本 A L147–153、465–480](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L465-L480) 與 [Vincent 1667 年回述 V L2174–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2174-L2206)：原文 SHA-256 分別為 `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`、`36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`，與研究表相符。A 記火從布丁巷麵包師住屋開始、後錄屋主自辯地面鋪磚；V 回述火沿坡往橋邊。兩份都**沒有拍到點火瞬間，也沒有驗證屋內具體擺設或動作**。
- 我在原始 1280×720 JPEG 重新看了第二輪 `fire001-1.jpg`（`c9655cc1…`）、`fire013-1.jpg`（`c1a8738b…`）、`fire096-1.jpg`（`c5021bfa…`）。第一張睡者睜眼、窗外近代感；第二張兒童貌乘車、橋像城門且沒有火線；第三張單人與磚地較接近，焦點卻變成手指下的凸起獨立磚。這些是[第二輪原圖裁決](r7-pilot-second-native.md)的具體失敗，不能因自動 judge 對其中兩張標 `passed: true` 就轉成 KEEP。

## 三景新的候選 prompt 與原圖判準

以下英文是**未寫入 `video.json` 的完整替換候選**。為避開兩輪中反覆出現的童貌人物、睡者睜眼和拉車失敗，前兩景讓火／煙成為單一主動作；火源屋及街景都是時代與內容相關的卡通示意，不是現場重建。第三景改用成人看向**整片平坦地磚**，不再要求伸出食指指認一塊磚。`look` 仍只由既定 `cute-mystery` preset 指定。

| 景 | 新候選 prompt | 原生尺寸 **KEEP** 必要條件與來源界線 |
| --- | --- | --- |
| `fire001` | `Wide shot of a narrow timber-lined lane in 1666 London before dawn, thin smoke rising from the roof of one small house with closed wooden shutters, soft grey light` | 一棟舊式木屋有可見煙、窗板關閉，時間讀作凌晨；**不需畫睡者**。不可出現醒著的「睡者」、兒童被指成屋主、現代玻璃牆／城市燈或具體點火者。A 只支持屋址與時段；關窗、屋形是無可讀字的示意。 |
| `fire013` | `Wide shot from the Thames bank at grey dawn in 1666 London, a low stone-arched bridge crosses the visible river with small timber houses on its deck; a sloping lane of timber roofs on the near bank leads down to the bridge as a small line of flame advances along those roofs` | **河水在石拱下、屋舍在橋面上**，近岸坡街與火線在通往橋的一側能讀出；可有普通背景人，但不能讓人物或手推車主導故事。城門／懸索橋、現代道路或火已越過橋而無來源皆 REJECT。V 是事後回述路線，不能當成精確逐街地圖或目擊攝影。 |
| `fire096` | `Low medium shot inside a plain timber-walled room in 1666 London, one middle-aged adult baker in a linen apron looks down at a broad flat brick-paved floor filling the foreground, soft lamplight from the side` | **整片連續、平坦的房間地面**清楚鋪磚；一名可辨成人只是看向地面。凸起獨立磚／盒變焦點、巨大磚造壁爐、活火或「驗出」火源皆 REJECT。A 只載 Farriner 事後說法；人與室內尺寸為卡通示意，不是經核實的火場照片或口供當場動作。 |

上述判準只退與旁白、來源或系列畫風衝突的圖；卡通化的次要細節、非可讀塗鴉、與原件不同的普通木料質感不單獨構成退圖理由。九題機器評審與獨立原生尺寸內容判讀均須記錄，`-trim.jpg`、接觸表及生成成功率不能代替原生圖驗收。若新候選仍反覆畫不出橋面與地磚，須另設**新的**整集視覺方案，不把退圖換成大批字卡；正文仍須達系列插圖占比至少 70%。

## 新方案的門檻、額度與累計費用

1. 額度恢復後先重查精確稿、網站卡、`media-status` 和 ledger，再由作者把三句採入 `video.json`，跑 lint 並請未撰詞者覆核**新版**書面分鏡；改 prompt 會改分鏡雜湊，不能轉移舊版 storyboard 核准。先僅各產一張 `fire001/013/096`，每張做 judge，另開原生 1280×720 圖記 SHA、九題及逐條 KEEP/REJECT 理由。
2. **新方案放量門檻是 3／3 原圖 KEEP**。這三處都是前兩輪未解的核心主物件；不能用一處容易景掩蓋仍錯的橋或地面。首輪任一景 REJECT，先停其餘 **110** 景和配樂；每個失敗景只准一次有界 prompt 修詞、另由未撰詞者覆核，再各重畫一張。第二張仍 REJECT 即停**這個新方案**，不買第三張湊分數，也不沿用舊 STOP 前的六張拒收圖。三景通過也只放行按精確版逐張評審其餘圖，並不等於全片通過。
3. 本次即時 `media-status` 顯示圖片生成 **18,699／20,000**、圖片 judge **20,000／20,000（剩 0）**、配樂 **60／60（剩 0）**。未能評審的新圖不產，不在本月開這項付費試畫或配樂；重啟時依網站當時實際額度，而非本快照。

私有 ledger SHA-256 `2ba2778aa137fff3decda79c86ce320a1b1d4fe7457433b1878e6181ca12f588`：舊方案六張圖與六次 judge **已花 US$0.081**，配樂 0、預留 0。現版乾跑為 113 景、一輪約 US$1.53、三輪約 US$4.58，600 秒 Lyria 配樂約 US$0.08。若新方案全 113 景每景最多三次，以本次實價 `0.081 + 113 × 3 × (0.0035 + 0.0100) + 0.08 = US$4.7375`；因此提出**含舊支出的整集累計硬上限 US$4.75**。原 [US$4.66 上限](r7-media-budget.md)綁舊方案，不自動轉到新雜湊；本書面預檢也不是新的付費核准。若新稿張數、定價或快取狀況改變，先按較高的即時乾跑／ledger 重算一次性上限。未完成全片插圖、音樂、組片、Shorts、最終品質檢查與網站審查前，不稱成片。
