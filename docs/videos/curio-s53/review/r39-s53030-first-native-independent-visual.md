# S53 R39｜`s53030` 首張原生圖獨立原尺寸視覺判定

2026-10-22 UTC。**HUMAN REJECT。**我不是本景提示詞、出圖或機器評審作者；直接檢視首張 1280×720 未裁原圖，核對現行分鏡、口播、claims、固定 Survey D 原文與 Curio 插圖驗收規則。此判定只綁定下列影像與稿件版本；本回只寫此收據，沒有裁圖、改稿、改 claims、改私有圖單或購買媒體。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| `/workspace/.video-work/curio-s53/keyframes/s53030-1.jpg`，首張未裁原圖，1280×720；本景所選圖亦為同一檔，沒有 trim | `41ce684ead97291c27cc24e1a3b924d7b842ba45e59ce29bdf101546027e3c1f` |
| `docs/videos/curio-s53/video.json` | `7ebd094e7bd89ba3ebf036440385ffb6f54aa3f8bdf746b30bbcc91c7d72ba10` |
| `docs/videos/curio-s53/claims.md` | `7ea2850176e7e8a27e10fa7807db0007358f52868eb3f8bedd87ca8a711820f4` |
| `docs/videos/curio-s53/script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 固定 1913 年 *San Francisco Relief Survey* `/tmp/s53-sf-relief/56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| 檢視時私有 `/workspace/.video-work/curio-s53/keyframes/manifest.json` | `ba387840f0cbca1d0c1c38afb9e97438e51dbc9b360cc230af0ed382dea1747b`；本景 request key `457afbc153ef36d9`，選上述原圖 |

`s53030` 口播是「可等著換進木屋的人，還要再等多久？」；prompt 要求 1906 年火災後避難地的廣景，一位匿名住戶看木匠繼續建另一棟木屋。claims 同列只概括「建屋宣布、9 月施工及分散營地」。固定 [Survey D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865) 記載救濟小屋用來取代帳棚、1906 年 9 月 10 日開工、9 月 16 日漢密爾頓廣場完成 20 棟，以及此後至少兩三個月才有相當數量房屋備妥供難民使用。原文沒有指認此位住戶、木匠、工位或某棟屋的外觀；插圖只能作故事概念示意。20 棟完工不等於當日無人入住，也不等於當時所有小屋都未完工。

原圖是可愛、平面著色的 2D 卡通，沒有照片、3D 或油畫質感，畫風與 `cute-mystery` 方向相容。左側唯一人物圓臉平滑、身形矮小，原尺寸下**偏童貌**，沒有可清楚判為成年住戶的面紋或其他成年特徵；Q 版比例本身不足以證明他是兒童，年齡歧義單獨不作硬性退件。人物只是站在街邊望向右側，沒有可辨的等待隊列或與建屋工程互動。

畫面右側佔主體的是**已完成的大型住宅**：高屋頂、幾個老虎窗、煙囪、兩層窗列、門廊與完整階梯，前方是整理過的道路／人行區；中景另有紅色圓形交通標誌。沒有帳棚、裸地營地、木匠、未完工小屋、木料或施工動作。不能單靠屋頂樣式為建物精確斷代，也不能從模糊的標誌圖樣斷言確切交通規則；但這一整組視覺語言明顯像有道路標誌的完整住宅街景，不像 Survey D 所述正從帳棚過渡到小型救濟小屋的 1906 年營地。尤其已完工大宅與本句「還要等多久」、下句「大批小屋得再過兩三個月才備妥」相接時，容易讓觀眾誤讀為待分配的救濟木屋已是眼前這種現成住宅。

私有 manifest 記機器評審 **9.29／10、`passed=true`**；`style=10`、`details=7`，唯一問題是「missing carpenters working on a wooden house」。我同意木匠缺失，但退件理由不只是一名背景人物缺席：場景主體變成與口播及來源脈絡相反的完整住宅街景，失去「仍待興建、仍須等待」的核心訊息，並混入現代感的道路標誌。依 `.agents/skills/curio-episode/SKILL.md` 的「評審過了就收；只退會誤導的圖／畫風漂移」界線，這是會誤導的內容替換，故 **HUMAN REJECT**，不能把機器 PASS 當本景的人眼 KEEP。此收據不決定重畫、替圖或下一景，也不回綁私有 manifest。
