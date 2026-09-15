"""Measure red/green with identical independent assertions and an actual Claude fix."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

OUT=Path(__file__).resolve().parent
initial=json.loads((OUT/'capstone-implementation.json').read_text(encoding='utf-8'))
directory=Path(initial['directory'])
assert directory.name.startswith('mokaair-capstone-live-')
test=OUT/'capstone-acceptance.test.mjs'
def verify():return subprocess.run([shutil.which('node'),'--test',str(test)],cwd=directory,env={**os.environ,'CAPSTONE_DIRECTORY':str(directory)},text=True,encoding='utf-8',capture_output=True,timeout=20)
before=(directory/'model.js').read_text(encoding='utf-8')
assert 'item.id !== id ?' in before
red=verify();assert red.returncode!=0
prompt='修正 model.js 中 toggleTodo 的指定故障：目前把其他 id 的項目切換、目標 id 卻不變。請 Read 該檔及 tests/model.test.mjs，使用 Edit 只修正 model.js；不改測試或其他檔案，不建立代理、不執行命令、不連外部服務。回報實際修正與未執行的檢查。'
command=[shutil.which('claude'),'-p','--model','haiku','--output-format','stream-json','--verbose','--max-budget-usd','0.50','--max-turns','8','--no-session-persistence','--setting-sources','project','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--tools','Read,Edit','--allowedTools','Read,Edit','--disallowedTools','Agent','--permission-mode','dontAsk']
run=subprocess.run(command,cwd=directory,input=prompt,text=True,encoding='utf-8',capture_output=True,timeout=120)
events=[json.loads(line) for line in run.stdout.splitlines() if line.startswith('{')]
(OUT/'capstone-repair-events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result=next((event for event in reversed(events) if event.get('type')=='result'),{})
green=verify()
diff=subprocess.check_output(['git','diff','--','model.js'],cwd=directory,text=True,encoding='utf-8')
other=subprocess.check_output(['git','diff','--name-only'],cwd=directory,text=True,encoding='utf-8')
report={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Intentional ID inversion in an isolated synthetic project, real Claude repair, identical independent test before and after','model_override':'haiku','assertions_sha256':hashlib.sha256(test.read_bytes()).hexdigest(),'red':{'exit':red.returncode,'output':red.stdout},'repair':{'exit':run.returncode,'result':result},'green':{'exit':green.returncode,'output':green.stdout},'diff_against_prefault_feature':diff,'changed_tracked_files_after_repair':other,'passed':run.returncode==0 and not result.get('is_error',True) and green.returncode==0 and not diff and not other}
(OUT/'capstone-repair.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'red_exit':red.returncode,'green_exit':green.returncode}))
raise SystemExit(0 if report['passed'] else 1)
