# 前兩集繁中動畫：隔離管理員操作手冊

2026-10-02。這份文件是待執行的交接，不是部署、後台核准或生成收據。現在**動畫 0 秒**；144.86 秒／159.05 秒是兩集實際 WAV 編排的聲音預演。E1「姐。」重錄後的 measured edit 已複製至本目錄，草案記錄的是該版檔案雜湊。任何後续重錄、剪輯或腳本變更，都要重新綁定。

操作權威是 [scoped_drama.py](../../../../../ops/video/scoped_drama.py) 的 `Manifest` schema 和實際檢查，配套 [42 個離線測試](../../../../../apps/api/tests/test_scoped_drama.py) 已通過 Ruff、mypy 及獨立覆核。PostgreSQL 真實鎖、供應商地域／可用性與成片品質尚未 live 驗證。

執行前再核對並行 PR #1132／#1139 的最新 head 與實際 API image；本兩集維持既定 profile，不切換 #1139 的 `long-anime-v1`，也不為此修改 shared core。

[scoped-production-manifest.draft.json](scoped-production-manifest.draft.json) 是**不可執行草案**。外層 `execution_enabled:false`、說明欄位及內層尚空的 review IDs／影格 hashes，均不符合 live schema；它也不能通過一般 preview。只可作為填寫依據，不可刪掉草案標記就送出。

## 範圍與目前缺口

只允許 `wedding-reckoning-competition-e01`、`wedding-reckoning-competition-e02`；兩集 voice slug 不是動畫 production slug。本輪不做 E3。先完成完整繁中全片與 CC，使用者本人確認後才開始外語工作，包含實作。

全域 `drama_enabled` 維持 **OFF**，不啟用 worker 或其他作品 queue。Runner 只建立 transient settings clone，固定 Gemini Pro Image、Veo 3.1 Lite 1080p／8 秒／16:9、Lyria 3.5；不改資料庫設定，不降成 720p 或切其他影片模型。配樂原開關需已開；同作品圖片 override 若不同於固定模型會拒絕。

目前仍缺可用 SSH 主機位址／連接埠及本執行環境對該目的地的 TCP 網路授權；尚未連線。金鑰可用性不是網路連通證明。正式操作另需可連 PostgreSQL／Redis、可讀現有有效供應商設定和 media store 的管理員執行環境。配對 video token 不能取代主機操作權限，也不能授予管理角色。

原作品最新 setting／outline／chapter 1 和本輪兩集的 script／look／storyboard **尚未有一組經此手冊核對的真實 approved receipts**。提交為 pending 不等於批准。Runner 不建立或代填這些批准；缺少任何本次請求所需的實際核准就停止。

兩集完整劇本已經正常後台送審並讀回：E1 review `b909e8f3-0cfd-4488-b323-1d81dbaa0dce`、E2 review `e0c54172-1349-40fa-b29f-0da3422e84cb`，均為 **pending／decided_at=null**。入口：[E1 待審](https://mokaair.com/zh-TW/admin/videos?video=wedding-reckoning-competition-e01)、[E2 待審](https://mokaair.com/zh-TW/admin/videos?video=wedding-reckoning-competition-e02)。草案保留真實 IDs，沒有把它們寫成核准。

## 81 鏡、預算與階段

| 項目 | 本輪依據 |
| --- | --- |
| E1 | 原 42 鏡；S35 併 S34、S39 併 S38後，40 個實測剪輯窗口。保留原 `source_ids`，不重編場景 ID |
| E2 | 41 個實測窗口 |
| 首輪影片來源 | 81 × 8 秒＝648 生成秒；648 × US$0.08＝**US$51.84** |
| Pilot | `phase:pilot`，僅 E1；目前首 15 窗口共 51 秒聲音編排，15 × 8 秒來源的純 Veo 首輪估 US$9.60 |
| 後續兩集 | `phase:episodes`，E1 剩餘 25 窗口及 E2 41 窗口；已採用 pilot 鏡頭沿用，不再買一遍 |
| 人工登記費用預留 | `manual_reserve_usd` 至少 **10**；涵蓋原 US$5 預留，不再相加。這是配音、HTTP judge 等場外用量的額度，不是人工薪資報價或已知帳單 |
| 上限 | Pilot 累計 **US$100**；本輪兩集累計 **US$350，包含 pilot**。全案 US$4,000 總帽仍在，runner只管本輪，不能藉此動用剩餘總額 |

US$51.84 只是假定每窗首輪一份合用 Lite 片段的 catalog 估算，不含角色圖、關鍵影格、judge、配音、配樂或重拍；不是發票。兩組合鏡仍須真實動作成立，若拆回原兩鏡，首輪 Veo 估價增加 US$1.28，記明原因後重新評估。

Runner 將已知 job、失敗／未知嘗試和 durable reservation 保守納入曝險；供應商或 service 將 estimate 歸零，不等於已證實退款。manual reserve 同時計入 pilot 與 batch，歷史已記錄高值不能降低。一般 HTTP judge／TTS 不會自動逐筆匯入 runner；操作員須記到 [cost-ledger.csv](../cost-ledger.csv)，並在場外曝險超過預留前提高下一份 reviewed manifest 的預留。實際 USD 未有供應商帳單時保留未知，不填零。

`phase` 由每個 request 明確指定。**工具不會自動從 pilot 進入 episodes，也沒有用影片品質判斷解鎖的能力。** 操作員先完成角色圖、首鏡和代表 pilot 的驗收，才製作下一份 `phase:episodes` manifest。不能提早將 pilot 費用標為 episodes 來避開 US$100 子額度。

## 檔案與真實核准的對照

所有 Artifact 路徑均相對於 `--artifact-root`；完整 bytes 的 SHA-256 必須一致。禁止絕對路徑、`..` 或跳出根目錄的 symlink。私有 bundle 可保留 repo 相同的 `docs/videos/...` 結構，再加 `reviews/e01/`、`reviews/e02/` 存實際送審 artifacts。媒體與供應商收據放 repo 外。

| schema 欄位／檢查 | 必須使用的真實來源 |
| --- | --- |
| `source` | `docs/videos/series-plans/binge-five-20260928/wedding-reckoning/source.mjs`；raw SHA `ef8b5993221a3c065850eb326e7259ea7688457267188b31c2a725aedd2d29f3` |
| 原 source object | `SHA256(JSON.stringify(source))`＝`37328fa1c643e0edfcd1d138a158410653b36d6e02739ce7a9c555b26bc5bb9c`；它與上一列 raw file SHA 不同 |
| E1 `script` | `docs/videos/series-plans/competition-20261002/pilot/episode-01-screenplay.md` |
| E2 `script` | `docs/videos/series-plans/competition-20261002/episodes/episode-02-screenplay.md` |
| E1／E2 `edit` | 本目錄 `episode-01-measured-edit.json`／`episode-02-measured-edit.json`；不是舊 planning edit 或 voice-only video.json |
| `series_documents` | 原 `wedding-reckoning` 最新 setting 0、outline 0、chapter 1 的真實 `VideoDramaDoc.id`；每份 `status=approved`、有 `decided_at`，原 series 必須 `active`，paused／finished 不放行 |
| series `body_sha256` | Runner `canonical_hash({"body_md": doc.body_md, "body_json": doc.body_json})`。用 DB／正常後台回傳的原值，不改空白；不是 MD 單檔 hash。已批 setting 的 `production_design.source_binding.source_sha256` 必須是上述 source object SHA |
| episode `script` review | production slug 的 `VideoProject`：`format=drama`、`series_slug=wedding-reckoning`、`episode_number=1/2`，且未 dropped；`VideoReview.gate=script` 的內容 hash 對到本集上述 script bytes |
| 每個 `look` review | 同 production project、`subject` 是該上鏡角色 ID，真實已選 `choice` 經 `payload.options[].file_role` 對到 `files[].sha256`，並對到該 look artifact 的候選 |
| `storyboard` review | 同 production project 的真實關鍵影格 manifest；`shots[scene_id].sha256` 對到本次 `first_frame`；使用末幀時 `end_frame.sha256` 也一致，本鏡 `needs_review=false`、非 incomplete，review payload 同樣列明本鏡已無待修項 |

每個 request 的 `characters` 必須完整等於 measured edit 本鏡 `data.characters`。畫外發聲者不因此成為入鏡角色；肩膀、手等可見人物仍按已定稿的 visible cast 處理。`payload.shot_id` 使用小寫 `scene_id`，如 `wr-e01-s34`，不是大寫 `WR-E01-S34`。每鏡 motion／camera 必須與該 edit 對齊；不能只用其他鏡已批的 frame 過關。

同 gate／subject 若有更晚的 pending 或 rejected review，舊 approved review也不可用。修改任何 look／storyboard artifact bytes 都需要新 hash 和相應真實核准。

### 逐角色 look artifact：避免既有送審碰撞

現有 CLI 可對各角色送相同 `characters/manifest.json` hash，但後端同內容去重未把 `subject` 納入；不可假設一次 look push 已得到全部角色的獨立 review。此批採**每角色各一份內容不同的實際 look artifact**：例如 `reviews/e01/looks/zhitang.json` 的 `characters` 只包含知棠候選，`chengchuan.json` 只包含承川候選。每份實檔雜湊、候選圖及 `subject` 經正常送審介面提交，得到其自身真實 review ID／choice／核准，再由 runner 引用。不是只為改 hash 添加無關字元，也不直接插入 approved DB rows。

送審後逐角色讀回核對 ID、project、subject、artifact hash、選中候選與狀態；若發生碰撞就停止，修正正常送審資料。E2 可重用已驗收圖片 bytes，但仍需 E2 production project 自己的真實 look reviews，不能冒用 E1 的 review ID。

共用流程問題另由 [角色 look 審核識別票](../../../../../tasks/open/2026-10-02-keep-character-look-review-identities-distinct.md) 追蹤；本輪逐角色實檔送審不修改 shared core。

目前 runner 的所有 `image.references`，不論標作 character、style 或 previous_frame，其 SHA 都必須是本次附上的 look reviews **已選候選圖**；一般 style frame、上一鏡圖或沒被選的候選不能換個 role 就當 reference。Runner 不會自動補齊人物 refs。Lite `clip.references` 必须為空；首末格走 `first_frame`／`last_frame`。

## 從草案建立 live bundle

1. 鎖定當輪 script、實測 edit，重新計算檔案 hash，逐一核對 edit 的 `source_binding.source_object_sha256` 和 `screenplay_sha256`。兩集 artifacts 每一版都要 pin，即使當次只做 E1 一張圖。
2. 以正常後台流程送審並取得上述原作品與本次所需 gates 的真實核准。資料只有 pending 時保留 pending；不得把 UUID 填上就當 approved。
3. 依階段另存一份符合 `Manifest` 的 JSON。只保留 `schema_version,campaign,locale,source,series_documents,episodes,budget,requests`；不要帶 draft 外層欄位。所有 ID、SHA、prompt、圖檔都須已存在且經該階段審查。
4. **角色設定圖／style_frame／music 先需原文件及本集 script；keyframe 再加本次上鏡角色 look；clip 再加本次 storyboard。** 一次可只列一個 request。不要把尚未生成影格、未審 gate 或 null placeholders 混入 live manifest：`read_manifest` 會檢查全部 request 列出的 review artifacts，未選中的也一樣。
5. Keyframe prompt 以本鏡 `data.prompt` 開頭並含原 camera；clip prompt 以 `data.motion` 開頭並含原 camera，再補該鏡已核定造型方向。完整 payload、seed、negative prompt、phase 都受 manifest 的 raw SHA 綁定，審閱後不得默默改。
6. 圖片須經既有 media 上傳介面放入相應 production slug 的 media store；只放 review store 或本機檔案不夠。不要用 voice slug 代替 production slug。
7. 完成 live preview 後保存輸出的 manifest SHA、request SHA、settings SHA、operation 與保守費用，再由管理員使用這個**已審閱的 digest**執行。重算新 digest 並不能代替重新審閱內容。

取得 schema 的離線指令，在 repo 根目錄執行；不連 DB 或供應商：

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python ops/video/scoped_drama.py --schema
```

## 管理員 preview 與單一請求

以下是**後續管理員操作示例，尚未執行**。先完成 SSH host／port、網路路徑與主機授權；照 [prod-host-ops](../../../../../.agents/skills/prod-host-ops/SKILL.md) 及其連線規則進入主機，不在此文件假造 SSH endpoint。正式 repo 慣例路徑 `/root/travel_scanner` 仍須進主機核對。

下列命令假定：已審 runner 位於該 repo、既有 API image／PostgreSQL／Redis 已可用且相容、私有 bundle 已放在操作員設定的 `WEDDING_BUNDLE` 路徑，並可供 API 的 UID 10001 讀取。不要為執行本工具自動 build、pull、重建服務、啟動 migrate 或 workers；若這些前提不成立先停止。Compose `run --no-deps` 只開一個一次性管理程序，沿 API 既有環境及 media volume，掛入的 runner／bundle 都唯讀。

```bash
cd /root/travel_scanner
# WEDDING_BUNDLE 由管理員設為實際已審私有 bundle 的絕對路徑。
# 以下 stage manifest 只含本階段已齊備的 artifacts/reviews。
docker compose -f docker-compose.prod.yml run --rm --no-deps --pull never \
  -v "$PWD/ops/video/scoped_drama.py:/review-runner.py:ro" \
  -v "${WEDDING_BUNDLE:?set the reviewed bundle path}:/review:ro" \
  api python /review-runner.py \
  --input /review/manifests/pilot-look-reviewed.json \
  --artifact-root /review --request pilot-e01-look-zhitang
```

沒有 `--execute` 就是 preview：讀真 DB 和實檔核對，不呼叫 provider、advance job、reserve 或写 audit。若 `ADMIN_EMAILS` 恰有一個帳號，工具在 API 環境內選取它；必須仍是 active、未刪除／停權且有效能力同時包含 `content.manage`、`settings.manage`。若有多個，管理員透過私有 `WEDDING_ADMIN_EMAIL` 變數加入 `--actor-email "$WEDDING_ADMIN_EMAIL"`，不印出環境或秘密、不在公開文檔記實際 email。

管理員審閱 preview 後，才以其 digest 執行同一個 request；以下 `WEDDING_MANIFEST_SHA` 必须設定為該份**已審閱** manifest 的 64 字元 hash：

```bash
docker compose -f docker-compose.prod.yml run --rm --no-deps --pull never \
  -v "$PWD/ops/video/scoped_drama.py:/review-runner.py:ro" \
  -v "${WEDDING_BUNDLE:?set the reviewed bundle path}:/review:ro" \
  api python /review-runner.py \
  --input /review/manifests/pilot-look-reviewed.json \
  --artifact-root /review --request pilot-e01-look-zhitang \
  --execute --expected-manifest-sha "${WEDDING_MANIFEST_SHA:?use the reviewed preview digest}"
```

設定圖選擇和首鏡 keyframe 經真實 look／storyboard 核准後，建立新 `pilot-first-clip-reviewed.json`；先用下列命令 **preview**：

```bash
docker compose -f docker-compose.prod.yml run --rm --no-deps --pull never \
  -v "$PWD/ops/video/scoped_drama.py:/review-runner.py:ro" \
  -v "${WEDDING_BUNDLE:?set the reviewed bundle path}:/review:ro" \
  api python /review-runner.py \
  --input /review/manifests/pilot-first-clip-reviewed.json \
  --artifact-root /review --request pilot-e01-s01-clip --first-shot
```

確認後以這份新 manifest 的已審 digest，對同命令加 `--execute --expected-manifest-sha "$WEDDING_MANIFEST_SHA"`。**這次首鏡是可能計費的生成，不是免費地域檢查。** `--first-shot` 只限制 pilot clip，不核對它是否真為故事第一鏡，也不判斷畫質。操作員需指定草案中的 `wr-e01-s01`，保存原 job／operation，確認地區與模型可用，驗片後再進下一鏡。每次最多送一請求或 poll 一次，不會自動跑下一鏡。

## 續取、失敗與交付

| Runner 狀態 | 操作 |
| --- | --- |
| `submit_once` | 首次新請求；先持久記 reservation，再沿既有 submit_job／meter／store 送出 |
| `resume_poll` | 已 submitted 且有 vendor reference；使用同 manifest／request 繼續取回，不加購一份。按供應商正常輪詢間隔，避免緊密迴圈 |
| `return_ready` | 直接回傳既有 job ID／file SHA，不再次生成 |
| queued、unknown 或 reservation 無 job | 停止；即使可能在真正 vendor 呼叫前就被 quota 擋下，也不自動清除 reservation。先核對原紀錄／供應商 operation，不換 request ID 或 seed 規避 |
| failed／expired | 同 request 永不自動重送。必要重拍要記具體缺陷、終態 prior job 的 `retake_of`、`retake_reason`，真正修改 seed／prompt，另存新 reviewed manifest；仍計原 paid／unknown 曝險 |
| 別的 campaign request 正 pending | 先 resume／reconcile 那筆；不另開新的生成 |

全批使用 dedicated connection 的 session advisory lock，跨 service commit 保持；對普通 HTTP 的同 request 競態亦拒絕服務隱含重試。輸出的前後 global settings hash 應一致，全域 drama 仍 OFF。未知／不合規金額不能當零，逾時不刪 audit 來重試。

`ready` 只表示媒體工作回來，不是驗收。另用 ffprobe 實測回傳尺寸／fps／時長，做正常 judge、人工看臉／年齡／頭紗／道具／手部／動作／連續性與可剪性檢查。固定 8 秒是送出參數，非工具已驗證輸出。保留乾燥中文角色人聲與其他音效／配樂，丟棄 Veo 原生音訊，禁止停格補長；再按實測剪輯、完成繁中混音與可關 CC。

每一版保存 manifest bytes／digest、source/script/edit hashes、真實核准 receipts、request hash、job ID、attempt、生成秒數、保守費用與後續帳單／採用理由。Pilot 確認後才以新 reviewed manifest 進 `episodes`；前兩集完片後重新估算全片成本。此 runner 不會自動剪片、對嘴、做 CC、多語或上架；這些仍按既有繁中製作與交付流程完成。
