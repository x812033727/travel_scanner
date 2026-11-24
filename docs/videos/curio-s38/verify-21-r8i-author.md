# S38 R8i｜`pf006` 退圖後單一提示詞修訂

2026-10-21 00:29 UTC。**作者凍結，待未撰詞者做精確差分與史料／畫面紙上覆核；沒有新的付費圖片，整集 STOP 保留。**本次只改 `pf006` 的 `data.prompt`，沒有改旁白、劇本、來源、已通過的 `pf004/005`、畫風、片頭片尾或網站核准。

## 退圖與修詞理由

[R8h 原生圖停點](verify-20-r8h-three-shot-native.md)的 `pf006` 新圖 `a87978e35d8cfb9355ca75969aca21a5082f701da2887dc3503a36471320a78f`（私有保留同 SHA）仍是童貌女僕坐在室內，窗外像近火；機器 judge 8.41／10 判 3D 感、主體動作錯、黑邊與側面不足。它不是合格圖。舊提示詞雖寫 adult 與 `leans out`，鏡位從室內窗邊仍讓模型把人物放在室內；這輪改成**街外視角**，以敞開的上層窗戶、成人比例及上半身探窗寫明可見動作，讓火只成為遠方低屋頂後的一點光。

新版完整提示詞：

> Exterior medium-wide view from a narrow London lane before dawn in 1666. An upper-floor wooden casement stands open in a red-brick house; one clearly adult household maid with mature facial features, in a plain linen coif and dark wool gown, leans her upper body through the window and faces in side profile toward a small orange glow beyond distant low gabled rooftops

此為 [D2a](research.md)「女僕 Jane 叫醒佩皮斯看火、他以為火遠」的**概念插畫**，不是日記所證實的 Jane 年齡、臉、衣服、確切窗口或屋舍。只一名主要人物、一個探窗看遠火的連續動作；沒有在單景提示詞加入 `cartoon`、`vector`、色盤或任何畫風／負面指令。下一張若仍是童貌、室內坐姿、貼窗大火、現代建築、3D 感或黑邊，必須原生 REJECT，不因機器總分而放行。

## 凍結與付款界線

[機器可讀精確差分](verify-21-r8i-structured-diff.json) SHA-256 **`7dc90011ba627af6916cdd07625b4f6bd172ee768c4d5022042bf7905928af81`**。我用新檔把唯一新提示詞逐字換回 R8h 舊字串，完整原始位元組 SHA 回到 **`7e9eb1a2019bbf55727ac08c1bf273fc2fbf420223c6425083558afbfb9b0631`**；解析後只一處葉節點 `scenes[5].data.prompt` 不同。R8i `video.json` SHA-256 **`de27c08f77dd91e66703fcf5c875ee1ea787d34246b93bc6237af8c7fcd03861`**，`visualHash` **`79b6a9303fdfaeba`**；`brief.md`、`research.md`、`claims.md`、`script.md` 分別仍是 `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。Lint 實測 0 error／0 warning；聲音無須重錄。

私有 `STOP` 仍在，ledger **US$0.2760**（16 image、14 judge、1 music），含舊 `pf003` **US$0.0035 reserved**；整集硬上限仍是 **US$4.58**。目前 manifest 的 `visual_hash` 屬 R8h，並非 R8i 整體分鏡通過；`pf004/005` 的圖片只是若 request key／judge stamp 在新版逐景核對不變，才具備沿用條件。未撰詞者紙上 PASS 後，`pf006` 也只剩**一次 1 take + 1 judge** 試畫；若再退圖，保留 STOP，不能擴大購買。
