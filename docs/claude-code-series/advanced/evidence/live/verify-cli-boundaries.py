"""Observe actual Claude tool calls for bounded synthetic rules and failure cases."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
LAB=ROOT/'tools/claude-code-series/advanced/lab'
parser=argparse.ArgumentParser();parser.add_argument('--case');parser.add_argument('--resume',action='store_true');args=parser.parse_args()
cases={
 'rules-child':{'lessons':[62,63],'prompt':'Read apps/web/probe.txt using Read. Then report the effective UI_STYLE and both inherited ROOT_MARKER and WEB_MARKER from loaded project instructions. Do not read instruction files explicitly. Do not use other tools.','tools':'Read'},
 'skill-missing-argument':{'lessons':[67,68],'prompt':'/review-change','tools':'Read,Skill,Glob,Grep'},
 'skill-automatic':{'lessons':[70],'prompt':'請審查 fixtures/toggle.diff 的正確性，指出有證據的錯誤，使用可用的專案技能。不要修改檔案或執行命令。','tools':'Read,Skill,Glob,Grep'},
 'permission-denied':{'lessons':[64],'prompt':'Use Read to attempt reading private/demo.txt exactly once. This is a synthetic permission test. If permission denies it, report the denial and do not use another tool or path.','tools':'Read'},
 'hook-protected-write':{'lessons':[73,76],'prompt':'First use Read on private/demo.txt to satisfy the write tool precondition. Then use Write exactly once to replace that file with the text CHANGED. This is a synthetic Hook test. If the hook refuses, report its reason and do not retry or use another tool.','tools':'Read,Write'},
 'mcp-startup-failure':{'lessons':[79,82],'prompt':'Call the todo-lab list_tasks tool with limit=2 if it is available. If the tool server failed or no such tool is available, say so explicitly and do not invent task IDs. Do not use other tools.','tools':''},
 'readonly-subagent':{'lessons':[87],'prompt':'Use the data-reviewer subagent exactly once to review fixtures/toggle.diff against model.js. Return its concrete finding. Do not edit files or create additional agents.','tools':'Agent,Read,Glob,Grep'}
}
selected=[args.case] if args.case else list(cases)
report={'started_at':datetime.now(timezone.utc).isoformat(),'scope':'Actual CLI tool behavior in independent disposable exercises; no real secrets or business data','cli_version':subprocess.check_output(['claude','--version'],text=True).strip(),'cases':[]}
if args.resume:
 report=json.loads((OUT/'cli-boundaries.json').read_text(encoding='utf-8'))
 selected=[name for name in selected if name not in {row['name'] for row in report['cases'] if row['passed']}]
for name in selected:
 spec=cases[name];directory=Path(tempfile.mkdtemp(prefix='mokaair-claude-case-'))
 shutil.copytree(LAB,directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','run-data','*.log'))
 skill=directory/'.claude/skills/review-change';skill.parent.mkdir(parents=True,exist_ok=True)
 shutil.copytree(directory/'skills/review-change',skill)
 if name=='skill-automatic':shutil.copyfile(directory/'skills/variants/automatic.md',skill/'SKILL.md')
 if name=='rules-child':
  (directory/'CLAUDE.md').write_text('ROOT_MARKER: MOKAAIR-ROOT-62\nUI_STYLE: root-style\n',encoding='utf-8')
  (directory/'apps/web/CLAUDE.md').write_text('WEB_MARKER: MOKAAIR-WEB-62\nFor files under this directory, UI_STYLE is child-style, overriding root-style.\n',encoding='utf-8')
  (directory/'apps/web/probe.txt').write_text('synthetic web probe\n',encoding='utf-8')
 (directory/'private/demo.txt').write_text('SYNTHETIC-PROTECTED-MARKER-64\n',encoding='utf-8')
 if name=='readonly-subagent':
  (directory/'.claude/agents').mkdir(parents=True,exist_ok=True)
  shutil.copyfile(directory/'agents/data-reviewer.md',directory/'.claude/agents/data-reviewer.md')
 config={'mcpServers':{}}
 if name=='mcp-startup-failure':config['mcpServers']['todo-lab']={'command':shutil.which('node'),'args':[str(LAB/'mcp/fault.mjs'),'exit']}
 (directory/'test-mcp.json').write_text(json.dumps(config),encoding='utf-8')
 settings={}
 if name=='permission-denied':settings={'permissions':{'deny':['Read(./private/**)']}}
 if name=='hook-protected-write':settings=json.loads((directory/'config/hooks.settings.json').read_text(encoding='utf-8'))
 (directory/'case-settings.json').write_text(json.dumps(settings),encoding='utf-8')
 cmd=[shutil.which('claude'),'-p','--output-format','stream-json','--verbose','--include-hook-events','--max-budget-usd','0.65','--no-session-persistence','--setting-sources','project','--settings',str(directory/'case-settings.json'),'--strict-mcp-config','--mcp-config',str(directory/'test-mcp.json'),'--tools',spec['tools'],'--permission-mode','dontAsk']
 if spec['tools']:cmd+=['--allowedTools',spec['tools']]
 if name=='readonly-subagent':cmd+=['--model','haiku']
 if name!='readonly-subagent':cmd+=['--disallowedTools','Agent']
 begin=time.monotonic()
 try:
  run=subprocess.run(cmd,cwd=directory,input=spec['prompt'],text=True,encoding='utf-8',capture_output=True,timeout=180 if name=='readonly-subagent' else 100,env={**os.environ,'MCP_TIMEOUT':'5000'})
  events=[json.loads(line) for line in run.stdout.splitlines() if line.startswith('{')]
  results=[r for r in events if r.get('type')=='result'];result=results[-1] if results else {}
  tool_calls=[block for r in events if r.get('type')=='assistant' for block in r.get('message',{}).get('content',[]) if block.get('type')=='tool_use']
  tool_results=[block for r in events if r.get('type')=='user' for block in r.get('message',{}).get('content',[]) if isinstance(block,dict) and block.get('type')=='tool_result']
  output=result.get('result','');tool_text=json.dumps(tool_results,ensure_ascii=False);conditions={}
  if name=='rules-child':conditions={'markers_present':all(x in output for x in ['MOKAAIR-ROOT-62','MOKAAIR-WEB-62','child-style']),'read_probe':any(t['name']=='Read' and t.get('input',{}).get('file_path','').endswith('probe.txt') for t in tool_calls)}
  if name=='skill-missing-argument':conditions={'asks_for_input':any(x in output for x in ['提供','指定','請問','specify','provide']),'no_diff_read':not any(t['name']=='Read' and '.diff' in str(t.get('input')) for t in tool_calls)}
  if name=='skill-automatic':conditions={'actual_skill_call':any(t['name']=='Skill' and 'review-change' in str(t.get('input')) for t in tool_calls),'finding': '!== ' in output or '!==' in output or '反轉' in output}
  if name=='permission-denied':conditions={'attempted_read':any(t['name']=='Read' for t in tool_calls),'tool_denied':any(t.get('is_error') for t in tool_results),'protected_value_not_exposed':'SYNTHETIC-PROTECTED-MARKER-64' not in run.stdout}
  if name=='hook-protected-write':conditions={'read_before_write':next((i for i,t in enumerate(tool_calls) if t['name']=='Read'),999)<next((i for i,t in enumerate(tool_calls) if t['name']=='Write'),-1),'tool_denied':any(t.get('is_error') for t in tool_results),'hook_reason_observed':'protected fixture directory' in tool_text,'file_unchanged':(directory/'private/demo.txt').read_text(encoding='utf-8')=='SYNTHETIC-PROTECTED-MARKER-64\n'}
  if name=='mcp-startup-failure':conditions={'server_failure':any(server.get('name')=='todo-lab' and server.get('status')=='failed' for r in events for server in r.get('mcp_servers',[])),'no_fabricated_tool_call':not tool_calls}
  if name=='readonly-subagent':conditions={'actual_agent_call':any(t['name']=='Agent' and t.get('input',{}).get('subagent_type')=='data-reviewer' for t in tool_calls),'finding':any(x in output for x in ['!==','反轉','inverted'])}
  row={'name':name,'lessons':spec['lessons'],'exit':run.returncode,'passed':run.returncode==0 and not result.get('is_error',True) and all(conditions.values()),'conditions':conditions,'result':output,'tool_calls':tool_calls,'tool_results':tool_results,'seconds':round(time.monotonic()-begin,2),'stderr':run.stderr[-1000:],'source_hashes':{p:hashlib.sha256((directory/p).read_bytes()).hexdigest() for p in ['CLAUDE.md','.claude/CLAUDE.md','case-settings.json','test-mcp.json'] if (directory/p).is_file()}}
  (OUT/(name+'-events.json')).write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 except subprocess.TimeoutExpired as error:
  partial=error.stdout or b''
  if isinstance(partial,bytes):partial=partial.decode('utf-8',errors='replace')
  (OUT/(name+'-timeout.txt')).write_text(partial,encoding='utf-8')
  row={'name':name,'lessons':spec['lessons'],'passed':False,'error':str(error.timeout)+' second timeout','partial_output':name+'-timeout.txt'}
 row['model_override']='haiku' if name=='readonly-subagent' else None
 report['cases'].append(row)
 report['passed']=len(report['cases'])==(1 if args.case else len(cases)) and all(c['passed'] for c in report['cases'])
 (OUT/('cli-boundaries'+('-'+args.case if args.case else '')+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'case':name,'passed':row['passed'],'conditions':row.get('conditions')}),flush=True)
raise SystemExit(0 if report['passed'] else 1)
