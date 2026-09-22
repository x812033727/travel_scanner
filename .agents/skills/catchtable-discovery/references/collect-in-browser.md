# 本機瀏覽器：收集榜單、看店頁、找官方來源

只在本機做（站主的 Chrome／Edge，或本機 Claude Code／Codex 的瀏覽器）。雲端容器對
`api.catchtable.net` 是 Cloudflare 403，headless Chromium 卡代理憑證，別再試。

## 1. 榜頁抄清單

打開榜頁，**先捲到底讓清單全部載入**（有分頁或無限捲動就一直捲到不再增加），再在 DevTools
Console 貼這段。它把頁面上所有 `/shop/<alias>` 連結依 DOM 順序列出，去重，印成 JSON 並複製到剪貼簿：

```js
(() => {
  const seen = new Map();
  for (const a of document.querySelectorAll('a[href*="/shop/"]')) {
    const m = (a.getAttribute("href") || "").match(/\/shop\/([^/?#]+)/);
    if (!m) continue;
    const alias = decodeURIComponent(m[1]);
    if (seen.has(alias)) continue;
    const label = (a.innerText || a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 200);
    seen.set(alias, { rank: seen.size + 1, alias, label });
  }
  const out = { page: location.href, captured_at: new Date().toISOString(), entries: [...seen.values()] };
  console.log(JSON.stringify(out, null, 2));
  if (typeof copy === "function") copy(JSON.stringify(out, null, 2));
})();
```

貼進 `rankings.json` 之前對三件事：

- **家數**與畫面上的一致；多出來的通常是頁尾「如果您喜歡」的推薦或導覽列，刪掉。
- **`rank` 是 DOM 順序**，畫面有名次數字就照畫面改。
- `label` 只是幫你認店；店名、料理、區域以店頁為準。

候位榜的路徑是 `/zh-TW/top-list/waiting/<city>/<cuisine>`，最佳餐廳榜是
`/zh-TW/ranking/location/<region>`；換城市或料理就是換路徑段，先在畫面上切一次再抄網址，不要猜。

## 2. 店頁怎麼看

開 `https://www.catchtable.net/zh-TW/shop/<alias>`，等它渲染完（空殼對不存在的 alias 也回 200，
真正的 404 是渲染後才出現）。要抄的：

| 東西 | 在哪裡 | Console 幫手 |
| --- | --- | --- |
| 韓文店名（含分店名） | 標題底下的原文 | — |
| 道路名地址、電話、營業時間 | 資訊分頁 | — |
| 料理類型、區域 | 標題附近的標籤 | — |
| 四語網址 | `hreflang` | `[...document.querySelectorAll('link[rel="alternate"]')].map(l => l.hreflang + " " + l.href)` |
| 訂位控制項 | 頁面底部的固定列與日期選擇 | `[...document.querySelectorAll("button")].map(b => b.innerText.trim()).filter(Boolean)`；`document.querySelector('[data-testid="dock-waiting-btn"]')?.innerText` |

判定（2026-09-11 站主規則，2026-09-21 實測）：

- 有「預訂」、日期與人數選擇、「尋找可用時間」→ `reservation`。
- 只有 `dock-waiting-btn`「登記遠端候位」→ `waiting_only`。
- 什麼控制項都沒有 → `none`；當天顯示「今日公休」而看不到控制項 → `unclear`，改天再開。
- **不整頁搜「預訂」**：頁尾「如果您喜歡」會列別家可訂位的店。
- 平台 API 的 `serviceTypes` 欄位單獨看會誤判（효뜨那筆含 `DINING_GLOBAL` 卻只能候位），一律以渲染後的控制項為準。

## 3. 官方來源去哪找（依序）

來源要是**講這家分店**的頁，文字看得到、當天讀到。等級照 `docs/korea-food-specials/README.md`：

1. 觀光局店家頁：Visit Seoul（店家頁網址帶 `KOP…` 編號）、VisitKorea（繁中站
   `big5chinese.visitkorea.or.kr`、英文站 `english.visitkorea.or.kr`）、Visit Busan、Visit Jeju、
   `tour.daegu.go.kr`、`tour.jeonju.go.kr`、區廳的美食名錄。
2. 政府認證名冊：백년가게、서울미래유산。
3. 店家自己的官網（CatchTable 店頁資訊分頁常有「홈페이지」連結；Instagram、Naver 部落格、
   smartstore 不算）。

抓頁用 `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"`，先剝掉
`<!-- -->` 再讀，看狀態碼；引文逐字抄，300 字內；`checked_on` 是真的打開那頁的日期。米其林官網對
我們每個工具都 403，不當來源也不繞。

找不到就 `no_official_source`，把搜過的關鍵字寫進 `notes`，下一批不用重找。

## 4. 每家店做完就存

一家寫完就存 `candidates.json`；代理被切斷時留下的是檔案，不是報告。十家一組交回，換人抽三分之一
重開店頁與官方頁。
