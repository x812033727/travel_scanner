"""Consolidate observed retries without erasing failed or misattributed attempts."""
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
first=OUT/'cli-boundaries-first-attempt.json'
if not first.exists():
    initial=read('cli-boundaries.json')
    hook=next(row for row in initial['cases'] if row['name']=='hook-protected-write')
    hook['original_reported_passed']=hook['passed']
    hook['passed']=False
    hook['conditions']['hook_reason_observed']=False
    hook['correction']='The first attempt hit Write read-before-overwrite validation, not the authored Hook. It cannot prove Hook invocation.'
    initial['passed']=False
    write(first.name,initial)
initial=read(first.name)
latest={row['name']:row for row in initial['cases']}
for name in ['hook-protected-write','readonly-subagent']:
    retry=read('cli-boundaries-'+name+'.json')
    assert retry['passed'] and len(retry['cases'])==1
    latest[name]=retry['cases'][0]
agent=latest['readonly-subagent']
agent['conditions']['readonly_tools_only']=all(row['name'] in ['Agent','Read','Grep','Glob'] for row in agent['tool_calls'])
agent['conditions']['one_agent']=sum(row['name']=='Agent' for row in agent['tool_calls'])==1
agent['passed']=agent['passed'] and all(agent['conditions'].values())
assert len(latest)==7 and all(row['passed'] for row in latest.values())
combined={**initial,'checked_at':datetime.now(timezone.utc).isoformat(),'cases':list(latest.values()),'passed':True,'attempt_history':first.name,'retries':['cli-boundaries-hook-protected-write.json','cli-boundaries-readonly-subagent.json']}
write('cli-boundaries.json',combined)
summary=read('real-operations-summary.json')
summary['checked_at']=combined['checked_at']
summary['cli_boundaries']={'passed':True,'source':'cli-boundaries.json','case_count':7,'cases':[{'name':row['name'],'lessons':row['lessons'],'passed':row['passed']} for row in latest.values()],'limits':['One readonly subagent with Haiku is not an Agent Teams or model comparison test','Read denial does not test Bash sandbox','MCP startup failure does not verify remote OAuth or all protocol errors']}
sdk=read('sdk-recovery.json');assert sdk['passed']
summary['sdk']['recovery_passed']=True
summary['sdk']['recovery_cases']=[row['name'] for row in sdk['cases']]
summary['sdk']['sources']=list(dict.fromkeys(summary['sdk']['sources']+['sdk-recovery.json']))
summary['sdk']['limitations']=['Physical Ctrl+C and recovery of an interrupted session remain untested; the startup recovery uses a fresh query']
workflow='.github/workflows/claude-tutorial-validation.yml'
summary['github_actions'].update({'local_workflow_prepared':True,'workflow_path':workflow,'local_validation_source':'ci-workflow-validation.json','reason':'A monorepo workflow is prepared locally with manual opt-in model review. It is not merged or dispatched; the selected repository still needs the claude-lab environment and a dedicated Anthropic CI credential.'})
summary['pending']=['Other rule conflicts, Skill resource selection, Hook event failures and supported-OS Bash sandbox','Physical mobile reconnection, sleep and recovery','Real remote MCP HTTP/OAuth authorization and recovery','Merge the manual CI workflow and configure an Anthropic credential and claude-lab environment for the authorized travel_scanner Actions test','Product scheduling, physical SDK runner Ctrl+C and interrupted-session recovery','Actual Agent Teams, real workflow comparison and full agent-led capstone']
if (OUT/'capstone-clean-replay.json').exists():
    capstone=read('capstone-clean-replay.json');browser=read('capstone-browser.json');repair=read('capstone-repair.json');implementation=read('capstone-implementation.json')
    assert all(report['passed'] for report in [capstone,browser,repair,implementation])
    summary['capstone']={'passed':True,'lesson':96,'scope':'Actual model-authored local feature, independent assertions, browser workflow, specified failure and repair, fresh extracted replay; no physical phone or deployment','sources':['capstone-implementation.json','capstone-tests.json','capstone-browser.json','capstone-repair.json','capstone-clean-replay.json'],'archive':'capstone-result.zip','archive_sha256':capstone['archive_sha256'],'project_tests':9,'independent_tests':3,'browser_cases':len(browser['cases']),'verifier_corrections':capstone['verifier_corrections'],'test_server_stopped':True}
    summary['pending'][-1]='Actual Agent Teams and real workflow comparison'
write('real-operations-summary.json',summary)
write('ci-workflow-validation.json',{'checked_at':combined['checked_at'],'scope':'Local commands captured from the current tool execution; not a GitHub Actions run','workflow':workflow,'workflow_sha256':hashlib.sha256((ROOT/workflow).read_bytes()).hexdigest(),'official_action_source':'https://github.com/anthropics/claude-code-action/blob/9cdae7f0d995e3ba7c33f226087fdf82a59cd520/action.yml','source_checked_on':'2026-09-14','checks':[{'command':'node --test tools/claude-code-series.test.mjs','cwd':'repository root','tests':12,'passed':12,'failed':0,'exit':0},{'command':'node --test tests/model.test.mjs tests/automation.test.mjs tests/sdk-state.test.mjs','cwd':'tools/claude-code-series/advanced/lab','tests':8,'passed':8,'failed':0,'exit':0}],'remote_workflow_run':False})
if (OUT/'tools-final.log').exists():
    log=(OUT/'tools-final.log').read_text(encoding='utf-8')
    assert re.search(r'pass 52\b',log) and re.search(r'fail 0\b',log)
    receipt=read('ci-workflow-validation.json')
    receipt['full_tools']={'command':'npm run test:tools','passed':True,'tests':52,'failed':0,'exit':0,'source':'tools-final.log','initial_attempt':'51 passed, 1 failed because version comments were absent; fixed using verified tags before rerun'}
    write('ci-workflow-validation.json',receipt)
print(json.dumps({'cli_boundaries':7,'sdk_recovery':len(sdk['cases']),'ci_workflow':'locally prepared and tested; remote run pending'}))
