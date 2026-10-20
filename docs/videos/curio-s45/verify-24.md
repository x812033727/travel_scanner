# S45 R10-V2｜三景提示詞定點修補候選

2026-10-20 UTC。首輪 [MiniMax 原生試圖 0/3 KEEP](verify-23.md) 後，只改 `video.json` 的 `bly001/bly039/bly088` 三個 `data.prompt`；`brief.md`、`research.md`、`claims.md`、102 句口播、`script.md`、縮圖、說明欄、場景順序及片尾均不變。新提示詞分別限定 1887 年的紐約報館、渡船艙與河岸登船；清楚指定成年女記者、1880 年代服裝、單一主體及 16:9 內滿版畫面，排除首輪的現代裝置、年長男子、孩童遊湖與黑邊。這些都是**卡通示意**，不指定原船樣式或原址細部。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` |
| `research.md` | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `video.json`（R10-V2） | `19785376c41d7da718c5db5333af513d159e98ee5590feab35e0b56b3d5ab4e7` |
| `script.md`（R10 未動） | `b5354170966637ceea44ba6d2b96d27b052f3195db02ba91507af2dff984986c` |
| `claims.md`（R10 未動） | `81f0d836ab7a5026a13654b88e3c5517a51fc8be124eaacfaba3a3f0c39e30f1` |

`script --slug curio-s45` 重生後腳本 hash 原樣，敘事短碼 `cd13e6ba7042c612`、語音短碼 `e0a77b2e5e59e9f9` 未改。`lint` 0 errors；新增的 16:9 與成年字詞重複提示有 2 項風格冗贅 warning，片尾口播不請訂閱有 1 舊 warning。三處重複是為針對**實際已發生**的錯圖，不是新增史實；畫面是否有用仍須原尺寸驗收。音檔與時間軸 SHA 仍由 [verify-22.md](verify-22.md) 記錄，新視覺雜湊會使舊插圖 manifest 失效。

這只是作者的**書面候選**。另一位工作者須重開固定 Bly 原著並查三條新提示詞是否越界及 R10 其餘畫面是否維持；獨立 PASS 後才可用原先 US$3.97 全片上限再對三景**各一張**第二輪試畫。第二輪若仍低於 ≥2/3 原尺寸 KEEP，停止付費圖、配樂與成片。
