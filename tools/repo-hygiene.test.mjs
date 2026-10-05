/**
 * Host details in committed records.
 *
 * The repository is public, and evidence logs, release notes and task files are often pasted
 * from a terminal. A path under one person's Windows profile, a PuTTY saved-session name or a
 * throwaway database password in such a paste works for nobody else and tells a stranger how
 * the production host is reached. `tools/skills.test.mjs` already keeps them out of the skills;
 * this test does the same for every tracked file under `docs/`, `tasks/` and `ops/`.
 *
 * Write the placeholders instead: `<repo>` for the checkout, `<home>` for the user profile,
 * `<saved-session>` for the PuTTY session, `<disposable-password>` for a password. In Markdown,
 * keep them inside a code span, or the renderer drops them as unknown HTML tags.
 */
import assert from "node:assert/strict";
import test from "node:test";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const AREAS = ["docs", "tasks", "ops"];
const BINARY = /\.(png|jpe?g|gif|webp|avif|ico|mp3|mp4|m4a|wav|webm|mov|zip|gz|tgz|pdf|woff2?|ttf|otf|sqlite|db)$/i;

// Account names that are not one person's machine: placeholders (`<you>`, `%USERNAME%`,
// `YOUR_NAME`, a lone `x`, "your account" in the tutorial languages), Windows' own profiles and
// GitHub's hosted Windows runner. An account name written in capitals passes, too.
const NOT_A_PERSON = String.raw`(?:<|%|\$|\{|\.\.\.|(?:[A-Z][A-Z0-9_]*|[a-z]|Public|Default|All Users|Shared|username|user|you|name|example|runneradmin)(?![\w-])|[^\\/\s"'<>]*(?:你的|您的|あなた|사용자|ユーザー))`;
// Test-only credentials that the CI workflows (.github/workflows/ci.yml) define in the open.
const CI_TEST_VALUES = new Set(["travel", "community-test-only-password"]);
const PLACEHOLDER_VALUE = /^(?:<.*>?|\$.*|%.*%?|\{.*\}?|\*+|\.\.\.|x+|redacted|changeme)$/i;
// `password=url.password`, `password=secrets.token_urlsafe(32)`, `password=db_password`: code
// that reads a value, not a value.
const CODE_VALUE = /^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\.[A-Za-z_]\w*|\()|^[A-Za-z_]*(?:pass|pw|secret|token)\w*$/i;

function placeholderOrCode(raw) {
  const value = raw.replace(/^(["'])(.*)\1$/, "$2");
  if (value === "") return true;
  return PLACEHOLDER_VALUE.test(value) || CODE_VALUE.test(value) || CI_TEST_VALUES.has(value);
}

const CHECKS = [
  {
    name: "user-path",
    // C:\Users\<name>, C:/Users/<name>, JSON-escaped C:\\Users\\<name>, Git Bash /c/Users/<name>,
    // WSL /mnt/c/Users/<name>, and Claude Code's project slug C--Users-<name>-...
    patterns: [
      new RegExp(String.raw`(?<![A-Za-z0-9_])[A-Za-z]:(?:\\+|/+)(?:Users|users|USERS)(?:\\+|/+)(?!${NOT_A_PERSON})[^\\/\s"'<>]+`, "g"),
      new RegExp(String.raw`(?<![\w.-])(?:/mnt)?/[a-z]/Users/(?!${NOT_A_PERSON})[^\\/\s"'<>]+`, "g"),
      /(?<![A-Za-z0-9])[A-Z]--Users-[A-Za-z0-9]+(?=-|\\|\/|$)/gm,
    ],
  },
  {
    name: "plink-load",
    patterns: [/\bplink(?:\.exe)?["']?(?:\s+\S+){0,6}?\s+-load\s+["']?(?![<$%{])[^\s"'\\]+/gi],
  },
  {
    name: "password",
    patterns: [/(?<![\w-])[\w-]*password\s*=(?!=)\s*("[^"\n]*"|'[^'\n]*'|[^\s"'`,;)&|\\]*)/gi],
    allow: (match) => placeholderOrCode(match[1] ?? ""),
  },
  {
    name: "db-url-password",
    patterns: [
      /\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|rediss?|amqps?)(?:\+[a-z0-9]+)?:\/\/[^\s:@/"'`]+:([^\s@/"'`]+)@/gi,
    ],
    allow: (match) => placeholderOrCode(match[1]),
  },
];

function findings(text) {
  const found = [];
  for (const check of CHECKS) {
    for (const pattern of check.patterns) {
      for (const match of text.matchAll(pattern)) {
        if (check.allow?.(match)) continue;
        const line = text.slice(0, match.index).split("\n").length;
        found.push({ check: check.name, line });
      }
    }
  }
  return found;
}

// Files that still carry a host detail, with how many of each are tolerated. There are two
// reasons only. A digest recorded elsewhere binds the file, so scrubbing it means rebinding
// every receipt in the chain in the same change, with a dated note beside each new digest
// (task 2026-10-02-rebind-receipts-after-scrubbing-host-details did that for eleven files).
// Or the file is another ticket's: a file in tasks/open is written only by its owner, so
// it is cleaned when the owner next edits it. A task file is keyed by its id, so moving it from
// open/ to done/ keeps its entry. The numbers only go down: when you clean a file, lower its
// entry or delete it.
const KNOWN = {
  "docs/videos/sothatswhy-t27/author-note.md": { "user-path": 1 },
  "docs/videos/sothatswhy-t27/branding-adoption.json": { "user-path": 9 },
  "docs/videos/sothatswhy-t27/fact-source-audit.json": { "user-path": 6 },
  "docs/videos/sothatswhy-t27/final-runtime-review.json": { "user-path": 42 },
  "docs/videos/sothatswhy-t27/final-runtime-review.md": { "user-path": 2 },
  "docs/videos/sothatswhy-t27/production-record.md": { "user-path": 1 },
  "docs/videos/sothatswhy-t27/runtime-audit.json": { "user-path": 11 },
  "docs/videos/sothatswhy-t27/runtime-audit.md": { "user-path": 7 },
  "docs/videos/sothatswhy-t27/visual-review.json": { "user-path": 234 },
  "docs/videos/sothatswhy-t27/visual-review.md": { "user-path": 2 },
  "tasks/2026-09-07-contextual-travel-services.md": { "user-path": 1 },
  "tasks/2026-09-07-hotel-platform-options-and-quote-readiness.md": { "user-path": 1 },
  "tasks/2026-09-16-news-batch-4-4-the-8.md": { "user-path": 1 },
  "tasks/2026-09-20-five-language-article-batch-003.md": { "user-path": 2 },
  "tasks/2026-09-20-fix-nonroot-source-mount-permissions-in.md": { "user-path": 1 },
  "tasks/2026-09-20-launch-articles-batch-8.md": { "user-path": 2 },
  "tasks/2026-09-20-launch-korea-food-specials-1.md": { "user-path": 2 },
  "tasks/2026-09-20-localize-hong-kong-ferry-tram-zh.md": { "user-path": 1 },
  "tasks/2026-09-20-visitjeju-hidden-payload-recheck.md": { "user-path": 1 },
  "tasks/2026-09-21-taiwan-zh-tw-third-sub-batch.md": { "user-path": 1 },
  "tasks/2026-09-27-correct-wordpress-user-roles-unrelated-ai.md": { "user-path": 2 },
  "tasks/2026-09-27-general-audience-ai-agent-versus-chatbot.md": { "user-path": 1 },
  "tasks/2026-09-27-general-audience-ai-citation-checking-video.md": { "user-path": 1 },
  "tasks/2026-09-27-integrate-batch029-wordpress-contact-guides.md": { "user-path": 2 },
  "tasks/2026-09-27-localize-wordpress-chat-and-booking-batch029.md": { "user-path": 4 },
  "tasks/2026-09-27-localize-wordpress-contact-forms-and-smtp.md": { "user-path": 3 },
  "tasks/2026-09-28-batch032-wordpress-five-language-content.md": { "user-path": 1 },
  "tasks/2026-09-28-correct-measurement-guide-source-links-before.md": { "user-path": 1 },
  "tasks/2026-09-28-drama-listener-stale-check.md": { "user-path": 1 },
  "tasks/2026-09-28-drama-revised-document-readiness.md": { "user-path": 2 },
  "tasks/2026-09-28-video-1m-ai-agents.md": { "user-path": 2 },
  "tasks/2026-09-28-video-1m-ai-price-war.md": { "user-path": 2 },
  "tasks/2026-09-28-video-1m-free-vs-paid.md": { "user-path": 2 },
  "tasks/2026-09-28-video-1m-google-vids-free.md": { "user-path": 1 },
  "tasks/2026-09-28-video-1m-siri-ai.md": { "user-path": 1 },
  "tasks/2026-09-28-video-1m-vibe-coding.md": { "user-path": 1 },
  "tasks/2026-09-29-resume-imported-long-video-languages.md": { "user-path": 2 },
  "tasks/2026-10-02-investigate-loading-query-timeouts-under-windows.md": { "user-path": 1 },
  "tasks/2026-10-02-produce-one-t27-japan-trash-bin.md": { "user-path": 1 },
};

function key(path) {
  return path.replace(/^tasks\/(?:open|done)\//, "tasks/");
}

function scan() {
  const listed = execFileSync("git", ["ls-files", "-z", "--", ...AREAS], {
    cwd: ROOT,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  const result = new Map();
  for (const path of listed.split("\0")) {
    if (!path || BINARY.test(path)) continue;
    let text;
    try {
      text = readFileSync(join(ROOT, path), "utf8");
    } catch {
      continue; // listed but deleted in the working tree
    }
    if (text.includes("\0")) continue;
    const found = findings(text);
    if (found.length) result.set(path, found);
  }
  return result;
}

const scanned = scan();

function counts(found) {
  const byCheck = {};
  for (const { check } of found) byCheck[check] = (byCheck[check] ?? 0) + 1;
  return byCheck;
}

test("no tracked file under docs/, tasks/ or ops/ gains a host detail", () => {
  const offences = [];
  for (const [path, found] of scanned) {
    const allowed = KNOWN[key(path)] ?? {};
    for (const [check, count] of Object.entries(counts(found))) {
      if (count <= (allowed[check] ?? 0)) continue;
      const lines = found.filter((f) => f.check === check).map((f) => f.line);
      offences.push(`${path}: ${check} on line ${[...new Set(lines)].join(", ")}`);
    }
  }
  assert.deepEqual(offences, [], "replace with <repo>, <home>, <saved-session> or <disposable-password>");
});

test("the tolerated list only shrinks", () => {
  const byKey = new Map([...scanned].map(([path, found]) => [key(path), counts(found)]));
  const stale = [];
  for (const [file, allowed] of Object.entries(KNOWN)) {
    const now = byKey.get(file) ?? {};
    for (const [check, count] of Object.entries(allowed)) {
      if ((now[check] ?? 0) < count) stale.push(`${file}: ${check} is down to ${now[check] ?? 0}; lower KNOWN`);
    }
  }
  assert.deepEqual(stale, []);
});

test("each check catches its leak and leaves placeholders alone", () => {
  const caught = (text) => findings(text).map((f) => f.check);
  assert.deepEqual(caught(String.raw`cd C:\Users\alice\repo`), ["user-path"]);
  assert.deepEqual(caught(String.raw`{"cwd": "C:\\Users\\alice\\repo"}`), ["user-path"]);
  assert.deepEqual(caught("cd c:/users/alice/repo"), ["user-path"]);
  assert.deepEqual(caught("/c/Users/alice/repo/apps/api"), ["user-path"]);
  assert.deepEqual(caught("/mnt/c/Users/alice/repo"), ["user-path"]);
  assert.deepEqual(caught(String.raw`%TEMP%\claude\C--Users-alice-repo\scratchpad`), ["user-path"]);
  assert.deepEqual(caught(String.raw`& 'C:\Program Files\PuTTY\plink.exe' -load prodbox -batch 'id'`), [
    "plink-load",
  ]);
  assert.deepEqual(caught("plink -batch -l root -load prodbox uptime"), ["plink-load"]);
  assert.deepEqual(caught("--env POSTGRES_PASSWORD=throwaway_9x2k"), ["password"]);
  assert.deepEqual(caught("postgresql+asyncpg://qa:throwaway_9x2k@127.0.0.1:5432/qa"), [
    "db-url-password",
  ]);

  for (const fine of [
    String.raw`cd <repo>\apps\api`,
    String.raw`C:\Users\<you>\AppData`,
    String.raw`C:\Users\%USERNAME%\.ssh`,
    String.raw`C:\Users\Public\Documents`,
    String.raw`Set-Location -LiteralPath 'C:\Users\YOUR_NAME\Documents\lab'`,
    "Set-Location -LiteralPath 'C:\\Users\\\u4f60\u7684\u5e33\u865f\\Downloads'",
    String.raw`home folders such as C:\Users\x are blocked`,
    String.raw`C:\Users\runneradmin\AppData\Local\Temp`,
    "https://support.google.com/a/users/answer/10665800",
    "plink -load <saved-session> -batch 'id'",
    "POSTGRES_PASSWORD=travel",
    "MINIO_ROOT_PASSWORD=community-test-only-password",
    "POSTGRES_PASSWORD=<disposable-password>",
    "POSTGRES_PASSWORD=$POSTGRES_PASSWORD",
    "password=url.password",
    "password = secrets.token_urlsafe(32)",
    "connect(user=user, password=db_password)",
    "if password == expected:",
    "postgresql+asyncpg://travel:travel@postgres:5432/travel_scanner",
    "postgresql+asyncpg://tutorial_test:{password}@localhost/db",
    "https://user:secret@example.com/",
  ]) {
    assert.deepEqual(caught(fine), [], fine);
  }
});
