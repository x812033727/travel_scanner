import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";

import { IntlMessageFormat } from "intl-messageformat";

import { checkI18n, parameters } from "./check-i18n.mjs";

const ROOT = resolve(import.meta.dirname, "..");
const LOCALES = ["en", "ja", "ko", "zh-TW", "zh-CN"];

function write(root, relative, text) {
  const file = join(root, relative);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, text);
}

function fixture(t, reference, translations = {}) {
  const root = mkdtempSync(join(tmpdir(), "check-i18n-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  for (const locale of LOCALES) {
    write(root, `apps/web/messages/${locale}/example.json`, JSON.stringify(translations[locale] ?? reference));
    write(root, `apps/web/messages/${locale}/admin.json`, JSON.stringify({
      uiText: { namespaces: { admin: "Admin", example: "Example" } },
    }));
  }
  write(root, "apps/api/app/ui_text/schemas.py", 'UI_TEXT_NAMESPACES: tuple[str, ...] = ("admin", "example")\n');
  write(root, "apps/web/lib/ui-text.ts", 'export const EDITABLE_NAMESPACES = ["admin", "example"];\n');
  return root;
}

function catalog(locale, namespace) {
  return JSON.parse(readFileSync(join(ROOT, "apps/web/messages", locale, `${namespace}.json`), "utf8"));
}

test("ICU apostrophe quoting distinguishes literals from substituted parameters", () => {
  assert.deepEqual(parameters("'{source}'"), []);
  assert.deepEqual(parameters("‘{source}’"), ["source"]);
  assert.deepEqual(parameters("''{source}''"), ["source"]);
  assert.deepEqual(parameters("You're booking {name}"), ["name"]);
  assert.deepEqual(parameters("{last}, {first}, {last}"), ["first", "last"]);
});

test("all nested select, plural and ordinal branches contribute their arguments", () => {
  const message = "{kind, select, first {{count, plural, =0 {No {zero}} one {{person}} other {# {items}}}} other {{fallback}}}";
  assert.deepEqual(parameters(message), ["count", "fallback", "items", "kind", "person", "zero"]);
  assert.deepEqual(parameters("{place, selectordinal, one {{winner}} other {# {runners}}}"), ["place", "runners", "winner"]);
  assert.deepEqual(parameters("{count, plural, one {one item} other {# items}}"), ["count"]);
});

test("number, date and time formats are arguments without needing marker values", () => {
  assert.deepEqual(parameters("{amount, number, ::currency/USD} on {when, date, short} at {clock, time, short}"), ["amount", "clock", "when"]);
});

test("path examples and markup do not change ICU argument extraction", () => {
  assert.deepEqual(parameters("Put <slug> under <VIDEO_WORKDIR>/_sfx/<name>/ with {filename}"), ["filename"]);
  assert.deepEqual(parameters("<strong>{name}</strong>"), ["name"]);
});

test("malformed ICU syntax is rejected instead of being treated as no parameters", () => {
  assert.throws(() => parameters("Hello {name"), /EXPECT_ARGUMENT_CLOSING_BRACE/);
  assert.throws(() => parameters("{count, plural, one {item}}"), /MISSING_OTHER_CLAUSE/);
});

test("a locale that escapes an English parameter fails the catalog check", (t) => {
  const root = fixture(t, { label: "The {source} model" }, { ko: { label: "'{source}' 모델" } });
  const result = checkI18n(root);
  assert.deepEqual(result.errors, ["ko/example.json:label: ICU parameters differ from en"]);
  assert.equal(result.localeCount, 5);
  assert.equal(result.namespaceCount, 2);
});

test("curly and doubled apostrophes both preserve the catalog's parameter contract", (t) => {
  const root = fixture(t, { label: "The {source} model" }, {
    ko: { label: "‘{source}’ 모델" },
    ja: { label: "''{source}'' モデル" },
  });
  assert.deepEqual(checkI18n(root).errors, []);
});

test("tokens intentionally literal in English are also allowed to be literal in a translation", (t) => {
  const root = fixture(t, { help: "URL: '{destination}' and '{departure_date}'" }, {
    ko: { help: "URL: '{departure_date}', '{destination}'" },
  });
  assert.deepEqual(checkI18n(root).errors, []);
});

test("turning a literal English token into an argument also fails the contract", (t) => {
  const root = fixture(t, { help: "Use '{destination}' in the URL" }, {
    ko: { help: "URL의 {destination}" },
  });
  assert.deepEqual(checkI18n(root).errors, ["ko/example.json:help: ICU parameters differ from en"]);
});

test("literal template tokens still cannot be dropped or renamed in translations", (t) => {
  const root = fixture(t, { help: "URL: '{destination}' for {name}" }, {
    ko: { help: "URL for {name}" },
    ja: { help: "URL: '{place}' for {name}" },
  });
  assert.deepEqual(checkI18n(root).errors, [
    "ja/example.json:help: ICU parameters differ from en",
    "ko/example.json:help: ICU parameters differ from en",
  ]);
});

test("a quoted argument in a non-default nested branch is still detected", (t) => {
  const source = "{kind, select, special {{count, plural, one {{person}} other {# {items}}}} other {{fallback}}}";
  const root = fixture(t, { label: source }, { ko: { label: source.replace("{person}", "'{person}'") } });
  assert.deepEqual(checkI18n(root).errors, ["ko/example.json:label: ICU parameters differ from en"]);
});

test("invalid translated ICU reports its locale, namespace and full key", (t) => {
  const root = fixture(t, { panel: { label: "Hello {name}" } }, { ko: { panel: { label: "Hello {name" } } });
  const { errors } = checkI18n(root);
  assert.equal(errors.length, 1);
  assert.match(errors[0], /ko\/example\.json:panel\.label:/);
  assert.match(errors[0], /EXPECT_ARGUMENT_CLOSING_BRACE/);
});

test("invalid English ICU is reported as an English source error", (t) => {
  const root = fixture(t, { label: "Hello {name" }, Object.fromEntries(
    LOCALES.filter((locale) => locale !== "en").map((locale) => [locale, { label: "Hello {name}" }]),
  ));
  const { errors } = checkI18n(root);
  assert.ok(errors.some((error) => /en\/example\.json:label:.*EXPECT_ARGUMENT_CLOSING_BRACE/.test(error)), errors.join("\n"));
});

test("the duplicate-key guard still reads raw JSON before parsing", (t) => {
  const root = fixture(t, { label: "Hello {name}" });
  write(root, "apps/web/messages/ko/example.json", '{"label":"hidden","label":"Hello {name}"}');
  assert.deepEqual(checkI18n(root).errors, [
    "ko/example.json:label: duplicate key, JSON.parse silently keeps the last one",
  ]);
});

test("missing translation keys are still rejected even if their parameters match", (t) => {
  const root = fixture(t, { first: "Hello {name}", second: "Goodbye {name}" }, {
    ko: { first: "Hello {name}" },
  });
  assert.deepEqual(checkI18n(root).errors, ["ko/example.json: translation keys differ from en"]);
});

test("the namespace and editable-allowlist guards remain active", (t) => {
  const root = fixture(t, { label: "Hello {name}" });
  rmSync(join(root, "apps/web/messages/ko/example.json"));
  write(root, "apps/web/lib/ui-text.ts", 'export const EDITABLE_NAMESPACES = ["admin"];\n');
  const { errors } = checkI18n(root);
  assert.ok(errors.includes("ko: namespace files differ from en"));
  assert.ok(errors.some((error) => error.startsWith("apps/web/lib/ui-text.ts: the editable namespace allowlist differs")));
});

test("the three repaired Korean messages actually render their supplied values", () => {
  const messages = [
    [catalog("ko", "admin").aiSettings.overview.inherits, "source"],
    [catalog("ko", "catalogReview").actionUnavailable, "action"],
    [catalog("ko", "hotspotThemes").intros.generateTitle, "name"],
  ];
  for (const [message, parameter] of messages) {
    const value = `TEST_${parameter.toUpperCase()}`;
    const rendered = new IntlMessageFormat(message, "ko").format({ [parameter]: value });
    assert.deepEqual(parameters(message), [parameter]);
    assert.ok(rendered.includes(`‘${value}’`), rendered);
    assert.ok(!rendered.includes(`{${parameter}}`), rendered);
  }
});

test("restoring the three original Korean strings reproduces all three contract failures", (t) => {
  const root = fixture(t, {
    inherits: catalog("en", "admin").aiSettings.overview.inherits,
    actionUnavailable: catalog("en", "catalogReview").actionUnavailable,
    generateTitle: catalog("en", "hotspotThemes").intros.generateTitle,
  }, { ko: {
    inherits: "'{source}'의 모델을 이어받음",
    actionUnavailable: "현재 '{action}' 작업을 할 수 없습니다",
    generateTitle: "'{name}' 소개문 생성",
  } });
  assert.deepEqual(checkI18n(root).errors, [
    "ko/example.json:inherits: ICU parameters differ from en",
    "ko/example.json:actionUnavailable: ICU parameters differ from en",
    "ko/example.json:generateTitle: ICU parameters differ from en",
  ]);
});

test("the actual Travelpayouts help keeps its documented tokens literal in all five locales", () => {
  const tokens = ["destination", "departure_date", "return_date", "sub_id"];
  for (const locale of LOCALES) {
    const message = catalog(locale, "admin").providerFields.travelpayouts_static_url_template.help;
    assert.deepEqual(parameters(message), [], locale);
    const rendered = new IntlMessageFormat(message, locale).format({});
    for (const token of tokens) assert.ok(rendered.includes(`{${token}}`), `${locale}: ${token}`);
  }
});

test("the repository CLI still validates the complete default catalog and exits successfully", () => {
  const result = spawnSync(process.execPath, [join(ROOT, "tools/check-i18n.mjs")], {
    cwd: ROOT,
    encoding: "utf8",
  });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /^Validated 5 locales across \d+ namespaces\./);
});
