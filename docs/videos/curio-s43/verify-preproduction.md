# S43 A 案本地候選稿交接（2026-10-20）

本稿在網站大綱仍等待站主選案時預寫，只作無付費前製。站台精確大綱回條及 `brief.md` 雜湊見 [verify-site-gates.md](verify-site-gates.md)。**A 案的完成與 lint 通過不是 outline／script／media 核准。**

| 檔案 | SHA-256 |
| --- | --- |
| [video.json](video.json) | `3171f4c35f469cd5b0ed448346f5b7b74d1b7a3a26f96458afd35689ae24e5fa` |
| [script.md](script.md) | `68a6ee00e20b990734ab779da4bf18c9ace9005c608371eeebbc5271f16efb9f` |
| [claims.md](claims.md) | `8cc02c74a4b989f3d9b300dbbe91d03a61aaf5b993337409f7187263d88e388b` |

本地 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s43 --json` 結果：**0 errors、0 warnings**，總長估算 10.16 分鐘、92 句含 3 句片尾、2154 個口播單位。首章約 0:58；7 章，15 組伏筆／回收。正文 89 景全是 `shot`，89 個 ID 與 89 筆 `claims.md` 行相合。這些是稿件與畫面配置的靜態檢查，**未合成語音，未量測正文或成片實長**。

劇本從 1831 年 9 月 Wood 收到船長來信、達爾文第二次想退出開場，倒回 Henslow 邀請、父親反對、Wedgwood 勸說，再回到船長面談與後來的鼻子回憶。每景 claim 附固定 GITenberg 行號；插圖提示詞只是一人一動作的卡通示意，未生成也未經獨立內容審核。片中原信缺失、自傳晚出及編者改動的界線仍須由**另一名**查核者逐景覆核，不能只憑作者的對照表。

## 明確待辦

1. 兩名只讀這版 `script.md`、不先讀來源／企劃／前輪評語的讀者，各依 `narrative --slug curio-s43 --json` 題目獨立回答並記錄 exact SHA。任何有效未過項都由作者修正，然後重做新版本盲讀。
2. 另一名史料／畫面查核者重新下載三份固定全文核 SHA，逐條核 89 句口播、89 個圖片提示詞、15 組伏筆與來源／畫面界線。變動後須對新 SHA 重核；此處**沒有宣稱獨立查核通過**。
3. `review-pull --gate outline` 現為 `waiting for the owner`（exit 3）。站主在後台選定 A 並由工具取得對同一 `brief.md` SHA 的核准前，不能推 `script` 關卡或以別集的權限進行語音、插圖、配樂、組片。劇本關卡將重新生成 `script.md`，屆時需重核其雜湊。

影片 metadata 已寫固定資料來源與頻道連結；實際品牌動畫將於成片時使用共用 5 秒片頭、21 秒片尾，片頭在開場濃縮後，片尾末 16 秒供私人上傳後由 YouTube Studio 設定可點影片／訂閱連結。現在沒有實際動畫畫面、可點連結、媒體報價或支付。
