# S45 R10-V3｜付費第二輪試圖前的書面修正

2026-10-20 UTC。R10-V2 三景提示詞的[獨立覆核](review/r10-v2-visual-independent.md)為 **HOLD**，因此沒有執行第二輪付費 MiniMax。這版只再修 `bly039`、`bly088` 的 `data.prompt`，不動 `bly001`、102 句口播、`claims.md`、縮圖、來源、章節、片頭片尾及所有其他景。這是**作者候選**，不是獨立 PASS 或原生圖驗收。

- `bly039`：女記者在窄凳前景，同行者留在鏡外；關閉的小窗位於後方高處，不呈現可辨岸景。避免將原著有人同艙、禁看高窗的記述畫成獨坐觀景窗。
- `bly088`：畫成她登上一艘普通、有甲板的渡島船，陪審團同行但在鏡外；移除原著沒有指認的 `large wooden public ferry`、船身大小及材質。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` |
| `research.md` | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `video.json`（R10-V3） | `5e6385179874fd55225c670fdac0658bb6d99f139cd970cacc380ac596dda565` |
| `script.md`（重生後同 R10） | `b5354170966637ceea44ba6d2b96d27b052f3195db02ba91507af2dff984986c` |
| `claims.md`（同 R10） | `81f0d836ab7a5026a13654b88e3c5517a51fc8be124ea3f0c39e30f1` |

`script --slug curio-s45` 已重生且雜湊未變；`lint` 是 0 errors／3 warnings（三景重複 16:9、全片多次用 adult、既存片尾口頭訂閱提醒），未用警告數掩蓋史料問題。R10 的[政策與音訊 102/102 零旗標](verify-22.md)仍綁相同口播；畫面版本 hash 已變，舊圖與 manifest **不**匹配。另一位工作者須核對這兩景及差分；獨立 PASS 後才在原先 US$3.97 整集上限內重試三景各一張。第二輪原尺寸 KEEP 若仍不足 2/3，就停止本集付費插圖、配樂與成片。
