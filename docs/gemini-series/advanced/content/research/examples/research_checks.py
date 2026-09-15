"""Local evidence checks. No network, model calls, source editing or media generation."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


def rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def local(root, name):
    root = Path(root).resolve()
    candidate = root / name
    if not name or Path(name).is_absolute() or candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
        raise ValueError("path_outside_exercise")
    if not candidate.is_file():
        raise ValueError("missing_file")
    return candidate


def versions(root, phase="phase2"):
    data = rows(Path(root) / "sources-v1-v2.csv")
    active = [r for r in data if r[phase] == "yes"]
    if len(active) != 6 or {r["source_id"] for r in active} != {f"S0{i}" for i in range(1, 7)}:
        raise ValueError("need_six_unique_active_sources")
    for row in data:
        file = local(root, row["path"])
        if hashlib.sha256(file.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("source_bytes_changed")
    return {"activeSources": 6, "selectedS01": next(r["version"] for r in active if r["source_id"] == "S01"), "sourceBytesMatch": True, "driveSyncTested": False}


def evidence(root):
    root = Path(root)
    data = rows(root / "evidence-matrix.csv")
    if len(data) != 5 or len({r["id"] for r in data}) != 5:
        raise ValueError("need_five_unique_claims")
    for row in data:
        ids = row["source_ids"].split("|")
        quotes = json.loads(row["quotes"])
        status = row["status"]
        if status not in {"supported", "conflict", "unknown"} or not row["judgment"].strip():
            raise ValueError("judgment_required")
        if not isinstance(quotes, dict) or not set(quotes).issubset(ids) or len(ids) != len(set(ids)):
            raise ValueError("invalid_quote_sources")
        if status != "unknown" and (not quotes or set(quotes) != set(ids)):
            raise ValueError("supported_claim_needs_quotes")
        if status == "conflict" and len(ids) < 2:
            raise ValueError("conflict_needs_two_sources")
        for sid in ids:
            if not re.fullmatch(r"E[1-3]", sid):
                raise ValueError("unknown_source")
            source = local(root, f"sources/{sid}.md").read_text(encoding="utf-8")
            if sid in quotes and (not isinstance(quotes[sid], str) or not quotes[sid].strip() or quotes[sid] not in source):
                raise ValueError("fabricated_quote")
    return {"claims": len(data), "quoteStructureValid": True, "humanSemanticReviewRequired": True, "modelCitationClicksTested": False}


def quiz(root):
    data = rows(Path(root) / "questions.csv")
    if len(data) != 12 or len({r["id"] for r in data}) != 12:
        raise ValueError("need_twelve_unique_questions")
    for row in data:
        if row["answer"] not in {"A", "B", "C"} or len({row[k].strip() for k in "ABC"}) != 3 or any(not row[k].strip() for k in "ABC"):
            raise ValueError("invalid_options_or_answer")
        source = local(root, row["source"]).read_text(encoding="utf-8")
        marker = "## " + row["concept"] + "\n"
        if marker not in source or not row["quote"] or row["quote"] not in source.split(marker, 1)[1].split("\n## ", 1)[0]:
            raise ValueError("answer_source_not_supported")
    return {"questions": len(data), "sourceQuotesMatch": True, "humanQuestionReviewRequired": True, "learnerResults": "not_run"}


def papers(root):
    data = rows(Path(root) / "paper-matrix.csv")
    if len(data) != 3 or len({r["id"] for r in data}) != 3:
        raise ValueError("need_three_papers")
    for row in data:
        file = local(root, row["file"])
        content = file.read_bytes()
        if not content.startswith(b"%PDF") or hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ValueError("paper_bytes_changed")
        if any(not row[k].strip() for k in ["question", "sample", "method", "metric", "locators", "limit", "license"]):
            raise ValueError("missing_method_or_limit")
    return {"papers": 3, "bytesMatch": True, "comparableAsSingleRanking": False, "reason": "different tasks, datasets and metrics", "modelExtractionTested": False}


def media(root):
    root = Path(root)
    facts = rows(root / "lesson-facts.csv")
    data = rows(root / "consistency-log.csv")
    expected = {(f["id"], form) for f in facts for form in ["handout", "audio", "video"]}
    seen, reviewed = set(), 0
    for row in data:
        pair = row["fact_id"], row["format"]
        if pair not in expected or pair in seen:
            raise ValueError("duplicate_or_unknown_media_fact")
        seen.add(pair)
        if row["status"] == "not_run":
            continue
        if row["status"] != "reviewed" or not all(row[k].strip() for k in ["location", "actual", "judgment"]):
            raise ValueError("review_evidence_required")
        reviewed += 1
    if seen != expected or len(facts) != 10:
        raise ValueError("need_thirty_observations")
    return {"required": 30, "reviewed": reviewed, "pending": 30 - reviewed, "modelMediaGenerationVerified": False, "note": "records alone do not prove generated audio or video exists"}


def transit(root):
    root = Path(root)
    file = root / "youbike-snapshot.json"
    data = json.loads(file.read_bytes())
    if not isinstance(data, list) or not data:
        raise ValueError("snapshot_must_be_nonempty_array")
    provenance = json.loads((root / "snapshot-provenance.json").read_text(encoding="utf-8"))
    if hashlib.sha256(file.read_bytes()).hexdigest() != provenance["sha256"]:
        raise ValueError("snapshot_hash_mismatch")
    fetched = datetime.fromisoformat(provenance["fetched_at"])
    if fetched.tzinfo is None:
        raise ValueError("capture_timezone_required")
    required = {"sno", "sna", "sarea", "infoTime", "act", "available_rent_bikes", "available_return_bikes"}
    seen, times = set(), []
    for row in data:
        if not isinstance(row, dict) or not required.issubset(row):
            raise ValueError("missing_required_fields")
        if not isinstance(row["sno"], str) or not row["sno"] or row["sno"] in seen:
            raise ValueError("duplicate_or_invalid_station_id")
        seen.add(row["sno"])
        for key in ["available_rent_bikes", "available_return_bikes"]:
            if type(row[key]) is not int or row[key] < 0:
                raise ValueError("invalid_station_count")
        dt = datetime.strptime(row["infoTime"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=8)))
        if dt > fetched:
            raise ValueError("station_time_after_capture")
        times.append(dt)
    declared = set(json.loads((root / "metadata-fields.json").read_text(encoding="utf-8"))["declared"])
    actual = set.intersection(*(set(r) for r in data))
    return {"scope": "single frozen historical snapshot", "stations": len(data), "uniqueIds": len(seen), "areaCounts": dict(sorted(Counter(r["sarea"] for r in data).items())), "actValues": dict(sorted(Counter(r["act"] for r in data).items())), "infoTimeMin": min(times).isoformat(), "infoTimeMax": max(times).isoformat(), "fetchedAt": provenance["fetched_at"], "declaredButAbsent": sorted(declared - actual), "presentButNotDeclared": sorted(actual - declared), "currentAvailabilityVerified": False, "annualUsageInferable": False, "capacityMeaningVerified": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["versions", "evidence", "quiz", "papers", "media", "transit"])
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    result = globals()[args.kind](args.directory)
    print(json.dumps(result, ensure_ascii=False, indent=2))
