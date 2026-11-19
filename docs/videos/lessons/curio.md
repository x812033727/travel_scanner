# 奇聞檔案局：教訓

只跟奇聞檔案局有關的教訓。所有 AI 劇都會遇到的寫在 `shared.md`，奇聞和原來如此都會遇到的寫在 `explainer.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/奇聞檔案局/_規則與教訓/教訓/教訓.md`（docs/videos/rules-sync）。
之前的教訓：`.agents/skills/curio-episode/references/w03-lessons.md`。

## 2026-11-19 · 站主定：開場鉤子禁疊「問題菜單」、開頭不放片頭
- **前 300 秒觀眾審查（硬性關卡）**：警告擋不住，所以配音前加一關：三位獨立讀者用三種觀眾身分（路人、滑手機的人、挑剔的老觀眾）讀前 300 秒，三位都 ≥ 8.5、不滑走、沒有任何問題才可以 `tts`。預設由製作中的 AI 自己派三個全新子代理（`--record`，不花站台額度，作者不能當讀者）；要多一層保險就用 `--ask` 讓站台的模型跑。多人比一人好：每個身分抓的問題不一樣。
- **開頭 15 秒接上縮圖**：觀眾是看了縮圖和標題才點進來的，開頭 15 秒沒聽到那件事，就會以為點錯（原來如此 QR Code 那集前 15 秒流失約四成）。lint：`narrative.mjs` `thumbnailEchoProblems`。現有 91 集裡有 38 集被抓到，例如 curio-s27 縮圖寫「維京盔沒有角」，開頭卻在講挪威農家挖地。
- **開場只問一個問題**：鉤子是一個問句或觀眾熟悉的情境，接反差與承諾句；不准連丟三個以上問題把這集排成菜單（其他問題變成後面章節的 `loops`）。lint：`narrative.mjs` `questionMenuProblems`（`curio-`、`story-`、`sothatswhy-`），開場（第一章、最多 90 秒）扣掉承諾句的問句超過 2 句即警告。
- **開頭不放片頭，第一句直接開始**：新集不再先播頻道片頭，`0:00` 就是鉤子；片尾照舊。工具已預設 `intro_at: "none"`（`core/branding.mjs` `noIntroSeries`），已 pin 的舊片不動。

## 2026-11-18 · curio-w01／w02／s13-v2／s26-v2 · 對標黑猫研究院（`@qiqiqushi0`）補強旁白去但書化、禁用萬用道具與停頓快推運鏡
對比黑猫研究院高點閱長片與本系列已交付集數（W01、W02、S13 v2、S26 v2），補齊縮圖（#2164）與需求四問（#2136）之外影響完播率與視覺重音的三處差距：
- **旁白清掉法條但書、「查不到」與多版本史料校勘，改講人的困境與出招**：W01 旁白連講 5 次「照…的公開資料／年報寫／翻遍年報也找不到／沒有公布評審補助費／千萬別聽成…」，S 系列中段也常停下來逐條比對三四種史料版本，聽感像審計報告與文獻校勘。精準的法規適用範圍、年報附註與未公開數字一律放進 `claims.md` 與 `youtube.description`；旁白只講「誰被逼到牆角、對手出了什麼招、這一招買到或賠掉什麼」，歷史奇聞跟著當事人的抉擇走（`narrative.mjs` `caveatRecitationProblems` 全集超過 1 句即警告，盲評 `STORY_SERIES_PANEL_QUESTIONS.no_detour` 同步把關）。
- **插圖禁用萬用「鼓扁錢包／空白厚書」洗版，同類上限 2 鏡**：W01 畫了 4 次錢包、W02 畫了 7 次錢包、S13 v2 與 S26 v2 分別畫了 9 次與 10 次素色厚書，導致觀眾每分鐘都在看同一種代替物。數字與機制優先畫該題專屬的無字實體物件、剖面或動作反差（如輪胎胎紋、黃銅閥門、封條木箱、插進鎖孔的鑰匙）；`purse`／`wallet` 與 `thick/plain-covered book` 全集同類最多 **2 鏡**（`curio.mjs` `genericPropWarnings` 達 3 鏡即警告）。
- **合成運鏡 `still_motion: "beat"` 升級為 `beat-motion-v5`（停 0.8 秒＋快推 2.2 秒）**：舊版 `beat-motion-v4` 讓 6 秒靜圖全程勻速滑行，1080p 實測 `slow_share` 高達 `0.580`，畫面像慢慢飄；改為先停 24 格（0.8 秒）看清構圖、再用 66 格（2.2 秒）完成 `zoom: 0.22`／`panZoom: 1.2` 快推或橫移並停在特寫細節接 15 格淡化後，`slow_share` 降至 **`0.059`**（≤ 0.30 達標）、`high_motion_share` **`0.084`**、`mean_difference` **`5.78`**，貼齊黑猫實測區間。
- 已升為規則：`tools/video/automation/register.mjs`、`tools/video/core/narrative.mjs`、`tools/video/core/curio.mjs`、`tools/video/assemble/drama.mjs`、`.agents/skills/brand-story/SKILL.md`、`.agents/skills/youtube-video/references/script-writing.md`、`.agents/skills/producer/references/pace-targets.md`。

## 2026-11-14 · curio-s10／s13／s23–s26-v2、w01、w02 · Claude（c14 重做收尾）
八集都照 PR #2099（同節拍 2–3 句併一景、說明欄與縮圖新規則、八語系列後綴）與語速 4.4 重做完，八語 MiniMax 配音。這一輪學到的：
- **先確認稿子版本**：W01、W02 在 main 上的 `video.json` 停在 11/04 舊稿，真正做成成片的稿子只在 Drive 製作檔的 `_repo/docs/videos/<slug>/`。拿舊稿併景、重錄會白花錢，而且 `status` 才會顯示「manifest 沒有圖」。重製前先跑 `status`：`keyframes drawn` 是 [x]、manifest 的 shot id 對得上 scene id，才動手。
- **聲音指示**：「語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音。」W01 實測 4.84、W02 4.58–4.61 字／秒，不用 `voice.tempo`。
- **MiniMax 外語比 dub 的預算估得慢**：八語第一輪幾乎每語都有句子塞不進；縮過一輪剛好卡預算的句子，第二輪還會超。縮句時每句比預算再少 2–3 字（泰語 3–5 字）。日語一集常要縮 60–80 句。
- **念法**（MiniMax）：越南語千分位點「35.000」念成 35 → 寫 35000；韓語千分位逗號與「2만 5000」會漏念「2」→ 寫「2만 5천」；印尼語月份或句首直接接年份會被聽成時間（「2019,」→「Twenty Four Seven」）→ 加 tahun；「NT$10 million」念成 19 million → 寫「10 million Taiwan dollars」；西語縮寫「EE. UU.」避免，寫全名。日語：「年報」念成「れんぽう」→ 寫「年次報告」；「家庭用」念錯 → 「かてい用」；「下がる」的「下」會念成「もと」→ 換「落ちる／低め」；數字與年份念錯（250→150、2400万→40万、2025→2015、61→11）就改假名；「年平均250」會被聽成「年平均に150」→ 寫「年平均で250」。
- **改寫後一定量長度**：比預算長的句子 `--keep-fitting` 不會換掉，舊錄音留著但字幕已是新字，兩邊對不上。改完要看 dub 有沒有印 `do not fit`，有就再縮或改回原句。
- **check-audio 的 Gemini 會限流**（「請求過於頻繁」），那一輪顯示的 0 flagged 是沒檢查到，要重跑；第二意見用 `--second-opinion "python3 tools/video/tts/whisper_second_opinion.py"`（WHISPER_MODEL=medium）。剩餘標記以人名、同音字為主時就收工。
- **外語縮圖**：羅馬字人名或 Michelin 這種 8 個字母的詞單獨一行就只剩 23 px；第一行換短的主體詞（Stars、Guía、Sanada），第二行粗體 6–7 個字母內；日語問號用半形 `?`（全形會掉 2 px）。逐語用 `headlineSizeEstimate` 估過 24 px 才渲染。
- **備份與配音不要同時跑**：配音在寫檔時 `todrive` 會報 differences，備份被判不乾淨；先排除 `dubs/` 備份、推成片，配音完成後隨上架包再整包備份。
- **web.archive.org 從雲端容器連不上**（proxy 斷線），qa 的 links 會把存檔連結判成打不開；用 `https://archive.org/wayback/available?url=<原網址>&timestamp=<時間>` 查得到 200 就是連結沒壞。
- **磁碟**：每集上架包推完、todrive 0 differences 後，刪該集 `build/`、`segments/`、`keyframes/`、`dubs/*/audio`（逐句錄音約 1 GB），留 `final.mp4`、`upload/`、各語合成好的音軌。

## 2026-11-13 · curio-s10／s13／s14／s23–s26-v2 · 站主發現、Claude 量
設定都是新版，實測語速卻都不到 4.4：停頓（0／150 毫秒）與 beat 都對，聲音指示也寫了「一秒四到五個字」，七集實測只有 4.08–4.33 字／秒。站主定 4.4 為下限，不符合的全部重做，八語改用 MiniMax 重錄。
- **怎麼量**：timeline.json 每句 `audio_samples` 加總 ÷ 48000 是純講話秒數；字數用稿子去掉空白與標點。全片長度除會把換景停頓算進去，偏低。
- **為什麼慢**：Gemini 會把聲音指示裡的速度打折扣，要寫比目標快的速度（原來如此寫「一秒五個字以上」才念到 4.4）。
- **下次怎麼做**：錄完旁白先量語速，到 4.4 才送審；check-audio 過了不代表語速對。
- **重錄的限制**：同一集正在跑 `keyframes` 時，`tts` 會被鎖（「the project is held by keyframes」）什麼都不送；換聲音指示的重錄排在關鍵影格畫完之後。
- 已升為規則：`.agents/skills/curio-episode/SKILL.md` §系列定案〈語速與停頓〉〈八語〉。

## 2026-11-13 · curio-s23-v2／s24-v2／s25-v2 · Claude（c14 重做）
image-01 插圖過了 judge 還不夠，獨立放大檢查每集都抓出約一半要重畫。三集都反覆出現下面這些問題，都是 judge 放過、放大看才看到的：
- **錶面、刻度、書頁會長出字或數字**：寫「closed」「face down」都沒用。改成闔上的木製錶盒、闔上的書、綁繩的卷軸、捆起來的紙束。錶盒的黃銅扣片會被看成眼睛或字，寫 `a plain wooden box tied with a simple cord`。
- **只寫手的鏡頭會冒出整張臉**：常常就是那位不該入畫的人（例如 1912 年的寫信人）。一律改成只畫物件的靜物，並設 `nobody`。
- **畫風開頭**：`Flat 2D drawing, bold dark outlines, simple shapes.` 有效。換成 `Flat 2D picture, heavy dark linework.`、`Flat 2D image, strong inked contours.` 幾乎都被畫成動畫背景或 3D。lint 會警告這個開頭用太多次，不用理它。
- **戶外場景**（樹、果園、草地）：一直被畫成柔邊的白天風景。改成 `deep navy night sky` 配單一物件的近景才過。
- **三角帽**（牛頓的代表物）：俯視一直畫成軟呢帽、牛仔帽，甚至長角。正面視角（`Front view of a plain matte black three-cornered tricorn hat with its wide brim folded up into three sharp points`）才畫得出來。帽子要全集一致：宣告代表物的那一景，要跟後面每一景同一頂。
- **Ada 走樣**（變小孩、包頭、短髮、短袖、耳環、眼鏡歪）：固定描述要加 `shoulder-length wavy black bob with a side fringe, white collared shirt under a long-sleeved mustard knit cardigan, adult proportions, chest up`。手上不拿東西，只寫一個表情。
- **天平、弩炮、倒插的箭、打開的門**：模型畫不出特定的傾斜或方向。改成不靠那個動作也能對上旁白的畫面，例如用兩樣東西對比、畫結果、換一個物件。
- **judge 只因小地方退件的 take**（瀏海少一撮、多一個髮夾）：放大檢查乾淨的話，可以用 `keyframes import --provider external --usd 0` 直接選用，比一直重畫省錢。
