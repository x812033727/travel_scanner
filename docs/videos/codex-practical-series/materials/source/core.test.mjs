import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { addTask, toggleTask, removeTask, visibleTasks, decodeTasks, encodeTasks, documentFrom,
  decodeCsv, encodeCsv, importCsv, importJson, weeklyReport, archiveTasks, restoreTasks } from './core.mjs';
const fixture = name => readFileSync(new URL('./fixtures/' + name, import.meta.url), 'utf8');
const tasks = decodeTasks(fixture('tasks.json'));
const frozen = value => Object.freeze(value.map(task => Object.freeze({ ...task })));
test('same title has separate identities; requested toggle/delete only', () => {
  const input = addTask(addTask([], 'Read', 'a'), 'Read', 'b');
  assert.deepEqual(removeTask(input, 'a').map(task => task.id), ['b']);
  const changed = toggleTask(input, 'b', '2026-10-05T02:00:00.000Z');
  assert.equal(changed[0].completed, false); assert.equal(changed[1].completed, true);
  assert.equal(input[1].completed, false);
  assert.equal(toggleTask(changed, 'b', '2026-10-06T02:00:00.000Z')[1].completedAt, null);
});
test('filters/search preserve order and frozen input, including empty and Unicode', () => {
  const input = frozen(tasks);
  assert.deepEqual(visibleTasks(input, 'completed', '  READ ').map(task => task.id), ['old', 'week-a']);
  assert.deepEqual(visibleTasks(input, 'all').map(task => task.id), tasks.map(task => task.id));
  assert.deepEqual(visibleTasks(input, 'all', '週報').map(task => task.id), ['boundary']);
  for (const filter of ['all','active','completed']) assert.deepEqual(visibleTasks([], filter), []);
  assert.deepEqual(input, tasks);
});
test('title constraints and duplicate identity validation', () => {
  assert.throws(() => addTask([], '  ', 'x')); assert.throws(() => addTask([], 'x'.repeat(101), 'x'));
  assert.throws(() => addTask(tasks, 'Unique title', 'old'));
  assert.equal(addTask([], '  中文 ✨  ', 'u')[0].title, '中文 ✨');
});
test('storage roundtrip and damaged storage never rewrite the supplied source', () => {
  assert.deepEqual(decodeTasks(encodeTasks(tasks)), tasks); assert.deepEqual(decodeTasks(null), []);
  const damaged = '{"version":2,"tasks":[';
  assert.throws(() => decodeTasks(damaged)); assert.equal(damaged, '{"version":2,"tasks":[');
  for (const value of [{version:3,tasks:[]}, {version:2,tasks:[...tasks,tasks[0]]},
    {version:2,tasks:[{...tasks[0],completedAt:'2026-02-30T01:00:00.000Z'}]},
    {version:2,tasks:[{...tasks[3],completedAt:'2026-10-05T02:00:00.000Z'}]}]) assert.throws(() => documentFrom(value));
});
test('v1 migration never invents completion dates', () => {
  const input = fixture('legacy-v1.json'); const migrated = decodeTasks(input);
  assert.equal(migrated[0].completed, true); assert.equal(migrated[0].completedAt, null);
  assert.equal(migrated[1].completedAt, null); assert.equal(JSON.parse(encodeTasks(migrated)).version, 2);
  assert.deepEqual(archiveTasks(migrated, '2026-10-11T15:59:59.999Z').archived, []);
});
test('CSV preserves quoted CRLF/LF, comma, quote, Unicode; accepts BOM and CRLF rows', () => {
  assert.deepEqual(decodeCsv(fixture('tasks.csv')), tasks);
  const input = [{id:'crlf', title:'林, "Alex"\r\n週報',completed:false,completedAt:null},
    {id:'lf', title:'Line1\nLine2',completed:false,completedAt:null}];
  assert.deepEqual(decodeCsv(encodeCsv(input)), input);
  const windows = '\uFEFFid,title,completed,completedAt\r\ncrlf,"林, ""Alex""\r\n週報",false,\r\nlf,"Line1\nLine2",false,\r\n';
  assert.deepEqual(decodeCsv(windows), input);
  assert.deepEqual(decodeCsv('id,title,completed,completedAt\n'), []);
  assert.deepEqual(decodeCsv('\uFEFFid,title,completed,completedAt\r\n'), []);
  assert.throws(() => decodeCsv('id,title,completed,completedAt\rx,title,false,\r'));
});
test('invalid JSON/CSV import rejects the entire batch and retains existing data', () => {
  const input = frozen(tasks); const original = encodeTasks(input);
  for (const raw of [fixture('invalid.csv'), 'id,title,completed,completedAt\nx,title,maybe,\n',
    'id,title,completed,completedAt\nx,"unclosed,false,\n', 'id,title,completed,completedAt\nx,"ok"bad,false,\n',
    'id,title,completed,completedAt\nx,title,false,,extra\n', fixture('tasks.csv')]) assert.throws(() => importCsv(input, raw));
  for (const raw of ['bad-json', fixture('tasks.json'), '{"version":2,"tasks":[{"id":"new","title":"","completed":false,"completedAt":null}]}']) assert.throws(() => importJson(input, raw));
  assert.equal(encodeTasks(input), original);
  assert.equal(importJson(input, '{"version":2,"tasks":[{"id":"new","title":"Read","completed":false,"completedAt":null}]}').length, 6);
});
test('known weekly truth uses inclusive Asia/Taipei days, not UTC date substrings', () => {
  assert.deepEqual(weeklyReport(tasks, '2026-10-05', '2026-10-11'), JSON.parse(fixture('truth.json')));
  assert.equal(weeklyReport(tasks, '2026-10-11', '2026-10-11').completedInWeek, 1);
  assert.equal(weeklyReport(tasks, '2026-10-10', '2026-10-10').completedInWeek, 0);
  assert.throws(() => weeklyReport(tasks, '2026-02-30', '2026-03-01'));
  assert.throws(() => weeklyReport(tasks, '2026-10-11', '2026-10-05'));
});
test('archive includes known completed <= cutoff; preserves unknown/pending and restores backup', () => {
  const input = frozen(tasks); const backup = encodeTasks(input);
  const result = archiveTasks(input, '2026-10-03T08:00:00.000Z');
  assert.deepEqual(result.archived.map(task => task.id), ['old']);
  assert.deepEqual(result.retained.map(task => task.id), ['week-a','boundary','pending','unknown']);
  assert.deepEqual(restoreTasks(backup), tasks); assert.equal(encodeTasks(input), backup);
  assert.throws(() => archiveTasks(input, '2026-10-03'));
});
