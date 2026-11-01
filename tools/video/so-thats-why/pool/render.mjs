const cell = (value) => String(value ?? '').replaceAll('|', '／').replaceAll('\n', ' ');
const sourceLabel = (source, reading) => reading.origin.startsWith('legacy:') ? `${new URL(source.url).hostname}${new URL(source.url).pathname}` : reading.title;

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
  const domains = [...new Set(chosen.map((row) => row.domain))].sort();
  const lines = [`# ${chosen.length} 筆原來如此素材候選`, '', '每筆是不同核心問題的初篩候選，不等於一支長片或已審劇本。來源及適用範圍可用本機搜尋頁查看；歷史來源須刷新，新研究的推導例子仍需補直接證據。', '', '[可搜尋清單](index.html) · [來源索引](SOURCES.md) · [影片主題組合](THEMES.md) · [去重紀錄](DEDUP.md)', ''];
  for (const domain of domains) {
    const rows = chosen.filter((row) => row.domain === domain);
    lines.push(`## ${domain}（${rows.length}）`, '', '| ID | 疑問 | 要研究的機制／差別 | 段落預估（未試讀） | 來源數 |', '| --- | --- | --- | --- | --- |');
    for (const row of rows) lines.push(`| [${row.id}](index.html#${row.id}) | ${cell(row.question)} | ${cell(row.answer_target)} | ${row.editorial ? `${row.editorial.seconds.join('–')} 秒` : '待逐題評估'} | ${new Set(row.source_refs.map((ref) => ref.source_id)).size} |`);
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
  lines.push('', `其他歷史剔除、暫緩與轉系列保留在 pool.json 的 prior_decision／exclusion_reason，不因新批次出現相似標題就復活。未入本輪 ${pool.counts.selected_candidates.toLocaleString('en-US')} 筆的合格題保留候補狀態，不冒稱已採用。`);
  return `${lines.join('\n')}\n`;
}

export function validateThemes(themes, pool) {
  if (!Array.isArray(themes.episodes) || !themes.episodes.length) throw new Error('Theme list is empty');
  if (new Set(themes.episodes.map((episode) => episode.id)).size !== themes.episodes.length) throw new Error('Duplicate theme id');
  for (const episode of themes.episodes) {
    for (const key of ['id', 'title', 'core_question', 'connection', 'boredom_risk', 'drop_if', 'evidence_gaps']) if (!episode[key]) throw new Error(`${episode.id}: missing ${key}`);
    if (episode.production_ready !== false || episode.status !== 'EDITORIAL_THEME_NOT_SCRIPT') throw new Error('A theme cannot grant production approval');
    if (!Number.isFinite(episode.target_minutes) || episode.target_minutes <= 0 || !Array.isArray(episode.range_minutes) || episode.range_minutes.length !== 2 || episode.range_minutes.some((n) => !Number.isFinite(n) || n <= 0)) throw new Error(`${episode.id}: invalid duration`);
    if (!episode.candidate_ids?.length || new Set(episode.candidate_ids).size !== episode.candidate_ids.length) throw new Error('Theme needs unique candidate ids');
    if (episode.candidate_ids.some((id) => !pool.candidates.some((row) => row.id === id && row.selected))) throw new Error(`${episode.id}: theme includes an unselected or alias record`);
    const minimumChapters = episode.format === 'short_explainer' ? 2 : 4;
    if (!episode.chapters?.length || episode.chapters.length < minimumChapters || episode.chapters.some((chapter) => !chapter.title || !Number.isInteger(chapter.seconds) || chapter.seconds <= 0 || !chapter.new_information || !chapter.candidate_ids?.length || chapter.candidate_ids.some((id) => !episode.candidate_ids.includes(id)))) throw new Error(`${episode.id}: every chapter needs selected evidence and a new judgement`);
    if (Math.abs(episode.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0) - episode.target_minutes * 60) > 1e-9) throw new Error(`${episode.id}: invalid time budget`);
    if (episode.range_minutes[0] > episode.target_minutes || episode.range_minutes[1] < episode.target_minutes) throw new Error(`${episode.id}: time range does not include target`);
  }
  return themes;
}

export function renderThemes(themes, pool) {
  const lines = ['# 從素材池挑出的影片主題', '', `${themes.episodes.length} 組編輯候選；由來源、共同追問與章節推進選出，不是點閱率預測或已核准影片。時間是正文估計，尚未試讀；每章須再拆成 30–45 秒內有資訊推進的節拍。標題只是包裝提案，未查的例子不可寫成事實。`, '', '| 順序 | 主題 | 正文估計 | 素材數 |', '| --- | --- | --- | --- |'];
  for (const episode of themes.episodes) {
    const seconds = episode.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0);
    const duration = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
    const range = episode.range_minutes.map((minutes) => {
      const total = Math.round(minutes * 60);
      return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, '0')}`;
    }).join('–');
    lines.push(`| ${episode.id} | ${episode.title} | ${duration}（工作範圍 ${range}；分:秒；未試讀） | ${episode.candidate_ids.length} |`);
  }
  for (const episode of themes.episodes) {
    lines.push('', `## ${episode.id} ${episode.title}`, '', `**追問：** ${episode.core_question}`, '', `**為什麼能接成一集：** ${episode.connection}`, '', '| 段落 | 秒數預算 | 新增理解 | 使用素材 |', '| --- | --- | --- | --- |');
    for (const chapter of episode.chapters) lines.push(`| ${chapter.title} | ${chapter.seconds} | ${chapter.new_information} | ${chapter.candidate_ids.join('、')} |`);
    for (const variantId of episode.variant_budget_ids ?? []) {
      const variant = pool.raw_records.find((row) => row.id === variantId);
      if (variant) lines.push('', `本片採用合併案例 **${variantId} ${variant.question}**（核心 ${pool.dedup.aliases[variantId]}）；使用此案例已審的段落預算，不另計素材或加上原情境的秒數。`);
    }
    lines.push('', '**素材與來源：**', '');
    for (const id of episode.candidate_ids) {
      const row = pool.candidates.find((candidate) => candidate.id === id);
      const ids = [...new Set(row.source_refs.map((ref) => ref.source_id))];
      lines.push(`- ${id} ${row.question} — ${ids.slice(0, 3).map((sourceId) => { const source = pool.sources.find((item) => item.id === sourceId); return `[${new URL(source.url).hostname}](${source.url})`; }).join('、')}。${row.notes}`);
    }
    lines.push('', `**可能無聊的地方：** ${episode.boredom_risk}`, '', `**先刪／撤題條件：** ${episode.drop_if}`, '', `**待補證據：** ${episode.evidence_gaps}`);
  }
  return `${lines.join('\n')}\n`;
}

export function renderHtml(pool, themes) {
  const sourceIds = new Set(pool.candidates.filter((row) => row.selected).flatMap((row) => row.source_refs.map((ref) => ref.source_id)));
  const payload = JSON.stringify({ candidates: pool.candidates.filter((row) => row.selected), sources: pool.sources.filter((source) => sourceIds.has(source.id)), themes: themes.episodes }).replaceAll('<', '\\u003c');
  return `<!doctype html>
<html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>原來如此素材池</title>
<style>body{margin:0;background:#faf6ea;color:#142c42;font:16px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:32px 22px}h1{font-size:32px;margin-bottom:8px}h2{font-size:21px}p{max-width:900px}.eyebrow{color:#8b4a1b;font-weight:700}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.stat{background:#fff;border:1px solid #d4c9ae;padding:14px 22px;border-radius:12px}.stat b{font-size:27px;display:block}.controls{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#faf6eaf5;padding:12px 0}input,select,button{font:inherit;padding:10px 12px;border-radius:8px;border:1px solid #9ca8ad}input{flex:1;min-width:240px}button{cursor:pointer;background:#142c42;color:white}a{color:#155f88}article{background:#fff;border:1px solid #d7d0bd;border-radius:12px;padding:18px 22px;margin:14px 0}summary{cursor:pointer;font-weight:700}small,.muted{color:#526777}.tag{font-size:13px;padding:3px 8px;background:#f1e3b6;border-radius:5px}.detail{border-top:1px solid #e9e4d8;padding-top:12px;margin-top:12px}.sources li{margin:6px 0}.warning{border-left:4px solid #c48a20;padding-left:12px}#count{font-weight:600}@media(max-width:600px){h1{font-size:26px}main{padding:22px 14px}.controls{position:static}input{min-width:0;width:100%;box-sizing:border-box}select{max-width:100%}}</style>
<main><div class="eyebrow">原來如此事務所 · 2026-11-01</div><h1>${pool.counts.selected_candidates.toLocaleString('en-US')} 個疑問，先找值得追的故事</h1><p>搜尋生活物件、現象或機制。每筆保留來源、小節與適用範圍，再選能推進同一問題的素材組成影片。</p><p class="warning">這是初篩素材池。題級來源閱讀不等於完整答案已查核；生活例證、逐字稿和實際片長仍要驗證。</p>
<div class="stats"><div class="stat"><b>${pool.counts.selected_candidates}</b>入選素材</div><div class="stat"><b>${sourceIds.size}</b>使用來源頁（含歷史）</div><div class="stat"><b>${themes.episodes.length}</b>影片主題候選</div><div class="stat"><b>${pool.counts.alias_records}</b>合併的別名紀錄</div></div>
<p><a href="THEMES.md">查看影片章節與片長</a> · <a href="SOURCES.md">完整來源索引</a> · <a href="DEDUP.md">去重紀錄</a> · <a href="README.md">這批怎麼建立</a></p>
<label for="q">找素材</label><div class="controls"><input id="q" type="search" placeholder="例如：冰、葉子、聲音、密碼" aria-label="搜尋素材"><select id="domain" aria-label="分類"><option value="">全部分類</option></select><select id="theme" aria-label="影片主題"><option value="">全部素材</option></select></div><p id="count" aria-live="polite"></p><section id="results"></section><button id="more">再顯示 50 筆</button></main>
<script type="application/json" id="data">${payload}</script>
<script>
const data=JSON.parse(document.getElementById('data').textContent),sources=new Map(data.sources.map(x=>[x.id,x]));
const q=document.getElementById('q'),domain=document.getElementById('domain'),theme=document.getElementById('theme'),results=document.getElementById('results'),more=document.getElementById('more');let limit=50;
for(const d of [...new Set(data.candidates.map(x=>x.domain))].sort()){const o=document.createElement('option');o.value=d;o.textContent=d;domain.append(o)}
for(const t of data.themes){const o=document.createElement('option');o.value=t.id;o.textContent=t.id+' '+t.title;theme.append(o)}
function el(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e}
function render(){const term=q.value.trim().toLocaleLowerCase();const t=data.themes.find(x=>x.id===theme.value);const rows=data.candidates.filter(x=>(!domain.value||x.domain===domain.value)&&(!t||t.candidate_ids.includes(x.id))&&(!term||(x.id+' '+x.question+' '+x.answer_target+' '+x.scope+' '+JSON.stringify(x.question_variants||[])).toLocaleLowerCase().includes(term)));results.replaceChildren();document.getElementById('count').textContent='找到 '+rows.length+' 筆 · 顯示 '+Math.min(rows.length,limit)+' 筆';for(const row of rows.slice(0,limit)){const card=el('article','');card.append(el('span',row.id+' · '+row.domain,'tag'),el('h2',row.question),el('p','要研究：'+row.answer_target));if(row.editorial)card.append(el('p','段落預估：'+row.editorial.seconds.join('–')+' 秒（未試讀；不是整片長度）','muted'));const detail=el('details','');detail.append(el('summary','呈現方式、來源與待查事項'));const body=el('div','','detail');body.append(el('p','範圍：'+row.scope),el('p',row.notes,'muted'));if(row.editorial)body.append(el('p','新增理解：'+row.editorial.payoff),el('p','畫面構想：'+row.editorial.visual));for(const variant of row.question_variants||[])body.append(el('p','合併原題 '+variant.id+'：'+variant.question,'muted'));const ul=el('ul','','sources');for(const id of [...new Set(row.source_refs.map(x=>x.source_id))]){const s=sources.get(id);const refs=row.source_refs.filter(x=>x.source_id===id);const readings=s.readings.filter(x=>refs.some(r=>r.origin===x.origin));const reading=readings[0]||s.readings[0];const li=el('li','');const a=el('a',reading.origin.startsWith('legacy:')?new URL(s.url).hostname+new URL(s.url).pathname:reading.title);a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';li.append(a,el('small',' — '+reading.publisher+' · '+(reading.accessed_on||'歷史引用，當期未讀外站')));for(const ref of refs)li.append(el('div','本題定位：'+ref.locator,'muted'));for(const item of readings)li.append(el('div',item.origin+' · '+item.reading_scope+' · '+(item.accessed_on||'當期未讀外站'),'muted'));ul.append(li)}body.append(ul);detail.append(body);card.append(detail);results.append(card)}more.hidden=rows.length<=limit}
for(const control of [q,domain,theme])control.addEventListener('input',()=>{limit=50;render()});more.addEventListener('click',()=>{limit+=50;render()});if(location.hash){try{q.value=decodeURIComponent(location.hash.slice(1))}catch{q.value=''}}render();
</script></html>\n`;
}
