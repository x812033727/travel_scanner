// tally.mjs: score every run in runs/ from its stream and the files it left.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
const L = new URL(".", import.meta.url).pathname;
const EXPECTED = JSON.parse(readFileSync(join(L, "expected.json"), "utf8"));
const fmt = (n) => n.toLocaleString("en-US");
function score(name) {
  const dir = join(L, "runs", name);
  if (!existsSync(join(dir, "stream.jsonl"))) return null;
  const meta = readFileSync(join(dir, "meta.txt"), "utf8");
  const arm = /arm: (\w+)/.exec(meta)[1];
  const lines = readFileSync(join(dir, "stream.jsonl"), "utf8").trim().split("\n").filter(Boolean).map((l) => JSON.parse(l));
  const init = lines.find((l) => l.type === "system" && l.subtype === "init") ?? {};
  const result = lines.find((l) => l.type === "result") ?? {};
  const calls = [];
  let firstUsage = null, lastText = "";
  for (const l of lines) {
    if (l.type !== "assistant") continue;
    const m = l.message ?? {};
    if (!firstUsage && m.usage) firstUsage = m.usage;
    for (const c of m.content ?? []) {
      if (c.type === "tool_use") calls.push({ name: c.name, input: c.input });
      if (c.type === "text" && c.text.trim()) lastText = c.text;
    }
  }
  const skillCalls = calls.filter((c) => c.name === "Skill" && JSON.stringify(c.input).includes("monthly-report"));
  const readSkill = calls.filter((c) => ["Read", "Glob", "Grep"].includes(c.name) && JSON.stringify(c.input).includes("SKILL.md"));
  const ranScript = calls.filter((c) => c.name === "Bash" && String(c.input.command).includes("sum.mjs"));
  const reportPath = join(dir, "lab", "reports", "2026-09.md");
  const report = existsSync(reportPath) ? readFileSync(reportPath, "utf8") : null;
  const replyLast = lastText.trim().split("\n").filter((x) => x.trim()).pop() ?? "";
  const f = {
    F1_file: !!report,
    F2_title: !!report && report.split("\n")[0].trim() === "# 2026 年 9 月 月結報表",
    F3_total: !!report && report.includes(fmt(EXPECTED.total)),
    F4_returns: !!report && EXPECTED.returns.every((r) => report.includes(r)),
    F5_large: !!report && EXPECTED.large.every((r) => report.includes(r)),
    F6_lastline: /報表已寫到 reports\/2026-09\.md[，,]\s*總營收 85,290 元[。.]?$/.test(replyLast.replace(/[*_`>]/g, "").trim()),
  };
  const wrongTotal = report ? [...report.matchAll(/總營收[^\d]*([\d,]+)/g)].map((m) => m[1]).filter((x) => x !== fmt(EXPECTED.total)) : [];
  const first = firstUsage ? (firstUsage.input_tokens ?? 0) + (firstUsage.cache_creation_input_tokens ?? 0) + (firstUsage.cache_read_input_tokens ?? 0) : null;
  return {
    name, arm, model: init.model, skills: init.skills, permissionMode: init.permissionMode,
    skillCalled: skillCalls.length, skillInput: skillCalls[0]?.input ?? null, readSkillMd: readSkill.length, ranScript: ranScript.length,
    calls: calls.map((c) => c.name).join(" "), ...f, steps: Object.values(f).filter(Boolean).length, wrongTotal,
    firstRequestTokens: first, turns: result.num_turns, cost: result.total_cost_usd, subtype: result.subtype, denials: (result.permission_denials ?? []).length,
    replyLast,
  };
}
const names = readdirSync(join(L, "runs")).sort();
const rows = names.map(score).filter(Boolean);
console.log(JSON.stringify(rows, null, 2));
console.log("\nname arm | skillCalled readSKILL ranScript | F1 F2 F3 F4 F5 F6 steps | first_tokens turns cost");
for (const r of rows) console.log(`${r.name} ${r.arm} | ${r.skillCalled} ${r.readSkillMd} ${r.ranScript} | ${[r.F1_file, r.F2_title, r.F3_total, r.F4_returns, r.F5_large, r.F6_lastline].map((x) => (x ? "Y" : "n")).join(" ")} ${r.steps} | ${r.firstRequestTokens} ${r.turns} ${r.cost?.toFixed(3)} ${r.subtype} denials=${r.denials}`);
