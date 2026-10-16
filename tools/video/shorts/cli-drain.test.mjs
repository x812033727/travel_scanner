import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { main } from './cli.mjs';

test('supported Shorts tick obeys the shared STOP and drain before posting', async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), 'shorts-drain-'));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const calls = [];
  const context = {
    env: {
      VIDEO_WORKDIR: base,
      MOKAAIR_SITE: 'https://site.test',
      MOKAAIR_VIDEO_TOKEN: `mkv_${'s'.repeat(43)}`,
    },
    fetch: async (url, init) => {
      calls.push([new URL(url).pathname, init.method]);
      return new Response(JSON.stringify({ sent: 0 }), {
        status: 200, headers: { 'content-type': 'application/json' },
      });
    },
  };

  for (const marker of ['STOP', 'DEPLOY_DRAIN']) {
    const file = path.join(base, marker);
    writeFileSync(file, marker);
    await assert.rejects(main(['tick'], context), (error) => {
      assert.equal(error.who, 'owner');
      assert.match(error.message, /Shorts tick held by STOP or DEPLOY_DRAIN/);
      return true;
    });
    assert.deepEqual(calls, [], `${marker}: no request left the CLI`);
    rmSync(file);
  }

  assert.equal(await main(['tick'], context), 0);
  assert.deepEqual(calls, [['/api/video/automation/shorts/tick', 'POST']]);
});
