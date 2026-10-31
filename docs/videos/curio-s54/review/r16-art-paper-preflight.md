# S54 R16｜三景插圖書面預檢

2026-10-20 23:35 UTC。**以下是未採入分鏡的候選方案；付費試畫、圖片評審及原圖驗收均未執行。** 已有的 [R16 史料與書面畫面覆核](r16-source-independent.md)、[敘事合併](r16-merge-policy/summary.md)及 [148／148 句機器音檢](r16-audio-gate/summary.md)只適用原版；網站大綱、劇本、音訊卡仍待站主決定。本頁沒有修改凍結創作、旁白、`look` 或媒體，亦非站主的付費或分鏡核准。

## 固定版與場景界線

R16 五檔 SHA-256：`brief.md` `e45d0256fba6f068d0bbfc7614edf0444ed88156d850b64aa59f03644f680a0f`；`research.md` `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae`；`claims.md` `0477d725ca08d22589a7287b521d3738db75f2aa5033a5c9e414de8634a4ff1f`；`video.json` `1f030f6c5f58a9d09919f9fb0b6f716e64f14b468c8735ce29987ece2ad6dc02`；`script.md` `538c59b6e861b789a1bbd6ddd4609ee1a47edaac5ea6e98d41bee9ae677e162d`。`visualHash(video.json)` 是 **`ba9a43292268b35b`**；全片 146 景，其中 **138 個 `shot`**、7 張工具字卡、1 個片尾。候選只針對 `s54002`、`s54093`、`s54121`，均屬既有 `shot`；`look: {"preset":"cute-mystery"}` 保持原值。

| 鏡頭與風險 | 尚未寫入 `video.json` 的 MiniMax `image-01` 完整候選 prompt | 原生圖的必要判準與來源界線 |
| --- | --- | --- |
| `s54002`：1 月費率先上路，空盤若被畫成已有郵票，會倒置年表。 | `Medium close shot at a January 1840 post office counter, one adult sender points to an empty shallow wooden tray beside a sealed plain letter and a small coin, soft window light` | 要能讀出**空盤、素面信與硬幣**，不出現已貼票或可讀郵票圖樣。空盤及手勢只是概念插圖，不聲稱驗過 1 月 10 日某一窗口的實物。[H 13061–13083、13139–13147、13205–13211](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083)與 [L 4136–4146](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4136-L4146)分開 1 月 10 日費率與 5 月 6 日郵票；R16 [差分覆核](r16-source-independent.md)已核這一句。 |
| `s54093`：預付郵資容易被畫成「每封都貼票」，而日記只記付費比例。 | `Medium close shot in a January 1840 post office, one adult postal clerk drops a small coin into a cash tray beside a sealed letter with a plain blank front, gentle window light` | 要看出**現金收款與未貼票的普通信**；不畫貼票，也不以單封信表示 112,000 封的所在地或全國統計。[H 13208–13250](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13208-L13250)是希爾日記轉錄：一夜寄件中約 13,000–14,000 封未預付，其餘預付不等於貼票；[P08 研究界線](../research.md)及[既有書面覆核](r15-source-independent.md)亦如此判。 |
| `s54121`：希爾事後說指示信漏掉 *not*，原信未核；模型若畫可讀原件會虛構史證。 | `Medium shot inside a London receiving house in May 1840, one adult postal clerk closes an unmarked supply folder beside an empty wooden stamp tray, soft window light` | **只是一名職員、閉合素面資料夾與空盤**的後果示意；不能出現可讀指示信、放大的 *not*、仿原件或已分發到收件所的郵票。[H 13353–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13353-L13389)只支持希爾的事後說法及收件所未領到票；[P10 研究界線](../research.md)及[獨立書面覆核](r15-source-independent.md)都標明原信未驗。資料夾、職員與空盤不是該信或具體收件所的復原。 |

三句只寫景別、年代地點、單人動作、物件及柔和光線；畫風由既有 `look` 加上，不在 prompt 重寫。若正式生成，九題機器 judge 與**原生 1280×720 圖**都要看，記每張 prompt、JPG SHA、九題與 KEEP／REJECT 理由；只退會誤導的年代、付款媒介、可讀「原信」或明顯漂離系列畫風，不以無害卡通細節要求史物精確復原。這是紙上邊界自檢，還需未撰詞者對**採入後的新版**做獨立來源與書面畫面差分。

## 試畫門檻、停工與總價

1. 站台三張審核卡有決定且能綁定精確 R16 音訊後，先重查最新五檔 SHA、網站卡、`media-status`、私有 ledger、圖片快取與 `keyframes --takes 3 --dry-run`。如採用上列候選，只更動三景 `data.prompt`、重跑 lint 和獨立書面差分；新 `visualHash` 需重核分鏡綁定，原版書面判定及任何舊分鏡決定不能自動轉用。網站站主未核的關卡不以本地判讀代替。
2. 試畫**每景先限 1 take + 1 judge**，按表中三個主物件逐張看原圖；**三景 3／3 原生圖 KEEP** 才能放行其餘 135 張與配樂。任何一張 REJECT，立刻停新景、放量與配樂；全 pilot **合計最多一次**窄幅改詞、獨立來源／書面覆核及該失敗景的 1 take + 1 judge。重試仍 REJECT，或另一景也 REJECT，便 STOP 此方案；不得買第三張湊通過，也不以字卡替掉核心畫面規避正文至少 70% 插圖與連續最多 3 張卡的規則。全數 KEEP 後仍逐張驗收餘下圖片。
3. `media-status` 於 **2026-10-20 23:35 UTC** 回報本集 ledger **US$0、0 圖、0 judge、0 music、0 reservation**；當時站台月額度已變為圖片 **18,756／30,000**、judge **20,059／30,000（餘 9,941）**、配樂 **62／100（餘 38）**。這已不同於先前跨集盤點的 judge 20,000／20,000、music 60／60 快照；重啟時只以即時回條為準，額度增加也不解除網站卡及試畫 STOP。

當次 `keyframes --takes 3 --dry-run` 報 **138 張、三次約 US$5.59**；`music --dry-run` 報 600 秒約 **US$0.08**。現價每 take MiniMax 圖 **US$0.0035** 加 judge **US$0.0100**。三張首輪 **US$0.0405**；全 pilot 僅一次重試時最多 **US$0.0540**，均含在整集上限內。保守把 138 張全算三次，加配樂為 `138 × 3 × (0.0035 + 0.0100) + 0.08 = US$5.669`，故**整集累計硬上限提案 US$5.67**，包含目前 $0 已支出及所有試畫、重試、judge、配樂。若採入後景數、單價、ledger 或乾跑上限變大，先以較高數重算並落地整集一次性上限，再開付費工作。本頁不核准支出或稱影片已完成。
