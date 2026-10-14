# H05 v2｜`open-note` 原生示意卡窄修與離線審查

**後續關卡更新：**這份文件以下記錄改卡當下的離線候選與舊音訊。其後盲審要求兩句答案明示回扣；窄修已 11/11 通過並只重錄那兩句，正式時間軸和音訊檢查完成、新版後台核准仍待站主。以 [敘事回扣與正式語音](narrative-payoff-repair-20261014.md)及 [NOTES.md](NOTES.md) 頂端的現行雜湊為準。

日期：2026-10-14。這是候選畫面的**離線預檢**，不是完成圖組、後台音訊重新核准或成片驗收。唯一已付費的 MiniMax `open-note` 小樣因巨紙、多張可辨人臉與未要求的墨鏡人物遭人工退件；原圖、原始判圖與 US$0.0135 單次費用仍保留在 [visual-pilot-04.md](visual-pilot-04.md) 記載的外部封存目錄，沒有手改 `keyframes/manifest.json` 的 `passed=true`，也沒有再買圖或語音。

## 修訂範圍與來源

只把 `video.json` 的 `open-note` 由 `shot` 改為 `diagram`，資料改指向 [note-handoff.svg](diagrams/note-handoff.svg)；SVG SHA-256 `00480750d7ff7fc81981eb9405ecbaee25ad7af0d176b8067999fe025228fcb1`。場景 ID、順序、主張 `c04` 及 `h5v005` 旁白「起飛後，他把一張紙條遞給空服員。」沒有改。`c04` 的本地 [claims.md](claims.md) 與獨立 [verify-1.md](verify-1.md) 已把「男子把威脅紙條交給空服員」綁到 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)。圖只畫座位、空白小紙片及指向空服員的箭頭；旁註與右下角明示「非當年原件」，不重建紙張尺寸、筆跡、現場或人物外貌。圖中沒有宣稱炸彈真實存在。

| 項目 | 修訂前封存 | 修訂後候選 |
| --- | --- | --- |
| `video.json` SHA-256 | `74102087ca465c7c73044e1182671641965cc19cbd6f4d0470d11fcb9c16e6e3` | `c14695ef580539006621e24e1f3f25e0d9ffcb2ba399eea9fdd7d69aa2edbd1f` |
| narrative hash | `65c64491d8a53b77` | `e900e3c896cee888` |
| speech hash | `7d8cb6cb30ba87d9` | `7d8cb6cb30ba87d9` |
| look hash | `38b9efa0cb47553f` | `38b9efa0cb47553f` |
| pictures hash | `6b3167e632a73379` | `e3b9064c5fd3c46f` |
| visual hash | `c1c0fd1159f2c572` | `e9dce56adf6a594f` |

由 CLI 重生的 [script.md](script.md) SHA-256 `255e31bf6a2600dca805201ff6b224dbc54969bd77528cd575d67db3a3e2e821`，只更新第 5 景版型標記和尾端 narrative hash；逐句文字未改。`script --slug curio-h05-v2` 成功；`lint --slug curio-h05-v2 --json` 為 **0 errors、0 warnings**，93 景、108 句、六章。

## 現有 WAV 樣本的時間軸 dry-run

離線程式 `<home>/mokaair-work/videos/curio-h05-v2/_tools/note-diagram-preflight-20261014.mjs` 讀封存舊版、現稿及原 `timeline.json` 中 108 句的 `audio_samples`，使用現行 `buildTimeline` 重建候選時間軸。它逐項斷言場景 ID／順序、所有 line ID、文字、情緒、停頓與 reveal 一致；只有 `open-note` 內容不同。原正式時間軸 SHA-256 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984` **未寫入**。候選 `timeline-dry-run.json` SHA-256 `6ec8c8defa6c25b22f009e6184d89739144f3c2af8ac557c929862ba23d2c8ee`；`report.json` SHA-256 `2f2cd0a6e4e50658d5506ce7afecfb98411df99feeede91fb9438241571b0f83`。

| 指標 | 舊版 | 新版 dry-run |
| --- | ---: | ---: |
| 總長 | 16,073 格／30 fps，535.767 秒 | 相同 |
| `open-note` | 第 585–699 格，114 格／3.8 秒，1 個狀態 | 相同 |
| `shot` 景數 | 62 | 61 |
| 插圖格數 | 9,556 | 9,442 |
| 插圖時間占比 | 59.45% | **58.74%**，高於 50% |
| 狀態數／平均／最長 | 108／5.0 秒／7.3 秒 | 相同 |
| 節奏與章節問題 | 0／0 | **0／0** |

這是使用**原始音檔實際樣本數**的候選時間軸檢查，並未重建或核准正式 `timeline.json`。旁白 WAV SHA-256 仍為 `8b519d908e7b85d7d214288d3bf8c7ebb5bc897456a4b32c74143cff50253ba3`。已核准音訊卡綁的是舊時間軸；因場景版型與 hash 已變，必須在正式時間軸重建後重新跑所需敘事／音訊關卡，由主製作流程處理。`speechHash` 相同只代表不需重新合成逐句音檔。

## 隔離渲染、字幕與待審點

在 `<home>/mokaair-work/videos/_offline-h05-note-diagram-20261014/curio-h05-v2/` 用本機 `render --file ... --workdir ... --channel msedge` 重畫 1 個狀態，沿用 46 個本機原生卡／照片快取，**0 個版面錯誤**。只在隔離的 `video.json` 副本移除未有合格圖的縮圖 `boy-bank` 引用，正式主稿縮圖沒有變。`frames/583fcb0c1347195b.png` SHA-256 `0e21f242cb96f1e018fe3af209e55cab7cab8c6e112ebd8d796765406d41877b`；`frames/manifest.json` SHA-256 `7c1043b42eca749d2eda7ec9e6c2c0421110d88a95a92217c3d1c559813540ae`；`contact-sheet.png` SHA-256 `ac684fa280096213d294e44af0f4532eadddd056b4f28aa1ef28c652f01ffeb2`。人工打開完整 PNG，標題、動作箭頭、紙條、來源界線及「非當年原件」都可見；尚須獨立畫面審查。

用候選時間軸另外重算繁中正文 CC：108/108 cues、0 缺句、0 讀速／寬度／重疊問題。隔離收據在 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/caption-body-note-diagram-preflight-20261014/`，`receipt.json` SHA-256 `32b77c84e4590a0728cda7b6156985d40403bfe15a29b6ef6a208313dcfe26f1`；SRT `b4d584b70568d201d842ad5a45d4262993b41a7bafa5b06a22e7662ab9262de2`、VTT `d70d6c531f4fe277829f955399270c7bb4803d71d743867ae581423b4e90e7dc`，兩份位元內容與舊版相同。這只是正文時間預檢，品牌片段與成片仍缺；正式字幕須在 assemble 後產出並開播放器驗證遮擋。

目前 `keyframes/` 的退件 JPEG 與舊 `manifest.json` 只是歷史收據，不能轉成新版 `diagram` 的圖組核准。其他 61 個 `shot` 仍缺可用的全組畫面及連續三鏡實速審查；縮圖 `boy-bank` 仍無可用圖；正式 render、assemble、字幕、QA、上傳包、播放及站主驗收都未完成。**不擴批、不把此候選卡稱作正片完成。**
