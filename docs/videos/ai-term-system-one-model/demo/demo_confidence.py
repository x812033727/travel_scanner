"""Option (b): TypeSafe's documented confidence formulas, computed exactly.

Source: https://docs.typesafe.ai/confidence.md, section "How confidence is calculated"
(fetched 2026-10-03, HTTP 200, byte-identical to the copy in scratchpad/src/ts-confidence.md).
  Noul:   confidence = |2p - 1|
  Choice: confidence = (p_max - 1/n) / (1 - 1/n)
  Score:  max(0, 1 - sum_i p_i |i - m| / MAD_unif),  MAD_unif = (1/n) sum_i |i - (n-1)/2|
Exact arithmetic with Fraction so the printed numbers are not float artefacts.
"""
import json
from fractions import Fraction as F

from jevsrc import load


def choice_conf(ps):
    n = len(ps)
    assert sum(ps) == 1, ps
    return (max(ps) - F(1, n)) / (1 - F(1, n))


def noul_conf(p):
    return abs(2 * p - 1)


def score_conf(ps):
    n = len(ps)
    m = ps.index(max(ps))
    spread = sum(p * abs(i - m) for i, p in enumerate(ps))
    even = sum(abs(F(i) - F(n - 1, 2)) for i in range(n)) / n
    return max(F(0), 1 - spread / even)


def pmax_for(conf, n):
    """Inverse of the Choice formula: the top probability that yields `conf` with n options."""
    return conf * (1 - F(1, n)) + F(1, n)


def show(x):
    return {"exact": str(x), "decimal": round(float(x), 4)}


out = {"source": "https://docs.typesafe.ai/confidence.md (opened 2026-10-03)"}

# 1. Choice examples asked for in the brief
ten = [F(1, 2)] + [F(1, 18)] * 9          # 10 options, top 0.5, rest spread evenly
ten_skew = [F(1, 2), F(4, 10)] + [F(1, 80)] * 8  # 10 options, top 0.5, runner-up 0.4
choice_cases = {
    "3 options (0.6, 0.3, 0.1)": [F(6, 10), F(3, 10), F(1, 10)],
    "3 options (0.6, 0.2, 0.2)": [F(6, 10), F(2, 10), F(2, 10)],
    "2 options (0.9, 0.1)": [F(9, 10), F(1, 10)],
    "10 options, top 0.5, other nine 0.0556 each": ten,
    "10 options, top 0.5, runner-up 0.4, other eight 0.0125 each": ten_skew,
}
out["choice"] = {}
for name, ps in choice_cases.items():
    second = sorted(ps)[-2]
    out["choice"][name] = {
        "confidence": show(choice_conf(ps)),
        "top_probability": show(max(ps)),
        "top_to_second_ratio": show(max(ps) / second),
    }

# 2. Noul |2p - 1|
out["noul_abs_2p_minus_1"] = {str(p): show(noul_conf(F(p))) for p in ["0.5", "0.9", "0.97", "0.03", "0.66", "0.38"]}

# 3. Where does "confidence 0.4" come from? Same confidence, different top probability by n.
out["confidence_0.4_means_top_probability"] = {f"n={n}": show(pmax_for(F(2, 5), n)) for n in (2, 3, 4, 5, 10, 32, 255)}

# 4. What the site's default thresholds (jev_act_confidence 0.9, jev_flag_confidence 0.5,
#    apps/api/app/config.py:519-520) demand of the top probability, by number of options.
out["site_thresholds_as_top_probability"] = {
    f"n={n}": {"act_0.9": show(pmax_for(F(9, 10), n)), "flag_0.5": show(pmax_for(F(1, 2), n))}
    for n in (2, 3, 4, 5, 10, 32)
}

# 5. Score: the doc's own example and the two three-level cases it contrasts.
out["score"] = {
    "(0, 0.57, 0.43) doc example": show(score_conf([F(0), F(57, 100), F(43, 100)])),
    "(0, 0.5, 0.5) torn between neighbours": show(score_conf([F(0), F(1, 2), F(1, 2)])),
    "(0.5, 0, 0.5) torn between ends": show(score_conf([F(1, 2), F(0), F(1, 2)])),
    "choice formula on (0, 0.5, 0.5)": show(choice_conf([F(0), F(1, 2), F(1, 2)])),
}

# 6. The site's own router, loaded verbatim from apps/api/app/ai/jev.py, on the same numbers.
ns = load()
ChoiceAnswer, NoulAnswer, route = ns["ChoiceAnswer"], ns["NoulAnswer"], ns["route"]
rows = []
for label, ans in [
    ("choice (0.6,0.3,0.1) -> confidence 0.4", ChoiceAnswer(type="choice", choice="a", confidence=0.4,
                                                            probabilities={"a": .6, "b": .3, "c": .1})),
    ("choice 2-opt (0.9,0.1) -> confidence 0.8", ChoiceAnswer(type="choice", choice="a", confidence=0.8)),
    ("choice 3-opt top 0.95 -> confidence 0.925", ChoiceAnswer(type="choice", choice="a", confidence=0.925)),
    ("noul 0.97", NoulAnswer(type="noul", noul=0.97)),
    ("noul 0.90 (same 90% yes as the 2-option choice above)", NoulAnswer(type="noul", noul=0.90)),
    ("noul 0.66", NoulAnswer(type="noul", noul=0.66)),
    ("noul 0.38", NoulAnswer(type="noul", noul=0.38)),
    ("noul 0.03 (a confident NO)", NoulAnswer(type="noul", noul=0.03)),
]:
    rows.append({
        "answer": label,
        "en": route(ans, act_at=0.9, flag_at=0.5, locale="en"),
        "zh-TW (cjk_autopilot off, the default)": route(ans, act_at=0.9, flag_at=0.5, locale="zh-TW"),
        "zh-TW (cjk_autopilot on)": route(ans, act_at=0.9, flag_at=0.5, locale="zh-TW", cjk_autopilot=True),
    })
out["site_route_with_default_thresholds_0.9_0.5"] = rows

print(json.dumps(out, ensure_ascii=False, indent=1))
