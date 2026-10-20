# S52 R15｜18 句音訊旗標獨立覆核：聲學 HOLD

2026-10-20 UTC。這是對[正式待聽清單](r15-audio-final-flag-review.json)的獨立核對，**沒有取得實際聽音判讀**，所以 **18／18 句聲學判定均為 HOLD**。下表的差異只來自現有 Gemini 轉寫與凍結稿；「文字差異」不等於 TTS 真正唸錯，也不能把近音字或人名直接清旗標。未重配語音，未改劇本，沒有給音訊關 PASS。

## 證據與可聽性界線

- 凍結 `script.md` SHA-256：`1764cc03aa5bb5ea402e89b7e21e163d676045c6e42611dfaa54fdc69fa62131`；待聽清單 SHA-256：`ff842334caae89b9a12b9dea57420a8aac635191c00890066bf0c0129ed6fd04`。私有 `round2/check.json` SHA-256 `879e5813b7e967528c17f8c293dd5550b7b79d2127e432fb426a92f2afa8a6be`；`round2/check-flags.json` SHA-256 `a3f691fd4d79d9e626c4d807364e32787b3396916db8f63ac3f034de0efe8d85`。
- 現行 `timeline.json` SHA-256 `4c60f8f5e3b1ed502421c2bf10228c79a48d995c1dca7300490f3845e6c505a8`；`narration.wav` SHA-256 `7f9ff69bfc3d709ba73d822767070254a2d0955457eb5697fb002f7a0c1a8c95`。18 個單句 WAV 的 SHA 均與清單相符，皆為 48 kHz、16-bit、單聲道 PCM；FFmpeg 對全部 18 個檔案解碼無錯。逐句 `intended`、`heard`、Jev 分數、WAV hash 前 16 碼和時間格亦分別與 `check.json`、`timeline.json` 一致。
- 本工作階段試把 `s52004.wav` 轉成 MP3 並送入音訊輸入通道，但工具明確回覆 **“audio content omitted because you do not support audio input”**。命令列可驗證檔案解碼，卻不會讓審稿模型聽到聲音；沒有獨立聽音工具或聽者回條。`faster-whisper` 等第二轉寫器亦未安裝；再跑文字轉寫也不能冒充實聽。以下只記已核對的文字風險，不作聲學推論。

## 逐句結果

每列 `WAV SHA-256` 指向清單所列 `/workspace/.video-work/curio-s52/audio/<ID>.wav` 的現行音檔。`文字差異` 為凍結稿 → 現有 ASR，不是我的聽寫。

| ID | WAV SHA-256 | 文字差異及需聽辨之處 | 聲學判定 |
| --- | --- | --- | --- |
| `s52004` | `5c726267f84c5f78bd9c8896a720d40dba81ce6bfc0c7569ba5a00dce81f21df` | 「秒數」→「描述」；問題的量測對象在 ASR 文本改變，兩詞近音，須實聽。 | **HOLD** |
| `s52301` | `b6336ef10ca735d0874dfa712b0eff0fb139be25a54bb6ca026715f297156b5a` | 人名「基皮斯」→「吉皮斯」；近音拼寫，不能由字形斷定唸錯。 | **HOLD** |
| `s52314` | `7f4e482a0e50da9ca19c420a92e98e6aa7feaf1f8419faf38a05ee10f21d20d7` | 「原報」→「原本」、「等高度校鐘」→「等高度角校中」；ASR 改了史料與校時用語，須逐詞聽。 | **HOLD** |
| `s52054` | `2d0d94f911970c6ddb6a6de9882555522dad0e7d917bf53abae83b93ce8bd73f` | 「五月三十日」→數字寫法「5月30日」屬記法；「仍記」→「仍擠」須聽辨。 | **HOLD** |
| `s52070` | `3baaa42825d4c073aeac7da3c3752f9ae60577223b1944336d1b3fb8680afdcd` | 人名「格林」→「葛林」；同音字形差異。 | **HOLD** |
| `s52078` | `24ae3cf7f91fe2d0592127526025d4420d1b733c4baa8f07e271ac328b5bfdca` | 「逐人」→「族人」、「秒數」→「描述」；ASR 文本改變比較對象與數值含義。 | **HOLD** |
| `s52303` | `06c36c33ecd99078d5be3acdfccefc194963886564727050728e3ffc8415c5ee` | 人名「基皮斯」→「吉皮斯」；近音拼寫。 | **HOLD** |
| `s52094` | `5dea53586465f9b3c025664530d8fb317088959923c672e77c958c32be12699a` | 人名「基皮斯」→「開皮斯」；ASR 專名不穩，首字音須聽辨。 | **HOLD** |
| `s52116` | `ee361fc60af8d04e59200724def9f8f44a3fcdf31e20be99de5c8888a3bff2e5` | 人名「基皮斯」→「GP4」；ASR 將專名猜成字母數字，不能從輸出反推口播。 | **HOLD** |
| `s52117` | `a29707b63e17a01ab888e9231acfb0386d60f51ee1fc8c06e1efd8fe6e5db567` | 「依」→「以」、「格林」→「格令」；文字近／同音，標點差異不作語音錯誤。 | **HOLD** |
| `s52118` | `98365da1f4f7b7e70cf901db9175ff5da377c48cb2d25eb085fb91eb09ae3a5f` | 「秒數」→「描述」；ASR 文本把未列的讀時數值改成描述。 | **HOLD** |
| `s52306` | `48576095e5b977e7aa283ad8f2a0d29efcd84d04a5ee397a27ef0d10a3ebbc51` | 「基皮斯」→「基皮瑟」、「後出」→「後續」；前者專名近音，後者在 ASR 文本改了時間層次；「記錄／紀錄」為字形。 | **HOLD** |
| `s52122` | `090cb3da65aa3dddcf3f233322152de96960ac9b6f45dabb9cc1deff417e1ff1` | 句首回答「會。」在 ASR 中缺失；須實聽判斷是未唸、太輕、裁切或漏轉寫。 | **HOLD** |
| `s52316` | `448caafcacc574d0753f9593b930ae7ee28d3fae9fa561cf4ac695e0f5d4931d` | 「原報」→「原PO」；ASR 選現代詞，須聽辨聲母及韻母。 | **HOLD** |
| `s52321` | `b17e16cacd3c281e99f85ef81ee6e477ca5ff0c17984e31a7ab91a26916318f4` | 「內接觸」→「內接處」；接近同音，須聽句尾是否有「觸」的讀音。 | **HOLD** |
| `s52324` | `17d127e323ea663c021c186b8c40be0b96e614e11f33aeec92e4d4fe5bfd275a` | 「原報」→「原貌」；字義不同，尾字聲母亦值得實聽。 | **HOLD** |
| `s52127` | `650c72a1734ac1151a2861536abd3627a1ce9a295bf8fcd2dc721de0c4d4d457` | 「三處」→「刪除」、「秒數」→「描述」；ASR 文本改了來源數量和讀時數值。 | **HOLD** |
| `s52128` | `f8373dafe71c7ffbfdce6948186323e0bd8e86a0ac825a7ee009a59c198ffe16` | 「逐人」→「族人」、「四格」→「四個」；ASR 文本改了逐人四欄時刻的限定。 | **HOLD** |

## 關卡結果

18 個旗標均未獲聲學清除。現有正式 `check-audio` 為 119／119 已檢、18 flags、退出碼 1；依[影音工具的音訊關規則](../../../../.agents/skills/youtube-video/SKILL.md)，音訊卡仍須站主在網站審核，不能將這份技術核對當作音訊批准。需要能真正聽到上述 SHA 綁定 WAV 的聽者逐句核對，先分清口播與 ASR 猜字，再決定是否修改；兩輪定點重配已達本稿上限，沒有做第三輪。
