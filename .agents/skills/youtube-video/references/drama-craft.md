# 漫劇的手藝規格：開場、鏡位、剪接節奏、台詞與包裝

寫**有角色的漫劇**的劇本與分鏡之前讀；查核、修鏡頭、收到「看不下去」的回饋時再對一次。`.agents/skills/youtube-video/references/visual-quality.md` 管的是一版做出來之後怎麼診斷、怎麼改、怎麼留證據；這一篇管一開始就照什麼規格寫，以及用哪支腳本量。兩篇都不改授權、預算、模型、來源與核准流程。

不適用的：沒有角色的漫劇（扁平解說、品牌故事）照自己的 reference 寫，檢查腳本遇到 `characters` 是空的會說明並跳過。有角色、但整集沒有任何角色台詞的重述（神話那一類）照這篇寫，`hook.dialogue` 與 `lines.narrator` 兩列會沒過，在回報裡寫「依故事聖經，沒有角色台詞」。

規格分兩種，表裡分開標。**量到的**來自 2026-10-03 對五支以「AI漫剧」搜尋選出的中文漫劇（查閱時合計約 418 萬次觀看，含站主指定的《山海经之万兽图鉴》）前四分鐘的量測，紀錄在 `docs/videos/drama-craft/reference-study-20261003.md`；其中標「目視」的是看聯絡表的印象，沒有逐鏡計數。**編輯判斷**沒有量測依據，照剪接常規定的。量到的只說明「這幾支片長這樣」，不證明照做就會被看完，也不代表站主的 90 分。

## 一張表：參考片、目標、我們的試作

| 檢查列 | 項目 | 參考片 | 目標 | 《喜宴未散》E1／E2 實測剪輯 |
| --- | --- | --- | --- | --- |
| `pace.median` | 鏡頭長度中位數 | 1.5–2.25 秒 | 2–4 秒，建議 2.5–3.5 | 3.3／3.8 秒 |
| `pace.p90` | 九成的鏡頭不超過 | 2.5–4.75 秒 | 6 秒 | 5.1／5.2 秒 |
| `pace.longest` | 最長的鏡頭 | 3.75–10.25 秒 | 不超過 8 秒 | 7.3／6.1 秒 |
| `pace.spread` | 長短差（第 90 百分位 ÷ 第 10） | 3.3–6.3 倍 | 至少 2 倍 | 2.4／1.9 |
| `hook.opening` | 前 10 秒開始的鏡頭 | 4–8 個 | 至少 4 個 | 3／3 |
| `hook.opening30` | 前 30 秒開始的鏡頭 | 12–18 個 | 至少 10 個 | 9／8 |
| `hook.card` | 片頭 | 沒有，最長 0.25 秒 | 第一個場景是鏡頭，不是卡片 | 是鏡頭 |
| `hook.dialogue` | 第一句角色台詞 | 第一行字幕在 0.6–1.3 秒 | 10 秒內 | 5.2／0.2 秒 |
| `lines.median` | 台詞一句的長度 | 1–11 字（逐行數過的那支中位數 4） | 中位數不超過 12 字 | 10／13 字 |
| `lines.long` | 超過 20 字的句子 | 沒有看到 | 不超過一成（編輯判斷） | 0% |
| `lines.narrator` | 旁白占比 | 五支有四支前 60 秒的字幕讀起來都是對白（靜音下的判斷） | 不超過 35% | 8%／0% |
| `size.face` | 看得清表情的臉 | 幾乎每個鏡頭（目視） | 至少四成 | 51%／75% |
| `size.insert` | 插鏡（手、道具） | 約 5–17%（一支逐鏡數、兩支目視） | 5–25% | 46%／20% |
| `size.wide`、`size.reestablish` | 全景或多人鏡頭 | 每 6–8 個鏡頭一次（目視） | 5–30%，最多連 9 個鏡頭沒有 | 0%，整集沒有／3%，連 24 鏡 |
| `size.stall` | 同景別拍同一批人 | 沒有量 | 最多連 2 個（編輯判斷） | 連 5／連 2 |
| `size.named`、`size.agree` | 沒寫景別；`camera` 與 `prompt` 的景別不同 | — | 不超過兩成；0 個（編輯判斷） | 3%／2%；0 |
| `motion.look`、`motion.run` | 只有眼神、表情、呼吸或顫抖的鏡頭 | 沒有量 | 不超過三分之一，最多連 2 個（編輯判斷） | 33%，連 3／32%，連 2 |
| `motion.opening` | 開場三個鏡頭 | 都在事件裡 | 不能三個都是上面那種 | 三個都是／有動作 |
| `motion.repeat`、`cut.dissolve` | 同一種運鏡；溶接 | 沒有量 | 最多連 3 個；不超過一成（編輯判斷） | 0；0% |

E1 第一個鏡頭是 5 秒的旁白配鎖定中近景，動作是手指握緊一次；兩集 81 個鏡頭的 `camera` 全部寫鎖定。E1 的台詞長度與旁白占比已經在目標內（E2 的台詞偏長）；差的是開場、空間、插鏡太多與開頭三鏡沒有事發生。這是站主那句「不會想繼續看」在分鏡上對得到的地方。

## 一、開場：前 10 秒與前 100 秒

1. **第一格就在事件裡。** 參考片從一件正在進行的事開始，三支有旁人在看：敬茶、召喚測試、校門口被議論。沒有片頭卡、沒有世界觀說明。A 片的全景只停 1 秒。
2. **前 10 秒至少四個鏡頭，各回答一個問題**：這是哪裡（全景）→ 主角正在做什麼（中景，動作看得到）→ 她現在什麼心情（臉）→ 對方怎麼回應（反應鏡）。每個鏡頭給新的資訊；同一句話配兩個相似的畫面不算。全景配一句四個字以內的話，約兩秒：估計長度是每字 0.24 秒、每句 0.3 秒、每鏡 0.7 秒，而此批 `clips` 規格一刀最短 2 秒。
3. **10 秒內看得到衝突，30 秒內升級，100 秒內第一次反擊或轉機。** 量到的：A 片 8 秒婆婆不接茶、約 105 秒潑茶；E 片 22 秒宣布失敗、95–98 秒異獸出現；D 片 47 秒重生；B 片 13.6 秒反轉。既有規格更嚴的地方以它為準：有節奏規格的題材照 `.agents/skills/youtube-video/references/series.md` 的 `RETENTION_RULES`，十部動畫照 `.agents/skills/youtube-video/references/animation-production.md` 的「前 5 秒鉤子與 30 秒第一次回報」。
4. **旁白開場只有一種寫法**：主角自己的第一人稱獨白、一句話一個畫面、45 秒內講完並接回當下（參考片 D）。獨白是主角的聲音：`speaker` 寫主角的 id，`emotion` 寫「內心獨白」。畫面仍然要有事發生；獨白配一張不動的臉，`motion.opening` 與 `motion.run` 會沒過。第三人稱旁白配一個站著的人，是這次被退回的開場。
5. 前世、回憶、設定用畫面帶過，不用一個鏡頭慢慢說；要說就拆成每句兩秒的蒙太奇。
6. **頻道片頭**：裝了片頭素材的長片，正文前面會先播站主選定的 5 秒片頭（`docs/videos/README.md`、`docs/videos/BRANDING.md`），漫劇也算。這裡的秒數都從正文第一格起算，檢查腳本也只讀 `video.json`。參考片沒有片頭；漫劇要不要跳過片頭，列在最後一節等站主決定。

## 二、一場戲怎麼拍：鏡位與剪點

**鏡位**是攝影機擺在哪、拍誰；**剪點**是換畫面的那一刻。參考片一場對話只有三、四個鏡位，卻每兩秒換一次畫面：說話的人、聽的人、再回到說話的人。把分鏡寫成「一句台詞一個全新的構圖」會散；寫成「一個鏡位站著講完」就是簡報。

每一場戲先列鏡位，再排剪點：

| 鏡位 | 用途 | 規則 |
| --- | --- | --- |
| 全景或多人鏡頭 | 誰在哪、門在哪、誰在看 | 開場、換場、有人進出、新的節拍開始時各一次；約兩秒就離開 |
| 每個說話的人各一個中近景 | 看他說 | 視線有對象，不看鏡頭 |
| 聽的人的反應 | 這句話打到誰 | 重要的台詞後面接它，畫面是聽的人，聲音是說話的人 |
| 過肩 | 兩人的距離與高低 | 對峙、逼近、遞交時用 |
| 插鏡 | 回答一個故事問題：哪一份、誰的手、簽了沒 | 位置、留白與手的指向交代狀態，不靠多畫幾行字 |

- **回到同一個鏡位**時，`camera` 整行與 `prompt` 的第一個子句照抄上一次，只改表情與動作。腳本把這兩段相同的鏡頭算成同一個鏡位，印出「幾個鏡位／幾個鏡頭」；回報裡寫每場戲用了幾個鏡位。現在的工具每個鏡頭仍各買一張關鍵影格與一份素材（見第五節），所以這是為了畫面連貫，不是為了省錢。
- 同一景別拍同一批人最多連兩個；第三個改切反應、插鏡或換軸線。
- `camera` 的**第一個詞寫景別**，後面才寫運鏡或「locked」。腳本與圖片模型都讀它；`camera` 沒寫時才讀 `prompt` 裡明寫的景別（`Wide shot of …`）。兩邊寫的景別要一樣。

  | 寫在 `camera` 開頭 | 算進哪一列 |
  | --- | --- |
  | `Medium close-up`、`Close-up`、`Extreme close-up`、`Over-the-shoulder` | 臉（`size.face`） |
  | `Wide`、`Two-shot`（`Three-shot`、`Group shot`） | 全景或多人（`size.wide`、`size.reestablish`） |
  | `Insert`，或拍手與道具的近景（`Close-up of the pen hand`） | 插鏡（`size.insert`） |
  | `Medium shot`、`POV` | 三列都不算 |

- `prompt` 寫的是這個鏡頭的**第一格**，也就是 `motion` 的動作開始之前那一刻（手舉在桌面上方，不是紙已經放平）。剪進去的只有素材的前幾秒，`motion` 要寫這幾秒裡看得完的事。
- 這一節只管鏡位與剪點。一場戲的軸線、視線、進出同側與採用格連戲帳在 `.agents/skills/animation-camera/SKILL.md`「一場戲先定空間」與 `.agents/skills/animation-camera/references/scene-coverage.md` 第一節；上面那張景別表只是 craft 讀的那一份（`tools/video/core/craft.mjs` 的 `shotSize`），三個程式讀者（craft、插畫投影片的 `cameraMove`、assemble 的 `motionMove`）各從 `camera` 讀出哪些字、哪些字會分家，逐字表在 `.agents/skills/animation-camera/references/camera-keywords.md`。

## 三、鏡頭裡要有事發生

- 每個鏡頭寫一個**對人或對物做的動作**：端給、別過臉、推回去、撕開、放下、指著、站起來。`motion` 以「誰＋動詞」開頭；畫面裡只有一個人時可以省略主詞。
- 眼神、表情、呼吸、手指收緊、站著不動是反應，不是動作。反應鏡需要它們，所以腳本量的是比例與連續：不超過三分之一、最多連兩個、開場三個不能全是。加一個慢推不會讓它變成動作。
- 鎖定機位不是預設值。對話的近景可以鎖定；進場、揭露、情緒升高給推近或跟拍；同一種運鏡最多連三個。
- 一鏡一個主要動作、一種運鏡的限制不變（animation-production.md）：動作大不等於動作多，「伸手、拿起、交出、對方反應」仍然拆鏡。
- `visual: "still"` 的鏡頭畫面不會動：`prompt` 寫動作進行到一半的那一格，運鏡寫在 `camera`（關鍵字表在 `.agents/skills/youtube-video/references/drama.md`）。靜圖鏡頭的 `camera` 要寫運鏡或 `locked`：工具只讀 `camera`，不讀 `motion`（「推回去」「站起來」是畫面裡的事）；沒寫的鏡頭緩慢漂移（`drift`），寫 `locked`（static、fixed、tripod）就整格不動。
- 來源沒有的行為不能為了好看加進去；先在來源允許的行為裡挑看得見的那一個。

## 四、台詞

- 場上的人先開口。旁白留給時間跳接，占比不超過 35%。
- 一句以 12 字以內為主，超過 20 字的不超過一成；長句在換畫面的地方斷成兩句、兩個鏡頭。
- **長短要有差**：以一句一個鏡頭為主，但每場戲要有兩到四個字的短鏡，也要有一個把兩句掛在同一鏡上的停留（揭露或決定之前那一拍）。每個鏡頭都一樣長是節拍器；`pace.spread` 量這件事。
- **反應鏡與插鏡放的是畫外那個人正在說的那一句**：`speaker` 是說話的人，`data.characters` 只列畫面裡的人，`prompt` 寫明說話的人不在畫面裡。完全沒有聲音的動作鏡寫 `action_seconds`（1–8 的整數）加空的 `lines`，長度就是它；`lint` 只在兩種影片接受：有角色、沒有時長下限、不是知識長片、`category` 不是 anime 的漫劇（`tools/video/core/drama.mjs` 的 `timesSilentShots`），與 production policy 有效的 `long-anime-v1` 長篇動畫（`tools/video/core/anime-policy.mjs` 的 `validateAnimePolicy`）。旁白講述的影片、品牌故事那類有 480 秒下限的知識長片（它們的長度在旁白上量）與沒有有效長篇政策的 anime 類沒有這種鏡頭；完整條件在 `drama.md` 的「video.json 的重點」。檢查腳本的 `lines.empty` 只數既沒有台詞也沒有 `action_seconds` 的鏡頭。
- 我們不放名字卡、字幕是可開關的 CC，所以**第一次出場的人要被叫出名字或身份**（「媽，請喝茶」），關掉 CC 也知道誰是誰。

## 五、節奏與成本

- 目標是中位數 2.5–3.5 秒、九成不超過 6 秒、最長 8 秒，開場 30 秒至少 10 個鏡頭。參考片更快（中位數約 2 秒），我們先到這裡；中位數低於 2 秒就合併。檢查腳本的門檻是 `tools/video/core/craft.mjs` 的 `TARGETS`：`pace.median` 在 2–4 秒之間都算過（`medianShotSeconds`；2.5–3.5 是建議），`p90ShotSeconds` 6、`longestShotSeconds` 8、`opening30Shots` 10。
- `lint` 對有角色的漫劇在中位數低於 2 秒才警告（`tools/video/core/drama.mjs` 的 `MIN_MEDIAN_SHOT_SECONDS`；旁白講述的影片仍是 3 秒），並把這份規格沒過的每一列印成警告（`craft hook.opening: …`；同一套實作在 `tools/video/core/craft.mjs`，檢查腳本與工人都讀它）。免關卡作品的工人在開場與鏡位那幾列（`CRAFT_GATE_ROWS`：`hook.*`、`motion.opening`、`size.face`、`size.wide`、`size.reestablish`、`size.stall`）沒過時直接退回撰稿，其餘列由撰稿修或在回報裡回答。
- 切得密要花錢，而且照鏡頭數算，不照成片秒數算：每個鏡頭是一張關鍵影格、一次 judge，`clips` 等級再加一份素材與一次 judge。素材買幾秒由 `tools/video/media/clips.mjs` 的 `clipSeconds` 決定，不是鏡長：`veo-3.1*` 配 1080p 固定 8 秒（此批，價目在 `docs/videos/series-plans/production-20261001/profile.json`）；其他模型是鏡長進位成整秒、夾在 `MIN_CLIP_SECONDS` 4 與 `MAX_CLIP_SECONDS` 10 之間，再往上貼齊模型可給的秒數，所以 4 秒以下的鏡頭都買 4 秒。`hybrid`、`stills` 等級的靜圖鏡頭不買素材，但圖與 judge 照算。一鏡、一集、一個月各多少錢，三條路線（伺服器 API、Hailuo 網頁、Kling）的價目與額度，在 `.agents/skills/animation-production/SKILL.md`「錢怎麼算」「三條路線」，每個常數的出處在 `.agents/skills/animation-production/references/cost-model.md`。先把密度給開場 30 秒與每個爽點；任何等級，整集估價超出已核定的額度時，列出鏡頭數與金額問站主，不自己加。
- **同一份素材切兩三次**（說—聽—說回到同一鏡位）：第二次回到鏡位的鏡頭寫 `data.source: { shot, from_s }`，它不畫關鍵影格、不買素材，`assemble` 從那個鏡頭的素材第 `from_s` 秒切進來；`from_s` 加鏡長要在 lint 的上限內（`tools/video/core/drama.mjs` 的 `MAX_SOURCE_CLIP_SECONDS` 10 秒；有 production profile 的作品 8 秒，`tools/video/core/lint.mjs` 的 `productionShotProblems`），也要在來源鏡頭實際買到的秒數內（此批固定 8 秒；其他模型可能只有 4 秒，`clips` 在來源買下後把超出的切鏡標 `needs_review`），`clips --dry-run` 印出省下的秒數，帳本記一筆 `status: "cut"`。同一份素材放大成較近的景別（punch-in）還沒做：要拿一場試拍的素材量過 1.5 倍裁切後的畫質再決定，做好之前不要在分鏡裡假設它。

## 六、包裝

- 標題：處境的鉤子＋主角的反轉＋《劇名》；不提前講出排定的答案（既有規則）。
- 縮圖：依觀看數排的前 16 支裡，15 支是占滿畫面的臉、14 支在下三分之一放 4–8 個字的大字劇名。我們的 `headline` 上限約 12 字，寫 4–8 字。
- 多語：觀看數最高的那支有 10 種語言的 CC 與在地化標題。中文版定案後，標題說明與 CC 的語言照 `docs/videos/LANGUAGES.md` 做，是可以先評估的擴張。
- 畫質：五支裡三支最高 720p。先求 1080p 母帶乾淨穩定，不為更高解析度加預算。
- 與現行規格不同、要站主決定的四件事（預設都不變）：參考片全部**燒錄字幕**，我們只做 CC；一支有**角色名字卡**；兩支是**直式畫面**當長片上傳；參考片**沒有片頭**，我們的長片有 5 秒頻道片頭。證據在研究紀錄最後一節。

## 七、檢查

```bash
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs <VIDEO_DOCS>/video.json    # 撰稿後：長度照 lint 的估法
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs <實測剪輯.json>             # 旁白量過之後：用 shots[].editorial_duration_s
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs <檔案> --json | --strict    # --json 多出每個鏡頭被讀成什麼；--strict 有沒過的就結束碼 1
```

每一列是上表的一項：數值、目標、參考片的數字（沒有的標 editorial rule）；沒過的下面有一行怎麼改、項目代號與造成它的鏡頭 id。`info` 開頭的列只報數字。

- **什麼時候跑**：撰稿在 `lint` 之後跑、查核改完再跑、旁白實測剪輯出來後用實測檔再跑。
- **沒過怎麼辦**：改到過，或在回報裡逐項寫這一集為什麼不同（例如追逐戲沒有插鏡）。不改目標、不為一集調門檻、不靠改景別關鍵字騙過檢查。它不擋任何指令；`lint` 的錯誤要清掉，這支沒過的要改或回答。
- **它讀的是文字**：景別、運鏡、動作來自 `camera`、`prompt`、`motion` 的英文關鍵字。拿試拍兩集 81 個鏡頭與人工逐鏡判讀對照，景別 80 個一致、動作 81 個一致；換一種寫法仍可能誤判，覺得某列不對就用 `--json` 看那個鏡頭被讀成什麼。全過只代表分鏡的結構對了；畫面好不好看、演得像不像，仍要照 visual-quality.md 看實際小樣。
- 一個全新的代理只照這個 skill 寫了一段 24 鏡的開場（2026-10-03 的前向測試）：第一稿就過了當時 19 列裡的 18 列，前四鏡各有新資訊、衝突在 7.8 秒出現；它也回報了十幾處寫不清楚的地方，這一版已補上。這是一次測試，不是品質保證。

## 八、重新量參考片

換題材、站主給新的參考片、或距離上次量測超過一季時重量。兩種量法，紀錄都放 `docs/videos/drama-craft/`（資料夾的 `README.md` 列出每份紀錄、兩種量法的差別與 JSON 的欄位）：**瀏覽器探針**不下載、每 0.25 秒一格、看得到畫面內容，但一次只到 60–240 秒；**離線分析**（下一小節）逐格、任何長度、量得到聲音，但只有數字、要先下載。先寫探針的做法。在內建瀏覽器開影片頁，照 `.agents/skills/youtube-video/scripts/yt_shot_probe.js` 開頭的步驟：設定視窗大小 → 貼上腳本 → 等廣告結束 → `measure` 量前 240 秒 → `stats()`（看 `suspected_multi_cut_runs` 與 `high_motion_share`，見下面特效片那一條）→ 每鏡一格的聯絡表與每半秒一格的字幕帶各截圖。規矩：

- 至少三支、同題材；記片名、頻道、網址、查閱日、查閱當下的觀看數；量到的數字與原始鏡長寫進 `docs/videos/drama-craft/` 新的一份紀錄，不覆寫舊的。
- 「畫面可見」「推論」「沒有驗」分開寫，逐鏡數過的與目視的也分開寫。瀏覽器面板靜音時不對聲音下結論（有沒有旁白只能說「字幕讀起來像」）；只抽格就不對動作是否流暢下結論。
- 引用數字之前，拿一張聯絡表對過剪點；請另一個代理照同樣步驟重量一支，兩邊的剪點要對得上。
- **特效多、一直在動的片（打鬥、法術、閃電、粒子、攝影機從不停）腳本兩個方向都會錯**：鏡頭內每 0.25 秒的亮度差常在 20–60，跟剪點一樣大，所以 0.25–0.5 秒的短鏡連在一起會被併成一個剪點，閃光、爆炸長大、甩鏡的模糊格又會被算成剪點。`stats()` 的 `suspected_multi_cut_runs` 有任何一段，或 `high_motion_share` 超過約 0.1（2026-10-05 量前 60 秒：對話劇 xVXEefk1vWs 是 0.014、沒有任何一段；布袋喵 B 片是 0.646、11 段），就當成這種片：每一段用 1/8 秒的聯絡表（`every(start - 0.25, end, 0.125)`，見腳本開頭第 6 步）逐格數剪點，其餘的剪點也用聯絡表挑掉假的；鏡數、平均與中位數**只能寫範圍**（腳本的數字到對過聯絡表的數字），不能引用單一支片的精確值。例子是 2026-10-04 的真一隻布袋喵量測（`docs/videos/drama-craft/reference-study-20261004-budaimiao.md` 的「交叉驗證」）：腳本預設的剪點比裁定後少約三成，只看聯絡表目視數的又多約五成；B 片 19.75–26 秒與 213.5–220.5 秒腳本一個剪點都沒有，實際各有 8 個以上。腳本的 `cuts()` 沒有改，舊的量測仍然可以比。
- 不下載影片、不把別人的畫面或台詞放進我們的素材；引用只到說明結構所需的程度。
- 數字改了，回來改這一篇的表與 `drama_craft_check.mjs` 的 `TARGETS`、`REFERENCE`，兩邊一起；表裡每一列都對得到腳本的一列。

### 離線分析：任何長度、逐格

```bash
# 本機檔案；--range 可重複，省略就量整支
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file <影片檔> [--range 0-240] [--range 1800-1920] --out <OUT>/<id>.json
# YouTube：呼叫 yt-dlp 下載到暫存目錄、量完刪掉；--compare 拿既有紀錄對答案
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url <id 或網址> --range 0-120 --out <OUT>/<id>-0-120.json --compare docs/videos/drama-craft/reference-study-20261003.json
```

- **什麼時候用**：探針只量到 60 秒（面板藏著時 seek 失敗，`2026-10-05-re-run-yt-shot-probe-past`）、要量全片或第 30 分鐘、要量鏡內動作量或聲音時。它量不到畫面內容：景別、臉、插鏡、誰在說話仍要聯絡表與字幕帶（上一小節），兩種量法互補，不互相取代。
- **需要什麼**：ffmpeg，找法跟影片工具一樣（`FFMPEG_PATH`、PATH、Windows 的 winget 套件；指令只用參數陣列呼叫，Windows 與 WSL 都能跑）。`--url` 時另外要 yt-dlp（`pip install yt-dlp` 或 `winget install yt-dlp.yt-dlp`；不在 PATH 就 `--yt-dlp <路徑>` 或環境變數 `YT_DLP_PATH`）。yt-dlp 是當**外部程式呼叫**的，repo 不內含它的程式碼（Unlicense，借用它也只借做法）。**要不要下載是站主的決定**（YouTube 的服務條款）：腳本把檔案下載到暫存目錄，量完就刪（`--keep` 留著，路徑印在最後），進 repo 的只有 JSON 裡的數字；下載的影片不進 repo、不進素材。
- **量什麼、怎麼量**（每一條都寫在輸出 JSON 的 `method`）：
  - 剪點：`select='gt(scene,0.3)'` 逐格加 `showinfo`。ffmpeg 的 scene 分數是 min(d, |d − 前一對的 d|)／100，d 是相鄰兩格的平均亮度差（0–255），所以 0.3 是「亮度跳 30/255、而且比前一對多跳 30」的突變；探針的規則是 0.25 秒兩格差 26/255 加突變或直方圖位移。同一種量法、不同格距：相鄰格之間鏡內的差很小，所以門檻可以比探針嚴一點而不漏；ffmpeg 文件建議 0.3–0.5，`--scene` 可改。0.1 以上的候選分數都留在 `scene_scores`（`--floor`），不用重新解碼就看得到換門檻會多出或少掉哪幾個。剪點時間是新鏡頭的第一格（探針記的是取樣格，最多晚 0.25 秒）。溶接、慢擦接可能漏，閃光、爆炸長大、甩鏡可能多算——跟探針一樣，所以特效片一樣只寫範圍。
  - 動作：`signalstats` 的 YDIF，每 0.25 秒一格（`--step`），畫面先縮成 64×64、去掉底部 26%（燒錄字幕換行的地方），門檻照探針：差 <1 frozen、1–4 slow、>4 active、≥20 跟剪點一樣大；含剪點的取樣格不算。`near_frozen_share`、`high_motion_share` 與探針同名同義，可以直接比；`motion` 裡另有四種比例與平均差。它量的是畫面變了多少，不是誰在動。
  - 亮度與色彩：同一批取樣的 YAVG（平均、p10、p90）與 SATAVG，在 `picture`。
  - 聲音：`silencedetect`（−30 dB、至少 0.5 秒，`--silence-db`、`--silence-min`），`sound.non_silent_share` 是有聲音的比例，`silence_times` 列出每段靜音。有配樂的片幾乎不會靜音，所以這是台詞密度的**上限**，不是台詞；台詞長度與是不是旁白仍然只能從字幕帶讀。
- **輸出**：同 `docs/videos/drama-craft/` 紀錄 JSON 的形狀（`schema_version` 1；`videos[].ranges[]` 的 `shots`、`mean`、`median`、`p10`、`p90`、`longest`、`over_6s`、`opening_10s`、`opening_30s`、`spread_p90_over_p10`、`near_frozen_share`、`high_motion_share`、`cuts`、`lengths` 與探針的 `stats()` 同算法，`tools/reference-analysis.test.mjs` 拿 2026-10-03 紀錄的四段鏡長反算回每個已發表的數字），多出 `scene_scores`、`motion`、`picture`、`sound`，與 `source`（檔名、大小、sha256）。`--url` 時 `title`、`channel`、`published`、`views_at_check`、`highest_quality`、`caption_tracks` 從 yt-dlp 的 metadata 填；本機檔案這些是 null。欄位表在 `docs/videos/drama-craft/README.md`。
- **跟探針對答案**：`--compare <紀錄.json>` 把紀錄裡同一支片的每份剪點清單（`ranges[].lengths` 累加、逐鏡表 `shots[]` 的起點、`cross_check[].verifier_cut_times`）跟這次量到的在 ±0.3 秒內一對一配對（`--tolerance`），寫進 `comparison`、印在最後：對上幾個、只有這邊有的、只有紀錄有的。對話劇要先對過 2026-10-03 的清單（xVXEefk1vWs 前 120 秒的 46 個剪點）再引用它的數字；特效片兩邊都會錯，照上一小節只寫範圍。
- **還沒量的兩支**（2026-10-05 開這支腳本的環境連不到 YouTube，沒有下載任何影片；站主決定下載後在自己的機器跑）：

  ```bash
  node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url xVXEefk1vWs --range 0-120 --out <OUT>/xVXEefk1vWs-0-120.json --compare docs/videos/drama-craft/reference-study-20261003.json
  node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url m2qhz2n9618 --out <OUT>/m2qhz2n9618-full.json --compare docs/videos/drama-craft/reference-study-20261004-budaimiao.json
  ```

  要看的：第一支對上 46 個剪點裡的幾個（探針前 60 秒的 23 個全對上）、`high_motion_share` 是否仍遠低於 0.1（探針前 60 秒是 0.014）；第二支 19.75–26 與 213.5–220.5 秒各量到幾個剪點（裁定是各 8 個以上，探針一個都沒有）、全片的 `high_motion_share`（探針前 60 秒是 0.646）。數字出來後寫成 `docs/videos/drama-craft/` 新的一份紀錄（不覆寫舊的），再回來改這一節的數字與上一小節 0.1 的門檻，`reference-study-20261003.md` 的「獨立重量」補一句離線量到的結果。
- **測試**：`node --test tools/reference-analysis.test.mjs`，用 lavfi 合成的片（已知剪點、旋轉的中段、兩段靜音）與一個只會複製檔案的替身 yt-dlp，不連網；沒裝 ffmpeg 的機器（main 的 CI）會跳過實測那幾項、仍跑統計與解析的部分。

## 還沒驗、不能宣稱的事

- 聲音：配樂、音效、配音表演都沒有量；有沒有旁白是靜音下從字幕與畫面推的。聲音的做法照 animation-production.md 與 visual-quality.md，待有實際小樣再補規格。
- 留存：沒有任何一支的觀眾留存曲線；觀看數只說明有人點進來。
- 鏡頭內的動作量與攝影機運動、鏡位重複使用的比例：聯絡表看得出鏡位重複，量不出運鏡。
- 參考片的畫面怎麼做出來的：只有一支在畫面上標了 AI 生成。
- 這些目標全過之後站主會不會接受：要靠實際小樣、獨立冷看與站主自己看，不由這份規格或檢查腳本宣布。
