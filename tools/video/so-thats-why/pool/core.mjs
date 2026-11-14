import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { gunzipSync } from 'node:zlib';
import { ROOT, readCatalog } from '../catalog.mjs';
import { readProgram } from '../program.mjs';

export { ROOT };
export const DIR = 'docs/videos/so-thats-why/pool';
export const VERSION = 'candidate-pool-v1';
export const hash = (value) => createHash('sha256').update(value).digest('hex');
const parse = (root, file) => JSON.parse(readFileSync(path.join(root, file), 'utf8'));
export const normalizeQuestion = (text) => text.normalize('NFKC').toLowerCase().replace(/[\p{P}\p{Z}\s]/gu, '');
export function normalizeUrl(value) {
  const url = new URL(value);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || /^(localhost|127\.|0\.|10\.|192\.168\.|169\.254\.|\[)/.test(url.hostname)) throw new Error(`Not a public source URL: ${value}`);
  for (const key of [...url.searchParams.keys()]) if (/^(utm_|fbclid$|gclid$)/.test(key)) url.searchParams.delete(key);
  url.hash = '';
  return url.href;
}

export const CATEGORIES = Object.freeze([
  '物理化學與日常材料',
  '生物動物與植物',
  '地球天氣與太空',
  '數位科技與通訊工程',
  '飲食與廚房科學',
  '人體感官與日常行為',
  '建築交通與商業制度',
]);

const LEGACY_CATEGORY_OVERRIDES = Object.freeze({
  'LEG-S01': '建築交通與商業制度',
  'LEG-S02': '地球天氣與太空',
  'LEG-S03': '飲食與廚房科學',
  'LEG-S04': '生物動物與植物',
  'LEG-S05': '人體感官與日常行為',
  'LEG-S06': '人體感官與日常行為',
  'LEG-S07': '物理化學與日常材料',
  'LEG-S08': '飲食與廚房科學',
  'LEG-S09': '飲食與廚房科學',
  'LEG-S10': '人體感官與日常行為',
  'LEG-S11': '數位科技與通訊工程',
  'LEG-S12': '地球天氣與太空',
  'LEG-S13': '物理化學與日常材料',
  'LEG-S14': '人體感官與日常行為',
  'LEG-S15': '物理化學與日常材料',
  'LEG-S16': '建築交通與商業制度',
  'LEG-S17': '數位科技與通訊工程',
  'LEG-S18': '地球天氣與太空',
  'LEG-S19': '飲食與廚房科學',
  'LEG-S20': '人體感官與日常行為',
  'LEG-S21': '地球天氣與太空',
  'LEG-S22': '建築交通與商業制度',
  'LEG-S23': '地球天氣與太空',
  'LEG-S24': '人體感官與日常行為',
  'LEG-S25': '人體感官與日常行為',
  'LEG-S26': '人體感官與日常行為',
  'LEG-S27': '物理化學與日常材料',
  'LEG-S28': '地球天氣與太空',
  'LEG-S29': '地球天氣與太空',
  'LEG-S30': '飲食與廚房科學',
  'LEG-S31': '飲食與廚房科學',
  'LEG-S32': '地球天氣與太空',
  'LEG-S33': '物理化學與日常材料',
  'LEG-S34': '生物動物與植物',
  'LEG-S35': '生物動物與植物',
  'LEG-S36': '物理化學與日常材料',
  'LEG-S37': '人體感官與日常行為',
  'LEG-S38': '人體感官與日常行為',
  'LEG-S39': '人體感官與日常行為',
  'LEG-S40': '人體感官與日常行為',
  'LEG-S41': '生物動物與植物',
  'LEG-S42': '地球天氣與太空',
  'LEG-S43': '地球天氣與太空',
  'LEG-S44': '物理化學與日常材料',
  'LEG-S45': '人體感官與日常行為',
  'LEG-S46': '飲食與廚房科學',
  'LEG-S47': '生物動物與植物',
  'LEG-S48': '地球天氣與太空',
  'LEG-S49': '物理化學與日常材料',
  'LEG-S50': '飲食與廚房科學',
  'LEG-S51': '人體感官與日常行為',
  'LEG-S52': '人體感官與日常行為',
  'LEG-S53': '物理化學與日常材料',
  'LEG-S54': '飲食與廚房科學',
  'LEG-S55': '飲食與廚房科學',
  'LEG-S56': '地球天氣與太空',
  'LEG-S57': '地球天氣與太空',
  'LEG-S58': '地球天氣與太空',
  'LEG-S59': '生物動物與植物',
  'LEG-S60': '生物動物與植物',
  'LEG-S61': '生物動物與植物',
  'LEG-S62': '生物動物與植物',
  'LEG-S63': '生物動物與植物',
  'LEG-S64': '人體感官與日常行為',
  'LEG-S65': '人體感官與日常行為',
  'LEG-S66': '人體感官與日常行為',
  'LEG-S67': '人體感官與日常行為',
  'LEG-S68': '物理化學與日常材料',
  'LEG-S69': '物理化學與日常材料',
  'LEG-S70': '物理化學與日常材料',
  'LEG-S71': '飲食與廚房科學',
  'LEG-S72': '物理化學與日常材料',
  'LEG-S73': '飲食與廚房科學',
  'LEG-S74': '人體感官與日常行為',
  'LEG-S75': '人體感官與日常行為',
  'LEG-S76': '物理化學與日常材料',
  'LEG-S77': '物理化學與日常材料',
  'LEG-S78': '物理化學與日常材料',
  'LEG-S79': '飲食與廚房科學',
  'LEG-S80': '地球天氣與太空',
  'LEG-S81': '物理化學與日常材料',
  'LEG-S82': '地球天氣與太空',
  'LEG-S83': '地球天氣與太空',
  'LEG-S84': '地球天氣與太空',
  'LEG-S85': '物理化學與日常材料',
  'LEG-S86': '數位科技與通訊工程',
  'LEG-S87': '物理化學與日常材料',
  'LEG-S88': '物理化學與日常材料',
  'P52-008': '地球天氣與太空',
  'P52-009': '地球天氣與太空',
  'P52-010': '地球天氣與太空',
});

export function classifyCandidate(row) {
  if (row.category && CATEGORIES.includes(row.category)) return row.category;
  if (LEGACY_CATEGORY_OVERRIDES[row.id]) return LEGACY_CATEGORY_OVERRIDES[row.id];
  const d = (row.domain || '').toLowerCase();
  const q = row.question || '';
  const o = (row.origin || '').toLowerCase();

  if (d === 'business') return '建築交通與商業制度';
  if (d === 'travel') return /時差|暈機/.test(q) ? '人體感官與日常行為' : '建築交通與商業制度';
  if (d === 'tech') {
    if (/電動車.*一檔|遊戲主機.*賠錢|搜尋.*免費/.test(q)) return '建築交通與商業制度';
    return '數位科技與通訊工程';
  }
  if (d === 'weather_sky') return '地球天氣與太空';

  if (
    /食物|食品|廚房|烹調|烹飪|料理|烘焙|發酵|乳品|乳脂|乳酪|起司|咖啡|茶葉|釀造|酒|巧克力|糖晶|澱粉|麵團|麵筋|烤肉|梅納|焦糖|鍋巴|食材|蔬果保鮮|冷藏蔬果|冷凍肉|冷傷|調味料|味覺與飲食|飲食|保鮮|罐頭|醃漬|油炸|煮沸|爆米花|風味從哪裡來/.test(d) ||
    o.includes('-food-')
  ) {
    if (d === '食物網') return '生物動物與植物';
    return '飲食與廚房科學';
  }

  if (
    /動物|植物|生物|昆蟲|鳥類|魚類|海洋生物|哺乳|爬蟲|兩棲|無脊椎|真菌|微生物|細菌|病毒|細胞|基因|dna|遺傳|演化|物種|族群|生態|種子|果實|花|樹|葉|根|光合作用|授粉|寄生|共生|捕食|冬眠|隱生|水熊蟲|蜘蛛|黏菌|蟻|蜂|珊瑚|化石與古生物|古足跡|足跡與化石|週期蟬/.test(d) ||
    o.includes('-animal') || o.includes('-plant') || o.includes('-bio') || o.includes('-microb') || o.includes('-seeds') || o.includes('-whale') || o.includes('-flowe') || o.includes('-wood-') || o.includes('-tracks')
  ) {
    if (o.includes('-wood-') && /木材|家具|木板/.test(q) && !/樹幹|導管|活樹/.test(q)) return '物理化學與日常材料';
    if (o.includes('-rings') || /年輪裡的歷史/.test(d)) return '地球天氣與太空';
    if (/人體|人類視覺|人腦|說話|閱讀/.test(d)) return '人體感官與日常行為';
    return '生物動物與植物';
  }

  if (
    /交通|城市|建築|土木|橋梁|隧道|道路|街道|鐵路|鐵軌|高鐵|列車|飛機|航空|船舶|車輛|汽車|輪胎|號誌|黃燈|紅綠燈|塞車|車流|用水與污水|水處理|電網調度|商業|價格|定價|拍賣|市場|金融|支付|保險|制度|法律|標準|檢驗|抽樣|排隊|物流|供應鏈|住家建築|室內環境|古蹟|考古器物/.test(d) ||
    o.includes('-transp') || o.includes('-arch-') || o.includes('-struc')
  ) {
    return '建築交通與商業制度';
  }

  if (
    /資訊|數位|網路|網頁|電腦|半導體|晶片|密碼|加密|通訊|雷達觀測|衛星定位|gps|電子|電路|電源|電池|感測器|影像壓縮|音訊編碼|光電|檔案系統|記憶體|演算法|軟體|ai|機器學習|無線|藍牙|wi-fi|光纖|編碼|條碼|qr|時間同步|伺服器/.test(d) ||
    o.includes('-tech') || o.includes('-digit') || o.includes('-inform') || o.includes('-networ') || o.includes('-electr') || o.includes('-imagi') || o.includes('-image')
  ) {
    if (/靜電|磁學/.test(d)) return '物理化學與日常材料';
    if (/天氣|氣象|大氣|海洋|地質|冰河|太陽風暴|太空天氣|小天體|行星|黑洞|地圖/.test(d)) return '地球天氣與太空';
    if (/光學、成像與量測|量測與資料判讀/.test(d)) {
      return /電腦|數位|感測|相機|像素|快門|壓縮|演算法/.test(q) ? '數位科技與通訊工程' : '物理化學與日常材料';
    }
    return '數位科技與通訊工程';
  }

  if (
    /天文|宇宙|太空|行星|恆星|月球|太陽|黑洞|小行星|小天體|彗星|隕石|軌道|天氣|氣象|大氣|雲|雨滴|雷電|颱風|風暴|海洋|海浪|潮汐|海嘯|深海熱泉|海水|地質|地震|火山|斷層|岩石|礦物|地形|地圖|冰河|冰雪|凍土|地下水|河流|海岸|板塊|地球|古氣候|冰芯|海底/.test(d) ||
    o.includes('-earth') || o.includes('-astro') || o.includes('-space') || o.includes('-weathe') || o.includes('-landf') || o.includes('-lande') || o.includes('-rings') || o.includes('-seafl')
  ) {
    if (/雨滴碰撞/.test(d) && !/雷達|氣象|土壤侵蝕/.test(q)) return '物理化學與日常材料';
    return '地球天氣與太空';
  }

  if (
    /知覺|記憶|身體|感官|視覺|聽覺|觸覺|嗅覺|味覺|前庭|大腦|神經|睡眠|生理|呼吸|心跳|血液|體溫|流汗|皮膚|肌肉|骨骼|步行|運動生理|疼痛|痛覺|錯覺|注意力|認知|行為與學習|決策心理|選擇偏誤|說話|語音知覺|讀一行字|閱讀|用手觸碰|聲音知覺/.test(d) ||
    o.includes('-cognit') || o.includes('-body-') || o.includes('-sensi') || o.includes('-perce') || o.includes('-speec') || o.includes('-touch') || o.includes('-readi') || o.includes('-choic')
  ) {
    return '人體感官與日常行為';
  }

  if (o.includes('-life')) return '生物動物與植物';
  if (o.includes('-human')) {
    if (/價格|拍賣|排隊|車流|紅綠燈|黃燈|號誌|制度|檢驗|抽樣|稅|商業|交通|建築/.test(`${q} ${d}`)) return '建築交通與商業制度';
    return '人體感官與日常行為';
  }

  return '物理化學與日常材料';
}

export function checkpointFiles(root = ROOT) {
  const registry = parse(root, `${DIR}/checkpoints.json`);
  if (!Array.isArray(registry.checkpoints) || !registry.checkpoints.length || new Set(registry.checkpoints).size !== registry.checkpoints.length || registry.checkpoints.some((file) => !/^checkpoint-\d+\.json$/.test(file))) throw new Error('Invalid required checkpoint registry');
  if (!registry.checkpoints.includes(registry.editorial_baseline)) throw new Error('Missing editorial baseline checkpoint');
  return registry;
}

export function validateEditorial(row, { required = true } = {}) {
  if (row.category !== undefined && !CATEGORIES.includes(row.category)) throw new Error(`${row.id}: invalid category ${row.category}`);
  if (row.editorial === undefined && !required) return; // Only frozen historical IDs are exempt.
  const value = row.editorial;
  if (!value || !['segment', 'theme_seed'].includes(value.role) || typeof value.payoff !== 'string' || !value.payoff.trim() || typeof value.visual !== 'string' || !value.visual.trim()) throw new Error(`${row.id}: invalid editorial role, payoff or visual`);
  if (!Array.isArray(value.seconds) || value.seconds.length !== 2 || value.seconds.some((n) => !Number.isInteger(n) || n <= 0 || n > 600) || value.seconds[0] > value.seconds[1]) throw new Error(`${row.id}: invalid segment seconds`);
}

function sectionFor(text, id, shared) {
  if (!shared) return text;
  const start = new RegExp(`^##\\s+${id}\\b[^\\n]*`, 'm').exec(text);
  if (!start) return '';
  const body = text.slice(start.index + start[0].length);
  const end = /^##\s+[ABST]\d+\b/m.exec(body);
  return `${start[0]}${end ? body.slice(0, end.index) : body}`;
}
export function urlsIn(text) {
  const found = [];
  for (const match of text.matchAll(/https?:\/\//g)) {
    let value = ''; let depth = 0;
    for (const char of text.slice(match.index)) {
      if (/[\s<>"|；，。`（）\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(char)) break;
      if (char === '(') depth += 1;
      if (char === ')') { if (!depth) break; depth -= 1; }
      value += char;
    }
    value = value.replace(/[.,;\]]+$/, '');
    // Malformed historical literal /n concatenations are not a trustworthy URL.
    if (/\/nhttps?:|\/n\d{4}$/.test(value)) continue;
    found.push(value);
  }
  return [...new Set(found)];
}

export function intake(root = ROOT) {
  const catalog = readCatalog(root);
  const { program } = readProgram(root);
  const inputs = new Map();
  const bind = (file) => inputs.set(file, hash(readFileSync(path.join(root, file))));
  bind(`${DIR}/checkpoints.json`);
  const registry = checkpointFiles(root);
  let historicalIds;
  for (const file of registry.checkpoints) {
    bind(`${DIR}/${file}`);
    const checkpoint = parse(root, `${DIR}/${file}`);
    if (!/^baselines\/[\w.-]+\.json\.gz$/.test(checkpoint.file)) throw new Error('Invalid checkpoint path');
    bind(`${DIR}/${checkpoint.file}`);
    if (inputs.get(`${DIR}/${checkpoint.file}`) !== checkpoint.sha256) throw new Error('Checkpoint hash mismatch');
    if (file === registry.editorial_baseline) historicalIds = new Set(JSON.parse(gunzipSync(readFileSync(path.join(root, DIR, checkpoint.file))).toString('utf8')).pool.raw_records.map((row) => row.id));
  }
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
  for (const item of catalog.sources) bind(item.file);
  bind('docs/videos/so-thats-why/refresh-20261101/catalog.json');
  bind('docs/videos/so-thats-why/refresh-20261101/episodes.json');
  for (const topic of catalog.episodes) {
    const original = parse(root, topic.source_file).episodes.find((entry) => entry.id === topic.id);
    const refs = [];
    for (const file of topic.source_references ?? []) {
      bind(file);
      const text = readFileSync(path.join(root, file), 'utf8');
      const section = sectionFor(text, topic.id, file.includes('/topic-checks/'));
      for (const url of urlsIn(section)) {
        let id;
        try {
          id = sourceId(url, { origin: `legacy:${topic.id}`, title: '歷史查核包所列來源，題名待當期讀頁補核', publisher: new URL(url).hostname, accessed_on: null, imported_on: '2026-11-01', read_via: 'local_legacy_review_section', reading_scope: `${file}#${topic.id} 的來源清單；不表示本輪讀過外站`, locator: `${file}#${topic.id}`, summary: '保留過往查核來源指向，當期可達性及支持關係需重查。', rights: 'LINK_ONLY_NO_EXTERNAL_TEXT_COPIED' });
        } catch { continue; }
        refs.push({ source_id: id, origin: `legacy:${topic.id}`, locator: `${file}#${topic.id}`, supports: '歷史題級查核入口；不是當期劇本核准。' });
      }
    }
    for (const entry of topic.sources ?? []) {
      const id = sourceId(entry.url, { origin: `legacy:${topic.id}`, title: entry.supports, publisher: new URL(entry.url).hostname, accessed_on: topic.checked_on ?? null, imported_on: '2026-11-01', read_via: 'prior_topic_core_review', reading_scope: '2026-11-01 新題核心來源研究；未查全部新節目主張', locator: entry.supports, summary: entry.supports, rights: 'LINK_AND_ORIGINAL_SUMMARY_ONLY' });
      refs.push({ source_id: id, origin: `legacy:${topic.id}`, locator: entry.supports, supports: entry.supports });
    }
    const second = program.dispositions.find((entry) => entry.id === topic.id);
    const excluded = ['drop', 'hold', 'transfer'].includes(topic.disposition) || second?.disposition === 'hold';
    records.push({
      id: `LEG-${topic.id}`, legacy_id: topic.id, origin: 'legacy', question: topic.title,
      domain: topic.pillar, mechanism_key: `legacy.${topic.id.toLowerCase()}`,
      answer_target: (original.answer ?? topic.answer ?? topic.reason).slice(0, 800),
      scope: topic.limits?.join('；') ?? `沿用 ${topic.id} 題級條件，須讀原查核包的限制；${topic.reason}`,
      source_refs: [...new Map(refs.map((ref) => [`${ref.source_id}:${ref.locator}`, ref])).values()],
      premise_status: excluded ? 'excluded_legacy' : 'legacy_review_requires_refresh',
      eligible: !excluded && refs.length > 0,
      notes: [topic.reason, second?.reason, '來源與原答案只作研究入口，未完成當期逐主張覆核。'].filter(Boolean).join(' '),
      prior_decision: { first: topic.disposition, second: second?.disposition ?? null, episode: second?.episode_id ?? null },
      local_references: topic.source_references ?? [topic.source_file],
      original_record_sha256: topic.source_record_sha256,
    });
  }
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
      for (const key of ['id', 'url', 'title', 'publisher', 'accessed_on', 'read_via', 'reading_scope', 'locator', 'summary', 'rights']) if (!source[key]) throw new Error(`${file}: source missing ${key}`);
      if (localSources.has(source.id)) throw new Error(`${file}: duplicate source id ${source.id}`);
      const { id: localId, url, ...reading } = source;
      localSources.set(localId, sourceId(url, { ...reading, origin: batch.batch_id }));
    }
    for (const row of batch.candidates) {
      for (const key of ['id', 'question', 'domain', 'mechanism_key', 'answer_target', 'scope', 'source_locator', 'premise_status']) if (!row[key]) throw new Error(`${file}: candidate missing ${key}`);
      if (!row.source_ids?.length || row.source_ids.some((id) => !localSources.has(id))) throw new Error(`${row.id}: missing or unknown source`);
      if (!['screened', 'needs_check'].includes(row.premise_status)) throw new Error(`${row.id}: invalid premise status`);
      validateEditorial(row, { required: !historicalIds.has(row.id) });
      records.push({ ...row, origin: batch.batch_id, source_refs: row.source_ids.map((id) => ({ source_id: localSources.get(id), origin: batch.batch_id, locator: row.source_locator, supports: '支持選題前提或研究機制；生活例證與完整答案仍需逐主張覆核。' })), source_ids: undefined, eligible: row.premise_status === 'screened', notes: row.notes ?? '', local_references: [file] });
    }
  }
  if (new Set(records.map((record) => record.id)).size !== records.length) throw new Error('Raw IDs must be unique across batches');
  for (const file of ['core.mjs', 'store.mjs', 'cli.mjs', 'render.mjs', 'history.mjs', 'semantic.py']) if (existsSync(path.join(root, 'tools/video/so-thats-why/pool', file))) bind(`tools/video/so-thats-why/pool/${file}`);
  if (existsSync(path.join(root, DIR, 'baseline.json'))) {
    bind(`${DIR}/baseline.json`);
    const baseline = parse(root, `${DIR}/baseline.json`);
    if (!/^baselines\/[\w.-]+\.json\.gz$/.test(baseline.file)) throw new Error('Invalid baseline path');
    bind(`${DIR}/${baseline.file}`);
    if (inputs.get(`${DIR}/${baseline.file}`) !== baseline.sha256) throw new Error('Baseline hash mismatch');
  }
  return { records, sources: [...sources.values()].sort((a, b) => a.id.localeCompare(b.id)), not_added: notAdded, inputs: [...inputs].map(([file, sha256]) => ({ file, sha256 })) };
}

const pairId = (a, b) => [a, b].sort().join('~');
const grams = (value) => {
  const chars = [...normalizeQuestion(value).replaceAll('為什麼', '').replaceAll('怎麼', '').replaceAll('為何', '')];
  return new Set(chars.slice(1).map((_, index) => chars.slice(index, index + 2).join('')));
};
const dice = (a, b) => {
  let common = 0;
  for (const gram of a) if (b.has(gram)) common += 1;
  return a.size + b.size ? 2 * common / (a.size + b.size) : 0;
};

export function similarityPairs(records, aliasMap = {}) {
  const q = records.map((record) => grams(record.question));
  const targets = records.map((record) => grams(record.answer_target));
  const keyTerms = records.map((record) => new Set(record.mechanism_key.toLowerCase().split(/[._-]/).filter((part) => part.length > 2 && !['the', 'and', 'from', 'with', 'versus', 'legacy'].includes(part))));
  const postings = new Map();
  const mechanismGroups = new Map();
  records.forEach((record, index) => {
    if (!mechanismGroups.has(record.mechanism_key)) mechanismGroups.set(record.mechanism_key, []);
    mechanismGroups.get(record.mechanism_key).push(index);
    for (const token of new Set([...q[index], ...[...targets[index]].map((part) => `target:${part}`), ...[...keyTerms[index]].map((part) => `key:${part}`)])) {
      if (!postings.has(token)) postings.set(token, []);
      postings.get(token).push(index);
    }
  });
  const candidates = new Set();
  // An exact mechanism match must never disappear behind the common-token cap.
  for (const members of mechanismGroups.values()) {
    for (let i = 0; i < members.length; i += 1) for (let j = i + 1; j < members.length; j += 1) candidates.add(`${members[i]},${members[j]}`);
  }
  for (const members of postings.values()) {
    if (members.length > Math.min(200, Math.max(40, records.length * 0.15))) continue;
    for (let i = 0; i < members.length; i += 1) for (let j = i + 1; j < members.length; j += 1) candidates.add(`${members[i]},${members[j]}`);
  }
  const pairs = [];
  for (const value of candidates) {
    const [ai, bi] = value.split(',').map(Number);
    const a = records[ai]; const b = records[bi];
    if (aliasMap[a.id] && aliasMap[a.id] === aliasMap[b.id]) continue;
    const questionScore = dice(q[ai], q[bi]); const answerScore = dice(targets[ai], targets[bi]);
    const keyScore = dice(keyTerms[ai], keyTerms[bi]);
    const sharedKeys = [...keyTerms[ai]].filter((term) => keyTerms[bi].has(term)).length;
    const sameKey = a.mechanism_key === b.mechanism_key;
    if (!sameKey && questionScore < 0.38 && answerScore < 0.6 && !(keyScore >= 0.5 && sharedKeys >= 2)) continue;
    pairs.push({ id: pairId(a.id, b.id), a: a.id, b: b.id, question_score: Number(questionScore.toFixed(3)), answer_score: Number(answerScore.toFixed(3)), key_score: Number(keyScore.toFixed(3)), same_mechanism_key: sameKey, required: sameKey || questionScore >= 0.6 || answerScore >= 0.78, questions: [a.question, b.question] });
  }
  return pairs.sort((a, b) => Number(b.required) - Number(a.required) || Math.max(b.question_score, b.answer_score) - Math.max(a.question_score, a.answer_score) || a.id.localeCompare(b.id));
}

export function assemble(input, decisions = { merges: [], distinct: [], excluded: [] }, selection = null) {
  const byId = new Map(input.records.map((record) => [record.id, record]));
  const parents = new Map(input.records.map((record) => [record.id, record.id]));
  const resolve = (id) => {
    if (!parents.has(id)) throw new Error(`Unknown record ${id}`);
    if (parents.get(id) !== id) parents.set(id, resolve(parents.get(id)));
    return parents.get(id);
  };
  const links = [];
  const merge = (from, into, reason, kind) => {
    if (!reason) throw new Error('Every merge needs a reason');
    const left = resolve(from); const right = resolve(into);
    if (left !== right) parents.set(left, right);
    links.push({ duplicate_id: from, canonical_id: into, reason, kind });
  };
  // Only exact normalized questions auto-merge. Approximate similarity never decides identity.
  const exact = new Map();
  for (const record of input.records) {
    const key = normalizeQuestion(record.question);
    if (exact.has(key)) merge(record.id, exact.get(key), '完整問題正規化後相同；保留原 ID 與來源。', 'exact_question');
    else exact.set(key, record.id);
  }
  for (const item of decisions.merges ?? []) merge(item.duplicate_id, item.canonical_id, item.reason, 'editorial_core_question');
  const excludes = new Map((decisions.excluded ?? []).map((item) => {
    if (!byId.has(item.id) || !item.reason) throw new Error('Invalid exclusion');
    return [item.id, item.reason];
  }));
  const aliases = Object.fromEntries(input.records.map((record) => [record.id, resolve(record.id)]));
  const sourceSet = new Set(input.sources.map((source) => source.id));
  const excludedSourceRefs = (decisions.excluded_source_refs ?? []).map((item) => {
    if (!item || !byId.has(item.candidate_id) || aliases[item.candidate_id] !== item.candidate_id || !sourceSet.has(item.source_id) || typeof item.reason !== 'string' || !item.reason.trim()) {
      throw new Error('Invalid excluded_source_refs decision');
    }
    if ((item.origin !== undefined && (typeof item.origin !== 'string' || !item.origin.trim())) || (item.locator !== undefined && (typeof item.locator !== 'string' || !item.locator.trim()))) {
      throw new Error('Invalid excluded_source_refs filter');
    }
    return item;
  });
  const matchedExcludedRefs = new Set();
  const groups = new Map();
  for (const record of input.records) {
    const id = aliases[record.id];
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id).push(record);
  }
  const candidates = [...groups].map(([id, members]) => {
    const main = byId.get(id);
    const retired = members.some((record) => record.premise_status === 'excluded_legacy');
    const rejected = members.find((record) => excludes.has(record.id));
    const eligible = !retired && !rejected && members.some((record) => record.eligible);
    const mergedRefs = [...new Map(members.flatMap((record) => record.source_refs).map((ref) => [`${ref.source_id}:${ref.origin}:${ref.locator}`, ref])).values()];
    const rules = excludedSourceRefs.map((rule, index) => [rule, index]).filter(([rule]) => rule.candidate_id === id);
    const sourceRefs = mergedRefs.filter((ref) => {
      let drop = false;
      for (const [rule, index] of rules) {
        if (rule.source_id === ref.source_id && (rule.origin === undefined || rule.origin === ref.origin) && (rule.locator === undefined || rule.locator === ref.locator)) {
          matchedExcludedRefs.add(index);
          drop = true;
        }
      }
      return !drop;
    });
    if (eligible && rules.length && !sourceRefs.length) throw new Error(`${id}: excluded_source_refs cannot remove every source reference from an eligible candidate`);
    return {
      ...main, id, category: classifyCandidate(main), eligible, selected: false,
      aliases: members.map((record) => record.id).filter((member) => member !== id),
      question_variants: members.filter((record) => record.id !== id).map((record) => ({ id: record.id, question: record.question, answer_target: record.answer_target, scope: record.scope })),
      source_refs: sourceRefs,
      provenance_ids: members.map((record) => record.id),
      exclusion_reason: retired ? '含歷史剔除／轉線／暫緩題，保留關係但不得靠新標題復活。' : rejected ? excludes.get(rejected.id) : !eligible ? '缺來源或前提待查。' : null,
      verification: 'TOPIC_CANDIDATE_NOT_CLAIM_OR_SCRIPT_APPROVAL', production_ready: false,
    };
  });
  if (matchedExcludedRefs.size !== excludedSourceRefs.length) throw new Error('Stale excluded_source_refs decision did not match any source reference');
  const pairs = similarityPairs(input.records, aliases);
  const distinct = new Map((decisions.distinct ?? []).map((item) => {
    if (!byId.has(item.a) || !byId.has(item.b) || !item.reason || resolve(item.a) === resolve(item.b)) throw new Error('Invalid distinct decision');
    return [pairId(item.a, item.b), item.reason];
  }));
  const pending = pairs.filter((pair) => pair.required && !distinct.has(pair.id));
  let selected = [];
  if (selection) {
    if (!Array.isArray(selection.ids) || new Set(selection.ids).size !== selection.ids.length || !selection.reason) throw new Error('Invalid selection manifest');
    for (const id of selection.ids) {
      const entry = candidates.find((candidate) => candidate.id === id);
      if (!entry?.eligible) throw new Error(`${id}: selected id must be an eligible canonical question`);
      entry.selected = true;
    }
    selected = candidates.filter((candidate) => candidate.selected);
    if (selected.length !== selection.target_count) throw new Error('Selected count does not match reviewed target');
    if (pending.length) throw new Error(`${pending.length} high-similarity pairs still need editorial decisions`);
  }
  const byCategory = Object.fromEntries(CATEGORIES.map((cat) => [cat, {
    canonical: candidates.filter((row) => row.category === cat).length,
    selected: selected.filter((row) => row.category === cat).length,
  }]));
  return {
    schema_version: 1, revision: selection?.revision ?? 'unversioned-draft', status: selection ? 'CURATED_CANDIDATE_POOL_NOT_PRODUCTION' : 'DRAFT_INTAKE',
    categories: CATEGORIES,
    counts: { raw_records: input.records.length, canonical_questions: candidates.length, eligible_candidates: candidates.filter((candidate) => candidate.eligible).length, selected_candidates: selected.length, alias_records: input.records.length - candidates.length, historical_records: input.records.filter((record) => record.origin === 'legacy').length, source_urls: input.sources.length, current_research_source_urls: input.sources.filter((source) => source.readings.some((reading) => !reading.origin.startsWith('legacy:'))).length, selected_source_urls: new Set(selected.flatMap((row) => row.source_refs.map((ref) => ref.source_id))).size, new_suggestions_not_added: input.not_added?.length ?? 0, high_similarity_pending: pending.length, approved_scripts: 0, by_category: byCategory },
    inputs: input.inputs, sources: input.sources, candidates, raw_records: input.records,
    dedup: { aliases, merges: links, distinct: decisions.distinct ?? [], excluded: decisions.excluded ?? [], ...(excludedSourceRefs.length ? { excluded_source_refs: excludedSourceRefs } : {}), potential_pairs: pairs, required_pending: pending, method: 'exact normalized questions + authored core-question merges + lexical/target candidates and editorial review; no claim of exhaustive semantic equivalence' },
    selection: selection ?? null, not_added: input.not_added ?? [],
  };
}

export function loadDraft(root = ROOT) {
  const input = intake(root);
  const file = `${DIR}/dedup-decisions.json`;
  const decisions = existsSync(path.join(root, file)) ? parse(root, file) : { merges: [], distinct: [], excluded: [] };
  if (existsSync(path.join(root, file))) input.inputs.push({ file, sha256: hash(readFileSync(path.join(root, file))) });
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
  if (JSON.stringify(saved) !== JSON.stringify(current)) throw new Error('Pool drift: inputs, source packets or decisions changed; re-review and build');
  return saved;
}

export function writeJson(root, name, value) {
  const directory = path.join(root, DIR);
  mkdirSync(directory, { recursive: true });
  writeFileSync(path.join(directory, name), `${JSON.stringify(value, null, 2)}\n`);
}
