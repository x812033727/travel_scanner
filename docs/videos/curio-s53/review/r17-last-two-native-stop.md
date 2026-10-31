# S53 R17｜首章 `s53008–09` 兩張原生圖停線

2026-10-22 UTC。依 [兩景書面紙審](r17-s53008-09-prompt-independent.md) PASS，對 `s53008`、`s53009` 各做 MiniMax `image-01` **一次**生成與一次 judge，直接開 1280×720 **未裁切原 JPEG**。兩張均被機器評為 9.29/10 PASS，**人工兩張都 REJECT**；[逐張雜湊與判定清單](r17-last-two-native-inventory.json)記原圖、所選圖及評審問題。沒有續畫任何全片其他景。

| 景 | 未裁切原 JPEG SHA-256 | 人工退件理由 |
| --- | --- | --- |
| `s53008` | `530c5df852f300946dfc0ef36361e8499ef2713d7cd681be7c0a5a8308f44483` | 1908 訪查場景卻畫成近現代街道：現代立面、懸掛路燈／電線、黃背包與領帶，人物偏童貌。地圖雖無可讀標籤，整體年代已錯；機器只指出「沒有窗光」，漏判重大背景矛盾。 |
| `s53009` | `4b94deba4ae8dc3a6af72e216542c9ae3bed11d91ac8e224f3fad63edec187bd` | 未裁切原圖上下明顯黑色 letterbox，前景人物童貌，背景是東亞式街屋與屋簷；沒有 1907 舊金山的公共廣場或低矮救災小屋。機器只指出近景取代廣景，漏判年代、地點與風格。裁邊所選圖 SHA `d1c8c36ab94cef615f9f3f230582b8ebacee81f6785fa10932a70b0b31c6b537` 不能補救地點錯置。 |

稿件仍為 R17 `video.json` SHA-256 `6550c8f26db13d1f72e9f706404e8d80efe131789fb4b37918b2ea9f48e222ae`；STOP 用 EXIT trap 恢復。私有前後快照、原圖、裁圖、manifest、帳本、log 在 `/workspace/.video-work/curio-s53/review/r17-last-two-pre/`、`r17-last-two-post/`、`r17-last-two-native.log`。帳本由 **US$0.2565／19 images／19 judges** 到 **US$0.2835／21 images／21 judges**，恰增 US$0.0270，預約 0，低於 **US$4.78** 整集上限。當前 manifest SHA-256 `adac73fbf24d0e98cd1c501f65c0752492df745845f8b37e01d153d7968ec3b7`，ledger SHA-256 `dfb36735a8e2f5d1616ac71e55601e59aba7f2d38532f5b775e5c087652d5e6b`。

首章 `s53001` 來源卡與 `s53002–07` 六景已有人工作為候選的圖（`s53007` 合規重用 `s53003`），**但 `s53008–09` 尚無可收圖，首章及全片分鏡仍 HOLD。**下一步作者只對這兩景的成年訪查員、1908 街景／1907 廣場小屋、可愛漫畫風與畫框做具體 prompt 修復，留下逐字可逆差分後由另一人紙審；在解決重複出現的現代／東亞街景前不擴大付費批次。網站卡、人耳、配樂、長短片與 Studio 連結仍待完成。
