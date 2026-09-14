import { realpathSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
export function parseInput(args, base = process.cwd()) {
  if (args.length !== 2 || args[0] !== '--file' || !args[1].trim()) throw new Error('用法：--file <練習 diff 檔>');
  const root = realpathSync(base);
  const target = path.resolve(root,args[1]);
  if (!existsSync(target)) throw new Error('找不到檔案');
  const resolved = realpathSync(target);
  if (!statSync(resolved).isFile()) throw new Error('必須是檔案，不能是資料夾');
  const relative = path.relative(root,resolved);
  if (!relative || relative === '..' || relative.startsWith('..'+path.sep) || path.isAbsolute(relative)) throw new Error('檔案必須位於本練習目錄');
  if (path.extname(resolved) !== '.diff') throw new Error('只接受 .diff');
  return {file:resolved,relative};
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { console.log(JSON.stringify(parseInput(process.argv.slice(2)))); }
  catch(error) { console.error(error.message); process.exitCode=2; }
}
