# 內建瀏覽器：榜頁、店頁、資訊分頁

規則全文在 `docs/catchtable-ranking-discovery.md` 的「本機瀏覽器」一節；這裡是可以直接貼進 Console 的片段與代理提示。

## 榜頁：滾輪逐步累積

網址：最佳餐廳榜 `https://www.catchtable.net/zh-TW/ranking/location/location-<seoul|busan|jeju|daegu|all>`、
候位榜 `https://www.catchtable.net/zh-TW/top-list/waiting/<city>/all`。重新載入後在 Console 先定義累積器，然後**用滾輪**每次捲三格、等一秒、
再執行一次 `__scan()`，直到要的名次都齊、連續三步沒有新 alias。清單在捲過第 8 張卡（約 2,500px）之後才載下一頁；`window.scrollBy` 不會觸發，滾輪會。

```js
window.__r = { byRank: {}, byAlias: {}, conflicts: [] };
window.__scan = () => {
  for (const art of document.querySelectorAll("article")) {
    const badge = art.querySelector("div.absolute.top-0.left-0 span")            // 最佳榜
      || art.querySelector('div[class*="top-[0px]"][class*="left-[0px]"]');       // 候位榜
    const a = art.querySelector('a[href*="/shop/"]');
    const m = a ? (a.getAttribute("href") || "").match(/\/shop\/([^/?#]+)/) : null;
    const alias = m ? decodeURIComponent(m[1]) : null;
    const rank = badge && /^\d{1,3}$/.test(badge.textContent.trim()) ? Number(badge.textContent.trim()) : null;
    if (rank == null || !alias) continue;
    const label = (a.innerText || "").replace(/\s+/g, " ").trim().slice(0, 120);
    if (window.__r.byRank[rank] && window.__r.byRank[rank].alias !== alias) window.__r.conflicts.push({ rank, was: window.__r.byRank[rank].alias, now: alias });
    if (window.__r.byAlias[alias] != null && window.__r.byAlias[alias] !== rank) window.__r.conflicts.push({ alias, wasRank: window.__r.byAlias[alias], nowRank: rank });
    if (!window.__r.byRank[rank]) window.__r.byRank[rank] = { rank, alias, label };
    if (window.__r.byAlias[alias] == null) window.__r.byAlias[alias] = rank;
  }
  const ranks = Object.keys(window.__r.byRank).map(Number).sort((x, y) => x - y);
  return { n: ranks.length, max: ranks[ranks.length - 1], conflicts: window.__r.conflicts.length, scrollY: window.scrollY };
};
window.__scan();
// 捲完：JSON.stringify({ page: location.href, captured_at: new Date().toISOString(),
//   entries: Object.values(window.__r.byRank).sort((x, y) => x.rank - y.rank), conflicts: window.__r.conflicts }, null, 2)
```

關卡：`conflicts` 為空；名次從 1 連續到要的家數。榜單會隨時間變（同一天相隔 20 分鐘第 17–19 名順序就不同），`captured_at` 是證據，不補位。

## 店頁：訂位判定（lazy section 與隱藏面板）

服務區塊是 lazy section，靠 IntersectionObserver 掛載。**面板隱藏（`document.visibilityState === "hidden"`）或分頁在背景時永遠不會掛載**，
任何店都只剩底部「預訂」鈕或 `dock-waiting-btn`；`tabs_select` 救不了收起來的面板。判定一律連 `visibilityState` 一起記。
下面的片段先把 IntersectionObserver 包一層讓觀察器立刻回報進入視窗，再點「首頁」分頁讓區塊重新掛載——這只是讓頁面自己的元件在隱藏面板裡
照常渲染並向 CatchTable 取真實資料，不是繞過封鎖；做了要在報告揭露。先用一家已知可訂位的店當對照組。

```js
// 從 /zh-TW/shop/<alias>/info 進入（區塊還沒掛載），等 hreflang 出現後執行
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const q = s => document.querySelector(s);
  for (let i = 0; i < 20 && !q('link[rel=alternate]'); i++) await wait(500);
  if (!window.__ioPatched) {
    const Orig = window.IntersectionObserver;
    window.IntersectionObserver = class extends Orig {
      constructor(cb, opts) { super(cb, opts); this.__cb = cb; }
      observe(el) { super.observe(el); const self = this; setTimeout(() => { try { const r = el.getBoundingClientRect();
        self.__cb([{ isIntersecting: true, intersectionRatio: 1, target: el, time: performance.now(), boundingClientRect: r, intersectionRect: r, rootBounds: null }], self); } catch (e) {} }, 0); }
    };
    window.__ioPatched = true;
  }
  const home = [...document.querySelectorAll("a, button, div, span, li")].filter(e => (e.innerText || "").trim() === "首頁")[0];
  if (home) { (home.closest("a, button") || home).click(); await wait(3500); }
  for (let i = 0; i < 6; i++) { if (q('[data-testid="service-section-title"]') || q('[data-testid="service-tab-toggle"]') || q('[data-testid="waiting-remote-content"]') || q('[data-testid="waiting-onsite-content"]')) break; window.scrollBy(0, 400); await wait(1000); }
  const dining = q('[data-testid="service-tab-DINING"]');
  if (dining) { dining.click(); await wait(1500); }
  const body = document.body.innerText; const cut = body.indexOf("如果您喜歡"); const main = cut > 0 ? body.slice(0, cut) : body;
  return {
    visibility: document.visibilityState,
    hasDiningTab: !!dining, hasWaitingTab: !!q('[data-testid="service-tab-WAITING_REMOTE"]'), dock: q('[data-testid="dock-waiting-btn"]')?.innerText || null,
    dateTimePeople: /日期 • 時間 • 人/.test(main), findTimes: /尋找可用時間/.test(main),
    testids: [...document.querySelectorAll("[data-testid]")].map(e => e.getAttribute("data-testid")).filter((v, i, a) => a.indexOf(v) === i),
    hreflang: [...document.querySelectorAll("link[rel=alternate]")].map(l => l.hreflang + " " + l.href).filter(x => /zh-Hant|zh-Hans|^ja |x-default/.test(x)),
    api: performance.getEntriesByType("resource").filter(e => /api\.catchtable\.net\/api\/v5\/shop\//.test(e.name)).map(e => e.name.replace(/^.*\/api\/v5\/shop\//, "").replace(/\?.*$/, "")).filter((v, i, a) => a.indexOf(v) === i),
    head: main.slice(0, 300).replace(/\s+/g, " ")
  };
})()
```

| 看到 | booking | 平台列 |
| --- | --- | --- |
| `hasDiningTab` 且 `dateTimePeople` 且（`findTimes` 或有「預訂」鈕）；或沒有分頁切換但頁面直接是這組控制項（`service-section-title`＋日期列） | `reservation` | `verified` |
| 沒有 DINING；只有 `service-tab-WAITING_REMOTE`／`service-tab-RESERVED_ENTRY`／`waiting-remote-content`／`waiting-onsite-content`／dock | `waiting_only` | `disabled` |
| 什麼控制項都沒有 | `none` | `disabled` |
| 404 或身分對不上 | `unclear` | 不產列 |

`api` 裡出現 `dayslot-enc`／`timeslot-enc`／`online-reservation-open-schedule` 是訂位區塊真的掛上的旁證；`schedule` 只是營業時間。
dock 的「今日公休」是「現在不在營業時段」，不是判定依據。頁尾「如果您喜歡」列別家店，不看。

## 資訊分頁：地址、電話、網站

`navigate` 到 `/zh-TW/shop/<alias>/info`，等「位置」出現，點「原文語言」切成韓文道路名地址（點了之後韓文地址才會進 innerText）：

```js
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < 20 && !/位置/.test(document.body.innerText); i++) await wait(500);
  // 開關是 <button> 內的 <span>地址 原文語言</span>，不是獨立元素：找文字節點再點最近的 button
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let node, toggle = null;
  while ((node = walker.nextNode())) { if (/原文語言/.test(node.textContent)) { toggle = node.parentElement.closest("button") || node.parentElement; break; } }
  if (toggle) { toggle.click(); await wait(800); }
  const t = document.body.innerText.replace(/\n+/g, " | "); const i = t.indexOf("位置");
  return { info: t.slice(Math.max(0, i - 50), i + 1200),
           links: [...document.querySelectorAll('a[href^="http"]')].map(a => a.getAttribute("href")).filter(h => !/catchtable|apple\.com|play\.google|google\.com\/maps/.test(h)) };
})()
```

「網站」欄是 Instagram、smartstore 或 Naver 時記在 notes，不是來源；是店家自己的網域時去確認它講的是這家分店。

## 代理提示要帶的東西

- 硬規則九條（`docs/catchtable-ranking-discovery.md`「操作步驟與指令」）加上：來源網址只收 https；`notes` 1000 字、`quote` 300 字；訂位判定要連 `visibilityState` 一起寫進 `booking_observation`。
- 官方來源順序：觀光局店家頁（Visit Seoul `KOP…`／`ENP…`／`TCP…` 同尾碼同一頁；KTO 韓文 `detail/ms_detail.do?cotid=` 與英文 `contentsView.do?vcontsId=`；Visit Busan、Visit Jeju、`tour.daegu.go.kr`）→
  區廳（江南區 `visitgangnam.net`、首爾觀光財團 Taste of Seoul）→ 政府名冊 → 店家官網或母公司門市清單（要列這家分店的地址）。
  `korean.visitkorea.or.kr` 店家頁的地址是前端載入、內建瀏覽器導向會被彈回，改用英文站或 KTO 韓文的 `ms_detail` 網址。
- `/info` 分頁「網站」欄的網址原樣記進 `catchtable.website`（Instagram、smartstore 也記）；找不到官方頁時 `merchant_platform` 來源只能是這家的 CatchTable 店頁／`/info`，或等於這個欄位的網址，引文仍要含店名與地址。
- 分片檔每家寫完就覆寫；回報只回一張表。研究代理判訂位時分頁在背景，**一定要用上面的包裝片段**，否則會把可訂位的店看成候位。
