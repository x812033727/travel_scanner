import { stay22AllezCopy } from "./stay22-allez-copy";

const locales = new Set(["zh-TW", "zh-CN", "en", "ja", "ko"]);
const placements = new Set(["destination", "hotspot", "trip", "stay", "checklist"]);
const endpointPattern = /^\/api\/travel\/travel-services\/[a-f0-9-]+\/booking-options\/[a-f0-9-]+\/clickout$/;
const escape = (value: string) => value.replace(/[&<>"']/g, (character) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
}[character]!));

/** No external URL, arbitrary input, upstream message, or script may reach this document. */
export function hotelClickoutErrorPage({
  requestUrl, referrer, locale: requestedLocale, body, contentType, status,
}: {
  requestUrl: string; referrer: string | null; locale: string;
  body?: ArrayBuffer; contentType: string | null; status: number;
}): Response {
  const locale = locales.has(requestedLocale) ? requestedLocale : "zh-TW";
  const copy = stay22AllezCopy(locale);
  const url = new URL(requestUrl);
  const query = new URLSearchParams({ locale });
  const placement = url.searchParams.get("placement");
  if (placement && placements.has(placement)) query.set("placement", placement);
  let back = `/${locale}`;
  try {
    const requestedReturn = url.searchParams.get("return_to");
    const internalReturn = requestedReturn && requestedReturn.length <= 2048 &&
      requestedReturn.startsWith("/") && !requestedReturn.startsWith("//") &&
      !/[\\\u0000-\u0020]/.test(requestedReturn) ? requestedReturn : null;
    const source = new URL(internalReturn || referrer || back, url.origin);
    if (source.origin === url.origin && source.pathname.startsWith("/") &&
        !source.pathname.startsWith("//") && !source.pathname.startsWith("/api/") &&
        !/[\\\u0000-\u0020]/.test(`${source.pathname}${source.search}`)) {
      back = `${source.pathname}${source.search}`;
    }
  } catch { /* Use the internal home fallback. */ }
  query.set("return_to", back);
  const action = endpointPattern.test(url.pathname) ? `${url.pathname}?${query}` : null;
  const fields: [string, string][] = [];
  if (body && body.byteLength <= 4096 && contentType?.split(";", 1)[0] === "application/x-www-form-urlencoded") {
    const params = new URLSearchParams(new TextDecoder().decode(body));
    // Keep only bounded scalar form fields; no hidden URL, token, AID or campaign.
    for (const key of ["check_in", "check_out", "adults", "children"]) {
      const values = params.getAll(key);
      if (values.length === 1 && (/^(check_in|check_out)$/.test(key)
        ? /^\d{4}-\d{2}-\d{2}$/.test(values[0]) : /^\d{1,2}$/.test(values[0]))) {
        fields.push([key, values[0]]);
      }
    }
  }
  const hidden = fields.map(([key, value]) => `<input type="hidden" name="${key}" value="${escape(value)}">`).join("");
  const html = `<!doctype html><html lang="${locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="same-origin"><title>${escape(copy.errorTitle)}</title><style>
  *{box-sizing:border-box}body{margin:0;background:#f7f8fb;color:#192234;font:16px/1.6 system-ui,sans-serif;display:grid;min-height:100dvh;place-items:center;padding:24px}main{width:100%;max-width:520px;padding:clamp(24px,5vw,40px);background:white;border:1px solid #dce2e9;border-radius:24px;box-shadow:0 16px 64px #15233b0d;overflow-wrap:anywhere}h1{font-size:24px;line-height:1.35}p{color:#505f73}button,a{display:flex;min-height:48px;align-items:center;justify-content:center;width:100%;padding:12px 16px;border-radius:12px;font:inherit;text-decoration:none;cursor:pointer}button{border:0;background:#143e43;color:white}a{border:1px solid #cbd5df;color:#244455;margin-top:12px}button:focus-visible,a:focus-visible{outline:3px solid #197782;outline-offset:3px}small{display:block;margin-top:20px;color:#505f73}
  </style></head><body><main><h1>${escape(copy.errorTitle)}</h1><p>${escape(copy.errorDetail)}</p>${action ? `<form method="post" action="${escape(action)}">${hidden}<button type="submit">${escape(copy.retry)}</button></form>` : ""}<a href="${escape(back)}">${escape(copy.back)}</a><small>${escape(copy.openElsewhere)}</small></main></body></html>`;
  return new Response(html, {
    status: status >= 400 && status <= 599 ? status : 502,
    headers: {
      "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store",
      // Same-origin keeps retry POST Origin valid for the BFF's CSRF guard.
      // Successful external redirects separately enforce no-referrer.
      "Referrer-Policy": "same-origin", "X-Content-Type-Options": "nosniff",
      // HTTPS is needed for the trusted API's 303 affiliate destination; the
      // actual form action above is always an allowlisted first-party path.
      "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; form-action 'self' https:; base-uri 'none'; frame-ancestors 'none'",
    },
  });
}
