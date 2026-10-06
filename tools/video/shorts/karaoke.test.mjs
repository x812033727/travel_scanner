import test from 'node:test';
import assert from 'node:assert/strict';

import { measure } from '../core/captions.mjs';
import {
  CAPTION_BOX, CAPTION_RULES, CAPTIONS_ENV, DEFAULT_CAPTIONS, GROUP_MAX, GROUP_MIN, KARAOKE_VERSION, MIN_STATE_FRAMES,
  alignedGroupTimes, captionLines, captionStates, captionsOption, captionsSummary, estimateGroupTimes, groupLine, phraseGroups, phraseTiming, speechSpan, timingFile, tokens, weightOf,
} from './karaoke.mjs';

const tone = ({ lead = 0, speech = 1, tail = 0, amplitude = 8000, rate = 48_000 } = {}) => {
  const samples = new Int16Array(Math.round((lead + speech + tail) * rate));
  const from = Math.round(lead * rate);
  const to = from + Math.round(speech * rate);
  for (let i = from; i < to; i++) samples[i] = Math.round(Math.sin((2 * Math.PI * 440 * i) / rate) * amplitude);
  return samples;
};
const cjk = (count) => '一二三四五六七八九十'.repeat(Math.ceil(count / 10)).slice(0, count);

test('a Latin word or a number is one token, punctuation and brackets stay with their neighbour', () => {
  assert.deepEqual(tokens('用 GPT-5.5 算 2026 年'), ['用 ', 'GPT-5.5 ', '算 ', '2026 ', '年']);
  assert.deepEqual(tokens('你好，世界。'), ['你', '好，', '世', '界。']);
  assert.deepEqual(tokens('他說「好」！'), ['他', '說', '「好」！']);
  assert.deepEqual(tokens('（真的）85 元'), ['（真', '的）', '85 ', '元']);
  assert.deepEqual(tokens(''), []);
  for (const text of ['咖啡 85 元 × 2', 'GPT-5.5 和 Gemini 各算一次', '答案是 275 元…對嗎？']) assert.equal(tokens(text).join(''), text, 'tokens lose nothing');
});

test('the caption box holds fifteen full-width glyphs a line and two lines; the lines are decided once', () => {
  assert.ok(CAPTION_RULES.maxChars * 49 + 40 <= CAPTION_BOX.width, 'fifteen 49 px glyphs fit the padded box');
  assert.deepEqual(CAPTION_BOX, { x: 80, y: 1430, width: 820, height: 165 });
  assert.deepEqual(captionLines(cjk(15)), [cjk(15)]);
  const two = captionLines(cjk(20));
  assert.equal(two.length, 2);
  for (const line of two) assert.ok(measure(line, CAPTION_RULES) <= CAPTION_RULES.maxChars, line);
  assert.equal(two.join(''), cjk(20));
  const clause = captionLines('一張手寫的發票，兩個品項加上一張折價券');
  assert.deepEqual(clause, ['一張手寫的發票，', '兩個品項加上一張折價券'], 'a line ends where the clause ends when it can');
  assert.ok(captionLines(cjk(36)).length > 2, 'a phrase wider than two lines overflows, as the layout measurement reports');
  assert.deepEqual(captionLines('  '), []);
});

test('a line lights in groups of five to ten units, whole tokens, preferring to end on a clause', () => {
  assert.deepEqual(groupLine(cjk(10)), [cjk(10)]);
  const fifteen = groupLine(cjk(15));
  assert.equal(fifteen.length, 2);
  assert.deepEqual(fifteen.map((group) => measure(group, CAPTION_RULES)), [7, 8]);
  assert.deepEqual(groupLine('一張手寫的發票，兩個品項加'), ['一張手寫的發票，', '兩個品項加'], 'the comma wins over an even split');
  const latin = '我們請 ChatGPT 和 Gemini 各算一次';
  const groups = groupLine(latin);
  assert.equal(groups.length, 2);
  assert.equal(groups.join(''), latin);
  for (const word of ['ChatGPT', 'Gemini']) assert.equal(groups.filter((group) => group.includes(word)).length, 1, `${word} is lit whole`);
  assert.ok(!groups.some((group) => /(?:^|[^A-Za-z])(?:Chat|GPT|Gem|ini)(?:[^A-Za-z]|$)/.test(group)), 'no group holds half a Latin word');
  const edges = new Set();
  let offset = 0;
  for (const token of tokens(latin)) {
    offset += token.length;
    edges.add(offset);
  }
  let seen = 0;
  for (const group of groups) {
    seen += group.length;
    assert.ok(edges.has(seen), `a group ends on a token boundary: ${group}`);
  }
  for (let count = 11; count <= 30; count++) {
    const sizes = groupLine(cjk(count)).map((group) => measure(group, CAPTION_RULES));
    assert.ok(sizes.every((size) => size >= GROUP_MIN && size <= GROUP_MAX), `${count}: ${sizes}`);
    assert.equal(sizes.reduce((sum, size) => sum + size, 0), count);
  }
  assert.deepEqual(groupLine(''), []);
});

test('groups know their line, width and spoken weight; a number weighs two, a comma half', () => {
  assert.equal(weightOf('咖啡 85 元'), 5);
  assert.equal(weightOf('好，'), 1.5);
  assert.equal(weightOf(''), 1);
  const groups = phraseGroups('一張手寫的發票，兩個品項加上一張折價券');
  assert.deepEqual(groups.map((group) => group.line), [0, 1, 1]);
  assert.equal(groups[0].text, '一張手寫的發票，');
  assert.equal(groups.slice(1).map((group) => group.text).join(''), '兩個品項加上一張折價券');
  assert.deepEqual(groups.map((group) => group.width).sort(), [5, 6, 8]);
  assert.deepEqual(groups.map((group) => group.weight).sort(), [5, 6, 7.5], 'the comma adds half a unit to its seven characters');
});

test('the speech span skips the silence at the clip\'s edges and widens a little', () => {
  const span = speechSpan(tone({ lead: 0.2, speech: 1, tail: 0.3 }));
  assert.ok(Math.abs(span.start - 0.17) <= 0.015, `start ${span.start}`);
  assert.ok(Math.abs(span.end - 1.26) <= 0.015, `end ${span.end}`);
  assert.deepEqual(speechSpan(new Int16Array(48_000)), { start: 0, end: 1 }, 'a silent clip is taken as spoken end to end');
  const noisy = tone({ lead: 0.2, speech: 1, tail: 0.3 });
  for (let i = 0; i < noisy.length; i++) if (noisy[i] === 0) noisy[i] = (i % 7) - 3;
  const found = speechSpan(noisy);
  assert.ok(Math.abs(found.start - 0.17) <= 0.015 && Math.abs(found.end - 1.26) <= 0.015, 'a noise floor under the threshold does not move the edges');
  assert.deepEqual(speechSpan(tone({ speech: 0.5 }), 48_000), { start: 0, end: 0.5 });
});

test('each group takes its share of the speech span; the states cover the cue exactly', () => {
  const timed = estimateGroupTimes([{ weight: 1 }, { weight: 1 }, { weight: 2 }], { start: 0, end: 4 });
  assert.deepEqual(timed.map((group) => [group.start, group.end]), [[0, 1], [1, 2], [2, 4]]);
  const cue = { index: 0, frames: 90, text: 'x' };
  assert.deepEqual(captionStates(cue, [{ start: 0.1 }, { start: 1 }, { start: 2 }]), [{ group: 0, frames: 30 }, { group: 1, frames: 30 }, { group: 2, frames: 30 }]);
  assert.deepEqual(captionStates(cue, [{ start: 0.1 }, { start: 2.98 }]), [{ group: 0, frames: 90 }], 'a one-frame state folds into the one before it');
  assert.deepEqual(captionStates({ ...cue, frames: 40 }, [{ start: 0 }, { start: 0.02 }, { start: 1 }]), [{ group: 0, frames: 30 }, { group: 2, frames: 10 }], 'a short first state takes the second\'s frames');
  assert.deepEqual(captionStates(cue, []), [{ group: 0, frames: 90 }]);
  let seed = 7;
  const random = () => (seed = (seed * 48271) % 2147483647) / 2147483647;
  for (let round = 0; round < 200; round++) {
    const frames = 20 + Math.floor(random() * 160);
    const count = 1 + Math.floor(random() * 5);
    const seconds = frames / 30;
    const starts = Array.from({ length: count }, () => random() * seconds).sort((a, b) => a - b);
    const states = captionStates({ index: 0, frames }, starts.map((start) => ({ start })));
    assert.equal(states.reduce((sum, state) => sum + state.frames, 0), frames);
    assert.ok(states.every((state) => state.frames >= MIN_STATE_FRAMES || states.length === 1), JSON.stringify(states));
    assert.ok(states.every((state, index) => index === 0 || state.group > states[index - 1].group));
  }
});

test('timing.json says where its times came from, one phrase per cue, in the frames of the timeline', () => {
  const timeline = { fps: 30, frames: 150, cues: [{ index: 0, sceneIndex: 0, text: '一張手寫的發票，兩個品項加上一張折價券', startFrame: 0, endFrame: 90, frames: 90 }, { index: 1, sceneIndex: 0, text: '答案是 275 元', startFrame: 90, endFrame: 150, frames: 60 }] };
  const wavs = [{ samples: tone({ lead: 0.1, speech: 2.5, tail: 0.2 }), sampleRate: 48_000 }, { samples: tone({ speech: 1.6 }), sampleRate: 48_000 }];
  const timing = timingFile(timeline, wavs);
  assert.equal(timing.source, 'estimated');
  assert.equal(timing.method, KARAOKE_VERSION);
  assert.equal(timing.version, 1);
  assert.equal(timing.fps, 30);
  assert.equal(timing.phrases.length, 2);
  const [first, second] = timing.phrases;
  assert.equal(first.cue, 0);
  assert.equal(first.audio_seconds, 2.8);
  assert.deepEqual(first.lines, ['一張手寫的發票，', '兩個品項加上一張折價券']);
  assert.equal(first.groups.length, 3);
  assert.ok(first.groups[0].start >= 0.05 && first.groups[0].start <= 0.1, `the first group waits for the voice: ${first.groups[0].start}`);
  assert.ok(first.groups.every((group, index) => index === 0 || group.start === first.groups[index - 1].end), 'groups follow each other');
  assert.equal(first.states.reduce((sum, state) => sum + state.frames, 0), 90);
  assert.equal(first.states[0].frames >= Math.round(first.groups[1].start * 30), true, 'the first state runs until the second group is spoken');
  assert.deepEqual(second.lines, ['答案是 275 元']);
  assert.equal(second.groups.length, 1);
  assert.deepEqual(second.states, [{ group: 0, frames: 60 }]);
  assert.deepEqual(phraseTiming(timeline.cues[1], wavs[1].samples).states, second.states);
  assert.throws(() => timingFile(timeline, wavs.slice(1)), /a clip is required/);
  assert.deepEqual(captionsSummary(timing), { style: 'karaoke', source: 'estimated', version: KARAOKE_VERSION, groups: 4, states: first.states.length + 1 });
  assert.deepEqual(captionsSummary(null), { style: 'plain' });
});

test('measured character times light each group where its first unit is spoken, and the estimate stays when they do not spell the phrase', () => {
  const text = '一張手寫的發票，兩個品項加上一張折價券';
  const groups = phraseGroups(text);
  const units = [...text].map((character, index) => ({ text: character, start_ms: 100 + index * 200, end_ms: 300 + index * 200 }));
  const span = { start: 0.07, end: 4.5 };
  const timed = alignedGroupTimes(groups, units, span);
  assert.equal(timed.length, groups.length);
  assert.equal(timed[0].start, span.start, 'the first group starts with the speech span, as captionStates lays it');
  let offset = 0;
  for (const [index, group] of groups.entries()) {
    if (index > 0) assert.equal(timed[index].start, Number(((100 + offset * 200) / 1000).toFixed(3)), `${group.text} starts where its first character is spoken`);
    offset += [...group.text.replace(/\s+/g, '')].length;
  }
  for (let index = 0; index < timed.length - 1; index++) assert.equal(timed[index].end, timed[index + 1].start, 'groups follow each other');
  assert.equal(timed.at(-1).end, span.end, 'the last group ends with the span');
  assert.deepEqual(timed.map((group) => group.text), groups.map((group) => group.text));
  // A Latin word is one unit on both sides; whitespace counts for nothing.
  const latin = [['我', 0], ['們', 200], ['請', 400], ['ChatGPT', 600], ['和', 1400], ['Gemini', 1600], ['各', 2200], ['算', 2400], ['一', 2600], ['次', 2800]].map(([t, s]) => ({ text: t, start_ms: s, end_ms: s + 200 }));
  assert.deepEqual(alignedGroupTimes([{ text: '我們請 ChatGPT ' }, { text: '和 Gemini 各算一次' }], latin, { start: 0, end: 3.2 }).map((group) => [group.start, group.end]), [[0, 1.4], [1.4, 3.2]]);
  // A term the lexicon reads as one unit, cut between its words, shares its time by its letters.
  const term = alignedGroupTimes([{ text: '用 Claude ' }, { text: 'Code 寫' }], [{ text: '用', start_ms: 0, end_ms: 200 }, { text: 'Claude Code', start_ms: 200, end_ms: 1200 }, { text: '寫', start_ms: 1200, end_ms: 1400 }], { start: 0, end: 1.5 });
  assert.deepEqual(term.map((group) => [group.start, group.end]), [[0, 0.8], [0.8, 1.5]]);
  // Starts never run backwards and stay inside the span.
  const odd = [['一', 500], ['二', 600], ['三', 100], ['四', 200], ['五', 5000], ['六', 5100]].map(([t, s]) => ({ text: t, start_ms: s, end_ms: s + 100 }));
  assert.deepEqual(alignedGroupTimes([{ text: '一二' }, { text: '三四' }, { text: '五六' }], odd, { start: 0.05, end: 2 }).map((group) => [group.start, group.end]), [[0.05, 0.1], [0.1, 2], [2, 2]]);
  // What keeps the estimate: units that start elsewhere, a broken entry, nothing at all.
  assert.equal(alignedGroupTimes(groups, units.slice(1), span), null);
  assert.equal(alignedGroupTimes(groups, [{ text: '一', start_ms: 'x', end_ms: 1 }], span), null);
  assert.equal(alignedGroupTimes(groups, [], span), null);
  assert.equal(alignedGroupTimes([], units, span), null);
  assert.ok(alignedGroupTimes(groups, [...units, { text: '。', start_ms: 9000, end_ms: 9100 }], span), 'units past the last group are left alone');
});

test('timing.json follows measured times when every phrase has them, says which, and is the estimate byte for byte otherwise', () => {
  const timeline = { fps: 30, frames: 150, cues: [{ index: 0, sceneIndex: 0, text: '一張手寫的發票，兩個品項加上一張折價券', startFrame: 0, endFrame: 90, frames: 90 }, { index: 1, sceneIndex: 0, text: '答案是 275 元', startFrame: 90, endFrame: 150, frames: 60 }] };
  const wavs = [{ samples: tone({ lead: 0.1, speech: 2.5, tail: 0.2 }), sampleRate: 48_000 }, { samples: tone({ speech: 1.6 }), sampleRate: 48_000 }];
  const chars = (text, step) => [...text].filter((c) => c.trim()).map((c, i) => ({ text: c, start_ms: 50 + i * step, end_ms: 50 + (i + 1) * step }));
  const first = { source: 'azure', model: 'zh-TW-HsiaoChenNeural', chars: chars('一張手寫的發票，兩個品項加上一張折價券', 130) };
  const second = { source: 'aligned', model: 'fake', chars: [['答', 0], ['案', 200], ['是', 400], ['275', 600], ['元', 1200]].map(([t, s]) => ({ text: t, start_ms: s, end_ms: s + 200 })) };
  const estimate = timingFile(timeline, wavs);
  assert.equal(JSON.stringify(timingFile(timeline, wavs, null)), JSON.stringify(estimate));
  assert.equal(JSON.stringify(timingFile(timeline, wavs, [null, null])), JSON.stringify(estimate), 'nothing measured is the estimate, byte for byte');
  assert.deepEqual(Object.keys(estimate.phrases[0]), ['cue', 'text', 'audio_seconds', 'speech', 'lines', 'groups', 'states']);
  const partial = timingFile(timeline, wavs, [first, null]);
  assert.equal(partial.source, 'estimated', 'one phrase on an estimate keeps the file an estimate');
  assert.deepEqual(partial.phrases[0].aligned, { source: 'azure', model: 'zh-TW-HsiaoChenNeural' });
  assert.equal(partial.phrases[0].groups[1].start, Number(((50 + 8 * 130) / 1000).toFixed(3)), 'the second group starts where 兩 is spoken');
  assert.deepEqual(partial.phrases[1], estimate.phrases[1]);
  assert.deepEqual(captionsSummary(partial), { style: 'karaoke', source: 'estimated', version: KARAOKE_VERSION, groups: 4, states: partial.phrases[0].states.length + 1, aligned: 1 });
  const complete = timingFile(timeline, wavs, [first, second]);
  assert.equal(complete.source, 'aligned');
  assert.deepEqual(complete.phrases[1].aligned, { source: 'aligned', model: 'fake' });
  assert.deepEqual(complete.phrases[1].groups.map((group) => [group.start, group.end]), [[0, 1.6]], 'one group still spans the clip');
  assert.equal(captionsSummary(complete).aligned, 2);
  assert.equal(captionsSummary(complete).source, 'aligned');
  assert.equal(complete.phrases[0].states.reduce((sum, state) => sum + state.frames, 0), 90);
  assert.deepEqual(phraseTiming(timeline.cues[0], wavs[0].samples, 48_000, 30, first).groups, complete.phrases[0].groups);
  // A timing that does not spell the phrase keeps that phrase's estimate.
  const wrong = timingFile(timeline, wavs, [{ source: 'azure', model: 'v', chars: chars('別的句子', 100) }, second]);
  assert.equal(wrong.source, 'estimated');
  assert.deepEqual(wrong.phrases[0], estimate.phrases[0]);
  assert.deepEqual(wrong.phrases[1].aligned, { source: 'aligned', model: 'fake' });
});

test('the caption style is the flag, else the environment, else plain', () => {
  assert.equal(DEFAULT_CAPTIONS, 'plain');
  assert.equal(captionsOption(undefined, {}), 'plain');
  assert.equal(captionsOption(undefined, { [CAPTIONS_ENV]: 'karaoke' }), 'karaoke');
  assert.equal(captionsOption('plain', { [CAPTIONS_ENV]: 'karaoke' }), 'plain');
  assert.equal(captionsOption('karaoke', {}), 'karaoke');
  assert.throws(() => captionsOption('words', {}), /captions must be one of plain, karaoke/);
  assert.throws(() => captionsOption(undefined, { [CAPTIONS_ENV]: 'KARAOKE' }), /got KARAOKE/);
});
