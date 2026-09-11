/**
 * A JSON-LD block.
 *
 * No nonce, deliberately. `type="application/ld+json"` is a data block: the parser never executes
 * it, so `script-src` does not apply and the nonce-based policy in proxy.ts is not involved.
 * Taking one would mean calling `headers()` here and dragging every page that renders structured
 * data into a request-scoped render for nothing.
 *
 * Escaping `<` is not optional. Merchant names, hotspot names and post titles all flow into these
 * graphs, and one containing `</script>` would close this element early. `<` is a JSON escape
 * that parses back to `<`, so the graph is unchanged.
 */
export function StructuredData({ data }: { data: object | null | ReadonlyArray<object | null> }) {
  // A builder returns null rather than an empty graph (an empty BreadcrumbList is a Rich Results
  // error), so drop those instead of emitting `null` into the document.
  const graphs = (Array.isArray(data) ? data : [data]).filter((entry): entry is object => entry !== null);
  if (!graphs.length) return null;
  const payload = graphs.length === 1 ? graphs[0] : graphs;
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(payload).replace(/</g, "\\u003c") }}
    />
  );
}
