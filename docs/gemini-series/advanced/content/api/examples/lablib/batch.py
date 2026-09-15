"""Stable-key batch accounting; a plan is never a submission or a billing receipt."""
import json
import uuid
from pathlib import Path

from .common import digest, owned_name, read_json, serialized, write_json


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def reconcile(cases, results):
    keys = [c["key"] for c in cases]
    if len(set(keys)) != len(keys) or any(not isinstance(k, str) or not k for k in keys):
        raise ValueError("duplicate_or_invalid_case_key")
    seen, accepted, retryable, failed = set(), {}, [], []
    for row in results:
        key = row.get("key")
        if key not in keys or key in seen:
            raise ValueError("unknown_or_duplicate_result_key")
        seen.add(key)
        if row.get("response") and not row.get("error"):
            response = row["response"]
            candidates = response.get("candidates", [])
            text = "\n".join(p.get("text", "") for c in candidates for p in c.get("content", {}).get("parts", []))
            reasons = {c.get("finishReason", c.get("finish_reason")) for c in candidates}
            if text and reasons == {"STOP"}:
                accepted[key] = {"text": text, "usage": response.get("usageMetadata", response.get("usage_metadata"))}
            else:
                failed.append({"key": key, "reason": "blocked_truncated_or_empty_review_manually"})
        elif row.get("error") and not row.get("response"):
            code = row["error"].get("code")
            status = row["error"].get("status")
            if code in {429, 500, 502, 503, 504} or status in {"RESOURCE_EXHAUSTED", "UNAVAILABLE", "INTERNAL"}:
                retryable.append(key)
            else:
                failed.append({"key": key, "reason": "permanent_or_unknown_error"})
        else:
            failed.append({"key": key, "reason": "ambiguous_result"})
    return {"accepted": accepted, "retryable": retryable, "failed": failed, "missing": sorted(set(keys)-seen), "note": "missing items require job/result reconciliation, not automatic retry"}


def retry_cases(cases, summary, *, attempts=1):
    if type(attempts) is not int or not 1 <= attempts < 3:
        raise ValueError("retry_budget_exhausted")
    accepted = set(summary["accepted"])
    retry = set(summary["retryable"])
    if accepted & retry:
        raise ValueError("accepted_key_cannot_retry")
    return [c for c in cases if c["key"] in retry]


def merge_accepted(cases, summaries):
    reconcile(cases, [])
    keys = {c["key"] for c in cases}
    adopted = {}
    for index, summary in enumerate(summaries):
        for key, answer in summary["accepted"].items():
            if key not in keys or key in adopted:
                raise ValueError("unknown_or_already_adopted_key")
            adopted[key] = {**answer, "source_summary": index}
    return {"accepted": adopted, "unresolved": sorted(keys-adopted.keys()), "quality": "answers_still_require_gold_and_citation_review"}


def submit(client, cases_path, ledger_path, model, *, parent_ledger=None):
    path = Path(ledger_path)
    if path.exists():
        raise ValueError("existing_job_ledger_reconcile_not_resubmit")
    cases = jsonl(cases_path)
    if not cases or len(cases) > 20:
        raise ValueError("expected_1_to_20_cases")
    reconcile(cases, [])
    attempt = 1
    if parent_ledger:
        parent = read_json(parent_ledger)
        if parent.get("owner") != "gemini-batch-lab" or parent.get("remote_state") != "JOB_STATE_SUCCEEDED":
            raise ValueError("parent_job_not_reconciled")
        if digest(parent["input_path"]) != parent["input_sha256"] or digest(parent["output_path"]) != parent["output_sha256"]:
            raise ValueError("parent_files_changed")
        expected = retry_cases(jsonl(parent["input_path"]), reconcile(jsonl(parent["input_path"]), jsonl(parent["output_path"])), attempts=parent["attempt"])
        if cases != expected or model != parent["model"]:
            raise ValueError("retry_must_match_verified_transient_failures")
        attempt = parent["attempt"]+1
    ledger = {"owner": "gemini-batch-lab", "display_name": "batch-teaching-"+uuid.uuid4().hex[:12], "model": model, "attempt": attempt, "parent_ledger": str(Path(parent_ledger).resolve()) if parent_ledger else None, "input_path": str(Path(cases_path).resolve()), "input_sha256": digest(cases_path), "keys": [c["key"] for c in cases], "state": "upload_uncertain", "input_file": None, "job": None}
    with path.open("x", encoding="utf-8") as stream:
        json.dump(ledger, stream, ensure_ascii=False, indent=2)
    upload = client.files.upload(file=Path(cases_path), config={"display_name": ledger["display_name"], "mime_type": "application/jsonl"})
    ledger.update(input_file=owned_name(upload.name, "files/"), state="submission_uncertain")
    write_json(path, ledger)
    job = client.batches.create(model=model, src=upload.name, config={"display_name": ledger["display_name"]})
    ledger.update(job=owned_name(job.name, "batches/"), state="submitted")
    write_json(path, ledger)
    return ledger


def fetch(client, ledger_path, output_path):
    ledger = read_json(ledger_path)
    if ledger.get("owner") != "gemini-batch-lab":
        raise ValueError("not_this_exercise")
    job = client.batches.get(name=owned_name(ledger.get("job"), "batches/"))
    state = getattr(job.state, "name", str(job.state))
    ledger["remote_state"] = state
    ledger["job_metadata"] = serialized(job)
    write_json(ledger_path, ledger)
    if state != "JOB_STATE_SUCCEEDED":
        return {"state": state, "downloaded": False}
    if not job.dest or not job.dest.file_name:
        raise ValueError("missing_result_file_reconcile")
    ledger["output_file"] = owned_name(job.dest.file_name, "files/")
    write_json(ledger_path, ledger)
    data = client.files.download(file=job.dest.file_name)
    Path(output_path).write_bytes(data)
    ledger["output_sha256"] = digest(output_path)
    ledger["output_path"] = str(Path(output_path).resolve())
    write_json(ledger_path, ledger)
    return {"state": state, "downloaded": True}


def cleanup(client, ledger_path):
    ledger = read_json(ledger_path)
    if ledger.get("owner") != "gemini-batch-lab" or ledger.get("remote_state") not in {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}:
        raise ValueError("reconcile_terminal_job_before_cleanup")
    for field, api, prefix in [("job", client.batches, "batches/"), ("input_file", client.files, "files/"), ("output_file", client.files, "files/")]:
        if ledger.get(field) and not ledger.get(field+"_deleted"):
            try:
                api.delete(name=owned_name(ledger[field], prefix))
            except Exception as error:
                if getattr(error, "code", None) != 404:
                    raise
            ledger[field+"_deleted"] = True
            write_json(ledger_path, ledger)
    ledger["state"] = "cleaned"
    write_json(ledger_path, ledger)
    return {"state": "cleaned", "billing": "verify_separately"}
