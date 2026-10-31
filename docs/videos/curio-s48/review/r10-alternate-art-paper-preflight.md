# S48 R10｜停工後的三景新插圖方案書面預檢

2026-10-20 UTC。**三句候選提示詞已由撰案者核對固定史料；新方案的獨立書面覆核、付費圖、原圖驗收與整集放量均 NOT RUN。** [舊方案兩輪原圖裁決](r10-media-pilot.md)是 0／3、0／3 KEEP，已達原先的一次修詞與一次重試上限；本頁提出另一套可測的新方案，不改掉舊案的 STOP。沒有修改 `video.json`、`script.md`、`look`、已錄的 102 句旁白或網站審核卡，也沒有呼叫付費圖像與配樂。

## 固定版與失敗例

現行 `video.json` SHA-256 `dd91631217153e3fec5e0117dea73faa30811991fce3a211aad7d99615cca018`，`script.md` `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd`，全片 99 個 `shot`。我重取並核對 [Russell 1865 船上記述 R](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt) SHA-256 `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`，及 [Field 後出家族敘事 F](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt) SHA-256 `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。三張第二輪原生 1280×720 JPG 也已重開並核 SHA：`atl001` `f2024ccf…` 把收纜機變成有輻條的駕駛舵輪、電纜像髮絲；`atl017` `01b8ea0d…` 的人物變成小孩般小影，光點在巨大空白板中央；`atl070` `57c42f82…` 把電纜變成數尺寬的海堤。這三項主動作／物件錯誤才是新方案的驗收重點；`atl070` 多一位卡通路人本身不構成拒收。

## 三句紙上候選（**尚未寫入 `video.json`**）

| 鏡頭 | 精確候選 prompt | 固定來源與要看的原圖 |
| --- | --- | --- |
| `atl001` | `Medium close shot on the Great Eastern's forward deck in 1865, one adult deckhand in a wool work coat guides a rope-thick dark cable rising from the sea across two solid horizontal iron drums on a low frame, then aft across the deck, soft overcast light` | Russell [R3782–3798](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3782-L3798)記船首收線、經機械和捲鼓帶向船後。單人是卡通示意；兩個實心橫置鼓讓它與舵輪分開。原圖須看出**線從船外水面經低架橫鼓上甲板**，不得把核心裝置畫成有輻條的駕駛舵輪、讓線變成頭髮或憑空斷開。鼓數和船員外貌不冒充精確復原。 |
| `atl017` | `Medium close shot in an 1865 ship testing cabin, one adult electrician leans toward a palm-length narrow cream scale beside a tiny round mirror on a wooden bench, a pin-sized reflected light spot at the scale's far right edge, soft lamp light` | Russell [R2899–2915](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L2899-L2915)記小鏡反光沿刻度移動、當值者見光到末端後消失。原圖須有**正常大小的成年觀察者、小刻度與末端光點**；鏡子可簡化，毋須把完整光路或數值畫出。巨大空板、針式指針、中心光球或童貌主角若取代此主動作則 REJECT。 |
| `atl070` | `Medium shot on the shingle shore of Heart's Content in 1866, one adult worker in a plain wool cap lifts a dark rope-thick submarine cable from shallow water with both hands, the same narrow cable curves a short distance onto the beach toward a small wooden telegraph station, grey overcast daylight` | Field 書所引航程日記 [F8990–9035](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L8990-L9035)記新線於 7 月 27 日抵港、安排登岸與電報站；這是**新鋪的 1866 線**，不是後來撈回的舊線。工作者、握線姿勢與岸上短距離是示意。原圖須看出**手握的繩粗線**連到水際；不得成為人能走的道路、海堤、現代塑膠管或 1865 舊線已撈回的畫面。 |

三句只指定單人單動作、主物件與光源，不把畫風寫進 prompt；系列樣式仍靠現行 `look: {"preset":"cute-mystery"}`。史料不支持可讀儀表刻度、電報原文、船員身份、原樣艏部機械或可精確定位的海底纜線；新圖若加出這些宣稱不得當史證。**本頁自檢既非獨立書面 PASS，也不代表 MiniMax 會畫對。**

## 新方案試畫、門檻與費用

1. 待月額度恢復，先重查 `media-status`、當時精確 `video.json`、原始媒體帳本、網站審核卡與乾跑報價；目前跨集[額度盤點](../../curio-s46-s53-media-gates-20261020.md)記圖片評審 **20,000／20,000、剩 0**及配樂 **60／60、剩 0**，預期 2026-11-01 UTC 重置。評審不能呼叫時不買無法驗收的圖。本紙上方案如要採入，僅變更 `atl001/017/070` 三景 prompt，重跑 lint，**由未參與撰詞者**做來源／書面畫面差分覆核並重核畫面綁定；不沿用舊版分鏡審核結果。旁白文字不變，仍須核其 102 句音訊綁定。
2. 新 pilot 的三張圖各先限 **1 take + 1 judge**。逐張查看原生 1280×720、記 prompt／原圖 SHA 和九題 judge；獨立按上表判主動作、年代與系列畫風。機器 9.29 分不能蓋過錯誤的舵輪、刻度或海堤；額外無害卡通細節不另造退圖標準。**三景皆 KEEP** 才能開始其餘 96 景：三個物件各是本片核心，不能靠別景湊 2／3。任何一景首張 REJECT，立即停其他鏡頭與配樂，只准失敗景作**一次**窄幅改詞和獨立來源覆核，再各買最多 1 take + 1 judge；同景第二張仍 REJECT 就停止**此新方案**。原舊方案的 0／3、0／3 不洗成新圖通過；不以字卡換掉核心鏡頭來繞過系列 70% 插圖比例。
3. 私有 `media/ledger.json` 本次 SHA-256 `c6ffa9dea6cdc1b50a73f39706f45a5879bef05314eea86117f3316be633ca54`，已花 **US$0.0675**（5 張計費圖、5 次 judge；另 1 次零費失敗；配樂 0）。實價每 take 圖 US$0.0035、judge US$0.01。新三景若各首張與各一次重試，增量最多 `3 × 2 × 0.0135 = US$0.081`，**試畫累計上限提案 US$0.15**（含已花 US$0.0675）。現行 99 景、3 take 上限的乾跑仍報圖片約 US$4.01、600 秒配樂約 US$0.08；以所有 99 景都重新畫滿三次的保守算法，累計整集 `0.0675 + 99 × 3 × 0.0135 + 0.08 = US$4.157`，**整集累計上限提案 US$4.16**。這包含此前失敗圖支出，沒有把它誤算成可沿用的 5 張 KEEP。舊 [US$5.00 R10 本地上限](r10-media-pilot.md)綁舊提示詞，不能自動移到新雜湊；本站屆時報價、scene 數或價格若不同，先重新計算與落地整集一次性上限，再付款。本頁沒有核准支出或解除 STOP。

即使三景全過，餘下 96 景與音樂仍要逐張／逐項驗收，之後才有組片、字幕、Shorts、成片品管和私人上傳後的可點片尾推薦／訂閱元素。網站音訊卡目前仍待站主，不能用本地選擇冒充網站核准。
