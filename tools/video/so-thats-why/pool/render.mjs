import { CATEGORIES, classifyCandidate } from './core.mjs';

const cell = (value) => String(value ?? '').replaceAll('|', '／').replaceAll('\n', ' ');
const sourceLabel = (source, reading) => reading.origin.startsWith('legacy:') ? `${new URL(source.url).hostname}${new URL(source.url).pathname}` : reading.title;
const rowCategory = (row) => row?.category ?? classifyCandidate(row ?? {});

export function themeCategory(episode, byId) {
  if (episode.category) return episode.category;
  const tally = new Map();
  for (const id of episode.candidate_ids ?? []) {
    const cat = rowCategory(byId.get(id));
    if (cat) tally.set(cat, (tally.get(cat) ?? 0) + 1);
  }
  let best = null; let bestCount = -1;
  for (const [cat, count] of tally) if (count > bestCount) { best = cat; bestCount = count; }
  return best ?? CATEGORIES[0];
}

export function readingsForCandidate(source, row) {
  const refs = row.source_refs.filter((ref) => ref.source_id === source.id);
  if (!refs.length) return [];
  const origins = new Set(refs.map((ref) => ref.origin));
  const ids = new Set([row.id, ...(row.provenance_ids ?? [])]);
  return source.readings.filter((reading) => origins.has(reading.origin)
    || (Array.isArray(reading.applies_to_candidate_ids) && reading.applies_to_candidate_ids.some((id) => ids.has(id))));
}

export function renderSources(pool) {
  const selected = new Set(pool.candidates.filter((row) => row.selected).flatMap((row) => row.source_refs.map((ref) => ref.source_id)));
  const lines = ['# 素材來源索引', '', '精確 URL 已合併，同頁不同讀取範圍各自保留。查閱紀錄表示題級來源閱讀，不代表每一生活例證、完整答案或畫面使用權已通過。歷史包未讀外站的紀錄沒有填新查閱日。', '', '| 來源 ID | 頁面／機構 | 查閱範圍與日期 | 入選候選使用 |', '| --- | --- | --- | --- |'];
  for (const source of [...pool.sources].sort((a, b) => Number(b.readings.some((r) => !r.origin.startsWith('legacy:'))) - Number(a.readings.some((r) => !r.origin.startsWith('legacy:'))) || a.id.localeCompare(b.id))) {
    const reading = source.readings.find((item) => !item.origin.startsWith('legacy:')) ?? source.readings[0];
    const scopes = [...new Set(source.readings.map((item) => `${cell(item.origin)}：${cell(item.reading_scope)}；定位 ${cell(item.locator)}；${item.accessed_on ?? '歷史引用，當期未讀外站'}`))];
    lines.push(`| ${source.id} | [${cell(sourceLabel(source, reading))}](${source.url})<br>${cell(reading.publisher)} | ${scopes.join('<br>')} | ${selected.has(source.id) ? '是' : '歷史／候補索引'} |`);
  }
  return `${lines.join('\n')}\n`;
}

export function renderQuestions(pool) {
  const chosen = pool.candidates.filter((row) => row.selected);
  const categories = [...CATEGORIES, ...new Set(chosen.map(rowCategory).filter((cat) => !CATEGORIES.includes(cat)))];
  const lines = [`# ${chosen.length} 筆原來如此素材候選`, '', '每筆是不同核心問題的初篩候選，不等於一支長片或已審劇本。全池依 7 大分類歸檔（與雲端硬碟 `AI/備份/AI劇/原來如此事務所/<分類>/` 一致），保留原細類供精確篩選。來源及適用範圍可用本機搜尋頁查看；歷史來源須刷新，新研究的推導例子仍需補直接證據。', '', '[可成片清單](PRODUCIBLE.html) · [可搜尋清單](index.html) · [來源索引](SOURCES.md) · [影片主題組合](THEMES.md) · [去重紀錄](DEDUP.md)', ''];
  for (const cat of categories) {
    const rows = chosen.filter((row) => rowCategory(row) === cat).sort((a, b) => (a.domain || '').localeCompare(b.domain || '') || a.id.localeCompare(b.id, 'en', { numeric: true }));
    if (!rows.length) continue;
    lines.push(`## ${cat}（${rows.length}）`, '', '| ID | 細類 | 疑問 | 要研究的機制／差別 | 段落預估（未試讀） | 來源數 |', '| --- | --- | --- | --- | --- | --- |');
    for (const row of rows) lines.push(`| [${row.id}](index.html#${row.id}) | ${cell(row.domain)} | ${cell(row.question)} | ${cell(row.answer_target)} | ${row.editorial ? `${row.editorial.seconds.join('–')} 秒` : '待逐題評估'} | ${new Set(row.source_refs.map((ref) => ref.source_id)).size} |`);
    lines.push('');
  }
  return `${lines.join('\n').trimEnd()}\n`;
}

export function renderDedup(pool) {
  const lines = ['# 去重與保留理由', '', `原始紀錄 ${pool.counts.raw_records}；合併後核心問題 ${pool.counts.canonical_questions}；別名紀錄 ${pool.counts.alias_records}；本輪選入 ${pool.counts.selected_candidates}。`, '', '完整問題正規化相同可自動合併；相似分數只提候選，由編輯判斷核心答案和條件。保留每個原 ID、來源與處置理由，沒有刪掉原題。分數不能證明所有語意重複均被找出。', '', '## 合併', '', '| 原 ID | 指向 | 理由 |', '| --- | --- | --- |'];
  for (const item of pool.dedup.merges) lines.push(`| ${item.duplicate_id} | ${pool.dedup.aliases[item.canonical_id]} | ${cell(item.reason)} |`);
  lines.push('', '## 看似相近但保留分開', '', '| 問題一 | 問題二 | 差別 |', '| --- | --- | --- |');
  for (const item of pool.dedup.distinct) lines.push(`| ${item.a} | ${item.b} | ${cell(item.reason)} |`);
  lines.push('', '## 本輪另行退題', '', '| ID | 理由 |', '| --- | --- |');
  for (const item of pool.dedup.excluded) lines.push(`| ${item.id} | ${cell(item.reason)} |`);
  if (pool.dedup.excluded_source_refs?.length) {
    lines.push('', '## 排除的無關來源引用', '', '| 核心 ID | 來源 ID | 範圍過濾 | 理由 |', '| --- | --- | --- | --- |');
    for (const item of pool.dedup.excluded_source_refs) lines.push(`| ${item.candidate_id} | ${item.source_id} | ${cell([item.origin, item.locator].filter(Boolean).join(' · ') || '全部匹配引用')} | ${cell(item.reason)} |`);
  }
  lines.push('', `其他歷史剔除、暫緩與轉系列保留在 pool.json 的 prior_decision／exclusion_reason，不因新批次出現相似標題就復活。未入本輪 ${pool.counts.selected_candidates.toLocaleString('en-US')} 筆的合格題保留候補狀態，不冒稱已採用。`);
  return `${lines.join('\n')}\n`;
}

// The material review (reviews/material-20261111.md; owner 2026-11-11): the eight-minute floor stays for a
// long episode, and a long theme whose material would need padding waits (reserve), waits for a named partner
// (merge) or is dropped, instead of being made. Short explainers are not reviewed against that floor.
export const MATERIAL_VERDICTS = Object.freeze({ ready: '可成題', merge: '待合併', reserve: '後備', drop: '淘汰' });

// 獨立觀眾評分（站主 2026-11-14「把分數寫回題目池」）：未參與撰稿的評審只讀題案的片名、追問與章節，
// 以第一次滑到的一般觀眾打五項 1–10 分；共同錨點題校正評審鬆緊。是題案吸引力的參考，不是成片評分或點閱率預測。
export const AUDIENCE_DIMENSIONS = Object.freeze({ click: '點擊', hook: '鉤子', surprise: '驚喜', payoff: '兌現', share: '分享' });
export function validateAudience(owner, audience) {
  if (audience === undefined) return;
  const inRange = (value) => Number.isFinite(value) && value >= 1 && value <= 10;
  if (!audience || !inRange(audience.score) || Object.keys(AUDIENCE_DIMENSIONS).some((key) => !inRange(audience[key]))) throw new Error(`${owner}: audience needs score and ${Object.keys(AUDIENCE_DIMENSIONS).join(', ')} between 1 and 10`);
  if (!Number.isInteger(audience.rank) || !Number.isInteger(audience.of) || audience.rank < 1 || audience.rank > audience.of) throw new Error(`${owner}: audience rank must be 1..of`);
  if (!audience.comment || !/^\d{4}-\d{2}-\d{2}$/.test(audience.reviewed_on ?? '') || !/^reviews\/audience-[\w-]+\.json$/.test(audience.review ?? '')) throw new Error(`${owner}: audience needs a comment, reviewed_on and its reviews/audience-*.json record`);
}
const audienceLine = (audience) => `**獨立觀眾評分：** ${audience.score.toFixed(2)}／10（第 ${audience.rank}／${audience.of} 名；${Object.entries(AUDIENCE_DIMENSIONS).map(([key, label]) => `${label} ${audience[key]}`).join('、')}）— ${cell(audience.comment)}（${audience.reviewed_on}，[${audience.review}](${audience.review})）`;
function audienceRanking(episodes) {
  const scored = episodes.filter((episode) => episode.audience).sort((a, b) => a.audience.rank - b.audience.rank);
  if (!scored.length) return [];
  const { reviewed_on: on, review } = scored[0].audience;
  return ['', `## 獨立觀眾評分排名（${on}）`, '', `${scored.length} 組長題由未參與撰稿的評審以一般觀眾的角度讀題案打分（點擊、鉤子、驚喜、兌現、分享各 1–10，取平均；共同錨點題校正評審鬆緊；紀錄在 [${review}](${review})）。這是題案吸引力的參考，不是成片評分，也不是點閱率預測。`, '', '| 名次 | ID | 題案 | 分數 | 觀眾短評 |', '| --- | --- | --- | --- | --- |', ...scored.map((episode) => `| ${episode.audience.rank} | ${episode.id} | ${cell(episode.title)} | ${episode.audience.score.toFixed(2)} | ${cell(episode.audience.comment)} |`)];
}

export function validateThemes(themes, pool) {
  if (!Array.isArray(themes.episodes) || !themes.episodes.length) throw new Error('Theme list is empty');
  if (new Set(themes.episodes.map((episode) => episode.id)).size !== themes.episodes.length) throw new Error('Duplicate theme id');
  for (const episode of themes.episodes) {
    for (const key of ['id', 'title', 'core_question', 'connection', 'boredom_risk', 'drop_if', 'evidence_gaps']) if (!episode[key]) throw new Error(`${episode.id}: missing ${key}`);
    if (episode.category !== undefined && !CATEGORIES.includes(episode.category)) throw new Error(`${episode.id}: unknown category ${episode.category}`);
    if (episode.production_ready !== false || episode.status !== 'EDITORIAL_THEME_NOT_SCRIPT') throw new Error('A theme cannot grant production approval');
    validateAudience(episode.id, episode.audience);
    // 站主 2026-11-14：之後擴充出的可成題長題也要補獨立觀眾評分，沒評分不能進池。
    if (episode.audience === undefined && episode.target_minutes >= 8 && episode.material?.verdict === 'ready') throw new Error(`${episode.id}: a producible long theme needs an independent audience score (theme.audience, recorded in reviews/audience-*.json); see the pool README`);
    if (!Number.isFinite(episode.target_minutes) || episode.target_minutes <= 0 || !Array.isArray(episode.range_minutes) || episode.range_minutes.length !== 2 || episode.range_minutes.some((n) => !Number.isFinite(n) || n <= 0)) throw new Error(`${episode.id}: invalid duration`);
    if (!episode.candidate_ids?.length || new Set(episode.candidate_ids).size !== episode.candidate_ids.length) throw new Error('Theme needs unique candidate ids');
    if (episode.candidate_ids.some((id) => !pool.candidates.some((row) => row.id === id && row.selected))) throw new Error(`${episode.id}: theme includes an unselected or alias record`);
    const minimumChapters = episode.format === 'short_explainer' ? 2 : 4;
    if (!episode.chapters?.length || episode.chapters.length < minimumChapters || episode.chapters.some((chapter) => !chapter.title || !Number.isInteger(chapter.seconds) || chapter.seconds <= 0 || !chapter.new_information || !chapter.candidate_ids?.length || chapter.candidate_ids.some((id) => !episode.candidate_ids.includes(id)))) throw new Error(`${episode.id}: every chapter needs selected evidence and a new judgement`);
    if (Math.abs(episode.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0) - episode.target_minutes * 60) > 1e-9) throw new Error(`${episode.id}: invalid time budget`);
    if (episode.range_minutes[0] > episode.target_minutes || episode.range_minutes[1] < episode.target_minutes) throw new Error(`${episode.id}: time range does not include target`);
    if (episode.material !== undefined) {
      const material = episode.material;
      if (!Object.hasOwn(MATERIAL_VERDICTS, material?.verdict) || !material.reviewed_on || !material.review || !Number.isFinite(material.est_minutes)) throw new Error(`${episode.id}: material needs a verdict (${Object.keys(MATERIAL_VERDICTS).join(', ')}), est_minutes, reviewed_on and review`);
      if (material.verdict !== 'ready' && !material.missing) throw new Error(`${episode.id}: a ${material.verdict} theme says what is missing`);
      if (material.verdict === 'merge' && !material.merge_with) throw new Error(`${episode.id}: a merge theme names what it merges with`);
      if (material.verdict === 'ready' && material.est_minutes < 8.5) throw new Error(`${episode.id}: a ready long theme carries at least 8.5 minutes of material`);
    }
  }
  return themes;
}

export function renderThemes(themes, pool) {
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  const lines = ['# 從素材池挑出的影片主題', '', `${themes.episodes.length} 組編輯候選；由來源、共同追問與章節推進選出，不是點閱率預測或已核准影片。時間是正文估計，尚未試讀；每章須再拆成 30–45 秒內有資訊推進的節拍。標題只是包裝提案，未查的例子不可寫成事實。`, '', '**素材審視（2026-11-11）：** 長題照 8 分鐘下限逐題重算，素材撐不起不重複旁白的列為後備、待合併或淘汰，缺什麼寫在各題審視欄（[reviews/material-20261111.md](reviews/material-20261111.md)）。短題不受此下限審視，欄位寫「未審」。', '', '| 順序 | 分類 | 主題 | 正文估計 | 素材數 | 素材審視 |', '| --- | --- | --- | --- | --- | --- |'];
  for (const episode of themes.episodes) {
    const cat = themeCategory(episode, byId);
    const seconds = episode.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0);
    const duration = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
    const range = episode.range_minutes.map((minutes) => {
      const total = Math.round(minutes * 60);
      return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, '0')}`;
    }).join('–');
    lines.push(`| ${episode.id} | ${cat} | ${episode.title} | ${duration}（工作範圍 ${range}；分:秒；未試讀） | ${episode.candidate_ids.length} | ${episode.material ? `${MATERIAL_VERDICTS[episode.material.verdict]}（素材約 ${episode.material.est_minutes} 分）` : '未審'} |`);
  }
  lines.push(...audienceRanking(themes.episodes));
  for (const episode of themes.episodes) {
    const cat = themeCategory(episode, byId);
    const material = episode.material;
    const verdict = material ? [`**素材審視：** ${MATERIAL_VERDICTS[material.verdict]}，素材約 ${material.est_minutes} 分`, material.missing ? `；缺：${material.missing}` : '', material.merge_with ? `；合併對象：${material.merge_with}` : ''].join('') : '';
    lines.push('', `## ${episode.id} ${episode.title}`, '', `**分類：** ${cat}`, '', ...(verdict ? [verdict, ''] : []), ...(episode.audience ? [audienceLine(episode.audience), ''] : []), `**追問：** ${episode.core_question}`, '', `**為什麼能接成一集：** ${episode.connection}`, '', '| 段落 | 秒數預算 | 新增理解 | 使用素材 |', '| --- | --- | --- | --- |');
    for (const chapter of episode.chapters) lines.push(`| ${chapter.title} | ${chapter.seconds} | ${chapter.new_information} | ${chapter.candidate_ids.join('、')} |`);
    for (const variantId of episode.variant_budget_ids ?? []) {
      const variant = pool.raw_records.find((row) => row.id === variantId);
      if (variant) lines.push('', `本片採用合併案例 **${variantId} ${variant.question}**（核心 ${pool.dedup.aliases[variantId]}）；使用此案例已審的段落預算，不另計素材或加上原情境的秒數。`);
    }
    lines.push('', '**素材與來源：**', '');
    for (const id of episode.candidate_ids) {
      const row = byId.get(id);
      const ids = [...new Set(row.source_refs.map((ref) => ref.source_id))];
      lines.push(`- ${id} ${row.question} — ${ids.slice(0, 3).map((sourceId) => { const source = pool.sources.find((item) => item.id === sourceId); return `[${new URL(source.url).hostname}](${source.url})`; }).join('、')}。${row.notes}`);
    }
    lines.push('', `**可能無聊的地方：** ${episode.boredom_risk}`, '', `**先刪／撤題條件：** ${episode.drop_if}`, '', `**待補證據：** ${episode.evidence_gaps}`);
  }
  return `${lines.join('\n')}\n`;
}

export function renderHtml(pool, themes) {
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  const chosen = pool.candidates.filter((row) => row.selected).map((row) => ({ ...row, category: rowCategory(row) }));
  const sourceIds = new Set(chosen.flatMap((row) => row.source_refs.map((ref) => ref.source_id)));
  const payload = JSON.stringify({ categories: pool.categories ?? CATEGORIES, candidates: chosen, sources: pool.sources.filter((source) => sourceIds.has(source.id)), themes: themes.episodes.map((episode) => ({ ...episode, category: themeCategory(episode, byId) })) }).replaceAll('<', '\\u003c');
  return `<!doctype html>
<html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>原來如此素材池</title>
<style>body{margin:0;background:#faf6ea;color:#142c42;font:16px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:32px 22px}h1{font-size:32px;margin-bottom:8px}h2{font-size:21px}p{max-width:900px}.eyebrow{color:#8b4a1b;font-weight:700}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.stat{background:#fff;border:1px solid #d4c9ae;padding:14px 22px;border-radius:12px}.stat b{font-size:27px;display:block}.controls{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#faf6eaf5;padding:12px 0}input,select,button{font:inherit;padding:10px 12px;border-radius:8px;border:1px solid #9ca8ad}input{flex:1;min-width:220px}button{cursor:pointer;background:#142c42;color:white}a{color:#155f88}article{background:#fff;border:1px solid #d7d0bd;border-radius:12px;padding:18px 22px;margin:14px 0}summary{cursor:pointer;font-weight:700}small,.muted{color:#526777}.tag{font-size:13px;padding:3px 8px;background:#f1e3b6;border-radius:5px;margin-right:6px;display:inline-block}.detail{border-top:1px solid #e9e4d8;padding-top:12px;margin-top:12px}.sources li{margin:6px 0}.warning{border-left:4px solid #c48a20;padding-left:12px}#count{font-weight:600}@media(max-width:600px){h1{font-size:26px}main{padding:22px 14px}.controls{position:static;display:grid;grid-template-columns:minmax(0,1fr)}input{min-width:0;width:100%;box-sizing:border-box}select{max-width:100%}}</style>
<main><div class="eyebrow">原來如此事務所 · 建立於 2026-11-01</div><h1>${pool.counts.selected_candidates.toLocaleString('en-US')} 個疑問，先找值得追的故事</h1><p>依 7 大分類與細類搜尋生活物件、現象或機制。每筆保留來源、小節與適用範圍，再選能推進同一問題的素材組成影片。</p><p class="warning">這是初篩素材池。題級來源閱讀不等於完整答案已查核；生活例證、逐字稿和實際片長仍要驗證。</p>
<div class="stats"><div class="stat"><b>${pool.counts.selected_candidates}</b>入選素材</div><div class="stat"><b>${sourceIds.size}</b>使用來源頁（含歷史）</div><div class="stat"><b>${themes.episodes.length}</b>影片主題候選</div><div class="stat"><b>${pool.counts.alias_records}</b>合併的別名紀錄</div></div>
<p><a href="PRODUCIBLE.html">可成片清單</a> · <a href="THEMES.md">查看影片章節與片長</a> · <a href="SOURCES.md">完整來源索引</a> · <a href="DEDUP.md">去重紀錄</a> · <a href="README.md">這批怎麼建立</a></p>
<label for="q">找素材</label><div class="controls"><input id="q" type="search" placeholder="例如：冰、葉子、聲音、密碼" aria-label="搜尋素材"><select id="category" aria-label="大分類"><option value="">全部分類（7 類）</option></select><select id="domain" aria-label="細類"><option value="">全部細類</option></select><select id="theme" aria-label="影片主題"><option value="">全部素材</option></select></div><p id="count" aria-live="polite"></p><section id="results"></section><button id="more">再顯示 50 筆</button></main>
<script type="application/json" id="data">${payload}</script>
<script>
const data=JSON.parse(document.getElementById('data').textContent),sources=new Map(data.sources.map(x=>[x.id,x]));
const q=document.getElementById('q'),category=document.getElementById('category'),domain=document.getElementById('domain'),theme=document.getElementById('theme'),results=document.getElementById('results'),more=document.getElementById('more');let limit=50;
for(const c of data.categories){const o=document.createElement('option');o.value=c;o.textContent=c;category.append(o)}
function syncDomains(){const cur=domain.value;domain.replaceChildren();const all=document.createElement('option');all.value='';all.textContent='全部細類';domain.append(all);const list=[...new Set(data.candidates.filter(x=>!category.value||x.category===category.value).map(x=>x.domain))].sort();for(const d of list){const o=document.createElement('option');o.value=d;o.textContent=d;domain.append(o)}domain.value=list.includes(cur)?cur:''}
syncDomains();
for(const t of data.themes){const o=document.createElement('option');o.value=t.id;o.textContent=t.id+' ['+t.category+'] '+t.title;theme.append(o)}
${readingsForCandidate.toString()}
function el(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e}
function render(){const term=q.value.trim().toLocaleLowerCase();const t=data.themes.find(x=>x.id===theme.value);const rows=data.candidates.filter(x=>(!category.value||x.category===category.value)&&(!domain.value||x.domain===domain.value)&&(!t||t.candidate_ids.includes(x.id))&&(!term||(x.id+' '+x.category+' '+x.domain+' '+x.question+' '+x.answer_target+' '+x.scope+' '+JSON.stringify(x.question_variants||[])).toLocaleLowerCase().includes(term)));results.replaceChildren();document.getElementById('count').textContent='找到 '+rows.length+' 筆 · 顯示 '+Math.min(rows.length,limit)+' 筆';for(const row of rows.slice(0,limit)){const card=el('article','');card.id=row.id;card.append(el('span',row.id,'tag'),el('span',row.category,'tag'),el('span',row.domain,'tag'),el('h2',row.question),el('p','要研究：'+row.answer_target));if(row.editorial)card.append(el('p','段落預估：'+row.editorial.seconds.join('–')+' 秒（未試讀；不是整片長度）','muted'));const detail=el('details','');detail.append(el('summary','呈現方式、來源與待查事項'));const body=el('div','','detail');body.append(el('p','範圍：'+row.scope),el('p',row.notes,'muted'));if(row.editorial)body.append(el('p','新增理解：'+row.editorial.payoff),el('p','畫面構想：'+row.editorial.visual));for(const variant of row.question_variants||[])body.append(el('p','合併原題 '+variant.id+'：'+variant.question,'muted'));const ul=el('ul','','sources');for(const id of [...new Set(row.source_refs.map(x=>x.source_id))]){const s=sources.get(id);const refs=row.source_refs.filter(x=>x.source_id===id);const readings=readingsForCandidate(s,row);const reading=readings[0]||s.readings[0];const li=el('li','');const a=el('a',reading.origin.startsWith('legacy:')?new URL(s.url).hostname+new URL(s.url).pathname:reading.title);a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';li.append(a,el('small',' — '+reading.publisher+' · '+(reading.accessed_on||'歷史引用，當期未讀外站')));for(const ref of refs)li.append(el('div','本題定位：'+ref.locator,'muted'));for(const item of readings)li.append(el('div',item.origin+' · '+item.reading_scope+' · '+(item.accessed_on||'當期未讀外站'),'muted'));ul.append(li)}body.append(ul);detail.append(body);card.append(detail);results.append(card)}more.hidden=rows.length<=limit}
category.addEventListener('input',()=>{syncDomains();limit=50;render()});
for(const control of [q,domain,theme])control.addEventListener('input',()=>{limit=50;render()});more.addEventListener('click',()=>{limit+=50;render()});if(location.hash){try{q.value=decodeURIComponent(location.hash.slice(1))}catch{q.value=''}}render();
</script></html>\n`;
}

export function producibleData(pool, themes) {
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  const longReady = themes.episodes.filter((ep) => ep.format !== 'short_explainer' && (ep.material?.verdict ?? 'ready') === 'ready');
  const shortThemes = themes.episodes.filter((ep) => ep.format === 'short_explainer');
  const mapEp = (ep) => ({
    id: ep.id,
    category: themeCategory(ep, byId),
    title: ep.title,
    minutes: ep.material?.est_minutes ?? ep.target_minutes,
    target_minutes: ep.target_minutes,
    q: ep.core_question,
    chapters: ep.chapters.length,
    cores: ep.candidate_ids.map((id) => ({ id, category: rowCategory(byId.get(id)), q: byId.get(id)?.question ?? '' })),
  });
  return {
    revision: pool.revision,
    categories: CATEGORIES,
    long_themes: longReady.map(mapEp),
    short_themes: shortThemes.map(mapEp),
  };
}

export function renderProducible(pool, themes) {
  const payload = JSON.stringify(producibleData(pool, themes)).replaceAll('<', '\\u003c');
  return `<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>原來如此事務所可成片清單</title>
<style>
:root{--bg:#faf6ea;--paper:#fffdf7;--ink:#142c42;--muted:#526777;--line:#d7d0bd;--accent:#8b4a1b;--accent-soft:#f5e6d3;--tab:#ede6d3}
@media (prefers-color-scheme: dark){:root{--bg:#121b24;--paper:#1a2633;--ink:#e8eef4;--muted:#9fb2c2;--line:#2d3d4e;--accent:#e59d5c;--accent-soft:#342619;--tab:#223040;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 system-ui,"Noto Sans TC",sans-serif;padding:28px 16px 48px}
.wrap{max-width:1080px;margin:0 auto;display:grid;gap:20px}
.eyebrow{font-size:12px;letter-spacing:.08em;color:var(--accent);font-weight:700}
h1{font-size:clamp(26px,4vw,36px);margin:4px 0 6px}
.lede,.note,#count,footer{color:var(--muted);margin:0}
.note{font-size:13px;border-left:3px solid var(--accent);padding-left:10px}
.strip{display:flex;flex-wrap:wrap;gap:10px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px 16px}
.stat b{display:block;font-size:24px}
.stat span{font-size:13px;color:var(--muted)}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.tabs{display:flex;gap:4px;background:var(--tab);padding:4px;border-radius:10px}
.tabs button{font:inherit;border:0;background:transparent;color:var(--muted);padding:7px 14px;border-radius:7px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--paper);color:var(--ink);font-weight:700}
input[type=search],select{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px 10px}
input[type=search]{flex:1 1 220px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:8px;align-content:start}
.meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.id{font:600 12px ui-monospace,monospace;color:var(--accent)}
.pill{font-size:12px;padding:1px 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.pill.min{background:transparent;border:1px solid var(--line);color:var(--muted)}
.card h2{font-size:17px;line-height:1.4;margin:0}
.card p{margin:0;color:var(--muted);font-size:14px}
.cores{margin:0;padding:8px 0 0;list-style:none;display:grid;gap:4px;border-top:1px dashed var(--line);font-size:13.5px}
.cores li{display:grid;grid-template-columns:auto 1fr;gap:8px}
footer a{color:var(--accent)}
</style>
</head><body>
<div class="wrap">
  <header>
    <div class="eyebrow">原來如此事務所 · 素材池 ${pool.revision}</div>
    <h1>可成片主題清單（依 7 大分類）</h1>
    <p class="lede">長片題案皆通過 8.5 分鐘素材下限審視且核心問題均有獨立來源；短題候選適合 Shorts 或短篇。開拍前仍須照系列流程完成逐主張查核與試讀。</p>
  </header>
  <div class="strip" id="strip"></div>
  <p class="note">由 <code>tools/video/so-thats-why/pool</code> 的 build 產生，與雲端硬碟 <code>AI/備份/AI劇/原來如此事務所/&lt;分類&gt;/</code> 對齊。</p>
  <div class="controls">
    <div class="tabs" role="tablist" aria-label="清單">
      <button role="tab" id="tab-long" aria-selected="true">可成題長片</button>
      <button role="tab" id="tab-short" aria-selected="false">短題候選</button>
    </div>
    <select id="cat" aria-label="分類"><option value="">全部分類（7 類）</option></select>
    <input id="q" type="search" placeholder="搜尋：問題、現象、關鍵字" aria-label="搜尋">
  </div>
  <p id="count" aria-live="polite"></p>
  <section class="grid" id="list"></section>
  <footer>資料來源：同一目錄的 <a href="THEMES.md">THEMES.md</a>、<a href="QUESTIONS.md">QUESTIONS.md</a> 與 pool.json；搜尋全部入選核心問題見 <a href="index.html">index.html</a>。</footer>
</div>
<script type="application/json" id="data">${payload}</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const $=id=>document.getElementById(id);
const el=(t,c,txt)=>{const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e};
let mode='long';
for(const c of D.categories){const o=el('option',null,c);o.value=c;$('cat').append(o)}
const longCores=D.long_themes.reduce((n,t)=>n+t.cores.length,0);
for(const [n,l] of [[D.long_themes.length,'組可成題長片（共 '+longCores+' 題核心）'],[D.short_themes.length,'組短題候選'],[D.categories.length,'個系列分類']]){const s=el('div','stat');s.append(el('b',null,String(n)),el('span',null,l));$('strip').append(s)}
function setMode(m){mode=m;$('tab-long').setAttribute('aria-selected',m==='long');$('tab-short').setAttribute('aria-selected',m==='short');render()}
$('tab-long').onclick=()=>setMode('long');$('tab-short').onclick=()=>setMode('short');
$('cat').oninput=render;$('q').oninput=render;
function render(){
  const cat=$('cat').value,term=$('q').value.trim().toLowerCase(),list=$('list');list.replaceChildren();
  const src=mode==='long'?D.long_themes:D.short_themes;
  let n=0;
  for(const t of src){
    if(cat&&t.category!==cat)continue;
    const hay=(t.id+t.category+t.title+t.q+t.cores.map(c=>c.id+c.q).join('')).toLowerCase();
    if(term&&!hay.includes(term))continue;n++;
    const c=el('article','card');const m=el('div','meta');
    m.append(el('span','id',t.id),el('span','pill',t.category),el('span','pill min','約 '+t.minutes+' 分'),el('span','pill min',t.cores.length+' 題 · '+t.chapters+' 段'));
    const ul=el('ul','cores');for(const k of t.cores){const li=el('li');li.append(el('span','id',k.id),el('span',null,k.q));ul.append(li)}
    c.append(m,el('h2',null,t.title),el('p',null,t.q),ul);list.append(c);
  }
  $('count').textContent=(mode==='long'?'可成題長片':'短題候選')+'：顯示 '+n+' 筆';
}
setMode(mode);
</script>
</body></html>
`;
}
