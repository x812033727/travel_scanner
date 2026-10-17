// Image-to-video page helpers for the 3D donghua clips, in one file so a wiped browser profile can
// reload them (2026-10-17: quitting the app logged Hailuo out and cleared localStorage, which held
// every helper). Paste the whole file into the page (javascript_tool), then:
//   await __dh.boot(base)   // base = raw.githubusercontent URL of this folder at a pinned commit
//   void __dhq.run()        // one driver; __dhq.log, __dhq.clipsdone(), __dhq.markc([...])
// State lives in localStorage: zturls (first-frame CDN paths, edhN-sNN-t1 aliases), ztmiddhN
// (clip jobs), ztcmapdh (card group -> c:aN-sNN), ztcidh (label -> card id), ztdlc (downloaded).
window.__yz = {
  editor() { const el = document.getElementById("video-create-textarea"); let f = el && Object.entries(el).find(([k]) => k.startsWith("__reactFiber"))?.[1]; while (f) { const v = f.memoizedProps?.value; if (v && typeof v.insertText === "function" && Array.isArray(v.children)) return v; f = f.return; } return null; },
  bar() { const b = [...document.querySelectorAll("button")].find((x) => x.innerText.trim() === "創建"); let q = b; for (let i = 0; i < 4 && q; i++) q = q.parentElement; return q?.innerText.replace(/\s+/g, " ").trim(); },
  balance() { return (document.body.innerText.match(/\n([\d,]{5,})\nMax/) || [])[1]; },
  groups() { return [...document.querySelectorAll("[id^=media-group-]")].map((g) => g.id.replace("media-group-", "")); },
};
window.__yzv = {
  react(el, depth = 8) { for (let i = 0; i < depth && el; i++) { const pk = Object.keys(el).find((k) => k.startsWith("__reactProps")); if (pk && typeof el[pk].onClick === "function") { el[pk].onClick({ stopPropagation() {}, preventDefault() {}, currentTarget: el, target: el }); return true; } el = el.parentElement; } return false; },
  leaf(t, inPop) { return [...document.querySelectorAll("span,div")].find((e) => e.children.length === 0 && e.textContent.trim() === t && !e.closest("[id^=media-group-]") && (inPop ? !!e.closest(".ant-popover:not(.ant-popover-hidden)") : !e.closest(".ant-popover"))); },
  chips() { return [...document.querySelectorAll("span,div")].filter((e) => e.children.length === 0 && /^(全能參考|起始\/結束幀|16:9|21:9|自動|2K|768p|\d+s)$/.test(e.textContent.trim()) && !e.closest("[id^=media-group-]") && !e.closest(".ant-popover")).map((e) => e.textContent.trim()); },
};
// A sleep that keeps running while the pane is hidden (page timers freeze there).
const __sleep = async (ms) => { const t = performance.now(); while (performance.now() - t < ms) { try { await fetch("/favicon.ico?" + Math.random(), { cache: "no-store" }); } catch {} } };
window.__v2 = {
  pick(t) { const l = __yzv.leaf(t, true); if (l && !__yzv.react(l, 4)) l.click(); return t; },
  up() { const inp = document.querySelectorAll("input[type=file]")[0]; let q = inp; for (let k = 0; k < 8 && q; k++) q = q.parentElement; return ([...(q?.querySelectorAll("img") || [])].map((i) => i.src).find((s) => /cdn\.hailuoai.*multi_chat_file.*\.jpeg/.test(s)) || "").split("multi_chat_file/")[1] || ""; },
  openDur() { const cur = __yzv.chips().find((c) => /^\d+s$/.test(c)); return __yzv.react(__yzv.leaf(cur)); },
  esc() { document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true })); },
  async type(text) {
    const ed = __yz.editor(); const last = ed.children.length - 1; const lt = (ed.children[last].children ?? []).map((c) => c.text ?? "").join("");
    ed.select({ anchor: { path: [0, 0], offset: 0 }, focus: { path: [last, 0], offset: lt.length } }); ed.deleteFragment();
    text.split("\n").forEach((l, i) => { if (i) ed.insertBreak(); if (l) ed.insertText(l); });
    const typed = ed.children.map((n) => (n.children ?? []).map((c) => c.text).join("")).join("\n");
    return [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(typed)))].map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 16);
  },
};
window.__feed = function () { const out = []; for (const el of document.querySelectorAll("[id^=media-group-]")) { const g = el.id.replace("media-group-", ""); let f = Object.entries(el).find(([k]) => k.startsWith("__reactFiber"))?.[1]; let bf = null; for (let k = 0; f && k < 8 && !bf; k++) { bf = f.memoizedProps?.batchFeed; f = f.return; } const x = bf?.feeds?.[0]; if (!x) continue; const s = JSON.stringify(x); const m = s.match(/"withoutWatermarkURL":"([^"]+)"/) || s.match(/"coverURL":"([^"]+)"/); const u = m ? m[1] : ""; out.push([g, x.commonInfo?.id, x.commonInfo?.status, (u.split("/moss/prod/")[1] || "").split("?")[0]].join(" ")); } return out.join("\n"); };
window.__v3zt = {
  sleep: __sleep,
  url(id) { return "https://cdn.hailuoai.video/moss/prod/" + JSON.parse(localStorage.zturls)["edh" + localStorage.ztep.slice(2) + "-" + id + "-t1"]; },
  async mode() { let t = performance.now(); while (!__yzv.chips().length && performance.now() - t < 15000) await __sleep(500); for (let k = 0; k < 3 && !__yzv.chips().includes("起始/結束幀"); k++) { const l = __yzv.leaf("全能參考"); if (l) l.click(); await __sleep(900); __v2.pick("起始/結束幀"); t = performance.now(); while (!__yzv.chips().includes("起始/結束幀") && performance.now() - t < 6000) await __sleep(300); } return JSON.stringify(__yzv.chips()); },
  async upload(id) { const before = __v2.up(); const r = await fetch(this.url(id)); const buf = await r.arrayBuffer(); const inp = document.querySelectorAll("input[type=file]")[0]; const dt = new DataTransfer(); dt.items.add(new File([buf], id + ".png", { type: "image/png" })); inp.files = dt.files; inp.dispatchEvent(new Event("change", { bubbles: true })); let up = ""; const t = performance.now(); while (((up = __v2.up()) === before || !up) && performance.now() - t < 90000) await __sleep(500); window.__v3up = up; return JSON.stringify({ st: r.status, changed: up !== before, up: up.slice(0, 24) }); },
  async dur(secs) { const want = secs + "s"; if (__yzv.chips().includes(want) && __yzv.chips().includes("2K")) return "ok"; __v2.openDur(); await __sleep(1000); for (const t of ["2K", want]) { const c = [...document.querySelectorAll("span,div")].filter((e) => e.children.length === 0 && e.textContent.trim() === t && !e.closest("[id^=media-group-]")); const d = c.find((e) => { let q = e; for (let i = 0; i < 4 && q; i++) { q = q.parentElement; if (q && (t === "2K" ? /768p/.test(q.textContent) : /15s/.test(q.textContent))) return true; } return false; }); if (d) __yzv.react(d, 4); } await __sleep(600); __v2.esc(); await __sleep(600); return JSON.stringify(__yzv.chips()); },
  async go(id) { const [m, h, secs] = JSON.parse(localStorage["ztmid" + localStorage.ztep])[id]; const sha = await __v2.type(m); await __sleep(1500); const want = "1 " + secs * 12 + " 創建"; const up = __v2.up(); const pre = { bar: __yz.bar(), chips: __yzv.chips(), sha }; if (sha !== h || pre.bar !== want || !pre.chips.includes("起始/結束幀") || !pre.chips.includes("2K") || !up || up !== window.__v3up) return JSON.stringify({ abort: true, id, pre, want, h }); const before = __yz.groups(); [...document.querySelectorAll("button")].find((x) => x.innerText.trim() === "創建").click(); let fresh = []; const t = performance.now(); while (!fresh.length && performance.now() - t < 12000) { await __sleep(500); fresh = __yz.groups().filter((g) => !before.includes(g)); } await __sleep(1200); return JSON.stringify({ id, fresh, bal1: __yz.balance() }); },
};
window.__dhc = {
  rm() { const b = document.querySelector('button[aria-label="Remove image"]'); if (!b) return "none"; const pk = Object.keys(b).find((k) => k.startsWith("__reactProps")); if (b[pk]?.onClick) b[pk].onClick({ stopPropagation() {}, preventDefault() {} }); else b.click(); return "removed"; },
  cmap() { return JSON.parse(localStorage.ztcmapdh || "{}"); },
  async one(id) { const label = "c:a" + localStorage.ztep.slice(2) + "-" + id; if (Object.values(this.cmap()).includes(label) || JSON.parse(localStorage.ztdlc || "[]").includes(label)) return "already " + id; const r0 = this.rm(); await __sleep(1500); const up = await __v3zt.upload(id); const g = await __v3zt.go(id); return r0 + " | " + up + " | " + g; },
};
window.__dhq = {
  log: [],
  q() { return JSON.parse(localStorage.dhq || "[]"); },
  ready(it) { const [e, id] = it.split(":"); return !!JSON.parse(localStorage.zturls)["edh" + e + "-" + id + "-t1"]; },
  // Card text -> label by the clip prompt, so image cards or late cards never get a wrong label.
  reconcile() { const keys = []; for (const e of Object.keys(localStorage).filter((k) => /^ztmiddh\d+$/.test(k)).map((k) => k.slice(7))) { const mid = JSON.parse(localStorage["ztmiddh" + e] || "{}"); for (const [id, v] of Object.entries(mid)) keys.push(["c:a" + e + "-" + id, v[0].split("[Shot 1] ")[1].replace(/\s+/g, " ")]); } const m = __dhc.cmap(); const fixed = []; for (const el of document.querySelectorAll("[id^=media-group-]")) { const g = el.id.replace("media-group-", ""); const t = el.innerText.replace(/\s+/g, " "); const shot = t.split("[Shot 1] ")[1] || ""; const lens = keys.map(([l, k]) => { let i = 0; while (i < k.length && k[i] === shot[i]) i++; return i; }); const best = Math.max(0, ...lens); const hits = best >= 100 ? keys.filter((_, i) => lens[i] === best) : []; if (hits.length === 1) { if (m[g] !== hits[0][0]) { fixed.push(g + "=" + hits[0][0]); m[g] = hits[0][0]; } } else if (!hits.length && m[g] && /^c:a\d+-/.test(m[g])) { fixed.push("drop " + g + " " + m[g]); delete m[g]; } } localStorage.ztcmapdh = JSON.stringify(m); return fixed; },
  cardids() { const m = __dhc.cmap(); const ids = JSON.parse(localStorage.ztcidh || "{}"); for (const el of document.querySelectorAll("[id^=media-group-]")) { const g = el.id.replace("media-group-", ""); if (!m[g]) continue; let f = el[Object.keys(el).find((k) => k.startsWith("__reactFiber"))]; for (let i = 0; i < 10 && f; i++) { const bf = f.memoizedProps?.batchFeed; if (bf) { const c = bf.feeds?.[0]?.commonInfo?.id; if (c) ids[m[g]] = c; break; } f = f.return; } } localStorage.ztcidh = JSON.stringify(ids); return Object.keys(ids).length; },
  clipsdone() { const m = __dhc.cmap(); const dl = new Set(JSON.parse(localStorage.ztdlc || "[]")); return __feed().split("\n").filter((l) => { const [g, c, s, u] = l.split(" "); return m[g] && /^c:a\d+-/.test(m[g]) && s === "2" && u && /\.mp4$/.test(u) && !dl.has(m[g]); }).map((l) => { const [g, c, s, u] = l.split(" "); return m[g] + " 2 " + u; }); },
  markc(ls) { const dl = new Set(JSON.parse(localStorage.ztdlc || "[]")); ls.forEach((x) => dl.add(x)); localStorage.ztdlc = JSON.stringify([...dl]); return dl.size; },
  // The page's queue counter goes stale; toggling the favourites filter re-fetches the list.
  async refresh() { try { const b = [...document.querySelectorAll("button")].find((x) => x.textContent.trim() === "僅收藏"); const pk = Object.keys(b).find((k) => k.startsWith("__reactProps")); for (let i = 0; i < 2; i++) { b[pk].onClick({ stopPropagation() {}, preventDefault() {}, currentTarget: b, target: b }); await __sleep(4000); } } catch (e) {} },
  async run() { window.__dhqstop = false; const gen = (window.__dhgen = (window.__dhgen || 0) + 1); while (!window.__dhqstop && gen === window.__dhgen) { this.reconcile(); this.cardids(); const done = new Set([...Object.values(__dhc.cmap()), ...JSON.parse(localStorage.ztdlc || "[]")]); const left = this.q().filter((it) => { const [e, id] = it.split(":"); return !done.has("c:a" + e + "-" + id); }); if (!left.length) { this.log.push("queue empty"); return; } const it = left.find((x) => this.ready(x)); if (!it) { await __sleep(30000); continue; } const [e, id] = it.split(":"); localStorage.ztep = "dh" + e; const r = await __dhc.one(id); await __sleep(4000); const fx = this.reconcile(); this.log.push(new Date().toISOString().slice(11, 19) + " " + it + " " + ((r.match(/"fresh":\[[^\]]*\]|abort|bal1":"[\d,]+/g) || []).join(" ")) + (fx.length ? " | " + fx.join("; ") : "")); if (!/"fresh":\["\d+/.test(r)) { if (/abort/.test(r)) __dhc.rm(); await __sleep(30000); await this.refresh(); await __sleep(20000); } } },
};
window.__dh = {
  // Loads clip jobs from GitHub, first-frame URLs from the given receipt lines ("label url"),
  // sets the page to start/end-frame mode, 2K, 4 s, and queues every clip of episodes 2-5.
  async boot(base, receipts, downloaded, eps = [2, 3, 4, 5]) {
    if (downloaded) __dhq.markc(downloaded);
    for (const e of eps) { const c = await (await fetch(base + "clips-dh-e" + String(e).padStart(3, "0") + ".json")).json(); const mid = {}; for (const [k, v] of Object.entries(c)) mid[k.replace(/^a\d+-/, "")] = v; localStorage["ztmiddh" + e] = JSON.stringify(mid); }
    if (receipts) { const u = JSON.parse(localStorage.zturls || "{}"); for (const line of receipts.trim().split("\n")) { const [lab, url] = line.split(" "); const m = lab.match(/^a(\d+)-(s\d+)-t\d$/); if (m) u["edh" + m[1] + "-" + m[2] + "-t1"] = url.split("/moss/prod/")[1]; } localStorage.zturls = JSON.stringify(u); }
    const ids = (e) => Object.keys(JSON.parse(localStorage["ztmiddh" + e])).map((id) => e + ":" + id);
    localStorage.dhq = JSON.stringify(eps.flatMap(ids));
    localStorage.ztep = "dh" + eps[0];
    const a = await __v3zt.mode(); const b = await __v3zt.dur(4);
    return [a, b, __yz.bar(), __yz.balance(), this.reconcileAll()];
  },
  reconcileAll() { const fx = __dhq.reconcile(); __dhq.cardids(); return Object.values(__dhc.cmap()).filter((v) => /c:a\d+-/.test(v)).length + " mapped; " + fx.length + " fixed"; },
};
"hailuo-dh ready";
