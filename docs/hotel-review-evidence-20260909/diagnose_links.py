"""Bounded normal link-health reads; no DB queries, provider quotes or mutations."""

import asyncio
import importlib.util
import sys
from pathlib import Path

import httpx

SPEC = importlib.util.spec_from_file_location(
    "platform_link_diagnostic", Path(__file__).with_name("hotel_review_evidence_20260909.py")
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)


async def main():
    baseline, _, pending = OP.load_baseline(sys.argv[1])
    manifest = OP.CORE.read_json(sys.argv[2])
    OP.validate_manifest(manifest, pending)
    output = Path(sys.argv[3])
    if await asyncio.to_thread(output.exists):
        raise ValueError("Refusing to overwrite link diagnostics")
    options = {r["id"]: r for r in baseline["options"]}
    semaphore = asyncio.Semaphore(3)

    async def check(entry):
        async with semaphore:
            url = entry["option_patch"]["url"]
            error_type = None
            try:
                health = await OP.CORE.check_hotel_link(
                    OP.CORE.HotelLink(
                        provider=options[entry["id"]]["provider"],
                        url=url,
                        evidence_url=url,
                    )
                )
            except (httpx.HTTPError, ConnectionError, TimeoutError) as exc:
                # Same classification as the normal admin review; never claim healthy.
                health, error_type = "unconfirmed", type(exc).__name__
            except ValueError as exc:
                health, error_type = "unsafe", type(exc).__name__
            result = {
                "id": entry["id"],
                "url": url,
                "health": health,
                "error_type": error_type,
                "checked_at": OP.CORE.datetime.now(OP.CORE.UTC),
            }
            OP.CORE.emit(result)
            return result

    results = await asyncio.gather(
        *(check(e) for e in manifest["decisions"] if e["kind"] == "option")
    )
    OP.CORE.save_new(
        output,
        {
            "tag": OP.TAG,
            "manifest_hash": OP.MANIFEST_HASH,
            "normal_guard_unchanged": True,
            "database_queries": 0,
            "mutations": 0,
            "quote_calls": 0,
            "clickout_calls": 0,
            "results": results,
        },
    )
    await OP.CORE.engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
