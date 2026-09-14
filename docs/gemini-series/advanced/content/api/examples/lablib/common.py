"""Explicit clients, bounded inputs and durable author-owned resource records."""
import hashlib
import json
import os
import re
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def question(text):
    if not isinstance(text, str) or not text.strip() or len(text) > 1500:
        raise ValueError("question_required_max_1500_characters")
    return text.strip()


def https_url(value):
    if not isinstance(value, str) or any(ord(c) < 33 for c in value) or "\\" in value:
        raise ValueError("unsafe_url")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("unsafe_url")
    return value


def owned_name(value, prefix):
    if not isinstance(value, str) or not re.fullmatch(re.escape(prefix) + r"[A-Za-z0-9_-]+", value):
        raise ValueError("resource_name_outside_ledger")
    return value


def client_for(family, *, test_url=None):
    import httpx
    from google import genai
    from google.genai import types

    if family not in {"interactions", "generateContent"}:
        raise ValueError("unknown_api_family")
    if test_url is not None:
        if not re.fullmatch(r"http://127\.0\.0\.1:\d+", test_url):
            raise ValueError("test_transport_must_be_loopback")
        key = "fixture-not-a-real-key"
    else:
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("set_GEMINI_API_KEY_on_server")
    # SDK 2.23.0 retries an Interaction once even when attempts=0/1: constructor
    # normalization and its generated bridge disagree. Enforce one transmission
    # per explicit create call through the supported httpx_client request hook.
    guard = {"active": False, "sent": False}

    def before_request(request):
        if guard["active"] and request.method == "POST" and request.url.path.endswith("/interactions"):
            if guard["sent"]:
                raise ValueError("automatic_interaction_resend_prevented")
            guard["sent"] = True

    transport = httpx.Client(event_hooks={"request": [before_request]})
    options = types.HttpOptions(timeout=15000, retry_options=types.HttpRetryOptions(attempts=1), httpx_client=transport)
    if test_url:
        options.base_url = test_url
    sdk = genai.Client(api_key=key, http_options=options)

    class BoundedClient:
        def __getattr__(self, name):
            return getattr(sdk, name)

        def create(self, **kwargs):
            if guard["active"]:
                raise ValueError("single_user_client_not_concurrent")
            guard.update(active=True, sent=False)
            try:
                return sdk.interactions.create(**kwargs)
            finally:
                guard["active"] = False

        @property
        def interactions(self):
            return SimpleNamespace(create=self.create)

        def close(self):
            sdk.close()
            transport.close()

        def __enter__(self):
            return self

        def __exit__(self, *_):
            self.close()

    return BoundedClient()


def model_name():
    model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    if not re.fullmatch(r"gemini-[a-zA-Z0-9._-]+", model):
        raise ValueError("use_a_verified_model_id")
    return model


def serialized(reply):
    return reply if isinstance(reply, dict) else reply.model_dump(mode="json", exclude_none=True)


def text_blocks(reply):
    for step in serialized(reply).get("steps", []):
        if step.get("type") == "model_output":
            yield from (b for b in step.get("content", []) if b.get("type") == "text")
