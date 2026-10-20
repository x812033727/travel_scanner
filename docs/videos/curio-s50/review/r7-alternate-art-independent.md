# S50 R7｜新三景插圖候選的獨立書面覆核

2026-10-20 UTC。結論：**三句候選提示詞的史料界線與書面畫面 PASS；新圖片、機器評審及原圖驗收 NOT RUN。** 我未撰寫[候選方案](r7-alternate-art-paper-preflight.md)，也未修改 `video.json`、畫風、旁白或媒體；原[第二輪 0／3 KEEP、STOP](r7-pilot-second-native.md)仍有效。本判定只適用下列精確文字，不能轉移到改寫後的提示詞或實際生成圖。

## 凍結資料與獨立核對

候選方案 SHA-256 為 `10a079f9e9cd6edf1a2014b51c65fbf22b6c2830d2731f5819105b1a03749df7`；現版 `brief.md`、`research.md`、`claims.md`、`video.json`、`script.md` 依序為 `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b`、`27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95`、`4e07795ddf55b4b686431851664cb1c686333233417e378b87b9e96c1180bedc`、`603dc5bbde9737dcce0cb2327cdb4db698bfd5fac7dba07e21e3bf86278a1cc1`、`5f9ae7f8b89b5f898c982dd51215c5d148901820bf715e10e6d43f8872ef782b`。現版仍有 113 張 `shot`，`look` 僅設 `cute-mystery`。

我重新下載兩份固定提交的原始 XML：[A，1667 年證詞刊本](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml) SHA-256 `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`；[V，Vincent 的 1667 年回述](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml) SHA-256 `36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`。A [147–153](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L147-L153)記布丁巷麵包師住屋與凌晨一至二點的起火時段，A [465–480](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L465-L480)是屋主後來的鋪磚地面自辯；V [2174–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2174-L2206)事後描述火沿坡往橋、橋上有屋、火在橋處受阻。這些文字不證明點火瞬間、精確街景、屋內家具或火源。

我以原尺寸重看第二輪三張 1280×720 JPEG，SHA-256 依 `fire001/013/096` 為 `c9655cc1b04ff83b4e3ab713ea42d98269d6ea101e00c50e7051e8661fbd8ed6`、`c1a8738bf924ab3d8641ff3da8e4033e383199a9589f9dc5f3c1c6a3d4da6ba0`、`c5021bfa2b762203d83b139c2ab476f4cfd61d5db4297eedcd51b56aa789cbd2`；問題與[原生裁決](r7-pilot-second-native.md)相符。第一輪的三張退圖另依[首輪逐圖紀錄](r7-pilot-first-independent.md)核對，未把它們或第二輪退圖當成可用素材。

| 景 | 對候選完整 prompt 的獨立判定 | 原圖必查之處 |
| --- | --- | --- |
| `fire001` | **PASS。** `thin smoke rising from the roof of one small house with closed wooden shutters` 以屋外煙與關窗示意凌晨住戶未醒，避免前兩輪的童貌／睜眼睡者。A 支持地址與時段，V 支持夜深；木屋尺寸、窗板和煙的形狀僅是卡通化環境，不作原件或現場重建。 | 煙從舊式屋頂而非近代城市樓群可辨、窗板關閉；不得讓新人物冒充已知屋主或點火見證。凌晨柔光不等於有史料記下實際窗光。 |
| `fire013` | **PASS。** 河水、石拱與橋面屋舍區分倫敦橋與前次誤畫的城門；近岸坡路火線對應 V 的往橋方向。`grey dawn` 僅是畫面光線，來源沒有把火抵橋的時刻精確到黎明，成片不得另加確切時刻；火線不能被畫成已經跨河。 | 從原圖能分清**橋下河水、橋面屋舍、近岸往橋方向**；若畫成無河的城門、現代橋、火跨到對岸，退圖。原圖沒有人的必要，但生成器若補人物，不能讓人物變成主角或目擊證據。 |
| `fire096` | **PASS。** `broad flat brick-paved floor` 直對 A 的 `the Room was paved with Bricks`；成人麵包師只作後來自辯的卡通示意，低頭看地面不冒充當時火場勘驗。候選去掉前輪指向獨立凸磚的動作，也不指定大磚壁爐。 | 連續平坦的**房間地面**為主體；凸起單磚、磚造巨爐或活火若使觀眾誤以為已驗出起火結構，退圖。成人與室內擺設不是已證實的 Farriner 現場肖像。 |

三句未把畫風詞寫入 prompt，仍靠既定 `cute-mystery` preset。兩張無人火景是為了避開兩輪反覆生成的假睡者與童貌搬運者，屬以火／煙為主動作的有限例外；模型仍可能補人物或把橋畫成城門，因此書面 PASS 不預測 MiniMax 成功率。候選的 **3／3 原圖 KEEP、每失敗景一次有界修詞重試後仍失敗即 STOP** 規則保留；評審九題與原圖內容判讀都要留下，不能只看 `passed: true`。帳本仍為已花 US$0.081；預檢的 `0.081 + 113×3×0.0135 + 0.08 = US$4.7375` 算式正確，**US$4.75 是新方案的累計硬上限提案，未取得付費核准**。站台圖片評審與配樂額度均為零，沒有啟動新圖、配樂或組片。
