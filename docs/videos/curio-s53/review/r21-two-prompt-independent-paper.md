# S53 R21｜兩景獨立史料與書面畫面覆核

2026-10-22 UTC。**紙審 PASS 2／2；原生圖尚未驗收。** 本次僅核 `s53010`、`s53018` 的 R21 提示詞，對應 `video.json` SHA-256 `4ac9a518d7387ea66918a89946636ee7dd6412f4926fbe7c5ccbb5a5a249f64a`、`claims.md` `02ee7918a362ce130bed4a9e2c1491f0da80880207d7c57d6aa9eae1820a3022`、不變的 `script.md` `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。非作者自行重讀固定 1913 年 *San Francisco Relief Survey* 原文，原檔 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。

| 景 | 原文、R20 失敗與 R21 書面判定 |
| --- | --- |
| `s53010` | [固定 L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)記 1906 年 4 月 18 日清晨地震、大火在數小時內擴散；成年住戶、院牆及遠煙是明示的原創概念示意，不冒充可辨目擊者。R19 圖有現代汽車，R20 原生圖變成寫實長街與電線桿；R21 指定銀鬢成年比例、人物佔大幅、短舊木牆填滿其餘畫面，紙面足以阻止長街視角且沒有車、電燈、可讀字或未核實的現場文件。**PASS；下一張是第三／最後一次原生嘗試，失敗不得第四畫。** |
| `s53018` | [固定 L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)直說南公園面積不足以放分開的小屋；窄帳棚間距是空間不足的概念示意，非南公園照片或小屋施工圖。R19 供應商拒絕輸入而無圖，R20 真圖有現代高樓與寬大道；R21 用左右與後方帆布牆封滿視野、只餘一人肩寬裸地，且沒有觸發拒絕的英文專名。**PASS；仍須原尺寸核是否畫成真正狹窄、無高樓。** |

[作者可逆差分](r21-two-prompt-structured-diff.json)逐項重新驗證：解析前後 `video.json` 只見 `scenes[9]`／`scenes[14]` 的兩個 `data.prompt` 葉節點變化，`claims.md` 僅兩列畫面欄變化；以新字串逐字反填，可位元組還原 R20 兩檔 SHA-256 `f868ce55f98f7868a8052098d0f6439344585df9e0fa1d0cb32eb0ddbbac21dd` 與 `81f03c571693ff7b28e9898f64dcbb64e9442ec66bde2597c6dfcd7874b7ef1c`。其餘 122 景、126 句台詞、運鏡及章界不變；獨立 CLI `lint --slug curio-s53 --json` exit 0、0 errors／0 warnings。

私人 manifest SHA-256 `75c59a8855284a3defe6f2acfd4f0c30bb52f344e1756bc29ef573cadfb5f1b7`、帳本 SHA-256 `c385ac8815a3ef7e3fa500c79dd1039ee6b9f21fc94bafc2c0c0deebd52c435b` 均與 [R20 停線](r20-two-native-stop.md)相同；14 張早先 KEEP 的場景提示詞未改，`STOP` 在位，`jobs.json` 空，累計 **US$0.4320／33 image／32 judge／0 預約**，低於整集 **US$4.78**。紙審只允許每景一張上限內試畫，還須逐張看 1280×720 原圖與裁圖，不以機器分數代替畫面判斷。

## 媒體服務狀態

紙審後只做一次**唯讀** `keyframes --shot s53010,s53018 --takes 1 --dry-run` 狀態探測，設 20 秒上限；探測逾時 exit **124**，沒有拿到可用狀態，stdout／stderr 皆無資料。先前作者的 dry-run 也因 `https://mokaair.com` 無法連線而失敗，因此本輪**原生試畫 HOLD**，沒有移除 STOP、沒有 image／judge 呼叫。探測後 manifest／ledger SHA-256 仍分別為 `75c59a8855284a3defe6f2acfd4f0c30bb52f344e1756bc29ef573cadfb5f1b7`／`c385ac8815a3ef7e3fa500c79dd1039ee6b9f21fc94bafc2c0c0deebd52c435b`，`STOP` 保留、jobs 清空。待服務可用後再先重驗精確 R21 雜湊、額度、帳本和 STOP，才可各限一次；`s53010` 是第三／最後一張，任何失敗改走同章合格圖重用或來源註記字卡。
