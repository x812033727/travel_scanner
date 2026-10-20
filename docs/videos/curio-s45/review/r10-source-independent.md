# S45 R10｜單句改寫的獨立史料與書面畫面覆核

2026-10-20 UTC。**史料文字 PASS、書面畫面 PASS**，僅限下列精確 R10 版本；語音、網站關卡、生成畫面與成片不在此結論內。我沒有撰寫 R10 句子，也沒有用 R9 的音檢或網站決定替新版簽核。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` |
| `research.md` | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `video.json` | `6339b421fd41c585039d5b3b8ef933513dff05b0fe9fbf56da82ab929d9537cb` |
| `script.md` | `b5354170966637ceea44ba6d2b96d27b052f3195db02ba91507af2dff984986c` |
| `claims.md` | `81f0d836ab7a5026a13654b88e3c5517a51fc8be124eaacfaba3a3f0c39e30f1` |

直接核對本集固定的 [Nellie Bly 1887 原著轉錄](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3143-L3146)：本地原文 `/tmp/curio-bly-source/59899-0.txt` SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`，與 [research P12](../research.md) 所釘位元組相同。第 3143–3146 行由 Bly 第一人稱回述：她原以為大陪審團不會支持她，接著寫 *“Yet they did, and their report to the court advises all the changes made that I had proposed.”* 這是**她的書所說**，不是本集獨立讀過的大陪審團報告。

以已提交的 R9 基線 `2a62f0b3` 逐檔比對：`video.json`、`script.md` 與 `claims.md` 只改 `bly098` 一句，其餘口播、場景提示詞、卡片、縮圖、說明欄和 `loops` 未改。R10「**布萊在書裡寫：陪審團仍支持她，報告建議採納她提出的改革提案；本集沒讀到報告原件。**」把兩個判斷都留在 Bly 的書中，並明示缺原件；沒有把原書後一句一百萬美元預算或制度改善說成核實結果。`bly097` 仍先問陪審團是否支持，`bly098` 仍直接作答。`claims.md` 同 ID、同台詞，原書定位仍是 P12 的 L3143–3146。文字內容與出處相合。

機械交叉比對：`video.json` 的 **102/102** 句按順序與重產的 `script.md` 旁白逐字相同，102 個 ID 無重複；99 個正文 `bly` 主張列與 JSON 同 ID、同台詞。`lint --slug curio-s45 --json` 為 0 errors、1 個既存片尾訂閱口播 warning；這個 warning 不是 R10 史料或畫面錯誤。`git diff --check` 乾淨。

`bly098` 的書面提示詞完全未改：普通法院走廊，一名成年記者拿**空白資料夾**，沒有捏造可讀的大陪審團報告、原件引文、改革實施景象或特定人物肖像。因此書面畫面仍符合來源邊界；實際生成圖片另須驗收。R9 的[完整來源／畫面審查](r9-source-independent.md)所涵蓋其餘未改內容，差分仍有效。新文字仍須全新敘事評審、政策判讀、精確劇本決定及新 `bly098` 語音音檢。
