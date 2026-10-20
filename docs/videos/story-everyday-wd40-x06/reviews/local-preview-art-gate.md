# X06 WD-40｜MiniMax 畫面關卡暫停紀錄

2026-10-20 的第一批試畫在第二章 `x06-b02-s06` 連續三張未通過後停止。
沒有繼續生成全片，也沒有將被判退的圖視為可用畫面。這是本機概念
試看片的人工檢查，並非頻道正式素材核准。

| 項目 | 關卡當時數值 |
| --- | --- |
| 已選鏡頭 | 12；機器評審 11 通過、1 待複查 |
| 人工初看 | 4 暫可用、8 **不可入片** |
| MiniMax image-01 與評審 | 各 21 次；10 張個別 take 被判退 |
| X06 媒體帳 | US$0.2835，預留交易 0 |
| 站點當時剩餘配額 | 圖片 1,969；評審 703；新配樂 0 |
| 已審口播稿 SHA-256 | `4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba` |
| 原 keyframes manifest SHA-256 | `03b2e2bd8f17c7fe9fe93effa33b3fe2a3ea771b58b2ef9e0094d9c3bc88036f` |
| 原媒體 ledger SHA-256 | `4ecda01504bdb48038301c40ebff6889f40b83a0a58b537c880ea8df2bd1cb5b` |
| 逐張人工關卡 JSON SHA-256 | `2687a4dfe69c1e887360d38869097228256d1d2f9e57b12122a0be3197df60d6` |

待複查或不可入片的入選鏡頭：

| 鏡頭 | 人工判定原因 |
| --- | --- |
| `x06-b01-s04` | 貨架瓶身有字形，且不是要求的俯視角。 |
| `x06-b01-s06` | 人物戴了兩頂帽子，地上的罐身有類文字筆畫。 |
| `x06-b02-s01` | 倉庫牆牌和多個紙箱出現假字樣，雖然 judge 判通過。 |
| `x06-b02-s02` | 應是成年工人，成圖仍像孩童。 |
| `x06-b02-s04` | 人物未分箱，紙箱上有條碼式印刷。 |
| `x06-b02-s05` | 左側箱上有中文樣貌的字、右側有紅色符號，雖然 judge 判通過。 |
| `x06-b02-s06` | 三張皆被判退；第一張有類 Amazon 彎箭頭商標，第三張門牌有可辨英數。 |
| `x06-b02-s07` | 要求獨自俯視比較，成圖卻有三人，帳頁也有文字樣線條。 |

個別 take 的其它失敗包括罐身清楚的 `P`、箱上的紅色數字、缺少指定動作、
人物數量與年齡錯誤、構圖不符。`x06-b01-s01`、`x06-b01-s03`、
`x06-b01-s05`、`x06-b02-s03` 四張只有「本次人工初看暫可用」狀態，
仍須在完整作品中再看一次。

工作區 `review/local-preview/art-gate-2026-10-20.json` 將判定綁到每張
入選圖檔的 SHA-256；同目錄的 `art-gate-2026-10-20-evidence/` 保存原
manifest、ledger 與原始圖檔副本。兩者都不進 git。即使接下來重寫
視覺提示詞與重新生成，這批失敗證據仍可獨立核對。本機預覽流程需有
綁定**最新**腳本與 manifest、逐鏡標為可用的 `art-review.json` 才能組片。

## 同日隔離三鏡小試

獨立視覺差異審查把新 `video.json` SHA-256
`907f8e3ff45f3edf0bbed64a54216c761696e8e954d51c315a8a228069e204d1`
綁回舊來源與兩份盲讀。只在隔離工作區指定 `x06-b02-s01`、
`x06-b02-s02`、`x06-b02-s06`，最多三次 take；主工作區 STOP 從未移走。
實際只用 4 張 MiniMax 和 4 次評審，增量 US$0.0540。三張被選的圖
雖都得 judge PASS（9.29/10），人工檢查仍有兩張禁止入片：

| 鏡頭 | 機器／人工結果 | 看到的事實 |
| --- | --- | --- |
| `x06-b02-s01` | PASS／**HOLD** | 小噴罐變成推車上的大型金屬桶，背景紙箱仍有印記。 |
| `x06-b02-s02` | PASS／**HOLD** | 鉸鏈變成手握直桿，背景機具出現類文字面板。 |
| `x06-b02-s06` | PASS／暫可用 | 港口、貨輪、空白貨櫃與推車表達出口；鏡頭較提示詞所說的特寫為廣。 |

主工作區已核對隔離帳前綴完全一致後合回四筆實際生成及四筆評審，
現在 ledger 為 US$0.3375／25 張／25 次 judge／未結 0；當前 manifest
保留 4 張舊圖與 3 張小試圖。新 manifest SHA-256
`9ac79b9e28d3ddd49831b121bb43ea20b3a4193a70e463a3a003b7a5d9a9fa25`；
ledger SHA-256 `f8f5eef2cdd263baea1624d3411154ead0346d8db3992c07a179959c563e9eaa`；
新逐鏡關卡 `review/local-preview/pilot-art-gate-2026-10-20.json` SHA-256
`57abd75f565bafbc447e82dd909a41dfd32e6268f5825ed0584798e45942c3bd`。
完整原圖、失敗 take、評審意見和新帳本留在媒體工作區，不進 git。

## 第二輪兩鏡小試：仍維持 STOP

`reviews/visual-v2-independent.json` 由獨立審查者把第二輪僅兩個 prompt 的
變動綁到 `video.json` SHA-256
`d1ac6f93e15396813dda6ac2d76028f6539be2d746d647d1fd44e4790dd5d0c5`；
口播、卡片、來源、其餘 76 個提示詞未變。正式主工作區的 STOP 保留，
隔離 `--shot x06-b02-s01,x06-b02-s02 --takes 3` 乾跑後才送圖。
送圖前站點剩餘圖片 1,891、評審 591，本集已花 US$0.3375、未結 0。
隔離執行實際新增三張 MiniMax 和三次評審，US$0.0405，未用滿
六張／六評審／US$0.081 的上限。兩張入選圖都由人工看過，並對照
實際口播 `x060201`、`x060202` 和
`.agents/skills/curio-episode/SKILL.md`〈插圖怎麼驗收〉重新判定：

| 鏡頭 | 入選 take／機器 | 人工結果與可見問題 |
| --- | --- | --- |
| `x06-b02-s01` | 1，9.29 PASS；SHA-256 `9a5de8a924bd3b9684e8679e0e3e66d9bfca3182150a893ca4fd890e9534ba71` | **暫可用**：噴罐與出貨門口支援「已在美國之外賣噴劑」；多一位卡通人物、托盤仍空著不是旁白主張，箱面筆畫不可讀，未見商標。 |
| `x06-b02-s02` | 2，9.29 PASS；SHA-256 `26ad3a56885e25b06fc7ca817621c92a80f5e6e6d06b756fb0343e3b9251263e` | **暫可用**：工作檯的鉸鏈樣接點支援潤滑與卡住零件的用途；靜圖姿勢與卡通人物比例不是旁白主張，未見可讀字或商標。第一次 take 6.88 FAIL。 |

五張舊的暫可用圖，其 prompt、take 與檔案 SHA-256 均未改；兩張新圖
按系列標準也暫可用，因此全片目前 **7/78** 張暫可用。最初把提示詞
的「一個人、放上托盤、轉動鉸鏈」當成旁白事實，過嚴的 HOLD 判讀已在
媒體工作區 `review/local-preview/v2-art-gate-initial-hold-2026-10-20.json`
留檔；重新判定沒有改圖或重送評審。原來的小試 manifest、
ledger、人工關卡與兩鏡原圖在媒體工作區
`review/local-preview/v1-pilot-evidence/` 先封存，再合入這輪帳本。
目前主工作區 ledger 為 **US$0.3780／28 圖／28 評審／未結 0**，SHA-256
`72828f3a8c236ba09f14a51da2f6154a099a6a0526fd6cc5285098430f51fb94`；
manifest SHA-256
`549d991ff7588c09c7c1b3f819757b31031ad5fd7e3e14618d7c119d23ffa5aa`。
SHA 綁定的人工關卡 `review/local-preview/v2-art-gate-2026-10-20.json`
SHA-256 為
`9d8df57230a6eae6d1e7da4e076429b3477fad2eba8aaacd3d5e20e5cfd976de`，
並已作為當前 `art-review.json`；其狀態仍是 STOPPED，所有原圖都留在
媒體工作區。此關卡逐張核對評審結果、旁白、字樣和畫風，並不核准
尚未生成的 71 鏡、全片合成或發布。

## 第三輪跨類型三鏡小試

保留同一份已審 `video.json` SHA-256
`d1ac6f93e15396813dda6ac2d76028f6539be2d746d647d1fd44e4790dd5d0c5`，
沒有改旁白或提示詞。送圖前站點尚有圖片 1,851、評審 552、配樂 0；
本集帳本 US$0.3780、未結 0。隔離工作區只允許
`x06-b03-s09,x06-b04-s14b,x06-b05-s01`，每鏡最多 3 take，
批次最壞 US$0.1215；主 STOP 未移走。三鏡各在第 2 take 通過，
實際新增 6 張 MiniMax 與 6 次評審，US$0.0810。

| 鏡頭／代表類型 | 選圖 SHA-256／機器評分 | 原尺寸人工結果 |
| --- | --- | --- |
| `x06-b03-s09`／路線象徵 | `401bbc3b596fc54a34473a787cd1f4a4ec7293eee2968347b41a176cbc2ec37c`／9.29 PASS | **暫可用**：兩名卡通工人把繩子接成延長的路線，支援通路擴張口播；未見可讀字、商標或畫風漂移。 |
| `x06-b04-s14b`／家清地毯 | `4ffa6aa4605d2a266a50200c3da566d1dd314de5932bf47004f7611476429846`／9.29 PASS | **暫可用**：店員在地毯店刷洗小塊地毯，支援家清產品引進當地的畫面；未見可讀標籤、商標或畫風漂移。 |
| `x06-b05-s01`／財務比較 | `28dcf0765eae7782121f848abbddd58f403baea00507b362fc4b2a7c7ad80b78`／10 PASS | **暫可用**：大、小兩堆無字籌碼支援兩類銷售規模差異，精確數字仍由原生卡負責；書脊只有不可讀橫線。 |

合回前逐筆比對 56 筆舊帳完全相同、舊 7 個選圖物件完全相同，
隔離帳僅新增上述 3 鏡 12 筆已結交易且未結 0。合回後主 ledger
**US$0.4590／34 圖／34 評審／未結 0**，SHA-256
`f950698bd2318831c58d0699c88049fa428577af6384de6c251b59438a6d7595`；
manifest SHA-256
`c5198d0127477f0275af7033bd3c8d697707ab18aeeae9a79d6bfa29b189ed44`。
三鏡逐圖結果與原七張選圖綁在主工作區
`review/local-preview/family-art-gate-2026-10-20.json`，SHA-256
`f5344777c2975c3aede4198dd07cd40b99ee18f62c6e89cc9e4064412ecd7b69`；
前一輪 manifest、ledger、人工關卡另存於
`review/local-preview/family-pilot-evidence/`。現在 10/78 張暫可用，
主 STOP 及 68 張尚未完成的畫面關卡保留；不是最終畫面或發布核准。

## 限定產圖第 1 批：12 鏡

從同一個已審稿 SHA
`d1ac6f93e15396813dda6ac2d76028f6539be2d746d647d1fd44e4790dd5d0c5`
的未試鏡抽出 `x06-b01-s04,s06`、`x06-b02-s04,s05,s07,s07b,s08,s09,s10`
及 `x06-b03-s01,s01b,s02`；隔離 `--shot` 12 鏡、`--takes 3`，
乾跑確認最壞 36 張／36 評審、US$0.4860。實際 17 張／17 評審，
增量 **US$0.2295**，12 鏡入選全部 judge PASS 且原尺寸人工檢查
暫可用。`x06-b02-s08` 和 `x06-b03-s02` 都用到第 3 take，
其餘未入選原 take 留存。`x06-b02-s09` 背景有不可辨的模糊店面筆畫，
沒有清晰可讀字或商標，按系列準則保留。

合回時核對舊 10 張選圖與 68 筆帳本前綴完全相同；11 個歷史影格
檔名碰撞先封存原圖到 `review/local-preview/batch01-evidence/`
再覆寫新 take。合回 ledger **US$0.6885／51 圖／51 評審／未結 0**，
SHA-256 `685a5ea595407bc4aa293339183bcfc90da07fb7c7624083b71ce1cf29ec67ab`；
manifest SHA-256
`94c29ae0864674af1f021bda5f53a5e430ad77783ff8abc903cff85a9de4733f`；
人工關卡 `review/local-preview/batch01-art-gate-2026-10-20.json`
SHA-256 `9ad814b920a839e10a4b832486d884155d0cced5d9a6bc8a0b2c16c9d4abd2af`。
全片當時 **22/78** 張暫可用，主 STOP 保留。

## 限定產圖第 2 批：12 鏡、2 HOLD

再以隔離 `--shot` 限 `x06-b03-s03,s04,s05,s05b,s07,s08,s10,s11,s12,s13,s14,s15`，
每鏡最多三次；實際 21 張／21 評審，增量 **US$0.2835**。
11 張入選 judge PASS，但其中一張被人工拒收；另一張三次都被
機器判退：

| 鏡頭 | 選圖 SHA-256／judge | 人工結論 |
| --- | --- | --- |
| `x06-b03-s07` | `23e5a22d5be03123e9b2ebdf494661859b0da73ec517a201e9deee3f3adec24a`／9.41 **FAIL** | 三張皆有右下紅色簽名樣 watermark；所選舊圖只作失敗證據，**HOLD／不可入片**。 |
| `x06-b03-s12` | `27634002e04dd54132f3583351c7b10f887498fa8dc582cd04ced316239d780b`／9.29 PASS | 右上藍綠店招有兩個清晰漢字樣字形，獨立抽看也確認，**HOLD／不可入片**。 |

其餘 10 張入選圖逐張原尺寸對照旁白與系列驗收標準，未見來源矛盾、
可讀字／商標或畫風漂移，暫可用。合回前再次核對舊 22 個選圖物件
與 102 筆舊帳相同；新 42 筆只屬這 12 鏡、未結 0。原 manifest、
ledger、人工關卡在 `review/local-preview/batch02-evidence/`。
主 ledger 現為 **US$0.9720／72 圖／72 評審／未結 0**，SHA-256
`96f6ce31fb1cbe5cc25230b4042aba29855124c770118b544fc9b81e3ed44171`；
manifest SHA-256
`ed89706cd41410e1d5c90d847f7879292f84d7d79c786f589d5ecfdaba091c5a`；
含全部 34 鏡逐張狀態的
`review/local-preview/batch02-art-gate-2026-10-20.json` SHA-256
`89e0595ad7198af86bfbededd8121e5beaecdc2e227315aba5046abf35ff80f7`。
**32/78** 暫可用、2 HOLD、44 未試，主 STOP 保留。

第二批後站點剩圖片 1,644、評審 342、配樂 0。44 未試若每鏡最多三次
需要最多 132 次評審；兩個 HOLD 待新 prompt 獨立審查後若各三次，
另需最多 6 次。X09 至少保留 99 次，X05 正在用同站額度，因此
第三批在跨集容量核定前不啟動。兩鏡 prompt-only 改稿的差異、
失敗原因與新 SHA 見 `visual-v3-offline-proposal.md`；舊圖不會因
改稿而自動通過，仍待有界重試。

## v3 提示詞審查與安全橋接

獨立差異審查 `visual-v3-independent.md` 為 prompt-only PASS，SHA-256
`5ab635105dc384bbec80b4f32346697247c0ebdcdcff539391674f7b436c84a7`；
新主片 SHA-256
`931efad38297c832fd11a2aedfc12cc2ef5c61373e36632a1fcd916dbdf0fc68`，
視覺 hash 從 `75d7afe80701ca12` 變成 `1ceea6211d4c482a`。
零成本橋接逐一核對 32 張原已暫可用鏡頭的提示詞、選圖物件、原檔 SHA
均未變，保留其原圖和判定。兩個舊 HOLD 選圖與失敗原因原封封存在媒體
工作區 `review/local-preview/v3-bridge-evidence/`，從當前 manifest
撤下，不能入片，也不會自動換成新 prompt 的通過圖。橋接憑據
`review/local-preview/v3-bridge.json` SHA-256
`14f66c1f9177df1c01b82d72a9d6d88b175e80d385c9e52dddbf2a7e4669dbd2`；
新 manifest SHA-256
`66e2f7a1d0fbbd28fc1b9392c06bd8511a96aa328db21b98b1722b37173a9d03`；
STOP 狀態人工關卡 SHA-256
`8c0dcc76b7b48ceabc96a19636784f22f986ce933ef6f2e194a0abcf5c4e8e0f`。
總帳沒有變，仍為 US$0.9720、72 圖／72 評審、未結 0，SHA-256
`96f6ce31fb1cbe5cc25230b4042aba29855124c770118b544fc9b81e3ed44171`；
主 STOP 留在原位。現行 manifest 32 張暫可用、46 鏡待畫，其中兩鏡
已有舊版失敗紀錄。此橋接由製作端做雜湊與原檔讀回，不自稱新的獨立
畫面驗收；進一步產圖仍受即時跨集額度與 US$25 上限約束。

## v3 兩鏡限定重試

即時站點剩 296 次評審、X05／X09 預留確認後，從橋接後主工作區複製
隔離工作區，只開 `x06-b03-s07,x06-b03-s12`、每鏡最多三次。
`s07` 第 2 take 獲 judge PASS 9.29，原尺寸圖 SHA-256
`34497aa6adbf808f7b5818d94fea011904121f97710e2bc31511f5f79266abc9`：
無字 Y 形路線槽和手中小圓柱是仍待決定的通路象徵；獨立抽看同意
沒有標籤、浮水印、商標或旁白矛盾，暫可用。`s12` 第 1 take 雖得
judge PASS 9.29，SHA-256
`e87f305702162306a9f2c7e59219603cf4008edbc035d48e20d8c677c29cb5c0`，
卻畫了完整店櫃及兩個孩童樣人物，成人拿瓶面向他們，像已在實際
銷售；口播只說「公司計畫」，故人工與獨立抽看均 **HOLD**。不在同一
prompt 盲目加到三次，下一輪須先做另一次 prompt-only 審查。

本輪實耗 3 圖／3 評審、US$0.0405；合回後總帳 **US$1.0125**、
75 圖／75 評審、未結 0，SHA-256
`8bab398fc1f1300470abf27b5ab951ab7e7b9ec61928ff2eac0d5c1143c9ce2c`。
原兩景舊版失敗檔名先封存；所有原 32 張選圖物件與 144 筆舊帳
完全相同。新 manifest SHA-256
`2fe364e2c0555b5fc75965b3255e2e212c96f0440e6a03e2936b1fd047ee245a`；
人工 gate SHA-256
`453f1be82b8d9c0fb9a46c14a3a378520168312ef41eb1cf09bb8382e29f80d7`；
單批憑據 `review/local-preview/v3-retry-art-gate.json` SHA-256
`b1a2f7c3c1a332e4d98e45cb3d96edc69e9945db6009dd5bf82014ed26f7903e`。
目前 **33/78** 暫可用、1 HOLD、44 未試，主 STOP 保留。

## 第 3 批安全早停：3 鏡已選、1 鏡未評審

先核站點 judge 剩 277、X09 保留 99、X05 承諾在安全邊界停止，
從主工作區複製獨立批次，只允許 12 個尚未畫過的鏡頭，最多三次。
前 3 鏡只有 `x06-b03-s15b` judge PASS 9.29，原尺寸選圖 SHA-256
`045996f50012fbdd6a19670ec81ba4a0559bd28d0aa7f1c61242851786eb4729`；
買家在兩側貨架比較無字物件，未見清晰字、商標或敘事矛盾，暫可用。

`x06-b03-s16` 三次 judge 全退：多餘人物、紙袋替代海綿、未做上架
動作，末張另有浮水印／游離物件。選圖 SHA-256
`1a2cdbbd31db99256078870bf3e2179593118d769825413fed47c75aa95c9109`
仍 HOLD。`x06-b04-s02` 三次也全退：額外購物者、紙包代肥皂、
黑邊；選圖 SHA-256
`ede0dd5e07feb1e3677834be7bc9ad28ab13f7e96e4f22ef60a53b90b387d658`
只站在籃子旁，沒有口播要求的放入動作，仍 HOLD。隨即在隔離批次
放 STOP，工人安全退出；下一鏡 `x06-b04-s02b` 已付費取回原圖，
尚未送 judge、未入 manifest，原圖 SHA-256
`cab2a38a2df9292c6ccad99d128866a3a16540c51a59a46511945f3a8eeb1b2d`，
只作帳本及失敗風險證據，不能入片。其餘 8 個 allowlist 鏡頭從未送圖。

隔離批次實耗 **8 圖／7 評審、US$0.0980**；舊 34 個選圖物件、
150 筆舊帳與原檔 SHA 均核同後合回，未評審圖也留檔。主 ledger
**US$1.1105／83 圖／82 評審／未結 0**，SHA-256
`f74f080e0c970330826a0176f719f537ab9208fe2fc41cb6655df799a2d16679`；
manifest SHA-256
`efd4feabc68b8567104b3169308751a4f40d0aa84d2303521725c94818de5422`；
STOP 人工關卡 SHA-256
`95604af13c0082258c2ece11cde5f420a158b83fcd4d5625fb312529f8296804`；
批次憑據 `review/local-preview/batch03-art-gate-2026-10-20.json`
SHA-256 `6cfbbe7031d6a05f7c8d51bf4adcae4b91f93a39c1403a688e4008e333cc125e`。
目前 **34/78** 暫可用、3 HOLD、41 未試。X05 已停止付費，站點
judge 剩 246；X06 對 41 未試＋3 HOLD 的最壞新一輪需求 132，
X09 至少保留 99，跨集緩衝僅 15 次。主 STOP 保留，暫停後續付費圖。

## v4 三鏡離線修稿與零成本橋接

獨立**提案**審查 `visual-v4-independent.md` SHA-256
`58569e6d6377a24c45d2aadb12c8bef676d3473eb254ea3d105e0779a08e6beb`
接受三個 HOLD 鏡頭的文字策略；提案 SHA-256
`b697f096e66f2e82eda849ea16166049dc66443aba26346f6554e070212d9219`。
逐字套用後主片 SHA-256
`acfeb244c3d67578223516a749617c89b2dad8f3df28766f85bae4e6f460ccb4`；
深比 93 景全部非 prompt 欄位相同，僅 `x06-b03-s12`、
`x06-b03-s16`、`x06-b04-s02` 三個 `data.prompt` 不同。
新視覺 hash `2f613d75fac3591d`。套用後獨立覆核
`visual-v4-postapply-independent.md` 已 PASS，SHA-256
`99ee92559c6fbd66463b5b96063d726044db0fd7a45a8ee45fb30e240fbcb55a`；
只核提示詞差異與零成本橋接，**沒有解除 STOP 或授權新付費圖**。

零成本橋接逐張核對 34 張原已暫可用鏡頭的未改提示詞、選圖物件、
圖檔 SHA 全相同；三個舊 HOLD 及選圖檔封存在媒體工作區
`review/local-preview/v4-bridge-evidence/` 並從當前 manifest 撤下，
原本已付費但未評審的 `x06-b04-s02b` 原圖 SHA
`cab2a38a2df9292c6ccad99d128866a3a16540c51a59a46511945f3a8eeb1b2d`
亦保留。新 manifest SHA-256
`39635fc22fc2dec9b71e736fc61137d0f50c22baff1adbcac127a821e5488080`；
STOP 人工 gate SHA-256
`c48c604145128b5b98bb02ba9d3a5b2ba31ab6f478a2aba9541e9b248d6b7b5d`；
橋接憑據 `review/local-preview/v4-bridge.json` SHA-256
`fc0054acbb4ac8f95dee244c0d6b3191fda77772383171b778b49bb7d9075ae8`。
總帳未變，仍 US$1.1105／83 圖／82 評審／未結 0，SHA-256
`f74f080e0c970330826a0176f719f537ab9208fe2fc41cb6655df799a2d16679`。
目前當前 manifest 為 34 張暫可用、44 鏡待畫，其中三鏡有舊版
失敗紀錄；主 STOP 保留，未送 v4 新圖或評審。
