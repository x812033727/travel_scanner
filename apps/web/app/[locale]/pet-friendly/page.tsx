import { getTranslations } from "next-intl/server";
import { PetDirectory } from "@/components/community/pets";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("petFriendlyTitle"), description: t("petFriendlyDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="pets"><PetDirectory /></CommunityPage>; }
