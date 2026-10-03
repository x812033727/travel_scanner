# 成本模型：每個常數的出處、逐層算例、雜湊失效表、估價與實際的落差

`SKILL.md` 的「錢怎麼算」是結論；這一篇是每個數字從哪裡來、怎麼算、哪裡會算錯。標籤：**工具規定**（程式碼常數）、**價目**（catalog 或官方頁，附查閱日）、**模型限制**、**量到的**（試拍）、**換算**（照上面的數算出來的，不是量的）。`episode_estimate.mjs` 的 `PRICES` 表以這裡為準，`tools/animation-production.test.mjs` 對照 `apps/api/app/video_media/catalog.py` 驗 API 價。

## 一、常數

| 常數 | 值 | 出處 | 標籤 |
| --- | --- | --- | --- |
| 圖 Gemini 3 Pro Image | US$0.134／張，1K 與 2K 同價；漫劇關鍵影格一律 1K（`stillPictures` 只有 slides 與 explainer） | `apps/api/app/video_media/catalog.py`（2026-09-28 讀 Google 價目頁）；`tools/video/media/keyframes.mjs:154-158` | 價目、工具規定 |
| 圖 Gemini 3.1 Flash Image | US$0.067（1K）／0.101（2K）；品牌故事與投影片用 | 同上 | 價目 |
| 圖 MiniMax image-01 | US$0.0035；一張參考圖，不保證同一張臉 | 同上 | 價目 |
| 片段 Gemini Omni 1.1 Flash（預設） | US$0.15／秒；4–10 秒整數；720p／1080p；3 張參考圖；原生音訊 | catalog.py（2026-09-26 讀） | 價目、模型限制 |
| 片段 Veo 3.1 Lite | US$0.08／秒；4／6／8 秒，1080p 只有 8（720p 貼需求選 4／6／8）；0 張參考圖；原生音訊必開；720p 官方價 0.05 但預算照 1080p 記。adapter 省略 Lite 不支援的 `negativePrompt`，把完整 `look.negative` 接成主提示的 `Avoid: …`（歷史失敗與修正在 `error-catalogue.md` #23） | catalog.py（2026-10-01 核對）；`apps/api/app/video_media/jobs.py:278-286`、`300-306` | 價目、模型限制 |
| 片段 Veo 3.1 | US$0.40／秒；4／6／8，1080p 只有 8；3 張參考圖；id 仍 `preview` | catalog.py | 價目、模型限制 |
| 片段 Veo 3.1 Fast | US$0.12／秒；同上 | catalog.py | 價目 |
| 片段 MiniMax H3 | US$0.13／秒（2K 的價；768P 官方 0.08，catalog 不分）；catalog 秒數 4–10、官方頁 4–15；9 張參考圖 | catalog.py；`platform.minimax.io` 價目頁（2026-10-03 讀） | 價目、模型限制 |
| 音樂 Lyria 3.5 | US$0.08／首；10–600 秒；SynthID | catalog.py；`apps/api/app/video_media/schemas.py:80` | 價目 |
| judge | US$0.01／次，記帳定值；真實成本是 Gemini 視覺模型的 token（DRAMA.md 寫「依 token」） | catalog.py `JUDGE_USD_PER_CALL`；`tools/video/media/stages.mjs:28` | 工具規定 |
| 一次 take 的上限 | 設定圖 `MAX_LOOK_ROUNDS` 2（`look.candidates` 2–4，lint，預設 3；`look --candidates` 1–6 只改這一次跑的張數，不進 `video.json`）；關鍵影格 `MAX_KEYFRAME_TAKES` 3（`--takes` 1–6）；素材 `MAX_CLIP_TAKES` 2（`--takes` 1–5） | `look.mjs:21`、`drama.mjs:107,282-283`、`keyframes.mjs:24,136`、`clips.mjs:36,164` | 工具規定 |
| 買的秒數 | `veo-3.1*` 配 **1080p** 固定 8；其他（含 Lite 720p）`clamp(ceil(frames/30), 4, 10)` 往上貼齊模型秒數表 | `clips.mjs:59-67`（`MIN_CLIP_SECONDS` 4、`MAX_CLIP_SECONDS` 10） | 工具規定 |
| 鏡長估法 | 每個字 0.24 秒（`DEFAULT_CPM` 250）、每句 0.3 秒、每鏡 0.7 秒；`action_seconds` 直接是秒數 | `tools/video/core/timeline.mjs:19-22`；`estimateTimeline` | 工具規定 |
| 參考圖 | 每張圖或片段最多 4 張（catalog 寫 Gemini 3 Pro Image 收 14，伺服器只放 4）；每張 ≤ 7 MB、合計 ≤ 20 MB | `schemas.py:32`、`keyframes.mjs:26`、`clips.mjs:39`；`jobs.py:74-75` | 工具規定 |
| 提示詞 | prompt ≤ 4000、negative ≤ 1000；judge 題目 ≤ 400、檔案 ≤ 6、題目 ≤ 12 | `schemas.py:33,52-53,120-131` | 工具規定 |
| 月預算 | 片段 3,000 秒、圖 1,500、judge 3,000、音樂 60；單支 US$200；`max_retakes_per_shot` 2；`judge_min_score` 7 | `apps/api/app/video_automation/models.py:86-93` | 工具規定 |
| 每小時 | 圖送出 240、片段與音樂送出 60、輪詢 900、judge 360、上傳 600、下載 600 | `apps/api/app/video_media/admin_api.py:73-78` | 工具規定 |
| 預算單位 | 片段以秒計，圖與音樂一張一首各 1；送廠商前預留，廠商拒收或判失敗才退 | `apps/api/app/video_media/meter.py`（`units_of`）；`jobs.py:366-384` | 工具規定 |
| 退不退 | 送出被拒、輪詢失敗、內容被濾：退；**生成成功但下載失敗：不退** | `jobs.py:480-489`、`532-548`、`558-607` | 工具規定 |
| 同一請求 | `(slug, request hash)` 一個 job；失敗 3 次後 409 `video_media_job_exhausted`；`submitted` 超過 24 小時 `expired` | `jobs.py:360-364`、`518-523`；`models.py` `MAX_ATTEMPTS` | 工具規定 |
| 試拍的保守預留 | 圖每張 0.134、片段每次 0.64、另加 manual reserve US$10；合計 US$15.18；`actual_billed_usd` null | `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md` §保守預留；`docs/videos/series-plans/competition-20261002/cost-ledger.csv` | 量到的 |

## 二、一鏡

一個有角色的 clip 鏡頭買四樣：關鍵影格（圖價）、它的 judge、素材（秒 × 單價）、它的 judge。公式：

```text
一次       = image + 0.01 + seconds × usd_per_second + 0.01
到上限     = 3 × (image + 0.01) + 2 × (seconds × usd_per_second + 0.01)
still      = image + 0.01           （到上限 3 ×）
data.source 切鏡 = 0               （帳本記 saved_seconds × usd_per_second）
end_frame  = + image                （不 judge；dry-run 多算了一次 judge，見第六節）
```

| 一鏡 3 秒台詞（90 格） | 買幾秒 | 素材一次 | 一鏡一次 | 一鏡到上限 | 利用率（換算） |
| --- | --- | --- | --- | --- | --- |
| Veo 3.1 Lite 1080p | 8 | 0.64 | 0.794 | 1.732 | 37.5% |
| Omni 1.1 Flash 1080p | 4 | 0.60 | 0.754 | 1.652 | 75% |
| Veo 3.1 1080p | 8 | 3.20 | 3.354 | 6.852 | 37.5% |
| Veo 3.1 Fast 1080p | 8 | 0.96 | 1.114 | 2.372 | 37.5% |
| MiniMax H3（catalog 價） | 4 | 0.52 | 0.674 | 1.492 | 75% |
| 同一鏡 6 秒台詞（180 格） | Lite 8／Omni 6／H3 6 | 0.64／0.90／0.78 | 0.794／1.054／0.934 | — | 75%／100%／100% |
| 同一鏡 1.5 秒台詞（45 格） | Lite 8／Omni 4／H3 4 | 同 3 秒 | 同 3 秒 | — | 19%／37.5%／37.5% |

**鏡頭切短不省錢**：模型有下限（Lite 1080p 8、其他含 Lite 720p 4），3 秒以下的鏡頭跟 4 秒同價。密度只在 `data.source` 與 still 上省得回來，而 `data.source` 可切的秒數是來源鏡頭**實際買到**的：Omni／H3 下 3 秒的來源只買 4 秒，回同一鏡位的第二鏡只剩 1 秒可切（`SKILL.md` 的切鏡槓桿）。

## 三、一集：60 鏡、3 分鐘、3 個角色、各 3 張候選、一首音樂

鏡頭數照 drama-craft.md 的目標（中位數 2.5–3.5 秒，編輯判斷）：180 秒 ÷ 3 ≈ 60 鏡。假設每鏡 3 秒（實際有長有短，Omni／H3 下 5–6 秒的鏡頭會買 6 秒，估價時用 `episode_estimate.mjs` 逐鏡算）。

| 階段 | 數量 | 一次 | 到上限 | judge 一次／到上限 |
| --- | --- | --- | --- | --- |
| `look` | 3 × 3 ＝ 9 張 | 9 × 0.144 ＝ US$1.30 | 2 輪 US$2.59 | 9／18 |
| `keyframes` | 60 張 | 60 × 0.144 ＝ US$8.64 | 3 次 US$25.92 | 60／180 |
| `clips`（clips 等級，60 clip） | Lite 480 秒／Omni 240／H3 240／Veo 480 | 39.00／36.60／31.80／192.60 | 78.00／73.20／63.60／385.20 | 60／120 |
| `clips`（hybrid，24 clip ＋ 36 still） | Lite 192 秒 | 15.60／14.64／12.72／77.04 | 31.20／29.28／25.44／154.08 | 24／48 |
| `clips`（stills，6 clip ＋ 54 still） | Lite 48 秒 | 3.90／3.66／3.18／19.26 | 7.80／7.32／6.36／38.52 | 6／12 |
| `music` | 1 | US$0.08 | 0.08 | 0 |
| **整集 clips 等級** | — | Lite **49.02**／Omni 46.62／H3 41.82／Veo 202.62 | Lite **106.59**／Omni 101.79／H3 92.19／Veo 413.79 | 129／318 |
| 整集 hybrid | — | Lite 25.62 | 59.79 | 93／246 |
| 整集 stills | — | Lite 13.92 | 36.39 | 75／210 |

- Veo 3.1 的 clips 等級一次就過 US$200：`capProblem`（`tools/video/media/ledger.mjs:96-101`）在每次送出前算「已花 ＋ 這次」，超過就 `MediaError`（who owner，結束碼 3）；前面的鏡頭已經買了。
- 旁白與配音：DRAMA.md 估「配音與音樂不到 US$1」，TTS 的字數走站上另一個額度（`automated.md` 一次性設定），這裡不算。
- 一個月（預設額度）：片段秒數是 Lite 的瓶頸（480／3,000 → 6 集；每鏡兩次 → 3 集）；judge 是重跑的瓶頸（下節）。

### 重跑的真實成本

`keyframes` 與 `clips` 的 manifest 綁雜湊（第五節）。雜湊一變，manifest 從空的重建，每一鏡走一遍：`stage.image`／`stage.clip` 先查 `media/cache.json`（key 含 prompt、negative、參考圖、seed、秒數），沒變的鏡頭 `reused: true`、不付錢；但接著 **judge 照做**（`keyframes.mjs:233`、`clips.mjs:350`），clips 還重跑 ffmpeg QC。所以：

| 改動 | 重買 | judge | 核准 |
| --- | --- | --- | --- |
| 一鏡的 prompt | 1 張圖 ＋ 1 份素材 | 60 ＋ 60 ＝ 120 次 ＝ US$1.20 | storyboard 重審 |
| 一句台詞（秒數沒跨整數秒，或 Lite） | 1 句 TTS | 60 次（clips） | audio 重審 |
| look.style 一個字 | 9 張設定圖 ＋ 60 張圖 ＋ 60 份素材 ＝ Lite 約 US$49 | 129 次 | look、storyboard 都重審 |

每小時 judge 360 次：一輪全集重跑佔三分之一小時的額度；一個月 3,000 次 ＝ 25 輪。這就是「攢齊再跑」的理由。

## 四、同一集放到三條路線

素材而已，不含圖與 judge（那兩樣只有伺服器路線有）。方案的月費、年繳、點數、隊列、頁面的每秒美元、條款、Kling 的會員表與開發者 API、MiniMax 的套餐**只寫在 `providers-and-plans.md` §1.2–1.4**（2026-10-03 讀官方頁，附網址）；這裡只留 60 鏡的換算。

**Hailuo**：頁面的 US$/s（Pro 以上 2K 0.081、768P 0.047；Standard 0.101／0.059）是用年繳價算的；由「秒數／月」反推，每個方案都是 **2K ≈ 12 點/秒、768P ≈ 7 點/秒**（換算）。用月費攤：Pro 一點 ≈ US$0.0122 → 2K ≈ 0.147/s、768P ≈ 0.086/s；Max 一點 ≈ 0.0074 → 2K ≈ 0.089/s。`SKILL.md` 三條路線表的美元全用月費攤；Max 的無限模式含哪些模型見 providers §1.2 的 Max 列。

| 60 鏡的素材 | 點數 | 佔 Pro 4,500 | 月費攤的 US$ | 年繳（頁面價）的 US$ |
| --- | --- | --- | --- | --- |
| H3 768P 每鏡 4 秒（H3 最短） | 240 × 7 ≈ 1,680 | 37% | ≈ 20.5 | ≈ 11.3 |
| H3 2K 每鏡 4 秒 | 240 × 12 ≈ 2,880 | 64% | ≈ 35.2 | ≈ 19.4 |
| H3 768P 每鏡 8 秒（跟 Lite 一樣） | ≈ 3,360 | 75% | ≈ 41.1 | ≈ 22.6 |
| H3 2K 每鏡 8 秒 | ≈ 5,760 | 128%：一集超過一個月 | — | — |

**Kling**（每支點數未驗，照 40 點／標準 5 秒算）：60 鏡 × 一支 5 秒 ＝ 2,400 點 ＝ Pro 3,000 的 80%、Standard 660 的 3.6 倍，月費攤 ≈ US$29.6；> 5 秒的鏡要一支 10 秒（約兩倍）。開發者 API 1080p ≈ US$0.112/s 無音訊 → 60 鏡 × 5 秒 ≈ US$33.6（未驗）。

**MiniMax API 直接打**（不經伺服器）：60 鏡 × 4 秒在 768P US$19.20、2K 31.20（官方 0.08／0.13 per s）；伺服器的 `minimax` adapter 就是這條（`apps/api/app/video_media/providers/minimax.py`），只是 catalog 一律照 2K 的 0.13 記；預付套餐「H3 not supported」。

## 五、雜湊失效表

| 雜湊 | 算什麼 | 出處 | 綁它的檔 |
| --- | --- | --- | --- |
| `lookHash` | 解析後的 look（preset、style、negative、motion、candidates、style_frames）＋ 每個角色的 id、appearance、sheet_prompt | `tools/video/core/drama.mjs:575-578` | `characters/manifest.json`、`keyframes/manifest.json`、`clips/manifest.json`、`checks.json` |
| `visualHash` | 縮圖 ＋ 每個場景的 id、template、chapter、`data` 全部、句子 id 與 reveal ＋ 選用的命名造型 | `tools/video/core/timeline.mjs:186-196` | `keyframes/manifest.json`、`clips/manifest.json`、`frames/manifest.json`、`checks.json` |
| `speechHash` | voice、用到的字典條目、角色聲音、`action_seconds`、每句的文字／停頓／speaker／emotion／發音提示 | `timeline.mjs:161-184` | `timeline.json`、`clips/manifest.json`、`checks.json`、`captions` |
| `mixHash`／`subtitlesHash`／`sfxHash` | music 的 gain／duck／fade／track；subtitles；sfx | `drama.mjs:591-604` | `music/manifest.json`、`checks.json` |
| 快取 key | 圖：provider、model、prompt、negative、尺寸、seed、參考圖；片段：加 seconds、resolution、首尾幀 | `drama.mjs:581-589` | `media/cache.json` |
| 關卡 | 檔案的 SHA-256：script.md、characters/manifest.json、keyframes/manifest.json、timeline.json、final.mp4、upload/metadata.json | `tools/video/core/approvals.mjs:28-47` | `approvals.json` |

改了什麼會重買什麼、哪個核准失效：只有一張表，在 `SKILL.md`「哪個改動會重買什麼」。這裡多兩條表裡放不下的：句子 id 改了等於換句（visualHash 與 speechHash 都變，storyboard 與 audio 都重審）；更改或清空 `look.negative` 走第一列，全部重買；Lite adapter 已保留 avoidance，不必為 #23 的歷史相容性失敗更改已核准的值。

重跑 `look` 或 `keyframes` 就算全部從快取拿回，manifest 的 `generated_at` 也會變（`keyframes.mjs:314`、`look.mjs:221`），關卡的 SHA-256 就不同 → `stale`。

## 六、估價與實際的已知落差

1. **end_frame 的 judge 多算**：`keyframes --dry-run` 每個 end frame 加一次 `JUDGE_USD_PER_CALL`（`keyframes.mjs:169`），但 end frame 畫了不判（263-266）。每個 end frame 高估 US$0.01。
2. **解析度不改單價，但改秒數**：`meter.py` 的 `usd_for` 只看模型的 `usd_per_second`；Lite 720p 官方 0.05 記 0.08、H3 768P 官方 0.08 記 0.13。可是 `clipSeconds` 的「固定 8 秒」只在 `veo-3.1*` 配 `1080p`：沒有 profile 的集把 Lite 設 720p，3 秒的鏡頭買 4 秒 ＝ 0.32，帳本是 1080p 的一半（有 profile 的集 `productionClipSizeProblem` 要原生 1920×1080，不能）。H3 降 768P 秒數不變，帳本也不變。
3. **下載失敗照收費但不在月總額**：`jobs.py:558-607` 下載失敗 `refund=False`（廠商已經生成），而 `month_usd` 只加 `submitted` 與 `ready` 的 job（`meter.py`），失敗的不算。廠商帳單會比站上的月總額多這幾筆。
4. **judge 的 0.01 是定值**，真實是 token；每月 3,000 次的額度是次數，不是錢。
5. **Kling 每支點數未驗**；`episode_estimate.mjs --plan kling:*` 用 `--credits-per-video`（預設 40）算，印出時標未驗。
6. **H3 的秒數**：catalog 4–10、官方 4–15；`clipSeconds` 照 catalog 貼齊，超過 10 秒的鏡頭 lint 本來就擋。
7. **試拍的預留不是花費**：US$15.18 含 manual reserve 10；兩筆失敗的 Lite 片段 `usd_estimate` 0 但預留保留；`actual_billed_usd` null。報帳時三個數分開寫：預留、估價、實際帳單。
8. **外部片段**：`clips import` 在帳本記一筆 `status: "imported"`（點數與秒數；美元只有 `--usd` 給了才有），`status` 標出匯入幾支；`run_report.mjs` 把它們與買的分開列，指令落地前手放的（manifest 有、帳本沒有）也列成 external。
9. **利用率沒人記**：manifest 有 `needed_s` 與 `seconds`（`clips.mjs:396-398`），`run_report.mjs` 相除；試拍沒跑 `clips` 階段，沒有這個數。
10. **`max_clips_per_video`（預設 40）**：`media-status` 印得出，2026-10-03 在 `jobs.py` 與 `tools/video` 都沒找到擋它的程式碼。60 鏡的集會不會被擋，沒驗。
