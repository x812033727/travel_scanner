import { hasLocale } from "next-intl";
import { headers } from "next/headers";
import { notFound, redirect } from "next/navigation";
import OriginalLocaleLayout from "@/app/[locale]/layout";
import { Stay22Script } from "@/components/stay22-script";
import { getStay22ScriptConfig } from "@/lib/stay22-script.server";
import { stay22ScriptCopy } from "@/lib/stay22-script-copy";
import { routing } from "@/i18n/routing";
import { TEXT_SIZE_BOOTSTRAP_SCRIPT } from "@/lib/text-size";
import { THEME_BOOTSTRAP_SCRIPT } from "@/lib/theme";
import "@/app/globals.css";

export { generateMetadata, generateStaticParams } from "@/app/[locale]/layout";

export default async function PublicStay22Layout({ children, params }: {
  children: React.ReactNode; params: Promise<{ locale: string }>;
}) {
  const [{ locale }, config] = await Promise.all([params, getStay22ScriptConfig()]);
  if (!hasLocale(routing.locales, locale)) notFound();
  if (!config.enabled) return OriginalLocaleLayout({ children, params });
  const incoming = await headers();
  const requestPath = incoming.get("x-travel-pathname") || "";
  // Third-party code can read location.href even when no query is passed as props.
  // Remove all incoming conditions before this document loads the vendor script.
  if (requestPath.includes("?")) redirect(requestPath.split("?")[0]);
  const nonce = incoming.get("x-nonce") ?? undefined;
  const copy = stay22ScriptCopy(locale);
  // A different root from [locale]/layout.tsx: Next.js performs a complete document
  // navigation across this boundary, discarding the vendor runtime before private UI.
  // This is a DOM lifetime boundary, NOT a separate origin or cookie sandbox.
  return <html lang={locale} data-theme-preference="system" suppressHydrationWarning>
    <head><script nonce={nonce} dangerouslySetInnerHTML={{ __html: `${THEME_BOOTSTRAP_SCRIPT};${TEXT_SIZE_BOOTSTRAP_SCRIPT}` }} /></head>
    <body>
      <header className="mx-auto flex min-h-20 max-w-6xl flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] px-5 py-4">
        <a href={`/${locale}`} className="inline-flex min-h-11 items-center text-2xl font-bold tracking-tight">Mokaair</a>
        <nav aria-label={copy.publicPage} className="flex flex-wrap gap-2 text-sm">
          <a href={`/${locale}`} className="inline-flex min-h-11 items-center rounded-xl px-4">{copy.home}</a>
          <a href={`/${locale}/trips`} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-4">{copy.trips}</a>
        </nav>
      </header>
      {children}
      <footer className="mx-auto max-w-6xl space-y-3 border-t border-[var(--line)] px-5 py-7 text-xs leading-6 text-[var(--muted)]">
        <p>{copy.dataNotice}</p>
        <a href={`/${locale}/privacy`} className="inline-flex min-h-11 items-center underline">{copy.privacy}</a>
      </footer>
      <Stay22Script enabled lmaId={config.lma_id} locale={locale} />
    </body>
  </html>;
}
