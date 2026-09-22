"""``python -m app.guides.pack_cli``: the content-pack production commands.

Kept out of ``app/cli.py`` so this module's scope does not collide with unrelated CLI work on
the task board; ``guides-import`` (the deploy-time import) stays there.

    uv run python -m app.guides.pack_cli ingest --from <workdir> --slug <slug> \\
        [--dry-run] [--no-render]
    uv run python -m app.guides.pack_cli lint [--kind life] [--slug s]... \\
        [--render-dir <dir>] [--catalogue <md>]
    uv run python -m app.guides.pack_cli retopic [--kind life] [--prefix p]... [--slug s]... \\
        [--apply]
    uv run python -m app.guides.pack_cli relink [--kind k] [--prefix p]... [--slug s]... [--apply]
    uv run python -m app.guides.pack_cli autolink [--kind k] [--prefix p]... [--slug s]... \\
        [--limit 8] [--apply]
    uv run python -m app.guides.pack_cli summarize [--kind k] [--prefix p]... [--slug s]... \\
        [--from batch.json] [--replace] [--digest out.md] [--apply]
    uv run python -m app.guides.pack_cli jev-review editorial [--slug s]... [--kind k]... \\
        [--dir <content>] [--report out.json] [--max-calls 50] [--dry-run]
    uv run python -m app.guides.pack_cli jev-review overlap --proposal p.json | --draft pack.json \\
        [--kind k]... [--topic t]... [--chunk-size 80] [--no-final-round] [--dry-run]
    uv run python -m app.guides.pack_cli jev-review compare --before b.json --after a.json \\
        [--sample 40] [--seed 1] [--out sample.tsv] [--control slug]...

``jev-review`` reads packs and answers; it never writes one. Run it from ``apps/api`` so that
``JEV_API_KEY`` is read from the repository's own ``.env`` (``Settings`` resolves it relative
to the working directory), and read ``--dry-run`` before spending anything.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Any, cast

from app.config import get_settings
from app.guides import autolink, jev_review, retopic, summarize
from app.guides.content_pack import default_directory
from app.guides.pack_ingest import (
    PackIngestError,
    Problem,
    commons_client,
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


KINDS = ("intel", "howto", "life")


def _add_jev_review(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """The advisory checks. Every one of them can be asked what it would do first."""
    parser = commands.add_parser(
        "jev-review", help="Ask Jev what to look at. Advisory: no pack is ever written"
    )
    checks = parser.add_subparsers(dest="check", required=True)

    editorial = checks.add_parser(
        "editorial", help="One question per text unit: editor's voice or traveller's?"
    )
    editorial.add_argument("--slug", action="append")
    editorial.add_argument("--prefix", action="append", default=[])

    overlap = checks.add_parser(
        "overlap", help="Does a proposal repeat an article the catalogue already has?"
    )
    overlap.add_argument("--proposal", type=Path, help="{title, description, summary?}")
    overlap.add_argument("--draft", type=Path, help="A full pack, read as a proposal")
    overlap.add_argument("--topic", action="append", default=[])
    overlap.add_argument("--chunk-size", type=int, default=jev_review.DEFAULT_CHUNK_SIZE)
    overlap.add_argument(
        "--no-final-round",
        dest="final_round",
        action="store_false",
        help="Skip the round that makes the chunks' probabilities comparable",
    )

    for check in (editorial, overlap):
        check.add_argument("--dir", dest="directory", type=Path, help="A content directory")
        check.add_argument("--kind", action="append", choices=KINDS, default=[])
        check.add_argument("--locale", default="zh-TW")
        check.add_argument("--limit", type=int)
        check.add_argument("--top", type=int, default=jev_review.DEFAULT_TOP)
        check.add_argument("--max-calls", type=int, default=jev_review.DEFAULT_MAX_CALLS)
        check.add_argument(
            "--dry-run", action="store_true", help="Print the plan and send nothing"
        )

    compare = checks.add_parser("compare", help="Two editorial reports, paired. Never connects")
    compare.add_argument("--before", type=Path, required=True)
    compare.add_argument("--after", type=Path, required=True)
    compare.add_argument("--sample", type=int, default=0, help="Rows to draw for hand labelling")
    compare.add_argument("--seed", type=int, default=1)
    compare.add_argument("--out", type=Path, help="Where the sample TSV goes")
    compare.add_argument(
        "--control", action="append", default=[], help="A slug reported apart from the subjects"
    )

    for check in (editorial, overlap, compare):
        check.add_argument("--report", type=Path, help="Write the JSON report here")


def _proposal_of(args: argparse.Namespace, locale: str) -> tuple[jev_review.Proposal, list[str]]:
    if args.proposal and args.draft:
        raise jev_review.JevReviewError("give one of --proposal or --draft, not both")
    if args.draft:
        proposal, kind = jev_review.load_draft(args.draft, locale=locale)
        return proposal, list(args.kind) or list(jev_review.kinds_for_draft(kind))
    if args.proposal:
        return jev_review.load_proposal(args.proposal), list(args.kind)
    raise jev_review.JevReviewError("overlap needs --proposal <p.json> or --draft <pack.json>")


def _jev_review(args: argparse.Namespace, content_dir: Path) -> int:
    settings = get_settings()
    try:
        if args.check == "compare":
            result: dict[str, Any] = jev_review.compare_reports(
                args.before,
                args.after,
                sample=args.sample,
                seed=args.seed,
                out=args.out,
                control=tuple(args.control),
            )
            print(jev_review.render_compare(result))
            _write_report(args.report, result)
            return 0
        directory = args.directory or content_dir
        if args.check == "editorial":
            report = asyncio.run(
                jev_review.editorial_report(
                    settings=settings,
                    content_dir=directory,
                    locale=args.locale,
                    kinds=tuple(args.kind),
                    slugs=set(args.slug) if args.slug else None,
                    prefixes=tuple(args.prefix),
                    limit=args.limit,
                    dry_run=args.dry_run,
                    max_calls=args.max_calls,
                )
            )
            print(jev_review.render_editorial(report, top=args.top))
        else:
            proposal, kinds = _proposal_of(args, args.locale)
            report = asyncio.run(
                jev_review.overlap_report(
                    settings=settings,
                    proposal=proposal,
                    content_dir=directory,
                    kinds=tuple(kinds),
                    topics=tuple(args.topic),
                    locale=args.locale,
                    chunk_size=args.chunk_size,
                    limit=args.limit,
                    top=args.top,
                    final_round=args.final_round,
                    dry_run=args.dry_run,
                    max_calls=args.max_calls,
                )
            )
            print(jev_review.render_overlap(report))
    except jev_review.JevReviewError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    _write_report(args.report, report)
    # Flags are advice, so they never fail the run. A provider that could not be reached did.
    return 1 if report["errors"] else 0


def _write_report(path: Path | None, report: dict[str, Any]) -> None:
    if path is None:
        return
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"wrote {path}")


def main(argv: list[str] | None = None) -> int:
    if isinstance(sys.stdout, TextIOWrapper):
        # The reports are Chinese and this is run on Windows, where the console default is
        # cp950 and a Han character raises UnicodeEncodeError on the way out.
        sys.stdout.reconfigure(encoding="utf-8")
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

    retopic_parser = commands.add_parser(
        "retopic", help="Propose two-level topics for packs from their slugs and series"
    )
    retopic_parser.add_argument("--kind", choices=("intel", "howto", "life"), default="life")
    retopic_parser.add_argument("--prefix", action="append", default=[])
    retopic_parser.add_argument("--slug", action="append")
    retopic_parser.add_argument(
        "--apply", action="store_true", help="Rewrite the topics of the changed packs"
    )
    retopic_parser.add_argument("--dry-run", action="store_true", help="The default: print only")

    for name, help_text in (
        ("relink", "Turn raw site URLs to articles into article inlines"),
        ("autolink", "Link the first mention of a glossary term or keyword to its article"),
    ):
        link_parser = commands.add_parser(name, help=help_text)
        link_parser.add_argument("--kind", choices=("intel", "howto", "life"))
        link_parser.add_argument("--prefix", action="append", default=[])
        link_parser.add_argument("--slug", action="append")
        link_parser.add_argument(
            "--apply", action="store_true", help="Rewrite the blocks of the changed packs"
        )
        link_parser.add_argument("--dry-run", action="store_true", help="The default: print only")
        if name == "autolink":
            link_parser.add_argument(
                "--limit", type=int, default=autolink.MAX_AUTOLINKS, help="Links per article"
            )

    summarize_parser = commands.add_parser(
        "summarize", help="Propose or apply summary and FAQ blocks from the article's own text"
    )
    summarize_parser.add_argument("--kind", choices=("intel", "howto", "life"))
    summarize_parser.add_argument("--prefix", action="append", default=[])
    summarize_parser.add_argument("--slug", action="append")
    summarize_parser.add_argument(
        "--from", dest="batch", type=Path, help="A reviewed batch: slug → locale → summary/faq"
    )
    summarize_parser.add_argument(
        "--replace", action="store_true", help="Overwrite a summary or FAQ already there"
    )
    summarize_parser.add_argument(
        "--digest", type=Path, help="Write what a summary is written from, per document, here"
    )
    summarize_parser.add_argument(
        "--apply", action="store_true", help="Rewrite the blocks of the changed packs"
    )
    summarize_parser.add_argument(
        "--dry-run", action="store_true", help="The default: print only"
    )

    _add_jev_review(commands)

    args = parser.parse_args(argv)
    content_dir = args.content_dir or default_directory()
    public_dir = args.public_dir or default_public_dir()

    if args.command == "jev-review":
        return _jev_review(args, content_dir)

    if args.command in {"relink", "autolink"}:
        proposals = autolink.proposals(
            content_dir,
            cast(autolink.Mode, args.command),
            kind=cast(Kind | None, args.kind),
            prefixes=tuple(args.prefix),
            slugs=set(args.slug) if args.slug else None,
            limit=getattr(args, "limit", autolink.MAX_AUTOLINKS),
        )
        print(autolink.render_table(proposals))
        if args.apply and not args.dry_run:
            for path in autolink.apply(proposals, content_dir):
                print(f"wrote {path}")
        else:
            print("dry run: nothing written")
        return 0

    if args.command == "summarize":
        kind = cast(Kind | None, args.kind)
        prefixes = tuple(args.prefix)
        slugs = set(args.slug) if args.slug else None
        try:
            batch = summarize.load_batch(args.batch) if args.batch else None
            summary_rows = summarize.proposals(
                content_dir,
                kind=kind,
                prefixes=prefixes,
                slugs=slugs,
                batch=batch,
                replace=args.replace,
            )
        except summarize.SummarizeError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        if args.digest:
            digest = summarize.render_digest(
                content_dir, kind=kind, prefixes=prefixes, slugs=slugs
            )
            args.digest.write_text(digest, encoding="utf-8")
            print(f"wrote {args.digest}")
        print(summarize.render_table(summary_rows))
        if args.apply and not args.dry_run:
            for path in summarize.apply(summary_rows, content_dir):
                print(f"wrote {path}")
        else:
            print("dry run: nothing written")
        return 0

    if args.command == "retopic":
        rows = retopic.proposals(
            content_dir,
            kind=cast(Kind, args.kind),
            prefixes=tuple(args.prefix),
            slugs=set(args.slug) if args.slug else None,
        )
        print(retopic.render_table(rows))
        if args.apply and not args.dry_run:
            for path in retopic.apply(rows, content_dir):
                print(f"wrote {path}")
        else:
            print("dry run: nothing written")
        return 0

    if args.command == "ingest":
        try:
            with commons_client() as client:
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
        if errors(problems) or (args.warnings and any(p.level != "info" for p in problems)):
            failed = True
    print(f"{len(findings)} entries checked")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
