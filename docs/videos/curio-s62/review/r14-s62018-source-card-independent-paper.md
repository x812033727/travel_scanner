# curio-s62 s62018 耗盡後來源卡：獨立紙審

2026-10-22 UTC；不同作者 reviewer policy_duration_incremental_review。**PASS 書面來源卡**。3 actual已耗盡、0 remaining；不清除先前三張原圖FAIL、不允許第四張。未付費、未動media／manifest。

## 來源判斷

重開固定 `/tmp/curio-s62-sidereal.txt` L550–568，其中L558–564在小孔薄金屬片量星間角距段寫 `within an error of one or two minutes.` 卡「1–2角分／伽利略自述的量測誤差」與原口播「他說這樣量出的角距，仍可能差上一兩角分。」相符。minutes指angular minutes，非時間分鐘、不是現代儀器校準／獨立重測。

此是1610作者敘述經1880 Carlos譯本轉述的測量誤差說明；數字表示其所稱誤差幅度／容許誤差，不主張每筆觀測必定至少差1角分，也不增補現代可靠精度。未使用後世周期或四顆天體的具名身分。

114 scenes：109 shot、5 big；插圖109/114=95.61%，高於70%。最長連續卡1；新增s62018前後皆shot。獨立lint為0 errors／3詞頻warnings。

## 精確未變與綁定

- 將當前唯一卡的template/data逆套作者old，完整video SHA回到先前獨立審核的`6616f4f080b947bf392a5fc5835676d1259c9f229983e7ac3dae134530dec316`。因此只有此卡template/data改變：全部114 spoken及其他scene、既有KEEP、look等完全不變。
- 正式script與claims均包含當前全部114句逐字文字；script重產不代表改口播。
- 本次原文檔SHA重新驗算，來源版本與研究固定值一致。

- `video.json` SHA-256：`db347370e999f27694850db6ad45931d1aa59886932512893abfdee1c4745180`
- `script.md` SHA-256：`bb125a43aa15e2fcbda3f25b7e137d6ae81cb97f5a35973f8702a8774231f766`
- `claims.md` SHA-256：`22cc526f6293de6a0fa282bce8ae1ff9f9d06b325498a6d7d198b392010ce8fd`
- `research.md` SHA-256：`7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb`
- `review/r14-s62018-source-card-author.json` SHA-256：`bc5bba259db22f7cd61a0528db7cba2e4979f0a8e3b1a1b8568c6b4eb9ac1121`
- `/tmp/curio-s62-sidereal.txt` SHA-256：`74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`
