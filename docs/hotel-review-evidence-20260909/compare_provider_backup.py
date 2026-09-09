"""Read-only backup/current comparison; output hashes/field names, never settings secrets."""

import hashlib
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/root/mokaair-hotel-evidence-20260909-FbmevgwP")
BACKUP_SHA = "fb52a997476aadb43ba44c0da770df4f1b543521fa8c6f9a6b267feec24a792f"
CONTAINER = "travel_scanner-postgres-1"


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def sql(query):
    result = subprocess.run(
        [
            "docker",
            "exec",
            CONTAINER,
            "psql",
            "-X",
            "-q",
            "-A",
            "-t",
            "-v",
            "ON_ERROR_STOP=1",
            "-U",
            "travel",
            "-d",
            "travel_scanner",
            "-c",
            "BEGIN READ ONLY; " + query + "; ROLLBACK;",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def unescape(value):
    if value == r"\N":
        return None
    escapes = {"b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v"}

    def replace(match):
        token = match.group(1)
        if token.startswith("x") and len(token) > 1:
            return chr(int(token[1:], 16))
        if token[0] in "01234567":
            return chr(int(token, 8))
        return escapes.get(token, token)

    return re.sub(r"\\(x[0-9a-fA-F]{1,2}|[0-7]{1,3}|.)", replace, value)


def normalize(row):
    row = dict(row)
    for key, value in row.items():
        if value is not None and key.endswith("_at"):
            row[key] = datetime.fromisoformat(value).astimezone(UTC).isoformat()
    return row


def main():
    path = ROOT / "backup-before.dump"
    if hashlib.sha256(path.read_bytes()).hexdigest() != BACKUP_SHA:
        raise ValueError("Wrong protected backup")
    with path.open("rb") as stream:
        restored = subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                CONTAINER,
                "pg_restore",
                "--data-only",
                "--table=provider_configs",
                "--file=-",
            ],
            stdin=stream,
            check=True,
            capture_output=True,
            text=True,
        )
    columns, originals, reading = None, [], False
    for line in restored.stdout.splitlines():
        match = re.fullmatch(r"COPY public\.provider_configs \((.+)\) FROM stdin;", line)
        if match:
            if columns is not None:
                raise ValueError("Duplicate COPY section")
            columns, reading = match.group(1).split(", "), True
        elif reading and line == r"\.":
            reading = False
        elif reading:
            values = [unescape(v) for v in line.split("\t")]
            if len(values) != len(columns):
                raise ValueError("COPY width mismatch")
            row = dict(zip(columns, values, strict=True))
            row["enabled"] = {"t": True, "f": False}[row["enabled"]]
            row["priority"] = int(row["priority"])
            row["config"] = json.loads(row["config"])
            originals.append(normalize(row))
    current = sql("SELECT json_agg(to_jsonb(p) ORDER BY provider) FROM provider_configs p")
    current = [normalize(r) for r in current]
    old = {r["provider"]: r for r in originals}
    new = {r["provider"]: r for r in current}
    if reading or len(old) != 15 or set(old) != set(new):
        raise ValueError("Unexpected provider inventory")
    comparisons = []
    for provider in sorted(old):
        if set(old[provider]) != set(new[provider]):
            raise ValueError("Provider column set changed")
        changed = [k for k in old[provider] if old[provider][k] != new[provider][k]]
        item = {
            "provider": provider,
            "changed_fields": changed,
            "before_sha256": digest(old[provider]),
            "current_sha256": digest(new[provider]),
        }
        if provider == "layout":
            a, b = old[provider]["config"], new[provider]["config"]
            item["config_changed_fields"] = sorted(
                k for k in set(a) | set(b) if a.get(k) != b.get(k)
            )
            item["updated_at"] = new[provider]["updated_at"]
        comparisons.append(item)
    audit = sql(
        "SELECT coalesce(json_agg(json_build_object("
        "'action',action,'target',target,'created_at',created_at,"
        "'config_fields',metadata_json->'config_fields',"
        "'actor_present',actor_user_id IS NOT NULL,"
        "'actor_matches_hotel_root',actor_user_id=(SELECT actor_user_id "
        "FROM catalog_review_runs WHERE id='5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a')) "
        "ORDER BY created_at),'[]'::json) FROM admin_audit_logs "
        "WHERE action='layout_settings_updated' AND target='layout' "
        "AND created_at >= '2026-09-09 00:32:08.141514+00:00'"
    )
    report = {
        "tag": "hotel-review-evidence-20260909",
        "method": "read_only_backup_vs_current",
        "checked_at": datetime.now(UTC).isoformat(),
        "database_writes": 0,
        "backup_sha256": BACKUP_SHA,
        "secret_values_emitted": False,
        "comparisons": comparisons,
        "concurrent_layout_audits": audit,
        "note": "Actual concurrent difference, not an exception to strict acceptance. "
        "No setting restored, changed or normalized in the database.",
    }
    with (ROOT / "provider-config-concurrency.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
