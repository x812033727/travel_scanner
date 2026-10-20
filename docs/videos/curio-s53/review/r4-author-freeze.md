# S53 R4｜作者修訂稿凍結，交獨立來源與雙人盲讀

2026-10-20 UTC。R3 [獨立史料覆核](r3-source-independent.md)為限縮 **HOLD**、書面畫面 PASS；[官方雙人盲讀合併](r3-official-panel-merged.md)為 **10／13，FAIL**（`scene_first`、`payoffs`、`no_detour`）。本檔只固定 R4 作者候選稿；不能取代差分來源覆核、兩位新讀者盲評、語音或畫面驗收。

## 五檔精確雜湊

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](../brief.md) | `b029ee451bfad26fe9cd03463ccd8e4a6b2d6cf01d6248b9b6ae4b405051bbc8` |
| [research.md](../research.md) | `048f181b8dd93705550c074c8e1cce5121b3af2f0b1a677767e01b7af4b20d84` |
| [claims.md](../claims.md) | `f8be9d38935c5e6512bc14ad19842ac9e6b9347570d05b6fa3e0cd60f05b91db` |
| [video.json](../video.json) | `e271691db8c0dac4d70c4e5ef3aa5878c2f9ba2549975a7699134ea0bff70088` |
| [script.md](../script.md)（CLI 重生） | `5783416b22cce59b8fa0acfbfe24fac1a539094c697e5ec67950077917ea9ba2` |

固定史料未更換：[R：1913 年救濟調查](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt) `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`；[C：1906 年新聞編書](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt) `4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c`。口播史實仍只依 R；C 未變成小屋住戶的一手證詞。

## 依 R3 報告修訂

- `s53011` 的公園／廣場暫住主張，改連 R [L4250–4264](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4250-L4264) 直接錨點。`s53095` 依 R [L5011–5016](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5011-L5016) 限定為「帶孩子的寡婦」，同步主張、旁白與 CLI 劇本。
- 開場 `s53001`–`s53004` 保持在 **1907 年六月同一處廣場**，期限、小屋及住戶付款連續前進；`s53005` 立即交代這道要求出自 **1913 年編纂調查**，避免把調查誤作當日錄音。`s53069` 以「開場那道」回呼期限。
- 刪去與搬屋主線較遠的木材／運貨細節 `s53019`、`s53022`，以及完整分配名冊 `s53035` 和兩層公寓旁枝 `s53044`。`s53020`–`s53027` 直接問公地的使用期限；`s53033`–`s53037` 只保留先得屋者、營地外次序與領屋後可移往自有／承租地的轉折。`s53038`–`s53043` 把建屋總數接到完工後不到五個月的清場壓力，沒有把 5,610 說成金門公園單一棟數。
- `s53116` 問 **交不起地租，小屋會怎樣**，`s53117` 指向失訪組，`s53129` 明確回呼，`s53130` 才以報告所知 **23 戶被地主扣屋**作答；未把這 23 戶混進受訪的 680 戶，也不推算全市發生率。`loops` 增列這組及兩組即時問答。`s53112a`、`s53114a` 補足買地分期與僅抵利息的有來源進展，使刪去名冊後，正文仍高於八分鐘快估下限。
- 變動的畫面只用無字文件、地塊、小屋與匿名成人；沒有畫無據可驗的搬屋機械、原件或確定家庭個案。`youtube.description` 的史料全文與頻道連結、原訂 5 秒片頭和 21 秒片尾／結束畫面位置仍在企劃與素材規劃中。

## 本地檢查與交接

七章、127 景：119 張 `shot`、7 張數字卡、1 張片尾；**129 句**與 `claims.md` 129 列逐 ID／文字／順序相同，CLI 已重生 `script.md`，16 條 `loops` 的位置有效。`node tools/video/cli.mjs lint --slug curio-s53 --json`：**0 errors／0 warnings**；`npm run test:docs-videos`：**236／236**；`npm run check:tasks`：**2124 票格式通過**（其他任務既有警告）。

`estimateTimeline` 在 250／325 CPM 下，濃縮開場 **50.67／41.10 秒**；開場後至片尾前正文 **611.93／498.67 秒**，快估 **8:18.67**；口播包 **679.67／553.47 秒**。若另接原訂 5 秒片頭和 21 秒片尾，文字估值約 **11:45.67／9:39.47**。均不是實際 TTS 或影片長度。

**下一關：**新覆核者按本檔五個 hash 重新核 R4 變動句、來源與書面畫面；兩位此前未讀 R4 稿的讀者只拿同一 R4 口播稿作隔離 13 題盲評，再合併官方裁決。其後才可處理政策、站台劇本卡、付費配音與插圖。R4 作者機械檢查不等於獨立 PASS。
