// Independent, read-only probe of the actual checkChapter function body.
// No model, host, source file or paid operation is invoked.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const workerFile = path.resolve(here, '../../../../../tools/video/automation/story.mjs');
const workerSource = fs.readFileSync(workerFile, 'utf8');
const start = workerSource.indexOf('async function checkChapter(');
const end = workerSource.indexOf('/** A line the listener', start);
assert.ok(start >= 0 && end > start, 'read the actual worker function');
const checkChapterSource = workerSource.slice(start, end);

async function runAt(priorRounds) {
  const chapter = { key: 'hook', title: 'Hook', scenes: [{ id: 'hook-01',
    lines: [{ id: 'line-01', text: 'Example.' }] }], claims: [] };
  const entry = { written: true, checked: false, listened: false,
    check_rounds: priorRounds, lint: null };
  const state = { slug: 'story-rolling-suitcase-v2', story: { chapters: {
    hook: entry, origin: { checked: false }, idea: { checked: false },
    engine: { checked: false }, turn: { checked: false }, now: { checked: false },
  } } };
  let askedRound = null;
  const context = {
    seriesInfo: () => ({ plan: { sources: [], chapters: [{ point: 'point' }],
      must_verify: [], names: [] }, title: 'Title' }),
    entryOf: (_state, key) => _state.story.chapters[key],
    CHAPTER_OF: new Map([['hook', { index: 0 }]]),
    readChapter: () => chapter,
    factChapters: () => [],
    chapterNarration: () => [],
    anchorsFor: () => [],
    factsPayload: () => [],
    sourcesPayload: async () => [],
    checkerSourceOrder: () => [],
    CHECKER_TOKENS: 1,
    STORY_VARIANT: 'story',
    isObject: (value) => value !== null && typeof value === 'object',
    applyPatch: () => ({ chapter, changed: [], dropped: [], refused: [] }),
    checkedRows: () => Array.from({ length: 4 }, (_, index) => ({
      id: `c${index}`, verdict: 'CHANGED' })),
    COUNTED: new Set(['CHANGED', 'ATTRIBUTED', 'NOT FOUND']),
    saveChapter: () => {},
    relint: async () => ({ other: [] }),
    CHANGED_FACTS_RECHECK: 3,
    CHAPTER_KEYS: ['hook', 'origin', 'idea', 'engine', 'turn', 'now'],
    VERDICTS: ['CONFIRMED', 'PLAN', 'CHANGED', 'ATTRIBUTED', 'NOT FOUND',
      'OUT OF SCOPE'],
    isText: (value) => typeof value === 'string' && value.length > 0,
  };
  const actualCheckChapter = vm.runInNewContext(`${checkChapterSource}\ncheckChapter`,
    context, { filename: workerFile });
  const automation = { ctx: { now: () => new Date('2026-10-17T00:00:00Z') },
    settings: { max_verify_rounds: 3 },
    stage: async (_kind, _slug, payload) => { askedRound = payload.round;
      return { claims: [], patch: {}, drop: [], report: 'Four changed facts.' }; },
    cleared: () => {}, persist: () => {}, retryLater: () => { throw Error('unexpected retry'); },
  };
  await actualCheckChapter(automation, state, 'hook');
  return { askedRound, checked: entry.checked, changed: entry.changed };
}

test('actual worker cap accepts four changed facts when old check_rounds=2', async () => {
  assert.deepEqual(await runAt(2), { askedRound: 3, checked: true, changed: 4 });
  assert.deepEqual(await runAt(0), { askedRound: 1, checked: false, changed: 4 });
});
