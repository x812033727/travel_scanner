eval(localStorage.yzsrc);eval(localStorage.feedsrc);eval(localStorage.job2src);
window.__zt = {
  urls() { return JSON.parse(localStorage.zturls || "{}"); },
  map() { return JSON.parse(localStorage.ztmap || "{}"); },
  bal() { return (document.body.innerText.match(/\n([\d,]{4,6})\n繁中/) || [])[1]; },
  input() { return [...document.querySelectorAll("input[type=file]")].find((i) => { let q = i; for (let k = 0; k < 5 && q; k++) q = q.parentElement; return /参考图/.test(q?.innerText || ""); }); },
  async prep(names) {
    if (__yz.refs() !== "0") return "refs not empty " + __yz.refs();
    const u = this.urls(); const dt = new DataTransfer(); const st = [];
    for (const n of names) { if (!u[n]) return "no url " + n; const r = await fetch("https://cdn.hailuoai.video/moss/prod/" + u[n]); st.push(r.status); dt.items.add(new File([await r.arrayBuffer()], n + ".png", { type: "image/png" })); }
    const input = this.input(); input.files = dt.files; input.dispatchEvent(new Event("change", { bubbles: true }));
    return JSON.stringify({ st, refs: __yz.refs() });
  },
  async go(label, prompt, n, aspect) {
    const m = this.map(); if (Object.values(m).includes(label)) return "already " + label;
    if (__yz.chip()[0] !== aspect) await __yz.aspect(aspect);
    const want = "1 " + (20 + n) + " 創建"; const t = performance.now();
    while ((__yz.bar() !== want || __yz.refs() !== String(n)) && performance.now() - t < 40000) await __job2.sleep(700);
    const chip = __yz.chip(); const bar = __yz.bar();
    if (chip.length !== 1 || chip[0] !== aspect || bar !== want || __yz.refs() !== String(n)) return "abort " + chip + " | " + bar + " | " + __yz.refs();
    const before = __yz.groups(); const bal0 = this.bal();
    __yz.setPrompt(prompt); await __job2.sleep(1500);
    [...document.querySelectorAll("button")].find((x) => x.innerText.trim() === "創建").click();
    let fresh = []; const t2 = performance.now();
    while (!fresh.length && performance.now() - t2 < 15000) { await __job2.sleep(500); fresh = __yz.groups().filter((g) => !before.includes(g)); }
    await __job2.sleep(800);
    const card = fresh.length ? document.getElementById("media-group-" + fresh[0]).innerText : "";
    if (fresh.length) { const mm = this.map(); mm[fresh[0]] = label; localStorage.ztmap = JSON.stringify(mm); }
    return JSON.stringify({ label, fresh, match: card.includes(prompt.slice(0, 30)), bal0, bal1: this.bal() });
  },
  done() { const m = this.map(); return __feed().split("\n").filter((l) => m[l.split(" ")[0]]).map((l) => { const [g, c, s, u] = l.split(" "); return [m[g], s, u].join(" "); }).join("\n"); },
};
"zt ready";
