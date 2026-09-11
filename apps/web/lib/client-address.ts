/**
 * The visitor's address as our own reverse proxy reported it.
 *
 * Shared because two callers need the identical reading. The BFF forwards it on every
 * browser call, and the server-rendered pages -- which reach the API directly, without
 * passing through the BFF -- have to forward the same value or their traffic arrives
 * anonymous and indistinguishable from one very busy container.
 *
 * The right-most `x-forwarded-for` entry is the one our proxy appended; everything to
 * its left was supplied by the caller and can say anything at all.
 */
export function forwardedClientAddress(headers: Headers): string | undefined {
  const forwarded = headers.get("x-forwarded-for")
    ?.split(",")
    .map((value) => value.trim())
    .filter(Boolean)
    .at(-1);
  const candidate = forwarded || headers.get("x-real-ip")?.trim();
  return candidate && candidate.length <= 64 ? candidate : undefined;
}
