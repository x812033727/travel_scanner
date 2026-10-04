# DevDay 2026 的 25 項發表，你今天碰得到幾項？照方案分五張清單，這週就能做

slug：`openai-devday-2026-recap`｜旁白繁體中文（台灣）；CC 繁中，其他語言由站主每支勾選｜企劃日 2026-10-03｜目標 8–12 分鐘｜插圖投影片（docs/videos/ILLUSTRATED.md）｜分類 ai-news

沒有來源文章、沒有 `cta` 場景。官方頁都是協調者 2026-10-03 抓下來的版本（`_tools/sources/INDEX.md`）；回顧頁自述「超過 20 項重大發表」，實際列 5 區 25 項（4＋7＋4＋7＋3），影片一律說 25 項或「超過 20 項（OpenAI 自己的說法）」。注意：抓下來的檔頭（`INDEX.md` 與 `devday-2026-recap.zh-Hant.md` 第 6 行）寫「26 個項目」，逐項數 `###` 標題是 25，撰稿與查核以 25 為準，不要照檔頭改回 26。

## 觀眾

台灣與其他華語觀眾優先，四種人，共同點是「每天在用，想知道自己這一層到底變了什麼」：

- 付 Plus 的人：看過 DevDay 的新聞，標題全是 dots、Pro 500、Ultrafast，卻不確定自己花的那一份有沒有變多。搜尋：「DevDay 2026」「GPT-6.1 Sol Plus 能用嗎」「Codex 雲端」「Codex CLI 語音」。
- 付 Pro 的人（含 Pro 200 舊用戶）：想知道 dots、ChatGPT 空間、動態頁面、協作投影片、會議外掛程式是不是已經在自己的帳號裡，還有 Pro 200 的額度為什麼要改、10 月 29 日之後會怎樣。搜尋：「ChatGPT Pro 500」「Pro 200 額度」「ChatGPT 空間」「dots 怎麼用」。
- 公司或團隊用 Business、Enterprise 的人：要回答老闆「Slack 裡的 @ChatGPT、團隊任務、工作站、Codex Security Cloud、私密智慧我們能開嗎」。搜尋：「ChatGPT Slack Teams」「Codex Security Cloud」「OpenAI 市集」。
- 接 API 的開發者：想知道 gpt-6.1-sol 的牌價、Ultrafast 的 `service_tier`、Agents API 的電腦操作、Decisions API、Amazon Bedrock Managed Agents、MCP 事件各自是什麼。搜尋：「GPT-6.1 Sol 價格」「Ultrafast API」「Agents API computer use」「Decisions API」。

他們都已經會用聊天工具，看過本頻道的〈聊天機器人時代結束了〉就更好，不用再聽一次 AI 代理怎麼運作。五張清單裡只要認得出自己那一張就夠；所有人共同的那一張（「使用 ChatGPT 登入」）放最前面，因為每個登入的人都會碰到。

## 觀眾看完能做到的事

- 下次在合作網站看到「使用 ChatGPT 登入」或「以 ChatGPT 繼續」，先讀畫面列出的三樣（姓名、電子郵件、個人檔案照片），確定對方拿不到聊天、記憶、檔案、token、帳務；接著看有沒有第二個獨立的「訂閱共用」請求，要就設上限，不要就只完成登入。公司帳號看不到按鈕先問管理員：這個權限是全域管理員在 OpenAI Admin Console 的 External access 管的，工作區的擁有者或一般管理員不會自動有權限改它（https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt ，2026-10-02 更新）。
- 對照自己的方案打勾：Plus 在 ChatGPT 工作與 Codex 可以選 GPT‑6.1 Sol（對話還沒有）；GPT‑5.5 10 月 14 日從 ChatGPT 與 Codex 退場，Codex 裡改選一個還在的模型，哪一個合用，拿自己的任務算一次再定（https://learn.chatgpt.com/docs/agent-configuration/speed ，官方只寫退場日，沒寫該換哪一個）；帳號裡已經有 dot 的 Pro 用戶打開 dots 的「自訂規則」，把一件會動到別人的操作設成「要先核准」，並確認密碼永遠只有自己能改（dots 是向符合資格的市場逐步推出，台灣有沒有以官網為準）；Pro 200 舊用戶打開「設定 → 我的方案」確認自己是哪一階，再翻信箱找 OpenAI 的通知（說明中心只說那裡看得到方案與可改的方案，受影響的人會收到 email）；開發者先看自己要不要速度，要，才把 Ultrafast 的 ×6（牌價）或 8 份（額度）套到自己的用量上；Sol 對 Astra 的月帳單用上一支「GPT-6 vs Opus 5.5 值不值得付」的公式。

## 站主觀點

套用立場：1、2、3、5、6、7、8

我看 DevDay 這種一次二十幾項的發表，先不問「哪一項最厲害」，先問「我今天登入，碰得到哪幾項」。所以這支影片照方案分清單，每一項旁邊只寫官方頁當天的寫法：誰能用、在哪裡用、哪裡還沒有；同一頁寫得不一樣的（Codex 雲端那一段同時寫「適用於 Plus、Pro、Business、Healthcare、Education 和 Enterprise」和「適用於所有方案」；GPT‑6.1 Sol Ultrafast 回顧頁寫「即將推出」、Sol 頁寫「一併推出」；Ultrafast 在 API 的速度回顧頁寫 6 倍、API 指南寫 up to 8x；協作投影片回顧頁寫可多人同時編輯、空間頁寫投影片協作即將推出），我就直說「以官網為準」，不替它圓。

我最在意的一項不是最大的，是最多人會碰到的：「使用 ChatGPT 登入」。它是一個設定上的界線：官方說明中心寫明只交出姓名、電子郵件、個人檔案照片，聊天、記憶、檔案、token、帳務一律不給；訂閱共用是另一個獨立的核准，可以不答應，答應了也能設上限（https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt ）。所以這支影片給觀眾的那一個動作就是：下次看到那顆按鈕，先讀畫面上列的三樣，再決定要不要勾第二個。帳號裡已經有 dot 的人多一個動作，也是設定不是提示：把 dots 裡一件會動到別人的操作設成「要先核准」。

至於錢，我的看法是付費要付在真的用得到的額度和能力上，先算，再決定要不要升級。會動到帳單的只有三個數字：五分之一（GPT‑6.1 Sol 的 API 標準價是每百萬輸入 2 美元、輸出 10 美元，Astra 是 10 和 50，https://developers.openai.com/api/docs/pricing ）、六倍（Astra Ultrafast 在 API 價目表上每一欄都是標準 Astra 的 6 倍，在 ChatGPT 裡用方案額度的 8 倍、點數的 6 倍，https://learn.chatgpt.com/docs/agent-configuration/speed ）、五百美元（Pro 現在有 100、200、500 三階，只有 Pro 500 含 Ultrafast，推出時 Pro 100 和 Pro 200 買點數也開不了，https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers ）。GPT‑6.1 Sol 在 Plus 的 ChatGPT 工作與 Codex 裡就能選，是這次對最多人有用的一項；Pro 500 買到的是速度和最高額度，不是更聰明的模型，速度是不是你的瓶頸，要用自己的任務算一次才知道。新功能不是換方案、也不是換模型的理由，影片只給算法，不替觀眾選。dots 我不在這裡重講，上一支「聊天機器人時代結束了」已經講過它怎麼運作、怎麼失敗，這裡只把它排進 Pro 那張清單。全部數字都是 OpenAI 自己頁面上的，速度倍數一律說是 OpenAI 的說法；「超過 20 項」「12 億名使用者」「4,000 個應用程式」「32 家合作夥伴」是 OpenAI 自己的數字；我沒有實測任何一項，影片裡也不會說用起來怎樣。

## 示範或實算

三段都用 2026-10-03 抓下來的官方頁數字；每一段寫明哪個選項的哪一章用它。

**示範一：「使用 ChatGPT 登入」的設定走一遍**（選項 A 第 2 章的 `steps`、`bullets`；選項 B 第 1 章；選項 C 第 6 章一句帶過）。來源：OpenAI 說明中心 https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt （頁面更新 2026-10-02），與回顧頁同一段。這是照說明頁讀的五步，不是實測。

| 畫面上會遇到的 | 官方頁怎麼寫 | 觀眾要做的 |
| --- | --- | --- |
| 合作網站的登入頁或外掛程式目錄裡的「Sign in with ChatGPT／Continue with ChatGPT」 | 首批合作夥伴 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel；OpenAI Academy 與 ChatGPT Sites 也有 | 認出按鈕 |
| 第 3 步「檢視登入流程顯示的身分資訊」 | 對方只拿到姓名、電子郵件地址、個人檔案照片（如有） | 讀那三樣 |
| 官方列的「不會分享」 | 聊天內容或記憶、檔案或 token、帳務與其他帳號資料 | 知道底線在哪 |
| 第 5 步「另行檢視並核准其他權限」 | 合作工具可以另外請求使用你 ChatGPT 方案內含的用量（訂閱共用）；你可以設定上限；不核准也能完成登入；核准了也拿不到對話與記憶 | 要就設上限，不要就跳過 |
| 公司帳號 | 全域管理員在 OpenAI Admin Console 的 External access 管；工作區擁有者或管理員不會自動有權限；Business／Enterprise 的管理員預覽期間，ChatGPT Sites 與 Ads 的委派存取預設關閉 | 看不到按鈕先問管理員，不是壞掉 |

**實算二：同一件事開 Ultrafast，三種付法各多扣多少**（選項 A 第 6 章的 `stats`、`compare`、`big`、`chat`；選項 B 第 6 章；選項 C 第 3 章的 `steps`、`table`、`code`、`stats`）。只算 DevDay 新出現的那一欄，不再算「一趟任務三個模型各多少錢」：Sol 對 Astra 的整月帳單上一支「GPT-6 vs Opus 5.5 值不值得付」用 GPT‑6 Sol 算過（同一個代理任務組合，Astra 約 $348、Sol 約 $70），GPT‑6.1 Sol 只是快取輸入從 GPT‑6 Sol 的 $0.20 降到 $0.10，把那支的公式改一個數字就好；怎麼讀同一個模型的八格價目表指向「AI 價格戰」那一支。牌價 ×6 是對照 pricing 頁標準表與 Ultrafast 表算出的比值，8 份／6 倍與 2.5 份／2 倍才是 speed 頁與說明中心直接寫的倍數：

| 付法 | 標準 | Ultrafast | 來源（2026-10-03） |
| --- | --- | --- | --- |
| API 牌價（GPT‑6 Astra，每百萬 token，短脈絡） | 輸入 $10／快取輸入 $1／輸出 $50 | 輸入 $60／快取輸入 $6／輸出 $300（每一欄 ×6）；長脈絡 $120／$12／$450 | https://developers.openai.com/api/docs/pricing （Ultrafast 表當天只列 gpt-6-astra） |
| ChatGPT 工作與 Codex 的方案額度 | 1 份 | 8 份（Fast 是 2.5 份） | https://learn.chatgpt.com/docs/agent-configuration/speed ；https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers |
| 買來的點數、Enterprise 用量計費 | 1 倍 | 6 倍（Fast 是 2 倍） | https://learn.chatgpt.com/docs/agent-configuration/speed |

官方頁寫明這些倍數是計費率，不是速度保證。Sol 的牌價只放一張 `big`：輸入 $2、輸出 $10 是 Astra 的五分之一，快取輸入 $0.10 是十分之一（https://developers.openai.com/api/docs/pricing ），不做任務算術；觀眾問「該換 Sol？」的 `chat` 指向上一支的公式。

**實算三：Ultrafast 把額度用掉多快**（選項 A 第 4 章的 `stats`；選項 B 第 4 章；選項 C 第 5 章）。來源：https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers （2026-10-02 更新）與 https://learn.chatgpt.com/docs/agent-configuration/speed 。同一個模型同一件事，標準模式算 1 份方案額度，Fast 算 2.5 份，GPT‑6 Astra Ultrafast 算 8 份；用買來的點數時 Fast 是 2 倍、Ultrafast 是 6 倍；官方頁寫明這是額度消耗率，不是速度保證。所以「每天用 Ultrafast 跑 10 件事」等於「用標準模式跑 80 件事」的額度，這是算得出來的；每階 Pro 能跑幾件，官方沒有數字，算不出來，以官網為準。Ultrafast 在 ChatGPT 工作與 Codex 只有 Pro 500 與符合資格的 Enterprise／Edu；推出時 Pro 100、Pro 200 買點數也不解鎖；Enterprise 工作區預設關閉，要美國以外推論駐留的工作區不開放。觀眾問「該選哪一階」時，站主只給算式（先數一天有幾件事是坐著等它跑完的，再乘 8 份），不落在方案名上。

## 大綱

三個選項角度不同：A 照方案由小到大排五張清單（誰今天就能用）；B 先把登入按鈕的設定走一遍再分清單（先做一件事，再看全貌）；C 先算會動到帳單的三個數字，再把 25 項分四格（錢與方案優先）。三個都不從 dots 講起、不解釋 dots 怎麼運作；每章一個自己的地點與道具，一天從清晨排到深夜，夜景三章以內；三個的卡片序列都不以 `title` 接 `big`／`compare`／`quote`／`stats` 開頭，第一張畫面都是 `shot`，鉤子在 20 秒內落地。卡片容量照 `tools/video/templates/templates.mjs`：`bullets` 最多 6 條、`steps` 2–5 步、`table` 最多 8 列、`stats` 1–4 格、`chat` 最多 3 句、中文原句的 `quote` 沒有譯文就一次全出（0）。

### 選項 A：先看你付的是哪一種：五張清單（推薦）

一行說明：照方案由小到大排五張清單（所有人 → Plus → Pro → 團隊 → 開發者），登入示範放在最前面的「所有人」那一章並把九項點名，Pro 那一章把三個級別、Pro 200 的四步、額度消耗率講完，開發者那一章用「五分之一、六倍、五百美元」收束並做實算二；和 B（先做登入示範再分清單）、C（先算三個數字再分四格）相比，觀眾最快找到自己那一章，而且「你以為／其實」落在第一章。

開場鉤子（口播）：「DevDay 一口氣發表了二十幾樣東西。可是你今天打開 ChatGPT，碰得到的到底有幾樣？答案不在新聞裡，在你付的是哪一種方案。這集把 25 項照所有人、Plus、Pro、團隊、開發者分成五張清單，再教你一個這週就能改的設定。」

你以為／其實：「你以為 DevDay 的東西都要等開放、要加錢 → 其實 OpenAI 回顧頁列的 25 項裡，官網寫著『適用於所有方案』的有 6 項，加上寫給所有 Codex 使用者、全球已登入使用者、所有其他方案的 3 項，共 9 項的『適用於』那一行寫的是所有方案、所有 Codex 使用者、所有其他方案或全球已登入使用者；免費方案含哪些頁上沒寫，以官網為準」

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 25 項裡，你今天碰得到幾項？ | 25 | `shot`：清晨的火車站售票大廳，五個窗口，人排成幾列（遠景）；`title`：「DevDay 2026 的 25 項，你今天碰得到幾項？」副標「照方案分五張清單」；`shot`：窗口前一隻手遞出月票的特寫；`chat`：觀眾「25 項我今天能用幾項？」→ 站主「先看你付的是哪一種」（2） | 「先從每個人都有的那一張開始？」 |
| 2 | 每個人都有的九項，和那顆登入按鈕 | 135 | `chapter`；`shot`：上午的運動中心櫃台，泳客出示會員卡，櫃台人員看一眼（中景）；`stats`：「6 項」官網寫「適用於所有方案」、「3 項」寫給所有 Codex 使用者、所有其他 ChatGPT 方案、全球已登入使用者（2，出處 OpenAI 回顧頁，註：免費方案含哪些頁上沒寫，以官網為準）；`bullets`：九項點名，Codex 的四項：Codex 雲端（同一段也寫 Plus 以上，以官網為準）、Codex CLI（語音、/agents、worktree）、程式碼審查（桌面應用程式，GitHub 提取要求與 GitLab 合併要求）、Codex Security Cloud（所有 Codex 使用者）（4）；`bullets`：其他五項：外掛程式擴充功能（開發者可在側邊欄做專屬入口、互動面板、檔案檢視器）、外掛程式建立與提交（建立工具、新提交流程、目錄排序，使用者仍逐一核准存取權限）、MCP 事件（回顧頁寫『正加入支援』，提議中的規格）、可分享的個人檔案（所有其他 ChatGPT 方案，Enterprise、Edu、Healthcare 即將推出）、使用 ChatGPT 登入（全球已登入使用者，依組織設定）（5，都是回顧頁「適用於」那一行的寫法）；`shot`：手上那張會員卡的特寫，只有一塊剪影色塊和一條色帶；`steps`：登入五步：合作網站（首批 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel，以官網為準）或外掛程式目錄 → 按「使用 ChatGPT 登入」→ 讀畫面列的身分資訊 → 想用再繼續 → 其他權限另行核准（5）；`shot`：更衣室鑰匙板，一把置物櫃鑰匙另外遞出去（訂閱共用是另一把鑰匙）；`bullets`：對方拿到的三樣 vs 永遠不給的（聊天與記憶、檔案與 token、帳務）（2）；`shot`：救生員把水道繩拉緊到一個記號（設上限）；`shot`：經理室門上的插銷（全域管理員在 Admin Console 的 External access 管，看不到按鈕先問管理員）；`shot`：泳客拿著會員卡走過櫃台、鑰匙留在板上（不核准共用也能登入） | 「那付了 Plus 的人，多了哪幾樣？」 |
| 3 | Plus 的清單：九項之上再加 Sol，順便看 Codex 的三項怎麼用 | 110 | `chapter`；`shot`：接近中午的社區腳踏車修理店，師傅一邊修一邊和客人說話（中景，Codex CLI 用講的）；`big`：「GPT‑6.1 Sol：ChatGPT 工作與 Codex 有了，對話還沒有」小字「Plus、Pro、Business、Enterprise、Edu（Sol 頁 2026-09-29）」；`shot`：三個修車架同時架著三台車（/agents 分派多個智慧體）；`bullets`：九項裡 Codex 的三項怎麼用：Codex 雲端（任務在雲端跑）、Codex CLI（語音、/agents、worktree）、桌面應用程式的程式碼審查（GitHub 提取要求與 GitLab 合併要求、可開自動審查）（3，都是回顧頁的寫法）；`shot`：鐵門拉下一半、店裡的修車架上輪子還在轉（任務在你睡著時繼續跑）；`quote`：Codex Cloud 頁原句「Each task has its own workspace and can keep working while your computer is asleep.」譯「每個任務有自己的工作區，你的電腦睡著了也能繼續」（1，learn.chatgpt.com 2026-10-03）；`shot`：師傅交車前轉一下前輪聽聲音（審查先看摘要再看差異）；`shot`：一把舊扳手被收進抽屜最裡面（GPT‑5.5 要退場）；`stats`：GPT‑5.5 於 2026-10-14 退出 ChatGPT、ChatGPT 工作與 Codex，API 不受影響（2）；`shot`：客人牽著修好的車在店門口的街上試騎（小笑點：旁邊一隻貓坐在輪胎堆上） | 「那 Pro 多付的那一份，換到什麼？」 |
| 4 | Pro 的清單：四項，加一項看市場，和三個級別 | 140 | `chapter`；`shot`：下午的共用陶藝工作室，長桌邊三個人各做各的，角落一台拉坯機空著還在轉（dot 在你不在時工作）；`bullets`：dots（符合資格的市場逐步推出，第一個不另收費，台灣有沒有，以官網為準，怎麼運作、怎麼失敗看上一支）、ChatGPT 空間（網頁與桌面可編輯，行動版只能看，分享頁面不分享私人對話與記憶，但頁上寫的都看得到）、動態頁面、協作投影片（可匯出 PowerPoint 或 Google 簡報，回顧頁寫可多人同時編輯、空間頁寫投影片協作即將推出，以官網為準）、會議外掛程式 Beta（Pro 與 Business，macOS 桌面應用程式）（5）；`big`：「跟 dot 聊天不算額度，叫它在 Codex 或 ChatGPT 工作裡跑任務才算」小字「第一個 dot 不另收費」（dots 頁 2026-09-29 那兩句的寫法，不另做 quote 卡）；`shot`：拉坯機上的土慢慢成形，旁邊沒有人（dot 替你跑的任務才扣額度）；`shot`：兩雙手在同一個碗上，一個修坯、一個上釉（頁面一起改）；`big`：「主動研究只用唯讀工具・自訂規則：允許、先核准、封鎖・改密碼一律你自己來」小字「出處 dots 頁 2026-09-29；dots 怎麼運作、怎麼失敗看上一支」；`shot`：窯邊兩個人在講、第三個人點頭記著（會議筆記）；`table`：Pro 100 $100／Pro 200 $200／Pro 500 $500，只有 Pro 500 含 Ultrafast（3，註腳一行：Pro 只能月繳，點數適用 Codex、ChatGPT 工作、ChatGPT for Word／Excel／PowerPoint，不是每個功能都能用點數，推出時 Pro 100／200 買點數也開不了 Ultrafast）；`shot`：陶藝師看著三座大小不同的窯（三個級別）；`steps`：Pro 200 的四步：9/22–9/29 上午 10 點（太平洋時間）之間訂過 → 舊額度留到 10/29 → 之後換新額度、月費不變 → 留舊額度不等於升級、不會多出 Ultrafast（4，說明中心 2026-10-02）；`shot`：陶藝師把兩把窯房的鑰匙並排放在掌心，一把舊一把新（舊額度與新額度）；`stats`：「8 份」同一件事 Astra Ultrafast 吃的方案額度（標準 1 份、Fast 2.5 份）、「80 件」每天用 Ultrafast 跑 10 件等於標準模式幾件的額度（2，額度消耗率不是速度保證，每階能跑幾件算不出來，以官網為準）；`chat`：觀眾「我每天用 Codex 兩三個小時，該選哪一階？」→ 站主「先數你一天有幾件事是坐著等它跑完的，再對照官方的消耗率：同一件事 Ultrafast 吃 8 份額度，等的時間值不值這 8 倍，只有你自己的量算得出來」（2）；`shot`：工作室門口的台階上坐著一隻貓，門半開（離開前先看一眼） | 「公司帳號呢？團隊多了哪幾樣？」 |
| 5 | 團隊的清單 | 110 | `chapter`；`shot`：傍晚出餐的餐廳廚房，主廚隔著出菜口喊話（遠景，@ChatGPT 在頻道裡）；`bullets`：建立團隊並共用任務、Slack 與 Microsoft Teams 的 @ChatGPT（用管理員連的工具或你授權後用你的，沒有授權的同事也能補背景）、可連結外掛程式的工作站（各自的權限登入）、私密智慧（API 的零資料保留搭配私密安全處理，按專案開啟、要先取得 ZDR 核准，私密推論是預覽版，以官網為準）、OpenAI 市集 Beta（5）；`shot`：每個廚師在自己的工作台用自己的刀（工作站：各自的權限）；`shot`：一個廚師按鈴把托盤交到下一站（團隊任務依排程或情況變化時動）；`shot`：出菜口旁的白板上貼滿空白的單子，一個沒有授權的外場也能補一張（沒有授權的同事也能補背景）；`steps`：Codex Security Cloud（卡片標「所有 Codex 使用者都有，公司帳號多的是把整個存放庫排程掃」）：安裝外掛程式 → 連 GitHub → 一次性掃描 → 看發現、按「Fix with Codex」出草稿提取要求 → 持續掃描（5）；`shot`：廚房後門的鐵捲門拉下一半，裡面的燈還亮著（人走了，掃描沒停）；`bullets`：公司要看的兩件事：資料駐留端點對 2026-03-05 起發布、且符合資料駐留資格的模型加價 10%／Enterprise 的 Ultrafast 預設關、要美國以外推論駐留的工作區不開放（2）；`shot`：後門供應商搬著箱子交貨（市集：用既有合約的承諾支出）；`stats`：「32 家」市集首批合作夥伴（OpenAI 自己的數字）、「Beta」開放符合資格的企業客戶（2，以官網為準） | 「接 API 的人，牌價到底變了多少？」 |
| 6 | 開發者的清單：三個數字，和 Ultrafast 的三種付法 | 125 | `chapter`；`shot`：晚上的夜市小吃街，一攤前兩口鍋（遠景）；`big`：「五分之一・六倍・五百美元」小字「Sol 的牌價、Ultrafast 的牌價、Pro 500 的月費」；`shot`：攤前的價目木牌只畫了三格、沒有字，攤主指著其中一格；`stats`：Astra 標準 → Astra Ultrafast，每一欄 ×6：「$10→$60」輸入、「$1→$6」快取輸入、「$50→$300」輸出（3，API 牌價 2026-10-03，長脈絡 $120／$12／$450，Ultrafast 表當天只列 gpt-6-astra）；`shot`：一台外送機車從排隊的人旁邊鑽過去（速度要加錢）；`compare`：左「它賣的是速度（OpenAI 的說法）」Codex 最高 8 倍、每秒 300 token，API 回顧頁寫 6 倍、API 指南寫 up to 8x，以官網為準，右「它收的是錢」API 每欄 6 倍，ChatGPT 工作與 Codex 方案額度 8 份、買的點數 6 倍，Fast 是 2.5 份／2 倍（2）；`shot`：攤商在秤上秤兩堆東西（特寫，手與秤）；`big`：「Sol 的牌價：輸入 $2、輸出 $10，是 Astra 的五分之一，快取輸入 $0.10 是十分之一」小字「gpt-6.1-sol：脈絡 1,050,000、知識截止 2026-04-30（developers.openai.com 模型頁 2026-10-03），不做任務算術」；`chat`：觀眾「所以該換 Sol？」→ 站主「整月帳單上一支用 GPT‑6 Sol 算過，Astra 約 $348、Sol 約 $70，GPT‑6.1 Sol 只是快取再便宜一半，把那支的公式改一個數字就好」（2）；`bullets`：Astra 的 `service_tier` 設 ultrafast（API 所有人可用，速率上限低）、Agents API 不另收費只付 token 與工具、Agents API 的電腦操作（API，Pro 500 與符合資格的 Enterprise 在 Codex 與 ChatGPT 工作）（3）；`shot`：攤主把攤子交給幫手自己去進貨（Agents API：任務執行框架由 OpenAI 代管）；`bullets`：Decisions API 限量預覽（以官網為準）、Amazon Bedrock Managed Agents（以官網為準）、MCP 事件（回顧頁寫適用於所有方案，這裡放開發者只因為它是提議中的規格）（3）；`shot`：射氣球的遊戲攤，靶只有幾個固定的位置（Decisions API：預設答案有限）；`shot`：收攤時燈一盞盞關，人潮散了 | 「那這週，每一張清單的人該先做哪一件事？」 |
| 7 | 這週做的一件事，和還不能碰的 | 70 | `shot`：深夜家裡的餐桌，一杯茶、一本闔上的筆記本（中景）；`steps`：所有人：下次看到登入按鈕先讀三樣 → Plus：GPT‑5.5 10 月 14 日從 ChatGPT 與 Codex 退場，Codex 裡改選一個還在的模型，哪一個合用，拿自己的任務算一次再定 → Pro：帳號裡已經有 dot 的人，把一件會動到別人的操作設成「要先核准」，Pro 200 打開「設定 → 我的方案」確認自己是哪一階，再翻信箱找 OpenAI 的通知 → 開發者：先看自己要不要速度，要，才把 Ultrafast 的 ×6（牌價）或 8 份（額度）套到自己的用量上，Sol 對 Astra 的月帳單用上一支的公式（4）；`shot`：鉛筆放在筆記本上，旁邊一枚月票；`bullets`：還不能碰的：GPT‑6.1 Sol Ultrafast（回顧頁寫即將推出、Sol 頁寫一併推出，以官網為準）、空間的行動版編輯與投影片的多人協作（空間頁寫即將推出）、會議外掛程式的 Enterprise、Decisions API 全面開放、dots 的簡訊、個人檔案的 Enterprise／Edu／Healthcare（其他方案已經有）（6，寫「即將推出」的都在這）；`shot`：關掉家裡餐廳的燈，走廊留一盞；`outro`：「25 項裡，你今天碰得到幾項？」：官網說登入就有 9 項，Plus 再加 Sol 一項，Pro 再加 4 項、dots 看市場、Pro 500 這一階算一項，團隊再加 5 項，開發者 4 項看牌價，加起來 25，會動到帳單的只有五分之一、六倍、五百美元，下一步：留言 | 最後一句回答開場：「所以不是新聞說了幾項，是你付的那一種方案裡，今天打開就有的那幾項；要不要多付，三個數字算完再說。」 |

實算二在第 6 章、實算三在第 4 章，登入示範與九項點名在第 2 章。結尾的下一步（只有一個）：「留言告訴我你是哪一張清單的人，這週先碰哪一項。」總長約 715 秒，旁白約 2,980 字（每分鐘 250 字估；真實語速約 300 字，實剪落在 10 分鐘上下）；37 個 `shot`、37 張卡片（含 5 張章節卡），畫面狀態 128 個（`_tools/critic-jev/states.mjs` 的算法），平均 5.6 秒一個，每章都在 5.0 秒以上；shot 帶運鏡、每張 6–10 秒，所以插圖時間超過一半。夜景：第 5 章（廚房燈下）、第 6、7 章，三章。25 項的加總：9（所有人）＋1（Sol）＋5（dots、空間、動態頁面、協作投影片、會議外掛程式）＋1（Pro 500 級別）＋5（團隊任務、@ChatGPT、工作站、私密智慧、市集）＋4（極速、Decisions API、Agents API 的電腦操作、Bedrock）＝25；Codex Security Cloud 與 MCP 事件只算在所有人的九項裡，不重複算。

### 選項 B：先把登入按鈕走一遍，再分清單

一行說明：把「使用 ChatGPT 登入」的設定走一遍當開場（觀眾在前兩分鐘就做完一件事），之後才分「所有人的九項」、Plus、Pro、團隊、開發者五張清單，實算放最後；和 A 相比先做再分，更貼近立場 5，但「25 項」的全貌要到第 2 章才出現；和 C 相比錢講得最晚。

開場鉤子（口播）：「下次看到『使用 ChatGPT 登入』這顆按鈕，先別急著按。它只會把三樣東西交出去；可是同一個流程裡還有第二個核准，叫訂閱共用，可以不答應，答應了也能設上限。從這顆按鈕開始，把 DevDay 的 25 項照你能不能用分清單。」

你以為／其實：「你以為用 ChatGPT 登入別的網站，就是把 ChatGPT 帳號整個交出去 → 其實官方說明中心列的只有姓名、電子郵件、個人檔案照片三樣，聊天、記憶、檔案、token、帳務都不給；訂閱共用是另一個獨立的核准，不核准也能完成登入」

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 那顆按鈕只交出三樣：登入流程走一遍 | 125 | `shot`：上午的運動中心櫃台，泳客出示會員卡（中景）；`title`：「使用 ChatGPT 登入，交出的只有三樣」副標「DevDay 2026 的 25 項，照你能不能用分清單」；`shot`：會員卡的特寫，只有一塊剪影色塊和一條色帶；`bullets`：姓名、電子郵件、個人檔案照片（3）；`shot`：櫃台人員把會員卡翻過來，指著卡上的三樣；`steps`：五步：合作網站或外掛程式目錄 → 按「使用 ChatGPT 登入」→ 讀畫面列的身分資訊 → 想用再繼續 → 其他權限另行核准（5）；`shot`：更衣室鑰匙板上另外遞出一把鑰匙（訂閱共用是另一把鑰匙）；`bullets`：永遠不給的三類：聊天與記憶、檔案與 token、帳務（3）；`shot`：救生員把水道繩拉到記號（設上限）；`table`：首批合作夥伴 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel（6，以官網為準）；`shot`：經理室門上的插銷（全域管理員在 Admin Console 的 External access 管，看不到按鈕先問管理員）；`shot`：泳客走過櫃台，鑰匙留在板上（不核准共用也能登入） | 「除了這顆按鈕，還有幾項是官網說今天登入就有的？」 |
| 2 | 官網說每個人今天就有的九項 | 90 | `chapter`；`shot`：接近中午的火車站售票大廳，五個窗口（遠景）；`stats`：「6 項」官網寫「適用於所有方案」、「3 項」所有 Codex 使用者、所有其他方案、全球已登入使用者（2，OpenAI 回顧頁，免費方案含哪些頁上沒寫）；`shot`：窗口前遞出月票的手；`bullets`：Codex 的四項：Codex 雲端（同一段也寫 Plus 以上，以官網為準）、Codex CLI、程式碼審查、Codex Security Cloud（所有 Codex 使用者）（4）；`bullets`：其他五項：外掛程式擴充功能、外掛程式建立與提交、MCP 事件、可分享的個人檔案（所有其他方案）、使用 ChatGPT 登入（全球已登入使用者）（5）；`shot`：站務員把一塊木牌翻面（同一頁兩種寫法，以官網為準）；`shot`：月台上一列區間車慢慢進站，門開了一半；`shot`：出站口的閘門，一張月票刷過去就開（登入就有的） | 「付了 Plus，多了哪幾樣？」 |
| 3 | Plus 的清單：再加 Sol，順便看 Codex 的三項怎麼用 | 100 | `chapter`；`shot`：午後的腳踏車修理店，師傅邊修邊和客人講話（CLI 用講的）；`big`：「GPT‑6.1 Sol：ChatGPT 工作與 Codex 有了，對話還沒有」小字「Plus、Pro、Business、Enterprise、Edu」；`shot`：三個修車架三台車（/agents）；`bullets`：Codex 雲端（任務在雲端跑）、Codex CLI（語音、/agents、worktree）、桌面應用程式的程式碼審查（GitHub PR 與 GitLab MR、可開自動審查）（3）；`shot`：鐵門半拉、輪子還在轉；`quote`：Codex Cloud 頁「Each task has its own workspace and can keep working while your computer is asleep.」與譯文（1）；`shot`：舊扳手收進抽屜；`stats`：GPT‑5.5 於 2026-10-14 退出 ChatGPT、ChatGPT 工作與 Codex，API 不受影響（2）；`shot`：客人在店門口試騎 | 「Pro 多付的那一份換到什麼？」 |
| 4 | Pro 的清單：四項，加一項看市場，和三個級別 | 120 | `chapter`；`shot`：下午稍晚的陶藝工作室，角落的拉坯機空著還在轉；`bullets`：dots（符合資格的市場逐步推出，第一個不另收費，台灣有沒有以官網為準，怎麼運作看上一支）、ChatGPT 空間（網頁與桌面可編輯，行動版只能看）、動態頁面、協作投影片（回顧頁寫可多人同時編輯、空間頁寫投影片協作即將推出，以官網為準）、會議外掛程式 Beta（5）；`shot`：工作室牆上的工具架，五格各放一件；`big`：「跟 dot 聊天不算額度，叫它在 Codex 或 ChatGPT 工作裡跑任務才算」小字「第一個 dot 不另收費」；`shot`：拉坯機上的土慢慢成形，旁邊沒有人；`shot`：兩雙手在同一個碗上；`big`：「主動研究只用唯讀工具・自訂規則：允許、先核准、封鎖・改密碼一律你自己來」小字「出處 dots 頁 2026-09-29；怎麼運作看上一支」；`table`：Pro 100／200／500，只有 Pro 500 含 Ultrafast（3，註腳：Pro 只月繳，點數適用 Codex、ChatGPT 工作、ChatGPT for Word／Excel／PowerPoint，推出時買點數開不了 Ultrafast）；`shot`：三座大小不同的窯；`steps`：Pro 200 的四步：9/22–9/29 上午 10 點太平洋時間訂過 → 舊額度留到 10/29 → 月費不變 → 不等於升級、不會多出 Ultrafast（4）；`shot`：兩把窯房鑰匙並排在掌心；`stats`：「8 份」同一件事 Ultrafast 吃的額度（標準 1、Fast 2.5）、「80 件」10 件 Ultrafast 等於標準幾件（2，每階能跑幾件以官網為準）；`shot`：台階上的貓 | 「團隊多了哪幾樣？」 |
| 5 | 團隊的清單 | 100 | `chapter`；`shot`：傍晚出餐的廚房，主廚隔著出菜口喊話；`bullets`：團隊與共用任務、@ChatGPT、工作站、私密智慧（API 的零資料保留搭配私密安全處理，按專案開啟、要 ZDR 核准，私密推論預覽版，以官網為準）、市集 Beta（5）；`shot`：各自的工作台各自的刀；`shot`：出菜口旁的白板貼滿空白的單子，外場補上一張；`steps`：Codex Security Cloud 五步（卡片標「所有 Codex 使用者都有」）（5）；`shot`：廚房後門鐵捲門拉下一半、燈還亮；`bullets`：公司要看的兩件事：資料駐留端點對 2026-03-05 起發布、且符合資料駐留資格的模型加價 10%／Enterprise 的 Ultrafast 預設關（2）；`shot`：後門交貨的供應商；`stats`：「32 家」首批合作夥伴（OpenAI 自己的數字）、「Beta」開放符合資格的企業客戶（2，以官網為準） | 「接 API 的人，牌價變了多少？」 |
| 6 | 開發者的清單：三個數字，和 Ultrafast 的三種付法 | 115 | `chapter`；`shot`：晚上的夜市小吃街；`big`：「五分之一・六倍・五百美元」；`shot`：攤前的價目木牌只畫了三格、沒有字；`stats`：Astra 標準 → Ultrafast 每欄 ×6：「$10→$60」輸入、「$1→$6」快取輸入、「$50→$300」輸出（3，長脈絡 $120／$12／$450）；`shot`：外送機車鑽過人群；`compare`：賣的是速度（Codex 8 倍，API 回顧頁 6 倍、指南 8x，以官網為準）vs 收的是錢（API 每欄 6 倍、額度 8 份、點數 6 倍，Fast 2.5 份／2 倍）（2）；`shot`：攤前排隊的人龍和空著的快速窗口；`big`：「Sol 的牌價：輸入 $2、輸出 $10 是 Astra 的五分之一，快取輸入 $0.10 是十分之一」小字「脈絡 1,050,000、知識截止 2026-04-30」；`chat`：「該換 Sol？」→「整月帳單上一支用 GPT‑6 Sol 算過，Astra 約 $348、Sol 約 $70，6.1 Sol 只是快取再便宜一半，公式改一個數字」（2）；`bullets`：`service_tier` 設 ultrafast、Agents API 不另收費、Agents API 的電腦操作（3）；`shot`：攤主把攤子交給幫手；`bullets`：Decisions API 與 Bedrock 以官網為準、MCP 事件（提議中的規格，回顧頁寫適用於所有方案）（3）；`shot`：秤上的兩堆東西；`shot`：收攤關燈 | 「這週先做哪一件？」 |
| 7 | 這週做的一件事 | 65 | `shot`：深夜餐桌上的茶和筆記本；`steps`：四步：所有人登入先讀三樣／Plus：GPT‑5.5 10 月 14 日退場，Codex 裡改選一個還在的模型，哪一個合用拿自己的任務算一次再定／Pro：帳號裡已經有 dot 的人設一件「要先核准」，Pro 200 看「我的方案」再翻信箱／開發者：要速度才把 ×6 或 8 份套到自己的用量上（4）；`bullets`：還不能碰的六項：Sol Ultrafast（兩頁說法不同，以官網為準）、空間的行動版編輯與投影片多人協作、會議外掛程式的 Enterprise、Decisions API 全面開放、dots 的簡訊、個人檔案的 Enterprise／Edu／Healthcare（6）；`shot`：關燈留一盞；`outro`：回答開場：「那顆按鈕只交出三樣，其他的看你付哪一種：登入就有 9 項、Plus 加 Sol、Pro 加 4 項與 dots 看市場、團隊加 5 項、開發者 4 項，會動到帳單的只有三個數字」，下一步：留言 | 最後一句回答開場 |

登入示範在第 1 章，實算二在第 6 章、實算三在第 4 章。結尾的下一步（只有一個）：留言。總長約 715 秒，旁白約 2,980 字；7 章、七個地點；38 個 `shot`、37 張卡片，畫面狀態 135 個，平均 5.3 秒一個；shot 帶運鏡、每張 6–10 秒，插圖時間超過一半。夜景：第 5、6、7 章。風險：第 1 章只講一顆按鈕，搜尋「DevDay 2026」進來的人要等到第 2 章才看到 25 項的全貌。

### 選項 C：先算三個數字，再把 25 項分四格

一行說明：錢與方案優先：開場就把會動到帳單的三個數字（五分之一、六倍、五百美元）擺出來，第 2–5 章依序講 Sol 的價、同一件事開 Ultrafast 的三種付法、極速賣的速度與誰能開、Pro 三階怎麼對號，第 6 章才把 25 項分成「官網寫所有方案或 Plus 以上就能用的、要 Pro 的、要公司買的、API 為主的」四格；和 A、B 相比，數字先出來、觀眾最快知道自己要不要掏錢，但登入那一個動作縮成一句，不做設定示範。

開場鉤子（口播）：「DevDay 講了二十幾樣東西，真正會動到你帳單的只有三個數字：五分之一、六倍、五百美元。先把這三個數字算清楚，再把其他的分成四格：官網寫人人能用的、要 Pro 的、要公司買的、API 為主的。」

你以為／其實：「你以為新模型出來，想用就要多付錢 → 其實 GPT‑6.1 Sol 的 API 價是 Astra 的五分之一，每百萬輸入 2 美元、輸出 10 美元，而 Sol 頁寫 Plus、Pro、Business、Enterprise、Edu 在 ChatGPT 工作與 Codex 裡就能選它，對話裡還沒有」

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 三個數字 | 25 | `shot`：清晨早餐店的櫃台，一隻手把三枚硬幣推過木檯面，老闆娘在煎台前側身；`title`：「DevDay 2026 先算帳」副標「五分之一、六倍、五百美元」；`chat`：觀眾「新模型出來，是不是又要多付錢？」→ 站主「先看三個數字」（2）；`shot`：三枚硬幣排成一列的特寫 | 「新模型出來，是不是又要多付錢？」 |
| 2 | 你以為要加錢，其實是五分之一 | 100 | `chapter`；`shot`：上午的傳統市場水果攤，兩籃一樣的橘子，一籃掛大標籤一籃掛小標籤，攤主正在秤；`stats`：Astra 輸入 $10／輸出 $50 → Sol $2／$10，快取輸入 $0.10（3）；`shot`：攤主把一顆橘子切開給客人試吃（接近 Astra 的能力，OpenAI 自己公布的評測）；`quote`：Sol 頁原句「接近 Astra 的智慧，價格僅需五分之一」，OpenAI 2026-09-29（0，中文原句不另譯、一次全出）；`shot`：客人提著兩袋橘子走出市場，背影；`table`：誰能用 Sol：API、Plus、Pro、Business、Enterprise、Edu，在 ChatGPT 工作與 Codex，對話裡尚未提供（3）；`shot`：市場出口的遮雨棚下，一個人翻看手裡的購物袋 | 「那同一件事開極速，三種付法各多扣多少？」 |
| 3 | 同一件事開極速，三種付法 | 110 | `chapter`；`shot`：中午的小吃店後面那張結帳桌，一疊收據夾在鐵夾上，算盤和三個硬幣堆；`steps`：三種付法：用 API 牌價 → 用方案額度（Pro 500、符合資格的 Enterprise／Edu）→ 用買來的點數（3）；`shot`：老闆把硬幣分成三堆，兩堆六枚高、一堆八枚高；`table`：API 牌價每一欄 ×6（輸入 $10→$60、快取輸入 $1→$6、輸出 $50→$300）／方案額度 8 份／買的點數 6 倍（3，pricing 頁與 speed 頁 2026-10-03，Ultrafast 表當天只列 gpt-6-astra）；`code`：算式「標準牌價 × 6 ＝ Ultrafast 牌價，件數 × 8 ＝ 方案額度份數，件數 × 6 ＝ 點數倍數」；`shot`：客人把現金、一本票券和一張會員卡並排放在檯面上（三種付法）；`stats`：「2.5 份／2 倍」Fast 的額度與點數、「$120／$12／$450」Ultrafast 的長脈絡牌價（2，官方寫明倍數是計費率不是速度）；`shot`：老闆把算盤撥回零；`shot`：老闆娘把三堆硬幣推回抽屜，檯面只留一枚 | 「那六倍買到的『極速』，到底有多快、誰能開？」 |
| 4 | 極速：賣的是速度，誰能開 | 100 | `chapter`；`shot`：下午的火車月台，一列快車呼嘯而過，旁邊一列區間車慢慢進站，一個人看著兩邊；`compare`：左「它賣的是速度（OpenAI 的說法）」Codex 最高 8 倍、每秒 300 token，API 回顧頁寫 6 倍、API 指南寫 up to 8x，以官網為準，右「它收的是錢」API 每欄 6 倍，方案額度 8 份，點數 6 倍（第 3 章算過）（2）；`shot`：月台上兩班車的時刻牌只畫兩個箭頭、沒有字；`stats`：「8 倍」Codex 的 token 生成速度（每秒 300 個，OpenAI 的說法，量的是生成速度，不是整件任務的完成時間）、「6 倍 vs up to 8x」API 的倍數：回顧頁 vs API 指南，以官網為準（2）；`shot`：月台售票窗口，一隻手遞出比旁邊厚很多的一疊鈔票；`shot`：快車車廂裡的人靠窗坐著，窗外景色拉成線；`table`：誰能用：API 所有人（速率上限低）、ChatGPT 工作與 Codex 只有 Pro 500 和符合資格的 Enterprise／Edu（Enterprise 工作區預設關）、GPT‑6.1 Sol Ultrafast 回顧頁寫即將推出、Sol 頁寫一併推出，以官網為準（3）；`shot`：月台柱子旁，一個人把車票收回口袋，沒上快車 | 「所以 Pro 500，到底是誰該看的？」 |
| 5 | Pro 100、200、500：對號入座 | 115 | `chapter`；`shot`：傍晚老公寓的樓梯間，三層樓梯平台，一個人站在第二層往上看；`table`：Pro 100 $100、Pro 200 $200、Pro 500 $500，只有 Pro 500 含 Ultrafast（3）；`shot`：一樓信箱牆前，住戶手裡拿著一封信（Pro 200 的通知）；`steps`：9/22–9/29 上午 10 點太平洋時間訂過 Pro 200 → 舊額度留到 10/29 → 之後換新額度、月費不變 → 留舊額度不等於升級、不會多出 Ultrafast（4）；`shot`：舊住戶把一把舊鑰匙和一把新鑰匙並排放在掌心；`chat`：觀眾「我每天用 Codex 兩三個小時，該選哪一階？」→ 站主「先數你一天有幾件事是坐著等它跑完的，同一件事 Ultrafast 吃 8 份額度，等的時間值不值這 8 倍，只有你自己的量算得出來」（2）；`shot`：住戶在二樓平台停下來看手裡的鑰匙；`stats`：同一件事：標準 1 份、Fast 2.5 份、Ultrafast 8 份額度，10 件 Ultrafast＝80 件標準，每階能跑幾件以官網為準（3）；`shot`：三樓的門口，一個人把手放在門把上但沒開門；`bullets`：Pro 只能月繳，點數適用 Codex、ChatGPT 工作、ChatGPT for Word／Excel／PowerPoint，推出時 Pro 100／200 買點數也開不了 Ultrafast，GPT‑5.5 於 10/14 從 ChatGPT 與 Codex 下架，API 不受影響（4）；`shot`：樓梯間的窗，天色轉成橘色 | 「剩下的二十幾項，哪些是你本來就有的？」 |
| 6 | 25 項分四格 | 130 | `chapter`；`shot`：黃昏的社區回收站，四個分類桶，一個人提著袋子正在分東西；`table`：格一「官網寫所有方案、或 Plus 以上就能用」分四列、第二欄點名：GPT‑6.1 Sol｜Plus 以上，ChatGPT 工作與 Codex／Codex 四項｜雲端（同頁兩種寫法，以官網為準）、CLI、程式碼審查、Security Cloud／外掛程式三項｜擴充功能、建立與探索、MCP 事件／個人檔案、登入｜所有其他方案、全球已登入（4，共 10 項，免費方案含哪些頁上沒寫）；`shot`：第一個桶旁邊貼著一張只畫了剪影色塊和色帶的會員卡（登入只交出三樣，訂閱共用另外核准）；`shot`：第一個桶已經滿了，蓋子壓不下去；`table`：格二「要 Pro 以上」：dots（Pro、Business Premium、Enterprise，符合資格的市場逐步推出，第一個不另收費）、ChatGPT 空間、動態頁面、協作投影片（回顧頁寫可多人同時編輯、空間頁寫投影片協作即將推出，以官網為準）、會議外掛程式 Beta、Pro 500 級別（Astra Ultrafast）（6）；`quote`：dots 頁原句「你與 Dot 的對話不會計入 ChatGPT 的用量限制。當你請 Dot 在 Codex 或 ChatGPT 工作中啟動或管理任務時，這些任務仍會照常計入用量限制。」OpenAI 2026-09-29（0，中文原句不另譯、一次全出）；`shot`：回收站旁邊的人把一個紙箱整個扛走（dots：第一個不另收費）；`table`：格三「要 Business／Enterprise」：可連結外掛程式的工作站、建立團隊並共用任務、Slack 與 Teams 的 @ChatGPT、OpenAI 市集（4）；`shot`：兩個人在第三個桶前討論該丟哪一桶；`bullets`：格四「API 為主」：Decisions API（限量預覽）、Agents API 的電腦操作（API，Pro 500 與符合資格的 Enterprise 也能在 Codex 與 ChatGPT 工作用）、Amazon Bedrock Managed Agents（以官網為準）、極速（API 的 Ultrafast 價目層，ChatGPT 工作與 Codex 要 Pro 500 或符合資格的 Enterprise／Edu）、私密智慧（API 專案層級，先取得 ZDR 核准，私密推論預覽版，以官網為準）（5）；`shot`：收拾完的回收站，四個桶蓋好，一個人提著空袋子走回家 | 「所以看完這集，你的方案要不要動？」 |
| 7 | 所以，要不要換方案？ | 55 | `shot`：晚上家裡的餐桌，一個人拿鉛筆在小本子上寫，旁邊一杯茶；`chat`：觀眾「一句話，我該升級嗎？」→ 站主「先用自己的用量算一次，再看等待時間值不值錢」（2）；`bullets`：三個動作：要速度的人把 Ultrafast 的 ×6 或 8 份套到自己的用量上、Sol 對 Astra 用上一支的月帳單公式，打開「我的方案」確認是哪一階，再翻信箱找 10/29 的通知，下次看到登入按鈕先讀三樣（3）；`shot`：那個人合上本子，把筆放在上面；`outro`：「新功能不是換方案的理由，要不要動，先看自己的帳單」，下一步：留言告訴我你在哪一格、這週先碰哪一項 | 最後一句回答開場：「會動到你帳單的只有三個數字，其他的，看你在哪一格。」 |

實算二在第 3 章、實算三在第 5 章，登入只在第 6 章一句帶過。總長約 635 秒（旁白約 2,650 字）；30 個 `shot`、30 張卡片，畫面狀態約 100 個，平均 6.3 秒一個。七個地點：早餐店櫃台、水果攤、小吃店結帳桌、火車月台、老公寓樓梯間、社區回收站、家裡餐桌；只有第 6、7 章在黃昏與夜裡。結尾的下一步（只有一個）：留言。風險：Pro 200 的窗口與 10/29 期限過了之後，第 5 章要重寫；登入那一個設定動作沒有示範；第 3、4 章都講極速，撰稿時第 3 章只講錢、第 4 章只講速度與誰能開，不要互相重複。

## 會過期的事實

| 事實 | 重新確認的來源（撰稿日再開一次；openai.com、help.openai.com、chatgpt.com、learn.chatgpt.com 要用瀏覽器開） |
| --- | --- |
| 回顧頁列的項目數（5 區 25 項；頁面自述「超過 20 項重大發表」；抓下來的檔頭寫 26，逐項數 `###` 標題是 25）、每一項的「適用於」寫法、Codex 雲端同一段兩種寫法（Plus 以上／所有方案）、免費方案含哪些頁上沒寫 | https://openai.com/zh-Hant/index/devday-2026-recap/ （頁面日期 2026-09-29） |
| GPT‑6.1 Sol：Plus、Pro、Business、Enterprise、Edu 在 ChatGPT 工作與 Codex 可用、對話尚未提供；API 牌價 $2／$0.10／$10；Pro 500 每月 $500；Astra Ultrafast 最高 8 倍（OpenAI 的說法）；Sol Ultrafast「一併推出」（回顧頁寫「即將推出」，兩頁說法不同，以官網為準）；評測分數是 OpenAI 自己公布的 | https://openai.com/zh-Hant/index/introducing-gpt-6-1-sol/ |
| Ultrafast 的速度倍數：回顧頁寫 Codex 最高 8 倍（每秒 300 個 token）、API 最高 6 倍；API 指南寫「up to 8x faster speeds than Standard mode」；speed 頁寫量的是 token 生成速度、不是整件任務的完成時間；影片說 Codex 最高 8 倍，API 的倍數兩頁不同、以官網為準；速度一律是 OpenAI 的說法 | https://developers.openai.com/api/docs/guides/ultrafast-mode ；https://learn.chatgpt.com/docs/agent-configuration/speed ；回顧頁 |
| 牌價表：Astra 10／1／12.5／50、Sol 2／0.10／2.5／10、Luna 0.10／0.01／0.125／0.50、Ultrafast Astra 60／6／75／300（長脈絡 120／12／150／450；Ultrafast 表 2026-10-03 只列 gpt-6-astra）；Fast 2 倍；長脈絡門檻 272K；資料駐留端點對 2026-03-05 起發布、且符合資料駐留資格的模型加價 10% | https://developers.openai.com/api/docs/pricing |
| gpt-6.1-sol 脈絡 1,050,000、最大輸出 128,000、知識截止 2026-04-30 | https://developers.openai.com/api/docs/models/gpt-6.1-sol |
| Ultrafast 的 `service_tier: "ultrafast"`、目前對 GPT‑6 Astra 廣泛開放、所有 API 使用者可用但速率上限低；只支援美國資料駐留與全球處理 | https://developers.openai.com/api/docs/guides/ultrafast-mode |
| Pro 100 $100、Pro 200 $200、Pro 500 $500；只有 Pro 500 含 Ultrafast；推出時 Pro 100／200 買點數不解鎖；Pro 200 舊額度：2026-09-22 到 09-29 10 a.m. PT 有效訂閱者用到 2026-10-29，留舊額度不等於升級、不會多出 Ultrafast；Fast 扣額度 2.5 倍、Astra Ultrafast 8 倍（額度消耗率，不是速度保證）；Pro 只月繳；點數適用 Codex、ChatGPT 工作、ChatGPT for Word／Excel／PowerPoint，不是每個功能都能用；各階額度大小官方沒有數字；「設定 → 我的方案」只寫看方案與可改的方案，受影響的人會收到 email | https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers （更新 2026-10-02） |
| 使用 ChatGPT 登入：只分享姓名、電子郵件、個人檔案照片；不分享對話、記憶、檔案、token、帳務；首批合作夥伴 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel；訂閱共用另行核准、可設上限、不核准也能登入；全域管理員在 Admin Console 的 External access 管，工作區擁有者或管理員不自動有權限；Sites 與 Ads 委派存取預設關閉 | https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt （更新 2026-10-02） |
| Fast 額度 2.5 倍（點數 2 倍）、Astra Ultrafast 額度 8 倍（點數 6 倍）；Ultrafast 只在 Pro $500 與符合資格的 Enterprise／Edu；Enterprise 工作區預設關閉、要美國以外推論駐留的工作區不開放；GPT‑5.5 於 2026-10-14 退出 ChatGPT、ChatGPT 工作與 Codex，API 不受影響（頁上沒寫該換哪一個模型） | https://learn.chatgpt.com/docs/agent-configuration/speed |
| Codex 雲端：環境、每個任務有自己的工作區、在你電腦睡著時繼續（原句「Each task has its own workspace and can keep working while your computer is asleep.」） | https://learn.chatgpt.com/docs/cloud |
| dots：Pro、Business Premium、Enterprise（管理員啟用；含 Edu、Healthcare）、「向適用市場…陸續推出」「逐步開放給符合資格市場的 Pro 與 Business Premium 使用者」；第一個 dot 不另收費；對話不計入用量限制、Codex 與 ChatGPT 工作的任務照常計入（講的是額度，不是錢）；第一個月上限較高；主動研究唯讀；自訂規則允許／先核准／封鎖；改密碼一律本人；簡訊即將推出；4,000 個應用程式（OpenAI 自己的數字）；哪一階 Pro 起含 dot、台灣是否在符合資格的市場、Business Premium 價錢都沒寫 | https://openai.com/zh-Hant/index/introducing-dots/ |
| ChatGPT 空間：Pro、Business、Enterprise；網頁與桌面可建立編輯、行動版只能看；分享頁面不會分享私人對話與記憶，但頁上寫的都看得到；協作者各自的訓練設定套用在共用內容上；會議外掛程式 Beta 在 macOS 桌面應用程式、Pro 與 Business；空間頁第一段與「看看」段都寫「投影片（和試算表）的協作功能即將推出」，和回顧頁協作投影片「邀請多位團隊成員同時直接編輯」衝突，影片兩邊都說、以官網為準 | https://chatgpt.com/zh-Hant/features/space/ |
| Codex Security Cloud 的五步（安裝外掛程式、連 GitHub、一次性掃描、Fix with Codex 出草稿提取要求、持續掃描）；適用於所有 Codex 使用者（所以只算在所有人的九項，不算團隊的） | https://learn.chatgpt.com/docs/security/setup ；回顧頁 |
| 私密智慧：零資料保留搭配私密安全處理（ZDR with PSP）、私密推論預覽版；ZDR with PSP 是 API 專案層級、按專案開啟、組織要先取得 ZDR 核准；回顧頁只寫「讓企業」，沒綁任何 ChatGPT 方案 | https://developers.openai.com/api/docs/guides/private-safety-processing ；回顧頁 |
| Agents API 公開測試版、不另收費只付 token 與工具、沙箱合作夥伴九家；電腦操作是 DevDay 加的（回顧頁的「瞭解詳情」連到 vercel 預覽網址，不引用） | https://openai.com/zh-Hant/index/introducing-the-agents-api/ （2026-09-10） |
| MCP 事件：提議中的規格（Triggers and Events Working Group 章程頁，2026-10-03 回 200） | https://modelcontextprotocol.io/community/working-groups/triggers-events |
| 回顧頁「總計 12 億名使用者」、市集首批 32 家合作夥伴、「超過 20 項」 | 都是 OpenAI 自己在回顧頁的數字，引用時說「OpenAI 自己說」 |
| 上一支的月帳單數字（代理任務組合：Astra 約 $348、GPT‑6 Sol 約 $70；GPT‑6 Sol 快取輸入 $0.20） | docs/videos/gpt6-vs-opus55-worth-paying/claims.md（c8），撰稿時再對一次那支的 video.json |
| 沒抓到、影片只寫「以官網為準」：Decisions API 文件、Amazon Bedrock Managed Agents 頁、Codex CLI 版本說明、OpenAI 市集頁、Plus 的月費、Business Premium 的價錢、Sol 評測分數以外的任何第三方數字 | 回顧頁的「瞭解詳情」無連結，或連到 vercel 預覽網址（不引用） |

## 素材

- 官方頁原文（協調者 2026-10-03 抓取）：`_tools/sources/` 全部檔案；每個數字旁邊的網址就是上表的網址。沒有站內文章，所以沒有 `cta` 場景；dots 指向上一支 `always-on-agent-explained`，讀價目表的方法指向 `ai-price-war-gpt-6-sol-vs-opus-5-5`，每月帳單（Astra 約 $348、GPT‑6 Sol 約 $70）指向 `gpt6-vs-opus55-worth-paying`，US$20 買到什麼指向 `free-vs-paid-ai-plans-2026`（口播只說「上一支」「另一支」，說明欄放連結）。
- 實算：Ultrafast 的三種倍數都是官方頁直接寫的（牌價 ×6 是 pricing 頁 Ultrafast 表對標準表的每一欄；額度 8 份、點數 6 倍、Fast 2.5 份／2 倍是 speed 頁與說明中心的原句）；`_tools/planner-B/calc.mjs` 那組「一趟任務三個模型各多少錢」（$24／$4.40／$144）不再用，因為上一支已經算過同一組 token 的月帳單。
- `quote` 卡只放上述頁面的原句：Sol 頁「接近 Astra 的智慧，價格僅需五分之一」、dots 頁「你與 Dot 的對話不會計入 ChatGPT 的用量限制」與下一句（只有選項 C 用 quote 卡；A、B 改寫成 `big`「跟 dot 聊天不算額度，叫它在 Codex 或 ChatGPT 工作裡跑任務才算」）、Codex Cloud 頁「Each task has its own workspace and can keep working while your computer is asleep.」，標 OpenAI 與日期；中文原句沒有譯文，一次全出。
- 插圖：全部 AI 生成，`look` 交給工人輪替。選項 A、B 七個地點：火車站售票大廳（清晨／接近中午）、運動中心櫃台與更衣室（上午）、社區腳踏車修理店（中午）、共用陶藝工作室（下午）、餐廳廚房與後門（傍晚出餐）、夜市小吃街（晚上）、家裡的餐桌（深夜）；選項 C 七個地點：早餐店櫃台、傳統市場水果攤、小吃店結帳桌、火車月台、老公寓樓梯間與信箱牆、社區回收站、家裡餐桌。不畫字、logo、真人相貌、螢幕、筆電、手機、機器人、雲、燈泡、鐘面；會員卡只畫一塊剪影色塊與一條色帶（不畫小臉），白板上的單子是空白的，木牌與時刻牌不畫字，月票、車票、信封、收據都畫成沒有字的空白紙片。縮圖用「五個窗口的售票大廳」那個 shot（選項 C 用「三枚硬幣推過木檯面」）。
- 不用：產品截圖（介面會改，而且沒有授權）、各家 logo、vercel 預覽網址的內容、Sol 頁的評測圖表、回顧頁的客戶評語與「實驗室現場直播」影片、任何人的照片；登入流程全部用櫃台與鑰匙板的比喻畫。

## 不做的事

- 不解釋 dots 怎麼運作、怎麼失敗（上一支講過），只排它在 Pro 清單裡的位置和官方寫明的三條界線；不把 dots 說成今天登入就有（符合資格的市場逐步推出，台灣有沒有以官網為準）。
- 不重講怎麼讀同一個模型的八個價格（長脈絡、快取寫入、批次、Fast），指向「AI 價格戰」那一支；不算每月帳單，也不再算「一趟任務三個模型各多少錢」（「GPT-6 vs Opus 5.5 值不值得付」用同一組 token 算過，GPT‑6.1 Sol 只差快取價），只講 Ultrafast 三種付法的官方倍數。
- 不換算台幣；不引用 Sol 頁上的評測分數細節，最多一句「OpenAI 自己公布的評測說接近 Astra」；不講 Opus、Gemini 或任何對手。
- 不說任何一項「用起來怎樣」：站主沒有實測，影片不出現使用心得；登入五步是照說明頁讀的；示意比喻一律是比喻，不冒充畫面；速度倍數一律說是 OpenAI 的說法。
- 不給升級建議（不說「Pro 500 值得」或「不值得」，也不說「會等就該升 Pro 500」），不給換模型建議（GPT‑5.5 退場只說退場日與「改選一個還在的」，不說該換成哪一個），只給算法和官方的額度規則；不講投資、法律、醫療、選舉。
- 不談 OpenAI 的營收、估值、募資；不引用回顧頁的客戶評語與 Agents API 頁的客戶數字。
- 不引用回顧頁連到 vercel 預覽網址的兩份文件（電腦操作、外掛程式擴充功能），那兩項只用回顧頁的一段話（第 2 章點名時各一句）。
- 不猜 Plus 的月費、Business Premium 的價錢、Decisions API 的價格、Bedrock 的細節、Codex CLI 的版本號、各階 Pro 的額度數字、台灣是否在 dots 的符合資格市場；查不到就「以官網為準」。
- 第 1 章不放目錄卡；旁白不唸網址、不唸 `service_tier` 這類程式字串（放卡片）；不出現「經查證」「根據官方文件」。
