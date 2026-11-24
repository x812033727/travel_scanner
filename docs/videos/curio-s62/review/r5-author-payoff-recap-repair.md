# S62 R5｜作者回收與重述定稿

2026-10-22 UTC。**作者候選；R5 尚待獨立來源／書面畫面覆核及兩位全新正式盲讀，不可用於付費媒體。** R4 [獨立史料／書面畫面覆核](r4-independent-source-visual.md) PASS；[兩位正式盲讀合併](r4-formal-merge-audit.md) 11／13 HOLD，共同未通過 `payoffs`、`no_recap`。A 指 s62113 尾問沒有後續回答、s62084 重說 s62062；B 指 s62080–81 只交代猜測卻問實際去向、s62062 與 s62046 重疊。B 另指出 s62084 打斷單線／像回顧、s62105 名稱插段像岔題；本輪一併收窄。

## 定點修改與史料界線

- s62046 改回 1 月 10 日原文記下的黃道共線，將「首夜哪一點沒見到」僅留在 s62062。s62080 問伽利略如何解釋 1 月 23 日不見的兩點，s62081 立即回答「他猜被木星擋住」；問題不要求原書無法證實的實際去向。s62083–84 改為 1 月 24 日第六個時辰的兩段新角距：較近點離木星三角分，另一點再往外兩角分，見固定英譯 [L1479–1489](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1479-L1489)。不再倒回首夜重說身份不明。
- s62105 的片尾資訊卡撤去「美第奇星」命名岔段，改成原書對最外側一點的周期試估；s62106 說重返相似位置**似乎約半個月**，保留作者試估措辭，來源 [L1820–1826](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1820-L1826)，不冒充後世精密周期。s62111 提問其餘幾點待測要交給誰，s62112 緊接原書邀其他天文學家使用準確鏡筒的回答；s62113 改成逐夜相對位置使判斷能被續查的收束句，不再留下尾問。
- 1 月 7 日只見三點但原書沒有識別未見的第四點或當晚沒分出的原因，仍在 s62062 明確說出；1 月 10 日及 23 日的遮擋是作者分別對那些夜晚的猜測，不移植為首夜確定答案。

## 可逆差分與綁定雜湊

[結構化 JSON 差分](r5-author-structured-diff.json)記下 R4→R5 **13 個**完整 leaf before／after，含 8 句旁白、3 個原創提示詞、1 張卡的 2 欄；正向逐葉套用、反向還原，已確認兩版 `video.json` 完全相等。[JSON 封裝的文字 unified diff](r5-author-text-diff.json)涵蓋 `brief.md`、`research.md`、`script.md`、`claims.md`，取出 `patch` 欄後以 `git apply -R --check` 驗證可反向套用。JSON 跳脫保留 unified diff 空白行的必要前綴，避免檔案本身產生尾端空白。

| 檔案 | R4 SHA-256 | R5 SHA-256 |
| --- | --- | --- |
| `brief.md` | `9f63e8de4d158b2e4bdbfcc86579463274966d88bb548318e6bc4200615f4337` | `5d87a5bbaaf69375f941610ee09befdb3e75b29dc1462b115e512448a8cdc24c` |
| `research.md` | `442cbe52e4c92f962726f4940e182bd10bedb41417cb239ede9daf008c5ea74a` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92` | `e7d14243eefff747d94ed2f28193ab93c0af97646b2ff55de935161c7643067a` |
| `script.md` | `8343a4f903fe4b405b1e6364cd67737ed7f3aead625b5fe713bf91c873c05c14` | `2d92a72e535f03b53c70c3aa3b52c218c035c1ee53eb1ca82d3d0a802a6cc091` |
| `claims.md` | `2edb12dd02afa0ed03744616fcb27e889498356709d4c1cf95be415c30914218` | `d1f2280234a7f393403e6aa97d36e24e8305d8d5788fbce69c581193b7f3bf36` |
| `r5-author-structured-diff.json` | — | `b420a6bd1a17a4c9420aa102db52d2c7242d2b525a4320bca61e72eb7c1809ed` |
| `r5-author-text-diff.json` | — | `0bb3f01e8854d1667f9b157fe9079f8af041714050bc376c98a14e6d9025d137` |

固定 1880 年 Carlos 英譯原文 raw SHA-256 仍為 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。官方 CLI 重產 `script.md`，`narrative_hash` **`85c4d37cd19c407a`**，`speech_hash` **`74d1eb578710bea3`**。

## 作者端檢查與交接

官方 `lint --slug curio-s62 --json`：**0 error、0 warning**；114 句、114／114 同字逐句主張，每句有固定來源行錨；110 張不重複原創插圖提示、4 張資訊卡、最多連續一張卡、7 章、13 組提問回收。以官方 `estimateTimeline`，250 CPM 濃縮開場 **47.47 秒**、正文 **10.157 分鐘**；較快 325 CPM 開場 **38.37 秒**、正文 **8.235 分鐘**。固定 5 秒片頭、21 秒片尾末 16 秒 Studio 真可點元素的安排不計入正文；實際 TTS 時長仍須另測。`git diff --check` exit 0，文字補丁反向檢查 exit 0，沒有虛構影片 ID。沒有 TTS、插圖、配樂、渲染、上傳或付款。請新的獨立來源／畫面覆核者和兩位只讀同一 R5 劇本的正式盲讀者重驗；R4 的票不延用。
