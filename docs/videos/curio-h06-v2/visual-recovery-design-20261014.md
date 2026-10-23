# H06 v2｜三鏡小樣失敗後的免費視覺修訂案

日期：2026-10-14。這份文件原是**尚未套用**的設計稿；第五輪三鏡原圖、judge、人工判定與 US$0.0405 的收據在 [視覺小樣第五輪](visual-pilot-01.md)及外部 `review/pilot-three-20261014T030325Z/`。該輪 `video.json` SHA-256 為 `499fcab1f69d8eb9e9e25d65f9f89eb37ccd686142637092b852676b2ba9b68a`。站主後續核准下述混合修訂與第一、第三鏡各一張的小樣；執行及結果見文末「第六輪執行紀錄」，不能把原先提案視為分鏡已核准。

## 連續三鏡的畫面設計

| 順序／句 ID | 正式時窗 | 設計與畫面方向 | 來源界線 |
| --- | ---: | --- | --- |
| `hook-hospital-door`／`dszz` | 293–449 幀，5.20 秒 | **待換圖**。寬景、左側小型全背影剪影；抽象牆與地面斜向右方留白，`pan right`。不再以居中門框、具體窗／長椅或照片感表示病院。 | [c03](claims.md)只支持 1922 年病院裡有人將她與公主連在一起，不能指定誰先說、她當時的姿勢／服裝／房間外觀。剪影是現代編輯示意，非安德森肖像或現場重建。 |
| `hook-hospital-door-beat-2`／`v202` | 449–601 幀，5.07 秒 | **暫留原圖候選，不改提示**。正中央平面空門與左右兩塊無人陰影，`push in`；judge 10/10。 | 表示卷宗保存兩種說法，並非病院實物或誰先開口的證明。原圖可單獨讀懂，但首鏡退件，且現有首鏡與此鏡 dHash 距離 4；不能當成連續分鏡已過。 |
| `hook-three-answers`／`ykiq` | 601–756 幀，5.17 秒 | **待換圖**。俯看、斜排的無字色塊與一小段紅色審查路徑，`pan left`。相對前一鏡的居中門口，換成無建築、左上／右下動線。 | [c05–c07](claims.md)支持 1970 年法律審的程序範圍；此處只示意上級審查前審，不畫真法院、法官、判決原件、徽章、證書或女工身分的裁定。 |

三鏡保留原 scene ID、line ID、`shot` 類型、章節、口播與影格時窗。畫面節拍是**斜向人物剪影 → 中央空門 → 俯看色塊**；視角、主體位置及運鏡依序為 `pan right`、`push in`、`pan left`，避免再出現三張門口照片。`hook-hospital-door-beat-2` 只是人工認為可留的**單張候選**，尚未獲 storyboard 核准，不能 `--accept-best` 或手改 manifest。

### `hook-hospital-door` 待審提示草案

`data.camera`: `pan right`（維持）；`data.prompt` 草案：

> Wide flat 2D editorial cut-paper diagram of an unspecified Berlin hospital setting in 1922, not an archival scene. At the far left, one small anonymous adult woman appears only as a dark rear-facing silhouette from shoulders to hem; no face, side profile, identifiable clothing or action. Three broad opaque wall and floor planes sweep diagonally across the frame toward a pale abstract light rectangle at right, with one tiny vermilion square as a graphic accent. Keep the right half open; there is no doorway, bench, detailed window, visitor, sign or record. Coarse irregular ink edges, matte paper layers and visibly drawn shadows fill the 16:9 frame without photographic lighting or realistic surfaces.

目的不是補出來源沒有的病院內景，而是讓觀眾知道故事轉到病院。背影只承接「女子在病院」的旁白，不暗示她的容貌、誰先說公主名字或她當時站在何處。若離線看圖時剪影被畫成可辨正／側臉，或背景像特定史照，直接退回。

### `hook-three-answers` 待審提示草案

`data.camera`: `pan left`（原為 `drift`）；`data.prompt` 草案：

> Wide flat 2D top-down editorial diagram of appellate review, made only of four thick unlettered color tiles rather than documents. A lower-right dark tile sits beneath an upper-left muted-teal tile; one short vermilion ink path bends between them and stops at the upper tile. Put the red bend in the centre third as the single focus, with wide open matte-paper ground around it. Use opaque cut-paper fields and irregular ink edges, never realistic stone or glass. No courthouse, doorway, stairs, people, text, seals, heraldry, gavel or purported case files. This modern visual metaphor shows a higher court checking an earlier decision; it does not identify the woman or depict the real court.

此鏡只接住 `[ykiq]` 的「審查前審判決」，不提前說法院已確認另一身分。紅色只是一小段編輯圖形，修正第五輪缺少紅點的風格失敗；不得把色塊畫成有字判決或歷史文件。

## 50% 插圖占比的硬邊界

正式正文 15,028 幀，至少 **7,514 幀**要是 `shot`。目前 49 個 shot 合計 **7,560 幀／50.3061%**，只有 **46 幀／1.53 秒**餘裕。兩張草案仍是 `shot`，所以只改其 prompt／camera 且不移動句子時，這個算術占比不變；成片仍須按實際時長重新測。

| 若改走原生 `diagram` | 剩餘 shot 幀／占比 | 回到 50% 至少要補的可信 shot 幀 |
| --- | ---: | ---: |
| 只轉 `hook-hospital-door`（少 156 幀） | 7,404／49.2680% | 110 |
| 只轉 `hook-three-answers`（少 155 幀） | 7,405／49.2747% | 109 |
| 兩鏡都轉（少 311 幀） | 7,249／48.2366% | 265 |

因此本案不能直接把任何退件長鏡改字卡、沿用原時間軸並宣稱符合 50%。若日後改模板，先找**來源可畫且實際有新內容**的時窗補足上述 shot 幀，再重跑敘事、音訊與正式節奏關卡；不能延長靜畫或重播同圖湊秒。現有工具沒有已驗證的任意 SVG 匯入 keyframe 流程，也不能手改舊 manifest 冒充 accepted shot。

## 有界的下一次驗證

1. **先做免費預檢。** 以隔離副本放入上面兩個 prompt／camera，對照 c03、c05–c07，跑 `lint` 及兩個 `keyframes --dry-run --shot ID --takes 1`，保存完整提示、模型、價格及新 `pictures_hash`。把三鏡排成 5.20／5.07／5.17 秒的正常速度草圖，特別看左側剪影、中央空門、俯視色塊是否明顯不同，且沒有假文字或可辨的真實場所。隔離預檢不寫正式 manifest。
2. **核對綁定。** 只改這兩個 shot 的 prompt／camera 時，`narrative_hash`、`speech_hash`、逐句影格與現有 audio approval 理應不變；`pictures_hash`、`visual_hash` 必改。實作時實際讀回雜湊與 `status`，不能只依本頁推論。第二鏡的既有圖由工具按本身 request key 與 judge stamp 判斷可否沿用，不手填接受狀態。
3. **另獲有界授權後才付費。** 提案上限是第一、第三鏡**各一張／一次 judge，共兩張兩判**，不重抽第二鏡、不跑整批。先再次檢查 STOP、LEASE、核准、模型、帳本保留額、每片 US$80 上限及 dry-run；以第五輪實際單張 US$0.0135 粗估兩張約 **US$0.027**，正式價格以送出前站上讀回為準。每鏡順序送出，未知計費／服務錯誤即停，不自動重送；明確 judge FAIL 才可在封存收據後處理另一個不同鏡頭。
4. **連續畫面關卡。** 分別目視原圖與實際裁切圖，記錄 judge 與人工判定，正常速度檢查這三鏡及前兩張原生圖卡的轉場、來源界線、相似度與真實 50% shot 比例。任何圖仍像照片、露臉、捏造史料或與鄰鏡重複，就不送分鏡審核；不能讓一張 judge PASS 代替連續段的人審。

## 第六輪執行紀錄（2026-10-14）

站主核准後，只把上面第一、第三鏡的 prompt 套入 `video.json`，第三鏡 camera 改成 `pan left`；第二鏡與所有 scene ID、模板、句子、順序及時窗不變。新 `video.json` SHA-256 `a41d5d784a4e7bfe189b8b2683a172656d84174bc1c2e247ff91f335c5f6f7d1`。`narrative_hash=a8b72a5524beace9`、`speech_hash=9ae95e3507d3809f`，104 句逐句起訖影格與場景影格重新計算後都和原正式時間軸相同；時間軸 SHA-256 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2` 仍對應現存音訊核准。`pictures_hash` 改為 `1fa2c8f61603eff9`、`visual_hash` 改為 `529d6a4176e2c008`。`lint` 為 0 error；`cadenceProblems=[]`。

生圖前先封存舊 `video.json`、manifest、ledger、state、approvals、正式時間軸和五張原有圖；檢查專案及上層無 `STOP`、專案無 `LEASE`、無待結算工作、帳本 0 保留額，兩鏡 `--dry-run --takes 1` 都顯示 MiniMax `image-01` 1K 可用、提示長度在預算內及 US$80 單片上限。然後依序各送出**一張圖及一次正常 judge**，沒有重抽或擴批。逐檔 SHA、原圖、裁切圖、命令輸出、每步帳本／manifest 與人工判定封存在外部 `review/pilot-revision-two-20261014T040020Z/`；其 `postflight-summary.json` SHA-256 `956b669a063cf3c61d58f441094c176c483669f5512cc7ce6595de92ef2ecaa1`。結果見 [視覺小樣第六輪](visual-pilot-01.md)。

三鏡聯絡表顯示左側背影、中央空門與俯看色塊彼此可區分，但第一鏡多出提示排除的長椅；第三鏡紅色只成左上弧線，沒有接上第二鏡的紅色方塊，右側大色塊過於抽象，位置亦偏離設計。兩張新圖皆獲 judge PASS，人工分別列 **HOLD** 與 **HOLD／待複核候選**；`hook-hospital-door-beat-2` 仍是未變的單張候選，整段未送分鏡核准。`shot` 時間仍是 7,560／15,028 幀（50.3061%，只多 46 幀），成片實測尚未進行；其餘 46 個 shot 缺圖，縮圖仍無可用來源。本輪授權的兩張已用完，不再擴批。

其後站主改選免費來源圖卡加離線有聲草剪；第一、第三鏡的 SVG、字幕壓力測試、實際 50% 缺額與有界補鏡提案記在 [原生三鏡草剪](native-three-scene-preview-20261014.md)。該頁只是隔離預覽，正式腳本與本輪 HOLD 收據仍保持原狀。
