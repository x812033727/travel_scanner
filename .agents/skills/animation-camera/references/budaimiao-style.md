# 可選風格：布袋喵參考風格

站主已選定：同時學畫風、角色表演、鏡位與剪接感，做成**可選風格**。使用者說「套用布袋喵參考風格」、指定真一隻布袋喵頻道或明確要求這組參考時，讀本篇；其他動畫沿原作品的規格。這是代理選用的導演與美術手冊，**不是** `look.preset` 的新 enum、後台選單或自動工人的設定。

預設 16:9；品牌、片頭、角色聲音、配音與 CC 沿本案 Mokaair 規格。參考的是可移用的製作方法，示例用原創角色與台詞，不把原片、角色造型、音樂或畫面當生成素材。Hailuo 與 Kling 的網頁生成讀 [browser-production.md](../../animation-production/references/browser-production.md)；先依使用者指定的內建瀏覽器路線核對能力，不自動改走先前的 CLI 選擇。

## 1. 來源與觀察邊界

頻道：[真一隻布袋喵](https://www.youtube.com/@%E7%9C%9F%E4%B8%80%E9%9A%BB%E5%B8%83%E8%A2%8B%E5%96%B5)。查閱日 **2026-10-04**，在 Codex 內建瀏覽器開原片，略過廣告後確認正片時長，再取播放器時間碼；未下載原片。下表是**抽樣影格的可見狀態**，不是逐鏡量測或完整動作驗收。時間碼保留到小數只是播放器讀值，沒有這個精度的剪點分析。

| 原片 | 已觀察的正片秒數 | 畫面可見 |
| --- | --- | --- |
| [佛魔終戰・蓮華之擊](https://www.youtube.com/watch?v=NEhqMfAGCQA)，播放器 339.561 秒 | 0.00、6.31、33.95、169.77、271.63、292.01 | 開場口部近距離畫面；地面金色法陣；衣襬與腳部細節；人物持武器的中景；遠景巨大蓮華圖形；胸前衣飾與武器細節 |
| [殺生為護生・佛劍分說詩號](https://www.youtube.com/watch?v=QpAl1SN0HKY)，播放器 29.661 秒 | 8.64、9.54、24.65 | 背身人物、長形武器與天空分層；眼部極近景；人物斜身與穿過畫面的金色光束 |
| [萬里黃沙雙天會・梵天聖炎焚魔障](https://www.youtube.com/watch?v=5QcL49ezzG0)，播放器 332.781 秒 | 33.27、166.37、266.19 | 分居畫面兩側的雙人對峙；持武器人物中近景與精細服裝配件；人物與大型金色能量形體同框 |

**推論／本案採用方向**：細節插鏡、人物表情與尺度全景值得組成同一場戲；衣飾和武器可作身份錨點，光影與特效可表現威壓。

**同日稍後的逐鏡量測**：七支片（含上表的 D 與 A）從頭量到片尾、兩支由另一個代理交叉裁定，紀錄與逐鏡資料在 [reference-study-20261004-budaimiao.md](../../../../docs/videos/drama-craft/reference-study-20261004-budaimiao.md)。補上了上面缺的比例與順序（量到或目視，詳見該檔）：

- 打鬥片中位數約 0.75–1.0 秒（兩支裁定；單支數字不可引用），打鬥段每 0.2–0.5 秒一剪；看得到的真鏡頭最長約 5 秒，只給法印、龍捲、慢推站姿這類不用演的東西。
- 全景 45%、插鏡 11%、畫面沒有人的鏡頭 35%（打鬥六支 23–43%）、以臉為主體的 6–16%。
- 七支只有兩鏡看得到嘴在動，都沒對到字；台詞燒錄成單行字幕，也會壓在臉上，但那張臉的嘴閉著、流血或切出畫面。
- 一擊拆成招式鏈：出手插鏡 → 一閃 → 爆炸或煙塵的全景 → 受力反應；兩人接觸的同框最長 1.75 秒。
- 主角常分段亮相（先腳或道具、再臉、最後中景），進場常先拍腳；每個角色一套配色、能量一人一色，錨點插鏡在一支片裡回來 5–10 次。
- 沒有證據的事：同一支素材在閃光處切成好幾拍（看起來像的五處沒有一處被判成真剪點，多數是同一鏡裡的閃電）。

**仍未驗證**：聲音（配音、配樂、音效）、留存率、運鏡幅度、作者用的模型、一支生成多長、每鏡抽幾次。播放器靜音；不能聲稱聽過。以後有正常速度的連續小樣再驗，不能拿截圖或 judge 通過當相似度已達標。

**跟我們規格不同、要站主決定的**（預設不變）：參考片是 2.33:1 寬銀幕、燒錄字幕、沒有 CC；我們是 16:9、CC。要在 16:9 裡加上下黑邊做成寬銀幕，有效畫面約 1920×817，關鍵影格要照這個安全範圍構圖，先問站主。

## 2. 落到既有 look 與逐鏡欄位

| 層面 | 本案的可執行寫法 | 避免的失真 |
| --- | --- | --- |
| 人物與衣飾 | 國漫式成人比例、清楚眼形與線條、明暗塑形；指定髮結、袖口、扣件、武器數量與持握側。各角色有自己的識別點 | 只寫「高品質國漫」、全員同一張臉；細節每鏡換位置；把寫實皮膚或塑膠反光當精細 |
| 光影與空間 | `look.style` 放媒介與材質；每鏡 `prompt` 寫本場光源方向、前中後景、地面與兩人距離。冷暖分層依場景定 | 全部場景共用金色法陣／泛光；特效和背光淹沒臉、手與接觸點 |
| 表演 | `prompt` 是動作前的首格；`motion` 寫誰、對象、方向、幅度和收勢。布料、髮絲只作次要回應 | 人物站姿展示服裝；手勢無目的；同一鏡要求走位、拔劍、施法和擊中 |
| 特效尺度 | 蓄勢小而集中；出招方向可追蹤；接觸點可辨；大場面重新交代人物尺度與位置 | 用一團亮光遮住接觸；對手沒有反應；特效在空間軸線中突然換方向 |
| 配色（原片看得到） | 每個角色一套配色、能量一人一個顏色，寫進 P2 的色彩腳本；遠景的小人只靠顏色認 | 兩個角色的能量同色；配色在 `look` 核准後才定 |
| 進場與亮相（原片看得到） | 先拍腳踏進畫面，再接上半身；主角亮相分段：腳或道具 → 臉 → 中景，名號是一行字幕 | 第一次登場就給全身走位；做名字卡 |
| 出招預告（原片看得到） | 眼睛的大特寫亮起或轉色，下一鏡出招；臉少而短，嘴閉著 | 說話的嘴停在畫面上；臉的鏡頭比動作還長 |
| 特效與空景（原片看得到） | 約三分之一的鏡頭沒有人（量到）：雷、火、裂地、法陣、巨物，表現尺度與壓迫，也遮住四肢；餘波交給環境與物件 | 每鏡都有角色；用角色動作撐大場面 |

前四列是**創作建議**，不是原片測量值；後四列是在原片目視看得到的做法（時間碼見研究紀錄，只有「約三分之一沒有人」是算出來的比例），寫法仍是我們的建議。先選這套風格並定 `look`，再做設定圖與逐鏡首格；改已核准的 `look` 會使後續媒體與核准失效，照 production skill 處理。

示例 [budaimiao-example.json](budaimiao-example.json) 已提供可讀的 `look`。使用 `preset: "custom"`，由 `look.style` 寫具體的線條、陰影、衣飾和空間；`look.motion` 只寫單一動作、身份與道具穩定，**不含共通運鏡指令**，讓每鏡的 `camera` 決定怎麼動。不要將頻道名稱當模型咒語，也不要把場景光或法陣寫成全片必帶的 `look.style`。

## 3. 原創八鏡：斷橋前的一步

示例是**離線單場戲**，不是已製作的一集。沈星澄守橋，陸衡試探防線；無旁白。攝影機全場在橋台南側，沈在畫面左面向右、陸在右面向左，三米以兩人軀幹的位置量。s01 只把右腳前滑半步擴大站姿，軀幹留在同一塊石板上，不是整個人前進；s07 的十厘米後仰隨收勢恢復，腳沒有移位。沈單劍持右手；陸單杖、左手較靠近中央銅環，轉成橫持也不交換握點。冷天光與右側暖輪廓光屬這場戲，其他場景另定。

| 鏡 | 敘事與 camera | 首格 → 主要動作 → 收勢／接戲 |
| --- | --- | --- |
| s01 | 空間與保護意圖；`Two-shot, eye level, locked` | 劍低、杖直立 → 沈右腳前滑半步擴站姿、軀幹不前移 → 左右位置與軀幹間距不換 |
| s02 | 對手威壓；`Medium close-up, low angle, slow push in` | 杖直立 → 陸轉為胸前橫持 → 雙手握點固定 |
| s03 | 意志與反應；`Extreme close-up, eye level, locked` | 沈眼睛睜開看右 → 小幅瞇眼 → 目光穩定；刻意的短反應鏡 |
| s04 | 武器蓄勢插鏡；`Insert of the sword hilt, locked` | 右手持劍於腰高 → 上提二十厘米 → 劍到胸高、朝右；只畫手、袖口與武器 |
| s05 | 出招；`Medium close-up, eye level, pan right` | 胸前劍尖帶短青弧 → 一道青弧向右離框 → 手臂與劍位置保留 |
| s06 | 接觸；`Over-the-shoulder from behind Shen on Lu, locked` | 青弧離銅環十厘米 → 一次撞杖 → 接點短促火花；近側肩膀不變成正臉 |
| s07 | 力量造成的後果；`Close-up, eye level, slow push in` | 火花餘光、杖橫持 → 陸上身後退十厘米 → 腳留地、杖仍橫持 |
| s08 | 回全景與態度；`Wide shot, low angle, slow pull out` | 雙方仍相距三米 → 沈降劍二十厘米 → 保持橋頭防線 |

鏡長由 JSON 台詞與 `action_seconds` 作**規劃估算**，不是參考片節奏或實測媒體時長。估出的約 21 秒、每鏡約 2.6 秒是**對話節奏版**；照參考片的打鬥節奏，s04–s07 各 1 秒、s01 與 s08 各 2 秒，加上 s02、s03 的台詞，這場約 10–12 秒。s04／s05／s06 的 `action_seconds` 在場景層，`lines: []`；示例未設 anime 類別或長篇 production policy，按有角色的普通短漫劇讀取。正式長篇動畫須依 `long-anime-v1` 的有效 production policy、台詞／音軌時間軸及契約處理動作拍（`tools/video/core/schema.mjs`、`tools/video/core/anime-policy.mjs`），不能靠換 category 規避規格。JSON 的 voice 是完整離線示例用值，不代表試音或配音已完成。

剪接建議：登場／對峙留讀人物的空間，蓄勢細節接出招，出招方向接下一鏡接觸，接觸接對手反應，再回全景。參考片的段落會變速（目視）：對峙約 1 秒一鏡，連擊 0.25–0.5 秒，召喚與餘波 1–3 秒，尾聲 2–4 秒；我們的動作拍最短 1 秒，連擊段先用 1 秒的拍。不要讓每鏡都推近、讓模型代剪或把每支完整生成秒數原封不動留在成片；實際剪點在動作有意義的時刻。下場若人物移位，重新建立軸線與全景。

## 4. 同鏡的 Hailuo／Kling 網頁提示

兩家都上傳**同一鏡核准的首格**，保持 16:9、一個連續鏡頭。下面是英文動態正文，不是圖片提示；美術與構圖先由首格成立。共用句尾：`Preserve the supplied first frame, character identities, costumes and weapon geometry. One continuous shot, no cuts, no added text.` 若 UI 有正式負面欄，貼本集 `look.negative`；沒有就不貼，也不寫進正文（否定句會被畫成正向）。要貼的完整正文由 `animation-preproduction` 的 `shot_plan.mjs` 照各家官方格式組好，這裡的表是它的動作與運鏡那一段。

| 鏡 | Hailuo 動態正文 | Kling 動態正文 |
| --- | --- | --- |
| s01 | `Locked two-shot. Shen slides her right foot half a step forward into a wider stance and stops, her torso staying over the same flagstone on screen left, sword low. Lu remains on screen right.` | `Single locked two-shot. Shen left widens her stance with one half-step slide of her right foot; her torso stays over the same flagstone. Lu stays right; keep the three-metre torso gap and both weapon grips.` |
| s02 | `Low-angle medium close-up, slow push in. Lu rotates his single staff from vertical to a horizontal guard across his chest and stops; both hands keep their grip points.` | `One low-angle medium close-up with a slow push in. Lu on screen right rotates one staff into a chest-level horizontal guard. Preserve the left-hand and right-hand grip points; no extra weapon.` |
| s03 | `Locked extreme close-up of Shen's eyes. She narrows her open eyes slightly toward screen right once and steadies her gaze; no head turn.` | `One locked extreme close-up. Shen looks off screen right, narrows her open eyes slightly once and settles. Keep her eye shape and hair-cord position; no exaggerated expression.` |
| s04 | `Locked insert. The right hand in the silver cuff lifts the single sword hilt twenty centimetres from waist to chest height and stops. The blade remains horizontal toward screen right.` | `Single locked insert of the hilt and right hand only. Raise the one sword twenty centimetres to chest height with the same grip; blade points screen right. Keep the face out of frame.` |
| s05 | `Medium close-up, pan right. One narrow cyan arc travels from Shen's sword tip toward screen right and exits the frame. Her right arm and single sword keep their position.` | `One medium close-up with a pan right. The single cyan arc leaves the sword tip and travels left to right toward Lu off screen right. Keep Shen's chest-height sword and right-hand grip stable.` |
| s06 | `Locked over-the-shoulder view from Shen onto Lu. One cyan arc strikes the central bronze band of Lu's horizontal staff once, with brief amber sparks at that point. His grip stays fixed.` | `Single locked over-the-shoulder shot, Shen's shoulder foreground left and Lu screen right. The incoming cyan arc from the left contacts the staff's central bronze band once. Keep the contact visible, the staff horizontal and both grips unchanged.` |
| s07 | `Close-up, slow push in. Lu recoils ten centimetres through his upper torso from the impact and settles. His feet stay planted and his single staff remains horizontal.` | `One close-up with a slow push in. Lu on screen right recoils ten centimetres at the torso, then settles facing left. Retain his robe clasp and horizontal staff; no fall or new injury.` |
| s08 | `Low-angle wide shot, slow pull out. Shen lowers her single sword twenty centimetres toward her waist and stops on screen left. Lu keeps his guard on screen right; the bridge remains behind Shen.` | `One low-angle wide shot with a slow pull out. Shen left lowers her sword twenty centimetres and stops; Lu right holds his guard. Preserve the three-metre gap between torso positions and the same ruined bridge geometry.` |

這些是**待試拍的語意改寫**，沒有在兩家送出驗證。Hailuo API 的 `[static]`／`[zoom]`／`[pan]` 未證實適用網頁，不加進預設正文；Kling CLI 的 `enable_audio`、`prefer_multi_shots` 不是已驗證的網頁控制項。只操作當前頁面確實有的選項。`pan right` 指攝影機往右，背景會往左，不得用背景位移代替青弧的左→右出招方向；實際運鏡幅度仍由小樣核對。

## 5. 檢查與首輪小樣

```bash
node tools/video/cli.mjs lint --file .agents/skills/animation-camera/references/budaimiao-example.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs .agents/skills/animation-camera/references/budaimiao-example.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs .agents/skills/animation-camera/references/budaimiao-example.json
```

鏡頭欄位、讀法與連戲先過；單場戲的 `brief.md`、全片三章等整集要求另外記。本例估算約 21 秒，craft 不評「前30秒至少10鏡」；正式整集仍跑該列，不改共用 TARGETS。s03 是刻意的短眼部反應；`and／then` 的 info 逐鏡核對是否只在寫同一動作的停止、保持或收勢。其他警告逐項改或解釋，不靠換字騙檢查。

本例 2026-10-04 離線檢查：shot_reading `--strict` 讀八鏡零陷阱；craft 的適用 23 列全過，雙動作 info 七鏡逐一確認為主動作的停止／保持／收勢或名詞連接，沒有新增第二件事。完整 lint 留兩個整集錯誤（缺 `brief.md`、只有一章）及原創戲沒有事實來源的警告，鏡頭欄位零錯誤；不能把這個單場示例直接當成可開拍的完整集。

開拍鎖定包確認後（小樣是批次的第一批，站主看過才放量），先做 **s04 → s05 → s06 → s07** 一條完整的招式鏈（起勢插鏡、出招、接觸、受力反應）；預算緊就做 s05–s07 三鏡。同一首格設計體系、同一平台；手部細節、出招方向、對手接觸與反應要接得上。順便量一支生成能切出幾拍可用，這決定整集的預算。正常速度看剪在一起的片段，再逐幀核對握側、臉、衣飾、首格、接點和單鏡無切換；若改近側角色綁定或動作，先更新分鏡與來源綁定，再重新驗這段。

小樣結果分記美術、表演、運鏡、剪接、技術與站主接受；只有三鏡已通過相應檢查且站主接受這一版風格，才依本次預算與範圍擴製。技術成功、judge 通過、代理冷看、站主接受和成片交付各記其狀態；技能寫完不代表已生成或已達到參考片質感。
