# S51 R14｜獨立史料、主張與書面畫面覆核：PASS

2026-10-20 UTC。覆核對象為 [R14 作者凍結](r14-author-freeze.md)的精確五檔；我沒有修改劇本、主張或分鏡，也沒有呼叫政策、語音或生圖服務。判定：**史料 PASS、逐句主張 PASS、書面畫面 PASS**。本結果不代替新版雙人盲讀、網站劇本卡、政策、實際語音或生成圖驗收。

| 檔案 | 本次獨立 SHA-256 |
| --- | --- |
| `brief.md` | `5afa1ef9ac8e7f5651f92b2e813b3048c7b2f3f9a1a166310a0931db77829861` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `bc54c5376800e85a2bd58957d868789797b0b2b9b09c31da9b2b9ed198d5c107` |
| `script.md` | `d8d8a8c726a4849bb2320af9556a63b32e40f99076adc42f1833f481de2e8fbf` |
| `video.json` | `89723189c5b17fc0d28670e273a8de8557b4300c40327f13b867acb77a69faf5` |

三份固定原文的本機完整位元組與 `research.md` 相符：[G 1912 英國調查](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt) `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`、[B Beesley](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt) `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`、[A Gracie](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt) `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。R14 `research.md` 沒有變更；前版對其他敘事句與畫面提示詞的 [R13 獨立覆核](r13-source-independent.md)仍可作差分背景，不能當新版劇本總審查的替身。

`cal126` 現說「所以船長的目測，不能當成精準的實測距離。」G [L3509–3523](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3509-L3523)列船方位置所推的約 19 英里，G [L3539–3543](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3539-L3543)把約 5 英里明歸 Lord 的估計，調查又認為可能更遠、最多約 8–10 英里。當前 `cal122–126` 保留這些數值與歸屬，結句只區分**目測**與精準**實測**，沒有拿單一估值當確定船距。`claims.md` 的 `cal126` 同字且錨到研究 R12。該景書面提示詞只讓匿名史料員留一條未完成的距離尺；沒有偽造精確刻度、兩船定點或 1912 年現場畫面，故畫面設計 PASS，生成圖仍要另看。

`cal999c` 現說「想繼續從原文查明歷史疑問，歡迎訂閱。」這是頻道邀請，不新增歷史事實，也不提贊助商、商品或特定下集；主張表明確把它列作非史實口播。它沿用 `outro`，未新增插圖。可見的訂閱 CTA 仍為「訂閱奇聞檔案局」，片尾雙推薦框、頻道 URL、三份固定來源連結及濃縮開場後片頭的配置仍在；**是否通過本站業配分類必須以 R14 新請求決定**，不能由本史料覆核推定。

獨立解析核得 `video.json` **132** 句、**132** 個唯一 ID；與 `claims.md` 按 ID、順序及旁白文字 **132/132 同字**，`screenplay(doc)` 與 `script.md` 逐位元相同。**129** 個 `shot`、1 個 `outro`、**16** 組伏筆；`lint --slug curio-s51 --json` **0 errors、0 warnings**，`git diff --check` 通過。作者的正文快估約 8:31，實際聲音須另驗至少 8 分鐘。

下一關為兩名新讀者只讀當前 `script.md` 的 13 題盲評、正式合併，再對 R14 精確雜湊重新執行政策與網站劇本關卡。之前 R10 的音檔與 R13 的政策失敗回條都不能當成本版音質或政策結果。
