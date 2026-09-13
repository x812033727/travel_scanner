/**
 * The article routes live in their own root group, and a route group does not inherit the
 * boundaries of the one next to it. Without this file `notFound()` — which
 * `guides/[kind]/[slug]` calls deliberately for a `/guides/life/<slug>` URL — falls through
 * to Next's own screen: English only, on a site that ships five languages.
 */
export { default } from "@/app/[locale]/not-found";
