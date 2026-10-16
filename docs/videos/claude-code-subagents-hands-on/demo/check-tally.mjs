// Builds three MADE-UP sessions in a temporary folder (a stream in the shape the official
// headless and Agent SDK pages describe for Claude Code 2.1.295, and the project each would have
// left) and runs tally.mjs on them. It checks the parser and the counting rules: one session that
// read every log in the main conversation, one that handed the reading to the project's agent in
// the foreground, one whose agent ran in the background and whose report came back as a later
// message. The shape of an Agent call, of the messages under it and of the result line's
// modelUsage are guesses from the documentation that the first real session confirms or corrects.
// It is not evidence of anything a model did, and the made-up files are deleted when it ends.
// No session, no model.
// Usage: node <seed>/check-tally.mjs
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const truth = JSON.parse(readFileSync(join(here, 'truth.json'), 'utf8'));
const planted = truth.unfinished.map((job) => job.id);
const trap = truth.finishedInTheNextFile[0].id;
const scratch = mkdtempSync(join(tmpdir(), 'log-lab-tally-'));
const cwd = join(scratch, 'log-lab');
const days = ['01', '02', '03', '04', '05', '06'].map((day) => `queue-2026-10-${day}.log`);
const init = (tools, agents) => ({
  type: 'system', subtype: 'init', cwd, model: 'made-up-model', claude_code_version: '0.0.0', permissionMode: 'default',
  tools, mcp_servers: [], plugins: [], skills: ['verify', 'debug'], slash_commands: ['clear'], agents,
});
let ids = 0;
const usage = (read) => ({ input_tokens: 3, cache_creation_input_tokens: 500, cache_read_input_tokens: read, output_tokens: 10 });
const call = (name, input, read, parent = null) => {
  ids += 1;
  return { type: 'assistant', parent_tool_use_id: parent, message: { id: `m${ids}`, model: 'made-up-model', usage: read ? usage(read) : undefined, content: [{ type: 'tool_use', id: `t${ids}`, name, input }] } };
};
const back = (text, parent = null, id = `t${ids}`) => ({ type: 'user', parent_tool_use_id: parent, message: { content: [{ type: 'tool_result', tool_use_id: id, content: text }] } });
const say = (text, read) => { ids += 1; return { type: 'assistant', parent_tool_use_id: null, message: { id: `m${ids}`, model: 'made-up-model', usage: usage(read), content: [{ type: 'text', text }] } }; };
const result = (text, tree) => ({
  type: 'result', subtype: 'success', num_turns: 4, permission_denials: [], result: text, total_cost_usd: 0,
  usage: { input_tokens: 12, cache_creation_input_tokens: 3000, cache_read_input_tokens: 20000, output_tokens: 900 },
  modelUsage: { 'made-up-model': { inputTokens: 20, outputTokens: 1500, cacheReadInputTokens: tree, cacheCreationInputTokens: 6000 } },
});
const logText = (name) => readFileSync(join(here, 'log-lab', 'logs', name), 'utf8');
const report = `${planted.map((id) => `${id}｜queue-2026-10-01.log｜1`).join('\n')}\n共 ${planted.length} 筆`;

function project(name, { agent, reportFile }) {
  const lab = join(scratch, `${name}.lab`);
  cpSync(join(here, 'log-lab'), lab, { recursive: true });
  if (agent) {
    mkdirSync(join(lab, '.claude', 'agents'), { recursive: true });
    cpSync(join(here, 'variants', 'log-scout.agent.md'), join(lab, '.claude', 'agents', 'log-scout.md'));
  }
  if (reportFile) writeFileSync(join(lab, 'REPORT.md'), `${report}\n`);
}
project('made-up-inline', { agent: false });
project('made-up-delegated', { agent: true });
project('made-up-background', { agent: true, reportFile: true });

const reads = (parent) => days.flatMap((name) => [call('Read', { file_path: join(cwd, 'logs', name) }, parent ? 0 : 9000 + ids * 400, parent), back(logText(name), parent)]);
const delegated = [];
{
  delegated.push(init(['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Task'], ['Explore', 'Plan', 'general-purpose', 'log-scout']));
  const agentCall = call('Agent', { description: 'made up', prompt: 'made-up task', subagent_type: 'log-scout' }, 9200);
  const parent = agentCall.message.content[0].id;
  delegated.push(agentCall, { type: 'user', parent_tool_use_id: parent, message: { content: [{ type: 'text', text: 'made-up task' }] } });
  delegated.push(call('Glob', { pattern: 'logs/*.log' }, 0, parent), back(days.join('\n'), parent), ...reads(parent));
  delegated.push(back(report, null, parent), say('done', 9900), result(`沒有結束的 job：${planted.join('、')}`, 60000));
}
const background = [];
{
  background.push(init(['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Agent'], ['Explore', 'log-scout', 'an-agent-from-somewhere-else']));
  const agentCall = call('Agent', { description: 'made up', prompt: 'made-up task 【trip-queue】', subagent_type: 'log-scout', run_in_background: true, model: 'sonnet' }, 9200);
  const parent = agentCall.message.content[0].id;
  background.push(agentCall, back('Async agent launched. agentId: 0123456789abcdef0123', null, parent), say('waiting', 9300));
  background.push({ type: 'system', subtype: 'task_notification' });
  background.push({ type: 'user', parent_tool_use_id: null, message: { content: [{ type: 'text', text: `made-up notification\n${report}` }] } });
  background.push(call('Write', { file_path: join(cwd, 'REPORT.md') }, 9800), back('ok'));
  background.push(result(`【trip-queue】\n寫進 REPORT.md 了：${planted.slice(0, 5).join('、')}`, 61000));
}
const streams = {
  'made-up-inline': [
    init(['Read', 'Glob', 'Grep', 'Edit', 'Write'], undefined),
    call('Glob', { pattern: 'logs/*.log' }, 8700), back(days.join('\n')),
    ...reads(null),
    result(`沒有結束的 job：${planted.join('、')}\n另外 ${trap} 在當天的檔案裡沒有 done。`, 90000),
  ],
  'made-up-delegated': delegated,
  'made-up-background': background,
};
const files = Object.entries(streams).map(([name, lines]) => {
  const file = join(scratch, `${name}.stream.jsonl`);
  writeFileSync(file, `${lines.map((line) => JSON.stringify(line)).join('\n')}\n`);
  return file;
});
const run = spawnSync(process.execPath, [join(here, 'tally.mjs'), ...files], { encoding: 'utf8' });
process.stdout.write(run.stdout.split(scratch).join('<scratch>'));
process.stderr.write(run.stderr);
rmSync(scratch, { recursive: true, force: true });
process.exitCode = run.status ?? 1;
