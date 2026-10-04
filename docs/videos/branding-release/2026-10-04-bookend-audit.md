# 長片片頭、片尾與原縮圖稽核（2026-10-04）

站主指出〈DevDay 2026 的 25 項，你今天碰得到幾項？照方案分五張清單，這週就能做〉
沒有開頭與結尾動畫，要求確認每支影片，並指定補動畫後上傳 YouTube 仍用原本縮圖。

## 稽核範圍與證據界線

2026-10-04 台北時間 12:31 完成正式站唯讀盤點：76 支影片，包含 61 支長片與
15 支 Shorts。依每支最新 final 審核、附件 SHA、branding hash、換版收據、
publish 狀態及 YouTube 身分判讀；61 支長片均成功取得，沒有請求失敗。
原始回應及媒體證據保存在 Git 外，不把憑證或私人操作紀錄寫入本報告。

| 判讀 | 數量 |
| --- | ---: |
| 已有最新 final 審核的長片 | 36 |
| 其中 final 已核准／待審 | 33／3 |
| 最新 final 有 branding 綁定 | 23 |
| 其中有 branding 且已核准／待審 | 20／3 |
| 最新 final 沒有 branding 綁定 | 13 |
| 尚無 final 的長片 | 25 |
| 有 YouTube ID 紀錄的長片 | 11 |

「沒有 branding 綁定」表示站上缺少該版片頭片尾的來源證明，單憑這個欄位
不能斷言影片每一格都沒有動畫；「有綁定」也不代替逐片播放驗看。
主機另以 canonical 媒體存在狀態與 checks 交叉核對：八支既有完成影片的 checks 也無 branding
（七支已有 YouTube 紀錄，加上已撤銷的 `wordpress-7-1-2-version-check`），
`claude-opus-5-5-three-numbers` 則有 branding。這次未下載重看全部 YouTube 版本。
Shorts 依既有規格不自動套長片片頭片尾；尚無 final 的 25 支不能列為已完成動畫。

## 每支最新 final 的站上快照

hash 顯示前 12 碼。YouTube 欄只代表有無已回填 ID，不以 stage 名稱推論已上架。
publish 欄的 `superseded` 是保留的舊包，**目前無有效上架包**；`無` 表示未找到
publish 審核。下表是本次修改前快照，候選成片與新的送審結果另記於末節。

| slug | branding hash | 最新 final | YouTube ID 紀錄 | 有效 publish／最新歷史 |
| --- | --- | --- | --- | --- |
| openai-devday-2026-recap | 無 | approved | 無 | approved |
| sothatswhy-t27 | 047ff12a4888 | approved | 無 | approved |
| shorts-poster-blind-long-v1 | a27622022d8d | pending | 無 | 無 |
| sothatswhy-t26 | a27622022d8d | approved | 無 | approved |
| shorts-prompt-check-long-v1 | a27622022d8d | pending | 無 | 無 |
| free-vs-paid-ai-plans-2026 | a27622022d8d | approved | 無 | superseded |
| shorts-receipt-total-long-v1 | a27622022d8d | pending | 無 | 無 |
| ai-price-war-gpt-6-sol-vs-opus-5-5 | a27622022d8d | approved | 無 | superseded |
| ai-real-world-03-machine-internet | a27622022d8d | approved | 無 | 無 |
| ai-real-world-02-confident-errors | a27622022d8d | approved | 無 | 無 |
| ai-real-world-06-digital-yesman | a27622022d8d | approved | 無 | 無 |
| ai-real-world-05-uneven-abilities | a27622022d8d | approved | 無 | 無 |
| ai-real-world-04-tasks-and-jobs | a27622022d8d | approved | 無 | 無 |
| ai-real-world-01-image-trust | a27622022d8d | approved | 無 | 無 |
| ai-real-jobs-chart | a27622022d8d | approved | 無 | superseded |
| openai-agents-broke-in | a27622022d8d | approved | 無 | superseded |
| why-openai-killed-sora | a27622022d8d | approved | 無 | superseded |
| rtx-spark-local-ai | a27622022d8d | approved | 無 | superseded |
| always-on-agent-explained | a27622022d8d | approved | 無 | superseded |
| ai-agents-explained-what-they-cost | a27622022d8d | approved | 無 | superseded |
| siri-ai-ios-27-how-to-get-it | a27622022d8d | approved | 無 | superseded |
| vibe-coding-first-website-2026 | a27622022d8d | approved | 無 | superseded |
| google-vids-free-ai-video-omni-1-1 | a27622022d8d | approved | 無 | superseded |
| meta-anti-scam-2fa-passkey | 無 | approved | 有 | approved |
| gemini-connected-apps-permissions | 無 | approved | 有 | approved |
| claude-opus-5-5-three-numbers | 0e1274bf0277 | approved | 有 | approved |
| google-vids-omni-free-quota | 無 | approved | 有 | approved |
| wordpress-7-1-2-version-check | 無 | approved | 無 | approved |
| openai-cursor-wind-down-nov-12 | 無 | approved | 有 | approved |
| gpt-6-sol-luna-where-to-use | 無 | approved | 有 | approved |
| enisa-threat-landscape-2026-denominator | 無 | approved | 有 | approved |
| openai-academy-learning-paths | 無 | approved | 有 | approved |
| gpt6-vs-opus55-worth-paying | 無 | approved | 無 | approved |
| ai-agent-permissions | 無 | approved | 有 | approved |
| gemini-student-offer | 無 | approved | 有 | approved |
| chatgpt-ads-upgrade | 無 | approved | 有 | approved |

12:31 修改前快照中，13 支缺少 branding 綁定的完成長片裡，10 支已有 YouTube ID，另兩支
`wordpress-7-1-2-version-check` 與 `gpt6-vs-opus55-worth-paying` 已撤銷。
因此仍有效、未記錄上傳而且缺少綁定的完成長片只有 DevDay。
已上傳影片與已撤銷影片不在這次重製候選範圍內。

## DevDay 原因、素材與縮圖保留

DevDay 的本機 producer 工作根目錄在首次製作時沒有 `_branding/current.json`。
目前 `selectBrandingForBuild` 對找不到預設素材的新長片允許回傳無 branding；
既有成片則刻意保留原選擇，不因後來安裝 current 而自動換版。
因此安裝預設會修正之後的新片選擇，但已核准的 DevDay 必須使用獨立換版流程。

已將主機驗證過的全頻道素材安裝到該 producer 的影片工作根目錄，回讀為：

| 項目 | 驗證值 |
| --- | --- |
| 素材 id | mokaair-brand-package-v2-cc |
| branding hash | a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd |
| 片頭 | 150 格／5 秒 |
| 片尾 | 90 格／3 秒 |
| 片頭 SHA-256 | 50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d |
| 片尾 SHA-256 | 8d9546a6042bdc30e0ac597d4eb1452d9e84edc588424027df8f7378ccecf6b1 |
| 原核准 DevDay final SHA-256 | 01deb03e57d1010e234da402dc64137bda329df92a1b04e85120441ada2245ab |
| 原 DevDay thumbnail SHA-256 | 49ddfda07a3c7ac95a00920ac27a385c51e8afef32ba4ceed9de9561940f721b |
| 原縮圖格式與大小 | JPEG，225168 bytes |

原 DevDay final 與 publish 審核的 thumbnail 附件 SHA 相同。
新候選在 Git 外獨立目錄保留原正文影像，接上 5 秒片頭與 3 秒片尾，
字幕延後 5000 ms，第二章起章節隨正文延後，首章保留 `00:00`。
候選不覆蓋 canonical 成片、原批准或原上架包；新成片需重新綁定與審看。

`assemble` 的 bookend 包裝不修改縮圖；`package` 原樣複製既有 `thumbnail.jpg`；
YouTube 同步使用有效 publish 的 `thumbnail` 附件 bytes。
此次候選保留原縮圖，後續上架包與實際送往 YouTube 的縮圖都必須核對上述原 SHA，
不得從新增片頭抽第一格當縮圖，也不得因重新 render 而換圖。

## 其他換版的交接與縮圖差異

17 支最新 final 已由站主核准的長片換版都記錄 150 格片頭與 90 格片尾，
但仍缺目前有效的 publish 包。11 支保留的舊 publish 已為 `superseded`，
其 final 附件指向舊成片；其餘六支未找到 publish。
介面只把 `status=approved` 的 publish 當作上架來源，所以保留歷史附件
不能視為已完成新版本交付。

後續來源綁定、canonical 採用、字幕／多語音軌與上架包重建由既有任務
[換版核准後交接](../../../tasks/open/2026-10-01-hand-off-owner-approved-renewed-finals.md)
追蹤；本次稽核沒有繞過它的來源與核准保護，也沒有啟用 uploader。

可比較前版縮圖的換版中只有 `free-vs-paid-ai-plans-2026` 出現差異：
目前 renewed final 的 thumbnail SHA 為
`d390a9f221c9dc5a1cd8208a78953beb36727cf973591e5d3e98e9f8a97ba9c1`，
舊 publish 為 `04c8753c66b31392eb1f2dba78cd8eceb54ad8e453c10796bca4e78a3d35406d`。
這是本次前就存在的差異；稽核不能單憑 hash 判定其先前改版授權。
依站主本次原縮圖要求，新的交接必須明確保留各片原上架縮圖的 SHA，
這支的差異需要在交接時對照既有內容改版證據處理，不自動採用最新審片縮圖。

## DevDay 候選量測與送審

候選 final SHA-256 為
`4c1041bb469cde7ba3047cbdf11e363045689cc73d25812d0273da88ba896514`。
完整 ffmpeg 解碼已通過；原 final 與原 upload/final 的 SHA 仍為上述原值。
獨立覆核確認全部 24061 個原 H.264 影像封包與候選第150格起的封包 SHA
逐一相同，正文 PTS 精確延後5秒；沒有重畫或重編正文影像。

候選共24301格，1920×1080、30fps，包含150格片頭與90格片尾。
格數換算810.0333秒，實際容器量測810.1000秒：原AAC尾端造成片尾接點前
最後正文畫面延長約87.5ms，片尾圖像較格數時間軸音訊開始約晚66.7ms。
正文首格精確位於5.000000秒，沒有片頭／正文空檔。
原版與候選實測響度均為 −14 LUFS、true peak −0.8 dBTP。
抽查2秒片頭、6秒正文與808.5秒片尾：金色大門、原黃色漫畫場景、
Mokaair Logo與按讚／分享／小鈴鐺依序正確，未見黑畫面或文字裁切。

161個字幕cue的322個時間戳全部精確延後5000ms，其餘SRT bytes相同。
七個章節標題與影片標題不變，章節時間依序為
`00:00 / 00:46 / 02:53 / 04:21 / 07:07 / 09:05 / 11:50`。
description只改章節時間；原縮圖與候選縮圖SHA逐byte一致。

2026-10-04 台北時間 12:53:58 已從後台「成片換版」提交；唯讀回查確認：

| 項目 | 提交後回讀 |
| --- | --- |
| 新 final review id | `101dc061-4b83-4845-9137-a9a71ff32d27` |
| 狀態 | `pending`，`manual_review=true` |
| final 附件 | 上述候選 SHA，899751255 bytes |
| preview 附件 | `45f5044f11b3199454cb15f29a88eb160ca66e47fbb0302d415404e3672e0edd`，90910404 bytes |
| thumbnail 附件 | 原 SHA `49ddfda07a3c7ac95a00920ac27a385c51e8afef32ba4ceed9de9561940f721b`，225168 bytes |
| zh-TW CC 附件 | `0412f69dc7299557cf0c609fdda6a242602425e75fa4667ab84397e861f9fe26`，14158 bytes |
| 原 final／publish | 皆保留為 `superseded`，原附件逐項未變 |
| YouTube ID／排程時間 | 均為 `null`，與提交前相同 |
| ready_to_upload | `false` |

後台已顯示新的 720p 成片待審卡與 13:30 片長，原縮圖仍為預覽 poster。
原語言選項保持：en／ja／ko 選 metadata、CC、dub；zh-CN 選 metadata、CC。
外部證據 `devday-site-after.json`、`devday-readback-proof.json`、
`devday-pending-review.jpg` 記錄實際回讀與畫面。

將本次 DevDay 回讀套入 12:31 的完整盤點後，36 支完成長片中有24支帶
branding 綁定（20已核准、4待審），12支缺綁定（10支有YouTube ID、2支已撤銷）；
沒有把新待審候選列入已核准的17支既有換版。
canonical換版與多語上架包交接另由
[DevDay補版交接](../../../tasks/open/2026-10-04-adopt-approved-devday-bookend-replacement-and.md)
追蹤，依賴既有來源綁定交接工具。候選通過量測並不等於已核准、已完成
上架包或已上YouTube。
