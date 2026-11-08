#!/usr/bin/env node
// Checks one plan directory of the top-40 adaptations (setting.json, outline.json, season-NN.json)
// against the retention rules the site enforces on a chapter outline (tools/video/automation/series.mjs
// retentionProblem) plus the rules the 種田娶妻 plan introduced: every id defined, three to five
// distinct hooks an episode, mysteries revealed in their season, advertiser-safe public titles.
// Episode length and hook counts come from the directory's plan.json, so the same checker runs on
// docs/videos/series-plans/zhong-tian-qu-qi (50–180 s, 3 hooks) and on every top-40 plan (90–180 s, 3–5 hooks).
//   node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs <plan-dir> [--season N]
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const HOOK_TYPES = ["question", "danger", "image", "line", "reversal"];
export const CLIFF_TYPES = ["danger", "reveal", "choice", "reversal", "emotion"];
export const LEAD_ARCS = ["wins", "suffers", "mixed"];
export const BEATS = ["opening", "first_half", "midpoint", "second_half", "ending"];
export const SATISFACTIONS = ["face_slap", "identity_reveal", "counter_kill", "level_up", "first_clear", "betrayer_punished", "villain_humbled", "hidden_power", "public_vindication", "rescue", "reversal"];
// Words that get a public title or thumbnail limited (setting.json advertiser_safety).
export const BANNED_TITLE_WORDS = ["血", "屍", "裸", "性感", "火辣", "慘死", "自殺", "自盡", "血洗", "屠", "斬首", "凌遲", "酷刑"];
const TEXT_KEYS = ["title", "youtube_title", "logline", "hook", "mid_hook", "conflict", "turn", "spectacle", "glamour_shot"];

const isText = (value) => typeof value === "string" && value.trim().length > 0;
export const pad = (n) => String(n).padStart(2, "0");

/** Episode-length and hook-count limits of a plan, read from its plan.json with the 種田娶妻 defaults. */
export function limitsOf(plan = {}) {
  const seconds = plan.episode_seconds ?? {};
  const hooks = plan.hooks_per_episode ?? {};
  return {
    minSeconds: seconds.min ?? 50,
    maxSeconds: seconds.max ?? 180,
    finaleMinSeconds: seconds.chapter_finale_min ?? 120,
    minHooks: hooks.min ?? 3,
    maxHooks: hooks.max ?? 3,
    episodesPerChapter: plan.episodes_per_chapter ?? 10,
  };
}

export function seasonProblems(season, { setting, outline, plan = {}, guestIds = new Set() }) {
  const problems = [];
  const limits = limitsOf(plan);
  const per = limits.episodesPerChapter;
  const row = outline.seasons.find((item) => item.number === season.number);
  if (!row) return [`season ${season.number} is not in outline.json`];
  const where = (episode) => `S${pad(season.number)} episode ${episode?.number ?? "?"}`;
  for (const key of ["start_state", "end_state", "title"]) {
    if (season[key] !== row[key]) problems.push(`S${pad(season.number)}: ${key} must be copied from outline.json`);
  }
  const tones = new Set(setting.tones.map((tone) => tone.id));
  const characters = new Set([...setting.characters.map((item) => item.id), ...(setting.beasts ?? []).map((item) => item.id), ...guestIds]);
  const mysteries = new Map(setting.mysteries.map((item) => [item.id, item]));
  const threads = new Map((season.threads ?? []).map((item) => [item.id, item]));
  for (const thread of season.threads ?? []) {
    if (!/^s\d{2}-t\d{2}$/.test(thread.id ?? "")) problems.push(`S${pad(season.number)}: thread id ${thread.id} must look like s${pad(season.number)}-t01`);
    if (!isText(thread.question)) problems.push(`thread ${thread.id} needs a question`);
  }
  const episodes = season.episodes ?? [];
  const [first, last] = row.episodes;
  if (episodes.length !== last - first + 1) problems.push(`S${pad(season.number)} has ${episodes.length} episodes, wants ${last - first + 1}`);
  const planted = new Set();
  episodes.forEach((episode, index) => {
    const who = where(episode);
    if (episode.number !== first + index) problems.push(`${who}: numbers must run ${first}–${last} in order`);
    if (episode.season_episode !== index + 1) problems.push(`${who}: season_episode must be ${index + 1}`);
    if (episode.chapter !== Math.floor(index / per) + 1) problems.push(`${who}: chapter must be ${Math.floor(index / per) + 1}`);
    for (const key of TEXT_KEYS) if (!isText(episode[key])) problems.push(`${who} needs ${key}`);
    if (!Number.isInteger(episode.duration_s) || episode.duration_s < limits.minSeconds || episode.duration_s > limits.maxSeconds) problems.push(`${who}: duration_s must be ${limits.minSeconds}–${limits.maxSeconds}`);
    if ((index + 1) % per === 0 && episode.duration_s < limits.finaleMinSeconds) problems.push(`${who}: a chapter finale runs at least ${limits.finaleMinSeconds} seconds`);
    if (!HOOK_TYPES.includes(episode.hook_type)) problems.push(`${who}: hook_type must be one of ${HOOK_TYPES.join(", ")}`);
    if (!LEAD_ARCS.includes(episode.lead_arc)) problems.push(`${who}: lead_arc must be one of ${LEAD_ARCS.join(", ")}`);
    const beats = episode.satisfaction;
    if (!Array.isArray(beats) || beats.length < 2) problems.push(`${who} needs at least two satisfaction beats`);
    else {
      if (beats.some((beat) => !BEATS.includes(beat?.beat) || !SATISFACTIONS.includes(beat?.type))) problems.push(`${who}: satisfaction beats need a beat and a type from the lists`);
      if (!["opening", "first_half"].includes(beats[0]?.beat)) problems.push(`${who}: the first satisfaction beat lands in the opening or first half`);
    }
    if (!episode.cliffhanger || !CLIFF_TYPES.includes(episode.cliffhanger.type) || !isText(episode.cliffhanger.text)) problems.push(`${who} needs a cliffhanger {type, text, question}`);
    else if ((!isText(episode.cliffhanger.question) || episode.cliffhanger.question.length > 30)) problems.push(`${who}: cliffhanger.question is the question the viewer carries into the next episode, 30 characters at most`);
    const tension = episode.tension;
    if (!Array.isArray(tension) || tension.length !== 5 || tension.some((n) => !Number.isInteger(n) || n < 1 || n > 5)) problems.push(`${who} needs five tension scores 1–5`);
    else if (new Set(tension).size === 1) problems.push(`${who}: tension must not be flat`);
    else if (tension.at(-1) < 4) problems.push(`${who}: the ending tension is at least 4`);
    // The owner wants three to five hooks an episode: the opening, the middle, the ending and any
    // extra_hooks must each be a different beat, not one event told several times.
    const extras = episode.extra_hooks ?? [];
    if (!Array.isArray(extras) || extras.some((text) => !isText(text))) problems.push(`${who}: extra_hooks must be a list of sentences`);
    const hooks = [episode.hook, episode.mid_hook, episode.cliffhanger?.text, ...(Array.isArray(extras) ? extras : [])].filter(isText).map((text) => text.trim());
    if (new Set(hooks).size !== hooks.length) problems.push(`${who}: hook, mid_hook, cliffhanger.text and extra_hooks must all be different beats`);
    if (hooks.length < limits.minHooks || hooks.length > limits.maxHooks) problems.push(`${who}: an episode carries ${limits.minHooks}–${limits.maxHooks} hooks, this one has ${hooks.length}`);
    if (!Array.isArray(episode.tones) || !episode.tones.length || episode.tones.some((id) => !tones.has(id))) problems.push(`${who}: tones must be ids from setting.tones`);
    for (const key of ["characters", "locations"]) {
      if (!Array.isArray(episode[key]) || !episode[key].length || !episode[key].every(isText)) problems.push(`${who}: ${key} must be a nonempty text list`);
    }
    for (const id of episode.characters ?? []) if (!characters.has(id)) problems.push(`${who}: unknown character ${id}`);
    for (const key of ["setups", "payoffs", "reveals", "general_payoffs"]) if (!Array.isArray(episode[key])) problems.push(`${who}: ${key} must be a list`);
    for (const id of [...(episode.setups ?? []), ...(episode.payoffs ?? []), ...(episode.reveals ?? [])]) {
      if (!mysteries.has(id) && !threads.has(id)) problems.push(`${who}: unknown mystery or thread ${id}`);
    }
    for (const id of episode.setups ?? []) planted.add(id);
    for (const id of episode.payoffs ?? []) {
      if (threads.has(id) && !planted.has(id)) problems.push(`${who}: thread ${id} is paid before it is set up`);
      if (mysteries.has(id) && mysteries.get(id).setup_season > season.number) problems.push(`${who}: ${id} is paid before its setup season`);
    }
    for (const id of episode.reveals ?? []) {
      if (!mysteries.has(id)) problems.push(`${who}: reveals lists mysteries only (${id})`);
      else if (mysteries.get(id).reveal_season !== season.number) problems.push(`${who}: ${id} is revealed in season ${mysteries.get(id).reveal_season}, not here`);
    }
    if (!episode.state || !["time", "knowledge", "carry_forward"].every((key) => isText(episode.state[key]))) problems.push(`${who} needs state {time, knowledge, carry_forward}`);
    const title = episode.youtube_title ?? "";
    for (const word of BANNED_TITLE_WORDS) if (title.includes(word)) problems.push(`${who}: youtube_title uses 「${word}」, which gets a video limited`);
    if (title.length > 60) problems.push(`${who}: youtube_title runs over 60 characters`);
  });
  for (let index = 1; index < episodes.length; index++) {
    const [before, now] = [episodes[index - 1], episodes[index]];
    if (before.cliffhanger?.type && before.cliffhanger.type === now.cliffhanger?.type) problems.push(`${where(before)} and ${now.number} end on the same cliffhanger type`);
    if (before.lead_arc === "suffers" && now.lead_arc === "suffers") problems.push(`${where(before)} and ${now.number} both leave the lead suffering`);
  }
  // Seasons are written in parallel, so the boundary is fixed by rule: a season ends on a
  // reversal (the series finale too), never leaves the lead suffering, and opens on another type.
  const [opener, finale] = [episodes[0], episodes.at(-1)];
  if (opener?.cliffhanger?.type === "reversal") problems.push(`${where(opener)}: a season's first episode does not end on a reversal`);
  if (finale && finale.cliffhanger?.type !== "reversal") problems.push(`${where(finale)}: a season finale ends on a reversal`);
  if (finale?.lead_arc === "suffers") problems.push(`${where(finale)}: a season finale does not leave the lead suffering`);
  for (let start = 0; start + 4 <= episodes.length; start++) {
    const window = episodes.slice(start, start + 4);
    if (!window.some((episode) => episode.payoffs?.length)) problems.push(`${where(window[0])} to ${window[3].number} pay nothing off`);
  }
  for (const chapter of row.chapters) {
    const rows = episodes.filter((episode) => episode.chapter === chapter.number);
    const used = new Set(rows.flatMap((episode) => episode.tones ?? []));
    for (const tone of chapter.tones) if (!used.has(tone)) problems.push(`S${pad(season.number)} chapter ${chapter.number} never uses its tone ${tone}`);
  }
  for (const thread of season.threads ?? []) {
    if (!episodes.some((episode) => episode.payoffs?.includes(thread.id))) problems.push(`thread ${thread.id} is never paid off`);
  }
  return problems;
}

export function planProblems({ setting, outline, seasons, plan = {} }) {
  const problems = [];
  const guestIds = new Set();
  for (const season of seasons) {
    for (const guest of season.guest_cast ?? []) {
      if (!isText(guest.id) || !isText(guest.name) || !isText(guest.appearance)) problems.push(`S${pad(season.number)}: guest ${guest.id} needs id, name and appearance`);
      if (!guest.id?.startsWith(`s${pad(season.number)}-`)) problems.push(`S${pad(season.number)}: guest id ${guest.id} must start with s${pad(season.number)}-`);
      if (guestIds.has(guest.id) || setting.characters.some((item) => item.id === guest.id)) problems.push(`guest id ${guest.id} is defined twice`);
      guestIds.add(guest.id);
    }
  }
  for (const season of seasons) problems.push(...seasonProblems(season, { setting, outline, plan, guestIds }));
  const all = seasons.flatMap((season) => season.episodes ?? []);
  for (let index = 1; index < all.length; index++) {
    const [before, now] = [all[index - 1], all[index]];
    if (now.season_episode === 1 && before.cliffhanger?.type === now.cliffhanger?.type) problems.push(`episodes ${before.number} and ${now.number} (season boundary) end on the same cliffhanger type`);
    if (now.season_episode === 1 && before.lead_arc === "suffers" && now.lead_arc === "suffers") problems.push(`episodes ${before.number} and ${now.number} (season boundary) both leave the lead suffering`);
  }
  if (seasons.length === outline.seasons.length) {
    for (const mystery of setting.mysteries) {
      const count = all.filter((episode) => episode.reveals?.includes(mystery.id)).length;
      if (count !== 1) problems.push(`${mystery.id} is revealed ${count} times; it needs exactly one reveal`);
    }
  }
  return problems;
}

/** The outline itself: every season has the chapters its episode range needs, in order. */
export function outlineProblems({ setting, outline, plan = {} }) {
  const problems = [];
  const per = limitsOf(plan).episodesPerChapter;
  const tones = new Set(setting.tones.map((tone) => tone.id));
  let expectedFirst = 1;
  for (const season of outline.seasons ?? []) {
    const who = `outline season ${season.number}`;
    const [first, last] = season.episodes ?? [];
    if (first !== expectedFirst) problems.push(`${who}: episodes start at ${first}, expected ${expectedFirst}`);
    for (const key of ["title", "theme", "start_state", "end_state"]) if (!isText(season[key])) problems.push(`${who} needs ${key}`);
    const chapters = season.chapters ?? [];
    if (chapters.length * per !== last - first + 1) problems.push(`${who}: ${chapters.length} chapters of ${per} do not cover episodes ${first}–${last}`);
    chapters.forEach((chapter, index) => {
      const label = `${who} chapter ${chapter.number}`;
      if (chapter.number !== index + 1) problems.push(`${label}: chapters are numbered in order`);
      const [cFirst, cLast] = chapter.episodes ?? [];
      if (cFirst !== first + index * per || cLast !== first + index * per + per - 1) problems.push(`${label}: episodes must be ${first + index * per}–${first + index * per + per - 1}`);
      for (const key of ["title", "beats", "end", "spectacle"]) if (!isText(chapter[key])) problems.push(`${label} needs ${key}`);
      if (!Array.isArray(chapter.threads) || !chapter.threads.length) problems.push(`${label} needs threads`);
      if (!Array.isArray(chapter.tones) || !chapter.tones.length || chapter.tones.some((id) => !tones.has(id))) problems.push(`${label}: tones must be ids from setting.tones`);
    });
    expectedFirst = last + 1;
  }
  for (const mystery of setting.mysteries ?? []) {
    if (!(mystery.setup_season <= mystery.reveal_season)) problems.push(`${mystery.id}: setup_season must not be after reveal_season`);
  }
  return problems;
}

export function loadPlan(dir) {
  const read = (name) => JSON.parse(readFileSync(join(dir, name), "utf8"));
  const plan = existsSync(join(dir, "plan.json")) ? read("plan.json") : {};
  const setting = read("setting.json");
  const outline = read("outline.json");
  const numbers = outline.seasons.map((item) => item.number);
  const seasons = numbers.filter((n) => existsSync(join(dir, `season-${pad(n)}.json`))).map((n) => read(`season-${pad(n)}.json`));
  const missing = numbers.filter((n) => !existsSync(join(dir, `season-${pad(n)}.json`)));
  return { plan, setting, outline, seasons, missing };
}

function main() {
  const args = process.argv.slice(2);
  const dirArg = args.find((arg) => !arg.startsWith("--") && args[args.indexOf(arg) - 1] !== "--season");
  if (!dirArg) {
    console.error("usage: node validate.mjs <plan-dir> [--season N]");
    process.exit(2);
  }
  const dir = resolve(dirArg);
  const { plan, setting, outline, seasons, missing } = loadPlan(dir);
  const only = args.includes("--season") ? Number(args[args.indexOf("--season") + 1]) : null;
  const problems = outlineProblems({ setting, outline, plan });
  if (only) {
    const season = seasons.find((item) => item.number === only) ?? { number: only, episodes: [] };
    problems.push(...seasonProblems(season, { setting, outline, plan, guestIds: new Set((season.guest_cast ?? []).map((g) => g.id)) }));
  } else {
    problems.push(...planProblems({ setting, outline, seasons, plan }));
    if (missing.length) problems.push(`missing season files: ${missing.map(pad).join(", ")}`);
  }
  if (problems.length) {
    console.error(problems.join("\n"));
    console.error(`${problems.length} problem(s)`);
    process.exit(1);
  }
  const count = (only ? seasons.filter((item) => item.number === only) : seasons).reduce((sum, season) => sum + season.episodes.length, 0);
  console.log(`ok: ${setting.title} — ${only ? 1 : seasons.length} season(s), ${count} episodes`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
