# S38 R8ak 十九景正向地面提示獨立增量紙審

2026-10-22 UTC。審者 `/root/s38_pf021_last_paper`，未撰寫此次十九個地面修訂；曾是較早R8ag八十八景prompt作者，因此本票只獨立審查**協調者新增的地面字句及精確差分**，其餘沿用既有來源／畫面審查。結論：**PAPER PASS 19／19**。沒有媒體、creative檔案修改、manifest／ledger變更或Git提交。

現稿video SHA-256 **`5b2ba6712bbff7b021265864d2182a483c2387db592ac6f83b794b84c3f93fe9`**；script仍 `52a65118f58dae3378006d68524a07b41ecd0763e66ac5c931d2798f5560913e`，claims仍 `154e17297a27a6589868908efaab6a0cdef905fd802fb4cc79120aa4d6e7966f`。verify125差分SHA `3ef16279c11d81d837ccbb3ab2d80d7d0c1a096f751c89f79a6ed7db55c87d35`。

## 實際差分與來源界線

逐項核對PF033／038／039／053／058／059／066／075／080／081／082／084／090／093／094／097／099／103／104，共19個prompt。**每一筆唯一新增字串都是 `rough uneven cobblestones underfoot`，位於原有最後光線短語之前**；沒有刪改人物、動作、方向、房屋／物件、因果、日期或光線。以old字串反填全部new，逐位元組回復前稿video SHA `8d4b427f8587ef20fb5a12bf983444766ad68bb527ce4b9acd767ae3df87a172`，其餘場景完整物件及頂層欄位不變。

這些場景原本就是1666英國的街道、巷口、路邊登船處、城門、出庭院接街的路線或街上觀火／搬貨。粗糙石鋪地是**年代相容的正向插畫構圖**，針對PF029／031／033實圖曾出現現代漆線、瀝青路的具體錯誤；它沒有被旁白、claims或來源卡宣稱為日記考證過的每一段真實路面。固定來源仍是Pepys日記commit `68fcf49f70ee793b989a6fd0464264d55beb4451`，全文SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`；原有事件與觀察／聽聞界線由verify116、122及先前來源鏈承接。

PF053車上押送財物沒有變成馬車因此顛簸的新增事件；PF075只是在庭院往街道的出口有石地，不把院子全改成街道；PF080／081仍是炸屋及局部阻火，不聲稱道路材料造成止火；PF097仍是餘燼燙腳的脈絡，不把石地另立成危害原因；PF104仍是另一處火被工人與本人撲滅。未見新增結果或材料性史料矛盾。look／style／negative不變，亦不要求成圖逐塊石頭吻合才能收圖：judge-pass圖仍只因材料性來源／旁白矛盾或畫風漂移退件。

## 口播、KEEP及驗證

全片112個口播ID／文字與前稿逐項相等；script／claims原檔SHA未變。正式lint exit0，**0 errors／0 warnings**。active圖單列的24個KEEP完整場景均未改，選用實檔SHA逐張相符，judge PASS且無needs_review；PF034第二張為協調者及本審已看過的卡通木桶近景，沒有納入本輪修詞。PF033退圖未被此紙審重新接受。

只讀manifest SHA `6d54fd2b1cd7305e3aac6e6d87c4f26d43484ae33e1f3a1125c3e6b8aa1bfb7f`，24 KEEP；STOP在位、jobs空。ledger SHA `64f7cf2d0b27091e73f79e0f369379b0a479b9cdf6e42c4a0cd30d76e072cb66`，實付US$1.2040／84image／83judge／1music，舊US$0.0035 reservation保留。本票未重綁現稿visual hash。

## 實際次數與後續上限

PF033已付**一張**實際原生圖，最多尚可兩張；不能因修prompt而從零算。另查到委派訊息未列出的**PF035已付一張ready原圖**：image key `e0db65b6ca6e3649`，本機 `keyframes/pf035-1.jpg`，尚無對應judge入帳，應是STOP前仍在途的下載。已即時告知協調者；PF035不是零次未畫，須先由快取接回既有原圖再judge，且最多僅餘兩張新原生圖。其他PF036–PF111共76景在快照帳本沒有image紀錄。

按image US$0.0035＋judge US$0.01估：PF033最多兩試、PF035快取圖另一次judge加最多兩試，其餘76景各三試，剩餘上界US$3.142；加現付及reservation為 **US$4.3495 < US$4.58**。價格／額外重評若改變須重算，不得拿網站US$200通用cap取代本集上限。

本票支持在STOP下保留24個KEEP完整條目／實檔、妥善隔離退件並安全離線回綁現稿，核即時模型、餘額、價目、dry-run及各景跨版真實次數後，依既有整集授權繼續有界批次。不得重開已耗盡來源卡或重買24張KEEP；PF035快取不得遺失或被重複收費。這是書面PASS，未自行移除STOP、未宣稱新原圖或整集成片完成。
