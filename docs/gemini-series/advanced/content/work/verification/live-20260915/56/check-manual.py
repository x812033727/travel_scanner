"""Extract/check the saved Spark answer without fabricating publication times."""

import json
import re
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    raw = json.loads((HERE / "manual-response.json").read_text(encoding="utf-8"))
    blocks = re.split(r"\n更新 [123]\n", raw["text"])[1:]
    assert len(blocks) == 3
    rows = []
    for index, block in enumerate(blocks):
        published_raw = re.search(r"發布日：([^\n]+)", block)[1]
        published = datetime.strptime(published_raw, "%B %d, %Y").date()
        summary = re.search(r"繁體中文摘要：(.*)（(\d+)字）", block)
        quote = re.search(r'支持摘要的原文短句："([^"\n]+)"', block)[1]
        title = re.search(r"標題：([^\n]+)", block)[1]
        link = raw["links"][index + 3]
        assert link["text"] == title
        rows.append(
            {
                "published": published.isoformat(),
                "publishedPrecision": "day",
                "dateWithinRequestedCalendarRange": date(2026, 9, 7)
                <= published
                < date(2026, 9, 14),
                "title": title,
                "url": link["url"],
                "summary": summary[1],
                "modelClaimedLength": int(summary[2]),
                "unicodeCharacterCount": len(summary[1]),
                "within80UnderExplicitCountingRule": len(summary[1]) <= 80,
                "quoteWordCount": len(quote.split()),
                "quoteWithin10Words": len(quote.split()) <= 10,
            }
        )
    result = {
        "input": "manual-response.json",
        "rawTextChecksum": raw["textChecksum"],
        "countingRule": (
            "Unicode code points including spaces and Latin characters; "
            "excluding model count suffix"
        ),
        "ruleEstablishedAfterCapture": True,
        "publishedTimeInvented": False,
        "sourceSemanticReview": "source-review.md",
        "items": rows,
        "reportedCountsMatch": all(
            r["modelClaimedLength"] == r["unicodeCharacterCount"] for r in rows
        ),
        "allWithin80": all(r["within80UnderExplicitCountingRule"] for r in rows),
        "scheduledRunVerifiedByThisScript": False,
    }
    (HERE / "manual-structure-check.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "items": len(rows),
                "actualLengths": [r["unicodeCharacterCount"] for r in rows],
                "allWithin80": result["allWithin80"],
            }
        )
    )


if __name__ == "__main__":
    main()
