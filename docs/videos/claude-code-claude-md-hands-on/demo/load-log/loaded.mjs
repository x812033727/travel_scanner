import { appendFileSync, readFileSync } from 'node:fs';
import { isAbsolute, join, relative } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const log = process.env.LOAD_LOG
  ?? join(root, '.claude', 'loaded.log');

function name(file) {
  const rel = relative(root, file).replaceAll('\\', '/');
  if (!rel || rel.startsWith('..') || isAbsolute(rel)) {
    return '(outside the project)';
  }
  return rel;
}

const { load_reason, memory_type, file_path } = event;
const from = event.trigger_file_path;
const line = [load_reason, memory_type, name(file_path),
  from ? `<- ${name(from)}` : ''].join(' ').trim();

appendFileSync(log, `${line}\n`);
console.log(line);
