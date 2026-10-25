# C04 逐字稿移轉與故事字典時序收據

- 日期：2026-10-22（台北）。最終提交分支為 `codex/brand-story-bubble-wrap-c04-reviewed-script`，獨立工作樹由 Treatment commit `4fcf282b820df4625a5b1f7ca2a4ea310cd99fc0` 建立。舊草稿分支 `codex/brand-story-bubble-wrap-c04-script` 只作比對來源，不作審查或 PR 的最終版本。
- 站主選定的只是 C04 Treatment 方向；決定收據見 [plan-decision.md](plan-decision.md)。本移轉不代表逐字稿、費用、配音、圖片、配樂或上傳核准。

## 移轉基線

移轉時先帶入 `series.json`（兩工作樹 SHA-256 均為 `4F4EE515E08DC33712BD155C4236B3F7AABF4BB98BA85F85E65E655A21533B18`），再建立故事字典。草稿文字、視覺表與 builder 從舊工作樹帶入後的基線比對如下；新工作樹之後的修稿會使後兩者的雜湊改變，並以新工作樹凍結值為準。

| 檔案 | 舊樹移轉時 SHA-256 | 新樹移轉時 SHA-256 | 結果 |
| --- | --- | --- | --- |
| `draft-lines.tsv` | `71C6F7135DC77CF5768A10D17D579E1D889DAC90D94562367056D3819887083A` | 相同 | 逐句文字一致；舊盲評仍只綁舊稿或此基線稿，不延伸到後續修稿。 |
| `visual-plan.tsv` | `3661CC8D11A0A83ECFE695AB5D162B106CA2B7AE818E8EC3009E857674D67CD4` | 相同 | 此後已修正鏡頭與第三稿對位。 |
| `build-local.mjs` | `AE4E05D397BDE7856B0B64EE42186511DD5751DEE578E5B469E71AA5184415F2` | 相同 | 此後已加入逐句 `say_for` 雜湊。 |

## 字典初始化先於第一份影片資料

在**新工作樹**尚無 `video.json` 時，正式 `initializeStoryLexicon` 以 `series.json` 人名與產品名稱建立第一版故事專屬字典，isolated workdir 為 `<home>\AppData\Local\Temp\c04-bubble-lexicon-HKfJiU`。嚴格 `videoLexicon` 讀回為 snapshot 模式、sequence `1`，版本 SHA-256 `ab4ed5d515d659392a0e9424578990c1f75347274b15e43234517eacfe61484f`，初始事件 SHA-256 `0ee4af6626f27e7371c75b66892e0f517390727fec7262215666844991d5970a`。IBM、Sealed、NewAir 等名稱先以 `null` 待逐句發音確認；有版本紀錄不等於已審定唸法。

字典版本及事件於 `2026-10-22T02:50:21Z` 建立，`story-lexicon/current.json` 於同秒寫入；新工作樹首份 `video.json` 的檔案建立時間為 `2026-10-22T02:54:43Z`。舊工作樹曾先生成草稿影片資料，故不把它當成符合字典 genesis 時序的最後產物。所有最後的逐句事實審查、盲評、lint、時長與報價都必須重新綁定新工作樹凍結後的文字與影片資料雜湊。

## 新工作樹凍結讀回

2026-10-22 修正來源精度、鉤子與六個視覺提示詞後，以新工作樹這組檔案為唯一交付稿。舊工作樹的任何審查、影片資料或報價均不延伸到這組雜湊。

| 新工作樹檔案／收據 | SHA-256 | 本輪狀態 |
| --- | --- | --- |
| `draft-lines.tsv` | `39198B822F0F32F2162884DE6ED1030B4BCA0FF380BD09E0525893CB92915DB0` | 94 句；第 02–06 章 2,558 漢字，8:32 僅是每分鐘 300 字的規劃估算。 |
| `visual-plan.tsv` | `1FD21BC3F71A9D72489FADA9F42014300674632B7C060F00E4969E89597314E3` | 84 張插圖、10 張單焦點卡，最多連卡 1。 |
| `video.json` | `1BB9FD7355E6BFA5FCFA8D9A4BCFB0F89F2A5F01451131BDC3754B12243B330B` | 從以上兩表重新編譯；`lint` 0 errors／0 warnings。 |
| `reviews/script-source-review.md` | `9CD6A1AA9F9BE9F525F339512BAB1E1B8085381C1B2A2E6012707A87E5482E15` | 不同作者獨立核對 94／94 句、10 張卡與 10 個一手來源，PASS。 |

兩位盲讀各自讀取同一份最終 `draft-lines.tsv`，均於 `reviews/blind-reader-1.md`、`reviews/blind-reader-2.md` 留下綁定上述稿件雜湊的敘事 PASS。整片估價見 `production-quote.md`；成本、配音、實測時長、圖片與發布仍是獨立關卡。
