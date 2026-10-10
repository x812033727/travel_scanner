#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DOCS = path.join(ROOT, 'docs/videos/codex-practical-series');
export const sha256 = file => createHash('sha256').update(readFileSync(file)).digest('hex');
export function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).sort((a,b) => a.name.localeCompare(b.name)).flatMap(entry => {
    const file = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`Symlink not allowed: ${file}`);
    return entry.isDirectory() ? walk(file) : [file];
  });
}
export function checkCurriculum(base = DOCS) {
  const course = JSON.parse(readFileSync(path.join(base, 'curriculum.json'), 'utf8'));
  const errors = [];
  if (course.schema_version !== 1 || course.series_id !== 'codex-practical') errors.push('course identity');
  if (course.lessons?.length !== 18) errors.push('must contain exactly 18 lessons');
  const slugs = new Set();
  for (let index = 0; index < (course.lessons?.length ?? 0); index++) {
    const lesson = course.lessons[index];
    const number = String(index + 1).padStart(2, '0');
    if (lesson.number !== index + 1) errors.push(`lesson ${number}: order`);
    if (!lesson.title || !lesson.topic || !Array.isArray(lesson.outcomes) || lesson.outcomes.length < 2 || lesson.outcomes.length > 4 || lesson.outcomes.some(item => typeof item !== 'string' || !item.trim())) errors.push(`lesson ${number}: outcomes`);
    if (!lesson.challenge || lesson.materials !== `materials/lessons/${number}`) errors.push(`lesson ${number}: materials/challenge`);
    if (!Array.isArray(lesson.prerequisites) || lesson.prerequisites.some(n => !Number.isInteger(n) || n < 1 || n >= lesson.number)) errors.push(`lesson ${number}: prerequisites`);
    if (!Array.isArray(lesson.target_minutes) || lesson.target_minutes[0] < 12 || lesson.target_minutes[1] < lesson.target_minutes[0]) errors.push(`lesson ${number}: duration`);
    const spec = path.join(base, 'lessons', `${number}.md`);
    if (!existsSync(spec)) errors.push(`lesson ${number}: missing specification`);
    for (const surface of ['app', 'cli']) {
      const slug = lesson[`${surface}_slug`];
      if (slug !== `codex-practical-${number}-${surface}` || slugs.has(slug)) errors.push(`lesson ${number}: ${surface} identity`);
      slugs.add(slug);
      const brief = path.join(base, 'episodes', slug ?? '', 'brief.md');
      if (!existsSync(brief)) { errors.push(`${slug}: missing brief`); continue; }
      const text = readFileSync(brief, 'utf8');
      if (!text.includes('教學卡片') || !text.includes('驗收') || !text.includes('練習')) errors.push(`${slug}: teaching structure`);
      if (surface === 'app' && !/待.*(?:截圖|素材|操作)|pending_capture|未.*(?:截圖|觀察|實測)/u.test(text)) errors.push(`${slug}: capture evidence gate missing`);
    }
  }
  return { course, errors, lessons: course.lessons?.length ?? 0, episodes: slugs.size };
}

async function build(values) {
  if (!values.output || !values.python) throw new Error('build requires --output DIR --python EXE');
  const checked = checkCurriculum();
  if (checked.errors.length) throw new Error(checked.errors.join('\n'));
  const output = path.resolve(values.output);
  const relative = path.relative(ROOT, output);
  if (!(relative === '..' || relative.startsWith('..' + path.sep) || path.isAbsolute(relative))) throw new Error('Learner ZIPs and generated snapshots must be outside the Git checkout.');
  const delivery = path.join(output, 'delivery');
  mkdirSync(delivery, { recursive: true });
  const { materializeLesson } = await import('./labs.mjs');
  const packages = [];
  for (const lesson of checked.course.lessons) {
    const number = String(lesson.number).padStart(2, '0');
    const folder = path.join(output, 'materials/lessons', number);
    await materializeLesson(lesson.number, folder);
    for (const name of ['start', 'reference', 'challenge']) {
      if (!existsSync(path.join(folder, name, 'core.test.mjs'))) throw new Error(`Lesson ${number}: ${name} is not self-contained`);
    }
    for (const name of ['README.md', 'prompts.md', 'acceptance.md', 'answers.md']) {
      if (!existsSync(path.join(folder, name))) throw new Error(`Lesson ${number}: missing ${name}`);
    }
    const files = walk(folder).map(file => ({ path: path.relative(folder, file).replaceAll('\\', '/'), sha256: sha256(file) }));
    writeFileSync(path.join(folder, 'manifest.json'), JSON.stringify({ schema_version: 1, lesson: lesson.number,
      provenance: 'authored-reference-and-intentional-exercises; not model execution evidence', files }, null, 2) + '\n');
    const archive = path.join(delivery, `codex-practical-${number}-materials.zip`);
    const packed = spawnSync(values.python, [path.join(ROOT, 'tools/codex-practical/pack.py'), folder, archive], { encoding: 'utf8', windowsHide: true });
    if (packed.status !== 0) throw new Error(packed.stderr || 'ZIP creation failed');
    packages.push({ lesson: lesson.number, archive: path.basename(archive), sha256: sha256(archive), files: files.length });
  }
  const manifest = { schema_version: 1, series_id: 'codex-practical', lessons: 18, planned_episodes: 36,
    curriculum_sha256: sha256(path.join(DOCS, 'curriculum.json')), packages,
    media_status: 'not-inferred-from-materials', product_evidence_status: 'tracked-separately' };
  writeFileSync(path.join(delivery, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  mkdirSync(path.join(DOCS, 'evidence'), { recursive: true });
  writeFileSync(path.join(DOCS, 'evidence/packages.json'), JSON.stringify(manifest, null, 2) + '\n');
  console.log(JSON.stringify({ lessons: 18, episodes: 36, learner_packages: packages.length, output: delivery }));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const { values, positionals } = parseArgs({ allowPositionals: true, options: { output: { type:'string' }, python: { type:'string' } } });
  if (positionals[0] === 'build') await build(values);
  else if (positionals[0] === 'check') {
    const { errors, lessons, episodes } = checkCurriculum();
    console.log(JSON.stringify({ lessons, episodes, errors }, null, 2));
    process.exitCode = errors.length ? 1 : 0;
  } else throw new Error('Usage: node tools/codex-practical/course.mjs check|build [--output DIR --python EXE]');
}
