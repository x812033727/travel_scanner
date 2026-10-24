# S38 R8q｜PF009–014 提示詞獨立書面覆核

2026-10-22 UTC。**PASS，可在整集 US$4.58 上限內各畫一次 PF009–014 並逐張原圖驗收。**這只核准六景的付費測試，不是原生圖 KEEP、全片分鏡或音訊核准。我沒有參與 R8q 作者改稿。

我直接讀了固定 Pepys 日記 `/tmp/curio-s38-pepys-4200.txt`，SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，L65795–65819。原文依序是約凌晨三時 Jane 叫醒、佩皮斯穿睡袍望窗外、覺得遠而回床睡；約七時起身穿衣再望窗、覺得火更小更遠；Jane **聽說**三百多屋焚燒，他立即準備去塔上親看；塔上看到橋邊房屋火，當時只為 Michell 等人**擔心**，搭船後才見 Michell 家燒毀。R8q PF009–014 的單景提示詞按此順序呈現。木床、深色雙面呢衣、石塔平台、舊橋拱是 1660 年代畫面示意，不宣稱日記逐一記錄；沒有把轉述畫成文書、把擔心畫成已確認失屋、或讓現代吊橋再入鏡。

我獨立讀取 [R8q 逐字差分](verify-49-r8q-six-prompt-structured-diff.json)，核對 `scenes[8]`–`scenes[13]` 恰為 PF009–014 的六個 `data.prompt`。現行整檔 SHA-256 `087ae9c4cdbb8dea3430cd505d42624e06deca0a94b77e71c49164fbbcc2f4db`；逐字反向取代六字串還原 R8p SHA-256 `8db80e07bffff8863f949e4a458b9fed0a891e36ed93063bce59c3915fc6e142`。`claims.md`／`research.md`／`script.md` 的 SHA-256 仍各為 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`／`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`／`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。已收 PF001–005、PF008 的 manifest entry 與所選圖片 SHA 和批前私有備份逐項相同。

`lint --json` 為 0 errors／0 warnings，112 句；六景 `--takes 1 --dry-run` 回報 MiniMax `image-01` ready、約 US$0.08。私有帳本在付款前 US$0.4615／29 images／28 judges／1 music，另有 US$0.0035 舊預約，`STOP` 在位；距 US$4.58 上限有餘。新 prompt 雖降低已見的孩童、文書、現代橋錯誤，不能憑文字預判生成會合格。只用 EXIT trap 暫時移除 STOP，對六個 ID 各一次；直接看每張未裁切原圖，出現三張同類成人／年代問題時停止後續付費，記帳與圖單，最後恢復 STOP。其他尚未畫的 PF015–022 保持停止。
