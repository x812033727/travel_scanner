import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, mkdtempSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { inflateRawSync } from 'node:zlib';
import { spawnSync } from 'node:child_process';
import { load as parseYaml } from 'js-yaml';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = relative => JSON.parse(readFileSync(path.join(root, relative), 'utf8'));
const catalogue = read('apps/api/app/guides/series_data/claude-code.json');
const expected = new Set([...catalogue.entries.map(entry => entry.slug), catalogue.hub]);

test('the tutorial catalogue keeps stable slugs, complete ordering and resolvable paths', () => {
  assert.equal(catalogue.entries.length, 96);
  assert.equal(expected.size, 97);
  assert.equal(catalogue.groups.length, 16);
  assert.equal(catalogue.paths.length, 12);
  assert.deepEqual(catalogue.entries.map(entry => entry.number), Array.from({ length: 96 }, (_, i) => i + 1));
  for (const entry of catalogue.entries) {
    assert.ok(catalogue.groups.some(group => group.id === entry.group));
    assert.ok(entry.related.length <= 3);
    for (const slug of [...entry.prerequisites, ...entry.related]) assert.ok(expected.has(slug) && slug !== entry.slug);
  }
  for (const route of catalogue.paths) for (const slug of route.slugs) assert.ok(expected.has(slug));
});

test('all 97 native packs exist with source dates, code labels and valid references', () => {
  const checks = read('docs/claude-code-series/source-checks.json');
  for (const slug of expected) {
    const pack = read(`apps/api/app/guides/content/${slug}.json`);
    assert.equal(pack.slug, slug);
    assert.equal(pack.kind, 'life');
    assert.deepEqual(Object.keys(pack.locales), ['zh-TW']);
    const doc = pack.locales['zh-TW'];
    assert.ok(doc.blocks.length >= 10);
    assert.ok(existsSync(path.join(root, 'apps/web/public', doc.hero.src)));
    for (const source of doc.sources) assert.ok(checks.some(check => check.url === source.url && check.checked_on === source.checked_on && check.status === 200));
    for (const block of doc.blocks) {
      if (block.type === 'code') assert.ok(block.label && block.code.endsWith('\n'));
      if (block.type === 'rich_paragraph') for (const node of block.inlines) {
        if (node.type === 'article') assert.ok(expected.has(node.slug), `${slug}: ${node.slug}`);
      }
    }
  }
});

// The authoring script uses ordinary deflated ZIP members without data descriptors.
// Exercise the actual downloadable archives, not a second copy of their model logic.
function extractArchive(name, destination) {
  const archive = readFileSync(path.join(root, `apps/web/public/tutorials/claude-code/${name}.zip`));
  let offset = 0;
  while (archive.readUInt32LE(offset) === 0x04034b50) {
    assert.equal(archive.readUInt16LE(offset + 6) & 8, 0);
    const method = archive.readUInt16LE(offset + 8);
    const size = archive.readUInt32LE(offset + 18);
    const nameLength = archive.readUInt16LE(offset + 26);
    const extraLength = archive.readUInt16LE(offset + 28);
    const filename = archive.subarray(offset + 30, offset + 30 + nameLength).toString('utf8');
    const start = offset + 30 + nameLength + extraLength;
    const target = path.resolve(destination, filename);
    assert.ok(target.startsWith(path.resolve(destination) + path.sep));
    mkdirSync(path.dirname(target), { recursive: true });
    const packed = archive.subarray(start, start + size);
    assert.ok(method === 0 || method === 8);
    writeFileSync(target, method === 8 ? inflateRawSync(packed) : packed);
    offset = start + size;
  }
}

for (const [name, expectedStatus] of [['starter', 0], ['complete', 0], ['bug-toggle', 1]]) {
  test(`downloadable ${name} has the documented test outcome`, () => {
    const directory = mkdtempSync(path.join(tmpdir(), 'mokaair-claude-lab-'));
    try {
      extractArchive(name, directory);
      const childEnv = { ...process.env };
      delete childEnv.NODE_TEST_CONTEXT;
      const result = spawnSync(process.execPath, ['--test', '--test-reporter=tap', 'tests/model.test.mjs'], {
        cwd: path.join(directory, name), env: childEnv, encoding: 'utf8', windowsHide: true, timeout: 20_000,
      });
      assert.equal(result.status, expectedStatus, result.stdout + result.stderr);
      assert.match(result.stdout, /# tests [46]/u);
      if (name === 'bug-toggle') assert.match(result.stdout, /not ok.*識別碼/u);
    } finally {
      const resolved = path.resolve(directory);
      assert.ok(resolved.startsWith(path.resolve(tmpdir()) + path.sep + 'mokaair-claude-lab-'));
      rmSync(resolved, { recursive: true });
    }
  });
}

const documentFor = number => read(`apps/api/app/guides/content/${catalogue.entries[number - 1].slug}.json`).locales['zh-TW'];
const codeFor = (number, filename) => documentFor(number).blocks.find(block => block.type === 'code' && block.language === 'javascript' && block.label.includes(filename))?.code;
function temporaryExercise(run) {
  const directory = mkdtempSync(path.join(tmpdir(), 'mokaair-claude-exercise-'));
  try { return run(directory); }
  finally {
    assert.ok(path.resolve(directory).startsWith(path.resolve(tmpdir()) + path.sep + 'mokaair-claude-exercise-'));
    rmSync(directory, { recursive: true });
  }
}

test('published JSON examples parse and JavaScript examples pass native syntax checking', () => temporaryExercise(directory => {
  let checked = 0;
  for (const slug of expected) {
    const blocks = read(`apps/api/app/guides/content/${slug}.json`).locales['zh-TW'].blocks;
    for (const block of blocks.filter(b => b.type === 'code')) {
      if (block.language === 'json') assert.doesNotThrow(() => JSON.parse(block.code), `${slug}: ${block.label}`);
      if (block.language === 'javascript') {
        const target = path.join(directory, 'example.mjs');
        writeFileSync(target, block.code);
        const result = spawnSync(process.execPath, ['--check', target], { encoding: 'utf8', windowsHide: true, timeout: 10000 });
        assert.equal(result.status, 0, `${slug}: ${block.label}: ${result.stderr}`);
        checked++;
      }
    }
  }
  assert.ok(checked >= 10);
}));

test('article filter and refactoring examples pass their own tests against the downloadable starter', () => temporaryExercise(directory => {
  extractArchive('starter', directory);
  const project = path.join(directory, 'starter');
  const model = path.join(project, 'model.js');
  writeFileSync(model, readFileSync(model, 'utf8') + '\n' + codeFor(33, 'model.js') + '\n' + codeFor(56, 'model.js'));
  writeFileSync(path.join(project, 'tests/filter.test.mjs'), codeFor(33, 'tests/filter.test.mjs'));
  writeFileSync(path.join(project, 'tests/count.test.mjs'), codeFor(56, 'tests/count.test.mjs'));
  writeFileSync(path.join(project, 'tests/toggle-missing.test.mjs'), codeFor(34, 'tests/toggle-missing.test.mjs'));
  writeFileSync(path.join(project, 'tests/integration.test.mjs'), `import test from 'node:test';
import assert from 'node:assert/strict';
import { addTodo, toggleTodo, countTodos } from '../model.js';
test('refactored count consumes actual starter data', () => {
  const items = addTodo(addTodo([], 'A', 'a'), 'B', 'b');
  assert.deepEqual(countTodos(toggleTodo(items, 'a')), {total: 2, completed: 1, active: 1});
});`);
  const env = { ...process.env }; delete env.NODE_TEST_CONTEXT;
  const result = spawnSync(process.execPath, ['--test', '--test-reporter=tap', 'tests/model.test.mjs', 'tests/filter.test.mjs', 'tests/count.test.mjs', 'tests/toggle-missing.test.mjs', 'tests/integration.test.mjs'], { cwd: project, env, encoding: 'utf8', windowsHide: true, timeout: 20000 });
  assert.equal(result.status, 0, result.stdout + result.stderr);
  assert.match(result.stdout, /# tests 8/u);
}));

test('actual authored Hook scripts handle success, malformed input, syntax errors and repeated Stop events', () => temporaryExercise(directory => {
  const run = (number, name, event) => {
    const target = path.join(directory, name);
    writeFileSync(target, codeFor(number, name));
    return spawnSync(process.execPath, [target], { cwd: directory, input: JSON.stringify(event), encoding: 'utf8', windowsHide: true, timeout: 10000 });
  };
  const event = { cwd: directory, hook_event_name: 'PostToolUse', tool_name: 'Edit' };
  assert.equal(run(41, 'log-edit.mjs', event).status, 0);
  const log = readFileSync(path.join(directory, '.claude/hook-events.jsonl'), 'utf8');
  assert.equal(JSON.parse(log.trim()).tool, 'Edit');
  assert.equal(run(41, 'log-edit.mjs', {}).status, 1);
  assert.equal(readFileSync(path.join(directory, '.claude/hook-events.jsonl'), 'utf8'), log);
  const file = path.join(directory, 'app.js');
  writeFileSync(file, 'const broken = (');
  const broken = run(42, 'check-js.mjs', { ...event, tool_input: { file_path: file } });
  assert.equal(broken.status, 0);
  assert.equal(JSON.parse(broken.stdout).hookSpecificOutput.hookEventName, 'PostToolUse');
  assert.match(JSON.parse(broken.stdout).hookSpecificOutput.additionalContext, /SyntaxError/u);
  writeFileSync(file, 'const valid = 1;');
  assert.equal(run(42, 'check-js.mjs', { ...event, tool_input: { file_path: file } }).stdout, '');
  assert.match(JSON.parse(run(42, 'remind-tests.mjs', { stop_hook_active: false }).stdout).systemMessage, /沒有執行測試/u);
  assert.equal(run(42, 'remind-tests.mjs', { stop_hook_active: true }).stdout, '');
}));

test('advanced TDD lesson reproduces the bug and the identical authored assertions pass on the reference', () => temporaryExercise(directory => {
  extractArchive('advanced/lesson-85', directory);
  const env = { ...process.env }; delete env.NODE_TEST_CONTEXT;
  for (const [variant, status] of [['starter', 1], ['reference', 0]]) {
    const project = path.join(directory, variant);
    for (const filename of ['tests/toggle-regression.test.mjs', 'tests/toggle-missing.test.mjs']) {
      const code = codeFor(85, filename); assert.ok(code);
      writeFileSync(path.join(project, filename), code);
    }
    const result = spawnSync(process.execPath, ['--test', 'tests/toggle-regression.test.mjs', 'tests/toggle-missing.test.mjs'], { cwd: project, env, encoding: 'utf8', windowsHide: true, timeout: 20000 });
    assert.equal(result.status, status, result.stdout + result.stderr);
  }
}));

test('all advanced archives contain the authored lesson and installed reference materials', () => {
  for (let number = 61; number <= 96; number++) temporaryExercise(directory => {
    extractArchive(`advanced/lesson-${number}`, directory);
    assert.equal(readFileSync(path.join(directory, 'article.md'), 'utf8'), readFileSync(path.join(root, `docs/claude-code-series/lessons/${number}.md`), 'utf8'));
    assert.equal(JSON.parse(readFileSync(path.join(directory, 'lesson.json'), 'utf8')).number, number);
    for (const variant of ['starter', 'reference']) assert.ok(existsSync(path.join(directory, variant, 'package-lock.json')));
    if (number === 87) for (const role of ['data-reviewer', 'ui-reviewer']) assert.ok(existsSync(path.join(directory, 'reference/.claude/agents', `${role}.md`)));
    if (number === 96) assert.match(readFileSync(path.join(directory, 'reference/app.js'), 'utf8'), /filterTodos/);
  });
});

test('tutorial CI workflow parses and isolates secrets from pull request inputs', () => {
  const workflow = parseYaml(readFileSync(path.join(root, 'tools/claude-code-series/advanced/lab/automation/ci/review.yml'), 'utf8'));
  assert.deepEqual(Object.keys(workflow.on).sort(), ['pull_request', 'workflow_dispatch']);
  assert.deepEqual(workflow.permissions, { contents: 'read' });
  assert.doesNotMatch(JSON.stringify(workflow.jobs.baseline), /secrets|pull_request_target/);
  const job = workflow.jobs['model-review'];
  assert.equal(job.environment, 'claude-lab');
  assert.match(job.if, /workflow_dispatch/);assert.match(job.if, /default_branch/);
  assert.equal(job.steps[0].with.ref, '${{ github.event.repository.default_branch }}');
  const action = job.steps.find(step => step.id === 'review');
  assert.equal(action.with.show_full_output, 'false');assert.equal(action.with.display_report, 'false');
  assert.match(action.with.claude_args, /--tools Read/);
  assert.equal(job.steps.at(-1).with.path, 'run-data/review.json');
  for (const step of job.steps.filter(step => step.uses)) assert.match(step.uses, /@[a-f0-9]{40}$/);
});

test('repository Claude validation is opt-in, pinned to the dispatched commit, and read-only', () => {
  const workflow = parseYaml(readFileSync(path.join(root, '.github/workflows/claude-tutorial-validation.yml'), 'utf8'));
  assert.deepEqual(Object.keys(workflow.on), ['workflow_dispatch']);
  assert.equal(workflow.on.workflow_dispatch.inputs.run_model.type, 'boolean');
  assert.equal(workflow.on.workflow_dispatch.inputs.run_model.default, false);
  assert.deepEqual(workflow.permissions, { contents: 'read' });
  assert.doesNotMatch(JSON.stringify(workflow.jobs.baseline), /secrets|ANTHROPIC_API_KEY/);
  const job = workflow.jobs['model-review'];
  assert.equal(job.environment, 'claude-lab');
  assert.equal(job.needs, 'baseline');
  assert.match(job.if, /inputs\.run_model &&.*workflow_dispatch.*default_branch/);
  for (const candidate of Object.values(workflow.jobs)) {
    assert.match(candidate.if, /default_branch/);
    assert.equal(candidate.steps[0].with.ref, '${{ github.sha }}');
    assert.equal(candidate.steps[0].with['persist-credentials'], false);
    for (const step of candidate.steps.filter(step => step.uses)) assert.match(step.uses, /@[a-f0-9]{40}$/);
  }
  const action = job.steps.find(step => step.id === 'review');
  assert.equal(action.with.classify_inline_comments, 'false');
  assert.equal(action.with.show_full_output, 'false');
  assert.equal(action.with.display_report, 'false');
  assert.match(action.with.claude_args, /--tools Read --allowedTools Read/);
  assert.match(action.with.claude_args, /--max-budget-usd 0\.50/);
  assert.match(action.with.claude_args, /--strict-mcp-config/);
  const save = job.steps.find(step => step.env?.REVIEW_JSON);
  assert.equal(save.env.REVIEW_JSON, '${{ steps.review.outputs.structured_output }}');
  assert.equal(save.run, 'node automation/ci/save-review.mjs');
  assert.equal(job.steps.at(-1).with.path, 'tools/claude-code-series/advanced/lab/run-data/review.json');
});
