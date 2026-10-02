# T26 原創向量畫面獨立審稿

目前狀態：`PASS_RENDERER_STILLS_AND_SOURCE_REBIND / PENDING_COMPLETE_MP4_AUDIO_CC`。180 個實際 renderer still 狀態已完整覆核並綁定目前 manifest；兩處圖文矛盾已修圖及重渲染後實看關閉，178 張未改畫面的 bytes 完全相同。最末節為目前判定；前文原型、初版及待修記錄保留為歷史。

審稿者：`review_longform`；另一名獨立看圖協審：`review_fixture_gate`。日期：2026-10-02。作者與協調者製作素材，本審稿者未繪圖或修改 master。最初原型階段只實際看過兩張 PNG 原型、讀取 SVG 對應檔雜湊，並對照原旁白核對八張雙句字卡；後續完整 SVG／renderer still 覆核範圍逐節記載。至目前尚未審看完成 MP4，未審聽完整音訊或確認 CC。

## 原型看圖

兩名審稿者各自實際使用圖片工具查看下列 PNG，未發現必修。

| 原型 | PNG SHA256 | 對應 SVG SHA256 |
| --- | --- | --- |
| 日本個人飯碗與筷子 | `7a434fce568614ff4a6a3274749bd8299fa432b139e95ba40e3dd0b19e7c4807` | `be8ab0b9e52755daeaa37ed1a08c0b89c651a9a4693c8f170250cbd19c64ef11` |
| 韓國用餐者視角餐桌 | `bb10fc5e92821201ade72801b60dd11c167b434c052474e25652925426fcbe77` | `5b6ca24e86c637732acc71e18cf621b048f721e036056fcdb09ba1c17a41c9d6` |

PNG 位於外部 artifact 目錄 `C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/`，檔名為 `japanese-held-rice.png` 與 `korean-eater-view.png`；SVG 位於本集 `vector-prototype/`。PNG 與 SVG 為不同位元組，各自綁定；沒有把檔案 hash 相符當成看過圖片。

日本原型：畫面左側的手掌托住飯碗，右侧的手用筷取飯，兩個動作可辨；標示「常見吃法示意」，未畫成所有盤子都要托起。韓國原型：座位與用餐者手部在畫面下方，飯在左、湯在右、湯匙在湯右、筷子再在匙右，與已讀的國家遺產廳傳統擺位正文相符；標示「傳統擺位示意／以用餐者視角看」。文字可讀，沒有把指南轉成法律、全民習慣或文化優劣判斷。

## 八張雙句字卡

已逐一對照原 `video.json` SHA `29ed7604e7dac8e26dfcb79c8115c5f84dc0ca2c36d0ed247e82273643964523` 的場景與旁白，及 `claims.md` SHA `ec889a4246d9190deff7693347d33e1a97735f7c97fd3356151b80529e7fd523`。下列為修訂後的 mapping；沒有新增旁白或文化史主張。

| 場景 | 第一揭示 | 第二揭示 |
| --- | --- | --- |
| c2-s06 | 兩個動作分開看 | 托飯碗與拿筷子不同 |
| c2-s14 | 介紹提到飯菜交替 | 不是把每盤都拿起 |
| c3-s06 | 湯匙能吃飯，也能喝湯 | 同一把匙，切換用途 |
| c3-s14 | 兩張桌子一起看 | 托碗、舀飯兩種動作 |
| c4-s06 | 對面視角，左右相反 | 器皿沒動，視角改變 |
| c4-s14 | 假設換碗，座位與餐具不變 | 先確認用途，再觀察用法 |
| c6-s06 | 眼前有飯湯、匙筷 | 先看工具，再判斷動作 |
| c6-s14 | 先看飯碗用途，再看取食工具 | 觀察這口飯，不用國籍猜 |

已實際重讀 native helper，確認三處要求的短修詞落地：對面視角不寫成翻轉器皿；換碗保留「假設」；最後保留飯碗「用途」。八卡原 kicker 均轉為 bullets 的可見 `note`，保留常見吃法／原創情境／傳統擺位及用餐者視角限定。原標題、旁白 ID、claims 與 chapter 留存；兩句各 `reveal=1` 與目前 templates 的 visibility 語義相符，第一句揭示第一點、第二句加第二點。這是來源與呈現語義審查，不冒充已看過最終渲染字卡。

## 後續必要範圍

完整向量素材與 contact sheet 到齊後，須實際查看所有畫面及關鍵原尺寸圖，尤其 `c4-s17` 的完整飯湯匙筷幾何，以及 `c6-s09` 的對面觀看位置不能用鏡像替代。須確認兩個圖解狀態有對應旁白的可辨變化，文字沒有裁切、遮住器皿或違反限定。原型 PASS 不自動轉移到所有素材。

目前新 native brief SHA 為 `a3700f660d9ca4a8dd21db5c9587b28e90819606e8eb1b15ebe2836f107fea6d`。已讀原創 SVG 路線、素材授權登記與正常 QA 界線；brief 中旁白實測時間為協調者回報，本次看圖未獨立審聽或重放音訊量測。最後候選 master、brief、claims 與素材 manifest 必須重新綁定；`ush3` 拆為「吃完要放回去。」及「示範也有先後順序。」時，亦須核對順序與語意保留。

`PENDING`：完整 still images、字卡實際渲染、完整 MP4、音訊與字幕、正文及成片至少 480 秒實測、每狀態至多八秒與圖解至少占正文一半的真實時間軸、平台核准與發布。沒有任何上傳或公開判定。

## 完整初版聯絡表審查，尚待修圖及最終重綁

`review_longform` 已實際逐張 `view_image` 查看六章共十三張聯絡表，並對照 master 每景旁白；另原尺寸查看 `c3-s01-detail`、`c3-s04-detail`、`c5-s08-detail`、`c2-s17-detail2`。協審另實看第四及第六章四張表與相關單圖。這些是 still images 審查，未播放 MP4；沒有因 manifest 標 READY 或 157 個檔案 hash 不同就判全通過。

初版必要修圖已回報協調者及作者：

| 場景 | 實際看圖問題與必要變更 |
| --- | --- |
| c3-s01-detail | 旁白說有飯、湯及一把湯匙，圖只有飯湯兩碗；補入可辨湯匙。 |
| c3-s04-detail、c4-s17、c6-s07-detail 及同類舀飯狀態 | 旁白講舀起／移動一口飯，匙面卻空白；相關舀飯圖須有可辨飯粒。舀湯狀態須保留湯的內容，不能全部改為飯。 |
| c4-s07、c5-s08-detail、c6-s09-detail | 對面座位在上方且左右交換，但配菜仍在畫面上方、飯湯仍下方，並非同一餐桌的完整相反視角。須同步整桌前後及方向，或以固定世界位置、雙座位與觀看箭頭表示，不能只交换飯湯左右。 |
| c2-s17-detail2 | 雙手放碗圖的筷子疊在右手腕／袖上；應放到桌側，清楚保留先放筷、再雙手放碗的順序。作者另已在處理雙手及匙頭方向，仍須看修訂後畫面。 |
| c6-s10 到 detail | 飯碗、小盤、匙與手部圖像相同，僅文字框不同。若按兩個圖像狀態處理，detail 需有實際可辨的示範動作或新構圖；不能只憑檔名／hash 不同就當有效換圖。 |

其餘已看初版圖的奶油白、深藍、紅與芥末黃風格一致，托碗／匙筷用途可辨；傳統擺位圖以用餐者下方建立飯左湯右、匙在湯右及筷在匙右。文字保留常見／傳統／示意限定，未見國旗、材質因果、健康效果或文化優劣新增主張。相關 base/detail 多數有物件增添、分解、特寫或動作變化；這不取代實際八秒 cadence 與成片檢查。

下表為這輪實際看過的初版聯絡表檔案 hash；修訂後須重看變動圖及重新綁定，不能轉移這輪證據。

| 聯絡表 PNG | SHA256 |
| --- | --- |
| chapter-1-sheet-1.png | `d9dee67b61c8ea07f9defc6efa688904a02710973120c5277c7f50d29969a8a6` |
| chapter-2-sheet-1.png | `0cef5d5601816006a22b719e2ae1f8a4cf57dc235fd6d01f8894f18537bec52f` |
| chapter-2-sheet-2.png | `b9ad47d2082f829b418da536e091eef0ddc740499fc43285a5970e5a7a6066d4` |
| chapter-2-sheet-3.png | `46dba2b0e29b0e8467307e194957ae9941c63a6d27f04fd8f7b50f9e1cc45e1f` |
| chapter-3-sheet-1.png | `2c1521d674d2a332e06e0b122f51762b1130bd6dac417a57cc32fe7f722d95e8` |
| chapter-3-sheet-2.png | `c8a776a24800d3b55f4ef039d7a79e0fe1eb21888cdbe79bcd25ea2ef7adaab9` |
| chapter-3-sheet-3.png | `9ca74ac39db167e54f03f0dfc1848ce12d9c5ff745cb1f7389180a4ac02f98cd` |
| chapter-4-sheet-1.png | `bd26183f87d5efa77fbefd39787e67762fdb8583a687d7e26549b3955d2b304a` |
| chapter-4-sheet-2.png | `cb22d7e5bda0bdc7690311d6787cb5a6aae4737f73b445ebda6baf245c37c13f` |
| chapter-5-sheet-1.png | `9c45f24f177a8fee3a406923e1b04f3d5e70bfc7a6bd208de7c92a9a45e57ca3` |
| chapter-5-sheet-2.png | `375058c986582817231dcac8354695114e5268f2085db721706d31bca388c81d` |
| chapter-6-sheet-1.png | `6226a4b4d458f11a1d854d4e717a4011d6f6f0f206b6452bfa0de5e6bc35e2f6` |
| chapter-6-sheet-2.png | `a97340eb65c33b4d46d74953389534a2f363ec7bb8d30177c30e277bf12e0bda` |

這輪 snapshot 的 master SHA `2aadb090435e25610fe7bf6c190bed208b786952c309579eec7d669e6897fd20`；claims 仍為 `ec889a4246d9190deff7693347d33e1a97735f7c97fd3356151b80529e7fd523`；manifest 當時為 `c0043a639febae254d653de85ad3e8ee1d9a16620e11e157854ecf12898ca0ee`。master 已採協調者依第二次盲轉寫所選的三句同義改寫：fvxa 比較兩次舀起食物、ef73 三件事合成完整餐桌圖、6v83 分辨個人份／共用份。三句來源與口語文字等價，不增加文化普遍性；本項只核對文字，不冒充已獨立審聽新音訊。native conversion 尚未 apply，最終 master 與 brief 仍須重綁。

## 最後 frozen native 素材增量審查

已重新實際查看新版全部十三張聯絡表，涵蓋 manifest 登記的 157 個原創 SVG 狀態；另重新原尺寸查看下表十張修訂重點 PNG。沒有只讀作者 READY 或沿用初版 PASS。協審亦獨立重看 c4-s17、c6-s07-detail、c4-s07、c6-s09-detail、c6-s10-detail，所有先前必修關閉，沒有新必修。

修訂結果：c3-s01-detail 已顯示湯匙；舀飯圖有可辨飯粒，舀湯圖保留湯色；拌合圖可見碗內食物及混拌箭頭。雙手放碗圖的筷子已放在桌側，没有疊在袖或手上。對面圖保持同一桌面物件位置，以兩端座位、觀看方向箭頭及「桌面不移動／左右基準改變」限定表達，避免只交換左右或直接鏡像。c6-s10-detail 已成實際托碗／筷取食示範，主圖不再只換文字。完整圖的旁白配合、器皿用途、左右及示意／傳統限定可辨；未見新文化普遍性或歷史因果。

最後來源绑定：受審 native 候選 `candidate-native.json` SHA `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`；apply 前 master `2aadb090435e25610fe7bf6c190bed208b786952c309579eec7d669e6897fd20`；claims `ec889a4246d9190deff7693347d33e1a97735f7c97fd3356151b80529e7fd523`；brief `a3700f660d9ca4a8dd21db5c9587b28e90819606e8eb1b15ebe2836f107fea6d`；manifest `c0043a639febae254d653de85ad3e8ee1d9a16620e11e157854ecf12898ca0ee`。已逐一計算 157 SVG byte SHA，全部符合 manifest。來源與授權為作者登記的原創資產；審稿沒有冒充外部圖庫授權或付費生成證據。

13 張 frozen 聯絡表中章 1–3 的 byte SHA 與上表相同；章 4–6 以以下新版 SHA 取代初版。

| frozen 聯絡表 | SHA256 |
| --- | --- |
| chapter-4-sheet-1.png | `1583d746151ee944fc08e0d22e84081279261e6a8ae7e939404e6e4285385209` |
| chapter-4-sheet-2.png | `46032c6969c57fa8d8a57079ec4b006c8f8dec47948699f758fd5ad3e8849e2e` |
| chapter-5-sheet-1.png | `92aabbea558aafdc4ce0f51f5110a4f628675f6203b6acb335e404a986f1568e` |
| chapter-5-sheet-2.png | `fe478dd97e04548ba14a81d207575c36646019545f3480eab5a468f4b8fe7a27` |
| chapter-6-sheet-1.png | `64666bfa1481864fc112e596cdfe4351a4b252c9cfdd6b15825ffb622a16879d` |
| chapter-6-sheet-2.png | `cff23f1d5dae667d972cb20363c2a820a16f051e1b392aec1a4b6a29f910fa08` |

| 原尺寸重看修訂 PNG | SHA256 |
| --- | --- |
| c2-s17-detail2.png | `00d26d6dae7f058f87ba3e880deeeda897a44ab13a9580a2d9f153827006ff4c` |
| c3-s01-detail.png | `1c6aa4c3241ca24c426379d60ea19d5f34a4e31f6a590d80ed15e980b5337212` |
| c3-s04-detail.png | `3559fc6f7363781f3ffc12352ad83852ec6971cc9baff75e77e0440400a69f52` |
| c3-s10-detail.png | `a75bbc9e6b44139889c3315d2fa9f58f40b624058bf149cbbfdaad6832f926a5` |
| c4-s07.png | `5cef30b330a2f1764e5fe7deeac8dea4499c113e22b7c67dd5151394c20a1702` |
| c4-s17.png | `47f7b6be52ea5bbc57890cec637d6d3563fdcc6c0fb76185a2be8f7a1addc361` |
| c5-s08-detail.png | `15c53697a37645ed9da552ffaa009dc0776b41c08d23d24d9821c6db6f8779da` |
| c6-s07-detail.png | `04801bdb6ee5cd2200b8aa721a6df32dd8fd118e2f6b8a8807ba765f0a14d8dd` |
| c6-s09-detail.png | `d7c3653b70c82cb60b1a72b727d706e4e00cda401c107e1e6a9b2c47751f6379` |
| c6-s10-detail.png | `89a77a13e5b34932fff7a599658411b7a1e239d6b543a6c5dfe20c167b5922c6` |

全 157 PNG 的集合绑定 SHA 為 `ccb26b44f6ee377da62322f58f2ddbf5dcb30e6c966795c774e80665d9f60daf`：對 manifest 所列 SVG 取 basename、將副檔名改 `.png`，在外部 preview 目錄讀各檔 bytes；建立 `{name,sha256}` records，以 name 的 ASCII 順序排序，對 `JSON.stringify(records)+'\n'` 的 UTF-8 bytes 計算 SHA256。此集合 hash 綁定全組實際 PNG，不代表另外原尺寸看過每張；完整圖像覆蓋來自十三張聯絡表，十張重點另放大。

判定：`PASS_NATIVE_STILLS_AND_CARD_MAPPING`。上述受審候選與素材可由協調者進行正常 native 轉換製作。仍未看過最終 renderer 內的合成字卡／字幕與 MP4，亦未獨立審聽拆句音訊；真實每狀態八秒、图解正文半數、正文及成片至少八分鐘、聲音 QA、成片 QA、平台核准與發布須另關閉。這不是成片媒體整體 PASS。

Apply 後已另外獨立核對 `video.json` 實際 SHA 確為 `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`。最新未含 bookends 的時間軸 snapshot SHA `e2baf37ca8c14e675cd250c8a5a4deb1cf05d17cb726ba38c89b4843f72c5e57` 與目前 speech hash `ce1ab16b0fde5fad` 相符：正文 890.033 秒、180 狀態最長 7.667 秒、圖解 87.963%，機械時長／狀態門檻可用；詳見 `verify-1.md` 的 snapshot 核對。這一項新增證據不改變圖片 still PASS 與 MP4／音訊驗收的區分，後續音訊重錄仍須重绑時間軸。

## 正常 renderer 七張實際畫面抽樣

已使用 `view_image` 實際查看下列七張正常 renderer 產出的 1920×1080 PNG，位於 `C:/Users/x8120/mokaair-work/videos/sothatswhy-t26/frames/`。這輪核對不是來源 SVG preview：奶油色 SVG 已放入正常深色品牌 frame，字卡亦為實際合成結果。再次計算來源 bytes，master 仍為 `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`，manifest 仍為 `c0043a639febae254d653de85ad3e8ee1d9a16620e11e157854ecf12898ca0ee`。

| 場景與實際狀態 | renderer PNG | SHA256 |
| --- | --- | --- |
| c1-s01 opening big | b09688d6cc4415c9.png | `a6ba3e4405359ddc7534719178b510f6e4bbb04b16df91ca6b70c61385ce123b` |
| c1-s02 托碗／桌上舀飯 | 589909152041a951.png | `6858a17440717d006e3f7622537c684f3c15a0700f8d152f05c2d6e16fd015df` |
| c2-s04 雙手取碗 | 6340b36d8ab3b3e0.png | `c71573fa10e791d2552a09abc916363f9ebc2578b32af73fb6c4307ce1fa5f04` |
| c2-s06 bullets 第一揭示 | 0a70de916887308c.png | `2ea30aac6eab304d9950cb62aa30cc865fd253f7d2a98f5a4959e5144f301ec5` |
| c2-s06 bullets 第二揭示 | 569279a21373152c.png | `8c58689fdf6ce033171750e9d9230e3a8171c8c25304f7992b71417ceb72278d` |
| c2-s17-detail2 雙手放碗、筷在桌側 | 9ca9ce606d2cc331.png | `2d49c2465683a799addcba61987222166dc4f44df30c93dfdae5f208b77563d8` |
| c3-s01-detail 飯湯與湯匙 | da1dc5ba858c3500.png | `f2f103aed7de056112a7cee95ee83e81fe005927d4e2d56c43aa7e9ab0602f27` |

主標與動作圖清楚，沒有看到裁切、重疊、物件被品牌框遮住或現在必須修的佈局問題。c1-s02 的托碗／筷取飯與留桌／匙舀飯兩種動作可辨；c2-s04 雙手取碗、c2-s17-detail2 先放筷再雙手放碗，及 c3-s01-detail 用餐者視角飯左湯右／匙在湯右仍清楚。輔助短標籤比主標小，但在實際全尺寸畫面仍可讀；這項觀察沒有代替行動裝置播放或字幕驗收。c2-s06 實際第一狀態只見第一點，第二狀態加上第二點，原 note「常見吃法與原創情境」保留且可見。

判定：`PASS_RENDERER_SAMPLE_READABILITY`，此七張抽樣無必修，協調者可繼續正常 render／assemble。尚未查看全部 180 狀態的 renderer 聯絡表，未播放完成 MP4，未審聽完整音訊，也未確認字幕合成。這輪不構成整片 MP4 或全部 renderer states PASS，未新增任何平台核准或發布判定。

## 完整 180 renderer still 狀態覆核：兩項必修

全 180 張實際 renderer PNG 已逐 byte 複製到 repo 外 `C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/t26-renderer-review-pre-layoutfix/snapshots/`，每張均為 1920×1080，依正常 renderPlan 與實際 timeline 的 scene／state 對應，排成 32 張每頁至多六格的聯絡表。這是已完成 still 的快照，避免後續正常 force 重渲染途中混入新 bytes；沒有改素材、master 或程式。

`review_longform` 親自使用圖片工具看完第 1–3 章 16 頁／88 狀態，協審 `review_fixture_gate` 親自看完第 4–6 章 16 頁／92 狀態；另本人看過第 5 章第 1 頁及第 6 章第 4 頁以確認下列必修。兩人共另看 16 個 distinct 原尺寸狀態，包括先前七張 renderer 抽樣、本輪 c2-s08-detail／c3-s04-detail／c3-s10-detail、後三章四張擺位／動作重點及兩張問題圖。沒有把雜湊相符當成實際看圖。

| 章 | 頁數 | state 數 | 實際聯絡表審稿者 |
| --- | --- | --- | --- |
| 1 | 1 | 5 | review_longform |
| 2 | 8 | 43 | review_longform |
| 3 | 7 | 40 | review_longform |
| 4 | 6 | 36 | review_fixture_gate |
| 5 | 4 | 24 | review_fixture_gate；review_longform 另看問題所在第 1 頁 |
| 6 | 6 | 32 | review_fixture_gate；review_longform 另看問題所在第 4 頁 |

本輪總判定 `FIX_REQUIRED_RENDERER_STILLS`，不是全組 PASS。兩處是真正圖文矛盾，與進場動畫誤檢的 layout cache 問題分開處理；本輪結果優先於先前原圖聯絡表及 renderer 七張抽樣的通過判定。

| state／旁白 | 實際可見問題 | 最小修圖要求 | 問題 PNG SHA256 |
| --- | --- | --- | --- |
| #126 c5-s01-detail／yfhf：「沒有座位，也沒有其他餐具，你先別急著猜。」 | 圖有手持湯匙與小盤，先於下一景才拉開照片觀察小盤的順序。 | 只有飯碗的裁框／特寫；不得加入餐具、手或座位；以放大碗或辨識範圍標記區別上一景。 | `ad50bc18dbc970270e846ad931c00ab2dea3c9374abd88dcf53dc55bd65debaa` |
| #172 c6-s12-detail／ppmj：「一邊讓飯碗靠近，一邊讓湯匙把飯送過來。」 | 兩 panel 都是留桌碗＋匙，分別飯／湯，沒有托碗，右圖食物也不是飯。 | 左側托飯碗及筷取飯，右側留桌飯碗及匙面有飯；detail 相較上一景有可辨放大／動作變化。 | `218b645caa59ff7bfd7e7a43386f7b3d4456781a0b6e60c6287acbc1a88f56de` |

只需修兩張 SVG 與其素材 manifest 綁值；這兩句旁白事實與敘事已審，不應為配合錯圖而更動。其餘本輪 178 狀態未發現新增必修：雙手取／放飯碗、桌側已放筷、匙面飯粒、拌合圖、個人份與共用份、傳統用餐者視角，以及固定桌面／雙座位／觀看箭頭符合各景旁白。八張 bullets 的兩階段揭示與原 note 均可見，沒有裁切或新全民／法規／文化優劣主張。小型輔助標籤在原尺寸可读；這仍不是手機實際播放或 CC 驗收。

每個 state 的 PNG 路徑、SHA256、scene／state、對應 line ID、旁白及本輪實際看圖者，以及 32 頁聯絡表的各別 SHA 均保存於外部 `t26-renderer-review-pre-layoutfix/reviewed-receipt.json`，SHA256 `694c9e76402af53da438cfb4569e6eba34241f785960c91e65e9f8054636f139`。原始未標判定的 `receipt.json` 保留，SHA256 `c5c3fc9bec2f4466431faf7638034d2a0d5f7d6e92b11b66acefc9d2cfdc8f60`。全部 180 PNG byte SHA 已重新計算符合這兩份快照收據。PNG 集合綁值 `f67000bb0021b273d3215d80af6c2ad46f57598656ccefde92e4329d0a638354` 的算法：按影片 state 原順序取 `{key,sha256}`，對 `JSON.stringify(records)+'\n'` UTF-8 bytes 作 SHA256，未按檔名排序。

快照來源為 master `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`、claims `ec889a4246d9190deff7693347d33e1a97735f7c97fd3356151b80529e7fd523`、brief `a3700f660d9ca4a8dd21db5c9587b28e90819606e8eb1b15ebe2836f107fea6d`、素材 manifest `c0043a639febae254d653de85ad3e8ee1d9a16620e11e157854ecf12898ca0ee`。後續正常 force 完成與兩項修圖落地後，須核對全部 current manifest 的 PNG SHA；變更圖须實際重看，不能只換收據。

正常 renderer 動畫時序的獨立 readonly 診斷：原 `load()` 在進場動畫中執行 layoutProblems；紙張從 translateY(28px) 回到原位，而 still 在 seek(end+1) 後截圖。實測 c2-s04 的動畫中 transform 13.1125px，content 為 791／778px，settled 371ms 後為 778／778px且原 layoutProblems 為空；c1-s02 與 c3-s01-detail 同樣 settled 高差零。只在記憶體故意將 paper 設 900px，settled 後原檢查仍拒絕真正 61px 溢位。建議保留原 1px 門檻，把檢查移到 pause／seek 到 settled 後，保留字型、圖片及 refused request 規則；正常 force 重拍以清掉原 cache 中間動畫的錯誤。此為原因與修正建議證據，尚未判實作修正或全批正常 renderer layout gate 已過。

歷史候選與 backup 已移到 repo 外 `C:/Users/x8120/mokaair-work/videos/sothatswhy-t26/_source/native-conversion/`；本輪實際重算 `candidate-native.json` 仍為 `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`，`video.before-native-2aadb090435e.json` 仍為 `2aadb090435e25610fe7bf6c190bed208b786952c309579eec7d669e6897fd20`，歷史審查可由這些原 bytes 重核。

仍 `PENDING`：兩項圖文修正後實看、正常 renderer 完整 layout gate／manifest 重綁、完整 MP4、音訊、字幕、bookends 及全部成片 QA。沒有成片媒體整體 PASS，也沒有平台核准或發布判定。

## 兩項修圖的 native preview 增量閉合

已獨立使用圖片工具原尺寸查看更新的 `t26-vector-art-preview/c5-s01-detail.png` 與 `c6-s12-detail.png`。c5-s01-detail 現在只有放大的飯碗及照片裁框，沒有手、匙、盤或座位；裁框、飯碗大小與標示相較 base 有實際可辨變化，保留下一景才拉開照片的順序。c6-s12-detail 現在左側左掌托飯碗、右筷取飯，右側飯碗留桌、匙面有五顆可辨飯粒，沒有湯；相較 base 更近，新增動作箭頭與明確輔助標籤，與原旁白一致。兩項 native preview 語義必修關閉。

| 修圖 | SVG SHA256 | 真正看過的 preview PNG SHA256 |
| --- | --- | --- |
| c5-s01-detail | `c3d92b2b968e396edde125a70c837b91f27659fa8dce55a27b08e61298c5de69` | `24be7847b608c2df0f08b245c9d81c023cb17ba8b794284ace0a2b72c0007152` |
| c6-s12-detail | `0ee16da68dbf5abeab62dcff46c659c844da93d5d11966fdc911d806137ecef3` | `512709ef0bf001bd831dd8b82f516daee7a7d5b7680b888e6569b51a165a0585` |

已独立解析 `t26-two-art-fix-backup/manifest-before.json` 與目前 manifest，前者 byte SHA 確為 `c0043a639febae254d653de85ad3e8ee1d9a16620e11e157854ecf12898ca0ee`，後者為 `11cd8be93dace7a2775e2b586294c111cb9ece036db0153033c30d27cd36b3a5`。兩份均登記 157 SVG，恰上述兩筆 asset SHA 改變，其餘 155 筆相同；157 個目前 SVG byte SHA 均符合目前 manifest。再次計算 master／brief／claims SHA，仍與上一節快照的 `90975caf…44f25`／`a3700f66…fea6d`／`ec889a42…523` 相同，沒有因修圖改旁白。

判定 `PASS_NATIVE_ART_TWO_FIXES`，可正常重渲染。`PENDING_RENDERER_REBIND`：正常 force 與新 asset keys 完成後，仍須實看這兩張新的實際 renderer PNG，核對全部 180 states 與 current renderer manifest 的 byte SHA；前述 pre-layoutfix 收據及 FIX_REQUIRED 留作真實歷史。這項 preview 通過尚未把整組新 renderer、進場動畫或完整 MP4 判 PASS。

## 正常重渲染後完整 still 收據閉合

已真正使用圖片工具原尺寸查看正常 renderer 新產出的 `frames/661eca217e373f31.png`（c5-s01-detail）及 `frames/06e23040acd3d80d.png`（c6-s12-detail），並實看以目前 PNG 重建的第 5 章第 1 頁與第 6 章第 4 頁。圖文必修在正常品牌 frame 中亦已關閉：c5-s01-detail 只有飯碗放大裁框及範圍文字，沒有手、餐具、盤或座位；c6-s12-detail 左側托飯碗／筷取飯，右側留桌飯碗／匙面有飯粒，箭頭與標籤可辨，沒有湯碗。圖像變化與前後旁白順序一致，沒有新增裁切、重疊或必修。

| 更新 actual renderer still | 新 key | PNG SHA256 |
| --- | --- | --- |
| c5-s01-detail | `661eca217e373f31` | `cb04214551ce63a60e5fcb126a9c266ff9666ad117e3ae0017f825c387e434a8` |
| c6-s12-detail | `06e23040acd3d80d` | `6d8e4d7d63695b03d9c98dd2435b52517d5dd8bd5b8a4a758048ecc1881e2703` |

| 更新 actual renderer 聯絡表 | PNG SHA256 |
| --- | --- |
| chapter-5-page-1.png | `266896d1acb7afeeedec78ac29101ca6c0fe1324be65a266ed19e2bebf2d2051` |
| chapter-6-page-4.png | `a0720d7d2c1599ee8d3ce8187f91062e3f390ae5b0508202f608563b3176777f` |

獨立重新計算全部 180 個目前 renderer PNG byte SHA：其餘 178 張與真正審過的 pre-layoutfix snapshot 完全相同，只有上述兩張預期修圖改變；不需冒稱另外又原尺寸看過 178 張。以同一分頁規格保存目前 32 頁，30 頁 byte SHA 與已看聯絡表完全相同，兩張更新頁已實際重看。原本兩位審稿者的實際逐頁覆蓋依原收據保留，修圖後的兩張目前圖片與頁面明確由 `review_longform` 看過，不把協審舊圖審查寫成看過新圖。

目前 `frames/manifest.json` byte SHA `73c37da4e457a98f990a381a53ced902e7e4fe9884fbdb92172809fc432738d8`。已逐景／逐狀態與 current renderPlan 比對：180 states 的 scene、state 數、reveal、still 路徑及 inline asset 新 key 全部相符；`visual_hash=9e8853bd4d25fbd3`、`theme_hash=387c6c9767343f5d` 符合目前來源，fps=30、size=1920×1080，180 actual PNG 亦均為此尺寸。全部 planned cache state 的 problems 均空，manifest 登記的 2096 個 transition 檔案均存在；存在檢查沒有轉成逐格動畫視覺 PASS。協調者回報正常 force 180 drawn／0 reused／0 layout 及修圖後 2 drawn／178 reused 皆 exit0；本審稿者獨立核對的是上述 current manifest、cache、實際圖片及檔案 bytes。

最終 still 收據與 180 PNG snapshots、32 頁 current 聯絡表及 raw renderer manifest snapshot 位於 repo 外 `C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/t26-renderer-review-final-stills/`。`reviewed-receipt.json` byte SHA `13ef9fe9b1f716ba3afa43ae3df9f19a552a7ca394eaf06bb361deb3b0225468`，每個 state 的實际 PNG SHA、前版 SHA、是否 bytes 相同及審查依據均保存；集合 SHA `fc5d667d3af721a14b0b0cfd7cb5e885b37d911339ec9138a81251a22fdfc07a` 沿用前節的 state 順序 `{key,sha256}` UTF-8 JSON＋換行算法。

最後綁定來源：master `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`、claims `ec889a4246d9190deff7693347d33e1a97735f7c97fd3356151b80529e7fd523`、brief `a3700f660d9ca4a8dd21db5c9587b28e90819606e8eb1b15ebe2836f107fea6d`、native SVG manifest `11cd8be93dace7a2775e2b586294c111cb9ece036db0153033c30d27cd36b3a5`。實際 timeline byte SHA 仍為 `e2baf37ca8c14e675cd250c8a5a4deb1cf05d17cb726ba38c89b4843f72c5e57`，与先前實測正文 890.033 秒／狀態最長 7.667 秒／圖解 87.963% 的受核 snapshot 相同；沒有拿 still 通過當成成片實測。

目前判定：`PASS_RENDERER_STILLS_AND_SOURCE_REBIND`，無剩餘 still 畫面必修，可繼續正常 assemble。`PENDING_COMPLETE_MP4_AUDIO_CC`：完成 MP4 的實際播放、完整旁白及字幕、全部進場動畫、bookends、成片至少 480 秒及正式成片 QA 各須另驗。這份來源綁定畫面審稿不構成 MP4／聲音／字幕整體 PASS，也沒有平台核准、上傳或發布判定。

## 正常成片的實際解碼視覺抽樣

在協調者明確通知正常 assemble exit0 並提交 final、checks 與品牌 pin 後，才開啟 `C:/Users/x8120/mokaair-work/videos/sothatswhy-t26/final.mp4`。本輪獨立計算成片 SHA256 為 `8aa8ad5b2fb7f89ecddf3a020d048e158bdc70195386f100c27e52cee9cc67b3`，130,511,176 bytes；擷取前後及真正看圖後重新雜湊均相同。正常 `checks.json` SHA `d0323131fcd759d49f79c30f60545e69672c39d306442cdca2980cb37d0c2a1c`，`ok=true`、problems 空、26,941 frames、speech／visual 與受審 timeline／renderer manifest 相符；`branding.json` pin SHA `067cb1eda01ee22b85634fc81086c9891ffe1af1951e1b5bee8cbae5392e913c`，實際 I=150／B=26,701／O=90。來源 master、claims、brief、vector manifest、timeline 與 renderer manifest 的六個 SHA 仍逐一符合前節，沒有改稿或改素材。

抽樣以正常 `presentationTimeline` 的片頭 offset 及 `layoutScenes` 的 transition clamp 推導，採 0-based 解碼影格 n；正文 settled 中段為 `I+S+T+floor((E-S-T)/2)`，`T=min(transition.length,E-S-1)`。使用 ffmpeg select 解碼 n，沒有用猜測分鐘或不精準的時間 seek。每張樣本保存解碼器 pts 整數與原 time_base 算出的真實秒數，未把 n／30 冒作真實 PTS。

本人真正使用圖片工具看過四頁實際成片聯絡表，涵蓋下列 13 個 distinct frames；其中 10 張另查看完整 1920×1080 圖片。其餘額外解碼保存的 87 張片尾格未親自查看，收據明標 `DECODED_RETAINED_NOT_PERSONALLY_VIEWED`，沒有把檔案存在或 SHA 相同寫成看過。

| 抽樣內容 | 解碼格 n | 真實 PTS 秒 | 實際查看 |
| --- | ---: | ---: | --- |
| 片頭近末：CC 提醒 | 149 | 4.966667 | 原尺寸＋聯絡表 |
| 正文第一編碼格：enter 起點 | 150 | 5.000000 | 原尺寸＋聯絡表 |
| 正文首張 big 進場後 | 242 | 8.066667 | 原尺寸＋聯絡表 |
| c1-s02 首張雙動作圖 | 371 | 12.366667 | 原尺寸＋聯絡表 |
| c4-s03 state 2 用餐者左右擺位字卡 | 13609 | 453.609896 | 原尺寸＋聯絡表 |
| c5-s01-detail 修後飯碗特寫 | 18355 | 611.800781 | 原尺寸＋聯絡表 |
| c6-s12-detail 修後兩種取飯動作 | 25539 | 851.254427 | 原尺寸＋聯絡表 |
| c6-s14 state 2 最後 bullets | 26042 | 868.019792 | 原尺寸＋聯絡表 |
| c6-s16-detail 最後正文圖 | 26774 | 892.418164 | 聯絡表 |
| 正文末格 | 26850 | 894.951497 | 聯絡表 |
| 片尾首格 | 26851 | 895.100000 | 聯絡表 |
| 片尾中段 | 26896 | 896.600000 | 原尺寸＋聯絡表 |
| 片尾最後編碼格，實際仍可見 | 26940 | 898.066667 | 原尺寸＋聯絡表 |

片頭 Mokaair 與「開啟 CC 字幕」清楚；正文首格是正常進場起點，章節及品牌框已見，主內容稍後進場。settled 首張 big 與 c1-s02 雙動作圖完整、可讀。c4-s03 明示「傳統擺位示意：用餐者視角」，左側飯碗、右側湯碗字卡正確。c5-s01-detail 在真正成片中只有飯碗放大裁框，沒有手、餐具、盤或座位；c6-s12-detail 左側托飯碗及筷取飯、右側留桌飯碗及匙面有飯，箭頭與輔助標籤可辨，沒有湯。兩項必修已在實際 MP4 樣本內閉合。

最後 bullets 兩點及原 note 完整；正文最後圖與末格均為已審的餐具並列圖。片尾首格標誌、中段及最後格 CTA 完整，最後 n=26940 仍可見 Mokaair、按讚、分享與開啟小鈴鐺。上述指定樣本未見壞圖、錯誤修圖、裁切、重疊或新的必要視覺修正；這是接縫兩側樣本的觀察，沒有冒稱完整播放了接縫動作或聽過同步。

原始 `decoded-receipt.json` SHA `a837bf0e65bb4616579e66b64431c7a31f04dff39b7ca25ff94a5e4636555a35`；真正看圖後的 `reviewed-receipt.json` SHA `d576b2666912b69123b3576f7eef41940980b652024dff06945eec1c6845ed93`。它們與 100 張 actual-final PNG、四頁聯絡表、抽樣推導、ffmpeg argv／解碼 log 位於 repo 外 `C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/t26-final-mp4-samples/`；每個 PNG SHA、解碼 n、精確 PTS、是否親自看過及觀察均可重核。100 PNG 集合 SHA `c986f9e45ab2462c7eb970a9f0916d076da538d598e6a4249fea24a291a4c837`，算法為按解碼順序 `{frame,sha256}` 的 UTF-8 JSON 加換行。

### 實際時長及 PTS 界線

ffprobe 確認 1920×1080／H.264、26,941 video frames、r_frame_rate `30/1`；容器與影音 stream 時長實為 **898.100 秒**，avg_frame_rate `269410/8981`，不宣稱精確平均 30 fps。frame-count／30 為 898.033333 秒；正文 frame grid 仍為 890.033333 秒，均超過 480 秒。初次 outside 抽樣 helper 額外假設 video.duration 与 frame-count／30 差距小於一格，因 0.066667 秒差異而在擷取前 exit1；此真實失敗證據保留為 `first-strict-assumption-failure.json`。之後只修 outside 抽樣工具以記錄實際 PTS，未改 repo 程式、正常 assemble 門檻或素材。

協審 `review_fixture_gate` 真正唯讀核對所有正文影像封包及接縫 PTS，證據 `pts-seam-audit.json` SHA `1cef32b27b1e8f9e593502db4fbdccd26c0e825885f7655dcc4877c9cd271ada` 已由本人讀取及重新雜湊確認。26,701 body picture payload 逐筆一致，final PTS 恆加 5 秒；片頭／片尾五個 keyframe raw 差異逐 NAL 比較只增加 SPS/PPS，沒有新增或遺失 picture packet。WAV 正文 890.033333 秒，normal normalized audio／body 容器為 890.100000 秒，多 3,200 samples；concat 沿 body 容器時長將片尾排在 895.100000 秒。正文原已有 96 處場景接縫 PTS 量化偏差，累積短 0.048502604 秒；final 沿用，正文末格 PTS 894.951497396 秒至片尾開始間實際延長顯示 0.148502604 秒。這是真實時間戳與末格 hold 的偏差，不能稱為僅平均 fps 標籤差異。

已讀正常 `checkProbe`：它驗 picture packet 數與 r_frame_rate，audio duration 相對 frame-count／30 的既有容許範圍為 `-1/30` 至 `1/30+(3×1024)/48000`，沒有驗 PTS 格距。正常 checks 通過與這項偏差可同時成立。本次抽樣沒有看見壞圖，亦沒有因此判完整音訊、同步或所有動畫 PASS；時戳偏差由協調者的 runtime 稽核另記。

本輪最新判定：`PASS_ACTUAL_FINAL_MP4_VISUAL_SAMPLES_ONLY`，上述 13 個真正看過的成片視覺樣本無必修。**仍未由本審稿者驗收完整 MP4 播放、全部音訊、影音同步、CC 播放及所有進場／揭示動畫；正常 11 項 QA、平台核准與發布也沒有由這項抽樣代替。**
