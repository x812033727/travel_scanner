# 品牌故事重製：PR1860 正式片頭片尾

2026-10-26 已透過正式站唯讀 API 實際取得並安裝全頻道 current：
`mokaair-brand-package-v4-endscreen`。官方 `branding --pull --dry-run` 與
`branding --pull` 均 exit 0，metadata 與兩個素材下載路由均 HTTP 200。
這解決了先前只有本機 candidate、不能證明正式 v4 身份的缺口。

| 項目 | 正式站與本批安裝實讀結果 |
| --- | --- |
| package hash | `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88` |
| 片頭 | 5 秒、150 frames、2,708,408 bytes |
| 片頭 SHA-256 | `50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d` |
| 片尾 | 21 秒、630 frames、2,054,558 bytes |
| 片尾 SHA-256 | `00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396` |
| 共同影音規格 | 1920×1080、30/1 fps、H.264/yuv420p、AAC 48 kHz stereo |
| 正式站安裝時間 | `2026-10-12T11:46:32.849Z` |
| 本批安裝時間 | `2026-10-26T02:17:20.202Z` |
| 本批媒體根目錄 | `/workspace/work/brand-story-20261025/media` |

檔案實際安裝於 `<mediaBASE>/_branding/<package hash>/intro.mp4` 和 `outro.mp4`；
`<mediaBASE>/_branding/current.json` 指向這兩個檔案。未改其他工作機、全域預設或原有候選包。
素材、current、暫時 manifest、抽取的工具與 QA 截圖均在 Git 外。

## 來源與驗證收據

- [source-provenance.json](source-provenance.json)：工具來自 PR1860 已合併 commit
  `50a073cced2290ac87eb412e54139aff34a2d384`，reviewed head
  `fe5386a9c493f2e2939e8e6d30eec1953d3d22bc`。用 `git archive` 抽取 448 個必要區域檔案；
  保留 archive tree SHA 與關鍵檔案 SHA，使用既有 node_modules，未切換或合併共享 worktree。
- [dry-run.json](dry-run.json)、[install.json](install.json)：官方原生 CLI 輸出與各次 GET HTTP 收據。
  dry-run 只驗證，暫時下載隨後刪除；install 再下載並正式安裝。
- [media-qa.json](media-qa.json)、[intro-ffprobe.json](intro-ffprobe.json)、
  [outro-ffprobe.json](outro-ffprobe.json)：實際檔案 SHA、bytes、frames 與 packets 均與站上相同；
  兩檔完整 AV decode 均 exit 0、無 stderr。抽看片頭 2 秒為開門畫面，片尾 10 秒為
  Mokaair 字標、兩個影片框及訂閱圓框。這是素材 QA，未宣稱人工成片審核或驗聽。
- 既有 checkout 的 native core 也成功讀取相同安裝包；在獨立空白測試目錄做唯讀、記憶體內選擇，
  得到 `intro_at: after_first_chapter`。沒有建立任何單集 pin、timeline 或影片。
- [project-preflights.json](project-preflights.json)：已存在 submission-root 的逐集來源與 branding 選擇實測。
  它是當時的快照，合成前仍須以最新 source 再跑。

合併版本工具的外部位置是 `/workspace/work/brand-story-20261025/branding-pr1860-tool`；
詳細外部收據與抽看截圖在 `/workspace/work/brand-story-20261025/branding-pr1860-evidence`。
來源依據為 [PR1860](https://github.com/x812033727/travel_scanner/pull/1860) 的
`docs/videos/BRANDING.md`「從正式站取得目前的素材包」「本機成片要跟正式站同一包」「片頭位置」，
以及 curio skill 新增第 5 步。品牌故事採全頻道包，沒有把原劇重綁成 sothatswhy。

## 每一集實作要求

使用者明確要求加片頭片尾；本批不採 PR1860 原生「警告後仍無片頭繼續合成」的容許結果。
[preflight.mjs](preflight.mjs) 是可執行的唯讀前置檢查：驗證 reviewed 工具 tree、完整 decode 收據身份、
本批 current 與實際檔案 SHA/規格、fresh 正式站 package identity，以及指定單集的原生選擇。
缺檔、disabled、不同包、站上讀不到、跨系列或選不到 bookends 都 exit 1；不寫 pin、不合成、不呼叫付費服務。
[guard-negative-qa.json](guard-negative-qa.json) 記錄獨立外部 fixture 的「沒有 current」和「不同 id」都被拒絕；
未改正式安裝包。

本批所有單集都要求：濃縮開場 → 5 秒片頭 → 正文剩餘部分 → 21 秒片尾。
正常 `assemble` 必須帶 `--intro-after-condensation`。正文 720–840 秒以真正旁白與正文時間軸量測，
包含 cold open 和口述 CTA；片頭片尾另外增加 26 秒／780 格，不能拿來填正文長度。
八語字幕、章節與配音遵循實際片頭插入格數；片頭前不偏移，插入點之後 +150 格，片尾無正文殘留字幕。

原始 current 的 package hash 與插入位置參與計算後的 hash 不同；相同媒體放在濃縮開場後的預期
選擇 hash 為 `39d34ab0d563aff4143d88518e178fe57e769747772084c7e9b05f42f6aeda64`。
這是 native 函式的記憶體內選擇結果，尚不是任一集的 production pin。
片頭實際插入格數必須等真正 TTS／正文 timeline 存在後才由正常 assembly 決定，不能用估秒假建。

以 C03 為例，合成前先執行（其他集改成其真正 source root 與 slug）：

```bash
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node \
  docs/videos/brand-story-remakes-20261025/branding-pr1860/preflight.mjs \
  --project-root /workspace/work/brand-story-20261025/c03-submission-root \
  --slug story-everyday-moleskine-c03-remake-20261025 \
  --receipt /workspace/work/brand-story-20261025/branding-pr1860-evidence/c03-preflight.json
```

真正旁白、畫面、配樂與其餘必要 gates 已具備時，使用正常原生主入口；root override 是 `main` 的正式支援參數，
`--workdir` 是共同 mediaBASE，不是 slug 子目錄。以下命令是待前提齊全時的執行指南，本次未執行：

```bash
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node --input-type=module - <<'NODE'
import { main } from '/workspace/work/brand-story-20261025/branding-pr1860-tool/tools/video/cli.mjs';
process.exitCode = await main([
  'assemble', '--slug', 'story-everyday-moleskine-c03-remake-20261025',
  '--workdir', '/workspace/work/brand-story-20261025/media',
  '--intro-after-condensation',
], { root: '/workspace/work/brand-story-20261025/c03-submission-root' });
NODE
```

若是已有成片、仍未核准、需要採用 current 的狀態，preflight 與 assemble 同時加 `--adopt-branding`，
交由原生保護規則判斷能否採用；不能刪批准或用 `--force` 換 pin。
正常首次成功合成後才產生 `branding.json`。合成後必須實讀 `checks.branding`、總格數、實際輸出、
片頭前後接點、片尾音畫、字幕與章節；總格數應為實際 body frames +780。
隨後做八語包裝與正常 QA，保留新 final SHA，依既有流程送待人工審看，不能沿用舊成片核准。

若正式站日後換包，這份 policy 會故意拒絕；先重新核對正式來源並留下新的實讀收據，再更新本批要求。
不能直接借 sothatswhy 包、拉長／循環 canonical clip，或把舊 candidate 冒稱正式 v4。

## 本次完成界線

本次 unique reused files = 2；dry-run 和 install 各下載同一組兩檔，未新增 provider 素材。
`generated_story_media = 0`、`paid_requests = 0`。正式 branding 身份與取得、安裝、格式 QA 已完成。
真正故事 TTS、正文 measured duration、畫面、配樂、整片 render、final QA、八語成片與送審仍由主批次接續，
必須先通過各自 admission／budget／內容前提；branding 通過不代表付費製片獲得新授權。

## 合成入口強制檢查

本批 [runtime-cli](../runtime-cli.mjs) 的 `assemble` 現會先執行[必要素材守衛](required-assembly.mjs)：強制使用已驗證的媒體根、在真正assembly前核對正式站與兩個實檔，並補上 `--intro-after-condensation`。錯誤包、缺包、錯媒體根或核對失敗都不呼叫assembly；只有操作方明給 `--adopt-branding` 才傳遞，不自行重綁舊cut。[隔離守衛檢查](assembly-guard-check.json)只使用模擬預檢程序結果，不呼叫供應商或真正組片；真正檔案與正式站核對另有本頁原生收據。這不解除預算、TTS、來源、時長或final關卡。
