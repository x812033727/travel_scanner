"""Read two exact public Wikidata representations; never connect to production."""

import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
QID = "Q11288502"
REVISION = 2434981201
CLAIM = "Q11288502$5AB1D2CD-AE18-4CED-892C-97B7269B056A"
BASE_URL = "https://www.wikidata.org/wiki/Special:EntityData/Q11288502.json"


def fetch(url):
    request = urllib.request.Request(url, headers={
        "Accept": "application/json", "User-Agent": "MokaairHotelEvidenceReview/20260909",
    })
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=25) as response:
        if response.status != 200 or not response.url.startswith(BASE_URL):
            raise ValueError("Unexpected structured source response")
        body = response.read(2_000_001)
        if len(body) > 2_000_000:
            raise ValueError("Bounded source body exceeded")
    entity = json.loads(body)["entities"][QID]
    if entity["id"] != QID or entity["lastrevid"] != REVISION:
        raise ValueError("Exact reviewed source revision has changed")
    matches = [c for c in entity["claims"]["P625"] if c["id"] == CLAIM]
    if len(matches) != 1:
        raise ValueError("Exact independent coordinate claim missing")
    claim = matches[0]
    if claim["rank"] == "deprecated" or claim["mainsnak"]["snaktype"] != "value":
        raise ValueError("Coordinate claim not usable")
    value = claim["mainsnak"]["datavalue"]["value"]
    if value != {
        "latitude": 35.00886111, "longitude": 135.78794444,
        "altitude": None, "precision": 0.000001, "globe": "http://www.wikidata.org/entity/Q2",
    }:
        raise ValueError("Pinned independent coordinate differs")
    references = claim["references"]
    if len(references) != 1 or set(references[0]["snaks"]) != {"P143"}:
        raise ValueError("Unexpected upstream or mixed coordinate references")
    imported = references[0]["snaks"]["P143"]
    if len(imported) != 1 or imported[0]["datavalue"]["value"]["id"] != "Q177837":
        raise ValueError("Not the independent Japanese Wikipedia reference")
    return {
        "url": url, "http_status": 200, "checked_at": datetime.now(UTC).isoformat(),
        "body_sha256": hashlib.sha256(body).hexdigest(), "qid": QID,
        "lastrevid": entity["lastrevid"], "entity_modified_at": entity["modified"],
        "selected_claim": claim,
        "excluded_alternative_claim_ids": [
            c["id"] for c in entity["claims"]["P625"] if c["id"] != CLAIM
        ],
    }


def main():
    output = HERE / "westin-coordinate-evidence.json"
    if output.exists():
        raise ValueError("Evidence already exists; no requests made")
    current = fetch(BASE_URL)
    pinned = fetch(f"{BASE_URL}?revision={REVISION}")
    if current["selected_claim"] != pinned["selected_claim"]:
        raise ValueError("Current and pinned claims differ")
    report = {
        "tag": "hotel-review-evidence-20260909", "method": "anonymous_public_Wikidata_JSON",
        "production_requests": 0, "paid_api_calls": 0, "google_coordinates_used": False,
        "license_name": "CC0-1.0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "licensing_policy_url": "https://www.wikidata.org/wiki/Wikidata:Licensing",
        "semantics": "Representative hotel point, not a surveyed entrance or accuracy guarantee.",
        "exclusions": "Alternative Skyscanner P625 claims and Google/OTA coordinates excluded.",
        "current": current, "pinned": pinned,
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"qid": QID, "revision": REVISION, "claim": CLAIM, "verified": True}))


if __name__ == "__main__":
    main()
