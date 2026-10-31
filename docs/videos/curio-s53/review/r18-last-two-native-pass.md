# S53 R18｜首章最後兩張原生圖驗收

2026-10-22 UTC。依 [獨立紙審](r18-last-two-prompt-independent.md) PASS，僅對 `s53008`、`s53009` 各畫 MiniMax `image-01` **一次**並各做一次 judge。直接開啟兩張 1280×720 未裁切原 JPEG 及各自裁切所選圖後，**兩張人工 KEEP**；逐張檔案雜湊、機器分數及判定見 [R18 清單](r18-last-two-native-inventory.json)（SHA-256 `1212c1b9242f15db4d367b270a3ed36577a62b9cc54e035888224b81f8bbd745`）。沒有擴畫其他場景。

| 景 | 原圖 SHA-256 | 機器／人工 | 原圖與所選圖的檢查 |
| --- | --- | --- | --- |
| `s53008` | `9c79c5007a62d1f0260814fc42f49e26238975b7ae9b458ba0059a02285baf46` | 9.29 PASS／**KEEP** | 銀髮、皺紋明顯的成年訪查者持合起無字筆記本，走在低矮木板小屋與裸地前；不再有近現代市街、懸燈／電線、童貌與黑邊。裁圖 SHA `e1dfd630cf38cf6fc007eb110e3956c5b82a6af9280a37a72b18ba9b68b3a5f6`。機器只挑景別較遠，未構成旁白或史料矛盾。 |
| `s53009` | `8f3e573603dded9873367290fda8275e63f8a72825c9b6ec4299b1f4035ea070` | 10 PASS／**KEEP** | 灰髮皺紋成年住戶攜折毯，走在兩棟低矮木板小屋間的空曠裸地；不再有東亞式街屋、童貌與黑邊。裁圖 SHA `b957cf0aeee02ea366e48a64c973ca4d38bf41c676e249f0610be841bf641799`。以 1907 年廣場小屋作概念示意，未冒稱 1906 年震災首夜。 |

固定 R18 `video.json` SHA-256 `81c8a7ef0efda1d86c02ab6ebc20199f6b9d70149c2a8cfaab731594e7d06519`。CLI 輸出在私有 `review/r18-last-two-native.log`；它報 2 張新圖、8 張已繪景，因本容器缺相符 Playwright Chromium 而沒有產生 contact sheet，但命令退出 0。人工逐張檢查原圖與裁圖，不把 contact sheet 缺席說成整個分鏡已驗收。

EXIT trap 已恢復私有 `STOP`。前後快照存於 `/workspace/.video-work/curio-s53/review/r18-last-two-pre/` 與 `r18-last-two-post/`，含帳本、manifest、圖檔與 log；既有 `s53002–07` 六景的 manifest 條目及實際圖檔 SHA 完全未動。帳本由 **US$0.2835／21 images／21 judges／0 reservations** 增至 **US$0.3105／23 images／23 judges／0 reservations**，恰增 US$0.0270，低於已核的整集 US$4.78 上限。當前 manifest SHA-256 `2aa4d25a3950d5c076c2565702aff9e8431eed6e7c0ca62a4454a937558fd1f5`；ledger SHA-256 `442d21b4ff1258f7819c7540a462b5ddd296f18e84faaa16e9436ed43eac36ed`。

**首章狀態：**`s53001` 為已獨立核過的來源卡，`s53002–09` 八張插圖各有人工作為候選的 KEEP 圖；原生首章可進一步做聯絡表與聲畫檢視。其他章未畫，完整分鏡、站台卡、人耳、配樂、長片、Shorts 及 Studio 結束畫面連結仍待製作；此回條不是整片批准。
