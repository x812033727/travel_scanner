# S41 R5h 前製交接與逐景查核 — 2026-10-20

## 精確版本與判定

本收據只涵蓋〈焚書令下，《書》怎麼留下來？〉的書面劇本、來源、分鏡提示與一支 Short 企劃。五個經獨立來源／視覺審閱的檔案在審前、審後及交接時具有相同 SHA-256：

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `0b19563986aea2392e611bb2b6768c09848875f3d5206ec2ad07c310669208f5` |
| `video.json` | `79839877cff85a6965d0ae7cc34b2b0077febba4a328c9e7903b3a8d503e355c` |
| `claims.md` | `370a78a685512b3e7ca36c43c60060014f34567a11f1b832b6f54e3e4c9e39a4` |
| `research.md` | `2a8e586328f474dd41086e88a8826297116ddd84fb2e7a5456a12acf063d3eaa` |
| `brief.md` | `f1b37142edd09fc7a7d29e003f7be9e4f1a852525218211128a749a6f24db1ff` |

敘事雜湊是 `4d66117ae16c37a6`。程式校驗 `narrativeReviewMatches` 對 [合併紀錄](reviews/narrative.json) 回傳 `true`；該紀錄 SHA-256 是 `a81f23fd40072872197b0c0b8f76385d31abc18591681b347ddc4166568e4c47`。

兩名第一次閱讀此稿、互不參照的盲讀者各讀相同 `script.md`：

| 讀者 | 13 題判定 | 報告 SHA-256 | 結果 |
| --- | ---: | --- | --- |
| [A](reviews/blind-a.md) | 12 Yes／1 No | `42b7a71921b4499812c1863d17510eb5778c3ae147e0aa8fd06a684535a6efef` | 唯一 `chapters_link=No`：`qb059` 先介紹伏生，`qb060` 才明說藏牆。 |
| [B](reviews/blind-b.md) | 13 Yes／0 No | `f74384cb10da1892e54ff04de901932ad17659493771f768557236d5da960c36` | `chapters_link=Yes`：認為 `qb059` 指出承接主角、`qb060` 立即給動作。 |

`tools/video/core/narrative.mjs` 的 `mergePanelVerdicts` 規則採用任一讀者有引句的 Yes；必要題要兩人都答 No 才失敗。因此**合併敘事判定 PASS**，不把 A 的單獨 12/13 寫成兩人均滿分，也不再為一人意見改動定稿。

獨立 [來源與書面畫面完整覆核](reviews/source-visual.md) SHA-256 `3dab6cf0919195a9c0f71a152a276f35e83e41ff05437967d4d7e99626b2d9b5`：**SOURCE LOCK PASS；WRITTEN VISUAL PLAN PASS**。審閱者重新下載並比對 `research.md` 的七個 pinned raw 文字檔完整雜湊，逐一檢視正文 108 句、103 個插圖提示、5 張引文卡及 3 句片尾旁白。七檔只是《史記》與更晚《漢書》兩個傳世文獻家族，並非七份秦代獨立證詞，也沒有傳下來的秦廷原令。

本機 `node tools/video/cli.mjs lint --slug curio-s41`：0 errors、0 warnings。正文嚴格估時在 325 spoken units／分鐘約 8:22.3，300 單位／分鐘約 8:53.4；這不是實錄音長度，語音完成後須測量正文是否真的 ≥8 分鐘。全片時間估算包含片尾，因此不可代替正文門檻。

## 濃縮版與片頭片尾

[Short 企劃](shorts.json) SHA-256 `d5c29219bd68fe5d474505fe75a4e4129d47cd12d233afd0dda609e022ceb6a3`：一支 `from-episode` 六拍剪輯，取 `qb058`、`qb031`、`qb060`、`qb065`、`qb067`、`qb066` 的長片鏡頭；前兩拍交代《書》入令及博士官限定，接伏生藏牆、二十九篇、教學與缺篇界線。這些鏡頭均在現版 `video.json`，引文只連到固定版《史記》J6 與 J121。單支 Short 的 `validate` 顯示 schema/source hashes OK，`episodeShortsProblems` 對長片回傳空陣列；尚無圖、聲、成片或獨立 Short 成片 QA。

系列固定 5 秒／150 格片頭接在約 53 秒濃縮冷開場後；21 秒／630 格 v4 片尾與最後 16 秒 Studio 結束畫面元素的接點已規劃於 `brief.md`，範本 `oxEtlA8GWas`。MP4 的框線本身不可點，待私人上傳後必須在 YouTube Studio 匯入並實測「最符合觀眾喜好」、最新上傳與訂閱元素。此階段沒有合成動畫、語音、配樂、插圖、Short 或上傳。

## 後續製作界線

書面 PASS 僅可作送大綱的前製依據。站台大綱與劇本關卡須各自取得與現版雜湊相符的核准；正式語音後執行 `check-audio` 並測量正文長度。插圖開畫前依 S41 實際站台報價核准整集上限，不能沿用 S34 預算。生成後需驗收 103 張插圖、完成片頭片尾和配樂、成片 QA、私人上傳後 Studio 可點元素，再從長片實際鏡頭製作及查核 Short。
