export function safeNextPath(value: string | string[] | null | undefined, fallback = "/") {
  const candidate = Array.isArray(value) ? value[0] : value;
  if (!candidate || !candidate.startsWith("/") || candidate.startsWith("//")) return fallback;
  return candidate;
}

export function loginPath(nextPath: string) {
  return `/login?next=${encodeURIComponent(safeNextPath(nextPath))}`;
}
