# S62 R14｜剩餘 91 景原尺寸覆核

2026-10-22 UTC。**`s62023` 機器 PASS 但原圖日夜矛盾，已立即設 STOP。**R13 的 `s62018` 三次 image 均 machine FAIL，已改為固定史料來源資訊卡並經[獨立紙審](r14-s62018-source-card-independent-paper.md)通過；舊三張敗圖未洗白或增添第四次。`s62019` 在途快取原圖已由製作方[驗收](r14-s62019-cached-keep.md)，零次新出圖、judge 9.29 PASS。本票從 **`s62020`** 起，只判 R14 新生成原圖與所選裁切。判準只退重大 1610 年代、旁白／主角矛盾或明顯畫風漂移；匿名 chibi、ruff 和普通道具簡化不單獨退件。已固定的來源邊界見 [R8 史料／畫面紙審](r8-independent-source-visual.md)。

R14 開始時 `video.json` SHA-256 `db347370e999f27694850db6ad45931d1aa59886932512893abfdee1c4745180`，`script.md` `bb125a43aa15e2fcbda3f25b7e137d6ae81cb97f5a35973f8702a8774231f766`，`claims.md` `22cc526f6293de6a0fa282bce8ae1ff9f9d06b325498a6d7d198b392010ce8fd`。各行 actual 為該景累計實際 image 嘗試，機器敗圖不算人工 KEEP。

| 景 | actual | 選定原圖 SHA-256 | selected SHA-256 | 獨立判定與具體依據 |
| --- | ---: | --- | --- | --- |
| `s62020` | 1/3 | `2f7f522e12075d5033b47ab99b6b541d46bb4ac25864f9f35d58ceeff5e56386` (`s62020-1.jpg`) | `2aa33fa1739f3cbb56d51aa5d343be71cf98977c005fa4cc3f8d4936e538f635` (`s62020-1-trim.jpg`) | **KEEP。** 早期石陽台、夜空、月亮與細長簡化望遠鏡可示意從月面轉向行星的觀測；原圖與選裁均無現代器件或反向史實。冬帽和 chibi 比例不另退。 |
| `s62021` | 1/3 | `5ac2c95cccedaadba952a66dafee7f0dbfaa30353010f2f91008957992eac1d3` (`s62021-1.jpg`) | `e23be25bca797515b1814f28ad567f8868bfcf6fa3b80714cca312c9222bc3a3` (`s62021-1-trim.jpg`) | **KEEP。** 早期服飾與簡化鏡筒、窗外單個淡光體示意木星引出下一幕細點；大光斑屬卡通指示，不冒稱原始望遠鏡成像或肉眼精確盤面。沒有電子控制件。 |
| `s62022` | 2/3 | `9ee0b11298c27a163adb6c34edb105770d6980cd8c85bf3edb6549b6ef594614` (`s62022-2.jpg`) | `d8229c8eb80a472c1f0ea725b448e0af534552d6bba67bfdde9c0d9d8fdee363` (`s62022-2-trim.jpg`) | **KEEP。** 留鬍成年觀測者正以短光學筒朝暗處星點查看，對應「鏡頭旁細光」疑問；牆上深色凹處無電子邊框、文字或現代控制元件。take1 機器 FAIL 後 take2 補正，選裁保留人物和光點。 |
| `s62023` | 2/3 | `0427216d673232b01b9f9e11e9785fab28c4ab5e27bc1e6ca58a4183cfd77831` (`s62023-1.jpg`); `10e0c81f90a2dbf28023438a0d9088e1a402a5e8199cbc0a71fcd2fe0fcdadfc` (`s62023-2.jpg`) | `10e0c81f90a2dbf28023438a0d9088e1a402a5e8199cbc0a71fcd2fe0fcdadfc` (`s62023-2.jpg`，同原圖) | **REJECT／STOP。** 口播明說「**一月七日晚**，他第一次留意木星兩旁這幾點」，原圖兩次都明亮白晝：take1 明窗日光與庭院，機器因寫實 3D 背景 FAIL；take2 機器 10 PASS，但晴朗日光照著庭院、臉和紙，完全沒有夜空或燭火過渡。這是核心觀測時間矛盾。prompt 本身寫 `pale early light from the courtyard`，須先由作者處理；不能把機器 10 分當原圖史實通過。剩 1 次 actual。 |
| `s62024` | 1/3 | `3182ed90b4a1654486d46fa5e079e5c54fbc9ad3e7711a336e33b0b22c63609b` (`s62024-1.jpg`) | **無 selected**：STOP 前 image ready，尚未 judge／manifest shot | **HOLD，非 KEEP。** 夜色與觀測者吻合；天空有多個相近亮度的點，可能模糊本句「三個又小又亮的光點」的可辨數量。需完成正式 judge 後再依選圖與上下文判定，不能把 ready 當作通過。 |

R14 log 明寫 `stopped by the STOP file after 7 new keyframes`：`s62020`–`s62023` 共 6 次 image 已 judge，`s62024` 1 次 image ready 未 judge。停止時 `media/jobs.json` 為 `{"jobs":{}}`，STOP 在位；總帳 **39 image／38 judge／US$0.5165、零預留**。本輪 **3 KEEP、1 REJECT、1 HOLD**，其餘 **86 個 shot 未出圖**。manifest SHA-256 `140fc91d286e0bc09c5a2ac5208a736e2ebe32d4459f1c0faa17db2564fb2674`；`video.json`、`script.md`、`claims.md` 仍為上列 R14 雜湊。本票只設 STOP 並記原圖，不改提示詞、旁白、manifest 或媒體帳本，亦未呼叫付費工具。
