import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { ROOT, DIRECTORY, readCatalog, select, sourceMaterial } from './catalog.mjs';
import { plans, outside } from './episode-plan.mjs';

const hash = (value) => createHash('sha256').update(value).digest('hex');
export const TIERS = { pilot: '優先試做', next: '第二梯候選', conditional: '先過內容關卡' };
export const DISPOSITIONS = { episode: '組成影片', shorts: '改短片', reserve: '補強後重評', hold: '暫緩' };
const definition = 'tools/video/so-thats-why/episode-plan.mjs';
const read = (root, name) => readFileSync(path.join(root, DIRECTORY, name), 'utf8');

export function buildProgram(catalog, root = ROOT, input = { plans, outside }) {
  const active = catalog.episodes.filter((entry) => entry.active);
  const used = new Set();
  const planIds = new Set();
  for (const plan of input.plans) {
    if (!/^P\d{2,}$/.test(plan.id) || planIds.has(plan.id)) throw new Error('Duplicate or invalid episode id');
    planIds.add(plan.id);
    if (!Object.hasOwn(TIERS, plan.tier) || !plan.topics.length || !plan.question || !plan.join || !plan.cut || !plan.risk || !plan.evidence || !plan.visual) throw new Error(`${plan.id}: missing editorial decision`);
    if (plan.production_ready !== false || plan.status !== 'EPISODE_PLAN_NOT_SCRIPT') throw new Error(`${plan.id}: plan cannot grant production approval`);
    if (plan.chapters.length < 5 || plan.chapters.some((chapter) => !chapter.title || !chapter.new_information || !Number.isInteger(chapter.seconds) || chapter.seconds <= 0)) throw new Error(`${plan.id}: incomplete chapters`);
    const total = plan.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0);
    if (total !== plan.target_body_seconds || total < 480 || plan.planning_range_seconds.length !== 2 || plan.planning_range_seconds[0] > total || plan.planning_range_seconds[1] < total) throw new Error(`${plan.id}: duration budget mismatch`);
    for (const id of plan.topics) {
      if (used.has(id) || !active.some((entry) => entry.id === id)) throw new Error(`${id}: duplicate or excluded material`);
      used.add(id);
    }
  }
  for (const decision of input.outside) {
    if (used.has(decision.id) || !active.some((entry) => entry.id === decision.id) || !['shorts', 'reserve', 'hold'].includes(decision.disposition) || !decision.reason) throw new Error(`${decision.id}: invalid outside decision`);
    used.add(decision.id);
  }
  if (used.size !== active.length) throw new Error('Every first-pass active topic needs exactly one duration decision');
  const dispositions = active.map((entry) => {
    const plan = input.plans.find((candidate) => candidate.topics.includes(entry.id));
    return plan ? { id: entry.id, disposition: 'episode', episode_id: plan.id, reason: plan.join } : input.outside.find((decision) => decision.id === entry.id);
  });
  return {
    schema_version: 1, edited_on: '2026-11-01', status: 'EDITORIAL_EPISODE_PLANS_NOT_PRODUCTION',
    duration_basis: 'BODY_PLANNING_ESTIMATE_NOT_MEASURED_AUDIO', production_synced: false,
    source_catalog_sha256: hash(JSON.stringify(catalog)),
    definition: { file: definition, sha256: hash(readFileSync(path.join(root, definition))) },
    counts: {
      source_pool: active.length, episodes: input.plans.length,
      combined_episodes: input.plans.filter((plan) => plan.topics.length > 1).length,
      ...Object.fromEntries(Object.keys(DISPOSITIONS).map((key) => [key, dispositions.filter((entry) => entry.disposition === key).length])),
    },
    plans: input.plans, dispositions,
  };
}

export function readProgram(root = ROOT) {
  const catalog = readCatalog(root);
  const program = JSON.parse(read(root, 'episodes.json'));
  if (JSON.stringify(program) !== JSON.stringify(buildProgram(catalog, root))) throw new Error('Episode plan drift: review definitions and rebuild');
  if (read(root, 'EPISODES.md') !== renderProgram(program)) throw new Error('Episode document drift: rebuild after review');
  if (read(root, 'DURATION-AUDIT.md') !== renderDurationAudit(program, catalog)) throw new Error('Duration audit drift: rebuild after review');
  return { catalog, program };
}

export function episodeBrief(catalog, program, id, root = ROOT) {
  let plan = program.plans.find((entry) => entry.id === id);
  if (!plan) {
    select(catalog, id, { activeOnly: true });
    const decision = program.dispositions.find((entry) => entry.id === id);
    if (decision?.disposition !== 'episode') throw new Error(`${id} excluded by duration review: ${decision?.reason}`);
    plan = program.plans.find((entry) => entry.id === decision.episode_id);
  }
  return {
    status: 'EDITORIAL_BRIEF_NOT_IMPORT_READY', id: plan.id, requested_id: id,
    title: `${plan.title}｜原來如此事務所`, plan,
    current_profile: {
      ...catalog.profile, target_minutes: plan.minutes, body_budget_seconds: plan.target_body_seconds,
      estimated_spoken_characters: plan.estimated_spoken_characters, minimum_loops: plan.minimum_loops,
    },
    needs: ['依各章補逐段 treatment、轉折與伏筆回收，再試讀刪除重複內容', '逐主張重新查核、獨立聽眾審稿與實際旁白計時', '核對既有影片／製作狀態，新增版本重新綁定來源與核准', '依實際片長報整集費用並完成媒體驗收'],
    source_materials: plan.topics.map((topic) => sourceMaterial(catalog, topic, root)),
    notes: '片長是正文估計，片頭片尾另計；不是已量測的成片。初篩題號會導向整個單集，不再輸出固定 13 分鐘的孤立小題。',
  };
}

const time = (seconds) => `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
export function renderProgram(program) {
  const lines = [
    '# 30 支影片候選：先看故事厚度，再決定片長', '',
    '2026-11-01 第二輪。由 100 題初篩素材選出 44 題，組成 30 支候選（10 支合題、20 支獨立主題）。其餘 25 題改短片、26 題補強後重評、5 題暫緩；逐題見 [片長再篩表](DURATION-AUDIT.md)。數量是這輪取捨結果，不是固定配額。', '',
    'P01–P30 是企劃 ID，不是已建立的影片 slug。先做 P01–P06 的 treatment 與無付費試讀，再決定製作；不是一次買六集媒體。條件組須先解決各自的證據與主線問題。所有時間都是 **正文編輯估計**，尚無完整逐字稿、旁白或觀眾留存實測；片頭片尾會使成片略長。', '',
    '目前每支只有四個主節拍，尚未建立逐段資訊與 45 秒鉤子時間線；章節秒數不是已可講滿的證據。段落預算是初估，不是要把短答案拖滿。每章仍須拆成 30–45 秒內有新資訊的節拍；表中的大章不能整段只有一個鉤子。任何無新增因果、證據、反例或判斷的段落先刪。刪完未達 8 分鐘退出長片，夠好但短就接受較短形式，不補慢語速、空鏡或百科。', '',
    '下列機制與畫面是待查核的寫作安排，來源入口在題庫與逐集 brief；不是本輪完成的 30 集科學／醫學／工程事實核准。', '',
    '| 企劃 | 題目 | 合入素材 | 正文目標／範圍 | 梯次 |', '| --- | --- | --- | --- | --- |',
  ];
  for (const p of program.plans) lines.push(`| [${p.id}](#${p.id.toLowerCase()}) | ${p.title} | ${p.topics.join('＋')} | ${p.minutes} 分／${p.range.join('–')} 分 | ${TIERS[p.tier]} |`);
  for (const p of program.plans) {
    lines.push('', `<a id="${p.id.toLowerCase()}"></a>`, `## ${p.id} ${p.title}`, '',
      `**觀眾一路追問：** ${p.question}`, '',
      `**如何組成一集：** ${p.join}`, '',
      `**來源素材：** ${p.topics.join('、')}。**正文目標：** ${p.minutes} 分（估計範圍 ${p.range.join('–')} 分）；口語稿粗估 ${p.estimated_spoken_characters.join('–')} 字，試讀優先於字數；至少 ${p.minimum_loops} 個伏筆回收。`, '',
      '| 正文段落 | 預算 | 這一段增加什麼 |', '| --- | --- | --- |');
    let cursor = 0;
    for (const chapter of p.chapters) {
      lines.push(`| ${time(cursor)}–${time(cursor + chapter.seconds)} ${chapter.title} | ${chapter.seconds} 秒 | ${chapter.new_information} |`);
      cursor += chapter.seconds;
    }
    lines.push('', `**畫面／驗證方式：** ${p.visual}`, '', `**無聊風險：** ${p.risk}`, '', `**刪減或撤題條件：** ${p.cut}`, '', `**待補／待重新查核的證據：** ${p.evidence}`);
  }
  return `${lines.join('\n')}\n`;
}

export function renderDurationAudit(program, catalog) {
  const lines = ['# 100 題素材的片長再篩', '', '本表覆蓋第一輪留下的 100 題，每題只指定一次去向；其他 213 列維持 [第一輪處置](AUDIT.md)。補強後重評不進長片選單，短片也還要重新收斂到一個可獨立說清的小問題，並未產生 Shorts。歷史原稿、媒體與核准不變。', '', '| 題號 | 原素材題名 | 本輪決定 | 企劃／理由 |', '| --- | --- | --- | --- |'];
  for (const decision of program.dispositions) {
    const entry = select(catalog, decision.id);
    lines.push(`| ${entry.id} | ${entry.title} | ${DISPOSITIONS[decision.disposition]} | ${decision.episode_id ? `[${decision.episode_id}](EPISODES.md#${decision.episode_id.toLowerCase()})：` : ''}${decision.reason} |`);
  }
  return `${lines.join('\n')}\n`;
}
