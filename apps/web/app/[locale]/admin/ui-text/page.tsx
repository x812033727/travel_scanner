import { getTranslations } from "next-intl/server";
import { AdminUiTextPanel } from "@/components/admin-ui-text-panel";
import { defaultLocale, isLocale, type Locale } from "@/i18n/routing";
import {
  EDITABLE_NAMESPACES,
  flattenMessages,
  isEditableNamespace,
  type EditableNamespace,
} from "@/lib/ui-text";

// The API has no copy of the message catalogs, so the defaults an editor is overriding
// come from here: the web bundle already carries all of them. Only the one namespace and
// locale being edited is loaded and sent to the client, rather than all 165 KB.
async function loadCatalog(locale: Locale, namespace: EditableNamespace) {
  const messages = (await import(`../../../../messages/${locale}/${namespace}.json`)).default;
  return flattenMessages(messages);
}

function first(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

export default async function AdminUiTextPage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const t = await getTranslations("admin.uiText");
  const query = await searchParams;

  // Fall back silently rather than redirect: the selects then show the effective value and
  // a stale bookmark cannot bounce between URLs.
  const requestedNamespace = first(query.ns);
  const namespace: EditableNamespace = isEditableNamespace(requestedNamespace)
    ? requestedNamespace
    : "common";
  const requestedLocale = first(query.locale);
  const locale: Locale = isLocale(requestedLocale) ? requestedLocale : defaultLocale;
  const requestedReference = first(query.ref);
  const reference: Locale =
    isLocale(requestedReference) && requestedReference !== locale
      ? requestedReference
      : locale === defaultLocale
        ? "en"
        : defaultLocale;

  const [defaults, referenceDefaults, counts] = await Promise.all([
    loadCatalog(locale, namespace),
    loadCatalog(reference, namespace),
    Promise.all(
      EDITABLE_NAMESPACES.map(async (name) => ({
        namespace: name,
        // i18n/request.ts already imports every catalog on each request, so the module
        // cache makes counting all 21 of them here effectively free.
        keyCount: Object.keys(await loadCatalog(locale, name)).length,
      })),
    ),
  ]);

  return (
    <main className="admin-page">
      <p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">{t("eyebrow")}</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1>
      <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p>
      <AdminUiTextPanel
        // Remounting on every selection change is deliberate: router.push to the same route
        // only swaps props, and without a key the previous namespace's drafts would survive.
        key={`${namespace}/${locale}/${reference}`}
        namespace={namespace}
        locale={locale}
        referenceLocale={reference}
        defaults={defaults}
        referenceDefaults={referenceDefaults}
        namespaces={counts}
      />
    </main>
  );
}
