# artex-ai-attack-leftover-keys：查核第 2 輪（verify-2）

查核日期 2026-10-27。查核者是第三個獨立代理，既不是撰稿者，也沒做第 1 輪。每一頁都是今天自己用
`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重抓的，同一網域兩次之間至少隔 1.5 秒，去掉 `<!-- -->` 之後才讀。
抓下來的頁面放在工作區 `artex-ai-attack-leftover-keys/dl-verify2/`，跟腳本分開放；輔助腳本在 `_tools/verify2/`：
`fetch.py`、`urls.tsv`、`http-status.tsv`、`totext.py`、`rerun.sh`、`cmpcards.py`、`listener.py`、`draw.py`。
網頁搜尋用了 1 次，查 91APP 有沒有發布「下週」那份更新，結果沒找到。

範圍：
（A）verify-1 判成 CHANGED 的 7 列；
（B）撰稿者在 verify-1 之後改的地方（claims.md〈進度〉第一條），加上 c33；
（C）verify-1 判成 CONFIRMED 的各列中，用固定種子隨機抽三分之一。

## 來源與 HTTP 狀態（2026-10-27 抓取）

| 代號 | URL | HTTP | 備註 |
| --- | --- | --- | --- |
| MS | https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/ | 200 | datePublished 2026-10-21T18:23:55Z；dateModified 2026-10-26T16:32:11Z。純文字跟撰稿者 10-27 存的 `sources-20261027/msft` 完全相同 |
| 91N | https://91app.com/blog/91app-202610-security-incident/ | 200 | datePublished 2026-10-22T10:29:52Z，dateModified 2026-10-22T10:47:43Z |
| 91R | https://91app.com/91app-202610-security-incident/ | 200 | 頁面仍寫「資料更新日期 10/22」 |
| MODA | https://moda.gov.tw/ACS/press/news/press/21130 | 200 | 發稿日期 115 年 10 月 21 日 |
| IT65 | https://www.ithome.com.tw/news/179865 | 200 | 媒體，2026-10-21 |
| IT50 | https://www.ithome.com.tw/news/179850 | 200 | 媒體，2026-10-21 |
| IT23 | https://www.ithome.com.tw/news/179923 | 200 | 媒體，2026-10-23 |
| IT04 | https://www.ithome.com.tw/news/179804 | 200 | 媒體，2026-10-20，只拿來對「台灣的 Zeabur」 |
| SNS | https://scan.netsecurity.ne.jp/article/2026/10/21/56522.html | 200 | 媒體，2026-10-21 |
| GMO | https://gmo-cybersecurity.com/blog/20261019/ | 200（轉址到首頁） | 網站仍是暫時的簡易版，一手部落格今天還是讀不到 |
| ZB | https://zeabur.com/zh-TW/blogs/october-2026-security-incident | 200 | date 2026-10-19，全文時間是 UTC |
| CW | https://status.connectwise.com/pages/incident/619cf82551fec9053d612f09/6ad263692dc48705ab3da2cb | 200 | 10-16 那一則沒變；後面多了 10-18 的更新 |
| GPW | https://support.google.com/accounts/answer/41078?hl=zh-Hant | 200 | |
| G3P | https://support.google.com/accounts/answer/13533235?hl=zh-Hant | 200 | |
| GHS | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository | 200 | |
| GHO | https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/reviewing-your-authorized-oauth-apps | 200 | |
| MSL | https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity | 200 | |
| GITLOG | https://git-scm.com/docs/git-log | 200 | |
| RUN | 本機在新的空目錄重跑 `_tools/run/run.sh`（見〈示範重跑〉） | — | |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | 說明欄寫「ARTEX 攻擊全球幾百個組織」，已經沒有「同時」（verify-1 #4） | youtube.description | MS | 200 | CONFIRMED（"As early as September 2026 … to automate attacks targeting hundreds of organizations globally"） | — |
| A2 | 標題「它不靠猜密碼」、開場卡「AI 駭客不靠猜密碼」（verify-1 #6） | youtube.title；open.data.title | MS | 200 | CONFIRMED，當作定調的說法成立：Microsoft 寫 ARTEX 加速了 "password spraying, and OAuth application abuse"；有紀錄的那一波噴灑 "no successful authentication"；進去的路是 "applications that had already been granted access"。見〈懷疑〉 | — |
| A3 | 3zwr「同一天，署長還補了一個觀察」；kicker「資安署署長，iThome 報導」；說明欄「照 iThome 同日的報導」（verify-1 #26） | cheap/3zwr；cheap.data.kicker；description | IT65、MODA | 200 | CONFIRMED（iThome 寫「資安署今天(10/21)」與「蔡福隆透露」；兩頁都沒有「記者會」三個字） | — |
| A4 | 10/16「ConnectWise 公告備份服務遭入侵嘗試」；vwab「公告有人試圖入侵它的備份服務」；說明欄（verify-1 #32） | timeline.rows[2]、keys[2]；timeline/vwab；description | CW、MS | 200 | CONFIRMED（"October 16, 2026 5:48PM UTC … investigating recent attempts of unauthorized access associated with the ConnectWise Cloud Backup environment … no indication that partner backup data has been accessed"；MS 寫 "attempted unauthorized access"） | — |
| A5 | 說明欄「該報告沒有提到 ARTEX，也沒說攻擊者用了 AI 工具」（verify-1 #42） | youtube.description | ZB | 200 | CONFIRMED（HTML 與純文字裡 ARTEX 都是 0 次；報告提到 AI 的地方，只有攻擊者在找 AI 服務的金鑰、試圖呼叫 Amazon Bedrock，是攻擊的目標，不是使用的工具） | — |
| A6 | ei35「但例外之一，是你已經授權存取帳戶的那些第三方應用程式」；key「例外之一：…」（verify-1 #49） | google/ei35；google.data.keys[1]；google.data.quote | GPW | 200 | CONFIRMED（頁面列了三項例外；卡片引文跟原文逐字相符） | — |
| A7 | nq6x「就是目前分支的歷史裡沒有這個字」；caption 同義（verify-1 #56） | your-line/nq6x；your-line.data.caption | GITLOG、RUN | 200 | CONFIRMED（沒給範圍時 "it defaults to HEAD (i.e. the whole history leading to the current commit)"；重跑 `-G API_KEY` 沒有任何輸出） | — |
| B1 | 示範：四張終端機卡（`ls -A`、grep 那一行、`git log --oneline -G PASSWORD`、`git show a6036e8:.env`），提交編號 a6036e8／5f37a2a，ls 9.4、grep 3.11、git 2.43.0、Ubuntu 24.04.5 LTS，ran_on 2026-10-27；說明欄的三行指令；r1–r5 | ls、grep、gitlog、gitshow 的 data；9c5b、7iw4、yzmt、tpcz、hvxy、qyg2、tzyy、a497、5uez；description | RUN | — | CONFIRMED：四張卡的輸出跟重跑結果逐位元組相同；兩個提交都沒有 `gpgsig`；保留主機設定與隔離主機設定兩種跑法，提交編號都重現 | — |
| B2 | spray 卡：其中一波 8 個組織、327 個帳號；10/10–10/14；151,000+ 次失敗；最高每分鐘 2,900 次；約 98% 是帳號被鎖住；0 次成功登入；揭示順序跟旁白一致 | spray.data（title、stats、note、keys）；a6cm、5xut、krad | MS | 200 | CONFIRMED（"327 accounts across eight organizations"、"151,000+ failed logon events"、"peaking on October 11 at 2,900 failures per minute"、"lockout responses represented nearly 98% of all activity"、"no successful authentication … was observed"）。順序：stats 有 3 格、揭示 2 次，所以 151,000+ 跟 a6cm 一起出現，98% 在 5xut，0 在 krad，每一格都跟講到它的那一句同時出現 | — |
| B3 | kwax：署長說容易被打的，是防禦弱、對外服務開得多的 | cheap/kwax；cheap.data.key | IT65 | 200 | CHANGED：原話是「容易受駭的對象**包括**較容易支付贖金者、防禦能力較弱者、開放大量對外服務者」，一共三種。旁白只取兩種、又用「是」，聽起來像完整的名單 | 「容易被打的，是防禦弱、對外服務開得多的。」→「容易被打的，包括防禦弱、對外服務開得多的。」。key「防禦弱、對外開得多的先被打」沒改，見〈懷疑〉 |
| B4 | GMO：「光一組攻擊主機就鎖定約二十家企業」；label「日本：一組攻擊主機鎖定的企業」；key「日本：一組主機鎖定約 20 家」 | month/wnqk；month.data.stats[1]、keys[1]；description | SNS、IT50 | 200 | CONFIRMED（只有媒體來源）：IT50「一組使用ARTEX的攻擊基礎設施鎖定約20家日本企業」，後文又寫「另外6臺…攻擊主機」；SNS「この攻撃元インフラ…標的は約 20 社」「キャンペーンごとに別の攻撃用ホスト」。GMO 一手頁今天讀不到 | — |
| B5 | 時間線 10/14–15「Zeabur 遭入侵（報告未提 ARTEX）」；f3qn「十四、十五號，台灣的 Zeabur 被入侵，它的報告沒提到 ARTEX」 | timeline.rows[1]、keys[1]；timeline/f3qn | ZB、IT04 | 200 | CONFIRMED（ZB「2026 年 10 月 14 日至 15 日，攻擊者使用外洩的 Zeabur 內部憑證，入侵了…」，ARTEX 0 次；「臺灣雲端部署平臺Zeabur」只有媒體這樣寫） | — |
| B6 | gpaj「剛剛說過，它的報告沒提到 ARTEX，也沒說攻擊者用了 AI 工具」；zeabur.data.sub | zeabur/gpaj；zeabur.data.sub | ZB | 200 | CONFIRMED（同 A5） | — |
| B7 | tiky「緊接著，台灣的 91APP 也找到它的痕跡」 | open/tiky | MS、91N、IT23 | 200 | CONFIRMED：MS 發布於 2026-10-21 18:23:55 UTC，等於台灣 10-22 02:23；91APP 發布於 2026-10-22 10:29:52 UTC，等於台灣 10-22 18:29，前後相差約 16 小時。IT23 寫 91APP 先前的重訊「並未說明具體入侵途徑」，ARTEX 是 10-22 才公開的。見〈懷疑〉 | — |
| B8 | 說明欄「緊接著台灣的 91APP 也在調查報告裡寫出 ARTEX 的痕跡」 | youtube.description | 91N、91R | 200 | CONFIRMED（「系統內發現 ARTEX 1等工具痕跡」） | — |
| B9 | 6pn9「真正進去的，是早就被允許的 App，和放在程式碼倉庫裡的金鑰」 | not-guessing/6pn9 | MS、91R、91N、IT23 | 200 | CONFIRMED，可以當摘要：MS 寫 "applications that had already been granted access"；91R「從內部 GitLab 系統上找到…金鑰」；91N 與 IT23「自／從 GitLab 取得」。GitLab 是程式碼倉庫平台，這句也沒說金鑰在 git 歷史裡。見〈懷疑〉 | — |
| B10 | urui「剛剛那把資料庫金鑰，也在 GitLab 這種倉庫裡；怎麼放的，報告沒寫。」 | one-line/urui | 91N、91R、IT23 | 200 | CONFIRMED（三頁都沒寫存放方式）。全長 36 字 | — |
| B11 | c33：署長列的容易受駭的三種對象，旁白取後兩種 | claims.md c33 | IT65 | 200 | CONFIRMED。c33 已補上 B3 的改動 | claims.md c33 補註 |
| C1 | （verify-1 #2）「Microsoft 評估：一個中國政府相關的駭客組織」 | open/y9kb；description | MS | 200 | CONFIRMED（"a China-state aligned actor"；"Microsoft assesses"） | — |
| C2 | （#3）用 ARTEX 攻擊幾百個組織 | open/7tzn；description | MS | 200 | CONFIRMED | — |
| C3 | （#5）好幾次不到三小時拿下雲端管理權限 | open/tiky；three-hours.data；zz9s；uesa；title；description | MS | 200 | CONFIRMED（"multiple instances where the time from initial targeting to privileged access was less than 3 hours"） | — |
| C4 | （#8）其中一波十五萬次全部失敗 | not-guessing/4irk、key；spray/a6cm；closing/wkg5；view/hvs8；description | MS | 200 | CONFIRMED | — |
| C5 | （#9）早就被允許的 App；granted 卡的引文與翻譯 | granted.data.quote、translation；j7dk；6pn9；hvs8 | MS | 200 | CONFIRMED（引文逐字相符） | — |
| C6 | （#12）151,000+ | spray.data.stats[0] | MS | 200 | CONFIRMED | — |
| C7 | （#13）最高一分鐘 2,900 次 | spray/a6cm；spray.data.stats[0].note | MS | 200 | CONFIRMED | — |
| C8 | （#16）拿到備份服務商 ConnectWise 的應用程式憑證 | granted/wqed；granted.data.keys[0] | MS、CW | 200 | CONFIRMED（"acquiring control of the identities of multiple ConnectWise cloud applications … stolen app credentials"；"cloud backup vendor"；CW 10-17 "unauthorized access to application identities"） | — |
| C9 | （#18）兩千兩百五十多個；超過 2,250 個租戶 | three-hours/v7kk、data.sub；description | MS | 200 | CONFIRMED（"attempt to sign-in to more than 2,250 tenants"；"to machine speed"） | — |
| C10 | （#34）10/21 Microsoft 報告與資安署示警同一天 | timeline.rows[4]；sfzc | MS、MODA | 200 | CONFIRMED（MS「October 21」；MODA「今(21)日」，發稿 115 年 10 月 21 日） | — |
| C11 | （#35）10/22 91APP 公布 18 天調查報告 | timeline.rows[5]；26an；open.data.subtitle；route-91app.data.source | 91N | 200 | CONFIRMED | — |
| C12 | （#39）「沒有新的漏洞」 | route-91app/qb46 | 91R | 200 | CONFIRMED，屬推論（「AppSmith 存在漏洞，91APP 未及時套用修補更新」） | — |
| C13 | （#44）八月出事後換過一輪，沒換到這幾把 | zeabur/siri、data.text | ZB | 200 | CONFIRMED（「八月的輪替沒有涵蓋這次被使用的憑證」；IT04 轉述「設定儲存庫中以明文保存的叢集管理權杖與AWS金鑰」） | — |
| C14 | （#47）Zeabur 報告日期 2026-10-19 | zeabur.data.sub；zeabur-ask.data.source；description | ZB | 200 | CONFIRMED（"date":"2026-10-19"） | — |
| C15 | （#54）`git log --oneline -G PASSWORD` 的兩筆（現在是 5f37a2a、a6036e8） | gitlog.data；qyg2、tzyy | RUN | — | CONFIRMED（同 B1） | — |
| C16 | （#58）GitHub："…as a first step you need to revoke and/or rotate that secret." | rotate.data；4qg5；description | GHS | 200 | CONFIRMED（逐字相符） | — |
| C17 | （#61）GitHub：Settings → Applications → Authorized OAuth Apps → Revoke；「不認得的就撤銷」 | accounts.data.steps[1]、keys[1]；2wc7 | GHO | 200 | CONFIRMED（profile picture → Settings → "Integrations" section → Applications → Authorized OAuth Apps → Revoke；"you don't recognize or that are out-of-date"） | — |
| C18 | （#64）91APP 實際影響多少會員，報告說之後才公布 | unknown/8e9n、data.text | 91N、91R、IT23 | 200 | CONFIRMED（「預計於下週向社會更新進一步的調查結果，包括受影響範圍」；報告頁今天仍是 10/22；搜尋沒找到更新）。這條會過期 | — |
| C19 | （#65）資安署說七月國內也監測到類似 AI 攻擊，沒說是哪一套工具 | unknown/i653、data.text；description | IT65、MODA | 200 | CONFIRMED（媒體：「資安署也透露今年7月監測到類似AI攻擊活動」；兩頁都沒有寫工具名稱） | — |

### 抽樣（範圍 C）

`_tools/verify2/draw.py` 從 verify-1 主張表裡判定欄以 CONFIRMED 開頭的列抽樣，`random.Random(20261027).sample(列, ceil(n/3))`。
解析出 57 列，verify-1 寫的是 58 列：#53 的主張欄含 `||`，表格切欄時錯位，所以沒進入候選。#53 是 grep 卡，已經在 B1 裡重跑核對過。
抽出 19 列：2、3、5、8、9、12、13、16、18、34、35、39、44、47、54、58、61、64、65，就是上表的 C1–C19。

## 示範重跑

- `_tools/verify2/rerun.sh` 在兩個新建的空目錄各跑一次 `_tools/run/run.sh`，兩次都設
  `GIT_AUTHOR_NAME/EMAIL`、`GIT_COMMITTER_NAME/EMAIL`＝demo／demo@example.invalid：
  - `demo-hostcfg/`：保留主機的全域設定，全域 `commit.gpgsign` 是 true，被倉庫內的 `commit.gpgsign false` 蓋過；
  - `demo-isolated/`：`GIT_CONFIG_GLOBAL=/dev/null`、`GIT_CONFIG_NOSYSTEM=1`。
- 兩份逐字輸出（`transcript-hostcfg.txt`、`transcript-isolated.txt`）跟撰稿者的 `_tools/run/transcript-20261027-unsigned.txt` **逐位元組相同**，三份的 sha256 都是 c8b6f491…a578。
  兩個提交都沒有 `gpgsig`，提交編號是 a6036e8（add db config）、5f37a2a（remove secrets from repo）。
- `cmpcards.py` 拿 video.json 四張 terminal 卡的 command／output 跟重跑結果比對：ls、grep、gitlog、gitshow 四張全部 MATCH。
  `git log --oneline -G API_KEY` 沒有輸出。環境是 ls 9.4、grep 3.11、git 2.43.0、Ubuntu 24.04.5 LTS，跟卡片上寫的一致。
- repo 裡只剩 brief.md 還寫舊的 984e6d1／b3faea1。brief.md 不在可改範圍，影片內容沒用到它。

## 摘要

- 檢查的主張：37 列（A 7、B 11、C 19）。CONFIRMED 36、CHANGED 1、NOT FOUND 0、OUT OF SCOPE 0。
- 改動（1 處）：B3 kwax「容易被打的，是…」→「容易被打的，包括…」。署長原話列了三種對象，旁白只取兩種。claims.md c33 補註，〈進度〉加一條 verify-2 的紀錄。
  sources 的 checked_on 本來就是 2026-10-27，不用改。
- 看法：沒有跟 brief〈站主觀點〉衝突的地方。view 一景標了「我的看法是」；answer 一景「AI 會先挑最便宜的門」是署長那句「AI同樣會優先尋找容易突破的對象」的轉述，跟站主觀點一致。
  brief 的站主觀點本身仍寫明是「提案」。另外，verify-1 指出的張力（院長說「中大型企業是這波AI攻擊的高風險目標」）在 kwax 改寫後變小了，但 naive→answer 那條「我不是大公司」的迴圈仍然沒提院長這句。
- 聽眾檢查：
  - 照原始字元算（含空格與標點）超過 40 的有 tiky 41（「緊接著」改寫後變長）、qyg2 41、vtxp 43、78d5 42。去掉空格與標點都在 33–37 之間，lint 的 spoken units 不報警告。
  - `API_KEY`（asmx）不在 docs/videos/lexicon.json。
  - 沒有括號、網址或流程話。
  - spray 一景的揭示順序已經修好。其他揭示都沒有早於介紹它的句子；after-found 第二、三步仍然比旁白晚一句出現，是晚出現，不是早。
  - spray 卡標題寫「8 個組織、327 個帳號」，旁白沒念到。
- lint：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug artex-ai-attack-leftover-keys` → 0 errors, 0 warnings（估 9.5 分鐘、102 句）。

### 懷疑但沒改的事

- tiky「緊接著，台灣的 91APP 也**找到**它的痕跡」：緊接在 Microsoft 之後的，是 91APP **公布**痕跡這件事。91APP 哪一天找到 ARTEX 痕跡，報告沒寫，但時間順序說成「之後找到」不能證明是錯的。說明欄寫的是「在調查報告裡寫出」，比較準確。
- 標題「它不靠猜密碼」是一個概括：Microsoft 只寫出一波噴灑全部失敗，沒說好幾次不到三小時的案例全部來自授權過的 App。不過 Microsoft 把速度歸因於 "privileged authentication material"，所以這個定調站得住。
- 6pn9「放在程式碼倉庫裡的金鑰」：91APP 寫的是「內部 GitLab 系統上找到」。GitLab 上也有 CI 變數等不在 git 檔案裡的地方，所以這句比原文稍微具體一點；urui 已經說明「怎麼放的，報告沒寫」。
- cheap.data.key「防禦弱、對外開得多的先被打」：「先」對應署長「AI同樣會優先尋找容易突破的對象」，可以接受，沒改。
- wnqk「一組攻擊主機」：IT50 寫「一組攻擊基礎設施」，SNS 寫「攻撃元インフラ」。GMO 一手頁今天讀不到，只能用媒體對。
- granted/anq3「所以也沒有兩步驟驗證可以擋」：仍然是推論，Microsoft Learn 寫 workload identities "Can't perform multifactor authentication"，不是報告原話（同 verify-1）。
- 會過期的事實：
  - MS 頁 dateModified 是 2026-10-26，內容跟撰稿者 10-27 的快照相同，無法跟 10-21 的原版比較；
  - 91APP「下週」的更新今天還沒出來；
  - Zeabur 報告寫明會更新；
  - ConnectWise 狀態頁還在增加新的更新。
- 作業紀錄：抓頁面時對撰稿者的 `_tools/sources-20261027/` 重跑了一次 totext.py，那裡的 `.txt` 會重新產生；HTML 沒有動。

### 能不能稱為「已查核」

**可以。** 本輪只改了 1 處事實，低於要開第三輪的門檻（超過 3 處）。所有主張都已判定，lint 0 錯誤，示範可以逐位元組重現。
上架前要再看一次 91APP 有沒有發布「下週」那份更新；如果發布了，unknown/8e9n 要跟著改。
