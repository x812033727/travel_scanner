"""Clean a practice CSV without overwriting either the input or an existing output."""
import argparse
import csv
import json
import re
import sys
from pathlib import Path


def clean(source: Path, target: Path) -> dict[str, int]:
    if source.resolve() == target.resolve():
        raise ValueError("Input and output must differ")
    rows = []
    seen = set()
    counts = {"kept": 0, "duplicate": 0, "invalid": 0}
    with source.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if reader.fieldnames != ["name", "email"]:
            raise ValueError("Expected exactly: name,email")
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("Malformed CSV row")
            name = row["name"].strip()
            email = row["email"].strip().lower()
            # An exercise-level shape check, not proof an address can receive mail.
            if not name or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                counts["invalid"] += 1
            elif email in seen:
                counts["duplicate"] += 1
            else:
                seen.add(email)
                rows.append({"name": name, "email": email})
                counts["kept"] += 1
    # Exclusive creation: a rerun never silently replaces an existing result.
    with target.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["name", "email"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        counts = clean(args.source, args.target)
    except (OSError, ValueError, csv.Error) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(counts), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
