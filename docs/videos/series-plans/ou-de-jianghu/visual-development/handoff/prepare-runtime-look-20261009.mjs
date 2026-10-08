// Offline, one-time integration of the nine finalized full-body candidates.
// --apply imports pending candidates; --check is read-only. Neither mode judges or approves.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const script = fileURLToPath(import.meta.url);
const handoff = path.dirname(script);
const root = path.resolve(handoff, '../../../../../..');
const options = parseArgs({ options: { apply: { type: 'boolean' }, check: { type: 'boolean' }, 'media-base': { type: 'string' } }, strict: true });
assert.ok(Boolean(options.values.apply) !== Boolean(options.values.check), 'choose exactly one of --apply or --check');
const baseArgument = options.values['media-base'] ?? process.env.VIDEO_WORKDIR;
assert.ok(baseArgument && path.isAbsolute(baseArgument), 'supply an absolute --media-base path (the base above the episode slug), or VIDEO_WORKDIR');
const mediaBase = path.resolve(baseArgument);
const slug = 'ou-de-jianghu-e001';
const workdir = path.join(mediaBase, slug);
const directory = path.join(workdir, 'adoption/20261009');
const projectFile = path.join(workdir, 'plan/preflight-20261009-v4/video.json');
const projectSha = 'cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17';
const portraitReceiptPath = 'docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits/finalized-views-receipt.json';
const resultFile = path.join(handoff, 'runtime-look-preparation-20261009.json');
const markdownFile = path.join(handoff, 'runtime-look-preparation-20261009.md');
const externalResult = path.join(directory, 'receipts/runtime-look-preparation-20261009.json');
const manifestFile = path.join(workdir, 'characters/manifest.json');
const expected = [
  ['shen-guihe', 3, 'f92406c0e73a7458e012a1487a60cd966b128192f776ddd272028cbd3724ccac'],
  ['ji-wushuang', 1, '6ed68b1de7db15559e4b9d57c84ba92c0ffff80bf1e59970c82677d4915ecec3'],
  ['ji-wen', 1, '8a60b9ce8f83534542d002caedc0102d65255137d9eca99190091565e3ed9a35'],
  ['bao-sanqian', 1, '625174d287f29d8fda2791f8193a89c26476a121bea7b1d80aa52fbc9e43afd9'],
  ['yin-wusheng', 1, 'ccf625f6813518032435c4a462a1203e6128691afda10516fe9dbcf95e5972ea'],
  ['yan-hui', 1, '5cf0a08166ecbb00a7f1a484c4bc7c8ec16ab772f5ad61f1f8390c44792caa21'],
  ['nie-gutie', 1, '866e1e8cb75e7fabd7ebdc7ae2deca88938b79fc05f864a9c708d31d5d597115'],
  ['xuanmen-elder', 1, '564e79297979b1c7bb49b3fba39d8c3e590a2fc6bae246fa37b01837ac61667d'],
  ['luo-qingyan', 1, '9b3991c06ec0ae39acedaec6332a698d7209a75bbb3e5b245e79b6b3da96aeef'],
];
const baselineNames = ['adoption', 'animation-reference', 'art-direction', 'external-look-staging', 'final-art', 'plan', 'portraits', 'preproduction-pr-body.md', 'scene-props'].sort();
const preservedAdoptionNames = ['capture-gate-preflight.mjs', 'gate-preflight-20261009.full.json', 'gate-preflight-file-checks.json', 'media-status-snapshot.json', 'native-plan-readonly.json', 'plan-ready-normal.execution.json', 'plan-ready-normal.stderr.txt', 'plan-ready-normal.stdout.json'].sort();
const sha = value => createHash('sha256').update(value).digest('hex');
const bytes = file => readFileSync(file);
const hashFile = file => sha(bytes(file));
const read = file => JSON.parse(readFileSync(file, 'utf8'));
const json = value => `${JSON.stringify(value, null, 2)}\n`;
const slash = value => value.replaceAll('\\', '/');
const mediaPath = file => `<VIDEO_WORKDIR>/${slash(path.relative(mediaBase, file))}`;
const repoPath = file => slash(path.relative(root, file));
const publicPath = file => path.relative(mediaBase, file).startsWith('..') ? repoPath(file) : mediaPath(file);
const inside = (base, file) => { const rel = path.relative(realpathSync(base), realpathSync(file)); assert.ok(rel && !rel.startsWith(`..${path.sep}`) && rel !== '..' && !path.isAbsolute(rel), `path outside expected base: ${file}`); return file; };
const resolvePublic = value => value.startsWith('<VIDEO_WORKDIR>/') ? inside(mediaBase, path.join(mediaBase, value.slice(16))) : inside(root, path.join(root, value));
const saveNew = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, typeof value === 'string' ? value : json(value), { flag: 'wx' }); };
const mode = [options.values.check ? '--check' : '--apply'];
let fetchAttempts = 0;
const denyFetch = async () => { fetchAttempts++; throw new Error('Network forbidden in offline runtime look preparation'); };
globalThis.fetch = denyFetch;
const { main } = await import(pathToFileURL(path.join(root, 'tools/video/cli.mjs')));
const { lookHash, resolveLook } = await import(pathToFileURL(path.join(root, 'tools/video/core/drama.mjs')));
const { stopRequested } = await import(pathToFileURL(path.join(root, 'tools/video/core/paths.mjs')));
const { acquireProjectLease, leaseHolder } = await import(pathToFileURL(path.join(root, 'tools/video/core/project-lease.mjs')));
const { inspectLookPng } = await import(pathToFileURL(path.join(root, 'tools/video/media/look.mjs')));
const { sheetKey } = await import(pathToFileURL(path.join(root, 'tools/video/media/series-store.mjs')));

function guard({ phase, lease = null } = {}) {
  assert.equal(stopRequested(workdir), false, 'STOP exists at project or work base; no operation allowed');
  if (lease) lease.verify();
  else assert.equal(leaseHolder(workdir), null, 'pre-existing LEASE requires manual reconciliation; never take over here');
  const allowed = [...baselineNames, ...(phase === 'runtime' ? ['characters'] : []), ...(lease ? ['LEASE'] : [])].sort();
  assert.deepEqual(readdirSync(workdir).sort(), allowed, `unexpected runtime state during ${phase}`);
  for (const name of allowed) assert.equal(lstatSync(path.join(workdir, name)).isSymbolicLink(), false, `refuse symlink: ${name}`);
  for (const name of ['keyframes', 'clips', 'approvals.json', 'media', 'audio', 'tts', 'frames', 'timeline.json', 'auto.json', 'video.json', 'script.md', 'characters/choice.json']) {
    assert.equal(existsSync(path.join(workdir, name)), false, `refuse existing or newly created protected state: ${name}`);
  }
}
function tree(dir) {
  const entries = [];
  function walk(current) {
    for (const name of readdirSync(current).sort()) {
      const file = path.join(current, name), stat = lstatSync(file);
      assert.equal(stat.isSymbolicLink(), false, `refuse symlink in candidate tree: ${file}`);
      if (stat.isDirectory()) walk(file);
      else { assert.ok(stat.isFile()); entries.push({ path: slash(path.relative(dir, file)), bytes: stat.size, sha256: hashFile(file) }); }
    }
  }
  walk(dir);
  return entries;
}
function verifyInputs(bindings) { for (const entry of bindings) assert.equal(hashFile(resolvePublic(entry.path)), entry.sha256, `input changed: ${entry.path}`); }
function verifyRuntime(result) {
  const manifest = read(manifestFile);
  assert.equal(hashFile(manifestFile), result.runtime_manifest_sha256);
  assert.equal(manifest.look_hash, result.look_hash);
  assert.equal(manifest.external_imports, true);
  assert.equal(manifest.contact_sheet, null);
  assert.deepEqual(Object.keys(manifest.characters).sort(), expected.map(each => each[0]).sort());
  for (const entry of result.candidates) {
    const character = manifest.characters[entry.character_id];
    assert.equal(character.candidates.length, 1);
    assert.equal(character.suggested, null);
    assert.equal(character.needs_review, true);
    const candidate = character.candidates[0];
    assert.equal(candidate.n, 1); assert.equal(candidate.judge, null); assert.equal(candidate.judge_state, undefined);
    assert.equal(candidate.sha256, entry.sha256);
    assert.equal(hashFile(path.join(workdir, candidate.file)), entry.sha256);
    assert.equal(candidate.key, entry.candidate_key);
    assert.equal(candidate.external_import.source_sha256, entry.source_sidecar_sha256);
    assert.equal(hashFile(path.join(workdir, candidate.external_import.source_file)), entry.source_sidecar_sha256);
    assert.equal(hashFile(resolvePublic(entry.source_sidecar)), entry.source_sidecar_sha256);
    assert.deepEqual(candidate.external_import.source_files, result.source_files);
    assert.equal(candidate.external_import.character_key, entry.character_key);
    assert.deepEqual(inspectLookPng(bytes(path.join(workdir, candidate.file))), entry.native_dimensions);
  }
  assert.deepEqual(tree(path.join(workdir, 'characters')), result.runtime_character_tree);
  assert.equal(sha(json(result.runtime_character_tree)), result.runtime_character_tree_sha256);
  assert.equal(result.runtime_character_tree.length, 27, 'one manifest, 18 candidate/sidecar files and eight prior manifest snapshots');
}
function markdown(result) {
  return `# 第一集正常 runtime 候選接入收據（2026-10-09）\n\n九張最新版全身圖已離線接入正常工作目錄，全部仍是待 judge、待選用候選。這份收據只更新本次接入狀態；原始畫像與隔離 staging 收據保留其歷史狀態。素材／v4 與 Hailuo 預算的正式採用由主控另綁決策收據；本次工具沒有寫入 look 核准或 plan 開拍鎖定。\n\n- 工作目錄：\`${result.workdir}\`；CLI \`--workdir\` 傳入其上一層 base，未套錯雙層 slug。\n- \`runtime_candidates_integrated: true\`、\`owner_adoption_recorded_here: false\`、\`budget_authorization_recorded_here: false\`、\`look_approved: false\`、\`plan_locked: false\`。\n- ${result.command_count} 次 CLI：9 dry-run、9 import、9 exact-rerun，全部 exit 0；整個 characters 樹重跑後位元組相同。\n- \`fetch_attempts: 0\`；\`paid_requests: 0\`；未帶 \`--judge\`、未 choose／approve／review-push／review-pull。global fetch 與 CLI fetch 均在程序內禁止。\n- 啟動時無 LEASE／STOP、characters／keyframes／clips／approvals／media；持有本程序專屬 lease 後才寫入，每次命令前重查，完成後明確 release 並確認 LEASE 消失。\n- 每人恰一候選 n=1；\`judge=null\`、\`suggested=null\`、\`needs_review=true\`；沒有 choice／approvals／付費帳本／series-store 寫入。\n\n## 綁定與核對\n\n| 證據 | SHA-256／值 |\n| --- | --- |\n| v4 video.json | \`${result.project_sha256}\` |\n| 正式 repo video.json | \`${result.canonical_project_sha256}\` |\n| look_hash（v4 與 repo 相同） | \`${result.look_hash}\` |\n| 正常 characters/manifest.json | \`${result.runtime_manifest_sha256}\` |\n| 全 characters 樹索引 | \`${result.runtime_character_tree_sha256}\` |\n| 27 次命令紀錄 | \`${result.command_log_sha256}\` |\n\n12 份正典來源逐檔重新算 SHA-256，完整清單見同名 JSON 的 \`source_files\`；畫像收據、原圖、所有原參照圖及 v4 文件也重新算 hash 並前後核對。九張原生 PNG 均為 1024 × 1536，未改圖或放大。v4 與 repo 的 look_hash 和九個 sheetKey 相同，只證明角色基底契約相容，不等於 v4 劇本／plan 已正式採用。\n\n| 角色 ID | 接入版本 | 原圖 SHA-256 | source sidecar SHA-256 |\n| --- | --- | --- | --- |\n${result.candidates.map(entry => `| ${entry.character_id} | ${entry.key} | \`${entry.sha256}\` | \`${entry.source_sidecar_sha256}\` |`).join('\n')}\n\n## 保留的關卡\n\n主控在接入前已傳達使用者正式採用 146 份素材、v4、Hailuo 本期 26980.8 點及小樣 316.8 點；正式決策由主控另記。本收據不重寫原始收據的歷史 pending 值。使用者明確不授權 API 扣款，look 留待實際判圖；本工具沒有執行 judge、選用、核准或 plan 寫入。後續必須用真實 judge 結果走正常選用與 look 審核，不能把本次候選接入或人工實圖覆核寫成 judge。既有八張 staging 圖仍同版；沈歸鶴這次接入 full-body-v3，舊 staging 的 v1 保留不動。\n\n## 重查\n\n在 repo 根目錄以可用 Node 執行 \`node ${repoPath(script)} --check --media-base "<VIDEO_WORKDIR>"\`。此模式只讀核對來源、原圖、sidecar、manifest、完整候選樹、27 筆命令與本收據；若後續正常 judge 或來源更新導致改變，它會失敗提示歷史收據已非目前狀態。\n\n外部完整收據：\`${result.external_receipt}\`；命令紀錄：\`${result.command_log}\`。\n`;
}

if (mode[0] === '--check') {
  guard({ phase: 'runtime' });
  const result = read(resultFile);
  assert.equal(hashFile(script), result.preparation_script_sha256);
  if (result.portability_revision) {
    const revision = result.portability_revision;
    assert.equal(hashFile(resolvePublic(revision.executed_script)), revision.executed_script_sha256);
    assert.equal(hashFile(resolvePublic(revision.original_receipt)), revision.original_receipt_sha256);
    const original = read(resolvePublic(revision.original_receipt));
    assert.equal(original.preparation_script_sha256, revision.executed_script_sha256);
    assert.deepEqual(result, { ...original, preparation_script_sha256: hashFile(script), portability_revision: revision }, 'only portability audit metadata may differ from the executed receipt');
  }
  assert.equal(readFileSync(externalResult, 'utf8'), readFileSync(resultFile, 'utf8'));
  assert.equal(readFileSync(markdownFile, 'utf8'), markdown(result));
  verifyInputs(result.input_bindings);
  verifyRuntime(result);
  const commandLog = resolvePublic(result.command_log);
  assert.equal(hashFile(commandLog), result.command_log_sha256);
  const commands = read(commandLog);
  assert.equal(commands.length, 27);
  assert.equal(commands.every(each => each.exit_code === 0), true);
  for (const entry of result.command_logs) assert.equal(hashFile(resolvePublic(entry.path)), entry.sha256);
  assert.equal(fetchAttempts, 0);
  console.log(json({ status: 'read_only_runtime_check_passed', candidates: 9, sources: 12, fetch_attempts: 0, manifest_sha256: result.runtime_manifest_sha256 }));
} else {
  guard({ phase: 'initial' });
  assert.deepEqual(readdirSync(directory).sort(), preservedAdoptionNames, 'only the confirmed sibling-agent diagnostic evidence may preexist');
  for (const file of ['sources', 'logs', 'receipts'].map(name => path.join(directory, name)).concat([resultFile, markdownFile])) assert.equal(existsSync(file), false, `refuse overwrite/resume: ${file}`);
  assert.equal(hashFile(projectFile), projectSha, 'expected exact v4 bytes');
  const doc = read(projectFile), canonicalFile = path.join(root, `docs/videos/${slug}/video.json`), canonical = read(canonicalFile);
  const receiptFile = path.join(root, portraitReceiptPath), receipt = read(receiptFile);
  assert.equal(receipt.owner_accepted, false);
  assert.equal(receipt.source_files.length, 12);
  assert.equal(new Set(receipt.source_files.map(each => each.path)).size, 12);
  assert.deepEqual(doc.characters.map(each => each.id).sort(), expected.map(each => each[0]).sort());
  const currentLookHash = lookHash(doc);
  assert.equal(currentLookHash, '9b3e6914dbc8d109'); assert.equal(lookHash(canonical), currentLookHash);
  const sources = receipt.source_files.map(entry => { assert.equal(hashFile(inside(root, path.join(root, entry.path))), entry.sha256); return { path: entry.path, sha256: entry.sha256 }; });
  const bindings = new Map();
  const bind = file => { const key = publicPath(file), digest = hashFile(file); assert.ok(!bindings.has(key) || bindings.get(key) === digest); bindings.set(key, digest); };
  for (const file of [projectFile, canonicalFile, receiptFile, ...sources.map(each => path.join(root, each.path)), ...preservedAdoptionNames.map(name => path.join(directory, name))]) bind(file);
  const selected = expected.map(([id, version, digest]) => {
    const key = `${id}-full-body-v${version}`;
    const matches = receipt.assets.filter(each => each.character_id === id && each.view === 'full-body' && each.latest_version);
    assert.equal(matches.length, 1); const asset = matches[0];
    assert.equal(asset.key, key); assert.equal(asset.sha256, digest); assert.equal(asset.owner_accepted, false);
    const imageFile = resolvePublic(asset.path); assert.equal(hashFile(imageFile), digest); bind(imageFile);
    const dimensions = inspectLookPng(bytes(imageFile)); assert.equal(dimensions.width, 1024); assert.equal(dimensions.height, 1536);
    for (const reference of asset.references ?? []) { const file = resolvePublic(reference.path ?? reference.file); assert.equal(hashFile(file), reference.sha256); bind(file); }
    const character = doc.characters.find(each => each.id === id), canonicalCharacter = canonical.characters.find(each => each.id === id);
    const characterKey = sheetKey(character, resolveLook(doc.look));
    assert.equal(sheetKey(canonicalCharacter, resolveLook(canonical.look)), characterKey);
    return { asset, imageFile, dimensions, characterKey, sourceFile: path.join(directory, 'sources', `runtime-look-${id}.source.json`) };
  });
  const inputBindings = [...bindings].map(([file, digest]) => ({ path: file, sha256: digest }));
  const commands = [], commandLogs = [];
  let lease;
  let runtimeTree, manifestHash;
  try {
    // Refuse any pre-existing lease, even stale. Own one handle across every sidecar/CLI write.
    guard({ phase: 'initial' });
    lease = acquireProjectLease(workdir, { owner: 'offline-runtime-look-preparation-20261009' });
    guard({ phase: 'initial', lease });
    mkdirSync(directory, { recursive: true });
    for (const entry of selected) {
      guard({ phase: 'prepared', lease });
      const asset = entry.asset;
      saveNew(entry.sourceFile, { schema_version: 1, character_id: asset.character_id, look_hash: currentLookHash, image_sha256: asset.sha256,
        source_files: sources, prompt_sha256: asset.prompt_sha256, ...(asset.references?.[0] ? { reference_sha256: asset.references[0].sha256 } : {}),
        integration_target: 'normal_runtime_pending_candidate', owner_adoption_recorded_here: false, source_receipt_owner_accepted: false, look_approved: false,
        selection_key: asset.key, provenance_receipt: portraitReceiptPath, provenance_receipt_sha256: hashFile(receiptFile),
        project_file: mediaPath(projectFile), project_sha256: projectSha });
      entry.argv = ['look', 'import', '--file', projectFile, '--workdir', mediaBase, '--character', asset.character_id, '--image', entry.imageFile, '--source', entry.sourceFile];
    }
    async function run(entry, phase) {
      guard({ phase: existsSync(path.join(workdir, 'characters')) ? 'runtime' : 'prepared', lease });
      verifyInputs(inputBindings);
      const argv = [...entry.argv, ...(phase === 'dry-run' ? ['--dry-run'] : [])];
      assert.ok(!argv.some(arg => ['--judge', '--choose', 'approve', 'review-push', 'review-pull'].includes(arg)));
      let stdout = '', stderr = '';
      const startedAt = new Date().toISOString();
      const exitCode = await main(argv, { root, fetch: denyFetch, stdout: { write: value => { stdout += value; } }, stderr: { write: value => { stderr += value; } } });
      const command = { phase, character_id: entry.asset.character_id, started_at: startedAt, finished_at: new Date().toISOString(), argv, exit_code: exitCode, stdout, stderr };
      lease.verify(); assert.equal(stopRequested(workdir), false, 'STOP appeared; preserve existing evidence and stop');
      const log = path.join(directory, 'logs', `runtime-look-${String(commands.length + 1).padStart(2, '0')}-${phase}-${entry.asset.character_id}.json`);
      saveNew(log, command); commands.push(command); commandLogs.push({ path: mediaPath(log), sha256: hashFile(log) });
      assert.equal(exitCode, 0, `${phase} ${entry.asset.character_id}: ${stdout} ${stderr}`);
      assert.equal(fetchAttempts, 0);
      if (phase === 'dry-run') assert.equal(existsSync(path.join(workdir, 'characters')), false, 'dry-run wrote runtime characters');
    }
    for (const entry of selected) await run(entry, 'dry-run');
    for (const entry of selected) await run(entry, 'import');
    manifestHash = hashFile(manifestFile); runtimeTree = tree(path.join(workdir, 'characters'));
    for (const entry of selected) await run(entry, 'exact-rerun');
    assert.equal(hashFile(manifestFile), manifestHash, 'exact reruns changed manifest bytes');
    assert.deepEqual(tree(path.join(workdir, 'characters')), runtimeTree, 'exact reruns changed any candidate/history bytes');
    guard({ phase: 'runtime', lease }); verifyInputs(inputBindings);
    saveNew(path.join(directory, 'logs/runtime-look-commands.json'), commands);
  } finally { lease?.release(); }
  guard({ phase: 'runtime' });
  const manifest = read(manifestFile), commandFile = path.join(directory, 'logs/runtime-look-commands.json');
  const result = { schema_version: 1, created_at: new Date().toISOString(), status: 'normal_runtime_offline_pending_candidates_verified',
    runtime_candidates_integrated: true, owner_adoption_recorded_here: false, budget_authorization_recorded_here: false, look_approved: false, plan_locked: false,
    authorization_context: { source: 'root delegation update before offline integration', material_and_v4_adoption: 'root to bind a separate owner-decision receipt',
      hailuo_period_credit_cap: 26980.8, hailuo_pilot_credit_cap: 316.8, paid_api_authorized: false, look_gate: 'pending real judge; no choose or approval authorized in this task' },
    paid_judge_requested: false, image_generation_requested: false, fetch_attempts: fetchAttempts, paid_requests: 0,
    work_base: '<VIDEO_WORKDIR>', workdir: mediaPath(workdir), project: mediaPath(projectFile), project_sha256: projectSha,
    canonical_project: repoPath(canonicalFile), canonical_project_sha256: hashFile(canonicalFile), canonical_and_v4_look_and_sheet_keys_equal: true,
    look_hash: currentLookHash, source_files: sources, input_bindings: inputBindings,
    runtime_manifest: mediaPath(manifestFile), runtime_manifest_sha256: manifestHash,
    runtime_character_tree: runtimeTree, runtime_character_tree_sha256: sha(json(runtimeTree)),
    preparation_script: repoPath(script), preparation_script_sha256: hashFile(script),
    command_count: commands.length, all_exit_codes_zero: commands.every(each => each.exit_code === 0),
    command_log: mediaPath(commandFile), command_log_sha256: hashFile(commandFile), command_logs: commandLogs,
    same_hash_rerun_preserved_manifest_and_all_candidate_bytes: true, dry_runs_created_no_characters: true,
    preexisting_lease_or_stop: false, own_lease_explicitly_released: true, lease_absent_after_release: true,
    preserved_preexisting_adoption_files: preservedAdoptionNames,
    harness_history: [{ phase: 'initial_guard_before_any_cli_or_runtime_write', exit_code: 1, attempts: 2, reason: 'Sibling agent had added read-only diagnostic files under adoption/20261009, then its file-check receipt. Both guards stopped before any CLI/runtime write. Verified ownership with root and preserved all eight files by SHA before the successful run.' },
      { phase: 'input_validation_before_any_cli_or_runtime_write', exit_code: 1, reason: 'Finalized Shen v3 edit reference uses file, while older reference records use path. Added support for both documented source shapes; validation stopped before any lease or write.' },
      { phase: 'offline_import_and_verification', exit_code: 0 }],
    absent_runtime_states: ['choice', 'approvals', 'keyframes', 'clips', 'media/ledger', 'runtime video.json', 'plan lock'],
    series_store_written: false, existing_staging_modified: false, external_receipt: mediaPath(externalResult),
    candidates: selected.map(entry => { const candidate = manifest.characters[entry.asset.character_id].candidates[0]; return {
      character_id: entry.asset.character_id, key: entry.asset.key, original: entry.asset.path, sha256: entry.asset.sha256, native_dimensions: entry.dimensions,
      source_sidecar: mediaPath(entry.sourceFile), source_sidecar_sha256: hashFile(entry.sourceFile),
      runtime_file: mediaPath(path.join(workdir, candidate.file)), runtime_source: mediaPath(path.join(workdir, candidate.external_import.source_file)),
      candidate_key: candidate.key, character_key: entry.characterKey, candidate_count: 1, n: 1, judge: null, suggested: null, needs_review: true, owner_adoption_recorded_here: false }; }),
    note: 'Pending candidates only. No paid judge, choose, approval, plan mutation, image generation, provider request or series-store write. Original receipt/staging states remain historical; v4 plan is not adopted by this import.' };
  assert.equal(commands.length, 27); assert.equal(fetchAttempts, 0);
  verifyRuntime(result); verifyInputs(inputBindings);
  saveNew(externalResult, result); saveNew(resultFile, result); saveNew(markdownFile, markdown(result));
  console.log(json({ status: result.status, candidates: 9, sources: 12, commands: 27, fetch_attempts: 0, paid_requests: 0, look_approved: false, manifest_sha256: manifestHash }));
}
