# 跟參考作品與業界做法的差距（2026-11-05）

站主評分：我們的動畫 40 分，參考的《孟婆今天也不想上班》（伶伶AI剧场）80 分。這份整理參考作品和其他 AI 漫劇／短劇團隊做了哪些我們沒做的事，
也列出業界常用、但我們產線還沒有的工具。已經知道的事不重講，只在對照時引用：

- 第一季審片：`season1-review.md`
- 每鏡規則：`.agents/skills/animation-preproduction/references/storyboard-shot-spec.md`
- 量過的觀看感：`camera-feel-study-20261105.md`（`origin/claude/zhong-tian-camera-feel` 分支）

**方法與限制**：只在網路上讀，沒有下載任何影片或軟體。YouTube 的影片頁與搜尋頁用抓取工具讀不到內容（只回頁尾），
所以參考頻道的資料來自公開的 RSS feed 與 oEmbed（標題、日期、觀看數、說明），畫面上的觀察沿用 camera-feel 那份的量測。
用這種方式看不到的項目（字幕字型、是否對嘴、配樂）一律標「未驗證」。中國的教學文章很多帶培訓或導流性質，引用的是它們的做法，
不代表那些做法有成效數據。

## 一、參考作品做了什麼（有出處）

### 1.1 《孟婆今天也不想上班》與伶伶AI剧场

- **頻道定位**：伶伶AI剧场的簡介寫的是古風各題材短劇全集（逆襲、宮鬥、甜寵、權謀、穿越、仙俠），內容純屬虛構。
  出處：[頻道頁](https://www.youtube.com/channel/UCjkV7Ezf_3hN3_5C1YnkSwA)（搜尋摘要）。
- **上傳節奏**：RSS 最新 15 支是第 12–26 集，2026-10-03 到 10-18 共 16 天，一天上一到兩集（10-08、10-09、10-10、10-14 都是一天兩支）。
  出處：[頻道 RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCjkV7Ezf_3hN3_5C1YnkSwA)。
- **標題格式固定**：寫成「【孟婆今天也不想上班_NN】阴间牛马日常 | 一句梗」，後面接一串固定 hashtag
  （#孟婆只想下班 #aishorts #ai漫剧 #ai短剧 #aivideo #aianimation）。
  - 每集的梗句都是職場流行語或歌詞：「令人心动的offer！」「简单点~说话的方式简单点~」「到底是谁发明的团建！」「一天天哪来那么多会要开！」。
  - 出處同上（RSS）。
- **說明欄是同一段劇情簡介**：每集都貼同一段，開頭是一句鉤子：「孟婆上一次准时下班，还是在秦朝。」
  接著是設定（每天熬一千碗湯、系統派 3,200 件急件、白無常一直來找她、她在等一個承諾要來的人）。出處同上。
- **題材結構**：每集一個獨立的職場梗（開會、團建、帶新人、流程），角色固定，也有主線伏筆（「黑衣人篇」「黑衣人終於露臉了」）。
  所以不看前一集也看得懂，不需要前情提要。出處同上（集名）。
- **觀看數其實不高**：伶伶AI剧场這 15 支每支 78–386 次。B 站上 盐嬅呀 發的同系列〈阴间牛马日常2.5〉有 9,793 播放、316 讚，
  標「含AI生成内容」，標籤是「AI夏日小剧场、牛马日常、自制剧情」。
  - 出處：[B 站 BV1zjHL6AEE3](https://www.bilibili.com/video/BV1zjHL6AEE3/)。
  - YouTube 上還有別的頻道「夢劇場D-Drama」發〈孟婆不想上班【合集1】〉〈【合集7】〉，見 [oEmbed 合集1](https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=mOsXLeFmZEg&format=json)、
    [oEmbed 合集7](https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=Jqt16aUfI90&format=json)。
  - 伶伶AI剧场是原作者還是轉載，**未驗證**。
  - 所以它跟 camera-feel 那份的結論一樣，是**風格參考，不是流量參考**。
- **畫面與剪接**（camera-feel 量測，第 7 集 20–44 s、90–114 s）：整段在同一個服務台，兩個人來回對話；鏡頭只在過肩、反打、嘴部特寫、
  反應特寫、單據插入鏡之間切換；一場戲講完一件事；每集 2–3.5 分鐘。
- **未驗證**：有沒有用對嘴模型、字幕字型與位置、配樂是不是固定主題曲。要確認得逐格看或下載音軌，需要站主同意。

### 1.2 其他熱門 AI 短劇（camera-feel 量過的三支）

- 好運劇場（37 萬觀看）、九公主AI劇場（108 萬）、漫劇速報（62 萬，3D 古風）：鏡長中位數 1.0–5 秒，跟我們差不多。
  差距在鏡內動量 6.4–15（我們 2.2–5.2）和靜止幀 1–27%（我們 22–59%）。
- 這三支都是長的合集：取樣點到 1,800 秒以上，代表至少 30 分鐘。YouTube 上同類頻道也常發「第一、二季合集」，
  例如 [《十二分身》合集](https://www.youtube.com/watch?v=CIS3t6Is2E0)（搜尋摘要；頻道歸屬未驗證）。

### 1.3 業界教學與報導裡的固定做法

- **前 3 秒要有衝突，不鋪世界觀**：前三秒要讓觀眾知道誰倒楣、誰不服、誰要反擊。
  - 60 秒樣片的結構：0–3 秒鉤子、3–15 秒處境、15–35 秒升級、35–50 秒反轉、50–60 秒懸念。
  - 一集 1–2 個主角色、12 鏡、每鏡 3–6 秒。
  - 出處：[匠人學院《AI 漫劇從 0 到成片實操手冊》](https://jiangren.com.au/ebooks/ai-manga-drama-production-handbook-2026/AI%20%E6%BC%AB%E5%89%A7%E4%BB%8E%200%20%E5%88%B0%E6%88%90%E7%89%87%E5%AE%9E%E6%93%8D%E6%89%8B%E5%86%8C%20-%20%E5%8C%A0%E4%BA%BA%E5%AD%A6%E9%99%A2.pdf) 第 3、6 頁。
  - 其他經驗帖也寫「單集 1 分鐘、3 秒內出現視覺奇觀或強衝突、結尾預留懸念」「每句台詞不超過 15 字、每集場景不超過 3 個」。
    出處：[gitcode 經驗帖](https://gitcode.csdn.net/6a2bd08210ee7a33f27bc2f9.html)、[B 站專欄 cv49758743](https://www.bilibili.com/read/cv49758743)（搜尋摘要，未逐字核對）。
- **別做成「會動的 PPT」**：同一本手冊把「全是中景站樁」列為十大坑之一。它的做法：
  - 遠景交代環境，中景放人物互動，近景看情緒，特寫給證據；
  - A 說完先切 B 的反應鏡；
  - 空鏡用來轉場、避免越軸；
  - 匯出前逐條打勾，檢查有沒有越軸。
  - 出處：同一本手冊第 8–9、11 頁。
- **字幕與音效的交付標準**（同一本手冊第 10 頁）：
  - 字幕要在手機上看得清、斷句自然，加分做法是「關鍵詞加粗或換色」。
  - 剪輯要「音效幫忙打節奏」。
  - 封面是「人物＋衝突一句話」，加分做法是「看得出下一秒要發生什麼」。
  - 返工信號：BGM 蓋過台詞、字幕擋臉。
- **即夢／剪映這一派的參數**：
  - 字幕放在畫面下方五分之一、避開臉；BGM 是人聲的 20–30%。
  - 音效只放在關鍵動作上（門、腳步、風、拔刀）；轉場統一用 0.2 秒疊化。
  - 對嘴用即夢或可靈的「唇形同步」，嘴型不對就改用側面或遠景。
  - 3 分鐘一集約 60–80 鏡。
  - 出處：[人人都是產品經理 6461537](https://www.woshipm.com/ai/6461537.html)。
- **首尾幀做轉場**：用前一支的最後一格和下一支的第一格，生成中間的轉場片段。
  出處：[人人都是產品經理 6305282](https://www.woshipm.com/share/6305282.html)（海螺路線的教學）。
- **平台把整條管線包起來**：即夢「短劇工作室」把劇本模型 Dream、資產（角色場景跨集重用）、分鏡、「3D 導演台」（擺角色位置與機位）、
  生成與後期串成一條，Seedance 2.5 促銷價約 0.19 元／秒。
  出處：[搜狐 2026-10-29](https://www.sohu.com/a/1094548390_122944309)。
- **規模化團隊靠人力加 AI**：頭部公司半年從幾十人擴到 1,200 人，月產從十幾集到一百多集，用 Seedance 2.0、可靈、Veo3。
  出處：[zgeo 分析](https://www.zgeo.com.cn/news/ai-comic-drama-seedance2-bytedance-geo-analysis)。
- **觀眾開始反感「模板臉」與同質化**：出處是 [36 氪](https://eu.36kr.com/en/p/3978895442033672)（搜尋摘要）。
  這跟我們審片清單上的配角撞臉是同一個問題。
- **YouTube 規則**：
  - 2024-10-15 起，3 分鐘以內、方形或直式的影片算 Shorts。出處：[Engadget](https://engadget.com/entertainment/youtube/youtube-shorts-can-now-run-up-to-three-minutes-160002081.html)。
  - 2025-07-15 起，原本的「重複內容」改名「非原創內容」（inauthentic content），量產、模板化的內容不能營利。
    出處：[TechRepublic](https://techrepublic.com/article/news-youtube-ai-video-monetization-rules)。
    一天上好幾集同模板的 AI 劇，要注意每集要有真的新內容。

### 1.4 對照：參考作品有、我們沒有的

| 項目 | 參考作品／業界 | 我們現在 | 出處 |
| --- | --- | --- | --- |
| 對嘴 | 業界用即夢／可靈的唇形同步；參考片有嘴部特寫（是否另做對嘴，未驗證） | 產線不對嘴；臉部景別又有台詞的鏡列為 B 級風險，建議台詞放到聽的人身上 | 1.3；`animation-preproduction/references/shot-risk.md` |
| 一集的結構 | 一集一個獨立梗或一場戲，前 3 秒衝突，結尾包袱或懸念 | 一集 6–10 個說話的人、好幾個場景，一句 4–5 字 | 1.1、1.3；camera-feel |
| 鏡內動作 | 動量 6–15，靜止幀 ≤27% | 動量 2–5，靜止幀 22–59% | camera-feel |
| 標題 | 「劇名_集數」加系列標語加一句梗，hashtag 固定 | 每集標題在 `episodes.csv` 的 `youtube_title` 各寫各的，沒有固定格式；合集是「種田娶妻打天下 第1–5集 \| CC字幕」（`hailuo/README.md`）。是否有固定格式，**未逐集核對** | 1.1 |
| 說明欄 | 同一段簡介，開頭一句鉤子 | 每集各寫 | 1.1 |
| 字幕 | 關鍵詞加粗或換色，放下方五分之一、避開臉 | 燒錄一般字幕；系統音只出面板、不上字幕 | 1.3；season1-review |
| 音效 | 音效幫忙打節奏，關鍵動作都有 | 有音效庫，但一集裡不多 | 1.3；camera-feel |
| 配樂 | BGM 是人聲的 20–30%，情緒高點才拉大 | 三首 cue 輪流，一集換 6 次；側鏈 ratio 8 讓音樂忽大忽小 | 1.3；camera-feel |
| 上傳形式 | 單集 2–3.5 分鐘當 Shorts 上（#aishorts）；熱門頻道另發 30 分鐘以上的合集 | 單集 16:9，整季合一支 | 1.1、1.2 |

## 二、我們缺的工具與做法

可行性的「自架」是指放在現有的 RunPod pod（ComfyUI、network volume）上跑；顯存以官方 README 為準。

| 缺什麼 | 解決什麼問題 | 可行性與成本 | 出處 |
| --- | --- | --- | --- |
| **生成後對嘴：LatentSync 1.6**（只重畫嘴部） | 說話人嘴不動、畫外台詞時畫面上的人在張嘴；做到之後，說話近景不必再避開 | 開源 Apache-2.0；推論至少要 18 GB 顯存（1.5 版 8 GB）；ComfyUI 有社群 wrapper。3D 國漫臉的效果官方沒寫，**未驗證**。可以放在 RunPod 上跑，只花 GPU 時間 | [GitHub](https://github.com/bytedance/LatentSync)、[HF 1.6](https://huggingface.co/ByteDance/LatentSync-1.6)、[ComfyUI 教學](https://zhuanlan.zhihu.com/p/16072872848) |
| **影片轉影片配音：InfiniteTalk**（嘴、頭、身體跟著音訊重做） | 除了嘴，連點頭、身體的節奏也跟台詞對上，直接解決「站著講話不動」 | 開源 Apache-2.0；Wan2.1-I2V-14B 底模，480p／720p；會模仿原片運鏡，但不完全一樣；超過 1 分鐘會偏色。比 LatentSync 重很多，出來的 720p 要再接 SeedVR2 | [GitHub](https://github.com/MeiGen-AI/InfiniteTalk)、[ComfyUI 文件](https://docs.comfy.org/tutorials/video/wan/wan-infinitetalk.md) |
| **說話鏡直接用音訊生成：Wan2.2-S2V** | 從一張首格加一段台詞，生成會說話、有手勢的鏡頭（肖像、半身、全身） | 開源，第三方列 Apache-2.0；480p／720p；要換一條 Wan 路線，跟 H3 的畫風一不一致**未驗證** | [betanews](https://betanews.com/2025/08/28/alibaba-launches-new-open-source-tool-that-turns-photos-into-video/)、[vast.ai](https://vast.ai/model/wan-2.2-s2v-14b) |
| 付費對嘴 API：sync.so lipsync-2-pro、可靈對口型 | 同 LatentSync，不用自己架 | sync 約 US$0.067–0.083／秒（約 US$4–5／分鐘），臉以 512×512 生成；卡通臉**未驗證**。可靈在網頁上操作 | [sync 文件](https://sync.so/docs/models/lipsync)、[fal](https://fal.ai/models/fal-ai/sync-lipsync/v2)、[可靈教學（摘要）](https://www.waytoagi.com/zh/question/87749) |
| **看畫面自動配音效：HunyuanVideo-Foley／MMAudio** | 腳步、放東西、衣料、環境聲每鏡都有，不用一個一個從音效庫挑 | Foley：XXL 版要 20 GB（offload 12 GB），授權**未核對**。MMAudio：程式 MIT，但權重是 **CC-BY-NC 4.0**，營利頻道不宜用；約 6 GB，預設 8 秒 | [Foley GitHub](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley)、[論文](https://arxiv.org/abs/2508.16930)、[MMAudio](https://github.com/hkchengrex/MMAudio) |
| 付費文字生音效：ElevenLabs SFX v2 | 補音效庫沒有的聲音（法術、系統提示音、古代器物） | 0.5–30 秒；第三方報價約 US$0.12／分鐘，彼此對不上，**未驗證** | [ElevenLabs 說明](https://elevenlabs.io/docs/help-center/product/core-capabilities/sound-effects/how-much-does-it-cost-to-generate-sound-effects/llms.txt)、[ModelsLab](https://modelslab.com/sound-effects-api-pricing.md) |
| **季主題曲、角色主題、一場一首：ACE-Step 1.5** | 取代三首 cue 輪流；有分軌，可以只留鼓或弦來壓在對白底下 | 開源 MIT，有分軌功能；訓練資料是否合法授權，**未驗證**。可以在 RunPod 上一次做好一季的曲庫 | [HF](https://huggingface.co/spaces/MBLF/ACE-Step-1.5/blob/main/README.md) |
| **補幀：RIFE 4.9／GIMM-VFI**（取代 ffmpeg `minterpolate`） | 慢放時邊緣糊、動作黏（camera-feel 原因 4）；也可以把 24 fps 補成 48 fps 讓動作更順 | 開源，ComfyUI 有節點；rife426 載入有問題，用 rife49。慢放的上限還是照 1.1 倍 | [ComfyUI-VFI](https://www.runcomfy.com/comfyui-nodes/ComfyUI-VFI/rife-interpolation)、[vast.ai RIFE](https://vast.ai/model/rife)、[GIMM 工作流](https://comfy.org/zh-CN/hub/workflows/gimm-frame-interpolation-268307c5793e/) |
| **鏡頭 QA 自動關卡：Gemini 影片理解** | 送剪前自動抓服裝錯、說話人錯位、分身、假字、表情不符，這些原本要七個子代理逐鏡看 | 已經有 Gemini 金鑰；預設每秒取 1 格，可以設 fps，用 MM:SS 回報時間點，也聽得到音訊。快動作可能漏，所以搭配我們自己的 freezedetect 與動量指標（動量 ≥7、靜止幀 ≤15% 才放行） | [Gemini 影片理解文件](https://aistudio.google.com/docs/video-understanding) |
| **字幕動畫與強調：ASS `\kf` 逐字上色** | 關鍵詞換色、重點台詞跳出來；系統音也能做成另一種字幕樣式 | 免費；ffmpeg 要有 libass；時間點用 whisper 或強制對齊抓，不要用估的 | [逐字字幕寫法](https://dev.to/danielrusnok/captions-that-read-along-one-word-at-a-time-3alg)、[n8n 範例](https://n8n.io/workflows/18486-burn-word-highlighted-karaoke-captions-onto-videos-with-ffmpeg-and-ffprobe/) |
| 首尾幀生成：Wan2.1 FLF2V-14B-720P | 鏡與鏡用動作接起來、在動作中間切；轉場片段 | 開源，ComfyUI 可用；H3 能不能指定尾格，**未驗證**，要換路線 | [LocalAI PR](https://github.com/mudler/LocalAI/pull/9440)、[ComfyUI wiki](https://comfyui-wiki.com/en/models/wan/flf2v) |
| 運鏡控制：Uni3C、ReCamMaster | 照指定軌跡跟拍、環繞、升降；ReCamMaster 可以把已經生成的固定鏡重新渲染成移動鏡 | 程式公開，都是 Wan2.1 底模，跟 H3 是不同路線；授權與顯存**未核對**，屬於研究等級 | [Uni3C](https://ewrfcas.github.io/Uni3C)、[ReCamMaster](https://github.com/KlingAIResearch/ReCamMaster) |
| 角色 LoRA（給首格產圖用） | 配角撞臉、服裝跳版；業界做法是 SDXL＋LoRA 加 ControlNet 姿勢 | 我們的首格是 Qwen，能不能訓角色 LoRA、H3 參考圖要配多高的權重，都**未驗證**；可以先用重畫定妝（瘦長臉、白鬍）解決 | [騰訊雲文章](https://developer.cloud.tencent.com/article/2733949)、[woshipm 參考權重 0.7–0.8](https://www.woshipm.com/ai/6461537.html) |
| 3D 走位與機位台（即夢 3D 導演台） | 先擺好人物左右與鏡位再生成，解決越軸、人物左右對調 | 即夢付費平台，國內帳號；我們只能學它的做法：場頭先畫一張俯視站位圖 | [搜狐](https://www.sohu.com/a/1094548390_122944309) |

## 三、建議的優先順序（前五項）

1. **加一道生成後對嘴**（LatentSync 1.6，不夠再用 InfiniteTalk）。
   - 先在 r2 第 1 集挑三個嘴看得見的說話鏡，在 RunPod 上試。
   - 站主開聲音看並排，嘴型對得上、臉沒有糊，才把 `speech.visible-mouth` 從 B 級風險降下來。
   - 這是參考作品「兩人互看、嘴在動、一看就知道誰在說話」的前提，也是說話人錯位最根本的修法。
   - 成本只有 GPU 時間。
2. **每集照「一場戲、一個梗、前 3 秒衝突」重寫，包裝也照抄格式**。
   - 第 49 集以後每集一兩個場景，第一句就是衝突，結尾是包袱或懸念；做到不看前一集也懂。
   - 標題改成「【種田娶妻打天下_NN】系列標語｜一句梗」，說明欄放固定的鉤子簡介；封面是「人物＋衝突一句話」。
   - 3 分鐘以內的集數另出直式版本，當 Shorts 上；整季另發合集長片。
   - 不花點數，改企劃與 `youtube-locales` 就好。
3. **聲音整套換**。
   - 用 ACE-Step 1.5 做季主題曲、三位女主各一段角色主題，一場一首。
   - 側鏈改成 ratio 3–4、release ≥800 ms；BGM 約人聲的 20–30%。
   - 用 HunyuanVideo-Foley（先核對授權）幫每鏡自動配 Foley，再跟 `_series/sfx` 混；MMAudio 的權重不能營利，不用。
   - 參考片的配樂還沒量，如果站主同意下載它的音軌，順便量。
4. **送剪前加自動 QA 關卡**。
   - 每支片段送 Gemini 影片理解，問固定幾題：服裝跟參考圖一不一致、畫面裡幾個人、誰的嘴在動、有沒有文字、表情是不是笑。
   - 同時算動量與靜止幀，不合格的自動退回重抽。
   - 把這季審片的必修項目（衣服、分身、說話人、假字）從人工逐鏡看，變成程式擋。
5. **剪接與字幕的小改，可以馬上做**。
   - 慢放改用 RIFE（上限 1.1 倍），拿掉 `PUNCH` 裁切放大，在動作中間切（camera-feel 改法前三項）。
   - 字幕改成 ASS：關鍵詞換色，系統音用另一種樣式上字幕（現在只出面板），位置在下方五分之一、避開臉。
   - 不用重拍，重跑剪接就能拿一集給站主看。

運鏡控制（Uni3C、ReCamMaster）和首尾幀（FLF2V）都要離開 H3 換成 Wan 路線，暫時不排；
先用 storyboard-shot-spec 的「每鏡一個動作、過肩反打、加前景」把鏡內動量拉起來，量過還不夠，再評估這兩項。
