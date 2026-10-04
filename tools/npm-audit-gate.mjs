#!/usr/bin/env node
// The daily npm audit's verdict: `npm audit --json` on stdin, exit 1 when an advisory at high
// severity or above is not exempted in tools/npm-audit-allow.json. An exemption names one advisory
// of one package, says why, and carries a review date after which it stops counting, so a red run
// means something new again while an advisory without a fix is being waited on.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const BLOCKING = new Set(["high", "critical"]);
const ADVISORY = /GHSA(?:-[23456789cfghjmpqrvwx]{4}){3}/;

/** The advisories themselves: a package's `via` lists either an advisory or the name of the
 * dependency that carries one, and only the first kind is a finding. */
export function findings(report) {
  if (!report || typeof report.vulnerabilities !== "object" || report.vulnerabilities === null) {
    throw new Error(`npm audit gave no report${report?.error ? `: ${report.error.summary ?? report.error.code}` : ""}`);
  }
  const found = new Map();
  for (const [name, entry] of Object.entries(report.vulnerabilities)) {
    for (const via of entry.via ?? []) {
      if (typeof via !== "object" || !BLOCKING.has(via.severity)) continue;
      const advisory = ADVISORY.exec(via.url ?? "")?.[0] ?? String(via.source ?? via.url);
      found.set(`${name} ${advisory}`, { package: name, advisory, severity: via.severity, title: via.title ?? "", url: via.url ?? "" });
    }
  }
  return [...found.values()];
}

export function allowProblems(allow) {
  if (!Array.isArray(allow)) return ["the allow list is not an array"];
  const problems = [];
  for (const [index, entry] of allow.entries()) {
    const where = `entry ${index + 1}`;
    if (!ADVISORY.test(entry?.advisory ?? "")) problems.push(`${where}: advisory is not a GHSA id`);
    if (typeof entry?.package !== "string" || !entry.package) problems.push(`${where}: no package`);
    if (typeof entry?.reason !== "string" || entry.reason.length < 40) problems.push(`${where}: the reason says too little`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(entry?.review_by ?? "") || Number.isNaN(Date.parse(entry.review_by))) problems.push(`${where}: review_by is not a date`);
  }
  return problems;
}

/** `today` is a YYYY-MM-DD string; an exemption counts through its review date. */
export function verdict(report, allow, today) {
  const problems = allowProblems(allow);
  if (problems.length) return { ok: false, blocking: [], exempted: [], expired: [], unused: [], problems };
  const all = findings(report);
  const match = (finding) => allow.find((entry) => entry.advisory === finding.advisory && entry.package === finding.package);
  const exempted = all.filter((finding) => match(finding) && match(finding).review_by >= today);
  const expired = all.filter((finding) => match(finding) && match(finding).review_by < today);
  const blocking = all.filter((finding) => !match(finding));
  const unused = allow.filter((entry) => !all.some((finding) => finding.advisory === entry.advisory && finding.package === entry.package));
  return { ok: blocking.length === 0 && expired.length === 0, blocking, exempted, expired, unused, problems: [] };
}

function main() {
  const allowFile = fileURLToPath(new URL("./npm-audit-allow.json", import.meta.url));
  const report = JSON.parse(readFileSync(0, "utf8"));
  const allow = JSON.parse(readFileSync(allowFile, "utf8"));
  const result = verdict(report, allow, new Date().toISOString().slice(0, 10));
  const line = (finding) => `${finding.package} ${finding.severity} ${finding.advisory} ${finding.title}`.trim();
  for (const problem of result.problems) console.log(`allow list: ${problem}`);
  for (const finding of result.blocking) console.log(`BLOCKING ${line(finding)} ${finding.url}`);
  for (const finding of result.expired) console.log(`EXPIRED exemption, review it again: ${line(finding)}`);
  for (const finding of result.exempted) console.log(`exempted until ${allow.find((entry) => entry.advisory === finding.advisory && entry.package === finding.package).review_by}: ${line(finding)}`);
  for (const entry of result.unused) console.log(`::warning::npm-audit-allow.json still exempts ${entry.package} ${entry.advisory}, which npm audit no longer reports: remove the entry`);
  console.log(result.ok ? "npm audit gate: ok" : "npm audit gate: FAILED");
  process.exitCode = result.ok ? 0 : 1;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
