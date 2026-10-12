#!/usr/bin/env node
// Refresh the external delivery index from actual checked files. No network, upload, or approval.
import { createHash } from 'node:crypto';
import { createReadStream, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: { 'output-root': { type: 'string' }, 'source-map': { type: 'string' } } });
const root = path.resolve(values['output-root'] ?? path.join(homedir(), 'mokaair-work/curio-five-recuts-20261012'));
const sourceMapPath = path.resolve(values['source-map'] ?? path.join(root, 'source-map.json'));
const slugs = ['curio-h02', 'curio-u02', 'curio-h03', 'curio-l08', 'curio-h01'];
const locales = ['zh-TW', 'en', 'ja', 'ko'];
const read = (p) => JSON.parse(readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const has = (p) => existsSync(p) && statSync(p).isFile();
const absolute = (p) => path.resolve(p).replaceAll('\\', '/');
const link = (label, p) => `[${label}](<${absolute(p)}>)`;
const titleCell = (s) => String(s).replaceAll('|', '\\|').replaceAll('\n', ' ');
const inside = (file, base) => { const r = path.relative(base, file); return r === '' || (!r.startsWith('..') && !path.isAbsolute(r)); };
const hashCache = new Map();
async function sha(file) {
  const p = path.resolve(file), statBefore = statSync(p), key = `${p}:${statBefore.size}:${statBefore.mtimeMs}`;
  if (hashCache.has(key)) return hashCache.get(key);
  const h = createHash('sha256');
  for await (const chunk of createReadStream(p)) h.update(chunk);
  const after = statSync(p);
  if (after.size !== statBefore.size || after.mtimeMs !== statBefore.mtimeMs) throw new Error(`File changed while hashing: ${p}`);
  const result = h.digest('hex'); hashCache.set(key, result); return result;
}
function inspectJson(file, errors) {
  if (!has(file)) { errors.push(`Missing ${file}`); return null; }
  try { return read(file); } catch (e) { errors.push(`Invalid JSON ${file}: ${e.message}`); return null; }
}
const map = has(sourceMapPath) ? read(sourceMapPath) : { episodes: [] };
const entries = [];
for (const slug of slugs) {
  const base = path.join(root, slug), upload = path.join(base, 'upload'), source = map.episodes.find((e) => e.slug === slug);
  const qaFile = path.join(base, 'qa.json'), metadataFile = path.join(upload, 'metadata.json');
  const errors = [], qa = has(qaFile) ? inspectJson(qaFile, errors) : null;
  const metadata = has(metadataFile) ? inspectJson(metadataFile, errors) : null;
  const originalMetadata = source && has(source.metadata) ? read(source.metadata) : null;
  const item = {
    slug, title: metadata?.title ?? originalMetadata?.title ?? slug,
    status: qa?.ok ? 'validating-artifacts' : qa?.status ?? 'awaiting-render',
    technical_qa_passed: false, current_artifact_hashes_verified: false,
    final: path.join(upload, 'final.mp4'), qa: qaFile, metadata: metadataFile,
    source_provenance: path.join(base, 'source-provenance.json'),
    localized_descriptions: Object.fromEntries(locales.map((l) => [l, path.join(upload, `description.${l}.txt`)])),
    verified_thumbnail: null,
    captions: Object.fromEntries(locales.map((l) => [l, path.join(upload, 'captions', `${l}.srt`)])),
    dubs: Object.fromEntries(locales.slice(1).map((l) => [l, path.join(upload, 'dubs', `${l}.wav`)])),
    available_captions: locales.filter((l) => has(path.join(upload, 'captions', `${l}.srt`))),
    available_dubs: locales.slice(1).filter((l) => has(path.join(upload, 'dubs', `${l}.wav`))),
    original_review_notes: Object.fromEntries(locales.map((l) => [l, qa?.review_limitations?.original_locale_notes?.[l] ?? source?.locales?.[l]?.source_review_note ?? null])),
    opening_audio: {}, owner_playback_verified: false, youtube_endscreens_configured: false, uploaded: false, published: false, errors,
  };
  for (const locale of locales) {
    const directory = path.join(base, 'intro', locale), checkFile = path.join(directory, 'check.json');
    const check = has(checkFile) ? read(checkFile) : null;
    const appliedCheck = qa?.audio?.[locale]?.opening_check ?? null;
    const resolutions = (appliedCheck?.second_opinion_evidence?.entries ?? []).map((entry) => {
      const evidence = has(entry.file) ? read(entry.file) : null;
      return { line: entry.line, outcome: evidence?.outcome ?? 'evidence-missing', qualified_review: evidence?.qualified_review ?? null, file: entry.file, sha256: entry.sha256 };
    });
    item.opening_audio[locale] = { report_exists: !!check, original_report_ok: check?.ok ?? false, original_flags: check?.flags ?? [], second_opinion_evidence_exists: has(path.join(directory, 'second-opinion.json')), applied_check: appliedCheck, resolutions };
  }
  if (qa?.ok) {
    try {
      if (!metadata || !has(item.source_provenance)) errors.push('Missing metadata/source provenance');
      if (!has(item.final)) errors.push('Missing final.mp4');
      else {
        const actual = await sha(item.final); item.final_sha256 = actual;
        if (actual !== qa.final_sha256 || actual !== metadata?.final_sha256) errors.push('Final SHA differs from QA/metadata');
      }
      for (const locale of locales) {
        const file = item.captions[locale];
        if (!has(file)) errors.push(`Missing ${locale} captions`);
        else if (await sha(file) !== qa.captions?.[locale]?.sha256 || metadata?.caption_bindings?.[locale]?.final_sha256 !== qa.final_sha256) errors.push(`Changed or unbound ${locale} captions`);
      }
      for (const locale of locales.slice(1)) {
        const file = item.dubs[locale], binding = metadata?.dubs?.find((d) => d.locale === locale);
        if (!has(file)) errors.push(`Missing ${locale} WAV`);
        else if (await sha(file) !== qa.audio?.[locale]?.sha256 || binding?.sha256 !== qa.audio?.[locale]?.sha256 || binding?.final_sha256 !== qa.final_sha256) errors.push(`Changed or unbound ${locale} WAV`);
        if (qa.audio?.[locale]?.samples !== qa.total_frames * 1600) errors.push(`${locale} WAV sample count mismatch`);
      }
      for (const locale of locales) {
        const text = locale === 'zh-TW' ? metadata : metadata?.localizations?.[locale];
        if (!text?.title || !text?.description || Array.from(text.title).length > 100 || Array.from(text.description).length > 5000) errors.push(`${locale} metadata missing or too long`);
        const textFile = path.join(upload, `description.${locale}.txt`);
        if (!has(textFile) || readFileSync(textFile, 'utf8') !== `${text.title}\n\n${text.description}\n`) errors.push(`${locale} description file differs from metadata`);
      }
      const endscreenFile = path.join(upload, 'endscreen-setup.json'), endscreen = inspectJson(endscreenFile, errors);
      if (!endscreen || endscreen.end_frame !== qa.total_frames || endscreen.start_frame !== qa.total_frames - 480 || endscreen.start_seconds !== qa.total_frames / 30 - 16 || endscreen.duration_seconds !== 16 || endscreen.template_video_id !== 'oxEtlA8GWas' || endscreen.configured !== false) errors.push('Endscreen must start on the clear v4 canvas (last 16 seconds); run endscreen-timing.mjs after final QA');
      else {
        const setupSha = await sha(endscreenFile);
        if (metadata?.endscreen_setup?.sha256 !== setupSha || qa.endscreen_timing?.setup_sha256 !== setupSha || metadata.endscreen_setup.duration_seconds !== 16 || qa.endscreen_timing.final_sha256 !== qa.final_sha256) errors.push('Endscreen setup is not bound to metadata/QA after timing correction');
        item.endscreen = { file: endscreenFile, start_seconds: endscreen.start_seconds, end_seconds: endscreen.end_seconds, duration_seconds: 16, setup_sha256: setupSha };
      }
      const sums = inspectJson(path.join(upload, 'checksums.json'), errors);
      for (const [relative, expected] of Object.entries(sums ?? {})) {
        const file = path.resolve(upload, relative);
        if (!inside(file, upload) || !has(file) || await sha(file) !== expected) errors.push(`Invalid checksum entry: ${relative}`);
        else if (file === path.resolve(upload, 'thumbnail.jpg')) item.verified_thumbnail = { file, sha256: expected };
      }
      if (!item.verified_thumbnail && metadata?.thumbnail && originalMetadata?.thumbnail && source?.metadata) {
        const file = path.resolve(upload, metadata.thumbnail), originalRoot = path.dirname(source.metadata);
        const original = path.resolve(originalRoot, originalMetadata.thumbnail);
        if (inside(file, upload) && inside(original, originalRoot) && has(file) && has(original)) {
          const actual = await sha(file), sourceSha = await sha(original);
          if (actual === sourceSha) item.verified_thumbnail = { file, sha256: actual, verification: 'matches-original-thumbnail', source_file: original };
        }
      }
      for (const [file, expected] of Object.entries(qa.source_hashes_after ?? {})) {
        if (inside(file, path.join(base, 'intro')) && (!has(file) || await sha(file) !== expected)) errors.push(`Opening evidence changed since final QA: ${file}`);
      }
      if (metadata?.video_id !== null || metadata?.uploaded !== false || metadata?.published !== false) errors.push('Output metadata inherited an upload/publication identity');
      if (qa.full_av_decode !== 'passed' || qa.decoded_frames !== qa.total_frames || !qa.retained_body_picture_unchanged || !qa.sources_unchanged) errors.push('Incomplete technical QA evidence');
      item.duration_seconds = qa.duration_seconds; item.total_frames = qa.total_frames; item.metadata_limits = qa.metadata_limits ?? metadata?.metadata_limits;
      item.current_artifact_hashes_verified = errors.length === 0;
      item.technical_qa_passed = errors.length === 0;
      item.status = errors.length ? 'artifact-validation-failed' : 'technical-qa-passed';
    } catch (error) { errors.push(error.message); item.status = 'artifact-validation-failed'; }
  }
  entries.push(item);
}
const index = { schema_version: 1, generated_at: new Date().toISOString(), output_root: root, episodes: entries, total_episodes: 5, technical_qa_passed: entries.filter((e) => e.technical_qa_passed).length, expected_cc_files: 20, expected_dub_wavs: 15, owner_playback_verified: false, youtube_endscreens_configured: false, uploaded: false, published: false };
mkdirSync(root, { recursive: true });
writeFileSync(path.join(root, 'delivery-index.json'), `${JSON.stringify(index, null, 2)}\n`);
const rows = entries.map((e) => `| ${e.slug} | ${titleCell(e.title)} | ${e.status} | ${e.available_captions.length}/4 | ${e.available_dubs.length}/3 | ${e.duration_seconds?.toFixed(3) ?? '—'} |`);
const parts = [
  '# 奇聞檔案局五支新版影片交付索引', '',
  `更新時間（UTC）：${index.generated_at}。本表由實際 QA 與檔案雜湊產生。技術驗證通過：${index.technical_qa_passed}/5。`, '',
  '站主完整試播、YouTube Studio 片尾連結設定、重新上傳及公開發布均尚未確認。技術 QA 通過不能代替這些完成狀態。', '',
  '| 影片 | 標題 | 實際狀態 | CC | 配音 WAV | 秒數 |', '| --- | --- | --- | --- | --- | --- |', ...rows, '',
];
for (const e of entries) {
  parts.push(`## ${e.slug}`, '', `${e.title}`, '');
  if (e.technical_qa_passed) parts.push(`- ${link('新版完整影片', e.final)}`, `- ${link('技術 QA', e.qa)} · ${link('來源與原始審稿紀錄', e.source_provenance)} · ${link('上架欄位', e.metadata)}`);
  else parts.push(`目前狀態：${e.status}。現存中間檔案不代表可以上傳。`);
  if (e.technical_qa_passed) {
    parts.push(`- 標題與說明文字：${locales.map((l) => link(l, e.localized_descriptions[l])).join(' · ')}`);
    if (e.verified_thumbnail) parts.push(`- ${link('縮圖（已核對 SHA256）', e.verified_thumbnail.file)}`);
    parts.push(`- CC：${locales.map((l) => link(l, e.captions[l])).join(' · ')}`, `- 配音：${locales.slice(1).map((l) => link(l, e.dubs[l])).join(' · ')}`);
    parts.push(`- ${link('片尾設定', e.endscreen.file)}：${e.endscreen.start_seconds.toFixed(3)}–${e.endscreen.end_seconds.toFixed(3)} 秒，匯入 oxEtlA8GWas 範本，配置最新上傳／最適合觀眾／訂閱。`);
  }
  for (const [locale, note] of Object.entries(e.original_review_notes)) if (note) parts.push(`- 保留原始 ${locale} 審稿註記：${typeof note === 'string' ? note : JSON.stringify(note)}`);
  for (const [locale, opening] of Object.entries(e.opening_audio)) {
    const applied = opening.applied_check?.second_opinion_resolved ?? [];
    if (applied.length) {
      const labels = { 'resolved-exact': '獨立逐字結果一致', 'resolved-numeric': '獨立逐字結果的數字寫法一致', 'resolved-reviewed-homophone': '限本次 WAV 的日語同音字覆核通過' };
      const detail = opening.resolutions.map((r) => `${r.line}：${labels[r.outcome] ?? r.outcome}`).join('；');
      parts.push(`- ${locale} 開場原始自動聽辨旗標保留；${detail || applied.join('、')}。每筆結論綁定原音檔與證據雜湊，沒有改列成原始聽辨全過或站主聽過。`);
    }
  }
  if (e.errors.length) parts.push('', ...e.errors.map((s) => `- 待處理：${s}`));
  parts.push('');
}
writeFileSync(path.join(root, 'DELIVERY-INDEX.md'), parts.join('\n'));
console.log(JSON.stringify({ technical_qa_passed: index.technical_qa_passed, total: 5, index: path.join(root, 'delivery-index.json'), readme: path.join(root, 'DELIVERY-INDEX.md'), statuses: entries.map((e) => ({ slug: e.slug, status: e.status, errors: e.errors })) }, null, 2));
