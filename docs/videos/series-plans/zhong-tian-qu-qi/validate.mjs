#!/usr/bin/env node
// Checks the 種田娶妻 plan: setting, outline and the five season files against the retention
// rules the site enforces on a chapter outline (tools/video/automation/series.mjs
// retentionProblem) plus this plan's own: 300 episodes, 50–180 seconds, three distinct hooks per episode, mysteries revealed in
// their season, every id defined, advertiser-safe public titles.
//   node docs/videos/series-plans/zhong-tian-qu-qi/validate.mjs [--season N]
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const read = (name) => JSON.parse(readFileSync(join(here, name), "utf8"));

export const HOOK_TYPES = ["question", "danger", "image", "line", "reversal"];
export const CLIFF_TYPES = ["danger", "reveal", "choice", "reversal", "emotion"];
export const LEAD_ARCS = ["wins", "suffers", "mixed"];
export const BEATS = ["opening", "first_half", "midpoint", "second_half", "ending"];
export const SATISFACTIONS = ["face_slap", "identity_reveal", "counter_kill", "level_up", "first_clear", "betrayer_punished", "villain_humbled", "hidden_power", "public_vindication", "rescue", "reversal"];
// Words that get a public title or thumbnail limited (setting.json advertiser_safety).
export const BANNED_TITLE_WORDS = ["血", "屍", "裸", "性感", "火辣", "慘死", "自殺", "自盡", "血洗", "屠", "斬首", "凌遲", "酷刑"];
const TEXT_KEYS = ["title", "youtube_title", "logline", "hook", "mid_hook", "conflict", "turn", "spectacle", "glamour_shot"];

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const pad = (n) => String(n).padStart(2, "0");

export function seasonProblems(season, { setting, outline, guestIds = new Set() }) {
  const problems = [];
  const plan = outline.seasons.find((row) => row.number === season.number);
  if (!plan) return [`season ${season.number} is not in outline.json`];
  const where = (episode) => `S${pad(season.number)} episode ${episode?.number ?? "?"}`;
  for (const key of ["start_state", "end_state", "title"]) {
    if (season[key] !== plan[key]) problems.push(`S${pad(season.number)}: ${key} must be copied from outline.json`);
  }
  const tones = new Set(setting.tones.map((tone) => tone.id));
  const characters = new Set([...setting.characters.map((row) => row.id), ...setting.beasts.map((row) => row.id), ...guestIds]);
  const mysteries = new Map(setting.mysteries.map((row) => [row.id, row]));
  const threads = new Map((season.threads ?? []).map((row) => [row.id, row]));
  for (const thread of season.threads ?? []) {
    if (!/^s\d{2}-t\d{2}$/.test(thread.id ?? "")) problems.push(`S${pad(season.number)}: thread id ${thread.id} must look like s${pad(season.number)}-t01`);
    if (!isText(thread.question)) problems.push(`thread ${thread.id} needs a question`);
  }
  const episodes = season.episodes ?? [];
  const [first, last] = plan.episodes;
  if (episodes.length !== last - first + 1) problems.push(`S${pad(season.number)} has ${episodes.length} episodes, wants ${last - first + 1}`);
  const planted = new Set();
  episodes.forEach((episode, index) => {
    const who = where(episode);
    if (episode.number !== first + index) problems.push(`${who}: numbers must run ${first}–${last} in order`);
    if (episode.season_episode !== index + 1) problems.push(`${who}: season_episode must be ${index + 1}`);
    if (episode.chapter !== Math.floor(index / 10) + 1) problems.push(`${who}: chapter must be ${Math.floor(index / 10) + 1}`);
    for (const key of TEXT_KEYS) if (!isText(episode[key])) problems.push(`${who} needs ${key}`);
    if (!Number.isInteger(episode.duration_s) || episode.duration_s < 50 || episode.duration_s > 180) problems.push(`${who}: duration_s must be 50–180`);
    if ((index + 1) % 10 === 0 && episode.duration_s < 120) problems.push(`${who}: a chapter finale runs at least 120 seconds`);
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
    // The owner wants two or three hooks an episode at least: the opening, the middle and the
    // ending must be three different things, not one event told three times.
    const hooks = [episode.hook, episode.mid_hook, episode.cliffhanger?.text].filter(isText).map((text) => text.trim());
    if (new Set(hooks).size !== hooks.length) problems.push(`${who}: hook, mid_hook and cliffhanger.text must be three different beats`);
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
  // reversal (the series finale too, which leaves a door for a second part), never leaves the lead suffering, and opens on another type.
  const [opener, finale] = [episodes[0], episodes.at(-1)];
  if (opener?.cliffhanger?.type === "reversal") problems.push(`${where(opener)}: a season's first episode does not end on a reversal`);
  if (finale && finale.cliffhanger?.type !== "reversal") problems.push(`${where(finale)}: a season finale ends on a reversal`);
  if (finale?.lead_arc === "suffers") problems.push(`${where(finale)}: a season finale does not leave the lead suffering`);
  for (let start = 0; start + 4 <= episodes.length; start++) {
    const window = episodes.slice(start, start + 4);
    if (!window.some((episode) => episode.payoffs?.length)) problems.push(`${where(window[0])} to ${window[3].number} pay nothing off`);
  }
  for (const chapter of plan.chapters) {
    const rows = episodes.filter((episode) => episode.chapter === chapter.number);
    const used = new Set(rows.flatMap((episode) => episode.tones ?? []));
    for (const tone of chapter.tones) if (!used.has(tone)) problems.push(`S${pad(season.number)} chapter ${chapter.number} never uses its tone ${tone}`);
  }
  for (const thread of season.threads ?? []) {
    if (!episodes.some((episode) => episode.payoffs?.includes(thread.id))) problems.push(`thread ${thread.id} is never paid off`);
  }
  return problems;
}

export function planProblems({ setting, outline, seasons }) {
  const problems = [];
  const guestIds = new Set();
  for (const season of seasons) {
    for (const guest of season.guest_cast ?? []) {
      if (!isText(guest.id) || !isText(guest.name) || !isText(guest.appearance)) problems.push(`S${pad(season.number)}: guest ${guest.id} needs id, name and appearance`);
      if (!guest.id?.startsWith(`s${pad(season.number)}-`)) problems.push(`S${pad(season.number)}: guest id ${guest.id} must start with s${pad(season.number)}-`);
      if (guestIds.has(guest.id) || setting.characters.some((row) => row.id === guest.id)) problems.push(`guest id ${guest.id} is defined twice`);
      guestIds.add(guest.id);
    }
  }
  for (const season of seasons) problems.push(...seasonProblems(season, { setting, outline, guestIds }));
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

function main() {
  const setting = read("setting.json");
  const outline = read("outline.json");
  const only = process.argv.includes("--season") ? Number(process.argv[process.argv.indexOf("--season") + 1]) : null;
  const numbers = only ? [only] : outline.seasons.map((row) => row.number);
  const seasons = numbers.filter((n) => existsSync(join(here, `season-${pad(n)}.json`))).map((n) => read(`season-${pad(n)}.json`));
  const missing = numbers.filter((n) => !existsSync(join(here, `season-${pad(n)}.json`)));
  const problems = only ? seasonProblems(seasons[0] ?? { number: only, episodes: [] }, { setting, outline, guestIds: new Set((seasons[0]?.guest_cast ?? []).map((g) => g.id)) }) : planProblems({ setting, outline, seasons });
  if (missing.length && !only) problems.push(`missing season files: ${missing.map(pad).join(", ")}`);
  if (problems.length) {
    console.error(problems.join("\n"));
    console.error(`${problems.length} problem(s)`);
    process.exit(1);
  }
  const count = seasons.reduce((sum, season) => sum + season.episodes.length, 0);
  console.log(`ok: ${seasons.length} season(s), ${count} episodes`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
