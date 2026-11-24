# S38 R8aa｜PF018 搬家當上船單一畫面修稿

2026-10-22 UTC。**作者提示詞提案，待非作者依固定日記紙審；沒有付費重畫。**R8z PF018 首張原圖[人工退件](verify-87-r8z-pf018-seed1-human-reject.md)：前景主要是孩童，遠方貨船沒有可辨的搬箱動作。原稿把「一人在小船看一家人搬箱」塞進同一張，模型畫成兒童雙船相望。R8aa 只將 PF018 的圖片 prompt 收成**一位明顯成年住戶，把一只木箱舉過平底貨船低船舷，箱子正在入船**；觀眾以看見這個動作理解佩皮斯沿河所見，不要求模型再畫佩皮斯及無史料支持的「一家人」。

[固定 Pepys 1666-09-02 日記 L65816–65834](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65834)寫他 `got a boat and through bridge`，沿河見眾人 `bringing them into lighters that layoff`。新 prompt 的泰晤士河登船處、成年人、木箱和低平貨船是為這句做示意，不把畫面當原件或聲稱日記記了此人身分。旁白「他搭船沿河看，人們正把家當搬上平底貨船。」及 D2a 主張逐字不變。PF019 已審過的日記卡和其他鏡頭均未改。

[可逆單葉差分](verify-88-r8aa-pf018-prompt-structured-diff.json)僅 `scenes[17].data.prompt`；R8z `video.json` SHA-256 `4f30f598c40dcdb9a6cc3d9edd0fa2bb2117d7f455609c4dd4f2730c9f119022` → R8aa `e25b7163f2efa7f830c0b94e421511ceaa4662fb985b53d2290e3a715a16556b`。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`，均不變。正式 lint 0 errors／0 warnings，104／111 正文景仍為插圖，最長連卡 3。

私人 active manifest SHA `a7c5920fd1e4c96b66bb7d9331541c36683987999617279bca9a75c21197c48d` 含 11 張舊 KEEP、沒有 PF018，**仍綁 R8z 舊 visual hash**；ledger SHA `a753f6ef1831579858e439305677e3c4a8599b35141b9136e37099fe84d772c0`，US$0.782／52 image／52 judge／1 music，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。非作者紙審 PASS 後須先做安全離線圖單重綁、再最多一張 PF018 原圖及一次 judge、看原圖判定。PF018 實際原圖嘗試累計一張，本提案不重設計數。
