/**
 * The API's `warnings` arrays carry two different things.
 *
 * Its own warnings are codes — `walk_route_beta`, `weather_beyond_forecast` — so the
 * reader's catalog can say them in the reader's language. They used to be whole
 * Traditional Chinese sentences, printed verbatim on every locale.
 *
 * But not everything in those arrays is ours: the weather provider is asked for the
 * reader's language and returns its own advisories as free text, already localised.
 * Dropping those would throw away real content, so shape decides. A code-shaped
 * string this build does not know renders nothing — its own name helps nobody — and
 * anything that is not code-shaped is passed through as it came.
 *
 * A warning that has to name something — a currency, a module, the day it could not
 * compare — carries its values in the same string, after a `?`:
 *
 *     stale_exchange_rate?currency=JPY
 *     provider_fallback?module=flights&provider=Amadeus
 *
 * `app/warnings.py` writes them; the values are percent-encoded there, so a provider
 * called `Trip.com & co` cannot split the string apart. The shape test still decides:
 * a sentence that happens to contain a question mark is not a code, and is passed
 * through untouched.
 */
const CODE = /^[a-z][a-z0-9_]*$/;
const PARAMETERISED = /^([a-z][a-z0-9_]*)\?([A-Za-z0-9_%.+~-]+=[^&\s]*(?:&[A-Za-z0-9_%.+~-]+=[^&\s]*)*)$/;

function parse(warning: string): { code: string; values?: Record<string, string> } | null {
  if (CODE.test(warning)) return { code: warning };
  const match = PARAMETERISED.exec(warning);
  if (!match) return null;
  const values: Record<string, string> = {};
  for (const [name, value] of new URLSearchParams(match[2])) values[name] = value;
  return { code: match[1], values };
}

export function translateWarnings(
  warnings: readonly string[] | undefined,
  known: ReadonlySet<string>,
  translate: (key: string, values?: Record<string, string>) => string,
): string[] {
  return (warnings || [])
    .map((warning) => {
      const parsed = parse(warning);
      if (!parsed) return warning;
      return known.has(parsed.code) ? translate(`warning.${parsed.code}`, parsed.values) : "";
    })
    .filter(Boolean);
}
