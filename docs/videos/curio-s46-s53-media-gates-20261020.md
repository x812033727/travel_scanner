# Curio S46–S53：媒體關卡盤點（2026-10-20 UTC）

這是現行收據與平台額度的**唯讀排程盤點**，不改任何一集已凍結的稿、音檔或圖片，也不把書面分鏡、機器評審或本機委派選擇當成網站站主審核。八個編號中，本表涵蓋已開工的 S46、S48、S49、S50、S51、S52、S53；S47 另有工作票，不屬此批交接。

`media-status --slug curio-s51 --json` 於 2026-10-20 22:34 UTC 回報站台月額度：圖片生成 **18,699／20,000**，但圖片評審 **20,000／20,000、剩 0**，配樂 **60／60、剩 0**。生成後無評審不能驗收為可用插圖；配樂亦不能再生成。依 [S51 額度回條](curio-s51/review/r15-keyframes-pilot3-quota.md)，月額度按 UTC 月重置，下一次預期為 2026-11-01。重啟時先重查即時數值與每集 ledger，不憑本表當日快照開畫。

| 集數 | 已驗證可沿用的語音 | 當前視覺停點 | 無額度前可做的事／重啟順序 |
| --- | --- | --- | --- |
| [S46](curio-s46/verify-26.md) Blackwell 入學 | R14 **118／118、0 旗標**；開場 43.93 秒、正文 10:42.17。 | [兩輪三景試畫](curio-s46/review/r14-art-pilot-second-native.md)僅 **1／3 KEEP**，原方案已停，尚有 107 張正文插圖未畫。 | 保留 R14 音訊；如另設畫面方案，先用原尺寸失敗例設計新的三景可檢查提示詞與預算／停損線，不能把原試畫當已放行整集。 |
| [S48](curio-s48/verify-15.md) 海底電纜 | R10 **102／102、0 旗標**；網站音訊卡仍 pending。 | [兩輪三景試畫](curio-s48/review/r10-media-pilot.md)均 **0／3 KEEP**；錯誤包括舵輪代替收纜輪、光學測量景失焦、電纜變寬路，原方案停止。 | 新視覺方案須先處理三個核心物件的可讀性與年代，重新宣告停損與上限；不沿用已失敗的兩輪作新方案 PASS。 |
| [S49](curio-s49/verify-15.md) 月球騙局 | R15 **131／131、0 旗標**；網站 outline／script／audio 仍待站主。 | [首 14 景原圖](curio-s49/review/r15-final-visual-independent.md) **14／14 KEEP**，整集 122 個 `shot`，其餘 108 景未有同級驗收。 | **額度恢復後優先續畫**現行 exact `visual_hash` 的剩餘景；已通過的 14 張先核 manifest／檔案 SHA，逐張驗新圖，勿整批重付費。 |
| [S50](curio-s50/verify-12.md) 倫敦大火麵包房 | R7 **119／119、0 旗標**；開場 47.03 秒、正文 10:55.37。 | [兩輪三景試畫](curio-s50/review/r7-pilot-second-native.md)均 **0／3 KEEP**，原方案 STOP；全片 113 個 `shot` 尚未畫齊。 | 新方案要避免童貌人物、錯誤灶台與非主動作；先記新的三景測試與停損條件，不直接續買原方案。 |
| [S51](curio-s51/verify-15.md) 加州人號火箭 | R15 **131 句、0 旗標**，實測正文 10:45.07。 | 前 23 景仍有原圖拒收／待定；[第三輪定點三景](curio-s51/review/r15-keyframes-pilot3-quota.md)的提示詞已獨立覆核，評審額度在新圖前用完，`STOP` 保留。 | 額度恢復後先限縮重畫 `cal005/015/018`，按原尺寸查三景；通過前不解除 `STOP`、不開其餘圖或配樂。 |
| [S52](curio-s52/verify-19.md) 金星凌日 | R19 **115／115、0 旗標**；開場 44.13 秒、正文 10:25.03。 | 未完成整集插圖與配樂；網站真人音訊審查仍待決。 | 以 R19 精確稿與 ledger 重報全片圖數／費用，再按系列評審逐張驗收。 |
| [S53](curio-s53/verify-10.md) 舊金山救災小屋 | R10 **126／126、0 旗標**；開場 50.33 秒、正文 9:48.37。 | [插圖非付費報價](curio-s53/review/r10-art-preflight.md)已寫；付費圖、配樂均未做，網站三張手推卡 pending。 | 額度恢復後核當時的精確稿／報價與 ledger，再啟動可愛插圖及原圖驗收。 |

**排程建議：**先續 S49 已通過原圖的同版剩餘景，並在 S51 限縮三景驗證修詞有效；S52、S53 隨後按已過音訊版開畫。S46、S48、S50 先做新的視覺方案和小樣判準，因既定試畫已觸發 STOP。所有七集在整片插圖、配樂、組片、字幕、成片品管及片頭後的可點片尾之前，仍不是完成影片。兩個推薦影片元素與訂閱元素需要私人上傳後於 YouTube Studio 設定；本機外框和說明欄頻道／史料 URL 不能代替可點元素。

## S46 新視覺方案的兩景紙上候選

S46 的原方案已因 **1／3 KEEP** 停止，這裡只替兩張退圖寫候選提示詞；**沒有改 `video.json`、沒有產圖，也沒有重新放行原試畫**。現版 `video.json` SHA-256 `790f04b477f0ad4c91f41e3e089e3c5c486addda36822140b0e2d85167f9f0a4`，依[第二輪原生裁決](curio-s46/review/r14-art-pilot-second-native.md)：`bkw002` 失敗於兩個童貌人物和沒有封口信封，`bkw007` 失敗於主體床頭卡懸浮；`bkw006` 已 KEEP，無須改。

| 景 | 紙上候選 prompt（新方案，未審未畫） | 想解決的可見問題及史料界線 |
| --- | --- | --- |
| `bkw002` | `Medium close shot, a single adult woman in a plain long-sleeved 1840s dress sits alone at a wooden writing desk, her face visible as she lifts one small closed white envelope toward her eyes, the folded triangular seal facing the viewer, soft grey window light` | 把**一人、一封信、可見封舌**放在同一個主動作，不再同時指定美式桌、年齡、長頸服裝等多組次要條件。只示意她手持信，不重建 [1895 自傳轉錄的校方原件](curio-s46/claims.md)或可讀文字。 |
| `bkw007` | `Medium shot, one adult woman in a plain 1840s infirmary stands beside a wooden bed, her hand resting on a blank rectangular bedside card fastened flat against the upright wooden headboard by two visible cords, soft grey window light` | 讓**紙卡、繩、直立床頭板**成為一個可畫的連接關係，避免卡片懸在空中；卡上不畫字、不畫病患。僅示意 [Blackwell 自述的床頭紀錄停寫](curio-s46/claims.md)，不當作存世病歷。 |

這兩句只是給後續製作者和**未參與撰詞者**獨立書面查核的候選。後續應先依固定自傳 [P06](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2153-L2177)／[P13](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)覆核來源及畫面界線，寫明**新的**全片媒體上限、三景小樣門檻和停止條件，才考慮在 `video.json` 實作與額度恢復後的付費試畫。若新圖仍無法清楚顯示床頭卡，可在不破壞插圖占比與敘事節拍的前提下另設少量資訊卡方案；也須重新審核該版，不能把現行失敗圖沿用為 PASS。

本表只依連結收據與當次只讀 `media-status` 排優先序。下一位製作者應以各集 `tasks/open`、`verify-*`、精確檔案 SHA、網站卡及私有工作目錄重新核對；不得由本表移轉任何來源、敘事、政策或視覺 PASS 到改稿後的新雜湊。
