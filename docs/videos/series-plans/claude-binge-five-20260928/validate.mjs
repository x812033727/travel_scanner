// Read-only checks over a work's `source.mjs`: first the pipeline's own rules, run by the very
// functions the worker applies before it files a document (tools/video/automation/series.mjs:
// `documentProblem` for the setting book, the outline and each chapter, `retentionProblem`
// across all forty episodes), then the rules this batch adds for a two-hour binge that has to
// hold a viewer: hooks short enough to be spoken in about six seconds, cliffhanger types that
// differ across chapter boundaries too, chapters that close on a reveal or a reversal, one
// world-flip near the middle, every mystery planted, advanced and paid where its schedule says,
// every character and place registered, and packaging inside YouTube's limits.
//   node validate.mjs [slug…] [--source-only] [--write-report]
// `--source-only` skips the comparison of generated files with `compile(source)`.
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { CHAPTERS, COMMON, ROOT, SLUGS, compile, hash, jobSeries, loadSource } from "./build.mjs";
import { documentProblem, retentionProblem } from "../../../../tools/video/automation/series.mjs";
import { GENRE_SPECS, HOOK_TYPES, LEAD_ARCS, SATISFACTION_TYPES } from "../../../../tools/video/automation/prompts.mjs";

const GEMINI_VOICES = new Set([
  "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede", "Callirrhoe", "Autonoe",
  "Enceladus", "Iapetus", "Umbriel", "Algieba", "Despina", "Erinome", "Algenib", "Rasalgethi",
  "Laomedeia", "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird",
  "Zubenelgenubi", "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
]);
const CLIFF_TYPES = new Set(["danger", "reveal", "choice", "reversal", "emotion"]);
const BEAT_ORDER = ["opening", "first_half", "midpoint", "second_half", "ending"];
const TONES = new Set(["dual-male-leads-subtext", "dual-male-leads-explicit", "hetero-leads", "no-romance"]);
const ROLES = new Set(["lead", "support", "antagonist"]);
const REQUIRED_TAGS = ["漫劇", "AI漫劇", "一口氣看完"];
// The retention rules say the hook is spoken inside about five seconds and the tool refuses one
// that ends after eight (250 characters a minute = 33 characters). We stop at 28 so the spoken
// line lands near six seconds with room for the actor's pauses.
export const HOOK_MAX_CHARS = 28;
export const WORLD_FLIP_RANGE = [18, 22];
// The image prompts take a character's appearance word for word into every shot of every episode
// (tools/video/media/look.mjs, keyframes.mjs), so a look that depends on the episode cannot be
// drawn from it; what changes belongs in continuity_notes and the shot prompt.
export const TIMED_APPEARANCE = /\b(?:episodes?|eps?\.?\s*\d+|later|initially|at first|at the start|onwards?|near the end|by the end|as the story|from then on|no longer)\b/i;

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const spoken = (text) => [...String(text).replace(/[\p{P}\p{Z}\s]/gu, "")].length;
const chars = (text) => [...String(text)].length;

/** Everything wrong with a source, as sentences; empty when the work may be built and filed. */
export function validateSource(source, expectedSlug = source?.series?.slug) {
  const errors = [];
  const warnings = [];
  const check = (ok, message) => {
    if (!ok) errors.push(message);
  };
  const warn = (ok, message) => {
    if (!ok) warnings.push(message);
  };
  try {
    const s = source.series;
    const series = jobSeries(source);
    check(s.slug === expectedSlug, `series.slug must be ${expectedSlug}`);
    check(/^[a-z0-9][a-z0-9-]{1,39}$/.test(s.slug), "series.slug: lowercase ascii, 2 to 40 characters");
    for (const key of ["title", "logline", "premise", "note"]) check(isText(s[key]), `series.${key} is missing`);
    check(chars(s.title) <= 200, "series.title over 200 characters");
    check(chars(s.premise) <= 4000, "series.premise over 4000 characters");
    check(chars(s.note) <= 2000, "series.note over 2000 characters");
    const spec = GENRE_SPECS[s.genre];
    check(Boolean(spec), `series.genre "${s.genre}" is not a genre preset`);
    check(spec?.retention === true, "every work of this batch uses a genre with the retention rules (not xianxia-bonds)");
    check(!spec || spec.leads.includes(s.lead), `series.lead "${s.lead}" is not allowed for ${s.genre}`);
    check(TONES.has(s.tone), `series.tone "${s.tone}" is not a tone`);
    check(s.lead !== "dual-male" || s.tone.startsWith("dual-male"), "a dual-male lead needs a dual-male tone");
    check(s.lead === "dual-male" || !s.tone.startsWith("dual-male"), "a dual-male tone needs a dual-male lead");
    const allowedSatisfactions = new Set(spec?.satisfactions ?? Object.keys(SATISFACTION_TYPES));

    // --- the setting book -------------------------------------------------------------
    const st = source.setting;
    check(isText(st.world?.era), "setting.world.era is missing");
    check(Array.isArray(st.world?.places) && st.world.places.length >= 3, "setting.world.places: at least three");
    check(Array.isArray(st.world?.factions) && st.world.factions.length >= 2, "setting.world.factions: at least two");
    for (const f of st.world?.factions ?? []) check(isText(f.name) && isText(f.wants) && isText(f.hides), `faction ${f.name}: needs name, wants, hides`);
    check(Array.isArray(st.rules) && st.rules.length >= 4, "setting.rules: at least four hard rules with prices");
    for (const key of ["tone", "imagery", "ending"]) check(isText(st[key]), `setting.${key} is missing`);
    check(Array.isArray(st.naming) && st.naming.length >= 2, "setting.naming: at least two rules");
    check(Array.isArray(st.never) && st.never.length >= 3, "setting.never: at least three");
    check(Array.isArray(st.cold_open) && st.cold_open.length >= 4, "setting.cold_open: the first thirty seconds in at least four beats");
    for (const beat of st.cold_open ?? []) check(isText(beat.seconds) && isText(beat.picture) && isText(beat.audio), "cold_open beats need seconds, picture, audio");
    const cast = new Map();
    for (const c of st.characters ?? []) {
      const p = `character ${c.id}: `;
      check(/^[a-z][a-z0-9-]{1,23}$/.test(c.id ?? ""), p + "id must be lowercase ascii, 2 to 24 characters");
      check(!cast.has(c.id), p + "duplicate id");
      cast.set(c.id, c);
      for (const key of ["name", "role", "age", "appearance", "personality", "want", "fear", "secret", "speech"]) check(isText(c[key]), p + `missing ${key}`);
      check(ROLES.has(c.role), p + "role must be lead, support or antagonist");
      check(chars(c.appearance ?? "") <= 800, p + "appearance over 800 characters");
      check(/^[\x20-\x7E]+$/.test(c.appearance ?? ""), p + "appearance must be English (ASCII) for the image model");
      check(!TIMED_APPEARANCE.test(c.appearance ?? ""), p + `appearance must not depend on the episode ("${(c.appearance ?? "").match(TIMED_APPEARANCE)?.[0]}"); put changes in the character's looks or continuity_notes`);
      // A look's appearance stands in for the base one in the episodes it covers (AUTHORING.md,
      // 換裝與變化): its shape is documentProblem's to check below, its words the base's rules.
      for (const look of Array.isArray(c.looks) ? c.looks : []) {
        if (!isText(look?.appearance)) continue;
        const q = `${p}look ${look.id}: `;
        check(chars(look.appearance) <= 800, q + "appearance over 800 characters");
        check(/^[\x20-\x7E]+$/.test(look.appearance), q + "appearance must be English (ASCII) for the image model");
        check(!TIMED_APPEARANCE.test(look.appearance), q + `appearance must not depend on the episode ("${look.appearance.match(TIMED_APPEARANCE)?.[0]}"); the look's from and to say when it is worn`);
      }
      check(c.voice?.provider === "gemini" && GEMINI_VOICES.has(c.voice?.name) && isText(c.voice?.style), p + "voice must be a Gemini prebuilt voice with a style");
      check(Array.isArray(c.relationships) && c.relationships.length >= 1, p + "at least one relationship");
      check(Object.hasOwn(st.lexicon ?? {}, c.name), p + `name "${c.name}" must be in the lexicon`);
    }
    const leads = (st.characters ?? []).filter((c) => c.role === "lead");
    check(leads.length === (s.lead === "dual-male" ? 2 : 1), `expected ${s.lead === "dual-male" ? 2 : 1} lead(s), found ${leads.length}`);
    check((st.characters ?? [])[0]?.role === "lead", "the lead comes first in characters");
    check((st.characters ?? []).some((c) => c.role === "antagonist"), "at least one antagonist");
    check((st.characters ?? []).length >= 6 && (st.characters ?? []).length <= 12, "cast of 6 to 12 named characters");
    for (const c of st.characters ?? []) for (const r of c.relationships ?? []) check(cast.has(r.with) && isText(r.kind), `character ${c.id}: relationship with unknown "${r.with}"`);
    const places = new Map();
    for (const p of st.world?.places ?? []) {
      check(/^[a-z][a-z0-9-]{1,23}$/.test(p.id ?? "") && isText(p.name) && isText(p.description), `place ${p.id}: needs id, name, description`);
      check(!places.has(p.id), `place ${p.id}: duplicate id`);
      places.set(p.id, p);
    }
    const mysteries = new Map();
    for (const m of st.mysteries ?? []) {
      const p = `mystery ${m.id}: `;
      check(/^m\d{2}$/.test(m.id ?? ""), p + "id is m01…m12");
      check(!mysteries.has(m.id), p + "duplicate id");
      mysteries.set(m.id, m);
      check(isText(m.question) && isText(m.answer), p + "needs question and answer");
      check(Number.isInteger(m.planted) && m.planted >= 1 && m.planted <= COMMON.planned_episodes, p + "planted must be an episode number");
      check(Array.isArray(m.advanced) && new Set(m.advanced).size === m.advanced.length, p + "advanced: distinct episode numbers");
      for (const n of m.advanced ?? []) check(Number.isInteger(n) && n > m.planted && n <= COMMON.planned_episodes, p + `advanced episode ${n} is outside (planted, 40]`);
      if (COMMON.open_ended) check(m.reserved === true ? m.revealed === null : Number.isInteger(m.revealed), p + "a reserved mystery has no reveal; others do");
      else {
        check(m.reserved !== true, p + "a closed first part reserves nothing");
        check(Number.isInteger(m.revealed) && m.revealed > m.planted && m.revealed <= COMMON.planned_episodes, p + "revealed must be an episode after planted");
        for (const n of m.advanced ?? []) check(n < m.revealed, p + `advanced episode ${n} must come before the reveal`);
      }
    }
    check(mysteries.size >= 8 && mysteries.size <= 12, `8 to 12 mysteries (found ${mysteries.size})`);

    // --- the chapters and episodes ----------------------------------------------------
    check(Array.isArray(source.chapters) && source.chapters.length === CHAPTERS, `exactly ${CHAPTERS} chapters`);
    const episodes = (source.chapters ?? []).flatMap((c) => c.episodes ?? []);
    check(episodes.length === COMMON.planned_episodes, `exactly ${COMMON.planned_episodes} episodes`);
    check(episodes.every((e, i) => e.number === i + 1), "episodes numbered 1 to 40 in order");
    for (const c of source.chapters ?? []) {
      const p = `chapter ${c.number}: `;
      for (const key of ["title", "theme", "stakes", "question", "start_state", "end_state", "turn"]) check(isText(c[key]), p + `missing ${key}`);
      check((c.episodes ?? []).length === COMMON.episodes_per_chapter, p + `${COMMON.episodes_per_chapter} episodes`);
    }
    const titles = new Set();
    const hooks = new Set();
    const appearances = new Map([...cast.keys()].map((id) => [id, 0]));
    const placeUse = new Map([...places.keys()].map((id) => [id, 0]));
    const setupsSeen = new Map();
    const payoffsSeen = new Map();
    let flips = 0;
    for (let i = 0; i < episodes.length; i++) {
      const e = episodes[i];
      const p = `episode ${e.number}: `;
      for (const key of ["title", "logline", "hook", "conflict", "turn", "theme", "carry"]) check(isText(e[key]), p + `missing ${key}`);
      check(e.timeline === "present" || e.timeline === "past", p + "timeline is present or past");
      check(!titles.has(e.title), p + "title repeats another episode's");
      titles.add(e.title);
      check(!hooks.has(e.hook), p + "hook repeats another episode's");
      hooks.add(e.hook);
      check(spoken(e.hook) <= HOOK_MAX_CHARS, p + `hook is ${spoken(e.hook)} spoken characters; at most ${HOOK_MAX_CHARS}`);
      check(spoken(e.hook) >= 6, p + "hook too short to be a line");
      check(HOOK_TYPES.includes(e.hook_type), p + `hook_type must be one of ${HOOK_TYPES.join(", ")}`);
      check(LEAD_ARCS.includes(e.lead_arc), p + `lead_arc must be one of ${LEAD_ARCS.join(", ")}`);
      check(CLIFF_TYPES.has(e.cliffhanger?.type) && isText(e.cliffhanger?.text), p + "cliffhanger needs a type and text");
      if (i > 0) check(e.cliffhanger?.type !== episodes[i - 1].cliffhanger?.type, p + `same cliffhanger type as episode ${episodes[i - 1].number} (chapter boundaries count)`);
      if (e.number % COMMON.episodes_per_chapter === 0) check(["reveal", "reversal"].includes(e.cliffhanger?.type), p + "a chapter's last episode ends on a reveal or a reversal");
      check(Array.isArray(e.tension) && e.tension.length === 5 && e.tension.every((t) => Number.isInteger(t) && t >= 1 && t <= 5), p + "tension: five integers 1 to 5");
      check(new Set(e.tension ?? []).size > 1, p + "tension is flat");
      check((e.tension ?? [])[4] >= 4, p + "tension ends below 4");
      check(Array.isArray(e.characters) && e.characters.length >= 2 && e.characters.length <= 4, p + "2 to 4 named characters");
      check(new Set(e.characters ?? []).size === (e.characters ?? []).length, p + "a character listed twice");
      for (const id of e.characters ?? []) {
        check(cast.has(id), p + `unknown character "${id}"`);
        if (appearances.has(id)) appearances.set(id, appearances.get(id) + 1);
      }
      check(Array.isArray(e.locations) && e.locations.length >= 1 && e.locations.length <= 2, p + "1 or 2 places");
      for (const id of e.locations ?? []) {
        check(places.has(id), p + `unknown place "${id}"`);
        if (placeUse.has(id)) placeUse.set(id, placeUse.get(id) + 1);
      }
      check(Array.isArray(e.satisfaction) && e.satisfaction.length >= 2, p + "at least two satisfaction beats");
      let lastBeat = -1;
      const types = new Set();
      for (const b of e.satisfaction ?? []) {
        check(BEAT_ORDER.includes(b.beat) && allowedSatisfactions.has(b.type), p + `satisfaction beat must be {beat, type} of the genre's types (got ${b.beat}/${b.type})`);
        check(isText(b.text) && chars(b.text) >= 8, p + "each satisfaction beat says what the viewer sees (≥ 8 characters)");
        check(BEAT_ORDER.indexOf(b.beat) >= lastBeat, p + "satisfaction beats out of order");
        lastBeat = BEAT_ORDER.indexOf(b.beat);
        warn(!types.has(b.type), p + `satisfaction type ${b.type} twice in one episode`);
        types.add(b.type);
      }
      check(["opening", "first_half"].includes((e.satisfaction ?? [])[0]?.beat), p + "the first satisfaction beat lands in the first half");
      for (const id of e.setups ?? []) {
        check(mysteries.has(id), p + `unknown setup ${id}`);
        const m = mysteries.get(id);
        if (m) check(m.planted === e.number || m.advanced.includes(e.number), p + `setup ${id} is not on its schedule (planted ${m.planted}, advanced ${m.advanced.join("/")})`);
        setupsSeen.set(id, (setupsSeen.get(id) ?? 0) + 1);
      }
      for (const id of e.payoffs ?? []) {
        check(mysteries.has(id), p + `unknown payoff ${id}`);
        const m = mysteries.get(id);
        if (m) {
          check(e.number > m.planted, p + `payoff ${id} before it was planted`);
          check(m.revealed === e.number || m.advanced.includes(e.number), p + `payoff ${id} is not on its schedule (advanced ${m.advanced.join("/")}, revealed ${m.revealed})`);
        }
        payoffsSeen.set(id, (payoffsSeen.get(id) ?? 0) + 1);
      }
      if (e.world_flip) {
        flips++;
        check(e.number >= WORLD_FLIP_RANGE[0] && e.number <= WORLD_FLIP_RANGE[1], p + `the world flip belongs in episodes ${WORLD_FLIP_RANGE.join("–")}`);
        check(["reveal", "reversal"].includes(e.cliffhanger?.type), p + "the world-flip episode ends on a reveal or a reversal");
      }
    }
    check(flips === 1, `exactly one episode carries world_flip (found ${flips})`);
    for (const m of mysteries.values()) {
      const planted = episodes.find((e) => e.number === m.planted);
      check(Boolean(planted?.setups?.includes(m.id)), `mystery ${m.id}: episode ${m.planted} must list it in setups`);
      if (m.revealed) {
        const revealed = episodes.find((e) => e.number === m.revealed);
        check(Boolean(revealed?.payoffs?.includes(m.id)), `mystery ${m.id}: episode ${m.revealed} must list it in payoffs`);
      }
      for (const n of m.advanced) {
        const ep = episodes.find((e) => e.number === n);
        check(Boolean(ep?.setups?.includes(m.id) || ep?.payoffs?.includes(m.id)), `mystery ${m.id}: episode ${n} advances it, so it lists it in setups or payoffs`);
      }
    }
    for (const [id, n] of appearances) {
      check(n > 0, `character ${id} never appears`);
      const role = cast.get(id)?.role;
      warn(role !== "lead" || n >= Math.ceil(episodes.length * 0.6), `lead ${id} appears in only ${n} of ${episodes.length} episodes`);
    }
    for (const [id, n] of placeUse) check(n > 0, `place ${id} is never used`);
    for (let i = 2; i < episodes.length; i++) {
      const arcs = [episodes[i - 2], episodes[i - 1], episodes[i]].map((e) => e.lead_arc);
      warn(!arcs.every((a) => a === "wins"), `episodes ${episodes[i - 2].number}–${episodes[i].number} are three wins in a row; trouble should follow a win`);
      const hookTypes = [episodes[i - 2], episodes[i - 1], episodes[i]].map((e) => e.hook_type);
      warn(new Set(hookTypes).size > 1, `episodes ${episodes[i - 2].number}–${episodes[i].number} open on the same hook type three times`);
    }

    // --- the pipeline's own rules, on the built documents ----------------------------
    const files = compile(source);
    for (const kind of ["setting", "outline"]) {
      const problem = documentProblem(kind, JSON.parse(files[`${kind}.json`]), { series });
      if (problem) errors.push(`pipeline ${kind}: ${problem}`);
    }
    for (let n = 1; n <= CHAPTERS; n++) {
      const problem = documentProblem("chapter", JSON.parse(files[`chapter-${String(n).padStart(2, "0")}.json`]), { series, chapter_number: n });
      if (problem) errors.push(`pipeline chapter ${n}: ${problem}`);
    }
    const retention = retentionProblem(series, episodes);
    if (retention) errors.push(`pipeline retention across chapters: ${retention}`);
    for (const [name, body] of Object.entries(files)) {
      if (name.endsWith(".json") && name !== "manifest.json" && name !== "documents.json") {
        const doc = JSON.parse(body);
        if (doc.body_md) check(chars(doc.body_md) <= 200_000, `${name}: body_md over 200,000 characters`);
      }
    }

    // --- packaging --------------------------------------------------------------------
    const pk = source.packaging ?? {};
    check(Array.isArray(pk.titles) && pk.titles.length === 3 && new Set(pk.titles).size === 3, "packaging.titles: three distinct titles");
    for (const t of pk.titles ?? []) check(isText(t) && chars(t) <= 100 && !/[<>]/.test(t), `title "${t}" must be ≤ 100 characters with no angle brackets`);
    check(isText(pk.description) && Buffer.byteLength(pk.description, "utf8") <= 1200, "packaging.description: present and at most 1,200 bytes (the tool appends chapters)");
    check(Array.isArray(pk.tags) && pk.tags.join(",").length <= 500, "packaging.tags: at most 500 characters in all");
    for (const tag of REQUIRED_TAGS) check((pk.tags ?? []).includes(tag), `packaging.tags must include ${tag}`);
    check(Array.isArray(pk.thumbnails) && pk.thumbnails.length === 3, "packaging.thumbnails: three compositions");
    for (const t of pk.thumbnails ?? []) {
      check(isText(t.id) && isText(t.headline) && chars(t.headline) <= 12, `thumbnail ${t.id}: headline ≤ 12 characters`);
      check(t.tag == null || chars(t.tag) <= 6, `thumbnail ${t.id}: tag ≤ 6 characters`);
      check(Number.isInteger(t.episode) && t.episode >= 1 && t.episode <= 3, `thumbnail ${t.id}: from episodes 1–3 (the tool picks keyframes there)`);
      check(isText(t.composition) && isText(t.scene) && isText(t.promise), `thumbnail ${t.id}: needs composition, scene, promise`);
    }
    for (const key of ["audience", "visual_identity", "music", "pinned_comment"]) check(isText(pk[key]), `packaging.${key} is missing`);
    check(Array.isArray(pk.why_million) && pk.why_million.length >= 3, "packaging.why_million: at least three reasons");
    check(Array.isArray(source.continuity_notes) && source.continuity_notes.length >= 3 && source.continuity_notes.every(isText), "continuity_notes: at least three nonempty rules");
  } catch (error) {
    errors.push(`invalid source shape: ${error.message}`);
  }
  return { errors, warnings };
}

/** The generated files that differ from what `compile(source)` gives now. */
export async function validateFiles(slug, source, root = ROOT) {
  const stale = [];
  for (const [name, expected] of Object.entries(compile(source))) {
    try {
      const actual = await fs.readFile(path.join(root, slug, name), "utf8");
      if (actual !== expected) stale.push(`${name}: stale, rebuild with node build.mjs ${slug}`);
    } catch {
      stale.push(`${name}: missing, build with node build.mjs ${slug}`);
    }
  }
  return stale;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const sourceOnly = args.includes("--source-only");
  const writeReport = args.includes("--write-report");
  const selected = args.filter((a) => !a.startsWith("--"));
  const results = [];
  for (const slug of selected.length ? selected : SLUGS) {
    try {
      const source = await loadSource(slug);
      const { errors, warnings } = validateSource(source, slug);
      const stale = sourceOnly ? [] : await validateFiles(slug, source);
      results.push({ slug, title: source.series.title, genre: source.series.genre, source_sha256: hash(source), episodes: source.chapters.flatMap((c) => c.episodes).length, errors: [...errors, ...stale], warnings });
    } catch (error) {
      results.push({ slug, errors: [error.message], warnings: [] });
    }
  }
  const report = { scope: "offline production plans; nothing measured on media", execution_scope: "local-validation-only", status_note: "This validation does not change or attest to production state or approve revised documents.", checked_at: new Date().toISOString().slice(0, 10), source_only: sourceOnly, ok: results.every((r) => r.errors.length === 0), works: results };
  if (writeReport) await fs.writeFile(path.join(ROOT, "validation-report.json"), `${JSON.stringify({ ...report, checked_at: undefined }, null, 2)}\n`, "utf8");
  for (const r of results) {
    process.stdout.write(`${r.slug}: ${r.errors.length} error(s), ${r.warnings.length} warning(s)\n`);
    for (const e of r.errors) process.stdout.write(`  ✗ ${e}\n`);
    for (const w of r.warnings) process.stdout.write(`  ⚠ ${w}\n`);
  }
  if (!report.ok) process.exitCode = 1;
}
