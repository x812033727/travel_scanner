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
export function StructuredData({ data }: { data: object | object[] }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, "\\u003c") }}
    />
  );
}
