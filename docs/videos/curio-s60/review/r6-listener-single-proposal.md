# S60 R6｜最後一輪措辭修訂的單句提案

2026-10-22 UTC。**只提案，未套用、未重錄。**這是既有 listener 措辭重寫的第 **2／2 輪**；R5 新措辭已用完一張加兩次重錄後，當前只剩 `s60061` 旗標。本票不重設重錄次數或措辭輪數，不宣稱聽過原音或把 Jev 旗標覆寫成通過。

| ID | 原句 | 候選（唯一一案） |
| --- | --- | --- |
| `s60061` | 十二月十六日，走在新路最前面的，是布亞蘭德。 | **十二月十六日，布亞蘭德走在隊伍最前頭帶路。** |

當前 Jev heard 為「十二月十六日，走在行路最前面的是布亞蘭德。」（`noul=0.06`），把「新路」轉寫為「行路」。候選直接講隊伍最前頭帶路，不再依賴「新／行」相近音節；日期「十二月十六日」與專名「布亞蘭德」完全不變。原句要表達的是他領先隊伍走這段路，並非一條另有名稱或已鋪設的「新路」；候選不刪掉路線領先者的事實，也不新增結果、距離或方向精度。

重開固定 Amundsen 原文 `/tmp/s60-verify-amundsen-4229.txt`（SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`），與 claims 目前 [P07 L12988–13061](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12988-L13061)同一固定 commit。L12988 記 `December 16` 與 `Bjaaland`，L12990–12991 說他獲派 `leading the expedition forward to the Pole itself`；L12996–12998 列 Hassel、Hanssen、Wisting、Amundsen 依序在其後。這直接支持他在隊伍最前頭帶路；沒有將推定子午線說成精確踏過地理極點。

提案快照：video SHA-256 `d84448550acee292a3657c218fb0d3ef5227d3aca7cf9681974e57bbfa0c961e`，script `47d0dacbfbdb09a72007feba838eaa3ecdaa87248258932ecc3c9dbf4f5ca75a`，claims `698be5b5deba5ba96a9b7f3b398a6f75b8d3c341596e121086506ddd28b1d8fd`；旗標檔 `6c0f073ae28f67c2bd1bbdc521185508339dcfc62d8231c10da072838480217c`，check 檔 `f77fc90b76f52bd5d898108e4654ec5e131e0cb817d85a66da23048014d60c79`。這些雜湊僅用於綁定讀到的材料，不是劇本或聲音核准。

協調者若採用，只改此句並同步 claims／script，取得新來源差分覆核及敘事盲讀、lint，然後在目前第 2／2 輪內只重錄此 ID、跑 check-audio。仍有旗標就保留給音訊審核，不能以另開 R7 重新取得更多措辭輪數。本工作只新增此提案檔；無 video/script/claims、媒體或 Git 操作。
