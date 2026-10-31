# S53 R20｜第二章兩景獨立書面覆核

2026-10-22 UTC。**PASS，僅准 `s53010` 與 `s53018` 各一張受控原生 MiniMax 試圖；原圖尚未驗收。**我未參與 R20 作者修稿，也未改創作檔。覆核輸入 `video.json` SHA-256 `f868ce55f98f7868a8052098d0f6439344585df9e0fa1d0cb32eb0ddbbac21dd`、`claims.md` `81f03c571693ff7b28e9898f64dcbb64e9442ec66bde2597c6dfcd7874b7ef1c`、`script.md` `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。

重新讀取固定 1913 年 *San Francisco Relief Survey* 原始文字，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。L1438–1465 明說 1906-04-18 05:12 地震、火災隨後蔓延；L4848–4870 明說 South Park 面積不足以容納分開的小屋。兩句旁白、claims 和分鏡 ID 一致。R20 的匿名成年住戶、庭院牆與火煙，以及近排帳棚和工作者，均是說明性的原創示意，不宣稱是原始照片、可辨個案、建築圖或地圖。

- `s53010` **PASS**：1906 年清晨、明確成年面容、舊式衣著、裁近住宅牆與遠煙符合來源且避開 R19 原圖的現代車街景；要求看原圖是否仍生出汽車、電街燈、現代街區、童貌或不同系列畫風。
- `s53018` **PASS**：畫面只用 1906 舊金山小型公共救濟公園通稱，不把 `South Park` 英文專名送圖像模型；擠近的帳棚與狹窄裸地說明來源所述空間不足。須在原圖驗出帳棚與窄地、無已建小屋、假地圖、文字地名或現代設施。R19 `input new_sensitive` 的成因未經供應商確認，不能宣稱已消除。

[R20 可逆差分](r20-two-prompt-structured-diff.json)反向將兩景 prompt 和 claims 同列視覺欄回填，兩檔位元組 SHA-256 恰回 R19 `62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a` 與 `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84`；其他 124 景、126 句口播與劇本未動。當前 manifest SHA `eafb17ba8426f1c6e79c263bed1bbfcb73f896bc8150b54cff3033e7cf9f0f66`；首章八張和 R19 六張共 14 張 KEEP 的 request key、選圖路徑及實際檔案 SHA 已作試畫前快照。帳本 SHA `e4761e22531131c77d9dbae201af16c822afad5c6bdf58d013395b16e6f68c69`，US$0.4050／31 image／30 judge／0 預約；`STOP` 在位、jobs 空。`keyframes --dry-run` 顯示 MiniMax `image-01` ready，兩景提示詞各 549/1070、502/1072 字元，在預算內；每景一次含 judge 約 US$0.0135，兩景最高 US$0.0270，仍低於整集 US$4.78 上限。

下一步在 EXIT/finally 恢復 `STOP` 的受控逐景指令內各試一張，再直接看 1280×720 原圖及選圖裁切。機器 PASS 不取代人工；三個相關原圖缺陷立即停批。這份紙審不核准其他章節、完整 storyboard、網站卡或成片。
