import { notFound } from "next/navigation";

/**
 * Next resolves an address that matches no route against the root not-found, which
 * has no locale and no providers — so the reader got Next's own English screen on a
 * site that ships five languages. This catch-all pulls unmatched paths back into the
 * locale segment, where [locale]/not-found.tsx answers in their language.
 */
export default function LocaleCatchAll() {
  notFound();
}
