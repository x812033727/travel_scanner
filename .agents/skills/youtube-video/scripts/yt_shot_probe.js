// Shot probe for a YouTube watch page: how often a reference video cuts, and what each shot shows.
//
// Run it in the in-app browser's JavaScript tool on an open watch page (the pane may be hidden;
// seeking and reading frames still work there). It defines window.__probe and changes nothing on
// the page except pausing and muting the player and, for a contact sheet, drawing one overlay.
// What the numbers do and do not prove, and how to record a study, is in
// .agents/skills/youtube-video/references/drama-craft.md.
//
//   1. Set the tab's viewport to 1200x800 first (a hidden pane can report a 0x0 window, and the
//      sheets are sized from the window). Open the video in a tab of its own.
//   2. Paste this file's text into the JavaScript tool. A fresh watch page refuses to eval
//      stored text (Trusted Types), so paste the text itself every time the page is loaded.
//   3. An advertisement replaces the video element's source, before the start and again in the
//      middle of a long video. Wait for it, or press its skip button with a real click (a
//      scripted .click() is ignored). __probe.meta().ad says whether one is showing; measure()
//      stops with status "ad" and sheet() returns { ad: true } without drawing when one starts.
//   4. Start the measurement without leaving its promise as the last expression (the tool
//      would wait for it and time out after about 45 s):
//          void __probe.measure({ start: 0, end: 240, step: 0.25 }); "started"
//      then poll __probe.state.status in later calls until it is "done" (about ten samples a
//      second) and read __probe.stats().
//   5. One frame from the middle of each shot, then one screenshot:
//          await __probe.sheet(__probe.mids(48), { cols: 12 })   // 9:16 video: 48 frames fit
//          await __probe.sheet(__probe.mids(72), { cols: 8 })    // 16:9 video: 72 frames fit
//      sheet() draws only what fits the window and returns { drawn, dropped }; ask for the rest
//      with mids(count, from). Keep a call under about 30 frames when the page is slow, and wait
//      a second before the screenshot: a hidden pane paints the overlay late.
//   6. Burned-in dialogue, read without sound: the subtitle band of every half second.
//          await __probe.sheet(__probe.every(0.5, 12, 0.5), { cols: 3, crop: [0.76, 0.98] })
//      The crop is [top, bottom] as fractions of the frame height: about [0.76, 0.98] on a 16:9
//      frame, [0.64, 0.8] or [0.74, 0.9] on a 9:16 one; look at one full frame first. A step
//      longer than half a second misses short lines, so do not state line lengths from one.
//   7. __probe.hide() removes the overlay. Reset the viewport and close the tab when done.
//
// What a cut is here: the frame's luma grid changed sharply against the sample before it, as a
// spike rather than as part of a run. Most cuts are placed within the step. A dissolve can be
// missed. A flash, a light leak or a fast move makes a run of flagged samples: the run is
// counted once, at its first sample, which can be more than a second before the real cut, and a
// fast move inside one shot can be counted as a cut. So quote the median and the spread, not a
// single shot's length, and check a contact sheet against the cuts before quoting anything.
(() => {
  const video = document.querySelector("video");
  const player = document.getElementById("movie_player");
  if (!video || !player) return "no player on this page";
  const W = 64, H = 64;
  const canvas = document.createElement("canvas");
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const adShowing = () => player.classList.contains("ad-showing");

  const seek = (t) => new Promise((resolve) => {
    let done = false;
    const finish = (ok) => { if (done) return; done = true; video.removeEventListener("seeked", on); resolve(ok); };
    const on = () => finish(true);
    video.addEventListener("seeked", on);
    video.currentTime = t;
    setTimeout(() => finish(false), 5000);
  });
  const ready = async () => {
    const t0 = Date.now();
    while (video.readyState < 2 && Date.now() - t0 < 4000) await sleep(40);
    return video.readyState >= 2;
  };

  // The frame without its bottom quarter: burned-in subtitles change there on every line and
  // would read as cuts.
  const signature = () => {
    ctx.drawImage(video, 0, 0, W, H);
    const keep = Math.floor(H * 0.74);
    const pixels = ctx.getImageData(0, 0, W, keep).data;
    const luma = new Float32Array(W * keep);
    const hist = new Float32Array(16);
    for (let i = 0, j = 0; i < pixels.length; i += 4, j++) {
      const y = (pixels[i] * 3 + pixels[i + 1] * 6 + pixels[i + 2]) / 10;
      luma[j] = y; hist[Math.min(15, y >> 4)] += 1;
    }
    for (let i = 0; i < 16; i++) hist[i] /= luma.length;
    return { luma, hist };
  };
  const distance = (a, b) => {
    let mad = 0; for (let i = 0; i < a.luma.length; i++) mad += Math.abs(a.luma[i] - b.luma[i]);
    let hd = 0; for (let i = 0; i < 16; i++) hd += Math.abs(a.hist[i] - b.hist[i]);
    return [mad / a.luma.length, hd / 2];
  };

  // samples: [time, mean absolute luma difference to the sample before (0–255), histogram distance (0–1)]
  const state = { status: "idle", samples: [], failed: 0, range: [0, 0, 0.25] };

  async function measure({ start = 0, end = 240, step = 0.25 } = {}) {
    video.pause(); if (player.mute) player.mute();
    Object.assign(state, { status: "running", samples: [], failed: 0, range: [start, end, step] });
    let previous = null;
    for (let t = start; t <= end + 1e-6; t += step) {
      if (adShowing()) { state.status = "ad"; return; }
      if (!(await seek(t)) || !(await ready()) || adShowing()) { state.failed += 1; continue; }
      const current = signature();
      if (previous) { const [mad, hd] = distance(previous, current); state.samples.push([+t.toFixed(2), +mad.toFixed(1), +hd.toFixed(3)]); }
      previous = current;
    }
    state.status = "done";
  }

  function cuts({ mad = 26, hd = 0.22, soft = 16 } = {}) {
    const s = state.samples, [, end, step] = state.range, out = [];
    for (let i = 0; i < s.length; i++) {
      const [t, m, h] = s[i];
      // The last sample has no neighbour after it and would end the range on a zero-length shot.
      if (t >= end - step / 2) continue;
      const before = i > 0 ? s[i - 1][1] : 0, after = i + 1 < s.length ? s[i + 1][1] : 0;
      const spike = m > 2.2 * Math.max(before, after, 4);
      if ((m >= mad && (h >= hd / 2 || spike)) || (m >= soft && h >= hd && spike)) out.push(t);
    }
    // Flagged samples in a row are one cut seen more than once; the first is kept.
    return out.filter((t, i) => i === 0 || t - out[i - 1] > step * 1.5);
  }

  const edges = (options) => [state.range[0], ...cuts(options), state.range[1]];

  function stats(options) {
    const found = cuts(options), all = edges(options), [start, end] = state.range, lengths = [];
    for (let i = 1; i < all.length; i++) lengths.push(+(all[i] - all[i - 1]).toFixed(2));
    const sorted = [...lengths].sort((a, b) => a - b);
    const q = (p) => sorted[Math.min(sorted.length - 1, Math.floor(p * sorted.length))];
    // Inside shots: the share of samples whose picture all but equals the one before. It says
    // how often the frame is frozen, not how much anyone moves.
    const flagged = new Set(found);
    const inside = state.samples.filter((sample) => !flagged.has(sample[0])).map((sample) => sample[1]);
    return {
      status: state.status, failed: state.failed, range: state.range, shots: lengths.length,
      mean: +((end - start) / lengths.length).toFixed(2), median: q(0.5), p10: q(0.1), p90: q(0.9),
      longest: sorted[sorted.length - 1], over_6s: lengths.filter((x) => x > 6).length,
      opening_10s: all.slice(0, -1).filter((t) => t < start + 10).length,
      opening_30s: all.slice(0, -1).filter((t) => t < start + 30).length,
      near_frozen_share: inside.length ? +(inside.filter((x) => x < 1).length / inside.length).toFixed(3) : null,
      cuts: found, lengths,
    };
  }

  /** The middle of each of `count` shots from shot `from` (the last shot included). */
  function mids(count, from = 0) {
    const all = edges(), out = [];
    for (let i = from; i < from + count && i + 1 < all.length; i++) out.push(+((all[i] + all[i + 1]) / 2).toFixed(1));
    return out;
  }

  /** Times from `start` to `end` every `step` seconds, for a subtitle-band sheet. */
  const every = (start, end, step) => Array.from({ length: Math.floor((end - start) / step + 1e-6) + 1 }, (_, i) => +(start + i * step).toFixed(2));

  /**
   * Frames at `times` in one overlay; crop = [top, bottom] as fractions of the frame height.
   * Only the frames that fit the window are drawn: { drawn, dropped } says how many.
   */
  async function sheet(times, { cols = 8, crop = [0, 1] } = {}) {
    video.pause();
    if (!times.length) return { drawn: 0, dropped: 0 };
    if (adShowing()) return { ad: true, drawn: 0 };
    if (!innerWidth || !innerHeight) return { error: "the window reports no size: set the viewport first" };
    let host = document.getElementById("__probe_sheet");
    if (!host) {
      host = document.createElement("canvas"); host.id = "__probe_sheet";
      host.style.cssText = "position:fixed;left:0;top:0;z-index:2147483647;background:#111";
      document.body.appendChild(host);
    }
    await seek(times[0]); await ready();
    const cw = Math.floor(innerWidth / cols);
    const ch = Math.round((cw * video.videoHeight * (crop[1] - crop[0])) / video.videoWidth);
    const rows = Math.max(1, Math.min(Math.ceil(times.length / cols), Math.floor(innerHeight / ch)));
    const fit = Math.min(times.length, rows * cols);
    host.width = innerWidth; host.height = rows * ch;
    host.style.display = "block";
    const g = host.getContext("2d"); g.fillStyle = "#111"; g.fillRect(0, 0, host.width, host.height);
    let unread = 0;
    for (let i = 0; i < fit; i++) {
      await seek(times[i]); if (!(await ready())) unread += 1;
      // An advertisement can start during the seek: its frame must not be drawn under a label.
      if (adShowing()) return { ad: true, drawn: i, dropped: times.length - i };
      // The stream can change resolution, so the frame size is read for every frame.
      const vw = video.videoWidth, vh = video.videoHeight;
      const x = (i % cols) * cw, y = Math.floor(i / cols) * ch;
      g.drawImage(video, 0, vh * crop[0], vw, vh * (crop[1] - crop[0]), x, y, cw - 2, ch - 2);
      g.fillStyle = "rgba(0,0,0,.75)"; g.fillRect(x, y, 46, 16);
      g.fillStyle = "#ff0"; g.font = "12px monospace"; g.fillText(String(times[i]), x + 3, y + 12);
    }
    return { cols, rows, cell: [cw, ch], frame: [video.videoWidth, video.videoHeight], drawn: fit, dropped: times.length - fit, unread };
  }
  const hide = () => { const host = document.getElementById("__probe_sheet"); if (host) host.remove(); };

  /** What the page says about the video: for the study record, not for judging it. */
  function meta() {
    const response = (player.getPlayerResponse && player.getPlayerResponse()) || {};
    const details = response.videoDetails || {};
    const micro = (response.microformat && response.microformat.playerMicroformatRenderer) || {};
    const tracks = (response.captions && response.captions.playerCaptionsTracklistRenderer && response.captions.playerCaptionsTracklistRenderer.captionTracks) || [];
    return {
      id: details.videoId, title: details.title, channel: details.author, views: details.viewCount,
      seconds: details.lengthSeconds, published: micro.publishDate, frame: [video.videoWidth, video.videoHeight],
      qualities: player.getAvailableQualityLevels && player.getAvailableQualityLevels(),
      captions: tracks.map((track) => track.languageCode + ":" + (track.kind || "manual")), ad: adShowing(),
    };
  }

  window.__probe = { measure, cuts, stats, mids, every, sheet, hide, meta, state, seek };
  return "probe ready";
})();
