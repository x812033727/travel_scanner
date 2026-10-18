// The reading rules of the tool-loading video, applied mechanically to the saved streams.
//
//   node <seed>/runner/ladder.mjs <logs> [--warm w0] [--base z1,z2] [--off zf] [--floor 11]
//                                        [--skip name,name]
//
// It reads every <name>.stream.jsonl in <logs> and the arm on line 1 of <name>.session.txt.
// First request = input + cache write + cache read of the first request of the main
// conversation (the same sum ctx-cost.mjs prints). The rules, fixed before any session ran:
//   - the warm-up run is shown and never used;
//   - a base run counts for an arm only when five init counts are the same in both: built-in
//     tools, skills, agents, slash commands, plugins. The base of an arm is the mean of the
//     base runs that match it (--base for the default arms, --off for arms with tool search
//     off). No matching base run: the arm gets no "minus base";
//   - the bar is the larger of the difference between the two default base runs and --floor.
//     A difference no larger than the bar is "cannot tell";
//   - two arms are compared directly only when skills, agents, slash commands and plugins are
//     the same in both;
//   - the ladder is N = 2, 10 and 40. The server with no tools (N = 0) is never a rung: it is
//     printed on lines of its own;
//   - "is it a straight line" is asked in characters, not in tools: x is what the server hands
//     over (the tools/list JSON when loaded up front, the prefixed names when deferred; the
//     constants below are check-server.mjs's figures). The line goes through N = 2 and 10 and is
//     read at N = 40; each of the three runs is allowed half the bar, so the tolerance is
//     bar / 2 x (1 + |1 - t| + |t|) with t = (x3 - x1) / (x2 - x1), which is bar x t here.
// It calls no model, prints no name but the arms' own, and never reads a rate-limit event.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

// Characters the server hands a client for N tools (check-server.mjs checks this line).
const CHARS = {"up":{"0":2,"2":302,"10":1473,"40":6003},"names":{"0":0,"2":41,"10":219,"40":946}};
const RUNGS = [2, 10, 40];

const args = process.argv.slice(2);
const VALUED = ['--warm', '--base', '--off', '--floor', '--skip'];
const option = (name, fallback) => { const at = args.indexOf(name); return at >= 0 ? args[at + 1] : fallback; };
const dir = args.find((arg, at) => !arg.startsWith('--') && !VALUED.includes(args[at - 1]));
const floor = Number(option('--floor', '11'));
if (!dir || !existsSync(dir) || !Number.isFinite(floor) || floor < 0) {
  console.error('usage: node ladder.mjs <logs> [--warm w0] [--base z1,z2] [--off zf] [--floor 11] [--skip name,name]');
  process.exit(2);
}
const warm = option('--warm', 'w0');
const baseNames = option('--base', 'z1,z2').split(',');
const offNames = option('--off', 'zf').split(',');
const skip = option('--skip', '').split(',').filter(Boolean);
const num = (value) => Number(value).toLocaleString('en-US');
const round1 = (value) => Math.round(value * 10) / 10;
const signed = (value) => `${value >= 0 ? '+' : '-'}${num(Math.abs(round1(value)))}`;
const mean = (list) => list.reduce((n, each) => n + each, 0) / list.length;

function read(name) {
  const lines = readFileSync(join(dir, `${name}.stream.jsonl`), 'utf8').split('\n').filter(Boolean).flatMap((line) => {
    try { return [JSON.parse(line)]; } catch { return []; }
  }).filter((line) => line.type !== 'rate_limit_event');
  const record = existsSync(join(dir, `${name}.session.txt`)) ? readFileSync(join(dir, `${name}.session.txt`), 'utf8') : '';
  const arm = (record.match(/^# \S+ \| arm (\S+)/) ?? [])[1] ?? '?';
  const ended = /^# \S+ \| end /m.test(record);
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const seen = new Set();
  const requests = [];
  for (const line of lines) {
    if (line.type !== 'assistant' || line.parent_tool_use_id) continue;
    const message = line.message ?? {};
    if (!message.id || !message.usage || seen.has(message.id)) continue;
    seen.add(message.id);
    const u = message.usage;
    const total = (u.input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0);
    if (message.model === '<synthetic>' || total === 0) continue;
    requests.push(total);
  }
  const tools = init.tools ?? [];
  const counts = {
    builtin: tools.filter((tool) => !String(tool).startsWith('mcp__')).length,
    skills: (init.skills ?? []).length, agents: (init.agents ?? []).length,
    commands: (init.slash_commands ?? []).length, plugins: (init.plugins ?? []).length,
  };
  return { name, arm, ended, requests, first: requests[0] ?? null, counts, mcp: tools.filter((tool) => String(tool).startsWith('mcp__')).length };
}
const all = readdirSync(dir).filter((file) => file.endsWith('.stream.jsonl')).map((file) => file.replace(/\.stream\.jsonl$/, '')).sort()
  .filter((name) => !skip.includes(name)).map(read);
const byName = (name) => all.find((s) => s.name === name);
const usable = (s) => s && s.first !== null && s.ended;
const key = (s, withTools) => `${withTools ? `${s.counts.builtin}/` : ''}${s.counts.skills}/${s.counts.agents}/${s.counts.commands}/${s.counts.plugins}`;
const countsShown = (s) => `built-in ${s.counts.builtin} | skills ${s.counts.skills} | agents ${s.counts.agents} | slash ${s.counts.commands} | plugins ${s.counts.plugins}`;

const bases = baseNames.map(byName).filter(usable);
const offs = offNames.map(byName).filter(usable);
const spread = bases.length === 2 && key(bases[0], true) === key(bases[1], true) ? Math.abs(bases[0].first - bases[1].first) : null;
const bar = Math.max(spread ?? 0, floor);
// The base of an arm: the mean of the runs in the pool whose counts match it. withTools false
// leaves the built-in tools out of the match (ToolSearch goes when tool search is off).
const baseOf = (s, pool, withTools = true) => {
  const fit = pool.filter((b) => key(b, withTools) === key(s, withTools));
  return fit.length ? { mean: mean(fit.map((b) => b.first)), names: fit.map((b) => b.name) } : null;
};
const told = (diff, limit = bar) => (Math.abs(diff) <= limit ? `${signed(diff)} (cannot tell: inside ${num(round1(limit))})` : signed(diff));

console.log(`== the base runs (floor ${num(floor)})`);
const w = byName(warm);
console.log(`warm-up ${warm}: ${w ? `first request ${w.first === null ? 'none' : num(w.first)} | ${countsShown(w)} | shown, never used` : 'no such stream'}`);
for (const name of baseNames) { const s = byName(name); console.log(`base ${name}: ${usable(s) ? `first request ${num(s.first)} | ${countsShown(s)}` : 'no usable stream (missing, interrupted, or no request)'}`); }
for (const name of offNames) { const s = byName(name); console.log(`base with tool search off ${name}: ${usable(s) ? `first request ${num(s.first)} | ${countsShown(s)}` : 'no usable stream'}`); }
console.log(spread === null ? `bar: ${num(bar)} (the floor: there are not two default base runs with the same counts)` : `bar: ${num(bar)} (the larger of |${bases[0].name} - ${bases[1].name}| = ${num(spread)} and the floor ${num(floor)})`);
if (usable(w) && bases.length) {
  const fit = baseOf(w, bases);
  console.log(fit ? `warm-up minus the base runs with the same counts (${fit.names.join(', ')}): ${signed(w.first - fit.mean)}`
    : `warm-up: no base run has its counts; against each, for the record: ${bases.map((b) => `${b.name} ${signed(w.first - b.first)}`).join(', ')}`);
}
if (offs.length && bases.length) {
  const fit = baseOf(offs[0], bases, false);
  console.log(`tool search off, no server, minus the default base: ${fit ? `${told(offs[0].first - fit.mean)} (against ${fit.names.join(', ')})` : 'not compared (no default base run has its skills, agents, slash commands and plugins)'} | built-in tools ${offs[0].counts.builtin} against ${bases[0].counts.builtin}`);
}

const arms = {};
for (const s of all) {
  const m = s.arm.match(/^(use-)?([dua])(\d+)$/);
  if (!m) continue;
  const id = `${m[1] ?? ''}${m[2]}${m[3]}`;
  if (arms[id]) { console.error(`two streams have the arm ${id} (${arms[id].name}, ${s.name}): pass --skip with the one that is not to be read`); process.exit(2); }
  arms[id] = { ...s, mode: m[2], n: Number(m[3]), use: Boolean(m[1]) };
}
const get = (mode, n) => { const a = arms[`${mode}${n}`]; return usable(a) ? a : null; };
const direct = (a, b) => (a && b && key(a, false) === key(b, false) ? a.first - b.first : null);
const ns = RUNGS.filter((n) => arms[`d${n}`] || arms[`u${n}`]);

console.log('');
console.log('== the ladder: first request of each arm');
console.log('N | deferred: first, minus base | up front: first, minus base | deferred minus up front');
for (const n of ns) {
  const cell = (a, pool) => {
    if (!a) return 'no usable stream';
    const base = baseOf(a, pool);
    return `${num(a.first)}, ${base ? told(a.first - base.mean) : 'no base run with the same counts'}`;
  };
  const d = get('d', n); const u = get('u', n); const gap = direct(d, u);
  console.log(`${n} | ${cell(d, bases)} | ${cell(u, offs)} | ${gap === null ? 'not compared' : told(gap)}`);
}
// How the previous video measured its up-front arm: against the default base, built-in tools apart.
console.log(`up front minus the default base (two things differ; how the previous video measured it): ${ns.map((n) => { const u = get('u', n); const base = u ? baseOf(u, bases, false) : null; return `${n} ${base ? signed(u.first - base.mean) : 'not compared'}`; }).join(' | ') || 'none'}`);
console.log(`MCP tools on the init event: ${Object.values(arms).filter((a) => !a.use).sort((a, b) => a.mode.localeCompare(b.mode) || a.n - b.n).map((a) => `${a.mode}${a.n} ${a.mcp}`).join(' | ') || 'none'}`);
// Threshold mode (ENABLE_TOOL_SEARCH=auto) is outside the run list: read only when its stream exists.
for (const a of Object.values(arms).filter((each) => !each.use && each.mode === 'a' && usable(each))) {
  const d = get('d', a.n); const u = get('u', a.n);
  console.log(`threshold mode, N = ${a.n}: first ${num(a.first)} | built-in tools ${a.counts.builtin} | minus deferred ${direct(a, d) === null ? 'not compared' : told(direct(a, d))} | minus up front ${direct(a, u) === null ? 'not compared' : told(direct(a, u))}`);
}

console.log('');
console.log('== per tool, between two rungs of the same mode (arms that differ only in N)');
// One line per mode through N = 2 and 10, in characters; null when a rung is missing or two
// rungs cannot be compared directly.
const lines = {};
for (const mode of ['d', 'u']) {
  const label = mode === 'd' ? 'deferred' : 'up front';
  const what = mode === 'd' ? 'names' : 'tools/list';
  const x = CHARS[mode === 'd' ? 'names' : 'up'];
  const have = ns.map((n) => get(mode, n)).filter(Boolean);
  for (let at = 1; at < have.length; at += 1) {
    const gap = direct(have[at], have[at - 1]);
    const more = have[at].n - have[at - 1].n;
    const chars = round1((x[have[at].n] - x[have[at - 1].n]) / more);
    console.log(`${label} ${have[at - 1].n} -> ${have[at].n}: ${gap === null ? 'not compared' : `${told(gap)} for ${more} more tools${Math.abs(gap) > bar ? ` = ${signed(gap / more)} a tool` : ''}`} | ${what} ${num(chars)} characters a tool`);
  }
  const [a, b, c] = RUNGS.map((n) => get(mode, n));
  if (!a || !b || direct(b, a) === null) continue;
  const slope = (b.first - a.first) / (x[b.n] - x[a.n]);
  const at = (chars) => a.first + slope * (chars - x[a.n]);
  const tolerance = (chars) => { const t = (chars - x[a.n]) / (x[b.n] - x[a.n]); return (bar / 2) * (1 + Math.abs(1 - t) + Math.abs(t)); };
  lines[mode] = { at, tolerance, zero: at(x[0]), base: baseOf(a, mode === 'd' ? bases : offs) };
  if (c && direct(c, a) !== null) {
    const off = c.first - at(x[c.n]);
    const limit = tolerance(x[c.n]);
    console.log(`${label}: a straight line in characters of ${what} through N = ${a.n} and ${b.n} (${num(x[a.n])} and ${num(x[b.n])}) puts N = ${c.n} (${num(x[c.n])}) at ${num(Math.round(at(x[c.n])))}; it came out ${num(c.first)} (${signed(off)}; ${Math.abs(off) <= limit ? `within ${num(round1(limit))}, in proportion to the characters` : `more than ${num(round1(limit))} off the line`})`);
  }
  if (lines[mode].base) console.log(`${label}: the same line at N = 0 (${num(x[0])} characters) is ${num(Math.round(lines[mode].zero))}, ${signed(lines[mode].zero - lines[mode].base.mean)} over its base (a calculation, not a run)`);
}
if (lines.d && lines.u) console.log(`the deferred line at N = 0 minus the up-front line at N = 0: ${signed(lines.d.zero - lines.u.zero)} (the part that does not follow the number of tools; a calculation)`);

// The server with no tools, when its stream exists: never a rung, never part of a line.
const d0 = get('d', 0);
if (arms.d0) {
  console.log('');
  console.log('== the server with no tools (d0), on its own');
  if (!d0) console.log('d0: no usable stream');
  else {
    const base = baseOf(d0, bases);
    console.log(`d0: first request ${num(d0.first)} | ${countsShown(d0)} | MCP tools on the init event ${d0.mcp}`);
    console.log(`server with no tools, minus base: ${base ? told(d0.first - base.mean) : 'no base run with the same counts'}`);
    for (const [mode, label] of [['d', 'deferred'], ['u', 'up-front']]) {
      const line = lines[mode];
      const pair = get(mode, 2);
      if (!line || direct(d0, pair) === null) { console.log(`the ${label} line at N = 0 (calculation) minus d0 (run): not compared`); continue; }
      const gap = line.zero - d0.first;
      const limit = line.tolerance(CHARS[mode === 'd' ? 'names' : 'up'][0]);
      console.log(`the ${label} line at N = 0 (calculation) minus d0 (run): ${signed(gap)} (${Math.abs(gap) <= limit ? `within ${num(round1(limit))}: d0 sits on the ${label} line` : `more than ${num(round1(limit))}: d0 is off the ${label} line`})`);
    }
  }
}

console.log('');
console.log('== where deferred loading becomes the smaller first request');
const rungs = ns.map((n) => { const gap = direct(get('d', n), get('u', n)); return { n, gap, sign: gap === null ? null : Math.abs(gap) <= bar ? 0 : Math.sign(gap) }; });
let turned = false;
rungs.forEach((rung, at) => {
  if (rung.gap === null) { console.log(`N = ${rung.n}: not compared`); return; }
  console.log(`N = ${rung.n}: ${rung.sign === 0 ? 'cannot tell' : rung.sign > 0 ? 'up front is smaller' : 'deferred is smaller'} (${signed(rung.gap)})`);
  const before = rungs[at - 1]; const after = rungs[at + 1];
  if (before && before.sign && rung.sign && before.sign !== rung.sign) {
    turned = true;
    const cross = before.n + (before.gap / (before.gap - rung.gap)) * (rung.n - before.n);
    console.log(`   between N = ${before.n} and ${rung.n} the order turns over; on a straight line between those two rungs, at about ${round1(cross)} tools (a calculation: nothing was run between them)`);
  }
  if (rung.sign === 0 && before && after && before.sign && after.sign && before.sign !== after.sign) {
    turned = true;
    console.log(`   the order turns over at about N = ${rung.n}: the rungs on either side point opposite ways and this one cannot tell (no calculation between rungs)`);
  }
});
if (!turned && rungs.length === RUNGS.length && rungs.every((rung) => rung.sign) && new Set(rungs.map((rung) => rung.sign)).size === 1) console.log('   the order does not turn over among these three tool counts');
else if (!turned) console.log('   no turn-over can be placed from these rungs');

const uses = Object.values(arms).filter((a) => a.use && usable(a)).sort((a, b) => a.mode.localeCompare(b.mode));
if (uses.length) {
  console.log('');
  console.log('== the sessions that call one tool (the request names the tool)');
  console.log('arm | requests | each request | last minus first | all requests added up | first request minus the same arm without a call');
  for (const a of uses) {
    const gap = direct(a, get(a.mode, a.n));
    console.log(`use-${a.mode}${a.n} | ${a.requests.length} | ${a.requests.map(num).join(', ')} | ${signed(a.requests.at(-1) - a.first)} | ${num(a.requests.reduce((x, y) => x + y, 0))} | ${gap === null ? 'not compared' : signed(gap)}`);
  }
  const d = uses.find((a) => a.mode === 'd'); const u = uses.find((a) => a.mode === 'u');
  if (d && u && d.n === u.n && key(d, false) === key(u, false)) {
    console.log(`deferred minus up front, N = ${d.n}: first request ${told(d.first - u.first)} | last request ${told(d.requests.at(-1) - u.requests.at(-1))} | all requests added up ${signed(d.requests.reduce((x, y) => x + y, 0) - u.requests.reduce((x, y) => x + y, 0))} | requests ${d.requests.length} against ${u.requests.length}`);
  }
}
// What needs a rerun under a new name: an arm of the ladder whose counts match no base run.
const lost = Object.values(arms).filter((a) => usable(a) && a.mode !== 'a' && !baseOf(a, a.mode === 'u' ? offs : bases));
if (lost.length) { console.log(''); console.log(`arms whose counts match no base run (rerun under a new name, then --skip the old one): ${lost.map((a) => a.name).join(', ')}`); }
const rest = all.filter((s) => !usable(s));
if (rest.length) { console.log(''); console.log(`not read (no request, or the record has no end line): ${rest.map((s) => s.name).join(', ')}`); }
