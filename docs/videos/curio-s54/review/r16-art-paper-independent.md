# S54 R16｜三景候選插圖獨立書面覆核

2026-10-20 23:39 UTC。**書面候選 PASS（3／3）；原生圖片 KEEP 尚未判，亦非網站大綱／劇本／音訊卡、分鏡或付費核准。** 我未寫[候選預檢](r16-art-paper-preflight.md)，沒有改五份凍結創作檔、三句候選 prompt 或 `look`，也沒有生成圖片、呼叫付費 judge 或配樂。此判定只供日後考慮採入候選；採入後的新 `video.json` 要另做獨立來源及書面畫面差分，不能沿用本版的 `visualHash` 或既有分鏡判定。

## 固定版、場景與系列規則

重新計算 R16 五檔 SHA-256：`brief.md` `e45d0256fba6f068d0bbfc7614edf0444ed88156d850b64aa59f03644f680a0f`；`research.md` `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae`；`claims.md` `0477d725ca08d22589a7287b521d3738db75f2aa5033a5c9e414de8634a4ff1f`；`video.json` `1f030f6c5f58a9d09919f9fb0b6f716e64f14b468c8735ce29987ece2ad6dc02`；`script.md` `538c59b6e861b789a1bbd6ddd4609ee1a47edaac5ea6e98d41bee9ae677e162d`。本次所讀[候選預檢](r16-art-paper-preflight.md) SHA-256 為 `f5932a61542fce7bf537400a26efd9ae24712f86853a6f5db67b98b4a51a1442`。用工具實際 `visualHash(video.json)` 算得 **`ba9a43292268b35b`**。146 景中有 **138 `shot`、7 `big` 字卡、1 `outro`**；`s54002`、`s54093`、`s54121` 均為既有 `shot`，`look` 正是 `{"preset":"cute-mystery"}`。`lint --slug curio-s54 --json` 為 0 error、0 warning。

[Curio skill](../../../../.agents/skills/curio-episode/SKILL.md)與[系列畫面規格](../../history-curiosity/look.md)要求 MiniMax `image-01` 的內容相關可愛插圖、單人單動作、畫風只由既有 `look` 提供、模型文字用素面物件避開。圖片是示意，不是當日實物或文書的復原；九題 judge 以外，原生圖仍須檢查會與旁白或來源衝突的年代、付款媒介、可讀偽文書及明顯畫風偏移。無害卡通細節本身不是退件理由。正文至少 70% `shot`、連續最多三張卡片，不能拿卡片掩蓋核心插圖退件。

## 三句候選的史料與畫面判定

逐字受審候選：

- `s54002`：`Medium close shot at a January 1840 post office counter, one adult sender points to an empty shallow wooden tray beside a sealed plain letter and a small coin, soft window light`
- `s54093`：`Medium close shot in a January 1840 post office, one adult postal clerk drops a small coin into a cash tray beside a sealed letter with a plain blank front, gentle window light`
- `s54121`：`Medium shot inside a London receiving house in May 1840, one adult postal clerk closes an unmarked supply folder beside an empty wooden stamp tray, soft window light`

| 景 | 獨立覆核 | 原生圖 KEEP 時要確認 |
| --- | --- | --- |
| `s54002` | **PASS。** [H 13061–13083、13139–13147、13205–13211](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083)明說先以現金預付、郵票待備妥，以及 1840-01-10 費率生效；[L 4136–4146](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4136-L4146)把費率日與 5 月 6 日郵票准用日分列。候選 `January 1840 post office counter`、一位寄件人指向空木盤，旁有素面封信和硬幣，正好把「費率先到、票未到」畫成概念；沒有要求可讀郵票或現代物件。人物、木盤與手勢不作確切 1 月 10 日窗口復原。 | 空盤、素面信與硬幣可辨；不能出現已貼票、可讀票樣或現代收銀設備。 |
| `s54093` | **PASS。** [H 13208–13250](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13208-L13250)的希爾日記轉錄只說 112,000 封中約 13,000–14,000 未預付，沒有說其餘貼了票，也沒給該郵局位置或全國總數。候選 1840 年 1 月郵局的一名職員把硬幣放進收款盤，旁有正面全白的普通信，以現金付款示意「預付不等於貼票」；不把單封信充作數量證據。無文字或現代道具要求。 | 現金收款與未貼票的素面信可辨；不能出現貼票、暗示已售郵票的陳列或把統計寫成偽帳簿。 |
| `s54121` | **PASS。** [H 13353–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13353-L13389)是希爾事後說倫敦收件所沒有領到郵票，並稱財政部指示信漏了 *not*；原信未核。候選 1840 年 5 月倫敦收件所的一名職員關上**素面**資料夾，旁有空木盤，畫的是配送未到的後果，沒有聲稱還原原信、特定職員或特定收件所。5 月而非 1 月，時序正確；沒有要求可讀指示信或現代物件。 | 資料夾須閉合、素面，盤須空；不能出現可讀信件、放大的 *not*、仿原件或收件所已拿到郵票。 |

三句不需在紙上改詞。這只是提示詞與來源相容的判定；模型若自行畫出誤導細節，須看 1280×720 **原生 JPG** 再作 KEEP／REJECT，不靠縮圖或九題分數代替。每張記精確 prompt、JPG SHA、九題結果及人工原因。

## 試畫停工、即時額度與上限

沿用候選預檢的窄幅試畫界線：網站三張審核卡先有決定，且能綁定精確 R16 音訊；開付費前重查五檔、網站卡、`media-status`、私有 ledger、圖片快取及 dry-run。若採入三句，必須重核新 `visualHash` 的分鏡綁定並重新獨立覆核。三景各先 **1 take + 1 judge**，只有 **3／3 原生圖 KEEP** 才可放行餘下 135 張和配樂。任一 REJECT 立即停新景、放量和配樂；整個 pilot 合計最多一次窄幅改詞、獨立差分覆核及失敗景 **1 take + 1 judge**。重試仍 REJECT，或另一景 REJECT，即 **STOP**；不得買第三張湊過線。

23:39 UTC 重新讀取 `media-status --slug curio-s54 --json`：本集 ledger 仍 **US$0、0 圖、0 judge、0 music、0 reservation**。站台當時月額度為圖片 **18,769／30,000（餘 11,231）**、judge **20,071／30,000（餘 9,929）**、配樂 **62／100（餘 38）**；是會變動的站台快照，不把它當付費許可。`keyframes --takes 3 --dry-run` 仍報 138 景、最多約 US$5.59；用既有 R16 時間線執行 `music --dry-run` 報 600 秒約 US$0.08。首輪 `3 × (0.0035 + 0.0100) = US$0.0405`，唯一一次重試後 pilot 最多 `4 × 0.0135 = US$0.0540`。保守整集 `138 × 3 × (0.0035 + 0.0100) + 0.08 = US$5.669`，向上取分後的**累計硬上限提案 US$5.67**包含目前 US$0、pilot、重試、全部圖片與 judge、配樂。若採入後張數、價格或帳本變大，付費前重算較高上限。

**結論：候選書面 PASS，無提示詞修正要求；原生圖及網站關卡仍待其各自驗收。** 本頁沒有核准花費、核准網站卡或宣稱現有音訊已由站主批准。
