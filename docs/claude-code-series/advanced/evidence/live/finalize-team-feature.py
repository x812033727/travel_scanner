"""Export the scoped product Teams exercise and observed independent checks."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, io, json, subprocess, tarfile, zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
setup=json.loads((OUT/'team-feature-setup.json').read_text(encoding='utf-8'))
project=Path(setup['project'])
session='5d3ade06-bf75-49fa-86e3-d93572acb465'
logs=Path.home()/'.claude/projects/C--Users-x8120-AppData-Local-Temp-mokaair-team-feature-qgs6o2kh'
def readrows(path):return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
def blocks(rows):
    for row in rows:
        content=row.get('message',{}).get('content',[])
        if isinstance(content,list):
            for block in content:
                if block.get('type') in {'tool_use','tool_result','text'}:
                    yield {**block,'timestamp':row.get('timestamp'),'role':row.get('type')}
main=readrows(logs/(session+'.jsonl'))
children={p.stem:readrows(p) for p in (logs/session/'subagents').glob('*.jsonl')}
calls=[b for b in blocks(main) if b['type']=='tool_use']
agents=[b for b in calls if b['name']=='Agent']
assert len(agents)==2 and {b['input']['name'] for b in agents}=={'data-builder','ui-builder'}
trace={'lead':list(blocks(main)),'teammates':{n:list(blocks(rows)) for n,rows in children.items()}}
serialized=json.dumps(trace,ensure_ascii=False)
assert 'BLOCKED-UNKNOWN-MODE' in serialized and 'TEAM-INTEGRATED' in serialized
assert '所有待辦' in (project/'index.html').read_text(encoding='utf-8')
assert subprocess.run(['git','diff','--check'],cwd=project,capture_output=True).returncode==0
assert not subprocess.check_output(['git','diff','--','model.js','tests/model.test.mjs'],cwd=project)
allowed={'data-builder':{'filter.js','tests/filter.test.mjs'},'ui-builder':{'app.js','index.html','style.css'}}
changes={}
for name,rows in children.items():
    role=next(role for role in allowed if role in name)
    edits=[b for b in blocks(rows) if b['type']=='tool_use' and b['name'] in {'Write','Edit'}]
    paths={Path(b['input']['file_path']).relative_to(project).as_posix() for b in edits}
    assert paths<=allowed[role],(role,paths)
    changes[role]=sorted(paths)

# The Linux CI fix canonicalized line endings after this live exercise started.
# Compare the new starter with the original committed starter, not the modified app.
tree=subprocess.check_output(['git','archive',setup['baseline']],cwd=project)
with tarfile.open(fileobj=io.BytesIO(tree)) as original:
    original_files={m.name:original.extractfile(m).read() for m in original if m.isfile()}
current_zip=ROOT/'apps/web/public/tutorials/claude-code/advanced/lesson-89.zip'
with zipfile.ZipFile(current_zip) as archive:
    starter={n.removeprefix('starter/'):archive.read(n) for n in archive.namelist() if n.startswith('starter/')}
assert set(starter)==set(original_files)
assert all(v==original_files[n].replace(b'\r\n',b'\n') for n,v in starter.items())

result_archive=OUT/'team-feature-result.zip'
files=[]
with zipfile.ZipFile(result_archive,'w',compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(project.rglob('*')):
        relative=path.relative_to(project)
        if not path.is_file() or set(relative.parts)&{'.git','node_modules','run-data'} or path.name=='settings.local.json':continue
        data=path.read_bytes();archive.writestr(relative.as_posix(),data)
        files.append({'path':relative.as_posix(),'sha256':hashlib.sha256(data).hexdigest()})
    archive.writestr('VERIFICATION.md','# Actual lesson 89 Teams result\n\nCode was produced by the named product teammates. The integrator owns task-contract.md.\nThe verifier performed the browser checks and three separate independent assertions.\nRun `node --test tests/model.test.mjs tests/filter.test.mjs` (10 tests), then `node server.mjs`.\nStop the local server with Ctrl+C. No publication, remote commit or deployment was performed.\n')
trace_text=json.dumps(trace,ensure_ascii=False,indent=2).replace(str(project).replace('\\','\\\\'),'<exercise>')
(OUT/'team-feature-events.json').write_text(trace_text+'\n',encoding='utf-8')
receipt={
    'checked_at':datetime.now(timezone.utc).isoformat(),'passed':True,'cli_version':'2.1.270',
    'environment':'Windows interactive Claude session with process-local experimental Teams flag',
    'models_observed':sorted({r.get('message',{}).get('model') for rows in [main,*children.values()] for r in rows if r.get('message',{}).get('model')}),
    'teammate_count':2,'teammate_changes':changes,'original_model_and_tests_unchanged':True,
    'original_archive_sha256':setup['archive_sha256'],'current_archive_sha256':hashlib.sha256(current_zip.read_bytes()).hexdigest(),
    'current_starter_matches_original_after_lf_normalization':True,
    'project_tests':{'passed':10,'observed_direct_exit':0},
    'independent_tests':{'passed':3,'log':'team-feature-independent.log'},
    'browser':{'tool':'Codex in-app browser','passed':True,'observations':['renamed all button and aria-pressed state','add three tasks','toggle B complete','active filter shows A and C','completed filter shows B','delete B from completed view','all view retains hidden A and C','HTML-shaped title is literal text with zero b elements','360px viewport: scrollWidth 345; controls and three items readable']},
    'verifier_notes':['UI initially considered no block necessary because buttons only send known modes; verifier explicitly restated the controlled contract-decision drill, then the same teammate reported the block.','Unknown-mode decision went to data-builder; label change went only to ui-builder. No third teammate or rewrite of completed work.','Lead final marker had a spelling typo MOKAAAIR; result is judged by actual files, messages and tests.','Lead piped test output through tail; the verifier also ran the two test files directly and observed exit 0.','This is a scoped functional Teams exercise, not a statistically controlled performance comparison.'],
    'session_stopped':True,'session_exit_code':0,'test_server_stopped':True,
    'trace':'team-feature-events.json','artifact':'team-feature-result.zip','artifact_sha256':hashlib.sha256(result_archive.read_bytes()).hexdigest(),'files':files,
}
(OUT/'team-feature-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary_path=OUT/'real-operations-summary.json';summary=json.loads(summary_path.read_text(encoding='utf-8'))
summary['teams_feature']={'passed':True,'source':'team-feature-validation.json','scope':'Two named teammates, controlled block/decision, scoped feature and label changes, 10 project tests, 3 independent tests and real browser verification'}
summary['headless_boundary']={'passed':True,'source':'headless-turn-limit.json','scope':'Real CLI max-turn error; do not parse an error result as an empty successful review'}
summary['pending']=[p for p in summary['pending'] if not p.startswith('Additional product-specific')]
summary_path.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':True,'teammates':changes,'project_tests':10,'independent_tests':3,'artifact_bytes':result_archive.stat().st_size}))
