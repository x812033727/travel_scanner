// A drama series' shared assets into its Drive backup folder, from the machine that holds them
// (tasks/open/2026-11-04-zhong-tian-an-imported-drama-episode.md).
//
// <VIDEO_WORKDIR>/_series/<series>/ keeps what every episode draws on and no episode's package
// carries: refs-dh/ and refs/ (the character, costume and set references; Tang Xiaotang's
// high-collar costume fix needs tangxiaotang-portrait-t2.png) and sfx/ (the synthesized library,
// whose rain and water are random, so a remade one sounds different). An imported drama is made
// off the host, so the host's backup never sees them. Run this where they are, after an episode
// adds or changes one, into the Drive folder mounted on that machine:
//
//   node tools/video/import/series-backup.mjs <VIDEO_WORKDIR>/_series/zhong-tian-qu-qi \
//     "G:/我的雲端硬碟/AI/備份/drama/zhong-tian-qu-qi/_series"
//
// Only files that differ (size, then sha256) are copied; nothing at the target is deleted, so a
// reference replaced in the workdir keeps its old copy on Drive. SHA256SUMS at the target lists
// what the source holds now, in sha256sum's format.
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const SUMS = "SHA256SUMS";
const sha256 = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

function walk(dir, base = dir, out = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (entry.name.startsWith(".") || entry.name.startsWith("._")) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, base, out);
    else if (entry.isFile() && !(dir === base && entry.name === SUMS)) out.push(path.relative(base, full).split(path.sep).join("/"));
  }
  return out;
}

/** Copy `source`'s files into `target` where they differ. Returns { files, copied, unchanged, sums }. */
export function backupSeries(source, target, { log = () => {} } = {}) {
  if (!existsSync(source) || !statSync(source).isDirectory()) throw new Error(`${source} is not a folder`);
  if (path.resolve(source) === path.resolve(target)) throw new Error("the source and the target are the same folder");
  const files = walk(source);
  if (!files.length) throw new Error(`${source} holds no files`);
  let copied = 0;
  const lines = [];
  for (const relative of files) {
    const from = path.join(source, relative);
    const to = path.join(target, relative);
    const hash = sha256(from);
    lines.push(`${hash}  ${relative}`);
    if (existsSync(to) && statSync(to).size === statSync(from).size && sha256(to) === hash) continue;
    mkdirSync(path.dirname(to), { recursive: true });
    copyFileSync(from, to);
    if (sha256(to) !== hash) throw new Error(`${relative} did not arrive whole at ${target}`);
    copied += 1;
    log(`copied ${relative}`);
  }
  mkdirSync(target, { recursive: true });
  writeFileSync(path.join(target, SUMS), `${lines.join("\n")}\n`);
  return { files: files.length, copied, unchanged: files.length - copied, sums: path.join(target, SUMS) };
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  const [source, target] = process.argv.slice(2);
  if (!source || !target) {
    console.error("usage: node tools/video/import/series-backup.mjs <VIDEO_WORKDIR>/_series/<series> <Drive folder>/_series");
    process.exit(2);
  }
  const result = backupSeries(path.resolve(source), path.resolve(target), { log: (line) => console.log(line) });
  console.log(`${result.files} file(s): ${result.copied} copied, ${result.unchanged} already there; ${result.sums}`);
}
