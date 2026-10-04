"""Option (a), writing-day half. NOT RUN during research (2026-10-03): it needs the owner's key.

Uses the repository's own JevClient (apps/api/app/ai/jev.py, loaded verbatim by jevsrc.py), so the
request is exactly what the site would send. Default is a dry run that prints the plan and sends
nothing. A live run needs BOTH `--live` and JEV_API_KEY in the environment; the key is read once,
passed to the client's Authorization header, and never printed or written anywhere.

  python3 demo_live_jev.py                 # plan only, no network
  JEV_API_KEY=... python3 demo_live_jev.py --live --repeat 3 --out live-YYYYMMDD.json

Calls in a live run: `repeat` identical calls on the zh-TW email (default 1; each call carries all
five questions, the reversed-order one included) + 1 call on the English rendering, + 2 with
--date-probe.
"""
import argparse
import asyncio
import json
import os
import sys
from datetime import UTC, datetime

import httpx

sys.path.insert(0, os.path.dirname(__file__))
import jevsrc  # noqa: E402
from demo_tokens import email, email_en, full, plan  # noqa: E402  (the exact questions)

ns = jevsrc.load(jevsrc.CLIENT)
JevClient, route, NoulAnswer = ns["JevClient"], ns["route"], ns["NoulAnswer"]
# Optional probe of a documented weakness (jev-1.13 "reads dates as text"): the same two dates in
# one format and in mixed formats. Correct answer: yes in both. Pre-registered failure: the two
# states land on opposite sides of 0.5, or either is below 0.5.
DATE_STATES = {
    "same_format": {"class_date": "2026-10-10", "signup_deadline": "2026-10-08"},
    "mixed_format": {"class_date": "2026年10月10日（週六）", "signup_deadline": "10/8/2026"},
}
DATE_QUESTION = {"deadline_first": ns["NoulQuestion"](
    instructions="The sign-up deadline is earlier than the class date.")}
BASE_URL = "https://api.typesafe.ai/v1"  # the host app.config pins Jev to
MODEL = "jev-1.13.0"                     # pinned version, not the moving jev-latest alias


def summary(answers):
    def ch(name):
        a = answers[name]
        dist = "  ".join(f"{k} {v:.2f}" for k, v in sorted(a.probabilities.items(), key=lambda kv: -kv[1]))
        return a.choice, a.confidence, dist
    return {
        "event_date": ch("event_date"),
        "event_date_reversed": ch("event_date_reversed"),
        "event_date_forced": ch("event_date_forced"),
        "event_date_forced_fixed": ch("event_date_forced_fixed"),
        "headcount_is_estimate": answers["headcount_is_estimate"].noul,
    }


async def run(args):
    key = os.environ.get("JEV_API_KEY", "")
    if not key:
        sys.exit("JEV_API_KEY is not set; nothing was sent")
    seen_models = []

    async def remember_model(response):
        await response.aread()
        try:
            seen_models.append(response.json().get("model"))
        except ValueError:
            seen_models.append(None)

    http = httpx.AsyncClient(timeout=20.0, event_hooks={"response": [remember_model]})
    client = JevClient(key, BASE_URL, MODEL, 20.0, client=http)
    del key
    record = {"ran_at": datetime.now(UTC).isoformat(), "requested_model": MODEL, "runs": []}
    try:
        jobs = [("zh-TW", email)] * args.repeat + [("en (Mokaair translation)", email_en)]
        for label, state in jobs:
            answers, usage = await client.ask(state, full)
            record["runs"].append({
                "state": label,
                "answers": {k: a.model_dump() for k, a in answers.items()},
                "usage": usage,
                "model": seen_models[-1] if seen_models else None,
                "route_zh_default": {k: route(a, act_at=0.9, flag_at=0.5, locale="zh-TW") for k, a in answers.items()},
                "route_en": {k: route(a, act_at=0.9, flag_at=0.5, locale="en") for k, a in answers.items()},
                "summary": summary(answers),
            })
        if args.date_probe:
            for label, state in DATE_STATES.items():
                answers, usage = await client.ask(state, DATE_QUESTION)
                record["runs"].append({"state": f"date probe {label}", "state_value": state,
                                       "answers": {k: a.model_dump() for k, a in answers.items()},
                                       "usage": usage, "model": seen_models[-1] if seen_models else None})
    finally:
        await http.aclose()
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=1)
    first = record["runs"][0]
    s = first["summary"]
    # At most 8 lines of at most 78 columns: what the `terminal` slide can hold.
    print(f"model {first['model']}  usage {json.dumps(first['usage'])}"[:78])
    print(f"event_date -> {s['event_date'][0]}  conf {s['event_date'][1]:.2f}")
    print(f"  {s['event_date'][2]}"[:78])
    print(f"options reversed -> {s['event_date_reversed'][0]}  conf {s['event_date_reversed'][1]:.2f}")
    print(f"headcount_is_estimate  noul {s['headcount_is_estimate']:.2f}")
    print(f"forced date -> {s['event_date_forced'][0]}  conf {s['event_date_forced'][1]:.2f}")
    print(f"fixed (+not_stated) -> {s['event_date_forced_fixed'][0]}  conf {s['event_date_forced_fixed'][1]:.2f}")
    print(f"route zh-TW: {first['route_zh_default']['headcount_is_estimate']} | en: {first['route_en']['headcount_is_estimate']}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--live", action="store_true")
    p.add_argument("--repeat", type=int, default=1)
    p.add_argument("--out", default="live-jev.json")
    p.add_argument("--date-probe", action="store_true", help="2 more calls: the date-ordering probe")
    args = p.parse_args()
    if not args.live:
        print(json.dumps({"dry_run": True, "calls": args.repeat + 1 + (2 if args.date_probe else 0),
                          "date_probe": {k: plan(v, DATE_QUESTION) for k, v in DATE_STATES.items()},
                          "zh": plan(email, full), "en": plan(email_en, full)}, ensure_ascii=False, indent=1))
        return
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
