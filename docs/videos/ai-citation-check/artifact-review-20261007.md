# 實際合成產物與關卡綁定覆核

**實際本機 draft 綁定 PASS；原生整體 QA 仍為 false（9/11），沒有音訊、最終影片或上架批准。** 覆核者 `language_review_contract` 只讀實際完成收據、檔案與原生純函式；沒有合成、TTS、ASR、judge、來源 API 重試、review API、Git 或批准操作。此次唯一寫入為本紀錄，不代表站主播放／聆聽驗收。

下文 `OP` 是 `<home>/mokaair-work/ai-teaching-continuation-20261007`，`DRAFT` 是 `OP/render-preview/ai-citation-check`，`REFERENCE` 是 `OP/media/ai-citation-check`。後者保留付費原始音訊與未知請求；前者是免費本機預覽，不帶批准或 provider journals。獨立主要媒體讀取為 `2026-10-07T10:01:01.364Z`，QA 完成後的收尾再核對為 `10:04:55.187Z`。

## 真正完成的操作與結束碼

| 實際操作 | 留存收據與時間 | 結束結果／界線 |
| --- | --- | --- |
| 最後 native assemble | `OP/logs/20261007T095154Z-draft-assemble.exit.json`；`09:51:54.610559Z` 開始、`09:58:09.065994Z` 結束，PID 44800。收據 SHA `03e178b1324027b18e5a8e2b9c39c45b0ab7667a1b9114198a11f2f7a3b8db17`。 | 實際 exit 0；2/36 segments 重編，其餘重用；native log 記錄 18,596 frames、−14 LUFS、true peak −1 dBFS，373 秒。這是免費本機合成完成。 |
| 無憑證 native diagnostic QA | `OP/render-preview/diagnostic-qa-proof.json`；`10:00:27.921Z` 開始、`10:01:06.251Z` 結束。proof SHA `fbde1735a2b3055eadea1f819a9e8828f6838d97c99238f059279cca6284d92f`。 | proof 記錄 native main 返回 **3**；主操作者另觀察外層 exec shell 的非零結果為 **1**。兩層結束碼分別記錄：3 是本輪缺少批准／無憑證的原生結果，1 是外層執行失敗呈現；本覆核直接讀到的是 main=3 的持久 proof，沒有把 shell=1 冒充 native code。 |
| 免費 native review | `OP/logs/20261007T100123Z-draft-review.exit.json`；`10:01:23.703383Z` 開始、`10:01:27.508668Z` 結束，PID 19340。收據 SHA `93dbc9beeb92fbe42be240051e7034fe5a79bc20d0bc85caa9ba035a7ff4128e`。 | 實際 exit 0，產生 `DRAFT/review/audio.html` 與 `final.html`。生成聆聽／觀看頁面不等於有人使用它們或接受內容。 |

## 實際影片、音訊與視覺

`DRAFT/final.mp4` 為 91,117,107 bytes，SHA-256：

`fdc4afbcee830e7990805c89dbf0424fc067efc62d6a295abd17f66354410ca5`

獨立呼叫本機 ffprobe 實測容器 619.900000 秒（10 分 19.9 秒）；H.264 影片 1920×1080、30/1 fps、18,596 frames、619.866667 秒；AAC 音軌 48,000 Hz、stereo、619.900000 秒。畫格數精確符合 timeline 的 18,596；音訊封裝結尾比影片長約 0.033 秒，原生 probe／組裝檢查無 drift 問題。這是檔案／串流檢查，沒有實際播放或逐秒聆聽。

原生純函式核對現行 `speech_hash=399237f659e75fc5`、`visual_hash=471d44f874da92e5`，`checksCurrent` 為 true，checks.ok=true、problems 空陣列。checks 內的 narration SHA 與 timeline、實際旁白檔均為：

`350294298b58308fb5a4e05b12a5cf6f131be371d8639f4b79569c98d8c7cf81`

獨立 native `audioEvidenceProblems` 核對 DRAFT 與 REFERENCE 全部 143 個 raw WAV／旁白的完整 SHA 和 WAV sample count，兩者問題都為空。timeline byte-identical，旁白完整 SHA 相同。合成完成後另用 `assembledAudioProblems` 核對當前 checks 對應同一旁白，問題為空。這只證明音訊身分與長度，不是發音正確或音訊批准。

當前 checks 記錄 −14 LUFS、true peak −1 dBFS、108 個 PSNR 比對樣本通過；render 純函式確認 67 個 slide states，無 layout／glyph／font 問題，包含源稿縮圖。QA 的 pace 為最長 14.9 秒、沒有超過 15 秒。數值檢查不取代站主對畫面、字幕與聽感的驗收。

## 關鍵檔案的完整 SHA

下表均為 DRAFT 的實際當前檔案；不是上一輪 assemble 的殘留 checks。QA 的 `final_sha256` 等於上述 MP4，proof 的 report SHA 等於當前 qa.json，收尾讀取再次一致。

| 檔案 | bytes | SHA-256 |
| --- | ---: | --- |
| `checks.json` | 17,598 | `f0fbcb30c16447d875e77f30818d029ab7872cc368a34eea30dd601a23a7f7df` |
| `review/qa.json` | 1,639 | `930f7a607ac3f29ecc2aabd319448c00628b3be123c4eceb5c357d5d76e5802c` |
| `review/metadata-draft/metadata-draft.json` | 7,823 | `014459f94b52a86e2e40a122fe65640fa539a7b70c00903b7e4e532aa6d98b22` |
| `timeline.json` | 47,060 | `3ef9c3e53d35f4192ca8207220ce2b4f0809e10cada127c20ac8a68665d841b5` |
| `frames/manifest.json` | 44,709 | `09eb29ba7b2efb51862fd46087631a8722fa809a0dc2b1e5677518518785e4f7` |
| `frames/cache.json` | 3,477 | `961a98bf5ec69e99a452714e1c0699973ea4aacc87d23a119a5dce7587cc951d` |
| `captions/manifest.json` | 540 | `04d475193658e8c9e19fe5b45bef080cfff7e585e8db26848076c73adc89aa8f` |
| `review/audio.html` | 53,268 | `87869b3e6a05d29fbbb2b26cbc2b078032d7a85d7d0ef27389d84601fa922d8c` |
| `review/final.html` | 25,937 | `6d1c3985cf1f290235b5a2a326faf0862defbed20cab3efcd782038161fb99ca` |

主操作者另外把上述 metadata draft 原始 bytes 放入 repo 的 [metadata-draft-20261007.json](metadata-draft-20261007.json)，方便 PR 直接讀取。`2026-10-07T10:08:46.921Z` 本覆核獨立讀取 repo 副本與實際 DRAFT 原件：兩者均為 7,823 bytes、SHA `014459f94b52a86e2e40a122fe65640fa539a7b70c00903b7e4e532aa6d98b22`，完整 byte comparison 相同。它是可審閱的同一份 draft metadata；檔案位置改變沒有使其成為 native upload package。原四語審稿的 18 個釘選保持有效，不改寫那些原紀錄。

目前 source 是 `video.json` SHA `ba96bc7d5d1cc5d6fd20172064baefabd2bb319b00ba67387b02b4e90c5e3423`。獨立再核對 `language-review-20261007.json` 的 18 個來源／四語翻譯／查核文件／五語 SRT／metadata draft／timeline 釘選，全部仍相同；沒有因 assemble 或 QA 改掉既有 source_hash 或審稿身分。metadata draft 的來源檔案 SHA 亦全 current；實際六章、五語第一行文章 CTA、字幕與四語審稿的詳細證據維持原紀錄。本份不重寫那些既有審稿或宣稱出現正式 upload 包。

## Diagnostic QA 的準確含義

實際 qa.json `ok=false`，九個通過項是 assemble、render、pace、captions、metadata、facts、links、thumbnail、disclosure；兩個未通過項如下：

- `narration`: `the narration has not been approved yet`。DRAFT 與 REFERENCE 的原生 `approvalState(audio)` 都是 missing；DRAFT `approvalState(final)` 亦 missing。
- `policy`: `no video tool token yet: run node tools/video/cli.mjs login`。這是主操作者刻意隔離的無憑證 context，policy **未執行**，不是實際帳號憑證失效或真實 judge 判了不合格；本紀錄不要求為診斷 context 登入。

獨立讀 `OP/diagnostic-qa.mjs`（2,301 bytes，SHA `c666496ad64f273badbf9d6513e12eb36799be818a3aa1e91afdad29e2862142`）及原生 caller：CLI overrides 確實替換 env／home／fetch，wrapper 移除 `MOKAAIR_VIDEO_TOKEN`，檢查隔離 home 的 credential file 不存在，`automationClient` 沒有 token 即在建立 paid policy request 前拒絕。另 injected fetch 只准 GET／HEAD，拒絕所有寫入 method。實際 QA 收據的 policy 為上述未執行狀態；本覆核只檢查隔離 credential 檔不存在，沒有讀取任何 token。

因此 proof 的 `paid_policy_calls:0` 是 **guarded assertion，並與實際 observed unrun 相符**；它不是 instrumented request counter，也不是帳戶用量或本片過去所有付費操作為零的證明。實際這輪只用 public fetch 查兩個連結，links 項通過。無憑證的 false policy 不可被改寫成通過，也不能拿原生 main=3 當成可以重試未知 ASR 的理由。

DRAFT 仍無 `approvals.json`、owner `languages.json`、`review/languages.json`、`dubs/manifest.json` 或 `upload/metadata.json`。publish 的原生狀態是 absent；metadata item 的通過與 `review/metadata-draft` 的完整文字檢查，不等於正式 package、選語或上架批准。免費 review HTML 的 exit 0 同樣沒有產生任何批准。

## 已保留的未知付費請求與 STOP

收尾讀取確認 REFERENCE 的 STOP 仍是原 bytes，SHA：

`c309e6e472ee224e570ef06afb5d0a12dc0edf618f29d2a5d357557243e2993a`

未知 ASR key `5f7cbb48ab7a326474e12293c3748be97720963d6bdbf619f3177362a929c037` 的 schema-1 sent receipt 仍為 339 bytes，SHA `301f66c5d2c8e50a52cdcd6e29c3a6381372b9095279bd0d10ce389e2128f9d9`，sent_at `2026-10-07T09:07:25.020Z`，沒有 answer 或 confirmed siblings。DRAFT 沒有複製 provider journal。

REFERENCE `review/check.json` SHA `63560b283fe060b31eb1c8cc2dd09a621ed6103d4abe28e5a7bfecba976bfa88` 保留 68 筆 heard，原生 `currentAudioCheck` 確認這 68 筆都屬當前 clip；未知 `ci037` 沒有 heard。check-flags 檔不存在不能被解讀成 143 句都完成語音查核。09:56 的本機 node process snapshot 只有已知免費 assembler、沒有 native paid producer；後續完成收據如上。無新增 provider 回答或 cost resolution，先前 `runtime-preflight` 的 unknown／不重試界線不變。

本份可供主操作者收攏當前本機審閱包證據。它不解除 STOP、不忘記或重送未知請求、不填補 native audio／policy／final／publish 關卡，也不記錄站主尚未提供的聆聽、播放或接受結論。
