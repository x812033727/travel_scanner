# H04 v2｜開場畫面離線修正草案（2026-10-14）

這是 [三鏡小樣](./visual-pilot-three-opening-20261014.md) 0／3 通過人工連續畫面審查後的**製片草案**，未修改 `video.json`、已核准的旁白與時間軸，也未生成或採用新圖。正常判圖的兩張 `passed=true` 仍以人工退件記錄為準；它們不能證明連戲、史料界線或全片畫質達標。

## 三鏡各自要回答的畫面問題

共通造型錨點：一頂**泛化示意**的長低脊線帳篷，左端三角入口；雪坡由畫面下方往遠處上升，視野內沒有樹。沿 `video.json.look` 的平面線條、大片色塊、簡單陰影與深藍／羊皮紙黃／暗青色票製作。這些是連戲設計，**不是**當年帳篷外形、擺放位置、搜救人數或室內物件位置的史料復原。所有生成圖都不得畫字、簽名、假卷宗、可辨認真人臉；片中以「畫面示意」和已登錄來源卡交代圖像性質。

| 現行鏡頭與旁白 | 草案路線 | 畫面任務與驗收失敗條件 |
| --- | --- | --- |
| `opening-search`／`h4v001` | 保留 MiniMax `shot`，重寫提示再試一張 | 從下坡看見遠處的空帳篷。兩名匿名小背影必須在**下方近景**，帳篷必須在**上方遠景**，中間有一大片連續空雪；若人物又站到帳邊、樹線出現，或像能辨認的歷史照片，就退件。兩人僅是構圖示意，不能當作當日人數證據。 |
| `opening-inside`／`h4v002` | 暫保留 MiniMax `shot`，與前鏡共同驗連戲 | 從同一種低脊線帳篷內朝左端三角入口看；中央空地與無人在場是唯一要讀懂的資訊。入口輪廓、日光與色塊密度要接前鏡；若變成厚塗動漫布料、華麗內裝，或呈現可以誤認為原始室內照片的細節，就退件。搜尋者除雪是旁白與來源主張，不要求生成一個沒有目擊細節的除雪動作。 |
| `opening-gear`／`h4v003` | **首選**改成有來源標示的原創 `diagram`；目前僅設計，不更動模板 | 以鞋與外衣的**抽象圖標**和來源文字表達「留在帳內」，不畫幾雙、各自擺在哪裡，也不畫成帳篷平面測繪。足跡往下方是同句的另一項卷宗記載，使用短文字引向後續的足跡來源卡；不要補出逐人的足跡路線。 |

`opening-search` 的候選 `data.prompt`（只描述畫面，畫風沿全局 `look`）：

> Wide establishing view of a broad smooth treeless snowy hillside in winter daylight. The hillside rises away from the lower foreground toward a low rounded skyline. A small long, low canvas ridge tent sits high on the distant slope, with a simple triangular entrance at its left end. Much lower on the hill, two small anonymous hooded searcher silhouettes stand in the near foreground with their backs to the viewer, looking uphill toward the tent. A wide uninterrupted area of empty snow clearly separates them from the tent. No tracks, other people, signs or writing.

`opening-inside` 的候選 `data.prompt`：

> Medium interior view along the centre of a generic long, low canvas ridge tent, looking outward through the simple triangular entrance at its left end. Its low straight roof ridge and plain taut side panels match the previous exterior view. An open strip of bare canvas floor leads toward the entrance; a few unidentifiable closed fabric bundles sit quietly at the far sides. No person is inside. Beyond the doorway a smooth treeless snowy upper slope meets a low rounded horizon in the same winter daylight. Keep the interior shapes broad and uncluttered, with the vacant centre as the focal area. No writing.

`opening-gear` 原創示意圖候選規格：16:9；上方標題「帳內留下的物品」，中間只用一組泛化鞋形與一組折疊外衣形狀，旁邊寫「多數鞋子與外衣仍在」，下方顯示「示意｜非物品數量與擺放復原」及「1959 年結案書，第 385 頁」。同句後半的足跡另以小字「殘留足跡往山下；卷宗第 386 頁」銜接既有 `document-footprints-slot` 與 `trail-varied` 的來源／示意分工。不要請生圖模型畫圖中的任何文字。第 385／386 頁和主張界線已登錄於 [claims.md](./claims.md)、[verification-notes.md](./verification-notes.md) 及 [visual-route-audit.md](./visual-route-audit.md)；正式圖須逐項核對原件裁切、可讀字級與「示意」標籤。

## 50% 插畫時長先決條件

現行已核准時間軸 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71` 共 15,827 格，其中 7,963 格為 `shot`（50.3128%）；`opening-gear` 佔第 419–621 格，**202 格**。直接把它改成 `diagram`，在總時長相同時變成 7,761／15,827＝**49.04%**。至少還須從非 `shot` 場景換入 **153 格真正有敘事作用、來源安全且實看合格的 `shot`**，才能達到 7,914 格的 50% 整數門檻；只新增片長更不能用 153 格抵銷，因分母也增加。不要為湊比例把 `journey-pack`、`buried-layer-close`（各 150 格）或必要的卷宗、模型條件、未知界線卡直接改成泛用雪景。`wind-moves-snow` 僅 102 格；`unmeasured-snow` 雖有 165 格，其「可能不等於已證明」的可見界線不能為達標而移除，且緊接 `wind-softens-edge`，易成重複雪景。

因此，**尚未找到並驗證可交換的至少 153 格之前，不在 `video.json` 落地 `opening-gear` 的 `diagram` 版本**。重配後須依當時實際時間軸重算 `illustrationShare`、`slideStates`、`cadenceProblems`，仍守單狀態最多 8 秒；來源、畫面、旁白／審核雜湊依正常流程重新綁定。

保留 50% 配額的另一條窄路是**讓 `opening-gear` 繼續為 MiniMax `shot`**，但畫面只作泛化物品意象，不再要求精確雙靴、件數、擺放或俯視帳篷平面；可用同一低脊線帳篷的一角、少量無標識鞋形與摺疊布料，讓第 385 頁既有 `document-shoes-slot` 來源卡和第 386 頁足跡卡承擔事實。此法不改目前 7,963 格分子，仍需對三張**新**影格逐張判圖、人工看圖和帶原旁白的連續試播；不能沿用三張退件圖或把泛化物件當歷史照片。

若選這條路，`opening-gear` 的候選提示僅為：「Medium close interior view of the same generic long, low canvas ridge tent. A few plain unbranded footwear shapes and folded outerwear lie on the canvas floor in one quiet foreground area, without an implied inventory or exact placement. A simple low roof ridge and a glimpse of the triangular doorway at the left end carry the same geometry and daylight as the previous view. The rest of the tent floor is visibly vacant. No people, tracks, labels or writing.」物件只能提示觀眾往卷宗卡看，不能當成第 385 頁物品清單的圖像證據。

這兩條路是待比較的草案，未取得可以批量沿用的畫風基準。若站主之後另行授權新的付費小樣，限定**至多三個相鄰鏡頭各一 take**（圖解路線至多兩張 MiniMax；第三個名額只在已選出補足時長的實際 `shot` 後使用），送出前做 dry-run、額度與 STOP／租約檢查，保留請求、判圖、雜湊與人工結論；未知計費或正常品質退件不重試同一鏡。0／3 的本輪結果不支持全片 MiniMax 擴批。
