# C04 Bubble Wrap｜站主本機試片核准收據

- 日期：2026-10-22（Asia/Taipei）。
- 決定：站主明確核准 **C04 目前這一版腳本與逐鏡方向**，並核准製作**一支本機試片**；這是在先前只採用 Treatment 方向之後的新核准，不沿用 C03 的授權。
- 範圍：94 句旁白、最多 84 張 MiniMax `image-01` 插圖（**每鏡累計最多三次**）、一首無人聲配樂，連同音訊查核、卡片、本機合成與 QA；**整支 US$25 為硬停線**。本次不授權上傳、發布、合併 PR 或部署。
- 企劃與腳本依序見草稿 PR [#1668](https://github.com/x812033727/travel_scanner/pull/1668)、[#1670](https://github.com/x812033727/travel_scanner/pull/1670)。腳本 PR 仍為草稿且標 `no-auto-merge`；核准製作不代表站主已驗收旁白、逐張圖片、試片或正式頻道動畫。

## 核准綁定的定稿

| 檔案 | SHA-256 |
| --- | --- |
| [`../story-everyday-bubble-wrap-c04/draft-lines.tsv`](../story-everyday-bubble-wrap-c04/draft-lines.tsv) | `39198B822F0F32F2162884DE6ED1030B4BCA0FF380BD09E0525893CB92915DB0` |
| [`../story-everyday-bubble-wrap-c04/visual-plan.tsv`](../story-everyday-bubble-wrap-c04/visual-plan.tsv) | `1FD21BC3F71A9D72489FADA9F42014300674632B7C060F00E4969E89597314E3` |
| [`../story-everyday-bubble-wrap-c04/video.json`](../story-everyday-bubble-wrap-c04/video.json) | `1BB9FD7355E6BFA5FCFA8D9A4BCFB0F89F2A5F01451131BDC3754B12243B330B` |

獨立逐句來源覆核 94／94 句 PASS、兩位盲讀 PASS、靜態視覺預檢 PASS 均綁定以上雜湊。可見媒體報價在腳本樹的 [`production-quote.md`](../story-everyday-bubble-wrap-c04/production-quote.md)：84 張最多三次的圖像與評審約 US$3.40，另暫估一首配樂 US$0.08；TTS、轉錄等供應商美元費用未拆帳，不能當作零。平台顯示的每支 US$200 技術上限不取代此 **US$25 站主停線**。

## 先後與停線條件

1. 付費前讀回三份 SHA、STOP、已有素材與台帳、目前可用供應商和 94 句乾跑。若來源或核准版本漂移，先停。
2. **先做 TTS，後買圖**。量第 02–06 章**實際純旁白**；若少於 480 秒，停線補強有一手來源的因果故事，重做事實／盲讀與相應站主腳本關卡，不用文字估時代替。
3. 只在時長與音訊關卡合格後跑插圖；任一鏡三次仍不合格，保留已付費素材並停下處理，不重置嘗試次數。配樂只買一首，讀取交付音檔的實際可解碼長度；短音檔不可因快取命中而被算成完整，也不可不查帳就重買。
4. 每個付費階段前後讀本片台帳，計入保留中／未知結果，超出整支 US$25 或無法證明下一步在上限內就停。僅製作本機試片；正式片頭片尾、音訊審聽、圖像驗收、成片 QA 與任何 Studio 元素都要留下各自證據。

此收據記錄站主在對話中的授權範圍，並非自行在後台建立的假 `approve` 或上傳許可。任何已核准三份檔案內容變更都需重新檢查授權和相應審核關卡。
