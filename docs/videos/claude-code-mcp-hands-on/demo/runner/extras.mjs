// What the seed's tally.mjs does not print, for each stream given:
// the seed's entries of mcp_servers in full, every system line that is not init (subtype and keys;
// permission_denied in full without ids), the usage of every request split in three, the final
// reply in full, the cost. Paths are written <lab>; uuids and tool-call ids are masked.
// Usage: node extras.mjs <logs>/<name>.stream.jsonl ...
import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const SEED = new Set(['gear', 'gear-more']);
let total = 0;
for (const file of process.argv.slice(2)) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
    try { return [JSON.parse(line)]; } catch { return []; }
  });
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const cwd = init.cwd ?? '';
  const mask = (text) => {
    let shown = String(text);
    for (const spelling of new Set([cwd.replaceAll('\\', '\\\\'), cwd, cwd.replaceAll('\\', '/')])) if (spelling) shown = shown.split(spelling).join('<lab>');
    return shown.replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>').replace(/toolu_[0-9A-Za-z]{6,}/g, 'toolu_<id>');
  };
  const result = lines.findLast((line) => line.type === 'result') ?? {};
  console.log(`== ${name}`);
  console.log(`   mcp_servers (the seed's, in full): ${JSON.stringify((init.mcp_servers ?? []).filter((s) => SEED.has(s.name)))}`);
  console.log(`   mcp_server_errors key: ${'mcp_server_errors' in init ? JSON.stringify(init.mcp_server_errors).length + ' chars' : 'not on the init line'}`);
  for (const line of lines) {
    if (line.type !== 'system' || line.subtype === 'init') continue;
    const keys = Object.keys(line).filter((k) => !['type', 'subtype', 'uuid', 'session_id'].includes(k));
    if (line.subtype === 'permission_denied') {
      const rest = Object.fromEntries(keys.map((k) => [k, line[k]]));
      console.log(`   system ${line.subtype}: ${mask(JSON.stringify(rest))}`);
    } else {
      console.log(`   system ${line.subtype}: keys ${keys.join(',')}`);
    }
  }
  const seen = new Set();
  let n = 0;
  for (const line of lines) {
    if (line.type !== 'assistant') continue;
    const m = line.message ?? {};
    if (!m.usage || seen.has(m.id)) continue;
    seen.add(m.id);
    n += 1;
    const u = m.usage;
    console.log(`   request ${n}: input ${u.input_tokens ?? 0} + cache write ${u.cache_creation_input_tokens ?? 0} + cache read ${u.cache_read_input_tokens ?? 0} = ${(u.input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0)} | blocks: ${(m.content ?? []).map((b) => b.type).join('+')}`);
  }
  // Assistant lines per message id: content blocks arrive one line each.
  const perId = new Map();
  for (const line of lines) if (line.type === 'assistant') perId.set(line.message?.id, [...(perId.get(line.message?.id) ?? []), ...(line.message?.content ?? []).map((b) => b.type)]);
  console.log(`   assistant lines per request: ${[...perId.values()].map((blocks) => blocks.join('+')).join(' | ')}`);
  for (const line of lines) {
    if (line.type !== 'user') continue;
    for (const block of Array.isArray(line.message?.content) ? line.message.content : []) {
      if (block.type !== 'tool_result') continue;
      console.log(`   tool_result keys: ${Object.keys(block).join(',')} | is_error: ${JSON.stringify(block.is_error)} | content: ${mask(JSON.stringify(block.content)).slice(0, 300)}`);
    }
  }
  console.log(`   result: subtype ${result.subtype} | num_turns ${result.num_turns} | duration_ms ${result.duration_ms} | duration_api_ms ${result.duration_api_ms} | total_cost_usd ${result.total_cost_usd} | permission_denials ${mask(JSON.stringify((result.permission_denials ?? []).map((d) => ({ tool_name: d.tool_name, tool_input: d.tool_input }))))}`);
  total += result.total_cost_usd ?? 0;
  console.log('   final reply, in full:');
  for (const row of mask(typeof result.result === 'string' ? result.result : '').split('\n')) console.log(`      | ${row}`);
}
console.log(`\ntotal_cost_usd added up over ${process.argv.length - 2} sessions: ${total.toFixed(4)}`);
