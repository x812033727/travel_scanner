# S53 R34｜`s53028` 最後量尺與木板修稿非作者書面紙審

2026-10-22 UTC。**書面 PASS，限本回精確稿件。**我不是 R34 修稿或出圖作者；獨立核固定 1913 年 *San Francisco Relief Survey* D 原文、R32 與 R33 兩張已退實圖、R34 可逆差分及有效私有選片／付費狀態。作者提交 commit `f073cfc0991ca0fa6115eddec4ae2f69417df73f`。本 PASS 僅是第三／最後一張 `s53028` 實際原生圖之前的書面判斷，並非那張圖的 KEEP、全片或發布核准；本回沒有修改私有圖單或購買媒體。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| R34 `docs/videos/curio-s53/video.json` | `f98955b261259a0f687e409a043afe910fe7e9c38a7630e2b5a2d665ebda4997` |
| R34 `docs/videos/curio-s53/claims.md` | `0197cf312874d34cc31895dee05993275357bceac6d81b951fa73334a78841d0` |
| R34 `review/r34-s53028-final-distinct-rule-board-structured-diff.json` | `9a7437910654b78ee32be6d4c7da8f26536368f181ea24472c20bea6d114a062` |
| R34 作者收據 `review/r34-s53028-final-distinct-rule-board-author.md` | `a5a90cfd73b790db508ec6c77fe7c7391685ca27c94adcce2576b6bd6bb5a81a` |
| 未變 `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 固定 `56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| R32 首張退件未裁／裁圖 | `422357339ab4a2ab4267593c1c33c44f73dec3013773009dbc7577b287466010`／`d4a06299fb0b6bd023478bdebb33c8e4bbde1e737979d007576f65336cbe0db5` |
| R33 第二張退件未裁／裁圖 | `433affe85ed0e5c9db5b61fadaeb9cf228a06a6c2ea8e8574c264eccfdee1f2e`／`87e41ddf06d462214a39e8cddb5073482745827d37f4a13f6ec127d2b4d36789` |
| 有效 18 KEEP `keyframes/manifest.json` | `1c97c4ab17ffcae0624c0f312d731c9b7c91919c167d0c7f41aee1e6cbdc12bf` |
| 有效 `media/ledger.json` | `51419ed2bc7373282deb3af23f3cdb1ae12c7243d1e5b3eb996b43f4d65c1c5c` |

固定 [Survey D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870) 在 L4858–4864 記土地及建築部建小屋以取代帳棚；1906 年 8 月 1 日宣布建屋、發包，**9 月 10 日開工**，**9 月 16 日 Hamilton Square 完成 20 間**。`s53028` 口播仍是「九月十日，小屋工程開始。」來源沒有指認一位木匠、摺尺、木板、鋸架或當日某帳棚工位。R34 的 claims 明確稱它們是原創 Q 版概念示意，不把道具當史料證物，也不畫開工當下已完工的屋子或屋架。

R32 第一張把此開工場景畫成童貌近代硬帽人物、沒有量測，兩側是已成形房屋；R33 第二張已回到成年裸地帳棚，卻變成接近寫實的人體比例，且僅有一根帶刻線木條，無第二片待量木板；兩張均 HUMAN REJECT。R34 書面改用**灰髮、面紋、未戴帽的中年成人**，同時明寫大圓頭、寬眼、短緊身體比例，以回到固定 `cute-mystery` 角色形狀；工具明寫**有折節和細刻線的短淺色木尺**，壓在**另一片明顯更寬、較深且無字的粗板**上，板由一個低鋸架承著。只留裸地和單面帆布帳棚牆，沒有完工屋或屋架。尺、板有不同寬度、顏色與刻線，並明說兩件都須入鏡，針對 R33 把兩件合成一根的問題；單片待量板不是宣稱當日有某處備料庫。個別 prompt 只描述可見角色比例和物件，沒有重述色盤或系列 look 名稱。

把結構差分中的兩個 `after` 字串各反填一次 `before`，逐位元組重現 R33 commit `35ff4eab4814f9dd202ccfa80f29caddac66de0a` 的 `video.json` SHA `b41e032ca0006897cf12328d43a0f1f13383d5645892eb34c89d7ba917ca8cfd`、`claims.md` SHA `f0e4d90b916e6676b9b70dc0637412bc29e00e6335abfa298f5f10edb68edbba`。124 景中只 `scenes[21].data.prompt` 改變，其餘 **123 景相同**；claims 132 行只第 28 行改變。**126／126** 口播 ID／文字相同，`script.md` 同 SHA，`speechHash=05c4d9a79a8708b4`，私人 `timeline.json` 亦仍記此 speech hash；音訊沒有隨本次文字修稿重作。自行計算 R34 `visualHash=4d419236d18aa61f`。以正確父目錄 `VIDEO_WORKDIR=/workspace/.video-work` 實跑 `node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0、**0 errors／0 warnings／126 lines**。

有效 18 KEEP manifest 仍綁 R33 舊 `visual_hash=33aeb288b6ac5808`，**尚未回綁 R34 新稿**，且沒有 `s53028`。18 筆與 R32 後圖單的 ID、request key、所選 SHA 完全一致，逐檔重算所選 SHA 全部吻合。ledger 逐筆重算 **US$0.6210／47 image／46 judge／0 預約**，包含 R32 錯置工作目錄首張及 R33 第二張各自的 image 與 judge；付費嘗試不能重置。`media/jobs.json` 為 `jobs={}`，`STOP` 在位。

書面結論 **PASS**：新 prompt 與 claims 對來源及兩次退件原因有具體、可核的修補。仍須在 STOP 下備份、離線回綁並復核 18 KEEP，用正確父工作目錄 `/workspace/.video-work` 做即時模型／額度／整集 US$4.78 上限預檢，之後最多試 `s53028` **第三張且最後一張**，再看未裁原尺寸及所選裁圖。近景加既有 `camera=pull back` 仍可能生成錯誤比例、硬帽、屋子，或再次合併尺與板；若第三張仍失敗，依已定停線評估誠實重用已收圖或來源卡，**不購第四張**。此紙審沒有放行 `s53029` 或批次付費。
