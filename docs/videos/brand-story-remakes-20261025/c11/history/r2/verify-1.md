# C11 UCC R2｜獨立來源與書面配鏡差分查核

查核者：`/root/c11_r1_source`。未撰寫中文候選或研究；未讀 native／blind 投票。

**SOURCE PASS／WRITTEN VISUAL PASS。** 無來源 blocker。

## 綁定輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `b3890b62bee517866a037249d9d5a853f39c5b52f7be0ac7e988fe053daa0156` |
| script.md | `78deb0291c93938e8e92760bfb46c509e3348a2ffe7efbbcfd8b10b70974ba7e` |
| narration-only.json | `1fe15fda9f959f32581e20748c5ee51fe9e9c518817aed4c48a4c7d98d3c30ad` |
| claims.json | `bfdc52d4ee66a39061d85a5955109edae2c31b499fdd2682e010c6dab695ba78` |
| reviews/source-r2-independent.json | `6489003dbff232c93d52a7530d5ff192fee6fba6ea25d1520ed1557c5d1a174a` |

R1 封存四核心綁定如下；R1 獨立報告 SHA `1b079f5056f4537f3b7c40795cb9d5ff8e0a07fb4108e7a803140151a2074a76`，R1 verify SHA `07e71456a58210030c4f990d78c0d8877c350338b0a69b0c6ef8b03b20eccb3c`。

| R1 封存檔 | SHA-256 |
| --- | --- |
| history/r1/video.json | `08a9c4e28411909bc4a2b95c47d7bb8f4832c37bba9333f5b009bf645819b08d` |
| history/r1/script.md | `d4497864572a1fe4bb9fc5fadb9acc07744b26e8f10b9f7310b5a525508d3279` |
| history/r1/narration-only.json | `0495cf0e6664aefaed5de83c3df526ad2b7176f0e2f0276a72da3aded5f0aef7` |
| history/r1/claims.json | `138f5ac1c87e7019c5d503331cfa6e0e7582769b86a40dcdc2cfb7486dda8f1a` |

## 差分與原件

R2 只改 h01 有聲文字、刪 t03；其餘 87 句相同。85 個保留圖景的 prompt／camera／visual 與一景三句片尾資料完全相同。85 個完整場景物件未改，只有 h01 場景的 text 改動；86 筆完整 claims row 未改，h01 更新 claim／kind／context，d12 只更新 author_context。首個 loop 由 h03→d12 改為 h01→d12，其餘 23 個 loop 物件未改。

原廠 UCC2025 原 HTML SHA `49619fe308ca3eb54f5585f5de4a788020d4cecfcc3f00ba291a8af6c5505656` 已重開、獨立重抽並親讀 p189–191；初代物件照也重開。原文列初代 1969、神戶本社保管，以專用工具開飲口及空氣孔兩處飲用。

- h01「只開一個孔就夠了嗎」是以規定做法提出的條件問句；不主張真有人單孔失敗、單孔必然不能流出，或今天打開神戶保存原罐。匿名持罐與另置工具提示詞沒有新增實驗。
- d12 的飲口／空氣孔用途直接對應 p190，是來源可支持的有限答案；沒有補壓力、流量或失敗經驗。
- t03 刪除重述後，t01 採訪歸屬與分離現象、t04 問題及 t05 均質化處置仍完整。
- 24 個 loop／48 個端點皆存在且向前，逐組讀過當前 setup、payoff 及來源關係；沒有引用刪除 ID。這不是敘事評分。

35 筆原始收件 bytes／SHA、31 個研究錨點加兩個新增錨點，以及文字／段落快取均重新驗綁；87 個保留句承接本人原先獨立 R1 查核。三份凍結研究、舊 28 檔及唯讀快照 SHA 不變，history 未改。

## 逐句來源結果

| 句 ID | 結果 | 來源 |
| --- | --- | --- |
| c11r1h01 | PLAN | UCC2025 |
| c11r1h02 | ATTRIBUTED | UCC2025 |
| c11r1h03 | PLAN | UCC2025 |
| c11r1h04 | PLAN | UCC2026、UCC2025、JNET2023 |
| c11r1h05 | PLAN | JNET2023、UCC2025 |
| c11r1h06 | PLAN | UCC2026、UCC2025 |
| c11r1o01 | ATTRIBUTED | UCC2026 |
| c11r1o02 | ATTRIBUTED | UCC2026 |
| c11r1o03 | PLAN | UCC2026 |
| c11r1o04 | ATTRIBUTED | GUINNESS2019 |
| c11r1o05 | PLAN | UCC2026 |
| c11r1o06 | PLAN | UCC2026、HAMADA2021、SHIMANE_FIRST |
| c11r1o07 | ATTRIBUTED | HAMADA2021、SHIMANE_FIRST |
| c11r1o08 | ATTRIBUTED | CAN_INTERVIEW、UCC2026 |
| c11r1o09 | ATTRIBUTED | UCC_MUSEUM |
| c11r1o10 | PLAN | UCC2026 |
| c11r1o11 | ATTRIBUTED | JNET2023 |
| c11r1o12 | PLAN | UCC2026 |
| c11r1o13 | PLAN | UCC2026 |
| c11r1o14 | PLAN | JNET2011 |
| c11r1t01 | ATTRIBUTED | JNET2011 |
| c11r1t02 | PLAN | JNET2011 |
| c11r1t04 | PLAN | JNET2011 |
| c11r1t05 | ATTRIBUTED | JNET2011 |
| c11r1t06 | PLAN | JNET2011 |
| c11r1t07 | PLAN | JNET2011 |
| c11r1t08 | PLAN | JNET2011 |
| c11r1t09 | ATTRIBUTED | UCC2026、JNET2011 |
| c11r1t10 | PLAN | JNET2011 |
| c11r1t11 | PLAN | JNET2011 |
| c11r1t12 | PLAN | JNET2011 |
| c11r1t13 | ATTRIBUTED | JNET2011 |
| c11r1t14 | PLAN | JNET2011 |
| c11r1t16 | PLAN | UCC2025_REPRO |
| c11r1w01 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w02 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w03 | PLAN | UCC2025_REPRO |
| c11r1w04 | PLAN | UCC2025_REPRO |
| c11r1w05 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w06 | ATTRIBUTED | UCC2025_REPRO |
| c11r1w07 | PLAN | UCC2025_REPRO |
| c11r1w08 | PLAN | UCC2025_REPRO、JNET2023 |
| c11r1w09 | ATTRIBUTED | UCC2025_REPRO、JNET2023 |
| c11r1w10 | PLAN | GUINNESS2019 |
| c11r1w11 | ATTRIBUTED | GUINNESS2019 |
| c11r1w12 | PLAN | GUINNESS2019 |
| c11r1w17 | ATTRIBUTED | GUINNESS2019 |
| c11r1w13 | ATTRIBUTED | GUINNESS2019 |
| c11r1w14 | ATTRIBUTED | GUINNESS2019 |
| c11r1w15 | PLAN | GUINNESS2019 |
| c11r1w16 | PLAN | JNET2011 |
| c11r1s01 | ATTRIBUTED | JNET2011 |
| c11r1s02 | ATTRIBUTED | JNET2011 |
| c11r1s03 | PLAN | JNET2011 |
| c11r1s04 | PLAN | JNET2011 |
| c11r1s05 | PLAN | JNET2011、UCC2025、JNET2023 |
| c11r1s19 | ATTRIBUTED | JNET2023 |
| c11r1s20 | ATTRIBUTED | JNET2023 |
| c11r1s21 | ATTRIBUTED | JNET2023 |
| c11r1s06 | CONFIRMED | UCC2025、JNET2023 |
| c11r1s07 | ATTRIBUTED | JNET2023 |
| c11r1s08 | ATTRIBUTED | JNET2023 |
| c11r1s09 | PLAN | UCC2025、JNET2023 |
| c11r1s10 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s11 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s12 | PLAN | UCC2025、JNET2023 |
| c11r1s13 | PLAN | UCC2025、JNET2023 |
| c11r1s14 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s15 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1s16 | ATTRIBUTED | JNET2023 |
| c11r1s17 | ATTRIBUTED | JNET2023 |
| c11r1s18 | PLAN | JNET2023 |
| c11r1d01 | ATTRIBUTED | UCC2025、JNET2023 |
| c11r1d02 | ATTRIBUTED | JNET2023 |
| c11r1d03 | PLAN | JNET2023 |
| c11r1d04 | PLAN | JNET2023 |
| c11r1d05 | PLAN | JNET2023 |
| c11r1d06 | ATTRIBUTED | JNET2023 |
| c11r1d07 | ATTRIBUTED | GUINNESS2019 |
| c11r1d09 | PLAN | UCC2025 |
| c11r1d10 | PLAN | UCC2025 |
| c11r1d11 | CONFIRMED | UCC2025 |
| c11r1d12 | CONFIRMED | UCC2025 |
| c11r1d13 | PLAN | UCC2025 |
| c11r1d14 | PLAN | UCC2025 |
| c11r1ct1 | PLAN | JNET2011、UCC2025_REPRO、JNET2023、UCC2025 |
| c11r1ct2 | PLAN | 觀眾提問／頻道邀請 |
| c11r1ct3 | PLAN | 觀眾提問／頻道邀請 |

## 範圍限制

官方規劃正文 2,550 spokenUnits，含 coldopen 166 與有聲 CTA 103。原生估時約 700.77 秒，只是規劃估計；實聲未知，不判時長 PASS／FAIL。正式頻道 bookends 另計。

本檔只核來源與書面配鏡。1978／1981 拉環矛盾、Mira 與含奶首款歸屬、歷史回顧與現場原件的界線維持 R1 限定。未授予 owner／預算、canonical、provider、讀音、TTS／實聲、生成圖、素材沿用、音訊字幕、媒體 QA、打包或發布核准；作者 PENDING／HOLD 未改，core／research／history／task／其他 reviews 未改，無 Git、後台或 spawn。
