import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { decodeTasks, weeklyReport } from './core.mjs';
export function reportArguments(args) {
  const [input, ...options] = args; const result = { input, compact:false };
  if (!input || input.startsWith('--')) throw new Error('Usage: node report.mjs INPUT --from YYYY-MM-DD --to YYYY-MM-DD [--out NEWFILE] [--compact]');
  for (let i=0;i<options.length;i++) {
    const key = options[i].slice(2);
    if (options[i] === '--compact') {
      if (result.compact) throw new Error('Unknown or duplicate option');
      result.compact = true; continue;
    }
    if (!['from','to','out'].includes(key) || !options[i].startsWith('--') || result[key] !== undefined) throw new Error('Unknown or duplicate option');
    const value = options[++i];
    if (!value || value.startsWith('--')) throw new Error('Missing option value');
    result[key] = value;
  }
  if (!result.from || !result.to) throw new Error('Both --from and --to are required');
  return result;
}
export function formatReport(result, compact=false) { return JSON.stringify(result,null,compact?undefined:2)+'\n'; }
export function runReport(args) {
  const options = reportArguments(args);
  const tasks = decodeTasks(readFileSync(options.input, 'utf8'));
  const result = weeklyReport(tasks, options.from, options.to);
  if (options.out) writeFileSync(options.out, formatReport(result,options.compact), { flag:'wx' });
  return result;
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { const args=process.argv.slice(2); process.stdout.write(formatReport(runReport(args),reportArguments(args).compact)); }
  catch(error) { console.error(error.message); process.exitCode=1; }
}
