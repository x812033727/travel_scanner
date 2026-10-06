import assert from "node:assert/strict";
import test from "node:test";

import { resolveMusic } from "../core/drama.mjs";
import { illustratedFixture } from "../core/fixtures/load.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { bedFilter, illustratedTransition, layoutDrama, mixFilter, soundGraph } from "./drama.mjs";
import { PlanError } from "./plan.mjs";
import {
  duckedBedArgs,
  MIN_GAP_FRAMES,
  mixWindowsArgs,
  parseEbur128Windows,
  POP_WINDOW_FRAMES,
  SFX_NAMES,
  SFX_TARGET_LUFS,
  sfxAudibility,
  sfxCues,
  sfxGains,
  sfxMeasureArgs,
  sfxPlan,
  sfxSetHash,
  sfxSetProblems,
  sfxSounds,
  sfxTrackArgs,
  sfxTrackGainDb,
  soundMeasurement,
  underMixArgs,
  WHOOSH_LEAD_FRAMES,
} from "./sfx.mjs";

function framesManifestFor(doc, timeline) {
  return { scenes: timeline.scenes.map((scene) => ({ id: scene.id, states: doc.scenes.find((each) => each.id === scene.id).template === "shot" ? [] : scene.states.map((_, index) => ({ still: `frames/${scene.id}-${index}.png`, transition: [] })) })) };
}

function illustratedLayout(doc, timeline) {
  const keyframes = { shots: Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: `keyframes/${scene.id}.png`, sha256: "e".repeat(64) }])) };
  return layoutDrama(doc, timeline, framesManifestFor(doc, timeline), null, keyframes, { transitionRule: illustratedTransition, cardMotion: true });
}

const MANIFEST = { sounds: { stamp: { file: "stamp.wav", sha256: "a".repeat(64) }, whoosh: { file: "whoosh.wav" }, pop: { file: "pop.wav" } } };
// A measured set: the three rule sounds and one more, with what `assemble sfx-measure` writes.
const MEASURED = {
  manifest_version: 2,
  sounds: {
    stamp: { file: "stamp.wav", sha256: "a".repeat(64), lufs_i: -20.4, lufs_m: -18.1, peak_dbtp: -8, seconds: 0.4 },
    whoosh: { file: "whoosh.wav", lufs_i: -24, peak_dbtp: -9, seconds: 1.2, target_lufs: -20 },
    pop: { file: "pop.wav", lufs_i: -22, lufs_m: -20, peak_dbtp: -8 },
    bell: { file: "bell.ogg", lufs_i: -19, lufs_m: -17, peak_dbtp: -4 },
  },
};
// What ffmpeg 6.1 printed for a 250 ms synthetic tone padded with a second of silence.
const EBUR128 = [
  "[Parsed_ebur128_2 @ 0x55c3fa531740] t: 0.0999792  TARGET:-23 LUFS    M:-120.7 S:-120.7     I: -70.0 LUFS       LRA:   0.0 LU  FTPK: -21.1 -21.1 dBFS  TPK: -21.1 -21.1 dBFS",
  "[Parsed_ebur128_2 @ 0x55c3fa531740] t: 0.199979   TARGET:-23 LUFS    M:-120.7 S:-120.7     I: -70.0 LUFS       LRA:   0.0 LU  FTPK: -21.1 -21.1 dBFS  TPK: -21.1 -21.1 dBFS",
  "[Parsed_ebur128_2 @ 0x55c3fa531740] t: 0.299979   TARGET:-23 LUFS    M:-120.7 S:-120.7     I: -70.0 LUFS       LRA:   0.0 LU  FTPK: -30.7 -30.7 dBFS  TPK: -21.1 -21.1 dBFS",
  "[Parsed_ebur128_2 @ 0x55c3fa531740] t: 0.399979   TARGET:-23 LUFS    M: -26.0 S:-120.7     I: -26.0 LUFS       LRA:   0.0 LU  FTPK:  -inf  -inf dBFS  TPK: -21.1 -21.1 dBFS",
  "[Parsed_ebur128_2 @ 0x55c3fa531740] t: 0.499979   TARGET:-23 LUFS    M: -30.8 S:-120.7     I: -27.8 LUFS       LRA:   0.0 LU  FTPK:  -inf  -inf dBFS  TPK: -21.1 -21.1 dBFS",
  "[Parsed_ebur128_2 @ 0x55c3fa531740] Summary:",
  "",
  "  Integrated loudness:",
  "    I:         -27.8 LUFS",
  "    Threshold: -39.5 LUFS",
  "",
  "  Loudness range:",
  "    LRA:         0.0 LU",
  "",
  "  True peak:",
  "    Peak:      -21.1 dBFS",
  "",
].join("\n");

test("a set names the three sounds, each a file in its directory", () => {
  assert.deepEqual(SFX_NAMES, ["stamp", "whoosh", "pop"]);
  assert.deepEqual(sfxSetProblems(MANIFEST), []);
  assert.match(sfxSetProblems(null)[0], /manifest\.json must hold an object/);
  assert.match(sfxSetProblems({ sounds: { stamp: { file: "stamp.wav" } } }).join(";"), /sounds\.whoosh is missing.*sounds\.pop is missing/);
  assert.match(sfxSetProblems({ sounds: { ...MANIFEST.sounds, pop: { file: "../pop.wav" } } })[0], /sounds\.pop\.file/);
  assert.match(sfxSetProblems({ sounds: { ...MANIFEST.sounds, pop: { file: "pop.wav", sha256: "zz" } } })[0], /sha256/);
  assert.notEqual(sfxSetHash(illustratedFixture(), MANIFEST), sfxSetHash(illustratedFixture(), { sounds: { ...MANIFEST.sounds, stamp: { file: "other.wav" } } }));
  // A version 1 set hashes as it did before version 2 existed (the Shorts build id carries it).
  assert.equal(sfxSetHash(illustratedFixture(), MANIFEST), "861f78911382114e");
});

test("a version 2 manifest names any sounds with their measured loudness; the rule sounds stay required and a version 1 set reads as before", () => {
  assert.deepEqual(sfxSetProblems(MEASURED), []);
  assert.deepEqual(sfxSetProblems({ ...MEASURED, manifest_version: 1, sounds: MANIFEST.sounds }), [], "version 1 spelled out");
  assert.match(sfxSetProblems({ ...MEASURED, manifest_version: 3 })[0], /manifest_version must be 1 or 2/);
  const unmeasured = structuredClone(MEASURED);
  delete unmeasured.sounds.bell.lufs_i;
  delete unmeasured.sounds.bell.peak_dbtp;
  assert.match(sfxSetProblems(unmeasured).join(";"), /sounds\.bell\.lufs_i is not measured; run node tools\/video\/cli\.mjs assemble sfx-measure.*sounds\.bell\.peak_dbtp is not measured/);
  assert.deepEqual(sfxSetProblems(unmeasured, { measured: false }), [], "the measuring step reads a manifest before it has them");
  const { stamp, ...rest } = MEASURED.sounds;
  assert.match(sfxSetProblems({ ...MEASURED, sounds: rest })[0], /sounds\.stamp is missing/);
  assert.match(sfxSetProblems({ ...MEASURED, sounds: { ...MEASURED.sounds, "Bell Tower": { file: "x.wav" } } })[0], /sounds\.Bell Tower: a sound's name/);
  assert.match(sfxSetProblems({ ...MEASURED, sounds: { ...MEASURED.sounds, stamp: { ...stamp, lufs_i: 3 } } })[0], /sounds\.stamp\.lufs_i must be a number, -70 to 0/);
  assert.match(sfxSetProblems({ ...MEASURED, sounds: { ...MEASURED.sounds, stamp: { ...stamp, target_lufs: -2 } } })[0], /sounds\.stamp\.target_lufs must be -40 to -6/);
  assert.match(sfxSetProblems({ ...MEASURED, sounds: { ...MEASURED.sounds, stamp: { ...stamp, seconds: 0 } } })[0], /sounds\.stamp\.seconds/);
  const sounds = sfxSounds(MEASURED);
  assert.deepEqual(sounds.whoosh, { file: "whoosh.wav", sha256: null, lufs_i: -24, lufs_m: -24, peak_dbtp: -9, seconds: 1.2, target_lufs: -20 }, "the manifest's own target; lufs_i stands in for a lufs_m not measured");
  assert.equal(sounds.stamp.target_lufs, SFX_TARGET_LUFS.stamp);
  assert.equal(sounds.bell.target_lufs, -16, "a sound outside the three gets the default target");
  assert.deepEqual(sfxSounds(MANIFEST).stamp, { file: "stamp.wav", sha256: "a".repeat(64), lufs_i: null, lufs_m: null, peak_dbtp: null, seconds: null, target_lufs: -14 });
  // The set hash covers every sound's file, the cue sheet and a measured set's targets.
  const doc = illustratedFixture();
  const measured = sfxSetHash(doc, MEASURED);
  assert.notEqual(measured, sfxSetHash(doc, { ...MEASURED, sounds: { ...MEASURED.sounds, bell: { ...MEASURED.sounds.bell, file: "other.ogg" } } }), "another file");
  assert.notEqual(measured, sfxSetHash({ ...doc, sfx: { ...doc.sfx, cues: [{ scene: "door", sound: "bell" }] } }, MEASURED), "a cue sheet");
  assert.notEqual(measured, sfxSetHash(doc, { ...MEASURED, sounds: { ...MEASURED.sounds, whoosh: { ...MEASURED.sounds.whoosh, target_lufs: -18 } } }), "another target");
  assert.equal(measured, sfxSetHash(doc, { ...MEASURED, sounds: { ...MEASURED.sounds, stamp: { ...MEASURED.sounds.stamp, lufs_m: -17 } } }), "a measurement alone is not another set");
});

test("the script's cues sound where the writer put them, and a rule's beat within the gap gives way", () => {
  const doc = illustratedFixture();
  const timeline = estimateTimeline(doc);
  const layout = illustratedLayout(doc, timeline);
  const rules = sfxPlan(layout, timeline, doc);
  const at = (id) => timeline.scenes.find((scene) => scene.id === id).start_frame;
  assert.deepEqual(sfxCues(doc, timeline), [], "no sheet, no cues");
  doc.sfx.cues = [{ scene: "door", sound: "bell", gain_db: -3 }, { frame: at("desk") + 10, sound: "chime" }, { frame: 1, sound: "pop" }];
  assert.deepEqual(sfxCues(doc, timeline), [
    { frame: at("door"), sound: "bell", scene: "door", cue: 0, gain_db: -3 },
    { frame: at("desk") + 10, sound: "chime", scene: "desk", cue: 1 },
    { frame: 1, sound: "pop", scene: "hook", cue: 2 },
  ]);
  const events = sfxPlan(layout, timeline, doc);
  // The stamps on the desk and door cards are within the gap of a cue, so the cues sound instead.
  assert.ok(rules.some((event) => event.sound === "stamp" && event.scene === "desk") && rules.some((event) => event.sound === "stamp" && event.scene === "door"));
  assert.deepEqual(events.filter((event) => event.cue === undefined).map((event) => [event.sound, event.scene]), rules.filter((event) => !(event.sound === "stamp" && ["desk", "door"].includes(event.scene))).map((event) => [event.sound, event.scene]));
  assert.deepEqual(events.filter((event) => event.cue !== undefined).map((event) => event.cue), [2, 1, 0], "every cue is kept, in frame order");
  events.forEach((event, index) => { if (index) assert.ok(event.frame >= events[index - 1].frame, "frame order"); });
  assert.throws(() => sfxCues({ ...doc, sfx: { ...doc.sfx, cues: [{ frame: timeline.total_frames, sound: "pop" }] } }, timeline), /sfx\.cues\[0\] is at frame \d+, past the video's \d+ frames/);
  assert.throws(() => sfxCues({ ...doc, sfx: { ...doc.sfx, cues: [{ scene: "nowhere", sound: "pop" }] } }, timeline), PlanError);
});

test("a measured set gains each cue toward its target in the finished mix, capped at the peak ceiling; a version 1 set keeps its one gain", () => {
  const sfx = { version: 2, gain_db: -12, trim_db: 0, sounds: sfxSounds(MEASURED) };
  const events = [{ frame: 30, sound: "stamp", scene: "a" }, { frame: 90, sound: "whoosh", scene: "b", cue: 0, gain_db: -2 }, { frame: 150, sound: "bell", scene: "c", cue: 1 }];
  // The normalization will add 2 dB to the whole mix, so a target in the mix is 2 dB lower on the track.
  const gained = sfxGains(events, sfx, 2);
  assert.deepEqual(gained[0], { ...events[0], gain_db: 2.1, target_lufs: -14 }, "-14 - 2 - (-18.1)");
  assert.deepEqual(gained[1], { ...events[1], gain_db: 0, target_lufs: -20 }, "the manifest's target, the cue's own gain on top");
  assert.deepEqual(gained[2], { ...events[2], gain_db: -1, target_lufs: -16 }, "a peak landing exactly on the ceiling is not capped");
  const loud = sfxGains([events[2]], { ...sfx, sounds: { ...sfx.sounds, bell: { ...sfx.sounds.bell, target_lufs: -10 } } }, 2);
  assert.deepEqual(loud[0], { ...events[2], gain_db: -1, target_lufs: -10, capped: true }, "the bell wanted +5 dB; its -4 dBTP peak allows -1");
  assert.equal(sfxGains(events, { ...sfx, trim_db: -3 }, 2)[0].gain_db, -0.9, "the script's gain_db trims every cue of a measured set");
  const v1 = { version: 1, gain_db: -12, trim_db: -12, sounds: sfxSounds(MANIFEST) };
  assert.deepEqual(sfxGains(events, v1, 2), [events[0], { ...events[1], gain_db: -2 }, events[2]], "no measurement: only a cue's own gain, over the track's");
  assert.equal(sfxTrackGainDb(v1), -12);
  assert.equal(sfxTrackGainDb(sfx), 0);
});

test("a sound is measured padded, as the track carries it, and ebur128's windows and summary are read back", () => {
  assert.deepEqual(sfxMeasureArgs("/sfx/stamp.wav"), ["-hide_banner", "-nostats", "-i", "/sfx/stamp.wav", "-af", "aformat=sample_rates=48000:channel_layouts=stereo,apad=pad_dur=1,ebur128=peak=true", "-f", "null", "-"]);
  const parsed = parseEbur128Windows(EBUR128);
  assert.equal(parsed.integrated, -27.8);
  assert.equal(parsed.truePeak, -21.1);
  assert.deepEqual(parsed.windows.slice(0, 4), [{ t: 0.0999792, m: -120.7, tp: -21.1 }, { t: 0.199979, m: -120.7, tp: -21.1 }, { t: 0.299979, m: -120.7, tp: -30.7 }, { t: 0.399979, m: -26, tp: -Infinity }]);
  assert.equal(parsed.windows.length, 5);
  assert.deepEqual(soundMeasurement(EBUR128), { lufs_i: -27.8, lufs_m: -26, peak_dbtp: -21.1 });
  assert.throws(() => soundMeasurement(EBUR128.replace(/I:\s+-27\.8/, "I:         -70.0").replace(/M: -26\.0/, "M:-120.7").replace(/M: -30\.8/, "M:-120.7")), /silent or empty/);
  assert.throws(() => parseEbur128Windows("nothing"), PlanError);
});

test("the audibility measurements run on the cut's own sound graph, the bed ducked by the mix's own compressor", () => {
  const music = resolveMusic({ music: { track: "m.mp3" } });
  const under = underMixArgs("n.wav", "m.mp3", music, 120);
  assert.deepEqual(under.slice(0, 2), ["-hide_banner", "-nostats"]);
  assert.deepEqual(under.slice(2, 10), soundGraph("n.wav", { musicFile: "m.mp3", music }, 120).inputs);
  assert.equal(under[under.indexOf("-filter_complex") + 1], `${soundGraph("n.wav", { musicFile: "m.mp3", music }, 120).filter};[mix]ebur128=peak=true[out]`);
  assert.deepEqual(under.slice(-5), ["-map", "[out]", "-f", "null", "-"]);
  const voice = underMixArgs("n.wav", null, null, 120);
  assert.deepEqual(voice.slice(2, 4), ["-i", "n.wav"]);
  assert.equal(voice[voice.indexOf("-filter_complex") + 1], "[0:a]aformat=sample_rates=48000:channel_layouts=mono,pan=stereo|c0=c0|c1=c0,ebur128=peak=true[out]");
  const ducked = duckedBedArgs("n.wav", "m.mp3", music, 120);
  const graph = ducked[ducked.indexOf("-filter_complex") + 1];
  assert.ok(graph.startsWith(`${bedFilter(music, 120)};`));
  assert.ok(graph.endsWith(";[ducked]ebur128=peak=true[out]"));
  const compressor = /\[bed\]\[side\]sidechaincompress=[^;]*\[ducked\]/;
  assert.equal(graph.match(compressor)[0], mixFilter(music, 120).match(compressor)[0], "the same compressor line as the mix");
  const mix = mixWindowsArgs("n.wav", "m.mp3", music, 120, "fx.wav");
  assert.ok(mix.includes("fx.wav"));
  assert.equal(mix[mix.indexOf("-filter_complex") + 1], `${soundGraph("n.wav", { musicFile: "m.mp3", music, sfxFile: "fx.wav" }, 120).filter};[mix]ebur128=peak=true[out]`);
});

test("a cue is heard when its loudest window clears the bed by 6 dB and the mix stays under the ceiling; a masked or clipping cue fails", () => {
  // Three seconds of 100 ms lines; a 0.3 s pop at frame 30 (1.0 s) is measured over (1.0, 1.7) s.
  const windows = (levels, key = "m") => levels.map((value, index) => ({ t: (index + 1) / 10 - 0.00002, m: key === "m" ? value : -30, tp: key === "tp" ? value : -20 }));
  const effect = windows(Array.from({ length: 30 }, (_, index) => (index >= 10 && index < 17 ? -20 : -120.7)));
  const under = windows(Array(30).fill(-18));
  const bed = windows(Array(30).fill(-30));
  const mix = windows(Array(30).fill(-6), "tp");
  const events = [{ frame: 30, sound: "pop", scene: "a", gain_db: 3, target_lufs: -16 }];
  const options = { seconds: { pop: 0.3 }, finalGain: 2 };
  const heard = sfxAudibility(events, { effect, under, bed, mix }, options);
  assert.deepEqual(heard.cues, [{ frame: 30, t: 1, sound: "pop", scene: "a", gain_db: 3, target_lufs: -16, effect_lufs_m: -18, under_lufs_m: -16, bed_lufs_m: -28, bed_margin_db: 10, voice_margin_db: -2, peak_dbtp: -4, ok: true }]);
  assert.deepEqual(heard.problems, []);
  assert.equal(heard.min_bed_margin_db, 10);
  const masked = sfxAudibility(events, { effect, under, bed: windows(Array(30).fill(-25)), mix }, options);
  assert.deepEqual(masked.problems, ["sound effect pop at 1.00 s (scene a) is masked by the music bed: 5.0 dB above it, below 6; raise the sound's target_lufs or the cue's gain_db, or move the cue"]);
  assert.equal(masked.cues[0].ok, false);
  const clipping = sfxAudibility([{ ...events[0], cue: 3 }], { effect, under, bed, mix: windows(Array(30).fill(-2), "tp") }, options);
  assert.deepEqual(clipping.problems, ["sound effect pop at 1.00 s (sfx.cues[3]) clips the voice: the mix would peak at 0.0 dBTP after normalization, above -1; lower the cue's gain_db or the sound's target_lufs"]);
  assert.equal(clipping.cues[0].peak_dbtp, 0);
  const dry = sfxAudibility(events, { effect, under, mix }, options);
  assert.equal(dry.cues[0].bed_lufs_m, null);
  assert.equal(dry.cues[0].bed_margin_db, null);
  assert.equal(dry.min_bed_margin_db, null);
  assert.deepEqual(dry.problems, [], "no bed masks nothing");
  const late = sfxAudibility([{ frame: 300, sound: "pop", scene: "z" }], { effect, under, bed, mix }, options);
  assert.match(late.problems[0], /sound effect pop at 10\.00 s \(scene z\) was not measured/);
  assert.equal(late.cues[0].effect_lufs_m, null);
});

test("effects fall on chapter cards, dissolves and reveals, thinned so they never crowd", () => {
  const doc = illustratedFixture();
  const timeline = estimateTimeline(doc);
  const layout = illustratedLayout(doc, timeline);
  const events = sfxPlan(layout, timeline, doc);
  const at = (id) => timeline.scenes.find((scene) => scene.id === id).start_frame;
  // The first scene opens a chapter but nothing sounds on frame 0; the later chapter openers stamp.
  assert.deepEqual(events.filter((event) => event.sound === "stamp").map((event) => event.scene), ["desk", "numbers", "door"]);
  assert.equal(events.find((event) => event.scene === "desk").frame, at("desk"));
  // A whoosh leads the dissolve into a picture by a few frames.
  const whoosh = events.find((event) => event.sound === "whoosh" && event.scene === "podium");
  assert.equal(whoosh.frame, at("podium") - WHOOSH_LEAD_FRAMES);
  // The stats card reveals twice: pops, no closer than the window allows.
  const pops = events.filter((event) => event.sound === "pop");
  assert.ok(pops.length >= 1 && pops.length <= 2, `${pops.length} pops`);
  assert.ok(pops.every((event) => event.scene === "numbers"));
  // Nothing within the minimum gap of the beat before it, and everything in frame order.
  events.forEach((event, index) => {
    if (index) assert.ok(event.frame - events[index - 1].frame >= MIN_GAP_FRAMES, `${event.sound} at ${event.frame} crowds ${events[index - 1].sound} at ${events[index - 1].frame}`);
  });
  for (const [index, event] of pops.entries()) if (index) assert.ok(event.frame - pops[index - 1].frame >= POP_WINDOW_FRAMES);
  assert.ok(events.every((event) => event.frame > 0));
});

test("the effects track opens each sound once, delays every beat to its frame and is cut to the video", () => {
  const files = { stamp: "/sfx/stamp.wav", whoosh: "/sfx/whoosh.wav", pop: "/sfx/pop.wav" };
  assert.equal(sfxTrackArgs([], files, 300, -12, "fx.wav"), null);
  const events = [{ frame: 30, sound: "whoosh" }, { frame: 90, sound: "stamp" }, { frame: 150, sound: "whoosh" }];
  const args = sfxTrackArgs(events, files, 300, -12, "fx.wav");
  assert.deepEqual(args.slice(4, 8), ["-i", "/sfx/whoosh.wav", "-i", "/sfx/stamp.wav"], "each sound opened once, in first use order");
  const graph = args[args.indexOf("-filter_complex") + 1];
  assert.match(graph, /^\[0:a\]aformat=sample_rates=48000:channel_layouts=stereo,adelay=1000\|1000\[e0\];\[1:a\]aformat=[^;]*adelay=3000\|3000\[e1\];\[0:a\][^;]*adelay=5000\|5000\[e2\];/);
  assert.match(graph, /\[e0\]\[e1\]\[e2\]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0\[all\];\[all\]volume=-12dB,apad=whole_dur=10\.000000,atrim=0:10\.000000,asetpts=PTS-STARTPTS\[out\]$/);
  assert.deepEqual(args.slice(-7), ["-map", "[out]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "fx.wav"].slice(-7));
  const one = sfxTrackArgs([{ frame: 45, sound: "pop" }], files, 60, -6, "fx.wav");
  assert.match(one[one.indexOf("-filter_complex") + 1], /\[e0\]acopy\[all\]/);
  // A measured set's events carry their own gain, applied before the delay; the track's gain is then 0.
  const gained = sfxTrackArgs([{ frame: 30, sound: "stamp", gain_db: 2.1 }, { frame: 90, sound: "pop", gain_db: -0.5 }, { frame: 150, sound: "pop" }], files, 300, 0, "fx.wav");
  const gainedGraph = gained[gained.indexOf("-filter_complex") + 1];
  assert.match(gainedGraph, /^\[0:a\]aformat=sample_rates=48000:channel_layouts=stereo,volume=2\.1dB,adelay=1000\|1000\[e0\];\[1:a\]aformat=[^;]*stereo,volume=-0\.5dB,adelay=3000\|3000\[e1\];\[1:a\]aformat=[^;]*stereo,adelay=5000\|5000\[e2\];/);
  assert.match(gainedGraph, /\[all\]volume=0dB,apad/);
});
