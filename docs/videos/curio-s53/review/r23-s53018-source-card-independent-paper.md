# S53 R23｜南公園來源卡與未畫住用景獨立紙審

2026-10-22 UTC。**PASS，僅限本回兩景的史料與書面畫面。**審查對象是作者修正灰髮描述後的 `video.json` SHA-256 `2b5d0bfd85a581cac1e08ac8c155a9e8f89969634cc98e1c5300fe3457c7720e`、`claims.md` SHA `a276b8561f713f6160fe8fd4d68c79f0c85640ce0f4db2cf031d81f99e3c278e`、未改 `script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。本回無付費媒體呼叫、圖單重綁、網站核准或整章分鏡核准。

## 固定史料與兩景裁決

我重新打開 `/tmp/s53-sf-relief/56217-0.txt`，實算 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，等於 [`research.md`](../research.md) 固定 1913 年 *San Francisco Relief Survey* 的雜湊。[L4848–4853](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4853) 原文是 `except in one locality, South Park, whose limited area gave no space for separate cottages`。它支持「南公園面積不足，不能安排分開的小屋」，不支持確切帳棚間距、人物動作或現場重建。

| 景 | 獨立判定 |
| --- | --- |
| `s53018` | **PASS 來源引句卡。**主文「沒有空間安置分開的小屋」保留 `gave no space for separate cottages` 的意思；上標給南公園與 1906 年背景，下標明說是 **1913 年調查、英語原文意譯**，沒有把後出的調查冒充 1906 年中文目擊記錄。卡片不再展示 [R22 最後原生圖](r22-s53018-final-native-independent-reject.md)裡反向暗示寬敞通道的退件畫面。旁白未動。`s53010` 日期卡和此卡之間有 `s53011`、`s53014`、`s53015`、`s53017` 四張 `shot`，沒有相連卡片。 |
| `s53085` | **PASS 未畫提示詞。**[L4998–5005](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4998-L5005)記 5,343 棟小屋搬出、除少數外繼續作住宅，且空地分租給個別屋主；[L4900](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4900)稱其為木屋。灰髮中年住戶在已安置的小屋門口開門，是一人一動作的原創住用示意，沒有指認個案、地址或搬運方法。提示詞現在明寫 `grey-haired`，與 [`claims.md`](../claims.md) 同列一致；台詞、`camera`、`visual` 不變。尚未有此景的成圖，故實圖品質仍待原生圖及 judge。 |

`s53018` 的 `big` 卡另用本機 Chromium、專案 HTML/CSS 與字型，在 1920×1080 直接做書面版面探針：來源、主文及下標均可見，無資源拒載與溢出；主文以 190px、下標以 48px 顯示，沒有因 `.fit` 被縮字。這是卡片版面預檢，不是已合成的成片或正式 `render` 收據。

## 差分、lint 與時長

我獨立將 [R23 可逆差分](r23-s53018-source-card-structured-diff.json)四筆新字串各精確反填一次：`video.json` 回到 R22 SHA `49bdd04e5ebb88ff98cd207c6da0545faf1d1721834a0dc099d514a2daf9fa99`，`claims.md` 回到 R22 SHA `34f765eee27fb0ff083413e3e209b42d5dd09b5a2a7a89f16d14556ce1cac44b`，且逐位元組等於 `030ac39b^` 中的兩檔。現行差分檔 SHA **`a924df519500fd9ec7bdeabfdc5a2ccb8a9a38d655e074c76f029a664656e6e4`**；除 `s53018`、`s53085` 外 122 景不變，126 句口播全不變。

`node tools/video/cli.mjs lint --slug curio-s53 --json` 退出 0，**0 errors／0 warnings**。全 124 景除片尾的 123 景中，`shot` 113 景，**91.9%**；連續卡片最多 1 張。`cottage` 出現於 **37／113** 張插圖提示詞，未再越過三分之一警告。

已合成 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054` 與 `narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 未變。正文由 `s53010` 到 `outro` 起點是 **17,651 影格／588.37 秒（9:48.37）**，超過正式長片 QA 的 14,400 影格下限。114 句音檔的 `audio_samples` 合計 **472.66 秒（7:52.66）**；差額 **115.71 秒**是既有時間軸的每句呼吸、換景等間隔，R23 未額外加停頓。純文字以 325 字／分鐘壓力估算為 2,001 漢字 **6.16 分鐘**，或含標點的 2,230 非空白字元 **6.86 分鐘**；這兩者不是實際語音或成片時長。正式規則量測已合成時間軸，仍須後續成片 QA 驗證。

## 私有媒體安全界線

只讀檢查 `/workspace/.video-work/curio-s53/`：`keyframes/manifest.json` SHA `96ef6a6d67c03fd37f86963f819f5bdbafce8c72fbb9f04d0bb983b371a04ef5`，14 張 KEEP 的選圖實檔逐一符合 manifest SHA，對這 14 景的 `keyframeProblems` 為空；`s53010`、`s53018`、`s53085` 都沒有圖單條目。R23 有 113 張 `shot`，其餘 99 景仍缺合格圖。manifest 的舊 `visual_hash=133eba68d1a96469`，現稿重算 `visualHash=14dade824c0840b3`，**尚未重綁，不能把舊 manifest 當現稿已完成分鏡**。

`media/ledger.json` SHA `dc7aaf8ca062b7680113bde534ce7d1cbdc218ab5567626f0365f6fa39dfc01f`：US$0.4725、36 image、35 judge、0 預約；`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 jobs 空，`STOP` 存在。本紙審 PASS 只解除這兩景的書面來源與提示詞疑點；私有圖單後續安全重綁、其餘實圖驗收、站主網站關卡、人耳聆聽及成片 QA 各自仍待完成。
