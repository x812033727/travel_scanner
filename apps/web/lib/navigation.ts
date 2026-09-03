export function safeNextPath(value: string | string[] | null | undefined, fallback = "/") {
  const candidate = Array.isArray(value) ? value[0] : value;
  if (
    !candidate
    || !candidate.startsWith("/")
    || candidate.startsWith("//")
    || candidate.includes("\\")
    || /[\u0000-\u001f\u007f]/.test(candidate)
  ) return fallback;
  return candidate;
}

export function loginPath(nextPath: string) {
  return `/login?next=${encodeURIComponent(safeNextPath(nextPath))}`;
}

const WEB_LINK_PROTOCOLS = ["http:", "https:"] as const;

/**
 * Accept a provider-, AI-, or admin-supplied URL for an `href`, form action, or navigation only
 * when it uses an expected scheme. React already neutralises `javascript:` URLs in `href`, but
 * `window.location.assign` does not, and this keeps `data:`/`file:`/custom schemes out as well.
 */
export function safeExternalHref(
  value: string | null | undefined,
  allowedProtocols: readonly string[] = WEB_LINK_PROTOCOLS,
): string | undefined {
  if (!value) return undefined;
  let parsed: URL;
  try {
    parsed = new URL(value);
  } catch {
    return undefined;
  }
  return allowedProtocols.includes(parsed.protocol) ? value : undefined;
}
