# A01 round15 畫面提示詞離線候選 — HOLD

此資料夾從 round14 凍結 manifest 產生新的獨立候選；不覆寫 round14。唯一內容變動是七景的 data.prompt。六章原有 79 鏡、108 句的場景界線、旁白 ID 與文字、claim、loop、series、source map 皆保持不變。畫風仍是 MiniMax image-01 的 cute-mystery。這只是文字候選，沒有產圖、TTS、影片、正式機寫入或審稿收據。

| 景 | 修正後的畫面焦點 | 必守的史料邊界 |
| --- | --- | --- |
| hook-01 | 匿名旅客雙手各提一只沉重箱子，臉與負重是主體 | [Sadow 本人訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)沒有證明當時是月夜或黃昏；移除可見月亮與天空時段。 |
| hook-03 | 前景是承載機器的普通輪板，背景是手提一只無輪箱的匿名旅客 | 凍結的 traveler-heavy 角色會被產圖工序加回提示詞；保留角色並以空地分隔輪板與箱子。來源不支持板材或推板者職業，因此不指定木板與工人。兩個主體仍有混淆風險，須看實際生成圖。 |
| origin-06 | 中性背景的簡化輪子箱展示示意 | [溫尼特卡歷史學會館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)證明留有一只安妮塔自製輪子箱，未證明它就是先前旅程插畫指的那一只；畫面不設館內場景，不指定伸縮木柄或獨特結構，也不當作館藏品外觀重建。 |
| origin-13 | 已裝四個腳輪的箱底，旁置一條繩子 | 本人訪談說明四輪與繩子，沒有提供「用螺絲鎖上第四輪」的製作過程。 |
| origin-15 | 一舊一新的空白資料夾 | [Sadow 專利](https://patents.google.com/patent/US3653474A/en)列出較早的 Kelly 專利；畫面用資料夾表示先後，不偽造兩張歷史專利圖，也不虛構審查員查卷事件。 |
| engine-r12-04 | 箱底近景：窄箱蓋底部兩組、寬箱身底部兩組輪件 | [Sadow 專利原件第 2 頁說明](https://patentimages.storage.googleapis.com/51/47/07/5a7ab3afa14edd/US3653474.pdf)的示例說明四組 23–26 分居箱蓋窄段與箱身寬段；插畫是設計示意，不代表已出售實物。產圖後須人工核對輪件數與位置。 |
| turn-12 | 匿名一般乘客一面拉直立兩輪箱、一面看向手柄 | 產圖工序會附上凍結的 traveler-upright 角色描述，因此動作要與「拉箱」一致。[Travelpro 自述](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)的顧客注意與 1991 年離職是兩條敘述；移除機長帽及同一時地的暗示。第二句仍由旁白交代，畫面不演成 Plath 的個人事件。 |

本輪不替未來源支持的細節補一個「看似真實」的畫面。提示詞用匿名人物與普通道具，沒有品牌標誌、可讀專利文字、實物精確復原或真人特徵。實際產圖提示詞會在鏡頭文字後附上 data.characters 指向的角色外觀；本輪在 effective-prompts.json 逐景列出附加後的完整提示詞、角色與長度，七景在 MiniMax 1,500 字限制內都未截字，並核對八條原有 claim 的來源索引。hook-01 的鏡頭文字明確要求兩只箱子，但凍結角色外觀只寫一只；最終能否畫出兩只仍需實際產圖 QA。hook-03 同時出現前景輪板與背景旅客，也須確認主體沒有混合。若 MiniMax 把輪子放錯、補出文件字、把示意箱畫得像前一段同一物件，應退回該景提示詞；不要拿生成圖當史料。idea-09 的廣告標語仍只在旁白；原提示詞已避開圖中文字，若將來要顯示原文，應由後製文字卡處理，不請影像模型拼字。

執行 node build.mjs --write 產生候選；node build.mjs --check 逐位元組重算。builder 先核 round14 manifest、六章、series 與 source map 的 SHA-256，再核七處原提示詞。其餘欄位一概不准改，並輸出新的 manifest、有效提示詞、來源索引、機械檢查和逐章旁白／claim 雜湊。獨立視覺史料審查與三鏡小樣仍未做，round14 的敘事與事實待審狀態也未消失。

畫面節奏未由提示詞修好。round14 在每分鐘 250 spoken units 的文字估時下有 16 景超過 10 秒，round15 沒改旁白或鏡數，因此仍是同一 16 景：hook-07 10.70；origin-r12-01 10.60、origin-03 11.17、origin-13 10.90、origin-14 10.43、origin-15 11.40；idea-02 11.40、idea-06 10.67、idea-08 10.93、idea-10 11.73、idea-13 10.93；turn-01 10.43、turn-09 11.63、turn-12 11.90、turn-15 11.43；now-01 10.20 秒。這是文字估時，不是 TTS 或實際播放時間；長靜圖可能停滯。後續需以真實旁白與三鏡小樣決定是否剪成新的有根據鏡頭，不能靠同一張圖慢放硬撐。

下一步是獨立審查七景與來源、確認三鏡小樣計畫，再按既有付費與主機關卡執行。此資料夾不授權匯入、正式機部署、付費製作或 YouTube 上傳。
