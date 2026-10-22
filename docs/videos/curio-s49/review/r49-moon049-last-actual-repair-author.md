# S49 moon049｜最後一次實際出圖前的提示詞修訂（作者稿）

2026-10-22 UTC。**待獨立紙面覆核；尚未重綁、解 STOP 或送出最後一次付費重畫。**

## 為何修

第二次原圖雖經機器 9.29 PASS，獨立原尺寸覆核在 [剩餘插圖報告](remaining-native-review-20261022.md) 判 REJECT：畫的是已裝入木框的矩形窗片，沒有可辨的獨立圓形鏡片。口播 `moon049` 說虛構報導的鏡片先到倫敦，再造顯微鏡和轉動架。固定來源 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 第 488–499 行描述誇張鏡片數字，第 501–511 行分開描述運到 metropolis 的 lens 與之後製作的 microscope、mechanical frame-work。這是 Locke 名下 1859 年**重印的 1835 年虛構新聞**；提示詞只畫那篇故事的想像畫面，不重建 Herschel 的真實設備，也不指定來源未能核實的尺寸與精密型制。

## 單景修訂

舊 `data.prompt`：

> Medium shot in an imagined 1830s workshop from a fictional newspaper report: one adult craftsperson sets a plain model lens beside an unmarked movable frame, soft indirect light, no real Herschel equipment

新 `data.prompt`：

> Medium shot in an imagined 1835 London workshop from a fictional newspaper story: one adult craftsperson in a linen shirt and waistcoat steadies one detached round glass lens on a wooden table, its full circular rim visible beside an empty movable frame, soft indirect light

新版要求鏡片**獨立、圓形、整圈邊緣可見**，旁邊框架保持空置；成年工匠的 linen shirt／waistcoat、1835 London 明確限定年代與地點。舊提示詞末尾的抽象否定句 `no real Herschel equipment` 已由開頭的 `imagined`／`fictional newspaper story` 正面語境取代，沒有新增風格詞或否定詞。只改 `video.json` 的 `scenes[45].data.prompt`，並在 `claims.md` 的 `moon049` 視覺欄逐字同步；口播、鏡頭、動態及其餘 128 個場景均未改。逐欄資料見 [作者差異](r49-moon049-last-actual-repair-diff.json)。

## 狀態與門檻

- 動筆前確認 `/workspace/.video-work/curio-s49/STOP` 存在，`media/jobs.json` 為 `{"jobs":{}}`，剩餘批次 log 顯示 STOP 後排空；修訂後仍未動 STOP、manifest 或媒體帳本。
- `moon049` 已用 2／3 次實際出圖，只有 **1 次**；`moon050` 已用 1／3 次但沒有選圖。STOP 時總帳 106 image、106 judge、US$1.431、零預留。
- STOP 時舊 `video.json` SHA-256 `461a8c6f3cf3f2df0878321697a9f4a062cf699652bfddeb02856975eb6849d8`；本作者稿新 SHA-256 `454ea00f42ca79ba6a4c9a356c6fef736c361d04cf269371653225075b9d2955`。`claims.md` 舊 `d0db751d0fbccd7ee2618a061096b6aca1f8b4927dcec3e2b623809cb0f6295e` → 新 `6ddb3b559418fd7538892b7decbdc8c11d231f3c6927da861625f6dc7cbef7fa`。`script.md` 仍為 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；manifest 仍為 `d9bdfcec53f7059388fde67ff3fe82f6cf24c296c9f24a69220a793d050b6e4b`。
- `lint --slug curio-s49 --json` 退出 0、**0 errors／1 warning**：115 景中仍有 39 景提示詞含 `window`，超過其多樣性建議；本景新版不含 `window`，警告是全片既存情況。沒有付費工具呼叫。

下一步由另一人獨立核對來源和新版提示詞，通過後才可由製作方決定是否重綁並使用 `moon049` 最後一次實際嘗試；此作者稿本身不是驗收或畫圖授權。
