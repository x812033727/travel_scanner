# S50 R7｜首輪原生插圖獨立驗收

2026-10-20 UTC。對照 [試畫門檻與預算](r7-media-budget.md)、R7 `video.json` 精確 SHA-256 `e2c2537dc0fe97807e1f686a7d511b5f64d03680f89c1c0461cec3bbe8ad0234`、`claims.md` 及 `research.md` 的 R01／R02／R12。逐張以 `view_image` 的 **original** 檢視下列原生 1280×720 JPEG；沒有以 manifest 所選的 `-trim.jpg` 或縮圖代替。插圖是卡通示意，但人物、動作、可見事實仍須符合旁白與來源界線。

| 景與原生圖 SHA-256 | 人工判定 | 原生畫面及來源／旁白比對 |
| --- | --- | --- |
| `fire001` · `0e8a96d6a53b94ce6123e7ae13888a66c098a8b369b68182990c0467e17f3284` | **REJECT** | 只有一人、確實躺在床上，但像兒童而非成人；寬幅玻璃窗、橫簾、現代城市燈光與家具不似 1666 年倫敦。窗外沒有可辨認煙柱，也看不見木窗板。R01 只記布丁巷起火屋址，R02 事後記夜深有人未醒；此圖不應讓兒童或這戶睡者變成已知屋主／點火目擊者。原生圖無可讀文字瑕疵。 |
| `fire013` · `c58e188965f03e924f0bdc55654dccea40b306d3957eb2b064fb6e3f8531bca1` | **REJECT** | **兩名**兒童模樣人物，其中左側在手推車旁站立，沒有拉動；道路標線、店面盆栽和遠方懸索式橋均不屬 1666 年倫敦橋街景。煙很淡，火沿坡道朝橋的方向也沒有顯示。R02 是 Vincent 的事後火線回述，畫面不應像當時路人對火線的可靠目擊紀錄；匿名搬運者只能作環境示意。無可讀文字瑕疵。 |
| `fire096` · `f3855fda3f35b413cd7b7fab21bb54f2498f2b779ac1dd57fa5787e3e513ac9e` | **REJECT** | **兩名**兒童模樣人物，沒有一位清楚以手指指向地面；左手形狀亦不自然。畫面以巨大的磚拱爐體為主，易把 R12 所說的「**房間地面**鋪磚」誤讀成已核實的磚造壁爐結構。地面有磚塊，但無法補救人數、動作與證據層級的錯誤。R12 只是 Farriner 本人的事後自辯，不證實火源或爐體構造；無可讀文字瑕疵。 |

**首輪結果：0/3 KEEP；未達至少 2/3 KEEP 的全 113 景門檻。** `keyframes/manifest.json` 三景的自動 judge 均標 `passed: true`（9.29、9.29、7.18），其中已指出 `fire001` 無窗板／煙、`fire013` 多人且未拉車、`fire096` 多人且未指地；自動通過不取代原生尺寸的人工事實驗收。manifest 的 `fire001`、`fire096` 選圖為修邊版本，所以此處明列原生 JPEG 的不同 SHA。

## 各景一次、有界的提示詞修補建議

只替換三景 `data.prompt`；旁白、來源、`look: {"preset":"cute-mystery"}` 及其他畫風欄位維持原定。下列只描述畫面內容，不把畫風詞寫進提示詞。每景只再產一張原生圖並重新人工檢查；這些建議**尚未改入** `video.json`，也尚未執行付費重畫。

| 景 | 建議的完整替換提示詞 | 修補與來源界線 |
| --- | --- | --- |
| `fire001` | `Medium shot inside a modest 1666 London timber home before dawn, exactly one middle-aged adult neighbor in a linen nightshirt sleeping in a simple wooden bed; through a small leaded casement with a partly open wooden shutter, a thin plume of smoke rises beyond nearby timber rooftops, soft candlelight from the bedside` | 明示單一成人、舊式窗與可見遠煙；仍是匿名鄰居睡夢中的示意，不指認 Farriner 或點火者。 |
| `fire013` | `Wide shot down a narrow sloping street lined with timber houses in 1666 London, the old stone-arched London Bridge with houses on it ahead; exactly one adult porter in a plain wool coat strides uphill while pulling a wooden handcart by its handles, glancing back at a low trail of smoke and flame moving downhill toward the bridge, soft grey morning light` | 以舊倫敦橋的石拱與橋上屋替代懸索橋；搬運者清楚拉車，遠火方向對應事後路線。他是匿名示意人物，不是 Vincent 或特定目擊者。 |
| `fire096` | `Medium shot inside a modest 1666 London room with timber walls and a broad brick-paved floor, exactly one middle-aged adult baker in a linen shirt and apron standing alone and pointing one clear index finger down to the floor bricks in front of his boots, a small unlit fireplace recess in the far wall, soft lamplight` | 以普通房間**地面**為視線落點，壁爐僅為遠處小凹處；示意 Farriner 後來所說的房間，不能當成火場勘驗、已證實的壁爐材質或點火過程。 |

截至檢查時，私有 `/workspace/.video-work/curio-s50/media/ledger.json` 有三筆 MiniMax 圖片各 US$0.0035、三筆 Gemini judge 各 US$0.01，**已記帳 US$0.0405**（3 張圖、3 次 judge、無配樂）。若第二輪三景各只產一張且以同價各判一次，增量預估 US$0.0405，累計約 US$0.0810；仍須按實際 ledger 核對，並受整集 US$4.66 一次性上限約束。若第二輪仍低於 2/3 KEEP，依試畫規則停止本方案；本報不放行其餘圖片、音樂或合成。
