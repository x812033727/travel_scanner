# B18 來源歸屬旁白候選：獨立複核

**審稿者：`/root/b18_successor_independent_review`；日期：2026-10-17。結論：來源歸屬 P2 已修正；未見 P1；新增 1 項 P2 口播節奏。候選仍 HOLD。** 這份報告只審本候選的 row 與六句變更，不是正式 row review、65 筆逐景 verifier 或完整逐字稿審核；沒有觀看成片或試聽 TTS，也沒有讀取並行中的新版完整逐字稿。

## 固定版本與獨立重算

| 對象 | SHA-256／結果 |
| --- | --- |
| 本候選 `sha256.json` | `7f39a6b95a8233ff4cc32986588c71431886987c75a5d4cd9764c1bf1910753f` |
| 本候選 `B18.json` | `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681` |
| 本候選 canonical story | `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648` |
| 父版 manifest／父版獨立報告 | `03bcf39dbbbeb7c1159154effbe99f645088cc3a6a449b3d0349e62ab6543a9a`／`2d30144e7d2be77d12dbc9ec24b945b1fa75af7a02e8cc19aa4ccd3da97072c5` |

我自行重算 `sha256.json` 列出的 13 個檔案，零個 hash 不符；再跑 `build.mjs --check`，得到 `PASS_OFFLINE_CANDIDATE_HOLD`、85 景、88 句、65 筆 `UNCHECKED`。檢視 [`delta.json`](delta.json) 與父版後，資料層變更限定在 row／系列投影的 `must_verify[3].claim`、`hook` 一句、`idea` 四句、`now` 一句；覆蓋檔只有候選狀態與父版指標變動。六句的有效口播都是 `text`，沒有 `say` 覆寫。65 筆 claim 原文、`source`／`fact` 映射與 verdict 均未變；來源分布仍為 J-Net21 36、機械學會 5、發明協會 19、法院 3、石野 2。

## 六處歸屬與史料

| claim／景 | 新版有效口播的來源歸屬 | 判斷 |
| --- | --- | --- |
| `h5`／`hook-s004` | 「J-Net21 記下，試作輸送帶到了轉角就堵住，盤子掉下來」 | 舊版無歸屬的開場 P2 已補；景是一般插畫 shot，來源現在可聽見。 |
| `i1`／`idea-s024` | 「J-Net21 記載，輸送帶一到轉角就壅塞，盤子跟著掉下來」 | 舊版無歸屬的轉角敘述 P2 已補。 |
| `i5`／`idea-s031` | 「依 J-Net21 的記載，最後用來轉彎的是一片片扇形板」 | 結果仍指向 J-Net21，未把撲克牌／名片合成一個現場。 |
| `i6`／`idea-s032` | 「J-Net21 說，這種板子後來叫『魚鱗板』」 | 板片名稱有明示歸屬。 |
| `i7`／`idea-s033` | 「J-Net21 記載，從工廠參觀到試作機完成，前後約十年」 | 時長有明示歸屬，未改動 1957 年試作的下一句。 |
| `n7`／`now-s098` | 「按 J-Net21 的記載，早期的扇形板片，回答了當年那個彎怎麼過」 | 結尾回扣有明示歸屬。 |

[J-Net21 原文](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)〈町工場の経営者が協力〉直接記錄轉角輸送帶壅塞而掉盤、約十年的開發、扇形部件與「ウロコ」、1957 年試作；新版 row 把這些子句放在「據 J-Net21」之後，沒有添入原文未說的啤酒廠牌。`i3` 的上一景仍完整說出中小企業基盤整備機構，`i4` 本景仍說發明協會；[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)記名片扇形的另一說。兩個靈感版本仍保持互斥、各自歸屬。前次 [P2 審查](../B18-corner-and-source-card-candidate-20261017/INDEPENDENT-ROW-SOURCE-REVIEW.md)列的六處無歸屬均已處理。

row 的法院 [第 579776 號判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)專屬 `h7/t7/t8` 與 1972 年界線未動；1958 年首店雙來源字卡也未動。本報告沒有替這些不變部分重新核准正式 row，新的 canonical hash 仍使舊 `episodes/reviews/B18.json` 失效。

## P2：`i5`、`i6`、`i7` 連續重複同一來源名

`idea-s030` 才說「兩種記載，現在無法判定哪個才是現場；能確定的是」，緊接著 `idea-s031`、`s032`、`s033` 三景連續以「依 J-Net21 的記載」「J-Net21 說」「J-Net21 記載」起頭。三句構成同一個工程解答與時間推進，卻像連讀三條參考書目，打斷這個故事的節拍；前面 `idea-s027` 已說出機構全名，該段來源提示的密度更高。這是**文字層級的口播可行性與敘事問題**，不是史實或來源路由錯誤。

建議只改 `i6`／`i7` 的說法並保留可聽見、指向明確的來源承接，例如在 `i5` 點名 J-Net21 後，讓下一句說「同一篇報導把這種板片叫作……」、再讓時長句以「報導還記載……」承接。實際措辭須由完整逐字稿的獨立聽眾審稿者讀前後段決定，不能只用字面替換自稱已解決。每句仍要符合 `attributed:true` 的[品牌故事規則](../../../../../.agents/skills/youtube-video/references/story.md)。改動六章稿或 row 後，重算相應 hash、更新完整逐字稿與重審收據。

`J-Net21` 在本庫 `docs/videos/lexicon.json` 目前沒有專門發音項；六處英數混寫的 TTS 唸法、停頓與上述節奏**尚未試聽**。不能從文字檢查推論實際台灣口音旁白自然，須在後續試音／`check-audio` 判斷，再處理必要的發音詞或 `say`。本次沒有 TTS 或付費呼叫。

## 下一關界線

本候選可以進入**離線聽眾改稿**，以最小範圍解決三景重複並同步完整稿；仍不可當成正式機逐景查核已通過。正式採用須以最後版 hash 重做獨立 row review，保留法院 PDF 的 `reviewer_only:[4]`，再執行 65 筆正式逐景 verifier、完整稿獨立審核、listener／敘事／旁白／畫面／CC／成片各關卡。舊完整稿和舊審核收據不能沿用；此候選沒有匯入、主機寫入、媒體或上傳。
