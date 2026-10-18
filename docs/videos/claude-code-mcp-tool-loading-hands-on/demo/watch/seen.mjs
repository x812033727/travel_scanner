// 專案自己的記錄 hook：每個事件寫一行，不印任何東西。
// skill、agent、別的 MCP 伺服器與專案外的路徑只寫成代稱。
// 唯一會擋的一種：檔案工具（Read、Edit、Write、Glob、Grep）
// 指到專案以外的地方。那一筆寫 BLOCKED、結束碼 2，
// 在權限規則之前就停下來。
import { appendFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { isAbsolute, join, relative, resolve } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const from = event.cwd ?? root;
const log = process.env.SEEN_LOG
  ?? join(root, '.claude', 'seen.txt');
const BUILT_IN = ['Explore', 'Plan', 'general-purpose',
  'claude', 'statusline-setup', 'claude-code-guide'];
const FILE_TOOLS = ['Read', 'Edit', 'Write', 'NotebookEdit',
  'Glob', 'Grep'];
const OUT = '(outside the project)';
const OUT_TEMP = '(outside the project, in the temp folder)';

const agent = (value) => {
  const name = String(value ?? '');
  if (!name) return '(no type)';
  return BUILT_IN.includes(name) ? name : '(another agent)';
};
const inside = (base, path) => {
  const rel = relative(base, path).replaceAll('\\', '/') || '.';
  return rel.startsWith('..') || isAbsolute(rel) ? null : rel;
};
// Git Bash 的 /c/... 寫法在 Windows 上換成 C:/...
const native = (path) => (process.platform === 'win32'
  ? String(path).replace(/^\/([A-Za-z])\//, '$1:/')
  : String(path));
function where(path) {
  if (!path) return '-';
  if (String(path).startsWith('~')) return OUT;
  const at = resolve(from, native(path));
  const here = inside(root, at);
  if (here !== null) return here;
  return inside(tmpdir(), at) === null ? OUT : OUT_TEMP;
}
const cut = (text, most = 90) => {
  let shown = String(text ?? '');
  const forms = [root, root.replaceAll('\\', '/'),
    root.replaceAll('\\', '\\\\')];
  for (const each of forms) shown = shown.split(each).join('<lab>');
  // 別的 MCP 伺服器的工具名稱不留。
  shown = shown.replace(/mcp__(?!gear__)[\w-]+/g, 'mcp__(other)');
  return shown.replaceAll('\n', ' ⏎ ').slice(0, most);
};
// 檔案工具指到哪裡：路徑參數，或 Glob 的樣式、Grep 的 glob
// 開頭寫死的那一段（磁碟代號、/、~、.. 開頭才看）。
// Grep 的 pattern 是正規表示式，不是路徑，不看。
const ROOTED = /^([A-Za-z]:|[\\/]|~|\.\.([\\/]|$))/;
function aim(tool, input) {
  const path = input.file_path ?? input.notebook_path
    ?? input.path;
  const spot = path ? where(path) : null;
  if (spot && spot.startsWith('(outside')) return spot;
  const glob = tool === 'Glob' ? input.pattern
    : tool === 'Grep' ? input.glob : null;
  if (glob && ROOTED.test(String(glob))) {
    const stem = String(glob).split(/[*?[{]/)[0] || '.';
    const there = where(stem);
    if (there.startsWith('(outside')) return there;
  }
  return spot;
}

const kind = event.hook_event_name;
const tool = String(event.tool_name ?? '');
const input = event.tool_input ?? {};
const by = event.agent_id ? agent(event.agent_type) : 'main';
const id = String(event.tool_use_id ?? '').slice(-4) || '----';
const mcp = tool.startsWith('mcp__');
let blocked = false;
let line = `${kind} by=${by.replaceAll(' ', '_')} id=${id}`;
if (mcp && !tool.startsWith('mcp__gear__')) {
  line += ' mcp__(a server)';
} else if (mcp) {
  line += ` ${tool} ${cut(JSON.stringify(input), 60)}`;
} else if (tool === 'Skill') {
  line += ' Skill skill=(a skill)';
} else if (tool === 'Agent' || tool === 'Task') {
  line += ` ${tool} type=${agent(input.subagent_type)}`;
  line += ` prompt_chars=${String(input.prompt ?? '').length}`;
} else if (tool === 'ToolSearch') {
  line += ` ToolSearch query=${cut(input.query, 60)}`;
  line += ` max_results=${input.max_results ?? '-'}`;
} else if (tool) {
  const spot = aim(tool, input);
  const out = Boolean(spot) && spot.startsWith('(outside');
  blocked = out && kind === 'PreToolUse'
    && FILE_TOOLS.includes(tool);
  line += ` ${tool} ${spot ?? cut(input.pattern, 40)}`;
}
if (kind === 'PostToolUse') {
  const out = event.tool_response ?? {};
  const size = JSON.stringify(out).length;
  line += ` | response_chars=${size}`;
} else if (kind === 'PostToolUseFailure') {
  line += ` | error=${cut(event.error)}`;
} else if (kind === 'PermissionRequest') {
  const offered = event.permission_suggestions ?? [];
  line += ` | mode=${event.permission_mode}`;
  line += ` suggestions=${offered.length}`;
} else if (kind.startsWith('Subagent')) {
  line = `${kind} agent=${agent(event.agent_type)}`;
} else if (kind === 'UserPromptExpansion') {
  line = `${kind} ${event.expansion_type}`;
} else if (kind === 'InstructionsLoaded') {
  line = `${kind} ${event.load_reason} ${event.memory_type}`;
  line += ` ${where(event.file_path)}`;
}
if (blocked) line += ' | BLOCKED';

appendFileSync(log, `${line}\n`);
if (blocked) {
  // 這一行會交給 Claude；不帶任何路徑。
  console.error('Blocked by the project\'s logging hook: file tools'
    + ' may only touch files inside this project.');
  process.exitCode = 2;
}
