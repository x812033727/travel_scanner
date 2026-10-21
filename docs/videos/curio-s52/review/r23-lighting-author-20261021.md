# S52 R23｜全片晴天與戶外光線窄修

2026-10-21 UTC。R22 開場兩張原生圖已各有可用畫面；在擴畫前，我重新掃描全 113 景的光線詞，發現八格文字會令大溪地海岸出現「window light」，或把**1769 年 6 月 3 日觀測當天**畫成陰天。Cook 當日日誌 [L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)明說 `Not a Cloud was to be seen the whole day`。這些是**待生成提示詞的風險**，沒有把已收的兩張圖說成失效。

[結構化差分](r23-lighting-structured-diff.json)僅修 `s52006/020/021/026/056/071/081/100` 八個 `data.prompt` 的光線片語：岸邊改沿岸自然光；棚下改反射／環境光；明指觀測日的兩個 `overcast` 改晴空下的遮棚反光。各景原本的人物、動作、年份、器材與主要構圖保持；沒有改任何旁白、節奏、卡片、來源或另外 105 景。把八個新字串換回即逐位元恢復 R22 `video.json` SHA-256 **`3e380aa29543a868dd643f588834e188d48c481da4c36e0a738a17968af9ad41`**；R23 現檔 SHA-256 **`86f9b98339a6e29b73446709ebb923f323e77277076a698c718952df725acd81`**。brief／research／claims／script 未改，`speechHash=2af0a08f6e592b5d`，`visualHash=bee2b414f71945db`，lint **0 errors／0 warnings**。

R22 的兩張畫面 prompt 和 camera 本輪未變；工具的逐景快取可望沿用，但新 `visualHash` 仍須由工具實際確認，不能手動移植整版分鏡簽核。私有 `STOP` 現在仍在，ledger **US$0.0675**、整集上限 **US$4.46**。請非作者先核八葉差分、Cook 晴朗日誌、岸邊自然光及是否仍有顯著畫面矛盾，再決定是否擴畫；這份作者回條不放行付費全片。
