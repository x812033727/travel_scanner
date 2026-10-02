# 《喜宴未散，清算開始》開拍準備核對

更新日期：2026-10-02（Asia/Taipei）。初輪離線核對時沒有付費生成；本輪已完成工具配對與繁中開場 11 句 TTS。以下分開記錄歷史核對、現有能力及實際製作進度，沒有後台設定變更、動畫生成、成片驗收或 YouTube 操作。

本次最終交付鎖定同一畫面主版、zh-TW／ja／ko／en 四種角色配音，以及每種語言自己的可開關 SRT／VTT CC。**使用者最新指示：先完成整部自然台灣口音繁中影片與 CC，由使用者本人確認後，才開始外語工作，包括多語產線實作、台詞適配、試音、配音、混音與各語 CC。** 現有外語草稿僅保留，不在繁中製作期間平行執行。最終競賽主片公開前仍須四語全部驗收及掛載完成。

## 本輪實際產物

- 已合成 11 句繁中開場台詞，使用 3 個聲線，共 118 計費字元；標準 `check-audio` 已檢查11句：8句逐字吻合、2句同音字、1句由文字judge接受，0句被標記；人工聽校待完成，不能寫成聲線已驗收。
- 已有約 51 秒聲音版，由人聲與無聲動作窗口組成，**不是動畫，也不是 animatic**；實際動畫生成仍為 0 秒。逐鏡窗口見 [measured-edit.json](pilot/measured-edit.json)，語音測時見 [timing-report.json](pilot/timing-report.json)。
- E1 完整 33 句稿已落地於 [episode-01-screenplay.md](pilot/episode-01-screenplay.md)；稿件完成不等於 33 句均已合成或整集通過聲音／畫面驗收。
- 供應商沒有回傳這 118 字元的實際美元費用。[成本帳本](cost-ledger.csv) 保留計費字元，USD 待對帳；US$5 僅為目前語音／檢查的保守預留，並非實際花費。

## 已有什麼、還缺什麼

| 部分 | 實際已有 | 開拍／交付缺口與證據 |
| --- | --- | --- |
| 原作與攝製資料 | 40 集來源、逐集攝製設計、逐鏡命名造型、道具交接、音效方向、試音文字生成器；本輪另有 E1 33 句稿 | [profile](../production-20261001/profile.json) 是初輪歷史規格，仍標 `design-and-tooling-not-render-accepted`／`selected-not-auditioned`。初輪 `production-check` 曾驗 10 部／400 集資料零錯誤；當時未測聲音與影片。本輪部分 TTS 產物另按上節記錄，不冒充全角色／全片驗收。 |
| 後台資料 | [2026-10-02 同步收據](../production-20261002-sync/README.md) 記錄 10 部、60 份最新 v2 待審文件及 400 集設計已寫入 | 該次讀回為 `drama_enabled=false`、0 集／0 請求、無排程工作、文件未核准；這是歷史操作快照，開始前仍須重讀現況。不是已開拍。 |
| Veo 3.1 Lite | API catalog/provider 與片段 CLI 已支援核定模型、1080p、8 秒、首尾幀；不送 `referenceImages`；按 profile 阻擋錯模型／解析度 | 最新唯讀狀態為 `drama_enabled=false`、全域 clip 選 `gemini-omni-1.1-flash`，不是核定 Lite；動畫 0 秒。尚缺 keyframe、動作、身份與區域可用性樣片。核對 [`gemini_video.py`](../../../../apps/api/app/video_media/providers/gemini_video.py)、[`clips.mjs`](../../../../tools/video/media/clips.mjs)。Lite 原生音訊必開，成片另混角色人聲。 |
| 中文角色配音 | `tts` 已依 `speaker`、角色 voice、逐句 emotion 分批；本輪 3 聲線／11 句合成成功，逐句自動辨識已完成、0句被標記 | 仍須完成本輪聽校及其餘角色／旁白試音。核對 [`requests.mjs`](../../../../tools/video/tts/requests.mjs)、[`voice-audit.mjs`](../../../../tools/video/production/voice-audit.mjs)。合成成功不等於聲線已採用；試音計畫的校準句不是新增劇情台詞。 |
| CC | `captions` 已輸出多語 SRT/VTT、閱讀速度檢查，已有配音時間軸時可取其落點；漫劇預設不燒錄 | 沒有有效外語配音時會用主旁白時間軸；這種翻譯 CC 不能算外語音軌同步驗收。核對 [`core/stages.mjs`](../../../../tools/video/core/stages.mjs) 中 `timing: dub / narration`。 |
| ja／ko／en 角色配音 | 教學影片的單一旁白 dub 有可重用能力；本案外語僅留既有草稿 | **漫劇未實作，且依使用者指示延後至完整繁中影片本人確認後才動工**。[`dubs/cli.mjs`](../../../../tools/video/dubs/cli.mjs) 拒絕 `isDrama(doc)`；後台 [`admin_service.py`](../../../../apps/api/app/video_reviews/admin_service.py) 回 `video_locales_dub_not_for_drama`。只刪阻擋不等於整合完成。 |
| 120 分鐘合集 | `compile` 可接已核准集數、對齊音訊、合併每集皆具備的各語 CC | [`compile/cli.mjs`](../../../../tools/video/compile/cli.mjs) 尚無三條外語角色音軌的合集交付流程。須讓每條音軌共享同一合集剪輯、片頭片尾與總長，驗證接縫及字幕偏移。 |
| 上 YouTube | 既有 metadata／CC 包裝與上傳相關工具 | 不代表漫劇四語音訊已可自動上架。預定以同一主片掛四語音軌；需在目標頻道確認 Studio 多語音訊功能，並實際驗收播放器語言切換、預設語言及 CC。站主操作上架；本次未登入或確認帳號能力。 |

《喜宴》沒有製作設計中已標記的未成年入鏡路徑障礙。其餘 Codex 五部中，《朕不是你們的替死鬼》也沒有；《末班車上的第七個活人》《這座城欠他一盞燈》《世人忘我，死敵記我》各有未成年角色或孩子入鏡，現有 Lite 首格 I2V 路徑未驗證。這是本次選片的製作可行性差異，不是聲稱成人樣片已通過。

## CLI 的真實邊界

以下前兩項可在尚未開啟後台漫劇時準備；影像／聲音產物須放 repo 外。`<EPISODE_SLUG>` 要用實際建立的單集 slug，不能直接把系列 slug 當已有影片。

```bash
# 純離線，驗來源及攝製契約；不等於實拍驗收。
node tools/video/cli.mjs production-check --slug wedding-reckoning

# 純離線，重新由當前來源建立待審 bundle、試音文字、分鏡 HTML。
node tools/video/cli.mjs production-build --slug wedding-reckoning --out /workspace/mokaair-work/competition-20261002/review

# 已有合法單集 video.json 後，按聲線列請求與字數。
node tools/video/cli.mjs tts --slug <EPISODE_SLUG> --dry-run

# 已具時間軸、通過的 keyframe 與分鏡核准後，才有片段 dry run。
node tools/video/cli.mjs clips --slug <EPISODE_SLUG> --shot <SHOT_IDS> --dry-run
```

工具配對已完成，網路 CLI 在此環境使用 `node --use-env-proxy`。`tts --dry-run` 不合成，會用配對憑證唯讀查聲音／額度。`clips --dry-run` 也不送生成，但會先要求既有關鍵影格與分鏡核准，不能拿 40 集細綱直接報精確成本。`look`、`keyframes`、`music` 亦有 dry run；它們仍有各自檔案和階段前提。

`audition --text-file ... --voices gemini:<VOICE> --style ...` **沒有 `--dry-run`**，執行即會請求語音合成。既有 `audition-plan.json` 的 `args` 是之後執行的參數，不是已錄聲音。`dub --slug ... --locale ja,ko,en --dry-run` 仍會拒絕漫劇，不能列為本片已可用的成本預檢路線。

依 2026-10-02 官方核對，Lite 1080p 為 US$0.08／生成秒，每個 8 秒原片 US$0.64；剪掉的素材仍是生成成本。鏡數必須從實際對時分鏡計算；另加重拍、設定圖、關鍵影格、TTS、音樂及 judge。使用者已在本次對話同意US$3,000目標＋US$1,000預備金，實際執行遵守先US$100內pilot、累計US$350內前三集與總額守門，不要求再次確認相同預算。

## 最短開拍順序

1. **鎖本次可審版本。** 以當前來源重建《喜宴》bundle，保留原作／設計／profile 雜湊；核對後台最新文件與本次比賽增補的關係。不要把舊核准或舊 generated bundle 自動套到新版本。
2. **核對已完成的 E1 33 句稿及逐鏡表。** 沿既有開場的前世倉門→現世簽署→拒簽第一回報，保留 line/speaker ids、單鏡一動作、每鏡 2–8 秒使用段。三份文件唯一性、前世褲裝／現世婚紗與唯一銀方錶依現有 shot look 檢查；33 句稿尚不代表整集 TTS／成片完成。
3. **完成繁中聲音檢查，再做對時 animatic。** 目前 11 句已錄、`check-audio` 已完成、0句被標記；接著聽校聲線與表演，再覆蓋其餘角色、姐妹、隔門、醫護／火場等表演。約 51 秒聲音版只含人聲及無聲動作窗口，尚無 animatic。日後用已接受畫面做 animatic 時，仍須明標前製預覽。
4. **解決媒體設定界線，再先做一鏡和繁中 pilot。** 全域漫劇 OFF 且選錯模型；配對 token 無修改設定權限，也沒有既有單作品 Lite 覆寫。先形成只影響本案的受控執行方案，確認模型與支出守門後，才在累計 US$100 內做約 60 秒目標的動畫 pilot。必含雙人對話、手部接觸／撕展示副本、完整原件保留及服裝切換。可見嘴部特寫另驗口型，不宣稱已有自動 lip-sync。
5. **修問題，再鎖樣式批次完成繁中全片。** 保存採用臉、造型、聲線、圖／聲來源及拒用原因；預算與 bounded retakes 持續生效。完成全部繁中演出、全長剪輯、混音與 zh-TW CC，驗前 5／30 秒、篇章節奏及全片因果，交使用者本人確認完整影片。
6. **使用者確認完整繁中影片後，才開始外語階段。** 屆時才實作 locale×speaker casting、台詞翻譯／發音、逐句實測與超時重寫、乾聲＋獨立音效／音樂重混、各語 CC，以及合集拼接／來源雜湊檢查。外語短樣與整片製作都在這道確認之後；目前不平行開發或試作。不得把中文完整混音墊在外語聲音下。
7. **四語齊備才交公開上架包。** 在目標頻道實證單一主片可掛各音軌；全片各語聲音／CC、片頭片尾總長、角色身份、發音、字幕不提前劇透均有驗收記錄。四語片名、說明及縮圖承諾需一致；公開日期才成為三個月計分窗口的起點。

## 既有待辦與本次需保留的缺口

- [十部後台同步票](../../../../tasks/open/2026-10-02-ten-drama-backend-production-sync.md)：操作讀回已完成，票仍待程式／收據 PR review；驗證的是待審資料，不是媒體。
- [造型舊票](../../../../tasks/open/2026-10-01-owner-settles-the-looks-the-ten.md) 仍列部分早期限制；《喜宴》目前 `production-review.md` 已記完整命名造型與逐鏡工具。不要把舊票的「需第二角色 ID」當現行限制，也不要替其他工作批量結案；本片剩實際角色圖與切鏡驗收。
- [漫劇 policy 題組票](../../../../tasks/open/2026-09-28-video-drama-policy-questions.md)：自動成片 QA 仍可能套「有示範」等教學題。這會影響自動核准，必須在放量前處理或明確採既有人工成片審核；不能用自動核准一定成功作排程假設。
- [既有漫劇 pilot 票](../../../../tasks/open/2026-09-26-video-drama-pilot.md) 與 [series pilot 票](../../../../tasks/open/2026-09-26-video-series-pilot.md) 是其他題材的未完成端到端驗證，不是《喜宴》已驗收證據。
- [語言上傳同步票](../../../../tasks/open/2026-09-30-youtube-approved-languages-sync.md) 記錄分離語言核准與上傳包的整合問題；發布前核對合併／部署狀態，不能因本機已有 CC 檔就認為播放器已有四語。
- 本次核對前未找到針對這五部選一部、三個月點閱競賽的既有已完成工作，也未找到已完成的漫劇多角色多語／合集音軌實作。這些缺口須留在本次任務與後續實作票；不得把 profile 的 `planned-not-implemented-for-drama` 改成 ready 來取代實作與驗收。

參考：[動畫製作流程](../../../../.agents/skills/youtube-video/references/animation-production.md)、[本片攝製覆核](../binge-five-20260928/wedding-reckoning/production-review.md)、[Veo 官方文件](https://ai.google.dev/gemini-api/docs/veo)、[官方價格](https://ai.google.dev/gemini-api/docs/pricing)。

## 連線檢查的歷史與現況

**初輪歷史快照，已被後續配對取代：** 2026-10-02 首次檢查時配對檔不存在，未帶 token 的 status 回 401，CLI 回 exit 3。當時僅檢查存在性，沒有輸出秘密。Node v24.19.0、ffmpeg／ffprobe 7.1.5 可用。

**目前：** 使用者已完成既有裝置配對；`speech/status` 與 `media-status` 成功，Gemini 語音已設定，並已合成上述 11 句。無需重複配對或要求使用者貼 API 金鑰；本包不保存 token／一次性代碼。

最新唯讀 media／automation 設定仍為 `drama_enabled=false`，clip 選 `gemini-omni-1.1-flash`／1080p／8 秒，單片上限 US$200；這些後台值不等於本案 US$100 pilot 授權上限。`ClipJobIn` 沒有 per-request model／budget，作品層也沒有 Lite 片段模型覆寫。配對 token 可讀設定與已核准作品 context，不能更改管理設定或核准待審文件。《喜宴》當次讀回為 6 份待審、0 集 ready／started；不可藉此直接啟用全域 queue。繁中音訊可繼續按本案授權與帳本執行，動畫生成仍須先解決此界線。
