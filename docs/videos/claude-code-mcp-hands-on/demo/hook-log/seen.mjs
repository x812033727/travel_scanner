// 記錄用的 hook：每個事件寫一行，不擋任何東西。
import { appendFileSync, existsSync, readFileSync }
  from 'node:fs';
import { isAbsolute, join, relative } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const log = process.env.SEEN_LOG
  ?? join(root, '.claude', 'seen.txt');

// 這個專案自己接的伺服器：.mcp.json 裡的名稱
const config = join(root, '.mcp.json');
const mine = existsSync(config)
  ? Object.keys(JSON.parse(readFileSync(config, 'utf8'))
    .mcpServers ?? {})
  : [];

const tool = String(event.tool_name ?? '');
const server = (tool.match(/^mcp__(.+?)__/) ?? [])[1];
const ours = !server || mine.includes(server);
const input = event.tool_input ?? {};
const kind = event.hook_event_name;
const short = (value) => String(value ?? '')
  .replaceAll(root, '<lab>').replaceAll('\n', ' ').slice(0, 80);

function where(path) {
  if (!path) return '';
  const rel = relative(root, path).replaceAll('\\', '/') || '.';
  const out = rel.startsWith('..') || isAbsolute(rel);
  return out ? ' (outside the project)' : ` ${rel}`;
}

let line = `${kind} ${ours ? tool : 'mcp__(another server)'}`;
if (event.mcp_server) {
  line += ` source=${ours ? event.mcp_server.source : '-'}`;
}
if (kind === 'PreToolUse' && server && ours) {
  line += ` ${JSON.stringify(input)}`;
} else if (kind === 'PreToolUse' && tool === 'ToolSearch') {
  line += ` query=${short(input.query)}`;
} else if (kind === 'PreToolUse') {
  line += where(input.file_path ?? input.path);
} else if (kind === 'PostToolUse') {
  const size = JSON.stringify(event.tool_response ?? '').length;
  line += ` response_chars=${size}`;
} else if (kind === 'PostToolUseFailure') {
  line += ` error=${ours ? short(event.error) : '-'}`;
} else if (kind === 'PermissionDenied') {
  line += ` reason=${short(event.reason)}`;
} else if (kind === 'InstructionsLoaded') {
  line += `${event.load_reason} ${event.memory_type}`;
  line += where(event.file_path);
}

appendFileSync(log, `${line}\n`);
