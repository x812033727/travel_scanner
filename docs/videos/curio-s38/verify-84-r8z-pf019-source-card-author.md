# S38 R8z｜PF019「米切爾家已燒」日記引句卡提案

2026-10-22 UTC。PF019 第一張 MiniMax 原圖雖由機器判 9.29／10 PASS，非作者的[原圖與裁圖目視](verify-83-r8y-pf019-seed1-human-reject.md)確認房舍像架在第二艘漂浮木船上，沒有清楚岸線、燒痕或煙，人物也未望向房舍；這不能承接佩皮斯從船上**看見岸上米切爾家已燒**的日記記載。原圖已人工 REJECT，舊選圖從私人 active manifest 移除，JPEG 留作證據。作者提案以固定來源的引句卡保留這個關鍵回收，不再請模型猜屋與船的相對位置。

固定 [1666 年 9 月 2 日佩皮斯日記 L65816–65819](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65819)寫 `got a boat and through bridge`，接著 `Poor Michell's house ... already burned that way`。新卡 `kicker=佩皮斯日記・中文譯文`、`text=「米切爾家的房子，已經燒了」`、`sub=他乘船過橋後看見・1666．09．02`，只把原文的屋已燒與看到它的時間／視角譯成繁中，沒有指定屋貌、船型或起火原因。PF019 原旁白「到了船上，他才看見那位熟人的房子已經燒了。」和逐句主張未改。

[兩葉可逆差分](verify-84-r8z-pf019-source-card-structured-diff.json)只將 `scenes[18].template` `shot→big` 及 `scenes[18].data` 換成來源卡。R8y `video.json` SHA-256 `586c55b4328c96ab405156467ca2deb7cf294119e4043aaea579c27704404652`，R8z `4f30f598c40dcdb9a6cc3d9edd0fa2bb2117d7f455609c4dd4f2730c9f119022`；把兩葉逆填可逐位元還原 R8y。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 不變。正式 lint exit 0、0 errors／0 warnings；111 個正文景有 104 張插圖景（93.7%）、7 張卡、最多連卡 3 張，未超出系列下限／上限。新工具 `visual_hash=7f589efde612587a`，look 仍 `98a370ae40badbaf`。

**作者提案，待非作者固定史料與書面畫面紙審。** 私人 active manifest SHA `112d8b480d189080c7babc59b0fbfacf937cb501858f0ceb9eac42a805848b56` 仍綁 R8y，含 11 張既有 KEEP、無退件 PF019；ledger SHA `74dcfa1eb94fd57f80c6b3faf2688f384001ab05b20ac7329952c62449bcf237`，US$0.7685／51 image／51 judge／1 music，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。紙審 PASS 後須先離線重綁並逐張核 11 KEEP，再試 PF018／PF020–022 各一張既有紙審放行的原圖；此卡自身不需新 image／judge。後續約 93 張插圖仍未收圖，整集 US$4.58 上限不變。
