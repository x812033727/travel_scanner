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
