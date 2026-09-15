"""Check captured photo/Spark evidence; no model calls or live-state claims."""

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fnv(text):
    data = text.encode("utf-16le")
    value = 2166136261
    for offset in range(0, len(data), 2):
        value = (
            (value ^ int.from_bytes(data[offset : offset + 2], "little")) * 16777619
        ) & 0xFFFFFFFF
    return f"{value:08x}"


def main():
    historical = read(HERE.parent / "authoring-review.json")["files"]
    assert len(historical) == 154
    for item in historical:
        assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
    result = {"checkedAt": datetime.now(UTC).isoformat(), "historicalFilesUnchanged": 154}
    for number in (55, 56):
        directory = HERE / str(number)
        environment = read(directory / "environment.json")
        for item in environment["inputs"]:
            assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
        manifest = read(directory / "evidence-manifest.json")["files"]
        for item in manifest:
            path = directory / item["path"]
            assert path.resolve().is_relative_to(directory.resolve()), item["path"]
            assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"], item[
                "path"
            ]
            if path.suffix in {".md", ".txt", ".json"}:
                text = path.read_text(encoding="utf-8")
                assert not re.search(
                    r"AIza[0-9A-Za-z_-]{20,}|gemini\.google\.com/(?:app|spark/chat)/[0-9a-f]+", text
                ), path
        response_files = environment["responseFiles"]
        for name in response_files:
            response = read(directory / name)
            assert fnv(response["prompt"]) == response["promptChecksum"], name
            assert fnv(response["text"]) == response["textChecksum"], name
            assert datetime.fromisoformat(response["startedAt"]) <= datetime.fromisoformat(
                response["capturedAt"]
            ), name
        assert environment["apiCalls"] == 0 and environment["extraSpendTwd"] == 0
        result[str(number)] = {
            "evidenceFiles": len(manifest),
            "capturedResponses": len(response_files),
            "status": "integrity-pass",
            "semanticApproval": "pending",
        }
    photo = HERE / "55"
    original_photo_prompt = HERE.parents[1] / "examples/55/observation-prompt.txt"
    assert read(photo / "photo-v1.json")["prompt"] == original_photo_prompt.read_text(
        encoding="utf-8"
    ).rstrip("\n")
    assert read(photo / "environment.json")["physicalDevices"] == {
        "Android": "not_run",
        "iPhone": "not_run",
    }
    reopened = read(photo / "reopen-check.json")
    assert reopened["responseCount"] == 2
    assert reopened["checksums"] == [
        read(photo / f"photo-v{v}.json")["textChecksum"] for v in (1, 2)
    ]
    spark = HERE / "56"
    assert read(spark / "manual-response.json")["prompt"] == (
        spark / "prompt-manual.txt"
    ).read_text(encoding="utf-8").rstrip("\n")
    setup = read(spark / "schedule-setup.json")
    assert fnv(setup["prompt"]) == setup["promptChecksum"]
    assert setup["prompt"] == (spark / "prompt-schedule.txt").read_text(encoding="utf-8").rstrip(
        "\n"
    )
    assert setup["runNowClicked"] is False
    observations = read(spark / "schedule-observations.json")
    assert observations["finalState"] == "deleted" and observations["userConfirmedDeletion"]
    assert observations["runNowClicked"] is False
    assert observations["scheduledOutputCaptured"] is False
    assert observations["fullWeekStopObservation"] == "not_run"
    reopened_spark = read(spark / "reopen-check.json")
    assert reopened_spark["textChecksum"] == read(spark / "manual-response.json")["textChecksum"]
    result["56"]["automaticTrigger"] = observations["automaticTrigger"]
    result["56"]["finalScheduleState"] = observations["finalState"]
    result["publishable"] = False
    result["note"] = (
        "Integrity checks do not prove device behavior, "
        "scheduled execution, or semantic correctness."
    )
    (HERE / "mobile-spark-audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
