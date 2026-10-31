# S51 R15｜第二輪試畫後三景提示詞窄修

2026-10-20 UTC。依 [實際選圖覆核](r15-native-art-pilot2.md)只改 `cal005/015/018` 三個 `scene.data.prompt`，逐字同步 `claims.md` 末段相同景 ID 的畫面備註。首 131 條主張、引文、旁白、聲音、章節、其他提示詞皆未改。

| 景 | 修正與史料界線 |
| --- | --- |
| `cal005` | R06 只證午夜後白色信號火箭升起；畫一枚從海平線垂直升起的小型白色海事煙火和短尾，不畫飛彈，也不指定發射船身份。 |
| `cal015` | R01 及 G L3362–3364、L3399–3401 記貨船沒有乘客但船橋照常有人值班；畫一名值班員在室內木船橋，窗外黑海，不強求其面向。桌子是示意，非船上具體佈局證據。 |
| `cal018` | R04／G L3366–3373 支持格羅夫斯說見兩盞桅燈並猜是客輪；畫同一條無名遠船低剪影上高低兩白點，沒有證明它實為客輪或鐵達尼號。 |

| 檔案 | 前版 SHA-256 | 本版 SHA-256 |
| --- | --- | --- |
| `brief.md` | `bea6a0ff26ddfed12ee2b9d077b2359a12392c301bf9032c69e66a403337a0e3` | 同左 |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` | 同左 |
| `script.md` | `cbc5a1891deacd029e081b61eb316e076e422cdb45ebceb4b072fa875e55ce83` | 同左 |
| `claims.md` | `c9dc1ec402f48f3ee55e663c6a988872ca286c55994f766106fa29a006a23e69` | `8ed2a82a193ad95f4111af0136fb3da8892e1ebbbff5e16d1be6a1707140bdf1` |
| `video.json` | `6e387d19cf4562be1a34b75c0177a20de3a3ce67a583bcf4aba1cb84a1f26634` | `f67295e932e1733470e5e23dbc311bc4fdae075ced530d35bfeeaf61ffed08ba` |

三個新 prompt 各在 claims 畫面備註逐字出現一次；`lint --slug curio-s51 --json` 0 errors／0 warnings、`git diff --check` 通過。當時站台本月只餘四次圖像評審，故先用每景單次試畫檢查這三景；失敗即保留 HOLD，不把機器評審或站主審核寫成已過。
