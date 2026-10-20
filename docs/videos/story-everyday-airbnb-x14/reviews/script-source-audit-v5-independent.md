# X14 v5｜SEC 原件獨立來源與畫面查核：HOLD

**判定：HOLD。** 本收據只對 `video.json` SHA-256 `e38a12eef5f51da9eb13b8a1cab3bb7b7fdc867889e7580ae1c11cd1b961c199` 與 `shorts.json` SHA-256 `b581e9f717769bace170833d8ef48c36b7b499fcf306baaa40542dffbf31ac2e` 有效。2026-10-20 重新計算兩檔雜湊，並重新核對本機保存的 **同日從 SEC EDGAR 下載的 HTML 原始位元組**，非只讀作者的來源矩陣。A5 超過工人 3 MB 上限，僅供編輯者交叉核對。

| 原件 | 位元組 | 原始檔 SHA-256 |
| --- | ---: | --- |
| [A1：2020 Form 10-K](https://www.sec.gov/Archives/edgar/data/1559720/000155972021000010/airbnb-10k.htm) | 2,521,385 | `253c29e43012a62bf28b46ca69538d06994173398a49efa0e8a0b4d5d29f4331` |
| [A2：2020 Q4 股東信](https://www.sec.gov/Archives/edgar/data/1559720/000119312521056952/d147144dex991.htm) | 427,883 | `9cab0c90a7dee23d2663103af33ad9d11234ac383eefeca528e1f63b0376be33` |
| [A3：2021 Q4 股東信](https://www.sec.gov/Archives/edgar/data/1559720/000119312522043371/d251410dex991.htm) | 508,751 | `49605a7f787f9bd5fc9c30b58c3e9b35c13fb4f03f75ea676530ca20910e23be` |
| [A4：2022 Q4 股東信](https://www.sec.gov/Archives/edgar/data/1559720/000119312523039008/d451233dex991.htm) | 510,232 | `2e8d8f02457f3faf05c02555e365532f8b32b5cd60dd410b7a585e074c832ca1` |
| [A5：2022 Form 10-K，reviewer_only](https://www.sec.gov/Archives/edgar/data/1559720/000155972023000003/abnb-20221231.htm) | 3,213,119 | `ba6984f9a29367aa4aa7686b40ee8176b346704b626a7c07d01abf4157568277` |

逐句對過主片 119 句旁白及 `say`、26 張原生數字卡、90 個插畫鏡頭提示詞、片尾三句、標題／縮圖／說明／來源欄，以及兩支 Shorts 的 16 句旁白、16 個畫面標題及底鏡引用。`script.md`、`line-source-matrix.md`、`shorts-script.md` 和 `shorts-source-matrix.md` 的文字與當前 JSON 對齊。主張的數值、日期、分母及歸因保留了 v4 已由原件核對的邊界：三至四月**合計**取消量；全年 net nights/experiences 與 Q4 gross nights 不混用；房東支援 25% 的分母及 US$250m 承諾上限與 US$205.1m 列帳付款分開；年底 5.6m／6.6m 是含住宿與體驗的項目總量；2021 單季盈利與全年虧損分開；2022 首個全年盈利不歸功於某項單獨措施。Short 2 的 22% 已在旁白明讀 2021 年第四季。

## 阻擋項

1. 主片 `x140607`／`x14-b06-s07` 說「**另一位旅客則把目的地換到國境之外**」，但要給生圖模型的提示詞是「**an anonymous analyst compares that ribbon with an earlier, shorter quarter ribbon**」。這會生成長住色帶比較，而非旅客跨境換目的地；下一句 `x140608` 才問跨境份額。請將鏡頭改成匿名旅客把路線跨過無字邊界的單一動作，或將旁白改成真正與長住比較相符的銜接，不能用直式字卡蓋過不相干的底圖。
2. Short 1 第 6 拍 `x14-b02-s11` 的底鏡提示詞是記帳者把**訂單代幣分進數個碗**，但旁白／畫面標題是全年約 US$868.5m **非現金權證重估**。影片重構規格仍指示保留兩個碗與資料夾，會把權證會計項目畫成訂單分配。請改用損益簿與獨立權證重估欄的匿名抽象圖（文字及 US$ 數字由後製層加入），或選用與該會計含義相符的現有插畫，並同步更新 9:16 拍表。

上述是**圖文意義錯配**，不是 SEC 數字本身錯誤。修正並重新編譯後需新雜湊、新來源／畫面收據；本收據不得沿用為新版 PASS。此輪尚未生成圖片、TTS、音樂或成片，故也不構成視覺、發音、時長或上架驗收。
