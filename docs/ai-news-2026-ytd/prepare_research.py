"""Editorially verified source facts and distinct article briefs for this fixed batch."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKED = "2026-09-14"
items = []

def add(key, date, title, sources, facts, brief, label, nodes):
    items.append(dict(slug=f"ai-news-{key}-{date.replace('-', '')}", event_date=date,
        title=title, sources=[dict(title=t, url=u, checked_on=CHECKED) for t,u in sources],
        checked_on=CHECKED, verified_facts=facts, editorial_brief=brief,
        hero_label=label, diagram_nodes=nodes))

add("nvidia-rubin", "2026-01-05", "NVIDIA Rubin 在 CES 亮相：AI 算力升級會如何影響日常服務？",
    [("NVIDIA：Rubin 平台發布", "https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer"),
     ("NVIDIA：CES 2026 發表內容", "https://blogs.nvidia.com/blog/2026-ces-special-presentation/")],
    ["NVIDIA 於 1 月 5 日宣布 Rubin 六晶片平台，涵蓋 Vera CPU、Rubin GPU、互連、網路與資料處理。",
     "官方宣稱相對 Blackwell 可降低特定工作負載的推論成本；這是廠商條件下的比較，不是訂閱售價承諾。",
     "公告稱平台已進入全面生產，合作夥伴產品預計 2026 下半年提供；生產、交貨、雲端上架是不同階段。"],
    "以一般使用者看待雲端排隊、長任務、服務費為主。原創例子：小公司用 AI 整理商品資料，計算重試與人工核對後的每筆合格成本。解釋資料中心硬體不是家用顯卡新品，也不推論任何台灣上市價或投資報酬。表格比較訓練成本、推論成本、服務定價與使用者帳單。", "算力到服務的距離",
    [["運算平台", "處理模型工作"], ["雲端部署", "容量與維運"], ["應用服務", "方案與限額"], ["實際帳單", "核對完整成本"]])

add("chatgpt-health", "2026-01-07", "ChatGPT Health 年初登場：整理健康資料之前先看懂用途與界線",
    [("OpenAI：Introducing ChatGPT Health", "https://openai.com/index/introducing-chatgpt-health/"),
     ("OpenAI：OpenAI for Healthcare", "https://openai.com/index/openai-for-healthcare/")],
    ["1 月 7 日發布個人健康體驗 Health，可連結支援的健康資料與應用；它是獨立空間。",
     "官方明確說明 Health 不用於診斷或治療，不取代臨床照護；Health 對話不用於訓練基礎模型。",
     "年初採小規模先行使用及候補；原文 7 月 23 日更新為美國 18 歲以上使用者在 web 與 iOS 推出。",
     "病歷串接及部分應用有美國限制，Apple Health 連結需 iOS。不能據此推定台灣帳號可用；1 月 8 日醫療機構產品是另一項公告。"],
    "寫產品新聞而非醫療建議。原創情境：就診前把既有報告按日期和檢驗單位整理，列出想問醫師的問題；辨識過期報告與缺值，不自行判讀病情或調藥。討論家人同意、最少必要資料、刪除與連結設定。表格比較資料整理、術語解釋、就診問題和診療決策。", "資料帶進診間",
    [["整理來源", "日期與檢驗單位"], ["檢查缺漏", "保持原始記錄"], ["列出問題", "供就診討論"], ["專業判斷", "由醫療人員評估"]])

add("gemini-personal-intelligence", "2026-01-14", "Gemini Personal Intelligence：AI 連結郵件與相簿後，便利從哪裡來？",
    [("Google：Gemini Personal Intelligence", "https://blog.google/innovation-and-ai/products/gemini-app/personal-intelligence/"),
     ("Google：Personal Intelligence in Search", "https://blog.google/products-and-platforms/products/search/personal-intelligence-ai-mode-search/")],
    ["1 月 14 日 Gemini Personal Intelligence 在美國推出 beta，首批為符合資格的個人 Google AI Pro／Ultra 帳號。",
     "使用者選擇連結 Gmail、Photos、YouTube、Search；增強個人化預設關閉，可選擇來源及關閉。",
     "Google 說不直接用 Gmail 收件匣或 Photos 圖庫訓練，但有限的提示與回答可能用於改善功能；不能改寫成所有資料皆不用於訓練。",
     "官方承認可能錯誤串聯不相關資料或過度個人化。1 月 22 日另一公告把 Personal Intelligence 擴至 Search 的 AI Mode。"],
    "原創情境：從航班郵件與相簿整理家庭旅行偏好，但先確認目前同伴、日期、預算，不把舊旅行當新承諾。把個人帳號、工作帳號、搜尋入口分清楚，僅說首發地區；目前資格請讀者查自己的介面。表格比較資料來源、用途、可能誤解與核對點（三欄整合）。", "連結之前先選擇",
    [["選擇來源", "只連需要的應用"], ["提出問題", "說明此次情境"], ["核對引用", "辨識新舊資訊"], ["調整連結", "保留控制權"]])

add("gpt-53-codex", "2026-02-05", "GPT-5.3-Codex 推出：AI 寫程式如何走向可交付的工作？",
    [("OpenAI：GPT-5.3-Codex 發布", "https://openai.com/index/introducing-gpt-5-3-codex/")],
    ["2 月 5 日發布 GPT-5.3-Codex，整合程式與專業知識工作能力，支援長任務中的研究和工具使用。",
     "官方當時宣稱較前代快 25%；不能當成所有專案工時都少 25%。",
     "首發公告列付費 ChatGPT 方案的 Codex app、CLI、IDE extension 與 web，API 當時仍是後續計畫。",
     "公告展示可在執行中提問和調整方向，評測成績與自我開發案例均為 OpenAI 報告。"],
    "面向不熟程式的一般讀者和小團隊。原創例子：製作活動報名頁，先列欄位、錯誤提示、成功畫面與資料處理要求，分草稿、測試、審查、上線。不要將可寫程式宣傳成可保證安全上線。給可用的需求表達方式但不寫特定介面步驟。", "需求到可用成果",
    [["說明需求", "列出驗收條件"], ["小步實作", "保留修改紀錄"], ["測試流程", "檢查成功與失敗"], ["確認交付", "部署另行確認"]])

add("claude-opus-46", "2026-02-05", "Claude Opus 4.6 與長上下文：大量資料讀得進去，也要找得回來",
    [("Anthropic：Claude Opus 4.6", "https://www.anthropic.com/news/claude-opus-4-6"),
     ("Anthropic：模型狀態與淘汰時程", "https://docs.anthropic.com/en/docs/about-claude/model-deprecations")],
    ["2 月 5 日 Opus 4.6 發布，強調程式、研究與文件工作；Opus 首次提供 1M token 上下文 beta。",
     "公告同時介紹 adaptive thinking、effort 與 API context compaction。",
     "首發列 Claude、API 與主要雲端平台；1M beta 並非所有聊天帳號共同上限。",
     "基準成績是 Anthropic 評測，長上下文容量不能等同沒有遺漏或理解錯誤。"],
    "原創場景：社區管委會比較歷年維修報價，先製作文件清單、頁碼、日期，再抽查模型說法。解釋 token 不是固定中文字數，摘要壓縮可能失去細节。用長文件流程、資料分組及抽樣回原文的具體做法支撐文章，不做無來源數字比較。", "讀得進也找得回",
    [["列出文件", "日期與版本"], ["分組閱讀", "標示問題範圍"], ["附上出處", "回到段落頁碼"], ["抽查結論", "核對遺漏與矛盾"]])

add("qwen-35", "2026-02-16", "Qwen3.5 開放權重：可下載模型，與能在自己電腦運作差在哪？",
    [("Qwen：官方儲存庫發布紀錄", "https://github.com/QwenLM/Qwen3.8"),
     ("Qwen：Qwen3.5-397B-A17B 官方模型卡", "https://huggingface.co/Qwen/Qwen3.5-397B-A17B")],
    ["官方儲存庫 News 記載 2026 年 2 月 16 日發布首個 Qwen3.5 開放權重模型 Qwen3.5-397B-A17B。雲端 Plus 的版本日期 2 月 15 日不能當成這個開放模型的發布日。",
     "官方模型卡列總參數 397B、啟用 17B，為含視覺編碼器的混合架構，授權標示 Apache-2.0。",
     "官方同時區別自行部署權重與 Alibaba Cloud 的託管 Qwen3.5-Plus；後者有不同服務功能與上下文設定。",
     "啟用參數不等於整個模型檔案或記憶體需求，自行部署仍需硬體、軟體、維運及授權條件核對。"],
    "不給未驗證硬體最低需求，不引導一般讀者下載數百GB權重。原創例子：小店想用內部產品圖和規格問答，比較託管試用與找技術夥伴做離線小樣本。解釋開放權重不是完整訓練資料公開，也不保證所有衍生用途無條件自由。表格比較可下載、可啟動、可用與可維運。", "開放權重的四道門",
    [["確認授權", "查看官方版本"], ["估算資源", "完整模型需求"], ["測試任務", "用自己的樣本"], ["維護服務", "成本與資料治理"]])

add("gemini-31-pro", "2026-02-19", "Gemini 3.1 Pro 發布：複雜問題如何轉成可驗證的答案？",
    [("Google：Gemini 3.1 Pro", "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/"),
     ("Google：2026 年 2 月 Gemini 更新", "https://blog.google/innovation-and-ai/products/gemini-app/gemini-drop-february-2026/")],
    ["2 月 19 日 Google 發布 Gemini 3.1 Pro，強調複雜推理、資料整合和程式產生視覺。",
     "當時開發者在 Gemini API 等入口取得 preview；消費者入口包含 Gemini app 與 NotebookLM。",
     "原文說 Gemini app 的 Pro／Ultra 有較高上限，NotebookLM 的 3.1 Pro 當時限 Pro／Ultra；不同入口條件不能混寫。",
     "ARC-AGI-2 等評測屬 Google 發表的結果，不代表日常答案的正確率。"],
    "原創情境：家長比較三個課程，把費用、時段、距離、資料缺口轉成比較表，再要求逐條解釋推薦的權重。簡介推理模型用途和資料不足時該保留未知。對互動視覺先查公式和單位，別讓漂亮動畫代替證據。", "把推理變成檢查點",
    [["列出條件", "保留未知資訊"], ["比較選項", "說明取捨理由"], ["回查來源", "日期與單位"], ["自己決定", "核對關鍵假設"]])

add("gpt-54", "2026-03-05", "GPT-5.4 把推理與電腦操作放在一起：一般工作者該怎麼看？",
    [("OpenAI：GPT-5.4 發布", "https://openai.com/index/introducing-gpt-5-4/")],
    ["3 月 5 日 GPT-5.4 在 ChatGPT、API 與 Codex 發布；ChatGPT 名稱為 GPT-5.4 Thinking，另有 Pro。",
     "官方強調試算表、簡報、文件、程式與工具使用；API/Codex 引入原生電腦操作能力。",
     "API 與 Codex 的長上下文能力不能推定是 ChatGPT 的同等上限。",
     "API 當時可用，ChatGPT 與 Codex 分批推出；首發列出的方案是歷史資格，並非 9 月的現行價目表。"],
    "原創情境：把社團活動問卷做成摘要簡報。先定義欄位、分母、匿名化、缺值和輸出範本；開啟檔案核對公式而不是只看文字結案。清楚區分模型判斷、工具權限、登入狀態與實際提交。", "回答之外的操作",
    [["準備材料", "範本與資料"], ["列出步驟", "定義可做範圍"], ["產生成果", "保存原始檔案"], ["驗證內容", "確認再提交"]])

add("claude-interactive-visuals", "2026-03-12", "Claude 對話開始畫互動圖：看懂概念之前，先看懂圖的假設",
    [("Claude：互動視覺發布", "https://claude.com/blog/claude-builds-visuals"),
     ("Claude Help：Can Claude produce images?", "https://support.claude.com/en/articles/9002504-can-claude-produce-images")],
    ["3 月 12 日宣布 beta，Claude 可在對話中產生可調整的圖表、圖解與互動視覺，當時適用所有方案。",
     "官方區分對話內暫時性的互動圖與可分享下載的持久 artifacts；兩者用途不同。",
     "支援文件說這些視覺由 HTML／SVG 產生，不等同相片或繪畫型圖片生成。",
     "原文 4 月 22 日更新說 Cowork 所有付費方案亦可用；首發與後續擴展應分開。"],
    "原創情境：讓學生調整水箱進出水量或比較兩種通勤時間，先給數值、單位和邊界，逐一試滑桿。不要使用官方複利和週期表例子。具體教怎麼核對座標、比例、截斷軸、互動邊界與無障礙文字說明。", "讓假設看得見",
    [["設定數值", "單位與範圍"], ["畫出關係", "圖形對應公式"], ["調整變數", "測試邊界情況"], ["回到文字", "說明適用限制"]])

add("lyria-3-pro", "2026-03-25", "Lyria 3 Pro 延長 AI 音樂創作：從短片段到有段落的作品",
    [("Google：Lyria 3 Pro", "https://blog.google/innovation-and-ai/technology/ai/lyria-3-pro/")],
    ["3 月 25 日 Google 發表 Lyria 3 Pro，公告可產生最長 3 分鐘的音樂，並用提示安排前奏、主歌、副歌與橋段。",
     "同次公告擴展至 Google 的創作與開發入口，Vertex AI 當時為 public preview；各產品資格需分開看。",
     "Google 表示輸出嵌入 SynthID，並採避免模仿既有歌手的措施；標記不是商用授權或版權保證。"],
    "原創情境：製作社區影展入場配樂，寫出前段安靜、中段提升、最後留口播空間，逐段試聽。保留歌詞與自有素材來源，音量、咬字、段落接續是驗收點。只做創作工作流程，不給未經查證的特定平台商用條款。", "把音樂寫成段落",
    [["定義用途", "時長與播放場合"], ["規畫段落", "情緒與轉場"], ["逐段試聽", "口白與聲音平衡"], ["確認來源", "授權與標示"]])

add("project-glasswing", "2026-04-07", "Project Glasswing 與 Mythos Preview：AI 找到漏洞後，真正的工作才開始",
    [("Anthropic：Project Glasswing", "https://www.anthropic.com/glasswing"),
     ("Anthropic：Glasswing 初期進展", "https://www.anthropic.com/research/glasswing-initial-update")],
    ["4 月 7 日 Anthropic 發表 Project Glasswing，讓維護重要軟體的合作夥伴以 Claude Mythos Preview 做防禦性安全工作。",
     "Mythos Preview 是受限研究預覽，沒有對一般使用者全面開放。",
     "官方將漏洞發現能力歸因於更強的程式理解；漏洞數與能力描述是廠商報告。",
     "5 月 22 日後續公告強調發現後仍須驗證、揭露與修補；不要把候選漏洞直接當成已修復的事件。"],
    "面向一般讀者和網站管理者，使用不含攻擊細節的維護流程：資產盤點、確認受影響版本、廠商更新、備份、安裝後檢查。區分掃描提示、已確認漏洞、修補發布和使用者完成更新。不要生成漏洞利用方式或把未公開弱點猜成特定服務已被入侵。", "發現到修補的流程",
    [["發現線索", "尚待人工確認"], ["驗證影響", "版本與範圍"], ["協調修補", "維護者處理"], ["完成更新", "再檢查服務"]])

add("meta-muse-spark", "2026-04-08", "Meta Muse Spark 登場：社群裡的 AI 助手如何改變搜尋與提問？",
    [("Meta：Muse Spark 官方公告", "https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/"),
     ("Meta AI：Muse Spark 技術介紹", "https://ai.meta.com/blog/introducing-muse-spark-msl/")],
    ["4 月 8 日 Meta Superintelligence Labs 發表 Muse Spark，為支援工具使用的原生多模態推理模型。",
     "首發在 Meta AI app 與網站提供，API 為選定使用者的 private preview；不是公開權重下載發布。",
     "5 月 12 日更新說逐步擴展至 Meta 社群產品和眼鏡，眼鏡首波有美國及加拿大限制。",
     "官方演示視覺理解和個人化協助；功能、國家與產品入口仍可能不同。"],
    "原創情境：看到戶外活動貼文想整理裝備清單，分辨作者建議、AI補充和付費推廣。社群照片中的物品辨識只是線索，要核對規格；不推論Facebook每個台灣帳號已可用，不把模型當成讀私訊的普遍權限。比較公開內容、你主動提供材料與平台可用入口。", "社群資訊再核對",
    [["看見內容", "辨識原始作者"], ["提出問題", "界定資料範圍"], ["核對建議", "規格與時效"], ["選擇行動", "確認來源再用"]])

add("chatgpt-images-20", "2026-04-21", "ChatGPT Images 2.0：圖像開始加入思考，設計需求也要更清楚",
    [("OpenAI：ChatGPT Images 2.0", "https://openai.com/index/introducing-chatgpt-images-2-0/"),
     ("OpenAI：Images 2.0 System Card", "https://deploymentsafety.openai.com/chatgpt-images-2-0")],
    ["4 月 21 日 ChatGPT Images 2.0 發布，官方強調文字細節、世界知識與指令遵循。",
     "新增 images with thinking，可在產生前規畫並使用工具，系統卡描述網路資料和一個提示產生多張圖等能力。",
     "首發 Images 2.0 為所有 ChatGPT 方案；thinking 功能有付費方案及 Thinking／Pro 入口條件。",
     "9 月已另有 Images 2.5 公告；本篇是 4 月事件解析，不把 2.0 當作目前最新版本。"],
    "原創情境：台灣書店做讀書會海報，先提供真正日期、地址和精確書名，用於構圖的資料和上圖必須逐字正確的內容分開。比對字形、標點、日期、店名、尺寸留白和改版一致性。生成畫面仍須核對，不挪用真實活動身分或虛構宣傳背書。", "先規畫再成圖",
    [["交代用途", "版型與讀者"], ["鎖定資訊", "文字逐字核對"], ["生成版本", "比較構圖細節"], ["排版驗收", "尺寸與留白"]])

add("gpt-55", "2026-04-23", "GPT-5.5 走向多步驟工作：把模糊需求變成能驗收的交付",
    [("OpenAI：GPT-5.5 發布", "https://openai.com/index/introducing-gpt-5-5/")],
    ["4 月 23 日 GPT-5.5 發布，強調程式、線上研究、資料分析、文件、試算表及軟體操作的長任務。",
     "公告聲稱能力提升且每 token 延遲與 GPT-5.4 相當，Codex 任務用較少 token；這不保證每位使用者耗時或費用相同。",
     "首發 ChatGPT／Codex 逐步推出，4 月 24 日更新確認 GPT-5.5 與 Pro 的 API 可用。",
     "頁面已連到後續 GPT-6；本篇以 4 月公告的轉變為主，現有方案不能由舊文推定。"],
    "原創情境：協會整理贊助資料包，包括簡介、表格和信件草稿。把接受模糊需求與允許任意決定區分，為預算、對外承諾和寄送设停點。衡量合格交付的總成本、回頭改幾次、缺漏多少；不用泛泛提高效率反覆灌水。", "任務可以拆也要驗",
    [["說明成果", "對象與使用場合"], ["標記假設", "缺口先詢問"], ["逐段交付", "可檢查的版本"], ["確認行動", "外部承諾需核對"]])

add("gemini-omni", "2026-05-19", "Gemini Omni 在 I/O 亮相：用對話改影片，素材與連續性仍要自己把關",
    [("Google：Gemini Omni", "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/"),
     ("Google：Flow 與 Flow Music 更新", "https://blog.google/innovation-and-ai/models-and-research/google-labs/flow-updates/")],
    ["5 月 19 日 Google I/O 發布 Gemini Omni，初期以影片生成與對話式編輯為重點。",
     "官方示範用文字、圖片、影片作參考，多輪修改場景和角度；音訊參考初期只支援聲音參考，其他音訊是後續計畫。",
     "同日 Gemini app 公告列 Plus／Pro／Ultra 分批取得；Flow 等入口有各自供應條件。",
     "官方稱物理與場景連貫有所進步，不能當作所有生成影片都符合真實世界或已取得素材權利。"],
    "原創情境：以自攝陶藝製作過程做短片，先建立鏡頭清單和主體不可改項，逐鏡核對手部、工具、光影和人物同意。說明角色連續性、多輪改圖造成漂移與保留原始素材的重要。不要把示範短片當真實現場紀錄。", "一鏡一鏡看清楚",
    [["準備素材", "確認使用權利"], ["定義鏡頭", "主體與動作"], ["逐輪修改", "保留原始版本"], ["檢查連續", "時間與光影"]])

add("gemini-spark", "2026-05-19", "Gemini Spark 與 Daily Brief：AI 從晨間摘要走向背景辦事",
    [("Google：Gemini app 的下一步", "https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/"),
     ("Google：I/O 2026 一百項公告", "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/"),
     ("Google：2026 年 7 月 Gemini Drop", "https://blog.google/products-and-platforms/products/gemini/gemini-drop-july-2026/")],
    ["5 月 19 日介紹 Gemini Spark 雲端代理與 Daily Brief 個人晨報，可運用使用者選擇連結的應用。",
     "Spark 首發先給 trusted testers，美國 Ultra beta 是當時接下來一週的計畫；Daily Brief 首波美國 Plus／Pro／Ultra。",
     "官方說 Spark 可在裝置關閉時於雲端工作，並設計為花錢、寄信等重要操作前確認。",
     "7 月官方月報後續描述 Spark 擴展全球，但排除 EEA、英國、瑞士與奈及利亞；不可把五月預告當作台灣首發即全面開放。"],
    "原創情境：整理每週志工班表變更，先只做草稿和缺漏清單，再由負責人通知成員。區分摘要、提醒、排程、對外動作四級，說明錯誤來源會重複被排程放大；如何定期檢查規則、停用過期任務。不要把這篇新聞變成替讀者真的排程服務。", "背景工作也有邊界",
    [["選擇連結", "最少必要來源"], ["設定任務", "頻率與範圍"], ["審查草稿", "辨識重要變更"], ["確認動作", "通知與費用"]])

add("claude-fable-5-access", "2026-06-09", "Claude Fable 5 的發布、暫停與恢復：AI 服務可用性也是選擇條件",
    [("Anthropic：Claude Fable 5 與 Mythos 5", "https://www.anthropic.com/news/claude-fable-5-mythos-5"),
     ("Anthropic：Redeploying Fable 5", "https://www.anthropic.com/news/redeploying-fable-5")],
    ["6 月 9 日推出 Fable 5，官方稱為加上一般用途防護的 Mythos 級模型；Mythos 5 仍限特定對象。",
     "Anthropic 表示 6 月 12 日因美國出口管制暫停兩者存取；本文把原因歸因於官方說明，不獨立解釋法律。",
     "6 月 30 日公告限制解除，7 月 1 日恢復；Fable 與 Mythos 的對象仍不同。",
     "原有試用包含量有期限，恢復時 Fable 的部分方案優惠到 7 月 7 日，之後使用 credits；不能當作九月持續免費。"],
    "原創情境：小型研究團隊把重要結論存成通用文件，保留資料來源與可替代工具，不讓工作綁死單一模型。清楚列四個日期的時間表。分析服務中斷、原始檔持有、匯出、切換模型時重驗的具體成本，不猜政策未來。", "可用性也要留備案",
    [["確認入口", "資格與期限"], ["保留原稿", "資料可匯出"], ["準備替代", "重新驗證結果"], ["追蹤變更", "看官方時間線"]])

add("gpt-56-sol-preview", "2026-06-26", "GPT-5.6 Sol 從有限預覽開始：模型發表與人人可用為何不同？",
    [("OpenAI：GPT-5.6 Sol 預覽", "https://openai.com/index/previewing-gpt-5-6-sol/"),
     ("OpenAI：GPT-5.6 正式發布", "https://openai.com/index/gpt-5-6/")],
    ["6 月 26 日預覽 GPT-5.6 系列：Sol 為旗艦、Terra 偏平衡工作、Luna 偏快速低成本。",
     "OpenAI 表示經與美國政府溝通，初期只向小群 trusted partners 預覽；當時較廣開放是後續計畫。",
     "官方強調高風險能力防護、測試與反覆紅隊檢驗；這些不構成零風險保證。",
     "7 月另有 GPT-5.6 發布公告，後續現況必須看後續公告，不能把六月的限制描述成永久封閉。"],
    "原創例子：公司在看模型發表時，將展示、預覽資格、產品入口、商務合約與實際試用分成不同證據。對未開放功能建立觀察表而不是先承諾客戶交期。不要重複已有七月降價文；重點是發布階段判讀及選型驗收。", "發表到可用有階段",
    [["公開消息", "先看事件日期"], ["有限預覽", "辨識參與資格"], ["分批上線", "確認產品入口"], ["實際試用", "用任務驗收"]])

add("claude-sonnet-5", "2026-06-30", "Claude Sonnet 5：能力與成本之間，怎麼找日常工作的平衡？",
    [("Anthropic：Claude Sonnet 5", "https://www.anthropic.com/news/claude-sonnet-5"),
     ("Anthropic：模型狀態與淘汰時程", "https://docs.anthropic.com/en/docs/about-claude/model-deprecations")],
    ["6 月 30 日 Sonnet 5 發布，強調規畫、工具使用、程式與知識工作，首發列所有方案並為 Free／Pro 預設。",
     "官方稱接近 Opus 4.8 的部分表現但成本較低，屬廠商評測說法。",
     "公告 8 月 10 日更新：每百萬輸入 token 2 美元、輸出 10 美元的介紹價改為永久；原訂 9 月 1 日 3／15 美元不再適用。",
     "API 單價與聊天訂閱費不同，effort、任務長度及重試也影響實際使用量。"],
    "原創情境：每週整理客服常見問題，不含客戶個資。用簡單分類、矛盾比對、難題草稿三種任務看哪種需要較多思考，再比較合格結果率。表格清楚列輸入、輸出、訂閱與人工核對費用，只有公告美元數字可寫。", "按工作選擇力道",
    [["分類任務", "先辨識難度"], ["設定思考", "時間與品質"], ["記錄結果", "重試與漏答"], ["比較成本", "以合格交付計算"]])

add("chatgpt-work", "2026-07-09", "ChatGPT Work 正式亮相：如何把跨檔案工作交代清楚？",
    [("OpenAI：ChatGPT Work 發布", "https://openai.com/index/chatgpt-for-your-most-ambitious-work/"),
     ("OpenAI Academy：Get started with ChatGPT Work", "https://academy.openai.com/public/clubs/work-users-ynjqu/events/get-started-with-chatgpt-work-00rtqho2qa")],
    ["7 月 9 日 ChatGPT Work 發布，可跨連結應用與檔案處理長任務，製作文件、試算表、簡報等成果；官方以 GPT-5.6 提供能力。",
     "首發 web／mobile 先 Pro、Enterprise、Edu，接著 Plus／Business；桌面 Mac／Windows 當時列所有方案包括 Free。",
     "官方說工作耗用量隨任務規模而異，沿用 Codex 使用結構；不是一次聊天固定成本。",
     "可在工作中追蹤進度、回答問題、改方向及確認重要動作，模型能力不等於所有應用權限自動具備。"],
    "原創情境：替讀書社群整理年度活動資料，輸入範本、過去場次與預算，要求工作簿和簡報一致。列明結果存放位置、來源、未決問題、對外寄送停點。專講多檔案交接與跨工具一致性，不重寫GPT6模型介紹。", "把交付說到具體",
    [["提供背景", "範本與材料"], ["指定成果", "格式與用途"], ["跟進進度", "調整未決問題"], ["開檔驗收", "內容與來源一致"]])

add("gemini-36-flash", "2026-07-21", "Gemini 3.6 Flash 與 Flash-Lite：快速模型該如何分工？",
    [("Google：3.6 Flash、3.5 Flash-Lite 與 Cyber", "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/"),
     ("Google：2026 年 7 月 Gemini Drop", "https://blog.google/products-and-platforms/products/gemini/gemini-drop-july-2026/")],
    ["7 月 21 日 Google 發布 Gemini 3.6 Flash、3.5 Flash-Lite、3.5 Flash Cyber，分別強調綜合效率、大量低延遲工作及防禦資安用途。",
     "公告列 3.6 Flash API 每百萬輸入／輸出 1.50／7.50 美元，Flash-Lite 0.30／2.50 美元；屬當日美元 API 報價，不是訂閱月費。",
     "Cyber 的防禦用途與存取資格不能推定一般帳號可隨意切換；效能比較為 Google 發表結果。",
     "7 月 Gemini Drop 確認新 Flash 模型進入 Gemini app；9 月另有 3.8 Flash，本文是七月分工策略的歷史解析。"],
    "原創情境：公益市集大量整理攤位資料，先用快模型提取欄位，把衝突與模糊規格交給較強模型或人工。每筆保留原始來源，抽樣看漏字、數字、地址，不只比較每秒輸出。表格比較簡單分類、跨表比對、專業資安和最終發布核對。", "快慢工作分開做",
    [["簡單整理", "固定欄位輸出"], ["辨識例外", "缺值與矛盾"], ["深入核對", "難題另行處理"], ["抽查交付", "品質與總成本"]])

assert len(items) == 21
for item in items:
    item["source_policy"] = "Facts only from listed official sources checked on 2026-09-14. Benchmarks belong to vendors. Editorial examples are hypothetical, not hands-on product tests. Announcement access and future promises must be dated."
    item["status"] = "researched-not-written"
(HERE / "research").mkdir(exist_ok=True)
for item in items:
    (HERE / "research" / f'{item["slug"]}.json').write_text(json.dumps(item,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(HERE / "manifest.json").write_text(json.dumps(items,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(f"Prepared {len(items)} verified news briefs")
