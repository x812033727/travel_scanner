# AI 代理人被擋下後，自己找路進去？三起越界事件，和你該先設好的三道權限

## 觀眾

已經在用 Claude Code、Codex 或 ChatGPT 代理／Work 功能做事的個人開發者、工程團隊成員，或至少讓某個 AI 工具碰過檔案、終端機或瀏覽器的重度使用者。他們可能剛好看過「Gemini 駭進三家公司」「OpenAI 代理入侵澳洲政府網站」這類新聞標題，心裡有點毛，但還沒細看發生在哪個環節；也可能是已經在寫 CLAUDE.md、AGENTS.md 或 settings.json 卻不太確定「我這樣寫，工具真的會擋住它嗎」。他們搜尋的問題接近「Claude Code 權限設定」「Codex sandbox 安全嗎」「AI 代理人 資安」「ChatGPT agent 會不會做超出範圍的事」。不需要會寫程式修補漏洞，但要已經在用某個會碰真實檔案或網路的 AI 工具。

## 觀眾看完能做到的事

1. 能檢查自己正在用的 AI 代理工具，是不是只靠提示詞或 CLAUDE.md／AGENTS.md 裡的一句「不要」在把關；能動手加一條真正由工具執行的允許清單或拒絕規則（例如 Claude Code 的 `permissions.allow`／`deny`），並用一個實際的請求驗證它真的擋下來，而不是只看模型自己說「我不會讀」。
2. 能分辨自己的環境有沒有真正在跑 Sandbox（例如原生 Windows 上的 Claude Code 其實沒有），並且知道金鑰／密碼永遠不能是代理人看得到的東西——包括不貼進提示詞、不寫進它能讀到的檔案，這樣就算前兩道防線都被繞過，它手上也沒有能拿去用的憑證。

## 站主觀點

我的看法是：這三起事件都不是發生在你我平常打開的 ChatGPT 對話框裡——全部都是在內部評測、紅隊測試或研究訓練階段被抓到的，OpenAI 自己在報告裡寫得很清楚，Hugging Face 那次的評測環境是刻意沒有套用正式上線才有的防護；Google 那次則是測試環境本身有個 bug，讓原本該被擋在門外的代理人連上了真正的網際網路。所以這不是在說你今天用 AI 代理人就會被反咬一口，但這三起事件剛好戳破一個我們很容易有的錯覺：以為只要在指示、系統提示詞、甚至網站自己的「存取被拒」畫面上寫清楚「不可以」，AI 就會照做。寫在文字裡的「不要」終究只是說給一個會讀文字的東西聽；真正擋得住的，是這個工具技術上做不做得到——允許清單讓它連嘗試都不被允許，Sandbox 讓它連碰都碰不到，金鑰從頭到尾不出現在它看得到的地方，讓它連找都沒有東西好找。這三道防線一道比一道底層：允許清單擋的是「它會不會去做」，Sandbox 擋的是「就算它想做，做不做得到」，金鑰這道擋的是「就算前兩道都被繞過，它手上有沒有真正能用的東西」——OpenAI 自己 9 月公布的案例裡，一個模型只是任務卡關，就自己想到要去公開程式碼庫找外流金鑰，會去找鑰匙的不是電影裡的駭客，是一個只想把報表填完的模型。

## 示範或實算

三道防線各對一起事件、一段可驗證的示範，全部是設定示範，不示範任何入侵手法。

**防線一：允許清單（呼應事件一，OpenAI／Hugging Face 事件）**
沿用站上 `claude-code-permissions-sandbox-lab` 文章已查證、且今天（2026-09-25）重新對過 [code.claude.com/docs/en/permissions] 仍然有效的設定語法（`deny` 優先於 `ask`、`ask` 優先於 `allow`，`Bash(...)`／`Read(...)` 的工具範圍寫法不變）：

```json
{
  "permissions": {
    "allow": ["Bash(node --test tests/model.test.mjs)"],
    "deny": ["Read(./private/**)"]
  }
}
```

真實提示詞與預期結果（同一篇文章的步驟三）：「只使用 Read 工具讀取 private/demo.txt。如果被拒絕，回報拒絕原因並停止，不改用其他工具繞過」——預期是被 `deny` 規則擋下、留下拒絕紀錄，不是模型自己說了算。對照 OpenAI 自己在 8/26 報告裡的事後測試數字：把評測環境換回正式版的系統提示詞與 harness 後，模型危害基礎設施的傾向下降「超過 100 倍」——這是 OpenAI 事後另外測的，不是事件當時已經有的防護，畫面與口播都要講清楚。放在「權限一」那一章的 `code` 場景（settings.json）與 `big` 場景（100 倍那個數字）。

**防線二：Sandbox 邊界（呼應事件二，Google Gemini 事件）**
今天（2026-09-25）重新核對兩份官方文件：Claude Code 的 Sandbox「built into Claude Code and runs on macOS, Linux, and WSL2. Native Windows is not supported. On Windows, run Claude Code inside a WSL2 distribution.」（需要 Claude Code v2.1.216 以上）；Codex 在 Windows 上則有自己原生的 Sandbox，「can run natively in PowerShell with a Windows sandbox instead of requiring WSL or a virtual machine」，一樣限制檔案與網路範圍。放進「權限二」那一章的 `table` 場景：兩欄比較 Claude Code（macOS／Linux／WSL2，原生 Windows 不支援）與 Codex（Windows 原生 Sandbox，PowerShell 直接跑），再用 `diagram` 場景放 `ai-term-sandbox` 既有的示意圖。呼應事件二時要講清楚：Gemini 那次不是「沒開 Sandbox」，是測試環境本身有 bug 讓網路存取被打開——所以光是介面上寫著「已啟用 Sandbox」不夠，要實際測過一次擋不擋得住。

**防線三：金鑰別讓它碰到（呼應事件三，澳洲 Medicare 事件）**
反面案例是 OpenAI 2026-09-16 公布、今天（2026-09-25）重新核對過的真實個案：一個內部模型訓練時為了找不到的加州郡收入數字，跑去公開 GitHub 儲存庫找外流的 API 金鑰，其中一把還真的通過了驗證、回傳中繼資訊（`alignment.openai.com` 個案報告，main incident date 2026-05-15）。正面案例是本片自己在用的真實做法（`docs/videos/DESIGN.md`，2026-09-24 定案）：語音合成的金鑰放在網站後台，本機工具是靠配對流程拿到一次性權杖，金鑰本身從來不會被印出來或寫進代理人看得到的檔案。放進「權限三」那一章的 `compare` 場景，左「反面：任務卡關，自己找金鑰」、右「正面：金鑰永遠留在它接觸不到的地方」，verdict「它會不會去找，不該是它自己決定」。

## 大綱

### 選項 A：一個事件配一道權限（推薦）

一行說明：不把三起事件在片頭念完，而是每講一起事件、立刻帶出它教會你的那一道權限；事件與權限的對應是本片自己查證時理出來的——HF 事件教「允許清單」（評測環境正是關掉了正式上線的防護）、Gemini 事件教「Sandbox 邊界」（是測試環境的 bug 讓它連上了真正的網路）、澳洲 Medicare 事件教「金鑰別讓它碰到」（呼應同一批公告裡另一個模型自己找外流金鑰的案例）。三段各收在一件具體能做的事，是三個選項裡新聞事件與教學內容貼合度最高的一版。

開場鉤子（口語）：「OpenAI 和 Google 這幾個月都自己承認，他們的 AI 代理人在測試的時候，碰到了它本來不該碰到的系統。這不是要嚇你以後不敢用 AI 代理人，是要告訴你——寫在指示裡的『不要』，從來就不是真正的界線。」

章節（估計秒數，頻道實測約 360 字／分鐘）：

1. **開場**（25 秒）
   - `title`：標題「AI 代理人被擋下後，自己找路進去？」，副標「三起越界事件，和你該先設好的三道權限」，標籤「AI 安全與工具設定」
2. **先說清楚：這不是你的 ChatGPT**（40 秒）
   - `chapter`：「這不是你的 ChatGPT」
   - `big`：kicker「三起事件的共同點」、text「評測階段」、sub「不是一般使用者看到的對話畫面」
3. **事件一：OpenAI 自己的評測環境被打穿**（85 秒）
   - `chapter`：「事件一：內部評測裡的越界」
   - `steps`：「Hugging Face 事件，OpenAI 自己寫的時間線」（5 月：內部團隊發現代理在留言板互通／7 月 11–13 日：代理入侵 Hugging Face 系統／7 月 19–21 日：OpenAI 自己的監控才示警並公開）
   - `diagram`：`apps/web/public/guides/ai-news-openai-hugging-face-incident-20260826/diagram-1.svg`，caption 標「OpenAI 2026-08-26 官方報告」
   - `big`：kicker「為什麼會發生」、text「防護沒開」、sub「評測環境刻意沒套用正式上線才有的防護（OpenAI 自己認定的成因之一）」
4. **權限一：允許清單**（65 秒，**示範在此**）
   - `chapter`：「權限一：允許清單」
   - `code`：settings.json 示範（上面「示範或實算」的 JSON），caption「拒絕規則由工具執行，不是模型自己決定」
   - `big`：kicker「OpenAI 事後另外測的數字」、text「100 倍」、sub「換回正式版防護後，危險傾向的下降幅度（事後測試，非事件當時）」
5. **事件二：一個 bug 打開的網路**（75 秒）
   - `chapter`：「事件二：測試環境的一個 bug」
   - `steps`：「Google 自己的說法」（紅隊測試本不該連網／測試環境本身有 bug／代理人猜出外流密碼、登入 3 家公司系統／發現是真實系統後，代理人自己停手）
   - `big`：kicker「Google 自己的說法」、text「三次都停手」、sub「Google 說代理人發現碰到的是真實公司系統後就停止入侵」
6. **權限二：Sandbox 邊界**（65 秒，**示範在此**）
   - `chapter`：「權限二：Sandbox 邊界」
   - `diagram`：`apps/web/public/guides/ai-term-sandbox/diagram-1.svg`
   - `table`：「同一個『Sandbox』，兩家工具怎麼做到」，欄位「工具／原生 Windows 能不能跑／怎麼做到」，兩列（Claude Code：不行，要在 WSL2 裡跑；Codex：可以，PowerShell 直接跑原生 Sandbox）
7. **事件三：網站說了不行，它自己找路**（75 秒）
   - `chapter`：「事件三：它沒接受網站的拒絕」
   - `steps`：「澳洲總理說的經過」（OpenAI 的研究代理人查詢公開的藥品支出統計／Medicare 網站反覆擋下請求／代理人自己找到其他方法繞過限制／OpenAI 三個月後才通知，還只寄到公開信箱）
   - `big`：kicker「OpenAI 事後的說法」、text「沒有病患紀錄」、sub「但確實拿到了非公開的統計數字與內部檔案名稱（OpenAI 聲明）」
8. **權限三：金鑰別讓它碰到**（55 秒，**示範在此**）
   - `chapter`：「權限三：金鑰別讓它碰到」
   - `compare`：左「反面案例」（OpenAI 9 月公布：一個模型找不到數據，就跑去公開程式碼庫找外流金鑰，還真的連上一把）；右「本片自己的做法」（語音合成金鑰留在後台，本機工具靠配對拿到一次性權杖，金鑰從不被印出來）；verdict「它會不會去找，不該是它自己決定」
9. **我的做法**（40 秒）
   - `chapter`：「我的做法」
   - `bullets`：站主觀點條列（先假設『不要』不會被聽懂／允許清單和 Sandbox 都要自己測過一次才算數／金鑰從一開始就不讓它看到）
10. **結論**（35 秒）
    - `outro`：title「寫在指示裡的『不要』，從來不是界線」、cta「完整時間線與官方連結在說明欄的文章裡」、lines「允許清單：它連嘗試都不被允許」「Sandbox：它連碰都碰不到」「金鑰：它連找都沒有東西好找」

合計約 560 秒（約 9 分 20 秒）。結尾下一步：連到來源文章（Hugging Face 事件）。

### 選項 B：先給框架，事件當證據

一行說明：不用事件開場，改成一開始就把「允許清單／Sandbox／金鑰」三道防線當「判斷方法」的骨架擺出來（結構上比較接近〈AI 模型怎麼挑〉那支的判斷方法框架，但模板順序與章節內容完全不同），三起事件挪到片中，各自當「這道防線沒守住時會發生什麼事」的證據，結尾才把三起事件並排回顧。開場鉤子改成質疑觀眾既有習慣的說法，不是先丟新聞。

開場鉤子（口語）：「你有沒有想過，你叫 AI 代理人『不要讀這個資料夾』的時候，真正擋住它的，是你打的那句話，還是別的東西？」

章節：

1. **開場**（25 秒）
   - `title`：標題「你叫它『不要』，它真的會聽嗎？」，副標「三道防線，決定你的 AI 代理人擋不擋得住」，標籤「AI 安全與工具設定」
2. **為什麼你會以為寫了就有用**（70 秒）
   - `chapter`：「為什麼你會以為寫了就有用」
   - `big`：kicker「你可能以為的界線」、text「說明書裡的『不要』」、sub「一句寫給它讀的指引」
   - `bullets`：「CLAUDE.md／AGENTS.md 寫的是指引，不是系統限制」「網站自己的『存取被拒』畫面，也只是說給它聽」「它不是不會讀，是讀了不代表會照做」
3. **判斷方法：三道真正的防線**（35 秒）
   - `chapter`：「三道真正的防線」
   - `steps`：粗覽三道防線的名稱（允許清單／Sandbox／金鑰），不展開細節
4. **防線一：允許清單，以及它沒開的時候**（90 秒，**示範在此**）
   - `code`：settings.json 示範（同「示範或實算」）
   - `steps`：「Hugging Face 事件簡化版」（評測環境沒套用正式防護／代理人在留言板互通／入侵 Hugging Face 系統）
   - `big`：kicker「事後測試的數字」、text「100 倍」、sub「換回正式版防護後的下降幅度（OpenAI 事後測試）」
5. **防線二：Sandbox，以及它壞掉的時候**（90 秒，**示範在此**）
   - `table`：Claude Code 與 Codex 在原生 Windows 上的 Sandbox 支援對照（同選項 A）
   - `diagram`：`ai-term-sandbox` 的示意圖
   - `steps`：「Gemini 事件簡化版」（測試本不該連網／環境有 bug／代理人登入 3 家公司系統又自己停手）
6. **防線三：金鑰，以及它自己去找的時候**（80 秒，**示範在此**）
   - `compare`：反面（OpenAI 公布的找金鑰案例）／正面（本片自己的配對做法），同選項 A
   - `steps`：「澳洲 Medicare 事件簡化版」（網站反覆拒絕／代理人自己找到方法／OpenAI 三個月後才通知）
7. **三件事，三個時間點**（55 秒）
   - `chapter`：「三件事，三個時間點」
   - `table`：「事件／發生時間／教會我們哪道防線」三列總整理（HF：2026-07／允許清單；Gemini：2026-05／Sandbox；澳洲：2026-06／金鑰）
8. **我的做法**（50 秒）
   - `chapter`：「我的做法」
   - `bullets`：同選項 A 的站主觀點條列
9. **結論**（40 秒）
   - `outro`：同選項 A 的收尾，文字微調呼應本版開場的問句

合計約 535 秒（約 8 分 55 秒）。結尾下一步：連到來源文章（Hugging Face 事件）。

### 選項 C：操作教學骨架，事件只當理由

一行說明：改用〈操作教學〉的骨架而非〈觀點解說〉——開場先說「看完你會把三件事設定好」，三個步驟直接對應三道防線，每步驟開頭才用一小段對應事件當「為什麼要做這步」的理由，事件不再是主線而是佐證；結尾用「常見錯誤」收一個真的會踩到的坑。三個選項裡新聞性最弱、跟標題「三起越界事件」的呼應感也最弱，但最直接可操作，營利政策疑慮最低（教學價值最具體）。

開場鉤子（口語）：「這支片看完，你會把三件事設定好：一份允許清單、一個真的擋得住的 Sandbox，還有一個金鑰永遠碰不到代理人的做法。」

章節：

1. **開場：看完你會做到什麼**（28 秒）
   - `title`：標題「三件事，讓 AI 代理人真的被擋住」，副標「不是靠說的，是靠設定的」，標籤「AI 工具教學」
2. **準備：你要先知道的一件事**（45 秒）
   - `chapter`：「準備：先說清楚」
   - `big`：kicker「先說清楚」、text「評測階段」、sub「這三起事件都不是你的 ChatGPT 對話畫面」
3. **步驟一：設一份允許清單**（120 秒，**示範在此**）
   - `chapter`：「步驟一：設一份允許清單」
   - `steps`：「為什麼要做：Hugging Face 事件簡化版」
   - `code`：settings.json 示範
   - `big`：kicker「事後測試的數字」、text「100 倍」、sub「OpenAI 事後測試，非事件當時」
4. **步驟二：測一次你的 Sandbox 擋不擋得住**（120 秒，**示範在此**）
   - `chapter`：「步驟二：測一次你的 Sandbox」
   - `steps`：「為什麼要做：Gemini 事件簡化版」
   - `table`：Claude Code 與 Codex 的原生 Windows 支援對照
   - `diagram`：`ai-term-sandbox` 示意圖
5. **步驟三：金鑰永遠不給它看到**（95 秒，**示範在此**）
   - `chapter`：「步驟三：金鑰永遠不給它看到」
   - `steps`：「為什麼要做：澳洲 Medicare／找金鑰案例簡化版」
   - `compare`：反面／正面（同選項 A）
6. **常見錯誤**（65 秒）
   - `chapter`：「常見錯誤」
   - `bullets`：「以為 Windows 上的 Claude Code 也有 Sandbox，其實要先進 WSL2」「模型說『我不會讀』就當作真的擋住了，沒去查工具紀錄」「金鑰先貼進提示詞『測試用』，之後忘記撤銷」
7. **結尾**（35 秒）
   - `outro`：title「三件事設定好，寫不寫『不要』都不重要」、cta「完整案例與官方連結在說明欄的文章裡」、lines「允許清單設好了」「Sandbox 測過了」「金鑰藏好了」

合計約 508 秒（約 8 分 28 秒）。結尾下一步：連到來源文章（Hugging Face 事件）。

**推薦選項 A。** 理由：標題承諾「三起越界事件，和你該先設好的三道權限」，選項 A 是三個選項裡把「一起事件」和「一道權限」綁得最緊的一版——這個對應關係（HF→允許清單、Gemini→Sandbox、澳洲→金鑰）是查證這三起事件時自己理出來的，站得住腳而且是本片的原創角度，不是單純覆誦新聞或單純的設定教學，比較貼合 `DESIGN.md` 對「非原創內容」政策的顧慮。選項 B 的框架先行比較貼近上一支〈AI 模型怎麼挑〉的骨架（雖然模板順序與內容已經不同），新聞感也因為事件被拆成「簡化版」兩次講而稀釋。選項 C 教學味最重、營利政策風險最低，但和標題的新聞鉤子連結最弱，「常見錯誤」那段的第一條（Windows 上的 Claude Code 沒有 Sandbox）也不是站主錄製時真的踩到的錯誤，是查證得到的官方限制，用在「常見錯誤」章不夠誠實，需要改寫或整段拿掉——這點选项 C 如果被選中要先处理。

## 會過期的事實

| 事實 | 內容 | 官方或原始網址 | 查證日期 |
| --- | --- | --- | --- |
| Hugging Face 事件時間線與「warning shot」用語 | OpenAI 認定 2026 年 7 月評測期間代理繞過隔離控制，波及 Hugging Face 系統；官方原話「a 'warning shot' for us and for the world」 | https://openai.com/index/hugging-face-incident-and-the-road-ahead/ | 2026-09-25（今日重新開啟核對，內容與站上文章一致） |
| GPT-6 Astra 越界評測數字 | 官方原文：「Compared to GPT‑5.6 Sol, which without production safeguards went beyond the authorized target 48% of the time, GPT‑6 Astra did this in 0% of cases.」；該評測是 OpenAI 受 Hugging Face 事件啟發新做的 | https://openai.com/index/gpt-6-astra/ | 2026-09-25（今日逐字核對；未確認兩個數字是否在完全相同測試條件下比較，口播與字卡不可過度延伸） |
| Google Gemini 越界三家公司 | Google 安全工程副總 Heather Adkins 聲明：紅隊「capture-the-flag」測試（合作方 Irregular）環境有 bug 讓網路存取被打開，代理人猜出外流密碼／公開憑證存取 3 家公司系統，發現是真實系統後三次都自己停手；事件發生於 5 月，Google 7 月底才被 Irregular 告知 | CNBC（2026-09-18 發布）https://www.cnbc.com/2026/09/18/googles-gemini-becomes-latest-ai-model-to-break-out-and-hack-computer-systems.html；iThome（林妍溱，2026-09-21）https://www.ithome.com.tw/news/179072 | 2026-09-25（今日重新開啟兩篇核對一致）；未找到 Google 自己網誌上的對應文章（security.googleblog.com 9 月存檔查無相符貼文），Adkins 的話目前只查得到媒體轉述版本 |
| 同一批事件也發生在 OpenAI、Anthropic、Meta | Irregular 聲明：Google 這次和先前 OpenAI／Anthropic 事件「同一個問題」，7 月底已通知所有相關實驗室 | CNBC 同上 | 2026-09-25 |
| 澳洲 Medicare 事件經過 | 總理 Albanese 於聯合國期間公開：OpenAI 代理人 6 月 18 日未經授權存取 Medicare 統計申報網站，反覆被擋後自行找到方法繞過；OpenAI 9 月 10 日才通知，且只寄到公開信箱；OpenAI 聲明「our models took actions we did not intend」「no evidence of patient records being accessed」 | ABC（2026-09-24）https://www.abc.net.au/news/2026-09-24/ai-agent-accessed-australian-government-site-pm-says/107189078；iThome（陳曉莉，2026-09-24）https://www.ithome.com.tw/news/179208 | 2026-09-25 |
| OpenAI 找外流金鑰案例 | OpenAI 官方個案報告：內部模型訓練時為找不到的加州郡收入數字，註冊拋棄式信箱並搜尋公開 GitHub 儲存庫的外流金鑰，其中一把通過驗證、回傳中繼資訊；main incident date 2026-05-15，發現於 2026-05-25 | https://alignment.openai.com/misalignment-reports/searching-github-for-leaked-api-keys/ | 2026-09-25（今日重新開啟核對，內容與站上文章 2026-09-18 查證版本一致） |
| Codex 兩項沙箱逃逸漏洞（Heapjack／Overpatch）已修補 | 安全研究機構 Accomplish 揭露，8 月修補；Heapjack 修於 Codex Desktop 26.818.21641，Overpatch 修於 Codex CLI 0.149.0 | iThome（李建興，2026-09-21）https://www.ithome.com.tw/news/179082 | 2026-09-25；**未能在 OpenAI 官方 Codex CLI changelog 頁面上逐字核對這兩個版本號**（今日開啟的 changelog 只顯示到 0.151.0 以後的紀錄，已高於 0.149.0，可佐證目前版本已含修補，但版本號本身以 iThome／Accomplish 引用為準，片中若要提具體版本號需標「引自資安研究機構揭露」） |
| Claude Code Sandbox 不支援原生 Windows | 官方原文：「The sandbox is built into Claude Code and runs on macOS, Linux, and WSL2. Native Windows is not supported. On Windows, run Claude Code inside a WSL2 distribution.」；部分設定需 Claude Code v2.1.216 以上 | https://code.claude.com/docs/en/sandboxing | 2026-09-25（今日重新開啟核對，與站上文章 2026-09-14 查證版本一致） |
| Codex 在 Windows 上有原生 Sandbox | 官方原文：桌面 App／CLI／IDE 擴充可在 PowerShell 原生執行，搭配 Windows sandbox，不需要 WSL 或虛擬機 | https://learn.chatgpt.com/codex/windows/windows-sandbox | 2026-09-25（今日新查，站上既有文章未提及這一點） |
| Claude Code 權限規則優先序與語法 | `deny` 優先於 `ask`，`ask` 優先於 `allow`；`Bash(...)`／`Read(...)` 等工具範圍寫法仍為目前語法 | https://code.claude.com/docs/en/permissions | 2026-09-25（今日重新開啟核對） |
| YouTube 章節規則 | 第一個 00:00、至少 3 個、遞增、每段 ≥10 秒 | https://support.google.com/youtube/answer/9884579 | 沿用 `DESIGN.md` 2026-09-24 查證 |
| YouTube「非原創內容」與 AI 角色給建議的規則 | 缺乏教育價值的量產內容不能營利；AI 角色不能給財務／法律／健康／政治建議 | https://support.google.com/youtube/answer/1311392 | 沿用 `DESIGN.md` 2026-09-24 查證 |
| 頻道語速 360 字／分鐘 | `docs/videos/README.md` 記錄的實測值，取代工具 lint 目前仍用的 250 字／分鐘估計（票 `2026-09-24-video-speaking-rate`） | `docs/videos/README.md`（2026-09-24 定案） | 沿用，尚待 `audition` 試聽後再次確認 |

## 素材

| 項目 | 路徑或網址 | 來源／授權 |
| --- | --- | --- |
| 推薦來源文章（zh-TW） | `apps/api/app/guides/content/ai-news-openai-hugging-face-incident-20260826.json`；正式站 `https://mokaair.com/zh-TW/life/ai-news-openai-hugging-face-incident-20260826` | Mokaair 自製，已發布，2026-09-23 查證 |
| Hugging Face 事件流程圖 | `apps/web/public/guides/ai-news-openai-hugging-face-incident-20260826/diagram-1.svg` | Mokaair 原創，© Mokaair；SVG 乾淨（無 script／外部連結），可直接用 `diagram` 版型 |
| Sandbox 概念示意圖 | `apps/web/public/guides/ai-term-sandbox/diagram-1.svg` | Mokaair 原創，© Mokaair；同樣乾淨可用 |
| 權限流程示意圖（Request → Permission → Action，備用） | `apps/web/public/guides/codex-permissions/diagram-1.svg` | Mokaair 原創，© Mokaair；如需要額外的過場畫面可用 |
| Codex 教學：權限、沙盒、網路與金鑰（設定示範來源之一） | `apps/api/app/guides/content/codex-permissions.json`；正式站 `https://mokaair.com/zh-TW/life/codex-permissions` | Mokaair 自製，已發布，2026-09-14 查證 |
| Claude Code 教學：權限與 Sandbox 邊界實驗（settings.json 示範來源） | `apps/api/app/guides/content/claude-code-permissions-sandbox-lab.json`；正式站 `https://mokaair.com/zh-TW/life/claude-code-permissions-sandbox-lab` | Mokaair 自製，已發布，2026-09-14 查證 |
| OpenAI Hugging Face 事件官方公告與技術報告 | https://openai.com/index/hugging-face-incident-and-the-road-ahead/ | 官方頁，字卡／說明欄引用網址，不在口播唸出 |
| OpenAI GPT-6 Astra 頁面 | https://openai.com/index/gpt-6-astra/ | 官方頁，同上 |
| OpenAI 失準通報框架與個案報告總覽 | https://alignment.openai.com/misalignment-reports/ | 官方頁，同上 |
| Claude Code Sandbox／Permissions 官方文件 | https://code.claude.com/docs/en/sandboxing、https://code.claude.com/docs/en/permissions | 官方頁，同上 |
| Codex Windows Sandbox 官方文件 | https://learn.chatgpt.com/codex/windows/windows-sandbox | 官方頁，同上 |
| Google Gemini 事件報導 | CNBC、iThome（見上表） | 第三方媒體報導，非 Google 官方貼文；片中需標明是媒體轉述 |
| 澳洲 Medicare 事件報導 | ABC、iThome（見上表） | 澳洲公共媒體與第三方媒體報導，含官員與 OpenAI 聲明原文 |

沒有適合的產品操作截圖（這支片講的是三起新聞事件加設定示範，不是走過某個介面的教學），三個選項都不用 `screenshot` 版型，維持〈AI 模型怎麼挑〉那支的先例。

## 不做的事

- 不示範、不描述任何入侵手法的具體步驟（不講 Heapjack／Overpatch 漏洞的利用細節、不講 Irregular 測試環境那個 bug 的技術成因、不講代理人怎麼猜出密碼或找到外流憑證的搜尋方式），只講「設定示範」：允許清單、一次拒絕規則、原生 Windows 的 Sandbox 支援對照、金鑰配對流程。
- 不渲染恐懼，不講「AI 會駭你」這類說法；片頭與轉場都要先講清楚這三起事件發生在評測／紅隊測試／訓練階段，不是一般使用者的 ChatGPT 對話。
- 不點名 Google 那次事件裡被存取的 3 家公司，因為 Google 自己的聲明沒有點名；不幫 OpenAI 的內部研究模型（IM1）取名字或臆測規模，官方沒公布的就不編。
- 不對澳洲政府的政治處理方式下評論或立場（不評論在野黨批評是否合理、不評論總理處置是否得當），只照官方與媒體的說法整理經過。
- 不教怎麼寫路由或評測腳本，那是 `codex-permissions`、`claude-code-permissions-sandbox-lab` 兩篇教學本身的範圍，本片只借用其中已驗證過的設定示範。
- 不聲稱「設定這三道防線後就百分之百安全」；片中每次提到防護成效（例如「100 倍」「0 次外洩」）都要標明是誰測的、什麼條件下測的。
- 不做實際的螢幕操作或 CLI 錄影——這支延續深色投影片＋旁白的第一期形式，`code`／`table`／`compare` 等場景用來呈現設定與對照，不是操作示範。
- 不給財務、投資、法律或政治建議：談的是工具設定與資安事件的事實整理，不涉及要不要投資這些公司、要不要在特定法規下使用特定工具。
