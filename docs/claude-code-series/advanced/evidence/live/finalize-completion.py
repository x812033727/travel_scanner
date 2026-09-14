"""Consolidate observed product results without erasing earlier failed attempts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
session='66298802-5080-4384-bfae-d4d73b57db42'
project=Path.home()/'.claude/projects/C--Users-x8120-AppData-Local-Temp-mokaair-teams-live-d7295d31'
def rows(path):return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
main=rows(project/(session+'.jsonl'))
def blocks(events,kind):
 for row in events:
  content=row.get('message',{}).get('content',[])
  if isinstance(content,list):
   for block in content:
    if block.get('type')==kind:yield {**block,'timestamp':row.get('timestamp'),'role':row.get('type')}
calls=list(blocks(main,'tool_use'));answers=list(blocks(main,'tool_result'));texts=list(blocks(main,'text'))
children={p.stem:rows(p) for p in (project/session/'subagents').glob('*.jsonl')}
team_calls=[c for c in calls if c['name']=='Agent']
child_reads={name:sum(c['name']=='Read' for c in blocks(events,'tool_use')) for name,events in children.items()}
child_messages=[c for events in children.values() for c in blocks(events,'tool_use') if c['name']=='SendMessage']
followup=[c['text'] for events in children.values() for c in blocks(events,'text') if 'Acknowledged' in c.get('text','') and 'MOKAAIR-FOLLOWUP-89' in c.get('text','')]
created=next(c for c in calls if c['name']=='CronCreate')
lists=[c for c in calls if c['name']=='CronList']
last_list=next(a for a in answers if a['tool_use_id']==lists[-1]['id'])
cron_output=[c for c in texts if c['role']=='assistant' and '**MOKAAIR-CRON-93:**' in c['text']]
cron_pass=created['input']['recurring'] is False and bool(cron_output) and 'Total tasks:** 3' in cron_output[-1]['text'] and 'Completed tasks:** 1' in cron_output[-1]['text'] and 'No scheduled jobs' in str(last_list['content'])
team_pass=len(team_calls)==2 and len(children)==2 and all(n>=1 for n in child_reads.values()) and len(child_messages)>=2 and bool(followup)
start=next(r['timestamp'] for r in main if r.get('type')=='user' and 'Verify Agent Teams' in str(r.get('message',{}).get('content','')))
first_result=next(c for c in texts if '"taskCounts"' in c['text'] and '"pendingIds"' in c['text'])
elapsed=(datetime.fromisoformat(first_result['timestamp'])-datetime.fromisoformat(start)).total_seconds()
models=sorted({row.get('message',{}).get('model') for events in [main,*children.values()] for row in events if row.get('message',{}).get('model')})
trace={'main':[{'timestamp':r.get('timestamp'),'role':r.get('type'),'content':r.get('message',{}).get('content')} for r in main if r.get('type') in ['user','assistant']], 'teammates':{name:[{'timestamp':r.get('timestamp'),'role':r.get('type'),'content':r.get('message',{}).get('content')} for r in events if r.get('type') in ['user','assistant']] for name,events in children.items()}}
# Publish only this synthetic exercise's conversation, with local paths replaced.
directory=str(Path((OUT/'interactive-lab-path.txt').read_text(encoding='utf-8-sig').strip()))
trace=json.loads(json.dumps(trace,ensure_ascii=False).replace(json.dumps(directory)[1:-1],'<exercise>'))
write('interactive-products-events.json',trace)
products={'checked_at':datetime.now(timezone.utc).isoformat(),'cli_version':'2.1.233','environment':'Windows ARM64 interactive terminal; experimental Teams flag set only on this process','teams':{'passed':team_pass,'scope':'Two named in-process teammates, independent reads, task assignment, mailbox replies and a follow-up in the same teammate; not the full UI feature integration exercise','names':[c['input']['name'] for c in team_calls],'models_observed':models,'child_read_counts':child_reads,'mailbox_reply_count':len(child_messages),'followup':followup,'seconds_to_first_combined_result':elapsed,'verifier_corrections':['Lead model called these ordinary subagents because they do not survive exit. That classification conflicts with the current official Teams documentation: named Agent calls in an interactive flagged session create in-process teammates. Actual mailbox routing and reuse were observed.','Lead redundantly completed tasks already completed by teammates and received Task not found; retained in trace.']},'schedule':{'passed':cron_pass,'scope':'Session CronCreate/CronList with a real one-shot trigger reading local synthetic data; not cloud/desktop scheduling, sleep recovery or the lesson job runner','created':created['input'],'final_reply':cron_output[-1]['text'] if cron_output else None,'final_list':last_list['content']},'session_stopped':True,'exit_code':0,'trace':'interactive-products-events.json','official_sources':['https://code.claude.com/docs/en/agent-teams','https://code.claude.com/docs/en/scheduled-tasks']}
assert team_pass and cron_pass
write('interactive-products.json',products)
single=read('workflow-single-baseline.json');result=single['result']['result'];data=json.loads(re.search(r'\{[\s\S]*\}',result).group())
single_pass=single['exit']==0 and data=={'marker':'MOKAAIR-TEAMS-89','totalTaskCount':3,'completedCount':1,'pendingIds':['b','c']}
write('workflow-observations.json',{'passed':single_pass and team_pass,'scope':'One exploratory observation per workflow on the same three synthetic tasks; not a statistical benchmark','cli_version':'2.1.233','single':{'seconds':single['seconds'],'models':single['result'].get('modelUsage',{}),'api_equivalent_cost_usd':single['result'].get('total_cost_usd'),'source':'workflow-single-baseline.json','passed':single_pass},'teams':{'seconds_to_first_combined_result':elapsed,'models_observed':models,'source':'interactive-products.json','passed':team_pass,'cost_usd':None},'limitations':['Single observation per workflow, no randomized repeated trial','Teams includes coordination prompts; the single agent does not','Teammates used their inherited/default models; model mix is explicitly recorded','A Max subscription was used; reported API-equivalent cost is not an invoice','No causal speed, quality, or cost advantage inferred']})
summary=read('real-operations-summary.json');summary['checked_at']=products['checked_at']
extra=read('extra-boundaries.json');assert extra['passed'];summary['extra_boundaries']={'passed':True,'source':'extra-boundaries.json','case_count':6,'cases':[{'name':r['name'],'lessons':r['lessons']} for r in extra['cases']]}
sdk=read('sdk-terminal-recovery.json');assert sdk['passed'];summary['sdk']['terminal_cancel_resume_passed']=True;summary['sdk']['sources']=list(dict.fromkeys(summary['sdk']['sources']+['sdk-terminal-recovery.json']));summary['sdk']['limitations']=['Ctrl+C was sent through a real terminal PTY by the verifier, not a human keyboard. No network interruption or external side effect rollback is claimed.'];summary['sdk']['runner_driver_version']=2
summary['teams']={'passed':team_pass,'source':'interactive-products.json','scope':products['teams']['scope']}
summary['schedule']={'passed':cron_pass,'source':'interactive-products.json','scope':products['schedule']['scope']}
summary['workflow_comparison']={'passed':single_pass and team_pass,'source':'workflow-observations.json','scope':'Exploratory single observation of each workflow; not a performance benchmark'}
summary['remote_control']={'local_session_started':True,'browser_history_visible':True,'browser_command_sent':False,'passed':False,'session_stopped':True,'session_url':'https://claude.ai/code/session_01AtAGQZpAd4QrtVs7P7ix5o','reason':'Browser required elevated device verification (device_key_missing). Google sign-in did not navigate in the in-app browser; no remote command or physical phone recovery is claimed.'}
summary['sandbox']={'passed':False,'environment':'WSL Ubuntu ARM64','preflight':{'bubblewrap_present':True,'socat_present':False,'linux_claude_present':False},'reason':'During dependency setup WSL became unresponsive, including a read-only process listing. Only the three owned Windows WSL client trees were stopped; Linux installation outcome is unconfirmed. No WSL shutdown or sandbox weakening was used.'}
summary['github_actions'].update({'environment_count':1,'environment_created':True,'branch_policy':'main only','environment_secret_count':0,'reason':'Dedicated claude-lab environment exists with a main-only branch policy. Manual workflow awaits merge and baseline dispatch; the model job requires the user to add ANTHROPIC_API_KEY.'})
summary['pending']=['Physical phone reconnection, sleep and recovery; browser Remote Control device verification','A real remote MCP HTTP/OAuth service for authorization, revocation and recovery','Supported OS Bash sandbox; WSL setup could not complete','Merge/register the manual Actions workflow and run baseline; paid model job awaits dedicated ANTHROPIC_API_KEY','Additional product-specific failure and full Teams feature-integration exercises beyond the documented smoke scope']
write('real-operations-summary.json',summary)
print(json.dumps({'teams':team_pass,'schedule':cron_pass,'sdk_terminal':sdk['passed'],'extra_boundaries':6,'single_seconds':single['seconds'],'team_seconds':elapsed}))
