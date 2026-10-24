# S53 R33｜`s53028` 成年木匠量板非作者書面紙審

2026-10-22 UTC。**書面 PASS，限下列精確稿件。**我不是 R33 修稿或 R32 出圖作者；我曾獨立驗收 R32 原圖。此回另行核對 1913 年 *San Francisco Relief Survey* D 原文、R32 實際退件原圖與裁圖、R33 可逆差分及目前私人選片／付費狀態。R33 尚未生成第二張；本 PASS 不是圖像 KEEP、全片或發布批准。作者提交 commit `550107c84458c3e231fdc77904ab54477aea444d`。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| R33 `docs/videos/curio-s53/video.json` | `b41e032ca0006897cf12328d43a0f1f13383d5645892eb34c89d7ba917ca8cfd` |
| R33 `docs/videos/curio-s53/claims.md` | `f0e4d90b916e6676b9b70dc0637412bc29e00e6335abfa298f5f10edb68edbba` |
| R33 `review/r33-s53028-adult-measure-structured-diff.json` | `24de146b39fac91070f1350a05e17ad4d1258c91ddda16ea167a4ab1bd5fe1b9` |
| R33 作者說明 `review/r33-s53028-adult-measure-author.md` | `0f07b4ca3db722789af34c722843e5502bdd5336d70d73f3e036d7be8c99f996` |
| 未變 `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 固定 `56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| R32 巢狀私有未裁退件 `s53028-1.jpg` | `422357339ab4a2ab4267593c1c33c44f73dec3013773009dbc7577b287466010` |
| R32 巢狀私有所選 `s53028-1-trim.jpg` | `d4a06299fb0b6bd023478bdebb33c8e4bbde1e737979d007576f65336cbe0db5` |

固定 [Survey D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870) 於 L4858–4864 說小屋由土地及建築部興建以取代帳棚，1906 年 8 月 1 日公布建屋計畫並發包，**9 月 10 日開始施工**，**9 月 16 日 Hamilton Square 已完成 20 間**。`s53028` 的 126 句口播中本句仍為「九月十日，小屋工程開始。」R32 實際 1280×720 圖畫成童貌人物戴青綠近代硬帽、雙手扶板卻無量測工具，左右都是已成形有門窗屋頂的木屋；其機器 9.29 PASS 沒有排除施工階段與時代衝突，因此 HUMAN REJECT。

R33 改為一位清楚中年、灰髮、有面紋、未戴帽的匿名木匠，在裸地上用**短木摺尺沿低鋸架上的單片散置粗木板量長度**；只留一面帆布帳棚牆，明寫沒有完工住屋、屋頂或屋架。成人面貌、雙手及尺直接處理 R32 的童貌／不量板；單片木板與鋸架是開工的概念動作，未畫成真正發現的備料庫；帳棚牆合乎原文「建屋取代帳棚」的環境脈絡，且不預置 9 月 16 日完成的木屋。木匠、摺尺、木板、鋸架及具體帳棚工位**不是史料記錄的特定人物或物件**；`claims.md` 明說它們只是匿名近景概念示意，不主張當日確有此人、工具、帳棚工位或木板。這一書面設計沒有把原創道具說成來源證物，也沒有改寫 D 的日期。

我把差分中的 `after` 字串在現行兩檔各反填一次 `before`，逐位元組回復 R32 `video.json` SHA `b9ce6cc426d547642ff7f6a7ee8c3a2564aad2439ff4b659c0f337ba19e9fea6`、`claims.md` SHA `9be8b979eb0594e9244886811926878d894065872b561262a490c586f05b6e9b`。124 景中只有 `scenes[21]` 的 `s53028.data.prompt` 改動，其餘 123 景逐項相同；132 行 claims 只有第 28 行變動。126／126 個 speech ID 與文字逐項相同，`script.md` 未變，`speechHash=05c4d9a79a8708b4`。獨立計算新 `visualHash=33aeb288b6ac5808`。以 `VIDEO_WORKDIR=/workspace/.video-work` 實跑 `node tools/video/cli.mjs lint --slug curio-s53 --json`，exit 0、**0 errors／0 warnings／126 lines**。

有效私人 `keyframes/manifest.json` SHA `b080a08e4ddecaf1dfd84ebb67fb436cbecc542e3cf4ff5983fc0b66dc04971b`，仍為舊 `visual_hash=63a1d200e63843e2` 的 **18 KEEP**，不含 `s53028`；18 筆所選檔案 SHA 均與圖單吻合。新稿的 `visualHash` 尚未回綁，舊圖單**尚不適用**新稿。有效 `media/ledger.json` SHA `a29940cf76954de8595a3eaacd1a56da94a22a2a2508537dffc96661a384cc8b`，逐筆重算 **US$0.6075／46 image／45 judge／0 預約**，末兩筆就是 R32 錯誤巢狀工作目錄的一張圖與一次 judge，已只計一次；它們不能算成免費重試。`media/jobs.json` 為 `jobs={}`，`STOP` 在位。

紙審結論：**PASS**，可依既定停線流程先安全回綁並逐項復核 18 KEEP，再用正確父工作目錄 `/workspace/.video-work` 做即時模型、額度與整集 US$4.78 上限預檢，最多生成 `s53028` 第二張實際原生圖並獨立人眼驗收。`camera=pull back` 仍可能使近景變寬，模型也可能再畫出童貌、硬帽、成屋或看不見摺尺；這些是下一張**原尺寸**才可裁決的風險，機器 PASS 不代替人工 KEEP。此紙審沒有回綁、付款或開放其他景。
