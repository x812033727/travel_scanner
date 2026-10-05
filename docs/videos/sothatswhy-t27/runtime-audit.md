# T27 正文與成片實測稽核

判定：**PASS_CURRENT_FINAL_AND_BODY_OWNER_ACCEPTANCE_PENDING**。查核時間 2026-10-02T15:58:22.865Z，查核者 facts_t27。正常正文、成片、字幕、十一項 QA、四項上架包檢查及後台附件綁定已閉環；站主完整播放、字幕播放器切換與追加語言選擇仍未由本稽核證明，YouTube ID 為 null，未發布。

| 目前綁定 | SHA256 |
| --- | --- |
| video.json | `89d7d0fb16acfb196d5f19f6f9cc96a776b69b08234a492f1d3e8fd7078d494c` |
| 文字事實收據 | `fff4ae7c5bdac4beaaf8ce6b56253527836ced4024bd6f9a52efbf0e25582eda` |
| READY art manifest | `260ed6f4a37ce2199e8ef563fc0de0b4d92bd3368b67b89d5d4809927b538bda` |
| 原獨立 BODY 收據 | `88e9d72f4579b61d9a9f7ae142f7772419f76db428257c65a5485c235637b0d3` |
| final.mp4 | `3894c35e2cd5860d0b834c1ba02578986600c15e1e4ce53d59d0b95f1e993016` |
| upload/metadata.json | `0b391df71413e3ea5ef4307b4984d332dd81174e43af5fc98b92e4ed0abe79d3` |
| 本次成片閉環收據 | `b57d237ca6388663a2697973eae81bdb5efba46d0a17633e86c6f29509a991e8` |

2026-10-05 補記：倉庫是公開的，本稽核、`runtime-audit.json`、`fact-source-audit.json` 與 `visual-review.json` 內的本機使用者路徑已改為 `<home>`，其他內容不變；上表「文字事實收據」的 SHA256 因此改為遮蔽後的 fact-source-audit.json（任務 2026-10-05-scrub-local-user-paths-from-the）。遮蔽前的檔案與原雜湊見 commit bc5f18db8（#1144）。

## 實際成片與正文

重新讀取 ffprobe -count_frames 解碼目前 final.mp4，1920×1080、H.264／AAC；正文格線 nominal 30 fps，實際 r_frame_rate／avg_frame_rate 為 30/1／103220/3441。讀取前後的 current source、收據、媒體與短檔案 snapshot SHA 均相同。沒有修改影片、設定、核准或增加付費請求。

| 項目 | 實測 |
| --- | ---: |
| 逐句 clip 聲音合計 | 533.270000 秒 |
| 品牌片頭格數／nominal 格線長度 | 357 格／11.900000 秒 |
| 正文格數／nominal 格線長度 | 20197 格／673.233333 秒 |
| 品牌片尾格數／nominal 格線長度 | 90 格／3.000000 秒 |
| 實際影片串流 | 20644 格／688.200000 秒 |
| 實際封裝總時長 | 688.200000 秒 |
| 實際音訊串流 | 688.200000 秒 |
| 片頭實際 packet PTS 區間 | 0.000000–11.900000 秒／11.900000 秒 |
| 正文實際 packet PTS 區間 | 11.900000–685.200000 秒／673.300000 秒 |
| 片尾實際 packet PTS 區間 | 685.200000–688.200000 秒／3.000000 秒 |
| 成片中正文狀態 | 137 景 |
| 成片中最長／平均狀態 | 6.800000／4.914599 秒 |
| 成片中超過八秒 | 0 |
| 成片中圖解占正文 | 94.741270% |

逐句原始 WAV 共 533.270000 秒、正文 673.233333 秒、成片 688.200000 秒，均達至少 480 秒；片頭與片尾沒有用來補正文門檻。原 BODY 收據已核對 137 個 WAV／ASR clip hash／cache key，0 flags，正常 audio/outline gate current，buildTimeline 與旁白 PCM 逐位元重建相符。原 BODY 明細保留為不可變 snapshot，不重寫當時 FINAL_PENDING 的歷史判定。

actual packet PTS 對 body 與 final 全部 137 景核對，正文開始在成片 11.900000 秒、結束在 685.200000 秒。本稽核另讀 actual final 全部 packets，逐景起訖與 sync 收據相符且完整連續；成片正文 PTS span 673.300000 秒，比 nominal frame grid 673.233333 秒多 0.066667 秒。最大景起點偏差 0.040365 秒；body 檔實際 PTS span 673.192968 秒，較格線 -0.040365 秒。保留這些測得差異，沒有寫成零偏差或推定原因。成片平均 <=6 秒、最長 <=8 秒、圖解占比 >=50%。opening／middle／last_spoken_line 三處 narration→body 與 body→final 共六次 PCM 波形比對均 correlation >0.98，偏移誤差不超過 1/6000 秒；這是取樣聲音對時，未稱人工完整聽看。

## 字幕、核准與上架包

繁中 CC 共 137 cues，依目前 presentationTimeline 含片頭偏移 11.900000 秒重建。SRT／VTT 與重建文字逐位元一致，上架包中的繁中 SRT 也相同；未以檔案檢查冒充播放器 CC 選取驗收。

| 正常 gate | 目前狀態 | 綁定 SHA256 | 核准時間 |
| --- | --- | --- | --- |
| outline | approved／current | `25afc729f4c2243d98eedac3e1e2134b411da10a3b178e225e1734bb5201e62b` | 2026-10-02T12:49:59.344Z |
| audio | approved／current | `8e662e6faefb04b1d4c661f907affc983322d82eab752f8c4da1243e6814fc9e` | 2026-10-02T14:29:08.671Z |
| final | approved／current | `3894c35e2cd5860d0b834c1ba02578986600c15e1e4ce53d59d0b95f1e993016` | 2026-10-02T15:47:34.810Z |
| publish | approved／current | `0b391df71413e3ea5ef4307b4984d332dd81174e43af5fc98b92e4ed0abe79d3` | 2026-10-02T15:51:28.516Z |

正常 review/qa.json 為 11/11 PASS，綁目前 final SHA；正常 readPackageReport 為 4/4 PASS，綁目前 metadata SHA。上架包 final.mp4 與受核准 final 位元組相同，caption／描述／縮圖／揭露答案皆由正常 package 檢查讀取。沒有建立或跳過 gate。

後台只讀證據確認 final review cab3a243-7d28-433e-bca1-a0a4de07e247 與 publish review 2922dac4-fd3a-438c-9614-128ddadd1cc2 都 approved，且 publish 的 final attachment SHA 是目前影片；YouTube ID null、on_youtube false、locales_decided_at null。這證明後台附件與當前包相符，不將此視為 YouTube 已上架。

畫面查核保留137景初審與3修景重看的完整 lineage，visual-review.json current SHA `ef00f9439db65104f6f779ec7211d439efe956af6340c712699351fc1e42638a` 綁 source／art／frame bytes，並加入實際 final 15樣本的獨立實看。這是圖形語義覆核，不是人工聲音或站主完整播放。

2026-10-05 補記：上段 visual-review.json 的 SHA 是本機使用者路徑改為 `<home>` 後的值，其他內容不變（任務 2026-10-05-scrub-local-user-paths-from-the）；遮蔽前的檔案與原 SHA 見 commit bc5f18db8（#1144）。

品牌定案紀錄 SHA `43387f2d864d334a68dec480e3979c8e3169e153ad2d49fff3ad9488112d6f55` 及 owner-approval.json SHA `1247033a80b19e52cf59967dd55acb8aa3728634a8012eca57d95dc752fd9c80` 明列站主選用固定多語系列片頭；選定 intro／outro byte SHA 與本集 pin／實際媒體完全一致。片頭中的 English／美國為14國／地區穿插的一張品牌卡，不表示本集旁白／CC語系；本集仍是繁中旁白與繁中 CC，沒有因此選取額外語言。素材選用紀錄與本集 final/publish gate、站主完整播放驗收分開。

實際 final 解碼的 15 張取樣由 root 實看，未解問題 0；樣本 manifest、所有 PNG 與實看收據雜湊相符。這是取樣畫面確認，不是站主完整播放。

## 可追溯收據

- body：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-runtime-independent-body.json`，SHA256 `88e9d72f4579b61d9a9f7ae142f7772419f76db428257c65a5485c235637b0d3`
- final_audit：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-final-audit.json`，SHA256 `3d5ad153b104373edc3b5317d7601a4503eb3f4a252b14219adcb731411948c5`
- sync：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-sync-readonly.json`，SHA256 `0929e30144989b987f72e4816e3479aca78429b82b5ebe751bf6f3593e4e883e`
- remote_proof：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-remote-delivery-2026-10-02T15-52-00-323Z.json`，SHA256 `bdc2f89fed065da15a9436a01a77c4fc138ea83e270bce2d7fd3a34867585c10`
- samples_manifest：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-final-samples\manifest.json`，SHA256 `97e262f85fd4af745cb8ba959f40ec86d9ab62d1ab4b287d0e5386bb91d0785f`
- sample_review：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-final-stills-review.json`，SHA256 `f223318f99da7df7b8c41b4a1da397e6b3ec768aa131c3040d7e2f65247a811d`

閉環完整 JSON：`<home>\.codex\visualizations\2026\10\01\01a0f5cd-1f4c-7f91-9af1-b02370fcce78\t27-runtime-final-closure.json`，SHA256 `b57d237ca6388663a2697973eae81bdb5efba46d0a17633e86c6f29509a991e8`。之前正文摘要與 Markdown 原封不動保存在 repo 外 t27-runtime-body-summary-before-final.json/md。

**owner full-play／player CC acceptance／owner language choice／YouTube upload/publication = PENDING**。human_final_full_play=false，owner_full_playback_confirmed=false，owner_language_choice_pending=true，youtube_video_id=null，published=false。
