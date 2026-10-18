# A01 r20 離線故事盲讀收據（2026-10-19）

## 範圍與結論

先完整閱讀 `candidate/script.md` 的口播故事，記下鉤子、章節推進、問題回收、重複與片尾感受；之後才比較 r19，並抽核 r20 的 `candidate/video.json`、`candidate/claims.md`、`source-alignment.json`、`validation.json` 與相關第一手受訪、專利和當事機構資料。這是**離線編輯意見**，不是逐條主張審查、配音盲聽、成片審核或正式 `story/reviews/script-review.json`。

**故事盲讀：P0 0、P1 0、P2 3（非阻斷）。** r20 的主問句「箱子有輪子，為何還要等」有明確回答：安妮塔先示範自製輪箱可行，但本集材料未見其量產上架的紀錄；Sadow 的樣品碰到購買習慣和通路阻力；Plath 面對安檢與機組使用的不便；1993 年的商品測試再驗證「買得到」仍要「裝得下、用得順」。這些事件串成有因果的故事，沒有把三人說成經證實的直接傳承。**整體仍 HOLD**：74 筆 `PENDING` 主張、實際 TTS／剪輯、完整視覺與正式主機銜接均未由本收據批准。

## 鉤子、轉場與回收

- `hook-01` 至 `hook-06` 先給沉箱／輪板、安妮塔旅後是否續用、百貨願不願上架、安檢困境四個具體問題。`origin-r12-03`／`origin-1939-case` 回收旅後續用，`engine-05` 至 `engine-10` 回收百貨問題，`turn-07` 至 `turn-07c` 回收安檢懸念，`now-1993-retail` 至 `now-1993-stow` 回收普及後的使用問題。
- 安妮塔→Sadow 用「三十多年後」接續；Sadow 拖帶箱的搖擺→Plath 的另一種難題，有明確對象與界線；Plath 車庫→機組員→一般旅客→零售測試，時間和因果可跟上。片尾回到「肯拉、店肯賣、用起來順手」，再把證據界線說清楚，台灣華語口播語感自然。
- r20 的 `hook-04` 改「後來」，不再替 Sadow 拜訪採購填精確年份；`origin-r12-01`／`origin-01b` 改「第二趟長途旅行」，不把 1921 年首旅誤講成完整環球；`now-outro` 改「我們查到的資料還不能證明」，沒有斷言三人完全無設計關聯。[Sadow 受訪](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)、[Winnetka 家族史](https://www.winnetkahistory.org/who-were-the-burnhams/)和[輪箱館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)、[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)支持這樣的限縮。公司史稱 Plath「改良」Sadow 設計，但沒有交代他是否親見 Sadow 原型；館藏文章也沒有記載安妮塔直接影響後兩人。
- `turn-06` 的「得解開繩子，再把箱子卸下來」是當時所需步驟，語法上未宣稱那名旅客已經成功卸下；`t46` 及圖像提示詞均應維持「嘗試中」的界線。[2012 年 USA TODAY／ABC 受訪報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)只說旅客當時正費力想把箱子從推車解下。正式逐條審查仍須重核這一點。

## P2 編輯建議（不阻斷）

1. `origin-r12-01`、`origin-01b`（第 7、9 鏡，稿第 44、54 行）：兩鏡間只隔一鏡，兩次說「第二趟長途旅行」略重；錄音前可在不改史實前提下做一次順口試讀。它們分別交代動機與出發，現稿仍可理解。
2. `engine-porter`（第 26 鏡，稿第 128 行）：第一次出現的 Shiller 未給身分，觀眾可能要花一拍判斷說話者。若畫面能給簡短出處識別，會更順；切勿把他的轉述升格為 Sadow 的錄音逐字證詞。
3. `turn-09`（第 49 鏡，稿第 224 行）：安檢員「好」剛收回鉤子，隨即插入 1987／1988 的資料差異，情緒略停頓。可在剪輯或配音停頓處理；保留兩種年份的來源歸屬，不合併成單一年份。

## 片長與證據綁定

`validation.json` 給 1,853 口播單位；以每分鐘 300／275／250 單位估算，約 440.0／474.9／515.2 秒。前兩種紙上速度落在 7–8 分鐘，較慢速度超過 8 分半。這不是實際 TTS 或成片片長；片頭片尾、停頓和剪輯仍需實測。

本收據只對下列已讀位元組有效（SHA-256）：

| 檔案 | SHA-256 |
| --- | --- |
| `manifest.json` | `78826BCFC6356335855756FC7F81A7C846087DF340C4A7753C270C186D1077EB` |
| `candidate/script.md` | `173B921FBCB14DA1DBDD6D1B89E63D00F7B21BD60A7388A4012B765FEB923386` |
| `candidate/video.json` | `3045312831B7DC08E2C2AF1F284F7B56F05F58E92C9D78A3C3DB1A5B4B8059F8` |
| `candidate/claims.md` | `F4D91A46C6B7D8A1005053D506A09BC15B8AF592DF26BF8404F84CDAE2FA8388` |
| `source-alignment.json` | `127FBFBE5C0A87739CC7132124F7BE09D4142C1140EB9DE520FD63B25FEC788D` |
| `validation.json` | `FE378AC5FDF856E91E954CA598B3EE5589BB101507802F7634FFC18C38794C80` |

不繼承 r19 的審稿結果；未做 74 條主張的正式逐條批准、1939 年報紙逐頁視讀、正式機六章與來源合併驗證、實際 TTS、圖片驗收、付費素材或成片播放。上述任何綁定檔案變更，須重新盲讀或明列差異。
