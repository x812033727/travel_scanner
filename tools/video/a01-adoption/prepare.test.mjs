import assert from 'node:assert/strict';
import test from 'node:test';
import { chapterHeading, reviewedChapterLoops } from './prepare.mjs';

test('r23 section headings replace all six distinct 104 chapter titles', () => {
  const rows = [
    ['hook', '他看見重機器被輕鬆推走', '兩只沉箱旁的意外'],
    ['origin', '輪子箱跟著一家人出發', '安妮塔出發前的難題'],
    ['idea', '樣品被退回後拿到訂單', '機場裡的兩只沉箱'],
    ['engine', '旅客提著箱子走過航站', '樣品走進百貨辦公室'],
    ['turn', '機師把推車和箱子合在一起', '機師的兩道難題'],
    ['now', '箱子站著轉向，仍有需要提起的時候', '箱子走出車庫之後'],
  ];
  for (const [key, oldTitle, r23Title] of rows) {
    const newTitle = chapterHeading(key, [
      { id: `${key}-first`, chapter: r23Title },
      { id: `${key}-second` },
    ]);
    assert.equal(newTitle, r23Title);
    assert.notEqual(newTitle, oldTitle);
  }
});

test('only the first scene can declare a section heading', () => {
  assert.throws(() => chapterHeading('hook', [
    { id: 'hook-01', chapter: '鉤子' },
    { id: 'hook-02', chapter: '另一段' },
  ]), /chapter heading appears after first scene/);
  assert.throws(() => chapterHeading('hook', [
    { id: 'hook-01', chapter: '鉤子' },
    { id: 'origin-01' },
  ]), /chapter scene leaked across sections/);
});

test('eleven reviewed hook loops replace stale 104 setup ids', () => {
  const parts = [
    ['hook', ['r17h01', 'b6mn', 'jtmg', 'e37u', 'x7r4']],
    ['origin', ['r6o01', 'r3o01', 'r12o02']],
    ['idea', ['zaky', 'r14i02']],
    ['engine', ['76ur']],
    ['turn', ['r12t01', 'r6t01', 'q4zn', '3zwf', 'r13t02']],
    ['now', ['r15n02', 'r3n01', 'jspd', 'r4n01', 'r3n03']],
  ];
  const pairs = [
    ['r17h01', 'r3o01'], ['b6mn', '76ur'], ['jtmg', 'q4zn'],
    ['zaky', '76ur'], ['r12t01', '3zwf'], ['r15n02', 'jspd'],
    ['r3n01', 'r4n01'], ['r6o01', 'r12o02'], ['r6t01', 'r13t02'],
    ['e37u', 'r14i02'], ['x7r4', 'r3n03'],
  ];
  const video = {
    scenes: parts.map(([key, ids]) => ({ id: `${key}-01`,
      lines: ids.map((id) => ({ id })) })),
    loops: pairs.map(([setup, payoff]) => ({ setup, payoff, what: 'reviewed payoff' })),
  };
  const fresh = reviewedChapterLoops(video);
  assert.equal(Object.values(fresh).flat().length, 11);
  assert.equal(fresh.hook.length, 5);
  assert.equal(fresh.origin.length, 1);
  assert.equal(fresh.now.length, 2);
  assert.equal(Object.values(fresh).flat().some((loop) =>
    ['6h2q', 'y9b6'].includes(loop.setup)), false);
  assert.throws(() => reviewedChapterLoops({ ...video,
    loops: video.loops.map((loop, index) => index === 0
      ? { ...loop, payoff: 'r17h01' } : loop),
  }), /invalid reviewed loop/);
});
