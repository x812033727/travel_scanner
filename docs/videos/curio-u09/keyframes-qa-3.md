# U09 九鏡補圖後逐圖驗收（2026-10-16）

## 綁定、結果與費用

- 此輪沿用已核准的 `script.md` SHA-256 `A6EBACD14E9986B8422316ABAEC6178FF039D063F31FE33A1A01D14233AF3F5A`，及 [九鏡提示詞計畫](keyframes-repair-plan-2.md) 的 `video.json` SHA-256 `E9C4173F6A808A820C3563C13FC3E751344AD5694A117D0BF878D515CAC9E03E`；未改劇本、旁白或系列 `look`。
- 主代理依共享帳本預留 US$0.3645，只對九鏡跑一次 `keyframes --takes 3`。新媒體帳本為 508 筆、US$3.4290，舊值 472 筆、US$3.1860；增加 **18 張圖、18 次 Gemini 圖評、估算 US$0.2430**。共享帳本已讀回 U09 整集估算 US$4.129／US$6，預留狀態已核銷。此數是工具帳本估算，不是供應商最終發票。
- 新 `keyframes/manifest.json` SHA-256 `44A280F3BFE5D6B311AC7402A36AE0489182770AB90FEDA11AA5994AB5C789DC`；`media/ledger.json` SHA-256 `E933CEF664E37BF5EB8D084E223F02286C79BFD002D54DAEB96A37E754E678D1`，存於 repo 外 `<home>/mokaair-work/videos/curio-u09/`。91／91 有圖、89／91 評審通過，兩鏡仍待修；本輪九張選圖均以原尺寸打開核對旁白。

| 鏡頭 | 最終選圖（`keyframes/` 下，SHA-256） | 評審／目視判定 |
| --- | --- | --- |
| `missed-session` | `missed-session-2.jpg` `66F019FD28A12FC5F33FC1D7624A0F2D59D17C85426D1441410C0151C690B2E6` | 通過；一人坐在講堂面向黑板，沒有出現在快紀錄器旁。遠景偏寬不是史實矛盾。 |
| `brief-window` | `brief-window-2-trim.jpg` `DA2E411EEA5855ADD776F39C45CD728A30578CB522F06D03F282433BFCCB811F7` | **待修**；評審 frame 未過，上下仍有黑邊。畫面有人操作儀器，但不能以高總分覆蓋未過項。 |
| `another-pulse` | `another-pulse-1.jpg` `0B1F06ED767666E4A22C928BD384C17EA2B52099E4DEB82B4E69491225422216` | 通過；紀錄器吐出一條連續紙帶，紙上有多段墨跡。 |
| `more-marks` | `more-marks-2-trim.jpg` `C596D049A2E73A7138A081DAD891858E180430EC879C69066CFB0149B059270C` | **目視退回**；評審雖通過，圖把墨跡放在桌前三張分離的紙上，與旁白「同一卷紙上又有兩處」直接矛盾。 |
| `public-boundary` | `public-boundary-1-trim.jpg` `C4DA56B175A92188C5AE4E6FCEC88034B02F5CBBF4AB8DA2D5A4FA7596A345A4` | 通過；兩名虛構閱讀者拿著稿頁與脈衝圖，多一人是次要插畫細節，沒有把暫定解釋畫成定論。 |
| `line-of-sight` | `line-of-sight-2-trim.jpg` `3A11E2322DF5F13793F65E00C4080773F45610121386051E0F615F605CBFE547` | **目視退回**；評審雖通過，細線由星體小模型指向畫面上方，沒有碰到旁邊的地球儀；與「波束掃過地球」方向相反。 |
| `beam-away` | `beam-away-2-trim.jpg` `83FCBC81BF0DAFAEDFADD3107BBAAB0FA8146262D39172F79FD71A398ABF91BA` | **待修**；評審 subject 未過，人物與動作不符；目視還見主要光束來自檯燈，不是小星體模型，無法證明「星體波束轉向別處」。 |
| `testable-prediction` | `testable-prediction-2.jpg` `3774BB30F92B7F1B1D17AEA86AC8AA9917BAB6A91E3A292BC600674D2ABB8A4F` | 暫收；評審通過。紙上四排星形記號未清楚顯示間距變慢，也不聲稱已觀測到預測結果；屬表意較弱，不是反向史實。 |
| `later-support` | `later-support-2-trim.jpg` `31BAB25B5682EE0E130AE8336AFAC722B799E4CB6E5F90F08FA631C17774E155` | 暫收；評審通過。地球儀與小接收器可辨，星體及其波束缺席；只是不完整，沒有畫出錯誤發射源。 |

按系列 skill 的「只退會誤導的圖」界線，九鏡中五鏡可收、四鏡阻擋；連前輪其餘已驗圖，**目前最多 87／91 可用**。兩張評審通過但與旁白矛盾的圖不得當成有效分鏡。四頁聯絡表不能送站主核准。

## 同章退路與付費界線

四鏡均已歷經三張嘗試及提示詞修訂。`curio-episode` skill 的退路是使用同章已合格圖，或在卡片比例仍合規時改一張卡；不應無界重畫。原尺寸複查後可供主代理試切的**候選**如下，尚未替換、未重新評審，也不是定稿：

| 阻擋鏡頭 | 同章已通過候選 | 取捨 |
| --- | --- | --- |
| `brief-window` | `cold-return` | 有冷機房、接收器與操作人員；不會聲稱設備已量到訊號，但缺「短暫穩定／對準」的細節。隔三鏡，避免緊貼重複 `switch-work`。 |
| `more-marks` | `another-pulse` | 一條連續紙帶有多段墨跡，保留「同卷」；沒有明確兩組相隔很遠的痕跡。與原鏡相隔九鏡。 |
| `line-of-sight` | `lighthouse` | 光束掃過海面的已過插畫，只能作前一句燈塔比喻的延續，不能當成地球／接收器的實物示意；與前一鏡相同，節奏上明顯重複。若不接受重複，需要另走一張限額新圖或合規卡片。 |
| `beam-away` | `rotation-proposal` | 星體往空處放出單一道光，沒有錯誤的太空接收者；地球未畫出，靠前後鏡與旁白界定「別處」。相隔三鏡。 |

複用要連 `data.prompt` 和 `data.camera` 一起比對原鏡，才可能命中 MiniMax 圖片快取；工具的 Gemini 逐鏡評審仍可能是**新的付費呼叫**，不能把退路報成零成本或繞過分鏡門檻。若主代理採用，先做精確乾跑及共享帳本預留，且逐張確認新的 manifest 綁定、評審及接在旁白前後的畫面。此收據沒有改 `video.json`、媒體 manifest 或費用帳本，也沒有再次付費、送審或發片。
