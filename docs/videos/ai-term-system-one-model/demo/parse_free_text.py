"""Option (a), the generating-model half. The same two questions asked as free text; this file
holds the prompt and a strict parser. On writing day: send PROMPT to the generating model the
site already uses, N times (default 10), save the raw replies verbatim as a JSON list in
replies.json, then run `python3 parse_free_text.py replies.json`. It reports which replies a
program could read and why the others failed. Nothing here calls a model.

Self-test (`python3 parse_free_text.py --selftest`) runs on HAND-WRITTEN FIXTURES that only check
the parser; they are not model output and must never be shown as such.
"""
import json
import re
import sys

EMAIL = "你好，我是王小美，想幫社團報名下週六的手作課，大概六個人。"
PROMPT = (
    f"下面是一封報名信：「{EMAIL}」\n"
    "1. 信裡怎麼寫活動日期？從 A 寫了月和日、B 只說相對的日子（例如下週六）、C 沒寫，三個選一個。\n"
    "2. 信裡的人數是估計的嗎？回答是或否。\n"
    "每一題都附上 0 到 1 之間的把握。"
)

# What the code card shows (each line <= 64 characters, <= 16 lines).
CODE_CARD = '''NUM = r"(?<![\\d.])(?:0?\\.\\d+|1\\.0+|[01])(?![\\d.%])"
m1 = re.search(r"1[.、:：]\\s*\\(?([ABC])\\b", reply)
m2 = re.search(r"2[.、:：]\\s*(是|否)", reply)
p = re.findall(NUM, reply)
if not (m1 and m2 and len(p) == 2):
    raise ValueError("讀不懂，交給人")'''


def parse(reply: str):
    m1 = re.search(r"1[.、:：]\s*\(?([ABC])\b", reply)
    m2 = re.search(r"2[.、:：]\s*(是|否)", reply)
    p = re.findall(r"(?<![\d.])(?:0?\.\d+|1\.0+|[01])(?![\d.%])", reply)
    problems = []
    if not m1:
        problems.append("no A/B/C for question 1")
    if not m2:
        problems.append("no 是/否 for question 2")
    if len(p) != 2:
        problems.append(f"expected 2 numbers between 0 and 1, found {len(p)}")
    if re.search(r"\d{4}\s*年|\d{1,2}\s*月\s*\d{1,2}\s*日|\d{4}-\d{2}-\d{2}", reply):
        problems.append("reply contains a calendar date the email never gave")
    return {"ok": not problems, "date": m1 and m1.group(1), "estimate": m2 and m2.group(1),
            "numbers": p, "problems": problems}


if __name__ == "__main__":
    for line in CODE_CARD.splitlines():
        assert len(line) <= 64, (len(line), line)
    if sys.argv[1:] == ["--selftest"]:
        fixtures = [  # HAND-WRITTEN parser fixtures, NOT model output
            "1. B（把握 0.9）\n2. 是（把握 0.8）",
            "1. B，把握 90%\n2. 是，把握 85%",
            "活動日期應該是下週六，也就是 10 月 10 日。人數大約六人，是估計值。",
        ]
        print(json.dumps([parse(f) for f in fixtures], ensure_ascii=False, indent=1))
    elif sys.argv[1:]:
        replies = json.load(open(sys.argv[1], encoding="utf-8"))
        results = [parse(r) for r in replies]
        print(json.dumps({"n": len(results), "readable": sum(r["ok"] for r in results), "results": results},
                         ensure_ascii=False, indent=1))
    else:
        print(PROMPT)
