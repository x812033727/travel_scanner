"""``python -m app.guides.pack_cli``: the content-pack production commands.

Kept out of ``app/cli.py`` so this module's scope does not collide with unrelated CLI work on
the task board; ``guides-import`` (the deploy-time import) stays there.

    uv run python -m app.guides.pack_cli ingest --from <workdir> --slug <slug> \\
        [--dry-run] [--no-render]
    uv run python -m app.guides.pack_cli lint [--kind life] [--slug s]... \\
        [--render-dir <dir>] [--catalogue <md>]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import cast

import httpx

from app.guides.content_pack import default_directory
from app.guides.pack_ingest import (
    PackIngestError,
    Problem,
    errors,
    ingest,
    lint_all,
    render_svg,
)
from app.guides.schemas import Kind


def default_public_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "web" / "public"


def _print(problems: list[Problem], prefix: str = "") -> None:
    for problem in problems:
        print(f"{prefix}{problem}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pack_cli", description=__doc__.split("\n")[0])
    parser.add_argument("--content-dir", type=Path, default=None)
    parser.add_argument("--public-dir", type=Path, default=None)
    commands = parser.add_subparsers(dest="command", required=True)

    ingest_parser = commands.add_parser("ingest", help="Build one pack from a writing workspace")
    ingest_parser.add_argument("--from", dest="workdir", type=Path, required=True)
    ingest_parser.add_argument("--slug", required=True)
    ingest_parser.add_argument("--dry-run", action="store_true", help="Check, write nothing")
    ingest_parser.add_argument(
        "--no-render", action="store_true", help="Refuse a hero.svg instead of rendering it"
    )

    lint_parser = commands.add_parser("lint", help="Run the editorial rules over shipped packs")
    lint_parser.add_argument("--kind", choices=("intel", "howto", "life"))
    lint_parser.add_argument("--slug", action="append")
    lint_parser.add_argument("--render-dir", type=Path, help="Render every SVG to PNG here")
    lint_parser.add_argument("--catalogue", type=Path, help="A series list to compare against")
    lint_parser.add_argument(
        "--warnings", action="store_true", help="Exit 1 on warnings too, not only errors"
    )

    args = parser.parse_args(argv)
    content_dir = args.content_dir or default_directory()
    public_dir = args.public_dir or default_public_dir()

    if args.command == "ingest":
        try:
            with httpx.Client(timeout=60, follow_redirects=True) as client:
                report = ingest(
                    args.workdir,
                    args.slug,
                    content_dir=content_dir,
                    public_dir=public_dir,
                    client=client,
                    renderer=None if args.no_render else render_svg,
                    dry_run=args.dry_run,
                )
        except PackIngestError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        _print(report.problems)
        for path in report.written:
            print(f"wrote {path}")
        if report.ok and args.dry_run:
            print("dry run: nothing written")
        return 0 if report.ok else 1

    findings = lint_all(
        content_dir,
        public_dir,
        kind=cast(Kind | None, args.kind),
        slugs=set(args.slug) if args.slug else None,
        render_dir=args.render_dir,
        catalogue=args.catalogue,
    )
    failed = False
    for slug, problems in findings.items():
        if problems:
            print(slug)
            _print(problems, "  ")
        if errors(problems) or (args.warnings and problems):
            failed = True
    print(f"{len(findings)} entries checked")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
