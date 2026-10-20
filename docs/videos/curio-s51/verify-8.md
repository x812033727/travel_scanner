# S51 R8｜三組重述的作者限縮修訂

2026-10-20 UTC。[R7 獨立史料、主張與書面畫面](review/r7-source-independent.md)對精確 R7 五檔判 PASS；但兩位新讀者的[正式合併敘事裁決](review/r7-official-panel.md)為 **FAIL**：共同 `no_recap` No，A 指 `cal053→054` 相鄰重講碰冰，B 指 `cal133→134` 相鄰重講卡帕西亞號已接人，另注意 `cal004→032` 耳機動作沒有明確回呼。R8 是針對這些診斷的**作者候選**，不是新版獨立來源、畫面或敘事 PASS。

| 位置 | R8 變更與固定史料界線 |
| --- | --- |
| `cal032` | 刪去第二次講無線電員摘耳機的句子及該景插畫；`cal004` 已在開場給出十一點半的動作，`cal033` 仍說沒有第二名員工接班，`cal060` 明確以「還記得十一點半摘下的耳機嗎」回呼並首次說漏收求救電文。`claims.md` 的 `cal060` 註記同步移除過期的 `cal032` 交叉引用。G [L3340–3354](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3340-L3354)支持休班，G [L3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)支持漏收。 |
| `cal053–054` | `cal053` 只說幾分鐘後補發船的位置；`cal054` 只說報文催附近的船來援，不再連續重念已在 `cal046` 講過的撞冰。G [L3163–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3163-L3197)記約十二點二十五補發正確位置、求援電文及卡帕西亞號回應。兩景仍是無可讀文字的位置紙／訊號紙示意，沒有另造電文原件。 |
| `cal134` | 刪去剛在 `cal133` 說過的卡帕西亞號已接人；改為「還記得史東通報火箭嗎？他說船長還交代了什麼？」明示這是接回 `cal075–077` 的證詞，讓 `cal135` 用史東所說的新細節「有新消息派實習生來報」回答。G [L3428–3435](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3428-L3435)只支持 **Stone 的版本**，沒有把他的說法當船長本人親口證實；書面畫面仍是匿名的後來研究桌與兩張無字路線卡。 |

其他旁白、提示詞、聲線、音樂、16 組伏筆、`research.md` 與片尾均不變；`brief.md` 首段只更新關卡狀態。由 R7 **134 景／136 句**變成 R8 **133 景／135 句**，其中 **132 景正文 `shot`**。不以重述或留白補時。

| 內容檔 | R8 SHA-256 |
| --- | --- |
| `brief.md` | `dbb931dcccfddc12a6705c33ae79ed8d6e44cbdd33352675b2e29ca64360897c` |
| `research.md`（未改） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `240314a9c838f49d10c5efb184b56e6fc67ad5287471ab6c69d9cff58fef79a8` |
| `script.md`（CLI 重生） | `7886cad66f1b223494baf728ce985daca5214f3e4663d75e31344f03555cd11b` |
| `video.json` | `b0be4e53cd80dbc304fdd659261b18d8f8bbd8f064adaeb99a8641706d1c5060` |

作者本地檢查：`claims.md` 與 JSON **135/135** 同 ID、同序、同文；`screenplay(doc)` 與 `script.md` 逐位元一致；**132/132** 正文 `shot` 提示詞非空、伏筆 **16/16** setup/payoff ID 存在且順序正確。`node tools/video/cli.mjs lint --slug curio-s51 --json` 回報 **0 errors／0 warnings**；`git diff --check` 通過。`estimateTimeline` 在 250／300／325 CPM 時，首八景開場分別 **44.80／38.60／36.37 秒**；其後正文 **639.20／551.80／520.93 秒**，最快約 **8:40.93**。這是文字估時，**不是 TTS 實長**。

**下一關：**另一位工作者按上表精確五檔與固定 G／B／A 原文獨立核 R8 三組改動、逐句主張及書面畫面；兩名全新讀者只讀精確 R8 劇本按固定 13 題盲評。R7 的獨立來源 PASS 不自動變成 R8 放行；R8 作者自檢也不當敘事 PASS。政策、站台、TTS、付費插畫、配樂、成片及上傳均未開始。
