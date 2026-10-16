# H04 v2｜開場三鏡 MiniMax 修訂小樣

站主在上一輪三鏡人工審查 0／3 後，選擇保留 MiniMax 的混合畫面路線，並**只**授權 `opening-search`、`opening-inside`、`opening-gear` 各一張、每鏡一 take。三鏡維持 `shot`，以免把目前僅 50.3128% 的插畫時長降到規格以下。依 [離線修正草案](./opening-visual-recovery-draft-20261014.md) 只改這三個 `data.prompt`；場景順序、模板、camera、台詞與核准旁白均未改。

送出前，專案及上層 `STOP`、專案 `LEASE` 均不存在；帳本 US$2.8385／每片 US$80 上限、保留額零。已把當時 `video.json`、manifest、ledger、state、timeline、approvals 和會被覆寫的舊圖按 SHA-256 封存於 repo 外。改稿後 `lint` 為 0 errors、4 個既有提醒，三鏡 `keyframes --dry-run --takes 1` 均通過 1K／MiniMax `image-01` 的提示長度與額度檢查。MiniMax 不能在這條路線使用 style plate；畫風只能靠全局 look 文字及產後實看驗證。

| 鏡頭 | 新圖與正常判圖 | 人工逐張實看與連戲結論 |
| --- | --- | --- |
| `opening-search` | 選圖 `opening-search-1-trim.jpg` SHA-256 `5b15c122f4664ef392f08a51fa9abc829cf8fe14f0f6aef74a39411384492d0b`；request key `57de8b7cc4d633f7`；judge **10／10 PASS** | **條件候選**。兩名匿名人物確實在下坡前景、帳篷在遠處坡上，中間留空雪，沒有樹、文字或人物臉。帳篷被坡線擋住大半，只能作「發現帳篷」的泛化遠景；不可據此復原現場位置，仍待前後鏡與原旁白試播。 |
| `opening-inside` | 本次原圖 `opening-inside-1.jpg` SHA-256 `81cb65e60099b0b37baea620ef21499ab78f8eb1b07cca9c671628ec75ab3ac9`；request key `9fed090d891a3a91`；judge **9.29／10 PASS**，細節 7 分 | **人工退件**。能看出無人的平面帳內，但出口正對一片樹林，與前鏡無樹山坡的空間關係衝突；入口與底布也不能確認同一帳篷。不能因 judge 通過而採用。工作目錄 `opening-inside-1-trim.jpg` 是 10 月 13 日舊圖，本次 manifest 指向新原圖。 |
| `opening-gear` | 選圖 `opening-gear-1-trim.jpg` SHA-256 `4395048bbf813b37fa168c3baaa1fbbbc6143fbb6c2142075fd1e24685528c7a`；request key `b0f4aef245d47bc4`；judge **9.29／10 PASS**，細節 7 分 | **人工退件**。雖有空帳與衣物，圖像畫出具鞋帶的具體靴款、分散的物品擺法，會被誤讀為第 385 頁的實物清單與位置；帳口和地布與前鏡不同，也沒有連戲。精確鞋衣主張仍由已登錄第 385 頁卷宗卡承擔。 |

三個不同鏡頭各發出一次 MiniMax 圖像請求和一次正常 Gemini 判圖，帳本圖片 212→215、判圖 210→213，US$2.8385→**US$2.8790**，本輪實際增加 **US$0.0405**，reserved＝0。每張原圖與實際選圖、三階段 manifest／ledger、舊檔快照、請求鍵、SHA 和人工記錄保存在外部 `<home>/mokaair-work/videos/curio-h04-v2/review/pilot-mixed-three-opening-20261014/`。最終 `video.json` SHA-256 `77cc48df04e88fc35caa57fbfe7328ea984c63c296875912d32128a911429eed`，manifest SHA-256 `1e4f2001198c93afe78cefb3461634b4f2be43e4993bf94bfb384fb7cd1e1fcc`，ledger SHA-256 `3360f754379d1c33d1c89f6f4043d72e44934e4d80f9847a3b694de1cc3fa3fd`。

台詞不變，所以現行 narrative hash 仍是 `bd49404ff2771d33`、獨立說故事審查 **11／11**；`script_hash` 仍是 `831dbcdd2c7a88a3b36498249ab077c41065956a6f1f6acd768e7a6c27970047`。`timeline.json` SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71` 與後台音訊核准紀錄完全相符，`narration.wav` SHA-256 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd` 也未變。`shot` 時長仍為 7,963／15,827 格＝50.3128%；正式媒體品質未因比率合格而通過。

本輪僅 **1 張條件候選、2 張人工退件**，三鏡不能作同一帳篷的連續畫面，尚未做有聲試播，也沒有送 `review-push --gate storyboard`。49 個 `shot` 中 manifest 僅記四鏡；其餘 45 鏡仍缺現行圖片，片頭 `opening-question` 指向的縮圖也未通過。須先離線處理帳內無樹背景與鞋衣來源界線，重新確立可相接的造型基準；在這個小樣結果下不啟動全片 MiniMax 擴批。後續若改用有來源標示的原創圖解，應先補足並實測至少 153 格有敘事作用的安全 `shot`，再重算比例、最長狀態與相應核准雜湊，不能把這輪退件圖當成可用素材。
