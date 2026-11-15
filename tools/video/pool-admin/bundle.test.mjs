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
