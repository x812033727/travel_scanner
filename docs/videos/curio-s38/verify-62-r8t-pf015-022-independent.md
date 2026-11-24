# S38 R8t｜PF015–022 第一章剩餘八景書面預檢

2026-10-22 UTC。**七景書面 PASS，可按 PF015、PF016、PF017、PF018、PF020、PF021、PF022 順序各試一張；PF019 書面 HOLD，不購圖。** 逐張看未裁切原圖後才決定是否繼續下一景；相同成人／年代／來源／畫風問題累計三張即停後續付費。此票不是七張原生圖 KEEP，也不放行下一章。

固定 `/tmp/curio-s38-pepys-4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，9 月 2 日日記 L65807–65834 依序是塔上親見橋端火、塔官**口頭告訴**布丁巷國王烘焙師屋起火的說法、下塔搭船後才見 Michell 家已燒、眾人搬物到 `lighters` 或拋河、有人等火貼屋才上船、強風推火入城。`claims.md` 的 PF015–022 逐句與 `video.json` 旁白相同，沒有將口頭說法改成佩皮斯目擊，也沒有在登船前確認 Michell 屋損失。

| 景 | 書面票 | 來源、動作與生成風險 |
| --- | --- | --- |
| PF015 | **PASS** | 塔上觀看街屋起煙接續日記的橋端大火；成年 writer 握欄、17 世紀服裝、`push in`，不新增確定的住戶去向。問「他們要往哪裡退」是懸念。 |
| PF016 | **PASS** | Lieutenant of the Tower 口頭告訴火源說法；畫面要求 officer 對 diarist 說話，符合聽聞層級。無字地圖只是概念道具，原圖若變成正式書面證物、現代地圖或童貌，必須退。雙人互動是已知造成人物錯置的高風險。`drift left`。 |
| PF017 | **PASS** | 佩皮斯聽到塔官說法而非親見起火瞬間；望窗外煙的動作沒有偷畫火源。成年 Restoration 衣飾與 `pull back` 合書面要求。 |
| PF018 | **PASS** | 日記下塔後坐船，看居民把物品搬上平底貨船 `lighters`；小船觀察者與搬箱動作對應。`family` 是居民群像示意，不能把未記載的親屬關係或兒童當史實；原圖須查成年形象、木船與 1666 道具。`drift right`。 |
| PF019 | **HOLD** | 船上才見 Michell 家已燒的時間順序正確，但 prompt 的 `burned house near city Bridge` 無限定橋型。此前 PF013 即使明說 `old stone-arched London Bridge` 仍生成 1894 年 Tower Bridge；這個更含糊的橋提示詞有已證實的重大年代誤畫風險。先凍結不要求橋體入鏡的窄修候選並獨立核差分，再考慮付費。 |
| PF020 | **PASS** | `flinging into the river` 支持居民把家當拋進泰晤士河；一名成人與一個傾倒動作、17 世紀衣飾、`push in`，原圖仍須查物件與時代。 |
| PF021 | **PASS** | 日記明說有人等火觸屋才跑上船；岸邊居民往船趕、房後有煙是保守示意。原圖不能誤畫成早已安全撤離或現代船；`drift right`。 |
| PF022 | **PASS** | `wind mighty high and driving it into the City` 支持強風推煙火入城；佩皮斯坐船看城屋、`push in`，成年 17 世紀衣飾。問題「誰能讓它停」留到後章，不預先畫出消防結果。 |

七個 PASS prompt 都保留了原 `look.preset=cute-mystery` 的全局風格；各有一個主視角或動作、相鄰 camera 不成三連。老式否定附句與泛稱人物仍有已觀察到的童貌／近代物件／畫風漂移風險，故**書面 PASS 只准單次原生測試**，不可憑 prompt 或機器分數先收圖。PF019 的來源主張本身沒有 HOLD；HOLD 只針對目前畫面指令的橋型風險。

當前 R8t `video.json` SHA-256 `35a23a36a8503988bdb70ff2dc2c6e3bd2f02c226891a5119f3b9756b86d2532`，`script.md`／`claims.md` 分別 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`；正文 106／111 景插圖、連卡最多 2，lint 0 errors／0 warnings。私有 STOP 在位；ledger SHA `660db85effcba9197da0b1b3802ca05cab2a54a4950103f848139498c4df35ea`，US$0.5830／38 image／37 judge／1 music，舊 PF003 US$0.0035 reservation 未動，整集硬限 US$4.58。七景 dry-run 只列這七個 ID、MiniMax `image-01` ready、各 prompt 在長度內；全各一次約 US$0.09，按實際 US$0.0135／景最多 US$0.0945，總額最多 US$0.6775，低於硬限。

先備份 STOP／ledger／manifest 與九張 KEEP baseline，再在 EXIT 恢復 STOP 的**單 ID**指令中試 PF015；每景後查帳本、圖單、原生 JPEG／裁邊圖及九張 KEEP。若同類來源、成年、年代或畫風／黑邊問題達三張，立即停止，未到的 ID 不付款。PF019 始終不進本批；PF009／013／014 已是日記卡，其退件圖不得重新選入。
