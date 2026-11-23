#!/usr/bin/env node
// Copy the AI-drama rules and lessons from the repository to the owner's Google Drive (README.md).
//
//   node docs/videos/rules-sync/sync.mjs --dry-run            # list what would go where
//   node docs/videos/rules-sync/sync.mjs                      # rclone from this environment
//   node docs/videos/rules-sync/sync.mjs --rclone-dry-run     # ask rclone what it would change, write nothing
//   node docs/videos/rules-sync/sync.mjs --docker-image travel-scanner-video-worker:local \
//        --conf-dir /etc/travel-scanner/rclone-videos         # the production host
//
// The repository is the only original. Files are read from a git ref (origin/main by default, after a
// fetch), so the checkout's own branch does not matter. Drive gets a read-only copy: only the folders
// this script owns are touched. AI劇/_共用規則/ and each AI劇/<劇>/_規則與教訓/ are synced (a file
// replaced or removed there moves to AI劇/_舊版-規則同步/<UTC time>/, nothing is deleted); the episode
// AI劇/<劇>/<集>/教訓/ folders are only copied into, so a note removed from the repo stays there.
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const MANIFEST = path.join(HERE, "manifest.tsv");
export const WATCH = path.join(HERE, "watch.txt");
export const REMOTE = "videobackup";
export const OLD = "AI劇/_舊版-規則同步";
export const INDEX = "AI劇/_共用規則/目錄.md";
export const FILTERS = [
  `- /${OLD}/**`,
  "+ /AI劇/_共用規則/**",
  "+ /AI劇/*/_規則與教訓/**",
  "+ /AI劇/*/*/教訓/**",
  "+ /AI劇/*/*/*/教訓/**",
  "- **",
];
export const DRAMA_NAMES = {
  curio: "奇聞檔案局",
  sothatswhy: "原來如此事務所",
  "zhong-tian-qu-qi": "種田娶妻打天下",
  "zhong-tian-qu-qi-r2": "種田娶妻打天下（真人版）",
  "tai-nainai": "恁祖媽今年18",
};
export const CURIO_CATEGORIES = {
  H: "H-歷史懸案",
  S: "S-歷史人物與名場面",
  M: "M-奇異現象與自然",
  F: "F-童話神話與怪談原版",
  L: "L-都市傳說與消失地名",
  G: "G-靈異與超自然公案",
  P: "P-預言與末日",
  U: "U-外星太空與未知訊號",
  W: "W-商業與品牌奇聞",
  B: "W-商業與品牌奇聞",
};
export const SOTHATSWHY_PREFIX_CATEGORIES = {
  PHY: "物理化學與日常材料",
  BIO: "生物動物與植物",
  GEO: "地球天氣與太空",
  TEC: "數位科技與通訊工程",
  FOD: "飲食與廚房科學",
  HUM: "人體感官與日常行為",
  SOC: "建築交通與商業制度",
};
export const SOTHATSWHY_PLAN_CATEGORIES = {
  P01: "數位科技與通訊工程", P02: "地球天氣與太空", P03: "數位科技與通訊工程",
  P04: "地球天氣與太空", P05: "物理化學與日常材料", P06: "物理化學與日常材料",
  P07: "物理化學與日常材料", P08: "飲食與廚房科學", P09: "數位科技與通訊工程",
  P10: "數位科技與通訊工程", P11: "數位科技與通訊工程", P12: "數位科技與通訊工程",
  P13: "數位科技與通訊工程", P14: "地球天氣與太空", P15: "地球天氣與太空",
  P16: "地球天氣與太空", P17: "生物動物與植物", P18: "物理化學與日常材料",
  P19: "數位科技與通訊工程", P20: "物理化學與日常材料", P21: "人體感官與日常行為",
  P22: "物理化學與日常材料", P23: "地球天氣與太空", P24: "地球天氣與太空",
  P25: "建築交通與商業制度", P26: "建築交通與商業制度", P27: "建築交通與商業制度",
  P28: "建築交通與商業制度", P29: "數位科技與通訊工程", P30: "建築交通與商業制度",
};

let themeMapsCache = null;
function themeCategoryMaps() {
  if (themeMapsCache) return themeMapsCache;
  const load = (rel) => {
    const p = path.resolve(HERE, "..", rel);
    if (!fs.existsSync(p)) return new Map();
    const raw = JSON.parse(fs.readFileSync(p, "utf8"));
    const items = Array.isArray(raw) ? raw : (raw.episodes || raw.themes || []);
    return new Map(items.map((t) => [String(t.id).toUpperCase(), t.category]));
  };
  themeMapsCache = {
    curio: load("history-curiosity/pool/themes.json"),
    sothatswhy: load("so-thats-why/pool/themes.json"),
  };
  return themeMapsCache;
}

/** A glob (`*`, `**`, `?`, `{a,b}`) as an anchored RegExp over repository paths. */
export function globToRegExp(glob) {
  let out = "";
  let depth = 0;
  for (let i = 0; i < glob.length; i += 1) {
    const c = glob[i];
    if (c === "*" && glob[i + 1] === "*") {
      const slash = glob[i + 2] === "/";
      out += slash ? "(?:.*/)?" : ".*";
      i += slash ? 2 : 1;
    } else if (c === "*") out += "[^/]*";
    else if (c === "?") out += "[^/]";
    else if (c === "{") { out += "(?:"; depth += 1; }
    else if (c === "}" && depth) { out += ")"; depth -= 1; }
    else if (c === "," && depth) out += "|";
    else out += c.replace(/[.+^$()|[\]\\]/g, "\\$&");
  }
  return new RegExp(`^${out}$`);
}

/** The part of a glob before its first wildcard, up to the last slash: what relative paths are kept from. */
export function globBase(glob) {
  const first = glob.search(/[*?{]/);
  const fixed = first === -1 ? glob : glob.slice(0, first);
  return fixed.slice(0, fixed.lastIndexOf("/") + 1);
}

function lines(text) {
  return text.split("\n").map((line) => line.replace(/\r$/, "")).filter((line) => line.trim() && !line.startsWith("#"));
}

export function readManifest(text = fs.readFileSync(MANIFEST, "utf8")) {
  return lines(text)
    .map((line) => line.split("\t"))
    .filter((cells) => cells[0] !== "pattern")
    .map(([pattern, drive = "", except = "", note = ""], index) => ({
      pattern: pattern.trim(), drive: drive.trim(), except: except.trim(), note: note.trim(), index,
      regex: globToRegExp(pattern.trim()), exceptRegex: except.trim() ? globToRegExp(except.trim()) : null,
    }));
}

export function readWatch(text = fs.readFileSync(WATCH, "utf8")) {
  return lines(text).map((line) => ({ pattern: line.trim(), regex: globToRegExp(line.trim()) }));
}

/** `<劇>/<集數>` (or `<系列>/<分類>/<代碼>` for explainers) for an episode folder, or null. Same names as AI-DRAMA-DRIVE.md. */
export function episodeFolder(slug) {
  let m = slug.match(/^curio-([hsmflgpuwb])-([a-z]?\d+)(?=-|$)/);
  if (m) {
    const axis = m[1].toUpperCase();
    const raw = m[2].toUpperCase();
    const code = /^\d/.test(raw) ? `${axis}${raw}` : raw;
    return `${DRAMA_NAMES.curio}/${CURIO_CATEGORIES[axis]}/${code}`;
  }
  m = slug.match(/^curio-([hsmflgpuwb]\d+)(?=-|$)/);
  if (m) {
    const code = m[1].toUpperCase();
    return `${DRAMA_NAMES.curio}/${CURIO_CATEGORIES[code[0]]}/${code}`;
  }
  m = slug.match(/^curio-(t\d+)(?=-|$)/);
  if (m) {
    const code = m[1].toUpperCase();
    const cat = themeCategoryMaps().curio.get(code);
    return cat ? `${DRAMA_NAMES.curio}/${cat}/${code}` : null;
  }
  m = slug.match(/^sothatswhy-(phy|bio|geo|tec|fod|hum|soc)-([a-z]?\d+(?:-\d+)?)(?=-|$)/);
  if (m) {
    const prefix = m[1].toUpperCase();
    const raw = m[2].toUpperCase();
    const code = /^\d/.test(raw) ? `${prefix}-${raw}` : raw;
    return `${DRAMA_NAMES.sothatswhy}/${SOTHATSWHY_PREFIX_CATEGORIES[prefix]}/${code}`;
  }
  m = slug.match(/^sothatswhy-(phy|bio|geo|tec|fod|hum|soc)(\d+)(?=-|$)/);
  if (m) {
    const prefix = m[1].toUpperCase();
    return `${DRAMA_NAMES.sothatswhy}/${SOTHATSWHY_PREFIX_CATEGORIES[prefix]}/${prefix}${m[2]}`;
  }
  m = slug.match(/^sothatswhy-p(\d{2})(?=-|$)/);
  if (m) {
    const code = `P${m[1]}`;
    const cat = SOTHATSWHY_PLAN_CATEGORIES[code];
    return cat ? `${DRAMA_NAMES.sothatswhy}/${cat}/${code}` : null;
  }
  m = slug.match(/^sothatswhy-(g\d+)(?=-|$)/);
  if (m) {
    const code = m[1].toUpperCase();
    const cat = themeCategoryMaps().sothatswhy.get(code);
    return cat ? `${DRAMA_NAMES.sothatswhy}/${cat}/${code}` : null;
  }
  m = slug.match(/^(zhong-tian-qu-qi|tai-nainai)-e(\d{3})(?:-(\d{3}))?(-r\d+)?(?:-v\d+)?$/);
  if (m) {
    const name = DRAMA_NAMES[m[1] + (m[4] ? "-r2" : "")];
    return `${name}/第${m[2]}${m[3] ? `-${m[3]}` : ""}集`;
  }
  return null;
}

/** Where one row sends one file (a Drive path under the remote root), or null when it does not apply. */
export function destination(row, file) {
  if (!row.regex.test(file) || (row.exceptRegex && row.exceptRegex.test(file))) return null;
  if (row.drive === "-") return "-";
  if (row.drive === "{episode}") {
    const dir = path.posix.basename(path.posix.dirname(file));
    const folder = episodeFolder(dir);
    return folder ? `AI劇/${folder}/教訓/${dir}-${path.posix.basename(file)}` : null;
  }
  if (row.drive.endsWith(".md")) return row.drive;
  const base = globBase(row.pattern);
  return row.drive.replace(/\/?$/, "/") + file.slice(base.length);
}

/** Every file → its Drive paths; plus what watch.txt covers but nothing sends, and rows that match nothing. */
export function plan(files, rows, watch) {
  const sends = new Map();
  const ignored = new Set();
  const used = new Set();
  for (const file of files) {
    for (const row of rows) {
      const target = destination(row, file);
      if (target === null) continue;
      used.add(row.index);
      if (target === "-") { ignored.add(file); continue; }
      if (!sends.has(file)) sends.set(file, []);
      if (!sends.get(file).includes(target)) sends.get(file).push(target);
    }
  }
  const watched = files.filter((file) => watch.some((w) => w.regex.test(file)));
  const missing = watched.filter((file) => !sends.has(file) && !ignored.has(file));
  const unused = rows.filter((row) => !used.has(row.index)).map((row) => row.pattern);
  const targets = new Map();
  const clashes = [];
  for (const [file, list] of sends) {
    for (const target of list) {
      if (targets.has(target) && targets.get(target) !== file) clashes.push(`${target}: ${targets.get(target)} and ${file}`);
      targets.set(target, file);
    }
  }
  return { sends, ignored, missing, unused, clashes };
}

export function header(file) {
  return `> 正本：repo 的 \`${file}\`。這是自動同步的副本，請勿在雲端硬碟編輯；改 repo 合併後才會更新。\n\n`;
}

export function indexPage(sends) {
  const rows = [...sends].flatMap(([file, targets]) => targets.map((target) => [target, file])).sort();
  const groups = new Map();
  for (const [target, file] of rows) {
    const key = target.split("/").slice(0, 3).join("/");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(`- \`${target}\` ← \`${file}\``);
  }
  const body = [...groups].map(([key, list]) => `## ${key}\n\n${list.join("\n")}`).join("\n\n");
  return "# 規則與教訓目錄\n\n" +
    "自動產生（docs/videos/rules-sync）。做一集時讀：`AI劇/_共用規則/`、該劇的 `_規則與教訓/`、上一集的 `教訓/`。\n" +
    "要改任何一份，改 repo 裡的正本；雲端這裡會在合併後一小時內更新。\n\n" + body + "\n";
}

function git(repo, args, options = {}) {
  return execFileSync("git", ["-C", repo, ...args], { maxBuffer: 1 << 28, ...options });
}

export function stage(repo, ref, into, sends) {
  for (const [file, targets] of sends) {
    const content = git(repo, ["show", `${ref}:${file}`]);
    const text = file.endsWith(".md") ? Buffer.concat([Buffer.from(header(file)), content]) : content;
    for (const target of targets) {
      const out = path.join(into, target);
      fs.mkdirSync(path.dirname(out), { recursive: true });
      fs.writeFileSync(out, text);
    }
  }
  const index = path.join(into, INDEX);
  fs.mkdirSync(path.dirname(index), { recursive: true });
  fs.writeFileSync(index, indexPage(sends));
}

/** The rclone runs for one sync. Each owned rules folder is synced on its own (so rclone never tries to
 * remove an episode folder it does not own); the episode 教訓/ folders are only copied into. */
export function commands(sends, stamp, extra = []) {
  const common = ["--checksum", "--tpslimit", "5", "--retries", "5", ...extra];
  const roots = new Set(["AI劇/_共用規則"]);
  for (const targets of sends.values()) {
    for (const target of targets) {
      const m = target.match(/^(AI劇\/[^/]+\/_規則與教訓)\//);
      if (m) roots.add(m[1]);
    }
  }
  const runs = [...roots].sort().map((root) =>
    ["sync", `@STAGE/${root}`, `${REMOTE}:${root}`, ...common, "--backup-dir", `${REMOTE}:${OLD}/${stamp}/${root}`]);
  runs.push(["copy", "@STAGE/AI劇", `${REMOTE}:AI劇`, ...common,
    "--filter", "- /_共用規則/**", "--filter", "- /*/_規則與教訓/**",
    "--filter", "+ /*/*/教訓/**", "--filter", "+ /*/*/*/教訓/**", "--filter", "- **",
    "--backup-dir", `${REMOTE}:${OLD}/${stamp}/AI劇`]);
  return runs;
}

export function checkCommand() {
  return ["check", "@STAGE", `${REMOTE}:`, "--one-way", "--checksum", "--tpslimit", "5", "--retries", "5",
    ...FILTERS.flatMap((rule) => ["--filter", rule])];
}

/** Run rclone commands in order, stopping at the first failure; in one container on the host. */
function rclone(runs, into, options) {
  const stageArg = (arg, root) => (arg.startsWith("@STAGE") ? root + arg.slice("@STAGE".length) : arg);
  if (options.dockerImage) {
    const quote = (arg) => `'${arg.replace(/'/g, "'\\''")}'`;
    const script = runs.map((args) => `rclone --config /tmp/rclone.conf ${args.map((a) => quote(stageArg(a, "/stage"))).join(" ")}`);
    return spawnSync("docker", ["run", "--rm", "-u", "0", "--network", "host", "-v", `${options.confDir}:/conf:ro`,
      "-v", `${into}:/stage:ro`, "--entrypoint", "sh", options.dockerImage, "-c",
      ["cp /conf/rclone.conf /tmp/rclone.conf", ...script].join(" && ")], { encoding: "utf8", maxBuffer: 1 << 26 });
  }
  let last = { status: 0, stderr: "" };
  for (const args of runs) {
    const run = spawnSync("rclone", args.map((a) => stageArg(a, into)), { encoding: "utf8", maxBuffer: 1 << 26 });
    last = { status: run.status, stderr: `${last.stderr}${run.stderr || ""}` };
    if (run.status !== 0) break;
  }
  return last;
}

function parseArgs(argv) {
  const options = { ref: "origin/main", repo: path.resolve(HERE, "../../.."), fetch: true, dryRun: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--no-fetch") options.fetch = false;
    else if (arg === "--rclone-dry-run") options.rcloneDryRun = true;
    else if (arg === "--ref") options.ref = argv[++i];
    else if (arg === "--repo") options.repo = argv[++i];
    else if (arg === "--docker-image") options.dockerImage = argv[++i];
    else if (arg === "--conf-dir") options.confDir = argv[++i];
    else throw new Error(`unknown argument ${arg}`);
  }
  if (options.dockerImage && !options.confDir) throw new Error("--docker-image needs --conf-dir");
  return options;
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.fetch && options.ref.startsWith("origin/")) {
    git(options.repo, ["fetch", "-q", "origin", options.ref.slice("origin/".length)], { stdio: "inherit" });
  }
  const files = git(options.repo, ["ls-tree", "-r", "--name-only", "-z", options.ref]).toString().split("\0").filter(Boolean);
  const result = plan(files, readManifest(), readWatch());
  const commit = git(options.repo, ["rev-parse", "--short=12", options.ref]).toString().trim();
  const count = [...result.sends.values()].reduce((sum, list) => sum + list.length, 0);
  if (result.missing.length || result.clashes.length) {
    console.error(`rules-sync: not synced, manifest.tsv is incomplete at ${commit}`);
    for (const file of result.missing) console.error(`  no destination: ${file}`);
    for (const clash of result.clashes) console.error(`  two files, one destination: ${clash}`);
    process.exit(1);
  }
  const into = fs.mkdtempSync(path.join(os.tmpdir(), "rules-sync-"));
  try {
    stage(options.repo, options.ref, into, result.sends);
    if (options.dryRun) {
      for (const [file, targets] of [...result.sends].sort()) for (const target of targets) console.log(`${target}\t← ${file}`);
      console.log(`rules-sync: ${result.sends.size} files, ${count} copies at ${commit} (dry run, staged in ${into})`);
      return;
    }
    const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
    const copied = rclone(commands(result.sends, stamp, options.rcloneDryRun ? ["--dry-run"] : []), into, options);
    if (copied.status !== 0) throw new Error(`rclone: ${(copied.stderr || "").trim().slice(-800)}`);
    if (options.rcloneDryRun) {
      console.log((copied.stderr || "").trim().split("\n").slice(-15).join("\n"));
      console.log(`rules-sync: ${result.sends.size} files, ${count} copies at ${commit} (rclone dry run, nothing written)`);
      return;
    }
    const checked = rclone([checkCommand()], into, options);
    const found = [...(checked.stderr || "").matchAll(/(\d+) differences found/g)].map((m) => Number(m[1]));
    const differences = found.length ? found.at(-1) : checked.status === 0 ? 0 : -1;
    console.log(`rules-sync: ${result.sends.size} files, ${count} copies at ${commit}, ${differences} differences`);
    if (differences !== 0) process.exit(1);
  } finally {
    if (!options.dryRun) fs.rmSync(into, { recursive: true, force: true });
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
