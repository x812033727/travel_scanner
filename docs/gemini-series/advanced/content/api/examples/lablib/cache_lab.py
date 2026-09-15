"""Two API families, observed token usage, and explicit cache ownership."""
import time

from .common import digest, owned_name, read_json, serialized, write_json


def usage(reply, family):
    data = serialized(reply)
    if family == "interactions":
        raw = data.get("usage") or {}
        fields = ("total_input_tokens", "total_cached_tokens", "total_output_tokens", "total_thought_tokens")
    elif family == "generateContent":
        raw = data.get("usage_metadata") or {}
        fields = ("prompt_token_count", "cached_content_token_count", "candidates_token_count", "thoughts_token_count")
    else:
        raise ValueError("unknown_api_family")
    values = [raw.get(k) for k in fields]
    if any(v is not None and (type(v) is not int or v < 0) for v in values):
        raise ValueError("invalid_usage")
    prompt, cached, output, thoughts = values
    if prompt is not None and cached is not None and cached > prompt:
        raise ValueError("cached_exceeds_input")
    return {"family": family, "input": prompt, "cached": cached, "output": output, "thoughts": thoughts, "cache_hit_observed": None if cached is None else cached > 0, "bill": "not_measured"}


def implicit(client, document_path, questions, model, output_path):
    document = document_path.read_text(encoding="utf-8")
    result = {"model": model, "document_sha256": digest(document_path), "family": "interactions", "baseline": "first_observation_not_guaranteed_cache_miss", "rows": []}
    for prompt in questions[:3]:
        reply = client.interactions.create(model=model, input=document+"\n\n問題："+prompt, store=False, timeout=15)
        result["rows"].append({"question": prompt, "observed_at": time.time(), "usage": usage(reply, "interactions")})
        write_json(output_path, result)
    return result


def explicit_create(client, document_path, model, ledger_path):
    from google.genai import types
    if ledger_path.exists():
        raise ValueError("cache_ledger_exists_reconcile")
    ledger = {"owner": "gemini-cache-lab", "model": model, "document_sha256": digest(document_path), "state": "create_uncertain", "cache": None}
    with ledger_path.open("x", encoding="utf-8") as stream:
        import json
        json.dump(ledger, stream)
    cache = client.caches.create(model=model, config=types.CreateCachedContentConfig(contents=[document_path.read_text(encoding="utf-8")], ttl="300s"))
    ledger.update(cache=owned_name(cache.name, "cachedContents/"), state="created", created=serialized(cache), observed_at=time.time())
    write_json(ledger_path, ledger)
    return ledger


def explicit_query(client, ledger_path, prompt):
    from google.genai import types
    ledger = read_json(ledger_path)
    if ledger.get("owner") != "gemini-cache-lab" or ledger.get("state") != "created":
        raise ValueError("cache_not_ready")
    reply = client.models.generate_content(model=ledger["model"], contents=prompt, config=types.GenerateContentConfig(cached_content=owned_name(ledger["cache"], "cachedContents/"), automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
    return {**usage(reply, "generateContent"), "model": ledger["model"], "document_sha256": ledger["document_sha256"], "cache": ledger["cache"], "question": prompt, "observed_at": time.time()}


def explicit_delete(client, ledger_path):
    ledger = read_json(ledger_path)
    if ledger.get("owner") != "gemini-cache-lab":
        raise ValueError("not_this_cache_exercise")
    client.caches.delete(name=owned_name(ledger.get("cache"), "cachedContents/"))
    ledger["state"] = "deleted"
    write_json(ledger_path, ledger)
