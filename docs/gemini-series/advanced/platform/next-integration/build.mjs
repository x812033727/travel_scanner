/** Build only the prepared checkout; retain actual stdout and exit status as evidence. */
import { readFile, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import path from "node:path";

const here = import.meta.dirname;
const prepared = JSON.parse(await readFile(path.join(here, "prepared.json"), "utf8"));
const relative = path.relative(path.join(here, ".workspaces"), prepared.web);
if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) throw new Error("Build must stay inside the prepared workspace");
const startedAt = new Date().toISOString();
const environment = { NEXT_TELEMETRY_DISABLED: "1", NEXT_PUBLIC_SITE_URL: "https://mokaair.com", API_INTERNAL_URL: "http://127.0.0.1:9" };
const child = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "build", "--webpack"], {
  cwd: prepared.web, windowsHide: true, env: { ...process.env, ...environment }, stdio: ["ignore", "pipe", "pipe"],
});
let output = "";
for (const stream of [child.stdout, child.stderr]) stream.on("data", bytes => { const text = bytes.toString(); output += text; process.stdout.write(text); });
const exitCode = await new Promise((resolve, reject) => { child.on("error", reject); child.on("close", resolve); });
await writeFile(path.join(here, "build.log"), output);
await writeFile(path.join(here, "build-results.json"), JSON.stringify({ startedAt, finishedAt: new Date().toISOString(), node: process.version, environment, exitCode,
  fixtureArticles: prepared.fixtureArticles, originalCatalogueSha256: prepared.originalCatalogueSha256 }, null, 2) + "\n");
if (exitCode !== 0) process.exitCode = exitCode || 1;
