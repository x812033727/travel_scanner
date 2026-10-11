// 專案自己的記錄 hook：每個事件寫一行，不擋、不回任何決定。
// 不是這次種子的 skill、agent 與專案外的路徑，只寫成代稱。
import { appendFileSync, readFileSync } from 'node:fs';
import { isAbsolute, join, relative } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const kit = process.env.KIT_DIR ?? '';
const log = process.env.SEEN_LOG
  ?? join(root, '.claude', 'seen.txt');
const BUILT_IN = ['Explore', 'Plan', 'general-purpose',
  'claude', 'statusline-setup', 'claude-code-guide'];

const skill = (value) => {
  const name = String(value ?? '').replace(/^\//, '');
  return /^(ship-kit:)?release-prep$/.test(name)
    ? name : '(another skill)';
};
const agent = (value) => {
  const name = String(value ?? '');
  if (!name) return '(no type)';
  const ours = /^(ship-kit:)?log-scout$/.test(name);
  return ours || BUILT_IN.includes(name)
    ? name : '(another agent)';
};
const inside = (base, path) => {
  const rel = relative(base, path).replaceAll('\\', '/') || '.';
  return rel.startsWith('..') || isAbsolute(rel) ? null : rel;
};
function where(path) {
  if (!path) return '-';
  const here = inside(root, path);
  if (here !== null) return here;
  const there = kit ? inside(kit, path) : null;
  return there === null
    ? '(outside the project)' : `<plugin>/${there}`;
}
const cut = (text, most = 90) => {
  let shown = String(text ?? '');
  const hide = [[root, '<lab>'], [kit, '<plugin>']];
  for (const [base, mark] of hide) {
    if (!base) continue;
    const forms = [base, base.replaceAll('\\', '/'),
      base.replaceAll('\\', '\\\\')];
    for (const each of forms) {
      shown = shown.split(each).join(mark);
    }
  }
  return shown.replaceAll('\n', ' ⏎ ').slice(0, most);
};

const kind = event.hook_event_name;
const tool = String(event.tool_name ?? '');
const input = event.tool_input ?? {};
const by = event.agent_id ? agent(event.agent_type) : 'main';
const id = String(event.tool_use_id ?? '').slice(-4) || '----';
const ours = !tool.startsWith('mcp__');
let line = `${kind} by=${by.replaceAll(' ', '_')} id=${id}`;
if (!ours) {
  line += ' mcp__(a server)';
} else if (tool === 'Skill') {
  line += ` Skill skill=${skill(input.skill ?? input.name)}`;
  line += ` keys=${Object.keys(input).join(',')}`;
} else if (tool === 'Agent' || tool === 'Task') {
  line += ` ${tool} type=${agent(input.subagent_type)}`;
  line += ` background=${input.run_in_background ?? '-'}`;
  line += ` prompt_chars=${String(input.prompt ?? '').length}`;
} else if (tool) {
  const path = input.file_path ?? input.path;
  const what = path ? where(path) : cut(input.pattern, 40);
  line += ` ${tool} ${what}`;
}
if (kind === 'PostToolUse') {
  const out = event.tool_response ?? {};
  line += ` | status=${out.status ?? '-'}`;
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
  line += ` name=${skill(event.command_name)}`;
  line += ` source=${event.command_source}`;
} else if (kind === 'InstructionsLoaded') {
  line = `${kind} ${event.load_reason} ${event.memory_type}`;
  line += ` ${where(event.file_path)}`;
}

appendFileSync(log, `${line}\n`);
