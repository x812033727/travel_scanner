# C03 Moleskine｜上架就緒讀回（2026-10-24）

站主 2026-10-24 要求「補足品牌故事目前缺的，讓它可以上架；該有的規則、片頭片尾都要有」。本機工作區裡
四支「日用品的意外轉身」（C03–C06）只有 C03 Moleskine 做到插畫、字卡、配樂、縮圖都齊，因此這份讀回
以 C03 為對象，逐項核對品牌故事的規則、頻道片頭片尾，並列出到「可以上架」為止還缺的每一步。

**結論：C03 離上架包只差一句付費重錄（`c031202`，28 個計費字元），其餘素材與規則都已到位；
但這一句被 C 系列的付費保留擋在四層（工作區 `STOP`、三個本機 client、正式站 API），
本讀回沒有解除任何一層，也沒有送出任何付費請求。** 解除是另一張票的事（見最後一節）。

## 讀回的版本

| 檔案 | SHA-256 / 讀值 |
| --- | --- |
| `docs/videos/story-everyday-moleskine-c03/video.json` | `3b12bff0ab09a5827330c25121048912fefee014ec9134df582cff511a755109` |
| `script.md`（站主 2026-10-22 核准的那一版） | `5f148061a2fa4bb89a42b1d91adfa67a6bad4796ee5a44b82f1eea473722cb46`，與工作區 `approvals.json` 的 `script` 關卡相同 |
| `brief.md` | `6e2666b5ce66bfe098b31ff0426496127258adae0185b4e1458f88bde0229671`，與 `approvals.json` 的 `outline` 關卡相同 |
| 工作區 | `<home>\mokaair-work\videos\story-everyday-moleskine-c03\`；`STOP` 仍在（2026-10-22 預算保留） |
| `timeline.json` | speech hash `a23505d0a1da1c09`，94 句；只有 `c031202` 的文字是舊的「七十八家」 |
| `_branding/current.json` | `mokaair-brand-package-v4-endscreen`，hash `416c8768…a63e88`，2026-10-13 安裝 |

## 工作區裡已經有的

| 階段 | 讀值 |
| --- | --- |
| 旁白 | 94 句 WAV（Gemini Sulafat，2,587 計費字元）、`narration.wav`；93 句與現行稿一字不差 |
| 自動聽檢 | 94/94 查過，6 句旗標（`c030201`、`c030501`、`c030505`、`c030604`、`c031101`、`c031802`），都在文字沒改的 93 句內；五句 Jev 快取讀回在工作區 `review/jev-five-readback-20261024.md`（repo 外） |
| 插畫 | 73 張 `shot`、評審全過（`state.json` 最後一輪 `needs_review: []`），媒體帳本結算 US$1.713 |
| 字卡 | 21 張 `stats` 已渲染（`frames/`），每張只放一個數字、名字、引文或出處 |
| 配樂 | `music/5846379f92e64064.mp3`，Lyria 生成 174 秒（manifest 寫 600 秒是工具要求的長度，見 [配樂循環預檢](music-loop-precheck.md)） |
| 縮圖 | `thumbnail.jpg`，`thumbnail.data.brand: "Moleskine"`（左上大字品牌名） |
| 浮水印 | `watermark.json` v1 已採用 |
| 關卡 | `outline`、`script` 兩關已核准（本機 `approvals.json`）；旁白、分鏡、成片、上架都還沒核准 |

`node tools/video/cli.mjs status --slug story-everyday-moleskine-c03 --workdir <home>/mokaair-work/videos`
（2026-10-24）：brief、outline、script lint、fact-checked、script approved、keyframes、frames 打勾；
`narration synthesized: timeline.json was built for an older script` 起全部未完成。

## 規則逐項核對（brand-story skill §站主定案）

| 規則 | 現況 | 證據 |
| --- | --- | --- |
| 畫面：MiniMax `image-01`、`look` 只有 `{"preset":"cute-mystery"}` | 符合 | `video.json` 的 `look`；媒體帳本的圖片模型是 image-01 |
| 長度：約 10 分鐘、正文至少 8 分鐘 | 估 10.2 分鐘；舊時間軸第 2–20 段純語音 481.25 秒 | `lint` 估時；[音訊製作讀回](audio-production.md)。**重錄後要重量**，差距只有 1.25 秒 |
| 鉤子：每 30–45 秒一個、`loops` 至少 8 個 | 21 條 `loops`；lint 的 `TIGHT_CADENCE` 0 errors、0 warnings | `node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03`（2026-10-24） |
| 開場：第一秒在具體場景、30–60 秒停在問題上 | 第一章 6 句、估 38 秒，最後一句是「這本空白本怎麼把舊外形變成今天的生意？」 | `video.json` 第 1 章；lint 的章節時間 00:38 |
| 片頭：5 秒頻道片頭放在開場濃縮之後 | 會自動落在第 2 章開頭（估 00:38） | `tools/video/core/branding.mjs` 的 `defaultIntroAt`：`kind: story` 是 narrated long → `after_first_chapter`；`series.json` 的 `kind` 是 `story` |
| 片尾：21 秒 v4 結束畫面片尾 | 本機已安裝 v4 包 | `_branding/current.json`；`intro.mp4` sha256 `50a53efa…0bb67d` 150 格、`outro.mp4` sha256 `00eb9ccc…834396` 630 格，`ffprobe -count_frames` 讀回 1920×1080、30 fps、150／630 格，與 manifest 一致 |
| 結尾三句：回答開場的問題、留言題、有理由的訂閱邀請 | `c032001`–`c032002` 回答、`c032003` 留言題、`c032004`「想繼續從日用品看懂品牌怎麼做生意，歡迎訂閱」 | `video.json` 第 20 段 |
| 旁白不講下一支是什麼 | 符合 | 第 20 段沒有預告 |
| 字幕：不燒字幕、繁中 CC 一定有 | `subtitles.burn_in: false`；CC 由 `captions` 步驟產生（還沒跑） | `video.json` |
| 外語配音：站主成片後手動勾 | 尚未到這一步 | — |
| 縮圖：左上大字品牌名、不畫商標 | `brand: "Moleskine"`；插圖提示詞沒有商標、可讀字、真人長相 | `video.json`；[逐鏡畫面規格複核](visual-final.md) |
| 圖裡不能有 `names` 的名字 | lint 0 errors（故事規則） | `series.json` 的 `names` 9 個；lint |
| 奇聞檔案局畫面規則：插畫 ≥ 70%、連續卡片 ≤ 3 | 73／94 = 77.7%，最長連 2 張卡 | [奇聞檔案局規則重剪複核](curio-rules-recut.md) |
| 吉祥物 | 沒有（`characters: []`） | `series.json` |
| 預算：整片 US$25 | 已結算 US$1.713（媒體）＋ 2,587 字 TTS ＋ Jev 27 句；本讀回沒有新花費 | `media/ledger.json`、`state.json` |

## 到「可以上架」還缺的每一步

依序，每一步都要在工作區沒有 `STOP` 檔、付費保留解除之後才跑得動（第 1 步就是付費）：

1. `tts`：只重錄 `c031202`「到 2016 年底，已有七十九家直營店，也把銷售搬上網。」
   2026-10-24 乾跑：`94 requests, 1 to synthesize; about 28 billable characters now`，
   伺服器 `voice gemini:Sulafat ready`，Gemini 本月還剩 6,937,825 字。重錄後時間軸與 `narration.wav` 換新 speech hash。
2. `check-audio`：重跑逐句檢查；再由能播放原始 WAV 的人聽六句舊旗標、`c031202`、`c031301` 的「四成一」與外文名稱，
   確認後才核准旁白關卡（本機 `approvals.json` 的 `narration`）。量第 2–20 段純語音是否 ≥ 480 秒。
3. 分鏡關卡：73 張插畫與 21 張卡已過評審，站主看過聯絡表後核准 `storyboard`。
4. `clips`：靜態插畫的運鏡片段，不付費。
5. `music`：檔案已在快取（key `5846379f92e64064`），只重新綁定 mix hash，不重買；
   生成的 174 秒比成片短，依 #1825 在組片前把檢查過的循環記下。
6. `assemble`：採用本機 current（v4 包），片頭自動插在第 2 章開頭、片尾接在正文後；成功後工作區寫 `branding.json`
   （`intro_at: after_first_chapter`）。
7. `captions`：繁中 CC（SRT／VTT），時間軸含片頭偏移。
8. `qa`：含品牌片頭片尾、完整解碼、響度、字幕時序；配樂三個接縫要實際聽。
9. 成片關卡：站主看片後核准 `final`。
10. `package`：上傳包（MP4、縮圖、說明欄含四條來源、標題自動加「｜品牌故事」）。
11. 站主私人上傳；在 YouTube Studio「片尾」→「從影片匯入」選 `oxEtlA8GWas`，把三個元素拉到影片結束前 17 秒，
    用播放器實點驗證（[BRANDING.md](../../BRANDING.md) §結束畫面片尾）。
12. 語言：站主在影片頁勾選後才做外語配音；之後重新 `package`。

## 卡點：付費保留在四層，這份讀回沒有動任何一層

| 層 | 位置 | 行為 |
| --- | --- | --- |
| 工作區 | `STOP` 檔（2026-10-22「historical Gemini and media charges are not attributable…」） | 每個階段做完手上那一單位就退出 |
| 本機 client | `tools/video/core/pending-pilot-budget.mjs` 的 `isPreproductionHeld`（整個 `story-everyday-` 前綴）；`tts/cli.mjs`、`media/client.mjs`、`automation/client.mjs` 送出前就丟 `video_budget_preproduction_hold` | 乾跑可以，真跑不行 |
| 正式站 API | `apps/api/app/video_budget/models.py` 的 `PREPRODUCTION_HOLD_SLUGS`（C03–C06 未對帳、C07／C10／C15 無帳戶）；`video_automation/ai.py` 的 `is_preproduction_held` | #1782（2026-10-23 20:18 +0800）已在 2026-10-24 部署的 `c9cbf0022` 裡 |
| 設計文件 | `apps/api/app/video_budget/PENDING_EVERYDAY.md`：先對帳供應商帳單、每片一個帳戶（0138 已把 C03 列成 `pre-ledger-history` 的 `uncertain` 保留列）、再以**另一個審過的變更**解除 client 與 API 的保留 | 「這份文件、綠的 PR 或建了帳戶，都不等於可以付費、刪 `STOP`、上傳或發布」 |

因此第 1 步的那一句（約 28 個計費字元）現在從本機跑不動，也不能用不帶 `video_slug` 的請求繞過
（PENDING_EVERYDAY.md 明文禁止）。解除要做的事在票
[`2026-10-23-reconcile-c-series-prior-charges-and`](../../../../tasks/open/2026-10-23-reconcile-c-series-prior-charges-and.md)：
讀供應商帳單把 C03 的歷史花費釘死（或站主決定以 US$25 全額保留結案）、部署 0138 之後的對帳、
再出一個只解除 C03 的審過變更並部署。解除之後，上面 12 步由票
[`2026-10-24-c03-moleskine-finish-to-upload-package`](../../../../tasks/open/2026-10-24-c03-moleskine-finish-to-upload-package.md) 接手。

## 其他三支的位置（同一工作區）

| 集 | 有什麼 | 缺什麼 |
| --- | --- | --- |
| C04 Bubble Wrap | `outline`、`script` 核准、空的 `audio/` | 旁白（供應商 429 後沒再錄）、全部畫面、配樂 |
| C05 Kincho | 79 句旁白、`check.json`、離線 Whisper 旗標清單 | 站主音訊核准、全部畫面、配樂 |
| C06 Play-Doh | 94 句旁白、`check.json`、試聽 MP3 | 站主音訊核准、全部畫面、配樂 |

三支都要買圖，都在同一個付費保留之下；保留解除後也先做 C03。
