import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
try { process.stdout.write(execFileSync("node", [path.join(here, "..", "check.mjs"), "--ep", "6", ...process.argv.slice(2)], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 })); } catch (e) { process.stdout.write(String(e.stdout ?? "")); process.stderr.write(String(e.stderr ?? e.message)); process.exitCode = 1; }
