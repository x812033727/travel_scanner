#!/usr/bin/env python3
"""Render ready elementary episodes with bounded workers, watching one audio producer.

Run the shared preschool/audio.py separately. Only source-matching, integrity-
checked audio can enter the queue. This command never synthesizes or publishes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from elementary.profile import RENDERER
from elementary.shared import audio, build


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Complete authoring lessons.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--fps', type=int, default=15)
    parser.add_argument('--watch-audio', action='store_true', help='Wait for the separately running audio producer')
    parser.add_argument('--wait-timeout', type=float, default=1800, help='Maximum seconds without a ready audio episode')
    args = parser.parse_args()
    if not 1 <= args.workers <= 8 or args.wait_timeout <= 0:
        parser.error('workers must be 1–8 and wait-timeout must be positive')
    output = args.output.resolve()
    repo = Path(__file__).resolve().parents[3]
    if output == repo or repo in output.parents:
        parser.error('Media output must be outside the public repository')
    source = audio.load_source(args.source.resolve(), None)
    expected = {e['id']: e for e in source['episodes']}
    pending = set(expected)
    complete, failed, active = set(), {}, {}
    logs = output / 'build-logs'
    logs.mkdir(parents=True, exist_ok=True)
    idle_since = time.monotonic()
    last_notice = 0.0
    failure = None
    try:
        while pending or active:
            for eid, (process, stream) in list(active.items()):
                code = process.poll()
                if code is None:
                    continue
                stream.close()
                del active[eid]
                if code:
                    failed[eid] = f'build exit {code}; see build-logs/{eid}.log'
                else:
                    complete.add(eid)
                    print(f'READY {eid} ({len(complete)}/{len(expected)})', flush=True)
            if failed:
                raise RuntimeError(json.dumps(failed))
            doc = audio.read_json(output / 'lessons.resolved.json')
            measured = {e['id']: e for e in doc.get('episodes', [])}
            manifest = audio.read_json(output / 'audio-manifest.json')
            records = {e['id']: e for e in manifest.get('episodes', [])}
            scheduled = False
            for eid in sorted(pending):
                if len(active) >= args.workers:
                    break
                episode = measured.get(eid)
                if (not episode or not audio.source_matches(expected[eid], episode)
                        or not audio.episode_audio_ready(episode, output, records.get(eid))):
                    continue
                pending.remove(eid)
                scheduled = True
                if build.valid_final(episode, output, args.fps, renderer_profile=RENDERER):
                    complete.add(eid)
                    print(f'SKIP {eid}: validated current media', flush=True)
                    continue
                stream = (logs / f'{eid}.log').open('w', encoding='utf-8')
                command = [sys.executable, str(Path(__file__).with_name('build.py')),
                           '--source', str(output / 'lessons.resolved.json'), '--output', str(output),
                           '--episode', eid, '--fps', str(args.fps), '--skip-valid', '--no-player']
                try:
                    process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
                except BaseException:
                    stream.close()
                    raise
                active[eid] = (process, stream)
                print(f'START {eid}', flush=True)
            if scheduled or active:
                idle_since = time.monotonic()
            elif pending:
                if not args.watch_audio:
                    raise RuntimeError('Audio is missing or stale for: ' + ', '.join(sorted(pending)))
                if manifest.get('status') == 'failed':
                    raise RuntimeError('Audio producer failed; inspect audio manifest/log before resuming')
                if time.monotonic() - idle_since > args.wait_timeout:
                    raise RuntimeError('Timed out waiting for source-matching audio: ' + ', '.join(sorted(pending)))
            state = {'updated_at': audio.stamp(), 'expected': len(expected),
                     'complete': sorted(complete), 'active': sorted(active),
                     'waiting': sorted(pending), 'failed': failed,
                     'status': 'rendering', 'passed': False}
            audio.atomic_json(output / 'batch-status.json', state)
            if time.monotonic() - last_notice >= 30:
                print(f"PROGRESS {len(complete)}/{len(expected)}; rendering {','.join(sorted(active)) or '-'}; waiting {len(pending)}", flush=True)
                last_notice = time.monotonic()
            if pending or active:
                time.sleep(3)
        from elementary.player import write_player
        write_player(audio.read_json(output / 'lessons.resolved.json'), output)
    except BaseException as error:
        failure = error
        raise
    finally:
        for process, stream in active.values():
            if process.poll() is None:
                process.terminate()
        for process, stream in active.values():
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            stream.close()
        status = 'passed' if failure is None else 'interrupted' if isinstance(failure, KeyboardInterrupt) else 'failed'
        audio.atomic_json(output / 'batch-status.json', {
            'updated_at': audio.stamp(), 'expected': len(expected),
            'complete': sorted(complete), 'active': [],
            'waiting': sorted(set(expected) - complete), 'failed': failed,
            'status': status, 'passed': status == 'passed',
            'error': None if failure is None else f'{type(failure).__name__}: {failure}',
        })
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (audio.PipelineError, OSError, ValueError, RuntimeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        raise SystemExit(1)
