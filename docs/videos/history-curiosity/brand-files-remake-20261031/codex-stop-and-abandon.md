# 品牌故事改 W 軸：要站主決定的放棄清單與 Codex 停工說明（2026-10-31）

站主 2026-10-31 決定重做的品牌故事都改歸奇聞檔案局 W 軸。同一題已有舊的 `story-*-remake-20261025`，不先處理就會做兩次。
這份只列事實與建議。**放棄影片、停 Codex、關 PR 都由站主決定**，撰稿的 session 一件都沒做。站主答覆前，W04 之後的題目不開工。

## Codex 批次現在有沒有在跑

- 分支 `codex/brand-remakes-20261025` 最後一個 commit 是 2026-10-26 10:00 UTC（`fbbc4a39e`），之後五天沒有推送。
- [draft PR #1849](https://github.com/x812033727/travel_scanner/pull/1849) 還開著，2026-10-26 10:00 UTC 後沒有更新，0 則留言。票 `2026-10-25-brand-stories-new-rules-remakes` 只在該分支上，狀態是 `blocked`。
- 2026-10-26 之後實際做片的是 Claude session（0140、0141 帳戶與 UCC、CamelBak 兩支成片），帳戶那兩張票已結案；本機目前跑著的 session 沒有一個在做這批。
- 後台 15 支停在「大綱核准」，看不出有人在往下做。

**結論：看不到在跑的跡象，但雲端的 Codex 工作這裡看不到，不能保證它沒排著。要站主到 Codex 那邊看一眼。**

## 後台現況（2026-10-31 用影片工具權杖唯讀讀回）

`花費` 是後台 `media_usd`，只算插圖、配樂這類媒體，**不含旁白**（Moleskine 旁白已合成，這欄仍是 0）。

| 新代號 | 舊 slug | 後台階段 | 花費 |
| --- | --- | --- | ---: |
| W03 | `story-garmin-smartphone-pivot-worker-2026-remake-20261025` | 大綱核准 | 0 |
| W04 | `story-adapt-doraemon-after-fujiko-remake-20261025` | 大綱核准 | 0 |
| W05 | `story-adapt-seiko-quartz-astron-remake-20261025` | 大綱核准 | 0 |
| W06 | `story-dyson-japan-first-20261021-remake-20261025` | 大綱核准 | 0 |
| W07 | `story-everyday-bubble-wrap-c04-remake-20261025` | 大綱核准 | 0 |
| W08 | `story-everyday-camelbak-c14-remake-20261025` | **成片核准、未上傳** | 0.70 |
| W09 | `story-everyday-dr-martens-c07-remake-20261025` | 大綱核准 | 0 |
| W10 | `story-everyday-frixion-c15-remake-20261025` | 大綱核准 | 0 |
| W11 | `story-everyday-kikkoman-c08-remake-20261025` | 大綱核准 | 0 |
| W12 | `story-everyday-kincho-c05-remake-20261025` | 大綱核准 | 0 |
| W13 | `story-everyday-moleskine-c03-remake-20261025` | **旁白已合成，待核准** | 0 |
| W14 | `story-everyday-oxo-c10-remake-20261025` | 大綱核准 | 0 |
| W15 | `story-everyday-patagonia-c09-remake-20261025` | 大綱核准 | 0 |
| W16 | `story-everyday-play-doh-c06-remake-20261025` | 大綱核准 | 0 |
| W17 | `story-everyday-seven-bank-c19-remake-20261025` | 大綱核准 | 0 |
| W18 | `story-everyday-ucc-c11-remake-20261025` | **成片核准、未上傳** | 0.60 |
| W19 | `story-everyday-zippo-c20-remake-20261025` | 大綱核准 | 0 |
| W20 | `story-adapt-a4-paper-size`（[q5c-MXpsAuw](https://www.youtube.com/watch?v=q5c-MXpsAuw) 已上架） | 已完成 | 0 |
| W21 | `story-five-pringles-vat-case` | **成片核准、未上傳** | 0.40 |
| W22 | `story-five-lego-legoland` | **旁白已核准** | 0.29 |

上面這些的**舊版**（沒有 `-remake-` 的那一支，A4、品客、樂高除外）都已放棄，不用再處理。W01 杜比、W02 米其林的舊片已放棄且沒有 remake，也不用處理。

## 建議怎麼處理

| 組別 | 影片 | 建議 | 為什麼 |
| --- | --- | --- | --- |
| 還沒做的 remake | W03–W07、W09–W12、W14–W17、W19 的舊 slug（14 支） | **現在放棄** | 只有文字與大綱，沒有媒體花費；留著 Codex 或工人可能接著做 |
| 旁白做了一半 | W13 Moleskine | **現在放棄** | 旁白錢已花，新稿用不上；留著只會多花 |
| 樂高 | W22 舊 slug | **現在放棄** | 品牌故事走免關卡流程，工人開著就可能接著畫圖花錢 |
| 已有成片、未上傳 | W08 CamelBak、W18 UCC、W21 品客 | 暫留，新片核准再放棄 | 留著不花錢；放棄後成片就沒了退路。只是不要上傳 |
| 已上架 | W20 A4 | 不動，新片核准後站主決定改私人或刪除 | 計畫的原則：新片上架前舊片不動 |

## 預算帳戶（不用處理錢，但要知道）

- 0140 建了 UCC 一個、0141 建了 CamelBak、Moleskine、Bubble Wrap、Play-Doh、金鳥、龜甲萬六個，共 7 個，每個上限 US$25（`apps/api/migrations/versions/0140_c11_ucc_remake_budget.py`、`0141_story_remake_budgets.py`）。
- 帳戶是上限不是預付款，放棄不會退款也不用退款。依既有設計帳戶不刪，讀回才對得上（`apps/api/app/video_budget/PENDING_EVERYDAY.md`）。
- W 軸的 slug 是 `curio-`，**不走這些帳戶，也不借它們的額度**。W 軸的上限要站主另外核准。
- 那 7 個 slug 還留在 `ACTIVATED_STORY_SLUGS`，可以付費。放棄後建議開一張小票把它們移出，避免有人誤跑；不急，本次不動。
- 另外要注意：Seiko、哆啦A夢、Dyson、Garmin 四支的 slug 不是 `story-everyday-` 開頭，**不受那道預備製作擋板管**。所以它們更要靠放棄或停 Codex 才擋得住。

## 給 Codex 的停工說明（站主決定後可直接貼）

> 站主 2026-10-31 決定：`story-*-remake-20261025` 全部不再往下做，這些題目改由奇聞檔案局 W 軸（`curio-w*`）用新規則重寫。不燒字幕。
> 請停止分支 `codex/brand-remakes-20261025` 上票 `2026-10-25-brand-stories-new-rules-remakes` 的所有工作：不再送審、不再合成旁白、插圖或配樂，也不要動後台這些影片。
> 分支留著當資料來源，不要刪，也不要 force push；PR #1849 維持未合併。八語文字綁舊稿，不沿用。
> 回報目前有沒有排定的工作或未付款的請求，然後結束。

## 其他要站主知道的

- **輪子行李箱**：Codex 分支也寫了這題（R9，篇幅不足、還沒進後台），舊片已放棄。它**不在**這次的 22 支名單裡，所以先不動。
- **Codex 的成果不是白做**：分支上的來源清單可以當線索，W03 已唯讀參考。稿子、八語文字與審核紀錄綁舊內容，不沿用，也沒有改動那個分支。
- **PR #1849**：建議關閉不合併、分支保留。它有兩千多個檔案，且內容已被這次決定取代。
- 後台的 UCC、CamelBak 階段字樣是「on YouTube」，但沒有 YouTube 影片編號；依規則盤點（`old-rule-inventory-20261031.md`）它們是成片已核准、未上傳，表上照這個寫。
