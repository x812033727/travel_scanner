import assert from 'node:assert/strict';
import test from 'node:test';
import { buildFiles, checkFiles, SERIES } from './bundle.mjs';

test('the committed AI drama script bundle matches the repository byte for byte', () => {
  assert.equal(checkFiles().status, 'PASS');
});

test('every series is indexed with its episodes, docs and content hash', () => {
  const files = buildFiles();
  const index = JSON.parse(files['index.json']);
  assert.deepEqual(index.series.map((series) => series.key), SERIES.map((series) => series.key));
  for (const series of index.series) {
    assert.ok(series.episodes.length > 0, `${series.key} has episodes`);
    assert.equal(series.counts.episodes, series.episodes.length);
    const content = JSON.parse(files[`${series.key}.json`]);
    for (const episode of series.episodes) {
      assert.ok(episode.title, `${episode.slug} has a title`);
      assert.deepEqual(Object.keys(content.episodes[episode.slug]).sort(), episode.docs.map((doc) => doc.kind).sort());
    }
    assert.deepEqual(Object.keys(content.documents).sort(), series.documents.map((doc) => doc.id).sort());
  }
});
