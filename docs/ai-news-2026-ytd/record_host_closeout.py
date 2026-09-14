"""Read-only host proof after the owned publication hold has been cleared."""
import datetime
import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path

target = os.environ['NEWS_RELEASE_SHA']
assert re.fullmatch('[0-9a-f]{40}', target)
base = Path('/root/mokaair-release-ai-news-ytd-' + target[:8])
state = json.loads((base / 'state.json').read_text())
qa = state['publication_qa_completed']
assert state['target'] == qa['release_sha'] == target and qa['all_passed'] is True
assert not Path('/root/travel-scanner-deploy.hold').exists()
services = {}
for name in ['api', 'web']:
    container = json.loads(subprocess.check_output(['docker', 'inspect', f'travel_scanner-{name}-1'], text=True))[0]
    assert container['Image'] == state[name + '_image'] and container['State']['Running']
    services[name] = {'image': container['Image'], 'running': True}
checks = []
for url in ['http://127.0.0.1:8090/health', 'http://127.0.0.1:8090/ready', 'http://127.0.0.1:8091/zh-TW']:
    with urllib.request.urlopen(url, timeout=20) as response:
        assert response.status == 200
        result = {'url': url, 'status': response.status}
        if url.endswith('/ready'):
            result['body'] = json.load(response)
            assert result['body'] == {'status': 'ready', 'database': 'ok', 'redis': 'ok', 'schema': '0074_lifestyle_guides'}
        checks.append(result)
receipt = {'release_sha': target, 'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'owned_hold_cleared': True, 'public_qa': qa, 'services': services, 'health_checks': checks}
(base / 'closeout.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
