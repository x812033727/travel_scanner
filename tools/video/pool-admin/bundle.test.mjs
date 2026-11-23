import assert from 'node:assert/strict';
import test from 'node:test';
import { buildBundle, checkBundle } from './bundle.mjs';

test('the committed admin pool bundle matches both pools byte for byte', () => {
  assert.deepEqual(checkBundle(), { status: 'PASS', file: 'apps/api/app/video_pools/data/pools.json' });
});

test('every producible theme in the bundle is long and carries an audience score at or above the minimum', () => {
  const bundle = buildBundle();
  assert.deepEqual(bundle.series.map((series) => series.key), ['curio', 'so-thats-why']);
  for (const series of bundle.series) {
    const producible = series.themes.filter((theme) => theme.producible);
    assert.equal(series.counts.producible, producible.length);
    assert.ok(producible.length > 0, `${series.key} has producible themes`);
    for (const theme of producible) {
      assert.ok(theme.long, `${theme.id} is long`);
      assert.ok(theme.audience, `${theme.id} is scored`);
      if (theme.audience.rounds.length) assert.ok(theme.audience.score >= series.audience_min, `${theme.id} passed the gate after improving`);
    }
    assert.ok(series.expansions.length > 0, `${series.key} lists its batches`);
    assert.ok(series.episodes.length > 0, `${series.key} lists its produced episodes`);
    assert.equal(new Set(series.episodes.map((episode) => episode.key)).size, series.episodes.length);
    assert.ok(series.episodes.some((episode) => episode.candidate_ids.length), `${series.key} links episodes to pool topics`);
    assert.ok(series.expansions.every((batch) => batch.selected <= batch.candidates));
  }
});

test('the bundle lists the single-episode cores, which is where the business and brand topics live', () => {
  const bundle = buildBundle();
  const [curio, soThatsWhy] = bundle.series;
  assert.deepEqual(soThatsWhy.cores, [], 'So That’s Why has no stand-alone cores');
  assert.equal(curio.counts.cores, curio.cores.length);
  assert.equal(new Set(curio.cores.map((core) => core.id)).size, curio.cores.length);
  const scored = curio.cores.filter((core) => core.audience);
  assert.equal(curio.counts.cores_scored, scored.length);
  assert.equal(curio.counts.cores_passing, scored.filter((core) => core.audience.score >= curio.audience_min).length);
  assert.ok(curio.counts.cores_passing > 0);
  for (const core of curio.cores) {
    assert.ok(core.question && core.minutes.length === 2 && core.minutes[1] >= 8, `${core.id} can carry an episode`);
    // 評過分的單集題一定有需求分與併分前的五項平均；沒評過的可以只有需求分。
    if (core.audience) assert.ok(core.audience.base !== null && core.audience.demand === core.demand, `${core.id} carries its blend`);
  }
  // 沒有任何長題案屬於商業與品牌奇聞，後台要靠這份清單才看得到那一類。
  assert.ok(!curio.themes.some((theme) => theme.category?.startsWith('W-')));
  assert.ok(curio.cores.some((core) => core.category?.startsWith('W-')));
  // API 拒收超過 16 MiB 的資料包；留一段餘裕，長到這裡就該換成分頁載入。
  assert.ok(Buffer.byteLength(JSON.stringify(bundle)) < 12 * 1024 * 1024);
});
