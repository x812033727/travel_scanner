"""Probe the Korea Tourism Organization TourAPI gateway.

Written for the ``2026-09-06-korea-tourism-tourapi-spike`` task, which needs two numbers
nobody has produced yet:

* **Gate B, reachability.** Can ``apis.data.go.kr`` be reached at all from the production
  VPS egress? Three independent local runs scored 1/15, 0/17 and 0/3 while every other
  data.go.kr host answered instantly, so "the gateway works" is unproven rather than
  assumed. Reachability does not need a service key: a request rejected as a bad key still
  proves it crossed the network, so this script runs keyless too.
* **Gate C, corpus size.** ``areaBasedList2`` totals for Seoul and Busan against the
  nationwide total, so the region filter can be shown to actually bite.

Only ``httpx`` is imported beyond the standard library, so this runs unchanged inside the
production api container::

    docker compose -f docker-compose.prod.yml exec -T api python - < probe_tourapi.py \
        --service KorService2 --ldong 11 --repeat 20

Three traps this script exists to avoid, all of them silent:

* **HTTP 200 is not the success criterion.** data.go.kr answers a rejected key with an
  error envelope, and the observed failure mode was HTTP 403 carrying a JSON body. Success
  is ``resultCode == "0000"``, read out of the body.
* **Errors arrive in two different shapes.** The service layer answers in the format you
  asked for (``_type=json``), but the gateway in front of it answers in XML regardless.
  Both are parsed here.
* **``areaCode`` is dead and fails open.** It is marked 미사용항목(삭제예정); sending it
  raises no error and returns the nationwide total, which looks entirely normal. The live
  filter is ``lDongRegnCd`` (Seoul ``11``, Busan ``26``), which is what ``--ldong`` sends.
  Always compare a filtered count against the unfiltered control run: if they match, the
  filter did not apply and the numbers are worthless.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urlencode

import httpx

GATEWAY = "https://apis.data.go.kr/B551011"
SERVICES = ("KorService2", "ChtService2", "EngService2", "JpnService2", "ChsService2")

# A desktop user agent. Costs nothing to send and removes one variable from a failure that
# so far has no confirmed cause.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# data.go.kr's documented codes. Anything absent is reported verbatim rather than guessed.
RESULT_CODES: dict[str, str] = {
    "0000": "OK",
    "01": "APPLICATION_ERROR",
    "02": "DB_ERROR",
    "03": "NODATA_ERROR",
    "04": "HTTP_ERROR",
    "05": "SERVICETIME_OUT",
    "10": "INVALID_REQUEST_PARAMETER_ERROR",
    "11": "NO_MANDATORY_REQUEST_PARAMETERS_ERROR",
    "12": "NO_OPENAPI_SERVICE_ERROR",
    "20": "SERVICE_ACCESS_DENIED_ERROR",
    "21": "TEMPORARILY_DISABLE_THE_SERVICEKEY_ERROR",
    "22": "LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR",
    "30": "SERVICE_KEY_IS_NOT_REGISTERED_ERROR",
    "31": "DEADLINE_HAS_EXPIRED_ERROR",
    "32": "UNREGISTERED_IP_ERROR",
    "33": "UNSIGNED_CALL_ERROR",
    "99": "UNKNOWN_ERROR",
}

# Sent when no key is supplied. The point is to learn whether the request reaches the
# gateway, and a rejected key answers that just as well as an accepted one does.
PLACEHOLDER_KEY = "reachability-probe-no-key"


@dataclass
class Attempt:
    """One request and what came back, whatever shape it came back in."""

    ok: bool
    reached: bool
    status: int | None
    code: str | None
    message: str | None
    seconds: float
    total_count: int | None = None

    def label(self) -> str:
        if self.ok:
            total = self.total_count if self.total_count is not None else "?"
            return f"ok total={total}"
        if not self.reached:
            return f"unreachable {self.message}"
        named = RESULT_CODES.get(self.code or "", "")
        code = f"code={self.code}" if self.code else "code=?"
        detail = f" {named}" if named else ""
        note = f" {self.message}" if self.message and not named else ""
        return f"rejected {code}{detail}{note}"


def _dig(payload: Any, *path: str) -> Any:
    for key in path:
        if not isinstance(payload, dict):
            return None
        payload = payload.get(key)
    return payload


def _as_int(value: Any) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _from_json(body: str) -> tuple[str, str, int | None] | None:
    """Read the service envelope, or the gateway's own JSON error, out of ``body``."""
    try:
        payload = json.loads(body)
    except ValueError:
        return None
    if not isinstance(payload, dict):
        return None
    code = _dig(payload, "response", "header", "resultCode")
    if code is not None:
        message = _dig(payload, "response", "header", "resultMsg") or ""
        total = _dig(payload, "response", "body", "totalCount")
        return str(code), str(message), _as_int(total)
    # The gateway in front of the service answers in a shape of its own.
    code = _dig(payload, "OpenAPI_ServiceResponse", "cmmMsgHeader", "returnReasonCode")
    if code is not None:
        message = _dig(payload, "OpenAPI_ServiceResponse", "cmmMsgHeader", "returnAuthMsg") or ""
        return str(code), str(message), None
    return None


def _from_xml(body: str) -> tuple[str, str, int | None] | None:
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return None
    code = root.findtext(".//resultCode") or root.findtext(".//returnReasonCode")
    if code is None:
        return None
    message = root.findtext(".//resultMsg") or root.findtext(".//returnAuthMsg") or ""
    return code.strip(), message.strip(), _as_int(root.findtext(".//totalCount"))


def build_url(service: str, operation: str, key: str, encoded_key: bool, **params: Any) -> str:
    """Assemble the request URL.

    data.go.kr hands out the same key twice, once URL-encoded and once not. Encoding an
    already-encoded key turns every ``%2B`` into ``%252B`` and earns a code 30 that reads
    exactly like a wrong key, so ``encoded_key`` appends it verbatim for that case.
    """
    query = {key_: value for key_, value in params.items() if value is not None}
    if encoded_key:
        tail = urlencode(query, quote_via=quote)
        return f"{GATEWAY}/{service}/{operation}?serviceKey={key}&{tail}"
    return f"{GATEWAY}/{service}/{operation}?{urlencode({'serviceKey': key, **query})}"


def probe(client: httpx.Client, url: str) -> Attempt:
    started = time.monotonic()
    try:
        response = client.get(url)
    except httpx.HTTPError as error:
        return Attempt(
            ok=False,
            reached=False,
            status=None,
            code=None,
            message=f"{type(error).__name__}: {error}",
            seconds=time.monotonic() - started,
        )
    elapsed = time.monotonic() - started
    body = response.text
    parsed = _from_json(body) or _from_xml(body)
    if parsed is None:
        # A body neither parser recognised still proves the network hop happened.
        snippet = " ".join(body.split())[:160]
        return Attempt(
            ok=False,
            reached=True,
            status=response.status_code,
            code=None,
            message=f"unparsed body: {snippet!r}",
            seconds=elapsed,
        )
    code, message, total = parsed
    return Attempt(
        ok=code == "0000",
        reached=True,
        status=response.status_code,
        code=code,
        message=message,
        seconds=elapsed,
        total_count=total,
    )


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, round(fraction * (len(ordered) - 1)))
    return ordered[index]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Probe the TourAPI gateway.")
    parser.add_argument("--service", default="KorService2", help=f"one of {', '.join(SERVICES)}")
    parser.add_argument("--operation", default="areaBasedList2")
    parser.add_argument(
        "--ldong",
        default=None,
        help="lDongRegnCd: Seoul 11, Busan 26. Omit for the nationwide control run. Do not "
        "substitute the retired areaCode, which is ignored silently.",
    )
    parser.add_argument(
        "--content-type-id",
        default=None,
        help="Korean 12/14/39, multilingual 76/78/82. The two sets do not overlap.",
    )
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--count-only", action="store_true", help="one request, print totalCount")
    parser.add_argument("--key", default=os.environ.get("TOURAPI_SERVICE_KEY"))
    parser.add_argument(
        "--key-is-encoded",
        action="store_true",
        help="the key is already URL-encoded; append it verbatim instead of encoding again",
    )
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between attempts")
    parser.add_argument("--json", action="store_true", help="print one JSON object, not prose")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    key = args.key or PLACEHOLDER_KEY
    keyless = args.key is None
    repeat = 1 if args.count_only else max(1, args.repeat)
    url = build_url(
        args.service,
        args.operation,
        key,
        args.key_is_encoded,
        MobileOS="ETC",
        MobileApp="TravelScanner",
        _type="json",
        numOfRows=1,
        pageNo=1,
        lDongRegnCd=args.ldong,
        contentTypeId=args.content_type_id,
    )

    scope = f"lDongRegnCd={args.ldong}" if args.ldong else "nationwide (no region filter)"
    if not args.json:
        print(f"{args.service}/{args.operation}  {scope}  repeat={repeat}")
        if keyless:
            print("no service key: reachability only, a rejected key still counts as reached")
        print()

    attempts: list[Attempt] = []
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/xml;q=0.9, */*;q=0.5",
    }
    with httpx.Client(timeout=args.timeout, headers=headers, follow_redirects=True) as client:
        for index in range(repeat):
            if index and args.delay:
                time.sleep(args.delay)
            attempt = probe(client, url)
            attempts.append(attempt)
            if not args.json:
                status = attempt.status if attempt.status is not None else "---"
                print(
                    f"  {index + 1:>3}/{repeat}  {attempt.seconds:6.2f}s  "
                    f"http={status}  {attempt.label()}"
                )

    latencies = [attempt.seconds for attempt in attempts]
    reached = sum(1 for attempt in attempts if attempt.reached)
    succeeded = sum(1 for attempt in attempts if attempt.ok)
    totals = [attempt.total_count for attempt in attempts if attempt.total_count is not None]

    if args.json:
        print(
            json.dumps(
                {
                    "service": args.service,
                    "operation": args.operation,
                    "ldong": args.ldong,
                    "keyless": keyless,
                    "attempts": len(attempts),
                    "reached": reached,
                    "succeeded": succeeded,
                    "total_count": totals[0] if totals else None,
                    "latency_p50": round(percentile(latencies, 0.5), 3),
                    "latency_p90": round(percentile(latencies, 0.9), 3),
                    "latency_max": round(max(latencies), 3) if latencies else None,
                    "codes": sorted({attempt.code for attempt in attempts if attempt.code}),
                },
                ensure_ascii=False,
            )
        )
    else:
        print()
        print(f"reached   {reached}/{len(attempts)}  (the request crossed the network)")
        print(f"succeeded {succeeded}/{len(attempts)}  (resultCode 0000)")
        print(
            f"latency   p50 {percentile(latencies, 0.5):.2f}s  "
            f"p90 {percentile(latencies, 0.9):.2f}s  max {max(latencies):.2f}s"
        )
        if totals:
            print(f"totalCount {totals[0]}  ({scope})")
            if not args.ldong:
                print("  control run: a filtered count equal to this means the filter did nothing")

    if args.count_only:
        return 0 if succeeded else 1
    return 0 if succeeded == len(attempts) else 1


if __name__ == "__main__":
    sys.exit(main())
