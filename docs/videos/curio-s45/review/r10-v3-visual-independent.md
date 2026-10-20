# S45 R10-V3｜三景提示詞修正後獨立覆核

2026-10-20 UTC。**書面畫面 PASS**，限下列精確 R10-V3 版本；這不是生成圖片、配樂或成片驗收。V2 的 [HOLD](r10-v2-visual-independent.md) 所指出的船艙獨處、低窗觀景與原船規格暗示，已在 `bly039/bly088` 兩條提示詞修正。可依已核准的整集上限進行 `bly001/bly039/bly088` 各一張第二輪試圖，仍須逐張檢查原尺寸並套用試畫前的 ≥2/3 KEEP 門檻。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` |
| `research.md` | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `video.json`（受審 R10-V3） | `5e6385179874fd55225c670fdac0658bb6d99f139cd970cacc380ac596dda565` |
| `script.md` | `b5354170966637ceea44ba6d2b96d27b052f3195db02ba91507af2dff984986c` |
| `claims.md` | `81f0d836ab7a5026a13654b88e3c5517a51fc8be124eaacfaba3a3f0c39e30f1` |

重新打開本集固定的 [1887 年 Bly 原著轉錄](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)：本地 `/tmp/curio-bly-source/59899-0.txt` SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`，與 `research.md` 固定版本相同。逐欄比較 R10 基線 `77eca448` 和現在的 JSON，仍然只有 `bly001/bly039/bly088` 的三個 `data.prompt` 不同；其他畫面欄位、場景順序和口播沒有變。對 V2 報告所錄提示詞比較，`bly001` 原樣，V3 只修 `bly039/bly088`。

| 景 | 來源核對與裁決 |
| --- | --- |
| `bly001` | **PASS，沿用 V2 判斷。** 原著 L141–165 有 1887 年《世界報》委託與編輯談話；成年維多利亞時代女記者在紐約報館的單人畫面是普通卡通取景。空白資料夾不冒充原件；沒有聲稱當時房間裡只有她。 |
| `bly039` | **PASS。** 原著 L1511–1540 寫同行者坐在窄凳上、小窗關閉、窗位很高，艙內空氣悶，且想去看窗外會被看守喝止。新版讓布萊坐在窄凳前景，明說同行者在裁切畫面外；高處關閉小窗在背景，窗外沒有可辨景物。這是單一前景主體的示意，不再說她獨自待在艙內或看見特定河岸。沒有指定原船細部。 |
| `bly088` | **PASS。** 原著 L3049–3068 記陪審團邀 Bly 同行再去島上，這次搭乾淨的新船。新版明說陪審團同行但在取景外，畫普通、有甲板、前往島上的船；上船動作與台詞相合。沒有再聲稱是特定公共渡輪，也沒有原船大小、木材、欄杆或原址細部。 |

機械核對：`video.json` 100 場景、102 個互異口播 ID；`script.md` 同序 100 節、102 句逐句一致；`claims.md` 的 99 個正文列與 JSON 同 ID 同台詞。`node tools/video/cli.mjs lint --slug curio-s45 --json` 為 **0 errors、3 warnings**：三景 `16:9` 重述畫風、33/96 張圖含 `adult`、既有片尾訂閱提醒。這些是風格與片尾警告，不推翻本次史料／書面畫面 PASS。實際畫面仍須人工原尺寸驗收，尤其確認人物成年女性、1890 年以前的環境、船艙高窗與登船動作。本報告未改內容檔，未呼叫付費媒體。
