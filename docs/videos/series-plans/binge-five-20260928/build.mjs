import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

export const ROOT = path.dirname(fileURLToPath(import.meta.url));
export const SLUGS = ['wedding-reckoning', 'seventh-passenger', 'scapegoat-empress', 'city-owes-a-light', 'remembered-by-rival'];
export const COMMON = { total_minutes: 120, target_minutes: 3, planned_episodes: 40, episodes_per_chapter: 10, compilation: true, open_ended: false, visual_tier: 'hybrid', style_preset: 'cinematic-3d', aspects: ['world', 'bonds', 'structure', 'mood'], hands_off: false };
export const hash = (value) => createHash('sha256').update(typeof value === 'string' ? value : JSON.stringify(value)).digest('hex');
const lines = (items) => items.map((x) => `- ${x}`).join('\n');
const cell = (value) => String(value ?? '').replaceAll('|', '／').replaceAll('\n', '<br>');
const table = (heads, rows) => `| ${heads.join(' | ')} |\n| ${heads.map(() => '---').join(' | ')} |\n${rows.map(row => `| ${row.map(cell).join(' | ')} |`).join('\n')}`;
const csv = (v) => `"${String(v ?? '').replaceAll('"', '""')}"`;
const json = (v) => JSON.stringify(v, null, 2) + '\n';
const worldRows = (world) => Object.entries(world).flatMap(([key, value]) => {
  if (typeof value === 'string') return [[key, value]];
  if (key === 'narrator' && value && typeof value === 'object') {
    return [['旁白聲音提案', [value.provider, value.name, value.style].filter(Boolean).join(' / ')]];
  }
  return [];
});

export async function loadSource(slug) {
  if (!SLUGS.includes(slug)) throw new Error(`Unknown series: ${slug}`);
  return (await import(new URL(`./${slug}/source.mjs`, import.meta.url))).default;
}

export function compile(source) {
  const series = { ...source.series, ...COMMON };
  const chapters = source.chapters;
  const episodes = chapters.flatMap(c => c.episodes);
  const settingBody = { ...source.setting, title: series.title, tone: series.tone,
    mysteries: source.setting.mysteries.map(m => ({ ...m, planted_chapter: Math.ceil(m.planted / 10), reveal_chapter: Math.ceil(m.revealed / 10) })) };
  const settingMd = `# ${series.title}｜設定集\n\n> 本機製作企劃；聲音為擬定 casting，未試聽。故事與外觀為原創草案，未生成任何圖片或影片。\n\n## 世界觀\n\n${table(['項目','內容'], worldRows(settingBody.world))}\n\n${table(['勢力','想要什麼','隱瞞什麼'], settingBody.world.factions.map(f => [f.name,f.want,f.secret]))}\n\n## 規則與代價\n\n${lines(settingBody.rules)}\n\n## 人物\n\n${settingBody.characters.map(c => `### ${c.name}（${c.id}）\n\n${table(['項目','設定'], [['身分',c.role],['年齡',c.age],['性格',c.personality],['欲望',c.want],['恐懼',c.fear],['秘密',c.secret],['說話習慣',c.speech],['聲音提案',`${c.voice.provider} / ${c.voice.name} / ${c.voice.style}`],['外觀提示詞（跨集逐字沿用）',c.appearance]])}\n\n${table(['對象','關係'],c.relationships.map(r=>[r.with,r.kind]))}`).join('\n\n')}\n\n## 場景\n\n${table(['ID','場景','固定辨識'],settingBody.locations.map(l=>[l.id,l.name,l.description]))}\n\n## 長線謎團\n\n${table(['ID','問題','確定答案','埋下','推進','揭曉'],settingBody.mysteries.map(m=>[m.id,m.question,m.answer,m.planted,m.advanced.join('、'),m.revealed]))}\n\n## 語氣與畫面\n\n${source.packaging.visual_identity}\n\n${source.packaging.music}\n\n## 開場三十秒\n\n${table(['規劃秒段','畫面','聲音'],settingBody.opening_30_seconds.map(b=>[b.seconds,b.picture,b.audio]))}\n\n## 命名規則\n\n${lines(settingBody.naming)}\n\n## 不做的事\n\n${lines(settingBody.never)}\n\n## 發音表\n\n${table(['詞','擬定讀音'],Object.entries(settingBody.lexicon))}\n\n## 確定結局\n\n${settingBody.ending}\n`;
  const schedule = settingBody.mysteries.map(m=>({mystery:m.id,planted:m.planted,advanced:m.advanced,revealed:m.revealed}));
  const outlineBody = { chapters: chapters.map(c => ({ ...c, episodes: c.episodes.map(e => ({ number:e.number,title:e.title,logline:e.logline,timeline:e.timeline })) })), tension_map: chapters.map(c=>({chapter:c.number,stakes:c.stakes,question:c.question,turn:c.turn})), reveal_schedule:schedule };
  const outlineMd = `# ${series.title}｜四篇四十集總綱\n\n${series.premise}\n\n每集目標三分鐘，以下時間為規劃，不是實際配音或成片時間。\n\n## 全季張力地圖\n\n${table(['篇','時間','賭注','核心問題','篇末翻轉'],chapters.map(c=>[c.number,`${(c.number-1)*30}–${c.number*30} 分`,c.stakes,c.question,c.turn]))}\n\n${chapters.map(c=>`## 第 ${c.number} 篇：${c.title}\n\n${c.theme}\n\n起點：${c.start_state}\n\n終點：${c.end_state}\n\n${table(['集','標題','推進與新問題'],c.episodes.map(e=>[String(e.number).padStart(2,'0'),e.title,e.logline]))}`).join('\n\n')}\n\n## 謎團排程\n\n${table(['ID','埋下','推進','揭曉'],schedule.map(m=>[m.mystery,m.planted,m.advanced.join('、'),m.revealed]))}\n`;
  const files = {'series-request.json':json(series),'setting.md':settingMd,'setting.json':json({body_md:settingMd,body_json:settingBody}),'outline.md':outlineMd,'outline.json':json({body_md:outlineMd,body_json:outlineBody})};
  for (const c of chapters) {
    const md = `# ${series.title}｜第 ${c.number} 篇：${c.title}\n\n${c.theme}\n\n規劃長度 ${(c.number-1)*30}–${c.number*30} 分鐘；所有秒數待劇本、TTS 與成片重新量測。\n\n${c.episodes.map(e=>`## 第 ${String(e.number).padStart(2,'0')} 集：${e.title}\n\n${e.logline}\n\n${table(['節拍','內容'],[['開場鉤子',`${e.hook_type}｜${e.hook}`],['主要衝突',e.conflict],['中段轉折',e.turn],[e.closed_ending?'已閉合的情感收尾':'接續收尾',`${e.cliffhanger.type}｜${e.cliffhanger.text}`],['主角走向',e.lead_arc],['張力曲線',e.tension.join(' → ')],['出場角色',e.characters.join('、')],['主要場景',e.locations.join('、')],['主題句',e.theme],['埋下伏筆',e.setups.join('、')||'無新增'],['局部／完整回收',e.payoffs.join('、')||'本集推進，依總綱排程回收']])}\n\n${table(['回報','規劃位置','具體演出'],e.satisfaction.map(b=>[b.type,`${b.beat}／${b.planned_seconds} 秒`,b.text]))}\n\n${table(['連貫性','本集結束狀態'],Object.entries(e.state))}`).join('\n\n')}\n`;
    const stem=`chapter-${String(c.number).padStart(2,'0')}`;
    files[`${stem}.md`]=md;
    files[`${stem}.json`]=json({body_md:md,body_json:{chapter:c.number,episodes:c.episodes}});
  }
  const continuityRows=episodes.map(e=>[e.number,e.state.time,e.state.knowledge,e.state.character_state,e.state.evidence,e.state.carry_forward]);
  const continuityHeads=['集','故事時間','情報分布','人物與關係','證據／道具','下集承接'];
  files['continuity.md']=`# ${series.title}｜連貫性表\n\n${lines(source.continuity_notes)}\n\n${table(continuityHeads,continuityRows)}\n`;
  // Match the repository's LF policy so a Git checkout preserves manifest hashes.
  files['continuity.csv']='\uFEFF'+[continuityHeads,...continuityRows].map(r=>r.map(csv).join(',')).join('\n')+'\n';
  const pack={...source.packaging,status:'planning-only',category_id:'24',default_language:'zh-TW',caption_languages:['zh-TW','en','ja','ko','zh-CN'],caption_status:'not-produced',thumbnail_status:'composition-only',timing_status:'planned-not-measured',chapter_titles:episodes.map(e=>({episode:e.number,title:e.title})),compilation:{chapter_cards:false,outro:false},made_for_kids:false,disclosure:{synthetic_content:true,paid_promotion:'owner-to-confirm-at-upload'},publish_state:'not-uploaded'};
  files['packaging.json']=json(pack);
  files['packaging.md']=`# ${series.title}｜標題、縮圖與上架資料\n\n> 文案及構圖規格已備齊；縮圖圖片、五語字幕、章節時間碼、影片與正式上傳包尚未製作。\n\n## 觀眾與視覺\n\n${pack.audience}\n\n${pack.visual_identity}\n\n${pack.music}\n\n## 三組標題與縮圖\n\n${pack.thumbnail_variants.map((v,i)=>`### ${v.id}：${pack.titles[i]}\n\n- 圖上文字：${v.headline}\n- 構圖：${v.composition}\n- 素材出處：第 ${v.episode} 集，${v.scene}\n- 必須兌現：${v.promise}`).join('\n\n')}\n\n## 說明欄本文\n\n${pack.description}\n\n## 標籤\n\n${pack.tags.join('、')}\n\n## 置頂留言草稿\n\n${pack.pinned_comment}\n\n## 合集交接\n\n- 製作順序第 ${pack.release_order} 位。\n- 關閉逐集章節卡與片尾卡：在合集 video.json 的 compilation 設 chapter_cards=false、outro=false；這不是 SeriesIn 的欄位。\n- 保留 YouTube 章節，使用實際 compile/timeline.json 時間，不使用三分鐘乘集數假造時間碼。\n- 開場與逐集銜接不重述前情。最後一集關閉主線，用情感翻轉收尾。\n- 影片分類娛樂（24）；一般成人故事非兒童向。最終合成內容、兒童設定與付費宣傳依實際成片由站主確認。\n- 先製作繁中配音，五語 CC 為 zh-TW/en/ja/ko/zh-CN；本包不冒充已有 SRT。\n- 正式標題、說明及四語翻譯、字幕雜湊、縮圖 JPEG、UPLOAD.md 由完成的媒體產線另行產出。\n`;
  files['README.md']=`# ${series.title}\n\n${series.premise}\n\n狀態：**製作企劃**。目標 120 分鐘、四篇四十集；沒有建立後台作品、啟動媒體生成或上架。\n\n- [設定集](setting.md)：世界規則、人物聲音與外觀、開場、伏筆、確定結局。\n- [40 集總綱](outline.md)。\n- [第 1 篇細綱](chapter-01.md) · [第 2 篇](chapter-02.md) · [第 3 篇](chapter-03.md) · [第 4 篇](chapter-04.md)。\n- [連貫性表](continuity.md) · [CSV](continuity.csv)。\n- [標題縮圖與上架資料](packaging.md)。\n- [後台建立資料](series-request.json)：僅資料，不可批量提交；建立本身可能排入工人。\n\nJSON 文件保留既有產線的 body_md/body_json 形狀，仍須走伺服器裁決與雜湊核准。沒有把本機編輯審查偽裝成正式站核准。\n`;
  files['documents.json']=json({slug:series.slug,status:'prepared-not-submitted',documents:[{kind:'setting',chapter_number:0,...JSON.parse(files['setting.json'])},{kind:'outline',chapter_number:0,...JSON.parse(files['outline.json'])},...chapters.map(c=>({kind:'chapter',chapter_number:c.number,...JSON.parse(files[`chapter-${String(c.number).padStart(2,'0')}.json`])}))]});
  files['manifest.json']=json({schema_version:1,slug:series.slug,title:series.title,source_sha256:hash(source),stage:'production-plan',episode_count:episodes.length,chapter_count:chapters.length,media_generated:false,admin_series_created:false,published:false,files:Object.fromEntries(Object.entries(files).map(([name,data])=>[name,hash(data)]))});
  return files;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const slugs=process.argv.slice(2);
  for(const slug of slugs.length?slugs:SLUGS){
    const files=compile(await loadSource(slug));
    for(const [name,body] of Object.entries(files)) await fs.writeFile(path.join(ROOT,slug,name),body,'utf8');
    process.stdout.write(`${slug}: ${Object.keys(files).length} files built\n`);
  }
}
