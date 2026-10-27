# artex-ai-attack-leftover-keys：查核第 1 輪（verify-1）

查核日期 2026-10-27。查核者是獨立代理，不是撰稿者。每一頁都是今天自己用
`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重抓（同一網域間隔至少 1 秒，去掉 `<!-- -->` 才讀）；
撰稿者存的 `_tools/sources*/` 只拿來對照。網頁搜尋用了 1 次（找「記者會」的出處，沒找到）。
逐句抽出的清單（347 個字串，含每句 `text`、每張卡的 `data`、縮圖、標題、說明、標籤）在工作區 `_tools/verify/claims-extracted.tsv`；
下表把它們併成可查核的主張，同一個事實出現在幾個地方就列在同一列的「位置」。`video.json` 沒有任何 `say` 欄位，所以沒有 `say_for` 要更新。

## 來源與 HTTP 狀態（2026-10-27 抓取）

| 代號 | URL | HTTP |
| --- | --- | --- |
| MS | https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/ （datePublished 2026-10-21T18:23:55Z） | 200 |
| 91N | https://91app.com/blog/91app-202610-security-incident/ （datePublished 2026-10-22T10:29:52Z） | 200 |
| 91R | https://91app.com/91app-202610-security-incident/ （報告頁，「資料更新日期 10/22」） | 200 |
| MODA | https://moda.gov.tw/ACS/press/news/press/21130 （發稿日期 115 年 10 月 21 日） | 200 |
| IT65 | https://www.ithome.com.tw/news/179865 （2026-10-21，媒體） | 200 |
| IT50 | https://www.ithome.com.tw/news/179850 （2026-10-21，媒體） | 200 |
| IT23 | https://www.ithome.com.tw/news/179923 （2026-10-23，媒體） | 200 |
| IT04 | https://www.ithome.com.tw/news/179804 （2026-10-20，媒體；不在 sources，只用來確認 Zeabur 是臺灣平台） | 200 |
| SNS | https://scan.netsecurity.ne.jp/article/2026/10/21/56522.html （2026-10-21，媒體） | 200 |
| GMO | https://gmo-cybersecurity.com/blog/20261019/ → 轉到首頁（網站暫時改成簡易版），一手部落格今天讀不到 | 200（轉址） |
| ZB | https://zeabur.com/zh-TW/blogs/october-2026-security-incident （date 2026-10-19，時間皆 UTC） | 200 |
| CW | https://status.connectwise.com/pages/incident/619cf82551fec9053d612f09/6ad263692dc48705ab3da2cb （MS 報告連到的 ConnectWise 狀態頁；新增到 sources） | 200 |
| CWT | https://www.connectwise.com/company/trust/advisories | 403 |
| GPW | https://support.google.com/accounts/answer/41078?hl=zh-Hant | 200 |
| G3P | https://support.google.com/accounts/answer/13533235?hl=zh-Hant | 200 |
| GHS | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository | 200 |
| GHO | https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/reviewing-your-authorized-oauth-apps | 200 |
| MSL | https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity （新增到 sources） | 200 |
| GITLOG | https://git-scm.com/docs/git-log （新增到 sources） | 200 |
| RUN | 本機重跑 `_tools/run/run.sh`（見「示範重跑」） | — |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 月 21 日 Microsoft 公布報告 | open/y9kb；open.data.subtitle；ms-page.data.caption；timeline row 10/21、sfzc；granted/backdoor.data.source；m365.data.source；description | MS | 200 | CONFIRMED（頁面日期 October 21；發布時間 18:23 UTC＝臺灣 10/22 02:23，片中一律用各家自己標的日期） | — |
| 2 | 「Microsoft 評估」：一個中國政府相關的駭客組織 | open/y9kb；description | MS | 200 | CONFIRMED（"Storm-0940, a China-state aligned actor"；"Microsoft assesses" 原文接在 ConnectWise 責任上，整份是 Microsoft 的評估，歸屬寫法可接受） | — |
| 3 | 用 AI 工具 ARTEX 攻擊幾百個組織 | open/7tzn；description | MS | 200 | CONFIRMED（"automate attacks targeting hundreds of organizations globally"） | — |
| 4 | 說明欄「同時攻擊全球幾百個組織」 | youtube.description | MS | 200 | CHANGED：原文是 "As early as September 2026 … targeting hundreds"，沒有「同時」 | 「ARTEX 同時攻擊全球幾百個組織」→「ARTEX 攻擊全球幾百個組織」 |
| 5 | 好幾次不到三小時拿下雲端管理權限 | open/tiky；three-hours.data（numeral 3、kicker、sub「多次案例」）；zz9s；view/uesa；youtube.title；description | MS | 200 | CONFIRMED（"multiple instances where the time from initial targeting to privileged access was less than 3 hours"；「privileged access to an organization's cloud infrastructure」） | — |
| 6 | 標題「它沒猜密碼」、開場卡「AI 駭客不猜密碼」 | youtube.title；open.data.title | MS | 200 | CHANGED：Microsoft 寫 "Storm-0940 used ARTEX to accelerate scanning and reconnaissance, password spraying, and OAuth application abuse"，它有猜密碼，只是猜不中；片中自己也說猜了十五萬次 | 「它沒猜密碼」→「它不靠猜密碼」；「AI 駭客不猜密碼，」→「AI 駭客不靠猜密碼，」 |
| 7 | 隔天 91APP 找到 ARTEX 痕跡 | open/tiky；month/d5nu；description | 91N、91R | 200 | CONFIRMED（「系統內發現 ARTEX 等工具痕跡」，10-22 公布；臺灣時間兩者同在 10/22，見「懷疑」） | — |
| 8 | 其中一波猜了十五萬次密碼，全部失敗 | not-guessing/4irk、data.key；spray/5xut；closing/wkg5；view/hvs8；description | MS | 200 | CONFIRMED（151,000+ failed logon events；"no successful authentication … was observed"；十五萬是 151,000+ 的下取整） | — |
| 9 | 真正進去的是早就被允許的 App | not-guessing/6pn9；granted/j7dk；view/hvs8；granted.data.quote、translation | MS | 200 | CONFIRMED（引文逐字相符："to authenticate to Microsoft 365 customer environments through applications that had already been granted access"） | — |
| 10 | 「沒人記得的金鑰」 | not-guessing/6pn9 | 91N、91R | 200 | OUT OF SCOPE（修辭；報告沒寫金鑰被遺忘，見「懷疑」） | — |
| 11 | 10/10–10/14、八個組織、327 個帳號 | spray/a6cm；spray.data.title、stats[0].note、keys[0] | MS | 200 | CONFIRMED | — |
| 12 | 151,000+ 次登入失敗 | spray.data.stats[0] | MS | 200 | CONFIRMED | — |
| 13 | 最高一分鐘 2,900 次 | spray/5xut；spray.data.keys[1] | MS | 200 | CONFIRMED（10-11 尖峰 2,900 failures per minute） | — |
| 14 | 約 98%／將近九成八是帳號被鎖住 | spray/krad；spray.data.stats[1] | MS | 200 | CONFIRMED（"lockout responses represented nearly 98% of all activity"） | — |
| 15 | 成功登入零次 | spray/krad；spray.data.stats[2]、keys[2] | MS | 200 | CONFIRMED | — |
| 16 | 拿到備份服務商 ConnectWise 的應用程式憑證 | granted/wqed；granted.data.keys[0] | MS、CW | 200 | CONFIRMED（"acquiring control of the identities of multiple ConnectWise cloud applications … stolen app credentials"；MS 稱 ConnectWise 為 "cloud backup vendor"；CW 10-17 "unauthorized access to application identities"） | — |
| 17 | 不需要任何人登入，所以也沒有兩步驟驗證可以擋 | granted/anq3 | MS、MSL | 200 | CONFIRMED（推論）：MS 只寫 "without requiring an interactive user sign-in"、沒寫 MFA；Microsoft Learn 寫 workload identities "Can't perform multifactor authentication"，所以推論成立，已把 MSL 加進 sources。不算誇大，但這句不是報告原話（見「懷疑」） | —（只新增來源） |
| 18 | 對兩千兩百五十多個企業的雲端環境嘗試登入；超過 2,250 個租戶 | three-hours/v7kk、data.sub；description | MS | 200 | CONFIRMED（"attempt to sign-in to more than 2,250 tenants"；"to machine speed"） | — |
| 19 | 不到三小時「就是這樣來的：門早就開著，AI 只是走得很快」 | three-hours/zz9s、data.key | MS | 200 | CONFIRMED（MS 同段："use an agentic AI tool and privileged authentication material to quickly attempt to compromise many organizations"） | — |
| 20 | 韓國金融機構被 AI 工具配合跳板入侵，外洩逾 6 萬筆個資 | month/kwvr；month.data.stats[0]、keys[0]；description | MODA | 200 | CONFIRMED（「韓國金融機構遭 AI 工具結合多層跳板入侵並外洩逾 6 萬筆個資」） | — |
| 21 | 日本 GMO：一台攻擊主機鎖定約 20 家企業 | month/wnqk；month.data.stats[1]、keys[1]；description | SNS、IT50（GMO 一手頁讀不到） | 200 | CONFIRMED（媒體）：SNS「この攻撃元インフラ … 標的は約 20 社」「キャンペーンごとに別の攻撃用ホスト」「新たに 6 台」；IT50「一組攻擊基礎設施鎖定約20家」。說明欄已寫明是 ScanNetSecurity、iThome 報導 | — |
| 22 | 台灣 91APP：一座訂單資料庫被存取 | month/d5nu；month.data.stats[2]、keys[2]；timeline row 10/3、4zjm | 91N、91R | 200 | CONFIRMED（「Commerce Cloud 其中一座訂單資料庫於 10 月 3 日 11 時 … 被非法存取」） | — |
| 23 | 卡片來源「資安署 10-21；GMO 10-19；91APP 10-22」 | month.data.source | MODA、SNS、91N | 200 | CONFIRMED | — |
| 24 | 資安署：AI 降低攻擊成本、提高速度，但防禦的核心觀念沒有變 | acs/kj3y、dxwq；acs.data.quote、kicker、source、keys；description | MODA | 200 | CONFIRMED（引文逐字相符，原文逗號是半形，卡片用全形，不影響） | — |
| 25 | 署長：部分基礎扎實的企業，AI 評估攻擊成本後放棄，轉向防護較弱的目標 | cheap/na73、data.key；answer/2yvb；description | IT65 | 200 | CONFIRMED（媒體轉述，新聞稿沒有；歸屬見 #26） | — |
| 26 | 這句話是「記者會上」說的 | cheap/3zwr；cheap.data.kicker；description | IT65、MODA | 200 | CHANGED：iThome 與新聞稿都沒有「記者會」字樣，網頁搜尋也沒找到；只能確認是 iThome 10-21 報導的署長說法 | 「記者會上，署長補了一個觀察：」→「同一天，署長還補了一個觀察：」；kicker「資安署署長，記者會」→「資安署署長，iThome 報導」；說明欄「照 iThome 對同日記者會的報導」→「照 iThome 同日的報導」 |
| 27 | 「它不挑公司大小，挑的是便宜。」 | cheap/kwax | IT65 | 200 | OUT OF SCOPE（沒標成看法的推論；見「看法」） | — |
| 28 | 撬鎖／翻門墊、一晚翻幾千家 | doormat 全部 | — | — | OUT OF SCOPE（比喻） | — |
| 29 | 門墊的答案在 Microsoft 報告，連結在說明欄 | ms-page/wq9c、data.caption | MS；tools/video/core/lint.mjs composeDescription | 200 | CONFIRMED（sources 會組進上架說明；截圖選擇器 `h1.card-block__title` 在今天的頁面上存在） | — |
| 30 | 時間線 10/14–15 Zeabur 叢集與平台資料庫被讀取 | timeline row 2、keys[1]、f3qn | ZB | 200 | CONFIRMED（「2026 年 10 月 14 日至 15 日 … 入侵了共享叢集 … 最後讀取了平台資料庫」，UTC） | — |
| 31 | Zeabur 是台灣的雲端部署平台 | timeline/f3qn；zeabur.data.kicker「台灣例子」 | IT04 | 200 | CONFIRMED（媒體：「臺灣雲端部署平臺Zeabur」）；Zeabur 報告本身沒寫，頁尾只有「© 2026 Zeabur Inc.」 | — |
| 32 | 10/16 ConnectWise 公告備份服務被存取 | timeline row 3、vwab | CW、MS（CWT 403） | 200 | CHANGED：CW 10-16 17:48 UTC 的公告是 "investigating recent attempts of unauthorized access associated with the ConnectWise Cloud Backup environment"，並說 "no indication that partner backup data has been accessed"；MS 也轉述成 "attempted unauthorized access" | 卡片「ConnectWise 公告備份服務遭存取」→「ConnectWise 公告備份服務遭入侵嘗試」；旁白「公告它的備份服務被存取；」→「公告有人試圖入侵它的備份服務；」；卡片來源加 ConnectWise；說明欄加 ConnectWise 一句；sources 加 CW |
| 33 | 10/19 GMO 確認日本企業遭 ARTEX 攻擊 | timeline row 4、keys[3]、cawt | SNS、IT50 | 200 | CONFIRMED（媒體：「10 月 19 日 … ARTEX が使われていたことを確認」） | — |
| 34 | 10/21 Microsoft 報告與資安署示警同一天 | timeline row 5、sfzc | MS、MODA | 200 | CONFIRMED | — |
| 35 | 10/22 91APP 公布 18 天調查報告 | timeline row 6、26an；open.data.subtitle；route-91app.data.source | 91N | 200 | CONFIRMED | — |
| 36 | Appsmith 套件沒更新，攻擊者從這裡進內網 | route-91app/kwit、d7ke；data.steps[0]、keys[0]；description | 91N、91R | 200 | CONFIRMED（「未更新套件的內部效率工具（Appsmith）進入內部網路」） | — |
| 37 | 在 GitLab 拿到一把資料庫金鑰，用它進訂單資料庫 | route-91app/wzkp、kfdv；data.steps[1–2]；one-line/urui；description | 91N、91R、IT23 | 200 | CONFIRMED | — |
| 38 | 不含信用卡等支付資訊 | route-91app/kfdv；data.steps[2].detail、keys[2] | 91N | 200 | CONFIRMED | — |
| 39 | 「沒有新的漏洞」 | route-91app/qb46 | 91R | 200 | CONFIRMED（推論：報告寫 Appsmith「存在漏洞，91APP 未及時套用修補更新」，是已有修補的舊洞） | — |
| 40 | 金鑰在 GitLab 裡怎麼放的，報告沒有寫 | one-line/urui | 91N、91R、IT23 | 200 | CONFIRMED（三頁都只寫「自／從 GitLab 取得／找到」） | — |
| 41 | Zeabur 的報告沒有提到 ARTEX，也沒說攻擊者用了 AI 工具 | zeabur/gpaj、data.sub | ZB | 200 | CONFIRMED（全文 0 次 ARTEX；提到 AI 的地方是攻擊者在找 AI 服務金鑰、試呼叫 Bedrock，是目標不是工具） | — |
| 42 | 說明欄「該報告沒有提到 ARTEX 或 AI 工具」 | youtube.description | ZB | 200 | CHANGED：報告有提到 new-api／one-api、n8n 與 AI 服務金鑰，字面上「沒提到 AI 工具」不成立；改成跟旁白一樣的說法 | 「該報告沒有提到 ARTEX 或 AI 工具」→「該報告沒有提到 ARTEX，也沒說攻擊者用了 AI 工具」 |
| 43 | 長期有效、用明文保存的管理憑證 | zeabur/nwji、data.text | ZB | 200 | CONFIRMED（根本原因段；「管理權杖未設定有效期限，自 2024 年 1 月建立後未曾輪替」） | — |
| 44 | 八月出事後換過一輪，沒換到這幾把 | zeabur/siri、data.text | ZB | 200 | CONFIRMED（「八月的輪替沒有涵蓋設定儲存庫中以明文保存的叢集管理權杖與 AWS 金鑰」） | — |
| 45 | 三十七分鐘、三百二十多萬筆環境變數 | zeabur/29n6、data.key「37 分鐘，逾 321 萬筆」；description「321 萬筆」 | ZB | 200 | CONFIRMED（10-15 16:10–16:47 UTC＝37 分鐘；平台資料庫環境變數 3,218,965 筆「已確認」） | — |
| 46 | Zeabur 原句「請更換存放在 Zeabur 的所有密碼與金鑰，即使八月事件後已經換過。」 | zeabur-ask.data.quote、keys；fvak | ZB | 200 | CONFIRMED（逐字相符，在摘要「您需要做什麼」） | — |
| 47 | Zeabur 報告日期 2026-10-19 | zeabur.data.sub；zeabur-ask.data.source；description | ZB | 200 | CONFIRMED | — |
| 48 | Google 原句：改密碼會登出所有裝置，例外…第三方應用程式 | google.data.quote | GPW | 200 | CONFIRMED（逐字相符，「…」省略了其他例外） | — |
| 49 | 旁白「但例外是，你已經授權存取帳戶的那些第三方應用程式」 | google/ei35；google.data.keys[1] | GPW | 200 | CHANGED：頁面列了三項例外（驗證身分的裝置、授權過第三方應用程式的裝置、智慧住宅裝置） | 「但例外是，你已經授權…」→「但例外之一，是你已經授權…」；key「例外：…」→「例外之一：…」 |
| 50 | 攻擊者會替應用程式加上自己的憑證；原本的 App 修好後仍可能當後門 | backdoor/dqii、f3e5；data.quote、translation、keys；description | MS | 200 | CONFIRMED（引文逐字相符，"mediated" 是原文用字） | — |
| 51 | 示範倉庫：提交含假密碼的設定檔，下一次提交刪掉並加進忽略清單 | ls/9c5b、7iw4 | RUN | — | CONFIRMED | — |
| 52 | `ls -A` → `.git`、`.gitignore`；ls 9.4 | ls.data | RUN | — | CONFIRMED（逐位元組相同） | — |
| 53 | `grep … || echo "not found"` → not found；grep 3.11 | grep.data；tpcz、hvxy | RUN | — | CONFIRMED | — |
| 54 | `git log --oneline -G PASSWORD` → 984e6d1、b3faea1 兩筆；git 2.43.0、Ubuntu 24.04.5 | gitlog.data；qyg2、tzyy；description | RUN、GITLOG | — | CONFIRMED（開簽章重跑逐位元組相同；提交編號依賴這台主機的簽章設定，見「示範重跑」） | — |
| 55 | `git show b3faea1:.env` 整個檔案回來，密碼在第二行 | gitshow.data；a497、5uez；description | RUN | — | CONFIRMED | — |
| 56 | 「沒有任何輸出，就是歷史裡沒有這個字」 | your-line/nq6x；your-line.data.caption | RUN、GITLOG | 200 | CHANGED：git log 沒給範圍時「defaults to HEAD (i.e. the whole history leading to the current commit)」，別的分支不會搜到 | 「就是歷史裡沒有這個字」→「就是目前分支的歷史裡沒有這個字」；caption「代表歷史裡沒有…」→「代表目前分支的歷史裡沒有…」；sources 加 GITLOG |
| 57 | `-G API_KEY` 在示範倉庫沒有輸出 | your-line.data.caption；description | RUN | — | CONFIRMED（`-G SECRET` 也沒有輸出） | — |
| 58 | GitHub："…as a first step you need to revoke and/or rotate that secret." | rotate.data.quote、translation、keys；4qg5；description | GHS | 200 | CONFIRMED（逐字相符） | — |
| 59 | 改寫歷史只改得到你這一份；clone、fork 裡還在；通知有複本的人；順序 | after-found 全部 | GHS | 200 | CONFIRMED（"You cannot remove sensitive data from other users' clones"；forks "will continue to be accessible"；"Coordinate with colleagues"；輪替後改寫歷史 "may not be warranted"） | — |
| 60 | Google：連結的應用程式 → 查看詳細資料 → 移除存取權 | accounts.data.steps[0]、keys[0]；vtxp | G3P | 200 | CONFIRMED（完整路徑是「連結的應用程式」→「有權存取您的 Google 帳戶」→ 選應用程式 →「查看詳細資料」→「移除存取權」→「確認」；卡片是正確的節略） | — |
| 61 | GitHub：Settings → Applications → Authorized OAuth Apps → Revoke | accounts.data.steps[1]、keys[1]；2wc7 | GHO | 200 | CONFIRMED（頭像 → Settings → 側欄 Integrations 的 Applications → Authorized OAuth Apps → … → Revoke；「不認得的」對應 "you don't recognize or that are out-of-date"） | — |
| 62 | 不認得、不再用的先移除，需要時再授權 | accounts.data.steps[2]；yt6t | GHO | 200 | OUT OF SCOPE（建議） | — |
| 63 | M365：看應用程式（服務主體）登入、查新增的認證、查權限與角色變更 | m365 全部 | MS | 200 | CONFIRMED（Immediate actions："extend service-principal sign-in review"、"application or service-principal credential additions … privileged role assignments"） | — |
| 64 | 91APP 實際影響多少會員，報告說之後才公布 | unknown/8e9n、data.text | 91N、91R、IT23 | 200 | CONFIRMED（「預計於下週向社會大眾報告」；報告頁今天仍是「資料更新日期 10/22」）——會過期 | — |
| 65 | 資安署說七月國內也監測到類似 AI 攻擊，沒說哪套工具 | unknown/i653、data.text；description | IT65、MODA | 200 | CONFIRMED（媒體轉述：「資安署也透露今年7月監測到類似AI攻擊活動」；兩頁都沒有工具名） | — |
| 66 | 資安署建議離職當天停用帳號、每季覆核權限 | three-things/ijkr、data.source | MODA | 200 | CONFIRMED（重點一・嚴密帳號管理） | — |
| 67 | 「金鑰設期限」 | three-things.data.steps[2]、ijkr | — | — | OUT OF SCOPE（卡片來源已標「期限：站主看法」） | — |
| 68 | AI 會先挑最便宜的門 | answer/2yvb、data.key | IT65 | 200 | CONFIRMED（署長：「AI同樣會優先尋找容易突破的對象」） | — |
| 69 | 我的看法：AI 沒有發明新的入口 | view 全部 | — | — | OUT OF SCOPE（已標「我的看法是」，與 brief 站主觀點一致） | — |
| 70 | 錄製日期、示範環境、片中指令 | description 第 3 段與指令段 | RUN | — | CONFIRMED | — |
| 71 | 標籤（ARTEX、Microsoft Storm-0940、Zeabur 資安事件…） | youtube.tags | MS、ZB | 200 | CONFIRMED（沒有一個標籤把 Zeabur 跟 ARTEX 寫在一起） | — |
| 72 | 縮圖「撿鑰匙／不撬鎖」、sub「AI 駭客怎麼進去、你的鑰匙怎麼收回」 | thumbnail.data | — | — | OUT OF SCOPE（比喻；與修正後的標題不衝突） | — |
| 73 | 片頭問題、承諾、轉場問句、留言題、訂閱 | naive、stakes、promise、mfa、gone、keys-not-locks、closing 等 | — | — | OUT OF SCOPE | — |

## 示範重跑

- 在空目錄 `_tools/verify/demo-run/` 照指示設 `GIT_AUTHOR_NAME/EMAIL`、`GIT_COMMITTER_NAME/EMAIL`＝demo／demo@example.invalid，並以 `GIT_CONFIG_GLOBAL=/dev/null` 重跑：提交編號是 **a6036e8、5f37a2a**，不是 984e6d1、b3faea1；`git show b3faea1:.env` 失敗。tree（a043d09…、062d0ca…）與檔案內容完全相同。
- 原因：撰稿者的兩個提交帶 SSH 簽章（`gpgsig`），來自這台主機的全域設定 `commit.gpgsign=true`、`gpg.format=ssh`。在 `_tools/verify/demo-run2/` 保留全域設定重跑，逐字輸出前 17 行與 `transcript-20261027.txt` **逐位元組相同**（sha256 8b9b6ee1…）。
- 對影片的影響：卡片上的輸出是真的；但觀眾自己照做會得到不同的提交編號（本來就不會一樣，片中已用「<提交編號>」）。claims.md 原本寫「所以提交編號可以重現」，已改成寫明前提。

## 摘要

- 檢查的主張：73 列（由 347 個字串歸併）；CONFIRMED 58、CHANGED 7、NOT FOUND 0、OUT OF SCOPE 8。
- 改動的事實（7）：#4 說明欄「同時」；#6 標題與開場卡「沒猜／不猜密碼」→「不靠猜密碼」；#26「記者會」歸屬 → iThome 同日報導；#32 ConnectWise 10/16 是入侵嘗試，不是「被存取」；#42 說明欄 Zeabur「沒提到 AI 工具」的字面寫法；#49 Google 例外「之一」；#56 git log 只看目前分支。
- 新增來源：ConnectWise 狀態頁、Microsoft Learn（workload identities 不能做 MFA）、git-log 文件，checked_on 都是 2026-10-27。
- 會過期的事實：91APP「下週」公布受影響範圍（新聞稿 2026-10-22，報告頁今天仍是「資料更新日期 10/22」，預計 10/26–10/30 這週更新）；Zeabur 報告「調查仍在進行，本文會隨進度更新」（頁面日期 2026-10-19）；Microsoft 報告可能更新（2026-10-21）；ConnectWise 狀態頁持續更新（最後一則 2026-10-17 9:24PM EDT）；GMO 一手部落格今天轉到首頁（網站暫時改成簡易版），日本的數字目前只有媒體可對。
- 看法：view 一景已標「我的看法是」，與 brief 站主觀點一致；brief 的站主觀點本身寫明還是「提案」，等站主確認。cheap/kwax「它不挑公司大小，挑的是便宜。」沒標成看法，是旁白自己的推論；同一篇 iThome 裡資安院院長說「中大型企業是這波AI攻擊的高風險目標」，跟「不挑公司大小」有張力（署長說的是「幾乎所有企業都可能遭掃描」、會挑防禦弱的）。報告給站主，沒有改寫。
- 聽眾檢查：one-line/urui 41 字（超過 40）；your-line/asmx 的 `API_KEY` 不在 docs/videos/lexicon.json（lint 沒報錯，試聽時聽念法）；沒有「經查證」「本影片」這類流程話、沒有括號或網址。spray 一景：第二格「約 98%」在 5xut 出現，旁白到 krad 才講 98%（揭示早於介紹）。after-found 一景：步驟二、三的說明都比旁白晚一句出現（晚出現，不是早）。
- lint：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug artex-ai-attack-leftover-keys` → 0 errors, 0 warnings（估 9.5 分鐘、102 句）。

### 懷疑但沒改的事

- granted/anq3「所以也沒有兩步驟驗證可以擋」接在「報告說…」後面，聽起來像 Microsoft 的話；事實上成立（Microsoft Learn），但不是報告原文。要不要改成不像引述的說法，交給站主。
- timeline 把 Zeabur 排在一串 ARTEX 事件中間，章名與上一句是「台灣這次的鑰匙放在哪？」；撇清的那句（gpaj）晚約一分鐘才出現。沒有任何字句把 Zeabur 跟 ARTEX 連在一起，但聽眾可能自己連起來。
- Microsoft 報告發布在 2026-10-21 18:23 UTC，即臺灣時間 10/22 02:23；91APP 在臺灣時間 10/22 18:29 發布。照各家自己標的日期，「隔天」成立；照臺灣時間兩者同一天。
- not-guessing/6pn9「沒人記得的金鑰」是修辭，91APP 沒說那把金鑰被遺忘。
- stakes/yfkf「這種鑰匙…改密碼收不回來」：對授權過的 App 成立（Google 例外）；對留在 git 歷史裡的資料庫密碼，輪替那組密碼正是 GitHub 說的第一步，聽眾可能混淆「改帳號密碼」和「輪替金鑰」。
- month/wnqk「一台攻擊主機」：SNS 用「攻撃元インフラ」並說另外「新たに 6 台」，iThome 用「一組攻擊基礎設施」；讀成一台合理，但一手來源今天讀不到。
- 署長的話只有 iThome 轉述，新聞稿沒有；已照實寫成「iThome 報導」。

### 需要第二輪嗎

**需要。** 本輪改了 7 處事實（規則：超過 3 處 → 第二輪）。所有主張都已判定，沒有懸而未決的；但在第二輪查核前不能稱本稿「已查核」。
