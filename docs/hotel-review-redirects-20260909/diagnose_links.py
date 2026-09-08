"""Read-only normal server link checks, no database queries or URL-guard changes."""

import asyncio
import importlib.util
import sys
from pathlib import Path

WRAPPER = Path(__file__).with_name("hotel_review_redirects_20260909.py")
SPEC = importlib.util.spec_from_file_location("redirect_diagnostic", WRAPPER)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)


async def main():
    manifest = OP.CORE.read_json(sys.argv[1])
    observations = OP.CORE.read_json(sys.argv[2])
    output = Path(sys.argv[3])
    if await asyncio.to_thread(output.exists):
        raise ValueError("Refusing to overwrite diagnostics")
    expected = {e["id"]: e for e in manifest["decisions"]}
    results = []
    for observation in observations["entries"]:
        identifier = observation["option_id"]
        entry = expected[identifier]
        for label in ("requested_url", "final_url"):
            url = observation[label]
            if url not in entry["source_urls"]:
                raise ValueError("Unreviewed diagnostic URL")
            health = await OP.CORE.check_hotel_link(OP.CORE.HotelLink(
                provider="agoda", url=url, evidence_url=url,
            ))
            result = {
                "id": identifier, "url_kind": label, "url": url, "health": health,
                "checked_at": OP.CORE.datetime.now(OP.CORE.UTC),
            }
            results.append(result)
            OP.CORE.emit(result)
    OP.CORE.save_new(output, {
        "tag": OP.TAG, "normal_guard_unchanged": True, "database_queries": 0,
        "mutations": 0, "quote_calls": 0, "clickout_calls": 0, "results": results,
    })
    await OP.CORE.engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
