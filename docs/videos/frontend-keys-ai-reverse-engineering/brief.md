# 寫在前端的金鑰，等於公開：上線前檢查你自己的網站

企劃日期 2026-10-28。工具教學，**教學卡片**（`format: "slides"`、`category: "tutorial"`、`theme: "paper"`；teaching-flow §一–§九、§十二），
目標 10–12 分鐘（啟動訊息指定；8 分鐘是下限）。字卡主語言 zh-TW，產品、設定名稱、指令、檔名、變數名保留英文。站上沒有對應文章，沒有 `source_guide`。

一句話：瀏覽器拿到的不是你的 repo，是 build 出來的檔案；所以檢查要做在 build 出來的東西上，不是 repo 上。
跟前兩支的分界：`artex-ai-attack-leftover-keys` 講刪掉卻留在 git 歷史裡的金鑰（`git log -p`），這支講**從來沒進 git、卻被 build 送上網站**的那一把，
不碰 git 歷史；`muse-allow-always-agent-permission` 講代理權限按鈕，這支不講權限。旁白最多一句帶到 ARTEX。

時機（只當背景，不示範）：REA（Reverse Engineer Anything）這波「AI 把軟體拆開重做」的影片在兩週內大量出現，
西語圈 midudev〈La ingeniería inversa se volvió demasiado fácil〉12:01、555,085 次、7 天前（YouTube 搜尋 2026-10-28，`_tools/search/q4.json`）。
本片**不示範逆向任何人的網站、不教怎麼找出被隱藏或混淆的祕密**；所有執行都在觀眾自己的示範專案上、用一眼就看得出是假的金鑰。

事實來源（2026-10-28 用頻道 UA 開過，HTTP 200，原始 HTML 存在 `<VIDEO_WORKDIR>/frontend-keys-ai-reverse-engineering/_tools/sources/`）：
Vite〈Env Variables and Modes〉、〈Build Options〉、〈Shared Options〉；Next.js〈Environment Variables〉、〈productionBrowserSourceMaps〉、〈Data Security〉；
Firebase〈Learn about using and managing API keys for Firebase〉（頁面 Last updated 2026-10-20）；Stripe〈API keys〉；Supabase〈Understanding API keys〉；
Google Maps Platform〈API security best practices〉（Last updated 2026-10-27）；OpenAI API reference〈Authentication〉（developers.openai.com；help.openai.com 那頁回 403，沒用）；
Claude 說明中心〈API key best practices〉。

企劃先驗（**不算執行紀錄**，協調者要照「要先實作」再跑一次寫進 `runlog.txt`）：2026-10-28 在本容器（Ubuntu 24.04.5 LTS、Node v22.22.0、`vite/8.3.4`、Next.js 16.4.2、GNU grep 3.11、curl 8.5.0）
把下面每一項都跑過一次，結果跟「預期」一欄相同；檔案留在 `_tools/pilot/`（`shop-chat`、`define-case`、`fixed`、`next-leak`、`next-fixed`、`mock-upstream.mjs`），可以直接拿來重跑。

## 觀眾

自己做網站並部署的人：用 Vite（React、Vue、Svelte 都是）或 Next.js 的前端工程師；用 Cursor、Claude Code、Lovable、Bolt、v0 這類工具 vibe coding、
把「呼叫 OpenAI／Gemini／Claude 的小工具」直接部署上 Vercel、Netlify、Cloudflare Pages 的新手；接案做形象站、要串金流與地圖的人。
他們已經知道 API key 不能推上 GitHub，所以會把 `.env` 放進 `.gitignore`，上線前去 repo 或 GitHub 搜一下金鑰，搜不到就安心。
他們搜的是「API key 前端 外洩」「VITE_ 環境變數 安全嗎」「NEXT_PUBLIC 金鑰」「Firebase apiKey 可以公開嗎」「REA 逆向工程」。
他們不知道的是：`VITE_` 開頭的值在 build 時被**原樣寫進 JavaScript**，搜變數名稱反而搜不到；沒有前綴也可能經由 `define` 或 Next.js 的 props 送出去；
而被搜出來的金鑰裡，有一半本來就設計成可以公開，該做的是限制它，不是藏它。

### 先搜（teaching-flow §十一；YouTube 搜尋，2026-10-28，結果存在 `_tools/search/q1–q8.json`；訂閱數本機沒抓）

繁中關鍵字「API Key 前端 外洩」（q1）：

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| 白話解釋API到底是什麼？…為什麼API key外洩這麼嚴重？應該怎麼保護？ | Kelly Tsai | 18:10 | 55,429 | 4 天前 |
| GitHub上正在发生大规模API Key泄漏事件，小白需警惕！ | 网络小白_Uncle城 | 4:56 | 12,799 | 5 個月前 |
| 為什麼你需要API？\| 5分鐘秒懂 API Key 運作原理 | Eva | 5:14 | 7,675 | 1 年前 |
| 如何申請OpenAI API Key | C w C AI & 程式設計 | 3:32 | 8,613 | 1 年前 |
| 【开发扫盲】API 和 API Key 到底是什么？ | 01Coder | 9:50 | 860 | 3 個月前 |

繁中關鍵字「AI 逆向工程 網站」（q2）與「REA 逆向工程」（q6）：

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| The Fastest-Rising Repo on GitHub Is a Little Scary REA | Rob Shocks - Switch Dimension | 9:10 | 498,553 | 2 週前 |
| How To Use REA To Clone Any Software In Minutes | Eric Tech | 9:03 | 385,963 | 2 週前 |
| 我用 REA 逆向了付费颜色 APP，结果很意外！ | 程序员鱼皮 | 5:19 | 256,248 | 13 天前 |
| EP424 - 一句話逆向任何 App？AI 逆向工程 REA，這代表什麼 | AI懶人報 | 6:21 | 167,670 | 2 週前 |
| 為什麼整個 GitHub 都在瘋傳 REA？別人的程式碼，現在是你的了? | P & H | 8:27 | 166,360 | 2 週前 |
| REA 到底在紅什麼？原理、實測，以及我的看法 | Gary Chen | 13:23 | 86,564 | 13 天前 |
| 爆紅的逆向工程工具 REA，我開了 18 個分身實測：有用嗎？ | 蝦說 AI (小金老師) | 9:08 | 13,075 | 12 天前 |

讀法：REA 這一群全部在講「AI 能不能複製別人的軟體」，是攻方視角；「前端 金鑰 AI 逆向」（q5）零筆、「API key 前端 安全」（q7）只有一支 167 次的片，
**沒有一支從守方講「你的網站送出去了什麼」**。最接近的 Kelly Tsai 那支是概念解說（18 分鐘、講 API 是什麼），沒有動手檢查 build。
所以這支不做 REA 的總覽，**切一個概念**：「送到瀏覽器的都是公開的」，收在觀眾自己跑得出結果的三個動作。標題可借熱門片的字眼（「上線前」「一行指令」），
不用「駭」「破解」這類字。

## 觀眾看完能做到的事

- build 完之後，用一行 `sed -n 's/^[A-Z_]*=//p' .env | grep -rnoFf - dist/`（把 `.env` 裡的**每一個值**拿去搜 build 出來的資料夾）找出哪些金鑰被送進了網站，
  並看懂為什麼搜變數名稱、搜 repo 都找不到；換成自己的輸出資料夾（`dist/`、`build/`、`.next/`）重跑。怎麼知道做對了：搜得到的那幾行就是會送到每個訪客瀏覽器的字
  （第 1–2 章，`terminal`×3；**跑過（待第 1–3 項）**）。
- 把搜出來的每一把分成兩類，各自決定動作：設計上就公開的（Stripe publishable `pk_`、Firebase 的 web API key、Supabase publishable／anon、Google Maps 前端金鑰）
  留著、改去限制它；本來就是祕密的（OpenAI、Anthropic 的 API key，Stripe secret `sk_`，Supabase secret／service_role）搬走並換新
  （第 3 章，`table`；**引用**：各家官方頁原句，套在第 2 項跑出來的三個結果上）。
- 自己寫一個 31 行的 `server.mjs`（Node 內建 `http`，不裝套件），讓瀏覽器打 `/api/chat`、金鑰只在伺服器上加進去；改成自己要呼叫的網址與變數名稱，
  重 build、再搜一次只剩公開類，`curl` 打自己的 `/api/chat` 拿得到上游的回應。怎麼知道做對了：第一項那行指令不再印出祕密那一把
  （第 4 章，`code`×3＋`terminal`×2；**跑過（待第 5 項）**）。Next.js 的人寫 13 行的 `app/api/chat/route.js`，同一個檢查（第 5 章；**跑過（待第 6 項）**）。
- （選配，看第 7 項的結果決定留不留）讓自己的 AI 程式工具**只讀**自己的 `dist/`，找出 `.env` 裡沒有、直接寫死在程式裡的金鑰，並說出哪一家、能不能公開
  （第 2 章末；**跑過（待第 7 項）**；第 7 項沒有找到兩個 grep 都漏掉的那一把，這一項就拿掉）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，所以這一段是提案，站主選大綱時確認或改寫。語氣接站主 Muse 那支確認過的那句：「要用代理，但它照規則做事，規則的範圍是你按出來的。」）

我的看法是：前端沒有祕密。送到瀏覽器的每一個字，包括你以為「已經 build 掉了」的變數和註解，都當成貼在大樓公告欄上；以前要有人願意打開開發者工具慢慢看，
現在別人的 AI 幾分鐘就讀完。所以我上線前不搜 repo，我搜 build 出來的東西。
找到的金鑰我先分類，不是全部藏起來：本來就設計成公開的（Stripe 的 publishable、Firebase 的 web key），去限制它能做什麼；本來就是祕密的，搬到伺服器，
然後**換一把新的**，因為舊的那一把已經送出去過了。我照樣用 AI 寫前端，但哪些字會送到瀏覽器，是我決定的，不是 build 工具替我決定的。
我不知道的事：有多少上線的網站這樣漏了金鑰，我沒有可靠的數字，片裡不講比例。

## 示範或實算

製作路線：教學卡片（`theme: "paper"`，紙底、米白、墨黑、一個紅色強調；沒有 `shot`）。

**一個例子撐全片**：示範專案 `shop-chat`，一個只有一顆「Ask」按鈕的 Vite 小網站，按下去呼叫 OpenAI。`.env` 有四行，全是假的：

```
VITE_OPENAI_API_KEY=sk-demo-FAKE-0000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_DEMOFAKE0000
VITE_FIREBASE_API_KEY=AIza-DEMO-FAKE-0000
OPENAI_API_KEY=sk-server-FAKE-1111
```

假金鑰故意寫短、寫成 `FAKE`：repo 是公開的，長得跟真格式一樣（`AIza` 後面 35 字元、Stripe `sk_live_`）會被 GitHub 的祕密掃描當成真的；
這幾個只符合片中的搜尋指令，不符合任何一家的真實格式。`.gitignore` 是 `.env`、`node_modules`、`dist`。

**不用這個方法**（觀眾今天的做法，第一個拿得到「我的金鑰有沒有外洩」這個答案的）：`.env` 放進 `.gitignore`，上線前在 repo（或 GitHub）搜金鑰：
`git grep -n "sk-"` → 沒有輸出，exit 1。主例的差別是**同一個專案**上，那個做法說「乾淨」，build 出來的 `dist/` 卻有三把；兩邊都在這裡跑，並排上卡片。
**觀眾猜不到的結果**（主例自己的）：① 金鑰從沒進 git，卻在網站上；② build 完拿**變數名稱** `OPENAI_API_KEY` 去搜 `dist/`，一筆都沒有，因為名稱被換成了值，
要拿**值**去搜才找得到；③ 開了 source map，原始碼連註解 `// TODO: move the OpenAI call to a server before launch` 一起被送出去；
④ 第 5 章：Next.js 裡**沒加** `NEXT_PUBLIC_` 的金鑰，`.next/static` 搜不到，每個訪客拿到的頁面 HTML 裡卻有 `"apiKey":"sk-server-FAKE-1111"`。

**要先實作**（協調者在選大綱之前照順序跑，每一項把指令、完整輸出、日期與工具版本寫進 `<VIDEO_WORKDIR>/frontend-keys-ai-reverse-engineering/runlog.txt`；
跑不出「預期」的那一項，對應的成果拿掉）。示範資料夾放在工作區 `_demo/` 底下（路徑要短，`terminal` 卡不收家目錄），`node_modules` 用
`ln -s <ROOT>/node_modules node_modules`（Vite 走得通；Next.js 的 Turbopack 不接受指到專案外的 symlink，見第 6 項）。版本先記：`npx vite --version`
（預期 `vite/8.3.4 linux-x64 node-v22.22.0`）、`node -v`、`grep --version`、`curl --version`。

1. **主例的兩邊（RUN）**。檔案：`shop-chat/.env`（上面四行）、`.gitignore`、`index.html`（一顆 `#ask` 按鈕、一個 `#out`、`<script type="module" src="/src/main.js">`）、
   `src/main.js`（第 1 行 TODO 註解；`const key = import.meta.env.VITE_OPENAI_API_KEY;`、`const serverOnly = import.meta.env.OPENAI_API_KEY;`；按鈕 `fetch("https://api.openai.com/v1/responses", { headers: { Authorization: \`Bearer ${key}\` } })`；
   最後一行 `console.log` 印出 Stripe、Firebase 兩個 `VITE_` 值與 `serverOnly`），`package.json` 的 `"build": "vite build"`。範本在 `_tools/pilot/shop-chat/`。
   指令：`git init -q && git add -A && git commit -qm init`，然後 `git grep -n "sk-"` → 預期無輸出、exit 1；`git status --ignored --short` → 預期 `!! .env`。
   接著 `npm run build` → 預期 `dist/assets/index-<hash>.js` 約 1 kB（企劃先驗 1.06 kB）。
2. **build 的輸出（RUN）**。`sed -n 's/^[A-Z_]*=//p' .env | grep -rnoFf - dist/` → 預期三行：`dist/assets/index-<hash>.js:1:sk-demo-FAKE-0000`、`…:pk_test_DEMOFAKE0000`、`…:AIza-DEMO-FAKE-0000`，
   **沒有** `sk-server-FAKE-1111`。`grep -rn "OPENAI_API_KEY" dist/` → 預期無輸出、exit 1（名稱被換成值）。`grep -o 'var e=[^,]*' dist/assets/*.js` → 預期 `` var e=`sk-demo-FAKE-0000` ``；
   沒有前綴的 `serverOnly` 預期變成 `t=void 0`（Vite 文件的 `DB_PASSWORD` 例子，跑出來當對照）。認法：三把裡沒有一把出現在第 1 項的 `git grep`。
   另跑一次照形狀搜（給寫死在程式裡、不在 `.env` 的金鑰）：`grep -rnoP "sk-[\w-]+|pk_\w+|AIza[\w-]+" dist/` → 預期同樣三行（`-P` 要 GNU grep；macOS 的寫法放說明欄）。
3. **source map（RUN）**。`npm run build -- --sourcemap` → 預期多一個 `dist/assets/index-<hash>.js.map`；`grep -o '// TODO[^\\]*' dist/assets/*.map` → 預期印出
   `// TODO: move the OpenAI call to a server before launch`；再 `grep -c "OPENAI_API_KEY" dist/assets/*.map` → 預期 1（名稱搜得到了，在原始碼裡）。結束後 `npm run build` 不帶旗標重 build。
4. **常見失敗：沒有前綴也送出去（RUN）**。複製成 `define-case/`，加 `vite.config.js`（5 行：`loadEnv(mode, process.cwd(), "")`，`define: { "process.env.OPENAI_API_KEY": JSON.stringify(env.OPENAI_API_KEY) }`），
   `src/main.js` 的 `serverOnly` 改讀 `process.env.OPENAI_API_KEY`。`npm run build` 後跑第 2 項那一行 → 預期四行，多了 `sk-server-FAKE-1111`。
   認法：沒有 `VITE_` 前綴的那一把也進了 bundle。這是 AI 工具「修好 `process.env` is undefined」時常寫的寫法（這句是企劃的觀察，片中不講成數字）。
5. **修好（RUN）**。複製成 `fixed/`：`.env` 拿掉 `VITE_OPENAI_API_KEY` 一行、只留 `OPENAI_API_KEY=sk-demo-FAKE-0000`；`src/main.js` 改成 `fetch("/api/chat", { method: "POST", body: JSON.stringify({ input: "hi" }) })`；
   加 `server.mjs`（31 行，每行 ≤ 64 字元，全文在 `_tools/pilot/fixed/server.mjs`：`UPSTREAM` 讀 `process.env.UPSTREAM_URL`，預設 `https://api.openai.com/v1/responses`；
   `POST /api/chat` 讀 body、`fetch(UPSTREAM, { headers: { Authorization: \`Bearer ${process.env.OPENAI_API_KEY}\` } })`、原樣回傳；其他路徑用 `new URL(req.url, "http://localhost").pathname` 取路徑後從 `dist/` 讀檔，讀不到回 404）。
   上游用假的：`_tools/pilot/mock-upstream.mjs`（5 行，聽 8788，回 `{"got_key":true}` 表示收到 `Bearer sk-` 開頭的標頭，不印金鑰）。**不打真的 OpenAI。**
   指令：`npm run build`；第 2 項那一行 → 預期只剩 `pk_test_DEMOFAKE0000`、`AIza-DEMO-FAKE-0000` 兩行；另開兩個終端 `node mock-upstream.mjs`、`UPSTREAM_URL=http://127.0.0.1:8788 node --env-file=.env server.mjs`；
   `curl -s -X POST localhost:8787/api/chat -d '{"input":"hi"}'` → 預期 `{"got_key":true}`；`curl -s localhost:8787/ | grep -c sk-` → 預期 `0`。
   安全自檢（不上卡片）：`curl -s --path-as-is -o /dev/null -w '%{http_code}\n' 'localhost:8787/../.env'` 與 `'localhost:8787/%2e%2e/.env'` → 預期都是 `404`（企劃先驗過；這個檔案不能把 `.env` 當靜態檔送出去）。
   同一個 `curl` 也是第 6 章的觀察：**沒有瀏覽器、沒有登入**，一行就拿到回應，代表任何人都能經由這個端點花你的額度。
6. **對照：Next.js（RUN）**。`next-leak/`：`app/layout.jsx`、`app/chat.jsx`（`"use client"`，收 `apiKey` prop，fetch OpenAI）、`app/page.jsx`（伺服器元件 `<Chat apiKey={process.env.OPENAI_API_KEY} />`）、
   `.env.local` 一行 `OPENAI_API_KEY=sk-server-FAKE-1111`（**沒有** `NEXT_PUBLIC_`）。範本在 `_tools/pilot/next-leak/`。
   build：先試 `npm i next@16.4.2 react react-dom` 後 `npx next build`（Turbopack，觀眾的預設）；容器裝不了就用 symlink 加 `npx next build --webpack`，`tool_version` 寫「Next.js 16.4.2 (webpack)」。
   `grep -rl "sk-server-FAKE-1111" .next/static` → 預期無輸出、exit 1；`npx next start -p 3000` 後 `curl -s localhost:3000/ | grep -o '"apiKey":"[^"]*"'` → 預期 `"apiKey":"sk-server-FAKE-1111"`（企劃先驗在 `.next/server/app/index.html` 的 RSC 資料裡）。
   修好：`next-fixed/` 加 `app/api/chat/route.js`（13 行，同第 5 項的 `UPSTREAM` 與標頭），`chat.jsx` 改 fetch `/api/chat`、`page.jsx` 不再傳 prop。重 build → `.next/static` 與 `curl localhost:3000/` 都搜不到；
   `UPSTREAM_URL=http://127.0.0.1:8788 npx next start` 後 `curl -s -X POST localhost:3000/api/chat -d '{"input":"hi"}'` → 預期 `{"got_key":true}`。若 Turbopack 的輸出路徑不同，記下實際路徑，不改預期的結論。
7. **選配：讓自己的 AI 只讀自己的 dist（RUN）**。先在 `shop-chat/src/main.js` 加一行寫死、不在 `.env`、也不符合第 2 項形狀的字串：`const ADMIN = "demo-admin-7f3a9c";`（並用在一個 `X-Admin-Token` 標頭），重 build；
   第 2 項兩行指令 → 預期都**沒有**印出 `demo-admin-7f3a9c`。信任檢查排在授權之前：只開讀的工具。在 `shop-chat/` 跑
   `claude -p "$(cat review-prompt.txt)" --allowedTools "Read,Grep,Glob"`（Claude Code 2.1.312，`/opt/node22/bin/claude`），`review-prompt.txt` 一句：
   「只讀 dist/ 資料夾，列出每一個看起來像金鑰、權杖或密碼的字串：檔案、字串、可能是哪一家的什麼金鑰、能不能公開、理由一句。不要修改任何檔案。」
   預期：列出四個，包含 `demo-admin-7f3a9c`，並把 `pk_test_…` 標成可公開。認法：它找到兩個 grep 都漏掉的那一把。容器裡 headless 沒有登入、或它沒找到那一把，這一項與第四件成果一起拿掉，不降成引用。
8. **畫面截圖（SEEN 不適用，`screencast`）**：Vite〈Env Variables and Modes〉的「Protecting secrets」一段、Supabase〈Understanding API keys〉的 Key types 表、Stripe〈API keys〉的「Protect your keys」一段。公開頁，不登入。

沒有更高一級可以列的：第 1–6 項的結果本身就是指令與輸出，沒有「在產品介面上看到」這回事。限制公開金鑰（Firebase 的 API restrictions、Google Maps 的 Websites 限制、Supabase RLS）
要登入各家主控台，**不跑、不截任何人的主控台**；它不是成果，是「留下來」那一步，用官方頁的步驟（`steps`），卡片標「引用」。換掉舊金鑰同樣是官方頁的步驟。

示範在第 1–5 章：第 1 章 `terminal`×2（`git grep` 空／`grep dist` 三行），第 2 章 `terminal`×2＋`code`（map 裡的 TODO），第 4 章 `code`×3（`server.mjs` 全文）＋`terminal`×2，第 5 章 `terminal`×2＋`code`（`route.js`）。
`terminal` 卡的指令與輸出逐字取自 `runlog.txt`，提示字元只有 `$ `，每行 ≤ 78 欄；`ran_on` 是協調者實跑那天、`tool_version` 是印出那段輸出的程式（`vite/8.3.4`、`GNU grep 3.11`、`Next.js 16.4.2`）。

## 大綱

三個選項的共同點：主例都是 `shop-chat` 與同一組假金鑰，章序都照觀眾的問題（我會拿到什麼 → 跟我現在的做法差在哪 → 怎麼做 → 怎麼知道做對 → 怎麼留下來）。
差在主角是哪個框架、從哪個意外開場、分類放在哪裡。「我」的句子三個選項都取自：執行紀錄（「我 build 完搜變數名稱，一筆都沒有」「我沒加前綴，頁面裡還是有」）、
上面提案的立場（「我不搜 repo，我搜 build」「我照樣用 AI 寫前端」）、查不到的事（有多少網站這樣漏，我沒有數字）。

### 選項 A（推薦）：搜 repo 是乾淨的，搜 dist 有三把——Vite 主例、Next.js 當對照

角度：故事線「實測型」，主角是 `shop-chat`。從觀眾**現在的檢查失靈**開場，一路修到乾淨；Next.js 放第 5 章當「沒加前綴也會漏」的對照。跟 B 差在主框架與開場，跟 C 差在分類不是開場。

開場（teaching-flow §一，五句，前 20 秒說出 `.env`、`dist`、`VITE_`）：
「我把 `.env` 放進 `.gitignore`，整個 repo 搜 `sk-`，一筆都沒有；build 完再搜 `dist`，同一把金鑰就寫在 JavaScript 裡。」（結果）／
「你可能會想：金鑰又沒推上 GitHub，這有什麼關係？」（用觀眾的話問）／
「關係在於，瀏覽器拿到的不是你的 repo，是 build 出來的檔案：它會把 `VITE_` 開頭的值原樣寫進去，開了 source map 連註解都一起送。」（動詞清單：寫進去、送出去）／
「最近 AI 把別人的軟體拆開重做的影片一支幾十萬次，打開你網站的人，現在也有一個幾分鐘就讀完你整包 JavaScript 的 AI。」（利害）／
「一行搜尋、一張分類表、一個 31 行的伺服器檔，上線前把它找出來、搬走。」（承諾句）

案例與結果：「`shop-chat`：`git grep` 無輸出、`dist/` 搜出三把；搬到 `server.mjs` 後只剩兩把公開類、`/api/chat` 照常回應；證據 跑過（待第 1–5 項）＋引用（Vite、Stripe、Firebase、Supabase、OpenAI 官方頁）。」

旁白先講出來再答的疑問（§三，每次緊接答案）：「我 `.env` 有放 `.gitignore` 啊？」（第 1 章）、「那我搜變數名稱不就好了？」（第 2 章）、
「Firebase 那把也被搜出來了，要不要也藏？」（第 3 章）、「搬到伺服器，別人不就改打我的 `/api/chat`？」（第 6 章）、「我沒加前綴，總安全了吧？」（第 5 章）。
對照已在用的（§三）：觀眾現在的檢查＝搜 repo／GitHub（第 1 章）；選擇規則一句：「金鑰有沒有進 git，搜 repo；金鑰有沒有上網站，搜 build。」

例子在每章開頭的狀態（§四）：

0. 開場（45 秒）：`shop-chat` 已 build，repo 乾淨。`title`（標題）→ `compare`（左「搜 repo」：`git grep` 無輸出／右「搜 dist」：三行）→ `big`（你可能會想）→ `bullets`（承諾：一行搜尋、一張分類表、一個伺服器檔，`icon` 各一）。
1. 為什麼 repo 乾淨、網站卻有？（90 秒）狀態：剛 build 完。`code`（`.env` 四行，標出 `VITE_` 三行）→ `terminal`（`git grep -n "sk-"`：無輸出）→ `terminal`（`grep dist` 三行）→
   `quote`（Vite："VITE_* variables should not contain sensitive information such as API keys. The values of these variables are bundled into your source code at build time."＋譯文）→
   `big`（`VITE_`＝要送進瀏覽器的意思）。收尾問題：「那我拿變數名稱去搜 dist 呢？」
2. 搜值，不搜名字（100 秒）狀態：知道它在 `dist`，還不知道怎麼搜得全。`terminal`（`grep "OPENAI_API_KEY" dist/`：無輸出）→ `code`（bundle 裡那一段：`var e=\`sk-demo-FAKE-0000\``，`highlight`）→
   `big`（名字被換成值）→ `terminal`（`sed … .env | grep -rnoFf - dist/`：三行，`keys` 標「這一行換成你的資料夾」）→ `terminal`（`--sourcemap` 後 map 裡的 TODO 註解）→
   `quote`（Next.js：production 的 source map 預設關閉，"to prevent you leaking your source on the client"）→（選配第 7 項成立才有）`chat`（給 AI 的那句要求）＋`table`（它列出的四個，寫死的那把標紅）。
   收尾問題：「三把都搜出來了，三把都要藏嗎？」
3. 三把都要藏嗎？（100 秒）狀態：清單上三把。`table`（四列：Stripe `pk_`／Firebase web key／Supabase publishable／Maps 前端 key＝可公開；`source`：各官方頁）→
   `table`（四列：OpenAI／Anthropic API key、Stripe `sk_`、Supabase secret／service_role＝不能公開）→ `quote`（Stripe："Only publishable keys are safe to expose outside your application's backend."）→
   `quote`（Firebase："never include the Gemini Developer API in the allowlist for a publicly accessible API key"）→ `big`（可公開的去限制，祕密的搬走）→ `steps`（`shop-chat` 的三把：`pk_test` 留、`AIza` 留但限制、`sk-` 搬）。
   收尾問題：「`sk-` 那把要搬去哪？」
4. 寫一個 31 行的伺服器（130 秒）狀態：只剩一把要搬。`compare`（之前：瀏覽器直接打 OpenAI、帶金鑰／之後：瀏覽器打 `/api/chat`、伺服器加金鑰）→ `code`（`.env` 改一行、`main.js` 改 fetch）→
   `code`×3（`server.mjs` 第 1–12、13–24、25–31 行，`highlight` 觀眾要改的 `UPSTREAM` 與 `OPENAI_API_KEY` 兩處）→ `terminal`（重 build 後 grep：只剩兩行）→
   `terminal`（`curl -X POST localhost:8787/api/chat`：`{"got_key":true}`）→ `big`（grep 不再印出 `sk-`＝做對了）。收尾問題：「我用的是 Next.js，而且根本沒加前綴？」
5. 沒加前綴也會漏（100 秒）狀態：Vite 版乾淨了，換到 Next.js 版 `next-leak`。`code`（`page.jsx` 三行：`<Chat apiKey={process.env.OPENAI_API_KEY} />`）→ `terminal`（`grep .next/static`：無輸出）→
   `terminal`（`curl localhost:3000/ | grep apiKey`：`"apiKey":"sk-server-FAKE-1111"`）→ `quote`（Next.js Data Security："it's possible to accidentally expose private data through how data is fetched or passed to components"）→
   `big`（檢查要做在訪客拿到的頁面上，不只是資料夾）→ `code`（`route.js` 13 行）→ `terminal`（修好後 `curl` 搜不到）→ `bullets`（Vite 的同一種失敗：`define` 把沒前綴的值寫進去，第 4 項的一行輸出）。
   收尾問題：「搬好了，舊的那把怎麼辦？」
6. 留下來：換掉、限制、設上限（80 秒）狀態：兩版都乾淨。`big`（舊的那把已經送出去過：rebuild 收不回）→ `steps`（換新金鑰：OpenAI 撤銷「幾秒內生效」、Stripe Rotate；引用）→
   `steps`（限制公開的：Maps 的 Websites 限制、Firebase 只開 Firebase 用的 API、Supabase 開 RLS；引用，不截主控台）→ `terminal`（同一個 `curl`：沒有瀏覽器也打得通）→
   `bullets`（所以：定期看用量、設上限；Anthropic 說明頁：看 Usage 與 Logs，spend limits 與 rate limits「as a safeguard against unexpected usage due to leaked keys」，標準方案則是小心設定 auto-reload 的上限）。
7. 收尾（40 秒）：`big`（答案：送到瀏覽器的都是公開的，上線前搜 build、不搜 repo）→ `outro`（留言題：「你上一個上線的網站，build 出來搜過嗎？搜到了幾把？」＋訂閱邀請）。

總長約 685 秒（11.4 分鐘），旁白約 2,850 字。

### 選項 B：沒加 NEXT_PUBLIC_，頁面裡還是有——Next.js 主例、Vite 當對照

角度：主角換成 Next.js 版 `shop-chat`（同一組假金鑰），從「我照規矩沒加前綴」的安心失靈開場；Vite 的 `VITE_` 放第 2 章當「有前綴就一定送出去」的對照。
給用 v0、Vercel、Next.js 的觀眾；修法是 13 行的 Route Handler，比 A 的 31 行短。跟 A 差在開場的意外更深一層（沒前綴也漏）、但 Vite 觀眾要到第 2 章才被照顧到。

開場：「我的 OpenAI 金鑰沒有加 `NEXT_PUBLIC_`，`.next/static` 整包搜不到；可是打開首頁的 HTML，它就寫在 `"apiKey"` 後面。」／「你可能會想：Next.js 不是說沒前綴就只在伺服器上？」／
「它沒說錯，是我把它當成 props 傳給了一個 client component，這一傳，值就被寫進每個訪客拿到的頁面。」／「打開你網站的人，現在也有一個幾分鐘就讀完整頁的 AI。」／
「一行 curl、一張分類表、一個 13 行的 route，上線前把它找出來、搬走。」

案例與結果：「`next-leak`：`.next/static` 無、`curl /` 搜到 `"apiKey":"sk-server-FAKE-1111"`；搬到 `app/api/chat/route.js` 後搜不到、`/api/chat` 照常回應；證據 跑過（待第 6 項）＋對照 跑過（待第 1–2 項）。」

1. 開場（45 秒）`title` → `terminal`（`grep .next/static`：無）→ `terminal`（`curl / | grep apiKey`：有）→ `bullets`（承諾）。
2. 前綴到底管什麼？（100 秒）`quote`（Next.js：`NEXT_PUBLIC_` "will be inlined into any JavaScript sent to the browser"）→ Vite 對照：`terminal`（`git grep` 空）→ `terminal`（`dist` 三行）→ `big`（有前綴＝一定送出去，沒前綴≠一定不送）。收尾問題：「那沒前綴的是怎麼跑出去的？」
3. props 的那一傳（90 秒）`code`（`page.jsx`、`chat.jsx`）→ `quote`（Data Security）→ `big`（client component 收到的每個值都會進頁面）→ `terminal`（`sed … | grep -rnoFf - .next/server/app`）。收尾問題：「搜到的都要藏嗎？」
4. 三把都要藏嗎？（100 秒）同 A 第 3 章的兩張 `table`、兩張 `quote`。
5. 13 行的 route（110 秒）`compare` → `code`（`route.js`）→ `code`（`chat.jsx` 改 fetch）→ `terminal`（重 build 後 `curl /`：無）→ `terminal`（`POST /api/chat`：`{"got_key":true}`）。
6. 留下來（80 秒）同 A 第 6 章；`define` 的失敗放這裡一張 `bullets`。
7. 收尾（40 秒）。總長約 565 秒（9.4 分鐘），要到 10 分鐘以上得把 source map 那一段（第 3 項）補進第 2 章。

### 選項 C：AI 讀了你的網站，列出四個字串——先分類、再修

角度：疑問型。開場就是觀眾自己的 AI 讀自己的 `dist/` 交出的清單（第 7 項），全片回答「這四個哪個要緊」：一把要搬、兩把設計上公開但要限制、一把寫死的要刪。
搜尋指令放第 2 章當「不用 AI 也查得到的部分」。跟 A、B 差在主軸是判斷（分類）而不是搜尋，最貼 REA 的時機，但**整個開場押在第 7 項**：它沒成立，C 就不能選。

開場：「我讓自己的 AI 只讀我網站 build 出來的資料夾，它交回四個字串。」／「你可能會想：四個都要藏起來吧？」／「不用：兩個本來就設計成公開，一個要搬到伺服器，一個根本不該在那裡。」／
「別人的 AI 讀到的是同一份檔案。」／「一張分類表、一行搜尋、一個伺服器檔。」

案例與結果：「`shop-chat`（加了寫死的 `demo-admin-7f3a9c`）：AI 列出四個並分類；`grep` 兩行只找到三個；搬走後剩兩個公開類；證據 跑過（待第 7、2、5 項）＋引用（官方分類）。」

1. 開場（50 秒）`title` → `chat`（給 AI 的那句要求）→ `table`（它列出的四個）→ `bullets`（承諾）。
2. 不用 AI 查得到多少？（100 秒）`terminal`（`git grep` 空）→ `terminal`（`.env` 值搜 `dist`：三行）→ `big`（寫死的那把 grep 找不到）→ `terminal`（名字搜不到）→ `quote`（Vite）。
3. 哪些本來就公開？（110 秒）兩張 `table`＋Stripe、Firebase、Supabase 的 `quote`（Supabase：publishable key 不是用來防 "static or dynamic code analysis and reverse engineering attempts"）。
4. 搬走要緊的那一把（120 秒）同 A 第 4 章。
5. 沒前綴也會漏（80 秒）Next.js `curl` 一組＋`define` 一行。
6. 留下來（70 秒）＋收尾（40 秒）。總長約 570 秒。

**推薦 A**：主例的兩邊（`git grep` 與 `grep dist`）不靠任何需要登入的東西，第 1–5 項全是本機指令，最穩；開場直接打在觀眾現在那個檢查上；Next.js 的「沒前綴也漏」放在第 5 章當轉折，
比 B 多照顧到 Vite 這一大群；C 押在 AI headless 的那一次執行上，而且 AI 清單要逐字上卡片，變數最多。

## 會過期的事實

- `VITE_` 前綴的值在 build 時寫進 bundle、`VITE_*` 不該放 API key、`envPrefix` 不要設成 `''`：https://vite.dev/guide/env-and-mode 、https://vite.dev/config/shared-options#envprefix （2026-10-28 開過）
- Vite `build.sourcemap` 預設 `false`：https://vite.dev/config/build-options#build-sourcemap
- Vite `define` 在 build 時靜態替換：https://vite.dev/config/shared-options#define
- 片中的 Vite 版本 8.3.4 是執行紀錄印出的版本（`npx vite --version`），撰稿時以 `runlog.txt` 為準，不另找頁面。
- Next.js `NEXT_PUBLIC_` 在 `next build` 時 inline 進送到瀏覽器的 JavaScript、沒前綴的預設只在伺服器：https://nextjs.org/docs/app/guides/environment-variables （頁面 Last updated 2026-08-25）
- Next.js production 瀏覽器 source map 預設關閉：https://nextjs.org/docs/app/api-reference/config/next-config-js/productionBrowserSourceMaps
- Next.js 經由傳給元件的資料意外外洩、Taint API（experimental）：https://nextjs.org/docs/app/guides/data-security
- Next.js 的 `next build` 預設 Turbopack（"enabled by default"）、`--webpack` 改用 Webpack（執行紀錄要寫用了哪個）：https://nextjs.org/docs/app/api-reference/cli/next （2026-10-28 開過）
- Firebase web API key 在符合指引時不必當祕密、Gemini Developer API 不要放進公開金鑰的 allowlist：https://firebase.google.com/docs/projects/api-keys （Last updated 2026-10-20）
- Stripe「Only publishable keys are safe to expose outside your application's backend」、金鑰前綴 `pk_test_`／`sk_live_`、Rotate：https://docs.stripe.com/keys
- Supabase publishable／secret 與舊的 anon／service_role、secret key 在瀏覽器回 401、**anon 與 service_role 預計 2026 年底淘汰**：https://supabase.com/docs/guides/api/api-keys
- Google Maps 金鑰的 Websites（referrer）限制：https://developers.google.com/maps/api-security-best-practices （Last updated 2026-10-27）
- OpenAI：API key 不要放進瀏覽器或 App 的 client-side 程式碼、撤銷在幾秒內生效：https://developers.openai.com/api/reference/overview （Authentication 一節）
- Anthropic：不要把金鑰直接寫進程式或設定檔、看 Usage 與 Logs、spend limits（custom rate limit 的組織）與 auto-reload 上限（standard 的組織）：https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure
- 時機鉤子的觀看數（REA 群與 midudev）：YouTube 搜尋頁，撰稿當天重抓 `_tools/search/`（2026-10-28 的數字見〈觀眾〉兩張表）

## 素材

- `screencast`（公開官方頁，不登入）：Vite〈Env Variables and Modes〉的 Protecting secrets 一段（也是縮圖右側的主體）、Supabase〈Understanding API keys〉的 Key types 表、Stripe〈API keys〉的 Protect your keys 一段、Firebase〈API keys〉的 Security Rules 一段。
- `terminal`／`code` 卡：逐字取自協調者的 `runlog.txt`（第 1–7 項）；檔案範本在 `<VIDEO_WORKDIR>/frontend-keys-ai-reverse-engineering/_tools/pilot/`（企劃先驗用，不是執行紀錄）。
- 原始頁面 HTML：`_tools/sources/`（vite-env、vite-build、vite-shared、next-env、next-srcmap、next-datasec、next-cli、firebase、stripe、supabase、maps、openai-auth2、anthropic）。
- YouTube 搜尋結果：`_tools/search/q1–q8.json`（2026-10-28）。
- 縮圖：米白底，大字「搜過 dist 嗎」（6 字以內），右側 Vite 官方頁 Protecting secrets 那段的截圖；不用任何人的網站、不畫駭客。
- 說明欄：第 2 項兩行指令的 macOS／Windows（Git Bash、WSL）寫法、`server.mjs` 與 `route.js` 全文、各官方頁連結。

## 不做的事

- 不示範逆向工程任何人的網站或 App，不對別人的網址跑任何一行片中的指令；片中所有 `curl` 都只打 `localhost`。
- 不教怎麼找出被混淆、加密或隱藏的祕密，不講 REA 怎麼裝、怎麼用，不放它的連結；REA 與 midudev 只在開場當時機一句。
- 不碰 git 歷史裡的金鑰（`artex-ai-attack-leftover-keys` 講過），不重講 `git log -p`。
- 不比較祕密掃描工具（gitleaks、TruffleHog、GitHub secret scanning），不推薦付費服務。
- 不登入、不截任何主控台（OpenAI、Stripe、Firebase、Google Cloud、Supabase）；限制與換金鑰只用官方頁的步驟。
- 不講手機 App、瀏覽器擴充功能、桌面 App 的金鑰（同一個道理，但例子不同）；不講 CORS、CSP、OAuth 的細節。
- 不打真的 OpenAI API、不用任何真的金鑰；`server.mjs` 只做到「金鑰不在瀏覽器」，驗證、限流的完整寫法不在這支（第 6 章只講要設上限）。
