import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { destinationsCopy } from "@/lib/destinations-copy";
import type { DestinationSummary, GuideEntry } from "@/lib/destinations.server";

/**
 * A city guide, rendered entirely on the server.
 *
 * The point of the page is that a crawler -- and a reader with JavaScript off -- sees the place
 * names, not a filter bar that fills in after hydration. Everything below comes from props the
 * page already awaited.
 */

function Facts({ destination, copy }: { destination: DestinationSummary; copy: ReturnType<typeof destinationsCopy> }) {
  const days = destination.recommendedDays;
  const facts = [
    days ? { label: copy.factsDays, value: `${days.min}–${days.max} ${copy.daysUnit}` } : null,
    destination.timezone ? { label: copy.factsTimezone, value: destination.timezone } : null,
    destination.currency ? { label: copy.factsCurrency, value: destination.currency } : null,
  ].filter((fact): fact is { label: string; value: string } => fact !== null);
  if (!facts.length) return null;
  return (
    <dl className="mt-6 grid gap-4 sm:grid-cols-3">
      {facts.map((fact) => (
        <div key={fact.label} className="rounded-2xl border border-[var(--line)] p-4">
          <dt className="text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">{fact.label}</dt>
          <dd className="mt-1 font-semibold">{fact.value}</dd>
        </div>
      ))}
    </dl>
  );
}

function EntryList({ title, entries, empty, unavailable, action }: { title: string; entries: GuideEntry[] | null; empty: string; unavailable: string; action: React.ReactNode }) {
  return (
    <section className="mt-10">
      <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      {entries?.length ? (
        <ul className="mt-4 grid gap-2 sm:grid-cols-2">
          {entries.map((entry) => (
            <li key={entry.id} className="rounded-2xl border border-[var(--line)] px-4 py-3">
              <span className="font-semibold">{entry.name}</span>
              {entry.detail ? <span className="ml-2 text-sm text-[var(--muted)]">{entry.detail}</span> : null}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 leading-7 text-[var(--muted)]">{entries === null ? unavailable : empty}</p>
      )}
      <p className="mt-4">{action}</p>
    </section>
  );
}

export function DestinationGuide({
  locale,
  destination,
  places,
  hotspotsEnabled,
  merchants,
  related,
}: {
  locale: Locale;
  destination: DestinationSummary;
  places: GuideEntry[] | null;
  hotspotsEnabled: boolean;
  merchants: GuideEntry[] | null;
  related: DestinationSummary[];
}) {
  const copy = destinationsCopy(locale);
  const link = "font-semibold text-[var(--teal)] underline";
  // The original-script name is worth showing when it is not already the heading: it is what a
  // sign, a ticket machine or a taxi driver will use.
  const original = destination.localName && destination.localName !== destination.city ? destination.localName : null;
  return (
    <main className="mx-auto max-w-4xl px-5 py-10 md:px-8">
      <p className="text-xs font-bold uppercase tracking-widest text-[var(--teal)]">{copy.guideEyebrow}</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">{destination.city}</h1>
      <p className="mt-2 text-[var(--muted)]">
        {destination.country}
        {original ? ` · ${original}` : ""}
      </p>
      {destination.reason ? <p className="mt-5 max-w-2xl text-lg leading-8">{destination.reason}</p> : null}
      <Facts destination={destination} copy={copy} />

      {destination.areas.length ? (
        <section className="mt-10">
          <h2 className="text-2xl font-bold tracking-tight">{copy.areasTitle}</h2>
          <ul className="mt-4 flex flex-wrap gap-2">
            {destination.areas.map((area) => (
              <li key={area} className="rounded-full border border-[var(--line)] px-4 py-2 text-sm font-semibold">
                {area}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {hotspotsEnabled ? <EntryList
        title={copy.seeTitle}
        entries={places}
        empty={copy.emptyPlaces}
        unavailable={copy.unavailablePlaces}
        action={<Link className={link} href={`/hotspots?destination_id=${destination.id}`}>{copy.browsePlaces}</Link>}
      /> : null}
      <EntryList
        title={copy.eatTitle}
        entries={merchants}
        empty={copy.emptyFood}
        unavailable={copy.unavailableFood}
        action={<Link className={link} href={`/foods?destination_id=${encodeURIComponent(destination.id)}`}>{copy.browseFood}</Link>}
      />

      {/* The section publishes per locale, so a city may have articles in one language and
          none in another. These are links into a filtered list rather than a rendered count:
          the list answers honestly when it is empty, and this component stays synchronous --
          the page test renders it without awaiting anything. */}
      <section className="mt-10">
        <h2 className="text-2xl font-bold tracking-tight">{copy.guidesTitle}</h2>
        <ul className="mt-4 space-y-2">
          <li><Link className={link} href={`/guides/intel?destination=${encodeURIComponent(destination.id)}`}>{copy.guidesIntel}</Link></li>
          <li><Link className={link} href={`/guides/howto?destination=${encodeURIComponent(destination.id)}`}>{copy.guidesHowto}</Link></li>
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="text-2xl font-bold tracking-tight">{copy.planTitle}</h2>
        <ul className="mt-4 space-y-2">
          <li><Link className={link} href="/search/new">{copy.planTrip}</Link></li>
          <li><Link className={link} href={`/destinations/${destination.id}/services`}>{copy.stays}</Link></li>
        </ul>
        {/* Reviewed partner entrances for this city. A client island inside a server page: it
            renders nothing until the API says a surface is on and an offer is verified. */}
        <div className="mt-6">
          <DestinationAffiliateOptions destinationId={destination.id} destinationLabel={destination.city} contextual placement="city" />
        </div>
      </section>

      {related.length ? (
        <section className="mt-10">
          <h2 className="text-2xl font-bold tracking-tight">{copy.nearbyTitle}</h2>
          <ul className="mt-4 flex flex-wrap gap-2">
            {related.map((item) => (
              <li key={item.id}>
                <Link className="inline-block rounded-full border border-[var(--line)] px-4 py-2 text-sm font-semibold" href={`/destinations/${item.id}`}>
                  {item.city}
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <p className="mt-10">
        <Link className={link} href="/destinations">{copy.breadcrumb}</Link>
      </p>
    </main>
  );
}
