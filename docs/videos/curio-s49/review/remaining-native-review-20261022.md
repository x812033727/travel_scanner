# S49｜剩餘插圖批次首圖原尺寸覆核與 STOP

2026-10-22 UTC。**`moon049` 第二張雖獲機器 9.29 PASS，獨立原圖判 REJECT；已立即設下 `/workspace/.video-work/curio-s49/STOP`。** 工具在 `moon050` 首張機器 FAIL 後排空，log 明寫「stopped by the STOP file after 3 new keyframes」。這不是剩餘 79 景通過，也不動既有 36 張 KEEP。只對本次實際新增的原圖作以下判定；普通 chibi 比例與小道具簡化本身不是退件理由。

| 景／本批 take | 原生檔 SHA-256 | 機器與人工判定 | 依據 |
| --- | --- | --- | --- |
| `moon049` take 1 | `34312d087766d550bd41f7fbd6db04758211071d995ca0f6d4c027ae69308be6` (`moon049-1.jpg`) | 機器 **8.71 FAIL**；未選圖，無人工 KEEP | 原圖右下有可辨浮水印，畫風偏敘事動畫，人物正拿著裝在框中的冒煙圓筒而非獨立玻璃鏡片。由工具自行重試；保留敗圖紀錄。 |
| `moon049` take 2 | `d061b71d655b4438553c93cbf1f5e52c1fe8e4b729989aebe72d4e443de8cb3b` (`moon049-2.jpg`) | 機器 **9.29 PASS**、manifest selected 同原圖；**獨立 REJECT／STOP** | 本景口播是虛構報導說「鏡片先運到倫敦，再替它造顯微鏡與轉動架」。固定重印本第 501–511 行明確把完成並運到倫敦的**巨大圓形光學鏡片**，與後建的顯微鏡和水平／垂直可動框架分開。畫面卻只有已裝入素木框的**矩形窗玻璃**，桌上沒有可辨的獨立圓鏡；主動作與主角物件都消失。機器 notes 亦直指「plain model lens is missing from the table beside the frame」。這已把故事核心的光學鏡片換成窗片，不是可容忍的小道具幾何差異；更不能把虛構器材當 Herschel 真實裝置。 |
| `moon050` take 1 | `cea6a02d90119cab716592513266d7db41b61a31af4b8ac7660167442e1201e4` (`moon050-1.jpg`) | 機器 **8.71 FAIL**；manifest `incomplete`，**無 selected、無人工 KEEP** | 一張圖有兩人，地圖已畫虛線航路且含可讀中文假字；原提示是 1830 年代一名讀者指向**無字紙圖**，不能冒充真航線文件。工具原欲修後重試，但 STOP 已在下一次付費前擋住。此景仍待後續完整驗收。 |

來源限度：`claims.md` 的 `moon049` 指向 Locke 名下 **1859 年重印本**固定全文第 501–511 行；此為 1835 年虛構新聞的後出文本，**不是** Herschel 真實鏡片或 1835 年原報照片。`moon050` 的運輸、出航說法也是該虛構文本第 553–568 行。固定本機全文 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。

停止時狀態：本批新增 **3 次實際 image、3 次 judge**；帳本總計 **106 image／106 judge／US$1.431、零預留**，`media/jobs.json` 為空物件、沒有進行中的工具程序，STOP 在位。`moon049` 實際已用 **2／3**，只餘一次；`moon050` 已用 **1／3**，仍待修後續畫。其餘 77 個新景尚未生圖；36 個既有 KEEP 的內容與檔案不因本票改動。停止時 `keyframes/manifest.json` SHA-256 `d9bdfcec53f7059388fde67ff3fe82f6cf24c296c9f24a69220a793d050b6e4b`，`video.json` SHA-256 `461a8c6f3cf3f2df0878321697a9f4a062cf699652bfddeb02856975eb6849d8`，`claims.md` `d0db751d0fbccd7ee2618a061096b6aca1f8b4927dcec3e2b623809cb0f6295e`。本覆核只建立文件與 STOP，未動 creative、manifest、媒體帳本或呼叫付費工具。
