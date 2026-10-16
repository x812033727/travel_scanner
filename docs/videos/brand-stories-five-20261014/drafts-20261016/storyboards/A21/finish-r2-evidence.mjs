import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url)),p=path.join(dir,'run-offline-checks.mjs');
let s=fs.readFileSync(p,'utf8');
for(const [before,after]of [
 ['all_47_paragraphs_verbatim:true,narration_changes:0','all_47_active_paragraphs_verbatim:true,original_46_other_paragraphs_unchanged:true,original_ids_and_order_preserved:true,v1_preparation_files_preserved:true,narration_changes:1,changed_paragraph:"T06",claim_review_status:"AUTHOR_CLARIFICATION_PENDING_INDEPENDENT_RECHECK"'],
 ['47 段、2,281 字；逐段 ID／順序／UTF-16 偏移完整重建，無改字。','原稿 47 段、2,281 字；active 候選 47 段、2,283 字。只改 T06 主詞；其餘 46 段、所有 ID／順序不變。active 原段與 UTF-16 偏移完整重建。'],
 ['547.44–595.04 秒（9:07–9:55）','547.92–595.57 秒（9:08–9:56）'],
 ['573.44–621.04 秒（9:33–10:21）','573.92–621.57 秒（9:34–10:22）'],
 ['## 重跑\\n\\n在 repo 根目錄','## 唯一原文改動\\n\\nT06：\\n\\n> 這回，稅務機關要說服上訴法院，高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。\\n\\nC22 仍綁原 2009 判決（active source index 3）；此改寫由作者澄清主詞，獨立覆核待 root。完整前後字串／hash、v1 保全及分鏡 delta 見 revision-manifest.json 和 adaptation-manifest.json。S064 的示意律師改為中性法律讀者比較卷宗；同鏡不把兩方論點歸給一人。原稿、v1 分鏡與既有獨立 review 均未改。\\n\\n## 重跑\\n\\n在 repo 根目錄']
]){assert.ok(s.includes(before),before);s=s.replace(before,after);}
const before="write('offline-verification.json',result);";
const after=`write('offline-verification.json',result);
const v1=JSON.parse(fs.readFileSync(path.join(v1dir,'storyboard.json'),'utf8'));
const contentKeys=['text','narration_refs','units','estimated_spoken_seconds','prompt','visual_function'];
const shotDeltas=board.shots.flatMap((a,i)=>{const b=v1.shots[i],keys=contentKeys.filter(k=>JSON.stringify(a[k])!==JSON.stringify(b[k]));return keys.length?[{shot_id:a.id,changes:Object.fromEntries(keys.map(k=>[k,{before:b[k],after:a[k]}]))}]:[];});
assert.deepEqual(shotDeltas.map(d=>d.shot_id),['A21-S064','A21-S065']);
const adapted=read('adaptation-manifest.json');Object.assign(adapted,{original_paragraphs:47,active_paragraphs:47,original_units:2281,active_units:2283,independent_recheck:'PENDING_ROOT',changed_cids:['C22'],original_v3_and_v1_preserved:true});write('adaptation-manifest.json',adapted);
const revision={schema_version:1,status:'AUTHOR_REVISION_PENDING_INDEPENDENT_RECHECK',revision:'r2',basis:'Root full-read detected subject ambiguity in T05→T06; exact T06 clarification only.',original_fullscript_sha256:board.original_fullscript_sha256,before_storyboard_sha256:hash(fs.readFileSync(path.join(v1dir,'storyboard.json'))),after_storyboard_sha256:hash(fs.readFileSync(path.join(dir,'storyboard.json'))),before_active_narration_sha256:v1.active_narration_sha256,after_active_narration_sha256:board.active_narration_sha256,paragraph_delta:adaptation,unchanged_paragraphs:original.filter(p=>p.id!=='T06').map(p=>p.id),unchanged_ids_and_order:true,all_active_paragraphs_reconstructed:true,v1_files_preserved:v1hashes.files,source_pins_unchanged:board.source_pins,claim_delta:{id:'C22',active_worker_source_indices_zero_based:[3],source_facts_unchanged:true,review_status:'AUTHOR_CLARIFICATION_PENDING_INDEPENDENT_RECHECK'},shot_deltas:shotDeltas,timing_delta_note:'Only 2 extra nonpunctuation UTF-16 units in S064; later estimated start/end timestamps shift by 0.48–0.53 seconds through rounding. No extra pauses.',before_metrics:v1.metrics,after_metrics:board.metrics};write('revision-manifest.json',revision);`;
assert.ok(s.includes(before));s=s.replace(before,after);fs.writeFileSync(p,s);
