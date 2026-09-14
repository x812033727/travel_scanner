"""Record observed GitHub merge and workflow results without changing GitHub state."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--run-id', type=int)
args = parser.parse_args()
out = Path(__file__).resolve().parent


def gh(*arguments):
    return json.loads(subprocess.check_output(['gh', *arguments], text=True, encoding='utf-8'))


def save(name, value):
    (out/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


pr = gh('pr', 'view', '501', '--json', 'number,state,url,headRefOid,baseRefOid,mergedAt,mergeCommit')
assert pr['state'] == 'MERGED' and pr['mergeCommit']['oid']
checks = gh('pr', 'checks', '501', '--json', 'name,state,link')
assert checks and all(c['state'] == 'SUCCESS' for c in checks)
release = {
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'pull_request': {
        'number': pr['number'], 'url': pr['url'], 'state': pr['state'].lower(),
        'merged': True, 'merged_at': pr['mergedAt'], 'head': pr['headRefOid'],
        'base': pr['baseRefOid'], 'merge_commit': pr['mergeCommit']['oid'],
    },
    'pre_merge_checks': checks,
    'deployment': 'not-performed', 'import': 'not-performed', 'publication': 'not-performed',
}
if args.run_id:
    run = gh('run', 'view', str(args.run_id), '--json', 'databaseId,headSha,event,status,conclusion,url,jobs')
    assert run['event'] == 'workflow_dispatch' and run['status'] == 'completed' and run['conclusion'] == 'success'
    jobs = {j['name']: j['conclusion'] for j in run['jobs']}
    assert jobs == {'baseline': 'success', 'model-review': 'skipped'}, jobs
    release['baseline_workflow'] = {
        'id': run['databaseId'], 'url': run['url'], 'sha': run['headSha'],
        'conclusion': run['conclusion'], 'input': {'run_model': False}, 'jobs': jobs,
        'scope': 'Actual GitHub hosted baseline only; paid Claude model job skipped.',
    }
    save('github-actions-baseline.json', run)
save('release-state.json', release)
live = json.loads((out/'real-operations-summary.json').read_text(encoding='utf-8'))
live['github_actions']['workflow_merged'] = True
live['github_actions']['workflow_merge_commit'] = pr['mergeCommit']['oid']
if args.run_id:
    live['github_actions']['baseline_workflow'] = release['baseline_workflow']
    live['github_actions']['reason'] = 'Actual baseline workflow passed; paid model review requires the user-managed ANTHROPIC_API_KEY in claude-lab.'
    live['pending'] = ['Paid Actions model job awaits dedicated ANTHROPIC_API_KEY' if x.startswith('Merge/register the manual Actions') else x for x in live['pending']]
save('real-operations-summary.json', live)
print(json.dumps(release, ensure_ascii=True))
