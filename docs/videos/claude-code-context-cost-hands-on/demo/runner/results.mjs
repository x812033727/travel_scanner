// Runner: the small result files a card may quote, from the saved streams and records.
//   node results.mjs <logs> <out> <name> [<name> ...]
// first-request.json: per run, the three usage fields of the first request of the main
// conversation, their sum, the reported cost, the number of requests, and the init counts.
// No name that is not the seed's or Claude Code's own is written; no id, no path.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const [logs, out, ...names] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const rows = names.map((name) => {
  const lines = readFileSync(join(logs, `${name}.stream.jsonl`), 'utf8').split('\n').filter(Boolean).flatMap((line) => {
    try { return [JSON.parse(line)]; } catch { return []; }
  }).filter((line) => line.type !== 'rate_limit_event');
  const record = readFileSync(join(logs, `${name}.session.txt`), 'utf8');
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
    requests.push({ input: u.input_tokens ?? 0, cache_write: u.cache_creation_input_tokens ?? 0, cache_read: u.cache_read_input_tokens ?? 0, input_side: total });
  }
  const result = lines.filter((line) => line.type === 'result').at(-1) ?? {};
  const tools = init.tools ?? [];
  return {
    name,
    arm: (record.match(/^# \S+ \| arm (\S+)/) ?? [])[1],
    started: (record.match(/^# \S+ \| arm \S+ \| start (\S+)/) ?? [])[1],
    claude_code: init.claude_code_version,
    model: init.model,
    permission_mode: init.permissionMode,
    requests: requests.length,
    first_request: requests[0] ?? null,
    result: result.subtype,
    turns: result.num_turns,
    cost_usd: result.total_cost_usd,
    init_counts: {
      built_in_tools: tools.filter((tool) => !tool.startsWith('mcp__')).length,
      mcp_tools: tools.filter((tool) => tool.startsWith('mcp__')).length,
      mcp_servers: (init.mcp_servers ?? []).length,
      skills: (init.skills ?? []).length,
      agents: (init.agents ?? []).length,
      slash_commands: (init.slash_commands ?? []).length,
      plugins: (init.plugins ?? []).length,
    },
  };
});
writeFileSync(join(out, 'first-request.json'), `${JSON.stringify({ note: 'First request of the main conversation per run: input + cache_write + cache_read = input_side. One model, one version, one machine; base runs z1 and z2, every other arm once.', runs: rows }, null, 2)}\n`);
console.log(`wrote first-request.json: ${rows.length} runs | cost sum USD ${rows.reduce((n, row) => n + (row.cost_usd ?? 0), 0).toFixed(4)} | cost range ${Math.min(...rows.map((row) => row.cost_usd)).toFixed(4)} to ${Math.max(...rows.map((row) => row.cost_usd)).toFixed(4)}`);
