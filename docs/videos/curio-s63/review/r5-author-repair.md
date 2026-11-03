# S63 R5｜作者窄幅修稿紀錄

2026-10-22 UTC。此候選只回應 [R4 正式雙人盲讀 12／13 HOLD](r4-formal-merge-audit.md) 唯一共同阻擋項 `no_recap`。R4 的兩位讀者都指出 `s63103` 重講早已交代的費城接收者安排；A 單獨的 `payoffs` 否決依正式逐題 OR 已由 B 的有效肯定通過，原票和少數意見仍保存。

| ID | R4 → R5 | 固定史料與書面畫面 |
| --- | --- | --- |
| `s63103` | 刪除「費城友人已知貨箱會來」的重述，改為「清晨六點，一輛馬車駛到貨站。」 | Brown／Stearns [B09 L1564–1573](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1564-L1573) 說三點到站、六點馬車到來。單人插圖改為貨站外一輛馬車抵達；時間只由後製數字呈現。 |
| `s63104` | 將原句的六點馬車抵站拆到前句；此句只說來人詢問寫了收件地址的箱子、箱子被裝上馬車。 | 同一原文緊接 `a person inquired for a box directed to such a place` 與 `I was soon placed on this waggon`；原有單人裝車書面畫面沿用，沒有圖像模型生成可讀標籤。`s63105` 才說運到接收者住處。 |

R5 作者凍結：`video.json` SHA-256 `118430ef07ca7ac2e6d7c198088bdd1ef312755e126fef15ea2b310475a39adf`；`script.md` `dee3cb408979b3ca7dff85fb00e63915c2e54e555a0ee22e776e28fc97556c0f`；`claims.md` `5b616ce92afd61feed9264e57da240388619588e636550a91e93a315e2d6a9fc`。對 R4 的可逆差異只有上述兩個 ID 的旁白、`s63103` 插圖提示與精確來源錨點，以及相應文件狀態／視覺計畫。仍為 127 句、121 張單人插圖提示、6 張資訊卡；開場 167 漢字，約 **31 秒**，正文排除開場與 CTA 為 **2,673 漢字＝8.22 分鐘**（325 字／分鐘），維持至少八分鐘。Episode lint 0 錯誤／0 警告，`git diff --check` 通過。

**R5 仍待全新獨立史料／書面畫面覆核及兩位未看過 R4 的正式盲讀者。**R4 的來源 PASS 和 12／13 HOLD 都只適用舊雜湊；不能被移作 R5 准入。尚未呼叫付費語音、圖片、音樂或影片服務，也沒有成片、Short、上架或真實互連 watch URL。
