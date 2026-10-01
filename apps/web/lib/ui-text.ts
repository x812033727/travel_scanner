/**
 * Administrator overrides layered over the bundled message catalogs.
 *
 * `apps/web/messages` stays the versioned default; the API serves only the sentences an
 * administrator changed, and `applyUiTextOverrides` merges the two before next-intl ever
 * sees them. Everything here is pure so the admin editor can reuse it in the browser.
 *
 * See `docs/ui-text-overrides.md`.
 */
import { IntlMessageFormat } from "intl-messageformat";

// The namespaces of i18n/request.ts minus `legacy`. Kept in step with the API's own
// allowlist by tools/check-i18n.mjs.
export const EDITABLE_NAMESPACES = [
  "account",
  "admin",
  "alerts",
  "auth",
  "availability",
  "catalogReview",
  "common",
  "community",
  "errors",
  "foodAdmin",
  "foods",
  "hotspotAdmin",
  "hotspotThemes",
  "hotspots",
  "metadata",
  "navigation",
  "newTrip",
  "pricing",
  "restaurants",
  "search",
  "stayAreas",
  "travelServices",
  "trips",
  "usage",
] as const;

export type EditableNamespace = (typeof EDITABLE_NAMESPACES)[number];

/**
 * `legacy` drives components/legacy-ui-localizer.tsx, which rewrites DOM text by literal
 * zh-TW string. An override there would rewrite city and trip names coming from the API,
 * so it is refused in the admin API, in a database CHECK, and here.
 */
export const LOCKED_NAMESPACES = ["legacy"] as const;

export const UI_TEXT_MAX_LENGTH = 2000;
export const UI_TEXT_BATCH_LIMIT = 100;

// Retained for the editor's placeholder list and the API's lexical helper. Validation
// below uses the parser so compact plural branches are not mistaken for arguments.
const ICU_PARAMETER_PATTERN = /\{([A-Za-z_][\w]*)/g;

export type UiTextEntries = Record<string, string>;

export type UiTextPayload = {
  locale: string;
  version: string;
  entries: UiTextEntries;
};

export type SkipReason =
  | "locked_namespace"
  | "unknown_namespace"
  | "missing_default"
  | "not_a_leaf"
  | "parameter_mismatch";

export type MergeResult = {
  messages: Record<string, unknown>;
  applied: number;
  skipped: { key: string; reason: SkipReason }[];
};

export function isEditableNamespace(value: unknown): value is EditableNamespace {
  return EDITABLE_NAMESPACES.includes(value as EditableNamespace);
}

/** Unique placeholder names, sorted — set semantics, matching the API. */
export function messageParameters(message: string): string[] {
  const names = new Set<string>();
  for (const match of message.matchAll(ICU_PARAMETER_PATTERN)) names.add(match[1]);
  return [...names].sort();
}

/** True when the default uses ICU plural/select, whose brace structure must be preserved. */
export function hasAdvancedIcu(message: string): boolean {
  return /\{\s*[A-Za-z_]\w*\s*,\s*(plural|select|selectordinal)\b/.test(message);
}

export function bracesBalanced(message: string): boolean {
  let depth = 0;
  for (const character of message) {
    if (character === "{") depth += 1;
    else if (character === "}") {
      depth -= 1;
      if (depth < 0) return false;
    }
  }
  return depth === 0;
}

type IcuElements = ReturnType<IntlMessageFormat["getAst"]>;
type IcuSignature = Array<string | number | IcuSignature>;

/** Preserve runtime arguments in each branch, while leaving literal copy editable. */
function runtimeSignature(elements: IcuElements, literalTokens: Set<string>): IcuSignature {
  const signatures: IcuSignature[] = [];
  for (const element of elements) {
    if (element.type === 0) {
      // Help text intentionally quotes URL templates; those literal tokens must survive.
      for (const match of element.value.matchAll(/\{([A-Za-z_]\w*)\}/g)) {
        literalTokens.add(match[1]);
      }
      continue;
    }
    if (element.type === 7) {
      signatures.push([element.type]);
    } else if (element.type === 5 || element.type === 6) {
      const branches: IcuSignature = Object.keys(element.options).sort().map((selector) => [
        selector, runtimeSignature(element.options[selector].value, literalTokens),
      ]);
      signatures.push(element.type === 6
        ? [element.type, element.value, element.pluralType ?? "cardinal", element.offset, branches]
        : [element.type, element.value, branches]);
    } else if (element.type === 8) {
      // ignoreTag makes HTML-like help text literal; no rich-text arguments are expected.
      throw new Error("Unexpected ICU tag");
    } else {
      signatures.push([element.type, element.value]);
    }
  }
  // Repeating a simple argument within the same branch remains a copy choice. Retain
  // structured children: embedding serialized JSON would multiply escaping per depth.
  const unique = new Map(signatures.map((signature) => [JSON.stringify(signature), signature]));
  return [...unique.keys()].sort().map((key) => unique.get(key)!);
}

function messageSignature(message: string): string {
  // This is the same parser used by next-intl. Looking at every branch catches
  // quoted-away arguments that rendering one sample value would miss.
  const ast = new IntlMessageFormat(message, "en", undefined, { ignoreTag: true }).getAst();
  const literalTokens = new Set<string>();
  const runtime = runtimeSignature(ast, literalTokens);
  return JSON.stringify({ runtime, literalTokens: [...literalTokens].sort() });
}

/**
 * Why an override cannot replace this default, or undefined when it can. A literal-token
 * guard also protects intentionally quoted URL templates, while the AST protects
 * arguments and plural/select behavior that next-intl actually evaluates.
 */
export function overrideProblem(
  value: string,
  defaultValue: string,
): "braces" | "parameters" | undefined {
  let expectedSignature: string;
  let actualSignature: string;
  try {
    expectedSignature = messageSignature(defaultValue);
    actualSignature = messageSignature(value);
  } catch {
    return "braces";
  }
  if (actualSignature !== expectedSignature) return "parameters";
  return undefined;
}

/** Dotted paths to leaf strings, in catalog order. Mirrors flatten() in check-i18n.mjs. */
export function flattenMessages(
  value: unknown,
  prefix = "",
  result: UiTextEntries = {},
): UiTextEntries {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return result;
  for (const [key, child] of Object.entries(value as Record<string, unknown>)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (child !== null && typeof child === "object" && !Array.isArray(child)) {
      flattenMessages(child, path, result);
    } else {
      result[path] = String(child);
    }
  }
  return result;
}

export function isUiTextPayload(value: unknown): value is UiTextPayload {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Record<string, unknown>;
  if (typeof candidate.locale !== "string" || typeof candidate.version !== "string") return false;
  if (typeof candidate.entries !== "object" || candidate.entries === null) return false;
  return Object.values(candidate.entries as Record<string, unknown>).every(
    (entry) => typeof entry === "string",
  );
}

export function chunk<T>(items: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let index = 0; index < items.length; index += size) {
    chunks.push(items.slice(index, index + size));
  }
  return chunks;
}

/**
 * Layer overrides on top of the bundled catalogs.
 *
 * Copy-on-write, and not optionally so: `messages` holds the JSON modules `import()`
 * returned, which Node caches for the life of the process. Writing into them would
 * overwrite the bundled default permanently — "restore default" would then need a
 * restart, and the parameter check below would start comparing against an already
 * overridden value.
 *
 * An override never creates a key. One whose namespace is locked or unknown, whose key
 * has left the catalog, whose path is not a string leaf, or whose placeholders no longer
 * match the default is skipped and reported, so a stale row cannot put a raw key path or
 * a formatting error on the page.
 */
export function applyUiTextOverrides(
  messages: Record<string, unknown>,
  entries: UiTextEntries,
): MergeResult {
  const skipped: { key: string; reason: SkipReason }[] = [];
  let applied = 0;
  let result = messages;

  for (const [path, value] of Object.entries(entries)) {
    const separator = path.indexOf(".");
    if (separator <= 0) {
      skipped.push({ key: path, reason: "missing_default" });
      continue;
    }
    const namespace = path.slice(0, separator);
    if ((LOCKED_NAMESPACES as readonly string[]).includes(namespace)) {
      skipped.push({ key: path, reason: "locked_namespace" });
      continue;
    }
    if (!isEditableNamespace(namespace)) {
      skipped.push({ key: path, reason: "unknown_namespace" });
      continue;
    }

    const segments = path.slice(separator + 1).split(".");
    // Walk the existing tree first: nothing is copied until the override is known good.
    let node: unknown = result[namespace];
    for (const segment of segments.slice(0, -1)) {
      if (node === null || typeof node !== "object" || Array.isArray(node)) {
        node = undefined;
        break;
      }
      node = (node as Record<string, unknown>)[segment];
    }
    const leaf = segments[segments.length - 1];
    const parent =
      node !== null && typeof node === "object" && !Array.isArray(node)
        ? (node as Record<string, unknown>)
        : undefined;
    if (!parent || !(leaf in parent)) {
      skipped.push({ key: path, reason: "missing_default" });
      continue;
    }
    const defaultValue = parent[leaf];
    if (typeof defaultValue !== "string") {
      skipped.push({ key: path, reason: "not_a_leaf" });
      continue;
    }
    if (overrideProblem(value, defaultValue)) {
      skipped.push({ key: path, reason: "parameter_mismatch" });
      continue;
    }

    if (result === messages) result = { ...messages };
    // Clone every object along the path, so untouched branches keep their identity.
    let cursor = result as Record<string, unknown>;
    let key: string = namespace;
    for (const segment of segments.slice(0, -1)) {
      cursor[key] = { ...(cursor[key] as Record<string, unknown>) };
      cursor = cursor[key] as Record<string, unknown>;
      key = segment;
    }
    cursor[key] = { ...(cursor[key] as Record<string, unknown>), [leaf]: value };
    applied += 1;
  }

  return { messages: result, applied, skipped };
}
