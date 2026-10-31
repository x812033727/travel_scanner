# C11 UCC R6｜獨立來源與書面配鏡差分查核

查核者：`/root/c11_r4_source`。未寫中文候選、研究或共圖計畫；本輪未讀native／blind票。R4／R5已披露的歷史metadata暴露不作判定依據，本輪未新增暴露。

**SOURCE PASS／WRITTEN VISUAL PASS／PLANNED REUSE PASS。** 無必要修正。這是來源及書面共圖規劃核准；尚無實圖檔案或實際共用SHA證據，未授實際音畫、實聲長度、owner或production核准。

## 凍結輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `03817277b5c79f45c6064a082ac9a23279b9b11b289cd091cb2261a212d5d38b` |
| script.md | `1cc1d014cf1bf3c7aa6c1f44751e7c457bb5e327729d3e8a573867787a1c65d1` |
| narration-only.json | `faf50858697c1e48895435af3abad6068e9d047eb86cc8898b32bbdd7d36053b` |
| claims.json | `41d367767138c4d34da8af812f779f94151675e31abf9ae6ae07039feb1c5082` |
| image-reuse-plan.json | `bd7fd483d1f6bbb50f94d469dcf49a67b2d5233e855cbd280f6242b7a1f3a7c9` |
| reviews/source-r6-independent.json | `58ff9d0b1ce33e7374546aa1ae5cec788f40c8f0e413004f2897ba353cc8b258` |

R5來源報告SHA `78041720b1a086de11339f9ea1983a88f6bc09c45c425c96a234758dd9594dc7` 已實核；其來源PASS、書面配鏡HOLD分開承接，不把HOLD當PASS。R5四核心及R5→R4→R3→R2→R1來源proof鏈重新核實；R5沒有本輪適用verify。

| R5核心 | SHA-256 |
| --- | --- |
| history/r5/video.json | `4bf4cf8ac1afacd68988a00db34ce81cf494a623ee3f299dbeb098fad4bee8c3` |
| history/r5/script.md | `368afe9a2a7a8328dc03ba576d6a39fa4220b5c6d0d9e3ddd5cad8348723827c` |
| history/r5/narration-only.json | `4634101ecd26263111d14184e6d9540969b01ce4884d35592902ce8532bff2b3` |
| history/r5/claims.json | `381b148813eb5d8eeff02f7e194d77f1b1e22c6ede94f3d986dfd3286a7912a1` |

## 原件、差分與共圖規劃

R6把h04兩預告拆為h04與新增c11h04b1。79句成80句、76 shot成77 shot；總78 scene含一個outro、23 loops。其餘78句原文、76完整claim及74完整scene逐物件與R5相同；既有運鏡及visual模式不變。h04、t05、s11三個prompt改成兩組中性畫面，新h04b1複製s11的prompt及camera。只有冷罐預告的loop setup改綁新ID；六章章名、縮圖及其餘video欄位不變。

親讀原始HTML：UCC2026 p222–223的分離／風味／罐壁問題、JNET2011 p1121的均質化抑制分離、JNET2023 p1131與UCC2025 p167的工廠旁配送據點、冷罐與卡車。兩預告只問奶的狀態及冷罐交付，沒有新增史實或先揭方法。樣罐與樣杯不畫均一奶粒或設備；中性搬箱不畫卡車、冷卻裝置、路線或已送達結果。

依script-writing.md §開場濃縮「每一個預告句用回收它的那一章的畫面（同一張圖）」核對：

| 預告 | 真payoff | 共用計畫ID | 原生imageKey（規劃1K） |
| --- | --- | --- | --- |
| c11r1h04 | c11r1t05 | milk-sample-shared-still | `99c272f890e44236` |
| c11h04b1 | c11r1s11 | cold-delivery-crate-shared-still | `284cb84f75f0ea4c` |

已直接呼叫官方resolveLook、shotCast、composeShotPrompt、shotPrompt及Stage.imageKey作純本地計算：兩端原prompt、camera與完整composed prompt逐對相同，零裁切、零修正；兩個1K key均吻合sidecar。另以2K規劃尺寸驗算，每對仍相同。所有程式檔、規則檔、sidecar及其四核心／brief／series／claims.md綁定均以真SHA核實。這些參數是宣告計畫，沒有讀後台設定或呼叫provider。

image-reuse-plan明列source/reuse scene與line ID、固定asset_plan_id、四條claims引用，以及官方keyframes --shot的payoff先行、--takes 1、seed offset 0、首take正常judge通過後才走teaser精確cache重用。任一失敗、參數改變、有效cache缺失或選中圖分歧即應停止該對；不能另生相似圖冒作共圖。裁切後衍生檔、各scene judge、真manifest及組片實際輸入仍須在正式產圖後核同一路徑與SHA；本輪未執行這些媒體步驟。

80句video／script／narration-only／claims的ID、章名、文字與順序一致；77個prompt與claims一致；23 loops／46端點均存在且向前。35筆原件收件、5份清單、33研究／新增錨點的raw／cache／段落真SHA、三份研究、old28與snapshot皆實核未變。names不入prompt、look只cute-mystery、burn_in=true，縮圖仍指d11。

## 逐句結果

| 句ID | 結果 | 來源 |
| --- | --- | --- |
| c11r1h01 | PLAN | GUINNESS2019 |
| c11r1h02 | ATTRIBUTED | GUINNESS2019、UCC2025_REPRO |
| c11r1h03 | PLAN | GUINNESS2019 |
| c11r1h04 | PLAN | UCC2026 |
| c11h04b1 | PLAN | UCC2025、JNET2023 |
| c11r1h05 | PLAN | JNET2023、UCC2025 |
| c11r1h06 | PLAN | UCC2026、UCC2025 |
| c11r1o01 | ATTRIBUTED | UCC2026 |
| c11r1o02 | ATTRIBUTED | UCC2026 |
| c11r1o03 | PLAN | UCC2026 |
| c11r1o04 | ATTRIBUTED | GUINNESS2019 |
| c11r1o06 | PLAN | UCC2026、HAMADA2021、SHIMANE_FIRST |
| c11r1o07 | ATTRIBUTED | HAMADA2021、SHIMANE_FIRST |
| c11r1o08 | ATTRIBUTED | CAN_INTERVIEW、UCC2026 |
| c11r1o09 | ATTRIBUTED | UCC_MUSEUM |
| c11r1o10 | PLAN | UCC2026 |
| c11r1o11 | ATTRIBUTED | JNET2023 |
| c11r1o12 | PLAN | UCC2026 |
| c11r1o13 | PLAN | UCC2026 |
| c11r1o14 | PLAN | JNET2011 |
| c11r1t01 | ATTRIBUTED | JNET2011 |
| c11r1t04 | PLAN | JNET2011 |
| c11r1t05 | ATTRIBUTED | JNET2011 |
| c11r1t06 | PLAN | JNET2011 |
| c11r1t07 | PLAN | JNET2011 |
| c11r1t08 | PLAN | JNET2011 |
| c11r1t09 | ATTRIBUTED | UCC2026、JNET2011 |
| c11r1t10 | PLAN | JNET2011 |
| c11r1t11 | PLAN | JNET2011 |
| c11r1t12 | PLAN | JNET2011 |
| c11r1t13 | ATTRIBUTED | JNET2011 |
| c11r1t16 | PLAN | UCC2025_REPRO |
| c11r1w01 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w02 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w03 | PLAN | UCC2025_REPRO |
| c11r1w04 | PLAN | UCC2025_REPRO |
| c11r1w05 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w06 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w07 | PLAN | UCC2025_REPRO |
| c11r1w10 | ATTRIBUTED | UCC2025_REPRO、GUINNESS2019 |
| c11r1w11 | ATTRIBUTED | GUINNESS2019 |
| c11r1w17 | ATTRIBUTED | GUINNESS2019 |
| c11r1w12 | PLAN | GUINNESS2019 |
| c11r1w14 | ATTRIBUTED | GUINNESS2019 |
| c11r1w15 | PLAN | GUINNESS2019 |
| c11r1w16 | PLAN | JNET2011 |
| c11r1s01 | ATTRIBUTED | JNET2011 |
| c11r1s02 | ATTRIBUTED | JNET2011 |
| c11r1s03 | PLAN | JNET2011 |
| c11r1s04 | PLAN | JNET2011 |
| c11r1s05 | PLAN | JNET2011、UCC2025、JNET2023 |
| c11r1s19 | ATTRIBUTED | JNET2023 |
| c11r1s20 | ATTRIBUTED | JNET2023 |
| c11r1s21 | ATTRIBUTED | JNET2023 |
| c11r1s06 | CONFIRMED | UCC2025、JNET2023 |
| c11r1s07 | ATTRIBUTED | JNET2023 |
| c11r1s08 | ATTRIBUTED | JNET2023 |
| c11r1s09 | PLAN | UCC2025、JNET2023 |
| c11r1s10 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s11 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s13 | PLAN | UCC2025、JNET2023 |
| c11r1s14 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s15 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s16 | ATTRIBUTED | JNET2023 |
| c11r1s17 | ATTRIBUTED | JNET2023 |
| c11r1s18 | PLAN | JNET2023 |
| c11r1d01 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1d02 | ATTRIBUTED | JNET2023 |
| c11r1d03 | PLAN | JNET2023 |
| c11r1d04 | PLAN | JNET2023 |
| c11r1d05 | PLAN | JNET2023 |
| c11r1d06 | ATTRIBUTED | JNET2023 |
| c11r1d07 | ATTRIBUTED | GUINNESS2019 |
| c11r1d09 | PLAN | UCC2025 |
| c11r1d11 | CONFIRMED | UCC2025 |
| c11r1d12 | CONFIRMED | UCC2025 |
| c11r1d13 | PLAN | UCC2025 |
| c11r1ct1 | PLAN | JNET2011、UCC2025_REPRO、JNET2023、UCC2025 |
| c11r1ct2 | PLAN | 觀眾提問／頻道邀請 |
| c11r1ct3 | PLAN | 觀眾提問／頻道邀請 |

## 範圍限制

全有聲正文2,276 spokenUnits已用原生spokenUnits(spokenText(line))獨立重算，含coldopen157及有聲CTA103。拆句不增加units；這是紙面規劃，實聲尚未生成／量測，不判13分鐘實聲PASS／FAIL。

3→10→30箱仍為上島達司有限回憶；1969及四月只指商品上市。Mira 1965先例／加糖無奶與館方自稱含奶首款的歸屬保留；1978／1981拉環衝突不選首次年；製程／配送不編同期實驗、完整配方、車數或運單。35筆收件含失敗、重複載體與排除圖，不是35組獨立證據。

共圖只通過書面規劃：actual file及SHA仍為null、actual_same_asset_verified=false。只寫本verify與獨立source報告；未改core、計畫、研究、old28、snapshot、history或task，無provider／付費／後台／Git／新子代理，未授native／blind投票、owner、預算、canonical、讀音／TTS、實際圖像／共圖／聲音／字幕QA、打包或發布核准。

