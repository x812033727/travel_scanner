// Runner check, not in the brief: what tally.mjs does not print. The seed's tally.mjs was written
// before any session ran; it reads the first init line and the last result line and looks for the
// subagent's report in a tool result or in a later user message. In 2.1.295 the report of a
// background subagent arrives as a system line (subtype task_notification), and a session with a
// background subagent has one result line per turn. This script prints those parts.
// Paths, uuids and ids are masked as in inspect.mjs. rate_limit_event lines are never read.
// Usage: node extras.mjs [--full] <logs>/<name>.stream.jsonl [...]
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
// truth.json sits next to this script in the demo folder, and in ../seed where the runner used it.
const truthFile = existsSync(join(here, 'truth.json')) ? join(here, 'truth.json') : join(here, '..', 'seed', 'truth.json');
const truth = JSON.parse(readFileSync(truthFile, 'utf8'));
const UNFINISHED = truth.unfinished.map((job) => job.id);
const NEXT_FILE = truth.finishedInTheNextFile.map((job) => job.id);
const MARK = '【trip-queue】';
const COUNT_LINE = /^[\s>*_`-]*共\s*\d+\s*筆/;
const args = process.argv.slice(2);
const full = args[0] === '--full';
const files = full ? args.slice(1) : args;
const home = homedir();
const user = home.split(/[\\/]/).pop();
const spell = (path) => [path, path.replaceAll('\\', '/'), path.replaceAll('\\', '\\\\')];
const sum3 = (usage) => (usage ? (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0) : null);
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block.text ?? textOf(block.content) ?? '')).join('\n') : '');
const rows = [];

for (const file of files) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).map((line) => JSON.parse(line)).filter((line) => line.type !== 'rate_limit_event');
  const inits = lines.filter((line) => line.type === 'system' && line.subtype === 'init');
  const cwd = inits[0]?.cwd ?? '';
  const mask = (text) => {
    let shown = String(text);
    for (const each of spell(cwd)) if (each) shown = shown.split(each).join('<lab>');
    for (const each of spell(home)) if (each) shown = shown.split(each).join('<home>');
    shown = shown.split(user).join('<user>');
    return shown
      .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>')
      .replace(/toolu_[A-Za-z0-9]+/g, '<id>')
      .replace(/\b[0-9a-f]{12,}\b/gi, '<id>');
  };
  const show = (text, limit) => {
    const all = mask(text).split('\n');
    const shown = full ? all : all.slice(0, limit);
    for (const each of shown) console.log(`      | ${full ? each : each.slice(0, 110)}`);
    if (shown.length < all.length) console.log(`      | (${all.length - shown.length} more lines)`);
  };
  console.log(`== ${name} (runner extras)`);
  const sameInit = inits.every((each) => JSON.stringify([each.tools, each.agents, each.skills, each.model]) === JSON.stringify([inits[0].tools, inits[0].agents, inits[0].skills, inits[0].model]));
  console.log(`   init lines: ${inits.length}${inits.length > 1 ? ` (tools, agents, skills and model the same on each: ${sameInit ? 'yes' : 'NO'})` : ''}`);

  // Result lines: one per turn.
  const results = lines.filter((line) => line.type === 'result');
  results.forEach((result, at) => {
    const reply = typeof result.result === 'string' ? result.result : '';
    console.log(`   result line ${at + 1} of ${results.length}: ${result.subtype} | origin ${result.origin?.kind ?? '(none: the turn of the request)'} | num_turns ${result.num_turns} | usage ${sum3(result.usage)} input-side tokens, ${result.usage?.output_tokens} output | total_cost_usd ${result.total_cost_usd} | reply ${reply.length} chars, planted ids in it ${UNFINISHED.filter((id) => reply.includes(id)).length} of ${UNFINISHED.length}`);
  });
  const last = results.at(-1) ?? {};
  const stats = last.subagent_stats;
  if (stats) console.log(`   last result line, subagent_stats: spawned ${stats.spawned} | requested background ${stats.requested?.background}, foreground ${stats.requested?.foreground}, unset ${stats.requested?.unset} | started_in_background ${stats.started_in_background} | completed ${stats.completed} | failed ${stats.failed} | by_type keys ${Object.keys(stats.by_type ?? {}).length}`);
  else console.log('   last result line has no subagent_stats');
  if (results.length > 1) {
    console.log('   the reply of every result line before the last:');
    results.slice(0, -1).forEach((result) => show(result.result ?? '', 6));
  }

  // The main conversation, request by request.
  const mainUsage = new Map();
  const underUsage = new Map();
  let underAssistant = 0; let underUser = 0; let underText = 0;
  const underKeys = new Set();
  for (const line of lines) {
    if (line.type === 'assistant' && line.message?.usage && line.message.id) (line.parent_tool_use_id ? underUsage : mainUsage).set(line.message.id, line.message.usage);
    if (line.parent_tool_use_id && (line.type === 'assistant' || line.type === 'user')) {
      if (line.type === 'assistant') underAssistant += 1; else underUser += 1;
      for (const key of Object.keys(line)) if (!['type', 'message', 'uuid', 'session_id', 'parent_tool_use_id', 'timestamp', 'request_id'].includes(key)) underKeys.add(key);
      for (const block of (Array.isArray(line.message?.content) ? line.message.content : [])) if (block.type === 'text' && line.type === 'assistant') underText += 1;
    }
  }
  const fmt = (usage) => `${sum3(usage)} (in ${usage.input_tokens} + cache write ${usage.cache_creation_input_tokens} + cache read ${usage.cache_read_input_tokens}; out ${usage.output_tokens})`;
  console.log(`   main conversation, each request's input side: ${[...mainUsage.values()].map((usage) => sum3(usage)).join(', ')}`);
  console.log(`   lines under an Agent call: ${underAssistant} assistant, ${underUser} user | assistant text blocks ${underText} | extra keys on those lines: ${[...underKeys].join(', ') || 'none'}`);
  if (underUsage.size) console.log(`   requests under Agent calls, input side: ${[...underUsage.values()].map((usage) => fmt(usage)).join(' | ')}`);

  // Each Agent call: the task as Claude wrote it, how it was started, and what came back.
  const spawns = [];
  for (const line of lines) {
    if (line.type !== 'assistant' || line.parent_tool_use_id) continue;
    for (const block of line.message?.content ?? []) if (block.type === 'tool_use' && (block.name === 'Agent' || block.name === 'Task') && !spawns.some((each) => each.id === block.id)) spawns.push({ id: block.id, input: block.input ?? {} });
  }
  let launchChars = 0; let reportChars = 0; let insideChars = 0; let background = 0; let otherResultChars = 0; let reportFound = 0; let reportNext = 0; let reportMark = false; let reportCount = false;
  const spawnIds = new Set(spawns.map((each) => each.id));
  for (const line of lines) {
    if (line.type !== 'user' || line.parent_tool_use_id) continue;
    for (const block of (Array.isArray(line.message?.content) ? line.message.content : [])) {
      if (block.type !== 'tool_result') continue;
      if (spawnIds.has(block.tool_use_id)) launchChars += textOf(block.content).length; else otherResultChars += textOf(block.content).length;
    }
  }
  spawns.forEach((spawn, at) => {
    const prompt = String(spawn.input.prompt ?? '');
    console.log(`   Agent call ${at + 1}: description ${JSON.stringify(spawn.input.description ?? null)} | prompt ${prompt.length} chars, planted ids in it ${UNFINISHED.filter((id) => prompt.includes(id)).length}, names REPORT.md: ${prompt.includes('REPORT.md') ? 'yes' : 'no'}, marker: ${prompt.includes(MARK) ? 'yes' : 'no'}`);
    console.log('      the task as Claude wrote it:');
    show(prompt, 12);
    const started = lines.find((line) => line.type === 'system' && line.subtype === 'task_started' && line.tool_use_id === spawn.id);
    console.log(`      system/task_started: ${started ? `is_backgrounded ${started.is_backgrounded} | spawn_depth ${started.spawn_depth} | task_type ${started.task_type} | carries the prompt: ${started.prompt === prompt ? 'yes, the same text' : started.prompt === undefined ? 'no' : 'yes, a different text'}` : 'none seen'}`);
    const result = lines.find((line) => line.type === 'user' && !line.parent_tool_use_id && Array.isArray(line.message?.content) && line.message.content.some((block) => block.type === 'tool_result' && block.tool_use_id === spawn.id));
    const meta = result?.tool_use_result;
    const resultText = result ? textOf(result.message.content.find((block) => block.tool_use_id === spawn.id).content) : '';
    console.log(`      its tool result: ${result ? `${resultText.length} chars | tool_use_result status ${meta?.status ?? '-'} | isAsync ${meta?.isAsync ?? '-'} | resolvedModel ${meta?.resolvedModel ?? '-'} | totalTokens ${meta?.totalTokens ?? '-'} | totalToolUseCount ${meta?.totalToolUseCount ?? '-'} | keys ${meta && typeof meta === 'object' ? Object.keys(meta).join(',') : '-'}` : 'none seen'}`);
    const progress = lines.filter((line) => line.type === 'system' && line.subtype === 'task_progress' && line.tool_use_id === spawn.id);
    if (progress.length) console.log(`      system/task_progress lines: ${progress.length} | the last one: total_tokens ${progress.at(-1).usage?.total_tokens}, tool_uses ${progress.at(-1).usage?.tool_uses}`);
    const note = lines.find((line) => line.type === 'system' && line.subtype === 'task_notification' && line.tool_use_id === spawn.id);
    if (!note) {
      console.log('      system/task_notification: none seen for this call');
      if (meta?.status === 'completed' || (result && !meta?.isAsync)) {
        reportChars += resultText.length;
        reportFound = Math.max(reportFound, UNFINISHED.filter((id) => resultText.includes(id)).length);
        reportNext = Math.max(reportNext, NEXT_FILE.filter((id) => resultText.includes(id)).length);
        reportMark = reportMark || resultText.includes(MARK);
        reportCount = reportCount || resultText.split('\n').some((each) => COUNT_LINE.test(each));
        launchChars -= resultText.length;
      }
      return;
    }
    const summary = String(note.summary ?? '');
    if (meta?.isAsync) background += 1; else insideChars += summary.length;
    const countLine = summary.split('\n').find((each) => COUNT_LINE.test(each));
    if (meta?.isAsync) reportChars += summary.length;
    reportFound = Math.max(reportFound, UNFINISHED.filter((id) => summary.includes(id)).length);
    reportNext = Math.max(reportNext, NEXT_FILE.filter((id) => summary.includes(id)).length);
    reportMark = reportMark || summary.includes(MARK);
    reportCount = reportCount || Boolean(countLine);
    console.log(`      system/task_notification: status ${note.status} | keys ${Object.keys(note).filter((key) => !['type', 'subtype', 'uuid', 'session_id'].includes(key)).join(',')} | usage on it: ${note.usage ? JSON.stringify(note.usage) : 'none'}`);
    console.log(`      its summary (the subagent's report): ${summary.length} chars, ${summary.split('\n').length} lines | planted ids in it ${UNFINISHED.filter((id) => summary.includes(id)).length} of ${UNFINISHED.length} | next-file ids in it: ${NEXT_FILE.filter((id) => summary.includes(id)).join(' ') || 'none'} | a line "共 N 筆": ${countLine ? `yes (${countLine.trim().slice(0, 40)})` : 'no'} | marker ${MARK}: ${summary.includes(MARK) ? 'yes' : 'no'}`);
    show(summary, 24);
  });
  if (spawns.length) console.log(`   what reached the main conversation because of Agent calls: tool results of Agent calls ${launchChars} chars (of which the report itself, for a foreground call: ${insideChars}) + reports that arrived later as a task_notification (background calls: ${background}) ${reportChars} chars = ${launchChars + reportChars} | from its own tools ${otherResultChars} chars | all three ${launchChars + reportChars + otherResultChars}`);
  else console.log(`   no Agent call | tool results in the main conversation ${otherResultChars} chars`);
  const reply = typeof last.result === 'string' ? last.result : '';
  if (full) { console.log('   the final reply in full:'); show(reply, 0); }
  rows.push([name, spawns.length, spawns.length ? (background ? 'background' : 'foreground') : '-', launchChars, reportChars || insideChars, otherResultChars, launchChars + reportChars + otherResultChars,
    spawns.length ? `${reportFound}/7` : '-', spawns.length ? reportNext : '-', spawns.length ? (reportCount ? 'yes' : 'no') : '-',
    results.length, [...mainUsage.values()].map((usage) => sum3(usage)).join('+'), underUsage.size, [...underUsage.values()].reduce((total, usage) => total + sum3(usage), 0),
    last.duration_ms ?? '-', reply.length]);
}
if (files.length > 1) {
  console.log('\nname | Agent calls | how it ran | chars of the tool result of the Agent call | chars of the report itself | own-tool result chars | all that reached the main conversation | planted ids in the report | next-file ids in the report | report has 共 N 筆 | result lines | main requests (input side each) | requests under Agent | their input side added up | last turn duration_ms | final reply chars');
  for (const row of rows) console.log(row.join(' | '));
}
