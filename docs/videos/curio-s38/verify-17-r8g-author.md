# S38 R8g｜`pf004` 退圖後的單景提示詞窄修

2026-10-21 00:21 UTC。**作者凍結，待另一位讀者做精確差分與紙上來源／畫面覆核；原生新圖、整體分鏡和成片仍 HOLD。**本次只改 `pf004` 的一個 `data.prompt`。未刪 `STOP`、未呼叫付費圖片或 judge，也未更動旁白、劇本、畫風或網站核准。

## 退圖依據與新提示詞

[R8f 首次付費試圖](verify-16-r8f-native-stop.md)的 `pf004-1.jpg` SHA-256 為 `153d7687e6f0c0d8074d720e3ced300115025f26918e4af6a195611f313d1070`；原始工具輸出 SHA-256 `1937d4925ef9b482f9a90b0d9c4a92c6ff03930a2be7d6ce3f9842067b22015b`。我直接看過原生 1280×720 圖：人像明顯童貌且佔大半幅；火在花園或近屋前景，房屋像較晚期住宅。機器 judge 9／10，因中景而非寬景、背景照片式模糊而判退。這張圖沒有通過實際畫面驗收，不能因分數高就採用。

R8g `pf004` 完整提示詞：

> Wide establishing view from a walled London garden in 1666, one middle-aged English householder with a short beard and receding hairline, wearing a plain knee-length coat, appears head to toe as a small figure on the left and points over the wall toward a distant orange fire glow beyond narrow gabled rooftops; an intact brick house stands beside the garden under a soft overcast sky

此改法把成年人辨識線索放在人物前、以「head to toe as a small figure」限定全身寬景，並把遠火改成屋頂後方的橙色光，不要求在單景寫 `cartoon`、`vector`、色盤或任何 `look` 變更。它仍可能生成童貌或錯誤時代建築，必須以**下一張原生圖**驗收；judge 的風格修詞未直接塞入單景。日記 [D4b](research.md)記 9 月 4 日他在花園憂心辦公室和看火，[D5](research.md)到 9 月 5 日才確認自宅仍在；本景是 `pf004`「火最後有沒有燒到他的房子？」的開場疑問示意，**不聲稱史料驗證了真人相貌、花園與住屋的視線／相對位置或當日天氣**。新圖如顯示火已燒到院內，仍要退件。

## 固定版與差分

| 檔案 | R8g SHA-256 | 本輪 |
| --- | --- | --- |
| `brief.md` | `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b` | 未改 |
| `research.md` | `f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe` | 未改 |
| `claims.md` | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` | 未改 |
| `script.md` | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` | 未改；不重錄 |
| `video.json` | `dbd6a5c262674507e7e58097a436f2ff470fab89e21589ef5b83056b4742b2dd` | 只改 `scenes[3].data.prompt` |

[機器可讀前後完整字串差分](verify-17-r8g-structured-diff.json) SHA-256 `827315ee62173e32ca69f56cec3f96c66d02431e26a864b011a92ff0102d4cbf`。它從 R8f `video.json` 原始位元組還原並核到 SHA-256 `084ff89c7df3dbfc0c150263eec6d96c3dabf85fc1baacd864a7e40f41416616`；只把 `pf004` 新字串換回 R8f 舊字串，整個解析 JSON 即完全相同。`visualHash` 由 R8f `9dce146d046f75cf` 變成 R8g `a35aa792399bcd5c`；`lint --slug curio-s38 --json` 為 0 error／0 warning。原 manifest 仍綁 R8f `9dce146d046f75cf`，不是 R8g 畫面核准；`pf001/002` 是否可沿用，須讓工具按逐景 request key 與 judge stamp 重驗。

## 保留停點

私有 `/workspace/.video-work/curio-s38/STOP` 實測仍在。付費媒體累計 **US$0.2355**（13 張圖、11 次 judge、1 首音樂），含舊 `pf003` **US$0.0035 reserved**；整集硬上限仍為 **US$4.58**。`pf005/006` R8f 新提示詞仍未付費重試。下一位應先對 R8g **精確五檔 SHA、單葉差分、D4b／D5 來源和 Curio 提示詞規格**做獨立紙上覆核；通過後仍只能對 `pf004` 做**一次**新 1 take＋1 judge 原生重試，先核即時額度與帳本。若再退圖，維持 STOP，不能繼續買 `pf005/006` 或後續 100 餘景。即使該景通過，也要三景 3／3 native KEEP、另解 `pf003` 預約和新版分鏡關卡，才能考慮解停。網站音訊／分鏡卡仍待站主；本機委派紀錄不等於站主親自看過或試聽。
