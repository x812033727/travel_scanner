"""Option (a), offline half: the exact Jev request planned for writing day, and what the repo's
own estimate_tokens (apps/api/app/ai/jev.py, loaded verbatim) says it costs. No API is called.

State: the fictional sign-up email quoted in the public article ai-term-structured-outputs
(apps/api/app/guides/content/ai-term-structured-outputs.json, zh-TW block 13;
live at https://mokaair.com/zh-TW/life/ai-term-structured-outputs, HTTP 200 on 2026-10-03).
"""
import json
import re

from jevsrc import load

ns = load()
estimate_tokens = ns["estimate_tokens"]
USD = ns["USD_PER_INPUT_TOKEN"]
ChoiceQuestion, NoulQuestion = ns["ChoiceQuestion"], ns["NoulQuestion"]

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # the repository root
ARTICLE = ROOT / "apps/api/app/guides/content/ai-term-structured-outputs.json"
pack = json.load(open(ARTICLE, encoding="utf-8"))
blocks = pack["locales"]["zh-TW"]["blocks"]
para = blocks[13]["text"]
email = re.search(r"「(你好.*?)」", para).group(1)
assert email == "你好，我是王小美，想幫社團報名下週六的手作課，大概六個人。", email

# Our own English rendering of the same email, for the language comparison. Label it on screen as
# a Mokaair translation; the article itself has only zh-TW.
email_en = "Hi, I'm Wang Xiaomei. I'd like to sign my club up for the craft class next Saturday, about six people."

EVENT_DATE = ChoiceQuestion(
    instructions="How does the email say when the class is?",
    criteria={
        "calendar_date": "The email gives a calendar date for the class: a month and a day, with or without the year.",
        "relative_day": "The email names the day only relative to when it was written, such as next Saturday, and gives no month or day number.",
        "not_stated": "The email does not say when the class is.",
    },
)
# Same options in reverse order: jev-1.13 is documented to lean toward the first option.
EVENT_DATE_REVERSED = ChoiceQuestion(
    instructions=EVENT_DATE.instructions,
    criteria=dict(reversed(list(EVENT_DATE.criteria.items()))),
)
HEADCOUNT_IS_ESTIMATE = NoulQuestion(
    instructions="The email gives the number of people as an estimate rather than an exact count.",
    criteria={
        "true": "The number comes with a hedge such as about, around or roughly (大概, 左右, 約).",
        "false": "The number is stated as exact, or the email gives no number.",
    },
)
# Deliberately badly designed: no option is true and there is no way to say so.
EVENT_DATE_FORCED = ChoiceQuestion(
    instructions="On which date is the class?",
    criteria={
        "2026-10-10": "Saturday 10 October 2026",
        "2026-10-17": "Saturday 17 October 2026",
    },
)

core = {"event_date": EVENT_DATE, "headcount_is_estimate": HEADCOUNT_IS_ESTIMATE}
full = {**core, "event_date_reversed": EVENT_DATE_REVERSED, "event_date_forced": EVENT_DATE_FORCED}


def plan(state, questions):
    """The same arithmetic as JevClient._check_size: state plus every question's model_dump."""
    st = estimate_tokens(state)
    per_q = {k: estimate_tokens(q.model_dump(exclude_none=True)) for k, q in questions.items()}
    total = st + sum(per_q.values())
    return {"state_tokens": st, "question_tokens": per_q, "total_tokens": total,
            "usd": round(total * USD, 10), "calls_per_usd_cent": int(0.01 / (total * USD))}


def article_text(locale_blocks):
    parts = []
    for b in locale_blocks:
        for key in ("text", "code", "caption", "label"):
            if isinstance(b.get(key), str):
                parts.append(b[key])
        for key in ("items",):
            if isinstance(b.get(key), list):
                parts += [x for x in b[key] if isinstance(x, str)]
        if b.get("type") == "table":
            parts += [" | ".join(r) for r in [b.get("header", [])] + b.get("rows", [])]
    return "\n".join(parts)


whole = article_text(blocks)
out = lambda: {
    "email_zh": email,
    "email_chars": len(email),
    "email_en_mokaair_translation": email_en,
    "request_core_zh": plan(email, core),
    "request_full_zh": plan(email, full),
    "request_full_en": plan(email_en, full),
    "whole_article_as_state_core_questions": {**plan(whole, core), "article_chars": len(whole)},
    "probe_like_call_for_scale": plan("The sky is blue.", {"ok": NoulQuestion(instructions="The statement is true.")}),
    "usd_per_input_token": USD,
    "payload_full_zh": {"model": "jev-1.13.0", "state": email,
                        "questions": {k: q.model_dump(exclude_none=True) for k, q in full.items()}},
}
if __name__ == "__main__":
    print(json.dumps(out(), ensure_ascii=False, indent=1))
