"""Exercise the unmodified SDK runner's local rejection and startup recovery paths."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
RUNNER=ROOT/'tools/claude-code-series/advanced/lab/automation/sdk/run.mjs'
directory=Path(tempfile.mkdtemp(prefix='mokaair-sdk-recovery-')).resolve()
state_path=directory/'run-data/session.json'
report={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Unmodified lesson 94 runner: local state rejection, executable startup failure and fresh-query recovery; not physical Ctrl+C or network interruption','source_sha256':hashlib.sha256(RUNNER.read_bytes()).hexdigest(),'temporary_directory':str(directory),'cases':[]}
def run(name,args=(),binary=None):
    result=subprocess.run([shutil.which('node'),str(RUNNER),*args],cwd=directory,env={**os.environ,'CLAUDE_BIN':binary or shutil.which('claude')},capture_output=True,text=True,encoding='utf-8',timeout=100)
    state=json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else None
    return {'name':name,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr[-2000:],'state':state}

row=run('missing-session',('--resume',))
row['passed']=row['exit']==2 and row['state'] is None and 'No saved session' in row['stderr']
report['cases'].append(row)
state_path.parent.mkdir(parents=True,exist_ok=True)
invalid={'schemaVersion':1,'status':'failed','sessionId':None}
state_path.write_text(json.dumps(invalid),encoding='utf-8')
row=run('incompatible-session',('--resume',))
row['passed']=row['exit']!=0 and row['state']==invalid and 'No compatible saved session id' in row['stderr']
report['cases'].append(row)
row=run('executable-startup-failure',binary=str(directory/'intentionally-missing-claude.exe'))
row['passed']=row['exit']==1 and row['state']['status']=='failed' and not row['state']['sessionId'] and bool(row['state'].get('error'))
report['cases'].append(row)
row=run('fresh-query-after-startup-failure')
row['passed']=row['exit']==0 and row['state']['status']=='completed' and bool(row['state']['sessionId']) and 'MOKAAIR-SDK-94' in row['state'].get('result','')
report['cases'].append(row)
report['passed']=all(row['passed'] for row in report['cases'])
(OUT/'sdk-recovery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'cases':[{'name':row['name'],'passed':row['passed']} for row in report['cases']]}))
raise SystemExit(0 if report['passed'] else 1)
