import { appendFileSync, existsSync } from 'node:fs';
import { readFileSync, readdirSync } from 'node:fs';
import { isAbsolute, join, relative } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const log = process.env.SEEN_LOG
  ?? join(root, '.claude', 'seen.log');
const dir = join(root, '.claude', 'agents');
const files = existsSync(dir) ? readdirSync(dir) : [];
const mine = files.map((name) => name.replace(/\.md$/, ''));
const BUILT_IN = ['Explore', 'Plan', 'general-purpose',
  'claude', 'statusline-setup', 'claude-code-guide'];
const MARK = '【trip-queue】';

function agent(value) {
  const name = String(value ?? '');
  if (!name) return '(no type)';
  const known = mine.includes(name) || BUILT_IN.includes(name);
  return known ? name : '(another agent)';
}

function file(path) {
  if (!path) return '-';
  const rel = relative(root, path).replaceAll('\\', '/') || '.';
  if (rel.startsWith('..') || isAbsolute(rel)) {
    return '(outside the project)';
  }
  return rel;
}

const marked = (text) => (String(text ?? '').includes(MARK)
  ? 'yes' : 'no');
const kind = event.hook_event_name;
const by = event.agent_id ? agent(event.agent_type) : 'main';
const input = event.tool_input ?? {};
const spawns = ['Agent', 'Task'].includes(event.tool_name);
let line = `${kind} by=${by}`;
if (kind === 'PreToolUse' && spawns) {
  const type = agent(input.subagent_type);
  line += ` ${event.tool_name} type=${type}`;
  line += ` keys=${Object.keys(input).join(',')}`;
  line += ` model=${input.model ?? '-'}`;
  line += ` background=${input.run_in_background ?? '-'}`;
  line += ` prompt_chars=${String(input.prompt ?? '').length}`;
  line += ` mark_in_prompt=${marked(input.prompt)}`;
} else if (kind === 'PreToolUse') {
  const path = input.file_path ?? input.path;
  line += ` ${event.tool_name} ${file(path)}`;
} else if (kind === 'PostToolUse') {
  const out = event.tool_response ?? {};
  line += ` ${event.tool_name} status=${out.status ?? '-'}`;
  line += ` model=${out.resolvedModel ?? '-'}`;
  line += ` last_request_tokens=${out.totalTokens ?? '-'}`;
  line += ` tool_calls=${out.totalToolUseCount ?? '-'}`;
  line += ` keys=${Object.keys(out).join(',')}`;
} else if (kind === 'SubagentStart') {
  line = `${kind} agent=${agent(event.agent_type)}`;
} else if (kind === 'SubagentStop') {
  const last = event.last_assistant_message;
  line = `${kind} agent=${agent(event.agent_type)}`;
  line += ` last_chars=${String(last ?? '').length}`;
  line += ` mark_in_last=${marked(last)}`;
} else if (kind === 'InstructionsLoaded') {
  const { load_reason, memory_type, file_path } = event;
  line += ` ${load_reason} ${memory_type} ${file(file_path)}`;
}

appendFileSync(log, `${line}\n`);
