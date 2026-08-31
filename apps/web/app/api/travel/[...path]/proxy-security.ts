const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);

function normalizedOrigin(value: string | null | undefined): string | undefined {
  if (!value) return undefined;
  try {
    return new URL(value).origin;
  } catch {
    return undefined;
  }
}

export function observedRequestOrigin(headers: Headers, fallbackOrigin: string): string {
  const host = headers.get("host")?.trim();
  const forwardedProtocol = headers.get("x-forwarded-proto")?.split(",")[0]?.trim();
  const fallback = normalizedOrigin(fallbackOrigin);
  if (!fallback) return fallbackOrigin;
  const protocol = forwardedProtocol || new URL(fallback).protocol.slice(0, -1);
  if (!host || !/^(http|https)$/.test(protocol) || /[\s/@\\]/.test(host)) return fallback;
  return normalizedOrigin(`${protocol}://${host}`) || fallback;
}

export function validateProxyPath(path: string[]): string | undefined {
  if (path.length === 0) return undefined;
  const safe: string[] = [];
  for (const segment of path) {
    if (!segment || segment === "." || segment === ".." || /[\\/\0]/.test(segment)) {
      return undefined;
    }
    safe.push(encodeURIComponent(segment));
  }
  return safe.join("/");
}

export function isAllowedMutationOrigin(
  method: string,
  origin: string | null,
  requestOrigin: string,
  configuredSiteUrl?: string,
): boolean {
  if (SAFE_METHODS.has(method.toUpperCase())) return true;
  const candidate = normalizedOrigin(origin);
  if (!candidate) return false;
  const allowed = new Set([normalizedOrigin(requestOrigin), normalizedOrigin(configuredSiteUrl)]);
  return allowed.has(candidate);
}

export function safeRedirectLocation(
  location: string,
  requestOrigin: string,
): string | undefined {
  if (location.startsWith("/") && !location.startsWith("//")) return location;
  try {
    const target = new URL(location);
    if (target.protocol === "https:") return target.toString();
    if (target.protocol === "http:" && target.origin === normalizedOrigin(requestOrigin)) {
      return target.toString();
    }
  } catch {
    return undefined;
  }
  return undefined;
}

export function forwardedClientAddress(headers: Headers): string | undefined {
  const forwarded = headers.get("x-forwarded-for")
    ?.split(",")
    .map((value) => value.trim())
    .filter(Boolean)
    .at(-1);
  const candidate = forwarded || headers.get("x-real-ip")?.trim();
  return candidate && candidate.length <= 64 ? candidate : undefined;
}
