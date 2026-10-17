# AI 代理與聊天機器人：續作 V1 草稿收據

收據日期：2026-10-07；草稿首次 readback UTC 12:46:09。V1 檔案與 canonical QA 的讀檔快照為 UTC 12:37:26；V1 167 檔案核驗完成於 UTC 12:42:09。這份文件記錄 **639.4 秒的未核准 V1 草稿**，不是整條製作流程完成、音訊通過、站主接受或任務結案。V1 原始 142 個 WAV 與成片已保留；root 已安排後續六句 targeted 重錄，其實際結果不在本快照內。

路徑約定：`<repo>` 是本次 `codex/ai-agent-continuation-20261007` worktree；`<home>` 是使用者家目錄。製作根目錄為 `<home>/mokaair-work/ai-agent-continuation-20261007`，下文以 `<operation>` 簡稱。canonical 為 `<operation>/media/ai-agent-vs-chatbot`，隔離 preview 為 `<operation>/render-preview/ai-agent-vs-chatbot`。這些代號是可攜式文件路徑，沒有公開本機帳戶名稱或憑證。

## 目前階段與界線

| 項目 | 本快照所見 |
| --- | --- |
| 來源與文字 | 36 場景、142 句；歷史查詢／規劃日期與未實測步行、未查天氣界線已修正並獨立審稿。 |
| V1 旁白與時間軸 | 142 個實際 WAV；30 fps、19,182 frames、639.4 秒。 |
| 畫面 | 84 個實際 stills 與 320px 縮圖已有獨立視覺收據；不等於完整影片、過場或音訊驗收。 |
| 免費字幕草稿 | 五語共 719 cues；actual source、時間窗口、切分與 CPS 已覆核；不是五語 dub fit。 |
| Metadata | 五語、六章節的 source-bound 未核准 draft；不是正式 upload package。 |
| V1 初次 native 音訊檢查 | UTC 12:21:25：142 句、unchecked 0、14 flags，原 QA 已保留。 |
| 第二意見後 native 音訊檢查 | UTC 12:37:02：仍是同一批 V1 音訊，142 句、unchecked 0、8 cleared、6 flags，native exit 1。 |
| 本機 approvals | 只有 `outline`；沒有 narration、audio、final、languages 或 upload 核准。 |
| 語言選擇與發布 | `locales={}` 是 root 回報的既有 owner 狀態；未生成 dubs，未上傳或發布 YouTube。 |

此收據沒有呼叫 production/provider、沒有改 source、翻譯、media、cache、journal、STOP 或 approvals。音訊檢查結果、成片機械 `checks.ok=true`、metadata 欄位檢查及文字／圖片審稿各有自己的範圍，不能合併為「全部通過」。

## 接手與有限範圍的去重證據

接手前的 `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-ownership.json`，SHA `af97339478cfac5fe1c0e701f1bbb36e563d88c668255125501fc3e02da6410e`（3,505 B），記錄 UTC 11:05:15 的 scope `docs/videos/ai-agent-vs-chatbot`：實際 scoped `who-is-on-it` exit 0、沒有 active scoped task 或觸及該路徑的 open PR；30 個 worktrees 在該 scope 沒有未提交變更或未落地分支差異。當時 fresh remote main 是 `77a58c85a4912daad9a1d117364e5260d92a9cc6`；最後落地該 scope 的 commit 為 `ec383889f6d5ae582d07c350b5755899300aa4e7`（PR #867）。這是接手前的範圍快照，不是永久無衝突保證。root 後來於 UTC 11:09:17 認領既有 task `2026-09-27-general-audience-ai-agent-versus-chatbot`。

小型 archive inventory 為 `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-archive-inventory-20261007.json`，SHA `9b692aa5c25720424816a41b75474fcda570cb4ab6058500c5481869454ca682`（580 B），觀測 UTC 10:50:13。它記錄 `completed-roots.json`、`delivered-candidates.json`、`BACKUP-INDEX.json` 對本 slug 都無命中，指定 `video-upgrade-20261001/delivered-20261003-2010` 的 `completed-part-*.zip` manifest 無命中；當時 `<home>/mokaair-work/videos/ai-agent-vs-chatbot` 與 `<home>/mokaair-work/handoff/renewed-finals-20261007/ai-agent-vs-chatbot` 不存在。保留收據沒有 ZIP 掃描總數，因此本文件不宣稱已獨立驗證「29 archives」或全磁碟媒體不存在；也不混用 citation 影片的另一份 archive inventory。

## 可驗證的來源與查核 metadata

`<repo>/docs/videos/ai-agent-vs-chatbot/verify-2.md` 已逐句覆核全部 142 句、36 場景 data、metadata 與縮圖文字：23 CONFIRMED、2 已套用且 readback 的 CHANGED、117 OUT OF SCOPE。後者包含教學建議、自製示意與未有不可改寫 runtime 證據的歷史執行聲明，不代表它們都是外部確證。本輪四個 official primary URLs 的實際 GET 保存如下；access UTC 不等於出版日或 2026/9/27 的原始 request 時刻。

| 來源／publisher | 實際 URL | HTTP／retrieved UTC | 保存 HTML SHA-256 |
| --- | --- | --- | --- |
| Building effective agents／Anthropic | <https://www.anthropic.com/engineering/building-effective-agents> | 200／2026-10-07T10:50:35.553Z | `dd21017fd0dd6b72f020bbeaf69a3faf2ba7246c447144f452a34200e51ec3fe` |
| 開放時間與票價／國立臺灣博物館 | <https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444> | 200／2026-10-07T10:50:36.146Z | `b3477bef03781b7147b1f8a5ed25ded0cb1545e393a67f2cb23c5b592ee21653` |
| 2026 年節日開閉館公告／National Taiwan Museum | <https://www.ntm.gov.tw/en/News_Content.aspx?n=5713&s=251424> | 200／2026-10-07T10:50:41.115Z | `02c414a7607f8af3f3f498b13d2b93fa89c71196e364fa334dcb174d64d888a9` |
| 本館交通資訊／國立臺灣博物館 | <https://www.ntm.gov.tw/cp.aspx?n=5445> | 200／2026-10-07T10:50:38.710Z | `2d615b7e8b789f1e42e0cdfac64b16ad62177eedd287c978c97e543b4b7563f3` |

完整 request/retrieved UTC、HTTP、title、publisher、原 HTML 與可重算 text extraction 的 path／bytes／SHA，在 `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/collection.json`，SHA `36b3cbde3369ed8ac671022b5422e2c30783ee5032cc644b800133ac7a2d2257`（7,627 B）。本次重新讀檔核驗其中五個來源的 HTML 與 text 共十項 binding，全部相符；第五項是另外保存的 Mokaair 自有文章，不能替代四個官方來源。沒有重新網路請求或把此核驗冒充新的 source access。

ag018 明列 2026/9/27 查詢、規劃 9/28 的歷史示範；ag097 承認館方有步行建議，但我們未實測也沒查天氣。一般週一休館與指定 9/28 公告例外並存，不能外推每個週一；Open 是公告安排，不是旅客實際到訪、入館、付款或當前營運保證。Anthropic 的 workflow／agent 工程定義不是全部產品的正式分類或量化性能保證。

`verify-2.md` 的 visual-only appendix 另驗證當前 source 與已查文字的語音欄位、全部 36 個 native TTS plans 完全相同，speech hash 仍為 `80b70c13bcc03e34`。目前 visual hash 為 `b9ae256bfd4c2369`。這次排版／reveals 沒有重買語音或改上述歷史與來源含義。

## Source、翻譯與字幕實際 binding

以下檔案於 UTC 12:37:26 重新讀取完整 SHA。四語共 568 entries 已有獨立內容 review；JA ag080 的最小逗號修正透過正常 native worksheet／merge 套用，沒有手改 SRT。原 split 問題及 before/after 已保留在既有 caption review，未被本文件覆寫。

| `<repo>` 內檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/videos/ai-agent-vs-chatbot/video.json` | 36751 | `905ac35021688b7ca80264f12afd6f8973b959317438538e2199bdb4536a058c` |
| `docs/videos/ai-agent-vs-chatbot/verify-2.md` | 46827 | `4ae41e498d256f55553db30db691813cd83d6e1f6bde2cd82ce4e778a6782580` |
| `docs/videos/ai-agent-vs-chatbot/i18n/en.json` | 19784 | `6698e7fb1c3ea61feecf19c50d9b54fb66c57d06761125214f3773ad06244ecf` |
| `docs/videos/ai-agent-vs-chatbot/i18n/ja.json` | 22423 | `fbe6477c4964b164e3c4352a4d950f39e11de7f3616d5af5ccde8e1e0769cd19` |
| `docs/videos/ai-agent-vs-chatbot/i18n/ko.json` | 21600 | `2de7749c394238599128daaabd2368604439d00652603a8c1f883b993f3e5044` |
| `docs/videos/ai-agent-vs-chatbot/i18n/zh-CN.json` | 19921 | `bdf27a6bb64f542e6421659b486f2ac5a9de7f59e3a1e6377c0c02ed1b5906da` |
| `docs/videos/ai-agent-vs-chatbot/caption-review-20261007.md` | 14301 | `a3d3e6dac05a53593f9e2220218a8357487898e5082e4c2f70f5def1b5ee0a4e` |
| `docs/videos/ai-agent-vs-chatbot/visual-review-20261007.md` | 14362 | `184b4e59a8f1e9f3df6ade143dccd1f16b7246c5af7fced80ec9ced04095020d` |

五份 actual SRT 位於 `<operation>/media/ai-agent-vs-chatbot/captions`。全部精確匹配 native 重建；來源行 ID、scene、窗口、跨行切分與完整 joined text 已覆核，native CPS／width／overlap／duration 問題為零。字幕使用繁中 narration 窗口，translated splits 在該窗口內按文字 spoken-weight 分時；沒有外語逐詞實測或 dub 音訊對齊宣稱。

| SRT | Cues | 最大 CPS／native 上限 | Bytes | SHA-256 |
| --- | ---: | --- | ---: | --- |
| `zh-TW.srt` | 142 | 5.2945／9 | 12452 | `ca9c50884e56a9511b808d6382f1776c21885d3e2840cf85df44d101049386e4` |
| `en.srt` | 142 | 18.7477／20 | 12873 | `78cd1d4d78963fd693ed69748f45f4192b0ea9b36cec7ce71f3b383cae839a38` |
| `ja.srt` | 145 | 7.6923／8 | 15231 | `73850a8d6282e340c4024eeac51d1484216549f7dccb22fea15a20d1634015dc` |
| `ko.srt` | 148 | 10.1286／12 | 14892 | `cc605e96a1257963815566d3c4743ec6dd34e51140ef300c831f7e79f46d4107` |
| `zh-CN.srt` | 142 | 6.4480／9 | 12682 | `16e8d26e8aa8236dece5cfbd305da5eeb64aacf775533017ea4b616e7c73b079` |

完整 source／timeline／SRT/VTT／i18n／metadata bindings 收據為 `<operation>/caption-review/actual-captions.bindings.final.json`，review ID `ai-agent-actual-caption-bindings-2026-10-07T115100363Z`，SHA `f6f7a33376991115510e1098a44913965b8921f8a9b16e72549578080f355f5f`（26,359 B）。其 ready 僅限實際免費 caption 草稿及文字／欄位審稿，不含 owner 語言選擇、dub fit、音訊、成片或發布。

## 未核准 metadata 草稿

`<operation>/media/ai-agent-vs-chatbot/review/metadata-draft/metadata-draft.json`，SHA `0fc96d1dc3bcd9e0a3b0f6d48098509c13222ddaf7230eeba7db021d2cc07463`（9,022 B），purpose 為 `UNAPPROVED_METADATA_DRAFT`。七個 source bindings（source、lexicon、source article、四份 i18n）重新核驗全部相符；timeline SHA 亦相符。五語 title／description／tags 的 native budgets 無問題，六章節 clocks 為 `00:00`、`00:15`、`02:17`、`03:29`、`07:08`、`09:11`。每語描述保留四個官方來源標籤與 exact URL 各一次。

繁中 metadata description 第一行為：

`🔗 完整文章：https://mokaair.com/zh-TW/life/ai-agents-explained?utm_source=youtube&utm_medium=video&utm_campaign=ai-agent-vs-chatbot`

四個其他語系目前也使用該繁中文章 CTA，不宣稱文章已完成四語翻譯。`description.<locale>.txt` 展示稿是 `title + 空行 + metadata.description + 換行`，首行為 title、第三行才是 CTA。本快照未找到 `upload/metadata.json`、`languages.json` 或 `dubs` 目錄；這些草稿不能當成已選語言的 delivery package。四語 thumbnail words 尚缺，現用繁中 fallback，不能宣稱五語縮圖完成。

## V1 成片、實際畫面與保留副本

native preview render UTC 11:42:40 exit 0：84 drawn、0 reused、446 秒；native assemble UTC 12:01:19 exit 0。V1 機械成片 checks 記錄 `ok=true`、19,182 frames、integrated −14 LUFS、true peak −0.9 dBFS、problems 空。它驗證機械組裝，不覆蓋下述仍被 flagged 的語音內容。

| V1 artifact／私有相對位置 | Bytes | SHA-256 |
| --- | ---: | --- |
| `media/ai-agent-vs-chatbot/timeline.json` | 48788 | `dd814aca675fe70a819917c1139dd8d80add41075cc99a2a81483f3b78f112f0` |
| `media/ai-agent-vs-chatbot/narration.wav` | 61382444 | `a4bec99894f398e25b5255e394908908fcafd157616dd5fa5382642995e53466` |
| `render-preview/ai-agent-vs-chatbot/final.mp4` | 94920878 | `2b310b91cf84e04ea32163492f5aeb5f23e6ceae18545a5fea4cce922c670f64` |
| `media/ai-agent-vs-chatbot/final.mp4` | 94920878 | `2b310b91cf84e04ea32163492f5aeb5f23e6ceae18545a5fea4cce922c670f64` |
| `media/ai-agent-vs-chatbot/checks.json` | 18892 | `cf39932625dce76a5120cc0f6c97c996bbeea1a34682b225f9afb9a53a1e7409` |
| `media/ai-agent-vs-chatbot/frames/manifest.json` | 52141 | `0f3827a6e4aab3289b674bb32ee343aaeec86f4e4ff920fa17ff21f90fd814b1` |
| `visual-candidate/canonical-artifact-copy.json` | 148309 | `a226c12779499ada70f8437f6c2d17e3d1c80d684d5a9591fef38336a9d46e22` |
| `preserved-v1/manifest.json` | 26584 | `001688712586eb440eb1d5c2d499b52e7c11f2e9725ba89ee52d228df8cbcfdf` |

canonical 與 preview movie 的完整 bytes／SHA 在本快照相同。copy 收據於 UTC 12:10:23 保存 882 個實際 artifacts 的 pin，明列 raw audio 未變、没有複製 approvals 或 journals。圖片 review 實際覆蓋全部 84 stills、320px 縮圖；其 lower 15% caption reserve 僅是圖片範圍的結論，不聲稱整段播放器觀看、全部 792 過場 PNG 逐張觀看或音訊聽驗。

V1 的 `preserved-v1` 於 UTC 12:34:33 保留 167 個檔案，含原 142 WAV、narration、timeline、movie、checks、初次 QA／flags；deletions 0。UTC 12:42:09 本 reviewer 逐項重新讀取這 167 個實際檔案，bytes 與完整 SHA 全部符合 manifest，沒有缺檔或 mismatch。這是磁碟保留副本核驗，不是雲端備份同步或刪除授權。

`<operation>/movie-frame-check/manifest.json`，SHA `bf5252bb2b4aacd78a3af0b6c755744210a6fb5be3c7bcdd3837b3243a50e6a6`（1,666 B），釘住同一 V1 movie 及 UTC 12:02:27 擷取的九張實際影格（0、5、90、210、300、450、500、610、638.9 秒）。本文件讀取保存的 extraction manifest，沒有新增播放器、全片觀看或音訊聽验宣稱。

## 原生音訊 QA 與後續待辦

初次 native row 為 UTC `2026-10-07T12:21:25.194Z`：142 lines、110 exact、17 alike、15 judged、14 flagged、unchecked 0、37 transcribed、1 Jev call。14 個實際 flags 為 `ag003, ag010, ag090, ag029, ag031, ag093, ag125, ag097, ag047, ag048, ag137, ag107, ag064, ag076`。此處 alike/judged 是 native 記錄欄位，不能改稱全部人工聽驗合格。

| 原 QA 保留 artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `preserved-v1/review/check.json` | 57314 | `5b95a251defc54972444da0a3df6db9f2bc8c525919ecd6903a68b47784c701d` |
| `preserved-v1/review/check-flags.json` | 1663 | `cbfad676e22fa1b0a5e2ce71c4b1811c82f889072139315715d1a7fa0fc66971` |

離線 blind 第二意見只完成 priority 14：六筆取自已完成的原 blind outputs、另八筆真實離線辨識；原 broad sweep 只完成 55 rows，不能宣稱全 142 句完整第二意見通過。`<operation>/offline-audio-evidence/priority14/receipt.json` SHA `81f2a3a6be0c1f85c03ddf21e42c43f35622eaabf5c87d148e010c5bce91db45`（14,898 B）；`adapter-validation.json` SHA `934aefe226522ca08715a3d2372007976bdde4fecb89f1993669d478cfeeeaa1`（935 B）。它們記錄 exact 原請求 WAV／hash、14 output 與實際 blind transcript 相符、wrong-hash 反例拒絕、沒有以腳本或 hints 當答案、provider requests 0。

native 載入該第二意見後於 UTC `2026-10-07T12:37:02.231Z` 真實記錄：142 lines、110 exact、17 alike、15 judged、8 cleared、6 flagged、unchecked 0、0 transcribed、1 Jev call；實際程序 exit 1，收據 `<operation>/logs/20261007T123655Z-check-audio.exit.json` SHA `0894b0909412e75e2ab2963a49bf387953d0fa5a5b93577842421bc498d3c929`。餘六 flags 是 `ag010, ag029, ag093, ag125, ag097, ag107`，不是 zero flags，也不是 owner manual acceptance。尤其否定詞、日期／條件及外部指令意義仍需實際聽核／必要重錄。

| UTC 12:37:26 所讀 canonical QA artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `media/ai-agent-vs-chatbot/review/check.json` | 60412 | `9a4db6abf035446bd35643c7105f8368c6b06c0d5c1e1884d8bcca216e09e85f` |
| `media/ai-agent-vs-chatbot/review/check-flags.json` | 818 | `d24db33f38f12b808e29b32038ff6f3fa5fb677eab2a3f656958a4fab5778f47` |
| `media/ai-agent-vs-chatbot/state.json` | 1447 | `736f8ce1a430df954ecf718ac99b27c97915fd8b79231666b88ee2a407311212` |
| `media/ai-agent-vs-chatbot/approvals.json` | 311 | `ac5dcd8081c162f20999ade867685f8304949a995fd4d0f81d7de3b2db267596` |

本次將 142 個 current QA records 的 scene、intended text 與 clip16，逐項對照目前 source 與 V1 保留 WAV 的完整 SHA 前綴，全數相符；六個 flagged primary scores 都是有限數值。匹配的 exact/sound record 仍可有 `noul:null`，沒有把未評分 null 當成 judged-fine 或合格分數。第二意見清除也是 native 的實際結果，不是手改 scores、flags 或 approvals。

下一版須在實際重錄結束後更新六句 raw WAV／narration／timeline／caption／movie hashes，重跑真實 native audio QA 並保存仍餘 flags；若 timeline 改變，既有 CPS、切分、chapter clocks 需重新綁定。之後才處理必要 package 與 narration／audio／final／language／upload 的各自 owner gates。這份 V1 收據不得倒填為下一版、final pipeline pass、task done 或已核准上傳。

本次其他佇列的 citation `ci037` 未知 sent／STOP、Embedding hold 均沒有操作；不能以新影片的成功階段消除它們的既有不確定性。沒有 YouTube upload、public/private visibility mutation 或 publication。


## 本版繁中成片與基本上傳包交付（2026-10-07）

本追加 UTC `2026-10-07T13:41:08.828500+00:00`。前文 V1 字節完整保留，prefix SHA `aec1b46bdbff28afedb1cf3f390d6d511cf9307bbeee90bf6071c0f6512ab43d`；前文的 14→6 flags、V1 10:39、旧未核准 metadata 是當時紀錄。本版是重新聽核、局部重錄、同步四語與重組装後的實際 artifact，不能用同名路徑誤認成 V1。

**繁中 1080p 成片已完成，約 10:30；11/11 native QA 與 4/4 package check 通過。** 實際 movie 93,459,008 B，SHA `6e07ad6f915e35b49df565fceabe42ebee3f78821668f698b6bfc74cbeb7b9d9`；timeline 18,895 frames／30 fps＝629.833333 秒，ffprobe container 629.9 秒。142 句 current raw audio／scene／intended／clip 全綁定；最終 check 是 114 exact、17 sound／filler、1 Jev fine、10 second-opinion cleared、0 flagged、0 unchecked，不是人工完整聽完 142 句。組裝 checks current narration 相符、−14 LUFS／−0.9 dBFS，108 個影片影格匹配 slides、problems=[]。完整實際私人 artifacts 留在 `<operation>/media/ai-agent-vs-chatbot/`；沒有媒體進 Git。

六句首輪局部重錄之後餘三句，真正的新 blind 第二意見只處理這三句並清除 ag093／ag097；ag125 達設定三輪重錄仍有歧義，依 listener-rewrite 改成「交付物要保留日期和館名，不能只寫週一可以參觀。」。原句、每輪真實 WAV／flags／closed exits 及第一輪同義改詞均保存；正文其他 141 句和所有 scene data 未因該同義改詞改動。`verify-3.md` 獨立核對 inverse full-object、全部 TTS plans、四個 official raw HTML/text pins，事實含義不變。speech hash 由 `80b70c13bcc03e34` 改為 `ef2d1ce1ef5e5ea2`，已正常重合成和重綁後續音訊、字幕、metadata與movie。

普通局部重錄與同義改詞後合成的 native billable characters 分別是 114＋21＋21＋23＝199；初次全片 dry-run 是估計值，未拿估計或不完整 billable headers 冒充供應商最終金額。沒有提高 quota／retry上限、force重買、手改approval／Jev分數或清除其他未知請求。

### 真正的正式審核與本機匯入

四關各自由真實 POST／GET 與 native review-pull 綁定相同 SHA。audio／final／publish 是依站主既有設定自動核准，不是 owner 播放器／聽音驗收。

| Gate | Actual review UUID | 完整 content SHA-256 | API decided UTC | 核准來源 |
| --- | --- | --- | --- | --- |
| outline | `85db28ff-f4a4-4672-adbb-99c4d2b6a312` | `9093fcc62ad70a60bfcd8680389c833d85de87aba090a8028f0302a11976ba23` | `2026-09-28T12:16:08.376586Z` | 站主選大綱 A |
| audio | `832222e7-e54b-4bb2-96ee-dfa682331af1` | `31b39a0b6968fe0a3b65cc621805b23c20a1e3ff370631cd263378c64c80e0fe` | `2026-10-07T13:11:24.096518Z` | Jev 判斷每一句都唸對了，依設定自動核准 |
| final | `530de3a2-42ff-4a97-9696-20304c19c607` | `6e07ad6f915e35b49df565fceabe42ebee3f78821668f698b6bfc74cbeb7b9d9` | `2026-10-07T13:26:15.173984Z` | 自動品管 11 項全過，依設定自動核准 |
| publish | `ee696b32-f967-499a-b74f-2e0a761a0b84` | `6edd7beaf22414119832b5b02db122cbd715c600ae16c7a53242a3fdfcfaaeb5` | `2026-10-07T13:31:34.849657Z` | 上傳包 4 項齊全，依設定自動核准 |

原生程序都已保存 start／child／closed-exit：最後 audio exit 0、render exit 0、assemble exit 0、final review-push exit 0、package exit 0、publish review-push exit 0，final／publish pulls exit 0。來源與 metadata 的限額、五個有效連結、縮圖、政策、揭露及音量等 11 checks 全通過；`lint` 最終 0 errors／0 warnings。沒有把程序還在跑、缺 closed exit 或 UI stage 字串當完成。

### 本版 source、審稿、QA 與上傳包 pin

| Artifact（public 為 repo 相對；其餘為 `<operation>` 相對） | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/videos/ai-agent-vs-chatbot/video.json` | 36757 | `6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235` |
| `docs/videos/ai-agent-vs-chatbot/verify-2.md` | 46827 | `4ae41e498d256f55553db30db691813cd83d6e1f6bde2cd82ce4e778a6782580` |
| `docs/videos/ai-agent-vs-chatbot/verify-3.md` | 9595 | `2bb8ba843c6e82017b9c62f6ca21878b4a2f0fe83d5f3de76b19e5df11adec2a` |
| `docs/videos/ai-agent-vs-chatbot/caption-review-20261007.md` | 22518 | `90836d57a5386ec16df7f34cdbae1dac6bdc7a0cba448e2cd36016abff60b1d9` |
| `docs/videos/ai-agent-vs-chatbot/visual-review-20261007.md` | 17640 | `68904dd1b4d0582e2945847cade7cfea7552cfcc01b53dfc9f823363c8c6185d` |
| `docs/videos/ai-agent-vs-chatbot/offline-audio-review-20261007.md` | 16297 | `c46168ed50f399eb326309011e6696c2bf374e2be8804a64f7384337c106ad3b` |
| `docs/videos/ai-agent-vs-chatbot/i18n/en.json` | 19784 | `80ab0f62a861538d06776fdf7301508f08280f816ea3110b3868c31a42b2545f` |
| `docs/videos/ai-agent-vs-chatbot/i18n/ja.json` | 22432 | `cd1cca8082fd883172fdc9c547051757ffb3ff09ffa948a2aafa1cb60c6696d1` |
| `docs/videos/ai-agent-vs-chatbot/i18n/ko.json` | 21597 | `6eb812ed9183e605f0c2a73b1602c946475e773774f6f352eeebd9b221c785fd` |
| `docs/videos/ai-agent-vs-chatbot/i18n/zh-CN.json` | 19921 | `9300210c9bbbb4e8cef3f6cb3ebd8463755b0b5bc112d48da4a020821733c61b` |
| `media/ai-agent-vs-chatbot/timeline.json` | 48782 | `31b39a0b6968fe0a3b65cc621805b23c20a1e3ff370631cd263378c64c80e0fe` |
| `media/ai-agent-vs-chatbot/narration.wav` | 60464044 | `29582a770d65215d8b899b808ee34ae35c602be82989a94489edec7df9b202f5` |
| `media/ai-agent-vs-chatbot/final.mp4` | 93459008 | `6e07ad6f915e35b49df565fceabe42ebee3f78821668f698b6bfc74cbeb7b9d9` |
| `media/ai-agent-vs-chatbot/checks.json` | 18890 | `9d7b270a19e2c0b100fbf0cafe726eaffacc6980076a155a8d7c9eb7c2757628` |
| `media/ai-agent-vs-chatbot/review/check.json` | 59449 | `e42b771ffc51cb7bdda69d9ad47617144eed0ca7eb50b910c590afc1b26cd95a` |
| `media/ai-agent-vs-chatbot/review/check-flags.json` | 103 | `462f213813f05baac9c117c8dcd305079a6ee7b89eb5e77073dfb828f20f2f38` |
| `media/ai-agent-vs-chatbot/review/rewrites.json` | 268 | `ecf69b8f9f41260a00700f82859b9d08b773bf6dbd04a1264975b1d40aa3a1f1` |
| `media/ai-agent-vs-chatbot/review/qa.json` | 1663 | `7df049c267c34c300006f1ec21fe2b6cfe92d858db498285a01ad70f76f0e2bc` |
| `media/ai-agent-vs-chatbot/upload/metadata.json` | 8183 | `6edd7beaf22414119832b5b02db122cbd715c600ae16c7a53242a3fdfcfaaeb5` |
| `media/ai-agent-vs-chatbot/upload/UPLOAD.md` | 2240 | `ff005b2081c612428aff076ce6e62144245eba5bd4c9e18ee488303c4c748034` |
| `caption-review/actual-captions.bindings.final-audio.json` | 79349 | `fe9144d9dd30167e6b1381aa456ac17415abe118ec7139607e2802322f98991f` |
| `listener-rewrite1/actual-i18n-audit.json` | 17054 | `a4d3647c76e5c196b61c204781dd8aae6e787dc6521d06bc6c96050a3840e0ab` |
| `current-visual-review.json` | 180873 | `ffbaac351040e3f4e424115c28e415db4768b88066d5eafdb06aff195779d549` |
| `final-delivery-audit.json` | 32055 | `c49f87d54fea0ec7518149f26566e43d93deba0a3c9f9baed4eca0b81beeae94` |
| `final-package-audit.json` | 21863 | `20597a49ab346271e8f496b39214b2c55d0897e0a0411225cb2654277ecec43a` |

當前五語 SRT／VTT 718 cues（zh-TW142、EN142、JA145、KO147、zh-CN142），568 個四語 source_hash 全部 current，pure native 全檔 rebuild 與完整 bytes 相符，CPS／width／窗口／overlap 問題 0；JA ag080 的自然切分保留。六章節 current clocks 00:00／00:15／02:09／03:20／06:59／09:01。translated captions 使用繁中行窗口，不等於有外語配音或逐詞實測。

基本 upload 是14個檔案（13正式附件加UPLOAD.md）：實際影片、繁中縮圖、metadata、五語 description 和五語 SRT，逐檔 bytes 和當前 canonical／source-bound metadata 相符。四個其他語系 thumbnail words 缺，正常使用繁中 fallback，不能宣稱已完成五語縮圖。完整文章 CTA 是描述欄第一行、display description 的第三行；五語目前都指向既有繁中文章，不聲稱文章另有已發布四語。使用 `<operation>/media/ai-agent-vs-chatbot/upload/UPLOAD.md` 交接 Studio 步驟。

### 13:30 新語言選擇與真正剩餘事項

最新 GET UTC `2026-10-07T13:32:12.555Z`、HTTP200、actual body SHA `845998287d6c4c9a7b1726cff93aa24f9a8261ae05198d5d8376bee760dce32d`。站主已在 UTC `2026-10-07T13:30:52.197866Z` 儲存 EN／JA／KO 的 metadata＋CC＋dub、zh-CN 的 metadata＋CC（dub=false）。這個新選擇在基本包裝完成後，不能以13:29的language_choice:null／dubs=[]草稿冒充新三語配音交付。

當前 `youtube_video_id=null`、`ready_to_upload=false`，各選定 language parts 由API表示 working；此derived狀態不證明有實際工作進程。API `stage="on YouTube"` 是產線尚待完成的步驟，與本機status未勾的onYouTube一致，不代表已上傳。下一輪必須以本版來源、正式final及真實新選擇繼續 EN／JA／KO 配音的 fit／音訊 QA／字幕時間軸與 languages 包；任何既有 producer／未知答案須先釐清以免重买。站主 Studio 上傳與公開時間仍由站主操作；本輪沒有YouTube upload／visibility mutation／publication，也沒有 merge／deploy。

base私有收據 `<operation>/base-delivery-receipt.json` SHA `abf802f86780950530b547f7df1862bbb7f98bfbc6f8c574170640a1e2ef56cd`（7215 B）。成片與上傳包本身可供預覽和私人上傳；完整選語交付尚未就緒。任務保留review供PR檢視，新語言進度另保存，不把基本影片完成寫成全部語言或站主驗收完成。Citation ci037 sent／STOP、Embedding hold及其他影片的未決provider證據未被本輪改動。


## Public receipt 格式重綁

`.gitattributes` 的LF規範在git add時揭露 visual review 原133個CRLF；本輪已保存原全字節並只正規化換行，沒有變動任何source／媒體／審核。上表visual fullSHA `68904dd1b4d0582e2945847cade7cfea7552cfcc01b53dfc9f823363c8c6185d`（17,640 B）是保存的原工作區snapshot；現在repo文件為18649 B、SHA `200dc62750ec7186c1a5a117d567a1fe39c50360046d148fafc81de8487bce91`。其前文V1 prefix與9影格review仍可在不可改寫before副本精確回查，詳見visual文件最後的Git格式重綁。

私有rebind receipt `<operation>/line-ending-rebind/receipt.json` SHA `d4960d13c95df262dc983191e02bea528ad0d9b29defb2d0ee4fd9737b281beb`（1069 B），記錄before完整副本、LF normalized before-append及新public文件SHA、133次CRLF→LF、Unicode內容相等、source／audio／caption／movie無改動。後續以此LF公版為準，不拿Git自動換行造成的不同SHA假冒版本一致。
