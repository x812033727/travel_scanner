# S62 R15｜`s62023` 夜景提示詞獨立紙面覆核

2026-10-22 UTC。與 R15 提示詞作者不同的 reviewer。**PASS：固定來源、夜景提示詞與 `claims.md` 畫面欄逐字同步。**兩張先前白晝敗圖仍為 REJECT；本票只通過最後一次實際出圖前的紙面修稿，不把尚未生成的新畫面預先判 KEEP，也不啟動任何媒體。

## 固定來源與修復內容

固定原文 `/tmp/curio-s62-sidereal.txt` SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`，第 **1267–1273** 行明寫 1610 年一月七日 **first hour of the following night**、透過望遠鏡觀察木星與附近細點；譯註第 **1280–1281** 行釐清從日落起算。這是 Galileo 1610 年原書經 Carlos 1880 年英譯／編註的固定文本；譯註不冒充 Galileo 原句。`s62023` 口播「一月七日晚，他第一次留意木星兩旁這幾點。」與其相合。來源不固定陽台形狀或鏡筒構造；新圖只要求通用 1610 義大利石陽台、同一成年學者、普通手持光學筒，不冒稱真實原景或特定存世儀器。

作者 [R15 差異紀錄](r15-s62023-night-author.json)的新 `data.prompt`：

> Close shot on an Italian stone balcony on a clear winter night in January 1610, one adult European scholar in a wool doublet and white linen ruff leans to the eyepiece of a plain handheld telescope, dark sky beyond the stone parapet.

舊版 `pale early light from the courtyard` 曾導出兩張白晝原圖：`s62023` take1 machine FAIL，take2 machine 10 PASS 但獨立原圖 REJECT，詳 [R14 原圖覆核](r14-remaining-native-review.md)。新版明確指定一月冬夜和欄外暗天，將學者眼睛放在目鏡，沒有畫入實際星數、虛構原始星圖、電子器材或來源沒有的精密規格。**這一筆提示詞內容可修日夜衝突。**

## 精確變更與檔案綁定

逐葉比較 R14 已鎖定 `video.json` SHA-256 `db347370e999f27694850db6ad45931d1aa59886932512893abfdee1c4745180` 與 R15 作者版 `9fa0b2fc205310c5389b4611043be82c2590b773a3d6df7f58e2acf3c6a5a257`：**114 scene 同序，僅 `scenes[22].data.prompt`（`s62023`）一個 leaf 變動**。因此 114／114 口播文字、卡、其他 108 張 shot 提示、look、camera、visual、既有 KEEP 均未變。`script.md` 仍為 `bb125a43aa15e2fcbda3f25b7e137d6ae81cb97f5a35973f8702a8774231f766`。

作者其後把 `claims.md` **僅 `s62023` 畫面欄一列**替換，與 `video.json` 新 `data.prompt` 逐字一致；其他 claims 行及其來源錨不變。`claims.md` 舊 SHA-256 `22cc526f6293de6a0fa282bce8ae1ff9f9d06b325498a6d7d198b392010ce8fd` → **新 `1565041acc73dedfbe70c3bec542ba49d621ff4e437dc804b5332e2bcf561354`**。以 Git HEAD 舊版逐葉／逐行比對，僅上述 prompt leaf 與一列視覺欄變動；`video.json` 新 SHA-256 仍為 `9fa0b2fc205310c5389b4611043be82c2590b773a3d6df7f58e2acf3c6a5a257`。正式 `lint --slug curio-s62 --json` exit 0、**0 errors／3 全片詞頻 warnings**（`scholar` 108／109、`italian` 107／109、`adult` 107／109）；這三項不是本景日夜或來源錯誤。本票為獨立紙面 PASS，實際生圖後仍須再看原圖。

停止狀態獨立重驗：`/workspace/.video-work/curio-s62/STOP` 存在，`media/jobs.json` 為 `{"jobs":{}}`，manifest SHA-256 `140fc91d286e0bc09c5a2ac5208a736e2ebe32d4459f1c0faa17db2564fb2674`。`s62023` 已用 **2／3 actual**、剩 **1**；`s62024` 有 **1 次 ready、未 judge、無 selected**，本票未改其狀態。帳本總計 39 image、38 judge、US$0.5165、零預留。未修改提示詞、claims、旁白、manifest、媒體帳本或 STOP，亦未呼叫付費工具。
