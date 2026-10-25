# S61 R2｜獨立史料與書面畫面重覆核

2026-10-22 UTC。**PASS：R1 的軍種歸屬 HOLD 已解除，僅限固定稿的史料與書面畫面。**我沒有參與 R2 作者修訂，沒有修改企劃、旁白、證據表或分鏡，亦未呼叫任何付費媒體工具。這不是盲讀、原生插圖驗收或成片核准。

固定 Samuel Henry Prince，*Catastrophe and Social Change*（1920）全文 SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。L1832–1834 明寫「For the flooding of the powder magazine **in the naval yard** an **entire battery** volunteered. This was why the second explosion did not actually occur.」因此海軍造船廠是**火藥庫的位置**，原文沒有給志願砲兵隊海軍軍種；「灌水所以沒再爆炸」仍須歸給 Prince 的記述，不能自稱獨立軍方查證。

R2 的 `s61035` 明說「海軍造船廠的火藥庫」，`s61058` 明說「一整支砲兵隊」，企劃、P08 研究列、證據表與 YouTube 說明同步採同一來源邊界。R1 被點出的六個畫面 `s61009/54/58/63/98/102` 已改為未標軍種的志願者或一般砲兵志願者，沒有海軍砲兵、海軍人員標示或臆造水管；`s61058` 只示意隊員走向庫房，沒有偽造灌水設備或操作程序。其餘海軍造船廠守衛提示詞示意的是**地點**，沒有把守衛說成參與灌水的砲兵隊。消防員救火用的水管是另一來源錨點，未混作火藥庫的灌水方式。

我獨立以 `r2-author-delta.json` 對六個異動檔的逐行 before/after 與行號反向重放：每檔現值 SHA 與 delta 的 `after_sha256` 相同，逐行回復後 SHA 與 R1 凍結的 `before_sha256` 相同。六檔共 25 個替換行，無其他創作稿變動。R1 已逐一核過 107 句、95 個插圖提示與 9 張卡；本輪重核兩句異動旁白及七個相應證據列、六個異動提示詞，並確認新旁白與 `script.md`、新提示詞與 `claims.md` 逐字一致。`curio-s61` lint 為 **0 errors、0 warnings**、107 句、估時 10.293 分鐘。

| R2 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `91ff577923a5cac28728b3c67b86ab52e9d9b628afe435f5be7d43b74c57426d` |
| `research.md` | `a012983fabf32d076941412c791f650e84a8c5f9b96b8554aa3fdce913799c9c` |
| `video.json` | `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134` |
| `script.md` | `1f55c9182b1aac974cecea31d7755b1c310da29db651a6993aa310da9bb63fc9` |
| `claims.md` | `5087fd10009f997c135f420c2c09ba0ebd3a59ea996296f0ac31aa15006c681f` |

下一關為**兩位隔離盲讀者**與正式合併；在敘事與媒體關卡通過前，沒有語音、原圖、配樂、動畫、成片或可點 YouTube 連結的驗收結論。
