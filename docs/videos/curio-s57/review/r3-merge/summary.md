# S57 R3｜正式雙盲敘事合併診斷

2026-10-20 UTC。**敘事 HOLD：正式 OR 合併 10／13，三個必答題未過。**這是下表固定 R3 候選稿的雙盲讀者票合併，不是作者自評、史料 PASS 或媒體放行。[R3 獨立來源／書面畫面覆核](../r3-source-independent.md)另因二月補給先後顛倒 **HOLD**。因此 Jev 政策、語音、插圖、配樂及成片均不在本關執行。

| 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `7a68ed10261086ba13dbf1a85a87932eb8ad8a81723874c6abeb0df8490fe657` |
| `claims.md` | `0f7e8278ac3482b79bd9013d29c187940f99869794f1fe7c241071511459c262` |
| `video.json` | `698b29027e4b57523d62e7bda8210e5f2dfc5910a6a1b2507f156fdd3b6088a0` |
| `script.md` | `afc30e64b439c4d3ea783ab6a47b57f63b8c73c34ece00e85b3a4b46281c71f7` |

兩位無前情讀者的[原始 A 票](raw-ballot-a.md)與[原始 B 票](raw-ballot-b.md)逐字封存，SHA-256 分別為 `edbcd3034b36acff307ebc8b88c09556e280ac0157c85b1790c5b1d1bfc68de4`、`a640a2a0ab1f243497963ebb387d4f9222c0953035da1c2f867e20b20637d600`；兩份原票均寫明只讀 R3 `script.md` 與官方 13 題，且前後劇本 SHA 同上。A 為 **9 Yes／4 No**，B 為 **10 Yes／3 No**。我按原票逐題轉錄為[官方形狀 A JSON](ballot-a.json)、[B JSON](ballot-b.json)，保留每一票的 Yes／No；26 個引用以凍結稿對應 ID 的**逐字原句**補成官方欄位，並在[完整稽核](merge-audit.json)保留原票理由、引用 ID、來源／副本 SHA、對齊結果與兩份 `panelVerdict`。沒有改判任何一票。

使用 `tools/video/core/narrative.mjs` 的 `panelVerdict` 與 **`mergePanelVerdicts` 固定 OR**：同一題任一讀者有帶行號的 Yes，合併即 Yes；只有兩位都 No 才未過。[合併答案](merged-answers.json)與完整稽核記錄 13 題皆齊、規則 SHA `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。`no_detour` 為 A No、B Yes，故按規則合併通過；A 的湖行岔題異議仍在原票與稽核中，沒有偷改成兩票一致。

在執行 CLI 前及之後均重新核對五檔 SHA 全部吻合。以 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r3-merge/merged-answers.json --workdir /tmp/curio-s57-r3-merge-formal-20261020 --json` 跑官方關卡：**exit 1、`passed:false`、三題 required fail、0 advisory fail**。保留[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[exit code](cli.exit-code.txt)、[CLI 執行與前後 hash 狀態](cli-status.json)、[官方產生的敘事紀錄](official-narrative-record.json)。紀錄的 `panel_narration_sha256` 為 `046f945307f7b8a270e78326332f6f613748db0768bd40ba1e8ebd6a60068eaf`，紀錄檔 SHA-256 為 `1923cb55fa8736748af5e0bc3d085c3191506c7b4e87e7d974926266bc4db9dc`。

| 兩票共同 No | R3 精確斷點與修稿界線 |
| --- | --- |
| `chapters_link` | 兩位都指出開場 `s57010` 問「為何走成兩條路」，下一章首句 `s57011` 只報「1871 晚秋回到烏吉吉」，沒讓聽眾當下聽懂回溯如何接上分路問題。R3 修好後段 `s57164 → s57165` 的信件銜接，仍漏了這個開場邊界。章首須用有來源的病況／缺貨事實接回選擇，不可硬造因果。 |
| `payoffs` | 兩位都指出 `s57034` 假設「如果等不到救援，這段等待還能撐多久？」後面只讓援助抵達，沒有回答**救援未到時的可撐時長**。A 另指出 `s57090` 問河流實際方向，`s57091–s57093` 只載互相矛盾的說法與暫緩判斷。固定史料若無答案，應改問可被後文回答的具體問題，或刪去未回收的問句；不得編造時長或河流結論。 |
| `no_recap` | A 指 `s57156–s57157` 接連兩句都說路線是計畫、尚未走成；B 指 `s57067` 已說不肯放下考察，`s57072` 在同一勸歸段再說先完成未竟工作。兩個位置都應逐點處理，否則下一位讀者仍可能抓到另一處；保留必要的一次史料限定即可。 |

**下一步：**作者另產新版本，先修獨立史料 HOLD 的 18→19→20 日補給時序，並按三個共同 No 窄修敘事；重新凍結完整五檔 SHA，再由兩位新讀者各自盲讀、正式合併及獨立史料覆核。本 R3 合併與 R3 來源 HOLD 均只綁定此處五檔，不可套用到新版本。
