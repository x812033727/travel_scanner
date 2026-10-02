"""Prepare or atomically import a long anime planning package, without starting production.

Preparation needs no database. Database mode is a read-only preflight unless --apply
names the exact prepared bundle hash and an active administrator can be identified.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.video_automation.planning import bundle_hash, import_plan, prepare_bundle, validate_bundle

MAX_INPUT_BYTES = 8 * 1024 * 1024


def read_bundle(source: Path) -> dict[str, Any]:
    if str(source) == "-":
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    else:
        if source.stat().st_size > MAX_INPUT_BYTES:
            raise ValueError("bundle exceeds the 8 MiB input limit")
        raw = source.read_bytes()
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("bundle exceeds the 8 MiB input limit")
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a planning import bundle object")
    return value


async def run_import(args: argparse.Namespace, bundle: dict[str, Any]) -> dict[str, Any]:
    # Delay DB setup until after complete source validation and exact-hash verification.
    from app.config import get_settings
    from app.db import SessionFactory, engine
    from app.news_automation.sources_cli import admin_actor

    digest = bundle_hash(bundle)
    if args.apply and args.expected_sha256 != digest:
        raise ValueError("--apply requires the exact --expected-sha256 from this bundle's dry run")
    try:
        async with SessionFactory() as session:
            if not args.apply and session.get_bind().dialect.name == "postgresql":
                await session.execute(text("SET TRANSACTION READ ONLY"))
            actor = None
            if args.apply:
                email = args.actor_email
                if not email:
                    emails = sorted(get_settings().admin_email_set)
                    if len(emails) != 1:
                        raise ValueError(
                            "select one configured active administrator with --actor-email"
                        )
                    email = emails[0]
                actor = await admin_actor(session, email)
                if actor is None:
                    raise ValueError("an active administrator is required")
            result = await import_plan(session, bundle, actor=actor)
            if args.apply:
                await session.commit()
            else:
                await session.rollback()
            return {"applied": args.apply, **result}
    finally:
        await engine.dispose()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pack", type=Path, help="verified authored source directory")
    source.add_argument("--input", type=Path, help="prepared bundle; '-' reads stdin")
    parser.add_argument(
        "--prepare", type=Path, help="prepare only; '-' writes the bundle to stdout"
    )
    parser.add_argument("--apply", action="store_true", help="apply the preflighted bundle")
    parser.add_argument("--expected-sha256", help="exact bundle hash returned by the dry run")
    parser.add_argument(
        "--actor-email", help="configured administrator; omit when exactly one exists"
    )
    args = parser.parse_args(argv)
    if args.prepare and args.apply:
        parser.error("--prepare cannot be combined with --apply")
    if args.expected_sha256 and not args.apply:
        parser.error("--expected-sha256 is only used with --apply")
    try:
        bundle = prepare_bundle(args.pack) if args.pack else read_bundle(args.input)
        validate_bundle(bundle)
        digest = bundle_hash(bundle)
        if args.prepare:
            encoded = json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
            report = {"prepared": True, "sha256": digest, "ready_for_production": False}
            if str(args.prepare) == "-":
                sys.stdout.write(encoded)
                print(json.dumps(report), file=sys.stderr)
            else:
                args.prepare.write_text(encoded, encoding="utf-8")
                print(json.dumps(report))
        else:
            if args.apply and args.expected_sha256 != digest:
                raise ValueError(
                    "--apply requires the exact --expected-sha256 from this bundle's dry run"
                )
            print(json.dumps(asyncio.run(run_import(args, bundle)), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Planning import refused: {error}\n")
    except SQLAlchemyError:
        # SQL driver exceptions may contain connection details or statement parameters.
        parser.exit(
            1,
            "Planning import failed; verify database access and planning migrations. "
            "No success was reported.\n",
        )


if __name__ == "__main__":
    main()
