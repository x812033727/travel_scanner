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
 */
const CODE = /^[a-z][a-z0-9_]*$/;

export function translateWarnings(
  warnings: readonly string[] | undefined,
  known: ReadonlySet<string>,
  translate: (key: string) => string,
): string[] {
  return (warnings || [])
    .map((warning) => {
      if (!CODE.test(warning)) return warning;
      return known.has(warning) ? translate(`warning.${warning}`) : "";
    })
    .filter(Boolean);
}
