# B18 最終企劃 row 來源審稿方法

**範圍：** `B18.json` SHA-256 `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681`，canonical story SHA-256 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`；候選 manifest `8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754`。審稿者 `/root/b18_successor_independent_review`，2026-10-17。新 [`review-candidate.json`](review-candidate.json) 只對這份 row 的內容 hash 有效，沒有複製舊 `episodes/reviews/B18.json`。

## 已實際開啟的六個來源與十筆必查事實

| row fact | 核對結果 |
| --- | --- |
| 0、1、2 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)及[機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)支持 1958 年 4 月布施首店與啤酒工廠靈感；[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)支持首店約 20 坪、吧台、四貫 50 日圓。較早立食四貫 20 日圓及忙碌人手是另一階段，不當首店售價。啤酒工廠不指名公司。 |
| 3 | J-Net21〈町工場の経営者が協力〉直述轉角**輸送帶**壅塞、盤子掉落、約十年、扇形板片與 1957 年試作；撲克牌版本屬該文，發明協會記名片版本。現 row 以「據 J-Net21」統攝工程敘述，兩種靈感各署來源、不合成一個現場，`attributed:true` 有意義。前次六處口播無歸屬 P2 與三景重複來源名 P2 分別由[六句審查](../B18-attributed-narration-candidate-20261017/INDEPENDENT-ATTRIBUTION-REVIEW.md)及[最終兩句審查](INDEPENDENT-FLOW-REVIEW.md)處理；這些審查本身不代替本次 row review。 |
| 4 | [日本法院判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)理由 PDF P8 L466–474 指向第 579776 號登記；P10 L574–578 認定**該特定權利**於昭和 47 年（1972）期滿、其後已有與原告無關的多家公司經營。row 未延伸為所有權利或單一入場原因。PDF 是此 fact 唯一來源，正式工人讀取器無法轉成正文，故 `reviewer_only:[4]`。J-Net21／發明協會的 1978 年歷史版本僅保留於 caveat，不口播。 |
| 5、6 | J-Net21 支持對相似店警告及後來有加盟店獨立的報導脈絡；發明協會支持萬博受表彰、全國知名度與約 240 家版本。row 已標明歸屬及不得外推，不把這些當法院認定。 |
| 7 | 機械學會第 112 號分別列 1985 年製、2021 年仍於堺東店使用的輸送機，和元祿產業另存的早期魚鱗板；不是 1958 年首店同一機器。 |
| 8、9 | [石野集團年表](https://www.ishino-group.com/history/)直接記 1980 年大型店旁通裝置、1986 年ㄇ字型輸送帶店；發明協會沿革記其他新業者在後場製作並以直線帶送至客區。row 不主張同一店改裝或兩個設備事件互為因果。[石野集團介紹](https://www.ishino-group.com/group/)的 1974 年給茶整合口徑已直接讀到，與年表 1971 年已販售口徑不同，只留 caveat。 |

審查是對最終企劃 row 的來源確認；六個來源都已開啟，且其分歧、數字適用階段與 PDF 限制已在 row 中留界線。`review-candidate.json` 用新 reviewer、日期、新 canonical SHA、`sources_opened:6`、`changes:[]` 與 `reviewer_only:[4]`；`verdict:pass` 只代表這份 row 的來源審查，並非影片已完成。

**採用前界線：** 仍須把最終 row、系列投影及這份候選收據依既有流程一起審慎採用，讀回 final hash；65 筆 `UNCHECKED` 待正式 worker verifier 逐章查核。最終完整逐字稿、listener、敘事、TTS／`check-audio`、畫面、可關閉繁中 CC 和成片都另有關卡。本次沒有採用 active 檔、主機操作、付費製作或上傳。
