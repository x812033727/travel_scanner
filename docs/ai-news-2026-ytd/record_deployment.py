"""Write a public deployment receipt without exporting runtime configuration."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
if HERE.name == 'renders':
    HERE = HERE.parent
state = json.loads((HERE / 'renders/state.json').read_text(encoding='utf-8-sig'))
ci = json.loads((HERE / 'renders/ci.json').read_text(encoding='utf-8-sig'))
pr = json.loads((HERE / 'renders/content-pr.json').read_text(encoding='utf-8-sig'))
assert pr['state'] == 'MERGED' and pr['mergeCommit']['oid'] == state['target']
assert ci['headSha'] == state['target'] and ci['conclusion'] == 'success'
assert ci['status'] == 'completed' and all(j['conclusion'] == 'success' for j in ci['jobs'])
assert state.get('activated_at') and state['data_before'] == state['data_after_migrate']
assert state['backup']['index_verified'] and state['backup']['bytes'] > 0
assert state['backup']['mode'] == '0o600'
services = {}
for name, after in state['after'].items():
    before = state['before'][name]
    assert after['status'] == 'running' and after['env_hash'] == before['env_hash']
    if name in ['postgres', 'redis']:
        assert after == before
    else:
        assert after['restarts'] == 0
        assert after['image'] == state['web_image' if name == 'web' else 'api_image']
    services[name] = {key: after[key] for key in ['image', 'status', 'restarts']}
    services[name]['environment_unchanged'] = True
receipt = {
    'release_sha': state['target'], 'previous_sha': state['previous'],
    'content_base': state['content_base'], 'content_pr': pr['url'],
    'activated_at': state['activated_at'], 'built_at': state['built_at'],
    'ci_run': ci['url'], 'backup': state['backup'], 'services': services,
    'data_before': state['data_before'], 'data_after_migrate': state['data_after_migrate'],
    'protected_data_unchanged_during_deployment': True,
    'postgres_and_redis_preserved': True,
    'scope': 'Release application images; no article import is implied by this deployment receipt.',
    'health_validation': 'Two sets of three consecutive API health/readiness and web HTTP checks during activation.',
}
(HERE / 'deployment.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
print('Verified deployed SHA, CI, backup, services and preservation receipt')
