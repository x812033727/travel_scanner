import { notFound } from "next/navigation";
import OriginalDestinationServices, { type DestinationServicesParams } from "@/components/travel-services/destination-services-page";
import { CITIES, PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { Stay22PublicHotels } from "@/components/travel-services/stay22-public-hotels";
import { getStay22ScriptConfig } from "@/lib/stay22-script.server";
import { stay22ScriptCopy } from "@/lib/stay22-script-copy";

export { generateMetadata } from "@/components/travel-services/destination-services-page";

export default async function DestinationServices(props: {
  params: Promise<DestinationServicesParams>;
  searchParams: Promise<Record<string, string | undefined>>;
}) {
  const config = await getStay22ScriptConfig();
  if (!config.enabled) return OriginalDestinationServices(props);
  const { locale, destinationId } = await props.params;
  if (!new Set<string>([...CITIES, ...PUBLIC_DESTINATIONS]).has(destinationId)) notFound();
  const copy = stay22ScriptCopy(locale);
  // Search parameters deliberately do not flow into the third-party document.
  // It only shows the public destination; dates and occupancy are set externally.
  return <main className="mx-auto min-h-[65dvh] max-w-6xl space-y-7 px-5 py-9 sm:py-12">
    <div><p className="text-xs font-bold uppercase tracking-widest text-[var(--teal)]">{copy.publicPage}</p><h1 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">{copy.title}</h1><p className="mt-4 max-w-2xl leading-7 text-[var(--muted)]">{copy.subtitle}</p></div>
    <div className="space-y-3 rounded-3xl border border-[var(--line)] bg-[var(--teal-soft)] p-5 text-sm leading-7"><p>{copy.disclosure}</p><p>{copy.dateNotice}</p></div>
    <Stay22PublicHotels key={destinationId} destinationId={destinationId} locale={locale} />
  </main>;
}
