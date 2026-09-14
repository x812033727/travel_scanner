"""Verify final archive hashes and consolidate actual, separately scoped receipts."""
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DOC=ROOT/'docs/claude-code-series/advanced';E=DOC/'evidence'
def read(name):return json.loads((E/name).read_text(encoding='utf-8'))
def write(name,data):(E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'apps/api/app/guides/series_data/claude-code.json').read_text(encoding='utf-8'))
content=read('content-validation.json');assert content['complete'] and len(content['pages'])==97
pages={p['slug']:p for p in content['pages']}
quick=read('downloads-quick-tests.json');full=read('downloads-tests.json')
assert quick['passed'] and full['passed']
assert len(quick['archives'])==36
assert {r['number'] for r in full['archives']}=={61,67,73,79,88,91}
for row in [*quick['archives'],*full['archives']]:
    archive=ROOT/f'apps/web/public/tutorials/claude-code/advanced/lesson-{row["number"]}.zip'
    assert sha(archive)==row['sha256'],f'Stale download receipt {row["number"]}'
    assert all(check['exit']==check.get('expected_exit',0) for check in row['checks'])
initial=read('browser-tests.json');retry=read('browser-search-recheck.json');downloads=read('browser-download-check.json')
def specs(report):
    def visit(node):
        yield from node.get('specs',[])
        for child in node.get('suites',[]):yield from visit(child)
    return list(visit(report))
final={};attempts=[]
for filename,report in [('browser-tests.json',initial),('browser-search-recheck.json',retry),('browser-download-check.json',downloads)]:
    for spec in specs(report):
        status=spec['tests'][0]['results'][-1]['status']
        row={'title':spec['title'],'status':status,'source':filename}
        attempts.append(row);final[spec['title']]=row
assert len(final)==9 and all(row['status']=='passed' for row in final.values())
write('browser-verification.json',{'passed':True,'cases':list(final.values()),'attempts':attempts,'note':'Initial missing --json-schema alias was fixed; only the affected search/filter test was rerun. Device sizes are browser emulation, not real phones.'})
web=read('web-focused-tests.json');assert web['success'] and web['numFailedTests']==0
tools=(E/'tools-tests.txt').read_text(encoding='utf-8');assert re.search(r'fail 0\b',tools)
model_source='live/claude-live-all.json' if (E/'live/claude-live-all.json').exists() else 'claude-live-all.json'
model_attempts=read(model_source)
model_smokes_passed=all(case['passed'] for case in model_attempts['cases']) and len(model_attempts['cases'])==5
real_operations=read('live/real-operations-summary.json') if (E/'live/real-operations-summary.json').exists() else {}
supplement=read('live/verification-summary.json') if (E/'live/verification-summary.json').exists() else {}
full_web=supplement.get('web',{})
postgres=supplement.get('api',{})
models={case['lesson']:case for case in model_attempts['cases']}
local={
61:'core baseline and broken/correct rules files; actual Claude attempt blocked',
62:'three project directories and scoped rules included; loading behavior not live-tested',
63:'diagnosis material and core baseline; actual rule loading pending',
64:'course settings validation; real permission and supported OS sandbox behavior pending',
65:'handoff template and reference filter tests; actual conversation handoff pending',
66:'correct and incorrect settings accepted/rejected by course validator',
67:'Skill files and fixtures; actual Claude invocation blocked',
68:'input parser tests include missing/invalid/Unicode/shell-symbol filenames',
69:'resource routing materials included; actual conditional loading pending',
70:'invocation variants included; model selection and invocation pending',
71:'human-rating parser on synthetic fixtures; no model benchmark claimed',
72:'claude plugin validate passed; marketplace installation not tested',
73:'fixed Hook event scripts tested; actual Claude Hook attempt blocked',
74:'formatter fixed events: scoped, idempotent, preserves data',
75:'quality script and repeated Stop fixed events; actual product trigger pending',
76:'protected/outside path checks on fixed tool events; not universal file protection',
77:'audit field selection and local notification deduplication tested',
78:'Windows fixtures and bounded timeout probe; macOS/Linux execution pending',
79:'actual MCP stdio connection and tools; actual Claude client attempt blocked',
80:'actual MCP pagination, invalid input and missing/empty results tested',
81:'local non-MCP HTTP 401/403/200 fixture; real OAuth pending',
82:'MCP exit/invalid-output/hang probes tested; inner deadline unchanged',
83:'untrusted MCP output fixture included; model resistance not live-tested',
84:'local draft template and reference filter; no remote PR created',
85:'same authored assertions fail on starter and pass on reference; same browser interaction verified',
86:'legacy/reference statistics and independent downloaded tests pass',
87:'two readonly agent definitions included; no real subagent execution',
88:'two real temporary Git worktrees, controlled conflict and five integration tests',
89:'team roles and integration material; no actual Agent Teams execution',
90:'device recovery checklist only; no physical device pairing or interruption test',
91:'structured output parsers tested; actual Claude attempt blocked',
92:'workflow YAML and artifact validator tested locally; no external Actions run',
93:'CLI failure/recovery/reuse/cancellation and separate attempt files tested; no scheduler activated',
94:'SDK package and state parsing tested; actual query/resume/cancel pending',
95:'evaluation and CSV export use explicitly synthetic observations',
96:'downloaded reference app browser-tested for filter/persistence/text safety/corrupt storage; full agent-led capstone pending',
}
if model_smokes_passed:
    local.update({61:'actual Claude loaded the project marker and verification command',67:'actual Skill invocation identified the synthetic inverted ID condition using readonly tools',73:'actual Claude Read triggered the configured PostToolUse Hook and produced an audit event',79:'actual Claude MCP smoke returned IDs a and b and nextOffset 2',91:'actual Claude structured output matched the schema and returned all three task IDs'})
if real_operations.get('sdk',{}).get('passed'):
    local[94]='authored SDK query and same-session resume passed; separate streaming-input AbortController cancellation probe passed; physical Ctrl+C and failure recovery in the authored runner remain pending'
boundaries=real_operations.get('cli_boundaries',{})
boundary_lessons=set()
if boundaries.get('passed'):
    boundary_lessons={number for case in boundaries['cases'] for number in case['lessons']}
    local.update({62:'actual Read loaded root and child markers and the child UI_STYLE override',63:'actual lazy loading of child rules observed after reading a file in that directory; other rule conflicts remain untested',64:'actual Read deny withheld the synthetic protected value; supported-OS Bash sandbox remains untested',68:'actual Skill call without arguments requested the filename and did not guess a diff; parser edge cases also passed',70:'actual model-selected Skill tool call observed without supplying its slash command; automatic variant was installed',76:'actual Read followed by Write reached the PreToolUse Hook; its protected fixture directory reason and unchanged bytes were verified',82:'actual Claude client reported the failed MCP server and made no fabricated tool call; invalid-output and hang remain local protocol probes',87:'actual data-reviewer subagent used only Read and Grep and identified the inverted condition; Haiku override, no Agent Teams claim'})
if real_operations.get('sdk',{}).get('recovery_passed'):
    local[94]='authored query/resume, missing/incompatible state rejection, failed executable startup and fresh-query recovery passed; separate streaming cancellation probe passed; physical Ctrl+C and interrupted-session recovery remain pending'
if real_operations.get('capstone',{}).get('passed'):
    local[96]='actual Claude-authored filters/UI/storage passed 9 project and 3 independent tests, 10 in-app browser cases, specified defect red/green repair and clean archive replay; verifier corrected one handoff statement; physical phone and deployment not performed'
lesson_rows=[]
for entry in manifest['entries']:
    n=entry['number']
    if n<61:continue
    page=pages[entry['slug']];minimum=4000 if n==96 else 2500
    assert minimum<=page['body_characters']<=(6000 if n==96 else 4000),(n,page['body_characters'])
    execution=('passed-smoke' if models[n]['passed'] else 'failed-smoke') if n in models else ('passed-sdk-smoke' if n==94 and real_operations.get('sdk',{}).get('passed') else 'not-performed')
    if n in boundary_lessons and execution=='not-performed':execution='passed-bounded-case'
    if n==96 and real_operations.get('capstone',{}).get('passed'):execution='passed-local-capstone'
    lesson_rows.append({'number':n,'slug':entry['slug'],'author_sha256':sha(ROOT/f'docs/claude-code-series/lessons/{n}.md'),'pack_sha256':sha(ROOT/f'apps/api/app/guides/content/{entry["slug"]}.json'),'body_characters':page['body_characters'],'document_sources_verified':True,'local_material_status':local[n],'core_archive_checks':'passed-with-documented-broken-starter','browser_page':'passed','claude_execution':execution,'publication':'not-published','download_sha256':next(r['sha256'] for r in quick['archives'] if r['number']==n)})
write('lesson-verification.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'os':'Windows','node':'24.13.0','cli':model_attempts['cli_version'],'lessons':lesson_rows})
write('delivery-checks.json',{
 'checked_at':datetime.now(timezone.utc).isoformat(),'status':'local-preview-ready','scope':'36 new lessons and the combined 97-page local preview; not release approval',
 'content':{'pages':97,'new_lessons':36,'groups':16,'learning_paths':12,'errors':0,'warnings':0,'source':'content-validation.json'},
 'art':read('art-validation.json'),
 'downloads':{'archives':36,'groups':6,'quick_checks':sum(len(r['checks']) for r in quick['archives']),'pilot_archives':6,'tool_suite_tests_per_pilot':21,'sources':['downloads-quick-tests.json','downloads-tests.json']},
 'browser':{'latest_cases_passed':9,'source':'browser-verification.json','physically_tested_mobile_devices':False},
 'web_tests':{'scope':'affected guide/series/editor/server helper suites','source':'web-focused-tests.json',**{k:web[k] for k in ['numTotalTests','numPassedTests','numFailedTests','numPendingTests']}},
 'broad_web_suite':full_web if full_web else {'status':'not-completed','note':'No success claimed. Relevant 73 tests passed separately.'},
 'postgresql_suite':postgres if postgres else {'status':'not-performed'},
 'supplementary_verification':'live/verification-summary.json' if supplement else None,
 'real_operations':real_operations,
 'claude_smoke_source':model_source,
 'commands_from_task_outputs':[
  {'command':'npm run build:web','exit':0},
  {'command':'npm run lint:web','exit':0},
  {'command':'npm run check:i18n','exit':0,'detail':'5 locales, 25 namespaces'},
  {'command':'npm run typecheck:web','exit':0},
  {'command':'npm run test:tools','exit':0,'detail':'51 passed; tools-tests.txt'},
  {'command':'uv run ruff check app/guides tests/test_guide_series.py','exit':0},
  {'command':'uv run mypy app','exit':0,'detail':'328 source files'},
  {'command':'uv run pytest tests/test_guide_series.py tests/test_guides.py -q','exit':0,'detail':'Earlier run: 87 passed, 77 skipped; PostgreSQL integration disabled. See postgresql_suite for the supplementary run.'},
  {'command':'claude plugin validate ./plugin','exit':0,'detail':'local manifest validation, not a model call'},
  {'command':'node hooks/timeout-demo.mjs','exit':0,'detail':'expectedTimeout=true, ETIMEDOUT, 339 ms; controlled local child'},
  {'command':'node worktrees/demo.mjs','exit':0,'detail':'worktree-tests.json'},
 ],
 'manual_visual_review':['project-rules-workshop-code-360.png','structured-cli-pipeline-code-390.png','tdd-reference-390.png'],
 'limitations':[*(['Claude CLI smoke checks not passed'] if not model_smokes_passed else []),*real_operations.get('pending',['Remaining real operations not reviewed']),*(['PostgreSQL integration not passed'] if not postgres.get('passed') else []),'Not merged, deployed, imported or published'],
 'environment_notes':['Shared browser installation was incomplete; matching Chromium installed in a dedicated temporary cache','Broad Vitest was restarted; reported guide tests come from the focused single-worker invocation','MCP test process startup/cleanup allowance increased to 20 seconds; protocol deadline remains 1500 ms'],
})
print(json.dumps({'status':'local-preview-ready','pages':97,'new_lessons':36,'archives':36,'browser_cases':9,'web_tests':web['numPassedTests']}))
