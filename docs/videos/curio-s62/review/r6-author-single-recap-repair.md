# S62 R6｜作者單處重述退修

2026-10-22 UTC。**R6 作者候選；等待新一輪獨立來源／書面畫面覆核和兩位全新正式盲讀，不可用於付費媒體。** R5 [獨立來源覆核](r5-independent-source-visual.md) PASS，但[兩位正式盲讀合併](r5-formal-merge-audit.md)為 **12／13 HOLD**。兩人共同指出 `s62057` 已說 1 月 12 日細點幾小時後顯出，`s62058` 緊接著用另一句重說同一事實；共同 No 僅 `no_recap`。

## 修訂與原文界線

- `s62058` 改成當晚新資訊：原書在 [L1346–1353](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1346-L1353)記東、西兩個明亮點各離木星兩角分，後出的細點幾乎貼著木星。`s62057` 保留「幾小時後顯出」，不再連續重複時間與出現事件。
- 同一輪只作兩個低風險口播收窄：開場 `s62006` 改問稍晚是否仍只見兩點，由 `s62075` 回答，不先講細點會顯出；1 月 10 日 `s62045` 不再問原書無法確證的第三點實際去向，只陳述作者猜它可能被木星遮住。兩處對應 R5 單人讀者的次要意見，沒有增加任何新觀測或斷言。首夜未見哪一點仍在 `s62062` 明確說成不可反推。

## 可逆差分與固定雜湊

[R5→R6 結構化 JSON 差分](r6-author-structured-diff.json)記錄 `video.json` 的 **5 個**完整 leaf before／after：3 句旁白、1 組 loop 的 `payoff`／`what`。已逐葉正向重播與反向還原，分別得到兩版完整 JSON。[JSON 封裝的文字 unified diff](r6-author-text-diff.json)涵蓋 `brief.md`、`script.md`、`claims.md`；取出 `patch` 欄以 `git apply -R --check` 驗證可反向套用。`research.md` 逐位元未改。

| 檔案 | R5 SHA-256 | R6 SHA-256 |
| --- | --- | --- |
| `brief.md` | `5d87a5bbaaf69375f941610ee09befdb3e75b29dc1462b115e512448a8cdc24c` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` |
| `research.md` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `e7d14243eefff747d94ed2f28193ab93c0af97646b2ff55de935161c7643067a` | `9551bab89a03d91dc29afd103bdc383541fde1b10d8fb3b7de0eb218cbb6a7ad` |
| `script.md` | `2d92a72e535f03b53c70c3aa3b52c218c035c1ee53eb1ca82d3d0a802a6cc091` | `0816b0a91b5b4e22571db7cf04b350b121dd56e364a57637f228a1d3f9d8a3c3` |
| `claims.md` | `d1f2280234a7f393403e6aa97d36e24e8305d8d5788fbce69c581193b7f3bf36` | `830bfed106d7c5e49dfda5e5198ac39d35470dd18d0e4bb8df9a1c2a19d67eee` |
| `r6-author-structured-diff.json` | — | `45b436ae8040f44d2670b5d79c447bae9e99411007c2b5275ea2428ebb00b7bf` |
| `r6-author-text-diff.json` | — | `702127ee5eb9fd31cc40cc447fe48c49d40a97830a4c64278e61b9de7f96f028` |

固定 Carlos 英譯原文 raw SHA-256 仍是 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。官方 CLI 重產 `script.md`，`narrative_hash` **`12dee2d6e454e303`**，`speech_hash` **`036955a61b915372`**。

## 作者端檢查與交接

官方 `lint --slug curio-s62 --json`：**0 error、0 warning**；114 句、114／114 同字逐句主張，每句有固定來源行錨；110 張不重複原創插圖提示、4 張資訊卡、最多連續一張卡、7 章、13 組提問回收。官方 `estimateTimeline`：250 CPM 濃縮開場 **46.53 秒**、正文 **10.152 分鐘**；325 CPM 開場 **37.63 秒**、正文 **8.232 分鐘**。固定 5 秒片頭與 21 秒片尾最後 16 秒 Studio 元素仍不計入正文。這些是文字預估，實際 TTS 時長仍待測。沒有虛構影片 ID、TTS、插圖、配樂、渲染、上傳或付款。請新獨立來源／畫面覆核者及兩位只讀同一 R6 劇本的正式盲讀者重驗；R5 票不延用。
