# S38 R8ab｜PF018 第三張前最後一次提示詞窄修

2026-10-22 UTC。**作者提案，待非作者固定史料與書面畫面紙審；本輪沒有付費呼叫。**PF018 已有兩張實際原生圖：[首張](verify-87-r8z-pf018-seed1-human-reject.md)的前景孩童與無人搬箱、[第二張](verify-91-r8aa-pf018-seed1-fail-stop.md)的黑寬帶、未見箱子跨船舷和正式 judge `detached=0` 均退件。R8ab 只修 PF018 prompt，將畫面近取為一位**灰髮、中年、面部有歲月線條且寬肩的成年人**，身穿 1666 年可用的羊毛緊身上衣與亞麻領，雙手正把一只家用木箱越過平底貨船低船舷放上甲板。背景只留河水、陰天，減少近代排屋、帆布及游離索具出現的空間。

固定 [1666-09-02 Pepys 日記 L65816–65822](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65822)先記他下塔坐船，後記居民 `bringing them into lighters that layoff`；箱子的材質與人物造型只是插圖示意，不能宣稱日記辨認過這名住戶或箱內物品。旁白「他搭船沿河看，人們正把家當搬上平底貨船。」、`claims.md` D2a 和 PF019 已過的來源卡均未改。只畫一人一件可辨動作，不再要第二艘小船、岸邊另一群人或精確建築。

[單葉可逆差分](verify-92-r8ab-pf018-final-prompt-structured-diff.json)僅 `scenes[17].data.prompt`；R8aa `video.json` SHA-256 `e25b7163f2efa7f830c0b94e421511ceaa4662fb985b53d2290e3a715a16556b` → R8ab `b955dae2c2620b7477fcdef24606d9c1696f390c927f9fc7be10aa058d0b2ae9`，反填舊字串可逐位元復原 R8aa。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`，均不變；lint 0 errors／0 warnings、104／111 景仍是插圖、最長連卡 3。

私人 active manifest SHA `eca0cddcec00a26be05be63d6d62e6ce71f57e775595dbd74a02ba1cd5f0e507` 含 11 張 KEEP、無 PF018，**仍綁 R8aa 舊分鏡雜湊**。ledger SHA `c40120e6801716b79f867d873c4d2068ca2afd51ebdf379387f9b659a011594a`，US$0.7955／53 image／53 judge／1 music，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。非作者紙審 PASS 後須先安全離線重綁 11 KEEP，再僅試 PF018 **第三張／最後一張**實際原圖及一次 judge。若仍 FAIL／人工 REJECT，就走同章合格圖或日記來源卡，不購第四張。整集硬上限 US$4.58 不變。
