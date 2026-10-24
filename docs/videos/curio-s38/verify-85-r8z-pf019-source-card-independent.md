# S38 R8z｜PF019 日記引句卡獨立紙審

2026-10-22 UTC。**PASS，僅限 PF019 由退件插圖改為史料卡的書面內容與畫面配置。**這不是已重綁私人圖單、已收 PF018／PF020–022 新圖、網站站主核准或整集完片驗收。未執行付費媒體呼叫，也未修改作者的分鏡、旁白或主張。

## 獨立核對

- 重新讀取固定的 Pepys 日記轉錄 `/tmp/curio-s38-pepys-4200.txt`，實算 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，與 `research.md` 相同。1666 年 9 月 2 日條目 [L65816–65819](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65819)先說 `got a boat and through bridge`，接著 `there saw a lamentable fire. Poor Michell's house ... already burned that way`。卡片「米切爾家的房子，已經燒了」是省去地標的中文摘譯；下標「他乘船過橋後看見・1666．09．02」有正確的日期與見聞次序。它沒有把塔上擔憂誤作親見，也沒有虛構岸邊房屋外觀。`中文譯文` 標籤讓觀眾知道不是日記中文原文。
- `pf018` 先說搭船沿河與人搬家當，`pf019` 原旁白仍是「到了船上，他才看見那位熟人的房子已經燒了。」，`pf020` 再講有人丟東西入河。卡片在三者中間接住日記的辨認時刻，與 `claims.md` 的 `pf019 → D2a` 相合。退件原圖的人物未望向岸上、房屋像漂浮船體；來源卡不繼承該視覺錯誤。
- 從 Git 父提交獨立讀出 R8y `video.json` SHA-256 `586c55b4328c96ab405156467ca2deb7cf294119e4043aaea579c27704404652`，目前 R8z 為 `4f30f598c40dcdb9a6cc3d9edd0fa2bb2117d7f455609c4dd4f2730c9f119022`。遞迴比較只見 `scenes[18]` 的 `template` 及 `data` 物件變動；將舊 `shot/data` 原文在父版換成新 `big/data`，所得檔案 SHA 與 R8z **逐位元相同**。112 個場景 ID、所有旁白、其餘場景、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` 均未變。
- 正式 `node tools/video/cli.mjs lint --slug curio-s38 --json` exit 0，`errors=[]`、`warnings=[]`。除 `pf112` 片尾外，111 個正文景為 104 個 `shot`、7 個卡片（插圖占 93.7%），連續卡片最多 3 張；新 `pf019` 與 `pf013–015` 的三張卡之間隔著三個鏡頭，不使卡片連用過長。
- 私人圖單實算 SHA-256 `112d8b480d189080c7babc59b0fbfacf937cb501858f0ceb9eac42a805848b56`，仍綁舊 `visual_hash=099da572e40ba916`，其中只有 11 筆既收選圖、**沒有 `pf019`**；逐張選圖檔雜湊與條目所記 SHA 一致。ledger SHA `74dcfa1eb94fd57f80c6b3faf2688f384001ab05b20ac7329952c62449bcf237`，累計 US$0.7685／51 image／51 judge／1 music，另有 US$0.0035 預約；`STOP` 在位，jobs 空。本紙審沒有動它們。

## 下一關

在任何新圖之前，先以精確檔案雜湊和 11 筆 KEEP／實際檔案 SHA 斷言，備份舊 manifest，離線重綁新分鏡 `visual_hash=7f589efde612587a`，清除過期 contact sheet，確認 `pf019` 保持無圖條目，且 `STOP`、jobs 狀態受控。之後才可按既有獨立紙審，對 PF018、PF020–022 各做**單張**原圖及人工來源／年代目視；每張退件就停止並留下收據。整集 US$4.58 上限及人耳、站主、長短片驗收仍各自待完成。
