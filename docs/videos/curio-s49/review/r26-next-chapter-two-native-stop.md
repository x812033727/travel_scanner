# S49 R26｜第二章首兩張原生圖停批

2026-10-22 UTC。R26 [八景獨立紙審](r26-next-chapter-eight-prompt-independent-pass.md)放行 `moon032–039` 的書面提示詞；本輪依序只試 `moon032/033` 各一張 MiniMax image-01 原圖與各一次 judge。**兩張皆人工 REJECT，連續出現來源／年代錯位，已停批；`moon034–039` 未付費試畫。**機器兩張都 PASS，不能取代原圖驗收。

## 開畫前

精確 R26 `video.json` SHA-256 `57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`、`claims.md` `ced02136c94ec5f93f34a62ad5bddfd635b8fde8af93297cff531f91ae40bbcc`、`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。私人 manifest 的 `visual_hash=5781d6810538eb41` 已按[離線重綁回條](r26-next-chapter-manifest-offline-rebind.md)對齊，原有 **26 張 KEEP** 的圖單條目與實際檔案 SHA 再驗為 0 問題。起始 manifest SHA `d6089aa83b3de5ee2e3e32bfeddd55b0ed3adcc2f19d7892a805bec060a31bcb`；ledger SHA `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，US$0.9990／74 image／74 judge／0 預約；jobs 空、`STOP` 在位。站台 `media-status` 回 MiniMax image-01 ready；八景一張各一次 dry-run 約 US$0.11，對照本集已核 US$5.30 上限仍有餘額。每景均以 `--takes 1 --shot <id>` 單獨執行，shell EXIT trap 恢復 STOP。

## 原尺寸與裁圖驗收

| 景 | 站台結果及實際原圖 | 人工結論 |
| --- | --- | --- |
| `moon032` | 原生 1280×720 JPEG SHA `08969032b888ade381744ef83fb77f6619d63173e3858400cbfc3775f70a3f59`，所選即同檔；judge **9.29／10 PASS**，其 `details` 題已指出六格圖與多出的器材。 | **REJECT。**要求的是虛構構想的單張扁平紙，只有物鏡圓與暗室方形；原圖卻把紙畫成六格表，桌上另有紅頭、金屬身的現代手電筒式器材，像在展示已造設備，年代和證據層級都錯。灰髮成人及滿版構圖不能補救。 |
| `moon033` | 原生 1280×720 JPEG SHA `e954202f5302991dc728a4ac0aa98d2a076a3923e33d9021998dd918396d0ba7`；所選 1280×720 裁圖 SHA `8bf22fe8f13441dfe0d0ec64f8b6a6b771b947d12700c51d435de6aa3e339572`；judge **10／10 PASS**、無機器問題。 | **REJECT。**原圖與裁圖皆是明顯童貌人物，穿東亞式衣帽並站在現代頂燈下，並非提示詞所需 1830 年代成年學者在想像暗室中指向素面反射鏡。裁圖沒有消除年代、年齡與服飾錯誤。 |

[逐圖雜湊與帳本清單](r26-next-chapter-two-native-inventory.json) SHA-256 `a5fd10cedea1962d30bdeb31767123c936021860c3796f11d21a779f2c2451f7`。CLI 因容器缺相符 Playwright Chromium 沒產生 contact sheet，已直接逐張看原 JPEG 及唯一不同的選用裁圖；未把 judge PASS 當人工 KEEP。兩張的 `manifest.needs_review=false` 只是機器狀態，**不得送全片 storyboard 或當人工收圖**。

## 停線與交接

第二張驗完即停止；`moon034–039` 無新 job、無圖與評分。R26 原 26 張 KEEP 圖單條目逐項不變，新 manifest SHA `57d169e58776fd22bb03e5c42cdda984a91bff3fcb45643baf49cc9a120e1be8` 只新增兩個機器通過、人工退件的條目。ledger SHA `bdd5c8ebb1b7821f05532cb82af58b888424c31a98443b030a336f427d7067de`，**US$1.0260／76 image／76 judge／0 預約**，本輪加 US$0.0270，低於 US$5.30；jobs 空、`STOP` 已恢復。私有前快照與 CLI 逐景 stdout／stderr／exit 在 `/workspace/.video-work/curio-s49/review/r26-eight-native-pre/`、`r26-eight-native/`。

作者下一輪只窄修 `moon032/033` 的書面提示詞與 claims 同列畫面欄，重做獨立紙審及受控原圖驗收；其餘六景沿用已通過的書面結果，但批次需重新評估是否恢復。台詞／劇本未變。完整分鏡仍有 94 景未獲人工原圖收圖，網站卡、人耳旁白、長短片與 Studio 連結尚待。
