# A01 r18 獨立限縮審查 — HOLD

- 審查日期：2026-10-19。
- 審查對象：`A01-editorial-candidate-20261019-r18/manifest.json`，SHA-256 `6228FA78CBB686E01E10A5B1053204A53B71F248FCDA93AE364C501CCE518B4C`。
- 結果：就 r17→r18 差異及 r17 三項 P2 的修正，P0 0、P1 0、P2 0。可作下一份離線候選；這不是整支影片或正式機劇本的核准。

## 已核對

- r18 只修改第 43 鏡 `r6t01`、第 56 鏡 `r3n03` 兩句及 `n56` 主張，並澄清來源數量的收據文字；未改台詞 ID、其他鏡、圖片提示詞、相機動作、章序或 setup/payoff ID。
- [Judi Dash 1993 年《洛杉磯時報》原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)記載 Travelpro 起初郵購、受測四家品牌，並說相關型號可在主要百貨**或**行李專門店選購。`r3n03` 和 `n56` 已同時採用「或」，且不聲稱每家百貨都同時有四家，也不推算銷量。
- [Jayne Clark 2012 年刊載的 Plath 回憶](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)只支持守衛回答 OK。`r6t01` 現問「會怎麼回答」，第 48 鏡仍回答「好」，不把它說成已證實放行。
- README 和 `validation.json` 已分開標明：本候選 `candidate/series.json` 23 筆編輯企劃來源；另包擬採用 25 筆、未裝入本候選或正式機；`candidate/video.json.sources` 18 筆公開引用。73 筆場景主張 ID 唯一，且與 `source-map.json`、`source-alignment.json` 的 73 筆 URL／企劃索引／公開索引映射一致。
- `node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r18/build.mjs --check` 通過：65 鏡、77 句、73 筆主張、18 筆公開來源；`lint` 錯誤 0、可愛插畫檢查錯誤 0，仍有 31 項 `lint` 警告。文字估時 436.0 秒（300 字/分）、470.6 秒（275 字/分）、510.3 秒（250 字/分），並非實際配音或成片長度。掃描未見私人主機路徑、金鑰或密碼。

## 未完成與界線

本審查限於 r17→r18 修訂、所引兩篇來源及結構對照；沒有重新獨立查證全部 73 筆正式事實，全部仍為 `PENDING`。實際 TTS、剪輯長度、盲聽、圖片聯絡表、正式機 104→新版本的六章接續與重編主張 ID 均未驗證；也沒有正式的 `story/reviews/script-review.json` 收據。候選保持 **HOLD**，不據此解除 STOP、寫正式機、呼叫付費媒體、合成或上傳。
