# S53 R20｜兩景一次原生試畫與停批

2026-10-22 UTC。**本批結束：`s53010`、`s53018` 兩張原圖均人工 REJECT；不再以 R20 提示詞重畫。**試畫綁 `video.json` SHA-256 `f868ce55f98f7868a8052098d0f6439344585df9e0fa1d0cb32eb0ddbbac21dd` 與[非作者紙審](r20-two-prompt-independent-paper.md)。每景使用 `--shot <ID> --takes 1` 單獨呼叫；每次都由 EXIT trap 恢復 `STOP`，沒有背景未完成的付費命令。原圖與工具所選裁圖皆為 1280×720 JPEG，已逐張直接開原尺寸檢查；[雜湊及判定清單](r20-two-native-inventory.json)列出每份原圖、選圖、request key、機器評分與人工結論。

| 景 | 機器結果 | 原尺寸人工判定 |
| --- | --- | --- |
| `s53010` | **9/10 FAIL**；style 為寫實 graphic novel，背景為長街與電線桿，未得到近景庭院。 | **REJECT。**成人臉和連排街屋比系列 chibi 插畫寫實，畫面中央長街及多根電線桿佔大半幅，違背 R20 特意避免長街與現代感的提示詞。沒有明顯汽車，卻仍不符合系列造型與構圖。R19、R20 已各有一張失敗原圖；若作者再修，只剩一張第三／最後原生嘗試，失敗即改用同章合格圖或有來源註明的卡片。 |
| `s53018` | **9.29/10 PASS**，judge 只把背景建築當次要細節。 | **REJECT。**畫面最上方橫跨整幅的是可辨識的現代高樓天際線，與 1906 年舊金山營地不合；帳棚中間留出寬直大道，沒畫出南公園「空間不足」的窄地。灰髮 chibi 工作者與帳棚本身可辨，但這兩個實質畫面錯誤不能由機器分數抹去。R19 供應商曾拒絕輸入而沒有原圖，本張是此景首張實際原生圖。 |

帳本從 **US$0.4050／31 images／30 judge／0 預約**增至 **US$0.4320／33 images／32 judge／0 預約**，新增 US$0.0270，低於整集 US$4.78 上限。後帳本 SHA-256 `c385ac8815a3ef7e3fa500c79dd1039ee6b9f21fc94bafc2c0c0deebd52c435b`；後 manifest SHA-256 `75c59a8855284a3defe6f2acfd4f0c30bb52f344e1756bc29ef573cadfb5f1b7`。首章八張和 R19 六張共 **14 張 KEEP** 的完整 manifest 條目、request key、選圖路徑及實際檔案 SHA 均與試畫前逐一相同。`media/jobs.json` 空、`STOP` 已恢復，付費 MiniMax 端點已釋出。

兩次 CLI 均 exit 1，因 `s53010` 仍使整份 manifest `needs_review`；`s53018` 的機器 PASS 只是該景局部狀態，人工已退件。Playwright Chromium 版本不符令聯絡表未重生，本回條依逐張完整 JPEG 與裁圖人工驗收。下一步由作者窄修這兩景的提示詞與 claims 對應畫面欄，另一位非作者重新紙審後才可定點試畫；其餘章節、站台 storyboard 卡、人耳音訊與成片仍待。
