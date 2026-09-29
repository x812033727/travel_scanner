#!/usr/bin/env node
// Dated correction workflow. Sends only the final-cut review; never a publish gate.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { ROOT, lexiconFile } from '../../../../../tools/video/core/paths.mjs';
import { siteClient } from '../../../../../tools/video/shorts/site.mjs';
import { checkAudio, audioHash, buildClips } from '../../../../../tools/video/shorts/check.mjs';
import { runQa, siteHistory } from '../../../../../tools/video/shorts/qa.mjs';
import { evidenceRole, finalReview, projectBody, upload } from '../../../../../tools/video/shorts/push.mjs';
import { phrasesOf, sha256, validate } from '../../../../../tools/video/shorts/core.mjs';

const read = (file) => JSON.parse(readFileSync(file, 'utf8'));
const optional = (file) => existsSync(file) ? read(file) : null;
const digest = (file) => sha256(readFileSync(file));
const sameQa = (review, qa) => review?.payload?.qa?.final_sha256 === qa.final_sha256 && review.payload.qa.items?.length === qa.items.length && qa.items.every((item, index) => ['id', 'ok', 'detail'].every((key) => review.payload.qa.items[index][key] === item[key]));
const save = (file, value) => {
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
};
const { values } = parseArgs({ options: {
  manifest: { type: 'string' }, action: { type: 'string' }, receipts: { type: 'string' },
  slug: { type: 'string' },
} });
if (!values.manifest || !values.receipts || !['audio', 'qa', 'submit', 'confirm'].includes(values.action)) {
  throw new Error('Usage: --manifest external.json --receipts external-dir --action audio|qa|submit|confirm [--slug slug]');
}
const manifest = read(path.resolve(values.manifest));
const entries = (Array.isArray(manifest) ? manifest : manifest.entries).filter((entry) => !values.slug || entry.slug === values.slug);
if (!entries.length) throw new Error('No builds selected');
const client = siteClient(); // Credentials stay inside the existing client.
let history;
let settings;
if (values.action === 'qa') {
  settings = await client.settings();
  history = await siteHistory(client);
}
const lexicon = optional(lexiconFile(ROOT));
for (const entry of entries) {
  const directory = path.resolve(entry.directory);
  const doc = read(path.join(directory, 'script.json'));
  if (doc.slug !== entry.slug) throw new Error(`Manifest slug differs from script: ${entry.slug}`);
  const errors = validate(doc);
  if (errors.length) throw new Error(`${doc.slug}: ${errors.join('; ')}`);
  const finalFile = path.join(directory, 'upload/final.mp4');
  const finalSha256 = digest(finalFile);
  const documentSha256 = digest(path.join(directory, 'script.json'));
  const phrases = phrasesOf(doc);
  const hasCurrentWords = (check) => check?.results?.length === phrases.length && check.results.every((row, index) => row.index === index && row.text === phrases[index]);
  if (entry.final_sha256 && entry.final_sha256 !== finalSha256) throw new Error(`${doc.slug}: final changed after manifest`);
  if (entry.document_sha256 && entry.document_sha256 !== documentSha256) throw new Error(`${doc.slug}: script changed after manifest`);
  const receiptFile = path.join(path.resolve(values.receipts), `${values.action}-${doc.slug}.json`);
  let result;
  if (values.action === 'audio') {
    const old = optional(path.join(directory, 'check.json'));
    const clipsHash = audioHash(buildClips(directory, phrases.length));
    // Preserve a completed failed check too: unchanged audio is not repeatedly judged until lucky.
    result = old && hasCurrentWords(old) && old.audio_sha256 === clipsHash && old.lines === phrases.length && old.checked === old.lines
      ? old : await checkAudio({ directory, client, lexicon });
    console.log(`${doc.slug}: ${result.checked} phrases, ${result.flagged} flagged`);
  } else if (values.action === 'qa') {
    const check = optional(path.join(directory, 'check.json'));
    if (check && !hasCurrentWords(check)) throw new Error(`${doc.slug}: narration check is of different words; run audio first`);
    result = await runQa({ directory, client, settings, history });
    if (digest(finalFile) !== finalSha256 || digest(path.join(directory, 'script.json')) !== documentSha256) throw new Error(`${doc.slug}: build changed while QA ran`);
    const inputSha256 = Object.fromEntries(['check.json', 'verify.json', 'checks.json'].map((file) => [file, existsSync(path.join(directory, file)) ? digest(path.join(directory, file)) : null]));
    save(path.join(directory, 'qa-binding.json'), { document_sha256: documentSha256, final_sha256: finalSha256, qa_sha256: digest(path.join(directory, 'qa.json')), input_sha256: inputSha256 });
    console.log(`${doc.slug}: ${result.items.filter((item) => item.ok).length}/12; ${result.items.filter((item) => !item.ok).map((item) => `${item.id}: ${item.detail}`).join(' | ')}`);
  } else if (values.action === 'submit') {
    const qa = read(path.join(directory, 'qa.json'));
    const facts = read(path.join(directory, 'verify.json'));
    const qaBinding = read(path.join(directory, 'qa-binding.json'));
    if (qa.final_sha256 !== finalSha256) throw new Error(`${doc.slug}: QA is not bound to this final`);
    if (qaBinding.document_sha256 !== documentSha256 || qaBinding.final_sha256 !== finalSha256 || qaBinding.qa_sha256 !== digest(path.join(directory, 'qa.json'))) throw new Error(`${doc.slug}: QA is not bound to this script and report`);
    for (const file of ['check.json', 'verify.json', 'checks.json']) {
      if (!qaBinding.input_sha256?.[file] || qaBinding.input_sha256[file] !== digest(path.join(directory, file))) throw new Error(`${doc.slug}: ${file} changed after QA`);
    }
    if (facts.document_sha256 !== documentSha256 || facts.ok !== true) throw new Error(`${doc.slug}: facts are not verified for this script`);
    const before = await client.project(doc.slug);
    if (!before) throw new Error(`${doc.slug}: correction target does not exist`);
    if (before.youtube_video_id || before.dropped_at) throw new Error(`${doc.slug}: target has been uploaded or dropped; recheck its state before correcting it`);
    await client.report(doc.slug, projectBody({ doc, qa, check: optional(path.join(directory, 'check.json')), report: null, stage: 'final' }));
    const files = [];
    const roles = new Set();
    const attach = async (file, role) => {
      if (!existsSync(file)) return;
      if (roles.has(role)) role = `${role.slice(0, 31)}_${digest(file).slice(0, 8)}`;
      roles.add(role);
      files.push(await upload(client, doc.slug, file, role));
    };
    await attach(finalFile, 'preview');
    await attach(path.join(directory, 'upload/cover.png'), 'thumbnail');
    await attach(path.join(directory, existsSync(path.join(directory, 'contact-sheet.png')) ? 'contact-sheet.png' : 'contact.png'), 'contact_sheet');
    for (const evidence of doc.evidence ?? []) {
      const file = path.join(directory, 'evidence', evidence.path);
      if (!existsSync(file) || digest(file) !== evidence.sha256) throw new Error(`${doc.slug}: evidence changed: ${evidence.path}`);
      await attach(file, evidenceRole(evidence.path));
    }
    for (const [file, role] of [['script.json', 'evidence_script'], ['verify.json', 'evidence_verify'], ['check.json', 'evidence_narration'], ['checks.json', 'evidence_measurements'], ['layout-evidence.json', 'evidence_layout'], ['qa.json', 'evidence_qa'], ['qa-binding.json', 'evidence_qa_binding'], ['upload/zh-TW.srt', 'evidence_captions']]) {
      await attach(path.join(directory, file), role);
    }
    if (digest(finalFile) !== finalSha256 || digest(path.join(directory, 'script.json')) !== documentSha256 || files.find((file) => file.role === 'preview')?.sha256 !== finalSha256 || files.find((file) => file.role === 'evidence_script')?.sha256 !== documentSha256) {
      throw new Error(`${doc.slug}: build changed during upload; rerun verification and QA`);
    }
    const sent = await client.submit(doc.slug, {
      ...finalReview({ doc, qa, usage: optional(path.join(directory, 'usage.json')), timeline: read(path.join(directory, 'timeline.json')), finalSha256 }), files,
    });
    const after = await client.project(doc.slug);
    const found = after?.reviews?.find((review) => review.gate === 'final' && review.content_sha256 === finalSha256 && review.status !== 'superseded');
    if (!found) throw new Error(`${doc.slug}: reloaded project does not contain submitted final hash`);
    if (!sameQa(found, qa) || files.some((file) => !found.files?.some((saved) => saved.role === file.role && saved.sha256 === file.sha256))) throw new Error(`${doc.slug}: reloaded QA or attachments differ from the submitted review`);
    result = { review_id: found.id, status: found.status, note: found.note ?? null, submitted_status: sent.status, files: files.map(({ role, sha256 }) => ({ role, sha256 })), publish_submitted: false };
    console.log(`${doc.slug}: final ${found.status}, reloaded hash confirmed`);
  } else {
    const project = await client.project(doc.slug);
    const found = project?.reviews?.find((review) => review.gate === 'final' && review.content_sha256 === finalSha256 && review.status !== 'superseded');
    const qa = read(path.join(directory, 'qa.json'));
    if (!found || !sameQa(found, qa) || !found.files?.some((file) => file.role === 'preview' && file.sha256 === finalSha256)) throw new Error(`${doc.slug}: current backend final, QA or preview hash differs`);
    result = { found: true, qa_matches: true, preview_matches: true, title: project.title, status: found.status, review_id: found.id, stage: project.stage };
    console.log(`${doc.slug}: ${JSON.stringify(result)}`);
  }
  save(receiptFile, { slug: doc.slug, action: values.action, checked_at: new Date().toISOString(), final_sha256: finalSha256, document_sha256: documentSha256, result });
}
