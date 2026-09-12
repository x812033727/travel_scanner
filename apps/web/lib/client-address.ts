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

/**
 * The address headers an internal caller sends upstream.
 *
 * The address and the token travel together on purpose: the API believes a forwarded
 * address only once a token is configured and matches, so a producer that sends one
 * without the other stops being counted per visitor rather than failing loudly. Without
 * an address there is nothing to vouch for, so the token is not sent alone either.
 *
 * The token exists because nothing at the network layer separates our own web container
 * from anything else that can reach the API: neither Compose file declares `networks:`,
 * so addresses are dynamic and the whole bridge is one flat trust domain.
 */
export function forwardedClientHeaders(incoming: Headers): Record<string, string> {
  const address = forwardedClientAddress(incoming);
  if (!address) return {};
  const headers: Record<string, string> = { "X-Travel-Client-IP": address };
  const token = process.env.INTERNAL_PROXY_TOKEN?.trim();
  if (token) headers["X-Travel-Proxy-Token"] = token;
  return headers;
}
