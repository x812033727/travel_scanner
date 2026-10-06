/**
 * The shot probe the youtube-video skill ships (.agents/skills/youtube-video/scripts/yt_shot_probe.js).
 *
 * The probe runs pasted into a YouTube watch page, so it is one IIFE with no imports; here it runs
 * in a vm context with a stub page, and its samples are set by hand. Two things are pinned. The
 * cut list is the one every recorded study quotes (docs/videos/drama-craft/), so cuts() and the
 * stats fields that existed before the run report must give what the 2026-10-03 version gave:
 * LEGACY below is that version's code, copied unchanged. And a run of flagged samples, which
 * cuts() folds into one cut, is reported with its start and end: on the 2026-10-04 budaimiao
 * battle videos such runs held 8 or more real cuts each.
 */
import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const SOURCE = readFileSync(new URL("../.agents/skills/youtube-video/scripts/yt_shot_probe.js", import.meta.url), "utf8");

/** A fresh probe in its own context; nothing in it touches the stub page until measure() or sheet(). */
function load() {
  const context = {
    setTimeout,
    document: {
      querySelector: (selector) => (selector === "video" ? { pause() {}, addEventListener() {}, removeEventListener() {} } : null),
      getElementById: (id) => (id === "movie_player" ? { classList: { contains: () => false } } : null),
      createElement: () => ({ getContext: () => ({}) }),
    },
  };
  context.window = context;
  assert.equal(vm.runInNewContext(SOURCE, context), "probe ready");
  return context.window.__probe;
}

/** Values made in the vm context have its own prototypes; compare plain copies. */
const plain = (value) => JSON.parse(JSON.stringify(value));

// The 2026-10-03 cut rule and stats, as they were before the run report was added.
const LEGACY = {
  cuts(state, { mad = 26, hd = 0.22, soft = 16 } = {}) {
    const s = state.samples, [, end, step] = state.range, out = [];
    for (let i = 0; i < s.length; i++) {
      const [t, m, h] = s[i];
      if (t >= end - step / 2) continue;
      const before = i > 0 ? s[i - 1][1] : 0, after = i + 1 < s.length ? s[i + 1][1] : 0;
      const spike = m > 2.2 * Math.max(before, after, 4);
      if ((m >= mad && (h >= hd / 2 || spike)) || (m >= soft && h >= hd && spike)) out.push(t);
    }
    return out.filter((t, i) => i === 0 || t - out[i - 1] > step * 1.5);
  },
  stats(state, options) {
    const found = LEGACY.cuts(state, options), all = [state.range[0], ...found, state.range[1]];
    const [start, end] = state.range, lengths = [];
    for (let i = 1; i < all.length; i++) lengths.push(+(all[i] - all[i - 1]).toFixed(2));
    const sorted = [...lengths].sort((a, b) => a - b);
    const q = (p) => sorted[Math.min(sorted.length - 1, Math.floor(p * sorted.length))];
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
  },
};

/** A small seeded generator, so a failure names a series that can be rebuilt. */
function random(seed) {
  let x = seed >>> 0;
  return () => {
    x = (x + 0x6d2b79f5) >>> 0;
    let t = Math.imul(x ^ (x >>> 15), 1 | x);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Samples over [start, end] at `step` the way measure() records them (the first time has no
 * sample before it). `kind(t, next)` gives [mad, histogram distance] for the sample at t.
 */
function series(start, end, step, kind) {
  const samples = [];
  for (let t = start + step; t <= end + 1e-6; t += step) {
    const [m, h] = kind(+t.toFixed(2));
    samples.push([+t.toFixed(2), +m.toFixed(1), +h.toFixed(3)]);
  }
  return { status: "done", failed: 0, range: [start, end, step], samples };
}

/** A dialogue-like edit: quiet shots of 1-5 s, clean cuts, now and then a cut seen twice or a flash. */
function dialogue(seed, { start = 0, end = 120, step = 0.25 } = {}) {
  const next = random(seed), events = new Map();
  for (let t = start + 1; t < end; t += 1 + next() * 4) {
    const at = +(Math.round(t / step) * step).toFixed(2), roll = next();
    events.set(at, [30 + next() * 50, 0.15 + next() * 0.5]);
    // A cut that falls between two samples is seen by both; a light leak or a flash makes three.
    if (roll < 0.2) events.set(+(at + step).toFixed(2), [27 + next() * 20, 0.12 + next() * 0.2]);
    if (roll < 0.05) events.set(+(at + 2 * step).toFixed(2), [27 + next() * 20, 0.12 + next() * 0.2]);
  }
  return series(start, end, step, (t) => events.get(t) || [next() * 6, next() * 0.05]);
}

/** An effect-heavy edit: every sample anywhere from still to a cut, so each branch of the rule is hit near its edge. */
function busy(seed) {
  const next = random(seed);
  return series(0, 120, 0.25, () => {
    const roll = next();
    return [roll < 0.4 ? next() * 8 : roll < 0.7 ? 8 + next() * 22 : 16 + next() * 54, next() * 0.5];
  });
}

test("cuts() and the earlier stats fields give what the 2026-10-03 probe gave", () => {
  const probe = load();
  const checks = [];
  for (let seed = 1; seed <= 100; seed++) checks.push(dialogue(seed));
  // Different steps and a range that does not start at zero, as the studies used.
  checks.push(dialogue(101, { step: 0.125 }), dialogue(102, { start: 1800, end: 1920 }));
  // Busy series too: the rule must not drift where it is weakest either.
  for (let seed = 201; seed <= 240; seed++) checks.push(busy(seed));
  for (const state of checks) {
    probe.state.samples = state.samples;
    probe.state.range = state.range;
    for (const options of [undefined, { mad: 20 }, { hd: 0.3, soft: 12 }]) {
      assert.deepEqual(plain(probe.cuts(options)), LEGACY.cuts(state, options));
      const { high_motion_share, suspected_multi_cut_runs, ...earlier } = plain(probe.stats(options));
      assert.deepEqual(earlier, plain({ ...LEGACY.stats(state, options), status: probe.state.status, failed: probe.state.failed }));
      assert.equal(typeof high_motion_share, "number");
      assert.ok(Array.isArray(suspected_multi_cut_runs));
    }
  }
});

test("a run of back-to-back flagged samples is kept as one cut and reported with its start and end", () => {
  const probe = load();
  // Quiet shots with clean cuts at 5 and 30 s; 19.75-25.5 s is a montage of 0.25-0.5 s shots
  // where every sample changes as much as a cut (the budaimiao video B pattern).
  const state = series(0, 40, 0.25, (t) => {
    if (t === 5 || t === 30) return [60, 0.4];
    if (t >= 19.75 && t <= 25.5) return [30 + ((t * 8) % 5) * 6, 0.2];
    return [3, 0.02];
  });
  probe.state.samples = state.samples;
  probe.state.range = state.range;
  assert.deepEqual(plain(probe.cuts()), [5, 19.75, 30]);
  assert.deepEqual(plain(probe.runs()), [{ start: 19.75, end: 25.5, flagged: 24 }]);
  const stats = plain(probe.stats());
  assert.deepEqual(stats.suspected_multi_cut_runs, [{ start: 19.75, end: 25.5, flagged: 24 }]);
  // 23 of the run's samples are inside a shot as far as cuts() knows, and all of them move a lot.
  assert.equal(stats.high_motion_share, +(23 / (state.samples.length - 3)).toFixed(3));
  assert.equal(stats.shots, 4);
});

test("clean cuts, cuts seen twice and short flashes are not reported as runs", () => {
  const probe = load();
  const flags = new Set([5, 9.5, 9.75, 14, 14.25, 20.5]);
  const state = series(0, 30, 0.25, (t) => (flags.has(t) ? [45, 0.3] : [2, 0.01]));
  probe.state.samples = state.samples;
  probe.state.range = state.range;
  assert.deepEqual(plain(probe.cuts()), [5, 9.5, 14, 20.5]);
  assert.deepEqual(plain(probe.runs()), []);
  assert.equal(probe.stats().high_motion_share, 0.017);
  // Asked for, two flagged samples count as a run too.
  assert.deepEqual(plain(probe.runs(undefined, { min: 2 })), [
    { start: 9.5, end: 9.75, flagged: 2 },
    { start: 14, end: 14.25, flagged: 2 },
  ]);
});

test("two runs a sample apart stay two runs, as cuts() keeps a cut at each", () => {
  const probe = load();
  const state = series(0, 20, 0.25, (t) => ((t >= 4 && t <= 5) || (t >= 5.5 && t <= 7) ? [40, 0.25] : [1, 0.01]));
  probe.state.samples = state.samples;
  probe.state.range = state.range;
  assert.deepEqual(plain(probe.cuts()), [4, 5.5]);
  assert.deepEqual(plain(probe.runs()), [
    { start: 4, end: 5, flagged: 5 },
    { start: 5.5, end: 7, flagged: 7 },
  ]);
  // The flagged list is the raw material of both.
  assert.equal(probe.flagged().length, 12);
});

test("the probe stays one pasteable script", () => {
  assert.doesNotMatch(SOURCE, /^\s*(import|export)\s/m);
  assert.match(SOURCE, /^\(\(\) => \{/m);
  assert.match(SOURCE, /window\.__probe = \{[^}]*\bruns\b[^}]*\}/);
});
