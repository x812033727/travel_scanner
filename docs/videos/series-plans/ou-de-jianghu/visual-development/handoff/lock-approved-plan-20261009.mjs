import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { main } from '../../../../../../.agents/skills/animation-preproduction/scripts/plan_lock.mjs';
import { acquireProjectLease } from '../../../../../../tools/video/core/project-lease.mjs';

assert.ok(process.argv[2], 'Pass the normal episode media directory. This writes the approved plan once.');
const episode = path.resolve(process.argv[2]);
const file = path.join(episode, 'plan/preflight-20261009-v4/video.json');
const lock = path.join(episode, 'plan/lock.json');
const logs = path.join(episode, 'adoption/20261009');
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const expectedVideo = 'cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17';
assert.equal(hash(file), expectedVideo, 'The approved v4 bytes changed');
assert.ok(!fs.existsSync(lock), 'Refuse overwriting an existing plan lock');
assert.ok(!fs.existsSync(path.join(episode, 'STOP')), 'STOP exists');
assert.ok(!fs.existsSync(path.join(episode, 'LEASE')), 'Another producer holds the episode');
let fetchCalls = 0;
globalThis.fetch = async () => { fetchCalls++; throw Error('Network is disabled for this offline lock operation'); };
const lease = acquireProjectLease(episode, { owner: 'codex-ou-adoption-plan-lock' });
const records = [];
try {
  fs.mkdirSync(logs, { recursive: true });
  const common = ['--file', file, '--workdir', episode, '--route', 'hailuo', '--plan', 'hailuo:max',
    '--hailuo-model', 'h3', '--resolution', '2k', '--handle', '0.5', '--clip-takes', '2',
    '--expected-takes', '1.2,1.5,2', '--pilot', 'a02-s035,a02-s036,a02-s037', '--json'];
  for (const mode of ['write', 'check', 'ready']) {
    lease.verify();
    assert.ok(!fs.existsSync(path.join(episode, 'STOP')), 'STOP appeared');
    assert.equal(hash(file), expectedVideo);
    const argv = [...common, `--${mode}`];
    if (mode === 'write') argv.push('--assist', 'off', '--note', '採用素材與 v4，按此點數上限鎖定 plan');
    let stdout = '', stderr = '';
    const started_at = new Date().toISOString();
    const code = await main(argv, { write: s => { stdout += s; } }, { write: s => { stderr += s; } });
    const prefix = path.join(logs, `approved-plan-${mode}`);
    fs.writeFileSync(prefix + '.stdout.json', stdout, { flag: 'wx' });
    fs.writeFileSync(prefix + '.stderr.txt', stderr, { flag: 'wx' });
    const record = { mode, argv, started_at, ended_at: new Date().toISOString(), exit_code: code,
      stdout_sha256: hash(prefix + '.stdout.json'), stderr_sha256: hash(prefix + '.stderr.txt') };
    fs.writeFileSync(prefix + '.execution.json', JSON.stringify(record, null, 2) + '\n', { flag: 'wx' });
    records.push(record);
    assert.equal(code, mode === 'ready' ? 1 : 0, `Unexpected ${mode} result; inspect preserved logs`);
  }
  lease.verify();
  assert.equal(fetchCalls, 0);
  console.log(JSON.stringify({ modes: records.map(r => ({ mode: r.mode, exit_code: r.exit_code })),
    video_sha256: hash(file), plan_lock_sha256: hash(lock), fetch_calls: fetchCalls }));
} finally {
  lease.release();
}
