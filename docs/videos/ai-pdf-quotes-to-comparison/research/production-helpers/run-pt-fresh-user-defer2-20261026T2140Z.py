"""ONE normal PT unit, only after root's fresh explicit GO_PAID and committed grant.

This wrapper never resets native state, sends owner actions or starts a follow-up unit.
The unchanged language adapter owns every actual paid request and review boundary.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

HOME = Path('/workspace/work/ai-pdf-01')
ROOT = Path('/workspace/travel_scanner_pdf')
WORK = HOME / 'media/ai-pdf-quotes-to-comparison'
DOC = ROOT / 'docs/videos/ai-pdf-quotes-to-comparison'
ORIGINAL = Path('/workspace/work/ai-animation-01/media/ai-editable-explainer-animation')
PREFIX = HOME / 'pt-fresh-user-defer2-20261026T2140Z'
LOCALES = ['en', 'ja', 'ko', 'es', 'pt', 'id', 'vi', 'th']
PRIMARY = '346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(file):
    return json.loads(file.read_text())

def sha(file):
    h = hashlib.sha256()
    with file.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def save(suffix, value):
    with Path(str(PREFIX) + suffix).open('x') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')

def age(value):
    stamp = datetime.datetime.fromisoformat(value.replace('Z', '+00:00').replace(' UTC', '+00:00'))
    return (datetime.datetime.now(datetime.timezone.utc) - stamp).total_seconds()

def runtime():
    return {str(p.relative_to(WORK)): sha(p) for p in sorted(WORK.rglob('*')) if p.is_file() and p.relative_to(WORK).as_posix() != 'LEASE'}

def sources():
    return {str(p.relative_to(DOC)): sha(p) for p in [DOC / 'video.json', *(DOC / 'i18n').glob('*.json')]}

def raw(locale):
    return {p.name: sha(p) for p in sorted((WORK / 'dubs' / locale / 'audio').glob('*.wav'))}

def actual_producers():
    found = []
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit() or int(proc.name) == os.getpid():
            continue
        try:
            args = [a for a in (proc / 'cmdline').read_bytes().decode().split('\0') if a]
            executable = Path(args[0]).name if args else ''
            if (executable == 'node' or executable.startswith('python')) and any('ai-pdf-01' in a or 'ai-animation-01' in a or 'whisper_second_opinion' in a for a in args[1:]):
                found.append({'pid': int(proc.name), 'executable': executable, 'arguments': args[1:]})
        except (OSError, UnicodeError):
            pass
    return found

parser = argparse.ArgumentParser()
parser.add_argument('--execute', action='store_true', required=True)
parser.add_argument('--grant-file', type=Path, required=True)
parser.add_argument('--grant-sha256', required=True)
parser.add_argument('--source-commit', required=True)
parser.add_argument('--original-task-file', type=Path, required=True)
args = parser.parse_args()

assert len(args.grant_sha256) == 64 and sha(args.grant_file) == args.grant_sha256
grant = read(args.grant_file)
assert grant['slug'] == 'ai-pdf-quotes-to-comparison'
assert grant['coordinator'] == '/root/pdf_pt_resume_2136'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == args.source_commit
assert subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip() == ''
assert not actual_producers(), 'A real producer/Whisper process already exists'
for base in [WORK, ORIGINAL, WORK.parent, ORIGINAL.parent, HOME, ORIGINAL.parent.parent]:
    assert not (base / 'LEASE').exists() and not (base / 'STOP').exists(), f'Ownership/STOP not clear at {base}'
guard = read(args.original_task_file)
assert guard['owner'] == 'codex-ai-video' and age(guard['latest_checkpoint']) > 7200 and 0 <= age(guard['observed_at_utc']) < 600
pre_file = Path(str(PREFIX) + '-free-preflight.json')
pre = read(pre_file)
assert pre['actual_dry_run_exit'] == 0 and pre['project_runtime_byte_exact'] and pre['source9_byte_exact']
assert 0 <= age(pre['observed_at_utc']) < 600, 'Real primary/original GET and native budget preflight stale'
assert pre['original_final']['status'] == 'approved' and pre['original_retries'] == {} and pre['PDF_retries'] == {}
assert pre['PDF_final']['sha256'] == PRIMARY and pre['matching_QA11'] and pre['monthly_characters_remaining_at_read'] >= pre['estimated_billable_characters']
assert sha(Path(str(PREFIX) + '-dry-run.log')) == pre['dry_run_log_sha256']
free_before = read(Path(str(PREFIX) + '-before-free.json'))
all_before = runtime()
assert all_before == free_before['runtime_files'], 'Runtime changed since the qualified free preflight'
source_before = sources()
assert source_before == free_before['source_files']
state = read(WORK / 'auto.json')
assert state['status'] == 'done' and state.get('defer_count') == 2 and state.get('deferred_until') == '2026-10-26T21:05:02.168Z'
assert age(state['deferred_until']) >= 0
assert state['languages']['pt'] == {'shorten': 0, 'retakes': 0, 'reword': 0, 'check_stopped': True}
assert state['languages']['en'] == {'shorten': 1, 'retakes': 2, 'reword': 2, 'check_stopped': True}
assert state['languages']['ja'] == {'shorten': 0, 'retakes': 2, 'reword': 2, 'check_stopped': True}
assert not [p for p in WORK.rglob('*') if p.is_file() and '/speech-journal/' in str(p)]
assert not [p for p in (WORK / 'run-receipts').glob('*.json') if not read(p).get('adopted')]
assert sha(WORK / 'final.mp4') == PRIMARY
qa = read(WORK / 'review/qa.json')
assert qa['ok'] and qa['final_sha256'] == PRIMARY and len(qa['items']) == 11 and all(r['ok'] for r in qa['items'])
index_hashes = {}
for locale in LOCALES:
    idx_file = DOC / f'research/translation-reviews/{locale}.meaning-review.json'
    idx = read(idx_file)
    assert idx['passed'] and idx['source_video_sha256'] == source_before['video.json'] and idx['translation_sha256'] == source_before[f'i18n/{locale}.json']
    assert sha(DOC / idx['report_file']) == idx['report_sha256']
    index_hashes[locale] = sha(idx_file)
    for boundary in (HOME / 'author-review-boundaries').glob(f'{locale}.*.round-[12].*.json'):
        assert any(r['file'] == str(boundary.relative_to(HOME)) and r['sha256'] == sha(boundary) for r in idx.get('reviewed_boundaries', []))
assert not raw('pt') and not (WORK / 'dubs/pt.m4a').exists() and not (WORK / 'dubs/pt/skipped.json').exists()
protected_names = ['final.mp4', 'narration.wav', 'timeline.json', 'checks.json', 'approvals.json', 'languages.json', 'review/qa.json', 'frames/manifest.json']
for locale in ['en', 'ja', 'ko', 'es']:
    protected_names += [f'review/check.{locale}.json', f'review/check-flags.{locale}.json', f'dubs/{locale}.m4a', f'dubs/{locale}/fit.json', f'dubs/{locale}/timeline.json']
protected_names += [f'thumbnails/{locale}.jpg' for locale in LOCALES]
protected = {p: sha(WORK / p) for p in protected_names}
protected_raw = {locale: raw(locale) for locale in ['en', 'ja', 'ko', 'es']}
activation_file = Path('/workspace/work/video-asr-runtime/native-second-asr-environment.compatible.json')
activation = read(activation_file)
assert set(activation) == {'HF_HOME', 'HF_HUB_CACHE', 'HF_HUB_DISABLE_IMPLICIT_TOKEN', 'HF_HUB_OFFLINE', 'HF_HUB_DISABLE_TELEMETRY', 'WHISPER_MODEL', 'VIDEO_SECOND_OPINION'} and activation['WHISPER_MODEL'] == 'medium'
save('-admission.json', {'recorded_at_utc': now(), 'authorization': 'Fresh root explicit GO_PAID for ONE ordinary PT unit after actual nonpaid preflight; no future unit or service/billing cure asserted.', 'grant_file': str(args.grant_file), 'grant_sha256': args.grant_sha256, 'source_commit': args.source_commit, 'original_task_file': str(args.original_task_file), 'original_task_sha256': sha(args.original_task_file), 'free_preflight_sha256': sha(pre_file), 'preserved_defer_count': 2, 'preserved_due': state['deferred_until'], 'one_actual_unit_only': True, 'helper_sha256': sha(Path(__file__))})
save('-before.json', {'recorded_at_utc': now(), 'runtime_files': all_before, 'source_hashes': source_before, 'meaning_index_hashes': index_hashes, 'protected_hashes': protected, 'protected_raw_wav_hashes': protected_raw, 'native_before': state, 'grant_sha256': args.grant_sha256})
env = os.environ.copy()
env.update(activation)
command = ['node', '--use-env-proxy', str(HOME / 'languages.mjs'), '--execute', 'dub-reviewed', 'pt']
with Path(str(PREFIX) + '.log').open('x') as log:
    child = subprocess.Popen(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    save('-started.json', {'started_at_utc': now(), 'driver_pid': os.getpid(), 'native_pid': child.pid, 'command': command, 'log': str(PREFIX) + '.log', 'one_actual_unit_only': True})
    print(json.dumps({'driver_pid': os.getpid(), 'native_pid': child.pid, 'prefix': str(PREFIX)}, ensure_ascii=False), flush=True)
    progress_file = Path(str(PREFIX) + '-observed-progress.jsonl')
    while child.poll() is None:
        current = read(WORK / 'auto.json')
        flags_file = WORK / 'review/check-flags.pt.json'
        cache_file = WORK / 'review/check.pt.json'
        cache = read(cache_file) if cache_file.exists() else {}
        with progress_file.open('a') as handle:
            json.dump({'observed_at_utc': now(), 'native_pid': child.pid, 'actual_primary_WAVs': len([p for p in (WORK / 'dubs/pt/audio').glob('*.wav') if p.name.count('.') == 1]), 'actual_saved_primary_ASR': len(cache.get('lines', {})), 'actual_flags': read(flags_file).get('flags') if flags_file.exists() else None, 'native_PT': current.get('languages', {}).get('pt'), 'defer_count': current.get('defer_count'), 'due': current.get('deferred_until'), 'actual_lease_present': (WORK / 'LEASE').exists()}, handle, ensure_ascii=False)
            handle.write('\n')
        time.sleep(10)
    code = child.wait()
ended = now()
after = read(WORK / 'auto.json')
raw_pt = raw('pt')
cache_file = WORK / 'review/check.pt.json'
flags_file = WORK / 'review/check-flags.pt.json'
cache = read(cache_file) if cache_file.exists() else {}
flags = read(flags_file) if flags_file.exists() else None
protected_after = {p: sha(WORK / p) for p in protected_names}
after_runtime = runtime()
source_after = sources()
result = {'ended_at_utc': ended, 'actual_exit_code': code, 'native_pid': child.pid, 'driver_pid': os.getpid(), 'source_hashes_after': source_after, 'source_hashes_before': source_before, 'all_other_source_files_exact': all(source_after[p] == h for p, h in source_before.items() if p != 'i18n/pt.json'), 'meaning_indices_byte_exact': index_hashes == {l: sha(DOC / f'research/translation-reviews/{l}.meaning-review.json') for l in LOCALES}, 'protected_files_byte_exact': protected_after == protected, 'EN_JA_KO_ES_raw_wavs_byte_exact': protected_raw == {l: raw(l) for l in protected_raw}, 'EN_JA_native_counters_byte_exact': all(after.get('languages', {}).get(l) == state['languages'][l] for l in ['en', 'ja']), 'PT_primary_WAV_count': sum(name.count('.') == 1 for name in raw_pt), 'PT_raw_wav_hashes': raw_pt, 'PT_saved_primary_check_count': len(cache.get('lines', {})), 'PT_current_raw_matched_primary_check_count': sum(r.get('clip') == raw_pt.get(f'{i}.wav', '')[:16] for i, r in cache.get('lines', {}).items()), 'PT_current_flags': flags.get('flags') if flags else None, 'PT_native_after': after.get('languages', {}).get('pt'), 'native_status_after': after.get('status'), 'defer_count_before': state.get('defer_count'), 'defer_count_after': after.get('defer_count'), 'due_before': state.get('deferred_until'), 'due_after': after.get('deferred_until'), 'LEASE_STOP_absent': not (WORK / 'LEASE').exists() and not (WORK / 'STOP').exists(), 'runtime_changed_paths': sorted(p for p, h in after_runtime.items() if all_before.get(p) != h), 'runtime_deleted_paths': sorted(p for p in all_before if p not in after_runtime), 'actual_boundary_files': [str(p) for p in sorted((HOME / 'author-review-boundaries').glob('pt.*.round-[12].*.json'))], 'log_sha256': sha(Path(str(PREFIX) + '.log')), 'no_next_unit_started': True, 'voice_ready_not_inferred_from_exit_or_physical_track': True, 'owner_or_publication_actions': False}
save('-actual-outcome.json', result)
print(json.dumps({k: v for k, v in result.items() if k not in ['PT_raw_wav_hashes', 'source_hashes_before', 'source_hashes_after', 'runtime_changed_paths']}, ensure_ascii=False, indent=2), flush=True)
assert result['protected_files_byte_exact'] and result['EN_JA_KO_ES_raw_wavs_byte_exact'] and result['EN_JA_native_counters_byte_exact'] and result['all_other_source_files_exact'] and result['meaning_indices_byte_exact'], 'Protected state changed; preserve actual outcome and stop'
sys.exit(code)
