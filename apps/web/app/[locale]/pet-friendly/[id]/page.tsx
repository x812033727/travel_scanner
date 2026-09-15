import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { PetDetails } from "@/components/community/pets";
import { CommunityPage, communityMetadata } from "@/components/community/page";
import { getPetPlace, metaDescription } from "@/lib/community/public.server";

type Props = { params: Promise<{ locale: Locale; id: string }> };

/** The kinds `placeKinds` carries. `PetPlace.kind` is a plain string, and asking next-intl
 *  for a key that does not exist throws -- during `generateMetadata`, which would turn one
 *  unrecognised record into a 500 for a page that renders perfectly well without the label. */
const PLACE_KINDS: readonly string[] = ["restaurant", "cafe", "shop", "lodging", "attraction"];

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, id } = await params;
  const [place, t] = await Promise.all([getPetPlace(locale, id), getTranslations("community")]);
  if (!place) return communityMetadata("pets");
  // The name is already the title, so the description says what kind of place it is and
  // where, which is what tells two similarly named cafés apart in a result list.
  const kind = PLACE_KINDS.includes(place.kind) ? t(`placeKinds.${place.kind}`) : "";
  return communityMetadata("pets", {
    index: true,
    name: place.names[locale] || place.name,
    description: metaDescription([kind, place.destination, place.address].filter(Boolean).join(" · ")),
  });
}

export default async function Page({ params }: Props) {
  const { locale, id } = await params;
  const place = await getPetPlace(locale, id);
  return <CommunityPage title="pets" heading={false} member={false}><PetDetails id={id} initial={place ?? undefined} /></CommunityPage>;
}
