# B18 法院 PDF 分源與爭議年份降級候選

**狀態：隔離、離線、結構檢查通過；新雜湊的獨立 PDF 審稿與正式工人查核仍待完成。**

父版本為 [B18 名稱修正候選](../B18-worker-input-name-trim-candidate-20261017/README.md)，其 `sha256.json` SHA-256 是 `da3820bd403c4a9fb33d2b904cbf3f2b112579a060ee9ab6709c3ab07d7137c3`。本目錄沒有改動 `episodes/B18.json`、`episodes/reviews/B18.json`、`stories.json`，也沒有寫主機或呼叫付費供應商。

## 為何要拆

舊 `must_verify[4]` 將[法院判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)對第 579776 號實用新案的 1962 年登錄、1972 年期滿，與[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的 1978 年版本放在同一筆。舊 `must_verify[5]` 又將法院認定的後續其他經營者，與 J-Net21 的律師警告及加盟店獨立放在同一筆。正式來源讀取器對法院 PDF 只得到 `application/pdf`，不能把它的 `supports` 摘要當作新讀到的判決正文；混合來源使 `reviewer_only=[]` 的格式檢查雖通過，法院專屬結論卻沒有真正可讀的來源。

正式格式最多十筆 `must_verify`，因此維持十筆：

| 索引 | 現在查核的內容 | 僅引用來源 | 逐景連結 |
| --- | --- | --- | --- |
| 4 | 法院對特定權利的 1962 年登錄、1972 年期滿，以及期滿後其他無關企業經營的認定 | `sources[3]` 法院 PDF | `h7/e6/e7/t7/t8`；`e6` 另有可讀的直接 `sources[2]` 支持 1962 年登錄 |
| 5 | J-Net21 報導的律師警告與部分加盟店獨立；明確標記 `attributed` | `sources[0]` 可讀網頁 | `e8/t9`；爭議的 1978 年版本僅保留在來源摘要與 caveat，不進口播 |

`e8` 律師警告、`t9` 加盟店獨立保留直接 `sources[0]` 並續指 `fact: 5`；`t8` 法院認定的其他經營者改為 `fact: 4`。獨立讀判決時另發現原 `turn-s079` 口播的「在元祿之外」超出判決較窄的「與原告無關」，故**只把這一行**改成「判決也說，後來已有許多與提告的元祿壽司公司無關的業者，經營輸送帶壽司店。」；`t8` 場景主張文字與企劃 `turn.point` 同步收窄。法院 `sources[3].supports` 移除未經 P5 被告答辯證明的另一第 851953 號權利「期滿日」表述。`turn-s077` 畫面年份由 1970 年代初改為 1962 年的登錄情境；`turn-s079` 拿掉「1970 年代新開幕」暗示，改成 1972 年後未指定的時間與沒有開幕標示的店面。65 筆逐景主張均保留、直接來源與 `UNCHECKED` 判定都沒改。六章維持 85 景、88 句；其他 87 句、其餘畫面提示、角色和故事順序未改。`claim-coverage.json` 同步列出每筆映射，`delta.json` 列出精確變更。

法院判決**理由**第 8 頁 466–474 行載明第 579776 號登錄，第 10 頁 574–578 行載明昭和四七年（1972）因存續期間屆滿而消滅，後來其他企業也營運相關店。發明協會網頁第 34、43 行分別寫 1962 登錄及其 1978 年說法；J-Net21 報導本身以「特許」稱呼 1962 年權利並寫 1978 年失效。這些是不同來源的主張；本候選未確定完整權利鏈，沒有把所有店的出現歸因於某一次到期。企劃 caveat 明寫「本片不口播1978年」，只在來源摘要與 caveat 記錄互相牴觸的版本，避免正式 writer 將該爭議日期加回旁白。

## 驗證與下一關

執行 `node build.mjs --check`、`node manifest.mjs --check`。建置器驗父版 15 檔雜湊、限制只有兩筆 row 事實、一個企劃章摘要、一個 PDF `supports`、一條不口播 1978 年的 caveat、一個逐景 fact 指標、一句口播、一筆主張文字與兩個畫面提示變動，核對其餘 87 句與 64 筆主張原文及全部直接來源、`UNCHECKED` 判定，並跑正式 `storyProblems`。以已知法院 PDF 不可供工人讀取的**模擬**讀源結果驗證：未列 `reviewer_only` 時此 row 會被 `fetchProblems` 阻擋，獨立審稿人核准後若只列 `[4]` 則機械檢查可通過。模擬不是新的正式讀源收據。

新 `B18.json` SHA-256 `9a8ceabd48c6970cd654c077ab33499d070fbbcf5eca4e078e5777a12f99dc9b`，canonical story SHA-256 `7a598d16c9efcd9014f3554531dfe5569408cb1542cbeb1f90fdfbff4b0975e5`。舊的審稿收據綁舊雜湊，不能沿用。請由獨立審稿人依 [review-request.md](review-request.md) 重新打開 PDF 與兩頁報導，核准新 row 後才在**新收據**標記法院專屬事實 `reviewer_only: [4]`。編譯、匯入與正式逐章／逐景查核在那之前皆 HOLD；目前沒有配音、插圖、CC 或成片。
