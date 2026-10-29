# frontend-keys-ai-reverse-engineering：查核第 1 輪

查核者：獨立查核代理（不是撰稿者），2026-10-28 開始、2026-10-29（UTC）結束。官方頁用頻道 UA 重新抓，原始 HTML 與去標籤文字在
工作區 `frontend-keys-ai-reverse-engineering/_tools/verify1/src/`；抽出的主張清單在 `_tools/verify1/dump.txt`，卡片比對腳本是
`cards.py`（code 卡對 `_demo/`、terminal 卡對 `runlog.txt`）與 `fold.py`（ai-run 的折行）。網路搜尋 0 次。

## 來源（今天開的）

| 代號 | URL | HTTP | 抓取日 |
|---|---|---|---|
| S1 | https://vite.dev/guide/env-and-mode | 200 | 10-28 |
| S2 | https://vite.dev/config/build-options | 200 | 10-28 |
| S3 | https://vite.dev/config/shared-options | 200 | 10-28 |
| S4 | https://vite.dev/config/ | 200 | 10-28 |
| S5 | https://nextjs.org/docs/app/guides/environment-variables | 200 | 10-28 |
| S6 | https://nextjs.org/docs/app/api-reference/config/next-config-js/productionBrowserSourceMaps | 200 | 10-28 |
| S7 | https://nextjs.org/docs/app/guides/data-security | 200 | 10-28 |
| S8 | https://nextjs.org/docs/app/api-reference/cli/next | 200 | 10-28 |
| S9 | https://firebase.google.com/docs/projects/api-keys （Last updated 2026-10-20 UTC） | 200 | 10-28 |
| S10 | https://docs.stripe.com/keys | 200 | 10-28 |
| S11 | https://supabase.com/docs/guides/getting-started/api-keys | 200 | 10-28 |
| S12 | https://developers.google.com/maps/api-security-best-practices （Last updated 2026-10-28 UTC） | 200 | 10-28 |
| S13 | https://developers.openai.com/api/reference/overview | 200 | 10-28 |
| S14 | https://support.claude.com/en/articles/9767949-api-key-best-practices-keep-your-keys-safe-and-secure | 200 | 10-28 |
| S15 | https://code.claude.com/docs/en/cli-reference | 200 | 10-28 |
| S16 | https://code.claude.com/docs/en/tools-reference | 200 | 10-29 |
| S17 | https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/typescript （/docs/en/api/sdks/typescript 轉址過來） | 200 | 10-29 |
| S18 | https://www.youtube.com/results?search_query=REA%20%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B&sp=CAM%3D&hl=zh-TW&gl=TW （`_tools/verify1/yt-q6.json`） | 200 | 10-29 |
| S19 | https://www.gnu.org/software/grep/manual/grep.html （第一次連線被重設，重試 200；手冊是 3.12 版） | 200 | 10-29 |
| S20 | https://man.freebsd.org/cgi/man.cgi?query=grep&sektion=1 | 200 | 10-29 |
| S21 | https://nodejs.org/docs/latest-v22.x/api/cli.html | 200 | 10-29 |
| R | 工作區 `runlog.txt`（`=== run N`）與 `_tools/runs.sh` | — | — |
| D | 工作區 `_demo/` 的示範檔 | — | — |

## 主張表

| # | 主張 | 在哪裡 | 來源 | HTTP | 判定 | 前 → 後 |
|---|---|---|---|---|---|---|
| 1 | 金鑰沒推上 GitHub，網站上卻有三把；一行指令找出來 | youtube.title | R r1、r2 | — | CONFIRMED | |
| 2 | 搜過 dist 嗎／金鑰沒進 git，卻在網站上 | thumbnail | R r1、r2 | — | CONFIRMED | |
| 3 | tags | youtube.tags | — | — | OUT OF SCOPE | |
| 4 | .env 在 .gitignore，上線前在 repo 搜 sk 開頭 | vam6、open-title | R r1 | — | CONFIRMED | |
| 5 | `git grep -n "sk-"` 沒有任何輸出 | open-compare.left、9w6h | R r1（exit 1） | — | CONFIRMED | |
| 6 | dist 裡有 sk-demo、pk_test、AIza 三把；同一把還多兩把 | open-compare.right、pabv、7uad | R r2 | — | CONFIRMED | |
| 7 | 瀏覽器拿到的是 build 結果；VITE 變數原樣寫進去；開 source map 連註解送出 | open-why、43i7、24wj | S1、R r2、r3 | 200 | CONFIRMED | |
| 8 | 這兩週好幾支 AI 拆解軟體的影片都有幾十萬次觀看 | open-stakes、fj49 | S18 | 200 | CONFIRMED | 今天：Eric Tech 388,003、程序员鱼皮 259,099、Nate Herk 235,552、AI懶人報 167,981、P & H 167,893，都標 2 週前／13 天前 |
| 9 | 別人的 AI 幾分鐘就讀完你整包 JavaScript | open-ai-reads、htah | s1（站主觀點） | — | OUT OF SCOPE | 見〈觀點〉 |
| 10 | 一個 31 行的伺服器檔 | open-promise、phdf | R r5（`wc -l` 31） | — | CONFIRMED | |
| 11 | .env 四行全假，前三行 VITE_ 開頭 | env-file.data.code、qjxv、999v | D shop-chat/.env | — | CONFIRMED | |
| 12 | main.js 第 1–3 行（共 12 行）；第二行讀 VITE 那把、第三行讀沒前綴那把 | main-top、wu79、c3jb | D | — | CONFIRMED | |
| 13 | git status `!! .env`；git grep exit 1 | repo-check.data.steps | R r1 | — | CONFIRMED | |
| 14 | `npm run build` 兩行輸出；vite/8.3.4 | build（terminal） | R r1、versions | — | CONFIRMED | 逐字（節錄） |
| 15 | 照開頭搜 dist：三把在同一檔第 1 行 | grep-shape（terminal）、u6r6、z5xy | R r2 | — | CONFIRMED | 逐字 |
| 16 | VITE_* 不該放 API 金鑰（"VITE_* variables should not contain sensitive information such as API keys."） | vite-page、w2wy | S1 | 200 | CONFIRMED | |
| 17 | "The values of these variables are bundled into your source code at build time." 與譯文 | vite-quote、zps2、mc2b | S1 | 200 | CONFIRMED | |
| 18 | `grep -rn OPENAI_API_KEY dist/` 零筆 | name-search、jbq6 | R r2（exit 1） | — | CONFIRMED | |
| 19 | 變數名換成一個字母，值原樣在等號後 | var-e（terminal）、hzg4、pce7 | R r2 | — | CONFIRMED | 逐字 |
| 20 | sed＋grep 一行搜值，三把、標出行號；換掉 dist | grep-values（terminal）、9k8a、pff7、ime3、bbyp | R r2 | — | CONFIRMED | 逐字 |
| 21 | `--sourcemap` 多出 map 檔 | sourcemap（terminal）、vzeu | R r3 | — | CONFIRMED | 逐字（節錄） |
| 22 | map 檔裡的 TODO 原封不動 | todo（terminal）、54zf、rfa2 | R r3 | — | CONFIRMED | 逐字 |
| 23 | Vite 與 Next.js 正式版預設不產生瀏覽器 source map；Next 原句與譯文 | srcmap-quote、tz2b | S2（Default: false）、S6 | 200 | CONFIRMED | |
| 24 | 寫死的權杖在 main.js 第 3 行（共 13 行），第 8 行放進 X-Admin-Token | admin-line | D、R r7 | — | CONFIRMED | |
| 25 | 重 build 後兩種搜尋都只有原來三把 | admin-miss（terminal）、tzdq、2asv | R r7 | — | CONFIRMED | 逐字 |
| 26 | 讓 AI 讀之前先決定它能做什麼：不用問就能用的只給讀取類工具 | ai-trust、dn4h | S15（--allowedTools＝"Tools that execute without prompting for permission"） | 200 | CONFIRMED | 建議句；見〈懷疑但沒動〉 |
| 27 | 要求句（原檔一行，卡片依寬度換行） | ai-prompt、ai-prompt-2、nrc4、fbvx | D review-prompt.txt、R r7 | — | CONFIRMED | 去掉換行後逐字相同 |
| 28 | `claude -p … --allowedTools "Read,Grep,Glob"`；2.1.312 (Claude Code) | ai-run.command、tool_version | R r7 | — | CONFIRMED | |
| 29 | demo-admin 那一列折成兩行 | ai-run.data.output | R r7 | — | CONFIRMED | 拿掉換行後跟 runlog 那一列逐字相同（96 字、134 欄）；折點在第 77 欄，正是 78 欄終端機自動折行的位置 |
| 30 | 「不用問就能用的只有三個：讀取檔案、搜尋內容、照檔名找檔案」 | jkfs | S16、S15 | 200 | CHANGED | Read／Grep／Glob 的 Permission required 本來就是 No，Agent、Task 系列等也是 No，Bash 的內建唯讀指令也不問；這個旗標只是把這三個列進免詢問清單（在 Linux 上點名 Grep／Glob 還會把它們加回預設工具組）。「不用問就能用的只有三個：…」→「指令裡預先允許的只有三個：…」 |
| 31 | ai-run 的 key「不用問的工具：只給三個讀取類」 | ai-run.data.keys[0] | S16 | 200 | CHANGED | →「預先允許：只列三個讀取類工具」 |
| 32 | 用不開對話的模式，跑一次就結束 | jkfs | S15（"-p Print response without interactive mode"；"Query via SDK, then exit"） | 200 | CONFIRMED | |
| 33 | 表裡多了兩行 grep 都沒找到的那一個 | 3cgv | R r7 | — | CONFIRMED | |
| 34 | 四列表：sk-demo 不能、demo-admin 不能、pk_test 可以、AIza 視情況 | ai-table、yfdt、tsqd、4wbg、krds | R r7 | — | CONFIRMED | 節錄，格子的字取自原表 |
| 35 | Stripe pk 開頭的 publishable key 給前端用 | public-keys row 1、8vbt | S10（"Only publishable keys are safe to expose outside your application's backend."；pk_test_／pk_live_） | 200 | CONFIRMED | |
| 36 | Firebase 網頁金鑰只開 Firebase 服務就不必當祕密 | public-keys row 2、krnj | S9（"API keys restricted to Firebase services do not need to be treated as secrets"） | 200 | CONFIRMED | |
| 37 | Supabase publishable（舊名 anon）讀得到什麼由 RLS 決定 | public-keys row 3、w4tb | S11（"Anyone can read it, so it only reaches what Row Level Security allows"；anon＝"Legacy version of publishable keys"） | 200 | CONFIRMED | |
| 38 | Google Maps 網頁用的金鑰靠限制網站來源保護；列在「設計上可以公開的」 | public-keys row 4、3mtx | S12（Websites application restriction；"if the key is publicly exposed on your web page"） | 200 | CONFIRMED | 分類是推論，見〈懷疑但沒動〉 |
| 39 | OpenAI 的 API 金鑰不能出現在瀏覽器或 App 裡 | secret-keys row 1、fmfm | S13（"Don't share it with others or expose it in any client-side code such as browsers or apps."） | 200 | CONFIRMED | |
| 40 | Anthropic 的 API 金鑰同一列：不能出現在瀏覽器或 App 裡 | secret-keys row 1、fmfm | S17（"disabled by default to avoid exposing your secret API credentials"；dangerouslyAllowBrowser "exposes your secret API credentials in the client-side code"）、S14（"Keep it confidential"） | 200 | CONFIRMED | 瀏覽器有 Anthropic 原句；「App」是 OpenAI 的原句，Anthropic 那邊靠 S14 "Never include it directly in your code"。sources 加 S17 |
| 41 | Stripe sk 開頭的祕密金鑰只能留在後端 | secret-keys row 2、gq45 | S10 | 200 | CONFIRMED | |
| 42 | Supabase secret（舊名 service_role）會略過 RLS | secret-keys row 3、36cr | S11（"It bypasses Row Level Security"；service_role＝"Legacy version of secret keys"） | 200 | CONFIRMED | |
| 43 | "never include the Gemini Developer API in the allowlist for a publicly accessible API key"；2026-10-20 更新；要用 Gemini 另做一把 | firebase-quote、k67d、h5by、8j2k | S9 | 200 | CONFIRMED | |
| 44 | 公開的限制、祕密的搬走 | rule-big、cbt5 | s1 | — | OUT OF SCOPE | 觀點，與企劃一致 |
| 45 | 套回 shop-chat：Stripe 留、Firebase 留並限制、OpenAI 搬走 | shop-three | s1、S9、S10、S13 | 200 | CONFIRMED | |
| 46 | 現在瀏覽器帶金鑰直打 OpenAI；改成伺服器加金鑰轉送 | before-after、d4gj、2r49 | D shop-chat、fixed | — | CONFIRMED | |
| 47 | fixed/.env 三行，OpenAI 那行拿掉前綴 | fixed-env、umuu | D | — | CONFIRMED | |
| 48 | fixed/src/main.js 第 1–7 行（共 8 行），fetch 改 /api/chat | fixed-main、ura6 | D、R r5 | — | CONFIRMED | |
| 49 | server.mjs 31 行、只用 Node.js 內建模組；第 4–5、10–12、17、21–22、24–31 行的說明 | server-1a/1b/2a/2b/3、88z9、ctv3、c87u、dn6k、r9cx、xrzz、gq8y | D | — | CONFIRMED | 只 import node:http、node:fs/promises；fetch、URL 是全域 |
| 50 | 在 8787 埠等請求 | server-3、cpss | D | — | CONFIRMED | |
| 51 | 啟動：UPSTREAM_URL…、node --env-file=.env、server.mjs；假上游只回答有沒有收到金鑰 | start-parts、47nr、3s45 | runs.sh 第 28 行、D mock-upstream.mjs、S21（--env-file "Loads environment variables from a file … available to applications on process.env"） | 200 | CONFIRMED | |
| 52 | 拿原本四個值再搜：只剩 Stripe、Firebase | fixed-grep（terminal）、yzzc、8y8f | R r5 | — | CONFIRMED | 逐字 |
| 53 | curl POST /api/chat → {"got_key":true} | fixed-curl（terminal）、a6t3、m7n3 | R r5 | — | CONFIRMED | 逐字 |
| 54 | 搜不到祕密那把、功能照常 | done-big、u5vn | R r5 | — | CONFIRMED | |
| 55 | "By default, environment variables are only available on the server."；沒前綴只在伺服器 | next-env-quote、22v7、ss2k、t7gx | S5、R r6 | 200 | CONFIRMED | |
| 56 | page.jsx 全檔 4 行，把金鑰當參數傳給 Chat | next-page、m277 | D、R r6 | — | CONFIRMED | |
| 57 | `.next/static` 搜不到；Next.js 16.4.2 | next-static、kv4t | R r6（exit 1） | — | CONFIRMED | |
| 58 | curl 首頁 grep apiKey → 金鑰在頁面裡，反斜線是跳脫的引號 | next-curl（terminal）、gkv2、zhq8、scs6 | R r6 | — | CONFIRMED | 逐字 |
| 59 | "…accidentally expose private data through how data is fetched or passed to components" | next-datasec、x4yr、t7da | S7 | 200 | CONFIRMED | |
| 60 | 也要搜訪客拿到的頁面 | check-page、tqz6 | R r6 | — | CONFIRMED | |
| 61 | route.js 14 行，兩張卡第 1–7、8–14 行 | route-1、route-2、bqcq、2rm9 | D、R r6b | — | CONFIRMED | |
| 62 | chat.jsx 全檔 8 行，改打 /api/chat | next-chat、dgx8 | D、R r6b | — | CONFIRMED | |
| 63 | 修好後 grep -c → 0 | next-fixed-curl（terminal）、hfq3、qyjm | R r6b | — | CONFIRMED | 逐字 |
| 64 | loadEnv 第三參數 '' 讀全部變數；define 在 build 時替換 | define-table、789w、ku9y | S4（"Set the third parameter to '' to load all env regardless of the `VITE_` prefix."）、S3（"statically replaced during build"）、D | 200 | CONFIRMED | |
| 65 | define-case 搜出四把 | define-grep（terminal）、cywb、nnhu | R r4 | — | CONFIRMED | 逐字 |
| 66 | 舊的那把已送出去，重新 build 收不回，換新的 | old-key、62hq、e6vq | s1 | — | OUT OF SCOPE | 觀點，與企劃一致 |
| 67 | Stripe 輪替：撤銷舊的、給馬上能用的新金鑰 | rotate step 1、e6fa | S10（"Rotating an API key revokes it and generates a replacement key that's ready to use immediately."） | 200 | CONFIRMED | |
| 68 | OpenAI 撤銷幾秒內生效 | rotate step 2、675b | S13（"Revocations of an API key take effect within a few seconds."） | 200 | CONFIRMED | |
| 69 | 新的只放伺服器的環境變數 | rotate step 3、dku5 | S13（"Load API keys from an environment variable or key management service on the server."） | 200 | CONFIRMED | |
| 70 | Maps 限定你的網站；Firebase 只開自家服務；Supabase 資料表開 RLS | restrict、4nyd、dgjv、43gp | S12、S9、S11（"Row Level Security decides what this client can reach, so enable it on every table before you deploy."） | 200 | CONFIRMED | RLS 找到官方原句 |
| 71 | 剛剛那行 curl 沒開瀏覽器沒登入也拿到回應；伺服器檔不管誰能打 | endpoint-a、3agd、z2v4 | R r5、D | — | CONFIRMED | |
| 72 | 看用量和紀錄頁；能自訂速率的組織設花費與速率上限；標準的組織開自動儲值門檻小心設 | limits、pjbd、evbx、dh5p | S14 | 200 | CONFIRMED | 「標準方案的組織」是 "standard rate limit API orgs" 的意譯 |
| 73 | 我的看法／我照樣用 AI／我不知道／收尾 | my-view、my-ai、unknown、closing | s1、s2 | — | OUT OF SCOPE | 觀點，與企劃一致 |
| 74 | 執行環境：Linux、Node v22.22.0、vite/8.3.4、Next.js 16.4.2（Turbopack）、GNU grep 3.11、curl 8.5.0、Claude Code 2.1.312 | description | R versions、r6、r7 | — | CONFIRMED | |
| 75 | 指令 1、2、3、5 | description | R、runs.sh | — | CONFIRMED | 逐字 |
| 76 | -P 是 GNU grep 的選項；其他系統先 grep --version | description 第 2 條 | S19（-P／--perl-regexp，要系統有 PCRE）、S20（FreeBSD grep 沒有 -P） | 200 | CONFIRMED | |
| 77 | 第 4 條「讓 Claude Code 只用讀取類工具讀 dist/」 | description 第 4 條 | S16、S15 | 200 | CHANGED | →「讓 Claude Code 讀 dist/，預先允許的只列讀取類工具」；括號補「Read、Grep、Glob 在工作目錄裡本來就不用問，其他免問的工具照樣能用」 |
| 78 | route.js 全文 14 行 | description | D | — | CONFIRMED | 逐字 |
| 79 | 分類段；Supabase 2026 年底前淘汰 anon、service_role | description | S9–S14、S11（"Supabase is deprecating the anon and service_role keys by the end of 2026"） | 200 | CONFIRMED | |
| 80 | server.mjs 只做到金鑰不在瀏覽器 | description | D、R r5 | — | CONFIRMED | |
| 81 | sources | sources | S16、S17 | 200 | CHANGED | 加了 S16、S17 兩筆（checked_on 2026-10-29） |

## 摘要

- 查了 81 項：CONFIRMED 70、CHANGED 4（#30、#31、#77、#81，都是同一個事實：`--allowedTools` 的範圍）、NOT FOUND 0、OUT OF SCOPE 7。
- **事實改動：1 個**（`--allowedTools "Read,Grep,Glob"` 不等於「不用問就能用的只有三個」）。改到的地方：旁白 jkfs、ai-run 的 key、說明欄第 4 條、sources。
- 撰稿者的 6 個疑點：(1) Anthropic 跟 OpenAI 同列：成立，Anthropic 的 TypeScript SDK 頁有原句（瀏覽器預設關閉，以免把 secret API credentials 露在用戶端），已加進 sources 與 c10b；(2) RLS：Supabase 有原句 "enable it on every table before you deploy"，成立。Maps「可以公開」：Maps 頁沒有這句話，但有 "if the key is publicly exposed on your web page" 和 Websites 限制，所以留著；(3) `--allowedTools`：改了，見上；(4) ai-run 折行：一個字都沒改，折點跟 78 欄終端機自己折的位置一樣；(5) GNU grep 註記：成立（FreeBSD grep(1) 沒有 -P）；(6) Supabase 命名（anon＝publishable 的舊版、service_role＝secret 的舊版）與 "by the end of 2026" 都成立。
- 很快會過期的事：Supabase 舊金鑰「2026 年底前」淘汰（S11）；YouTube 觀看數與「這兩週」（S18，10-29 的數字）；Maps 頁 Last updated 2026-10-28（企劃記的是 10-27，已改 claims.md c8）；Firebase 頁 Last updated 2026-10-20；Claude Code 的 Glob／Grep 預設工具組行為（S16）會隨版本變。
- 觀點不一致：沒有內容衝突。開場 htah「以前要有人慢慢翻；現在別人的 AI，幾分鐘就讀完…」是企劃裡的站主觀點，旁白卻用直述句講、沒有標成觀點，「幾分鐘」也沒有計時。只回報，沒改。
- 聽眾檢查：超過 40 字的句子有 vam6（44）、jkfs（45）、w4tb（45）、fmfm（48）、36cr（41）、22v7（44）、4nyd（41）、7zxx（44），除了 36cr 都有逗號或分號斷開；旁白裡沒有「經查證、根據官方文件、本影片」，沒有括號，沒有網址；lint 沒有提出不在發音詞典裡的拉丁字；揭示順序沒問題。
- lint：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug frontend-keys-ai-reverse-engineering` 0 errors、0 warnings（12.3 分鐘、136 句）。第一次改完說明欄是 5,001 bytes，超過上限，把補的那句縮短後通過。
- 懷疑但沒改：
  - ai-trust 的「先決定它能做什麼」：`--allowedTools` 不會限制工具，真正拿掉工具要用 `--tools`（說明欄有寫）。這次在 Linux 上點名 Grep／Glob，作用是把這兩個工具加回來並免詢問。站主如果要旁白說到「限制」，要改用 `--tools "Read,Grep,Glob"` 重跑 r7。
  - Maps 列在「設計上可以公開的」：內文支持把限制過的金鑰放在網頁上，但頁首自動產生的 Page Summary 寫 "never exposing them directly in client-side code"；Google 也說一定要同時加 API 限制，卡片只講網站限制。
  - Anthropic 的「或 App 裡」是借 OpenAI 的原句推來的；Anthropic 的 SDK 頁說內部工具、短期除錯這兩種情況風險不大。
  - krnj 沒提 Firebase 的前提：要照指引設好 Security Rules 與 App Check。
  - dh5p 的「標準方案」：原文是 standard rate limit，不是一種方案。
- 要不要第 2 輪：**不用**（這輪事實改動 1 個，沒有超過 3 個）。
