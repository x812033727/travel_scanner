"""Audit saved Canvas evidence; does not call Gemini or rerun browser tests."""

import hashlib
import json
import re
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fnv(record):
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    data = raw.encode("utf-16le")
    value = 2166136261
    for i in range(0, len(data), 2):
        value = ((value ^ int.from_bytes(data[i:i + 2], "little")) * 16777619) & 0xFFFFFFFF
    return f"{value:08x}"


def main():
    env = read("environment.json")
    for entry in env["inputs"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"], entry["path"]
    manifest = read("evidence-manifest.json")
    for entry in manifest["files"]:
        path = HERE / entry["path"]
        assert path.stat().st_size == entry["bytes"], entry["path"]
        assert sha(path) == entry["sha256"], entry["path"]
    historical = json.loads(
        (HERE.parents[1] / "authoring-review.json").read_text(encoding="utf-8")
    )["files"]
    assert len(historical) == 154
    for entry in historical:
        assert sha(ROOT / entry["path"]) == entry["sha256"], entry["path"]

    copies = read("download-copy-check.json")["checks"]
    assert len(copies) == 4
    for entry in copies:
        assert sha(HERE / entry["savedFile"]) == entry["downloadSha256"]
        assert entry["downloadSha256"] == entry["savedSha256"] and entry["match"]
    for version in range(1, 5):
        response = read(f"v{version}-response.json")
        path = HERE / response["downloadedFile"]
        assert sha(path) == response["downloadedSha256"]
        assert path.stat().st_size == response["downloadedBytes"]
        if "promptFile" in response:
            assert sha(HERE / response["promptFile"]) == response["promptSha256"]
    for version in (3, 4):
        original = (HERE / f"budget-v{version}.html").read_text(encoding="utf-8")
        assert original.rstrip().endswith("</html>")
        script = re.findall(r"<script>(.*?)</script>", original, re.DOTALL)
        assert len(script) == 1
        assert script[0] == (HERE / f"v{version}-inline.js").read_text(encoding="utf-8")
        fixture = (HERE / f"budget-v{version}-text200-test.html").read_text(encoding="utf-8")
        assert fixture == original.replace(
            "</head>",
            "<!-- Test fixture only: double root font size; original model output is unchanged. -->\n"
            "<style>html { font-size: 200%; }</style>\n</head>",
            1,
        )

    expected = {}
    cent = Decimal("0.01")
    for case in read("regression-expected.json")["cases"]:
        people, unit, venue, rate = map(Decimal, case["inputs"])
        base = people * unit + venue
        reserve = (base * rate / 100).quantize(cent, rounding=ROUND_HALF_UP)
        total = base + reserve
        average = (total / people).quantize(cent, rounding=ROUND_HALF_UP)
        actual = [f"{value:.2f}" for value in (base, reserve, total, average)]
        assert actual == case["expected"]
        expected[case["id"]] = case

    records = read("v4-browser-records.json")
    ui = read("v4-ui-observations.json")
    assert len(records) == 29 and len(ui) == 6
    for group, checksums in (
        (records, read("v4-browser-checksums.json")),
        (ui, read("v4-ui-checksums.json")),
    ):
        assert len(group) == len(checksums)
        assert len({(r["width"], r["case"]) for r in group}) == len(group)
        for record, checksum in zip(group, checksums, strict=True):
            assert record["pass"]
            assert record["case"] == checksum["case"]
            assert record["width"] == checksum["width"]
            assert fnv(record) == checksum["browserFnv1a32"], record["case"]
    numeric = [r for r in records if r["case"].startswith("B")]
    invalid = [r for r in records if r["case"].startswith("I")]
    assert len(numeric) == 12 and len(invalid) == 17
    assert {(r["width"], r["case"]) for r in numeric} == {
        (width, case) for width in (360, 1440) for case in expected
    }
    for record in records:
        assert record["inputVerified"] and record["oldResultHiddenOnEdit"]
    for record in numeric:
        case = expected[record["case"]]
        assert record["inputs"] == case["inputs"]
        assert record["actual"] == record["expected"] == case["expected"]
        if record["width"] == 1440:
            assert record["actualViewportWidth"] == 1440
    for record in invalid:
        assert record["resultHiddenAfterInvalid"] and record["errors"]
        assert record["ariaInvalid"] == "true"
        assert record["field"] + "-err" in record["describedBy"].split()
        assert record["focusedId"] == record["field"]
        assert record["announcement"] == "表單有錯誤，請檢查輸入欄位"
    for record in ui:
        assert record["scrollWidth"] <= record["width"]

    previous = read("v3-ui-observations.json")
    rounding = next(r for r in previous if r["case"] == "B05-large-decimal-rounding")
    assert not rounding["pass"] and rounding["actual"] != rounding["expected"]
    assert rounding["expected"] == expected["B05"]["expected"]
    diagnostics = read("viewport-diagnostics.json")
    assert diagnostics["excludedFromFinalCounts"] and len(diagnostics["records"]) == 6

    html = (HERE / "budget-v4.html").read_text(encoding="utf-8")
    forbidden = r"https?://|fetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|localStorage|sessionStorage|document\.cookie"
    matches = re.findall(forbidden, html)
    assert not matches
    assert not re.findall(r"<(?:script|link|iframe|img)\b[^>]*(?:src|href)\s*=", html, re.IGNORECASE)
    assert "BigInt" in html
    assert env["googleApiCalls"] == 0 and env["additionalPurchases"] == 0
    report = {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "status": "saved-evidence-audit-passed",
        "publishable": False,
        "fullSeriesComplete": False,
        "historicalFilesUnchanged": len(historical),
        "sealedEvidenceFiles": len(manifest["files"]),
        "downloadCopies": len(copies),
        "independentDecimalCases": len(expected),
        "numericalBrowserObservations": len(numeric),
        "invalidInputBrowserObservations": len(invalid),
        "uiObservations": len(ui),
        "browserRecordChecksums": len(records) + len(ui),
        "staticExternalResourceNetworkStorageScan": "no matched constructs; not runtime proof",
        "excludedMisSizedObservations": 6,
        "limitations": env["limitations"],
        "notes": [
            "Audits preserved observations; does not execute a browser or establish independent authenticity.",
            "v1/v2 incomplete files and v3 failures remain preserved.",
            "No native zoom, physical device, assistive-technology user test or complete runtime network trace.",
        ],
    }
    (HERE / "capture-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
