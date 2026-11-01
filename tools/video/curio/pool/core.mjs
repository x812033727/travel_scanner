// 奇聞檔案局素材池：把題庫、已製作的集數、分支上的草稿與新批次讀成同一份去重後的候選池。
// 架構照原來如此事務所的素材池（PR x812033727/travel_scanner#1971 的 tools/video/so-thats-why/pool），
// 輸入格式與規則改成奇聞檔案局的：一題一個 topic-check 檔、已製作的集鎖定、長片 8–13 分鐘。
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
export const DIR = 'docs/videos/history-curiosity/pool';
export const BANK = 'docs/videos/history-curiosity';
export const TOOL_DIR = 'tools/video/curio/pool';
export const LONG_MIN = 8;
export const LONG_MAX = 13;
export const hash = (value) => createHash('sha256').update(value).digest('hex');
const parse = (root, file) => JSON.parse(readFileSync(path.join(root, file), 'utf8'));
const exists = (root, file) => existsSync(path.join(root, file));

export const normalizeQuestion = (text) => text.normalize('NFKC').toLowerCase().replace(/[\p{P}\p{S}\p{Z}\s]/gu, '');
export function normalizeUrl(value) {
  const url = new URL(value);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || /^(localhost|127\.|0\.|10\.|192\.168\.|169\.254\.|\[)/.test(url.hostname)) throw new Error(`Not a public source URL: ${value}`);
  for (const key of [...url.searchParams.keys()]) if (/^(utm_|fbclid$|gclid$)/.test(key)) url.searchParams.delete(key);
  url.hash = '';
  return url.href;
}

// Same parser as the so-thats-why pool; `<br>` and table pipes end a URL, so table cells split cleanly.
export function urlsIn(text) {
  const found = [];
  for (const match of text.matchAll(/https?:\/\//g)) {
    let value = ''; let depth = 0;
    for (const char of text.slice(match.index)) {
      if (/[\s<>"|；，。、`（）「」『』\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(char)) break;
      if (char === '(') depth += 1;
      if (char === ')') { if (!depth) break; depth -= 1; }
      value += char;
    }
    value = value.replace(/[.,;:\]*_]+$/, '');
    if (/\/nhttps?:|\/n\d{4}$/.test(value) || value.length < 12) continue;
    found.push(value);
  }
  return [...new Set(found)];
}

// topic-checks 一題一檔：整檔都是這一題的，不能像原來如此的共用檔那樣切 `## <id>` 小節（那樣會回傳空字串、默默丟掉所有網址）。
// 〈連結檢查〉表裡不是 200 的狀態記成這次讀取的限制。
export function linkStatuses(text) {
  const start = /^##\s*連結檢查[^\n]*$/m.exec(text);
  if (!start) return new Map();
  const body = text.slice(start.index + start[0].length);
  const end = /^##\s/m.exec(body);
  const section = end ? body.slice(0, end.index) : body;
  const statuses = new Map();
  for (const line of section.split('\n')) {
    if (!line.startsWith('|')) continue;
    const cells = line.split('|').map((cell) => cell.trim()).filter(Boolean);
    const urls = urlsIn(line);
    if (!urls.length || cells.length < 2) continue;
    const status = cells[cells.length - 1];
    for (const url of urls) if (!/^200\b/.test(status) && !status.startsWith('http')) statuses.set(url, status);
  }
  return statuses;
}

export const EPISODE_STATES = ['episode_dir', 'remake_dir', 'branch_draft', 'planned_w_axis', 'bank_scripted'];

function episodeDirs(root) {
  const base = path.join(root, 'docs/videos');
  if (!existsSync(base)) return [];
  return readdirSync(base).filter((name) => /^curio-[hmpulsfgw]\d+(?:-|$)/.test(name) && statSync(path.join(base, name)).isDirectory())
    .map((name) => ({ id: name.split('-')[1].toUpperCase(), dir: `docs/videos/${name}` }));
}

export function validateEditorial(row) {
  const value = row.editorial;
  if (!value || !['episode_core', 'chapter'].includes(value.role) || typeof value.payoff !== 'string' || !value.payoff.trim() || typeof value.visual !== 'string' || !value.visual.trim()) throw new Error(`${row.id}: invalid editorial role, payoff or visual`);
  const minutes = value.minutes;
  if (!Array.isArray(minutes) || minutes.length !== 2 || minutes.some((n) => !Number.isFinite(n) || n <= 0 || n > LONG_MAX) || minutes[0] > minutes[1]) throw new Error(`${row.id}: editorial.minutes must be [lo, hi] within 0–${LONG_MAX}`);
  if (value.role === 'episode_core' && minutes[1] < LONG_MIN) throw new Error(`${row.id}: an episode core must be able to reach ${LONG_MIN} minutes; mark it a chapter instead of padding`);
}

export function intake(root = ROOT) {
  const inputs = new Map();
  const bind = (file) => inputs.set(file, hash(readFileSync(path.join(root, file))));
  const sources = new Map();
  const records = [];
  const notAdded = [];
  const sourceId = (url, reading) => {
    const canonicalUrl = normalizeUrl(url);
    const id = `SRC-${hash(canonicalUrl).slice(0, 16)}`;
    if (!sources.has(id)) sources.set(id, { id, url: canonicalUrl, readings: [] });
    const source = sources.get(id);
    const item = { ...reading, original_url: url };
    if (!source.readings.some((old) => JSON.stringify(old) === JSON.stringify(item))) source.readings.push(item);
    return id;
  };
  const legacyRefs = (id, file, text, how) => {
    const statuses = linkStatuses(text);
    const refs = [];
    for (const url of urlsIn(text)) {
      let sid;
      try {
        sid = sourceId(url, { origin: `legacy:${id}`, title: '既有查核或研究檔所列來源；題名待當期讀頁補核', publisher: new URL(url).hostname, accessed_on: null, imported_on: '2026-11-01', read_via: how, reading_scope: `${file} 列出的來源；不表示本輪讀過外站`, locator: file, summary: '保留既有查核來源的指向；當期可達性與支持關係要重查。', rights: 'LINK_ONLY_NO_EXTERNAL_TEXT_COPIED', ...(statuses.has(url) ? { limitations: `原檔連結檢查：${statuses.get(url)}` } : {}) });
      } catch { continue; }
      refs.push({ source_id: sid, origin: `legacy:${id}`, locator: file, supports: '既有題級查核或集數研究的來源入口；不是當期逐主張核准。' });
    }
    return refs;
  };

  // 1. 題庫（topics.json 與 F/G 的 topics-fg.json）。
  const axes = {};
  const bank = new Map();
  for (const file of [`${BANK}/topics.json`, `${BANK}/topics-fg.json`]) {
    if (!exists(root, file)) continue;
    bind(file);
    const doc = parse(root, file);
    Object.assign(axes, doc.series?.axes ?? {});
    for (const topic of doc.topics) {
      if (bank.has(topic.id)) throw new Error(`Duplicate bank topic ${topic.id}`);
      bank.set(topic.id, { ...topic, bank_file: file });
    }
  }
  axes.W ??= '生意與品牌的奇聞';

  // 2. 哪些題已經做成集、在別的分支上有草稿，或已排進 W 軸：這些題只當去重對象，不能被併掉或淘汰。
  const production = new Map();
  const note = (id, state, locator) => {
    if (!production.has(id)) production.set(id, { states: new Set(), locators: [] });
    production.get(id).states.add(state);
    production.get(id).locators.push(locator);
  };
  const extra = new Map(); // id -> { question, answer_target, axis }
  for (const { id, dir } of episodeDirs(root)) {
    note(id, 'episode_dir', dir);
    if (exists(root, `${dir}/video.json`)) {
      bind(`${dir}/video.json`);
      const video = parse(root, `${dir}/video.json`);
      const title = (video.youtube?.title ?? video.title ?? '').replace(/｜奇聞檔案局$/, '');
      if (title && !bank.has(id) && !extra.has(id)) extra.set(id, { question: title, answer_target: '', axis: id[0] });
    }
  }
  const remakeDir = `${BANK}/remake-20261020`;
  if (exists(root, remakeDir)) {
    for (const name of readdirSync(path.join(root, remakeDir)).filter((n) => /^curio-s\d+$/.test(n)).sort()) {
      const id = name.split('-')[1].toUpperCase();
      const file = `${remakeDir}/${name}/video.json`;
      note(id, 'remake_dir', `${remakeDir}/${name}`);
      if (exists(root, file)) {
        bind(file);
        const video = parse(root, file);
        const title = (video.youtube?.title ?? video.title ?? '').replace(/｜奇聞檔案局$/, '');
        if (title && !bank.has(id) && !extra.has(id)) extra.set(id, { question: title, answer_target: '', axis: 'S' });
      }
    }
  }
  const branchRefs = new Map();
  const branchFile = `${DIR}/legacy/branch-episodes.json`;
  if (exists(root, branchFile)) {
    bind(branchFile);
    for (const episode of parse(root, branchFile).episodes) {
      const locator = `${episode.branch}@${episode.commit.slice(0, 8)}:docs/videos/${episode.slug}`;
      note(episode.id, episode.title ? 'branch_draft' : 'branch_research', locator);
      if (episode.title && !bank.has(episode.id) && !extra.has(episode.id)) extra.set(episode.id, { question: episode.title, answer_target: episode.question && episode.question !== episode.title ? episode.question : '', axis: episode.id[0] });
      const refs = [];
      for (const { url, file } of episode.urls) {
        const where = `${episode.branch}@${episode.commit.slice(0, 8)}:${file}`;
        let sid;
        try { sid = sourceId(url, { origin: `legacy:${episode.id}`, title: '分支上集數研究檔所列來源；題名待當期讀頁補核', publisher: new URL(url).hostname, accessed_on: null, imported_on: '2026-11-01', read_via: 'git_branch_file', reading_scope: `${where} 列出的來源；不表示本輪讀過外站`, locator: where, summary: '保留分支草稿研究的來源指向；當期可達性與支持關係要重查。', rights: 'LINK_ONLY_NO_EXTERNAL_TEXT_COPIED' }); } catch { continue; }
        refs.push({ source_id: sid, origin: `legacy:${episode.id}`, locator: where, supports: '分支草稿的研究來源；不是當期逐主張核准。' });
      }
      branchRefs.set(episode.id, refs);
    }
  }
  const wFile = `${DIR}/legacy/w-axis.json`;
  if (exists(root, wFile)) {
    bind(wFile);
    for (const episode of parse(root, wFile).episodes) {
      note(episode.id, 'planned_w_axis', episode.locator);
      if (!bank.has(episode.id) && !extra.has(episode.id)) extra.set(episode.id, { question: episode.question, answer_target: '', axis: 'W' });
    }
  }
  for (const topic of bank.values()) if (['scripted', 'published'].includes(topic.status)) note(topic.id, 'bank_scripted', topic.bank_file);

  // 3. 每一題（題庫題＋題庫外的集數）都成為一筆 legacy 原始紀錄。
  const ids = [...new Set([...bank.keys(), ...extra.keys()])].sort((a, b) => a.localeCompare(b, 'en', { numeric: true }));
  for (const id of ids) {
    const topic = bank.get(id);
    const made = production.get(id);
    const states = made ? [...made.states].sort() : [];
    const locked = states.some((state) => EPISODE_STATES.includes(state));
    const refs = [];
    const check = `${BANK}/topic-checks/${id}.md`;
    if (exists(root, check)) { bind(check); refs.push(...legacyRefs(id, check, readFileSync(path.join(root, check), 'utf8'), 'local_topic_check_file')); }
    for (const locator of made?.locators ?? []) {
      if (!locator.startsWith('docs/videos/curio-')) continue;
      for (const name of ['research.md', 'claims.md', 'brief.md']) {
        const file = `${locator}/${name}`;
        if (!exists(root, file)) continue;
        bind(file);
        refs.push(...legacyRefs(id, file, readFileSync(path.join(root, file), 'utf8'), 'local_episode_research_file'));
      }
    }
    refs.push(...(branchRefs.get(id) ?? []));
    const unique = [...new Map(refs.map((ref) => [`${ref.source_id}:${ref.locator}`, ref])).values()];
    const fromExtra = extra.get(id);
    const axis = topic?.axis ?? fromExtra.axis;
    records.push({
      id, origin: 'legacy', axis, domain: `${axis} ${axes[axis] ?? ''}`.trim(),
      question: topic?.title ?? fromExtra.question,
      hook: topic?.hook ?? '',
      case_key: `legacy.${id.toLowerCase()}`,
      answer_target: (topic?.finding ?? fromExtra.answer_target).slice(0, 800),
      scope: topic ? [topic.facts_to_verify?.length ? `待查：${topic.facts_to_verify.join('；')}` : '', topic.risk && topic.risk !== 'none' ? `風險：${topic.risk}` : ''].filter(Boolean).join('。') || '沿用題目卡；製作前逐條查核。' : '以集數工作目錄的企劃與查核為準。',
      bank_status: topic?.status ?? null,
      production: { states, locators: [...new Set(made?.locators ?? [])] },
      locked,
      source_refs: unique,
      premise_status: locked ? 'locked_produced' : topic?.status === 'checked' ? 'legacy_checked' : unique.length ? 'legacy_research_unreviewed' : 'legacy_card_unchecked',
      eligible: !locked && unique.length > 0,
      notes: [topic?.note, topic && topic.status === 'candidate' ? '題目卡是起草時憑既有知識寫的，還沒查核。' : '', '既有來源只當研究入口，本輪沒有重讀外站。'].filter(Boolean).join(' '),
      local_references: [topic?.bank_file, ...(made?.locators ?? [])].filter(Boolean),
    });
  }

  // 4. 新批次：每題要有可讀來源與片長估計。
  const batchDir = path.join(root, DIR, 'batches');
  const batches = existsSync(batchDir) ? readdirSync(batchDir).filter((file) => file.endsWith('.json')).sort() : [];
  for (const name of batches) {
    const file = `${DIR}/batches/${name}`;
    bind(file);
    const batch = parse(root, file);
    if (!batch.batch_id || !Array.isArray(batch.sources) || !Array.isArray(batch.candidates)) throw new Error(`Bad batch: ${file}`);
    for (const item of batch.not_added ?? []) {
      if (!item.question || !item.reason) throw new Error(`${file}: rejected suggestions need a question and reason`);
      notAdded.push({ ...item, origin: batch.batch_id, source_file: file });
    }
    const localSources = new Map();
    for (const source of batch.sources) {
      for (const key of ['id', 'url', 'title', 'publisher', 'accessed_on', 'read_via', 'reading_scope', 'locator', 'summary', 'rights']) if (!source[key]) throw new Error(`${file}: source ${source.id ?? '?'} missing ${key}`);
      if (localSources.has(source.id)) throw new Error(`${file}: duplicate source id ${source.id}`);
      const { id: localId, url, ...reading } = source;
      localSources.set(localId, sourceId(url, { ...reading, origin: batch.batch_id }));
    }
    for (const row of batch.candidates) {
      for (const key of ['id', 'axis', 'question', 'case_key', 'answer_target', 'scope', 'source_locator', 'premise_status']) if (!row[key]) throw new Error(`${file}: candidate ${row.id ?? '?'} missing ${key}`);
      if (!/^N\d{3,}$/.test(row.id)) throw new Error(`${row.id}: new candidates use N-prefixed ids`);
      if (!axes[row.axis]) throw new Error(`${row.id}: unknown axis ${row.axis}`);
      if (!row.source_ids?.length || row.source_ids.some((id) => !localSources.has(id))) throw new Error(`${row.id}: missing or unknown source`);
      if (!['screened', 'needs_check'].includes(row.premise_status)) throw new Error(`${row.id}: invalid premise status`);
      validateEditorial(row);
      const { source_ids: localIds, ...rest } = row;
      records.push({
        ...rest, origin: batch.batch_id, domain: `${row.axis} ${axes[row.axis]}`, hook: row.hook ?? '', bank_status: null, production: { states: [], locators: [] }, locked: false,
        source_refs: [...new Set(localIds)].map((id) => ({ source_id: localSources.get(id), origin: batch.batch_id, locator: row.source_locator, supports: '支持選題前提；完整劇本仍需逐主張查核。' })),
        eligible: row.premise_status === 'screened', notes: row.notes ?? '', local_references: [file],
      });
    }
    // 舊題（題庫裡還沒查的題目卡）的篩選研究：把來源掛回原 ID，題目卡原文保留在 card_*。
    for (const row of batch.legacy_updates ?? []) {
      for (const key of ['id', 'answer_target', 'scope', 'source_locator', 'premise_status']) if (!row[key]) throw new Error(`${file}: legacy update ${row.id ?? '?'} missing ${key}`);
      const record = records.find((item) => item.id === row.id && item.origin === 'legacy');
      if (!record) throw new Error(`${row.id}: legacy update for an unknown topic`);
      if (record.locked) throw new Error(`${row.id}: produced topics are researched in their episode folder, not in the pool`);
      if (record.screened_in) throw new Error(`${row.id}: already screened in ${record.screened_in}`);
      if (!row.source_ids?.length || row.source_ids.some((id) => !localSources.has(id))) throw new Error(`${row.id}: missing or unknown source`);
      if (!['screened', 'needs_check'].includes(row.premise_status)) throw new Error(`${row.id}: invalid premise status`);
      validateEditorial(row);
      Object.assign(record, {
        card_question: record.question, card_answer_target: record.answer_target,
        question: row.question ?? record.question, hook: row.hook ?? record.hook, answer_target: row.answer_target, scope: row.scope,
        editorial: row.editorial, risk: row.risk ?? null, screened_in: batch.batch_id,
        premise_status: row.premise_status === 'screened' ? 'legacy_screened' : 'legacy_needs_check',
        eligible: row.premise_status === 'screened',
        source_refs: [...record.source_refs, ...[...new Set(row.source_ids)].map((id) => ({ source_id: localSources.get(id), origin: batch.batch_id, locator: row.source_locator, supports: '篩選研究：支持修正後的題目前提；完整劇本仍需逐主張查核。' }))],
        notes: [record.notes, row.notes].filter(Boolean).join(' '),
        local_references: [...record.local_references, file],
      });
    }
  }
  if (new Set(records.map((record) => record.id)).size !== records.length) throw new Error('Raw IDs must be unique across the bank, episodes and batches');

  for (const file of ['core.mjs', 'render.mjs', 'history.mjs', 'store.mjs', 'cli.mjs', 'semantic.py']) if (exists(root, `${TOOL_DIR}/${file}`)) bind(`${TOOL_DIR}/${file}`);
  const externalFile = `${DIR}/external/so-thats-why-cores.json`;
  let external = null;
  if (exists(root, externalFile)) { bind(externalFile); external = parse(root, externalFile); }
  return { axes, records, external, sources: [...sources.values()].sort((a, b) => a.id.localeCompare(b.id)), not_added: notAdded, inputs: [...inputs].sort(([a], [b]) => a.localeCompare(b)).map(([file, sha256]) => ({ file, sha256 })) };
}

const pairId = (a, b) => [a, b].sort().join('~');
const STRIP = ['為什麼', '為何', '怎麼', '真的', '其實', '到底', '是誰', '什麼'];
export const grams = (value) => {
  let text = normalizeQuestion(value ?? '');
  for (const word of STRIP) text = text.replaceAll(word, '');
  const chars = [...text.replace(/\d+/g, '#')];
  return new Set(chars.slice(1).map((_, index) => chars.slice(index, index + 2).join('')).filter((gram) => gram !== '##'));
};
const dice = (a, b) => {
  let common = 0;
  for (const gram of a) if (b.has(gram)) common += 1;
  return a.size + b.size ? 2 * common / (a.size + b.size) : 0;
};

export function similarityPairs(records, aliasMap = {}) {
  const q = records.map((record) => grams(record.question));
  const targets = records.map((record) => grams(record.answer_target));
  const keyTerms = records.map((record) => new Set(record.case_key.toLowerCase().split(/[._-]/).filter((part) => part.length > 2 && !['the', 'and', 'case', 'legacy', 'from', 'with'].includes(part))));
  const postings = new Map();
  const caseGroups = new Map();
  records.forEach((record, index) => {
    if (!caseGroups.has(record.case_key)) caseGroups.set(record.case_key, []);
    caseGroups.get(record.case_key).push(index);
    for (const token of new Set([...q[index], ...[...targets[index]].map((part) => `target:${part}`), ...[...keyTerms[index]].map((part) => `key:${part}`)])) {
      if (!postings.has(token)) postings.set(token, []);
      postings.get(token).push(index);
    }
  });
  const candidates = new Set();
  for (const members of caseGroups.values()) for (let i = 0; i < members.length; i += 1) for (let j = i + 1; j < members.length; j += 1) candidates.add(`${members[i]},${members[j]}`);
  for (const members of postings.values()) {
    if (members.length > Math.min(200, Math.max(40, records.length * 0.15))) continue;
    for (let i = 0; i < members.length; i += 1) for (let j = i + 1; j < members.length; j += 1) candidates.add(`${members[i]},${members[j]}`);
  }
  const pairs = [];
  for (const value of candidates) {
    const [ai, bi] = value.split(',').map(Number);
    const a = records[ai]; const b = records[bi];
    if (aliasMap[a.id] && aliasMap[a.id] === aliasMap[b.id]) continue;
    const questionScore = dice(q[ai], q[bi]); const answerScore = targets[ai].size && targets[bi].size ? dice(targets[ai], targets[bi]) : 0;
    const keyScore = dice(keyTerms[ai], keyTerms[bi]);
    const sharedKeys = [...keyTerms[ai]].filter((term) => keyTerms[bi].has(term)).length;
    const sameKey = a.case_key === b.case_key;
    if (!sameKey && questionScore < 0.3 && answerScore < 0.3 && !(keyScore >= 0.5 && sharedKeys >= 2)) continue;
    pairs.push({ id: pairId(a.id, b.id), a: a.id, b: b.id, question_score: Number(questionScore.toFixed(3)), answer_score: Number(answerScore.toFixed(3)), key_score: Number(keyScore.toFixed(3)), same_case_key: sameKey, required: !(a.locked && b.locked) && (sameKey || questionScore >= 0.45 || answerScore >= 0.45 || (keyScore >= 0.5 && sharedKeys >= 2)), questions: [a.question, b.question] });
  }
  return pairs.sort((x, y) => Number(y.required) - Number(x.required) || Math.max(y.question_score, y.answer_score) - Math.max(x.question_score, x.answer_score) || x.id.localeCompare(y.id));
}

// 跨系列：奇聞檔案局的題對原來如此事務所的核心題，只比題目；高分的要寫處置（distinct 或 transfer）。
export function crossSeriesPairs(records, external) {
  if (!external) return [];
  const mine = records.map((record) => [record, grams(record.question)]);
  const theirs = external.cores.map((core) => [core, grams(core.question)]);
  const pairs = [];
  for (const [record, a] of mine) for (const [core, b] of theirs) {
    const score = dice(a, b);
    if (score >= 0.34) pairs.push({ id: `${record.id}~${core.id}`, curio_id: record.id, external_id: core.id, question_score: Number(score.toFixed(3)), required: score >= 0.45, questions: [record.question, core.question] });
  }
  return pairs.sort((x, y) => y.question_score - x.question_score || x.id.localeCompare(y.id));
}

const DISPOSITIONS = ['drop', 'transfer', 'shorts'];

export function assemble(input, decisions = {}, selection = null) {
  const byId = new Map(input.records.map((record) => [record.id, record]));
  const known = (id, what) => { if (!byId.has(id)) throw new Error(`${what}: unknown record ${id}`); return id; };
  const parents = new Map(input.records.map((record) => [record.id, record.id]));
  const resolve = (id) => {
    if (parents.get(id) !== id) parents.set(id, resolve(parents.get(id)));
    return parents.get(id);
  };
  const links = [];
  const merge = (from, into, reason, kind) => {
    if (!reason) throw new Error('Every merge needs a reason');
    known(from, 'merge'); known(into, 'merge');
    if (byId.get(from).locked) throw new Error(`${from}: a produced or in-production topic cannot be merged away; merge the other topic into it or declare them distinct`);
    const left = resolve(from); const right = resolve(into);
    if (left !== right) parents.set(left, right);
    links.push({ duplicate_id: from, canonical_id: into, reason, kind });
  };
  const exact = new Map();
  for (const record of input.records) {
    const key = normalizeQuestion(record.question);
    if (exact.has(key) && !record.locked) merge(record.id, exact.get(key), '完整問題正規化後相同；保留原 ID 與來源。', 'exact_question');
    else if (!exact.has(key)) exact.set(key, record.id);
  }
  for (const item of decisions.merges ?? []) merge(item.duplicate_id, item.canonical_id, item.reason, 'editorial_core_answer');
  const dispositions = new Map();
  for (const item of decisions.dispositions ?? []) {
    known(item.id, 'disposition');
    if (!DISPOSITIONS.includes(item.disposition) || !item.reason) throw new Error(`${item.id}: disposition must be drop, transfer or shorts with a reason`);
    if (item.disposition === 'transfer' && !item.transfer_to) throw new Error(`${item.id}: a transfer names its destination`);
    if (item.disposition === 'drop' && !item.reentry) throw new Error(`${item.id}: a drop states its re-entry condition`);
    if (byId.get(item.id).locked) throw new Error(`${item.id}: a produced or in-production topic cannot be dropped, transferred or turned into Shorts here`);
    if (dispositions.has(item.id)) throw new Error(`${item.id}: duplicate disposition`);
    dispositions.set(item.id, item);
  }
  const aliases = Object.fromEntries(input.records.map((record) => [record.id, resolve(record.id)]));
  for (const [id, item] of dispositions) if (aliases[id] !== id) throw new Error(`${id}: ${item.disposition} applies to a canonical core, not to an alias`);
  const groups = new Map();
  for (const record of input.records) {
    const id = aliases[record.id];
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id).push(record);
  }
  const selectedIds = new Set(selection?.ids ?? []);
  const held = new Map((selection?.held ?? []).map((item) => [item.id, item.reason]));
  const candidates = [...groups].map(([id, members]) => {
    const main = byId.get(id);
    const lockedMembers = members.filter((record) => record.locked);
    if (lockedMembers.length && !main.locked) throw new Error(`${id}: a group containing a produced topic must use it as the canonical id`);
    const disposition = dispositions.get(id);
    const eligible = !main.locked && !disposition && members.some((record) => record.eligible);
    const status = main.locked ? 'produced' : disposition ? (disposition.disposition === 'shorts' ? 'shorts' : 'excluded') : selectedIds.has(id) ? 'selected' : eligible ? 'held' : 'reserve';
    return {
      ...main, id, eligible, selected: status === 'selected', pool_status: status,
      aliases: members.map((record) => record.id).filter((member) => member !== id),
      question_variants: members.filter((record) => record.id !== id).map((record) => ({ id: record.id, question: record.question, answer_target: record.answer_target, scope: record.scope })),
      source_refs: [...new Map(members.flatMap((record) => record.source_refs).map((ref) => [`${ref.source_id}:${ref.origin}:${ref.locator}`, ref])).values()],
      provenance_ids: members.map((record) => record.id),
      disposition: disposition ? { disposition: disposition.disposition, reason: disposition.reason, ...(disposition.transfer_to ? { transfer_to: disposition.transfer_to } : {}), ...(disposition.reentry ? { reentry: disposition.reentry } : {}) } : null,
      exclusion_reason: disposition && disposition.disposition !== 'shorts' ? disposition.reason : status === 'held' ? held.get(id) ?? null : status === 'reserve' ? '還沒有可追溯來源：題目卡是起草時憑既有知識寫的，要先研究才能選入。' : null,
      verification: 'TOPIC_CANDIDATE_NOT_CLAIM_OR_SCRIPT_APPROVAL', production_ready: false,
    };
  }).sort((a, b) => a.id.localeCompare(b.id, 'en', { numeric: true }));
  const pairs = similarityPairs(input.records, aliases);
  const distinct = new Map((decisions.distinct ?? []).map((item) => {
    known(item.a, 'distinct'); known(item.b, 'distinct');
    if (!item.reason || resolve(item.a) === resolve(item.b)) throw new Error(`Invalid distinct decision ${item.a}~${item.b}`);
    return [pairId(item.a, item.b), item.reason];
  }));
  const pending = pairs.filter((pair) => pair.required && !distinct.has(pair.id));
  const cross = crossSeriesPairs(input.records, input.external);
  const crossDecisions = new Map((decisions.cross_series ?? []).map((item) => {
    known(item.id, 'cross_series');
    if (!['distinct', 'transfer'].includes(item.decision) || !item.reason || !item.external_id) throw new Error(`Invalid cross-series decision for ${item.id}`);
    if (item.decision === 'transfer' && dispositions.get(aliases[item.id])?.disposition !== 'transfer') throw new Error(`${item.id}: a cross-series transfer must also be a transfer disposition`);
    return [`${item.id}~${item.external_id}`, item];
  }));
  const crossPending = cross.filter((pair) => pair.required && !crossDecisions.has(pair.id) && !crossDecisions.has(`${aliases[pair.curio_id]}~${pair.external_id}`));
  if (selection) {
    if (!Array.isArray(selection.ids) || selectedIds.size !== selection.ids.length || !selection.reason) throw new Error('Invalid selection manifest');
    for (const id of selection.ids) {
      const entry = candidates.find((candidate) => candidate.id === id);
      if (!entry?.eligible) throw new Error(`${id}: selected id must be an eligible canonical core (sourced, not produced, not dropped)`);
    }
    for (const [id, reason] of held) {
      const entry = candidates.find((candidate) => candidate.id === id);
      if (!entry || entry.pool_status !== 'held' || !reason) throw new Error(`${id}: a held id must be an eligible, unselected core with a reason`);
    }
    const unexplained = candidates.filter((row) => row.pool_status === 'held' && !held.has(row.id));
    if (unexplained.length) throw new Error(`Eligible cores neither selected nor held: ${unexplained.map((row) => row.id).join(', ')}`);
    if (candidates.filter((row) => row.selected).length !== selection.target_count) throw new Error('Selected count does not match reviewed target');
    if (pending.length) throw new Error(`${pending.length} high-similarity pairs still need editorial decisions: ${pending.slice(0, 5).map((pair) => pair.id).join(', ')}`);
    if (crossPending.length) throw new Error(`${crossPending.length} cross-series pairs still need decisions: ${crossPending.slice(0, 5).map((pair) => pair.id).join(', ')}`);
  }
  const selected = candidates.filter((row) => row.selected);
  const count = (status) => candidates.filter((row) => row.pool_status === status).length;
  return {
    schema_version: 1, series: '奇聞檔案局', revision: selection?.revision ?? 'unversioned-draft', status: selection ? 'CURATED_CANDIDATE_POOL_NOT_PRODUCTION' : 'DRAFT_INTAKE',
    axes: input.axes,
    counts: {
      raw_records: input.records.length, canonical_cores: candidates.length, alias_records: input.records.length - candidates.length,
      produced_cores: count('produced'), selected_candidates: selected.length, held_candidates: count('held'), reserve_candidates: count('reserve'), shorts_candidates: count('shorts'), excluded_cores: count('excluded'),
      new_batch_records: input.records.filter((record) => record.origin !== 'legacy').length,
      source_urls: input.sources.length, current_research_source_urls: input.sources.filter((source) => source.readings.some((reading) => !reading.origin.startsWith('legacy:'))).length,
      selected_source_urls: new Set(selected.flatMap((row) => row.source_refs.map((ref) => ref.source_id))).size,
      new_suggestions_not_added: input.not_added?.length ?? 0, high_similarity_pending: pending.length, cross_series_pending: crossPending.length, approved_scripts: 0,
    },
    inputs: input.inputs, sources: input.sources, candidates, raw_records: input.records,
    dedup: { aliases, merges: links, distinct: decisions.distinct ?? [], dispositions: decisions.dispositions ?? [], cross_series: decisions.cross_series ?? [], potential_pairs: pairs, required_pending: pending, cross_series_pairs: cross, cross_series_pending: crossPending, method: 'exact normalized questions + authored core-answer merges + lexical candidate pairs (title, finding, case key) reviewed by an editor; cross-series lexical pairs against the so-thats-why pool; no claim of exhaustive semantic equivalence' },
    selection: selection ?? null, not_added: input.not_added ?? [],
    external: input.external ? { series: input.external.series, commit: input.external.commit, pool_revision: input.external.pool_revision, core_count: input.external.cores.length } : null,
  };
}

export function loadDraft(root = ROOT) {
  const input = intake(root);
  const file = `${DIR}/dedup-decisions.json`;
  const decisions = exists(root, file) ? parse(root, file) : {};
  if (exists(root, file)) input.inputs.push({ file, sha256: hash(readFileSync(path.join(root, file))) });
  return { input, decisions, draft: assemble(input, decisions) };
}

export function buildPool(root = ROOT) {
  const { input, decisions } = loadDraft(root);
  const file = `${DIR}/selection.json`;
  const selection = parse(root, file);
  if (!selection.revision || !selection.reviewed_on) throw new Error('Selection needs a reviewed revision');
  input.inputs.push({ file, sha256: hash(readFileSync(path.join(root, file))) });
  return assemble(input, decisions, selection);
}

export function readPool(root = ROOT) {
  const saved = parse(root, `${DIR}/pool.json`);
  const current = buildPool(root);
  if (JSON.stringify(saved) !== JSON.stringify(current)) throw new Error('Pool drift: the topic bank, episode folders, source files or decisions changed; re-review and run build');
  return saved;
}

export function writeJson(root, name, value) {
  const directory = path.join(root, DIR);
  mkdirSync(path.dirname(path.join(directory, name)), { recursive: true });
  writeFileSync(path.join(directory, name), `${JSON.stringify(value, null, 2)}\n`);
}
