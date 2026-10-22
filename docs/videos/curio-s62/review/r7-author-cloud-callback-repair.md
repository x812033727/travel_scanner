# S62 R7｜作者雲夜回呼退修

2026-10-22 UTC。**R7 作者候選；獨立來源／書面畫面覆核與兩位全新正式 13 題盲讀均待辦，不可用於付費媒體。** [R6 正式雙盲合併](r6-formal-merge-audit.md)是 **12／13 HOLD**，兩位讀者共同 No 只有 `no_recap`：開場 `s62004` 已說一月九日雲遮，正文 `s62041` 又重新說同一晚雲天，沒有點名這是回呼。R6 尚未有獨立史料票，本輪不沿用任何舊版審查結論。

## 兩句定點修訂

- `s62041` 以「**回到開場那夜**」明示回呼，接續伽利略先怕木星走得與計算不同、想拿九日位置核對卻沒有新位置的問題；`s62042` 改說原書的觀測圖從八日直接跳到十日，指出證據空格，不再重新描寫窗外雲天。固定 Carlos 英譯 [L1294–1313](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1294-L1313)先有八日 Fig. 2，接著作者等下一夜卻滿天雲，再接十日 Fig. 3。這兩句沒有聲稱九日曾見到星點，也不預先透露十日點數。
- 其餘 112 句、110 個原創插圖提示、4 張資訊卡、場景次序、loop 和 YouTube 說明欄均保持 R6 原字。`claims.md` 的 `s62042` 同時連 G04／G05 兩段固定行錨，對應八日和十日的兩幅圖。

## 可逆差分與固定雜湊

[R6→R7 結構化 JSON 差分](r7-author-structured-diff.json)完整保存 `video.json` **2 個** leaf before／after；逐葉正向重播與反向還原精確得到兩版 JSON。[JSON 封裝的文字 unified diff](r7-author-text-diff.json)涵蓋 `script.md` 和 `claims.md`，取出 `patch` 欄後 `git apply -R --check` 通過。`brief.md` 和 `research.md` 逐位元未改。

| 檔案 | R6 SHA-256 | R7 SHA-256 |
| --- | --- | --- |
| `brief.md` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` |
| `research.md` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `9551bab89a03d91dc29afd103bdc383541fde1b10d8fb3b7de0eb218cbb6a7ad` | `1c811dfb9561248e314f0a39a3510386a6188322521f2d1e6c403e03ab81de95` |
| `script.md` | `0816b0a91b5b4e22571db7cf04b350b121dd56e364a57637f228a1d3f9d8a3c3` | `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326` |
| `claims.md` | `830bfed106d7c5e49dfda5e5198ac39d35470dd18d0e4bb8df9a1c2a19d67eee` | `8cac2b796808afc29fe600c758d84a046342c7a89e7520fc4dfa512b5477f5e3` |
| `r7-author-structured-diff.json` | — | `ae9c5d5f5ecb104ff4b43e88db47bdcac9d96129e8d39b602e1ae1a7c1b90e76` |
| `r7-author-text-diff.json` | — | `865a14972411557c53b8f3ef373dead64121fd3e5b3583209da437f03b91a492` |

固定 1880 年 Carlos 英譯 raw SHA-256 仍為 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。官方 CLI 重產 `script.md`，`narrative_hash` **`edc7d2005d74f93c`**，`speech_hash` **`5611a33a9a3fd52a`**。

## 作者端檢查與交接

官方 `lint --slug curio-s62 --json`：**0 error、0 warning**；114 句、114／114 同字逐句主張，每句有固定來源行錨；110 張不重複原創插圖提示、4 張資訊卡、最多連續一張卡、7 章、13 組提問回收。官方 `estimateTimeline`：250 CPM 開場 **46.53 秒**、正文 **10.181 分鐘**；325 CPM 開場 **37.63 秒**、正文 **8.254 分鐘**。固定 5 秒片頭和 21 秒片尾最後 16 秒 Studio 元素不計入正文，實際 TTS 時長仍待測。無虛構影片 ID，也沒有 TTS、插圖、配樂、渲染、上傳或付款。請新的獨立來源／畫面覆核者和兩位只讀同一 R7 劇本的正式盲讀者重新審查；R6 票不延用。
