# S55 R10｜單句獨立史料與書面畫面覆核

2026-10-20 UTC。**史料 PASS；138／138 主張對齊 PASS；書面畫面 PASS。** 本判定只適用下列 R10 五檔；敘事雙盲、語音、實際插圖與站台核准仍分開驗收。我沒有修改作者稿或產生媒體。

| 內容檔 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `brief.md` | `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070` |
| `claims.md` | `9e65b7a2aeb55a749ba20397a589d840ae0b6b0cbda196026daf55f76781522c` |
| `video.json` | `cc86ecf2165f658417d81235d432cc00429e0f6cc853e3011d8b74d15177d6ed` |
| `script.md` | `5e231cb244bf28075f64df92d64d5a529d9b6d5e954fd093cdf42f13c80799f9` |

## 固定原文與修訂句

我從固定 Git 提交獨立重取 [F／富蘭克林五封信的 1907 年壓印副本編刊](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L122-L179)，全文 SHA-256 `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`，與研究表固定版本相同。[F 122–151](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L122-L151)記 Charles 的空球直徑 **12 英尺**，由繩鬆開升空，當時無乘客。[F 175–179](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L179)記 Montgolfier 另有直徑 **38 英尺**的球正在準備。R10 `s55038` 說「那顆新球直徑約三十八英尺，比先前查爾斯放飛的無人小球大出許多」，數字比較與「先前」「無人」均有上述文本支持；沒有把準備中的球說成已載人自由飛行。兩份數字同出富蘭克林的當時信，並非獨立量測證明，口播仍以「約」界定。

R9 的同句重唸十二英尺；R10 保留首次出現在 `s55018` 的十二英尺，在 `s55038` 只給新的三十八英尺和具體「先前查爾斯放飛」回呼。這解決兩位 R9 無背景讀者指出的表面重述，但新的敘事判斷須由新讀者做，不能沿用我這份來源判定。

## 精確差分、畫面與機械檢查

在 R10 `video.json` 將 `s55038` 新口播逆換為 R9 舊句，SHA-256 **恰等於**已凍結的 R9 `525ba099fc70de1c03d49327ac854348b001808d3c8580ad558ee487d8ccf669`；在 R10 `claims.md` 逆換同句並移去本輪新補的 F 122–151 連結，SHA-256 **恰等於** R9 `f069c516d79c16ef7091d1f4cda72927cbc3da583625f8d9b096c7a9ca64dff0`。故除口播一句與一列來源欄外沒有其他 `video.json` 或主張表變動，尤其鏡頭提示詞、章次、伏筆、片尾均未改。原提示詞畫一個準備中的大布球旁放更小的封閉球**模型**，沒有可讀尺標，也沒有把兩顆歷史實物畫成同時在場；作為卡通尺寸對照，書面上不與原文矛盾。實際生成後仍須看圖判定。

`video.json` 的非片尾正文有 **138 句**，與 `claims.md` **138 列**逐 ID、逐字、逐序一致，ID 無重複；`script.md` 與 `screenplay(video.json)` 位元組相同。濃縮開場 175 個漢字，按最快每分鐘 325 字為 **32.3 秒**；後續正文 2,626 個漢字，最快估算 **8.08 分鐘**。`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s55 --json` 為 **0 errors／0 warnings**、140 句含片尾。此為書面估算，不代表已合成 TTS 或通過音訊審核。

下一關是兩位真正無先前稿件背景的讀者各自對此 SHA 的官方 13 題投票，正式 OR 合併；其後才可處理政策與旁白。R9 的來源 PASS 也不直接充當 R10 的版本簽核。
