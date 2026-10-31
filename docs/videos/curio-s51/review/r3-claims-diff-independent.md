# S51 R3｜`cal061` 主張錨點獨立差分覆核

2026-10-20 UTC。**PASS：R3 來源包的唯一窄 HOLD 已解除。**我沒有參與 R3 作者修稿或這次錨點修補；依 [R3 獨立原文與書面畫面報告](r3-source-independent.md)所列的缺口，重讀固定 1912 年英國調查報告和研究表 R05／R07，並對目前檔案重算差分與雜湊。此裁決僅補上 `cal061` 主張表來源，不是敘事雙盲、實際圖像、音訊、站台或成片核准。

固定調查電子轉錄 `/tmp/s51-independent-sources/british-report.txt` SHA-256 `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`，與 [固定 G commit](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt) 和 `research.md` 所釘位元組一致。G [L3192–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3192-L3197) 說加州人號唯一無線電員睡著，沒有收到鐵達尼號電文，對應 R05；G [L3420–3442](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3442) 明列二副 Stone 與實習生 Gibson 在值班時觀察船燈，後來看到白色火箭，對應 R07。`cal061` 的「可是船橋還有人值班，夜空裡快出現另一種信號」因而可由 **R05、R07 合併**支撐；沒有把 Stone 報告或 Lord 的記憶衝突寫成定論。

我把目前 `claims.md` 的 `cal061` 一列反向換回舊 `[研究 R05]`，重算 SHA-256 正好是 R3 獨立報告釘定的舊值 `d711c1f0279e8fa7a2cf1d29683b0ba1540767fc4b5d5bfe8a8cbe179add111b`；新 `[研究 R05、R07]` 只出現於該列一次。這證明這次 `claims.md` 的位元組差分**只有該錨點**。`script.md`、`video.json`、`brief.md`、`research.md` 的雜湊均與 R3 凍結相同。

| 現行檔 | SHA-256 |
| --- | --- |
| `brief.md` | `82a2e4a3d7a240dd0f249eeeec3b3dffdf1446d9eb049432320e72fe6b6a1023` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md`（錨點修後） | `20ffe5c07e4210a248f0ea6daa9c3ab6131165df64f75ee79fafca68f620a8c6` |
| `script.md`（R3 不變） | `734cf4d7c474cd24a7dba87db738d07575654cbbd4ec84ad7006a7ff4b795a40` |
| `video.json`（R3 不變） | `70aa784c4f6175e557e3addd6550e2c0068047bac85e0a3a9690a81b1b855226` |

`lint --slug curio-s51 --json` 為 0 errors／0 warnings、140 lines，`git diff --check` 通過。R3 劇本的讀者曾共同指出章節銜接、問題回收及重述問題，**敘事仍 FAIL**；來源包這一格 PASS 不放行 TTS、付費圖或成片。下一步由作者修敘事，再對新版劇本重做來源與 script-only 雙盲。
