import { appendFileSync, existsSync } from 'node:fs';
import { readFileSync, readdirSync } from 'node:fs';
import { isAbsolute, join, relative } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const log = process.env.SKILL_LOG
  ?? join(root, '.claude', 'seen.log');
const dir = join(root, '.claude', 'skills');
const mine = existsSync(dir) ? readdirSync(dir) : [];

function skill(value) {
  const name = String(value ?? '').replace(/^\//, '');
  return mine.includes(name) ? name : '(not a project skill)';
}

function file(path) {
  const rel = relative(root, path ?? '').replaceAll('\\', '/');
  if (!rel || rel.startsWith('..') || isAbsolute(rel)) {
    return '(outside the project)';
  }
  return rel;
}

const kind = event.hook_event_name;
let line = kind;
if (kind === 'PreToolUse') {
  const input = event.tool_input ?? {};
  const name = input.skill ?? input.name ?? input.command;
  const keys = Object.keys(input).join(',');
  line += ` ${event.tool_name} ${skill(name)} keys=${keys}`;
} else if (kind === 'UserPromptExpansion') {
  const { expansion_type, command_name } = event;
  line += ` ${expansion_type} ${skill(command_name)}`;
  line += ` source=${event.command_source}`;
} else if (kind === 'InstructionsLoaded') {
  const { load_reason, memory_type, file_path } = event;
  line += ` ${load_reason} ${memory_type} ${file(file_path)}`;
}

appendFileSync(log, `${line}\n`);
