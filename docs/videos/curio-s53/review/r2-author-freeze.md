# S53 R2｜A 案全稿作者凍結，交獨立覆核

2026-10-20 UTC。R1 [獨立題材可行性覆核](r1-feasibility-independent.md)已通過固定來源與選題關；本次是**作者候選全稿**，不是作者自行簽發的逐句來源、書面畫面、盲讀或媒體 PASS。

## 凍結內容

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](../brief.md) | `b029ee451bfad26fe9cd03463ccd8e4a6b2d6cf01d6248b9b6ae4b405051bbc8` |
| [research.md](../research.md) | `048f181b8dd93705550c074c8e1cce5121b3af2f0b1a677767e01b7af4b20d84` |
| [claims.md](../claims.md) | `f0a96554ec6da45b96c6c4521c8cbb2d0823d94e2d6182c9d31037cd4dc89de1` |
| [video.json](../video.json) | `80d7ac1c1c156691634bdd0a492d234e5ca169a4a3825959d97bc5bdb9c25f9c` |
| [script.md](../script.md)（CLI 重生） | `b8fba10ed2e143eb677aaf389bb2c4d088cf7ecda8e376386788afe198852df4` |

題材主線是一棟**概念示意**小屋從公共空地、購屋契約、清場期限、另覓土地，到搬後訪查的行政生命史，不指稱存在同一個具名住戶。依 R1 要求，動筆前已把 A 案的承諾收窄成「誰付搬遷費、搬往哪種土地」，不講沒有原文的機械搬運步驟；`research.md` F08 拆開 **70／680** 與 **23／未得完整紀錄的 457**。558／82% 偏好句因分母語意不明，沒有進口播或字卡。清場要求在旁白歸屬於 1913 年救濟調查，沒有冒充另獲公園委員會原件。新增 F10–F13 的木料供應、移屋費、買地分期、遷後群居與供水也須逐句查。

固定全文仍是 [R：1913 年救濟調查](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt) `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，以及 [C：1906 年新聞編書](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt) `4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c`。本機 `sha256sum` 與原列相同；作者直接讀固定全文，C 只作有歸屬的尋人告示背景。行號及逐句連結在 `claims.md`；S53 R2 最後把遷後群居與約七成共地的引證延至 R L10995，未改口播。覆核者須自己重開全文。

## 文字與畫面交接

- 7 章，135 句對應 135 列 `claims.md`；`video.json` 共 133 景，其中正文 125 張 `shot`、7 張數字卡，另 1 張 `outro`。正文插圖占 125／132，卡片最大連續張數為 1。12 條 `loops` 有明確 setup／payoff；開場同時埋下購屋、搬遷費、訪查下落與地租四個問題。
- `lint --slug curio-s53 --json`：**0 errors／0 warnings**。估值在 250／325 CPM 時：濃縮開場 47.77／38.87 秒；片頭後到 `outro` 前正文 625.70／510.60 秒（最快仍 8 分 30.60 秒）。口播包估值 691.73／564.10 秒；若再接 5 秒片頭及 21 秒片尾，估值約 11:57.73／9:50.10。這不是實際 TTS 時長。
- 可用的原創動畫是本機 [Curio bookend 候選紀錄](../../branding-release/2026-10-20-curio-local-bookends.md)所列版本：`/workspace/.video-work/curio-brand-candidate/intro.mp4` 為 1920×1080、30 fps、150 格／5 秒，SHA `a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef`；`outro.mp4` 為同尺寸、630 格／21 秒，SHA `275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee`。本機品牌選擇指向該候選包 `1ffcf193d68dfface2d561c3362f69b8bfe8590a90b5d8fa257a8b783984a801`。濃縮開場後插入片頭；片尾第 5 秒起最後 16 秒保留兩個推薦影片框及訂閱圈。可點影片與訂閱元素須私人上傳後在 YouTube Studio 安裝及點測，不能由 MP4 畫框代替。
- `youtube.description` 已列 R、C 兩份固定來源全文及頻道連結。插圖提示詞只畫原創概念場景：不做某戶現場重建、可讀假契約、私人清場通知或搬屋機械；數字放後製卡片。片尾旁白不點名下一支影片。

本地機械檢查：135／135 句 ID、文字與 `claims.md` 對齊；125／125 插圖提示詞非空；來源及頻道 URL 存在。`npm run test:docs-videos` **236／236 通過**，`npm run check:tasks` **2124 票格式通過**（其餘票既有過期認領與 scope 警告），`git diff --check` 通過。尚無付費 TTS、MiniMax 插圖、配樂呼叫、站台送審、成片或上架；也未由作者自己跑盲評冒稱獨立結論。

**下一關：**另一位工作者按上表五檔 SHA 獨立重開 R／C，逐句核 `claims.md`、`video.json` 和插圖提示詞；兩位此前未讀本稿的隔離讀者各按 13 題盲評，再做政策與語音關卡。R1 題材 PASS 與本地 lint 不能放行任何媒體費用或 YouTube 動作。
