# C03 Moleskine｜上架包收據（2026-10-25）

站主 2026-10-24 決定：「解除 C03 的付費保留（本機 client 與 API 只放 C03）、部署，然後重錄 c031202 並一路做到
上架包。C03 的歷史花費以 US$25 全額保留結案。」這份收據記下從解除到上架包的每一步與讀回；
前一天的規則核對在 [upload-readiness-20261024.md](upload-readiness-20261024.md)。

**結果：上架包已在本機 `<home>\mokaair-work\videos\story-everyday-moleskine-c03\upload\`，`status` 到「upload package」打勾；
還沒上傳。站主上傳前請先看 `review/final.html`，並聽 `review/c031101-take2.mp3`（見下）。**

## 解除與部署

| 步驟 | 讀回 |
| --- | --- |
| PR #1832（squash `11e23a876`） | `ACTIVATED_STORY_SLUGS = {story-everyday-moleskine-c03}`：API `is_preproduction_held` 與本機 `isPreproductionHeld` 對 C03 放行，C04–C07、C10、C15 與其他 `story-everyday-*` 照舊保留 |
| 部署 | 2026-10-24 16:26–16:29Z，`DEPLOY_EXIT=0`、3/3 健康、alembic 0139（無新 migration）；驗證 13/13，含專屬兩項 `api-c03-activated`（c03held=False c04held=True c08held=True activated=1 held=6）、`worker-c03-activated`（[false,true,1]） |
| 主機結算 | `reconcile_cli --slug story-everyday-moleskine-c03 --operation-id pre-ledger-history --action settle --expected-status uncertain --actual-usd 25 --evidence-ref owner-decision-20261024-c03-full-ceiling`，先乾跑再 `--apply`（16:30:25Z）；讀回 `historical_closed_usd 25.000000`、`remaining 25.000000`、`admission_held false` |
| 工作區 `STOP` | 改名 `STOP.removed-by-claude-20261025`，檔尾註明原因 |

## 旁白

| 步驟 | 讀回 |
| --- | --- |
| `tts` | 1 句合成（`c031202`「七十九家」，28 計費字元）、93 句沿用；speech hash `0fcff03acf93ed47` |
| 純語音 | 第 1 章 31.74 s；第 2–20 章 **481.02 s**（≥ 480） |
| `check-audio` 第 1 次 | 94/94，`c031202` 通過；六句舊旗標照舊（`c030201`、`c030501`、`c030505`、`c030604`、`c031101`、`c031802`） |
| `tts --redo` | 六句各重錄一次（184 計費字元） |
| `check-audio` 第 2 次 | 63 逐字、9 近音、15 Jev 通過、6 由本機 Whisper 第二轉錄清除，**只剩 `c031101`**：兩次錄音 Gemini 都聽成「開展（的）那天」、上一輪 Whisper 聽成「開產那天」，三者都是「開場 chǎng」的近音；上市日與「四億八千八百萬歐元」兩個辨識器都聽對。判為辨識限制保留，MP3 留在 `review/c031101-take2.mp3` 給站主試聽 |
| 關卡 | `approve --gate audio`（timeline.json `6fead70ed499`，16:37:11Z）、`approve --gate storyboard`（manifest `3f0dbeaf9a20`） |

## 畫面、配樂、成片

| 步驟 | 讀回 |
| --- | --- |
| `clips` | 73 景全是靜態插畫，0 付費片段 |
| `music` | 既有 Lyria 檔 `5846379f92e64064.mp3` 實長 174.002 s，成片 607.533 s → 先被時長保留擋下；`music --loop` 記下 `stream_loop`、plays 4（#1825 的設計），沒有重買 |
| `assemble` | `final.mp4` **19,006 格**（633.6 s）、−14 LUFS、true peak −1.8 dBFS、音樂床 −33.6 LUFS；94 段 2,889 s 編完。`branding.json` pin：v4 包 `intro_at: after_first_chapter`、`intro_at_frame 1136`（**37.87 s**，第 2 章起）、150＋18,226＋630 格；hash `39d34ab0…eda64` |
| `captions` | zh-TW 112 則（含片頭偏移） |
| `qa` | **10/11**：assemble、render、narration、pace（最長 11 s）、captions、metadata（6 章）、facts、links（11 開）、thumbnail、disclosure 通過；**policy 沒過**：Jev「符合立場 0.74、留下觀察 **0.59**（門檻 0.6）、建議 0.02、業配 0.05、貶損 0.04」。同一份旁白的 policy 請求以收據去重（`video_budget_operation_reused`），不能再問一次；上架包不看這一項，成片關卡由站主親自看片決定 |
| 關卡 | `approve --gate final`（final.mp4 `915830a0969b`，17:39:29Z，註明 policy 0.59 與站主看片） |
| `package` | 4/4：`final.mp4`（sha256 `915830a0969b480225c5e4d655794489de29bcfd02cc15ad61a8de24187dc75b`，174,748,322 bytes）、`thumbnail.jpg`（`a4f1f7c3…f657faef`）、`captions/`、`description.zh-TW.txt`、`metadata.json`（`d0cb0a6f74c9`）、`UPLOAD.md` |

## 花費

主機帳戶讀回（2026-10-24 17:4xZ）：`historical_closed 25.000000`（站主結案）、解除後 **settled US$0.017682**（7 TTS、7 轉錄、2 Jev 判讀、1 policy），`remaining 24.982318`。媒體帳本未變：US$1.713（118 圖、122 評審、一首配樂）。

## 站主接下來

1. 看 `review/final.html`（片頭 37.87 s、片尾最後 21 s、三個配樂接縫約 174／348／522 s）；聽 `review/c031101-take2.mp3`。
2. 照 `upload/UPLOAD.md` 私人上傳 `final.mp4`、縮圖、繁中字幕；標題打包時自動加「｜品牌故事」。
3. YouTube Studio「片尾」→「從影片匯入」選 `oxEtlA8GWas`，三個元素拉到影片結束前 17 秒，播放器實點驗證。
4. `youtube-sync --video-id <id> --dry-run`；在影片頁勾語言後再做外語配音與重新 `package`。
