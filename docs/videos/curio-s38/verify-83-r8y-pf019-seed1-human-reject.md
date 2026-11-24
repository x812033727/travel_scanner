# S38 R8y｜PF019 首張原圖獨立目視退件與圖單隔離

2026-10-22 UTC。**PF019 HUMAN REJECT；本批停在 PF019，尚不可往 PF018／PF020–022 購圖或送 storyboard。**非作者直接查看 1280×720 原圖 `keyframes/pf019-1.jpg` SHA-256 `a56b8f49cb68004591c2f38e81c3bdf5230a7f68ddfa0bebcd74286c229e4eae` 及正式選中裁圖 `keyframes/pf019-1-trim.jpg` SHA-256 `230ee66fa1115d01e60cacffeb7fdfc64d80d6f14c44134edade28d1e5e77375`。此輪沒有付費媒體呼叫或提示詞編輯。

固定 R8y `video.json` SHA-256 `586c55b4328c96ab405156467ca2deb7cf294119e4043aaea579c27704404652`；PF019 仍是先前已紙審的原 prompt：佩皮斯於 1666-09-02 泰晤士河小木船上，**隔著船舷向上看岸邊**焦黑屋牆和下垂屋頂。固定 Pepys 日記 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` L65816–65819 明說他到水邊 `got a boat and through bridge`，然後記下 `Poor Michell's house ... already burned that way`。房子是他**從船上看見的岸上受火損房屋**，不是另一艘浮船的上層建築；此時序也避免把塔上掛念 Michell 說成已確認其屋燒毀。

實際兩圖在左側都呈現一段巨大彎曲木船舷／船殼，屋牆立在其上，木船外緣與水面相接；看不見承載房屋的固定岸線。觀者首先會讀成「另一艘船載著一幢屋子」，不會讀成船舷外岸上的 Michell 家。屋牆以淺色木板為主，雖有殘缺梁架，沒有清楚焦黑牆體或淡煙足以確認「已燒」。人物眼睛朝前下方的橫木／船內，不是抬眼看受損房屋。成年面貌、白色頸巾、深色衣服與卡通畫風大致合適，但主體的視線、房屋所在位置及受火損訊息一起失真，直接削弱本鏡的旁白回收。裁邊只去除上方約 1% 細邊，沒有改變問題。

正式 judge 對 image key `df95634e5f36c261`、stamp `aa82075dda74629e` 給 9.29／10、`passed:true`、`details:7`，只列 `character looks forward rather than looking up at the damaged wall`。眼神問題判得對，卻未辨房屋被畫成另一船上的結構及受火損不明；故機器 PASS 不能覆蓋人的來源／畫面判斷。

批後原 manifest SHA-256 `95880607894528f6eb488268323a168dca781464061d7b41d72dc142a773f5df` 已逐位元備份在私人 `review/r8y-pf019-seed1-human-reject/manifest-post-cli.json`，退件原圖／裁圖留在私人工作區供覆核。STOP 在位、jobs 為 `{}` 時，以原 SHA、PF019 key、入選檔 SHA、12 個條目及 11 張 KEEP 雜湊斷言後，**只從 active manifest 移除 PF019，並清空含舊畫面的 contact-sheet 指標**；沒有碰其餘圖單條目、ledger 或影像檔。現行 manifest SHA-256 `112d8b480d189080c7babc59b0fbfacf937cb501858f0ceb9eac42a805848b56`，仍綁 R8y `visual_hash=099da572e40ba916`、`look_hash=98a370ae40badbaf`。11 張先前 KEEP 的完整條目 canonical SHA-256 **`59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`**，每張入選檔 SHA 實算相符；細目見[圖單清冊](verify-83-r8y-pf019-reject-inventory.json)。

ledger SHA-256 `74dcfa1eb94fd57f80c6b3faf2688f384001ab05b20ac7329952c62449bcf237`，累計 **US$0.7685／51 image／51 judge／1 music**，另有 US$0.0035 reservation；私人 STOP 仍在且 jobs 空。若作者要修 PF019，書面提示應明確把房子**固定在對岸陸地**、與佩皮斯的小船隔著水面，明示燒黑殘牆／斷梁且不另畫載屋的船，並讓他朝岸上看；先做可逆單景差分、史料及非作者紙審，再另決定是否限額重試。此收據不放行任何進一步 PF019 付費呼叫、其他鏡頭批畫或全片 storyboard。
