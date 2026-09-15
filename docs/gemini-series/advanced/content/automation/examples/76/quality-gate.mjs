/** A deliberately narrow BeforeTool gate for a disposable documentation project. */
import { existsSync, lstatSync, readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';

function decide(event) {
  if (event.hook_event_name !== 'BeforeTool' || event.tool_name !== 'write_file') {
    return { decision: 'deny', reason: 'Unexpected event or tool; check the hook matcher.' };
  }
  const input = event.tool_input;
  if (!input || typeof input.file_path !== 'string' || typeof input.content !== 'string') {
    return { decision: 'deny', reason: 'file_path and content must be strings.' };
  }
  const root = realpathSync(event.cwd);
  const documents = path.join(root, 'docs');
  const file = path.resolve(root, input.file_path);
  const relative = path.relative(root, file).split(path.sep).join('/');
  if (!/^docs\/[a-z0-9-]+\.md$/.test(relative) ||
      realpathSync(documents) !== documents ||
      realpathSync(path.dirname(file)) !== documents ||
      (existsSync(file) && lstatSync(file).isSymbolicLink())) {
    return { decision: 'deny', reason: 'Only direct docs/*.md lesson files may be written.' };
  }
  const issues = [];
  if (!/^# [^\r\n]+$/m.test(input.content)) issues.push('missing_title');
  if (!/^## 來源\s*$/m.test(input.content)) issues.push('missing_sources');
  if (/\bTODO\b/.test(input.content)) issues.push('unfinished_todo');
  return issues.length ? { decision: 'deny', reason: issues.join(', ') } : { decision: 'allow' };
}

try {
  const event = JSON.parse(readFileSync(0, 'utf8'));
  process.stdout.write(JSON.stringify(decide(event)) + '\n');
} catch {
  process.stderr.write('quality-gate: invalid event or inaccessible lesson path\n');
  process.exitCode = 2;
}
