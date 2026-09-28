// Offline handoff regression: the real worker prepares a late episode from each import
// bundle, then writer/verifier stage calls are intercepted before any model or network call.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import * as codex from './build.mjs';
import * as claude from '../claude-binge-five-20260928/build.mjs';
import { Automation } from '../../../../tools/video/automation/flow.mjs';

test('all ten import bundles deliver continuity to the actual late-episode writer and verifier payloads', async (t) => {
  const base = await fs.mkdtemp(path.join(os.tmpdir(), 'drama-continuity-worker-'));
  assert.equal(path.dirname(base), path.resolve(os.tmpdir()));
  t.after(() => fs.rm(base, { recursive: true, force: true }));
  const root = path.join(base, 'repo');
  const work = path.join(base, 'work');
  const reports = [];
  const automation = new Automation({
    root, home: base, env: { VIDEO_WORKDIR: work },
    fetch: async () => { throw new Error('network forbidden in offline continuity regression'); },
    now: () => new Date('2026-09-28T00:00:00Z'),
    sleep: async () => {}, stdout: { write() {} }, stderr: { write() {} },
  }, { report: async (slug, payload) => { reports.push({ slug, payload }); } }, {});
  automation.refs = { series: 'Offline reference fixture' };

  for (const batch of [codex, claude]) {
    for (const slug of batch.SLUGS) {
      const source = await batch.loadSource(slug);
      const files = batch.compile(source);
      const series = JSON.parse(files['series-request.json']);
      const documents = JSON.parse(files['documents.json']).documents;
      const setting = documents.find(d => d.kind === 'setting');
      const chapter = documents.find(d => d.kind === 'chapter' && d.chapter_number === 4);
      const beat = chapter.body_json.episodes.find(e => e.number === 35);
      const episode = { number: 35, chapter_number: 4, title: beat.title, logline: beat.logline, beats: beat };
      const episodeSlug = `${slug}-e035`;
      await automation.draftEpisode({ slug: episodeSlug, premise: series.premise, target_minutes: 3 }, {
        series, setting, chapter, episodes: [episode], recaps: [], mysteries: setting.body_json.mysteries,
      }, episode);

      const dir = path.join(root, 'docs', 'videos', episodeSlug);
      const persisted = JSON.parse(await fs.readFile(path.join(dir, 'series.json'), 'utf8'));
      const state = JSON.parse(await fs.readFile(path.join(work, episodeSlug, 'auto.json'), 'utf8'));
      assert.equal(persisted.setting_md, setting.body_md, slug);
      assert.equal(persisted.chapter_md, chapter.body_md, slug);

      const intercepted = [];
      const stop = new Error('stop before a model call');
      automation.stage = async (stage, requestedSlug, payload) => {
        intercepted.push({ stage, requestedSlug, payload });
        throw stop;
      };
      await assert.rejects(automation.write(state), e => e === stop);
      // verify only needs sources before its stage call; no pretend script or verdict is saved.
      await fs.writeFile(path.join(dir, 'video.json'), JSON.stringify({ sources: [] }));
      await assert.rejects(automation.verify(state), e => e === stop);
      assert.deepEqual(intercepted.map(call => call.stage), ['writer', 'verifier'], slug);
      for (const call of intercepted) {
        assert.equal(call.requestedSlug, episodeSlug);
        assert.equal(call.payload.series.episode, 35);
        assert.equal(call.payload.setting_md, setting.body_md, `${slug}: ${call.stage}`);
        assert.equal(call.payload.chapter_md, chapter.body_md, `${slug}: ${call.stage}`);
        for (const rule of source.continuity_notes) {
          assert.ok(call.payload.setting_md.includes(rule), `${slug}: ${call.stage} lost ${rule}`);
        }
      }
    }
  }
  assert.equal(reports.length, 10, 'all report calls stayed in the local stub');
});
