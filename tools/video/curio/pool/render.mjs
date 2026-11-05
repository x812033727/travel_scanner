// 奇聞檔案局素材池的題案檢查與輸出頁；照原來如此事務所素材池的 render.mjs。
// 題案（themes.json）照這個池的片長規則：長片 8–13 分鐘，看內容決定，不為了片長硬湊。
import { LONG_MIN, LONG_MAX } from './core.mjs';

const cell = (value) => String(value ?? '').replaceAll('|', '／').replaceAll('\n', ' ');
const STATUS = { selected: '入選', held: '暫緩', reserve: '候補（待研究）', produced: '已製作／製作中', shorts: '轉 Shorts', excluded: '淘汰／轉出' };
const STATUS_ORDER = ['selected', 'held', 'reserve', 'shorts', 'excluded', 'produced'];
const THEME_STATUSES = new Set(['selected', 'held', 'reserve']);
const sourceLabel = (source, reading) => reading.origin.startsWith('legacy:') ? `${new URL(source.url).hostname}${new URL(source.url).pathname}`.slice(0, 90) : reading.title;
const mmss = (seconds) => `${Math.floor(seconds / 60)}:${String(Math.round(seconds % 60)).padStart(2, '0')}`;

export function validateThemes(themes, pool) {
  if (!Array.isArray(themes.episodes) || !themes.episodes.length) throw new Error('Theme list is empty');
  if (new Set(themes.episodes.map((episode) => episode.id)).size !== themes.episodes.length) throw new Error('Duplicate theme id');
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  const used = new Map();
  for (const episode of themes.episodes) {
    for (const key of ['id', 'title', 'core_question', 'connection', 'boredom_risk', 'drop_if', 'evidence_gaps']) if (!episode[key]) throw new Error(`${episode.id}: missing ${key}`);
    if (episode.production_ready !== false || episode.status !== 'EDITORIAL_THEME_NOT_SCRIPT') throw new Error('A theme cannot grant production approval');
    const [lo, hi] = episode.range_minutes ?? [];
    if (!Number.isFinite(episode.target_minutes) || !Number.isFinite(lo) || !Number.isFinite(hi) || lo < LONG_MIN || hi > LONG_MAX || lo > episode.target_minutes || hi < episode.target_minutes) throw new Error(`${episode.id}: a long episode is ${LONG_MIN}–${LONG_MAX} minutes and its range must contain the target; shorter material goes to a sibling theme or Shorts`);
    if (!episode.candidate_ids?.length || new Set(episode.candidate_ids).size !== episode.candidate_ids.length) throw new Error(`${episode.id}: theme needs unique candidate ids`);
    for (const id of episode.candidate_ids) {
      const row = byId.get(id);
      if (!row) throw new Error(`${episode.id}: ${id} is not a canonical core (aliases point to their canonical id)`);
      if (!THEME_STATUSES.has(row.pool_status)) throw new Error(`${episode.id}: ${id} is ${row.pool_status}; only selected, held or reserve cores can be planned`);
      if (used.has(id)) throw new Error(`${id}: used by both ${used.get(id)} and ${episode.id}; one core feeds one episode`);
      used.set(id, episode.id);
    }
    if (!episode.chapters?.length || episode.chapters.length < 4 || episode.chapters.some((chapter) => !chapter.title || !Number.isInteger(chapter.seconds) || chapter.seconds < 30 || !chapter.new_information || !chapter.candidate_ids?.length || chapter.candidate_ids.some((id) => !episode.candidate_ids.includes(id)))) throw new Error(`${episode.id}: needs at least 4 chapters, each ≥30 s with its own evidence and new understanding`);
    const covered = new Set(episode.chapters.flatMap((chapter) => chapter.candidate_ids));
    if (episode.candidate_ids.some((id) => !covered.has(id))) throw new Error(`${episode.id}: every listed core must carry at least one chapter`);
    if (episode.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0) !== Math.round(episode.target_minutes * 60)) throw new Error(`${episode.id}: chapter seconds must add up to the target exactly`);
  }
  // 撐不起一集的新題（chapter 或估不到 8 分鐘）不能單獨入選：要進題案，或轉 Shorts。
  for (const row of pool.candidates.filter((candidate) => candidate.selected && candidate.editorial)) {
    const thin = row.editorial.role === 'chapter' || row.editorial.minutes[1] < LONG_MIN;
    if (thin && !used.has(row.id)) throw new Error(`${row.id}: material for ${row.editorial.minutes.join('–')} min cannot stand alone; put it in a theme with its siblings or turn it into Shorts`);
  }
  return themes;
}

export function themeReadiness(episode, pool) {
  const rows = episode.candidate_ids.map((id) => pool.candidates.find((row) => row.id === id));
  const unsourced = rows.filter((row) => row.pool_status !== 'selected').map((row) => row.id);
  return { ready: !unsourced.length, unsourced };
}

export function renderSources(pool) {
  const selected = new Set(pool.candidates.filter((row) => row.selected).flatMap((row) => row.source_refs.map((ref) => ref.source_id)));
  const lines = ['# 素材來源索引', '', `${pool.counts.source_urls.toLocaleString('en-US')} 個來源網址（正規化後去重）；本輪新讀 ${pool.counts.current_research_source_urls}，入選題使用 ${pool.counts.selected_source_urls}。同一頁的不同讀取各自保留。歷史查核檔與集數研究檔列出的網址只當研究入口，本輪沒有重讀外站，沒有填查閱日。讀得到不等於圖片能用。`, '', '| 來源 ID | 頁面／機構 | 讀取範圍、定位與日期 | 限制 | 入選題使用 |', '| --- | --- | --- | --- | --- |'];
  const fresh = (source) => source.readings.some((reading) => !reading.origin.startsWith('legacy:'));
  for (const source of [...pool.sources].sort((a, b) => Number(fresh(b)) - Number(fresh(a)) || Number(selected.has(b.id)) - Number(selected.has(a.id)) || a.id.localeCompare(b.id))) {
    const reading = source.readings.find((item) => !item.origin.startsWith('legacy:')) ?? source.readings[0];
    const scopes = [...new Set(source.readings.map((item) => `${cell(item.origin)}：${cell(item.locator)}；${item.accessed_on ?? '歷史引用，本輪未讀'}`))];
    const limits = [...new Set(source.readings.map((item) => item.limitations).filter(Boolean))].map(cell);
    lines.push(`| ${source.id} | [${cell(sourceLabel(source, reading))}](${source.url})<br>${cell(reading.publisher)} | ${scopes.join('<br>')} | ${limits.join('<br>')} | ${selected.has(source.id) ? '是' : '歷史／候補'} |`);
  }
  return `${lines.join('\n')}\n`;
}

export function renderQuestions(pool) {
  const rows = pool.candidates;
  const lines = [`# 奇聞檔案局素材池：${rows.length} 個核心題`, '', `入選 ${pool.counts.selected_candidates}、暫緩 ${pool.counts.held_candidates}、候補 ${pool.counts.reserve_candidates}、轉 Shorts ${pool.counts.shorts_candidates}、淘汰或轉出 ${pool.counts.excluded_cores}、已製作或製作中 ${pool.counts.produced_cores}。合併進別題的 ${pool.counts.alias_records} 筆原始紀錄列在主題的「合併原題」。`, '', '「入選」是有可追溯來源、可以排進題案的題，不是已核准的劇本；「候補」是題目卡還沒查、要先研究的題；「已製作」只當去重對象。', '', '[可搜尋清單](index.html) · [影片題案與片長](THEMES.md) · [去重紀錄](DEDUP.md) · [來源索引](SOURCES.md)', ''];
  for (const axis of Object.keys(pool.axes)) {
    const group = rows.filter((row) => row.axis === axis).sort((a, b) => STATUS_ORDER.indexOf(a.pool_status) - STATUS_ORDER.indexOf(b.pool_status) || a.id.localeCompare(b.id, 'en', { numeric: true }));
    if (!group.length) continue;
    lines.push(`## ${axis} ${pool.axes[axis]}（${group.length}）`, '', '| ID | 狀態 | 題目 | 合併原題 | 素材估計 | 來源數 |', '| --- | --- | --- | --- | --- | --- |');
    for (const row of group) lines.push(`| [${row.id}](index.html#${row.id}) | ${STATUS[row.pool_status]} | ${cell(row.question)} | ${row.aliases.join('、')} | ${row.editorial ? `${row.editorial.minutes.join('–')} 分` : ''} | ${new Set(row.source_refs.map((ref) => ref.source_id)).size} |`);
    lines.push('');
  }
  return `${lines.join('\n').trimEnd()}\n`;
}

export function renderDedup(pool) {
  const byId = new Map(pool.raw_records.map((row) => [row.id, row]));
  const title = (id) => cell(byId.get(id)?.question ?? '').slice(0, 40);
  const lines = ['# 去重、合併與淘汰紀錄', '', `原始紀錄 ${pool.counts.raw_records}；合併後核心題 ${pool.counts.canonical_cores}；別名紀錄 ${pool.counts.alias_records}；入選 ${pool.counts.selected_candidates}。`, '', '只有完整題目正規化後相同才會自動合併。其餘的合併、保留分開、淘汰與轉出，都由編輯比較核心答案後寫下理由；相似分數只用來找要比較的對象。換地點、換年份、換主角不算新題。每個原 ID 與來源都保留，沒有刪掉原題。已製作或製作中的題只能當合併的主題，不能被併掉或淘汰。', '', '## 合併（同一個核心答案）', '', '| 原 ID | 原題 | 併入 | 理由 |', '| --- | --- | --- | --- |'];
  for (const item of pool.dedup.merges) lines.push(`| ${item.duplicate_id} | ${title(item.duplicate_id)} | ${pool.dedup.aliases[item.canonical_id]} ${title(pool.dedup.aliases[item.canonical_id])} | ${cell(item.reason)} |`);
  const group = (kind, heading, columns) => {
    const items = pool.dedup.dispositions.filter((item) => item.disposition === kind);
    lines.push('', `## ${heading}（${items.length}）`, '', columns, columns.replace(/[^|]+/g, ' --- '));
    for (const item of items) lines.push(kind === 'transfer' ? `| ${item.id} | ${title(item.id)} | ${cell(item.transfer_to)} | ${cell(item.reason)} |` : kind === 'drop' ? `| ${item.id} | ${title(item.id)} | ${cell(item.reason)} | ${cell(item.reentry)} |` : `| ${item.id} | ${title(item.id)} | ${cell(item.reason)} |`);
  };
  group('drop', '淘汰：太薄、無聊或撐不起一集，也沒有可併的兄弟題', '| ID | 題目 | 理由 | 重新收錄的條件 |');
  group('shorts', '轉 Shorts：有一個好轉折，但不夠撐長片', '| ID | 題目 | 理由 |');
  group('transfer', '轉到別的系列', '| ID | 題目 | 轉到 | 理由 |');
  lines.push('', '## 看似相近但保留分開', '', '| 題一 | 題二 | 差別 |', '| --- | --- | --- |');
  for (const item of pool.dedup.distinct) lines.push(`| ${item.a} ${title(item.a)} | ${item.b} ${title(item.b)} | ${cell(item.reason)} |`);
  lines.push('', '## 跨系列查重（對原來如此事務所）', '', pool.external ? `對照 ${pool.external.series}素材池 ${pool.external.core_count.toLocaleString('en-US')} 個核心題（commit \`${pool.external.commit.slice(0, 12)}\`，${pool.external.pool_revision}）。` : '沒有外部素材池快照。', '', '| 奇聞題 | 原來如此題 | 處置 | 理由 |', '| --- | --- | --- | --- |');
  for (const item of pool.dedup.cross_series) lines.push(`| ${item.id} ${title(item.id)} | ${item.external_id} | ${item.decision === 'transfer' ? '轉出' : '保留分開'} | ${cell(item.reason)} |`);
  lines.push('', '## 新批次沒收的方向', '', '| 點子 | 理由 | 相關既有題 |', '| --- | --- | --- |');
  for (const item of pool.not_added) lines.push(`| ${cell(item.question)} | ${cell(item.reason)} | ${(item.existing_ids ?? []).join('、')} |`);
  lines.push('', `高相似但還沒處置的配對：題庫內 ${pool.counts.high_similarity_pending}、跨系列 ${pool.counts.cross_series_pending}。這兩個數字不是 0 時不能 build。`);
  return `${lines.join('\n')}\n`;
}

export function renderThemes(themes, pool) {
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  const lines = ['# 從素材池排出的影片題案', '', `${themes.episodes.length} 組編輯候選。每一組都是同一個核心問題的兄弟題，接起來比各自單做更完整；不是點閱率預測，也不是已核准的影片。`, '', `**片長規則：** 長片 ${LONG_MIN}–${LONG_MAX} 分鐘，看素材決定。章節秒數是正文預估，還沒試讀；每章要再拆成 30–45 秒一個新資訊或懸念。撐不住就剪短、合併或撤案，不用重述、停頓或慢唸補時間。估不到 ${LONG_MIN} 分鐘的轉 Shorts 或留在後備。`, '', '「來源待補」的題案裡有還沒研究的候補題：要先查核、改成入選，才能寫企劃。', '', '| ID | 題案 | 正文估計 | 核心題數 | 來源 |', '| --- | --- | --- | --- | --- |'];
  for (const episode of themes.episodes) {
    const readiness = themeReadiness(episode, pool);
    lines.push(`| ${episode.id} | ${cell(episode.title)} | ${mmss(episode.target_minutes * 60)}（範圍 ${mmss(episode.range_minutes[0] * 60)}–${mmss(episode.range_minutes[1] * 60)}；未試讀） | ${episode.candidate_ids.length} | ${readiness.ready ? '已有可追溯來源' : `來源待補：${readiness.unsourced.join('、')}`} |`);
  }
  for (const episode of themes.episodes) {
    lines.push('', `## ${episode.id} ${episode.title}`, '', `**追問：** ${episode.core_question}`, '', `**為什麼接成一集：** ${episode.connection}`, '', '| 章 | 秒數 | 新增理解 | 用到的題 | 刪段條件 |', '| --- | --- | --- | --- | --- |');
    for (const chapter of episode.chapters) lines.push(`| ${cell(chapter.title)} | ${chapter.seconds} | ${cell(chapter.new_information)} | ${chapter.candidate_ids.join('、')} | ${cell(chapter.cut_if ?? '')} |`);
    lines.push('', '**用到的題與來源：**', '');
    for (const id of episode.candidate_ids) {
      const row = byId.get(id);
      const ids = [...new Set(row.source_refs.map((ref) => ref.source_id))];
      const links = ids.slice(0, 3).map((sourceId) => { const source = pool.sources.find((item) => item.id === sourceId); return `[${new URL(source.url).hostname}](${source.url})`; });
      lines.push(`- ${id}（${STATUS[row.pool_status]}）${cell(row.question)}${row.aliases.length ? `；合併原題 ${row.aliases.join('、')}` : ''} — ${links.length ? links.join('、') : '還沒有來源'}`);
    }
    lines.push('', `**可能無聊的地方：** ${episode.boredom_risk}`, '', `**撤案條件：** ${episode.drop_if}`, '', `**待補證據：** ${episode.evidence_gaps}`);
  }
  const shorts = pool.candidates.filter((row) => row.pool_status === 'shorts');
  lines.push('', `## 轉 Shorts（${shorts.length}）`, '', '| ID | 題目 | 理由 |', '| --- | --- | --- |');
  for (const row of shorts) lines.push(`| ${row.id} | ${cell(row.question)} | ${cell(row.disposition.reason)} |`);
  return `${lines.join('\n')}\n`;
}

export function renderHtml(pool, themes) {
  const shown = pool.candidates.filter((row) => row.pool_status !== 'excluded');
  const sourceIds = new Set(shown.flatMap((row) => row.source_refs.map((ref) => ref.source_id)));
  const slim = (row) => ({ id: row.id, axis: row.axis, domain: row.domain, question: row.question, hook: row.hook, answer_target: row.answer_target, scope: row.scope, notes: row.notes, pool_status: row.pool_status, status_label: STATUS[row.pool_status], aliases: row.question_variants.map((variant) => ({ id: variant.id, question: variant.question })), editorial: row.editorial ?? null, disposition: row.disposition, production: row.production.locators.slice(0, 3), source_refs: row.source_refs.map((ref) => ({ source_id: ref.source_id, origin: ref.origin, locator: ref.locator })) });
  const payload = JSON.stringify({ candidates: shown.map(slim), sources: pool.sources.filter((source) => sourceIds.has(source.id)).map((source) => ({ id: source.id, url: source.url, readings: source.readings.map((reading) => ({ origin: reading.origin, title: reading.title, publisher: reading.publisher, accessed_on: reading.accessed_on, locator: reading.locator, limitations: reading.limitations ?? '' })) })), themes: themes.episodes.map((episode) => ({ id: episode.id, title: episode.title, candidate_ids: episode.candidate_ids })), axes: pool.axes, statuses: STATUS }).replaceAll('<', '\\u003c');
  return `<!doctype html>
<html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>奇聞檔案局素材池</title>
<style>:root{--bg:#f6f1e7;--card:#fffdf8;--ink:#2a2233;--muted:#6a5f72;--line:#ddd2c2;--accent:#7a3e8e;--tag:#efe2f3;--warn:#b5651d}@media (prefers-color-scheme:dark){:root{--bg:#1b1720;--card:#252030;--ink:#efe9f4;--muted:#b4a9bf;--line:#3d3548;--accent:#d29be6;--tag:#3a2d45;--warn:#e7a35f}}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,"Noto Sans TC",sans-serif}main{max-width:1120px;margin:auto;padding:32px 22px}h1{font-size:30px;margin:4px 0 8px}h2{font-size:19px;margin:8px 0}p{max-width:900px}.eyebrow{color:var(--accent);font-weight:700}.stats{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}.stat{background:var(--card);border:1px solid var(--line);padding:10px 18px;border-radius:12px}.stat b{font-size:24px;display:block}.controls{display:flex;gap:10px;flex-wrap:wrap;position:sticky;top:0;background:var(--bg);padding:12px 0;z-index:1}input,select,button{font:inherit;padding:9px 12px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}input{flex:1;min-width:220px}button{cursor:pointer;background:var(--accent);color:var(--bg);border:0}a{color:var(--accent)}article{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:12px 0;overflow-wrap:anywhere}summary{cursor:pointer;font-weight:700}small,.muted{color:var(--muted)}.tag{font-size:13px;padding:2px 8px;background:var(--tag);border-radius:5px;margin-right:6px;display:inline-block}.detail{border-top:1px solid var(--line);padding-top:10px;margin-top:10px}.sources li{margin:6px 0}.warning{border-left:4px solid var(--warn);padding-left:12px}#count{font-weight:600}@media(max-width:600px){h1{font-size:24px}main{padding:20px 16px}.controls{position:static}input,select{min-width:0;width:100%}}</style>
<main><div class="eyebrow">奇聞檔案局 · 素材池 ${pool.revision}</div><h1>${pool.counts.canonical_cores} 個核心題，先找值得開的檔案</h1><p>題庫、已製作的集數、分支上的草稿與新研究的題，依核心答案去重後放在一起。每筆保留原 ID、合併的原題、來源與定位。</p><p class="warning">這是選題用的素材池，不是查核過的劇本。「入選」只代表有可追溯來源；「候補」的題目卡還沒查；舊查核檔的網址本輪沒有重讀。</p>
<div class="stats"><div class="stat"><b>${pool.counts.selected_candidates}</b>入選</div><div class="stat"><b>${pool.counts.reserve_candidates}</b>候補（待研究）</div><div class="stat"><b>${pool.counts.produced_cores}</b>已製作／製作中</div><div class="stat"><b>${pool.counts.alias_records}</b>併入別題</div><div class="stat"><b>${pool.counts.excluded_cores + pool.counts.shorts_candidates}</b>淘汰／轉出／轉 Shorts</div><div class="stat"><b>${themes.episodes.length}</b>影片題案</div></div>
<p><a href="THEMES.md">影片題案與片長</a> · <a href="DEDUP.md">去重與淘汰紀錄</a> · <a href="SOURCES.md">來源索引</a> · <a href="QUESTIONS.md">全部題目</a> · <a href="README.md">這個池怎麼建</a></p>
<label for="q">找題目</label><div class="controls"><input id="q" type="search" placeholder="例如：1947、燈塔、預言、格林" aria-label="搜尋題目"><select id="axis" aria-label="軸"><option value="">全部軸</option></select><select id="status" aria-label="狀態"><option value="">全部狀態</option></select><select id="theme" aria-label="影片題案"><option value="">全部題目</option></select></div><p id="count" aria-live="polite"></p><section id="results"></section><button id="more">再顯示 50 筆</button></main>
<script type="application/json" id="data">${payload}</script>
<script>
const data=JSON.parse(document.getElementById('data').textContent),sources=new Map(data.sources.map(x=>[x.id,x]));
const q=document.getElementById('q'),axis=document.getElementById('axis'),status=document.getElementById('status'),theme=document.getElementById('theme'),results=document.getElementById('results'),more=document.getElementById('more');let limit=50;
for(const [k,v] of Object.entries(data.axes)){const o=document.createElement('option');o.value=k;o.textContent=k+' '+v;axis.append(o)}
for(const [k,v] of Object.entries(data.statuses)){if(k==='excluded')continue;const o=document.createElement('option');o.value=k;o.textContent=v;status.append(o)}
for(const t of data.themes){const o=document.createElement('option');o.value=t.id;o.textContent=t.id+' '+t.title;theme.append(o)}
function el(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e}
function render(){const term=q.value.trim().toLocaleLowerCase();const t=data.themes.find(x=>x.id===theme.value);const rows=data.candidates.filter(x=>(!axis.value||x.axis===axis.value)&&(!status.value||x.pool_status===status.value)&&(!t||t.candidate_ids.includes(x.id))&&(!term||(x.id+' '+x.question+' '+x.hook+' '+x.answer_target+' '+JSON.stringify(x.aliases)).toLocaleLowerCase().includes(term)));results.replaceChildren();document.getElementById('count').textContent='找到 '+rows.length+' 筆 · 顯示 '+Math.min(rows.length,limit)+' 筆';for(const row of rows.slice(0,limit)){const card=el('article','');card.id=row.id;card.append(el('span',row.id,'tag'),el('span',row.domain,'tag'),el('span',row.status_label,'tag'),el('h2',row.question));if(row.hook)card.append(el('p',row.hook));if(row.editorial)card.append(el('p','素材估計：'+row.editorial.minutes.join('–')+' 分鐘（'+(row.editorial.role==='chapter'?'撐不起單集，要跟兄弟題併':'可當一集的主幹')+'；未試讀）','muted'));if(row.disposition)card.append(el('p','處置：'+row.disposition.reason,'muted'));const detail=el('details','');detail.append(el('summary','紀錄怎麼說、合併的原題與來源'));const body=el('div','','detail');if(row.answer_target)body.append(el('p','紀錄：'+row.answer_target));body.append(el('p','範圍：'+row.scope,'muted'));if(row.notes)body.append(el('p',row.notes,'muted'));for(const a of row.aliases)body.append(el('p','合併原題 '+a.id+'：'+a.question,'muted'));for(const p of row.production)body.append(el('p','製作位置：'+p,'muted'));const ul=el('ul','','sources');for(const id of [...new Set(row.source_refs.map(x=>x.source_id))]){const s=sources.get(id);const refs=row.source_refs.filter(x=>x.source_id===id);const reading=s.readings.find(x=>refs.some(r=>r.origin===x.origin))||s.readings[0];const li=el('li','');const a=el('a',reading.origin.startsWith('legacy:')?(new URL(s.url).hostname+new URL(s.url).pathname).slice(0,80):reading.title);a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';li.append(a,el('small',' — '+reading.publisher+' · '+(reading.accessed_on||'歷史引用，本輪未讀')));for(const ref of refs)li.append(el('div','定位：'+ref.locator,'muted'));if(reading.limitations)li.append(el('div','限制：'+reading.limitations,'muted'));ul.append(li)}if(!row.source_refs.length)body.append(el('p','還沒有可追溯來源。','muted'));body.append(ul);detail.append(body);card.append(detail);results.append(card)}more.hidden=rows.length<=limit}
for(const control of [q,axis,status,theme])control.addEventListener('input',()=>{limit=50;render()});more.addEventListener('click',()=>{limit+=50;render()});if(location.hash){try{q.value=decodeURIComponent(location.hash.slice(1))}catch{q.value=''}}render();
</script></html>
`;
}

// 可成片清單：所有題都已入選的題案，加上沒進任何題案、單獨成集的入選題（給站主排製作用）。
export function producibleData(pool, themes) {
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  const used = new Set(themes.episodes.flatMap((episode) => episode.candidate_ids));
  const short = (text, n) => { const value = (text ?? '').trim(); return value.length <= n ? value : `${value.slice(0, n)}…`; };
  const ready = themes.episodes.filter((episode) => episode.candidate_ids.every((id) => byId.get(id)?.selected));
  return {
    revision: pool.revision, axes: pool.axes,
    themes: ready.map((episode) => ({ id: episode.id, title: episode.title, minutes: episode.target_minutes, q: episode.core_question, chapters: episode.chapters.length, cores: episode.candidate_ids.map((id) => ({ id, axis: byId.get(id).axis, q: byId.get(id).question })) })),
    solo: pool.candidates.filter((row) => row.selected && !used.has(row.id)).map((row) => ({ id: row.id, axis: row.axis, q: row.question, hook: short(row.hook, 110), min: row.editorial ? row.editorial.minutes : null, src: new Set(row.source_refs.map((ref) => ref.source_id)).size, kind: row.id.startsWith('N') ? 'new' : row.screened_in ? 'screened' : 'checked' })),
  };
}

export function renderProducible(pool, themes) {
  const payload = JSON.stringify(producibleData(pool, themes)).replaceAll('<', '\\u003c');
  return `<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>奇聞檔案局可成片清單</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: a case-file register — summary strip, then two drawers (multi-topic episodes, single episodes) filtered by axis. */
:root{
  --bg:#f1f2ee; --paper:#fbfbf8; --ink:#1f2433; --muted:#5d6271; --line:#d9dbd3;
  --accent:#6b3fa0; --accent-soft:#ece4f6; --tab:#e6e7e0; --ok:#2f7d5b;
  --display:"LXGW WenKai TC","Noto Serif TC",serif; --body:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif; --mono:"IBM Plex Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#15171e;--paper:#1d2029;--ink:#e8e9ee;--muted:#a3a7b5;--line:#2f3340;--accent:#c4a2ec;--accent-soft:#2c2340;--tab:#252935;--ok:#79c9a4;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15171e;--paper:#1d2029;--ink:#e8e9ee;--muted:#a3a7b5;--line:#2f3340;--accent:#c4a2ec;--accent-soft:#2c2340;--tab:#252935;--ok:#79c9a4;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:15px/1.65 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 48px}
.wrap{max-width:1040px;margin:0 auto;display:grid;gap:22px}
header{display:grid;gap:8px}
.eyebrow{font:500 12px var(--mono);letter-spacing:.08em;color:var(--accent);text-transform:uppercase}
h1{font:700 clamp(26px,4.4vw,38px)/1.2 var(--display);margin:0;text-wrap:balance}
.lede{color:var(--muted);margin:0;max-width:62ch}
.strip{display:flex;flex-wrap:wrap;gap:10px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px 16px;min-width:0}
.stat b{display:block;font:700 24px var(--display);font-variant-numeric:tabular-nums}
.stat span{color:var(--muted);font-size:13px}
.note{font-size:13px;color:var(--muted);border-left:3px solid var(--accent);padding-left:10px;max-width:70ch}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.tabs{display:flex;gap:4px;background:var(--tab);padding:4px;border-radius:10px}
.tabs button{font:inherit;border:0;background:transparent;color:var(--muted);padding:7px 14px;border-radius:7px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--paper);color:var(--ink);font-weight:700}
input[type=search],select{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px 10px;min-width:0}
input[type=search]{flex:1 1 220px}
button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
#count{font-size:13px;color:var(--muted);margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:8px;align-content:start;min-width:0}
.meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.id{font:500 12px var(--mono);color:var(--accent)}
.pill{font-size:12px;padding:1px 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent);white-space:nowrap}
.pill.min{background:transparent;border:1px solid var(--line);color:var(--muted);font-variant-numeric:tabular-nums}
.card h2{font:700 17px/1.4 var(--display);margin:0;text-wrap:balance}
.card p{margin:0;color:var(--muted);font-size:14px}
.cores{margin:0;padding:0;list-style:none;display:grid;gap:4px;border-top:1px dashed var(--line);padding-top:8px}
.cores li{font-size:13.5px;display:grid;grid-template-columns:auto 1fr;gap:8px}
.cores .id{padding-top:2px}
.empty{color:var(--muted);text-align:center;padding:32px 0}
footer{font-size:13px;color:var(--muted)}
footer a{color:var(--accent)}
@media (max-width:480px){.grid{grid-template-columns:1fr}}
@media (prefers-reduced-motion:no-preference){.card{transition:border-color .15s}.card:hover{border-color:var(--accent)}}
</style>
</head><body>
<div class="wrap">
  <header>
    <div class="eyebrow">奇聞檔案局 · 素材池 ${pool.revision}</div>
    <h1>現在就能排製作的題目</h1>
    <p class="lede">每一題的核心前提都有兩個以上可讀來源，也經過非作者覆核。分兩種：幾題併成一集的題案，與單獨成一集的題。寫企劃前仍要照系列流程逐條查核。</p>
  </header>
  <div class="strip" id="strip"></div>
  <p class="note">由 <code>tools/video/curio/pool</code> 的 build 產生，素材池更新時跟著更新。片長規則：每集 8–13 分鐘，看素材決定。</p>
  <div class="controls">
    <div class="tabs" role="tablist" aria-label="清單">
      <button role="tab" id="tab-themes" aria-selected="true">多題一集</button>
      <button role="tab" id="tab-solo" aria-selected="false">單題一集</button>
    </div>
    <select id="axis" aria-label="軸"><option value="">全部軸</option></select>
    <input id="q" type="search" placeholder="搜尋：年份、人物、地名" aria-label="搜尋">
  </div>
  <p id="count" aria-live="polite"></p>
  <section class="grid" id="list"></section>
  <footer>資料來源：同一目錄的 <a href="THEMES.md">THEMES.md</a>、<a href="QUESTIONS.md">QUESTIONS.md</a> 與 pool.json；可搜尋全部題目見 <a href="index.html">index.html</a>。「素材估計」是研究代理估的正文分鐘數，還沒試讀；沒有估計的題是舊有完整查核的題，片長在寫企劃時決定。</footer>
</div>
<script type="application/json" id="data">${payload}</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const $=id=>document.getElementById(id);
const el=(t,c,txt)=>{const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e};
let mode='themes';
try{const m=localStorage.getItem('curio-mode');if(m==='solo'||m==='themes')mode=m}catch(e){}
const KIND={new:'新題',screened:'舊卡篩選',checked:'完整查核'};
const axesUsed=new Set([...D.themes.flatMap(t=>t.cores.map(c=>c.axis)),...D.solo.map(s=>s.axis)]);
for(const [k,v] of Object.entries(D.axes)){if(!axesUsed.has(k))continue;const o=el('option',null,k+' '+v);o.value=k;$('axis').append(o)}
const coreTotal=D.themes.reduce((n,t)=>n+t.cores.length,0);
for(const [n,l] of [[D.themes.length,'組多題題案（共 '+coreTotal+' 題）'],[D.solo.length,'題單獨成集'],[D.themes.length+D.solo.length,'集可以排']]){const s=el('div','stat');s.append(el('b',null,String(n)),el('span',null,l));$('strip').append(s)}
function setMode(m){mode=m;$('tab-themes').setAttribute('aria-selected',m==='themes');$('tab-solo').setAttribute('aria-selected',m==='solo');try{localStorage.setItem('curio-mode',m)}catch(e){}render()}
$('tab-themes').onclick=()=>setMode('themes');$('tab-solo').onclick=()=>setMode('solo');
$('axis').oninput=render;$('q').oninput=render;
function render(){
  const ax=$('axis').value,term=$('q').value.trim().toLowerCase(),list=$('list');list.replaceChildren();
  let n=0;
  if(mode==='themes'){
    for(const t of D.themes){
      if(ax&&!t.cores.some(c=>c.axis===ax))continue;
      const hay=(t.id+t.title+t.q+t.cores.map(c=>c.id+c.q).join('')).toLowerCase();
      if(term&&!hay.includes(term))continue;n++;
      const c=el('article','card');const m=el('div','meta');
      m.append(el('span','id',t.id),el('span','pill min',t.minutes+' 分鐘'),el('span','pill',t.cores.length+' 題 · '+t.chapters+' 章'));
      const ul=el('ul','cores');for(const k of t.cores){const li=el('li');li.append(el('span','id',k.id),el('span',null,k.q));ul.append(li)}
      c.append(m,el('h2',null,t.title),el('p',null,t.q),ul);list.append(c);
    }
  }else{
    for(const s of D.solo){
      if(ax&&s.axis!==ax)continue;
      if(term&&!(s.id+s.q+s.hook).toLowerCase().includes(term))continue;n++;
      const c=el('article','card');const m=el('div','meta');
      m.append(el('span','id',s.id),el('span','pill',(D.axes[s.axis]||s.axis)),el('span','pill min',s.min?('素材 '+s.min.join('–')+' 分'):'片長待企劃'),el('span','pill min',KIND[s.kind]+' · '+s.src+' 來源'));
      c.append(m,el('h2',null,s.q));if(s.hook)c.append(el('p',null,s.hook));list.append(c);
    }
  }
  $('count').textContent=(mode==='themes'?'多題一集':'單題一集')+'：顯示 '+n+' 筆';
  if(!n)list.append(el('p','empty','沒有符合條件的題目，換個關鍵字或軸看看。'));
}
setMode(mode);
</script>
</body></html>
`;
}
