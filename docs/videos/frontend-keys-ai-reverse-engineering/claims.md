# frontend-keys-ai-reverse-engineering：可查核的主張

撰稿 2026-10-28（選項 A，站主觀點照企劃）。每一行：編號｜主張（旁白或卡片上的說法）｜來源｜確認日期｜場景。
官方頁是 2026-10-28 用頻道 UA 抓下的原始 HTML，存在工作區 `frontend-keys-ai-reverse-engineering/_tools/sources/`（檔名寫在每一行最後）；
`r` 開頭的是這支片的執行紀錄，全部在工作區的 `frontend-keys-ai-reverse-engineering/runlog.txt`，以 `=== run N` 段落為準；
示範專案的原始檔在同一個工作區的 `_demo/`，`code` 卡逐字取自這些檔案。

## 事實（引用）

c1｜`VITE_` 開頭的變數在 Vite 打包後會出現在用戶端原始碼；`VITE_*` 變數不該放 API key 這類敏感資訊；原句 "The values of these variables are bundled into your source code at build time."（卡片引這一句，譯「這些變數的值，會在 build 時打包進你的原始碼」）；同頁 `DB_PASSWORD` 沒前綴不會送到用戶端｜https://vite.dev/guide/env-and-mode （Protecting secrets 警告框；`vite-env.html`）｜2026-10-28｜open-why、vite-page、vite-quote
c2｜這兩週好幾支「AI 拆解軟體」（REA）的影片都有幾十萬次觀看：Rob Shocks〈The Fastest-Rising Repo on GitHub Is a Little Scary REA〉498,553 次、2 週前；Eric Tech〈How To Use REA To Clone Any Software In Minutes〉385,963 次、2 週前；程序员鱼皮 256,248 次、13 天前；AI懶人報 167,670 次、2 週前；midudev〈La ingeniería inversa se volvió demasiado fácil〉555,085 次、7 天前。旁白只講「好幾支、都有幾十萬次」｜https://www.youtube.com/results?search_query=REA%20%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B&sp=CAM%3D&hl=zh-TW&gl=TW （`_tools/search/q6.json`）；midudev 那支在 `q4.json`｜2026-10-28｜open-stakes
c3｜Vite `build.sourcemap` 預設 `false`｜https://vite.dev/config/build-options （`vite-build.html`）｜2026-10-28｜srcmap-quote
c4｜Next.js 正式版 build 預設不產生瀏覽器 source map，原句 "During production builds, they are disabled to prevent you leaking your source on the client"｜https://nextjs.org/docs/app/api-reference/config/next-config-js/productionBrowserSourceMaps （`next-srcmap.html`）｜2026-10-28｜srcmap-quote
c5｜Stripe："Only publishable keys are safe to expose outside your application's backend."；沙盒金鑰 publishable 以 `pk_test_`、secret 以 `sk_test_` 開頭，正式環境 `pk_live_`／`sk_live_`；publishable key 不敏感｜https://docs.stripe.com/keys （Protect your keys、`stripe.html`）｜2026-10-28｜public-keys、secret-keys、shop-three
c6｜Firebase：設定符合指引時，只限 Firebase 服務的 API key 不必當祕密、可以放進程式碼；Firebase 提供的金鑰只用於 Firebase 相關 API，其他 API 用另一把、各自限制；原句 "never include the Gemini Developer API in the allowlist for a publicly accessible API key"；頁面 Last updated 2026-10-20｜https://firebase.google.com/docs/projects/api-keys （`firebase.html`）｜2026-10-28｜public-keys、firebase-quote、shop-three、restrict
c7｜Supabase：publishable key「Anyone can read it, so it only reaches what Row Level Security allows」；secret key 會略過 RLS（"bypassing Row Level Security"）、只用在後端；anon、service_role 是舊版的 publishable、secret；"Supabase is deprecating the anon and service_role keys by the end of 2026"（淘汰日期只在卡片的「舊名」與說明欄，旁白在撰稿第 3 輪拿掉了）｜https://supabase.com/docs/guides/getting-started/api-keys （企劃寫的 /docs/guides/api/api-keys 會轉址到這裡；`supabase.html`）｜2026-10-28｜public-keys、secret-keys、restrict
c8｜Google Maps Platform：API key 可加 application restriction，類型 Websites＝指定一個或多個 referrer 網站，之後只有這些來源的請求被允許；頁面 Last updated 2026-10-27（企劃記錄）｜https://developers.google.com/maps/api-security-best-practices （`maps.html`）｜2026-10-28｜public-keys、restrict
c9｜OpenAI："Remember that your API key is a secret. Don't share it with others or expose it in any client-side code such as browsers or apps. Load API keys from an environment variable or key management service on the server."｜https://developers.openai.com/api/reference/overview （Authentication 一節；`openai-auth2.html`）｜2026-10-28｜secret-keys、shop-three、rotate
c10｜Anthropic：API key 是帳戶的數位鑰匙，別人拿到就以你的名義產生費用；要保密（keep it confidential）；交給第三方時當加密 secret，"Never include it directly in your code or configuration files"｜https://support.claude.com/en/articles/9767949-api-key-best-practices-keep-your-keys-safe-and-secure （企劃寫的 keeping-… 網址會轉到這個 canonical；`anthropic.html`）｜2026-10-28｜secret-keys
c11｜Next.js："By default, environment variables are only available on the server. To expose an environment variable to the browser, it must be prefixed with NEXT_PUBLIC_."；`NEXT_PUBLIC_` 的值在 `next build` 時 inline 進送到瀏覽器的 JavaScript｜https://nextjs.org/docs/app/guides/environment-variables （`next-env.html`）｜2026-10-28｜next-env-quote
c13｜Next.js Data Security：Server Components 的寫法 "it's possible to accidentally expose private data through how data is fetched or passed to components"（卡片引從 accidentally 開始的子句）｜https://nextjs.org/docs/app/guides/data-security （`next-datasec.html`）｜2026-10-28｜next-datasec
c14｜Vite `define`："Entries will be defined as globals during dev and statically replaced during build"；`loadEnv` 第三個參數設 `''`「to load all env regardless of the `VITE_` prefix」（官方範例同樣把結果放進 `define`）｜https://vite.dev/config/shared-options （`vite-shared.html`）、https://vite.dev/config/ （`vite-config.html`，撰稿時補抓）｜2026-10-28｜define-table
c15｜Stripe："Rotating an API key revokes it and generates a replacement key that's ready to use immediately."｜https://docs.stripe.com/keys （Rotate an API key）｜2026-10-28｜rotate
c16｜OpenAI："Revocations of an API key take effect within a few seconds."｜https://developers.openai.com/api/reference/overview｜2026-10-28｜rotate
c17｜Anthropic：定期看 Console 的 Logs 與 Usage 頁；custom rate limit 的組織設 spend limits 與 workspace rate limits，"These limits act as a safeguard against unexpected usage due to leaked keys or errant scripts."；standard rate limit 的組織開 auto-reload 時 "Carefully consider auto-reload limits"｜https://support.claude.com/en/articles/9767949-api-key-best-practices-keep-your-keys-safe-and-secure｜2026-10-28｜limits
c18｜Claude Code CLI：`--allowedTools` 是「Tools that execute without prompting for permission」；要限制有哪些工具可用，改用 `--tools`。旁白因此只說「不用問就能用的，只給讀取類的工具」，不說其他工具被拿掉｜https://code.claude.com/docs/en/cli-reference （`cc-cli.html`，撰稿時補抓）｜2026-10-28｜ai-trust、ai-run

（c12 編號空著：原本給 next build 的靜態頁圖例，那一張卡在撰稿第 3 輪為了長度拿掉。）

## 站主觀點與不確定

s1｜站主觀點（brief.md〈站主觀點〉，站主 2026-10-28 選 A 時確認照用）：前端沒有祕密；送到瀏覽器的字都當成貼在公告欄上；以前要有人慢慢翻，現在別人的 AI 幾分鐘就讀完（「幾分鐘」是站主的說法，這支片沒有替 r7 計時）；上線前搜 build 不搜 repo；先分類：公開的去限制、祕密的搬走並換新；照樣用 AI 寫前端，但送到瀏覽器的字自己決定｜brief.md｜2026-10-28｜open-ai-reads、rule-big、shop-three、old-key、my-view、my-ai、closing
s2｜不確定：有多少上線的網站這樣漏了金鑰，沒有可靠的數字，片中不講比例｜brief.md〈站主觀點〉最後一句｜2026-10-28｜unknown

## 這支片自己的執行紀錄（runlog.txt）

環境（`=== versions`）：`vite/8.3.4 linux-x64 node-v22.22.0`、Node v22.22.0、GNU grep 3.11、curl 8.5.0；Next.js v16.4.2（run 6 的 `npx next --version`）；Claude Code 2.1.312（run 7 的 `claude --version`）。金鑰全是假的、故意寫短並帶 FAKE；所有 `curl` 只打 localhost；上游是 `_demo/mock-upstream.mjs`（5 行，聽 8788，只回 `{"got_key": <標頭是否以 Bearer sk- 開頭>}`），不打真的 OpenAI。

r1｜run 1：`shop-chat`。輸入：`.env` 四行（三行 `VITE_` 開頭＋`OPENAI_API_KEY=sk-server-FAKE-1111`）、`.gitignore`（.env、node_modules、dist）、`src/main.js` 12 行。動作：`git init` 並 commit；`git grep -n "sk-"`；`git status --ignored --short`；`npm run build`。預期：git grep 無輸出、`!! .env`、約 1 kB 的 js。實際：git grep 無輸出、exit 1；`!! .env`、`!! node_modules`；`dist/assets/index-jek3iDuZ.js 1.01 kB`。卡片 open-compare 左欄、repo-check（steps，source 標 r1）、build（terminal，tool_version 用 vite 自報的版本）｜runlog.txt `=== run 1`｜2026-10-28｜open-title、open-compare、env-file、main-top、repo-check、build
r2｜run 2：`sed -n 's/^[A-Z_]*=//p' .env | grep -rnoFf - dist/` → 三行（sk-demo、pk_test、AIza），沒有 sk-server；`grep -rn OPENAI_API_KEY dist/` → 無輸出、exit 1（卡片 name-search 是 big，因為空輸出放不進 terminal 卡）；`grep -o 'var e=[^,]*' dist/assets/*.js` → `` var e=`sk-demo-FAKE-0000` ``；`grep -o '[a-z]=void 0'` → `t=void 0`（沒上卡）；`grep -rnoP 'sk-[\w-]+|pk_\w+|AIza[\w-]+' dist/` → 同樣三行｜runlog.txt `=== run 2`｜2026-10-28｜open-compare、open-why、grep-shape、name-search、var-e、search-values、grep-values、open-promise
r3｜run 3：`npm run build -- --sourcemap` → 多一個 `index-jek3iDuZ.js.map`（`map: 1.11 kB`）；`grep -o '// TODO[^\\]*' dist/assets/*.map` → `// TODO: move the OpenAI call to a server before launch`；`grep -c OPENAI_API_KEY` map → 1（沒上卡）；不帶旗標重 build 後 map 不見（沒上卡）｜runlog.txt `=== run 3`｜2026-10-28｜open-why、sourcemap、todo
r4｜run 4：`define-case`，`vite.config.js` 5 行（`loadEnv(mode, process.cwd(), "")`＋`define: { "process.env.OPENAI_API_KEY": JSON.stringify(env.OPENAI_API_KEY) }`），`src/main.js` 第 3 行讀 `process.env.OPENAI_API_KEY`；build 後同一行搜尋 → 四行，多了 `sk-server-FAKE-1111`。第 4 行 90 字元放不進 `code` 卡，所以拆成 `table` 的兩段（第 3–4 行節錄），整個檔沒有上卡｜runlog.txt `=== run 4`｜2026-10-28｜define-table、define-grep
r5｜run 5：`fixed`，`.env` 三行（OpenAI 那行沒有前綴）、`src/main.js` 改打 `/api/chat`、`server.mjs` `wc -l` 31 行；build 後拿 `../shop-chat/.env` 的四個值搜 → 只剩 pk_test、AIza 兩行；`curl -s -X POST localhost:8787/api/chat -d '{"input":"hi"}'` → `{"got_key":true}`；`curl -s localhost:8787/ | grep -c sk-` → 0；`../.env` 與 `%2e%2e/.env` 都回 404（企劃說不上卡片，旁白也沒講）。伺服器的啟動指令 `UPSTREAM_URL=http://127.0.0.1:8788 node --env-file=.env server.mjs` 不在 runlog 裡，是協調者的 `_tools/runs.sh` 第 28 行實際執行的那一行；它 66 字元放不進 `code` 卡，所以 start-parts 用 `table` 拆三段、完整一行在說明欄。endpoint-a 的「沒開瀏覽器、沒登入就拿到回應」就是這個 curl｜runlog.txt `=== run 5`、`_tools/runs.sh`｜2026-10-28｜open-promise、before-after、fixed-env、fixed-main、server-1a、server-1b、server-2a、server-2b、server-3、start-parts、fixed-grep、fixed-curl、done-big、endpoint-a
r6｜run 6：`next-leak`，`.env.local` 一行 `OPENAI_API_KEY=sk-server-FAKE-1111`（沒有 NEXT_PUBLIC_）、`app/page.jsx` 把它當 `apiKey` 傳給 `"use client"` 的 `Chat`；`next build` 用 **Turbopack**（`▲ Next.js 16.4.2 (Turbopack)`，不是企劃寫的 webpack 備案），首頁 `○ (Static)`；`grep -rl "sk-server-FAKE-1111" .next/static` → 無輸出、exit 1（卡片 next-static 是 big）；`curl -s localhost:3000/ | grep -o '"apiKey":"[^"]*"'` → 無輸出（頁面在 RSC 資料裡跳脫引號）；`curl -s localhost:3000/ | grep -o 'apiKey[^}]*'` → `apiKey\":\"sk-server-FAKE-1111\"`（卡片用這一行）｜runlog.txt `=== run 6`｜2026-10-28｜next-env-quote、next-page、next-static、next-curl、check-page
r6b｜run 6b：`next-fixed`，`page.jsx` 改成 `<Chat />`、`chat.jsx` 改打 `/api/chat`、`app/api/chat/route.js` `wc -l` **14 行**（企劃寫 13）；build 後 `.next/static` 搜不到、`curl … | grep -o 'apiKey[^}]*'` 無輸出、`grep -c sk-server-FAKE-1111` → 0、`POST /api/chat` → `{"got_key":true}`（最後這個沒上卡，旁白也沒講）｜runlog.txt `=== run 6b`｜2026-10-28｜route-1、route-2、next-chat、next-fixed-curl
r7｜run 7：`shop-chat-ai`，`src/main.js` 第 3 行 `const ADMIN = "demo-admin-7f3a9c";`、第 8 行放進 `X-Admin-Token`；build 後兩行 grep（搜值、照開頭）都只找到原來三把，沒有 demo-admin；`claude -p "$(cat review-prompt.txt)" --allowedTools "Read,Grep,Glob"`（Claude Code 2.1.312）交回一張表列出四個字串：sk-demo＝OpenAI 祕密 API 金鑰、不能；demo-admin＝應用自家後端的管理權杖、不能；pk_test＝Stripe 可公開金鑰,測試環境、可以；AIza＝Google API 金鑰、視情況；並說沒有修改任何檔案。ai-run 卡的輸出是表裡 demo-admin 那一列，原本一行 134 欄，照 78 欄的終端寬度折成兩行（字一個沒改）；ai-table 的格子是那張表的節錄（「可能是哪家的什麼」欄去掉括號裡的前綴說明）｜runlog.txt `=== run 7`｜2026-10-28｜open-ai-reads、admin-line、admin-miss、ai-trust、ai-prompt、ai-prompt-2、ai-run、ai-table

## 與企劃不同的地方

- 片長：企劃估 685 秒；lint 估 12.3 分鐘（136 句、2,708 個口語單位）。第一版估 14.1 分鐘，砍了三輪，拿掉的是重講與可省的卡（見下），沒有拿掉成果。
- 開場的結果句原本是「整個 repo 搜 sk-，一筆都沒有」，改成「在 repo 裡搜 sk 開頭的金鑰」，因為 run 1 只搜了 `sk-`，不是「搜遍」。
- 開場的時機句不點名 REA 與 midudev（站主：REA 只給一句時機，標題與縮圖不用「駭」「破解」）；旁白說「好幾支 AI 拆解軟體的影片都有幾十萬次」。
- `git grep` 與 `.next/static` 的搜尋沒有輸出，`terminal` 卡要真的輸出，所以這兩個結果放在 `compare`／`steps`／`big` 卡上，source 標那次執行。
- Next.js 是 Turbopack（觀眾的預設），`curl` 卡用 `'apiKey[^}]*'` 那一行（輸出帶反斜線，旁白解釋是跳脫的引號）；企劃的 `'"apiKey":"[^"]*"'` 在紀錄裡沒有輸出，沒用。
- `route.js` 是 14 行（企劃 13），分兩張 `code` 卡（第 1–7、8–14 行）。
- 第 7 項成立，照選項 A 允許的位置放在第 2 章末，當「兩行 grep 都漏掉的那一個」；主例仍是 `shop-chat` 的三把。卡片：寫死那一行（code）、照開頭搜的結果（terminal）、信任檢查（big）、要求句（code 兩張，原檔一行依寬度換行）、claude 指令與 demo-admin 那一列（terminal）、四列表（table）。
- 「只開讀取」改寫成「不用問就能用的，只給讀取類的工具」：Claude Code 的 CLI 說明寫 `--allowedTools` 是免詢問的工具，真正限制可用工具的是 `--tools`；說明欄補了一句。
- Next.js 修好後的 `POST /api/chat` 卡、`next build` 輸出卡、Supabase「貼在大門上」的比喻卡、`mock-upstream.mjs` 的程式卡（第 4 行 70 字元也放不進 `code` 卡）都為了長度拿掉；假上游改在 start-parts 的旁白與表格裡交代。
- `vite.config.js` 第 4 行 90 字元放不進 `code` 卡，改用 `table` 拆兩段（第 3–4 行節錄）；企劃寫的是 `bullets`。
- `server.mjs` 全文 31 行分四張 `code` 卡上（1–12 兩張不同 highlight、13–23 兩張不同 highlight、24–31），企劃寫三張；說明欄不放 server.mjs 全文（YouTube 說明欄不收 `>`，而第 8 行有 `=>`），改寫「全文在第 4 章的卡片上」；route.js 全文放說明欄。
- 第 6 章的「同一個 curl」改成 big 卡回呼 r5，不重放同一張 terminal。
- 企劃的 Stripe〈Protect your keys〉與 Supabase〈Key types〉兩個 screencast 沒做，只做 Vite〈Protecting secrets〉（縮圖的主體）；Stripe 的原句意思已在分類表與 c5，再放一張是重講。
- 第 3 章的 Stripe quote 卡沒做（同上，分類表已有）。
- 「舊的 anon 與 service_role 今年底前淘汰」一句旁白拿掉，留在分類表的「舊名」與說明欄。

## 我懷疑但沒動的事

- ai-run 卡把 Claude Code 一行 134 欄的輸出照 78 欄折成兩行：字沒改，但折行位置是我依卡片寬度算的，不是實際終端機的寬度；查核覺得不妥，可改成只放 `table`（ai-table 已經有同一列）並把 ai-run 換成別的輸出列。
- ai-prompt 的要求句原檔是一行，`code` 卡依寬度換成三行；字沒改。
- secret-keys 把 Anthropic 跟 OpenAI 放在同一列「不能出現在瀏覽器或 App 裡」：OpenAI 的原句就是這樣講；Anthropic 的說明頁講的是「要保密、別人拿到就以你的名義計費、不要直接寫進程式或設定檔」，沒有逐字講瀏覽器。查核若覺得太強，可把旁白改成「OpenAI 的 API 金鑰不能出現在瀏覽器或 App 裡，Anthropic 的也一樣要保密」。
- 「別人的 AI 幾分鐘就讀完你整包 JavaScript」是站主觀點的原話，放在開場當利害句；r7 沒有計時，所以「幾分鐘」只有站主的說法撐。
- restrict 卡的 Supabase「打開資料列層級的存取規則（RLS）」：來源頁說 publishable key 只碰得到 RLS 允許的資料，沒有逐字寫「要打開 RLS」；這是從那句推出來的動作。
- public-keys 的 Google Maps 列標「設計上可以公開」：Maps 的安全頁是教怎麼限制放在用戶端的金鑰，沒有一句「可以公開」；分類是站主觀點（s1）加 c8。
- 估計 12.3 分鐘仍高於 10–12 的上緣；再砍就要動成果（define 的失敗、AI 檢查）或站主觀點，所以停在這裡，交協調者決定。
- 說明欄第 2 條寫「-P 是 GNU grep 的選項」，沒有在 macOS 或 Windows 跑過；企劃要的 macOS／Windows 寫法沒寫，因為沒有執行紀錄。

## 進度

- 全部 67 個場景寫完（open-title … closing），136 句，每句都有 id；`loops` 15 條；`sources` 16 個。
- lint：0 errors、0 warnings；`render/plan.mjs` 的 typingProblems 與 renderProblems 都是空的。
- 沒有 shorts.json（教學卡片沒有 shot）。
- 待做：獨立查核（verify-1.md），然後 `tts`。
