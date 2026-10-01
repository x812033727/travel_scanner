import { readFileSync } from "node:fs";
import { join } from "node:path";
import { IntlMessageFormat } from "intl-messageformat";
import { describe, expect, it } from "vitest";

import zhTwCommon from "@/messages/zh-TW/common.json";
import zhTwSearch from "@/messages/zh-TW/search.json";
import {
  EDITABLE_NAMESPACES,
  applyUiTextOverrides,
  bracesBalanced,
  chunk,
  flattenMessages,
  hasAdvancedIcu,
  isEditableNamespace,
  isUiTextPayload,
  messageParameters,
  overrideProblem,
} from "./ui-text";

function catalog() {
  return {
    navigation: { home: "首頁", trips: "我的旅程" },
    search: { results: { imageCredit: "圖片： " }, greeting: "你好，{name}" },
    usage: { charge: "{count, plural, one {# 次} other {# 次}}" },
    legacy: { 取消: "取消" },
  };
}

type IcuCase = {
  id: string;
  default: string;
  override: string;
  problem: "braces" | "parameters" | null;
  locale?: string;
  values?: Record<string, string | number>;
  rendered?: string;
};

const icuCases = JSON.parse(readFileSync(
  join(import.meta.dirname, "..", "..", "..", "docs", "ui-text-icu-cases.json"),
  "utf8",
)) as IcuCase[];

describe("shared ICU override cases", () => {
  it.each(icuCases)("$id", (example) => {
    expect(overrideProblem(example.override, example.default)).toBe(example.problem ?? undefined);
    const messages = { common: { message: example.default } };
    const merged = applyUiTextOverrides(messages, { "common.message": example.override });
    expect(merged.applied).toBe(example.problem ? 0 : 1);
    expect(merged.skipped).toEqual(example.problem
      ? [{ key: "common.message", reason: "parameter_mismatch" }]
      : []);
    const chosen = (merged.messages.common as Record<string, string>).message;
    expect(chosen).toBe(example.problem ? example.default : example.override);
    expect(messages.common.message).toBe(example.default);
    if (example.rendered !== undefined) {
      const formatter = new IntlMessageFormat(chosen, example.locale ?? "en", undefined, { ignoreTag: true });
      expect(formatter.format(example.values)).toBe(example.rendered);
    }
  });
});

describe("messageParameters", () => {
  it("keeps the legacy unique sorted lexical placeholder list", () => {
    expect(messageParameters("{count, plural, one {# day} other {# days}}")).toEqual(["count"]);
    expect(messageParameters("{b} {a} {b}")).toEqual(["a", "b"]);
    expect(messageParameters("{名字} and {# thing}")).toEqual([]);
    expect(messageParameters("'{destination}' is quoted")).toEqual(["destination"]);
    expect(messageParameters("plain")).toEqual([]);
  });

  it("uses the same expression as the catalog checker", () => {
    // The API, this merge and tools/check-i18n.mjs must agree on what a placeholder is;
    // if the checker's expression moves, this file has to move with it.
    const checker = readFileSync(
      join(import.meta.dirname, "..", "..", "..", "tools", "check-i18n.mjs"),
      "utf8",
    );
    expect(checker).toContain(String.raw`/\{([A-Za-z_][\w]*)/g`);
  });
});

describe("bracesBalanced and hasAdvancedIcu", () => {
  it("rejects a plural that lost its closing brace", () => {
    expect(bracesBalanced("{count, plural, one {# day} other {# days}}")).toBe(true);
    expect(bracesBalanced("{count, plural, one {# day}")).toBe(false);
    expect(bracesBalanced("}{")).toBe(false);
  });

  it("flags the defaults whose brace structure must be preserved", () => {
    expect(hasAdvancedIcu("{count, plural, one {# day} other {# days}}")).toBe(true);
    expect(hasAdvancedIcu("{mode, select, transit {轉乘} other {其他}}")).toBe(true);
    expect(hasAdvancedIcu("你好，{name}")).toBe(false);
  });
});

describe("overrideProblem", () => {
  it("accepts a rewrite that keeps every placeholder", () => {
    expect(overrideProblem("嗨，{name}！", "你好，{name}")).toBeUndefined();
    expect(overrideProblem("{count} / {count}", "{count}")).toBeUndefined();
    expect(overrideProblem(", ", ", ")).toBeUndefined();
  });

  it("names the reason it cannot be applied", () => {
    expect(overrideProblem("嗨", "你好，{name}")).toBe("parameters");
    expect(overrideProblem("嗨，{who}", "你好，{name}")).toBe("parameters");
    expect(overrideProblem("{count, plural, one {#}", "{count}")).toBe("braces");
  });

  it("checks a runtime name within each branch even when its literal token already appears elsewhere", () => {
    const original = "Help: '{name}'. {mode, select, short {{name}} other {{name}}}";
    const override = "Help: '{name}'. {mode, select, short {'{name}'} other {{name}}}";
    // A global set of runtime names and a global set of literal tokens both match.
    // The short branch still lost the only name it actually interpolates.
    expect(messageParameters(override)).toEqual(messageParameters(original));
    expect(new IntlMessageFormat(override, "en").format({ mode: "short", name: "Ada" }))
      .toBe("Help: {name}. {name}");
    expect(new IntlMessageFormat(override, "en").format({ mode: "other", name: "Ada" }))
      .toBe("Help: {name}. Ada");
    expect(overrideProblem(override, original)).toBe("parameters");
  });

  it("handles a deeply nested message within the editor's length limit", () => {
    const nest = (message: string) => Array.from({ length: 30 }, (_, index) => index)
      .reduce((inner, index) => `{choice${index}, select, other {${inner}}}`, message);
    const original = nest("Hello {name}");
    const override = nest("Welcome {name}");
    expect(override.length).toBeLessThan(2000);
    expect(overrideProblem(override, original)).toBeUndefined();
    expect(overrideProblem(nest("Welcome '{name}'"), original)).toBe("parameters");
    const values = { ...Object.fromEntries(Array.from({ length: 30 }, (_, index) => [`choice${index}`, "other"])), name: "Ada" };
    expect(new IntlMessageFormat(override, "en").format(values)).toBe("Welcome Ada");
  });
});

describe("flattenMessages", () => {
  it("produces dotted paths in catalog order", () => {
    expect(Object.keys(flattenMessages(catalog().search))).toEqual([
      "results.imageCredit",
      "greeting",
    ]);
    expect(flattenMessages(catalog().navigation)).toEqual({ home: "首頁", trips: "我的旅程" });
  });

  it("covers the real catalogs, hyphenated keys included", () => {
    const flat = flattenMessages(zhTwSearch);
    expect(Object.keys(flat).length).toBeGreaterThan(100);
    expect(Object.keys(flat).some((key) => key.includes("-"))).toBe(true);
    expect(Object.values(flat).every((value) => typeof value === "string")).toBe(true);
  });
});

describe("isUiTextPayload", () => {
  it("accepts the API shape and rejects anything else", () => {
    expect(isUiTextPayload({ locale: "en", version: "a", entries: { "a.b": "c" } })).toBe(true);
    expect(isUiTextPayload({ locale: "en", version: "a", entries: {} })).toBe(true);
    expect(isUiTextPayload({ locale: "en", version: "a", entries: { "a.b": 3 } })).toBe(false);
    expect(isUiTextPayload({ locale: "en", entries: {} })).toBe(false);
    expect(isUiTextPayload(null)).toBe(false);
  });
});

describe("applyUiTextOverrides", () => {
  it("keeps the working default when an old saved override quotes its argument away", () => {
    const original = "Hello {name}";
    const override = "Hello '{name}'";
    expect(new IntlMessageFormat(override, "en").format({ name: "Ada" })).toBe("Hello {name}");
    const messages = { common: { greeting: original, farewell: "Goodbye {name}" } };
    const merged = applyUiTextOverrides(messages, {
      "common.greeting": override,
      "common.farewell": "See you, ‘{name}’!",
    });
    const chosen = merged.messages.common as Record<string, string>;
    expect(merged.applied).toBe(1);
    expect(merged.skipped).toEqual([{ key: "common.greeting", reason: "parameter_mismatch" }]);
    expect(new IntlMessageFormat(chosen.greeting, "en").format({ name: "Ada" })).toBe("Hello Ada");
    expect(new IntlMessageFormat(chosen.farewell, "en").format({ name: "Ada" })).toBe("See you, ‘Ada’!");
    expect(messages.common.greeting).toBe(original);
    expect(messages.common.farewell).toBe("Goodbye {name}");
  });

  it("replaces a leaf without touching the input", () => {
    const messages = catalog();
    const snapshot = JSON.parse(JSON.stringify(messages));

    const result = applyUiTextOverrides(messages, { "navigation.home": "起點" });

    expect(result.applied).toBe(1);
    expect(result.skipped).toEqual([]);
    expect((result.messages.navigation as Record<string, string>).home).toBe("起點");
    expect((result.messages.navigation as Record<string, string>).trips).toBe("我的旅程");
    // Copy-on-write: request.ts hands us the JSON modules Node caches for the life of the
    // process, so a mutation here would outlive the request and defeat restore-default.
    expect(messages).toEqual(snapshot);
    expect(result.messages).not.toBe(messages);
    expect(result.messages.navigation).not.toBe(messages.navigation);
    expect(result.messages.search).toBe(messages.search);
  });

  it("replaces a nested leaf and keeps its siblings", () => {
    const messages = catalog();
    const result = applyUiTextOverrides(messages, {
      "search.results.imageCredit": "Photo: ",
      "search.greeting": "嗨，{name}",
    });

    expect(result.applied).toBe(2);
    const search = result.messages.search as { results: { imageCredit: string }; greeting: string };
    expect(search.results.imageCredit).toBe("Photo: ");
    expect(search.greeting).toBe("嗨，{name}");
    expect((messages.search as { greeting: string }).greeting).toBe("你好，{name}");
  });

  it("preserves leading and trailing space and newlines", () => {
    const messages = { common: { separator: ", ", note: "a\nb" } };
    const result = applyUiTextOverrides(messages, {
      "common.separator": " · ",
      "common.note": "c\nd",
    });
    expect(result.messages.common).toEqual({ separator: " · ", note: "c\nd" });
  });

  it("never creates a key and reports why each override was skipped", () => {
    const messages = catalog();
    const result = applyUiTextOverrides(messages, {
      "legacy.取消": "Cancel",
      "nope.key": "x",
      "navigation.gone": "x",
      "search.results": "x",
      "search.greeting": "嗨",
      bare: "x",
    });

    expect(result.applied).toBe(0);
    expect(result.messages).toBe(messages);
    expect(result.skipped).toEqual([
      { key: "legacy.取消", reason: "locked_namespace" },
      { key: "nope.key", reason: "unknown_namespace" },
      { key: "navigation.gone", reason: "missing_default" },
      { key: "search.results", reason: "not_a_leaf" },
      { key: "search.greeting", reason: "parameter_mismatch" },
      { key: "bare", reason: "missing_default" },
    ]);
    expect((messages.search as { results: unknown }).results).toEqual({ imageCredit: "圖片： " });
  });

  it("applies the good overrides in a batch that also carries bad ones", () => {
    const result = applyUiTextOverrides(catalog(), {
      "navigation.home": "起點",
      "navigation.gone": "x",
    });
    expect(result.applied).toBe(1);
    expect(result.skipped).toEqual([{ key: "navigation.gone", reason: "missing_default" }]);
  });

  it("keeps a plural override whose braces still balance", () => {
    const result = applyUiTextOverrides(catalog(), {
      "usage.charge": "{count, plural, one {# time} other {# times}}",
    });
    expect(result.applied).toBe(1);
    expect(result.skipped).toEqual([]);
  });

  it("merges over a real catalog and leaves every other key alone", () => {
    const messages = { common: zhTwCommon as unknown as Record<string, unknown> };
    const [firstKey, firstValue] = Object.entries(flattenMessages(zhTwCommon))[0];
    const result = applyUiTextOverrides(messages, { [`common.${firstKey}`]: "覆寫後的文字" });

    expect(result.applied).toBe(1);
    const merged = flattenMessages(result.messages.common);
    expect(merged[firstKey]).toBe("覆寫後的文字");
    expect(flattenMessages(zhTwCommon)[firstKey]).toBe(firstValue);
    expect(Object.keys(merged)).toEqual(Object.keys(flattenMessages(zhTwCommon)));
  });
});

describe("the editable namespace list", () => {
  it("matches the catalogs minus the locked one", () => {
    expect(EDITABLE_NAMESPACES).toHaveLength(24);
    expect(isEditableNamespace("travelServices")).toBe(true);
    expect(isEditableNamespace("community")).toBe(true);
    expect(EDITABLE_NAMESPACES).not.toContain("legacy");
    expect(isEditableNamespace("navigation")).toBe(true);
    expect(isEditableNamespace("catalogReview")).toBe(true);
    expect(isEditableNamespace("legacy")).toBe(false);
    expect(isEditableNamespace("nope")).toBe(false);
  });
});

describe("chunk", () => {
  it("splits a batch into request-sized pieces", () => {
    expect(chunk([1, 2, 3, 4, 5], 2)).toEqual([[1, 2], [3, 4], [5]]);
    expect(chunk([], 2)).toEqual([]);
    expect(chunk([1], 100)).toEqual([[1]]);
  });
});
