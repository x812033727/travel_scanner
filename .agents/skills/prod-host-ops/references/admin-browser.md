# 用瀏覽器操作後台、法律頁、分潤 clickout

## 驅動後台的 React 表單

後台要登入，我不能輸入密碼：瀏覽器登出了（session 重啟、token 過期）就請使用者在那個瀏覽器裡自己登入。登入的有效期是 `access_token_expire_minutes`，沒有 refresh 流程，長時間的驗證中途被登出是正常的，不是部署造成的。

**寫值**

- `form_input` 只改 DOM，不改 React state；存檔送出去的還是舊值，勾選框也一樣。
- 文字欄位：點欄位 → `ctrl+a` → `type` 打真的鍵盤（最可靠）；或先 `el.focus()` 再打鍵盤；或在 `javascript_tool` 裡用原型的 value setter 再派發事件：

  ```js
  const el = /* 用 read_page 或 find 找到的那個 input */ document.activeElement;
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(el, "新的值");
  el.dispatchEvent(new Event("input", { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
  ```

- `<select>`：設 `selectedIndex` 後派發 `change`。有連動的下拉（例如目的地 → 模組 → 品牌），**最後**才設依賴別人的那個，先設的會被後設的清掉。
- 勾選框：**真的點**（座標點擊或 `el.click()`）。如果先前用 `form_input` 勾過，DOM 已經是勾的、React 還不是，要點兩次，再看畫面與送出的值。
- 按鈕：`button.click()` 最穩；`computer` 的 ref 或座標點擊常因座標過期或截圖逾時打空。後台分類的膠囊按鈕曾經 ref 點擊切不過去、座標點擊才行。
- 存完看狀態文字（AI 卡片是「<卡片> 設定已加密儲存並立即套用。」），再重新載入頁面確認值還在。

**讀畫面**

- `read_page filter=interactive` 只列出視窗附近的元素，長表單要先捲過去。
- 發布類的確認框是原生 `<dialog open>`，沒有 `role=dialog`，焦點一開始在「關閉」上；用 `document.querySelector('dialog[open]')` 找。
- 區塊編輯器的每個 fieldset 以索引當 key：「上移」會交換內容、按鈕的 ref 不動。要插入區塊，先加在最後再一路上移。
- 後台側欄的 RSC prefetch 被邊緣層 429 與功能無關。
- 內建瀏覽器面板隱藏時 IntersectionObserver 不觸發、lazy 區塊不會掛載：看起來「沒出現」先確認面板是顯示的。

**不可逆的按鈕**（發布、確認發布、核准、退件）：先把要按的東西、影響範圍寫給站主，由站主決定自己按還是讓你按；auto 模式的分類器也會擋模型去按「發布」。

## 法律頁（/privacy、/terms、/about、/contact）

四頁 × 五語系＝20 份資料庫文件，後台在 `/zh-TW/admin/site-pages`，API 在 `apps/api/app/site_pages/`（管理端 `GET /api/travel/admin/site-pages/<slug>?locale=<語系>` 回 `draft` 與 `published`）。

- **改 `apps/api/app/site_pages/drafts/` 的 JSON 不會改到正式站。** `initialize_pages` 只補缺的列、從不覆寫；正式站的列早就建好了。之後任何政策修改＝在後台逐語系編輯＋發布，五次。
- 不要自己重寫政策文字；文字是站主的決定。

**發布前的雜湊核對**：確認後台存好的草稿和打算發布的文字（通常是 repo 的 drafts 檔）逐字相同。兩邊用同一個正規化與排序後算 SHA-256，只比雜湊；不一致時逐區塊算雜湊找出是哪幾塊。

```js
// 兩邊共用：補上預設值、鍵排序、忽略生效日（發布時才填）
const norm = (d) => ({ title: d.title, description: d.description, requirements: d.requirements,
  blocks: d.blocks.map((b) => b.type === "heading" ? { level: 2, ...b } : b.type === "list" ? { ordered: false, ...b } : b) });
const canon = (v) => Array.isArray(v) ? `[${v.map(canon).join(",")}]`
  : v && typeof v === "object" ? `{${Object.keys(v).sort().map((k) => JSON.stringify(k) + ":" + canon(v[k])).join(",")}}`
  : JSON.stringify(v);

// 瀏覽器（已登入後台的分頁）
const d = (await (await fetch("/api/travel/admin/site-pages/privacy?locale=en")).json()).draft;
[...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(canon(norm(d)))))]
  .map((x) => x.toString(16).padStart(2, "0")).join("");

// 本機 Node（repo 根目錄）
// const doc = JSON.parse(fs.readFileSync("apps/api/app/site_pages/drafts/en.json", "utf8")).privacy;
// crypto.createHash("sha256").update(canon(norm(doc))).digest("hex");
```

還沒存的表單內容不在 API 裡；要核對正在編輯的內容，先存草稿再比。

**發布**：逐語系按「發布」→ 原生 dialog → 真的點確認勾選框 → 填原因 → 「確認發布」。站主通常想自己按最後一下。

**發布後**：20 個公開網址（`https://mokaair.com/<語系>/<privacy|terms|about|contact>`）逐一抓，循序、每秒不超過一兩次，確認沒有 `sitePages.unpublished` 那句（zh-TW 是「內容準備中，確認完成後將在此公開。」）。公開 API 是 `GET /api/travel/site-pages/<slug>?locale=<語系>`。

社群的總開關「開放社群」依賴法律頁先上線（`docs/community.md`：先法律、後社群），要不要打開是站主的決定；快速檢查 `GET /api/travel/community/status`。

## 用真實點擊驗分潤 clickout

合作按鈕是 `<form method="post" target="_blank">` 送到 `/api/travel/affiliates/destination-offers/<id>/clickout`，API 回 303 到合作方並寫一筆 `affiliate_clicks`（含 placement）。**表單只能用 `rel="noopener"`**：加上 `noreferrer` 時瀏覽器以 `Origin: null` 送出 POST，BFF 的 `isAllowedMutationOrigin`（`apps/web/app/api/travel/[...path]/proxy-security.ts`）回 403 `cross_site_request_blocked`，新分頁只剩一段 JSON、點擊沒被記到。這個 bug 曾讓全站合作按鈕壞掉而 CI 全綠，因為單元測試斷言錯的值、e2e 在 BFF 前就攔下請求、HTTP 測試手寫了 Origin。

所以：

- **curl 帶 `Origin` 只證明伺服器規則**，證明不了瀏覽器實際送什麼。
- **內建瀏覽器面板不能驗**：它把 `target=_blank` 的表單 POST 變成同分頁的 GET（405）。
- 無頭 Chromium 打開 Klook 是空白頁（反機器人），但我們要的只是 303 與 `Origin`；要看合作方頁面本身，用面板直接開那個網址。

用 Playwright 在正式站真的點一次。在 web 目錄裡（`@playwright/test` 是那裡的 devDependency）存成暫存檔 `clickout-check.local.mjs`，用完刪掉、不要 commit：

```js
// node clickout-check.local.mjs <頁面網址> <按鈕文字>
import { chromium } from "@playwright/test";
const [url, label] = process.argv.slice(2);
const browser = await chromium.launch();
const context = await browser.newContext();
context.on("request", async (r) => {
  if (r.url().includes("/clickout")) console.log(r.method(), r.url(), "origin:", (await r.allHeaders()).origin);
});
context.on("response", (r) => {
  if (r.url().includes("/clickout")) console.log(r.status(), r.headers().location ?? "");
});
const page = await context.newPage();
await page.goto(url, { waitUntil: "networkidle" });
const popup = context.waitForEvent("page");
await page.getByText(label).first().click();
await (await popup).waitForLoadState("domcontentloaded").catch(() => {});
await browser.close();
```

通過＝`POST … origin: https://mokaair.com`，接著 `303 https://<合作方>…`（Klook 會帶上 `?aid=`）。`origin: null` 或 403 就是上面那個 bug。這會在正式站寫一筆真的 `affiliate_clicks`，驗完告訴站主有幾筆是測試。報表在後台（`GET /api/travel/admin/analytics/affiliates?range=`，依 partner／placement／module／destination 分）；夥伴×模組的就緒表來自 `GET /api/travel/affiliates/status`。

本機跑合作按鈕的 e2e 時用 CI 的方式：`npm run build` 後 `PLAYWRIGHT_SERVE_BUILD=true`（`next dev` 的 StrictMode 會讓 effect 打兩次），port 3000 被占就設 `PLAYWRIGHT_PORT`。e2e 的 `mock()` 回傳 `clickoutOrigins`，每個開新分頁的測試都要斷言它等於頁面的 origin。
