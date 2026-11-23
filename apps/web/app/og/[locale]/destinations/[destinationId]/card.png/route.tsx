import { NextResponse } from "next/server";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales, type Locale } from "@/i18n/routing";
import { destinationsCopy } from "@/lib/destinations-copy";
import { getDestination } from "@/lib/destinations.server";
import { renderEditorialOgCard } from "@/lib/editorial-og-card";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Dynamic 1200x630 editorial Open Graph / Google Discover card for a city destination guide.
 * Reads the verified city catalogue rather than query parameters so arbitrary text cannot be
 * injected into an image hosted on the site's origin.
 */
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ locale: string; destinationId: string }> },
): Promise<Response> {
  const { locale, destinationId } = await params;
  if (
    !(locales as readonly string[]).includes(locale)
    || !(PUBLIC_DESTINATIONS as readonly string[]).includes(destinationId)
  ) {
    return new NextResponse("not found", { status: 404 });
  }

  const typedLocale = locale as Locale;
  const destination = await getDestination(typedLocale, destinationId);
  if (!destination) return new NextResponse("not found", { status: 404 });

  const copy = destinationsCopy(typedLocale);
  const title = copy.guideMetaTitle.replace("{city}", destination.city).replace(/\s*\|\s*Mokaair$/, "");
  const meta = [destination.country, destination.localName && destination.localName !== destination.city ? destination.localName : null]
    .filter(Boolean)
    .join(" · ");

  return renderEditorialOgCard({
    locale: typedLocale,
    title,
    description: destination.reason || copy.indexIntro,
    badge: copy.guideEyebrow,
    meta,
  });
}
