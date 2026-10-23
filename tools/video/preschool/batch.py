#!/usr/bin/env python3
"""Resume a preschool media batch with one speech producer and bounded render workers.

The speech producer uses at most two network requests. Render workers consume
atomically published measured episodes as soon as their audio is complete.
All children are supervised and reaped; failures produce a nonzero exit status.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

from audio import (PipelineError, atomic_json, episode_audio_ready, load_source,
                   read_json, select_episodes, source_matches, stamp)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="unresolved lessons.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--start-episode", type=int)
    parser.add_argument("--end-episode", type=int)
    parser.add_argument("--episode")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--render-only", action="store_true", help="use existing complete audio; do not start a speech producer")
    parser.add_argument("--watch-audio", action="store_true", help="consume audio from an already running external producer until its manifest is ready or failed")
    parser.add_argument("--no-player", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.workers <= 3:
        raise PipelineError("Workers must be between 1 and 3.")
    if args.fps < 1 or args.fps > 30 or 30 % args.fps:
        raise PipelineError("Render fps must be a positive divisor of 30.")
    source_path = args.source.resolve()
    source = select_episodes(load_source(source_path, args.episode), args.start_episode, args.end_episode)
    expected = {episode["id"]: episode for episode in source["episodes"]}
    output = args.output.resolve()
    repo = Path(__file__).resolve().parents[3]
    if output == repo or repo in output.parents:
        raise PipelineError("Media output must be outside the public repository.")
    output.mkdir(parents=True, exist_ok=True)
    logs = output / "build-logs"
    logs.mkdir(exist_ok=True)
    directory = Path(__file__).resolve().parent
    selected_args = []
    for name, value in (("--start-episode", args.start_episode), ("--end-episode", args.end_episode), ("--episode", args.episode)):
        if value is not None:
            selected_args += [name, str(value)]
    children = []
    handles = []
    running = {}
    finished = []
    failed = {}
    missing = []
    audio = None
    started = stamp()
    interrupted = False
    failure = None
    external_status = None

    def spawn(command, logfile):
        handle = logfile.open("a", encoding="utf-8")
        handle.write(f"\n=== Started {stamp()} ===\n")
        handle.flush()
        handles.append(handle)
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT)
        children.append(process)
        return process

    def report(status):
        atomic_json(output / "batch-status.json", {
            "started_at": started, "updated_at": stamp(), "status": status,
            "requested": list(expected), "completed": finished, "failed": failed,
            "missing_audio": missing, "rendering": list(running),
            "audio_exit_code": audio.poll() if audio else None,
            "external_audio_status": external_status,
            "workers": args.workers, "source": str(source_path),
            "logs": str(logs), "error": failure,
        })

    try:
        if not args.render_only and not args.watch_audio:
            command = [sys.executable, str(directory / "audio.py"), "--source", str(source_path),
                       "--output", str(output), *selected_args]
            if args.cache_dir:
                command += ["--cache-dir", str(args.cache_dir.resolve())]
            audio = spawn(command, logs / "audio.log")
            print("BATCH speech producer started (maximum 2 network requests)", flush=True)
        last_progress = 0.0
        while True:
            for eid, process in list(running.items()):
                code = process.poll()
                if code is None:
                    continue
                del running[eid]
                if code == 0:
                    finished.append(eid)
                    print(f"BATCH ready {eid} ({len(finished)}/{len(expected)})", flush=True)
                else:
                    failed[eid] = {"exit_code": code, "log": str(logs / f"{eid}.log")}
                    print(f"BATCH ERROR {eid}: exit {code}; see {logs / f'{eid}.log'}", flush=True)
            measured = {episode["id"]: episode for episode in read_json(output / "lessons.resolved.json").get("episodes", [])}
            audio_manifest = read_json(output / "audio-manifest.json")
            external_status = audio_manifest.get("status") if args.watch_audio else None
            if args.watch_audio and external_status not in {"building", "ready", "failed"}:
                raise PipelineError("Start the external audio producer before --watch-audio; no active audio manifest was found.")
            records = {episode["id"]: episode for episode in audio_manifest.get("episodes", [])}
            ready = []
            for eid, lesson in expected.items():
                if eid in running or eid in finished or eid in failed:
                    continue
                episode = measured.get(eid)
                record = records.get(eid)
                if episode and record and source_matches(lesson, episode) and episode_audio_ready(episode, output, record):
                    ready.append(eid)
            while ready and len(running) < args.workers:
                eid = ready.pop(0)
                command = [sys.executable, str(directory / "build.py"), "--source", str(output / "lessons.resolved.json"),
                           "--output", str(output), "--episode", eid, "--fps", str(args.fps), "--skip-valid", "--no-player"]
                running[eid] = spawn(command, logs / f"{eid}.log")
                print(f"BATCH render {eid}", flush=True)
            producer_done = external_status != "building" if args.watch_audio else audio is None or audio.poll() is not None
            if producer_done and not running and not ready:
                missing = [eid for eid in expected if eid not in finished and eid not in failed]
                break
            report("building")
            if time.monotonic() - last_progress >= 30:
                print(f"BATCH {len(finished)}/{len(expected)} complete; rendering {', '.join(running) or 'waiting for audio'}", flush=True)
                last_progress = time.monotonic()
            time.sleep(3)
        audio_failed = (audio is not None and audio.returncode != 0) or external_status == "failed"
        if failed or missing or audio_failed:
            failure = "One or more episodes failed or did not receive matching complete audio. Re-run this command to resume."
            report("failed")
            print(f"BATCH ERROR: {len(failed)} render failures, {len(missing)} missing audio; audio exit {audio.returncode if audio else 'not run'}. See {logs}", flush=True)
            return 1
        if not args.no_player:
            player = spawn([sys.executable, str(directory / "build.py"), "--source", str(output / "lessons.resolved.json"),
                            "--output", str(output), "--player-only"], logs / "player.log")
            if player.wait() != 0:
                failure = "Player generation failed; completed media is preserved. See build-logs/player.log."
                report("failed")
                print(f"BATCH ERROR: {failure}", flush=True)
                return 1
        report("ready")
        print(f"BATCH READY: {len(finished)} episodes; {output / 'batch-status.json'}", flush=True)
        return 0
    except KeyboardInterrupt:
        interrupted = True
        failure = "Interrupted; cached speech, scenes, and completed episodes remain resumable."
        print(f"BATCH {failure}", file=sys.stderr, flush=True)
        return 130
    except Exception as error:
        failure = type(error).__name__
        raise
    finally:
        for process in children:
            if process.poll() is None:
                process.terminate()
        for process in children:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        for handle in handles:
            handle.close()
        if interrupted or failure:
            report("interrupted" if interrupted else "failed")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PipelineError as error:
        print(f"BATCH ERROR: {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
