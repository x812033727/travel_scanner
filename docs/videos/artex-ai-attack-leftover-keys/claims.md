# artex-ai-attack-leftover-keys：可查核的主張

撰稿 2026-10-27。每一行：編號｜主張（旁白或卡片上的說法）｜來源｜確認日期｜場景。
來源頁的 HTML 與抽出的純文字在工作區 `_tools/sources/`（2026-10-26 存，10-27 撰稿時重讀）；示範的指令稿與逐字輸出在 `_tools/run/`。

MS ＝ https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/

## 事實

c1｜Microsoft 2026-10-21 公布報告，評估一個中國政府相關（China-state aligned）的組織 Storm-0940 用 ARTEX 自動化攻擊；旁白說「評估」，對應原文 "Microsoft assesses"｜MS 第一段、What's happening｜2026-10-27｜open、ms-page、timeline
c2｜攻擊對象是全球幾百個組織（"targeting hundreds of organizations globally"）｜MS 第一段｜2026-10-27｜open
c3｜好幾次從鎖定目標到取得雲端特權存取不到三小時（"multiple instances where the time from initial targeting to privileged access was less than 3 hours"）；旁白「拿下雲端管理權限」對應 privileged access to an organization's cloud infrastructure｜MS 第一段｜2026-10-27｜open、three-hours
c4｜91APP 2026-10-22 公布 18 天調查報告，系統內發現 ARTEX 等工具痕跡；旁白「隔天」＝ Microsoft 報告的隔天｜https://91app.com/blog/91app-202610-security-incident/｜2026-10-27｜open、month、timeline
c5｜2026-10-10 至 10-14，對八個組織、327 個帳號的密碼噴灑：失敗登入 151,000+ 次，10-11 尖峰每分鐘 2,900 次，近 98% 的回應是鎖定，沒有任何成功驗證（"no successful authentication, token issuance, Graph call, or directory change was observed"）。Microsoft 也寫 Storm-0940 "used ARTEX to accelerate scanning and reconnaissance, password spraying, and OAuth application abuse"，所以它有猜密碼、只是沒猜中：verify-1 把標題「它沒猜密碼」與開場卡「AI 駭客不猜密碼」改成「不靠猜密碼」｜MS〈Password Spraying〉〈What is ARTEX?〉｜2026-10-27｜open、not-guessing、spray、youtube.title
c6｜攻擊者透過早就被授權的應用程式登入 Microsoft 365 客戶環境，不需要使用者互動式登入（"through applications that had already been granted access … without requiring an interactive user sign-in"）；旁白「沒有兩步驟驗證可以擋」是由「不需要互動式登入」推出的說法，原文沒有寫 MFA；查核 verify-1 另以 Microsoft Learn〈Conditional Access for workload identities〉為據：workload identities "Can't perform multifactor authentication"，所以這句保留｜MS 第三段；https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity｜2026-10-27｜not-guessing、granted
c7｜韓國金融機構遭 AI 工具結合多層跳板入侵，外洩逾 6 萬筆個資｜https://moda.gov.tw/ACS/press/news/press/21130（資安署新聞稿 2026-10-21）｜2026-10-27｜month
c8｜GMO サイバーセキュリティ by イエラエ 10-19 確認攻擊元使用 ARTEX；該攻擊基礎設施的標的約 20 家日本企業，另找到 6 台攻擊主機（媒體的「約 80 家」不用）｜https://scan.netsecurity.ne.jp/article/2026/10/21/56522.html 、https://www.ithome.com.tw/news/179850｜2026-10-27｜month、timeline
c9｜91APP Commerce Cloud 一座訂單資料庫於 10 月 3 日遭攻擊而被非法存取（報告寫「10 月 3 日 11 時」，時區未註明，卡片只寫日期）｜91APP 新聞稿｜2026-10-27｜month、timeline
c10｜資安署 10-21 新聞稿原句：「新興 AI 大幅降低了攻擊成本並提升攻擊速度，但防禦的核心觀念並未改變」｜moda.gov.tw/ACS/press/news/press/21130｜2026-10-27｜acs、timeline
c11｜署長蔡福隆 10-21 說（iThome 同日報導；報導與新聞稿都沒有寫「記者會」，verify-1 把旁白「記者會上」改成「同一天」、kicker 改成「資安署署長，iThome 報導」），政府觀察到部分資安基礎扎實的企業，AI 工具在評估攻擊成本後便放棄攻擊，轉向防護較弱的目標（媒體轉述，新聞稿沒有這句）｜https://www.ithome.com.tw/news/179865｜2026-10-27｜cheap
c12｜尖峰每分鐘 2,900 次失敗（10-11）｜MS〈Password Spraying〉｜2026-10-27｜spray
c13｜攻擊者取得多個 ConnectWise 雲端應用程式的身分後，以這些被盜的應用程式憑證登入客戶環境；ConnectWise 的事件與 Cloud Backup 有關，旁白稱「備份服務商」｜MS〈What is ARTEX?〉〈Downstream customer access〉｜2026-10-27｜granted
c14｜ConnectWise 被存取後，Storm-0940 用 ARTEX 嘗試登入超過 2,250 個租戶（tenants）；旁白說「兩千兩百五十多個企業的雲端環境」｜MS〈What is ARTEX?〉｜2026-10-27｜three-hours
c15｜Zeabur：2026-10-14 至 15（UTC）攻擊者用外洩的內部憑證入侵共享叢集、部分專用伺服器與內部系統，讀取平台資料庫｜https://zeabur.com/zh-TW/blogs/october-2026-security-incident｜2026-10-27｜timeline
c16｜ConnectWise 10-16（17:48 UTC）的初步公告寫的是調查 Cloud Backup 環境「recent attempts of unauthorized access」，並說「no indication that partner backup data has been accessed」；10-17 才寫「unauthorized access to application identities」。verify-1 把卡片「公告備份服務遭存取」改成「公告備份服務遭入侵嘗試」、旁白改成「公告有人試圖入侵它的備份服務」｜https://status.connectwise.com/pages/incident/619cf82551fec9053d612f09/6ad263692dc48705ab3da2cb；MS〈What is ARTEX?〉｜2026-10-27｜timeline
c17｜91APP：攻擊者透過一項未更新套件的內部效率工具 Appsmith 進入內部網路，自 GitLab 取得資料庫金鑰後入侵訂單資料庫；事件僅涉訂單資訊，不含信用卡等支付工具資訊｜91APP 新聞稿；iThome 179923｜2026-10-27｜route-91app
c18｜91APP 的報告沒有說明那把金鑰在 GitLab 裡怎麼存放（新聞稿與 iThome 都只寫「自 GitLab 取得」）｜同上｜2026-10-27｜route-91app、one-line
c19｜Zeabur 的初步報告沒有提到 ARTEX，也沒有說攻擊者使用 AI 工具（報告提到攻擊者在找 AI 服務的金鑰、試圖呼叫 Amazon Bedrock，這是攻擊目標，不是攻擊工具）｜Zeabur 初步報告全文｜2026-10-27｜zeabur
c20｜根本原因：長期有效的管理憑證以明文保存且可從公網使用；八月的輪替沒有涵蓋設定儲存庫中以明文保存的叢集管理權杖與 AWS 金鑰｜Zeabur 初步報告〈摘要〉〈為什麼還是發生〉｜2026-10-27｜zeabur
c21｜10-15 16:10 至 16:47（37 分鐘）平台資料庫被讀取；環境變數 3,218,965 筆（已確認）｜Zeabur 初步報告〈涉及哪些資料〉；iThome 179804 也寫「短短37分鐘」｜2026-10-27｜zeabur
c22｜原句：「請更換存放在 Zeabur 的所有密碼與金鑰，即使八月事件後已經換過。」｜Zeabur 初步報告〈摘要〉｜2026-10-27｜zeabur-ask
c23｜Google：變更或重設密碼會登出所有裝置，例外有三項（驗證身分的裝置、這一項、智慧住宅裝置），其中一項是「安裝了第三方應用程式的某些裝置，而且你已將帳戶存取權授予這些應用程式」；verify-1 把旁白「但例外是」改成「但例外之一，是」、key 改成「例外之一」｜https://support.google.com/accounts/answer/41078?hl=zh-Hant｜2026-10-27｜google
c24｜原句："These changes can remain active as a backdoor even after the original compromised application is mediated."（"mediated" 是原文用字）｜MS〈Downstream customer access〉｜2026-10-27｜backdoor
c25｜GitHub："as a first step you need to revoke and/or rotate that secret"｜https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository｜2026-10-27｜rotate
c26｜只改寫歷史並 force push，含敏感資料的提交仍可能留在 clone、fork、快取與參照它的 PR；別人的 clone 你刪不掉｜同上｜2026-10-27｜after-found
c27｜Google：「連結的應用程式」頁 → 有權存取您的 Google 帳戶 → 選應用程式 → 查看詳細資料 → 移除存取權 → 確認｜https://support.google.com/accounts/answer/13533235?hl=zh-Hant｜2026-10-27｜accounts
c28｜GitHub：頭像 → Settings → Integrations 的 Applications → Authorized OAuth Apps，不認得或過時的按 Revoke｜https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/reviewing-your-authorized-oauth-apps｜2026-10-27｜accounts
c29｜Microsoft 的立即行動：分別檢視服務主體（service principal）成功與失敗的登入；檢視應用程式或服務主體的認證新增、權限與角色指派｜MS〈Immediate actions〉｜2026-10-27｜m365
c30｜91APP：實際受影響範圍尚待確認，預計「下週」公布進一步結果；旁白說「之後才公布」｜91APP 新聞稿；iThome 179923｜2026-10-27｜unknown
c31｜資安署透露 7 月監測到類似 AI 攻擊活動，已預警並完成處置；沒有說是哪一套工具｜iThome 179865（新聞稿只寫「國內公私部門亦面臨備用與測試系統遭刺探風險」）｜2026-10-27｜unknown
c32｜資安署建議：離職當天停用帳號並定期清理閒置帳號，每季覆核權限。「金鑰設期限」是站主看法，依據是 Zeabur 報告說管理權杖「沒有期限」，卡片來源寫「期限：站主看法」｜資安署新聞稿〈重點一・嚴密帳號管理〉｜2026-10-27｜three-things

c33｜署長說容易受駭的對象包括較容易支付贖金者、防禦能力較弱者、開放大量對外服務者（旁白取後兩項；原話是「包括」三項，verify-2 把旁白 kwax「容易被打的，是…」改成「容易被打的，包括…」，免得聽成只有這兩種）｜https://www.ithome.com.tw/news/179865｜2026-10-27｜cheap
## 本片自己跑的紀錄

機器：Ubuntu 24.04.5 LTS；git version 2.43.0；ls (GNU coreutils) 9.4；grep (GNU grep) 3.11。日期 2026-10-27（第一次 2026-10-26，指令較長，沒上卡）。
指令稿 `_tools/run/run.sh`，提交者與時間固定（GIT_AUTHOR_DATE 2026-09-01、09-02），倉庫內 `git config commit.gpgsign false`（第一次跑時沿用了這台主機的全域簽章設定，提交編號因此只在這台主機重現；verify-1 抓到後改成不簽章重跑），提交編號 a6036e8（add db config）、5f37a2a（remove secrets from repo）在任何機器上都能重現；密碼是假的 `demo-not-a-real-secret`。逐字輸出 `_tools/run/transcript-20261027-unsigned.txt`（舊的簽章版留在 `transcript-20261027.txt`，不上卡）。

r1｜輸入：示範倉庫提交 `.env`（DB_HOST、DB_PASSWORD 兩行），下一次提交 `git rm .env` 並把 `.env` 寫進 `.gitignore`｜run.sh｜2026-10-27｜ls
r2｜`ls -A` → `.git`、`.gitignore`｜transcript｜2026-10-27｜ls
r3｜`grep -rn PASSWORD --exclude-dir=.git . || echo "not found"` → `not found`（預期：找不到；觀察：找不到）｜transcript｜2026-10-27｜grep
r4｜`git log --oneline -G PASSWORD` → `5f37a2a remove secrets from repo`、`a6036e8 add db config`（預期：列出動過那一行的兩次提交；觀察：一致）｜transcript｜2026-10-27｜gitlog
r5｜`git show a6036e8:.env` → `DB_HOST=orders-db.internal`、`DB_PASSWORD=demo-not-a-real-secret`（觀眾猜不到的結果：刪掉且忽略之後，整個檔案原樣回來）｜transcript｜2026-10-27｜gitshow
r6｜`git log --oneline -G API_KEY` → 沒有任何輸出（code 卡的說明改成「沒有任何輸出，代表目前分支的歷史裡沒有這個字」：git log 沒給範圍時預設 HEAD，只看目前分支，見 https://git-scm.com/docs/git-log；verify-1 也跑了 -G SECRET，同樣沒有輸出）｜transcript；git-log 文件｜2026-10-27｜your-line

## 與企劃不同的地方

- 片長估 9.5 分鐘（企劃寫 8–9），`target_minutes` 改成 [8, 10]；沒有為了壓長度刪事實。
- 時間線卡只寫日期不寫 UTC 時刻：91APP 的「10 月 3 日 11 時」沒寫時區，混著寫會錯。
- 第 4 章的 Zeabur 說法改成「報告沒有提到 ARTEX，也沒說攻擊者用了 AI 工具」（企劃寫「沒提 AI」，但報告有提到攻擊者在找 AI 服務的金鑰）。
- 示範改用四個短指令（`ls -A`、`grep … || echo`、`git log --oneline -G`、`git show`），企劃裡 `git log -p` 的輸出有 20 行，終端機卡放不下 8 行以上。
- 留言題併進 outro（lint 要求片尾三句：答案、留言題、訂閱）。
- 縮圖大字「撿鑰匙／不撬鎖」（六個字以內、不重複標題）。

## 我懷疑但沒動的事

- 「沒有兩步驟驗證可以擋」是從 "without requiring an interactive user sign-in" 推出來的，Microsoft 原文沒寫 MFA；查核時請判斷這樣說是否過度。
- 署長「AI 會放棄扎實的企業」只有媒體轉述（iThome），新聞稿沒有；卡片 kicker 寫「資安署署長，記者會」，說明欄寫 iThome。
- ARTEX 在 lexicon 念「阿特克斯」、Zeabur、Appsmith、ConnectWise 照英文念：試聽時要聽。
- 韓國「逾 6 萬筆」是資安署新聞稿的數字；iThome 另寫「至少 7 家金融機構」，片中沒用 7 家。

## 進度

- 2026-10-27 說故事關卡（盲讀，三位各自沒讀過別的東西的讀者）：第一讀 9 題沒過、第二讀 7 題、第三讀 7 題（必答）。兩輪改寫：開場只留停在結果之前的預告；刪掉「接下來」目錄句、韓日案例清單（month）與日期時間線（timeline），所以 c7、c8、c15、c16 不再出現在片中（說明欄與 sources 一併拿掉 GMO 兩筆）；第 4 章直接接 91APP 的路線，再用「還不是放得最隨便的」接 Zeabur；第 6 章不再編號「第一步…」；第 7 章第一句接住上一章；片尾不再重講十五萬次。第三讀還沒過的：no_spoiler（[vbbm] 預告一行拿回密碼）、one_line（[2yvb]）、no_toc（[v5t8]）、chapters_link（[kj3y]）、payoffs（[txje]）、no_recap（[wkg5] 與 [urua]）、no_detour（Zeabur 段）；其中 no_toc、chapters_link 的判定與第二讀相反。照 SKILL.md 主幹 4.5「最多兩輪，再不過才給站主」交站主決定。估 8.4 分鐘、92 句，lint 0 錯誤 0 警告。

- 2026-10-27 verify-1 之後（撰稿者）：示範改成不簽章重跑、卡片換成 a6036e8／5f37a2a；spray 卡的順序改成跟旁白同步（標題放 8 個組織、327 個帳號）；kwax 改成署長的原話（防禦弱、對外服務開得多）；GMO 改「一組攻擊主機」；時間線那一列就說 Zeabur 報告未提 ARTEX，第 4 章那句改成回呼；「隔天」改「緊接著」（Microsoft 10-21 美國時間發文＝台灣 10-22 凌晨）；「沒人記得的金鑰」改「放在程式碼倉庫裡的金鑰」；urui 縮到 34 字。

- 2026-10-27：37 景、102 句全部寫完，lint 0 錯誤 0 警告，估 9.5 分鐘。等查核（verify-1）。
- 2026-10-27 verify-1：另一個代理逐來源查核，改了 7 處事實（標題與開場卡「不猜密碼」→「不靠猜密碼」、署長的話不寫「記者會」、ConnectWise 10/16 是入侵嘗試、Google 例外之一、git log 只看目前分支、說明欄刪「同時」、說明欄 Zeabur 的寫法），新增三個來源；lint 0 錯誤。細節在 verify-1.md，需要第二輪查核。
- 2026-10-27 verify-2：第三個代理重抓所有來源（全部 HTTP 200；GMO 一手部落格仍轉到首頁），重跑示範（不簽章，提交編號 a6036e8／5f37a2a 在保留與隔離主機 git 設定兩種情況都重現，四張終端機卡逐位元組相符）。改了 1 處事實：kwax「容易被打的，是…」→「容易被打的，包括…」（署長列了三種，旁白只取兩種）。其餘 verify-1 改過的 7 處、撰稿者在 verify-1 之後改的各處、抽查的 19 列都成立。細節在 verify-2.md。
