// runlog.mjs: write a human-readable run log of every run (meta, prompt, every tool call and reply, the report left behind).
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
const L = new URL(".", import.meta.url).pathname;
const which = process.argv[2] ?? "runs";
const out = [];
const scrub = (s) => String(s).replaceAll(L, "<LAB>/");
for (const name of readdirSync(join(L, which)).sort()) {
  const dir = join(L, which, name);
  if (!existsSync(join(dir, "stream.jsonl")) || !existsSync(join(dir, "after.sha256"))) continue;
  out.push(`\n${"=".repeat(78)}\nRUN ${name}\n${"=".repeat(78)}`);
  out.push(scrub(readFileSync(join(dir, "meta.txt"), "utf8")).trim());
  out.push(`\n--- prompt (${name}/prompt.txt) ---\n${readFileSync(join(dir, "prompt.txt"), "utf8").trim()}`);
  out.push(`\n--- files before (sha256) ---\n${readFileSync(join(dir, "before.sha256"), "utf8").trim()}`);
  const lines = readFileSync(join(dir, "stream.jsonl"), "utf8").trim().split("\n").filter(Boolean).map((l) => JSON.parse(l));
  const init = lines.find((l) => l.type === "system" && l.subtype === "init") ?? {};
  out.push(`\n--- init ---\nmodel: ${init.model}\npermissionMode: ${init.permissionMode}\napiKeySource: ${init.apiKeySource}\nclaude_code_version: ${init.claude_code_version}\ntools: ${(init.tools ?? []).join(" ")}\nskills: ${(init.skills ?? []).join(" ")}\nplugins: ${(init.plugins ?? []).map((p) => p.name).join(" ")}\nmcp_servers: ${(init.mcp_servers ?? []).length}`);
  out.push(`\n--- transcript (assistant tool calls and text; tool results shortened to 400 chars) ---`);
  let n = 0, firstUsage = null;
  for (const l of lines) {
    if (l.type === "assistant") {
      const m = l.message ?? {};
      if (!firstUsage && m.usage) { firstUsage = m.usage; out.push(`[first request usage] input=${m.usage.input_tokens} cache_creation=${m.usage.cache_creation_input_tokens} cache_read=${m.usage.cache_read_input_tokens}`); }
      for (const c of m.content ?? []) {
        if (c.type === "tool_use") out.push(`[${++n}] TOOL ${c.name} ${scrub(JSON.stringify(c.input))}`);
        else if (c.type === "text" && c.text.trim()) out.push(`[${++n}] TEXT\n${scrub(c.text).trim()}`);
      }
    } else if (l.type === "user") {
      for (const c of l.message?.content ?? []) {
        if (c && typeof c === "object" && c.type === "tool_result") {
          const body = typeof c.content === "string" ? c.content : JSON.stringify(c.content);
          out.push(`    RESULT${c.is_error ? " (error)" : ""}: ${scrub(body).slice(0, 400).replaceAll("\n", "\\n")}${body.length > 400 ? " …" : ""}`);
        }
      }
    } else if (l.type === "result") {
      out.push(`\n--- result ---\nsubtype: ${l.subtype}\nnum_turns: ${l.num_turns}\ntotal_cost_usd: ${l.total_cost_usd}\nduration_ms: ${l.duration_ms}\npermission_denials: ${JSON.stringify(l.permission_denials ?? []).slice(0, 600)}\nmodelUsage: ${Object.keys(l.modelUsage ?? {}).join(" ")}`);
    }
  }
  const report = join(dir, "lab", "reports", "2026-09.md");
  out.push(`\n--- reports/2026-09.md after the run ---\n${existsSync(report) ? readFileSync(report, "utf8") : "(no file)"}`);
  out.push(`\n--- files after (sha256, .claude/ excluded) ---\n${readFileSync(join(dir, "after.sha256"), "utf8").trim()}`);
}
process.stdout.write(out.join("\n") + "\n");
