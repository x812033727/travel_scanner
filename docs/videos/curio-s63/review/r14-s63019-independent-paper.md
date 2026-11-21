# S63 R14｜`s63019` 耗盡後名稱卡獨立紙審

2026-10-22 UTC。與資訊卡作者不同的 reviewer。**PASS：固定來源支持卡片，畫面比例與連卡合規，`video.json`／`claims.md` 綁定一致。**這是替代耗盡插圖的紙面審核，不把三張原圖 FAIL 改判 KEEP，也不准第四次出圖；新的卡片尚須由製作方重綁 manifest 與後續正式關卡。

## 固定來源與卡片文案

固定 Brown／Stearns 文本 `/tmp/curio-s63-box-brown-1849.txt` SHA-256 `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2`。第 **1192–1195** 行明寫 Brown 結識名為 **Nancy** 的年輕女子，友誼發展為相愛，兩人須申請結婚許可。第 **913–914** 行已交代他被帶至 Richmond 工廠；第 **1199–1203** 行又稱 Nancy 的奴役者屬 Richmond 教會、之後她被賣給 Richmond 鞍匠。卡片「**南希／在里奇蒙相識**」的姓名是直接原文，「在里奇蒙」是這段連續敘事的地點歸納，**不是**原文在 L1192 的逐字地點句；作為簡短情節標示合理，不冒充婚姻證明或人物原件。該出版敘事是 Brown 自述事實經 Stearns 筆寫，不是當時錄音或 Brown 本人手稿。

`s63019` 的 127 句之一仍是「他在城裡認識南希，兩人相愛，卻連結婚都要別人點頭；這份允許能保住他們的家嗎？」。新 `big` 卡僅把姓名與相識城市放在畫面，沒有加入來源未見的日期、肖像、買賣條款或人物姿態。作者 [R14 差異紀錄](r14-s63019-source-card-author.json)把該景 `shot` 改為 `big`，`data.text`「南希」、`data.sub`「在里奇蒙相識」。`claims.md` 第 25 行的畫面欄已同步為「名稱資訊卡：南希／在里奇蒙相識；原文情節標示，非人物原件。」且來源錨、旁白欄未動。

## 精確變更、比例與工具結果

- 對 Git HEAD 舊 `video.json` 逐葉比對：共 **127 scene 同序**；只有 `scenes[18]`（`s63019`）的 `template`、`data` 從 shot 提示詞／鏡頭改為 `big` 卡，回填舊兩欄即還原整份 JSON。**127／127 spoken、其他 126 景及既有 KEEP 未變**。`script.md` 重產只更動本景標頭的 `（big）` 和 narrative footer；speech footer 仍為 `06b8d7048f7138e5`。
- 本版 **119／127 = 93.70% shot**，高於 Curio 70% 下限；8 張卡，最長相鄰 **2 張**（上限 3）。`s63019` 前後 `s63018`、`s63020` 均為 shot，不造成新連卡。
- 官方 `lint --slug curio-s63 --json` exit 0、**0 errors／2 warnings**：`s63018` 鏡頭距離詞及全片 `black` 詞頻；兩者均不是本卡來源或比例錯誤。

| 綁定檔案 | SHA-256 |
| --- | --- |
| `video.json` | `4f505343c41bbd8f80b5be96cd96df844a3d4c02a00ee20eb78b43d694c2bf2d` |
| `script.md` | `595d8e63c9e2870ca3c166fa0fe4f30ad38ff466104ec439d07586412a75abf6` |
| `claims.md` | `a29c2077d6c49a35dd5bc4b252709d88ccdc3867b28aebfd3ac1b66d659d5df1` |
| `/workspace/.video-work/curio-s63/keyframes/manifest.json` | `cacc4872f5fa5a02ddaed2311a48a81e09e28419f8b5d1ad84daf3e7fca24ec3` |

停止狀態：`STOP` 在位，`media/jobs.json` 為 `{"jobs":{}}`。帳本保留 `s63019` **3 次 image／3 次 judge**，皆 machine FAIL，剩 **0**；目前舊 manifest 該景仍是 `needs_review:true` 的敗圖條目（只列 2 個 takes），與帳本第三次實際嘗試不一致；因此後續重綁需以帳本和原圖敗圖紀錄為準，不能因 manifest 僅列兩次而再試第四張。本紙審沒有修改 manifest、STOP、媒體帳本、提示詞或旁白，亦未呼叫付費工具。
