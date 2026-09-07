/**
 * Administrator overrides layered over the bundled message catalogs.
 *
 * `apps/web/messages` stays the versioned default; the API serves only the sentences an
 * administrator changed, and `applyUiTextOverrides` merges the two before next-intl ever
 * sees them. Everything here is pure so the admin editor can reuse it in the browser.
 *
 * See `docs/ui-text-overrides.md`.
 */

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

// The same expression tools/check-i18n.mjs uses, so the catalog check, this merge and the
// API's Python copy all agree on what counts as a placeholder.
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

/**
 * Why an override cannot replace this default, or undefined when it can. A plural that
 * lost its closing brace keeps its argument name, so only the brace check catches it —
 * and next-intl would render the raw key path in its place.
 */
export function overrideProblem(
  value: string,
  defaultValue: string,
): "braces" | "parameters" | undefined {
  if (!bracesBalanced(value)) return "braces";
  const expected = messageParameters(defaultValue).join(",");
  if (messageParameters(value).join(",") !== expected) return "parameters";
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
