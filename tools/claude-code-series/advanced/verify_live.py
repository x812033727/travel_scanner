"""Run bounded Claude smoke cases in disposable exercises; store no account identity."""
import argparse,json,os,shutil,subprocess,tempfile,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3]
LAB=Path(__file__).with_name('lab')
EVIDENCE=ROOT/'docs/claude-code-series/advanced/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--case',choices=['61','67','73','79','91','all'],default='all');args=p.parse_args()
 binary=shutil.which('claude');node=shutil.which('node')
 if not binary:raise SystemExit('Claude CLI missing')
 directory=Path(tempfile.mkdtemp(prefix='mokaair-advanced-live-'))
 shutil.copytree(LAB,directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','run-data','*.log'))
 skill=directory/'.claude/skills/review-change';skill.parent.mkdir(parents=True,exist_ok=True)
 shutil.copytree(directory/'skills/review-change',skill)
 empty=directory/'empty-mcp.json';empty.write_text('{"mcpServers":{}}',encoding='utf-8')
 actual_mcp=directory/'actual-mcp.json'
 actual_mcp.write_text(json.dumps({'mcpServers':{'todo-lab':{'command':node,'args':[str(LAB/'mcp/server.mjs')]}}}),encoding='utf-8')
 schema=(directory/'automation/schema.json').read_text(encoding='utf-8')
 cases={
 '61':('Return only the project rule marker and core verification command from the loaded project instructions. Do not use tools.',[],['MOKAAIR-LAB-61','node --test tests/model.test.mjs'],''),
 '67':('/review-change fixtures/toggle.diff',[],['id','!=='],'Read,Skill,Glob,Grep'),
 '73':('Use Read to read fixtures/tasks.json once. Then report the number of items. Do not modify files.', ['--settings',str(directory/'live-hook-settings.json')],['3'],'Read'),
 '79':('Use the todo-lab list_tasks MCP tool with limit=2. Report the returned IDs and nextOffset. Do not read files.',[],['a','b'],''),
 '91':('Return a short Traditional Chinese summary and all unique task IDs for this synthetic data: '+(directory/'fixtures/tasks.json').read_text(encoding='utf-8'),['--json-schema',schema],['a','b','c'],'')
 }
 settings={'hooks':{'PostToolUse':[{'matcher':'Read','hooks':[{'type':'command','command':'node hooks/audit.mjs','timeout':5}]}]}}
 (directory/'live-hook-settings.json').write_text(json.dumps(settings),encoding='utf-8')
 evidence=[]
 for name in ([args.case] if args.case!='all' else list(cases)):
  prompt,extra,expected,tools=cases[name]
  cmd=[binary,'-p','--output-format','json','--max-budget-usd','0.50','--no-session-persistence','--setting-sources','project','--strict-mcp-config','--mcp-config',str(actual_mcp if name=='79' else empty),'--tools',tools,'--permission-mode','dontAsk','--disallowedTools','Agent']
  if tools:cmd+=['--allowedTools',tools]
  if name=='79':cmd+=['--allowedTools','mcp__todo-lab__list_tasks']
  cmd+=extra
  started=time.monotonic()
  try:
   result=subprocess.run(cmd,cwd=directory,input=prompt,text=True,encoding='utf-8',capture_output=True,timeout=90)
   try: data=json.loads(result.stdout)
   except json.JSONDecodeError:data={'parse_error':True,'result':result.stdout[-1000:]}
   text=json.dumps(data.get('structured_output',data.get('result','')),ensure_ascii=False)
   passed=result.returncode==0 and not data.get('is_error',True) and all(word in text for word in expected)
   if name=='73':
    logs=directory/'run-data/events.jsonl'
    passed=passed and logs.exists() and any(json.loads(line).get('tool')=='Read' for line in logs.read_text().splitlines())
   evidence.append({'lesson':int(name),'passed':passed,'returncode':result.returncode,'subtype':data.get('subtype'),'result':data.get('result'),'structured_output':data.get('structured_output'),'model_usage':data.get('modelUsage'),'duration_seconds':round(time.monotonic()-started,2),'usage':data.get('usage'),'stderr_summary':result.stderr[-1200:]})
  except subprocess.TimeoutExpired:evidence.append({'lesson':int(name),'passed':False,'failure':'timeout','duration_seconds':90})
  EVIDENCE.mkdir(parents=True,exist_ok=True)
  report={'checked_at':datetime.now(timezone.utc).isoformat(),'cli_version':subprocess.run([binary,'--version'],capture_output=True,text=True).stdout.strip(),'os':'Windows','scope':'isolated synthetic exercise; no production data','cases':evidence}
  (EVIDENCE/('claude-live-'+args.case+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(json.dumps({'lesson':name,'passed':evidence[-1]['passed'],'seconds':evidence[-1].get('duration_seconds')},ensure_ascii=False),flush=True)
 print('Temporary exercise retained for inspection: '+str(directory),flush=True)
 return 0 if all(x['passed'] for x in evidence) else 1
if __name__=='__main__':raise SystemExit(main())
