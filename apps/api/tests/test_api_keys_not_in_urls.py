"""Google API keys travel in the X-Goog-Api-Key header, never in a request URL.

On 2026-09-19 the production collector's log carried the full YouTube key once per search:
httpx logs every request URL at INFO and the key rode in the query string. A header is not
part of the URL, so it reaches no request log.
"""

from __future__ import annotations

import ast
import logging
import re
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import httpx
import pytest
from redis import Redis

from app.config import Settings
from app.hotspots import scheduler
from app.hotspots.guides import GOOGLE_API_KEY_HEADER, YouTubeGuideProvider
from app.providers.google_travel_impact import GoogleTravelImpactProvider

SECRET = "AIzaSy-test-key-that-must-never-appear-in-a-url"


def _recording_client(
    payloads: dict[str, dict[str, object]],
) -> tuple[httpx.AsyncClient, list[httpx.Request]]:
    """A client that answers each URL path with its payload and keeps every request."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=payloads[request.url.path])

    return httpx.AsyncClient(transport=httpx.MockTransport(handler)), seen


def _assert_key_in_header_only(requests: list[httpx.Request]) -> None:
    assert requests, "the call under test sent no request"
    for request in requests:
        assert request.headers.get(GOOGLE_API_KEY_HEADER) == SECRET
        assert "key" not in request.url.params
        assert SECRET not in str(request.url)


@pytest.mark.asyncio
async def test_youtube_search_and_import_send_the_key_as_a_header() -> None:
    video = {
        "id": "abcdefghijk",
        "status": {"privacyStatus": "public"},
        "snippet": {"title": "測試影片", "channelTitle": "頻道", "thumbnails": {}},
        "statistics": {"viewCount": "10"},
    }
    client, seen = _recording_client(
        {
            "/youtube/v3/search": {"items": [{"id": {"videoId": "abcdefghijk"}}]},
            "/youtube/v3/videos": {"items": [video]},
        }
    )
    provider = YouTubeGuideProvider(SECRET, client=client)
    try:
        await provider.search("清水寺 旅遊", "zh-TW", limit=5)
        await provider.import_video("https://www.youtube.com/watch?v=abcdefghijk", "zh-TW")
    finally:
        await client.aclose()
    # search + videos for the search, videos again for the import
    assert [request.url.path for request in seen] == [
        "/youtube/v3/search",
        "/youtube/v3/videos",
        "/youtube/v3/videos",
    ]
    _assert_key_in_header_only(seen)


@pytest.mark.asyncio
async def test_travel_impact_sends_the_key_as_a_header() -> None:
    client, seen = _recording_client(
        {"/v1/flights:computeFlightEmissions": {"flightEmissions": []}}
    )
    settings = Settings(google_travel_impact_api_key=SECRET)
    provider = GoogleTravelImpactProvider(redis=None, settings=settings, client=client)  # type: ignore[arg-type]
    try:
        await provider._compute([{"origin": "TPE", "destination": "NRT"}])
    finally:
        await client.aclose()
    assert [request.url.path for request in seen] == ["/v1/flights:computeFlightEmissions"]
    _assert_key_in_header_only(seen)


def _google_key_query_findings(root: Path) -> list[str]:
    # A small syntax guardrail, not a taint analyser: transport tests above prove the
    # actual requests. Discover new clients, including config-supplied Google base URLs.
    findings: list[str] = []
    for path in sorted(root.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        if not (
            "googleapis.com" in source
            or "GOOGLE_API_KEY_HEADER" in source
            or re.search(r"\bgoogle_\w+_(?:base_url|api_key)\b", source)
        ):
            continue
        tree = ast.parse(source)
        parents = {
            child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)
        }
        for node in ast.walk(tree):
            values: list[ast.AST] = []
            if isinstance(node, ast.Dict):
                values = [
                    value
                    for key, value in zip(node.keys, node.values, strict=True)
                    if isinstance(key, ast.Constant) and key.value in {"key", "$key"}
                ]
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "dict"
            ):
                values = [item.value for item in node.keywords if item.arg == "key"]
            elif isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Store):
                if isinstance(node.slice, ast.Constant) and node.slice.value in {"key", "$key"}:
                    values = [node]
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                if re.search(r"[?&](?:\$|%24)?key=", node.value):
                    values = [node]
            for value in values:
                assert isinstance(node, (ast.Dict, ast.Call, ast.Subscript, ast.Constant))
                scope: list[str] = []
                parent: ast.AST = node
                while parent in parents:
                    parent = parents[parent]
                    if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                        scope.insert(0, parent.name)
                # This vendor requires a query key; never exempt the entire routing file.
                if (
                    path.relative_to(root).as_posix() == "trips/routing.py"
                    and scope == ["EkispertRouteProvider", "_params"]
                    and any(
                        isinstance(item, ast.Attribute) and item.attr == "ekispert_api_key"
                        for item in ast.walk(value)
                    )
                ):
                    continue
                findings.append(
                    f"{path.relative_to(root).as_posix()}:{node.lineno}:{'.'.join(scope)}"
                )
    return findings


def test_no_google_client_builds_a_key_query_parameter() -> None:
    assert _google_key_query_findings(Path(__file__).resolve().parents[1] / "app") == []


@pytest.mark.parametrize(
    "marker",
    [
        'URL = "https://new.googleapis.com/v1"',
        "HEADER = GOOGLE_API_KEY_HEADER",
        "URL = settings.google_future_base_url",
    ],
)
@pytest.mark.parametrize(
    "query",
    [
        'params = {"key": secret}',
        "params = dict(key=secret)",
        'params["key"] = secret',
        'url = f"{URL}?key={secret}"',
    ],
)
def test_guardrail_discovers_new_google_clients(tmp_path: Path, marker: str, query: str) -> None:
    (tmp_path / "new_client.py").write_text(f"{marker}\n{query}\n", encoding="utf-8")
    assert _google_key_query_findings(tmp_path) == ["new_client.py:2:"]


def test_guardrail_allows_headers_and_oauth_without_demanding_an_api_key(tmp_path: Path) -> None:
    (tmp_path / "new_client.py").write_text(
        'URL = "https://new.googleapis.com/v1"\n'
        'headers = {"X-Goog-Api-Key": secret}\n'
        'oauth_headers = {"Authorization": "Bearer token"}\n'
        '# Example of forbidden syntax: {"key": secret}\n',
        encoding="utf-8",
    )
    assert _google_key_query_findings(tmp_path) == []


def test_guardrail_only_exempts_ekispert_credentials_in_its_params_method(tmp_path: Path) -> None:
    (tmp_path / "trips").mkdir()
    (tmp_path / "trips" / "routing.py").write_text(
        'URL = "https://routes.googleapis.com/v1"\n'
        "class EkispertRouteProvider:\n"
        "    def _params(self):\n"
        '        return {"key": self.settings.ekispert_api_key or ""}\n'
        "class GoogleRouteProvider:\n"
        "    def _params(self):\n"
        '        return {"key": self.settings.google_maps_api_key}\n',
        encoding="utf-8",
    )
    assert _google_key_query_findings(tmp_path) == [
        "trips/routing.py:7:GoogleRouteProvider._params"
    ]


@pytest.mark.parametrize("entrypoint", ["api", "worker"])
def test_entrypoints_quiet_http_logs_before_serving_or_working(
    entrypoint: str, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    from app import worker

    loggers = [logging.getLogger(name) for name in ("httpx", "httpcore")]
    previous = [logger.level for logger in loggers]

    def assert_quiet() -> None:
        for logger in loggers:
            assert logger.level == logging.WARNING
            assert not logger.isEnabledFor(logging.INFO)
            assert not logger.isEnabledFor(logging.DEBUG)
            assert logger.isEnabledFor(logging.WARNING)

    try:
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
        if entrypoint == "api":
            path = Path(__file__).resolve().parents[1] / "app" / "main.py"
            spec = spec_from_file_location("api_logging_contract", path)
            assert spec is not None and spec.loader is not None
            module = module_from_spec(spec)
            monkeypatch.setitem(sys.modules, spec.name, module)
            spec.loader.exec_module(module)
        else:

            class FakeWorker:
                def __init__(self, *_args: object, **_kwargs: object) -> None:
                    pass

                def work(self, **_kwargs: object) -> None:
                    assert_quiet()

            monkeypatch.setattr(Redis, "from_url", lambda _url: object())
            monkeypatch.setattr(worker, "Queue", lambda *_args, **_kwargs: object())
            monkeypatch.setattr(worker, "worker_class", lambda: FakeWorker)
            worker.main()
        assert_quiet()
        with caplog.at_level(logging.DEBUG):
            caplog.clear()
            for logger in loggers:
                logger.debug("private transport detail")
                logger.info("request URL must not be logged")
                logger.warning("upstream warning remains visible")
            assert [(record.name, record.levelno) for record in caplog.records] == [
                ("httpx", logging.WARNING),
                ("httpcore", logging.WARNING),
            ]
    finally:
        for logger, level in zip(loggers, previous, strict=True):
            logger.setLevel(level)


def test_the_collector_keeps_the_http_client_quiet() -> None:
    httpx_logger, httpcore_logger = logging.getLogger("httpx"), logging.getLogger("httpcore")
    before = (httpx_logger.level, httpcore_logger.level)
    try:
        scheduler.configure_logging()
        assert httpx_logger.level == logging.WARNING
        assert httpcore_logger.level == logging.WARNING
    finally:
        httpx_logger.setLevel(before[0])
        httpcore_logger.setLevel(before[1])
