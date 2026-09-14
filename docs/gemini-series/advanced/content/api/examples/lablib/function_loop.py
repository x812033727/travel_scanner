"""Manual stateless Interactions loop with a single read-only allowlisted tool."""
import json
import re
import time

from .common import question, serialized, text_blocks

TOOL = {
    "type": "function", "name": "lookup_order", "description": "Read one synthetic order; never change it.",
    "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"], "additionalProperties": False},
}


def lookup(name, arguments, orders):
    if name != "lookup_order":
        return {"error": "tool_not_allowed"}
    if not isinstance(arguments, dict) or set(arguments) != {"order_id"}:
        return {"error": "invalid_arguments"}
    order_id = arguments["order_id"]
    if not isinstance(order_id, str) or not re.fullmatch(r"DEMO-\d{3}", order_id):
        return {"error": "invalid_order_id"}
    record = orders.get(order_id)
    return {"found": False, "order_id": order_id} if record is None else {"found": True, "order_id": order_id, "order": record}


def run(create, prompt, orders, model, *, max_requests=3, clock=time.monotonic):
    if type(max_requests) is not int or not 1 <= max_requests <= 5:
        raise ValueError("max_requests_1_to_5")
    history = [{"type": "user_input", "content": [{"type": "text", "text": question(prompt)}]}]
    trace, seen = [], set()
    deadline = clock() + 45
    for turn in range(max_requests):
        if clock() >= deadline:
            return {"status": "deadline", "trace": trace}
        reply = serialized(create(model=model, input=history, tools=[TOOL], store=False, timeout=min(15, deadline-clock())))
        steps = reply.get("steps", [])
        trace.append({"request": turn+1, "interaction_id": reply.get("id"), "status": reply.get("status"), "usage": reply.get("usage"), "tool_results": []})
        calls = [s for s in steps if s.get("type") == "function_call"]
        if not calls:
            answer = "\n".join(b.get("text", "") for b in text_blocks(reply))
            return {"status": "answered" if answer and reply.get("status") == "completed" else "no_answer", "answer": answer, "trace": trace}
        if turn + 1 == max_requests:
            return {"status": "request_limit", "trace": trace}  # Do not execute tools whose result cannot be returned.
        ids = [s.get("id") for s in calls]
        if len(calls) > 4 or any(not isinstance(i, str) or not i for i in ids) or any(not isinstance(c.get("name"), str) or not c["name"] for c in calls) or len(set(ids)) != len(ids) or seen.intersection(ids):
            return {"status": "invalid_call_ids_or_count", "trace": trace}
        if reply.get("status") not in {"completed", "requires_action"}:
            return {"status": "unexpected_status", "trace": trace}
        history.extend(steps)  # Preserve thought signatures and every model step exactly.
        for call in calls:
            seen.add(call["id"])
            result = lookup(call.get("name"), call.get("arguments"), orders)
            trace[-1]["tool_results"].append({"call_id": call["id"], "result": result})
            history.append({"type": "function_result", "name": call.get("name"), "call_id": call["id"], "result": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]})
    raise AssertionError("unreachable")
