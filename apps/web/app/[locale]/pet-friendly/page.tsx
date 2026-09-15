import type { Metadata } from "next";
import { getLocale, getTranslations } from "next-intl/server";
import { PetDirectory } from "@/components/community/pets";
import { CommunityPage } from "@/components/community/page";
import { getPetPlaces } from "@/lib/community/public.server";

export async function generateMetadata(): Promise<Metadata> {
  const locale = await getLocale();
  const [t, places] = await Promise.all([getTranslations("metadata"), getPetPlaces(locale)]);
  return {
    title: t("petFriendlyTitle"),
    description: t("petFriendlyDescription"),
    // Indexable only once the directory itself is in the HTML. With the community switch off,
    // or the read failed, what the server sends is the gate and a heading -- a soft 404 to
    // hand a crawler, and the reason this route carried a blanket `noindex` until now.
    robots: { index: Boolean(places?.items.length), follow: true },
  };
}

export default async function Page() {
  const places = await getPetPlaces(await getLocale());
  return <CommunityPage title="pets"><PetDirectory initial={places ?? undefined} /></CommunityPage>;
}
