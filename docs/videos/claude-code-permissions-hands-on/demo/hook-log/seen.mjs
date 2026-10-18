// 記錄用的 hook：每個事件寫一行，不擋任何東西，也不回任何決定。
import { appendFileSync, readFileSync } from 'node:fs';
import { isAbsolute, join, relative } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const log = process.env.SEEN_LOG
  ?? join(root, '.claude', 'seen.txt');

const kind = event.hook_event_name;
const tool = String(event.tool_name ?? '');
const input = event.tool_input ?? {};
const ours = !tool.startsWith('mcp__');
const spellings = [root, root.replaceAll('\\', '/'),
  root.replaceAll('\\', '\\\\')];
const short = (value, most = 100) => {
  let text = String(value ?? '');
  for (const each of spellings) {
    text = text.split(each).join('<lab>');
  }
  return text.replaceAll('\n', ' ⏎ ').slice(0, most);
};

// 檔案工具：只寫專案裡的相對路徑；專案以外的不寫路徑。
function where(path) {
  if (!path) return '';
  const rel = relative(root, path).replaceAll('\\', '/') || '.';
  const out = rel.startsWith('..') || isAbsolute(rel);
  return out ? '(outside the project)' : rel;
}

function target() {
  if (!ours) return '';
  if (tool === 'Bash') return short(input.command);
  if (tool === 'Grep' || tool === 'Glob') {
    const dir = input.path ? ` in ${where(input.path)}` : '';
    return `${short(input.pattern, 60)}${dir}`;
  }
  return where(input.file_path ?? input.path);
}

const id = String(event.tool_use_id ?? '').slice(-4) || '----';
let line = `${kind} ${ours ? tool : 'mcp__(a server)'}`;
if (kind === 'InstructionsLoaded') {
  line += `${event.load_reason} ${event.memory_type} `;
  line += where(event.file_path);
} else {
  line += ` id=${id} ${target()}`;
}
if (kind === 'PermissionRequest') {
  const offered = event.permission_suggestions ?? [];
  const rule = offered[0]?.rules?.[0];
  line += ` | mode=${event.permission_mode}`;
  line += ` | suggestions=${offered.length}`;
  if (rule && ours) {
    const content = short(rule.ruleContent, 60);
    line += ` first=${rule.toolName}(${content})`;
  }
} else if (kind === 'PostToolUse') {
  const size = JSON.stringify(event.tool_response ?? '').length;
  line += ` | response_chars=${size}`;
} else if (kind === 'PostToolUseFailure') {
  line += ` | error=${ours ? short(event.error, 90) : '-'}`;
} else if (kind === 'PermissionDenied') {
  line += ` | reason=${short(event.reason, 90)}`;
}

appendFileSync(log, `${line}\n`);
