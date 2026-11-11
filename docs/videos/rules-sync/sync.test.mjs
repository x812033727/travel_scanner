import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  FILTERS, commands, destination, episodeFolder, globBase, globToRegExp, header, indexPage, plan, readManifest, readWatch,
} from "./sync.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
// Tracked files plus new ones not yet committed, so a file added in this change counts too.
const files = execFileSync("git", ["-C", ROOT, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", ".agents/skills", "docs/videos"],
  { maxBuffer: 1 << 28 })
  .toString().split("\0").filter(Boolean).filter((file) => fs.existsSync(path.join(ROOT, file)));
const rows = readManifest();
const watch = readWatch();

test("globs: *, **, {a,b} and the fixed base", () => {
  assert.ok(globToRegExp(".agents/skills/x/**/*.md").test(".agents/skills/x/SKILL.md"));
  assert.ok(globToRegExp(".agents/skills/x/**/*.md").test(".agents/skills/x/references/a.md"));
  assert.ok(!globToRegExp("docs/videos/so-thats-why/*.md").test("docs/videos/so-thats-why/week1/a.md"));
  assert.ok(globToRegExp("docs/{a,b}-*/NOTES.md").test("docs/b-x/NOTES.md"));
  assert.ok(!globToRegExp("docs/{a,b}-*/NOTES.md").test("docs/c-x/NOTES.md"));
  assert.equal(globBase(".agents/skills/x/**/*.md"), ".agents/skills/x/");
  assert.equal(globBase("docs/videos/{A,B}.md"), "docs/videos/");
});

test("episode folders use the drama backup names", () => {
  assert.equal(episodeFolder("curio-h04-v2"), "奇聞檔案局/H04");
  assert.equal(episodeFolder("curio-w02-michelin-guide-stars"), "奇聞檔案局/W02");
  assert.equal(episodeFolder("sothatswhy-p17-gecko-feet"), "原來如此事務所/P17");
  assert.equal(episodeFolder("zhong-tian-qu-qi-e033"), "種田娶妻打天下/第033集");
  assert.equal(episodeFolder("zhong-tian-qu-qi-e001-005-v2"), "種田娶妻打天下/第001-005集");
  assert.equal(episodeFolder("zhong-tian-qu-qi-e001-r2"), "種田娶妻打天下（真人版）/第001集");
  assert.equal(episodeFolder("tai-nainai-e005"), "恁祖媽今年18/第005集");
  assert.equal(episodeFolder("sothatswhy-t26"), null);
  assert.equal(episodeFolder("curio-five-recuts-20261012"), null);
});

test("one file can go to several places; except and - are honoured", () => {
  const sample = readManifest([
    "pattern\tdrive\texcept\tnote",
    "a/x/*.md\tAI劇/A/\ta/x/r2-*.md\t",
    "a/x/r2-*.md\tAI劇/B/\t\t",
    "a/x/keep.md\tAI劇/C/k.md\t\t",
    "a/old.md\t-\t\t",
    "docs/videos/{curio,tai-nainai}-*/NOTES.md\t{episode}\t\t",
  ].join("\n"));
  assert.equal(destination(sample[0], "a/x/keep.md"), "AI劇/A/keep.md");
  assert.equal(destination(sample[0], "a/x/r2-bible.md"), null);
  assert.equal(destination(sample[1], "a/x/r2-bible.md"), "AI劇/B/r2-bible.md");
  assert.equal(destination(sample[2], "a/x/keep.md"), "AI劇/C/k.md");
  assert.equal(destination(sample[3], "a/old.md"), "-");
  assert.equal(destination(sample[4], "docs/videos/curio-h04-v2/NOTES.md"), "AI劇/奇聞檔案局/H04/教訓/curio-h04-v2-NOTES.md");
  const result = plan(["a/x/keep.md", "a/x/r2-bible.md", "a/old.md", "docs/videos/curio-h04-v2/NOTES.md"], sample,
    readWatch("a/**/*.md\ndocs/videos/*/NOTES.md"));
  assert.deepEqual(result.sends.get("a/x/keep.md"), ["AI劇/A/keep.md", "AI劇/C/k.md"]);
  assert.deepEqual(result.missing, []);
  assert.ok(result.ignored.has("a/old.md"));
});

test("every rule and lesson file in watch.txt has a destination (add new ones to manifest.tsv)", () => {
  const result = plan(files, rows, watch);
  assert.deepEqual(result.missing, [], "these files have no row in docs/videos/rules-sync/manifest.tsv");
  assert.deepEqual(result.clashes, []);
});

test("every manifest row still matches a file", () => {
  assert.deepEqual(plan(files, rows, watch).unused, [], "remove or fix these rows in manifest.tsv");
});

test("every destination is inside a folder the sync owns", () => {
  const owned = FILTERS.filter((rule) => rule.startsWith("+ ")).map((rule) => globToRegExp(rule.slice(3).replace(/^\//, "")));
  for (const [file, targets] of plan(files, rows, watch).sends) {
    for (const target of targets) {
      assert.ok(!target.includes(".."), target);
      assert.ok(owned.some((regex) => regex.test(target)), `${file} → ${target} is outside the folders rules-sync owns`);
    }
  }
});

test("each drama has a lessons file, and every AI-drama skill is watched", () => {
  for (const name of ["shared", "explainer", "curio", "sothatswhy", "zhong-tian-qu-qi", "zhong-tian-qu-qi-r2", "tai-nainai"]) {
    assert.ok(files.includes(`docs/videos/lessons/${name}.md`), name);
  }
  const skills = fs.readdirSync(path.join(ROOT, ".agents/skills"))
    .filter((name) => /^(curio|sothatswhy|animation|minimax|zhong-tian|tai-nainai|drama)/.test(name));
  for (const skill of skills) {
    assert.ok(watch.some((w) => w.regex.test(`.agents/skills/${skill}/SKILL.md`)), `.agents/skills/${skill} is not in watch.txt`);
  }
});

test("the copy says where the original is, and the index lists it", () => {
  assert.match(header("docs/videos/lessons/curio.md"), /docs\/videos\/lessons\/curio\.md/);
  const page = indexPage(new Map([["docs/videos/lessons/curio.md", ["AI劇/奇聞檔案局/_規則與教訓/教訓/教訓.md"]]]));
  assert.match(page, /## AI劇\/奇聞檔案局\/_規則與教訓/);
  assert.match(page, /← `docs\/videos\/lessons\/curio\.md`/);
});

test("only owned folders are synced; episode notes are copied, never synced", () => {
  const runs = commands(new Map([
    ["a.md", ["AI劇/_共用規則/規則/a.md", "AI劇/奇聞檔案局/_規則與教訓/規則/a.md"]],
    ["b/NOTES.md", ["AI劇/奇聞檔案局/H04/教訓/curio-h04-NOTES.md"]],
  ]), "20261110T000000Z");
  const syncs = runs.filter((args) => args[0] === "sync").map((args) => args[2]);
  assert.deepEqual(syncs, ["videobackup:AI劇/_共用規則", "videobackup:AI劇/奇聞檔案局/_規則與教訓"]);
  for (const args of runs) {
    assert.ok(args.includes("--backup-dir"), args.join(" "));
    assert.notEqual(args[2], "videobackup:", "nothing is synced from the Drive root");
  }
  const copy = runs.find((args) => args[0] === "copy");
  assert.deepEqual(copy.slice(1, 3), ["@STAGE/AI劇", "videobackup:AI劇"]);
  assert.ok(copy.includes("+ /*/*/教訓/**"));
});
