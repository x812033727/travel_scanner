import test from 'node:test';
import assert from 'node:assert/strict';

import {
  FLOW_AUDIO_GUARDRAIL,
  SAFE_ZONE_FRAMING_NOTE,
  aggregateBlindReviews,
  exportFlowPromptSheet,
  preflightShort,
  rewriteClipForFlow,
} from './preflight.mjs';

function makeValidSpec(overrides = {}) {
  return {
    slug: 'wangjia-couple-e06',
    title: '老公說晚點再洗碗，三分鐘後廚房出現這畫面 #汪家夫妻',
    description: '阿福又踩到地雷了。本片畫面、配樂由 AI 生成。',
    tags: ['汪家夫妻', '柯基', '柴犬', '零台詞', 'AI短劇'],
    thumb: 's03-reveal',
    intros: {
      afu: 'the photo of A-Fu, a real Pembroke Welsh Corgi in a blue striped shirt',
      zhenzhu: 'the photo of Zhenzhu, a real Shiba Inu in a yellow floral apron',
    },
    shots: [
      {
        id: 's01-hook',
        camera: 'Medium shot, locked',
        chars: ['afu'],
        dur: 1.2,
        in: 0.2,
        ff: 'Medium shot of a cozy kitchen with a solid plain cream wall behind: A-Fu the corgi lies lazily on the sofa while a pile of unbranded ceramic plates sits on the counter.',
        clip: 'The corgi shown in <Picture 1> casually waves one furry paw without looking up. His lips remain closed. The camera holds a static shot.',
        sfx: [['tap', 0.3]],
      },
      {
        id: 's02-stare',
        camera: 'Close-up, slow push in',
        chars: ['zhenzhu'],
        dur: 2.0,
        hold: 0.5,
        music_off: true,
        in: 0.2,
        ff: 'Close-up of Zhenzhu the shiba inu in her yellow floral apron against a solid plain wall, brows pulled down, eyes narrowed.',
        clip: 'The shiba inu shown in <Picture 1> slowly turns her head to face the camera. Her lips remain closed. No smile at any moment. The camera pushes in with small amplitude at slow speed.',
        sfx: [['tension', 0.2]],
      },
      {
        id: 's03-reveal',
        camera: 'Medium shot, locked',
        chars: ['afu'],
        dur: 2.8,
        in: 0.2,
        ff: 'Medium shot of the kitchen sink: A-Fu the corgi himself is wearing giant yellow dish gloves and swimming goggles, surrounded by towering soap foam.',
        clip: 'The corgi shown in <Picture 1> scrubs a plain white plate frantically with two furry front paws while foam wobbles on his head. His lips remain closed. The camera holds a static shot.',
        sfx: [['pop', 0.4]],
      },
      {
        id: 's04-check',
        camera: 'Medium shot, locked',
        chars: ['zhenzhu'],
        dur: 2.4,
        in: 0.2,
        ff: 'Medium shot of Zhenzhu the shiba inu calmly inspecting a sparkling plain white plate on the counter, one furry paw resting beside it.',
        clip: 'The shiba inu shown in <Picture 1> nods once slowly and taps the counter with a furry paw. Her lips remain closed. The camera holds a static shot.',
        sfx: [['chime', 0.6]],
      },
      {
        id: 's05-payoff',
        camera: 'Medium close-up, locked',
        chars: ['afu'],
        dur: 3.0,
        hold: 0.8,
        music_off: true,
        in: 0.2,
        anchor: [0.5, 0.42],
        ff: 'Medium close-up of A-Fu the corgi in his blue shirt, exhausted, soap bubbles still popping on his ears as another towering stack of plain pots slides onto the counter.',
        clip: 'The corgi shown in <Picture 1> freezes with eyes wide open and ears flattened back as a bubble pops on his nose. His lips remain closed. The camera holds a static shot.',
        sfx: [['dun', 1.8]],
      },
    ],
    ...overrides,
  };
}

test('compliant zero-dialogue spec passes with zero errors and zero warnings', () => {
  const report = preflightShort(makeValidSpec());
  assert.equal(report.ok, true);
  assert.equal(report.mode, 'spec');
  assert.equal(report.series, 'wangjia-couple');
  assert.equal(report.summary.errors, 0);
  assert.equal(report.summary.warnings, 0);
  assert.equal(report.summary.totalDuration, 11.4);
});

test('catches SFX placed at or after shot duration and tight tail SFX', () => {
  const spec = makeValidSpec();
  spec.shots[0].sfx = [['tap', 1.2]]; // equal to dur -> error
  spec.shots[4].sfx = [['dun', 2.8]]; // 0.2s from end -> warn
  const report = preflightShort(spec);
  assert.equal(report.ok, false);
  assert.ok(report.issues.some((i) => i.code === 'sfx_outside_shot' && i.severity === 'error'));
  assert.ok(report.issues.some((i) => i.code === 'tail_sfx_tight' && i.severity === 'warn'));
});

test('catches duration hard bounds and single-shot dynamic length cap while allowing still shots', () => {
  const spec = makeValidSpec();
  spec.shots[2].dur = 4.2; // motion 4.2s > 3.5s -> error
  spec.shots[3].dur = 4.0;
  spec.shots[3].still = true; // still exempted
  const report = preflightShort(spec);
  assert.equal(report.ok, false);
  assert.ok(report.issues.some((i) => i.code === 'shot_too_long' && i.shot === 's03-reveal'));
  assert.ok(!report.issues.some((i) => i.code === 'shot_too_long' && i.shot === 's04-check'));

  const tooShort = makeValidSpec({ shots: makeValidSpec().shots.slice(0, 2) });
  const shortReport = preflightShort(tooShort);
  assert.ok(shortReport.issues.some((i) => i.code === 'total_duration_out_of_range' && i.severity === 'error'));
});

test('catches all 6 Gate-0 AI pitfalls without false positives on static camera or street lamp', () => {
  const spec = makeValidSpec();
  spec.shots[0].ff = 'Wide shot of an office with a laptop on the desk, no people, like a magazine cover; a human hand reaches toward the mug.';
  spec.shots[0].clip = 'The corgi holding a mug gives a rueful smirk while a hand reaches in from the edge.';
  spec.shots[1].ff = 'Medium shot of a cozy living room with a street lamp outside the window: Zhenzhu sits inside a blue ceramic vase.';
  spec.shots[1].clip = 'The shiba inu shown in <Picture 1> holds still. The camera holds a static shot.';

  const report = preflightShort(spec);
  const codes = new Set(report.issues.map((i) => i.code));

  assert.ok(codes.has('human_limb_prompt'));
  assert.ok(codes.has('offscreen_hand_with_subject'));
  assert.ok(codes.has('holding_without_paws'));
  assert.ok(codes.has('negative_people_prompt'));
  assert.ok(codes.has('open_background_risk'));
  assert.ok(codes.has('forbidden_print_keyword'));
  assert.ok(codes.has('prop_missing_unbranded_guard'));
  assert.ok(codes.has('ambiguous_smile_word'));
  assert.ok(codes.has('disguise_missing_self_anchor'));
  assert.ok(codes.has('h3_missing_picture1'));
  assert.ok(codes.has('clip_missing_camera_sentence'));
  assert.ok(codes.has('missing_closed_mouth_guard'));

  // s02-stare should NOT trigger open_background_risk ("street lamp") or holding_without_paws ("holds still" / "camera holds")
  assert.ok(!report.issues.some((i) => i.shot === 's02-stare' && i.code === 'open_background_risk'));
  assert.ok(!report.issues.some((i) => i.shot === 's02-stare' && i.code === 'holding_without_paws'));
});

test('enforces series-specific rules for influencer-piglet and raccoon-mischief', () => {
  const piglet = makeValidSpec({
    slug: 'influencer-piglet-e06',
    intros: { fenfen: 'pink piglet', bf: 'capybara boyfriend' },
  });
  piglet.shots[0].dur = 2.4; // > 1.5s hook error
  piglet.shots[0].chars = ['fenfen'];
  piglet.shots[1].chars = ['fenfen', 'bf']; // forbidden two-shot
  piglet.shots[2].chars = ['fenfen'];
  piglet.shots[3].chars = ['bf'];
  piglet.shots[4].chars = ['bf'];
  const pigReport = preflightShort(piglet);
  assert.ok(pigReport.issues.some((i) => i.code === 'piglet_hook_too_long' && i.severity === 'error'));
  assert.ok(pigReport.issues.some((i) => i.code === 'piglet_no_two_shot' && i.severity === 'error'));

  const raccoon = makeValidSpec({
    slug: 'raccoon-mischief-e06',
    intros: { doudou: 'young raccoon', mama: 'mother raccoon' },
  });
  raccoon.shots.forEach((s) => {
    s.chars = ['doudou'];
  });
  raccoon.shots[1].id = 's02-key';
  raccoon.shots[1].dur = 2.0;
  raccoon.shots[1].sfx = [['keys', 0.2]];
  const racReport = preflightShort(raccoon);
  assert.ok(racReport.issues.some((i) => i.code === 'raccoon_key_reaction_slow' && i.severity === 'warn'));
});

test('detects 9:16 Safe-Zone anchor violations and cut-plan (edit/plan.json) mode', () => {
  const plan = {
    music: 'edit/music.mp3',
    music_gain_db: -14,
    shots: [
      { clip: 'colab/s01.mp4', in: 0.2, dur: 1.2, sfx: [{ file: 'sfx/shutter.wav', at: 0.8 }] },
      { clip: 'colab/s02.mp4', in: 0.2, dur: 2.2, music_off: true, push: [1.0, 1.3], anchor: [0.92, 0.85] },
      { clip: 'colab/s03.mp4', in: 0.2, dur: 2.8 },
      { clip: 'colab/s04.mp4', in: 0.2, dur: 2.6 },
      { clip: 'colab/s05.mp4', in: 0.2, dur: 2.6, hold: 0.7, sfx: [{ file: 'sfx/sting.wav', at: 2.9 }] },
    ],
  };
  const report = preflightShort(plan);
  assert.equal(report.mode, 'plan');
  assert.equal(report.ok, false);
  assert.ok(report.issues.some((i) => i.code === 'anchor_outside_safe_zone' && i.severity === 'warn'));
  assert.ok(report.issues.some((i) => i.code === 'sfx_outside_shot' && i.severity === 'error'));
});

test('validates title CTA, thumb existence, and AI disclosure', () => {
  const spec = makeValidSpec({
    title: '記得按讚訂閱小鈴鐺！',
    description: '今天的小日常。',
    thumb: 'nonexistent-shot',
  });
  const report = preflightShort(spec);
  assert.ok(report.issues.some((i) => i.code === 'title_has_cta' && i.severity === 'error'));
  assert.ok(report.issues.some((i) => i.code === 'invalid_thumb' && i.severity === 'error'));
  assert.ok(report.issues.some((i) => i.code === 'description_missing_ai_disclosure' && i.severity === 'warn'));
});

test('exportFlowPromptSheet rewrites H3 <Picture 1> syntax and appends Veo silent guardrail', () => {
  const rewritten = rewriteClipForFlow('The corgi shown in <Picture 1> blinks once. The camera holds a static shot.');
  assert.ok(!rewritten.includes('<Picture 1>'));
  assert.ok(rewritten.includes('from the starting frame'));
  assert.ok(rewritten.includes(FLOW_AUDIO_GUARDRAIL));

  const spec = makeValidSpec();
  spec.shots[0].still = true;
  const md = exportFlowPromptSheet(spec);
  assert.ok(md.includes('AI/備份/Shorts/汪家夫妻/wangjia-couple-e06/flow-inputs/'));
  assert.ok(md.includes('AI/備份/Shorts/汪家夫妻/wangjia-couple-e06/flow-clips/'));
  assert.ok(md.includes(SAFE_ZONE_FRAMING_NOTE));
  assert.ok(md.includes('靜圖慢推（免進 Flow 生片）'));
  assert.ok(!md.includes('flow-clips/s01-hook.mp4'));
  assert.ok(md.includes('flow-clips/s02-stare.mp4'));
});

test('aggregateBlindReviews computes medians, flags sum mismatches, and blocks >=2 scroll-away traps', () => {
  const makeWork = (work, scores, total, scroll = null) => ({
    work,
    scores,
    total,
    would_scroll_away_at: scroll,
    fixes: scroll ? [`加速 ${scroll}`] : [],
  });
  const s82 = { hook: 13, premise: 9, laughs: 17, escalation: 8, surprise: 12, character: 8, payoff: 8, share: 7 }; // 82
  const s76 = { hook: 12, premise: 8, laughs: 15, escalation: 8, surprise: 11, character: 7, payoff: 8, share: 7 }; // 76
  const s64 = { hook: 9, premise: 7, laughs: 12, escalation: 6, surprise: 10, character: 7, payoff: 7, share: 6 }; // 64

  const reviews = [
    { judge: 'shorts-20', works: [makeWork('A', s82, 82), makeWork('B', s76, 76, 's02-key'), makeWork('C', s64, 64)] },
    { judge: 'married-35', works: [makeWork('A', s76, 76), makeWork('B', s82, 82, 's02-key'), makeWork('C', s64, 99)] }, // mismatch 99 vs 64
    { judge: 'comedy-director', works: [makeWork('A', s82, 82), makeWork('B', s76, 76), makeWork('C', s76, 76)] },
  ];

  const agg = aggregateBlindReviews(reviews, { threshold: 70 });
  assert.equal(agg.validationErrors.length, 1);
  assert.equal(agg.results[0].work, 'A');
  assert.equal(agg.results[0].passed, true);
  assert.equal(agg.results[0].median, 82);

  const workB = agg.results.find((r) => r.work === 'B');
  assert.equal(workB.median, 76);
  assert.equal(workB.passed, false); // blocked by >=2 judges scrolling away at s02-key
  assert.ok(workB.scrollTraps[0].includes('s02-key'));

  const workC = agg.results.find((r) => r.work === 'C');
  assert.equal(workC.median, 64);
  assert.equal(workC.passed, false); // blocked by median < 70
});
