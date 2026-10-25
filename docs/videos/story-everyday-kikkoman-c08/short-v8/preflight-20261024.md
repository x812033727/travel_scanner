# C08 short-v8｜非付費 canonical 轉換收據

日期：2026-10-24。站主在本次任務核准**精確 36 句旁白與 36 列配鏡方向**，不是核准製作費、短片時長豁免、匯入、上傳或發布。歷史候選頁首的 HOLD 是核准前狀態；本收據把稿件與畫面方向核准和媒體製作關卡分開。

| 凍結輸入 | SHA-256 |
| --- | --- |
| `../reviews/v8-short-narration-candidate-20261024.md` | `040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69` |
| `../reviews/v8-short-visual-plan-candidate-20261024.md` | `0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241` |

`build.mjs` 逐位元組核對兩個 SHA，36 個 ID 同序一對一，六章分別 6／6／6／5／7／6 句，30 個插圖鏡與 6 張後製卡。它把核准的 text、shot prompt 與 camera 原樣投影到 `video.json`，把全部逐鏡方向保存在 `visual-plan.json`，並只從原件投影 `script.md`／`claims.md`。同一指令重跑後三份輸出雜湊不變：`video.json` `D6BCD8C818B961FBD2DA97ACE8A475372DCE1A3427D4A4D919158B916B126DA3`、`visual-plan.json` `3BEBC4AFE361375B5AB3499E20BB63A832FA6BFC703B97D126F508733B695960`、`script.md` `CB220146D7C67D2FF1B4A09BBEF849972BA3806ED06F6E1F07141192321C4CDB`。

已核對原 84 句專案原件未動：`../script.md` `B9E4C547FFA190609B433D48FF7E27A94B9C9DF4322AEB48104A3163694B3376`、`../visual-plan.md` `776F26F2E15477D443C6D8CFAC0EF32440DCBE5EFA85CA022FEDE7F883A84785`、`../video.json` `57371891A62B0B8F4E6DDBD9E5FFEA196DADE2EF3D92B5F4BC17C319DD0805B2`。既有 `../reviews/v8-short-independent-review-20261024.md` 判定來源 36／36 與畫面 36／36 PASS，兩位盲讀無共同必要題否決；`verify-1.md` 只把該既有判定接到 QA，不冒充新查核。

## 非付費預檢

- `validateVideo`：0 schema errors；`factsChecks`：`verify-1.md marks no claim NOT FOUND`；`storyCuteVisualProblems`：0 errors；場景／台詞 36／36、30 shot、6 card、6 chapter。
- `node --test tools/video/core/schema.test.mjs tools/video/core/lint.test.mjs tools/video/qa/facts.test.mjs`：67／67 PASS。
- `npm run check:tasks`：exit 0，2129 票驗證；其他舊票的警告保持可見。
- `npm run test:docs-videos`：235／236 PASS、exit 1；唯一失敗是未修改的 `docs/videos/imported-long-languages/runner.test.mjs:679` 在 Windows 執行 `package-runtime.mjs` 子行程時以 `3221226505` 退出，stdout／stderr 為空。針對同一測項單獨重跑仍以相同代碼失敗；本輪沒有改該測項或其目標。這是本機完整 docs-videos gate 的剩餘失敗，不能說整套 PASS。
- `node tools/video/cli.mjs lint --file docs/videos/story-everyday-kikkoman-c08/short-v8/video.json`：**exit 1；3 errors、5 warnings**。錯誤是 `MoMA` 未經獨立念法核准、`target_minutes` 4 分鐘低於共用 8 分鐘下限、紙上約 4.6 分鐘正文低於同一下限。警告包括一鏡未明示景別、重複的 adult/table/bottle 提示詞、`v7n07` 約 10.4 秒；配鏡是核准原文，未暗改消警告。這不是 lint PASS。

## 專案路由與 HOLD

`--file` 才會讀 nested `short-v8/video.json`。現行 `--slug story-everyday-kikkoman-c08` 仍讀原 84 句專案（目前因 `c080611` 片尾衝突 exit 1）；`--slug story-everyday-kikkoman-c08-short-v8` 尚無頂層專案。因此本包是可審閱的待推進候選，不是 worker 可執行的正式專案。`README.md` 列明將來的整包推進、同 slug 工作目錄及獨立後台 `stories.json` 匯入確認。

本次沒有 TTS、MiniMax、Jev、配樂、圖片、媒體或後台寫入。v8 紙上純念字 236.64 秒、正文約 273.97 秒、片頭片尾後約 299.97 秒，皆非實測；30／36 插圖是按鏡數，非按正文秒數。`v7e03` 的平面瓶嘴功能圖仍須後製，不以 `stats` 文字預覽代替。C08 整支報價、供應商費用讀回、站主付費上限、實際 TTS／聲音驗收、短版專用時長路由、插圖秒數至少 70%、成片驗收、匯入與上傳均未通過。

本包縮短後的 YouTube 標題、描述、series logline 及沿用的縮圖文字只是待審 metadata；站主精確核准只綁定旁白與逐鏡方向，不能把本包 metadata 當成已核准可上傳。
