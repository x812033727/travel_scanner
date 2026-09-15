"""Single-user resource ledger. Mutations stop after uncertain outcomes; no blind retries."""
import time
import uuid
from pathlib import Path

from .common import digest, owned_name, read_json, serialized, write_json


def create_store(client, ledger_path):
    path = Path(ledger_path)
    if path.exists():
        raise ValueError("ledger_exists_reconcile_before_create")
    ledger = {"owner": "gemini-api-lab", "display_name": "teaching-"+uuid.uuid4().hex[:12], "state": "create_uncertain", "store": None, "documents": []}
    # Exclusive initial creation prevents a second local submit using the same ledger.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        import json
        json.dump(ledger, stream, ensure_ascii=False, indent=2)
    store = client.file_search_stores.create(config={"display_name": ledger["display_name"], "embedding_model": "models/gemini-embedding-2"})
    ledger.update(store=owned_name(store.name, "fileSearchStores/"), state="ready")
    write_json(path, ledger)
    return ledger


def load_ledger(path):
    ledger = read_json(path)
    if ledger.get("owner") != "gemini-api-lab" or ledger.get("state") not in {"ready", "cleanup_pending"}:
        raise ValueError("ledger_not_ready_reconcile")
    owned_name(ledger.get("store"), "fileSearchStores/")
    return ledger


def import_document(client, ledger_path, file, document_id, version):
    ledger = load_ledger(ledger_path)
    if ledger["state"] != "ready":
        raise ValueError("cleanup_in_progress")
    if any(d["id"] == document_id and d["version"] == version for d in ledger["documents"]):
        raise ValueError("version_already_recorded_reconcile")
    file = Path(file)
    display = f"{document_id}-{version}.txt"
    entry = {"id": document_id, "version": version, "display_name": display, "sha256": digest(file), "local_file": str(file.resolve()), "status": "upload_uncertain", "raw_file": None, "operation": None, "document": None}
    ledger["documents"].append(entry)
    write_json(ledger_path, ledger)
    raw = client.files.upload(file=file, config={"display_name": display, "mime_type": "text/plain"})
    entry.update(raw_file=owned_name(raw.name, "files/"), status="import_uncertain")
    write_json(ledger_path, ledger)
    operation = client.file_search_stores.import_file(file_search_store_name=ledger["store"], file_name=raw.name, config={"custom_metadata": [{"key": "document_id", "string_value": document_id}, {"key": "version", "string_value": version}]})
    entry.update(operation=serialized(operation), status="pending")
    write_json(ledger_path, ledger)
    return entry


def poll_document(client, ledger_path, document_id, version, *, polls=3, pause=time.sleep):
    from google.genai import types
    if type(polls) is not int or not 1 <= polls <= 6:
        raise ValueError("bounded_polls_required")
    ledger = load_ledger(ledger_path)
    entry = next(d for d in ledger["documents"] if d["id"] == document_id and d["version"] == version)
    if entry["status"] != "pending":
        raise ValueError("operation_not_pending")
    operation = types.ImportFileOperation.model_validate(entry["operation"])
    for attempt in range(polls):
        if not operation.done:
            operation = client.operations.get(operation)
            entry["operation"] = serialized(operation)
            write_json(ledger_path, ledger)
        if operation.done:
            if operation.error:
                entry.update(status="import_failed", error=serialized(operation).get("error"))
            elif operation.response and operation.response.document_name:
                name = owned_name(operation.response.document_name, ledger["store"]+"/documents/")
                entry.update(document=name, status="indexed_pending_review")
            else:
                entry.update(status="missing_document_id")
            write_json(ledger_path, ledger)
            return entry
        if attempt+1 < polls:
            pause(1)
    return entry  # Resume this exact operation later; don't upload again.


def delete_document(client, ledger_path, document_id, version):
    ledger = load_ledger(ledger_path)
    entry = next(d for d in ledger["documents"] if d["id"] == document_id and d["version"] == version)
    name = owned_name(entry.get("document"), ledger["store"]+"/documents/")
    entry["status"] = "delete_uncertain"
    write_json(ledger_path, ledger)
    client.file_search_stores.documents.delete(name=name, config={"force": True})
    remaining = {d.name for d in client.file_search_stores.documents.list(parent=ledger["store"])}
    if name in remaining:
        raise ValueError("deleted_document_still_listed")
    entry["status"] = "deleted_from_index"
    write_json(ledger_path, ledger)
    return entry


def query_store(client, ledger_path, prompt, model):
    from .common import question
    ledger = load_ledger(ledger_path)
    active = [d for d in ledger["documents"] if d["status"] == "indexed_pending_review"]
    if ledger["state"] != "ready" or any(d["status"] not in {"indexed_pending_review", "deleted_from_index"} for d in ledger["documents"]):
        raise ValueError("index_changes_unresolved")
    if not active or len({d["id"] for d in active}) != len(active):
        raise ValueError("one_current_version_per_document_required")
    return client.interactions.create(model=model, input=question(prompt), tools=[{"type": "file_search", "file_search_store_names": [ledger["store"]]}], store=False, timeout=15)


def cleanup(client, ledger_path):
    ledger = load_ledger(ledger_path)
    ledger["state"] = "cleanup_pending"
    write_json(ledger_path, ledger)
    if not ledger.get("store_deleted"):
        try:
            client.file_search_stores.delete(name=ledger["store"], config={"force": True})
        except Exception as error:
            if getattr(error, "code", None) != 404:
                raise
        ledger["store_deleted"] = True
        write_json(ledger_path, ledger)
    for entry in ledger["documents"]:
        if entry["raw_file"] and not entry.get("raw_deleted"):
            try:
                client.files.delete(name=owned_name(entry["raw_file"], "files/"))
            except Exception as error:
                if getattr(error, "code", None) != 404:
                    raise
            entry["raw_deleted"] = True
            write_json(ledger_path, ledger)
    ledger["state"] = "cleaned"
    write_json(ledger_path, ledger)
