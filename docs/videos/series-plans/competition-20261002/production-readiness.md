# 《喜宴未散，清算開始》開拍準備核對

核對日期：2026-10-02（Asia/Taipei）。這是本機程式、製作資料與既有操作收據的核對；沒有付費生成、後台變更、試聽、成片驗收或 YouTube 操作。

本次交付鎖定同一畫面主版、zh-TW／ja／ko／en 四種角色配音，以及每種語言自己的可開關 SRT／VTT CC。製作順序仍先完成自然台灣口音中文版，再重建日、韓、英角色音軌；**比賽公開前四語音軌與 CC 必須全部完成並驗收**，不把「先中文製作」誤解成「先以中文單語參賽」。

## 已有什麼、還缺什麼

| 部分 | 實際已有 | 開拍／交付缺口與證據 |
| --- | --- | --- |
| 原作與攝製資料 | 40 集來源、逐集攝製設計、逐鏡命名造型、道具交接、音效方向、試音文字生成器 | [profile](../production-20261001/profile.json) 仍為 `design-and-tooling-not-render-accepted`；候選聲線是 `selected-not-auditioned`。本次實跑 `production-check`：10 部／400 集資料零錯誤，聲音與影片未測。 |
| 後台資料 | [2026-10-02 同步收據](../production-20261002-sync/README.md) 記錄 10 部、60 份最新 v2 待審文件及 400 集設計已寫入 | 該次讀回為 `drama_enabled=false`、0 集／0 請求、無排程工作、文件未核准；這是歷史操作快照，開始前仍須重讀現況。不是已開拍。 |
| Veo 3.1 Lite | API catalog/provider 與片段 CLI 已支援核定模型、1080p、8 秒、首尾幀；不送 `referenceImages`；按 profile 阻擋錯模型／解析度 | 尚缺選片實際 keyframe、動作、身份與區域可用性樣片。核對 [`gemini_video.py`](../../../../apps/api/app/video_media/providers/gemini_video.py)、[`clips.mjs`](../../../../tools/video/media/clips.mjs)。Lite 原生音訊必開，但成片捨棄它，另混角色人聲。 |
| 中文角色配音 | `tts` 已依 `speaker`、角色 voice、逐句 emotion 分批；具音訊快取、同 take 引用、音軌時間軸與 dry run | 所選 8 名角色與旁白仍需實際試音。核對 [`requests.mjs`](../../../../tools/video/tts/requests.mjs)、[`voice-audit.mjs`](../../../../tools/video/production/voice-audit.mjs)。試音計畫的校準句不是新增劇情台詞。 |
| CC | `captions` 已輸出多語 SRT/VTT、閱讀速度檢查，已有配音時間軸時可取其落點；漫劇預設不燒錄 | 沒有有效外語配音時會用主旁白時間軸；這種翻譯 CC 不能算外語音軌同步驗收。核對 [`core/stages.mjs`](../../../../tools/video/core/stages.mjs) 中 `timing: dub / narration`。 |
| ja／ko／en 角色配音 | 教學影片的單一旁白 dub 有翻譯、時間視窗、重錄、混音、配音字幕等可重用能力 | **漫劇未實作**。[`dubs/cli.mjs`](../../../../tools/video/dubs/cli.mjs) 明確拒絕 `isDrama(doc)`；後台 [`admin_service.py`](../../../../apps/api/app/video_reviews/admin_service.py) 的 `_apply_locales` 回 `video_locales_dub_not_for_drama`。只刪這兩個阻擋仍不等於角色聲線、混音、驗收整合完成。 |
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

`tts --dry-run` 不合成；若有已配對工具 token，會唯讀查聲音／額度。`clips --dry-run` 也不送生成，但會先要求既有關鍵影格與分鏡核准，不能拿尚未撰寫的 40 集細綱直接報精確成本。`look`、`keyframes`、`music` 亦有 dry run；它們仍有各自檔案和階段前提。

`audition --text-file ... --voices gemini:<VOICE> --style ...` **沒有 `--dry-run`**，執行即會請求語音合成。既有 `audition-plan.json` 的 `args` 是之後執行的參數，不是已錄聲音。`dub --slug ... --locale ja,ko,en --dry-run` 仍會拒絕漫劇，不能列為本片已可用的成本預檢路線。

依 2026-10-02 官方核對，Lite 1080p 為 US$0.08／生成秒，每個 8 秒原片 US$0.64；剪掉的素材仍是生成成本。鏡數必須從實際對時分鏡計算；另加重拍、設定圖、關鍵影格、TTS、音樂及 judge。使用者已在本次對話同意US$3,000目標＋US$1,000預備金，實際執行遵守先US$100內pilot、累計US$350內前三集與總額守門，不要求再次確認相同預算。

## 最短開拍順序

1. **鎖本次可審版本。** 以當前來源重建《喜宴》bundle，保留原作／設計／profile 雜湊；核對後台最新文件與本次比賽增補的關係。不要把舊核准或舊 generated bundle 自動套到新版本。
2. **完成第一集可執行劇本與逐鏡表。** 沿既有開場的前世倉門→現世簽署→拒簽第一回報，固定 line/speaker ids、單鏡一動作、每鏡 2–8 秒使用段。三份文件唯一性、前世褲裝／現世婚紗與唯一銀方錶可直接由現有設計落到 shot look；不需要再發明角色或改原作。
3. **中文試音及對時 animatic。** 先覆蓋開場出場聲線及旁白，再覆蓋姐妹、隔門、醫護／火場聲場等代表性表演。實際量秒後縮短長句，保留反應和換氣；animatic 可用靜畫，不能當完成動畫。
4. **先做一鏡，再做代表 pilot。** 在已核定預算及既有關卡範圍內，首鏡確認區域可用性、同臉及動作，再做約 60 秒 pilot。必含可聽清的雙人對話、手部接觸／撕展示副本、完整原件保留、同集服裝切換；不用無人風景代替。以反應鏡、越肩、道具插入承接台詞；可見嘴部特寫另驗口型，不宣稱已有自動 lip-sync。
5. **修一次問題，再鎖樣式批次做章節。** 保存採用臉、造型、聲線、圖／聲來源及拒用原因；現有預算與 bounded retakes 持續生效。先完成中文版全集、全長剪輯與 zh-TW CC，驗前 5／30 秒承諾、每篇留存節點、音量及全片因果。
6. **平行完成外語產線，中文版鎖定後正式本地化。** 需 locale×speaker casting、保留 line/speaker ids 的台詞翻譯／發音、逐句實測與超時重寫、乾聲＋獨立音效／音樂重混、各語 CC，以及合集拼接和來源雜湊失效檢查。先以同一 pilot 做三語驗收，才擴至整片；不得把中文完整混音墊在外語聲音下。
7. **四語齊備才交公開上架包。** 在目標頻道實證單一主片可掛各音軌；全片各語聲音／CC、片頭片尾總長、角色身份、發音、字幕不提前劇透均有驗收記錄。四語片名、說明及縮圖承諾需一致；公開日期才成為三個月計分窗口的起點。

## 既有待辦與本次需保留的缺口

- [十部後台同步票](../../../../tasks/open/2026-10-02-ten-drama-backend-production-sync.md)：操作讀回已完成，票仍待程式／收據 PR review；驗證的是待審資料，不是媒體。
- [造型舊票](../../../../tasks/open/2026-10-01-owner-settles-the-looks-the-ten.md) 仍列部分早期限制；《喜宴》目前 `production-review.md` 已記完整命名造型與逐鏡工具。不要把舊票的「需第二角色 ID」當現行限制，也不要替其他工作批量結案；本片剩實際角色圖與切鏡驗收。
- [漫劇 policy 題組票](../../../../tasks/open/2026-09-28-video-drama-policy-questions.md)：自動成片 QA 仍可能套「有示範」等教學題。這會影響自動核准，必須在放量前處理或明確採既有人工成片審核；不能用自動核准一定成功作排程假設。
- [既有漫劇 pilot 票](../../../../tasks/open/2026-09-26-video-drama-pilot.md) 與 [series pilot 票](../../../../tasks/open/2026-09-26-video-series-pilot.md) 是其他題材的未完成端到端驗證，不是《喜宴》已驗收證據。
- [語言上傳同步票](../../../../tasks/open/2026-09-30-youtube-approved-languages-sync.md) 記錄分離語言核准與上傳包的整合問題；發布前核對合併／部署狀態，不能因本機已有 CC 檔就認為播放器已有四語。
- 本次核對前未找到針對這五部選一部、三個月點閱競賽的既有已完成工作，也未找到已完成的漫劇多角色多語／合集音軌實作。這些缺口須留在本次任務與後續實作票；不得把 profile 的 `planned-not-implemented-for-drama` 改成 ready 來取代實作與驗收。

參考：[動畫製作流程](../../../../.agents/skills/youtube-video/references/animation-production.md)、[本片攝製覆核](../binge-five-20260928/wedding-reckoning/production-review.md)、[Veo 官方文件](https://ai.google.dev/gemini-api/docs/veo)、[官方價格](https://ai.google.dev/gemini-api/docs/pricing)。

## 本聊天的實際連線檢查

2026-10-02唯讀檢查：Node v24.19.0、ffmpeg/ffprobe 7.1.5可用；影片工具配對檔尚不存在，MOKAAIR_VIDEO_TOKEN與MOKAAIR_SITE未設定（僅查存在性，沒有讀取秘密）。預設端點為https://mokaair.com，speech/status與media/status可達，未帶token回401 `video_tool_token_invalid`；`media-status` 回exit 3、`no video tool token yet`。這不能證明供應商金鑰或剩餘額度可用。

需使用既有裝置配對：`node --use-env-proxy tools/video/cli.mjs login --site https://mokaair.com --name codex-wedding-pilot-20261002`。站主在後台核對工具印出的驗證碼並允許，token直接寫入工具設定，不在聊天貼API金鑰。配對後先做不付費media/speech status，再做已授權上限內的少量試音。本包不保存一次性配對碼或token。
