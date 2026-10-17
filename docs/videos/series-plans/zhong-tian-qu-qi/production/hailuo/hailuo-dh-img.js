// Image-generation page helpers for the 3D donghua first frames and reference sheets, in one file
// (the browser profile was wiped once; see hailuo-dh.js for the clip page). Paste into the image page:
//   __zt.go(label, prompt, nRefs, aspect)       submit one image (refs already prepped)
//   await __zt.prep(["dh-xuyan-portrait-t1"])   attach reference pictures by zturls label
//   __zt.cycle(n)                               sync finished URLs, list new downloads, submit up to n first frames
// First-frame jobs come from localStorage.ztffdhN (ff-dh-e00N.json); labels aN-sNN-tK, refs dh-*.
(() => {
  const sleep = async (ms) => { const t = performance.now(); while (performance.now() - t < ms) { try { await fetch("/favicon.ico?" + Math.random(), { cache: "no-store" }); } catch {} } };
  window.__job2 = { sleep };
  window.__yz = {
    editor() { const el = document.getElementById("video-create-textarea"); let f = el && Object.entries(el).find(([k]) => k.startsWith("__reactFiber"))?.[1]; while (f) { const v = f.memoizedProps?.value; if (v && typeof v.insertText === "function" && Array.isArray(v.children)) return v; f = f.return; } return null; },
    setPrompt(t) { const ed = this.editor(); if (!ed) return -1; const last = ed.children.length - 1; const lt = (ed.children[last].children ?? []).map((c) => c.text ?? "").join(""); ed.select({ anchor: { path: [0, 0], offset: 0 }, focus: { path: [last, 0], offset: lt.length } }); ed.deleteFragment(); ed.insertText(t); return t.length; },
    chip() { return [...document.querySelectorAll("span,div")].filter((e) => e.children.length === 0 && /^(21:9|16:9|3:4|4:3|9:16|1:1|2:3|3:2|4:5|5:4)$/.test(e.textContent.trim()) && !e.closest("[id^=media-group-]") && !e.closest(".grid")).map((e) => e.textContent.trim()); },
    bar() { const b = [...document.querySelectorAll("button")].find((x) => x.innerText.trim() === "創建"); let q = b; for (let i = 0; i < 4 && q; i++) q = q.parentElement; return q?.innerText.replace(/\s+/g, " ").trim(); },
    groups() { return [...document.querySelectorAll("[id^=media-group-]")].map((g) => g.id.replace("media-group-", "")); },
    refs() { return (document.body.innerText.match(/参考图\s*\((\d+)\/16\)/) || [])[1]; },
    async aspect(a) {
      const chip = [...document.querySelectorAll("span,div")].find((e) => e.children.length === 0 && /^(21:9|16:9|3:4|4:3|9:16|1:1|2:3|3:2|4:5|5:4)$/.test(e.textContent.trim()) && !e.closest("[id^=media-group-]") && !e.closest(".grid"));
      if (chip?.textContent.trim() === a) return a;
      chip?.click(); await sleep(800);
      const d = [...document.querySelectorAll("div.cursor-pointer")].find((e) => e.textContent.trim() === a && !e.closest("[id^=media-group-]"));
      const pk = d && Object.keys(d).find((k) => k.startsWith("__reactProps"));
      d?.[pk]?.onClick({ stopPropagation() {}, preventDefault() {}, currentTarget: d, target: d });
      await sleep(400); document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
      return this.chip().join(",");
    },
  };
  window.__feed = function () { const out = []; for (const el of document.querySelectorAll("[id^=media-group-]")) { const g = el.id.replace("media-group-", ""); let f = Object.entries(el).find(([k]) => k.startsWith("__reactFiber"))?.[1]; let bf = null; for (let k = 0; f && k < 8 && !bf; k++) { bf = f.memoizedProps?.batchFeed; f = f.return; } const x = bf?.feeds?.[0]; if (!x) continue; const s = JSON.stringify(x); const m = s.match(/"withoutWatermarkURL":"([^"]+)"/) || s.match(/"coverURL":"([^"]+)"/); const u = m ? m[1] : ""; out.push([g, x.commonInfo?.id, x.commonInfo?.status, (u.split("/moss/prod/")[1] || "").split("?")[0]].join(" ")); } return out.join("\n"); };
  window.__zt = {
    log(s) { const a = JSON.parse(localStorage.ztlog || "[]"); a.push(new Date().toISOString().slice(11, 19) + " " + s); localStorage.ztlog = JSON.stringify(a.slice(-300)); },
    urls() { return JSON.parse(localStorage.zturls || "{}"); },
    map() { return JSON.parse(localStorage.ztmap || "{}"); },
    input() { return [...document.querySelectorAll("input[type=file]")].find((i) => { let q = i; for (let k = 0; k < 5 && q; k++) q = q.parentElement; return /参考图/.test(q?.innerText || ""); }); },
    async clear() { for (let i = 0; i < 20 && __yz.refs() !== "0"; i++) { const b = document.querySelector('button[aria-label="Remove image"]'); if (!b) break; const pk = Object.keys(b).find((k) => k.startsWith("__reactProps")); if (b[pk]?.onClick) b[pk].onClick({ stopPropagation() {}, preventDefault() {} }); else b.click(); await sleep(500); } return __yz.refs(); },
    async prep(names) {
      if (__yz.refs() !== "0") return "refs not empty " + __yz.refs();
      const u = this.urls(); const dt = new DataTransfer(); const st = [];
      for (const n of names) { if (!u[n]) return "no url " + n; const r = await fetch("https://cdn.hailuoai.video/moss/prod/" + u[n]); st.push(r.status); dt.items.add(new File([await r.arrayBuffer()], n + ".png", { type: "image/png" })); }
      const input = this.input(); input.files = dt.files; input.dispatchEvent(new Event("change", { bubbles: true }));
      return JSON.stringify({ st, refs: __yz.refs() });
    },
    // One image. The new card is matched by its prompt text (the feed also shows video cards) and
    // waited for 40 s, since a hidden pane draws new cards late and an early retry buys a duplicate.
    async go(label, prompt, n, aspect) {
      if (Object.values(this.map()).includes(label)) return "already " + label;
      if (__yz.chip()[0] !== aspect) await __yz.aspect(aspect);
      const want = "1 " + (20 + n) + " 創建"; const t = performance.now();
      while ((__yz.bar() !== want || __yz.refs() !== String(n)) && performance.now() - t < 90000) await sleep(700);
      const chip = __yz.chip(); const bar = __yz.bar();
      if (chip.length !== 1 || chip[0] !== aspect || bar !== want || __yz.refs() !== String(n)) return "abort " + chip + " | " + bar + " | " + __yz.refs();
      const before = __yz.groups(); const key = prompt.replace(/\s+/g, " ").slice(0, 60);
      __yz.setPrompt(prompt); await sleep(1500);
      [...document.querySelectorAll("button")].find((x) => x.innerText.trim() === "創建").click();
      let fresh = []; const t2 = performance.now();
      while (!fresh.length && performance.now() - t2 < 40000) { await sleep(700); fresh = __yz.groups().filter((g) => !before.includes(g) && (document.getElementById("media-group-" + g)?.innerText || "").replace(/\s+/g, " ").includes(key)); }
      if (fresh.length) { const mm = this.map(); mm[fresh[0]] = label; localStorage.ztmap = JSON.stringify(mm); }
      return JSON.stringify({ label, fresh });
    },
    done() { const m = this.map(); return __feed().split("\n").filter((l) => m[l.split(" ")[0]]).map((l) => { const [g, c, s, u] = l.split(" "); return [m[g], s, u].join(" "); }).join("\n"); },
    // Finished image URLs into zturls (PNG only), with the edhN-sNN-t1 aliases the clip page reads.
    syncall() { const u = this.urls(); for (const l of this.done().split("\n")) { const [lab, s, url] = l.split(" "); if (s === "2" && url && /\.png$/.test(url) && /^(dh-|a\d+-)/.test(lab)) u[lab] = url; } for (const [k, v] of Object.entries(u)) { const m = k.match(/^a(\d+)-(s\d+)-t\d$/); if (m) u["edh" + m[1] + "-" + m[2] + "-t1"] = v; } localStorage.zturls = JSON.stringify(u); return Object.entries(u).filter(([k]) => /^(dh-|a\d+-s)/.test(k)).map(([k, v]) => k + " 2 " + v); },
    ffjobs(e) { return JSON.parse(localStorage["ztffdh" + e] || "[]").map((j) => ({ ...j, names: j.refs.map((r) => r.replace(/\.png$/, "")), label: "a" + e + "-" + j.id + "-t1" })); },
    ready(e) { const u = this.urls(); const used = new Set(Object.values(this.map())); return this.ffjobs(e).filter((j) => !used.has(j.label) && j.names.every((x) => u[x])); },
    async drive(eps, max) { window.__ztstop = false; let cur = null, n = 0; for (const e of eps) { for (const j of this.ready(e).sort((x, y) => x.names.join(",").localeCompare(y.names.join(",")))) { if (window.__ztstop || n >= max) { this.log("batch end " + n); return; } const key = j.names.join(","); if (key !== cur) { const c = await this.clear(); if (c !== "0") { this.log("clear failed " + c); return; } if (j.names.length) this.log("prep " + key + " " + (await this.prep(j.names))); cur = key; } for (let tries = 0; tries < 20; tries++) { const r = await this.go(j.label, j.prompt, j.names.length, "16:9"); const ok = r.startsWith("already") || /"fresh":\["\d/.test(r); this.log(j.label + " " + (ok ? "OK" : "retry " + r.slice(0, 80))); if (ok) { n++; break; } if (r.startsWith("abort") && __yz.refs() !== String(j.names.length)) { await this.clear(); if (j.names.length) await this.prep(j.names); } await sleep(30000); } } } this.log("batch end all " + n); },
    markdl(ls) { const dl = new Set(JSON.parse(localStorage.ztdl2 || "[]")); ls.forEach((x) => dl.add(x)); localStorage.ztdl2 = JSON.stringify([...dl]); return dl.size; },
    newdl() { const dl = new Set(JSON.parse(localStorage.ztdl2 || "[]")); return this.syncall().filter((l) => !dl.has(l.split(" ")[0])); },
  };
  return "hailuo-dh-img ready";
})();
