# H05 v2｜三個連續插圖槽位的單張小樣

日期：2026-10-14。站主授權且只執行 `open-threat`、`open-tail`、`open-boy` 各一張 MiniMax `image-01` 1K 圖與各一次 Gemini 判圖；沒有重抽、擴批、送 storyboard 後台或變動原版企劃。這三景是 [原生 `open-note` 示意卡](open-note-diagram-revision-20261014.md) 後的連續付費插圖槽位，不代表整段已可用。

## 付費前鎖定

現行 `video.json` SHA-256 `472db853bc021374430ce5d80387442544cf72cd195f10e9e06aa86b07c94095`；`script.md` SHA-256 `4aa46b59a030b88ac35c7c7c0d9522ae69d41b0715d55a6b899d16bec52d73ba`，narrative `31f279e4aaa020c5`，speech `0b7b642f114d257f`。正式 `timeline.json` SHA-256 `db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee` 與後台音訊核准記錄相符，`status` 讀回 narration approved 及 storytelling panel passed；`narration.wav` SHA-256 `f0ce6fff529dfb60a72c0e7b4479938d48f6f476ca5961b7ea2190ba15f6feac`。專案及上一層均無 `STOP`，專案無 `LEASE`。三鏡分別執行 `keyframes --dry-run --shot ID --takes 1`，均通過提示字數與模型預檢；未改稿。

付費前帳本 20 筆，累計 **US$0.1350**；單片上限 US$80。外部 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/visual-pilot-05-20261014T030330Z/` 封存主稿、腳本、正式時間軸、核准、原 manifest、原帳本與三份 dry-run 輸出。`preflight.json` SHA-256 `0d311a8da16e8ed5187a16ed125be1b31f651e6cc313dd3a3da485327e68f98e`。原 manifest SHA-256 `aa89f3830cf9fb3343bd46aea3f4755ac8a93d7e4aca82f7d3ef04609ab006ba`，原帳本 SHA-256 `7ed7e0157abb0553c714aef1293d6b4752bd83fa80850f5f511e7cb67b16b2eb`。

## 逐鏡結果與人工結論

| 鏡頭與請求 | 原圖／選用圖 SHA-256 | 原判圖 | 人工實看 |
| --- | --- | --- | --- |
| `open-threat`；key `b03c10b67845c880`；job `d7198b57-6d4c-4cd5-a191-e6d5adce8bdb` | 原圖即選圖 `8c42cabded330f272894bc413163734b72ee3db9298182a9894d99a56e66bf56` | 9.29，PASS；但 `details=7` 並指出箱子在乘客腿上 | **退件**。完整 1280×720 圖中有兩名乘客、手與第二個紅包，黃箱放在腿上；讀不到提示所要「空座上關閉的單一公事包」，會引入無來源人物與物件。 |
| `open-tail`；key `c8dd04292446496a`；job `b0ae3571-9e8c-4691-81a3-0e572f2aec3b` | 原圖 `52226da38f6b5ca24796ab01618af88f4f4da7145d08d91bf7416acd664efaeb`；8% 上邊紙邊裁切後選圖 `5b1550581a8d0867f77d6dfd4bb3b4ccc394b1dfd2c89dca709fa68e4f2ed303` | 7.29，FAIL、`needs_review=true`；前景人物、機身字樣、數位繪畫感 | **退件**。原圖及選圖均有六名站在地面的觀眾、機身假字／標誌、非遠距後方視角，也不是口播所需的夜間空中遠景；裁紙邊不能修正。 |
| `open-boy`；key `01c69104c31adeab`；job `2ad47af5-5e13-4e94-b8f3-9cf98a05b409` | 原圖 `d56d7d8ba1d8dc8a4be9d3e42fedeebfcfd4a49d9b1ee20c85154bef293676b7`；8% 上邊紙邊裁切後選圖 `ff2f1f3a3d91692a5d392bdf1628697c7f746ef498701508801ce927e5fbf36a` | 10.00，PASS、0 機器問題 | **退件／本輪不採用**。匿名男孩背面蹲在河岸、無假字，基本構圖較接近；但腳下大片鮮橘紅斑塊容易被讀成未有來源的現場痕跡，天空也偏晴亮而非提示要求的陰天。主製作代理另行打開選圖後同意退件；不以 10 分跳過人工。 |

`open-threat`、`open-tail` 的限制分別對應本地 [c04／c07 查核](claims.md)，而 `open-boy` 的 c12 只確定男孩在河岸發現鈔票，沒有彩色標記地面的紀錄。圖像應被讀作情境插畫，不能讓虛構旁觀者、字樣或地面痕跡像史實。每鏡均以本機圖像工具打開原始 JPG 及實際選圖（若有裁切）；人工結論另記在此，**沒有手改** `keyframes/manifest.json` 的自動 PASS/FAIL。

## 帳本與下一關

每鏡只有 1 筆 MiniMax 圖像 US$0.0035 加 1 筆 Gemini 判圖 US$0.0100。新帳本恰多 **3 張圖、3 次判圖、US$0.0405**；舊 20 筆逐筆不變，現在 26 筆、累計 **US$0.1755**。外部 `audit.json` SHA-256 `fcc6d143dcecdb2dc1a9a85830b20f8cd3f89d228df0fd5d1645756c8a9171d6`，機械檢查三個 request key、各一 take、選圖 SHA、ledger 六筆增量及原本 20 筆不變。最終 manifest SHA-256 `ed2f85155a230caccd2db9c2990515649074cc0e804772683c5df145e8e73fe5`，最終帳本 SHA-256 `cb95b66de84d533c492cc9d1b1cbcf459ecdb7f6e4dd80693361ae439cc0f05f`；每鏡產生後的 manifest、帳本、原圖、裁圖與聯絡表均在同一封存目錄逐次留檔。

第三鏡 CLI 的 exit 1 是因 manifest 中先前 `open-tail` 判圖 FAIL 的整體品質阻擋；`open-boy` 自身生成與判圖均已完成，沒有未知計費狀態。三鏡圖像都保留，但**沒有可核准的連續三鏡**，更沒有完整 61 張付費插圖組。不得把機器 PASS 當作美術採用；先決定是否改為更多原生圖卡或重新設計鏡頭，再另行審核範圍及成本。此輪不再發 MiniMax 請求，不送 storyboard，不宣稱可 render、assemble、上傳或播出。