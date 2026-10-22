# S53 R41｜`s53031` 原 R40 提示詞付費前獨立預檢：HOLD

2026-10-22 UTC。**HOLD：不可用下列未修訂的 R40 `s53031` 提示詞直接購買第一張原生圖與 judge。**這是只讀史料及書面畫面預檢；判定對象是 [R41 可逆差分](r41-s53031-mature-carpenter-delay-structured-diff.json)的兩個 **`before`** 值，而非其 `after` 候選。未檢查或核准 R41 新稿，未生成圖像、購買媒體、修改圖單／帳本，沒有 Git 暫存、提交或 PR 操作。

## 凍結的判定對象

| 對象 | SHA-256／內容 |
| --- | --- |
| R40 `video.json` | `65bec2d34c7d8443b9e45112e1193c6645feee86e676c0552d78b79f2335c312` |
| R40 `claims.md` | `68c2ab442dd0b20daef0b39977360f6b03a0974132bfd5967d90a2a07db53a0c` |
| 未改口播 `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 固定 1913 年 *San Francisco Relief Survey* `/tmp/s53-sf-relief/56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| R41 差分檔；本回只讀 `before_sha256` 和 `before` | `f10442b1adad2e34bdea1f8581ca9cf8baa484711682b8d4a6bfaf0757444c75` |

`before` 的完整場景為 `id=s53031`、`template=shot`、口播「大批小屋，得再過兩三個月才備妥。」、`camera=pan right`、`visual=still`，其提示詞原字為：

> Medium shot at a refuge after the 1906 fire, an anonymous adult waits outside an unfinished row of cottages, soft overcast light

`before` 的 `claims.md` 整行原字為：

> | s53031 | 大批小屋，得再過兩三個月才備妥。 | [D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870) | 建屋宣布、9 月施工及分散營地 |

## 史料與書面畫面判定

固定調查 [D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865)記小屋為取代帳棚而建，1906 年 9 月 10 日開工，9 月 16 日漢密爾頓廣場有 20 棟完工，且至少經過兩三個月，才有相當數量的房屋備妥供難民使用。既定口播的「大批」與「得再過兩三個月才」可對應原文 *any considerable number* 和 *at least two or three months*；它不說 9 月 16 日沒有完工屋，也不指定任何住戶的入住日。這份 1913 年後出調查沒有辨認提示詞中的等待者、整排未完工屋或特定營地。

提示詞的 `after the 1906 fire` 可落在 9 月 10 日開工以前，也沒有把緊接前一景 9 月 16 日 20 棟完工的時間順序交代給生成模型。`anonymous adult` 缺乏能看出的成年特徵；`refuge` 與 `unfinished row of cottages` 未限定公共廣場帳棚、低矮救濟小屋和裸地，可能把等待中的小屋畫成郊區完工大宅，或令觀眾以為當時所有小屋仍未完工。這些是付費前可明確收窄的核心時間、主體與場地訊息，不是要求逐項復原沒有史料的小屋施工細節。原 `claims.md` 末欄僅寫「建屋宣布、9 月施工及分散營地」，沒有解釋本句的備妥延遲，也沒有界定人物、排屋與入住時間只是原創概念示意。

[R5 獨立來源與書面畫面審](r5-source-independent.md)曾對當時整版給 PASS，但其 `video.json`／`claims.md` 雜湊是 `2d9e0036…`／`6a0a1f31…`，不是這次凍結的 R40 版；該紙審也早於 `s53030` 的原生圖證據。[R39 相鄰景退件](r39-s53030-first-native-independent-visual.md)記錄類似籠統提示詞畫出偏童貌人物、完整大型住宅與道路標誌，沒有帳棚或建屋動作，雖然機器 judge 為 9.29 PASS。[R40 窄修後相鄰景入選](r40-s53030-second-native-keep.md)顯示明寫成年外貌、帳棚與低矮未完工屋架後，原圖才傳達等待／施工脈絡。此證據不證明 `s53031` 必會畫錯，但已足以要求在付費前修正同類的可預見歧義。

## 解 HOLD 的最小範圍

只需收窄 `s53031` 的 `data.prompt` 和同一行 `claims.md` 畫面註記；保留既定口播、D 引文、運鏡及其他場景。提示詞應清楚放在 **9 月 16 日以後的 1906 年秋季**，給唯一主要成年人物可見的灰髮／面紋與當時衣著，讓此人對一座低矮、仍在搭建的救濟小屋做一件簡單動作，背景用帳棚／裸地說明公共營地，避免大型完工住宅、鋪面道路、現代路牌與可讀原件。不要讓一排未完工屋或畫面文字暗示 20 棟並未完工、所有小屋同時未完工，或某戶在特定日期入住。註記應分開說明「9 月 16 日有 20 棟完工」與「相當數量仍待至少兩三個月才備妥」，並標明人物、工位、屋架及時間點是匿名原創概念，不是 1913 年調查核實的個案或入住紀錄。

新稿須另按固定 D、精確差分及系列規則做獨立書面覆核；書面 PASS 只能放行**一張**受 STOP、額度和帳本保護的原生圖加一次 judge。原尺寸仍須人工核看成年人、低矮在建救濟屋、帳棚／場地、無誤導性入住日期和 2D 畫風，機器 PASS 不能覆蓋實質年代或場景矛盾。本回 HOLD 不判定任何尚未驗收的圖。
