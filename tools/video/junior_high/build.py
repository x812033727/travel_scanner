"""Render the six-season junior-high course using shared audio and explicit artwork."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from junior_high.shared import audio, build as shared_build
from junior_high.profile import renderer_for


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Measured lessons.resolved.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--episode")
    parser.add_argument("--start-episode", type=int)
    parser.add_argument("--end-episode", type=int)
    parser.add_argument("--skip-valid", action="store_true")
    parser.add_argument("--no-player", action="store_true")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--mux-only", action="store_true")
    parser.add_argument("--player-only", action="store_true")
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    if output == repository or repository in output.parents:
        parser.error("Media output must be outside the public repository")
    if args.fps < 1 or args.fps > 30 or 30 % args.fps:
        parser.error("Render fps must be a positive divisor of 30")
    resolved = audio.read_json(args.source)
    selected = audio.select_episodes(resolved, args.start_episode, args.end_episode)
    if not args.player_only:
        for episode in selected["episodes"]:
            if args.episode and episode["id"] != args.episode:
                continue
            if args.skip_valid and shared_build.valid_final(episode, output, args.fps, renderer_profile=renderer_for(episode)):
                print(f"SKIP {episode['id']}: junior-high source, renderer and media match", flush=True)
                continue
            audio.audio_integrity(episode, output)
            if not args.mux_only:
                shared_build.render(episode, output, args.fps, renderer_profile=renderer_for(episode))
            shared_build.mux(episode, output, args.fps, renderer_profile=renderer_for(episode))
    if not args.no_player:
        from junior_high.player import write_player
        write_player(resolved, output)
    print(f"Preview: {output / 'index.html'}", flush=True)


if __name__ == "__main__":
    main()
