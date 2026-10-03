/**
 * Supply-chain pins and the announcer, which stop working without anyone noticing if a later
 * edit undoes them (L10, L11 and I4 in docs/security-review-2026-09-23.md).
 *
 * Images. A tag is a pointer its publisher can move, so `postgres:17-alpine` is whatever it
 * resolved to the day a build or a job pulled it, and a move on the registry changed the
 * production image on the next `--build` with no diff in this repository. Every image below is
 * pinned `tag@sha256:digest`. Dependabot moves the Dockerfile and compose digests; no Dependabot
 * ecosystem reads the images in workflows, so a person bumps those, and one image pinned two ways
 * is how such a bump gets half-applied — or how a Dependabot bump of mailpit in the compose file
 * leaves CI on the old one.
 *
 * uv. `pip install uv` in the API image installed whatever uv was newest on build day.
 *
 * Announcements. ci-red-main.yml listens to workflows by their `name:`, so a rename quietly
 * stops the issue; and its branch filter matches a branch name a fork chooses, so it also has to
 * look at the event that started the run.
 */
import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const WORKFLOWS = join(ROOT, ".github", "workflows");
const DOCKERFILES = ["apps/api/Dockerfile", "apps/web/Dockerfile"];
const COMPOSE_FILES = ["docker-compose.community.yml"];

/** Images not pinned yet, each with the open task that pins it. */
const NOT_PINNED_YET = new Map([
  // quay.io answers an anonymous manifest request with 401 since 2026-09-24, so there is no
  // digest to read; that task replaces these images.
  ["quay.io/minio/minio", "2026-09-24-run-the-local-community-storage-without"],
  ["quay.io/minio/mc", "2026-09-24-run-the-local-community-storage-without"],
]);

/** Images pinned by digest alone, with the reason a tag would say nothing. */
const DIGEST_ONLY = new Map([
  ["cgr.dev/chainguard/minio", "Chainguard's free tier publishes only :latest (see ci.yml)"],
]);

const read = (path) => readFileSync(join(ROOT, path), "utf8");

function workflowFiles() {
  return readdirSync(WORKFLOWS)
    .filter((name) => name.endsWith(".yml") || name.endsWith(".yaml"))
    .map((name) => `.github/workflows/${name}`);
}

/** `registry/name[:tag][@sha256:digest]` split into its parts. */
function parseReference(reference) {
  const [named, digest] = reference.split("@");
  const colon = named.lastIndexOf(":");
  const hasTag = colon > named.lastIndexOf("/");
  return {
    name: hasTag ? named.slice(0, colon) : named,
    tag: hasTag ? named.slice(colon + 1) : undefined,
    digest,
  };
}

function images() {
  const found = [];
  for (const file of DOCKERFILES) {
    const stages = new Set();
    for (const line of read(file).split(/\r?\n/)) {
      const from = /^FROM\s+(?:--platform=\S+\s+)?(\S+)(?:\s+AS\s+(\S+))?/i.exec(line);
      if (!from) continue;
      // `FROM builder` names an earlier stage, not an image.
      if (!stages.has(from[1])) found.push({ file, reference: from[1] });
      if (from[2]) stages.add(from[2]);
    }
  }
  // `image:` in compose and in a job's `services:`, and the `*_IMAGE` env vars the workflows'
  // `docker run` steps use (tools/ci-images.test.mjs). A value must sit on the same line.
  const yamlImage = /^[ \t]+(?:image|[A-Z][A-Z0-9_]*_IMAGE):[ \t]*(\S+)[ \t]*$/gm;
  for (const file of [...COMPOSE_FILES, ...workflowFiles()]) {
    for (const match of read(file).matchAll(yamlImage)) {
      found.push({ file, reference: match[1].replace(/^["']|["']$/g, "") });
    }
  }
  return found;
}

test("every image a Dockerfile, the community compose file or a workflow runs is pinned by digest", () => {
  const found = images();
  // A guard that finds nothing passes forever.
  assert.ok(found.length >= 10, `only ${found.length} image references found — the scan itself is broken`);
  const floating = found
    .filter(({ reference }) => !/@sha256:[0-9a-f]{64}$/.test(reference))
    .filter(({ reference }) => !NOT_PINNED_YET.has(parseReference(reference).name))
    .map(({ file, reference }) => `${file}: ${reference}`);
  assert.deepEqual(floating, [], "pin these as tag@sha256:<digest> (docker buildx imagetools inspect <image:tag>)");
});

test("a digest pin keeps its tag, so a reader and Dependabot know which version it is", () => {
  const unnamed = images()
    .map(({ file, reference }) => ({ file, reference, ...parseReference(reference) }))
    .filter(({ digest }) => digest)
    .filter(({ name, tag }) => !DIGEST_ONLY.has(name) && (!tag || tag === "latest"))
    .map(({ file, reference }) => `${file}: ${reference}`);
  assert.deepEqual(unnamed, [], "write the version tag in front of the digest, and not `latest`");
});

test("one image is pinned to the same tag and digest everywhere", () => {
  const byName = new Map();
  for (const { file, reference } of images()) {
    const { name } = parseReference(reference);
    if (!byName.has(name)) byName.set(name, new Map());
    const references = byName.get(name);
    references.set(reference, [...(references.get(reference) ?? []), file]);
  }
  const split = [...byName.entries()]
    .filter(([, references]) => references.size > 1)
    .map(([name, references]) =>
      `${name}: ${[...references.entries()].map(([reference, files]) => `${reference} in ${[...new Set(files)].join(", ")}`).join(" / ")}`,
    );
  assert.deepEqual(split, [], "copy the new pin into every file that names this image");
});

test("an image left unpinned names a task that is still open", () => {
  for (const [name, task] of NOT_PINNED_YET) {
    assert.ok(existsSync(join(ROOT, "tasks", "open", `${task}.md`)), `${name}: ${task} is closed — pin the image or drop it here`);
  }
});

test("the API image installs a pinned uv", () => {
  const installs = read("apps/api/Dockerfile")
    .split(/\r?\n/)
    .filter((line) => /\bpip install\b/.test(line))
    .flatMap((line) => line.split("&&")[0].split(/\s+/))
    .filter((word) => /^uv\b/.test(word));
  assert.ok(installs.length > 0, "no `pip install ... uv` found in apps/api/Dockerfile — the scan itself is broken");
  for (const word of installs) assert.match(word, /^uv==\d+\.\d+\.\d+$/, "install uv as uv==<version>");
});

function workflowName(file) {
  const name = /^name:[ \t]*(.+?)[ \t]*$/m.exec(read(file))?.[1];
  return name?.replace(/^["']|["']$/g, "");
}

test("red main announces CI and both audits, by the names those workflows really have", () => {
  const source = read(".github/workflows/ci-red-main.yml");
  const list = /^[ \t]+workflows:[ \t]*\[(.*)\][ \t]*$/m.exec(source);
  assert.ok(list, "no `workflows: [...]` list in ci-red-main.yml");
  const listened = list[1].split(",").map((entry) => entry.trim().replace(/^["']|["']$/g, ""));
  const names = new Set(workflowFiles().map(workflowName));
  assert.deepEqual(listened.filter((name) => !names.has(name)), [], "workflow_run matches `name:`; these name no workflow");
  for (const file of [".github/workflows/ci.yml", ".github/workflows/npm-audit.yml", ".github/workflows/pip-audit.yml"]) {
    assert.ok(listened.includes(workflowName(file)), `${file} (${workflowName(file)}) is not announced`);
  }
  for (const name of listened) {
    const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    // An entry without text would fail the job on the very run it should announce.
    assert.match(source, new RegExp(`^\\s+(?:"${escaped}"|${escaped}):\\s*\\{`, "m"), `no announcement text for ${name}`);
  }
});

test("red main ignores runs a fork started", () => {
  const source = read(".github/workflows/ci-red-main.yml");
  const condition = /^([ \t]+)if:[ \t]*>-?[ \t]*\r?\n((?:\1[ \t]+\S.*\r?\n)+)/m.exec(source)?.[2] ?? /^[ \t]+if:(.*)$/m.exec(source)?.[1];
  assert.ok(condition, "no `if:` on the announce job");
  assert.match(condition, /github\.event\.workflow_run\.conclusion == 'failure'/);
  // `branches: [main]` matches the head branch of the finished run, a name a fork picks, so the
  // event decides: main's CI is a `push`, the audits a `schedule`, and a fork can only start a
  // `pull_request` run here.
  const events = [...condition.matchAll(/github\.event\.workflow_run\.event == '([^']+)'/g)].map((match) => match[1]);
  assert.ok(events.includes("push"), "the condition does not require main's CI to be a push run");
  assert.deepEqual(events.filter((event) => !["push", "schedule"].includes(event)), []);
  assert.doesNotMatch(condition, /workflow_run\.event !=/, "list the events that may announce instead of excluding some");
});
