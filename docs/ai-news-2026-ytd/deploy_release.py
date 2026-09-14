"""Guarded news release; based on the verified existing host release procedure.
Run on the production host with NEWS_RELEASE_SHA and NEWS_PREVIOUS_SHA set explicitly.
The activate phase requires ci.json from the successful exact merged-SHA CI run.
This script does not import or publish articles, edit nginx, or print runtime secrets.
"""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.request

SLUGS = ['ai-news-nvidia-rubin-20260105', 'ai-news-chatgpt-health-20260107', 'ai-news-gemini-personal-intelligence-20260114', 'ai-news-gpt-53-codex-20260205', 'ai-news-claude-opus-46-20260205', 'ai-news-qwen-35-20260216', 'ai-news-gemini-31-pro-20260219', 'ai-news-gpt-54-20260305', 'ai-news-claude-interactive-visuals-20260312', 'ai-news-lyria-3-pro-20260325', 'ai-news-project-glasswing-20260407', 'ai-news-meta-muse-spark-20260408', 'ai-news-chatgpt-images-20-20260421', 'ai-news-gpt-55-20260423', 'ai-news-gemini-omni-20260519', 'ai-news-gemini-spark-20260519', 'ai-news-claude-fable-5-access-20260609', 'ai-news-gpt-56-sol-preview-20260626', 'ai-news-claude-sonnet-5-20260630', 'ai-news-chatgpt-work-20260709', 'ai-news-gemini-36-flash-20260721', 'ai-news-2026-january-september-index']
TARGET = os.environ['NEWS_RELEASE_SHA']
PREVIOUS = os.environ['NEWS_PREVIOUS_SHA']
CONTENT_BASE = os.environ.get('NEWS_CONTENT_BASE_SHA', PREVIOUS)
assert re.fullmatch(r'[0-9a-f]{40}', TARGET) and re.fullmatch(r'[0-9a-f]{40}', PREVIOUS)
assert re.fullmatch(r'[0-9a-f]{40}', CONTENT_BASE)
# The initial reviewed baseline is the current production commit. If main advances,
# record and inspect the exact intervening integrations before adding their pair here.
if CONTENT_BASE != PREVIOUS:
    reviewed_pairs = {
        ('46298e2863e9c2c4d6776e9d58a821be683a4b32', 'fc0c6763875ed7693ef2a94974a06338b6001968'),
        # PR #476: web minor/patch dependency updates; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '673a64b67bc525686dd9959e9b521a0c7662137e'),
        # PR #478: backend lockfile updates; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '5a00f72e7aae229de0f77a51c4d9afdcb967b0cf'),
        ('673a64b67bc525686dd9959e9b521a0c7662137e', '5a00f72e7aae229de0f77a51c4d9afdcb967b0cf'),
        # PR #480: pytest-cov development dependency only; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '05d0b671efddedb75da1c20093cce42f8b2f09ca'),
        # PR #477: Vitest development dependency only; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '769a892bc4e862f9cca73c341adbf13f27a5e563'),
        # PR #479: jsdom development dependency only; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '0b120251a0dcd71af50b3db49eca1dc370569ff0'),
        # PR #482: mypy development update and redundant cast removal; 14 checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', 'afff8db5eea8104f9055f15c04b0825e3df3c6bf'),
        # PR #498: disjoint life content and evidence, no runtime/schema change; 14 checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '8c83e90ab401f05044f614e5843c00d26aaed3dd'),
        # PR #494: three deferred dependency task records only; 14 checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', 'b3f8a241af46259ca5070131452c7dc39a63a7a7'),
        # PR #496: reviewed XML/URL ingestion defenses and regressions; 14 checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '88c23881898fa62f10cdbc59b9a639f5841c8423'),
        # PR #499: disjoint life guides, artwork and task records; 14 checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', 'f2567e51cc1ea0d0c3fc63005db21b2f44e5919c'),
    }
    assert (PREVIOUS, CONTENT_BASE) in reviewed_pairs, 'unreviewed integration baseline'
ROOT = Path('/root/travel_scanner')
BASE = Path('/root/mokaair-release-ai-news-ytd-' + TARGET[:8])
SOURCE = BASE / 'source'
ENV_FILE = ROOT / '.env'
SERVICES = ['api', 'web', 'worker', 'alert-worker', 'alert-scheduler',
            'hotspot-collector', 'analytics-scheduler', 'community-sweeper']
os.umask(0o077)
BASE.mkdir(mode=0o700, exist_ok=True)
locks = []
for path in ['/var/lock/travel-scanner-deploy.lock', '/root/mokaair-deploy.lock',
             '/run/mokaair-manual-deploy.lock', '/run/travel-scanner-deployer/deploy.lock']:
    handle = open(path, 'a+')
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    locks.append(handle)
from release_hold import acquire, verify
phase = sys.argv[1]
if phase == 'prepare':
    acquire(BASE, TARGET)
else:
    verify(BASE, TARGET)
log = open(BASE / (phase + '.log'), 'a', buffering=1)

def say(message):
    line = datetime.datetime.now(datetime.timezone.utc).isoformat() + ' ' + message
    print(line, flush=True)
    print(line, file=log)

def run(args, *, capture=False, env=None, cwd=None, timeout=1800, stdin=None):
    result = subprocess.run(args, cwd=cwd, env=env, stdin=stdin,
                            stdout=subprocess.PIPE if capture else log,
                            stderr=log, timeout=timeout, text=capture)
    if result.returncode:
        raise RuntimeError(f'{args[0]} {args[1]} failed with exit {result.returncode}; see private {phase}.log')
    return result.stdout.strip() if capture else None

def git(*args):
    return run(['git', '-C', str(ROOT), *args], capture=True)

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def inspect(name):
    return json.loads(run(['docker', 'inspect', name], capture=True))[0]

def containers():
    result = {}
    for service in SERVICES + ['postgres', 'redis']:
        obj = inspect(f'travel_scanner-{service}-1')
        result[service] = {
            'id': obj['Id'], 'image': obj['Image'], 'status': obj['State']['Status'],
            'restarts': obj['RestartCount'],
            'env_hash': hashlib.sha256(json.dumps(sorted(obj['Config']['Env'])).encode()).hexdigest(),
            'mounts': obj['Mounts'],
        }
    return result

def compose(*args, target=TARGET):
    env = os.environ.copy()
    env.update(RELEASE_SHA=target, RUNTIME_ENV_FILE=str(ENV_FILE))
    return run(['docker', 'compose', '-p', 'travel_scanner', '--env-file', str(ENV_FILE),
                '-f', str(SOURCE / 'docker-compose.prod.yml'), '--profile', 'hotspots', *args], env=env)

def write_state(state):
    (BASE / 'state.json').write_text(json.dumps(state, indent=2))

def database_fingerprint():
    psql = ['docker', 'exec', 'travel_scanner-postgres-1', 'psql', '-U', 'travel',
            '-d', 'travel_scanner', '-X', '-A', '-t', '-v', 'ON_ERROR_STOP=1', '-c']
    inventory = run(psql + ["SELECT table_name || '.' || column_name FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name, ordinal_position"], capture=True)
    tables = ['guide_articles', 'guide_article_locales', 'provider_configs', 'site_pages',
              'travel_hotspots', 'food_merchants', 'trip_plans', 'trip_plan_items', 'usage_accounts']
    fingerprints = {}
    for table in tables:
        assert any(line.startswith(table + '.') for line in inventory.splitlines())
        rows = run(psql + [f'SELECT row_to_json(t)::text FROM {table} AS t ORDER BY row_to_json(t)::text'], capture=True)
        fingerprints[table] = {'rows': len(rows.splitlines()), 'sha256': hashlib.sha256(rows.encode()).hexdigest()}
    return fingerprints

def healthy():
    streak = 0
    for attempt in range(40):
        try:
            for url in ['http://127.0.0.1:8090/health', 'http://127.0.0.1:8090/ready',
                        'http://127.0.0.1:8091/zh-TW']:
                with urllib.request.urlopen(url, timeout=15) as response:
                    assert response.status == 200
                    if url.endswith('/ready'):
                        ready = json.load(response)
                        assert ready == {'status': 'ready', 'database': 'ok', 'redis': 'ok',
                                         'schema': '0074_lifestyle_guides'}
            streak += 1
            say(f'Health checks {streak}/3 passed')
            if streak == 3:
                return
        except Exception:
            streak = 0
        time.sleep(3)
    raise RuntimeError('Health checks did not pass')

if phase == 'prepare':
    assert not (BASE / 'state.json').exists(), 'release state already exists'
    assert git('rev-parse', 'HEAD') == PREVIOUS
    assert not git('status', '--porcelain'), 'host checkout is dirty'
    git('fetch', 'origin', 'main')
    assert git('rev-parse', 'origin/main') == TARGET, 'main moved; refresh CI target'
    assert not git('diff', '--name-only', PREVIOUS, TARGET, '--',
                   'apps/api/migrations', 'docker-compose.prod.yml', '.env.example')
    git('merge-base', '--is-ancestor', PREVIOUS, CONTENT_BASE)
    git('merge-base', '--is-ancestor', CONTENT_BASE, TARGET)
    changed = git('diff', '--name-only', CONTENT_BASE, TARGET).splitlines()
    allowed = ('docs/ai-news-2026-ytd/', 'tasks/open/2026-09-14-ai-news-2026-year-to-date.md', 'tasks/done/2026-09-14-ai-news-2026-year-to-date.md', *[f'apps/api/app/guides/content/{slug}.json' for slug in SLUGS], *[f'apps/web/public/guides/{slug}/' for slug in SLUGS])
    assert changed and all(path.startswith(allowed) for path in changed), changed
    before = containers()
    assert all(value['status'] == 'running' for value in before.values())
    state = {'target': TARGET, 'previous': PREVIOUS, 'content_base': CONTENT_BASE, 'before': before,
             'env_hash': digest(ENV_FILE), 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    SOURCE.mkdir(mode=0o755)
    run(['git', '-C', str(ROOT), 'archive', '--format=tar', '--output', str(BASE / 'source.tar'), TARGET])
    old_umask = os.umask(0o022)
    try:
        run(['tar', '-xf', str(BASE / 'source.tar'), '-C', str(SOURCE)])
    finally:
        os.umask(old_umask)
    assert not (SOURCE / '.env').exists()
    rollback_tag = 'rollback-ai-news-' + TARGET[:8]
    for service, repo in [('api', 'travel-scanner-api'), ('web', 'travel-scanner-web')]:
        run(['docker', 'image', 'tag', before[service]['image'], f'{repo}:{rollback_tag}'])
    state['rollback_tag'] = rollback_tag
    write_state(state)
    compose('config', '--quiet')
    say('Preflight passed; building clean SHA-tagged API and web images while current services stay live')
    compose('build', 'api', 'web')
    for service, repo in [('api', 'travel-scanner-api'), ('web', 'travel-scanner-web')]:
        state[service + '_image'] = inspect(f'{repo}:{TARGET}')['Id']
    run(['docker', 'run', '--rm', '--entrypoint', 'python', f'travel-scanner-api:{TARGET}',
         '-c', "from pathlib import Path; assert Path('/app/app/main.py').is_file(); import json; assert all(Path('/app/app/guides/content', slug+'.json').is_file() for slug in ['ai-news-nvidia-rubin-20260105', 'ai-news-chatgpt-health-20260107', 'ai-news-gemini-personal-intelligence-20260114', 'ai-news-gpt-53-codex-20260205', 'ai-news-claude-opus-46-20260205', 'ai-news-qwen-35-20260216', 'ai-news-gemini-31-pro-20260219', 'ai-news-gpt-54-20260305', 'ai-news-claude-interactive-visuals-20260312', 'ai-news-lyria-3-pro-20260325', 'ai-news-project-glasswing-20260407', 'ai-news-meta-muse-spark-20260408', 'ai-news-chatgpt-images-20-20260421', 'ai-news-gpt-55-20260423', 'ai-news-gemini-omni-20260519', 'ai-news-gemini-spark-20260519', 'ai-news-claude-fable-5-access-20260609', 'ai-news-gpt-56-sol-preview-20260626', 'ai-news-claude-sonnet-5-20260630', 'ai-news-chatgpt-work-20260709', 'ai-news-gemini-36-flash-20260721', 'ai-news-2026-january-september-index'])"])
    state['built_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write_state(state)
    say('BUILD_READY ' + state['api_image'] + ' ' + state['web_image'])
elif phase == 'activate':
    state = json.loads((BASE / 'state.json').read_text())
    assert state.get('built_at') and not state.get('activated_at')
    ci = json.loads((BASE / 'ci.json').read_text())
    assert ci['headSha'] == TARGET and ci['status'] == 'completed' and ci['conclusion'] == 'success'
    assert all(j['conclusion'] == 'success' for j in ci['jobs'])
    git('fetch', 'origin', 'main')
    assert git('rev-parse', 'origin/main') == TARGET, 'main changed before activation'
    assert git('rev-parse', 'HEAD') == PREVIOUS and not git('status', '--porcelain')
    assert digest(ENV_FILE) == state['env_hash'], 'runtime environment changed'
    current = containers()
    assert current == state['before'], 'live containers changed since prepare'
    run(['nginx', '-t'])
    stopped = False
    advanced = False
    try:
        say('CI passed; stopping application writers for a consistent deployment backup')
        stopped = True
        run(['docker', 'stop', '--time', '45', *[f'travel_scanner-{s}-1' for s in SERVICES]])
        dump = BASE / 'predeploy.dump'
        with dump.open('wb') as output:
            result = subprocess.run(['docker', 'exec', 'travel_scanner-postgres-1',
                                     'pg_dump', '-U', 'travel', '-d', 'travel_scanner', '-Fc'],
                                    stdout=output, stderr=log, timeout=600)
        assert result.returncode == 0 and dump.stat().st_size > 0
        with dump.open('rb') as input_file:
            run(['docker', 'exec', '-i', 'travel_scanner-postgres-1', 'pg_restore', '--list'], stdin=input_file)
        state['backup'] = {'path': str(dump), 'bytes': dump.stat().st_size,
                           'sha256': digest(dump), 'mode': oct(dump.stat().st_mode & 0o777), 'index_verified': True}
        write_state(state)
        say('BACKUP_VERIFIED ' + json.dumps(state['backup']))
        state['data_before'] = database_fingerprint()
        compose('run', '--rm', '--no-deps', 'migrate')
        state['data_after_migrate'] = database_fingerprint()
        assert state['data_before'] == state['data_after_migrate'], 'protected data changed during migration'
        write_state(state)
        compose('up', '-d', '--no-build', '--no-deps', *SERVICES)
        healthy()
        old_umask = os.umask(0o022)
        try:
            git('merge', '--ff-only', TARGET)
            advanced = True
        finally:
            os.umask(old_umask)
        after = containers()
        for service in SERVICES:
            expected = state['web_image'] if service == 'web' else state['api_image']
            assert after[service]['image'] == expected and after[service]['status'] == 'running'
            assert after[service]['restarts'] == 0
            assert after[service]['env_hash'] == state['before'][service]['env_hash']
        for service in ['postgres', 'redis']:
            assert after[service] == state['before'][service]
        assert digest(ENV_FILE) == state['env_hash']
        healthy()
        for service, repo in [('api', 'travel-scanner-api'), ('web', 'travel-scanner-web')]:
            run(['docker', 'image', 'tag', state[service + '_image'], f'{repo}:local'])
        state['after'] = after
        state['activated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        state['ci_run'] = ci['url']
        write_state(state)
        say('DEPLOY_SUCCESS ' + TARGET)
    except BaseException as exc:
        say('Deployment failed: ' + str(exc) + '; restoring retained application images')
        if stopped:
            compose('up', '-d', '--no-build', '--no-deps', *SERVICES, target=state['rollback_tag'])
            healthy()
        state['failed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        state['error'] = str(exc)
        state['checkout_advanced'] = advanced
        write_state(state)
        raise
else:
    raise SystemExit('Use prepare or activate')
