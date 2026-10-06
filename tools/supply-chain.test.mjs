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
 * Playwright. The video worker's base image carries the browsers of one Playwright release, and
 * the worker drives them through the @playwright/test that ops/video/package.json installs, so a
 * patch tag from Dependabot's docker entry, or an npm bump of @playwright/test alone, would leave
 * a client looking for browser builds the image does not have.
 *
 * The video worker's other packages. Its image installs ops/video/package.json without a lock
 * file, and that file is not a workspace, so the root npm Dependabot group moves package-lock.json
 * alone: tools/video's tests would then run one release of a font or of pinyin-pro and the worker
 * another, which shows first in a published video's frames or in which narrated lines pass
 * check-audio. Dependabot brings them in a group of their own (`video-worker` in
 * .github/dependabot.yml): when its pull request moves a package ops/video/package.json pins, it
 * stays red here until a person copies the lock's versions into that file on its branch, and the
 * week's other bumps do not wait for it.
 * And a font tools/video draws with but the image lacks fails only on the host, quietly: the
 * worker keeps the video's own thumbnail for that language.
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

import { FONT_PACKAGES } from "./video/render/fonts.mjs";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const WORKFLOWS = join(ROOT, ".github", "workflows");
const DOCKERFILES = ["apps/api/Dockerfile", "apps/web/Dockerfile", "ops/video/Dockerfile", "ops/youtube-uploader/Dockerfile"];
const COMPOSE_FILES = ["docker-compose.yml", "docker-compose.community.yml"];

/** Root compose files not scanned yet, each with the open task that pins and adds them. */
const COMPOSE_NOT_SCANNED_YET = new Map([
  // Pinning its postgres recreates the production database container on the next deploy, so
  // that task checks what the host runs first.
  ["docker-compose.prod.yml", "2026-10-05-pin-prod-compose-postgres-redis-by"],
]);

/** Images that run as more than one tag on purpose, with the reason; each tag has one digest. */
const SEVERAL_TAGS = new Map([
  ["node", "the web image is Node 22 on Alpine; the YouTube uploader needs Debian for `playwright install --with-deps`"],
]);

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

/** Fonts tools/video draws with that the video worker's image does not install yet, each with the open task that adds them. */
const WORKER_FONTS_NOT_INSTALLED_YET = new Map([
  // The caption locales' own thumbnail fonts (#1109, #1111) came after ops/video/package.json (#755).
  ["@fontsource-variable/noto-sans-kr", "2026-10-05-video-worker-image-lacks-locale-thumbnail"],
  ["@fontsource-variable/noto-sans-sc", "2026-10-05-video-worker-image-lacks-locale-thumbnail"],
  ["@fontsource-variable/noto-sans-jp", "2026-10-05-video-worker-image-lacks-locale-thumbnail"],
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

test("every image a Dockerfile, a scanned compose file or a workflow runs is pinned by digest", () => {
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
  const tagsOf = new Map();
  for (const { file, reference } of images()) {
    const { name, tag } = parseReference(reference);
    tagsOf.set(name, new Set([...(tagsOf.get(name) ?? []), tag]));
    const key = SEVERAL_TAGS.has(name) ? `${name}:${tag}` : name;
    if (!byName.has(key)) byName.set(key, new Map());
    const references = byName.get(key);
    references.set(reference, [...(references.get(reference) ?? []), file]);
  }
  const split = [...byName.entries()]
    .filter(([, references]) => references.size > 1)
    .map(([name, references]) =>
      `${name}: ${[...references.entries()].map(([reference, files]) => `${reference} in ${[...new Set(files)].join(", ")}`).join(" / ")}`,
    );
  assert.deepEqual(split, [], "copy the new pin into every file that names this image");
  for (const name of SEVERAL_TAGS.keys()) {
    assert.ok((tagsOf.get(name)?.size ?? 0) > 1, `${name} runs one tag now — drop it from SEVERAL_TAGS`);
  }
});

test("an image left unpinned names a task that is still open", () => {
  for (const [name, task] of NOT_PINNED_YET) {
    assert.ok(existsSync(join(ROOT, "tasks", "open", `${task}.md`)), `${name}: ${task} is closed — pin the image or drop it here`);
  }
});

test("every root compose file is scanned, or names a task that is still open", () => {
  // Dependabot's docker-compose entry reads all of these, so one left out here is a pin nothing checks.
  const compose = readdirSync(ROOT).filter((name) => /^(?:docker-)?compose[^/]*\.ya?ml$/.test(name));
  assert.ok(compose.length >= COMPOSE_FILES.length, "no compose files found at the root — the scan itself is broken");
  const unscanned = compose.filter((name) => !COMPOSE_FILES.includes(name) && !COMPOSE_NOT_SCANNED_YET.has(name));
  assert.deepEqual(unscanned, [], "add these to COMPOSE_FILES");
  for (const [file, task] of COMPOSE_NOT_SCANNED_YET) {
    assert.ok(existsSync(join(ROOT, "tasks", "open", `${task}.md`)), `${file}: ${task} is closed — scan the file or drop it here`);
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

test("the video worker's Playwright image is the release of the @playwright/test it installs", () => {
  const from = /^FROM\s+mcr\.microsoft\.com\/playwright:v(\d+\.\d+\.\d+)-[a-z]+[@\s]/m.exec(read("ops/video/Dockerfile"));
  assert.ok(from, "no `FROM mcr.microsoft.com/playwright:v<version>-<distro>` in ops/video/Dockerfile — the scan itself is broken");
  const image = from[1];
  // The image's `npm install` reads this file without a lock file, so a range here would install
  // whatever release is newest on build day.
  const installed = JSON.parse(read("ops/video/package.json")).dependencies?.["@playwright/test"];
  // What tools/video runs with in CI and on a laptop. @playwright/test pins playwright, which pins
  // playwright-core, the package that names the browser builds.
  const locked = JSON.parse(read("package-lock.json")).packages;
  const versions = new Map([
    ["ops/video/package.json @playwright/test", installed],
    ...["@playwright/test", "playwright", "playwright-core"].map((name) => [`package-lock.json ${name}`, locked[`node_modules/${name}`]?.version]),
  ]);
  const apart = [...versions].filter(([, version]) => version !== image).map(([where, version]) => `${where}: ${version}`);
  assert.deepEqual(
    apart,
    [],
    `ops/video/Dockerfile runs Playwright ${image}'s browsers. Move the image (tag and digest: docker buildx imagetools ` +
      "inspect mcr.microsoft.com/playwright:v<version>-noble), ops/video/package.json and package-lock.json to one release in one change",
  );
});

test("the video worker installs exactly the versions package-lock.json resolves", () => {
  const pinned = Object.entries(JSON.parse(read("ops/video/package.json")).dependencies ?? {});
  assert.ok(pinned.length > 0, "no dependencies in ops/video/package.json — the scan itself is broken");
  const locked = JSON.parse(read("package-lock.json")).packages;
  // The lock always holds one exact version, so a range here (`^3.29.4`) is apart from it too.
  const apart = pinned
    .map(([name, version]) => ({ name, version, lock: locked[`node_modules/${name}`]?.version }))
    .filter(({ version, lock }) => version !== lock)
    .map(({ name, version, lock }) => `${name}: ${version} in ops/video/package.json, ${lock ?? "nothing"} in package-lock.json`);
  assert.deepEqual(
    apart,
    [],
    "write package-lock.json's version, exactly, into ops/video/package.json in the same change " +
      "(for @playwright/test, move the image as well: see the test above)",
  );
});

test("the video worker installs every font tools/video draws with, or names a task that is still open", () => {
  // fonts.mjs finds a font by require.resolve when a page needs it, so a missing one fails nowhere but on the host.
  const installed = JSON.parse(read("ops/video/package.json")).dependencies ?? {};
  const fonts = Object.values(FONT_PACKAGES);
  assert.ok(fonts.length >= 2, `only ${fonts.length} fonts in tools/video/render/fonts.mjs — the scan itself is broken`);
  const missing = fonts.filter((name) => !Object.hasOwn(installed, name) && !WORKER_FONTS_NOT_INSTALLED_YET.has(name));
  assert.deepEqual(missing, [], "add these to ops/video/package.json at the version package-lock.json resolves");
  for (const [name, task] of WORKER_FONTS_NOT_INSTALLED_YET) {
    assert.ok(!Object.hasOwn(installed, name), `${name} is installed now — drop it from WORKER_FONTS_NOT_INSTALLED_YET`);
    assert.ok(existsSync(join(ROOT, "tasks", "open", `${task}.md`)), `${name}: ${task} is closed — install the font or drop it here`);
  }
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
