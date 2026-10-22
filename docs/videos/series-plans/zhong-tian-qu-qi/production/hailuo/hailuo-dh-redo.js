// Re-shooting shots of finished episodes (the 2026-10-19 scan of episodes 1-24), on top of
// hailuo-dh-img.js (image page) and hailuo-dh.js + hailuo-dh-loop.js (clip page).
// Jobs come from redo-dh-scan.json: { e, id, label: "aN-sNN-t6", names, prompt, clip: [text, sha16, secs] | null }.
//
// Image page: load the jobs once, split them in two halves so two image tabs can draw at the same
// time without drawing the same label, then drive one half per tab.
//   localStorage.ztredo = JSON.stringify(await (await fetch(base + "redo-dh-scan.json")).json()); __redoSplit();
//   __redoHook(); void __zt.drive(["RA"], 100);        // the other tab: "RB"
//   await __rnew()                                     // "done n/N" + download lines of new redraws
// Clip page: after a redraw is checked, queue its clip; the clip is saved as take t6 by fetch-dh.sh
// when the download line is rewritten to c:aN-sNN-t6 (scratch dlr.sh did it with sed).
//   __rq(["a3-s01-t6", "a5-s31-t6"])
(() => {
  window.__redoSplit = () => {
    const all = JSON.parse(localStorage.ztredo).sort((x, y) => x.names.join(",").localeCompare(y.names.join(",")));
    const h = Math.ceil(all.length / 2);
    localStorage.ztredoA = JSON.stringify(all.slice(0, h));
    localStorage.ztredoB = JSON.stringify(all.slice(h));
    return [h, all.length - h];
  };
  // "R" is every redo job, "RA".."RD" the split lists; anything else is an episode's own first frames.
  window.__redoHook = () => {
    if (!window.__zt) return "load hailuo-dh-img.js first";
    if (!__zt.ffjobsOrig) __zt.ffjobsOrig = __zt.ffjobs;
    __zt.ffjobs = function (e) {
      if (e === "R") return JSON.parse(localStorage.ztredo || "[]");
      if (/^R[A-D]$/.test(e)) return JSON.parse(localStorage["ztredo" + e[1]] || "[]");
      return this.ffjobsOrig(e);
    };
    return "redo lists hooked";
  };
  window.__rseen = window.__rseen || new Set();
  window.__rnew = async () => {
    await __zt.syncall();
    const u = __zt.urls();
    const jobs = JSON.parse(localStorage.ztredo || "[]");
    const lines = jobs.filter((j) => u[j.label] && !__rseen.has(j.label)).map((j) => { __rseen.add(j.label); return j.label + " 2 " + u[j.label].replace("/user/multi_chat_file/", "~"); });
    return "done " + jobs.filter((j) => u[j.label]).length + "/" + jobs.length + "\n" + lines.join("\n");
  };
  // Clip page: point the episode's first-frame alias at the redraw, forget the old clip everywhere
  // the driver looks (card map, downloads, card ids, five-minute guard) and queue the shot.
  window.__rq = (labels) => {
    const jobs = JSON.parse(localStorage.ztredo || "[]");
    const u = JSON.parse(localStorage.zturls || "{}");
    const cm = JSON.parse(localStorage.ztcmapdh || "{}");
    let dl = JSON.parse(localStorage.ztdlc || "[]");
    const ci = JSON.parse(localStorage.ztcidh || "{}");
    const q = JSON.parse(localStorage.dhq || "[]");
    const out = [];
    for (const lab of labels) {
      const j = jobs.find((x) => x.label === lab);
      if (!j || !j.clip) { out.push("skip " + lab); continue; }
      if (!u[lab]) { out.push("nourl " + lab); continue; }
      const key = "ztmiddh" + j.e;
      const mid = JSON.parse(localStorage[key] || "{}");
      mid[j.id] = j.clip;
      localStorage[key] = JSON.stringify(mid);
      u["edh" + j.e + "-" + j.id + "-t1"] = u[lab];
      const c = "c:a" + j.e + "-" + j.id;
      for (const [k, v] of Object.entries(cm)) if (v === c) cm[k] = "x:old-a" + j.e + "-" + j.id;
      dl = dl.filter((x) => x !== c);
      delete ci[c];
      if (window.__sentAt) delete __sentAt[c];
      const it = j.e + ":" + j.id;
      if (!q.includes(it)) q.push(it);
      out.push("ok " + lab);
    }
    localStorage.zturls = JSON.stringify(u);
    localStorage.ztcmapdh = JSON.stringify(cm);
    localStorage.ztdlc = JSON.stringify(dl);
    localStorage.ztcidh = JSON.stringify(ci);
    if (window.__sentAt) localStorage.ztsentat = JSON.stringify(__sentAt);
    localStorage.dhq = JSON.stringify(q);
    // The driver's loop returns when its queue empties, so start it again.
    window.__dhqstop = false;
    if (window.__dhq) void __dhq.run();
    return out.join(" ");
  };
  return "hailuo-dh-redo ready";
})();
