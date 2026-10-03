"""Turn a CatchTable candidate file into the two importer files: the two-pass fallback.

Since 2026-10 one command imports a candidate file, merchants and platform rows together::

    python -m app.cli import-catchtable-candidates --file <BATCH>/candidates.json [--apply]

This script stays for the two-pass path (``import-trend-merchants`` then
``apply-food-platform-reviews``) and for reproducing the committed batches. It no longer
validates anything itself: the candidate schema, and the conversion into both files, live in
``app.foods.catchtable_import``, so the script and the importer can never disagree. Run it with
the API's Python from ``apps/api`` (``uv run python ../../tools/catchtable_build_batches.py``)::

    catchtable_build_batches.py --candidates <BATCH>/candidates.json --check
    catchtable_build_batches.py --candidates <BATCH>/candidates.json \
        --merchants-out <BATCH>/merchants.json
    # import-trend-merchants --file ... --apply on the host, then export the worklist, then
    catchtable_build_batches.py --candidates <BATCH>/candidates.json --worklist worklist.json \
        --platform-out <BATCH>/platform-reviews.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

API_DIR = Path(__file__).resolve().parents[1] / "apps" / "api"
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from app.foods.catchtable_import import (  # noqa: E402
    CandidateFileError,
    check_summary,
    load_candidate_file,
    merchant_rows,
    platform_document,
)


def load_worklist(path: Path) -> dict[str, str]:
    """slug -> merchant id from ``export-food-merchant-worklist`` output (or any list of rows)."""
    document = json.loads(path.read_text(encoding="utf-8"))
    rows: Any = document
    if isinstance(document, dict):
        for key in ("merchants", "rows", "items"):
            if isinstance(document.get(key), list):
                rows = document[key]
                break
    if not isinstance(rows, list):
        raise CandidateFileError(f"{path}: expected a worklist with a list of merchants")
    ids: dict[str, str] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("slug"), str):
            if isinstance(row.get("id"), str):
                ids[row["slug"]] = row["id"]
    return ids


def _write(path: Path, payload: Any) -> None:
    # newline="\n": the committed files are LF, and Windows would otherwise write CRLF.
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument(
        "--merchants-out", type=Path, help="Write the import-trend-merchants file here"
    )
    parser.add_argument(
        "--platform-out", type=Path, help="Write the apply-food-platform-reviews file here"
    )
    parser.add_argument(
        "--worklist", type=Path, help="export-food-merchant-worklist output, for merchant ids"
    )
    parser.add_argument("--check", action="store_true", help="Validate and summarize only")
    args = parser.parse_args(argv)
    try:
        prepared = load_candidate_file(args.candidates)
    except CandidateFileError as exc:
        for line in str(exc).split(" | "):
            print(f"ERROR {line}", file=sys.stderr)
        return 2
    report = check_summary(prepared)
    if args.merchants_out:
        rows = merchant_rows(prepared.candidates)
        _write(args.merchants_out, rows)
        report["merchants_written"] = len(rows)
    if args.platform_out:
        if not args.worklist:
            print(
                "ERROR --platform-out needs --worklist "
                "(merchant ids come from the exported worklist)",
                file=sys.stderr,
            )
            return 2
        document, missing = platform_document(prepared.candidates, load_worklist(args.worklist))
        _write(args.platform_out, document)
        report["platform_rows_written"] = len(document["records"])
        report["platform_rows_without_merchant"] = missing
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
