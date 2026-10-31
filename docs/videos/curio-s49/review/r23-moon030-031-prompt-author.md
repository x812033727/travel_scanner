# S49 R23｜moon030／031 原圖後窄修

2026-10-22 UTC。R22 [原生圖驗收](r22-first-chapter-tail-native-stop.md)已將 `moon028` 放行，首章累計 **25 張 KEEP**；`moon030` 因黑邊 **HOLD**，`moon031` 因擬印字與立體小圓筒 **REJECT**。本輪只改這兩景的 `data.prompt` 與 [claims](../claims.md) 同列畫面欄，待另一人按精確檔獨立書審。沒有改旁白、台詞、其餘 127 景或既有圖檔。

| 景 | 我直接看 1280×720 R22 原圖後的判斷與修法 |
| --- | --- |
| `moon030` | 原圖 `bf2372ee8e31…` 的成年舊式學者、單張無字紙與兩個分開的圓已合故事；原圖頂底信箱黑邊，裁後 `bc965c99c5e7…` 頂部仍約 5 像素暗條。保留人物、動作與留白，只要求牆、窗、桌延伸到畫面四邊。亦可先由下一位評估既有原圖能否用標準可追溯裁邊免費清除；本輪沒有修改選圖。 |
| `moon031` | 原圖 `6e297a01226b…` 雖為成年舊式讀者，紙上密集擬文字，另有離紙的立體小圓筒；`c07bae3d6d80…` 裁圖無法消除。新畫面改為成年讀者看背景上**小型、空心、無陰影的二維墨線符號**，不出現報紙、書本或具體器材。此符號只是旁白所述鏡筒重量的概念，不是取得原報插圖、原設計圖或真實器材。 |

來源界線沿用固定 [P05 L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520) 與 [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)：Herschel／Brewster 省鏡筒對話與父親望遠鏡鏡筒三千磅都是**文章敘事**，Jacoby 批評其光學術語拼貼。數字只由原旁白「文章說」限定，圖上沒有可讀文字或重量數字。`moon030` 為想像討論示意，`moon031` 為平面概念符號；不能當可核史實影像。

[逐字可逆結構差分](r23-moon030-031-prompt-structured-diff.json)保存兩景提示詞及 claims 畫面欄的舊／新全文。R22→R23 SHA-256：`video.json` `26a4812f69c312041509544b1b664c5568b523112d1c17ecfd8c79d5b8ef7052` → `fb144f9e2af0b6c59b08c477a149b21af6291af8b0b328934d96d87e1c3fe0b8`；`claims.md` `4e25e9837f5ea9365490aa40df0c55596124594154a61d58334a89abc5120cfb` → `0071e502905c7669a6bfb70c406921d52e82d5fa54a3e4c8ffd75240eb157809`。逐項反向替換可還原 R22 位元組 SHA。`script.md` 仍為 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。

`lint --json` exit **0**，**0 errors／0 warnings**、131 句；stdout、stderr、exit 已與本回條保存。另以 `keyframes --shot moon030,moon031 --takes 1 --dry-run` 檢查，遠端 `mokaair.com` 連線失敗、exit **4**；這是報價／可用性探測的網路失敗，**未生成或付費**，錯誤及 exit 亦已保存，重試前須確認服務可達。帳本仍為 **US$0.9720／72 image／72 judge／0 音樂／0 預約**（SHA-256 `de005bd134b4668a74c76f8e49262c1b4dbdf21f5e6a19377b4fa148f0887d0a`），圖單仍為 R22 SHA-256 `29fd2d89b96cb1dc609db00263337db9a46cd06089b462151940c399d0095d06`；本輪只有文字變更與檢查，沒有付費呼叫，私有 `STOP` 保持在位。此修法尚未產出 R23 新圖，需獨立書審後才可受控首試，並直接檢查原生 JPEG；機器 PASS 不等於人工放行。網站 outline／script／audio 卡仍待站主，全片分鏡尚未通過。
