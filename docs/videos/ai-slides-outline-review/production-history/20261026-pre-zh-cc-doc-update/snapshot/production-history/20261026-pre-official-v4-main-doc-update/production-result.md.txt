# 第四片製作進度快照

截至 2026-10-26T01:30:26.879Z，繁中 **1080p 本體候選已完成並附上後台下載證據**，遠端 final 仍為 pending。這份本體的當前旁白 118/118 接受、0 flags／unchecked，核心 QA 11/11 通過。官方頻道動畫片頭尾仍缺；八外語已完成本地 metadata、CC 草稿及縮圖，**實際外語音訊仍為 0/8 ready，overall_complete=false**。

| 項目 | 實際狀態與證據 |
|---|---|
| 凍結版本 | source `296fa0c93be25c7074ec50259db650f5663aca2324a5e0a16da2118406757c2f`；claims `2c56550a6ffde77c8ee781f909554a8c94c9f7d787f877fc34b4c385160778f7`；speech `a8055d3edb90bcda`；lexicon `378f875ef4daf76e4aadee22bae0aa3c523dd39528ca48f69f139c2a70843b0c`。本次只更新文件與安全收據。 |
| 當前音訊 | 正常複檢真正 exit0，118 checked／118 accepted／0 flags／0 unchecked；84 exact、15同音／語助、6 Jev、13第二轉寫。嚴格全目標核驗 ready=true／problems=[]，見[當前音檢收據](narration-listener-reword1-verification.json)。 |
| 實際正文時間 | 18106 frames／30＝603.533333 秒；outro 前591.366667秒；扣冷開與outro的正文566.133333秒。不是用片頭尾或慢播補足八分鐘。 |
| 實際 MP4 | 1920×1080、30fps、18106 video frames，視訊603.533333秒；AAC／容器603.605秒。52,296,204 bytes，SHA `3cdbde2a415d1c41a0e47c25e3914a687d9bef524763a750ea66a4b11f43fcea`。見[本體實測](body-candidate-verification.json)。 |
| 核心 QA | [原始 QA](body-core-qa.json) 11/11、ok=true，綁同一 MP4 SHA；仍保留27筆字幕閱讀速度提醒。這是無官方 bookends 的本體核心 QA，不能替代完整正式製作驗收。 |
| 後台下載 | 2026-10-26T01:05:11.570Z 完成13/13 parts上傳，server assembly驗SHA／大小；經正常驗證身分的metadata GET確認角色 `evidence_zh_tw_1080p_mp4`、同SHA及52,296,204 bytes。沒有把metadata回讀說成遠端binary重新下載／雜湊。見[真實附件收據](main-download-attachment.json)。 |
| 遠端狀態 | final review `532d5837-0036-4695-9535-97d0c6a6044b` 仍 pending；script／audio正常送審與本機委派採用分開，沒有遠端核准或站主UI點擊宣稱。本輪已用正常唯讀GET重新核對；沒有POST。 |
| 後台實際附件範圍 | [安全回讀](backend-current-final-safe-readback.json)列出的roles只有 `preview`、`contact_sheet`、`thumbnail`、`evidence_zh_tw_1080p_mp4`；9語title／description與當前本地native compose逐字相符。CC附件0/9、外語縮圖附件0/8，二者只本地生成，不能稱已送達。 |
| 當前lint | 0 errors／6 warnings：25秒冷開、2025必要重現，以及EN／ES／PT／ID標題手機列表寬度。原生估時／provider字元輸出不是實測時長或計費。 |
| 八語文字 | en／ja／ko／es／pt／id／vi／th 各118句、6章及title／description／tags／縮圖三欄完成，三組不同作者獨審後套用必要修正；可選字數精簡未整批採用。見[文字與 CC 初始快照](localization-initial-reviewed-snapshot.json)。 |
| 九套 CC | zh-TW 加八外語的SRT／VTT已建立。八外語仍依繁中主旁白時間軸，屬待實際配音後重排的草稿；不是八條配音已音檢通過。27筆CPS提醒原樣保留於QA與快照。 |
| 八語縮圖 | 原生已draw八張；root實看all8 contact。KO原「그다음 제작」斷詞後，正常merge／draw成「다음 제작」，root已實看修正。本文件作者只核對當前SHA與套用差異，沒有冒稱重新看過八張。見[KO獨審](thumbnail-ko-wrap-independent-review.json)及[套用核對](thumbnail-ko-wrap-application.json)。 |
| 外語音訊 | 0/8 accepted／ready、0/8已驗證音訊交付，尚未送language batch。後續由唯一producer先做EN synth／fit／meter；ASR仍hold，進行中或fit不算ready。 |
| 品牌與敘事 | 官方頻道動畫bookends仍missing。R2兩份raw及citation修復native各12/13、passed=false、no_recap；保留完整提示與必要算義的教學取捨，沒有重算成13/13。 |

原[verify-1](verify-1.md) REVISE、[verify-2](verify-2.md) R1 PASS、[verify-3](verify-3.md) 欄位回歸REVISE、[verify-4](verify-4.md) 修補PASS、[verify-5](verify-5.md) 當前三句PASS均保留原bytes與各自範圍。舊speech0f1的7→5→3旗、三句修詞／67 chars新TTS及114張原生render歷史不改寫；當前a805音檢通過由後續真實收據證明。

## 仍待完成

- 合法官方頻道動畫片頭尾與bookend guard、真正正式定版；靜態outro或null-branding核心QA不能替代。
- 八語逐語實際fit／meter／正常音檢與全目標核驗；按各語接受音訊的時間軸重建CC，再驗可下載角色／SHA／大小及真正language batch。
- 以另行授權的checked-only附件流程交付並核對9套CC與8張外語縮圖；目前final files沒有這些角色，metadata payload不代表字幕或縮圖檔已上傳。
- 遠端最終核准與整體交付狀態；目前僅本體候選可供審閱，overall及all_eight_ready均false。沒有YouTube公開、合併或部署。

本次更新前的狀態文件已[逐bytes封存](production-history/20261026-pre-body-delivery-doc-update/archive-manifest.json)，舊「assembly running／尚待音檢」只是當時快照，不能覆蓋上述新結果。詳[機器進度](production-progress.json)、[採用與界線](production-decision.md)及[收據索引](production-receipt-index.json)。
