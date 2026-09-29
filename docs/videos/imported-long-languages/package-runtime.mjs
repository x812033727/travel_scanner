// Freeze the already-tested tool code beside the prepared adapter for an isolated host job.
// Media and credentials are never added to the public repository or the code receipt.
import { createHash } from 'node:crypto';
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../..');
const { values } = parseArgs({ options: { manifest: { type: 'string' } }, strict: true });
if (!values.manifest) throw new Error('--manifest is required');
const base = path.dirname(path.resolve(values.manifest));
const manifest = JSON.parse(readFileSync(values.manifest, 'utf8'));
const root = path.resolve(base, manifest.root);
if (!root.startsWith(base + path.sep) || root === repo) throw new Error('Expected an isolated prepared root inside the batch');
const code = path.join(root, 'docs/videos/imported-long-languages');
const destinations = [path.join(root, 'tools/video'), path.join(root, '.agents/skills/youtube-video'), code];
if (destinations.some(existsSync)) throw new Error('Runtime already exists; inspect/resume it instead of overwriting');
cpSync(path.join(repo, 'tools/video'), destinations[0], { recursive: true, force: false, errorOnExist: true });
cpSync(path.join(repo, '.agents/skills/youtube-video'), destinations[1], { recursive: true, force: false, errorOnExist: true });
mkdirSync(code, { recursive: true });
for (const name of ['runner.mjs', 'prepare.mjs', 'preflight.mjs']) {
  cpSync(path.join(here, name), path.join(code, name), { force: false, errorOnExist: true });
}
const files = [];
function collect(dir) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) collect(file);
    else if (entry.isFile()) files.push({ path: path.relative(base, file).replaceAll('\\', '/'), sha256: createHash('sha256').update(readFileSync(file)).digest('hex') });
    else throw new Error(`Unexpected non-file entry: ${file}`);
  }
}
destinations.forEach(collect);
writeFileSync(path.join(base, 'runtime-receipt.json'), JSON.stringify({ created_at: new Date().toISOString(), node: process.version, files }, null, 2) + '\n');
console.log(JSON.stringify({ runtime_files: files.length, root, node: process.version }));
