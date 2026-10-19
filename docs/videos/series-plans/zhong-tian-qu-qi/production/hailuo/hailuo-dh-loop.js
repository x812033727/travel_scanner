// Clip-page loop helpers that used to live only in localStorage.ztloopsrc and were lost with the
// 2026-10-18 account change. Eval after hailuo-dh.js on the image-to-video page:
//   __wd()        restart __dhq.run() when its log has not moved for 240 s (not after "queue empty")
//   __lost()      clips sent (in ztcmapdh / ztcidh) and not downloaded whose card left the list
//   __dups()      labels that more than one card was matched to (a resend: cancel one if queued)
//   __rec()       finished clips found through their detail page, "c:aN-sNN 2 <path>" for fetch-dh.sh
//   __oneOrig(id) the unguarded __dhc.one; __dhc.one itself refuses a resend within 5 minutes
// ZT_EPS below is the batch of episodes the helpers look at; change it for each batch.
(() => {
  window.ZT_EPS = window.ZT_EPS || JSON.parse(localStorage.zteps || "[25,26,27,28,29]");
  const inBatch = (label) => { const m = /^c:a(\d+)-/.exec(label); return !!m && ZT_EPS.includes(Number(m[1])); };
  const cmap = () => JSON.parse(localStorage.ztcmapdh || "{}");
  const cids = () => JSON.parse(localStorage.ztcidh || "{}");
  const dl = () => new Set(JSON.parse(localStorage.ztdlc || "[]"));

  let seen = -1, movedAt = performance.now();
  window.__wd = function () {
    const n = __dhq.log.length;
    if (n !== seen) { seen = n; movedAt = performance.now(); return "ok " + n; }
    if (__dhq.log.at(-1) === "queue empty") return "empty";
    if (performance.now() - movedAt < 240000) return "wait " + Math.round((performance.now() - movedAt) / 1000) + "s";
    movedAt = performance.now(); void __dhq.run(); return "restarted";
  };

  window.__lost = function () {
    const onList = new Set(Object.entries(cmap()).filter(([g]) => document.getElementById("media-group-" + g)).map(([, l]) => l));
    const got = dl(); const ids = cids();
    return Object.keys(ids).filter((l) => inBatch(l) && !got.has(l) && !onList.has(l)).map((l) => l + " " + ids[l]);
  };

  window.__dups = function () {
    const by = {};
    for (const [g, l] of Object.entries(cmap())) if (inBatch(l)) (by[l] ||= []).push(g);
    return Object.entries(by).filter(([, gs]) => gs.length > 1).map(([l, gs]) => l + " " + gs.join(","));
  };

  // A finished clip's detail page carries the watermark-free mp4 (moss/prod/...-0_*.mp4) in its HTML.
  window.__rec = async function (labels) {
    const ids = cids(); const got = dl(); const out = [];
    for (const l of labels || Object.keys(ids).filter((x) => inBatch(x) && !got.has(x))) {
      try {
        const html = await (await fetch("/zh-Hant/my-work-detail/ai-video/" + ids[l], { cache: "no-store" })).text();
        const m = html.match(/moss\/prod\/([^"'\\\s?]+?-0_[^"'\\\s?]*?\.mp4)/);
        if (m) out.push(l + " 2 " + m[1]);
      } catch {}
    }
    return out;
  };

  // A card that has not appeared yet reads as "not sent"; sending again buys a duplicate.
  if (!window.__oneOrig) window.__oneOrig = __dhc.one.bind(__dhc);
  window.__sentAt = JSON.parse(localStorage.ztsentat || "{}");
  __dhc.one = async function (id) {
    const label = "c:a" + localStorage.ztep.slice(2) + "-" + id;
    const at = __sentAt[label];
    if (at && Date.now() - at < 300000) return "recent " + id;
    __sentAt[label] = Date.now(); localStorage.ztsentat = JSON.stringify(__sentAt);
    return __oneOrig(id);
  };
  // ...and the driver skips it meanwhile instead of waiting on it (it picks the first ready shot).
  if (!__dhq.readyOrig) __dhq.readyOrig = __dhq.ready.bind(__dhq);
  __dhq.ready = function (it) { const [e, id] = it.split(":"); const at = __sentAt["c:a" + e + "-" + id]; return this.readyOrig(it) && !(at && Date.now() - at < 300000); };
  // A failed card (status 3 or 5, "刪除所有失敗") still carries the shot's prompt, so reconcile maps
  // it back to the shot and the driver never sends it again: release it after every reconcile.
  if (!__dhq.reconcileOrig) __dhq.reconcileOrig = __dhq.reconcile.bind(__dhq);
  __dhq.reconcile = function () {
    const fixed = this.reconcileOrig();
    const m = cmap(); const ids = cids(); let n = 0;
    for (const line of __feed().split("\n")) {
      const [g, , s] = line.split(" ");
      if (!["3", "5"].includes(s) || !/^c:a\d+-/.test(m[g] ?? "")) continue;
      const label = m[g]; m[g] = "x:fail-" + label.slice(2); delete ids[label]; delete __sentAt[label]; n++;
      fixed.push("failed " + label);
    }
    if (n) { localStorage.ztcmapdh = JSON.stringify(m); localStorage.ztcidh = JSON.stringify(ids); localStorage.ztsentat = JSON.stringify(__sentAt); }
    return fixed;
  };
  return "hailuo-dh-loop ready " + ZT_EPS.join(",");
})();
