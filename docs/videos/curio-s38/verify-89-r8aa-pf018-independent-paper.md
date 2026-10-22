# S38 R8aa｜PF018 裝箱入船提示詞獨立紙審

2026-10-22 UTC。**PASS，僅限 PF018 提示詞的史料與書面畫面。**這不是新原圖的人工驗收、私人圖單重綁、網站分鏡核准或完片驗收。本審沒有呼叫付費 image／judge／music，也沒有改動私人媒體狀態。

## 來源與畫面

- 重新核對固定 Pepys 日記轉錄 `/tmp/curio-s38-pepys-4200.txt`，SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。[1666-09-02 L65816–65822](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65822)先記他 `got a boat and through bridge`，隨後記居民 `bringing them into lighters that layoff`。`pf018` 旁白「他搭船沿河看，人們正把家當搬上平底貨船。」、`claims.md` 的 `D2a` 對應與這段相合。`pf019` 仍在下一景才呈現已燒的米切爾家，不把他在塔上的擔憂當作親見。
- [R8z 原圖人工退件](verify-87-r8z-pf018-seed1-human-reject.md)的關鍵是前景孩童取代成年觀察者、後景沒有人裝箱。R8aa 把視線落點改為**一名明顯成年住戶正在把一只家用木箱舉過平底貨船低船舷，箱子可見地進入船內**。這是一人一動作，避開原稿的「觀察者＋一家人」雙組互動；不再要求畫出無來源的親屬或孩童，也不依賴遠景才看得到的搬箱動作。提示詞沒有把該人指認為佩皮斯。
- 木箱、既有幾只箱子、衣著和磚屋是日記只稱 `goods` 時所需的時代示意，不是有來源的貨物清單、個人身分或確切建築。`moored beside the bank` 比日記的 `lighters that layoff` 更具體；日記未提供可量的離岸距離，本紙審把它限為裝船動作的插畫佈景，不能據此聲稱貨船確實繫在岸邊。新原圖仍須檢查是否真的畫出**成年人和箱子入船**，以及年代、船型、肢體與系列畫風；機器分數不能代替這項人工判定。

## 可逆差分與靜態檢查

- 從 Git 父提交獨立讀取 R8z `video.json` SHA-256 `4f30f598c40dcdb9a6cc3d9edd0fa2bb2117d7f455609c4dd4f2730c9f119022`；當前 R8aa SHA-256 `e25b7163f2efa7f830c0b94e421511ceaa4662fb985b53d2290e3a715a16556b`。解析 JSON 遞迴比對恰好一葉不同：`scenes[17].data.prompt`，ID `pf018`；新舊字串逐字吻合[作者結構差分](verify-88-r8aa-pf018-prompt-structured-diff.json)。把新 prompt 的 JSON 字串換回舊值後，整份檔案與父版**逐位元相同**。其他 111 景、順序、運鏡、旁白、`look` 和卡片均未變。
- `script.md` SHA-256 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA-256 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`，均與父版相同。正式 `node tools/video/cli.mjs lint --slug curio-s38 --json` exit 0，`errors=[]`、`warnings=[]`、112 句。111 個正文景有 104 個 `shot`（93.7%）與 7 張卡片；最長連卡 3。R8z `visualHash` 為 `7f589efde612587a`，R8aa 應為 `819c6ff2d7c16ad0`。

## 私人停點

`/workspace/.video-work/curio-s38/STOP` 在位，`media/jobs.json` 為空 jobs。現行 `keyframes/manifest.json` SHA-256 `a7c5920fd1e4c96b66bb7d9331541c36683987999617279bca9a75c21197c48d` 仍綁 **R8z** `visual_hash=7f589efde612587a`，只有 11 張舊 KEEP，沒有 PF018；11 筆完整條目 canonical SHA-256 `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`，逐張選圖 JPEG SHA 均與圖單及先前清冊一致。`media/ledger.json` SHA-256 `a753f6ef1831579858e439305677e3c4a8599b35141b9136e37099fe84d772c0`，仍是 US$0.782／52 image／52 judge／1 music，另有舊 US$0.0035 reservation；聯絡表為空。以上與 [R8z 退件清冊](verify-87-r8z-pf018-seed1-reject-inventory.json)相符。

書面 PASS 後，任何新的 PF018 圖像請求都必須先在 STOP 與空 jobs 下安全離線重綁 R8aa 圖單，保全 11 筆 KEEP 與 ledger，再只試 PF018 **一張實際原圖和一次正式 judge**，立即檢查未裁切原圖。先前被退的 PF018 原圖仍算一次嘗試；新 prompt 不重設次數。PF020–022、完整 storyboard 及成片仍未在此審內驗收。
