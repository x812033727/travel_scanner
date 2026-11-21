# S38 R8h｜`pf004` 年齡與肖像暗示再窄修

2026-10-21 00:23 UTC。**作者凍結，待獨立紙上覆核；沒有新圖、沒有新支出，私有 `STOP` 保留。**R8g 在第一次 R8f 原生退圖後提出「middle-aged」「short beard and receding hairline」；協調者的獨立紙上檢查指出，1666 年的佩皮斯是在三十多歲，`middle-aged` 會引導過老形象，鬍鬚和髮際也不是固定日記 D4b／D5 支持的相貌。R8g 因此**未進入付費重試**，本輪僅修改它的 `pf004` 一個提示詞葉節點。

## R8h 文字與來源界線

> Wide establishing view from a walled London garden in 1666, one adult English householder in his thirties with mature facial features and a plain knee-length coat appears head to toe as a small figure on the left, pointing over the wall toward a distant orange fire glow beyond narrow gabled rooftops; an intact brick house stands beside the garden under a soft overcast sky

一人、指向遠火的一個動作、全身小人物與寬景仍在；不指定鬍鬚、髮際、可辨識肖像，也不把 `cartoon`、`vector`、色盤或 judge 的風格修詞加入單景。這是 [D4b](research.md)花園憂火與 [D5](research.md)隔日才確認自宅仍在的**概念插圖**，不是史料證明的本人外貌、窗景、屋舍位置或當日天氣。「in his thirties」是避免把人物畫成年老者的年齡帶，仍須靠原生圖核對是否看得出成年人；畫成幼童或火已進花園就要退圖。R8f 原生首試的失敗和 1 take 計數見[停點收據](verify-16-r8f-native-stop.md)。

## 凍結及逐葉差分

| 創作檔 | R8h SHA-256 | 與 R8g 相比 |
| --- | --- | --- |
| `brief.md` | `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b` | 未改 |
| `research.md` | `f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe` | 未改 |
| `claims.md` | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` | 未改 |
| `script.md` | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` | 未改；不重錄 |
| `video.json` | `7e9eb1a2019bbf55727ac08c1bf273fc2fbf420223c6425083558afbfb9b0631` | 只改 `scenes[3].data.prompt` |

[完整前後字串差分](verify-18-r8h-structured-diff.json) SHA-256 `30d31f5d5f44ff4703e6e64f8ace0409308400d746950e7e44fbce40f9c1edc7`；由現行檔把單一新字串換回 R8g 舊字串，原始位元組 SHA-256 精確還原為 `dbd6a5c262674507e7e58097a436f2ff470fab89e21589ef5b83056b4742b2dd`，其他解析 JSON 葉節點全同。`visualHash` 由 R8g `a35aa792399bcd5c` 變成 R8h `1f353c19c4d07f47`；原 manifest 仍屬 R8f `9dce146d046f75cf`，不能作新版分鏡核准。`lint --slug curio-s38 --json` 實測 0 error／0 warning。

## 下一關仍為 HOLD

私有 `STOP` 在 `/workspace/.video-work/curio-s38/STOP`；帳本仍是 **US$0.2355**，含舊 `pf003` **US$0.0035 reserved**，整集硬上限仍 **US$4.58**。R8h 先給未撰詞者獨立核對單葉差分、D4b／D5、年齡與視覺規格；紙上 PASS 之後，`pf004` 只剩**一次**已界定的 1 take＋1 judge 原生重試。若再退圖，維持 STOP，不續買 `pf005/006` 或後續景。三景都要原生圖 KEEP、另解 `pf003` 預約及新版分鏡關卡，才可考慮解停。網站音訊／分鏡卡仍待站主，本機委派紀錄不能寫成站主親看、親聽。
